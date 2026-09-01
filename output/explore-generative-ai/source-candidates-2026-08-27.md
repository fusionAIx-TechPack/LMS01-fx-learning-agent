# Source Research Dossier

Assessment date: 2026-08-27

## Course Research Request

The Course Requester entered only a source URL in the Agent Prompt:

- URL: https://learn.microsoft.com/en-in/training/modules/explore-generative-ai/

The agent inspected that URL and the Course Requester confirmed this Course
Research Request:

- Course Name: Explore Generative AI
- Course Overview: Understand the fundamentals of generative AI — distinguish between NLP, NLG, and large language models; assess how generative AI differs from traditional AI models and the role of data; and evaluate how generative AI services such as Microsoft Copilot enhance creativity and productivity.
- Course Duration: 60 minutes (the source page states no machine-readable completion time, so this is the `beginner` Level average)
- Level: fundamental (maps to `beginner` in the Course Brief)
- Language: en-US
- Audience: Developers, students, AI engineers, technology managers, and solution architects who are new to generative AI

Status: Confirmed on 2026-08-27.

## Source Candidates

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | Explore Generative AI | Microsoft Learn | learn.philanthropies.explore-generative-ai | Work through Explore Generative AI | Primary Source. Nine-unit module covering NLP/NLG/LLMs, generative vs. traditional AI, text-to-image, AI companions in content creation, and an exercise plus assessment. (Foundations, Concepts, Applications) | course | en-US | 35 | 40 | Free (anonymous access) | https://learn.microsoft.com/en-us/training/modules/explore-generative-ai/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK |
| 2 | Introduction to Generative AI | Google Cloud Tech | youtube.com/watch?v=G2fqAlgmoPo | Watch Google's Gen AI intro | Vendor-neutral primer on what generative AI is, common applications, model types, and how it differs from other machine learning. (Foundations, Concepts) | video | en-US | 22 | 25 | Free (anonymous access) | https://www.youtube.com/watch?v=G2fqAlgmoPo | https://www.youtube.com/static?template=terms | 200 OK |
| 3 | Generative AI in a Nutshell | Henrik Kniberg | youtube.com/watch?v=2IK3DFHRFfw | Watch Generative AI in a Nutshell | Widely shared visual explainer building intuition for how generative models work and where they help day to day. (Concepts, Applications) | video | en-US | 18 | 20 | Free (anonymous access) | https://www.youtube.com/watch?v=2IK3DFHRFfw | https://www.youtube.com/static?template=terms | 200 OK |
| 4 | What is generative AI? | IBM | ibm.com/think/topics/generative-ai | Read IBM on generative AI | Reference article defining generative AI, foundation models, the train/tune/generate lifecycle, benefits, risks, and use cases. (Foundations, Concepts) | article | en-US | 12 | 15 | Free (anonymous access) | https://www.ibm.com/think/topics/generative-ai | https://www.ibm.com/legal | 200 OK |

## Topic Coverage

| Topic | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| Foundations | 1, 2, 4 | Candidates 2 and 4 overlap on definitions; at most one belongs alongside the primary Source. |
| Concepts | 1, 2, 3, 4 | Well covered. Candidate 3 gives the clearest intuitive model. |
| Applications | 1, 3 | Covered by the primary module and the Nutshell explainer. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| Introduction to Generative AI — Google Cloud Skills Boost / Google Skills (course template 536) | Sign-in required; the anonymous YouTube version (candidate 2) is preferred, and the topic is already covered. |
| Introduction to Generative AI — Google Cloud Tech (candidate 2) | Overlaps candidate 3 on foundations with less pedagogical payoff; dropped to keep the path within 60 minutes. |
| What is generative AI? — IBM (candidate 4) | Solid reference but redundant with the primary module's own definitions; dropped to keep the path within 60 minutes. |
| AI Fluency: Explore AI basics — Microsoft Learn | Useful precursor but adds ~60 minutes and pushes the Course well past a short introductory Duration. |

## Selected Sources

The agent selected the Sources and their order, sized to the confirmed 60-minute
Course Duration. There is no separate human selection step; the Course Reviewer
inspects the staged Moodle Course in step 6.

| Order | Candidate ID | Source | Activity minutes | Reason selected |
| ---: | --- | --- | ---: | --- |
| 1 | 3 | Generative AI in a Nutshell | 20 | Fast, intuitive on-ramp; builds a mental model before the formal module. |
| 2 | 1 | Explore Generative AI (Microsoft Learn) | 40 | Primary Source; structured nine-unit treatment of NLP/NLG/LLMs, generative vs. traditional AI, and applications, with an exercise and assessment. |

Combined activity duration: 60 minutes (Course Duration: 60 minutes).

## Course Review

- 2026-08-27: Course Reviewer inspected the hidden local Moodle Course (staged at http://localhost:8080/course/view.php?id=2) and returned `accept`.
- A renderer fix was then applied (`moodle-cli/source_activity.php`: the Source CTA carries `nomediaplugin` so Moodle's media filter does not strip the safe external-link attributes from video/audio Source links). The package was rebuilt from the same Course Definition with `--accept` because the reviewed learner-visible content was otherwise unchanged.
- Clean-Moodle Trial Restoration passed: restored Course structure, learner-visible activities, single safe Source CTA, and manual completion all verified. `course-package.mbz` is validated.
