Sure Kamil — here is the English version ✨

Training Outline: Copilot Studio Agents — From Basics to Agentic Solutions
Assumptions
Starting level: Beginner → Intermediate
Target audience: Makers, consultants, low-code/AI architects, and people building business agents
Format: Each lesson is a short wrapper around an external resource: Microsoft Learn, documentation, workshop, article, or video
Estimated total duration: approx. 12–16 hours
Recommended delivery: 3–4 blocks of 3–4 hours, or as a self-paced learning path
Section 1 — Microsoft Copilot Studio Fundamentals
Goal: Understand what Copilot Studio is, how agent authoring works, and how to use topics, generative answers, testing, and publishing.

Lesson 1.1 — What is Microsoft Copilot Studio and When Should You Use It?
Resource: Get started with Microsoft Copilot Studio — Microsoft Learn

Lesson wrapper: This lesson introduces the core concepts: agent, topic, trigger phrase, authoring canvas, test pane, publishing, and analytics. Participants learn how Copilot Studio works as a low-code platform for building business agents.

What you will learn:

What an agent is in Copilot Studio
How the authoring environment works
What Power Platform environments are
The basic lifecycle: create → test → publish → analyze
When Copilot Studio is enough, and when you may need Power Automate, Dataverse, or Azure
Estimated time: 60–75 min

Lesson 1.2 — Build Your First Agent
Resource: Build an initial agent with Microsoft Copilot Studio — Microsoft Learn

Lesson wrapper: A practical lesson showing how to create a first agent, configure basic settings, use the conversational builder, and prepare a simple conversation scenario.

What you will learn:

How to create an agent from scratch
How to use natural language to generate the initial configuration
How basic agent settings work
How to move quickly from idea to working prototype
How to deploy or publish a simple agent
Estimated time: 60 min

Lesson 1.3 — Topics, Trigger Phrases, and Conversation Paths
Resource: Manage topics in Microsoft Copilot Studio — Microsoft Learn

Lesson wrapper: This lesson explains topics as small, intent-driven conversation flows. Topics are useful when the interaction should be predictable, testable, and aligned with business rules.

What you will learn:

What topics are
How to design trigger phrases
How to build conversation paths
How to handle questions, answers, and conditions
When to use topics instead of fully generative behavior
Estimated time: 75–90 min

Lesson 1.4 — Entities, Variables, and Conditions
Resource: Work with entities and variables in Microsoft Copilot Studio — Microsoft Learn

Lesson wrapper: This lesson shows how an agent collects information from the user, stores it in variables, and uses it in conversation logic. This is a foundation for agents that guide users through a process instead of only answering questions.

What you will learn:

What entities are
How the agent recognizes values from user input
How to use variables
How to create conditions and branching logic
How to prepare conversations for later actions
Estimated time: 60–75 min

Lesson 1.5 — Generative Answers and Basic Knowledge Sources
Resource: Build an initial agent with Microsoft Copilot Studio — Generative Answers section

Lesson wrapper: This lesson introduces generative answers and knowledge sources. Participants learn to distinguish informational agents from process-driven agents and understand when a knowledge source is enough versus when a topic or action is needed.

What you will learn:

What Generative Answers are
How an agent uses knowledge sources
How to restrict answers to trusted materials
How to test missing or ambiguous answers
Key risks: hallucinations, outdated content, and permission issues
Estimated time: 60 min

Section 2 — Designing Agentic Solutions
Goal: Move from “I have a chatbot” to “I have an agentic solution” — with a clear role, business goal, knowledge, actions, ownership, testing, and governance.

Lesson 2.1 — Agent Design Canvas: From Use Case to Agent Specification
Resource: Use the agent design framework — Microsoft Docs

Lesson wrapper: Participants learn how to design an agent before building it in the UI. The lesson covers business goal, users, allowed tasks, out-of-scope items, knowledge, actions, authentication, handoff, risks, and success metrics.

What you will learn:

How to describe the business goal of an agent
How to define responsibility boundaries
How to separate informational and transactional tasks
How to map knowledge sources and actions
How to prepare a minimal agent design specification
Estimated time: 75–90 min

Lesson 2.2 — Effective Agents: Design Best Practices
Resource: Build effective agents with Microsoft Copilot Studio — Microsoft Learn

Lesson wrapper: This lesson covers principles for building effective agents: clear scope, good greetings, reliable fallbacks, testable conversation paths, and realistic expectations for AI behavior.

What you will learn:

How to design a useful conversational experience
How to avoid overly broad agent scope
How to build fallback and escalation paths
How to guide users through a process
How to think about answer quality
Estimated time: 60–75 min

Lesson 2.3 — Generative Orchestration: Letting the Agent Choose Topics, Actions, and Knowledge
Resource: Apply generative orchestration capabilities — Microsoft Docs

Lesson wrapper: This lesson introduces a key shift from a classic bot to a more agentic solution: the agent can use generative orchestration to decide when to use knowledge, when to run a topic, and when to invoke an action.

What you will learn:

What generative orchestration is
How the agent selects tools based on user intent
How deterministic orchestration differs from generative orchestration
How chaining topics, actions, and knowledge affects solution design
What risks need to be controlled through testing and instructions
Estimated time: 75–90 min

Lesson 2.4 — Actions, Tools, and Integrations: Power Automate, Connectors, APIs, MCP
Resources: Enhance Microsoft Copilot Studio agents — Microsoft Learn Tools, knowledge, MCP, and API — Microsoft Docs

Lesson wrapper: This lesson shows how an agent goes beyond answering questions and starts performing tasks: checking status, saving data, launching workflows, calling APIs, or using connectors.

What you will learn:

When to use a Power Automate flow
When to use a connector or custom connector
When a REST API tool is enough
Where MCP fits
How to describe inputs, outputs, errors, and side effects
When to require user confirmation
Estimated time: 90 min

Lesson 2.5 — Security, Identity, Permissions, and Governance
Resources: Key concepts — Copilot Studio security and governance Manage your Copilot Studio projects, an overview

Lesson wrapper: A business agent must operate securely: with proper permissions, boundaries, ownership, DLP policies, and publishing controls. This lesson focuses on what must be planned before organizational deployment.

What you will learn:

How to think about dev/test/prod environments
How security and governance work in Copilot Studio
What to check for data sources and connectors
How to avoid personal connections as runtime dependencies
How to design for least privilege and auditability
Estimated time: 75–90 min

Section 3 — Building Agents on the Copilot Studio Platform
Goal: Build agents in practice: from a simple informational agent, through a process-driven agent with flows, to an autonomous agent.

Lesson 3.1 — Guided Project: Create an Agent in Copilot Studio
Resource: Guided Project — Create agents with Microsoft Copilot Studio

Lesson wrapper: A practical project where participants go through the full agent creation process: preparation, configuration, topics, generative AI, and testing.

What you will learn:

How to create an agent in a practical scenario
How to generate topics and responses
How to configure generative answers
How to test an agent iteratively
How to turn theory into a first working artifact
Estimated time: 90–120 min

Lesson 3.2 — Agent with Dataverse / Dataverse for Teams
Resource: Create an agent with Microsoft Copilot Studio and Dataverse for Teams — Microsoft Learn

Lesson wrapper: This lesson shows how an agent can use business data from Dataverse. It is a good point to understand the difference between static knowledge and operational data.

What you will learn:

How an agent can retrieve data from Dataverse
How to create and modify topics with logic
How to add inputs, variables, and conditions
How to call an action that retrieves data
How to publish the agent for a team or organization
Estimated time: 90 min

Lesson 3.3 — Agent Flows: Process Automation with Power Automate
Resource: Use Agent Flows in Copilot Studio — Microsoft Learn

Lesson wrapper: This lesson focuses on agent flows — the way an agent performs backend work. It is the bridge between conversational UI and real business processes.

What you will learn:

What agent flows are
How an agent triggers a flow
How to pass inputs and receive outputs
How to handle errors
How to design actions that are safe for users and systems
Estimated time: 75–90 min

Lesson 3.4 — Building an Autonomous Agent
Resources: Build an autonomous agent in Copilot Studio — Microsoft Learn Design autonomous agent capabilities — Microsoft Docs

Lesson wrapper: This lesson shows how to build an agent that not only responds to prompts, but can execute routine tasks and automated workflows. Participants learn the design requirements for autonomy: triggers, actions, guardrails, monitoring, and deployment.

What you will learn:

How an autonomous agent differs from a classic chat agent
Typical autonomous agent use cases
How to design a trigger and operating goal
How to constrain autonomy with rules, instructions, and confirmations
How to deploy and manage an agent in a live environment
Estimated time: 90–120 min

Lesson 3.5 — Publishing, Testing, Analytics, and Iteration
Resources: Get started with Microsoft Copilot Studio — test/publish/analyze sections Establish an application lifecycle management strategy

Lesson wrapper: The final lesson closes the agent development lifecycle: testing, publishing, analytics, improvements, and ALM. Participants learn not to treat publishing as the end of the project, but as the beginning of the operational lifecycle.

What you will learn:

How to test happy paths and edge cases
How to publish an agent
How to analyze usage and response quality
How to plan ALM for Copilot Studio
How to prepare a pre-production checklist
Estimated time: 75–90 min

Suggested Workshop Structure
Option 1 — Intensive 2-Day Workshop
Day	Scope	Time
Day 1 morning	Section 1: Copilot Studio fundamentals	3h
Day 1 afternoon	Topics, variables, Generative Answers, first agent	3h
Day 2 morning	Agentic solution design, actions, generative orchestration	3h
Day 2 afternoon	Agent flows, autonomous agent, governance, wrap-up	3h
Total: approx. 12h

Option 2 — Self-Paced Learning Path
Week	Scope	Time
Week 1	Copilot Studio fundamentals	3–4h
Week 2	Topics, variables, Generative Answers	3h
Week 3	Agentic solution design and integrations	3–4h
Week 4	Autonomous agents, ALM, governance	3–4h
Total: approx. 12–15h

Minimal Final Participant Project
By the end of the training, each participant should prepare:

1. Agent Design Canvas
Including:

Business goal
Users
Allowed and out-of-scope tasks
Knowledge sources
Actions
Security assumptions
Test cases
2. Working Copilot Studio Agent
Minimum requirements:

At least 2 topics
At least 1 knowledge source
At least 1 action or flow
Tested in the Copilot Studio test pane
3. Mini Test Plan
Covering:

Happy path
Ambiguous prompt
Missing data
Out-of-scope request
Action failure
Permission failure
4. Publishing and Governance Checklist
Including:

Environment
Owner
Connections
DLP/security
Monitoring/analytics
Iteration plan
Recommended Resource Sequence
Get started with Microsoft Copilot Studio
Build an initial agent with Microsoft Copilot Studio
Manage topics in Microsoft Copilot Studio
Work with entities and variables
Build effective agents
Apply generative orchestration capabilities
Enhance Copilot Studio agents
Use Agent Flows in Copilot Studio
Build an autonomous agent in Copilot Studio
Security and governance
ALM strategy