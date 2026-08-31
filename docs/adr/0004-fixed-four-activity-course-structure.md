# Every Course is a fixed activity structure

Supersedes the per-Source Moodle Page structure. A generated Course no longer
has one Moodle Page per Source grouped into learning-path modules. Instead every
Course has the same shape: a single section (section 0, renamed to the Course
topic, with `numsections` 0 so nothing renders above or below it) that contains
exactly five activities, in order:

1. **Course overview** (Page) — states the number of modules, the estimated
   time, and the instruction that the learner must complete every activity and
   then upload proof of completion to the assignment.
2. **&lt;Course topic&gt;** (URL) — a bare link that opens the URL the Course
   Requester entered, in a new window. No description. The selected Sources are
   kept in `brief.sources` and the dossier as the provenance record; they are
   not surfaced to the learner.
3. **Watch reference videos** (Page) — links to free reference videos from
   public platforms, or an empty-state message when none were selected.
4. **Submit Course Certification** (Assignment) — file-upload submission for the
   learner's certificate, badge, or completion screenshot. Completes on submit.
5. **Discussion Forum** (Forum) — a general, ungraded discussion forum for
   learner questions and discussion. Its intro renders on the Course page.

The agent still researches and selects the free Sources and records them in the
versioned Source Research Dossier. What changed is only what the Course is built
from that dossier — a compact, uniform structure rather than a bespoke
per-Source learning path. (Packaging later became unattended; see ADR-0005.)

Consequences:

- The Course Brief gains an optional `reference_videos` array and an optional
  `source_url` (the entered URL, used as the resource list's `externalurl`; it
  falls back to the first Source URL). It no longer uses `learning_path`, and
  per-Source `activity_instructions` are dropped (`activity_purpose` is kept as
  the one-line label in the resource list).
- The Course Definition replaces `modules` with a `structure` block.
- Completion: the overview, resource list, reference-video page, and discussion
  forum require an explicit learner *Mark as done*; the certification assignment
  completes automatically on submission. This narrows ADR-0002's "opening a
  Source never completes an activity" boundary for the assignment only.
- The Course Package uses four standard Moodle module types (`page`, `url`,
  `assign`, `forum`) instead of `page` alone; all remain core Moodle 5.0.x
  components with no user data.
