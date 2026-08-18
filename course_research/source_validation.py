from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .domain import AvailableSource, CourseBrief, CourseDefinitionError


REQUEST_TIMEOUT_SECONDS = 20


def _availability(url: str) -> int | None:
    headers = {"User-Agent": "fxlearning-source-validation/1.0"}
    for method in ("HEAD", "GET"):
        request = Request(url, headers=headers, method=method)
        if method == "GET":
            request.add_header("Range", "bytes=0-0")
        try:
            with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                return response.status if 200 <= response.status < 400 else None
        except HTTPError as error:
            if method == "HEAD" and error.code in {405, 501}:
                continue
            return None
        except (URLError, TimeoutError, ValueError):
            return None
    return None


def validate_selected_sources(brief: CourseBrief) -> list[AvailableSource]:
    total_minutes = sum(source.activity_duration_minutes for source in brief.sources)
    if total_minutes > brief.learning_time_minutes:
        raise CourseDefinitionError(
            "Human-selected Source Activities exceed the Course Brief learning-time budget."
        )
    available = []
    for source in brief.sources:
        status = _availability(source.url)
        if status is None:
            raise CourseDefinitionError(
                f"Human-selected Source is unavailable: {source.title} ({source.url})."
            )
        available.append(AvailableSource(source=source, http_status=status))
    return available
