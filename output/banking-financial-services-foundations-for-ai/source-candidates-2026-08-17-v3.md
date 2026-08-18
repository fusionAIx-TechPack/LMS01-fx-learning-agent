# Source Research Dossier

Assessment date: 2026-08-17

## Course Research Request

- Name: Banking and Financial Services Foundations for AI Solution Teams
- Description: A practical banking-operations, controls, technology, regulation, and responsible-AI foundation for JavaScript and Python developers, Pega architects, technical leads, and AI solution designers.
- Ordered topics: The 18 approved topics in the original dossier, including KYC, Client Lifecycle Management, AML/CFT, sanctions, fraud, transaction monitoring, investigations, and risk-based financial-crime controls.
- Audience: JavaScript developers, Python developers, Pega architects, technical leads, and AI solution designers with limited banking-domain experience
- Level: Beginner
- Language: en-US for the Course and every Source
- Intended learning outcome: Given a banking AI use case, analyse its customer journey, operational process, actors, data, systems, risks, and regulatory controls, then propose an appropriate AI-assisted solution with human oversight and measurable CSAT, cost, speed, and control outcomes.
- Learning-time budget: 720 minutes (12 hours)

## Availability Failure Requiring Reselection

The initially selected C06, *Risk-Based Approach for the Banking Sector*, is free and opens in an interactive browser, but both the FATF landing page and direct PDF return HTTP 403 to the repository's required availability validator. It cannot remain a selected Source.

## Replacement Source Candidates

| ID | Source | Publisher | Provider item ID | Activity name | Contribution and covered topics | Type | Language | Source minutes | Activity minutes | Access and sign-in | Source URL | Access evidence | Current availability |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| K01 | Guidelines on ML/TF risk factors | European Banking Authority | aml-cft-risk-factors-consolidated-2023 | Apply Risk-Based KYC | Consolidated, in-force guidance on institutional and customer ML/TF risk assessment, customer and beneficial-owner due diligence, simplified and enhanced due diligence, high-risk countries, products, channels, ongoing monitoring, governance, and sector-specific banking risks. Existing EBA guidance remains valid until replaced by AMLA. Covers approved topics 3, 6, 10–12, 15, and 17. | article | en-US | 75 | 90 | Public EBA guidance page and downloadable consolidated PDF; anonymous access; no payment or sign-in required. | https://www.eba.europa.eu/legacy/regulation-and-policy/regulatory-activities/anti-money-laundering-and-countering-financing-1?phase=consolidated&version=2023 | https://www.eba.europa.eu/regulation-and-policy/anti-money-laundering-and-countering-financing-terrorism | HTTP 200 with the Course validator user agent on 2026-08-17. |
| K02 | Wolfsberg Private Banking Principles | Wolfsberg Group | resources/legacy/45 | Review Private Banking KYC | Industry principles for AML controls in private banking, including client acceptance, identity and beneficial ownership, source of wealth and funds, additional diligence, prohibited customers, monitoring, responsibilities, controls, and periodic risk assessment. Covers approved topics 7, 10–12, and 17. | article | en-US | 35 | 50 | Public Wolfsberg Group resource with downloadable PDF; anonymous access; no payment or sign-in required. | https://wolfsberg-group.org/resources/legacy/45 | https://wolfsberg-group.org/resources | HTTP 200 with the Course validator user agent on 2026-08-17. |

## Topic Coverage

| Topic | Candidate IDs | Gap or overlap |
| --- | --- | --- |
| Enterprise and customer ML/TF risk assessment | K01, K02 | K01 is broader across banking products and customers; K02 focuses on private banking. |
| Customer identification, beneficial ownership, SDD, CDD, and EDD | K01, K02 | Both cover due diligence; K01 supplies the more complete regulatory framework. |
| Ongoing monitoring, high-risk countries, products, and delivery channels | K01 | K01 is the clear fit for general banking and digital channels. |
| Private banking, source of wealth, and source of funds | K02 | K02 is stronger in the wealth-management context but too narrow as the only KYC Source. |
| Current EU institutional context | K01 | EBA states that AML/CFT responsibilities moved to AMLA on 1 January 2026 and that existing EBA guidance remains valid until AMLA replaces it. |

## Recommendation

Select **K01** as the replacement for C06. It most closely preserves the original risk-based banking scope, activity name, and 90-minute allocation. The Course must describe it as an EU example within the approved international baseline and note the 2026 transfer of EU-level AML/CFT responsibility from EBA to AMLA.

K01 keeps the complete ordered path at **700 minutes**. K02 would reduce it to **660 minutes** and leave general retail, business, and digital-channel KYC under-covered.

## Excluded Candidates

| Source | Reason |
| --- | --- |
| C06: Risk-Based Approach for the Banking Sector — FATF | Browser-accessible but consistently returns HTTP 403 to the required automated Source availability check, including its direct PDF. |
| AMLA Regulatory Instruments | Current and publicly accessible, but primarily an inventory of existing and forthcoming instruments rather than a coherent beginner learning Source. |
| Bank of England CNRF Know Your Customer Questionnaire | Useful operational checklist, but too narrow and context-specific to replace general KYC/CLM and AML/CFT guidance. |

## Course Requester Selection

Status: Selected on 2026-08-17

Selected replacement: **K01**.

Final ordered Source path: **C09, C01, C02, C03, C04, R01, K01, C07, C08, C10**.

Selection note: K01 replaces C06 at the same position and with the same 90-minute Estimated Activity Duration. The complete selected path remains 700 minutes.
