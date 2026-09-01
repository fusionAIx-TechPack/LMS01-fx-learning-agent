# Source Activity renderer

## Purpose

Every Source Activity uses one global, code-owned renderer. A Course Definition supplies activity-specific data; it does not contain HTML, select a layout, or override the learner-visible structure.

The renderer makes repeated activities predictable without turning their learning purpose and instructions into repeated boilerplate.

## Course Definition contract

Each Source Activity has exactly one Source and records:

- a short navigation `name`;
- a unique, activity-specific `purpose`;
- unique, activity-specific `instructions` that name the learner's expected result;
- a positive `duration_minutes` for the complete activity;
- one Source with its title, URL, publisher, type, language, and positive Source `duration_minutes`;
- Source provenance, availability, and free-access evidence for review and packaging.

The activity duration includes the Source duration and all work required by the instructions. It must be greater than or equal to the Source duration.

Only English (`en-US`) Courses and Sources are supported. Generation fails for any other language rather than producing mixed-language output.

## Learner-visible structure

The renderer presents fields in this order:

1. the activity purpose;
2. `Estimated Activity Duration`;
3. a Source block containing title, publisher, human-readable type, and `Estimated Source Duration`;
4. one `Open Source in a new tab` call to action;
5. the activity instructions;
6. a `Completion` block directing the learner to finish the Source, produce the result required by the instructions, return to Moodle, and select `Mark as done`.

The Source duration is omitted when it equals the activity duration. The Source CTA is the only learner-visible link to the Source. It opens a new tab and must use safe external-link attributes.

Provider identifiers, availability status and check time, and free-access evidence remain available to Course review and package verification but are not shown to the learner.

## Moodle behavior

The Source Activity uses a standard Moodle Page activity so the Course Package requires no custom plugin. Its content contains rendered, escaped HTML from the global renderer. Visiting the activity or opening the Source does not complete it; completion remains manual.

A Moodle URL activity is deliberately not used: its workaround page adds a second Source link outside the generated content, which would violate the single-CTA contract.

The renderer should use semantic HTML and Moodle-compatible presentation hooks. The generated content must remain understandable without renderer-specific styling and under a different compatible Moodle theme.

## Validation and acceptance

Generation fails when:

- the Course or Source language is not `en-US`;
- an activity or Source duration is missing, non-integer, or not positive;
- the activity duration is shorter than the Source duration;
- a Source Activity contains zero or multiple Sources;
- purpose or instructions are empty or duplicated verbatim within the Course;
- the Source URL or review evidence is invalid under the existing Course Definition rules.

Package verification must prove that the rendered activity preserves the two durations, learner-specific purpose and instructions, Source metadata, single safe CTA, completion guidance, and manual completion behavior after clean Moodle restoration.
