# Source Research Dossier

Assessment date: 2026-08-18

## Course Research Request

- Name: KYC and CLM Basics for AI Developers
- Description: An introduction to Know Your Customer and Client Lifecycle Management for technical developers implementing AI solutions in banking.
- Ordered topics:
  1. KYC/CLM purpose and terminology
  2. Customer onboarding and the end-to-end client lifecycle
  3. Customer identification, CDD, EDD, screening, and risk assessment
  4. KYC/CLM data, documents, systems, and decision points
  5. Practical AI use cases across the lifecycle
  6. Human review, privacy, explainability, auditability, and regulatory controls
  7. Mapping an AI solution to a sample banking workflow
- Audience: Technical developers with limited KYC/CLM domain knowledge
- Level: Beginner
- Language: en-US
- Intended learning outcome: Given a sample banking onboarding scenario, explain the principal KYC and CLM stages, identify where AI can assist, and describe the necessary data, human-review, and audit controls.
- Learning-time budget: 120 minutes

## Source Candidates

All candidates were opened successfully on the assessment date. Durations are editorial estimates in whole minutes; Source Activity duration includes the Source plus the instructed analysis or mapping task. No candidate required payment, an account, or sign-in when assessed.

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| C1 | Information on Complying with the Customer Due Diligence (CDD) Final Rule | Financial Crimes Enforcement Network (FinCEN) | fincen/cdd-final-rule | Frame KYC and CLM | Introduces why CDD exists and its four core requirements: customer and beneficial-owner identity, relationship purpose/risk profile, and ongoing monitoring. Topics 1, 2, 3. | article | en-US | 5 | 10 | Free public-service page; anonymous access | https://www.fincen.gov/resources/statutes-and-regulations/cdd-final-rule | https://www.fincen.gov/site-policies-and-notices | Available; official HTML opened 2026-08-18. The page also links current 2026 relief and FAQs. |
| C2 | Customer Identification Program | Federal Financial Institutions Examination Council (FFIEC) | ffiec-bsaaml/AssessingComplianceWithBSARegulatoryRequirements/01 | Model customer identification | Defines account-opening data, documentary and non-documentary verification, failure paths, record retention, list comparison, notice, and third-party responsibility. Topics 2, 3, 4, 6. | article | en-US | 16 | 22 | Free official manual; anonymous HTML and PDF access | https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/01 | https://bsaaml.ffiec.gov/manual | Available; official HTML opened 2026-08-18 and listed by FFIEC as the 2021 CIP section. |
| C3 | Customer Due Diligence — Overview | Federal Financial Institutions Examination Council (FFIEC) | ffiec-bsaaml/AssessingComplianceWithBSARegulatoryRequirements/02 | Trace ongoing due diligence | Connects onboarding to customer risk profiles, higher-risk review/EDD, documented decision responsibilities, event-driven updates, and ongoing monitoring across the relationship. Topics 1, 2, 3, 4, 6. | article | en-US | 13 | 20 | Free official manual; anonymous HTML and PDF access | https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/02 | https://bsaaml.ffiec.gov/manual | Available; official HTML opened 2026-08-18 and listed by FFIEC as the 2018 CDD section. |
| C4 | Office of Foreign Assets Control—Overview | Federal Financial Institutions Examination Council (FFIEC) | ffiec-bsaaml/OfficeOfForeignAssetsControl/01 | Design sanctions screening | Explains risk-based sanctions controls, customer and transaction screening, match/false-hit handling, system sensitivity, rescreening, escalation, and evidence retention. Topics 3, 4, 6. | article | en-US | 15 | 22 | Free official manual; anonymous HTML and PDF access | https://bsaaml.ffiec.gov/manual/OfficeOfForeignAssetsControl/01 | https://bsaaml.ffiec.gov/manual | Available; official HTML opened 2026-08-18. Its 2014 section date is old, so implementation must still use current OFAC lists and program rules. |
| C5 | Artificial Intelligence in Financial Services: Report on the Uses, Opportunities, and Risks of Artificial Intelligence in the Financial Services Sector | U.S. Department of the Treasury | treasury/136/artificial-intelligence-in-financial-services-2024 | Map AI uses and risks | Provides banking AI examples directly relevant to AML/CFT and sanctions: identity verification, anomaly detection, suspicious-activity flagging, investigation support, data extraction, and reporting; pairs them with privacy, bias, explainability, vendor, monitoring, and compliance risks. Topics 4, 5, 6, 7. | article | en-US | 35 | 42 | Free official PDF; anonymous access | https://home.treasury.gov/system/files/136/Artificial-Intelligence-in-Financial-Services.pdf | https://home.treasury.gov/news/press-releases/jy2760 | Available; 36-page official PDF and its publication page opened 2026-08-18. Published December 2024. |
| C6 | NIST AI RMF Playbook | National Institute of Standards and Technology (NIST) | nist-airc/airmf-resources/playbook | Govern human-AI controls | Supplies selectable practices for governance, human oversight, privacy, explainability, documentation, impact assessment, testing, monitoring, and accountability when translating a KYC/CLM workflow into an AI-assisted design. Topics 5, 6, 7. | article | en-US | 20 | 28 | Free public NIST resource; anonymous HTML plus downloadable PDF/CSV/JSON | https://airc.nist.gov/airmf-resources/playbook/ | https://www.nist.gov/open | Available; official page opened 2026-08-18. NIST states AI RMF 1.0 and the Playbook are being updated, so recheck before Course packaging. |
| C7 | RISK MANAGEMENT—Supervisory Guidance on Model Risk Management | Board of Governors of the Federal Reserve System, OCC, and FDIC | federal-reserve/3-1579.242 | Control model risk | Covers model purpose/materiality, independent challenge, validation, outcome analysis, monitoring, governance, inventory, documentation, and vendor products for bank models. Topics 4, 5, 6, 7. | article | en-US | 20 | 27 | Free official supervisory guidance; anonymous HTML access | https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm | https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm | Available; revised interagency guidance dated 2026-04-17 opened 2026-08-18. It expressly excludes generative and agentic AI; use it for traditional/non-generative models and as analogous control guidance only. |

Combined duration of all seven candidate activities: **171 minutes**, which exceeds the 120-minute Course budget. Candidates C6 and C7 are alternatives for deeper AI governance rather than additions to the recommended path.

## Topic Coverage

| Topic | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| 1. KYC/CLM purpose and terminology | C1, C3 | Strong overlap on CDD; “CLM” is represented through onboarding, ongoing monitoring, updates, and relationship decisions rather than treated as a separate regulatory term. |
| 2. Onboarding and lifecycle | C1, C2, C3 | C2 is strongest for onboarding; C3 is strongest for ongoing lifecycle monitoring. Account exit appears only as a failed-verification decision in C2. |
| 3. Identification, CDD, EDD, screening, risk | C1, C2, C3, C4 | Strong coverage; C3 covers risk-based heightened review and C4 covers sanctions screening. |
| 4. Data, documents, systems, decisions | C2, C3, C4, C5, C7 | Strong overlap from operational and AI/model perspectives. |
| 5. AI use cases | C5, C6, C7 | C5 provides the most direct AML/KYC examples. C6 is cross-sector; C7 excludes generative and agentic AI. |
| 6. Human review, privacy, explainability, audit, controls | C2, C3, C4, C5, C6, C7 | Strong coverage, with C5/C6 strongest for AI-specific risks and C2–C4 strongest for regulated-process evidence. |
| 7. Map AI to a sample workflow | C5, C6, C7 | No official Source supplies the exact requested sample; the Learning Activity must ask the learner to map these controls onto a supplied onboarding scenario. |

## Recommendation

Recommended order: **C1 → C2 → C3 → C4 → C5**.

Combined recommended Source Activity duration: **116 minutes**, within the **120-minute** budget.

This path moves from the reason for KYC/CDD, through account opening and identity evidence, into ongoing relationship monitoring and sanctions screening, then asks the learner to map appropriate AI assistance and controls onto the same lifecycle. C5 should end with the sample-workflow exercise required by the learning outcome: identify AI-supported steps, input data, deterministic policy gates, human escalation points, records/audit evidence, and monitoring. C6 is the preferred substitution when the requester wants more explicit cross-sector AI governance; C7 is the preferred substitution for a traditional model-heavy implementation. No Source becomes selected through this recommendation.

Remaining gap: the shortlist does not teach a vendor-specific CLM platform or a jurisdiction-neutral definition of “CLM.” It intentionally teaches the underlying client lifecycle through official U.S. banking obligations and controls.

## Post-selection Availability Remediation

The repository's live Source validator accepted C1 and C5 but received HTTP 403 responses for the selected FFIEC C2 and C4 HTML pages. C3 remained the same Source but moved to FFIEC's validator-compatible official PDF URL. The Course Requester explicitly approved the following replacements on 2026-08-18:

| ID | Replaces | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| R1 | C2 | Customer identification programs for banks, savings associations, credit unions, and certain non-Federally regulated banks | Electronic Code of Federal Regulations | 31-cfr-1020.220 | Model Customer Identification | Provides the current legal CIP requirements for identity data, risk-based documentary and non-documentary verification, failure handling, records, government-list comparison, notice, and permitted reliance. Topics 2, 3, 4, 6. | article | en-US | 12 | 22 | Free official current regulation; anonymous access without payment or sign-in. | https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1020/subpart-B/section-1020.220 | https://www.ecfr.gov/reader-aids/using-ecfr/about-the-ecfr | HTTP redirect accepted by the Course validator on 2026-08-18. |
| R2 | C4 | Introduction to the Office of Foreign Assets Control | Office of Foreign Assets Control | ofac/introduction-to-ofac-2026 | Design Sanctions Screening | Current beginner guide explaining sanctions, screening inputs, alert assessment, due diligence, true-match decisions, blocking or rejection, reporting, records, compliance controls, and escalation. Topics 3, 4, 6. | article | en-US | 15 | 22 | Free official OFAC guide; anonymous public PDF without payment or sign-in. | https://ofac.treasury.gov/media/935656/download?inline= | https://ofac.treasury.gov/recent-actions/20260601 | HTTP 200 with the Course validator user agent on 2026-08-18. |

## Excluded Candidates

| Source | Reason |
| --- | --- |
| Risk-Based Approach for the Banking Sector (FATF, 2014) | The official page warns that the guidance does not reflect FATF revisions made after publication, including 2025 changes to Recommendation 1. Useful background, but not preferred for this short current course. |
| The FATF Recommendations (amended October 2025) | Authoritative and current, but too broad and long for a beginner 120-minute Course unless a tightly bounded extract is separately designed and timed. |
| FinCEN Innovation | Official and current but too brief and promotional to add educational substance beyond C5. |
| CDD Rule FAQs (FinCEN, consolidated May 2026) | Current and authoritative but long and detailed for beginners; keep as a follow-up reference after C1/C3 rather than a core Source Activity. |

## Course Requester Selection

Status: Selected on 2026-08-18

Final ordered Source IDs: **C1, R1, C3, R2, C5**.

Selection note: The Course Requester explicitly approved the original recommendation and then approved R1 and R2 after the live availability failure. C3 uses its official FFIEC PDF without changing Source content. The Course Brief allocates 120 minutes across the final five guided Source Activities.
