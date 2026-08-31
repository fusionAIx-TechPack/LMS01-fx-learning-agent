from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .domain import (
    AvailableReferenceVideo,
    AvailableSource,
    CourseBrief,
    CourseDefinitionError,
    humanize_minutes,
    slugify,
)
from .source_validation import (
    validate_entered_url,
    validate_reference_videos,
    validate_selected_sources,
)


# Every generated Course has the same five-activity shape. See
# docs/adr/0004-fixed-four-activity-course-structure.md.
OVERVIEW_ACTIVITY_NAME = "Course overview"
RESOURCES_ACTIVITY_FALLBACK_NAME = "Course resources"
VIDEOS_ACTIVITY_NAME = "Watch reference videos"
ASSIGNMENT_ACTIVITY_NAME = "Submit Course Certification"
DISCUSSION_ACTIVITY_NAME = "Discussion Forum"

DISCUSSION_INTRODUCTION = (
    "Ask questions and share what you learned with other learners taking this "
    "course. Post at least once, then mark this activity done."
)

OVERVIEW_INSTRUCTION = (
    "One must complete all contents to finish the course. On completion, candidates "
    "are requested to upload your badge, certification, or screenshot of completion "
    "in the assignment section."
)
ASSIGNMENT_INTRODUCTION = (
    "Upload proof that you completed this course: your certificate, your digital "
    "badge, or a screenshot of a completion screen. Accepted files are PDF or "
    "image. Submitting a file marks this activity complete."
)
VIDEOS_INTRODUCTION_WITH_ITEMS = (
    "Reference videos from public platforms that reinforce the course material. "
    "Watch the ones you find useful, then mark this activity done."
)
VIDEOS_INTRODUCTION_EMPTY = (
    "No additional reference videos were selected for this course. Mark this "
    "activity done to continue."
)

ASSIGNMENT_MAX_FILES = 3
ASSIGNMENT_FILE_TYPES = ".pdf,.png,.jpg,.jpeg,.webp"


def _source_value(available: AvailableSource, checked_at: str) -> dict[str, Any]:
    value = available.source.as_brief_value()
    value["availability"] = {"status": available.http_status, "checked_at": checked_at}
    return value


def _video_value(available: AvailableReferenceVideo, checked_at: str) -> dict[str, Any]:
    value = available.video.as_brief_value()
    value["availability"] = {"status": available.http_status, "checked_at": checked_at}
    return value


def _video_item(available: AvailableReferenceVideo) -> dict[str, Any]:
    video = available.video
    item = {"title": video.title, "url": video.url, "publisher": video.publisher, "note": video.note}
    if video.duration_minutes is not None:
        item["duration_minutes"] = video.duration_minutes
    return item


def generate_course_definition(brief: CourseBrief) -> dict[str, Any]:
    selected = validate_selected_sources(brief)
    validate_entered_url(brief)
    videos = validate_reference_videos(brief)
    checked_at = datetime.now(UTC).isoformat()

    outcome = brief.intended_learning_outcome.rstrip(". ") + "."
    introduction = brief.course_description or (
        f"This Course guides {brief.audience} toward: {outcome}"
    )
    total_minutes = brief.learning_time_minutes
    resources_name = brief.topic.strip() or RESOURCES_ACTIVITY_FALLBACK_NAME
    # Activity 2 is a bare link that opens the URL the Course Requester entered,
    # in a new window. The selected Sources are recorded in brief.sources and the
    # dossier for provenance; they are not surfaced to the learner.
    entered_url = brief.source_url or selected[0].source.url
    section_introduction = f"{introduction} {OVERVIEW_INSTRUCTION}"

    definition: dict[str, Any] = {
        "identity": {
            "fullname": brief.topic,
            "shortname": slugify(f"{brief.topic}-{brief.entry_level}")[:100].rstrip("-"),
            "summary": introduction,
        },
        "settings": {"format": "topics", "visible": True, "completion_tracking": True},
        "brief": {
            "topic": brief.topic,
            "audience": brief.audience,
            "entry_level": brief.entry_level,
            "language": brief.language,
            "intended_learning_outcome": brief.intended_learning_outcome,
            "learning_time_minutes": total_minutes,
            "sources": [_source_value(item, checked_at) for item in selected],
            "reference_videos": [_video_value(item, checked_at) for item in videos],
            "source_url": entered_url,
        },
        "structure": {
            "section_name": resources_name,
            "section_introduction": section_introduction,
            "activities": {
                "overview": {
                    "name": OVERVIEW_ACTIVITY_NAME,
                    "module_count": len(selected),
                    "estimated_time_minutes": total_minutes,
                    "estimated_time_label": humanize_minutes(total_minutes),
                    "outcome": outcome,
                    "instruction": OVERVIEW_INSTRUCTION,
                },
                "resources": {
                    "name": resources_name,
                    "primary_url": entered_url,
                },
                "videos": {
                    "name": VIDEOS_ACTIVITY_NAME,
                    "introduction": (
                        VIDEOS_INTRODUCTION_WITH_ITEMS if videos else VIDEOS_INTRODUCTION_EMPTY
                    ),
                    "items": [_video_item(item) for item in videos],
                },
                "assignment": {
                    "name": ASSIGNMENT_ACTIVITY_NAME,
                    "introduction": ASSIGNMENT_INTRODUCTION,
                    "max_files": ASSIGNMENT_MAX_FILES,
                    "file_types": ASSIGNMENT_FILE_TYPES,
                },
                "discussion": {
                    "name": DISCUSSION_ACTIVITY_NAME,
                    "introduction": DISCUSSION_INTRODUCTION,
                },
            },
        },
    }
    if brief.course_description is not None:
        definition["brief"]["course_description"] = brief.course_description
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
