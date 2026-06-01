# EU AI Act readiness

How the program prepares for Regulation (EU) 2024/1689 (the EU AI Act). The Act takes a risk-based approach: each AI use case is classified, and obligations attach to the class. This document records the classification method, a conservative classification of representative, illustrative use cases, and a gap log against the high-risk obligations that land from August 2 2026 and the general-purpose AI (GPAI) transparency duties.

This is a working model. No claim is made about any real organization's internal classification or posture. The use cases below are representative, classified conservatively, to demonstrate the method.

Direct catalog crosswalk (real reference from `02-controls/framework-crosswalk.yaml`):

| Control | EU AI Act reference |
|---------|---------------------|
| AAT-01 | Art.17(1)(c) |

## The clock

- 1 August 2024: the Act entered into force.
- 2 February 2025: prohibited-practice rules began to apply.
- 2 August 2025: GPAI model obligations began to apply.
- 2 August 2026: the bulk of high-risk obligations apply. This is the date the readiness gap log is built against.
- 2 August 2027: extended timeline for certain product-embedded high-risk systems.

## Risk classification method

Each use case is classified into one of four tiers, and the program defaults to the more conservative tier when a case is borderline, especially where minors or precise location are involved.

| Tier | Test | Program response |
|------|------|------------------|
| Prohibited | Falls under an Article 5 prohibited practice | Do not build. Block at intake. |
| High-risk | Annex III area or safety component, per Article 6 | Apply the full high-risk obligation set below. |
| Limited risk | Interacts with people or generates content (Article 50 transparency) | Disclose AI interaction and label AI-generated content. |
| Minimal risk | None of the above | Standard controls; no Act-specific obligation. |

## Representative classification

| Representative use case | Tier (conservative) | Reasoning |
|-------------------------|---------------------|-----------|
| Autonomous agent acting on a minor's real-time location for a safety alert | Treated to the high-risk standard | Acts on the safety and location of a vulnerable group at machine speed; governed by AAT-01 regardless of final legal classification. |
| Customer-facing conversational assistant | Limited risk | Article 50 transparency: the user is told they are interacting with AI. |
| Internal productivity and drafting AI | Minimal to limited | Governed by the acceptable-use policy; no regulated decision on individuals. |
| Any emotion recognition or biometric categorization | Block pending legal review | Potential Article 5 or high-risk exposure; routed to Legal/Privacy before any build. |

The conservative default means the hardest use case is held to the high-risk standard whether or not the final legal classification requires it. That is a deliberate margin of safety for a family-safety context.

## High-risk obligation gap log

For a use case held to the high-risk standard, the Act sets obligations across Articles 9 through 17. The log maps each to an owned control and records status.

| Obligation (article theme) | Owned control | Status | Notes |
|----------------------------|---------------|--------|-------|
| Risk management system (Art 9) | program risk register + AAT-01 | Operating | FAIR-structured risk register; AI risk governed under AAT-01. |
| Data and data governance (Art 10) | AI data classification (AAT-01) | Operating | Restricted classes for children's and precise-location data; provenance on training and retrieval data. |
| Technical documentation (Art 11) | control library + agent spec | Operating | The control library, agent spec, and DPIA form the technical file. |
| Record-keeping and logging (Art 12) | AAT-01 broker decision records, MON-01 | Operating | Per-action decision records with retention and integrity protection. |
| Transparency to deployers and users (Art 13, Art 50) | responsible-AI statement | Operating | Customer-facing statement plus AI-interaction disclosure. |
| Human oversight (Art 14) | AAT-01 human oversight gate | Operating | Named human approves irreversible or minor-account actions; kill-switch available. |
| Accuracy, robustness, cybersecurity (Art 15) | eval gate (CHG-02), OWASP mapping | Operating | Pre-deploy evaluation, drift checks, and the OWASP LLM Top 10 mitigations. |
| Quality management system (Art 17, incl. 17(1)(c)) | AAT-01, model change management | Operating to forward target | Data-management procedures and record-keeping are operating; a fully documented QMS is a forward target. |
| Post-market monitoring and incident reporting | MON-01, IRO-01 | Operating | Continuous monitoring, drift issues, and AI-incident response with notification path. |

## Art.17(1)(c) mapping

The catalog maps AAT-01 to Art.17(1)(c), the data-management procedures element of the quality management system for providers of high-risk AI. The program reads this as the requirement to have systematic, recorded procedures for how data is handled across the AI life cycle. AAT-01 answers it operationally: data scope is bounded at the authorization broker, restricted classes are carved out, every sensitive read is recorded with what was released and withheld, and changes to data handling pass through model change management. The broker decision record is the evidence that the data-management procedure is enforced, not just written.

## GPAI transparency duties

Where the program consumes a general-purpose AI model from a provider, the GPAI transparency duties are handled on the provider side and verified through TPM-01: the provider's documentation, training-data summary disclosures, and model-update notices are part of the vendor record. Where the program produces content with AI, that content is labeled, satisfying the downstream transparency expectation.

## Readiness posture

Operating now: classification at intake, the high-risk control set for the hardest use case, logging and human oversight, evaluation and monitoring, and AI vendor verification. Forward target: a fully documented quality management system to the letter of Article 17, and a conformity assessment path if a use case is formally classified high-risk. The gap log is the honest record of the distance to that target, maintained as the August 2 2026 date approaches.
