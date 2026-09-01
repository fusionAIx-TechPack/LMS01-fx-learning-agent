#!/usr/bin/env python3
from __future__ import annotations

import sys
from html.parser import HTMLParser


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: list[dict[str, str]] = []
        self._current: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._current = {name: value or "" for name, value in attrs}
            self._current["text"] = ""

    def handle_data(self, data: str) -> None:
        if self._current is not None:
            self._current["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current is not None:
            self.anchors.append(self._current)
            self._current = None


source_url = sys.argv[1]
parser = AnchorParser()
parser.feed(sys.stdin.read())
source_links = [anchor for anchor in parser.anchors if anchor.get("href") == source_url]
assert len(source_links) == 1, "learner-visible Source Activity must contain exactly one Source URL"
source_link = source_links[0]
assert source_link.get("target") == "_blank", "Source CTA must open a new tab"
assert {"noopener", "noreferrer"}.issubset(source_link.get("rel", "").split()), (
    "Source CTA must have safe external-link attributes"
)
assert source_link["text"].strip() == "Open Source in a new tab", "Source CTA label is incorrect"
