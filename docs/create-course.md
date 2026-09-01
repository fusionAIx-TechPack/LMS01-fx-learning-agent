# Using the `create-course` skill

This guide is for Course Requesters using an AI coding agent to turn a learning
need into a Moodle Course Package.

The skill is stored in `.agents/skills/create-course/`. Start the agent from the
repository root so it can discover the skill, repository instructions, domain
language, examples, and CLI tools.

With Codex CLI, run `codex` from the repository root. In the Codex app, open the
checked-out repository folder before starting the conversation. Invoke
`$create-course` with a hyphen; `create_course` is not the skill name.

## When to use it

Use `create-course` when you want to:

- create a new Course from a single source URL;
- research public Sources for a Course;
- resume a Course whose artifacts already exist in `output/<course-slug>/`;
- revise a Course after correcting its Sources or Definition;
- verify an existing Course Package against its Course Definition.

The workflow currently supports English (`en-US`) Courses using free external
articles, blog posts, videos, and courses. It produces a Moodle 5.0.x native
`.mbz` for manual production restoration.

Every generated Course has the same fixed five-activity structure — a course
overview, a link to the entered URL, a reference-video page, a
certification-upload assignment, and a discussion forum. See
[Course structure](course-structure.md).

## Before you start

Confirm that you have:

- access to the private `fusionAIx-TechPack/fx-learning-agent` repository;
- Python 3.11 or newer;
- Docker with Docker Compose v2 and a running Docker daemon;
- local port `8080` available (also `8081` if you run `bin/course-package verify`);
- access to a current public web search through the agent.

The generated Course uses no production credentials, and the packaging step is
unattended after you confirm the Course Research Request.

## Start a new Course

Enter `$create-course`. If you give no URL, the agent prompts:

> Provide a source URL, a list of source URLs in an order, or attach an Excel
> file (`.xlsx` or `.csv`) containing the source URLs — I will read them and
> build one course per URL.
>
> Or just send this to build from the spreadsheet already in `input/`:
>
> ```
> build from input
> ```

Provide one URL, or several (one per line) to build several courses in that
order, or attach a spreadsheet with a column of source URLs, or drop the
spreadsheet in `input/` and reply `build from input`. The agent reads any
spreadsheet with `bin/course-urls` (any column name, header row skipped):

```text
$create-course

https://academy.pega.com/topic/generative-ai-pega/v1
```

The agent inspects each URL and proposes a Course Research Request for you to
confirm — one per course, or, for a list, a single table you approve in bulk:

```text
Course Name: <derived name>
Course Overview: <what the learner will be able to do>
Course Duration: <approximate total in minutes>
Level: fundamental | beginner | intermediate | advanced
Language: en-US
Audience: <who the Course is for>

Would you like to continue creating the course for your Moodle?
```

The agent infers these fields from the source and states any assumption it
makes. Source research begins only after you confirm this proposal.

## What happens during a run

### 1. Course Research Request(s)

You enter one source URL or an ordered list. The agent inspects each and
proposes the Course Name, Course Overview, Course Duration (approximate, in
minutes), Level, `en-US` language, and Audience. For a list it proposes one
table and asks for a single bulk confirmation; it flags any URL that looks paid
or login-gated.

Your action: correct or confirm the proposal(s).

Completion evidence: an explicitly confirmed Course Research Request (or table)
in the conversation. Courses in a list are then built one at a time, each into
its own `output/<course-slug>/`; a URL that fails a gate is skipped, not fatal
to the rest.

### 2. Source research and selection

Starting from the URL you entered, the agent researches the current public web,
records the eligible Source Candidates, and selects the ordered subset of free
Sources that covers the Course Overview within the Course Duration. Each Source
carries its contribution, topic coverage, Source and activity durations,
provenance, current availability, access basis, Source URL, and a separate
free-access evidence URL. The agent also looks for a small number of free
reference videos from public platforms for the reference-video activity, and
records them in the dossier.

The durable results are saved as:

```text
output/<course-slug>/source-candidates-<assessment-date>.md
```

The agent selects the Sources and their order itself. There is no separate
selection step for you and no human review of the staged Moodle Course; the
agent's own review of the Course Definition (step 4) is the quality gate on
this selection.

Your action: none, unless you want to steer the research.

Completion evidence: the Source Research Dossier records the selected Sources in
order and their combined activity time fits the Course Duration.

### 3. Course Brief

The agent creates the Course directory and writes a JSON Course Brief containing
the selected Sources in order, each with a one-line purpose, and any reference
videos. It keeps exact external titles in Source metadata.

Your action: review any assumptions the agent surfaces. You do not need to edit
JSON unless you want to.

Completion evidence: a contract-valid Brief in the Course directory.

### 4. Course Definition

The agent builds and reviews the Course Definition:

```bash
bin/course-definition build \
  --brief output/<course-slug>/course-brief.json \
  --output output/<course-slug>/course-definition.json
```

The Definition is the readable, versionable source of truth. Its `structure`
block describes the five fixed activities — course overview, main link,
reference videos, certification assignment, discussion forum. See
[Course structure](course-structure.md).

This is the last point at which a weak Source choice can be caught, since there
is no human review of the staged Moodle Course.

Completion evidence: a valid, coherent Definition traceable to the approved
Course Research Request and selected Sources.

### 5. Package the Course

The agent runs the build unattended:

```bash
bin/course-package build \
  --definition output/<course-slug>/course-definition.json \
  --output output/<course-slug>/course-package.mbz \
  --accept --skip-restore
```

This stands up a local Moodle, generates the Course, runs an automated
review-learner HTTP check (the five activities are visible and the first four
offer an explicit *Mark as done*), and writes the `.mbz`. It does not pause for
review and does not run clean-Moodle Trial Restoration. See
[ADR-0005](adr/0005-automated-packaging.md).

Your action: none unless the agent reports a failing gate.

Completion evidence: the command exits zero, the automated verification message
is present, and the `.mbz` exists in the Course directory.

### 6. Handoff

The agent runs `bin/course-package down` and reports:

- Course Brief, Course Definition, and Course Package paths;
- the automated review-learner HTTP verification evidence;
- compatible Moodle version stated by the repository;
- that the `.mbz` is code-generated and smoke-checked but **not restore-tested**;
- the manual production-import boundary.

Before a production import, get the restore proof:

```bash
bin/course-package verify \
  --package output/<course-slug>/course-package.mbz \
  --definition output/<course-slug>/course-definition.json
```

Production import and publication require a separate authorization and are not
performed by this skill.

## Resume or revise a Course

Point the agent at the existing Course directory and say which gate was last
completed.

Resume after Source research:

```text
$create-course Resume output/pega-constellation-introduction/. The selected
Sources are recorded in the latest dossier. Create and validate the Course
Brief, then continue to Course Definition review.
```

Resume for packaging:

```text
$create-course Resume output/pega-constellation-introduction/ from the reviewed
Course Definition. Package it.
```

Revise Sources:

```text
$create-course The Sources are missing a key topic and the reference
videos are off-topic. Preserve existing artifacts, create new versioned
outputs, and resume from Source research.
```

Verify an existing package:

```text
$create-course Verify the existing Course Package in
output/pega-constellation-introduction/ against its Course Definition and report
the Trial Restoration evidence.
```

The workflow preserves prior and failed artifacts. When a requested output
already exists, use a new versioned filename rather than overwriting it.

## Artifact layout

One Course directory is the durable audit trail for one Course:

```text
output/<course-slug>/
├── source-candidates-<assessment-date>.md
├── course-brief.json
├── course-definition.json
├── course-package.mbz
└── <other Course-specific review or evidence files>
```

Keep `output/` free of loose files. The repository's `artifacts/` directory is
container scratch space and is not a durable handoff location.

## Blocking conditions

The agent stops at the affected gate when:

- the Course Requester has not confirmed the proposed Course Research Request;
- a Source is unavailable, unsupported, paid, or lacks provenance or access
  evidence;
- the selected Source Activities exceed the Course Duration;
- the Course Definition is invalid or pedagogically incoherent;
- Moodle generation, the automated review-learner HTTP check, or backup fails;
- the requested output path already exists.

Correct the failing input and resume from that gate. A later successful artifact
must not hide an earlier unresolved failure.

## Troubleshooting

### Packaging time

`bin/course-package build --accept --skip-restore` on the pre-built DB seed runs
in about a minute. Without the seed it also installs Moodle (a few minutes); see
"Faster cold builds" in the README. Add `--reuse` to skip the volume wipe when
re-running after a Brief or Definition fix. `bin/course-package verify` stands up
a second Moodle for the restore proof and adds ~30 s on the seed.

End a session with `bin/course-package down`.

### Docker is unavailable

Start the Docker daemon and verify it with `docker info`. Course Definition
generation can run without Moodle, but packaging and `verify` require Docker
Compose.

### Port 8080 or 8081 is already in use

Another Course build or test run may be active. Finish or identify that run
first. When nobody needs the disposable environments, stop them with:

```bash
bin/course-package down
```

Do not run multiple Course builds or `tests/all.sh` concurrently because the
repository uses fixed Compose projects and ports.

### An output already exists

Choose a versioned path such as `course-definition-v2.json` or
`course-package-v2.mbz`. The tools refuse overwrite so accepted and failed
evidence cannot be confused.

### A Source fails validation

Return to the Source Research Dossier, replace or re-evaluate the candidate,
record the updated Source selection and order, and generate new Brief and
Definition files.

### The Course Definition is weak

Keep the existing artifacts. Fix the Brief (Source selection, order, purposes,
reference videos), write a new versioned Definition, and re-package.

## Cleanup and production boundary

After packaging (and any `bin/course-package verify`), run:

```bash
bin/course-package down
```

This removes disposable Docker state but leaves `output/<course-slug>/` intact.

Before importing, run `bin/course-package verify` for the clean-restore proof.
To import, a Moodle administrator manually restores the `.mbz` as a new Course
in a compatible Moodle 5.0.x site. The package restores the Course visible; the
administrator inspects it in that environment and sets visibility under the
organization's normal controls. Production credentials remain outside this
repository and workflow.
