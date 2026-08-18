#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
output_dir=$(mktemp -d)
server_pid=
"$repo_root/bin/course-package" down >/dev/null 2>&1 || true
cleanup() {
  "$repo_root/bin/course-package" down >/dev/null 2>&1 || true
  if [[ -n $server_pid ]]; then kill "$server_pid" >/dev/null 2>&1 || true; fi
  rm -rf "$output_dir"
}
trap cleanup EXIT

if invalid_brief_output=$("$repo_root/bin/course-package" build \
  --brief "$repo_root/tests/fixtures/invalid-course-brief.json" \
  --definition-output "$output_dir/invalid-brief-definition.json" \
  --output "$output_dir/invalid-brief.mbz" --accept 2>&1); then
  echo "Invalid Course Brief unexpectedly entered Moodle generation" >&2
  exit 1
fi
grep -F 'Course Brief requires non-empty audience.' <<<"$invalid_brief_output"
test ! -e "$output_dir/invalid-brief-definition.json"
test ! -e "$output_dir/invalid-brief.mbz"

if same_output=$("$repo_root/bin/course-package" build \
  --brief "$repo_root/tests/fixtures/course-brief.json" \
  --definition-output "$output_dir/same-output" \
  --output "$output_dir/same-output" --accept 2>&1); then
  echo "Course Definition and Course Package unexpectedly shared an output path" >&2
  exit 1
fi
grep -F 'Course Definition and Course Package outputs must use different paths.' <<<"$same_output"
test ! -e "$output_dir/same-output"

if invalid_output=$("$repo_root/bin/course-package" build \
  --definition "$repo_root/tests/fixtures/invalid-modules-object.json" \
  --output "$output_dir/invalid-modules.mbz" --accept 2>&1); then
  echo "Object-valued modules unexpectedly passed Course Definition validation" >&2
  exit 1
fi
echo "$invalid_output"
grep -F 'Course Definition modules must be a JSON array.' <<<"$invalid_output"
test ! -e "$output_dir/invalid-modules.mbz"

if invalid_output=$("$repo_root/bin/course-package" build \
  --definition "$repo_root/tests/fixtures/invalid-activities-object.json" \
  --output "$output_dir/invalid-activities.mbz" --accept 2>&1); then
  echo "Object-valued activities unexpectedly passed Course Definition validation" >&2
  exit 1
fi
echo "$invalid_output"
grep -F 'Course Definition module 0 activities must be a JSON array.' <<<"$invalid_output"
test ! -e "$output_dir/invalid-activities.mbz"

if "$repo_root/bin/course-package" build \
  --definition "$repo_root/tests/fixtures/course-definition.json" \
  --output "$output_dir/rejected.mbz" --reject; then
  echo "Rejected Course unexpectedly produced a validated Course Package" >&2
  exit 1
fi
test ! -e "$output_dir/rejected.mbz"

touch "$output_dir/existing.mbz"
if "$repo_root/bin/course-package" build \
  --definition "$repo_root/tests/fixtures/course-definition.json" \
  --output "$output_dir/existing.mbz" --accept; then
  echo "Build unexpectedly overwrote an existing output" >&2
  exit 1
fi

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

if ! build_output=$("$repo_root/bin/course-package" build \
  --brief "$output_dir/course-brief.json" \
  --definition-output "$output_dir/generated-course-definition.json" \
  --output "$output_dir/copilot-studio-practical-basics.mbz" --accept 2>&1); then
  echo "$build_output" >&2
  exit 1
fi
echo "$build_output"
grep -F 'http://localhost:8080/course/view.php?id=' <<<"$build_output"
grep -F 'Local review admin login: admin / LocalOnly-ChangeMe1!' <<<"$build_output"
grep -F 'Local review learner login: course-review-learner / LocalOnly-Review1!' <<<"$build_output"
grep -F 'Verified restored Course through learner HTTP session.' <<<"$build_output"
grep -F "Course Definition generated and ready for review: $output_dir/generated-course-definition.json" <<<"$build_output"
grep -F 'Manual production import: in a compatible Moodle 5.0.x site' <<<"$build_output"

test -s "$output_dir/generated-course-definition.json"
python3 "$repo_root/tests/assert_course_definition.py" "$output_dir/generated-course-definition.json"
test -s "$output_dir/copilot-studio-practical-basics.mbz"
"$repo_root/bin/course-package" verify \
  --package "$output_dir/copilot-studio-practical-basics.mbz" \
  --definition "$output_dir/generated-course-definition.json"
