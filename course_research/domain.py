from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


class CourseDefinitionError(Exception):
    """A requester-facing failure that must not produce a Course Definition."""


@dataclass(frozen=True)
class SelectedSource:
    title: str
    activity_name: str
    url: str
    publisher: str
    provider_item_id: str
    source_type: str
    language: str
    activity_duration_minutes: int
    duration_minutes: int
    access_basis: str
    access_evidence_url: str
    activity_purpose: str | None = None
    activity_instructions: str | None = None

    def as_brief_value(self) -> dict[str, Any]:
        value = {
            "title": self.title,
            "activity_name": self.activity_name,
            "url": self.url,
            "publisher": self.publisher,
            "provider_item_id": self.provider_item_id,
            "source_type": self.source_type,
            "language": self.language,
            "activity_duration_minutes": self.activity_duration_minutes,
            "duration_minutes": self.duration_minutes,
            "access": {
                "free": True,
                "basis": self.access_basis,
                "evidence_url": self.access_evidence_url,
            },
        }
        if self.activity_purpose is not None:
            value["activity_purpose"] = self.activity_purpose
        if self.activity_instructions is not None:
            value["activity_instructions"] = self.activity_instructions
        return value


@dataclass(frozen=True)
class AvailableSource:
    source: SelectedSource
    http_status: int


@dataclass(frozen=True)
class LearningPathModule:
    name: str
    introduction: str
    source_provider_item_ids: tuple[str, ...]


@dataclass(frozen=True)
class CourseBrief:
    topic: str
    audience: str
    entry_level: str
    language: str
    intended_learning_outcome: str
    learning_time_minutes: int
    sources: tuple[SelectedSource, ...]
    course_description: str | None = None
    learning_path: tuple[LearningPathModule, ...] = ()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "course"


def locale_for_language(language: str) -> str:
    if language != "en-US":
        raise CourseDefinitionError("Course Brief and Sources must use en-US.")
    return language


def level_for_entry(entry_level: str) -> str:
    normalized = entry_level.casefold().strip()
    aliases = {
        "początkujący": "beginner",
        "podstawowy": "beginner",
        "średniozaawansowany": "intermediate",
        "zaawansowany": "advanced",
    }
    level = aliases.get(normalized, normalized)
    if level not in {"beginner", "intermediate", "advanced"}:
        raise CourseDefinitionError(
            "Course Brief entry_level must be beginner, intermediate, or advanced."
        )
    return level
