#!/usr/bin/env bash
set -euo pipefail

# A parent shell that exported MSYS_NO_PATHCONV stops Git Bash from translating
# the /c/... repo_root into a Windows path that python.exe can open. Clear it
# here; the sub-scripts re-enable it only around the docker calls that need it.
unset MSYS_NO_PATHCONV MSYS2_ARG_CONV_EXCL

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
python3 "$repo_root/tests/assert_create_course_skill.py"
python3 "$repo_root/tests/assert_course_urls.py"
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
