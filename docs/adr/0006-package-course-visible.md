# The packaged Course is visible

Earlier builds created the Moodle Course hidden (`visible` 0) and the `.mbz`
carried that setting, so a production restore landed a hidden Course that an
administrator then had to publish. Every generated Course is now created
visible (`visible` 1) and the package preserves that: a production restore
lands a visible Course.

Rationale: the meaningful review gate is the Course Research Request (ADR-0003)
and, on demand, `bin/course-package verify` (ADR-0005). Packaging the Course
hidden added a manual publish step at the destination without adding a real
safeguard — the disposable review Moodle at `localhost:8080` is not
internet-facing, and the destination administrator still restores into a site
under their own controls and can hide the Course there if they need to.

Consequences:

- `course_definition` requires `settings.visible` to be `true`;
  `moodle-cli/generate.php` creates the Course with `visible` 1;
  `moodle-cli/verify.php` asserts the restored Course is visible.
- `moodle-cli/prepare_learner.php` still forces `visible` 1 on the restored
  Course before the learner HTTP check, so an externally produced hidden `.mbz`
  can still be verified.
- The manual-import guidance changes from "restore as a new hidden Course and
  publish when ready" to "restore as a new Course, then set visibility to suit
  the destination site".
