---
name: create-course
description: Run or resume this repository's Moodle Course workflow from one source URL, an ordered list of them, or an attached spreadsheet of source URLs, including public-web Source research and selection and automated packaging into native Moodle .mbz files, one per URL.
---

# Create Course

Turn one source URL - or an ordered list of source URLs, or a spreadsheet of them, one course per URL - into Moodle Course Packages. The one human gate is the Course Requester confirming the derived Course Research Request(s); from there the workflow runs unattended. Packaging auto-accepts each generated Course and does not run clean-Moodle Trial Restoration by default (see [ADR-0005](../../../docs/adr/0005-automated-packaging.md)).

## Start

If the Course Requester invoked the skill without a URL, prompt exactly (both lines, the second verbatim as a ready-to-send command):

> **Provide a source URL, a list of source URLs in an order, or attach an Excel file (`.xlsx` or `.csv`) containing the source URLs - I will read them and build one course per URL.**
>
> Or just send this to build from the spreadsheet already in `input/`:
> ```
> build from input
> ```

Then wait for their input before doing anything else.

If the Course Requester replies `build from input` (or otherwise asks to build from the spreadsheet / `input/` folder), or attaches or names a spreadsheet: extract the ordered URL list with `bin/course-urls <file-or-dir>` - pass `input` to use the single spreadsheet in that folder, or the exact path when they named one. It prints one URL per line, in row order; the column name does not matter and a header row is skipped. Treat that list exactly as a pasted ordered list from step 2 onward.

## Workflow

### 1. Reconstruct the current contract

Read `AGENTS.md`, `CONTEXT.md`, `README.md`, and relevant `docs/adr/` entries. Inspect the current CLI help, example Course Brief, and implementation when a field or command is uncertain. Treat repository code as the source of truth.

Finish by stating the input (one URL or an ordered list), output paths, commands, and the single human gate (Course Research Request confirmation, one per course or one bulk table) that applies to this run.

### 2. Approve the Course Research Request(s)

The Course Requester provides one source URL, an ordered list, or a spreadsheet of URLs (read with `bin/course-urls`). Open each URL and inspect the resource and its visible structure, then propose the Course Research Request for confirmation in this exact format:

```
Course Name: <derived name>
Course Overview: <what the learner will be able to do>
Course Duration: <approximate total, calculated in whole minutes>
Level: fundamental | beginner | intermediate | advanced
Language: en-US
Audience: <who the Course is for>

Would you like to continue creating the course for your Moodle?
```

For a **list of URLs** (pasted or read from an attached spreadsheet with `bin/course-urls`): propose all Course Research Requests in one table (one row per URL, in the given order), flag any URL that looks paid or login-gated, and ask for a single bulk confirmation ("all good", or corrections per row). Then process the confirmed URLs one at a time through steps 3-7, each into its own `output/<course-slug>/`. A URL that fails a gate is reported and skipped; it does not block the rest.

Infer every field from the source and state any assumption you make. `fundamental` is a learner-facing label for an introductory Course; map it to `beginner` when you write the Course Brief `entry_level`, which the contract restricts to `beginner`, `intermediate`, or `advanced`. Keep the language fixed to English (`en-US`) for the Course and every Source, and keep terminology consistent with `CONTEXT.md`. Treat the Course Overview as one observable learning outcome sized to the Course Duration, and derive the ordered topics that express the intended learning sequence from the source structure when you build the Course Brief in step 4. Record the entered URL and this proposal in the Course Research Request section of the dossier.

Set the Course Duration from the source page's own stated completion, watch, or reading time when it gives one. When the page states no time, estimate it from the Level using a typical average: `fundamental`/`beginner` ≈ 60 minutes, `intermediate` ≈ 120 minutes, `advanced` ≈ 180 minutes. State which method you used.

For a list, add `--reuse` to `bin/course-package build` from the second course onward so each build skips the volume wipe.

Finish when the Course Requester has explicitly confirmed the proposed Course Research Request (or the bulk table).

### 3. Research and select Sources

Read [source-research.md](references/source-research.md). Treat the entered URL as the primary Source, then search the current public web for any further Sources needed to cover the Course Overview and topics. Collect enough evidence to populate every Source field in the Course Brief. Prefer a small, coherent learning path over a long link list.

Also search for one to three free reference videos from public platforms (for example YouTube or a vendor's video library) that reinforce the Course. Record their title, URL, publisher, a one-line note, and availability in the dossier. It is acceptable to select none if nothing fits.

Select the Sources and their order yourself, sized to the confirmed Course Duration; there is no separate human selection step. Record the researched candidates, the Sources you selected, their order, the reference videos, and the reasons in the versioned Source Research Dossier.

Finish when the dossier records the selected Sources in order, each accessible without payment, within the Course Duration, and fully evidenced.

### 4. Create the Course workspace and Brief

Create one durable directory at `output/<course-slug>/`. Keep the Course Brief, Course Definition, Course Package, research notes, and related artifacts inside it; keep the `output/` root free of loose Course files.

Once the dossier records the selected Sources, create the Course Brief JSON using `examples/copilot-studio-course-brief.json` and `course_research/cli.py` as the live contract. Set `source_url` to the exact URL the Course Requester entered; the main-link activity opens it in a new window. Include the selected Sources in their dossier order and any `reference_videos`. The Sources are a provenance record and set the Course overview's module count; they are not linked from the generated Course, but still record them fully. Preserve exact external titles in `title`, give each Source a short `activity_name` and a one-line `activity_purpose`, and estimate `activity_duration_minutes` explicitly for every Source, including its Source and instructed work; keep it at least as long as the Source duration and budget the Course using these activity durations.

Every Course is generated into the same fixed five-activity structure (course overview, main link, reference videos, certification assignment, discussion forum); see [docs/course-structure.md](../../../docs/course-structure.md). The Brief supplies the data, not the layout.

Choose new filenames when an artifact already exists. The workflow is append-safe and does not overwrite prior outputs.

Finish when the Brief is valid JSON, contains only the dossier's selected Sources and reference videos, and every artifact path belongs to the Course directory.

### 5. Generate and inspect the Course Definition

Run:

```bash
bin/course-definition build \
  --brief output/<course-slug>/course-brief.json \
  --output output/<course-slug>/course-definition.json
```

Inspect the generated Definition using [course-review.md](references/course-review.md). Check the `structure` block: the overview figures, the main link, the reference videos, and the assignment; and check the selected Sources are a coherent set for the topic. This inspection is the agent's own quality check on Source selection and ordering, since there is no later human review of the staged Course. If the Course is weak, fix the Brief where possible (Source selection, order, purposes, reference videos), write to a new Definition path, and repeat. Surface any limitation that requires a code change rather than silently hand-editing generated output.

Finish when the Definition is contract-valid, traceable to the selected Sources, and coherent as a Course.

### 6. Package the Course

Build the native `.mbz` from the Definition, unattended:

```bash
bin/course-package build \
  --definition output/<course-slug>/course-definition.json \
  --output output/<course-slug>/course-package.mbz \
  --accept --skip-restore
```

This stands up a local Moodle, generates the fixed five-activity Course, runs the automated review-learner HTTP verification, auto-accepts, and writes the `.mbz`. It does not pause for human review and does not run clean-Moodle Trial Restoration.

Treat any of these as a blocking failure: a missing or failed review-learner HTTP verification, a non-zero exit, or a Moodle generation or backup error. Report the failing gate and return to the earliest affected step.

Add `--reuse` to skip the volume wipe when re-running the build after correcting a Brief or Definition, and for every course after the first in a list. Choose a new `--output` filename when one already exists.

### 7. Hand off the Course Package(s)

Run `bin/course-package down` once the last `.mbz` exists.

When a `.mbz` was created successfully, lead the handoff with the exact line **"your mbz file created and ready to use"**. Then report the Brief, Definition, and Course Package paths, the automated review-learner HTTP verification evidence, the Moodle compatibility stated by the repository, and the manual production-import boundary.

For a **list**: build the courses one at a time. As soon as each course's `.mbz` exists, immediately post **"your mbz file created and ready to use"** with that course's folder and `.mbz` path, then start the next course - do not wait for the user between courses. After the last one, post a one-line summary table (a row per course: folder, `.mbz` path, activity count, elapsed time) plus any URLs skipped for a failed gate. Keep the local Moodle up between courses with `--reuse` and only run `bin/course-package down` after the final course.

The `.mbz` has not been restore-tested. State this plainly. Before any production import, restore proof is available on demand:

```bash
bin/course-package verify \
  --package output/<course-slug>/course-package.mbz \
  --definition output/<course-slug>/course-definition.json
```

Do not import or publish the `.mbz` in production unless the user separately authorizes that operation and supplies the required environment.

Finish when the `.mbz` exists in its Course directory and the handoff states that it is code-generated and automatically smoke-checked but not restore-proven.

## Failure handling

- Preserve failed and prior artifacts; use a new versioned filename for another attempt.
- Treat Source availability, provenance, paid access, Course Duration overrun, Moodle generation, backup, and automated review-learner HTTP verification failures as blocking gates.
- Report the failing gate and retain the last trustworthy artifact. Resume from that gate after correction.
- Keep production credentials and production Moodle outside this workflow.
