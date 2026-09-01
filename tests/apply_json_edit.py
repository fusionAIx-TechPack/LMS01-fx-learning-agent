#!/usr/bin/env python3
"""Apply a named JSON edit for the Course Definition contract tests.

Replaces the `jq` transformations these tests previously relied on so the suite
depends only on Python. Usage:

    apply_json_edit.py <source.json> <destination.json> <edit-name>
"""
from __future__ import annotations

import json
import sys


def polish_language(data: dict) -> None:
    """Set the Course Definition brief language to an unsupported locale."""
    data["brief"]["language"] = "pl-PL"


def overview_count_mismatch(data: dict) -> None:
    """Break the invariant that overview.module_count equals the Source count."""
    data["structure"]["activities"]["overview"]["module_count"] += 7


def drop_structure(data: dict) -> None:
    """Remove the structure block entirely."""
    data.pop("structure", None)


EDITS = {
    "polish-language": polish_language,
    "overview-count-mismatch": overview_count_mismatch,
    "drop-structure": drop_structure,
}


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 64
    source, destination, edit = argv[1], argv[2], argv[3]
    if edit not in EDITS:
        print(f"unknown edit: {edit}; expected one of {', '.join(sorted(EDITS))}", file=sys.stderr)
        return 64
    with open(source, encoding="utf-8") as handle:
        data = json.load(handle)
    EDITS[edit](data)
    with open(destination, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
