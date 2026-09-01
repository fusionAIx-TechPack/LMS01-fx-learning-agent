# FX Learning Course Generation

This context describes how internally used learning experiences are designed, assembled, reviewed, and transferred into Moodle.

## Language

### People

**Course Requester**:
The person who defines the learning need and selects the Sources recorded in the Course Brief.
_Avoid_: Content finder, automated researcher

**Course Reviewer**:
The person who inspects the generated Course and explicitly accepts or rejects it before packaging.
_Avoid_: Approver, administrator

### Learning design

**Course Research Request**:
The approved input to Source research defining the Course name, description, topics, audience, level, language, intended learning outcome, and learning-time budget without selecting Sources.
_Avoid_: Course Brief, search prompt

**Course Brief**:
The required input that defines a course's topic, audience, entry level, intended learning outcome, learning-time budget, and the human-selected Sources to use. Courses and Sources use English (`en-US`).
_Avoid_: Topic, prompt

**Course Definition**:
The readable, versionable source of truth derived from a Course Brief that describes Course identity, structure, Learning Activities, Sources, connective text, and Moodle-relevant settings.
_Avoid_: Course export, Moodle state

**Course**:
A structured internal learning experience that guides a learner toward an intended learning outcome through learning activities.
_Avoid_: Link collection, training materials

**Source**:
A free external article, blog post, video, or course selected to support a learning activity and accessible to the company's learners.
_Avoid_: Material, content

**Source Candidate**:
A public external resource surfaced by Course research for the Course Requester to assess; it does not become a Source until the Course Requester explicitly selects it.
_Avoid_: Selected Source, recommendation

**Source Research Dossier**:
The durable record of Source research containing the Course need, evaluated Source Candidates, evidence, recommendations, exclusions, and the Course Requester's final selection.
_Avoid_: Search results, link list

**Learning Activity**:
A course element that gives the learner a purpose, instructions, and an explicit completion expectation. The learner explicitly confirms completion in Moodle after doing the activity.
_Avoid_: Link, material

Its `name` is a short semantic label used throughout Moodle navigation.

**Source Activity**:
A Learning Activity organized around exactly one external Source and presented using one consistent learner-visible structure. Its purpose, instructions, Source details, and estimated duration remain activity-specific; opening the Source does not complete the activity.
_Avoid_: Link activity, URL activity, template

The exact external title belongs to the Source metadata and description, not the Source Activity's navigation name.

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
