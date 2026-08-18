#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
python3 "$repo_root/tests/assert_create_course_skill.py"
docker compose --project-directory "$repo_root" build source
mapfile -t compose_images < <(docker compose --project-directory "$repo_root" config --images)
contract_image=
for image in "${compose_images[@]}"; do
  if [[ $image == *-source ]]; then
    contract_image=$image
    break
  fi
done
[[ -n $contract_image ]] || { echo "Course Definition contract image was not built" >&2; exit 1; }
COURSE_DEFINITION_CONTRACT_IMAGE="$contract_image" "$repo_root/tests/course-definition.sh"
"$repo_root/tests/full-round-trip.sh"
