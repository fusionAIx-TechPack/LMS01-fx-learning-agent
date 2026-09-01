# Source Research Dossier

Assessment date: 2026-08-28

## Course Research Request

The Course Requester entered only a source URL in the Agent Prompt:

- URL: https://learn.microsoft.com/en-us/credentials/applied-skills/build-an-agent-in-microsoft-copilot-studio/

The agent inspected that URL (an assessment landing page for the Microsoft
Applied Skills credential APL-6006) together with its linked study guide
(https://aka.ms/APL6006-StudyGuide) and preparation learning path, and the
Course Requester confirmed this Course Research Request:

- Course Name: Build an Agent in Microsoft Copilot Studio
- Course Overview: Create, configure, and publish a working agent in Microsoft
  Copilot Studio - grounding it with generative AI and knowledge sources,
  authoring topics for guided conversations, and adding a tool - so you can
  complete the tasks measured by the APL-6006 Applied Skills assessment.
- Course Duration: 180 minutes
- Level: intermediate (used directly as `entry_level` in the Course Brief)
- Language: en-US
- Audience: App makers and business users who already have basic familiarity
  with Microsoft Copilot Studio and want to build a custom agent end to end,
  including anyone preparing for the "Build an agent in Microsoft Copilot
  Studio" Applied Skills assessment.

Status: Confirmed on 2026-08-28.

### Duration method and scope decision

The source page states no study or completion time. The initial proposal used
the Level average for `intermediate` (~120 minutes). Inspection of the page's
own stated preparation - the four-module Microsoft Learn path *Create agents in
Microsoft Copilot Studio* - showed those four modules total roughly 3-4 hours
and map almost one-to-one onto the assessment's five task areas. A 120-minute
Course could not honestly cover all five areas. The Course Requester agreed on
2026-08-28 to raise the Course Duration to 180 minutes and cover all four
preparation modules, each scoped in its Learning Activity to the assessment
tasks, preceded by a short orientation on the study guide.

### Source-duration evidence

Microsoft Learn renders module completion-time estimates client-side, so the
exact per-module minute figures are not present in the fetched page text. The
Source durations below are realistic estimates from each module's unit count
and structure, consistent with the estimates used for the same modules in this
repository's earlier `output/copilot-studio-course` dossier. Each Source
Activity duration is set at least as long as its Source duration and adds time
for the instructed hands-on work in a trial environment.

## Source Candidates

All candidates are free, English (`en-US`), publicly accessible on
learn.microsoft.com without payment. Anonymous read access; a free Microsoft
account is only needed to record progress or use the assessment lab, not to
read the material. Free-access basis for every candidate:
https://learn.microsoft.com/en-us/legal/termsofuse

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | Microsoft Applied Skills: Build an agent in Microsoft Copilot Studio | Microsoft Learn | credentials/applied-skills/build-an-agent-in-microsoft-copilot-studio | Know what the assessment covers | Primary Source (entered URL). Orientation: the five assessment task areas - create and configure an agent; configure generative AI and knowledge; create and configure topics; configure tools; share and publish - plus the linked study guide. | article | en-US | 10 | 15 | Free (anonymous read; free account only for the lab) | https://learn.microsoft.com/en-us/credentials/applied-skills/build-an-agent-in-microsoft-copilot-studio/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK (fetched 2026-08-28) |
| 2 | Get started with Microsoft Copilot Studio | Microsoft Learn | training/modules/power-virtual-agents-bots | Build and publish an agent | Create and configure agents with natural language, add instructions and suggested prompts, set the primary language, test in the test pane, publish and share. Covers assessment areas "Create and configure an agent" and "Share and publish an agent". 12 units incl. exercise. | course | en-US | 50 | 55 | Free (anonymous read; free account for module assessment) | https://learn.microsoft.com/en-us/training/modules/power-virtual-agents-bots/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK (fetched 2026-08-28) |
| 3 | Design agent conversations using topics | Microsoft Learn | training/modules/copilot-studio-topics | Author topics for conversations | Topics, triggers, conversation nodes (message, question), branching and conditions, redirects, adaptive cards, variables, entities, system topics. Covers assessment area "Create and configure topics". 12 units. | course | en-US | 40 | 45 | Free (anonymous read; free account for module assessment) | https://learn.microsoft.com/en-us/training/modules/copilot-studio-topics/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK (fetched 2026-08-28) |
| 4 | Build intelligent agents in Microsoft Copilot Studio | Microsoft Learn | training/modules/copilot-studio-knowledge | Add knowledge and generative AI | Knowledge sources, generative answers, model selection, content-moderation level, response formatting, disabling ungrounded responses and web search, conversational boosting. Covers assessment area "Configure generative AI and knowledge". 8 units incl. exercise. | course | en-US | 32 | 35 | Free (anonymous read; free account for module assessment) | https://learn.microsoft.com/en-us/training/modules/copilot-studio-knowledge/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK (fetched 2026-08-28) |
| 5 | Add structured automation to agents in Microsoft Copilot Studio | Microsoft Learn | training/modules/copilot-studio-structured-automation | Add a tool to the agent | Workflow tools, adding tools at agent and topic level, configuring tool input and output variables, referencing the tool from agent instructions, testing tool behavior. Covers assessment area "Configure tools". 9 units. | course | en-US | 28 | 30 | Free (anonymous read; free account for module assessment) | https://learn.microsoft.com/en-us/training/modules/copilot-studio-structured-automation/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK (fetched 2026-08-28) |
| 6 | Create agents in Microsoft Copilot Studio (learning path) | Microsoft Learn | training/paths/create-extend-custom-copilots-microsoft-copilot-studio | (not used directly) | The credential page's designated preparation path; the container for Sources 2-5. Recorded for provenance; the four member modules are used individually. | course | en-US | 210 | - | Free (anonymous read) | https://learn.microsoft.com/en-us/training/paths/create-extend-custom-copilots-microsoft-copilot-studio/ | https://learn.microsoft.com/en-us/legal/termsofuse | 200 OK (fetched 2026-08-28) |

## Topic Coverage

| Topic (assessment task area) | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| Orientation / what is assessed | 1 | Complete. Primary Source plus its study guide. |
| Create and configure an agent | 2 | Complete. |
| Share and publish an agent | 2 | Covered within the same module; no separate Source needed. |
| Create and configure topics | 3 | Complete. |
| Configure generative AI and knowledge | 4 | Complete. |
| Configure tools | 5 | Complete. |
| End-to-end agent build | 2, 3, 4, 5 | Slight overlap: module 2 also touches topics and generative AI at an introductory level; modules 3-5 go deeper. Ordering resolves this - module 2 first, then the focused modules. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| Create agents in Microsoft Copilot Studio (learning path, ID 6) | Used as the provenance container only. Its four modules are included individually so each maps to one Learning Activity with its own scoped instructions. |
| Build an initial agent with Microsoft Copilot Studio (training/modules/create-copilots-copilot-studio) | Overlaps heavily with Source 2 ("Get started"), which is the module the study guide names for the "create and configure an agent" tasks. Adding both would duplicate coverage and push past 180 minutes. |
| Quickstart: Create and deploy an agent with the standard harness (microsoft-copilot-studio/fundamentals-get-started) | A short doc quickstart; the hands-on build is already covered by Source 2's exercise. |
| Microsoft Copilot Studio product documentation (various) | Reference material, not structured learning; not needed to cover the assessment tasks within the Course Duration. |
| APL-6006 study guide as a standalone Source (credentials/applied-skills/resources/study-guides/apl-6006) | Its content is folded into Source 1's Learning Activity instructions so the entered URL remains the primary Source. |

## Selected Sources

The agent selected the Sources and their order, sized to the confirmed
180-minute Course Duration. There is no separate human selection step; the
Course Reviewer inspects the staged Moodle Course in step 6.

| Order | Candidate ID | Source | Activity minutes | Reason selected |
| ---: | --- | --- | ---: | --- |
| 1 | 1 | Microsoft Applied Skills: Build an agent in Microsoft Copilot Studio | 15 | Primary Source; orients the learner to the five task areas before building. |
| 2 | 2 | Get started with Microsoft Copilot Studio | 55 | The module the study guide names for creating, configuring, testing, and publishing an agent; the foundation the later modules build on. |
| 3 | 3 | Design agent conversations using topics | 45 | Deep coverage of topics, nodes, branching, and adaptive cards - the "create and configure topics" task area. |
| 4 | 4 | Build intelligent agents in Microsoft Copilot Studio | 35 | Knowledge sources and generative-answer settings - the "configure generative AI and knowledge" task area. |
| 5 | 5 | Add structured automation to agents in Microsoft Copilot Studio | 30 | Workflow tools and their inputs/outputs - the "configure tools" task area; last because it builds on a working, grounded agent. |

Combined activity duration: 180 minutes (Course Duration: 180 minutes).

## Reference Videos

Free videos from public platforms for the Course's reference-videos activity,
selected 2026-08-28.

| Title | Publisher | URL | Note | Current availability |
| --- | --- | --- | --- | --- |
| Create your first agent in Copilot Studio | Microsoft Learn Shows | https://learn.microsoft.com/en-us/shows/mastering-copilot-studio/create-first-agent-copilot-studio | Official short walkthrough of creating, instructing, and testing a first agent in the standard authoring experience. | 200 OK |
| How to Build AI Agents Using Microsoft Copilot Studio - Full Tutorial | YouTube | https://www.youtube.com/watch?v=4ftNLy9V-hs | Community hands-on end-to-end build covering knowledge, topics, tools, and publishing. | 200 OK |

Both are free to watch without payment. The Microsoft Learn Shows video is the
primary reference; the YouTube tutorial is a fuller hands-on complement.
