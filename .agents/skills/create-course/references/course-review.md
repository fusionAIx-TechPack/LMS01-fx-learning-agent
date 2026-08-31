# Course review

Use this checklist on the generated Course Definition before packaging. There is
no human review of the staged Moodle Course (see
[ADR-0005](../../../../docs/adr/0005-automated-packaging.md)), so this Definition
review is the agent's own quality check. Every Course has the same fixed
five-activity structure; see
[docs/course-structure.md](../../../../docs/course-structure.md).

## Definition review

- Confirm the identity, audience, level, language, intended outcome, and time
  budget match the approved Course Research Request.
- Confirm `structure.section_name` is the Course topic and that the Course has
  exactly one section (named for the topic) - no "General" or empty section.
- Course overview: `module_count` equals the number of selected Sources,
  `estimated_time_label` matches the budget, and the instruction tells the
  learner to complete everything and upload proof to the assignment.
- Main link: `resources.primary_url` equals `brief.source_url` (the entered URL);
  the activity is a bare link with no description.
- Sources: `brief.sources` is a coherent set for the topic, in a deliberate
  order, each fully evidenced. They are the provenance record and set the
  overview's module count; they are not shown to the learner.
- Reference videos: each is free, relevant, and on a public platform, or the
  empty state is acceptable for this Course.
- Assignment: accepts a file upload and completes on submission.
- Discussion forum: a general, ungraded forum named "Discussion Forum".
- Trace every Source and reference video to a dossier entry with complete
  provenance, access, duration, and availability evidence.
- Judge the Source selection and ordering as a coherent learning path - this is
  the last point at which a weak choice can be corrected.

## Automated packaging check

`bin/course-package build ... --accept --skip-restore` runs the review-learner
HTTP verification before writing the `.mbz`: it logs in as a disposable learner
and confirms the five activities are visible and that the first four offer an
explicit *Mark as done*. A missing or failed verification is a blocking failure.

## Restore proof (on demand)

The build does not run clean-Moodle Trial Restoration. Run

```
bin/course-package verify --package <mbz> --definition <definition>
```

to prove the `.mbz` restores into a fresh Moodle with its five activities,
resource links, reference-video list, submit-completion assignment, and manual
completion intact. Recommended before any production import. Until it has run,
report the package as generated and smoke-checked but not restore-proven.
