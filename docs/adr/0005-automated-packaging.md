# Packaging is automated: no staged-Course human review, no default Trial Restoration

Narrows ADR-0002 and ADR-0003. The `create-course` workflow no longer pauses
for a human to inspect the staged Moodle Course, and it no longer runs
clean-Moodle Trial Restoration as part of a course build. `bin/course-package
build` is invoked with `--accept --skip-restore`, so it stands up a local
Moodle, generates the Course, runs the automated review-learner HTTP
verification, and writes the native `.mbz` unattended.

The one remaining human gate is the Course Requester confirming the derived
Course Research Request (ADR-0003). After that the workflow runs to a `.mbz`
with no further human input.

Rationale: ADR-0004 fixed every Course to the same five-activity structure,
generated entirely by `moodle-cli/generate.php` from a contract-validated
Course Definition. There is no longer a per-Course layout or activity-design
decision for a human to catch at the staged-Course review; the meaningful
editorial choice - which free Sources, in which order - is made and recorded in
the Source Research Dossier and is the agent's own step-5 responsibility. The
automated review-learner HTTP verification still runs before backup and proves
the generated Course renders in Moodle with the five activities visible and
manual completion working.

Consequences:

- The staged-Course review, the disposable reviewer account, and the
  accept/reject prompt are no longer part of a normal run. `bin/course-package`
  keeps `--accept`, `--reject`, `--reuse`, and `--skip-restore`; the full
  interactive flow (omit the flags) still works for anyone who wants it.
- The `create-course` workflow builds **warm by default**: it passes `--reuse`
  on every `bin/course-package build` and does not run `bin/course-package down`,
  so the local Moodle install is kept between runs (~1-2 min/course instead of a
  cold ~2-3 min). It surfaces one line to the Course Requester when a cold build
  is unavoidable (the `*_source-db` / `*_source-data` volumes are gone, or the
  DB seed predates a `docker/moodle` / `moodle-cli` change) and continues.
  `bin/course-package down` is run only on request or for a release-clean build.
- A packaged `.mbz` is code-generated and smoke-checked but **not proven to
  restore**. `bin/course-package verify --package ... --definition ...` runs the
  clean-Moodle Trial Restoration on demand and is recommended before any
  production import.
- The handoff must state that the package was not restore-tested.
- ADR-0002's staged technical gate is preserved only as the on-demand `verify`
  path, not as a build-time requirement.
