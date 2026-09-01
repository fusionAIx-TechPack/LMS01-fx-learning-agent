from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .domain import AvailableSource, CourseBrief, CourseDefinitionError, SelectedSource, slugify
from .source_validation import validate_selected_sources


MAX_NAVIGATION_NAME_LENGTH = 40


def _phase(source: SelectedSource, brief: CourseBrief) -> str:
    title = source.title.casefold()
    foundations = ("fundament", "introduction", "overview", "get started", "choose", "plan")
    applications = ("build", "create", "configure", "publish", "deploy")
    if any(marker in title for marker in foundations):
        return "foundation"
    if any(marker in title for marker in applications):
        return "application"
    outcome_words = {word for word in brief.intended_learning_outcome.casefold().split() if len(word) > 3}
    return "application" if any(word in title for word in outcome_words) else "foundation"


def _activity(available: AvailableSource, brief: CourseBrief, checked_at: str, phase: str) -> dict[str, Any]:
    source = available.source
    generated_purpose = (
        f"Build the foundation {brief.audience} need using the Source: {source.title}."
        if phase == "foundation"
        else f"Apply the Source {source.title} to achieve: {brief.intended_learning_outcome}."
    )
    generated_instructions = (
        f'Open the Source "{source.title}", work through it, and record one principle to use in the following activities.'
        if phase == "foundation"
        else f'Open the Source "{source.title}", follow its steps, and record one decision or result tied to the Course outcome.'
    )
    return {
        "name": source.activity_name,
        "purpose": source.activity_purpose or generated_purpose,
        "instructions": source.activity_instructions or generated_instructions,
        "duration_minutes": source.activity_duration_minutes,
        "source": {
            "title": source.title,
            "url": source.url,
            "publisher": source.publisher,
            "provider_item_id": source.provider_item_id,
            "source_type": source.source_type,
            "language": source.language,
            "duration_minutes": source.duration_minutes,
            "availability": {"status": available.http_status, "checked_at": checked_at},
            "access": {
                "free": True,
                "basis": source.access_basis,
                "evidence_url": source.access_evidence_url,
            },
        },
    }


def _modules(selected: list[AvailableSource], brief: CourseBrief, checked_at: str) -> list[dict[str, Any]]:
    if brief.learning_path:
        by_id = {item.source.provider_item_id: item for item in selected}
        return [
            {
                "name": module.name,
                "introduction": module.introduction,
                "activities": [
                    _activity(by_id[source_id], brief, checked_at, "application")
                    for source_id in module.source_provider_item_ids
                ],
            }
            for module in brief.learning_path
        ]

    grouped: dict[str, list[AvailableSource]] = {"foundation": [], "application": []}
    for item in selected:
        grouped[_phase(item.source, brief)].append(item)
    if len(selected) > 1:
        if not grouped["foundation"]:
            grouped["foundation"].append(grouped["application"].pop(0))
        if not grouped["application"]:
            grouped["application"].append(grouped["foundation"].pop())

    labels = {
        "foundation": ("Foundations", f"Build shared foundations for {brief.audience}."),
        "application": ("Practice", f"Move from foundations to: {brief.intended_learning_outcome}."),
    }
    modules = []
    for phase in ("foundation", "application"):
        if not grouped[phase]:
            continue
        name, introduction = labels[phase]
        modules.append({
            "name": name,
            "introduction": introduction,
            "activities": [_activity(source, brief, checked_at, phase) for source in grouped[phase]],
        })
    return modules


def validate_course_definition(definition: dict[str, Any]) -> None:
    required_text = (
        definition.get("identity", {}).get("fullname"),
        definition.get("identity", {}).get("shortname"),
        definition.get("identity", {}).get("summary"),
        definition.get("general", {}).get("name"),
        definition.get("general", {}).get("introduction"),
    )
    if not all(isinstance(value, str) and value.strip() for value in required_text):
        raise CourseDefinitionError("Generated Course Definition is missing required identity or general text.")
    if definition.get("settings") != {"format": "topics", "visible": False, "completion_tracking": True}:
        raise CourseDefinitionError("Generated Course Definition has invalid Moodle settings.")
    if definition.get("brief", {}).get("language") != "en-US":
        raise CourseDefinitionError("Course Definition brief.language must be en-US.")
    modules = definition.get("modules")
    if not isinstance(modules, list) or not modules:
        raise CourseDefinitionError("Generated Course Definition requires at least one module.")
    purposes: set[str] = set()
    instructions: set[str] = set()
    for module in modules:
        if len(module.get("name", "")) > MAX_NAVIGATION_NAME_LENGTH:
            raise CourseDefinitionError(
                f"Generated Course Definition module name exceeds {MAX_NAVIGATION_NAME_LENGTH} characters."
            )
        if not isinstance(module.get("activities"), list) or not module["activities"]:
            raise CourseDefinitionError("Generated Course Definition module requires Learning Activities.")
        for activity in module["activities"]:
            source = activity.get("source", {})
            if not all(isinstance(activity.get(field), str) and activity[field].strip() for field in ("name", "purpose", "instructions")):
                raise CourseDefinitionError("Generated Learning Activity is missing required text.")
            if activity["purpose"] in purposes:
                raise CourseDefinitionError("Source Activity purpose must be unique within the Course.")
            purposes.add(activity["purpose"])
            if activity["instructions"] in instructions:
                raise CourseDefinitionError("Source Activity instructions must be unique within the Course.")
            instructions.add(activity["instructions"])
            if len(activity["name"]) > MAX_NAVIGATION_NAME_LENGTH:
                raise CourseDefinitionError(
                    f"Generated Learning Activity name exceeds {MAX_NAVIGATION_NAME_LENGTH} characters."
                )
            duration = activity.get("duration_minutes")
            if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
                raise CourseDefinitionError("Generated Learning Activity has invalid duration.")
            url = source.get("url")
            if not isinstance(source.get("title"), str) or not isinstance(url, str) or urlparse(url).scheme not in {"http", "https"}:
                raise CourseDefinitionError("Generated Learning Activity has an invalid Source.")
            if not all(
                isinstance(source.get(field), str) and source[field].strip()
                for field in ("publisher", "provider_item_id", "source_type", "language")
            ):
                raise CourseDefinitionError("Generated Learning Activity is missing Source provenance.")
            if source["source_type"] not in {"article", "blog", "video", "course"}:
                raise CourseDefinitionError("Generated Learning Activity has unsupported Source type.")
            if source["language"] != "en-US":
                raise CourseDefinitionError("Generated Source Activity Source language must be en-US.")
            if not isinstance(source.get("duration_minutes"), int) or source["duration_minutes"] <= 0:
                raise CourseDefinitionError("Generated Learning Activity has invalid Source duration.")
            if duration < source["duration_minutes"]:
                raise CourseDefinitionError("Generated Learning Activity duration is shorter than its Source duration.")
            access = source.get("access", {})
            if access.get("free") is not True or not isinstance(access.get("basis"), str):
                raise CourseDefinitionError("Generated Learning Activity is missing free Source access evidence.")
            availability = source.get("availability", {})
            if not isinstance(availability.get("status"), int) or not 200 <= availability["status"] < 400:
                raise CourseDefinitionError("Generated Learning Activity is missing Source availability evidence.")


def generate_course_definition(brief: CourseBrief) -> dict[str, Any]:
    selected = validate_selected_sources(brief)
    checked_at = datetime.now(UTC).isoformat()
    general_name = "Start here"
    outcome = brief.intended_learning_outcome.rstrip(". ") + "."
    introduction = brief.course_description or f"This Course guides {brief.audience} toward: {outcome}"
    definition = {
        "identity": {
            "fullname": brief.topic,
            "shortname": slugify(f"{brief.topic}-{brief.entry_level}")[:100].rstrip("-"),
            "summary": introduction,
        },
        "settings": {"format": "topics", "visible": False, "completion_tracking": True},
        "brief": {
            "topic": brief.topic,
            "audience": brief.audience,
            "entry_level": brief.entry_level,
            "language": brief.language,
            "intended_learning_outcome": brief.intended_learning_outcome,
            "learning_time_minutes": brief.learning_time_minutes,
            "sources": [source.as_brief_value() for source in brief.sources],
        },
        "general": {"name": general_name, "introduction": introduction},
        "modules": _modules(selected, brief, checked_at),
    }
    if brief.course_description is not None:
        definition["brief"]["course_description"] = brief.course_description
    if brief.learning_path:
        definition["brief"]["learning_path"] = [
            {
                "name": module.name,
                "introduction": module.introduction,
                "source_provider_item_ids": list(module.source_provider_item_ids),
            }
            for module in brief.learning_path
        ]
    validate_course_definition(definition)
    return definition


def write_course_definition(brief: CourseBrief, output: Path) -> None:
    if output.exists():
        raise CourseDefinitionError(f"Output already exists; refusing to overwrite it: {output}")
    definition = generate_course_definition(brief)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, delete=False) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(definition, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
        temporary_path.replace(output)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
