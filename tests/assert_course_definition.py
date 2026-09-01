#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


definition = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert definition["settings"] == {
    "format": "topics",
    "visible": False,
    "completion_tracking": True,
}
assert definition["brief"]["learning_time_minutes"] == 90
assert definition["brief"]["entry_level"] == "beginner"
assert definition["brief"]["language"] == "en-US"
assert len(definition["modules"]) >= 2
activities = [activity for module in definition["modules"] for activity in module["activities"]]
assert len(activities) >= 2
used_minutes = sum(activity["source"]["duration_minutes"] for activity in activities)
assert 67 <= used_minutes <= 90
activity_minutes = sum(activity["duration_minutes"] for activity in activities)
assert activity_minutes == 90
assert definition["modules"][0]["name"] == "Foundations"
assert definition["modules"][1]["name"] == "Practice"
assert all(len(module["name"]) <= 40 for module in definition["modules"])
assert all(len(activity["name"]) <= 40 for activity in activities)
assert all(activity["source"]["publisher"] == "Microsoft Learn" for activity in activities)
assert all(activity["source"]["language"] == "en-US" for activity in activities)
assert all(activity["source"]["provider_item_id"] for activity in activities)
assert {activity["source"]["source_type"] for activity in activities} == {"article", "video"}
assert all(activity["source"]["availability"]["status"] == 200 for activity in activities)
assert all(activity["source"]["access"]["free"] is True for activity in activities)
assert all(activity["source"]["access"]["basis"] for activity in activities)
assert all(
    activity["source"]["access"]["evidence_url"]
    == "https://learn.microsoft.com/en-us/training/support/integrations"
    for activity in activities
)
brief_sources = {
    source["provider_item_id"]: source for source in definition["brief"]["sources"]
}
assert all(
    activity["name"]
    == brief_sources[activity["source"]["provider_item_id"]]["activity_name"]
    for activity in activities
)
assert all(
    activity["source"]["title"]
    == brief_sources[activity["source"]["provider_item_id"]]["title"]
    for activity in activities
)
assert all(
    activity["duration_minutes"]
    == brief_sources[activity["source"]["provider_item_id"]]["activity_duration_minutes"]
    for activity in activities
)
assert all(
    activity["duration_minutes"] >= activity["source"]["duration_minutes"]
    for activity in activities
)
assert len({activity["purpose"] for activity in activities}) == len(activities)
assert len({activity["instructions"] for activity in activities}) == len(activities)
assert all(activity["instructions"].startswith("Open the Source") for activity in activities)
