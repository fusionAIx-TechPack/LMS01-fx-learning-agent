#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
output_dir=$(mktemp -d)
server_pid=
cleanup() {
  if [[ -n $server_pid ]]; then kill "$server_pid" >/dev/null 2>&1 || true; fi
  rm -rf "$output_dir"
}
trap cleanup EXIT

if invalid_output=$("$repo_root/bin/course-definition" build \
  --brief "$repo_root/tests/fixtures/invalid-course-brief.json" \
  --output "$output_dir/invalid.json" 2>&1); then
  echo "Invalid Course Brief unexpectedly produced a Course Definition" >&2
  exit 1
fi
echo "$invalid_output"
grep -F 'Course Brief requires non-empty audience.' <<<"$invalid_output"
test ! -e "$output_dir/invalid.json"

if missing_sources_output=$("$repo_root/bin/course-definition" build \
  --brief "$repo_root/tests/fixtures/missing-sources-course-brief.json" \
  --output "$output_dir/missing-sources.json" 2>&1); then
  echo "A Course Brief without human-selected Sources unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'Course Brief requires at least one human-selected Source.' <<<"$missing_sources_output"
test ! -e "$output_dir/missing-sources.json"

port_file="$output_dir/port"
request_log="$output_dir/requests.log"
python3 "$repo_root/tests/fixture_source_server.py" "$port_file" "$request_log" &
server_pid=$!
for _ in {1..50}; do
  [[ -s $port_file ]] && break
  sleep 0.1
done
[[ -s $port_file ]] || { echo "Fixture Source server did not start" >&2; exit 1; }
fixture_port=$(<"$port_file")
sed "s/__FIXTURE_PORT__/$fixture_port/g" \
  "$repo_root/tests/fixtures/course-brief.json" >"$output_dir/course-brief.json"
sed "s/__FIXTURE_PORT__/$fixture_port/g" \
  "$repo_root/tests/fixtures/unavailable-course-brief.json" >"$output_dir/unavailable-course-brief.json"
sed 's/"learning_time_minutes": 90/"learning_time_minutes": 80/' \
  "$output_dir/course-brief.json" >"$output_dir/over-budget-course-brief.json"
sed 's/"free": true/"free": false/' \
  "$output_dir/course-brief.json" >"$output_dir/paid-source-course-brief.json"
sed '0,/"source_type": "article"/s//"source_type": "podcast"/' \
  "$output_dir/course-brief.json" >"$output_dir/unsupported-source-course-brief.json"
sed '/"publisher":/d' \
  "$output_dir/course-brief.json" >"$output_dir/incomplete-source-course-brief.json"
sed '0,/"activity_name": "Copilot Studio fundamentals"/s//"activity_name": "12345678901234567890123456789012345678901"/' \
  "$output_dir/course-brief.json" >"$output_dir/long-navigation-name-course-brief.json"
sed 's/"language": "en-US"/"language": "pl-PL"/g' \
  "$output_dir/course-brief.json" >"$output_dir/polish-course-brief.json"
sed '/"activity_duration_minutes":/d' \
  "$output_dir/course-brief.json" >"$output_dir/missing-activity-duration-course-brief.json"
sed '0,/"activity_duration_minutes": 30/s//"activity_duration_minutes": 29/' \
  "$output_dir/course-brief.json" >"$output_dir/short-activity-duration-course-brief.json"

if missing_duration_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/missing-activity-duration-course-brief.json" \
    --output "$output_dir/missing-activity-duration.json" 2>&1); then
  echo "A Course Brief without activity duration unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'requires positive integer activity_duration_minutes.' <<<"$missing_duration_output"
test ! -e "$output_dir/missing-activity-duration.json"

if short_duration_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/short-activity-duration-course-brief.json" \
    --output "$output_dir/short-activity-duration.json" 2>&1); then
  echo "A Source Activity shorter than its Source unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'activity_duration_minutes must be at least Source duration_minutes.' <<<"$short_duration_output"
test ! -e "$output_dir/short-activity-duration.json"

if polish_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/polish-course-brief.json" \
    --output "$output_dir/polish.json" 2>&1); then
  echo "A Polish Course Brief unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'Course Brief and Sources must use en-US.' <<<"$polish_output"
test ! -e "$output_dir/polish.json"

if long_name_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/long-navigation-name-course-brief.json" \
    --output "$output_dir/long-navigation-name.json" 2>&1); then
  echo "An overlong Moodle navigation name unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'activity_name must be at most 40 characters for Moodle navigation.' <<<"$long_name_output"
test ! -e "$output_dir/long-navigation-name.json"

if budget_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/over-budget-course-brief.json" \
    --output "$output_dir/over-budget.json" 2>&1); then
  echo "Over-budget human-selected Sources unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'Human-selected Source Activities exceed the Course Brief learning-time budget.' <<<"$budget_output"
test ! -e "$output_dir/over-budget.json"

if paid_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/paid-source-course-brief.json" \
    --output "$output_dir/paid-source.json" 2>&1); then
  echo "A paid Source unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'must record free access evidence.' <<<"$paid_output"
test ! -e "$output_dir/paid-source.json"

if unsupported_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/unsupported-source-course-brief.json" \
    --output "$output_dir/unsupported-source.json" 2>&1); then
  echo "An unsupported Source type unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'source_type must be article, blog, video, or course.' <<<"$unsupported_output"
test ! -e "$output_dir/unsupported-source.json"

if incomplete_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/incomplete-source-course-brief.json" \
    --output "$output_dir/incomplete-source.json" 2>&1); then
  echo "A Source without publisher provenance unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'Course Brief requires non-empty publisher.' <<<"$incomplete_output"
test ! -e "$output_dir/incomplete-source.json"

"$repo_root/bin/course-definition" build \
    --brief "$output_dir/course-brief.json" \
    --output "$output_dir/course-definition.json"

test -s "$output_dir/course-definition.json"
python3 "$repo_root/tests/assert_course_definition.py" "$output_dir/course-definition.json"

jq '
  .course_description = "A deliberately designed learning path." |
  .sources[0].activity_purpose = "Establish the product foundation." |
  .sources[0].activity_instructions = "Open the Source and produce a capability map." |
  .sources[1].activity_purpose = "Apply the product to a first scenario." |
  .sources[1].activity_instructions = "Open the Source and produce a tested agent." |
  .sources[2].activity_purpose = "Connect topics to the scenario." |
  .sources[2].activity_instructions = "Open the Source and produce a topic checklist." |
  .learning_path = [
    {
      "name": "Product landscape",
      "introduction": "Build an ordered product foundation.",
      "source_provider_item_ids": [
        "learn.copilot-studio.topics-introduction",
        "learn.copilot-studio.fundamentals"
      ]
    },
    {
      "name": "Applied build",
      "introduction": "Turn the foundation into a working result.",
      "source_provider_item_ids": ["learn.copilot-studio.first-agent"]
    }
  ]
' "$output_dir/course-brief.json" >"$output_dir/designed-course-brief.json"

"$repo_root/bin/course-definition" build \
  --brief "$output_dir/designed-course-brief.json" \
  --output "$output_dir/designed-course-definition.json"
python3 "$repo_root/tests/assert_designed_course_definition.py" \
  "$output_dir/designed-course-definition.json"

jq '.learning_path[0].source_provider_item_ids[0] = "unknown-source"' \
  "$output_dir/designed-course-brief.json" >"$output_dir/unknown-path-source.json"
if unknown_path_output=$("$repo_root/bin/course-definition" build \
    --brief "$output_dir/unknown-path-source.json" \
    --output "$output_dir/unknown-path-source-definition.json" 2>&1); then
  echo "A learning path with an unknown Source unexpectedly produced a Course Definition" >&2
  exit 1
fi
grep -F 'references unknown Source provider_item_id: unknown-source' <<<"$unknown_path_output"
test ! -e "$output_dir/unknown-path-source-definition.json"

if [[ -n ${COURSE_DEFINITION_CONTRACT_IMAGE:-} ]]; then
  docker run --rm --entrypoint php \
    -v "$repo_root:/repo:ro" \
    -v "$output_dir/course-definition.json:/course-definition.json:ro" \
    "$COURSE_DEFINITION_CONTRACT_IMAGE" \
    -r 'require "/repo/moodle-cli/course_definition.php"; load_course_definition("/course-definition.json"); echo "Exact Course Definition contract accepted.\n";'

  sed '/"publisher":/d' "$output_dir/course-definition.json" >"$output_dir/missing-provenance.json"
  if provenance_output=$(docker run --rm --entrypoint php \
    -v "$repo_root:/repo:ro" \
    -v "$output_dir/missing-provenance.json:/course-definition.json:ro" \
    "$COURSE_DEFINITION_CONTRACT_IMAGE" \
    -r 'require "/repo/moodle-cli/course_definition.php"; load_course_definition("/course-definition.json");' 2>&1); then
    echo "Course Definition without Source provenance unexpectedly passed the Moodle contract" >&2
    exit 1
  fi
  grep -F 'requires Source publisher.' <<<"$provenance_output"

  sed '0,/"name": "Foundations"/s//"name": "12345678901234567890123456789012345678901"/' \
    "$output_dir/course-definition.json" >"$output_dir/long-module-name.json"
  if long_module_output=$(docker run --rm --entrypoint php \
    -v "$repo_root:/repo:ro" \
    -v "$output_dir/long-module-name.json:/course-definition.json:ro" \
    "$COURSE_DEFINITION_CONTRACT_IMAGE" \
    -r 'require "/repo/moodle-cli/course_definition.php"; load_course_definition("/course-definition.json");' 2>&1); then
    echo "An overlong Moodle module name unexpectedly passed the Moodle contract" >&2
    exit 1
  fi
  grep -F 'name must be at most 40 characters for Moodle navigation.' <<<"$long_module_output"

  jq '.modules[0].activities[1].purpose = .modules[0].activities[0].purpose' \
    "$output_dir/course-definition.json" >"$output_dir/duplicate-purpose.json"
  if duplicate_purpose_output=$(docker run --rm --entrypoint php \
    -v "$repo_root:/repo:ro" \
    -v "$output_dir/duplicate-purpose.json:/course-definition.json:ro" \
    "$COURSE_DEFINITION_CONTRACT_IMAGE" \
    -r 'require "/repo/moodle-cli/course_definition.php"; load_course_definition("/course-definition.json");' 2>&1); then
    echo "Duplicate Source Activity purposes unexpectedly passed the Moodle contract" >&2
    exit 1
  fi
  grep -F 'Source Activity purpose must be unique within the Course.' <<<"$duplicate_purpose_output"

  jq '.modules[0].activities[1].instructions = .modules[0].activities[0].instructions' \
    "$output_dir/course-definition.json" >"$output_dir/duplicate-instructions.json"
  if duplicate_instructions_output=$(docker run --rm --entrypoint php \
    -v "$repo_root:/repo:ro" \
    -v "$output_dir/duplicate-instructions.json:/course-definition.json:ro" \
    "$COURSE_DEFINITION_CONTRACT_IMAGE" \
    -r 'require "/repo/moodle-cli/course_definition.php"; load_course_definition("/course-definition.json");' 2>&1); then
    echo "Duplicate Source Activity instructions unexpectedly passed the Moodle contract" >&2
    exit 1
  fi
  grep -F 'Source Activity instructions must be unique within the Course.' <<<"$duplicate_instructions_output"

  jq '.brief.language = "pl-PL"' \
    "$output_dir/course-definition.json" >"$output_dir/polish-course-definition.json"
  if polish_definition_output=$(docker run --rm --entrypoint php \
    -v "$repo_root:/repo:ro" \
    -v "$output_dir/polish-course-definition.json:/course-definition.json:ro" \
    "$COURSE_DEFINITION_CONTRACT_IMAGE" \
    -r 'require "/repo/moodle-cli/course_definition.php"; load_course_definition("/course-definition.json");' 2>&1); then
    echo "A Polish Course Definition unexpectedly passed the Moodle contract" >&2
    exit 1
  fi
  grep -F 'Course Definition brief.language must be en-US.' <<<"$polish_definition_output"
fi
grep -F 'HEAD /sources/fundamentals' "$request_log"
grep -F 'HEAD /sources/first-agent' "$request_log"

if overwrite_output=$("$repo_root/bin/course-definition" build \
  --brief "$output_dir/course-brief.json" \
    --output "$output_dir/course-definition.json" 2>&1); then
  echo "Course Definition build unexpectedly overwrote an existing output" >&2
  exit 1
fi
grep -F 'Output already exists; refusing to overwrite it:' <<<"$overwrite_output"

if unavailable_output=$("$repo_root/bin/course-definition" build \
  --brief "$output_dir/unavailable-course-brief.json" \
    --output "$output_dir/unavailable.json" 2>&1); then
  echo "An unavailable human-selected Source unexpectedly produced a Course Definition" >&2
  exit 1
fi
echo "$unavailable_output"
grep -F 'Human-selected Source is unavailable: Unavailable Source' <<<"$unavailable_output"
test ! -e "$output_dir/unavailable.json"
