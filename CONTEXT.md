# FX Learning Course Generation

This context describes how internally used learning experiences are designed, assembled, reviewed, and transferred into Moodle.

## Language

### People

**Course Requester**:
The person who supplies the source URL and confirms the Course Research Request the agent derives from it.
_Avoid_: Content finder, automated researcher

**Course Reviewer**:
Optional role (see ADR-0005): a person who inspects the staged Course and types `accept` or `reject` when `bin/course-package build` is run without `--accept`. A normal `create-course` run packages unattended and has no Course Reviewer.
_Avoid_: Approver, administrator

### Learning design

**Course Research Request**:
The input to Source research, derived by the agent from a single source URL supplied by the Course Requester and confirmed by them. It defines the Course name, overview, audience, level, language, and approximate duration without selecting Sources.
_Avoid_: Course Brief, search prompt

**Course Brief**:
The required input that defines a course's topic, audience, entry level, intended learning outcome, learning-time budget, and the agent-selected Sources to use. Courses and Sources use English (`en-US`).
_Avoid_: Topic, prompt

**Course Definition**:
The readable, versionable source of truth derived from a Course Brief that describes Course identity, structure, Learning Activities, Sources, connective text, and Moodle-relevant settings.
_Avoid_: Course export, Moodle state

**Course**:
A structured internal learning experience that guides a learner toward an intended learning outcome. Every Course is generated into the same fixed structure: a **Course overview** page, a **URL** activity that opens the entered URL in a new window, a **reference videos** page, a **Submit Course Certification** assignment, and a **Discussion Forum**. See `docs/course-structure.md`.
_Avoid_: Link collection, training materials

**Source**:
A free external article, blog post, video, or course selected to support the Course and accessible to the company's learners. Sources are recorded in the Course Brief and the Source Research Dossier as the provenance record; they inform the Course overview's module count but are not linked from the generated Course.
_Avoid_: Material, content

**Reference Video**:
A free video from a public platform (for example YouTube or a vendor's video library) selected to reinforce the Course. Reference Videos are listed on the Course's reference-videos page and are separate from the ordered Sources.
_Avoid_: Source, tutorial

**Source Candidate**:
A public external resource surfaced by Course research and recorded in the dossier; it does not become a Source until the agent selects it for the Course.
_Avoid_: Selected Source, recommendation

**Source Research Dossier**:
The durable record of Source research containing the confirmed Course Research Request, evaluated Source Candidates, evidence, exclusions, and the ordered Sources the agent selected.
_Avoid_: Search results, link list

**Learning Activity**:
A course element that gives the learner a purpose, instructions, and an explicit completion expectation. The learner explicitly confirms completion in Moodle after doing the activity.
_Avoid_: Link, material

Its `name` is a short semantic label used throughout Moodle navigation.

**Main link**:
The single URL activity, named for the Course topic, that opens the URL the Course Requester entered in a new window. It carries no description. The learner marks it done explicitly.
_Avoid_: Resource list, Source Activity, template

**Estimated Source Duration**:
The estimated time needed to work through a Source, excluding any additional work required by its Learning Activity.
_Avoid_: Estimated time

**Estimated Activity Duration**:
The explicitly estimated total time needed to complete a Learning Activity, including its Sources and the work required by its instructions.
_Avoid_: Source duration, estimated time

### Delivery

**Course Package**:
A Moodle-native `.mbz` backup containing the reviewed course without user data, intended for manual restoration into the production Moodle instance.
_Avoid_: ZIP, course export

**Trial Restoration**:
A clean-Moodle restoration used to prove that a Course Package preserves the learner-visible Course and its completion behavior before production import.
_Avoid_: Import, deployment
