---
name: create-course
description: Run or resume this repository's Moodle Course workflow, including public-web Source research, human Source selection, local review, packaging, and Trial Restoration.
---

# Create Course

Turn a learning need into a reviewed, validated Moodle Course Package while preserving the repository's human review boundaries.

## Workflow

### 1. Reconstruct the current contract

Read `AGENTS.md`, `CONTEXT.md`, `README.md`, and relevant `docs/adr/` entries. Inspect the current CLI help, example Course Brief, and implementation when a field or command is uncertain. Treat repository code as the source of truth.

Finish by stating the input fields, output paths, commands, and human gates that apply to this run.

### 2. Approve the Course Research Request

Establish a Course Research Request containing the Course name, description, ordered topics, audience, level, intended learning outcome, learning-time budget, and language fixed to English (`en-US`) for the Course and every Source. Infer only low-risk details and state them; ask for any missing choice that materially changes the Course. The ordered topics express the intended learning sequence, not numeric weights.

Translate a broad idea into one observable outcome sized to the time budget. Keep Course terminology consistent with `CONTEXT.md`.

Finish when the Course Requester has approved every Course Research Request field.

### 3. Research Source candidates

Read [source-research.md](references/source-research.md). Search the current public web and collect enough evidence to populate every Source field in the Course Brief. Prefer a small, coherent learning path over a long link list.

Create and present the versioned Source Research Dossier as specified by the research reference. If the requester already supplied exact Sources, confirm that selection and validate them instead of replacing it.

Pause before recording candidates as selected Sources. Continue only after the Course Requester explicitly chooses their ordered selection, then update the dossier with that decision.

Finish when the dossier records the candidates and the explicitly selected Sources are ordered, within budget, accessible without payment, and fully evidenced.

### 4. Create the Course workspace and Brief

Create one durable directory at `output/<course-slug>/`. Keep the Course Brief, Course Definition, Course Package, research notes, and related artifacts inside it; keep the `output/` root free of loose Course files.

Only after the selection gate, create the Course Brief JSON using `examples/copilot-studio-course-brief.json` and `course_research/cli.py` as the live contract. Include only the explicitly selected Sources in their approved order. Write them exactly, including short semantic `activity_name` values suitable for Moodle navigation. Preserve exact external titles in `title`. Estimate `activity_duration_minutes` explicitly for every Source Activity, including its Source and instructed work; keep it at least as long as the Source duration and budget the Course using these activity durations.

Choose new filenames when an artifact already exists. The workflow is append-safe and does not overwrite prior outputs.

Finish when the Brief is valid JSON, contains only human-selected Sources, and every artifact path belongs to the Course directory.

### 5. Generate and inspect the Course Definition

Run:

```bash
bin/course-definition build \
  --brief output/<course-slug>/course-brief.json \
  --output output/<course-slug>/course-definition.json
```

Inspect the generated Definition using [course-review.md](references/course-review.md). If the generated learning path is weak, fix the Brief where possible, write to a new Definition path, and repeat. Surface any limitation that requires a code change rather than silently hand-editing generated output.

Finish when the Definition is contract-valid, traceable to the selected Sources, and reviewable as a coherent Course.

### 6. Stage the hidden Course for human review

Start the package build from the reviewed Definition:

```bash
bin/course-package build \
  --definition output/<course-slug>/course-definition.json \
  --output output/<course-slug>/course-package.mbz
```

Run it interactively. Require the successful hidden-Course review-learner HTTP verification before relaying the printed local Course URL and local-only credentials to the Course Reviewer. Treat a missing or failed verification as a blocking learner-verification failure. Keep the process open and wait for `accept` or `reject`, then send that exact decision to the waiting process. Reserve `--accept` and `--reject` for tests or an explicit automation request; they do not replace genuine review evidence.

On rejection, report the feedback and return to the earliest affected step. A rejection produces no accepted Course Package.

Finish when the Course Reviewer has inspected the hidden local Course and explicitly accepted or rejected it.

### 7. Prove and hand off the Course Package

After acceptance, allow the build to create the native `.mbz` and complete its clean-Moodle Trial Restoration. Require a zero exit status and the explicit restoration and learner-session verification messages. For an existing package, run `bin/course-package verify --package ... --definition ...`.

Report the Brief, Definition, and Course Package paths, review decision, Trial Restoration evidence, Moodle compatibility stated by the repository, and the manual production-import boundary. Call the `.mbz` importable only after Trial Restoration succeeds. Do not import or publish it in production unless the user separately authorizes that operation and supplies the required environment.

Run `bin/course-package down` after the reviewer no longer needs either local Moodle environment.

Finish when the validated `.mbz` exists in its Course directory and the handoff clearly separates local proof from production import.

## Failure handling

- Preserve failed and prior artifacts; use a new versioned filename for another attempt.
- Treat Source availability, provenance, paid access, time-budget, Moodle generation, review, backup, restoration, and learner verification failures as blocking gates.
- Report the failing gate and retain the last trustworthy artifact. Resume from that gate after correction.
- Keep production credentials and production Moodle outside this workflow.
