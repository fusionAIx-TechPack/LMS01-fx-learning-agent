# Source Research Dossier

Assessment date: 2026-08-18

## Course Research Request

- Name: Building a Custom Open-Weight LLM for Financial Crime Compliance
- Description: An applied Course on creating and evaluating a private, domain-adapted LLM for financial-sector workflows, with emphasis on Know Your Customer (KYC), Customer Lifecycle Management (CLM), and Financial Economic Crime (FEC).
- Ordered topics:
  1. Open-weight versus open-source and proprietary models
  2. Translating KYC, CLM, and FEC requirements into model tasks
  3. Model selection, licensing, infrastructure, privacy, and security
  4. Preparing governed financial-domain datasets
  5. Choosing between prompting, retrieval-augmented generation (RAG), LoRA/QLoRA fine-tuning, and continued pretraining
  6. Implementing a domain-adaptation workflow
  7. Evaluating accuracy, hallucinations, bias, explainability, and compliance risk
  8. Secure deployment, monitoring, human oversight, and model governance
- Audience: AI engineers, solution architects, data scientists, and technical compliance professionals working in regulated financial institutions.
- Level: Intermediate
- Language: en-US
- Intended learning outcome: Design and document a proof-of-concept open-weight LLM solution for one KYC, CLM, or FEC use case, including model choice, adaptation method, governed data flow, evaluation suite, deployment architecture, and human-control mechanisms.
- Learning-time budget: 480 minutes

## Source Candidates

All Sources and access-evidence pages were opened successfully on the assessment date. Durations are editorial estimates in whole minutes. A Source Activity includes the Source plus instructed analysis, implementation planning, or design work. None required payment, an account, or sign-in when assessed.

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| C1 | The Open Source AI Definition – 1.0 | Open Source Initiative | osi/open-source-ai-definition-1.0 | Classify Model Openness | Distinguishes open weights from Open Source AI by testing access to parameters, code, and data information; establishes a licensing checklist for model selection. Topics 1 and 3. | article | en-US | 10 | 20 | Free public OSI definition; anonymous access | https://opensource.org/ai/open-source-ai-definition | https://opensource.org/ai/faq | Available; canonical HTML and FAQ opened 2026-08-18. |
| C2 | Gemma model fine-tuning | Google AI for Developers | google-ai/gemma/tune | Plan Model Adaptation | Provides a concrete open-weight adaptation lifecycle: choose a framework, collect data, select full or parameter-efficient tuning, test success/failure/boundary cases, and deploy. Topics 3, 5, and 6. | article | en-US | 20 | 40 | Free public developer documentation; anonymous access; page content licensed CC BY 4.0 and samples Apache 2.0 | https://ai.google.dev/gemma/docs/tune?hl=en | https://developers.google.com/terms/site-policies | Available; official HTML opened 2026-08-18 and updated 2026-04-16. |
| C3 | Align your models | Google AI for Developers | google-ai/responsible/alignment | Govern Adaptation Data | Connects task and safety tuning to data curation, labeling quality, policy objectives, checkpoint choice, and safeguards; supports a governed KYC/FEC dataset specification. Topics 4, 5, 6, and 7. | article | en-US | 20 | 45 | Free public developer documentation; anonymous access; page content licensed CC BY 4.0 and samples Apache 2.0 | https://ai.google.dev/responsible/docs/alignment | https://developers.google.com/terms/site-policies | Available; official HTML and licensing page opened 2026-08-18. |
| C4 | LoRA | Hugging Face | huggingface-peft/conceptual-guides/lora | Configure LoRA Fine-Tuning | Explains low-rank adapters, frozen base weights, target modules, rank, scaling, adapter merging, and the steps needed to configure PEFT; supports a concrete LoRA/QLoRA experiment plan. Topics 5 and 6. | article | en-US | 25 | 55 | Free public PEFT documentation; anonymous access; PEFT repository is Apache-2.0 licensed | https://huggingface.co/docs/peft/main/conceptual_guides/lora | https://github.com/huggingface/peft/blob/main/LICENSE | Available; current documentation and repository license opened 2026-08-18. |
| C5 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Patrick Lewis et al. / arXiv | arxiv/2005.11401 | Design Grounded Retrieval | Establishes the parametric versus non-parametric memory distinction and the provenance, updateability, factuality, and retrieval trade-offs that motivate RAG for changing KYC/FEC knowledge. Topics 5, 6, and 7. | article | en-US | 30 | 45 | Free public research paper; anonymous HTML/PDF access under the paper's arXiv distribution terms | https://arxiv.org/abs/2005.11401 | https://info.arxiv.org/help/license/index.html | Available; canonical abstract/full-text page and arXiv licensing guidance opened 2026-08-18. |
| C6 | OPPORTUNITIES AND CHALLENGES OF NEW TECHNOLOGIES FOR AML/CFT | Financial Action Task Force (FATF) | fatf/opportunities-challenges-new-technologies-aml-cft | Map AML/CFT Technology | Grounds the solution in customer identification, CDD, monitoring, suspicious-activity analysis, auditability, privacy, cybersecurity, human input, and risk-based oversight. Topics 2, 4, 7, and 8. | article | en-US | 55 | 70 | Free official FATF/OECD PDF; anonymous access | https://www.fatf-gafi.org/content/dam/fatf-gafi/guidance/Opportunities-Challenges-of-New-Technologies-for-AML-CFT.pdf.coredownload.pdf | https://www.fatf-gafi.org/en/publications/Digitaltransformation/Opportunities-challenges-new-technologies-for-aml-cft.html | Available; 76-page official PDF and publication page opened 2026-08-18. Published 2021; use for durable principles and case studies, and recheck current jurisdictional rules during implementation. |
| C7 | Wolfsberg Principles for Using Artificial Intelligence and Machine Learning in Financial Crime Compliance | The Wolfsberg Group | wolfsberg/ai-ml-fcc-principles-2022 | Apply FEC AI Principles | Supplies five financial-crime-specific principles—legitimate purpose, proportionate use, expertise, accountability/oversight, and transparency—to constrain the PoC and its data use. Topics 2, 4, 7, and 8. | article | en-US | 10 | 30 | Free official industry-principles PDF; anonymous access | https://db.wolfsberg-group.org/assets/ae8ec2d1-da45-4cef-b6c6-166e2cf17c03/Wolfsberg%20Principles%20for%20Using%20Artificial%20Intelligence%20and%20Machine%20Learning%20in%20Financial%20Crime%20Compliance.pdf | https://wolfsberg-group.org/resources/legacy/93 | Available; 3-page official PDF and publication page opened 2026-08-18. Published 2022. |
| C8 | Artificial Intelligence in Financial Services: Report on the Uses, Opportunities, and Risks of Artificial Intelligence in the Financial Services Sector | U.S. Department of the Treasury | treasury/136/ai-financial-services-2024 | Design the Financial PoC | Provides financial-services AI use cases relevant to identity verification, AML/CFT and sanctions, plus privacy, bias, explainability, data, vendor, monitoring, and compliance risks; anchors the final architecture canvas. Topics 2, 3, 4, 7, and 8. | article | en-US | 35 | 60 | Free official U.S. Treasury PDF; anonymous access | https://home.treasury.gov/system/files/136/Artificial-Intelligence-in-Financial-Services.pdf | https://home.treasury.gov/news/press-releases/jy2760 | Available; 36-page official PDF and publication page opened 2026-08-18. Published December 2024. |
| C9 | Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile | National Institute of Standards and Technology (NIST) | nist/ai-600-1 | Build the Risk Control Plan | Supplies a GenAI risk taxonomy and lifecycle actions for governance, content provenance, privacy, security, evaluation, incident handling, and monitoring; supports the PoC risk register and control plan. Topics 3, 4, 7, and 8. | article | en-US | 60 | 80 | Free official NIST publication; anonymous PDF access | https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=958388 | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence | Available; 64-page official PDF and publication record opened 2026-08-18; record updated 2026-04-08. |
| C10 | Evaluate model and system for safety | Google AI for Developers | google-ai/responsible/evaluation | Specify the Evaluation Suite | Distinguishes development, assurance, red-team, and external evaluation; guides creation of task-specific success, failure, boundary, safety, fairness, and factuality tests. Topics 7 and 8. | article | en-US | 15 | 35 | Free public developer documentation; anonymous access; page content licensed CC BY 4.0 and samples Apache 2.0 | https://ai.google.dev/responsible/docs/evaluation | https://developers.google.com/terms/site-policies | Available; official HTML and licensing page opened 2026-08-18. |

Combined duration of all ten candidate Source Activities: **480 minutes**, exactly matching the **480-minute** Course budget.

## Topic Coverage

| Topic | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| 1. Open-weight versus open-source and proprietary models | C1, C2 | C1 provides the formal openness test; C2 provides one concrete open-weight family. It does not compare current benchmark rankings, which change too quickly for durable Course content. |
| 2. Translate KYC, CLM, and FEC requirements into model tasks | C6, C7, C8 | Strong coverage of AML/CFT and financial-crime controls. CLM is represented through onboarding, CDD, customer data, ongoing monitoring, and relationship decisions rather than as a standalone regulatory term. |
| 3. Model selection, licensing, infrastructure, privacy, and security | C1, C2, C8, C9 | Strong licensing and risk coverage. Hardware sizing remains scenario-specific and belongs in the learner's PoC rather than a static recommendation. |
| 4. Prepare governed financial-domain datasets | C3, C6, C7, C8, C9 | Strong overlap on lawful purpose, quality, minimization, bias, privacy, accountability, and separation of tuning from evaluation data. |
| 5. Choose prompting, RAG, LoRA/QLoRA, or continued pretraining | C2, C3, C4, C5 | Strong on tuning and RAG. Continued pretraining is treated as a high-cost option to justify, not implemented within this eight-hour Course. |
| 6. Implement a domain-adaptation workflow | C2, C3, C4, C5 | Coherent workflow coverage from data and architecture selection to an implementable LoRA/RAG experiment plan. The Course produces a PoC design, not a multi-GPU training run. |
| 7. Evaluate accuracy, hallucinations, bias, explainability, and compliance risk | C3, C5, C6, C7, C8, C9, C10 | Strong coverage; C10 supplies evaluation modes while financial Sources supply domain-specific failure consequences and control expectations. |
| 8. Secure deployment, monitoring, human oversight, and model governance | C6, C7, C8, C9, C10 | Strong and intentionally overlapping coverage from standard setter, banking-industry, government, and technical-risk perspectives. |

## Recommendation

Recommended order: **C1 → C6 → C7 → C8 → C2 → C3 → C5 → C4 → C9 → C10**.

Combined recommended Source Activity duration: **480 minutes**, exactly matching the **480-minute** budget.

The order first establishes honest model terminology and the regulated use case. It then converts KYC/CLM/FEC needs into explicit controls before choosing an adaptation technique. The technical sequence moves from the overall tuning lifecycle and governed data, through RAG versus weight adaptation, into a concrete LoRA plan. The final two activities turn the design into a risk-control plan and an evaluation suite. The Course should culminate in one documented PoC canvas, not a claim that the learner has trained a production-ready financial model in eight hours.

This recommendation is advisory. No candidate becomes a selected Source until the Course Requester explicitly confirms the exact IDs and order.

## Post-selection Availability Remediation

The repository's live Source validator received HTTP 403 responses from every tested official FATF URL for C6, although the Source remained accessible to an interactive browser and web research client. The Course Requester explicitly approved the following replacement on 2026-08-18:

| ID | Replaces | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| R1 | C6 | Information on Complying with the Customer Due Diligence (CDD) Final Rule | Financial Crimes Enforcement Network (FinCEN) | fincen/cdd-final-rule | Map KYC and CLM Controls | Defines the four core CDD requirements: customer identity, beneficial-owner identity, relationship purpose and risk profile, and ongoing monitoring. It grounds the selected LLM use case in regulated inputs, lifecycle events, and human-controlled outcomes. Topics 2, 4, 7, and 8. | article | en-US | 5 | 70 | Free public FinCEN information page; anonymous access without payment or sign-in | https://www.fincen.gov/resources/statutes-and-regulations/cdd-final-rule | https://www.fincen.gov/site-policies-and-notices | Available; official HTML and public-access policy opened 2026-08-18. |

R1 keeps the 70-minute allocation by replacing the broad FATF reading with a shorter regulatory Source followed by a deeper model-task and control-mapping exercise. C7 and C8 retain broader financial-crime AI, governance, sanctions, privacy, bias, vendor, and monitoring coverage.

The live validator also rejected C9's direct `tsapps.nist.gov` PDF endpoint because of its HTTP method behavior. C9 remains the same selected NIST AI 600-1 publication, but its Source URL in the Course Brief uses the canonical NIST publication record, which the validator accepted and which links to the full official PDF. This is a URL remediation, not a Source replacement.

The first accepted package attempt restored the Course but failed the post-restoration renderer gate because C9's remediated Source URL and access-evidence URL were identical. The failed `course-brief.json` and `course-definition.json` are preserved. `course-brief-v2.json` uses NIST's separate Public Access page (`https://www.nist.gov/open`) as C9 access evidence; the selected Source and learning path are unchanged.

## Excluded Candidates

| Source | Reason |
| --- | --- |
| Horizon Scan AI and Deepfakes (FATF, 2025) | Current and authoritative, but focused on criminals' use of AI and deepfakes rather than building a governed KYC/CLM/FEC LLM. |
| QLoRA: Efficient Finetuning of Quantized LLMs | Valuable primary research, but too detailed for the time budget and substantially overlaps C4. QLoRA remains an implementation option inside the LoRA activity. |
| Model-family benchmark leaderboards | Rankings and hardware/value trade-offs change rapidly; the Course instead teaches a repeatable model-selection checklist. |
| Vendor marketing pages for AML copilots | Excluded because they provide weaker technical and control evidence than FATF, Wolfsberg, Treasury, and NIST. |
| Full foundation-model pretraining tutorials | Training from scratch is outside the approved outcome and infeasible within the Course budget; the Course focuses on domain adaptation of an existing open-weight model. |

## Course Requester Selection

Status: Selected on 2026-08-18

Final ordered Source IDs: **C1, R1, C7, C8, C2, C3, C5, C4, C9, C10**.

Selection note: The Course Requester explicitly selected the complete recommended path in the stated order, then explicitly approved R1 as the replacement for C6 after the live availability failure. The ten selected Source Activities allocate exactly 480 minutes.
