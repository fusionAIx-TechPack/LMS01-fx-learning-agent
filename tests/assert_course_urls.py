#!/usr/bin/env python3
"""Contract test for bin/course-urls: spreadsheet -> ordered URL list."""
from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COURSE_URLS = REPO_ROOT / "bin" / "course-urls"

URLS = [
    "https://academy.pega.com/mission/11-customer-engagement-business-transformation/v1",
    "https://academy.pega.com/mission/system-architect/v8",
    "https://example.com/course/three",
]


def run(path: Path) -> list[str]:
    result = subprocess.run(
        [sys.executable, str(COURSE_URLS), str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def write_csv(path: Path) -> None:
    lines = ["Souce url"] + URLS + ["", "not-a-url"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _cell_xml(ref: str, text: str) -> str:
    return f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>'


def write_xlsx(path: Path) -> None:
    rows = ["Source URL", *URLS, "", "header-ish junk"]
    sheet_rows = "".join(
        f'<row r="{i + 1}">{_cell_xml(f"A{i + 1}", value)}</row>'
        for i, value in enumerate(rows)
    )
    sheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<sheetData>{sheet_rows}</sheetData></worksheet>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        "</sheets></workbook>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        archive.writestr("xl/worksheets/sheet1.xml", sheet)
    path.write_bytes(buffer.getvalue())


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        csv_path = tmp_path / "courses.csv"
        write_csv(csv_path)
        assert run(csv_path) == URLS, "CSV did not yield the ordered URL list"

        xlsx_path = tmp_path / "courses.xlsx"
        write_xlsx(xlsx_path)
        assert run(xlsx_path) == URLS, "XLSX did not yield the ordered URL list"

        # A directory with exactly one spreadsheet resolves to that file.
        one_dir = tmp_path / "one"
        one_dir.mkdir()
        write_xlsx(one_dir / "courses.xlsx")
        assert run(one_dir) == URLS, "directory with one spreadsheet did not resolve"

        # A directory with more than one spreadsheet is ambiguous -> non-zero.
        two_dir = tmp_path / "two"
        two_dir.mkdir()
        write_xlsx(two_dir / "a.xlsx")
        write_csv(two_dir / "b.csv")
        ambiguous = subprocess.run(
            [sys.executable, str(COURSE_URLS), str(two_dir)],
            capture_output=True,
            text=True,
        )
        assert ambiguous.returncode != 0, "ambiguous directory must fail"

        # A file with no URLs exits non-zero.
        empty = tmp_path / "empty.csv"
        empty.write_text("name\nfoo\nbar\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(COURSE_URLS), str(empty)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "a spreadsheet with no URLs must fail"

    print("bin/course-urls: CSV and XLSX ordered-URL extraction OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
