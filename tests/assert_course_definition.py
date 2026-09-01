#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


definition = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

assert definition["settings"] == {
    "format": "topics",
    "visible": True,
    "completion_tracking": True,
}
assert definition["brief"]["learning_time_minutes"] == 90
assert definition["brief"]["entry_level"] == "beginner"
assert definition["brief"]["language"] == "en-US"

sources = definition["brief"]["sources"]
assert len(sources) == 3
used_minutes = sum(source["duration_minutes"] for source in sources)
assert 67 <= used_minutes <= 90
activity_minutes = sum(source["activity_duration_minutes"] for source in sources)
assert activity_minutes <= 90
assert all(source["publisher"] == "Microsoft Learn" for source in sources)
assert all(source["language"] == "en-US" for source in sources)
assert all(source["provider_item_id"] for source in sources)
assert {source["source_type"] for source in sources} == {"article", "video"}
assert all(source["availability"]["status"] == 200 for source in sources)
assert all(source["access"]["free"] is True for source in sources)
assert all(source["access"]["basis"] for source in sources)
assert all(
    source["access"]["evidence_url"]
    == "https://learn.microsoft.com/en-us/training/support/integrations"
    for source in sources
)

videos = definition["brief"]["reference_videos"]
assert len(videos) == 1
assert all(video["availability"]["status"] == 200 for video in videos)
assert all(video["title"] and video["note"] and video["publisher"] for video in videos)

structure = definition["structure"]
assert structure["section_name"] == definition["identity"]["fullname"]
activities = structure["activities"]

overview = activities["overview"]
assert overview["name"] == "Course overview"
assert overview["module_count"] == len(sources)
assert overview["estimated_time_minutes"] == 90
assert overview["estimated_time_label"] == "1 hour 30 minutes"
assert overview["instruction"] and overview["outcome"]

resources = activities["resources"]
assert resources["name"] == definition["identity"]["fullname"]
assert resources["primary_url"] == definition["brief"]["source_url"]
assert "items" not in resources and "introduction" not in resources

video_activity = activities["videos"]
assert video_activity["name"] == "Watch reference videos"
assert len(video_activity["items"]) == len(videos)

assignment = activities["assignment"]
assert assignment["name"] == "Submit Course Certification"
assert assignment["max_files"] >= 1
assert assignment["file_types"]

discussion = activities["discussion"]
assert discussion["name"] == "Discussion Forum"
assert discussion["introduction"]
