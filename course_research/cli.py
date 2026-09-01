from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .domain import (
    CourseBrief,
    CourseDefinitionError,
    ReferenceVideo,
    SelectedSource,
    level_for_entry,
    locale_for_language,
)
from .generator import write_course_definition


MAX_NAVIGATION_NAME_LENGTH = 40


def _required_text(document: dict[str, Any], field: str) -> str:
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
        raise CourseDefinitionError(f"Course Brief requires non-empty {field}.")
    return value.strip()


def _optional_text(document: dict[str, Any], field: str) -> str | None:
    value = document.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise CourseDefinitionError(f"Course Brief {field} must be non-empty when provided.")
    return value.strip()


def _http_url(document: dict[str, Any], field: str, context: str) -> str:
    value = document.get(field)
    if not isinstance(value, str) or urlparse(value).scheme not in {"http", "https"}:
        raise CourseDefinitionError(f"{context} requires valid HTTP {field}.")
    return value.strip()


def _positive_int(document: dict[str, Any], field: str, context: str) -> int:
    value = document.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CourseDefinitionError(f"{context} requires positive integer {field}.")
    return value


def _selected_sources(document: dict[str, Any]) -> tuple[SelectedSource, ...]:
    values = document.get("sources")
    if not isinstance(values, list) or not values:
        raise CourseDefinitionError("Course Brief requires at least one human-selected Source.")
    sources = []
    for index, value in enumerate(values):
        context = f"Course Brief Source {index}"
        if not isinstance(value, dict):
            raise CourseDefinitionError(f"{context} must be a JSON object.")
        duration = _positive_int(value, "duration_minutes", context)
        activity_duration = _positive_int(value, "activity_duration_minutes", context)
        if activity_duration < duration:
            raise CourseDefinitionError(
                f"{context} activity_duration_minutes must be at least Source duration_minutes."
            )
        source_type = _required_text(value, "source_type")
        if source_type not in {"article", "blog", "video", "course"}:
            raise CourseDefinitionError(
                f"{context} source_type must be article, blog, video, or course."
            )
        access = value.get("access")
        if not isinstance(access, dict) or access.get("free") is not True:
            raise CourseDefinitionError(f"{context} must record free access evidence.")
        source = SelectedSource(
            title=_required_text(value, "title"),
            activity_name=_required_text(value, "activity_name"),
            url=_http_url(value, "url", context),
            publisher=_required_text(value, "publisher"),
            provider_item_id=_required_text(value, "provider_item_id"),
            source_type=source_type,
            language=_required_text(value, "language"),
            activity_duration_minutes=activity_duration,
            duration_minutes=duration,
            access_basis=_required_text(access, "basis"),
            access_evidence_url=_http_url(access, "evidence_url", f"{context} access"),
            activity_purpose=_optional_text(value, "activity_purpose"),
        )
        if len(source.activity_name) > MAX_NAVIGATION_NAME_LENGTH:
            raise CourseDefinitionError(
                f"{context} activity_name must be at most {MAX_NAVIGATION_NAME_LENGTH} characters for Moodle navigation."
            )
        sources.append(source)
    provider_ids = [source.provider_item_id for source in sources]
    if len(provider_ids) != len(set(provider_ids)):
        raise CourseDefinitionError("Course Brief Source provider_item_id values must be unique.")
    return tuple(sources)


def _reference_videos(document: dict[str, Any]) -> tuple[ReferenceVideo, ...]:
    values = document.get("reference_videos")
    if values is None:
        return ()
    if not isinstance(values, list):
        raise CourseDefinitionError("Course Brief reference_videos must be a JSON array.")
    videos = []
    for index, value in enumerate(values):
        context = f"Course Brief reference video {index}"
        if not isinstance(value, dict):
            raise CourseDefinitionError(f"{context} must be a JSON object.")
        duration = value.get("duration_minutes")
        if duration is not None and (
            isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0
        ):
            raise CourseDefinitionError(f"{context} duration_minutes must be a positive integer when provided.")
        videos.append(
            ReferenceVideo(
                title=_required_text(value, "title"),
                url=_http_url(value, "url", context),
                publisher=_required_text(value, "publisher"),
                note=_required_text(value, "note"),
                duration_minutes=duration,
            )
        )
    urls = [video.url for video in videos]
    if len(urls) != len(set(urls)):
        raise CourseDefinitionError("Course Brief reference video URLs must be unique.")
    return tuple(videos)


def load_course_brief(path: Path) -> CourseBrief:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CourseDefinitionError(f"Course Brief is missing or unreadable: {path}") from error
    except json.JSONDecodeError as error:
        raise CourseDefinitionError(f"Course Brief is not valid JSON: {error.msg}") from error
    if not isinstance(document, dict):
        raise CourseDefinitionError("Course Brief must be a JSON object.")

    minutes = document.get("learning_time_minutes")
    if isinstance(minutes, bool) or not isinstance(minutes, int) or minutes <= 0:
        raise CourseDefinitionError("Course Brief requires positive integer learning_time_minutes.")

    topic = _required_text(document, "topic")
    audience = _required_text(document, "audience")
    entry_level = _required_text(document, "entry_level")
    language = _required_text(document, "language")
    intended_learning_outcome = _required_text(document, "intended_learning_outcome")
    sources = _selected_sources(document)
    reference_videos = _reference_videos(document)
    source_url = document.get("source_url")
    if source_url is not None:
        source_url = _http_url(document, "source_url", "Course Brief")
    brief = CourseBrief(
        topic=topic,
        audience=audience,
        entry_level=entry_level,
        language=language,
        intended_learning_outcome=intended_learning_outcome,
        learning_time_minutes=minutes,
        sources=sources,
        course_description=_optional_text(document, "course_description"),
        reference_videos=reference_videos,
        source_url=source_url,
    )
    locale_for_language(brief.language)
    for source in brief.sources:
        locale_for_language(source.language)
    level_for_entry(brief.entry_level)
    return brief


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="course-definition")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser(
        "build", help="validate selected Sources and build a Course Definition"
    )
    build.add_argument("--brief", required=True, type=Path)
    build.add_argument("--output", required=True, type=Path)
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        brief = load_course_brief(args.brief.resolve())
        output = args.output.resolve()
        write_course_definition(brief, output)
        print(f"Course Definition generated and ready for review: {output}")
        return 0
    except CourseDefinitionError as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
