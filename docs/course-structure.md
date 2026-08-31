# Course structure

Every generated Course has the same fixed shape. A Course Definition supplies
data; it does not contain HTML, choose a layout, or vary the learner-visible
structure. See [ADR-0004](adr/0004-fixed-four-activity-course-structure.md).

## Section

The Course has exactly one section — section 0, the always-present top section,
renamed to the Course topic (`structure.section_name`) and holding all five
activities. Its summary is the Course description followed by the completion
instruction. `numsections` is 0, so there is no empty section below it and no
"General" heading.

## The five activities

| # | Moodle module | Name | Content |
| - | ------------- | ---- | ------- |
| 1 | Page   | `Course overview` | The intended outcome, then `Number of Modules:` (the count of selected Sources), `Estimated Time:` (the learning-time budget, humanised), and `Instruction:` — the learner must complete every activity and then upload proof of completion to the assignment. Shown on the Course page (*show description*). |
| 2 | URL    | the Course topic | A bare link. `externalurl` is `brief.source_url` — the URL the Course Requester entered after `/create-course` — set to **open in a new window** (`RESOURCELIB_DISPLAY_NEW`). No description. The selected Sources are recorded in `brief.sources` and the dossier for provenance; they are not surfaced to the learner. |
| 3 | Page   | `Watch reference videos` | A bulleted list of reference videos (title link, note, publisher), or an empty-state line when the Course selected none. |
| 4 | Assign | `Submit Course Certification` | File-upload submission (no online text, not graded) for the learner's certificate, badge, or completion screenshot. `max_files` and `file_types` come from the Definition. |
| 5 | Forum  | `Discussion Forum` | A general discussion forum (`type: general`), not graded, for learner questions and discussion. Its intro renders on the Course page. |

## Completion

- Activities 1–3 and the forum use **manual** completion: opening them does not
  complete them; the learner must select *Mark as done*.
- Activity 4 (the assignment) uses **automatic** completion on submission
  (`completionsubmit`).
- Course completion is reached when all five activities are complete.

## Provenance stays out of learner-visible content

Provider identifiers, availability status and check time, and free-access
evidence are recorded in `brief.sources` / `brief.reference_videos` for review
and package verification. They are never rendered into activity content. A
Source's own URL may legitimately contain its provider identifier as a path
segment; verification strips Source links before checking for leakage.

## Course Definition contract

`load_course_definition` (Python `course_research/cli.py` for the Brief, PHP
`moodle-cli/course_definition.php` for the Definition) rejects a Course when:

- the Course or any Source language is not `en-US`;
- there are zero selected Sources, or a Source is missing provenance, free-access
  evidence, availability evidence, or a valid HTTP URL;
- a Source activity duration is missing, non-positive, or shorter than the
  Source duration;
- `structure` is missing or any of its five activities is incomplete;
- `overview.module_count` does not equal the number of Sources;
- `brief.source_url` (the entered URL) is missing or invalid, or
  `resources.primary_url` is not equal to it;
- `videos.items` does not match `brief.reference_videos`;
- a reference video is missing its title, note, publisher, URL, or availability
  evidence.

## Package verification

After clean-Moodle Trial Restoration, `moodle-cli/verify.php` proves the
restored Course has one section (renamed to the topic) holding the five
activities in order and of the right module types (page, url, page, assign,
forum), the overview figures, the main link (correct `externalurl`, opens in a
new window, no description), the reference-video list (or empty state), the
assignment's file-submission and submit-completion configuration, the forum's
ungraded general-discussion configuration, manual completion on the first three
activities and the forum, and no user data.
