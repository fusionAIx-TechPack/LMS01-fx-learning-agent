# Source Research Dossier

Assessment date: 2026-08-31

## Course Research Request

The Course Requester entered only a source URL in the Agent Prompt:

- URL: https://microsoft.github.io/IoT-For-Beginners/#/

The agent inspected that URL and its backing repository
(github.com/microsoft/IoT-For-Beginners, MIT licensed, 24 lessons / 12 weeks
across 6 project modules) and the Course Requester confirmed this Course
Research Request:

- Course Name: IoT for Beginners
- Course Overview: Explain what the Internet of Things is, describe the parts of
  an IoT system - devices, sensors, actuators, and connectivity - and outline
  how IoT devices connect to and communicate over the internet.
- Course Duration: 60 minutes
- Level: fundamental (used as `entry_level: beginner`)
- Language: en-US
- Audience: Developers, students, and technology professionals new to IoT, with
  basic programming familiarity assumed.

Status: Confirmed on 2026-08-31.

### Duration method and scope

The curriculum page states no per-lesson or total time. Duration is the
`fundamental`/`beginner` Level average (60 minutes). The full curriculum runs
~12 weeks and is mostly hands-on with hardware (Arduino/Wio Terminal, Raspberry
Pi, or virtual-device options). A 60-minute Course therefore covers only the
conceptual foundations: the four lessons of the **Getting Started** module,
using their reading portions and not the hardware assignments.

### Source-duration evidence

The lesson README pages are concept-focused reading of moderate length. Source
durations below are realistic estimates (12-15 minutes each); each Source
Activity duration is set at least as long.

## Source Candidates

All candidates are lessons from Microsoft's open-source "IoT for Beginners"
curriculum: free, English (`en-US`), publicly readable on GitHub without
payment (a GitHub account is not needed to read). Free-access basis for every
candidate: https://github.com/microsoft/IoT-For-Beginners/blob/main/LICENSE

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | IoT for Beginners - Introduction to IoT | Microsoft | github.com/microsoft/IoT-For-Beginners/1-getting-started/lessons/1-introduction-to-iot | Introduction to IoT | What IoT is, everyday examples, and the high-level anatomy of an IoT application (device + cloud). | article | en-US | 15 | 15 | Free (anonymous read) | https://github.com/microsoft/IoT-For-Beginners/tree/main/1-getting-started/lessons/1-introduction-to-iot | https://github.com/microsoft/IoT-For-Beginners/blob/main/LICENSE | 200 OK (fetched 2026-08-31) |
| 2 | IoT for Beginners - A deeper dive into IoT | Microsoft | github.com/microsoft/IoT-For-Beginners/1-getting-started/lessons/2-deeper-dive | A deeper dive into IoT | Components of an IoT device (microcontrollers vs single-board computers), inputs, outputs, and how they run code. | article | en-US | 15 | 15 | Free (anonymous read) | https://github.com/microsoft/IoT-For-Beginners/tree/main/1-getting-started/lessons/2-deeper-dive | https://github.com/microsoft/IoT-For-Beginners/blob/main/LICENSE | 200 OK (fetched 2026-08-31) |
| 3 | IoT for Beginners - Interact with the physical world with sensors and actuators | Microsoft | github.com/microsoft/IoT-For-Beginners/1-getting-started/lessons/3-sensors-and-actuators | Sensors and actuators | What sensors and actuators are, analog vs digital, and how a device reads the world and acts on it. | article | en-US | 12 | 15 | Free (anonymous read) | https://github.com/microsoft/IoT-For-Beginners/tree/main/1-getting-started/lessons/3-sensors-and-actuators | https://github.com/microsoft/IoT-For-Beginners/blob/main/LICENSE | 200 OK (fetched 2026-08-31) |
| 4 | IoT for Beginners - Connect your device to the Internet | Microsoft | github.com/microsoft/IoT-For-Beginners/1-getting-started/lessons/4-connect-internet | Connect a device to the internet | How IoT devices communicate: MQTT, publish/subscribe, messaging and telemetry to and from the cloud. | article | en-US | 12 | 15 | Free (anonymous read) | https://github.com/microsoft/IoT-For-Beginners/tree/main/1-getting-started/lessons/4-connect-internet | https://github.com/microsoft/IoT-For-Beginners/blob/main/LICENSE | 200 OK (fetched 2026-08-31) |

## Topic Coverage

| Topic | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| What IoT is / IoT application anatomy | 1 | Complete for an introduction. |
| IoT device components | 2 | Complete. |
| Sensors and actuators | 3 | Complete. |
| Connectivity and messaging | 4 | Complete. |
| Farm / Transport / Manufacturing / Retail / Consumer projects | - | Deliberately excluded: hands-on, hardware-dependent, and collectively ~11 weeks. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| Lessons 5-24 (Farm, Transport, Manufacturing, Retail, Consumer projects) | Hands-on hardware/cloud builds; each needs a device and adds hours. Out of scope for a 60-minute conceptual introduction. |
| Hardware shopping lists / device setup pages | Setup material, not learning content; only relevant once a learner commits to a hardware path. |

## Selected Sources

The agent selected the Sources and their order (the Getting Started module
order), sized to the confirmed 60-minute Course Duration. There is no separate
human selection step; the Course Reviewer inspects the staged Moodle Course in
step 6.

| Order | Candidate ID | Source | Activity minutes | Reason selected |
| ---: | --- | --- | ---: | --- |
| 1 | 1 | Introduction to IoT | 15 | Primary conceptual entry point; frames the whole field. |
| 2 | 2 | A deeper dive into IoT | 15 | Builds the mental model of an IoT device before its senses. |
| 3 | 3 | Sensors and actuators | 15 | How a device perceives and affects the physical world. |
| 4 | 4 | Connect your device to the Internet | 15 | How devices talk to the cloud - the "Internet" half of IoT. |

Combined activity duration: 60 minutes (Course Duration: 60 minutes).

## Reference Videos

Free videos from public platforms for the Course's reference-videos activity,
selected 2026-08-31.

| Title | Publisher | URL | Note | Current availability |
| --- | --- | --- | --- | --- |
| IoT \| Internet of Things \| What is IoT? \| How IoT Works? \| IoT Explained in 6 Minutes | YouTube (Simplilearn) | https://www.youtube.com/watch?v=6mBO2vqLv38 | A concise 6-minute overview of what IoT is, how it works, and where it is used. | 200 OK |
| Internet of Things (IoT) Explained in 3 minutes | YouTube | https://www.youtube.com/watch?v=-M74HobvzGA | A short animated primer on connecting everyday objects to the internet for automation and data exchange. | 200 OK |

Both are free to watch without payment.
