# Source Research Dossier

Assessment date: 2026-08-27

## Course Research Request

The Course Requester entered only a source URL in the Agent Prompt:

- URL: https://microsoft.github.io/Data-Science-For-Beginners/#/

The agent inspected that URL (and the backing repository) and the Course
Requester confirmed this Course Research Request:

- Course Name: Data Science for Beginners
- Course Overview: Understand what data science is and its ethical considerations; distinguish data types and apply basic statistics and probability; work with data and explore datasets; and choose and build meaningful data visualizations, following the data science lifecycle from analysis to communication.
- Course Duration: 60 minutes (the source states no per-lesson or total time, so this is the `beginner` Level average; the full 20-lesson curriculum is ~10-15 hours and this Course is a focused introduction drawn from it)
- Level: fundamental (maps to `beginner` in the Course Brief)
- Language: en-US
- Audience: Students and professionals new to data science, with only basic computer literacy assumed

Status: Confirmed on 2026-08-27.

## Source Candidates

All candidates are lessons from Microsoft's open-source "Data Science for
Beginners" curriculum (MIT licensed, public GitHub, anonymous access).

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | Data Science for Beginners - Lesson 1: Defining Data Science | Microsoft | github.com/microsoft/Data-Science-For-Beginners/1-Introduction/01-defining-data-science | Study: Defining Data Science | Primary Source lesson. Defines data science, its fields and applications, and where it sits relative to AI and statistics. (Introduction) | article | en-US | 15 | 15 | Free (anonymous access) | https://github.com/microsoft/Data-Science-For-Beginners/tree/main/1-Introduction/01-defining-data-science | https://github.com/microsoft/Data-Science-For-Beginners/blob/main/LICENSE | 200 OK |
| 2 | Data Science for Beginners - Lesson 2: Data Science Ethics | Microsoft | github.com/microsoft/Data-Science-For-Beginners/1-Introduction/02-ethics | Study: Data Science Ethics | Introduces data ethics concepts, applied ethics, data privacy, consent, bias, and the practitioner's responsibilities. (Introduction, Ethics) | article | en-US | 15 | 15 | Free (anonymous access) | https://github.com/microsoft/Data-Science-For-Beginners/tree/main/1-Introduction/02-ethics | https://github.com/microsoft/Data-Science-For-Beginners/blob/main/LICENSE | 200 OK |
| 3 | Data Science for Beginners - Lesson 3: Defining Data | Microsoft | github.com/microsoft/Data-Science-For-Beginners/1-Introduction/03-defining-data | Study: Defining Data | Classifies data by structure (structured, semi-structured, unstructured) and source, and how each is worked with. (Introduction, Data) | article | en-US | 12 | 15 | Free (anonymous access) | https://github.com/microsoft/Data-Science-For-Beginners/tree/main/1-Introduction/03-defining-data | https://github.com/microsoft/Data-Science-For-Beginners/blob/main/LICENSE | 200 OK |
| 4 | Data Science for Beginners - Lesson 9: Visualizing Quantities | Microsoft | github.com/microsoft/Data-Science-For-Beginners/3-Data-Visualization/09-visualization-quantities | Study: Visualizing Quantities | Building the first visualizations: choosing chart types for quantities, reading a dataset, and producing an honest chart. (Data Visualization) | article | en-US | 15 | 15 | Free (anonymous access) | https://github.com/microsoft/Data-Science-For-Beginners/tree/main/3-Data-Visualization/09-visualization-quantities | https://github.com/microsoft/Data-Science-For-Beginners/blob/main/LICENSE | 200 OK |
| 5 | Data Science for Beginners - Lesson 4: Statistics & Probability | Microsoft | github.com/microsoft/Data-Science-For-Beginners/1-Introduction/04-stats-and-probability | Study: Statistics and Probability | Core descriptive statistics and probability for data science, with beginner-friendly examples. (Introduction, Statistics) | article | en-US | 20 | 20 | Free (anonymous access) | https://github.com/microsoft/Data-Science-For-Beginners/tree/main/1-Introduction/04-stats-and-probability | https://github.com/microsoft/Data-Science-For-Beginners/blob/main/LICENSE | 200 OK |
| 6 | Data Science for Beginners - Lesson 7: Python for Data Exploration | Microsoft | github.com/microsoft/Data-Science-For-Beginners/2-Working-With-Data/07-python | Study: Python for Data Exploration | Using Python and pandas to load and explore a dataset. (Working With Data) | article | en-US | 25 | 30 | Free (anonymous access) | https://github.com/microsoft/Data-Science-For-Beginners/tree/main/2-Working-With-Data/07-python | https://github.com/microsoft/Data-Science-For-Beginners/blob/main/LICENSE | 200 OK |

## Topic Coverage

| Topic | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| Introduction (what/why/ethics/data) | 1, 2, 3 | Complete for a short introduction. |
| Statistics | 5 | Available; omitted from the 60-minute selection to keep the path light and non-mathematical. |
| Working With Data | 6 | Available; needs Python and pushes well past 60 minutes, so excluded. |
| Data Visualization | 4 | One representative lesson gives a concrete, hands-off payoff. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| Lesson 4: Statistics & Probability | Solid but math-heavy; drops the 60-minute path below "gentle introduction". Kept as a candidate for a longer version. |
| Lesson 7: Python for Data Exploration | Requires Python setup and ~30 minutes on its own; out of scope for a no-prerequisites 60-minute Course. |
| Remaining 15 curriculum lessons (databases, NoSQL, the rest of visualization, lifecycle, cloud, real-world) | Valuable but collectively ~10+ hours; belong in a multi-part Course, not this introduction. |

## Selected Sources

The agent selected the Sources and their order, sized to the confirmed
60-minute Course Duration. There is no separate human selection step; the Course
Reviewer inspects the staged Moodle Course in step 6.

| Order | Candidate ID | Source | Activity minutes | Reason selected |
| ---: | --- | --- | ---: | --- |
| 1 | 1 | Lesson 1: Defining Data Science | 15 | Primary Source; frames the whole field. |
| 2 | 2 | Lesson 2: Data Science Ethics | 15 | Ethics belongs at the start, before technique. |
| 3 | 3 | Lesson 3: Defining Data | 15 | The vocabulary of data types the rest depends on. |
| 4 | 4 | Lesson 9: Visualizing Quantities | 15 | A concrete, satisfying first application of the ideas. |

Combined activity duration: 60 minutes (Course Duration: 60 minutes).
