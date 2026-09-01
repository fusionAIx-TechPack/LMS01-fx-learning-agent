#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


definition = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert definition["identity"]["fullname"] == "Microsoft Copilot Studio"
assert definition["identity"]["summary"] == "A deliberately designed learning path."
assert [module["name"] for module in definition["modules"]] == [
    "Product landscape",
    "Applied build",
]
activities = [
    activity for module in definition["modules"] for activity in module["activities"]
]
assert [activity["source"]["provider_item_id"] for activity in activities] == [
    "learn.copilot-studio.topics-introduction",
    "learn.copilot-studio.fundamentals",
    "learn.copilot-studio.first-agent",
]
assert [activity["purpose"] for activity in activities] == [
    "Connect topics to the scenario.",
    "Establish the product foundation.",
    "Apply the product to a first scenario.",
]
assert sum(activity["duration_minutes"] for activity in activities) == 90
