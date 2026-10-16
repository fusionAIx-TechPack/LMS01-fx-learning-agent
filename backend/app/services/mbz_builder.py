"""Builds a Moodle 5.x course backup (.mbz) from a Course Definition without running Moodle.

The template under backend/app/mbz_template/ is a real package produced by the
Moodle packaging engine (bin/course-package -> moodle-cli/generate.php + backup.php)
for the fixed five-activity course shape (docs/adr/0004). Every generated Course has
identical structure and internal ids; only the course-specific text differs. This
module swaps exactly those fields, rendering activity HTML the same way
moodle-cli/activity_content.php does, and leaves everything else byte-for-byte.
"""
from __future__ import annotations

import gzip
import io
import re
import secrets
import tarfile
import time
from pathlib import Path
from typing import Any, Callable

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "mbz_template" / "five-activity-course.mbz"

OVERVIEW_PAGE = "activities/page_1/page.xml"
RESOURCES_URL = "activities/url_2/url.xml"
VIDEOS_PAGE = "activities/page_3/page.xml"
COURSE_XML = "course/course.xml"
SECTION_XML = "sections/section_1/section.xml"
BACKUP_XML = "moodle_backup.xml"
ARCHIVE_INDEX = ".ARCHIVE_INDEX"

TIMESTAMP_TAGS = ("timemodified", "timecreated", "added", "backup_date")


class MbzBuildError(Exception):
    """The Course Definition cannot be packaged with the five-activity template."""


# ---- HTML rendering: mirrors moodle-cli/activity_content.php and course_definition.php ----

def _php_esc(value: str) -> str:
    """htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')."""
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_overview_page(overview: dict[str, Any]) -> str:
    return (
        '<div class="fx-course-overview">'
        f"<p>{_php_esc(overview['outcome'])}</p>"
        "<ul>"
        f"<li><strong>Number of Modules:</strong> {int(overview['module_count'])}</li>"
        f"<li><strong>Estimated Time:</strong> {_php_esc(overview['estimated_time_label'])}</li>"
        "</ul>"
        f"<p><strong>Instruction:</strong> {_php_esc(overview['instruction'])}</p>"
        "</div>"
    )


def render_videos_page(videos: dict[str, Any]) -> str:
    out = f'<div class="fx-reference-videos"><p>{_php_esc(videos["introduction"])}</p>'
    items = videos.get("items") or []
    if items:
        out += "<ul>"
        for item in items:
            line = (
                f'<a class="nomediaplugin" href="{_php_esc(item["url"])}" target="_blank" '
                f'rel="noopener noreferrer">{_php_esc(item["title"])}</a>'
            )
            if item.get("note"):
                line += f" &mdash; {_php_esc(item['note'])}"
            line += f" <em>({_php_esc(str(item['publisher']))})</em>"
            out += f"<li>{line}</li>"
        out += "</ul>"
    return out + "</div>"


def course_html(value: str) -> str:
    return f"<p>{_php_esc(value)}</p>"


# ---- XML editing helpers ----

def _xml_text(value: str) -> str:
    """Moodle's backup XML writer escapes only &, < and >."""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _set_element(xml: str, tag: str, value: str, *, count: int = 1) -> str:
    pattern = re.compile(rf"<{tag}>.*?</{tag}>", re.DOTALL)
    found = len(pattern.findall(xml))
    if found != count:
        raise MbzBuildError(f"Template has {found} <{tag}> elements, expected {count}")
    return pattern.sub(lambda _: f"<{tag}>{_xml_text(value)}</{tag}>", xml)


def _set_block_title(xml: str, block_pattern: str, title: str) -> str:
    """Replace the <title> inside the single block matched by block_pattern."""
    block = re.compile(block_pattern, re.DOTALL)
    matches = block.findall(xml)
    if len(matches) != 1:
        raise MbzBuildError(f"Template backup header block not found exactly once: {block_pattern}")
    return block.sub(
        lambda m: re.sub(r"<title>.*?</title>", f"<title>{_xml_text(title)}</title>", m.group(0), count=1, flags=re.DOTALL),
        xml,
    )


def _restamp(xml: str, now: int) -> str:
    return re.sub(
        rf"<({'|'.join(TIMESTAMP_TAGS)})>([1-9]\d*)</\1>",
        lambda m: f"<{m.group(1)}>{now}</{m.group(1)}>",
        xml,
    )


# ---- Builder ----

def _edits_for(definition: dict[str, Any], now: int) -> dict[str, Callable[[str], str]]:
    identity = definition["identity"]
    structure = definition["structure"]
    acts = structure["activities"]
    overview_html = render_overview_page(acts["overview"])
    videos_html = render_videos_page(acts["videos"])
    visible = "1" if definition.get("settings", {}).get("visible", True) else "0"

    def course(xml: str) -> str:
        xml = _set_element(xml, "shortname", identity["shortname"])
        xml = _set_element(xml, "fullname", identity["fullname"])
        xml = _set_element(xml, "summary", identity["summary"])
        return _set_element(xml, "visible", visible)

    def section(xml: str) -> str:
        xml = _set_element(xml, "name", structure["section_name"])
        return _set_element(xml, "summary", course_html(structure["section_introduction"]))

    def overview(xml: str) -> str:
        xml = _set_element(xml, "intro", overview_html)
        return _set_element(xml, "content", overview_html)

    def videos(xml: str) -> str:
        xml = _set_element(xml, "intro", videos_html)
        return _set_element(xml, "content", videos_html)

    def resources(xml: str) -> str:
        xml = _set_element(xml, "name", acts["resources"]["name"])
        return _set_element(xml, "externalurl", acts["resources"]["primary_url"])

    def backup(xml: str) -> str:
        xml = _set_element(xml, "original_course_fullname", identity["fullname"])
        xml = _set_element(xml, "original_course_shortname", identity["shortname"])
        xml = re.sub(r'backup_id="[0-9a-f]{32}"', f'backup_id="{secrets.token_hex(16)}"', xml)
        xml = _set_block_title(xml, r"<activity>\s*<moduleid>\d+</moduleid>\s*<sectionid>\d+</sectionid>\s*<modulename>url</modulename>.*?</activity>", acts["resources"]["name"])
        xml = _set_block_title(xml, r"<sections>\s*<section>.*?</section>", structure["section_name"])
        return _set_block_title(xml, r"<course>\s*<courseid>.*?</course>", identity["shortname"])

    return {
        COURSE_XML: course,
        SECTION_XML: section,
        OVERVIEW_PAGE: overview,
        VIDEOS_PAGE: videos,
        RESOURCES_URL: resources,
        BACKUP_XML: backup,
    }


def _archive_index(template_index: str, sizes: dict[str, int], now: int) -> str:
    lines = template_index.splitlines()
    out = [lines[0]]
    for line in lines[1:]:
        if not line.strip():
            continue
        name, kind, _size, _mtime = line.split("\t")
        if kind == "f":
            out.append(f"{name}\tf\t{sizes[name]}\t{now}")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def build_mbz(definition: dict[str, Any], output: Path, *, template: Path = TEMPLATE_PATH, now: int | None = None) -> None:
    """Write a restorable Moodle .mbz for a five-activity Course Definition."""
    acts = definition.get("structure", {}).get("activities", {})
    if set(acts) != {"overview", "resources", "videos", "assignment", "discussion"}:
        raise MbzBuildError("Course Definition does not use the fixed five-activity structure.")
    if output.exists():
        raise MbzBuildError(f"Output already exists; refusing to overwrite it: {output}")

    now = now or int(time.time())
    edits = _edits_for(definition, now)

    with tarfile.open(template, "r:gz") as src:
        members = src.getmembers()
        contents: dict[str, bytes] = {
            m.name: src.extractfile(m).read() for m in members if m.isfile()  # type: ignore[union-attr]
        }

    for name, edit in edits.items():
        if name not in contents:
            raise MbzBuildError(f"Template is missing {name}")
    for name, data in contents.items():
        if name == ARCHIVE_INDEX or not name.endswith(".xml"):
            continue
        xml = data.decode("utf-8")
        if name in edits:
            xml = edits[name](xml)
        contents[name] = _restamp(xml, now).encode("utf-8")

    sizes = {name: len(data) for name, data in contents.items()}
    contents[ARCHIVE_INDEX] = _archive_index(contents[ARCHIVE_INDEX].decode("utf-8"), sizes, now).encode("utf-8")

    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=now) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as dst:
            for member in members:
                info = tarfile.TarInfo(member.name)
                info.type = member.type
                info.mode = member.mode
                info.uid, info.gid = member.uid, member.gid
                info.uname, info.gname = member.uname, member.gname
                if member.isfile():
                    data = contents[member.name]
                    info.size = len(data)
                    info.mtime = member.mtime if member.mtime < 1400000000 else now
                    dst.addfile(info, io.BytesIO(data))
                else:
                    info.mtime = member.mtime
                    dst.addfile(info)

    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(".mbz.tmp")
    tmp.write_bytes(buffer.getvalue())
    tmp.replace(output)
