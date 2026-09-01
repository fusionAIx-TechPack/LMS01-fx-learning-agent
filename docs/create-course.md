# Using the `create-course` skill

This guide is for Course Requesters and Course Reviewers using an AI coding
agent to turn a learning need into a reviewed and validated Moodle Course
Package.

The skill is stored in `.agents/skills/create-course/`. Start the agent from the
repository root so it can discover the skill, repository instructions, domain
language, examples, and CLI tools.

With Codex CLI, run `codex` from the repository root. In the Codex app, open the
checked-out repository folder before starting the conversation. Invoke
`$create-course` with a hyphen; `create_course` is not the skill name.

## When to use it

Use `create-course` when you want to:

- create a new Course from an idea;
- research public Source Candidates for a Course;
- continue after selecting Sources;
- resume a Course whose artifacts already exist in `output/<course-slug>/`;
- revise a Course after a review rejection;
- verify an existing Course Package against its Course Definition.

The workflow currently supports English (`en-US`) Courses using free external
articles, blog posts, videos, and courses. It produces a Moodle 5.0.x native
`.mbz` for manual production restoration.

## Before you start

Confirm that you have:

- access to the private `fusionAIx-TechPack/fx-learning-agent` repository;
- Python 3.11 or newer;
- Docker with Docker Compose v2 and a running Docker daemon;
- local ports `8080` and `8081` available;
- access to a current public web search through the agent;
- enough time to select Sources and inspect the staged Course yourself.

The generated Course uses no production credentials. Credentials printed during
review belong only to the disposable local Moodle environment.

## Start a new Course

Use `$create-course` and provide as much of the Course Research Request as you
already know:

```text
$create-course

Create a Course with these parameters:
- name: <Course name>
- description: <why this Course is needed>
- ordered topics: <topic 1>, <topic 2>, <topic 3>
- audience: <who will take it>
- level: beginner | intermediate | advanced
- intended learning outcome: <one observable result>
- learning-time budget: <minutes>
- language: en-US
```

Example:

```text
$create-course

Create a beginner Course called "Introduction to Pega Constellation" for Pega
developers who are new to Constellation. In 90 minutes, the learner should be
able to explain the architecture and build a first view. Cover architecture,
views, fields, and debugging, in that order. Use English Course content and
Sources.
```

The agent may infer harmless details and will state those assumptions. It asks
for a choice when a missing answer would materially change the Course. Source
research begins only after you approve the Course Research Request.

## What happens during a run

### 1. Course Research Request

The agent restates the Course name, description, ordered topics, audience,
level, observable intended outcome, learning-time budget, and `en-US` language.

Your action: correct or approve every field.

Completion evidence: an explicitly approved Course Research Request in the
conversation.

### 2. Source research

The agent researches the current public web and normally presents 5–10 eligible
Source Candidates. Each candidate includes its contribution, topic coverage,
Source and activity durations, provenance, current availability, access basis,
Source URL, and separate free-access evidence URL.

The durable results are saved as:

```text
output/<course-slug>/source-candidates-<assessment-date>.md
```

The recommendation is advisory. A Source Candidate is not yet a Source.

Your action: select the exact ordered subset to use, or request another research
pass. A clear response can be as short as:

```text
Select candidates 1, 3, and 4 in that order.
```

Completion evidence: the Source Research Dossier records your explicit ordered
selection and the combined activity time fits the Course budget.

### 3. Course Brief

After selection, the agent creates the Course directory and writes a JSON Course
Brief containing only the selected Sources. It keeps exact external titles in
Source metadata and creates short semantic activity names for Moodle navigation.

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

The Definition is the readable, versionable source of truth for the Course
structure. Every Source Activity has one Source, a purpose, concrete
instructions, a total activity duration, and explicit manual completion.

Completion evidence: a valid, coherent Definition traceable to the approved
Course Research Request and selected Sources.

### 5. Hidden Moodle review

The agent starts an interactive build from the reviewed Definition:

```bash
bin/course-package build \
  --definition output/<course-slug>/course-definition.json \
  --output output/<course-slug>/course-package.mbz
```

Keep the command running. It prints:

- the direct hidden Course URL at `http://localhost:8080`;
- a disposable local reviewer login;
- a disposable enrolled learner login.

Your action: open the exact printed URL and inspect the Course. Check:

- Course identity, audience, outcome, sections, and activity order;
- activity purpose, instructions, Source metadata, and durations;
- the single safe **Open Source in a new tab** action;
- previous and next navigation;
- learner behavior: opening the Source leaves the activity incomplete, and the
  learner can explicitly select **Mark as done**.

Then return an explicit decision to the waiting process:

- `accept` — continue to packaging;
- `reject` — stop without producing an accepted package.

The agent should relay your exact decision. `--accept` and `--reject` are for
tests or explicitly requested automation and do not replace genuine review.

### 6. Packaging and Trial Restoration

After acceptance, the workflow creates a user-data-free native Moodle backup,
restores it into a clean Moodle at `http://localhost:8081`, and verifies the
restored Course through a learner session.

Your action: none unless the agent reports a failing gate.

Completion evidence: the command exits successfully and reports both clean
restoration and learner-session verification. The `.mbz` is importable only
after this evidence exists.

### 7. Handoff

The agent reports:

- Course Brief path;
- Course Definition path;
- Course Package path;
- Course Reviewer's decision;
- Trial Restoration and learner verification evidence;
- compatible Moodle version stated by the repository;
- the remaining manual production-import boundary.

Production import and publication require a separate authorization and are not
performed by this skill.

## Resume or revise a Course

Point the agent at the existing Course directory and say which gate was last
completed.

Resume after Source selection:

```text
$create-course Resume output/pega-constellation-introduction/. The Source
selection is recorded in the latest dossier. Create and validate the Course
Brief, then continue to Course Definition review.
```

Resume for Moodle review:

```text
$create-course Resume output/pega-constellation-introduction/ from the reviewed
Course Definition. Stage the hidden Course and wait for my review decision.
```

Revise after rejection:

```text
$create-course The staged Course was rejected because activity 2 instructions
do not ask for a concrete learner result. Preserve existing artifacts, create
new versioned outputs, and resume from the earliest affected gate.
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

- the Course Research Request lacks a material decision;
- the Course Requester has not explicitly selected Sources;
- a Source is unavailable, unsupported, paid, or lacks provenance or access
  evidence;
- the selected Source Activities exceed the learning-time budget;
- the Course Definition is invalid or pedagogically incoherent;
- the Course Reviewer rejects the staged Course;
- Moodle generation, backup, clean restoration, or learner verification fails;
- the requested output path already exists.

Correct the failing input and resume from that gate. A later successful artifact
must not hide an earlier unresolved human decision.

## Troubleshooting

### Docker is unavailable

Start the Docker daemon and verify it with `docker info`. Course Definition
generation can run without Moodle, but staging, packaging, and Trial Restoration
require Docker Compose.

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
record a new explicit human selection when the Source set changes, and generate
new Brief and Definition files.

### The Course was rejected

Keep the rejection feedback and existing artifacts. Resume from the earliest
artifact affected by the feedback; no accepted Course Package should exist for
that rejected attempt.

## Cleanup and production boundary

After the Course Reviewer no longer needs either local Moodle environment, run:

```bash
bin/course-package down
```

This removes disposable Docker state but leaves `output/<course-slug>/` intact.

To import a validated package, a Moodle administrator manually restores the
`.mbz` as a new hidden Course in a compatible Moodle 5.0.x site, inspects it in
that environment, and publishes it under the organization's normal controls.
Production credentials remain outside this repository and workflow.
