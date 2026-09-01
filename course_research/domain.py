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
        return value


@dataclass(frozen=True)
class ReferenceVideo:
    title: str
    url: str
    publisher: str
    note: str
    duration_minutes: int | None = None

    def as_brief_value(self) -> dict[str, Any]:
        value = {
            "title": self.title,
            "url": self.url,
            "publisher": self.publisher,
            "note": self.note,
        }
        if self.duration_minutes is not None:
            value["duration_minutes"] = self.duration_minutes
        return value


@dataclass(frozen=True)
class AvailableSource:
    source: SelectedSource
    http_status: int


@dataclass(frozen=True)
class AvailableReferenceVideo:
    video: ReferenceVideo
    http_status: int


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
    reference_videos: tuple[ReferenceVideo, ...] = ()
    # The URL the Course Requester entered after `/create-course`. The resource
    # list activity opens this URL; its sub-topics are the selected Sources.
    # Falls back to the first Source URL when absent.
    source_url: str | None = None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "course"


def humanize_minutes(total: int) -> str:
    hours, minutes = divmod(total, 60)
    parts: list[str] = []
    if hours:
        parts.append(f"{hours} hour" + ("s" if hours != 1 else ""))
    if minutes:
        parts.append(f"{minutes} minute" + ("s" if minutes != 1 else ""))
    return " ".join(parts) or "0 minutes"


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
