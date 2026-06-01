# Trust Collateral

**Pillar:** 07-stakeholder-management
**Owner (function):** GRC (accountable). Sales consumes. Security and Legal/Privacy review before anything is public or shared.
**Depends on:** [`../06-evidence-and-audit/trust-center-content.md`](../06-evidence-and-audit/trust-center-content.md), [`sales-faq.yaml`](./sales-faq.yaml), [`stakeholder-map.yaml`](./stakeholder-map.yaml)

## Purpose

Trust collateral is the set of customer-facing artifacts sales uses to answer security and AI questions: the trust brief, the prevetted questionnaire answers, and the objection-handling notes. All of it is generated from the same control library that the auditor sees, so the answer a prospect receives and the evidence an auditor samples are two renderings of one truth. This file explains how that collateral is produced and kept honest.

## The generation chain

```text
control library (02-controls)
   |  one control, defined once
   v
computed evidence (06-evidence-and-audit, ai_generated: false)
   |
   +--> auditor narrative (detailed, evidence-referenced)
   |
   +--> trust center entry (public, summarized)   <- trust-center-content.md
   |
   +--> trust collateral (sales-facing)            <- this file
           |
           +--> trust brief (the prevetted summary)
           +--> sales FAQ share/withhold (sales-faq.yaml)
           +--> questionnaire first-drafts (SIG, CAIQ, custom)
```

Every artifact at the bottom traces to a control at the top. Collateral is never authored independently of the controls; it is rendered from them.

## The artifacts

### Trust brief

A one-to-two page summary a prospect can receive without an NDA. It states the certifications, the data-handling posture, the access and monitoring controls, and the responsible-AI statement, each at summary level. It is the share column of the sales FAQ, assembled into a document. It carries nothing from the withhold column.

### Prevetted sales FAQ

The questions a buyer asks about location and family data, each with a share answer and a withhold boundary, in [`sales-faq.yaml`](./sales-faq.yaml). Sales answers the routine 80 percent from the share column. The sensitive 20 percent routes to GRC, and where noted to Legal and Privacy, under NDA. Sales never characterizes incident history, legal strategy, or a control gap from memory.

### Questionnaire first-drafts

For SIG, CAIQ, and common custom questionnaires, the answers are pre-mapped from the framework crosswalk. AI drafts the response set from the controls and their evidence; GRC reviews and completes the custom items; anything that would expose a gap or sensitive architecture is staged for an NDA-gated follow-up rather than answered in a non-NDA questionnaire.

## The 80/20 split

| Share (routine 80 percent) | Withhold / route under NDA (sensitive 20 percent) |
|----------------------------|---------------------------------------------------|
| Certification status | Full SOC 2 report, exceptions, bridge letter |
| Summary control descriptions | Access-control matrix, privileged-access inventory |
| Published subprocessor list | Contract terms, residency architecture, transitions |
| Consent posture for children's data | Internal readiness assessments, open remediation |
| IR program and breach-notice commitment | Specific past-incident detail, post-incident reports |
| Responsible-AI statement | Data-flow diagrams, model details, control mappings |

The split is not improvised per deal. It is prevetted and recorded, so the routine answer is ready and consistent and nobody re-answers the same question from scratch. This is the fatigue reduction that the stakeholder map names as the deliverable for sales.

## How collateral stays honest

- **One source.** Collateral renders from the control library and computed evidence, so it cannot drift from the audit evidence.
- **The claim-to-control trace.** Every public claim traces back to a control and a record (the trace in `trust-center-content.md`). A claim with no backing record is removed before publication.
- **Human review before public or shared.** Security and Legal/Privacy review the diff. Publication or release happens only through a merged pull request; the merge is the authorization.
- **Drift flags review.** When a control drifts and an Issue opens (`MON-01`), the trace flags any collateral that leaned on that control, prompting review before it is used again.

## Honest history in a sales setting

For matters of public record, collateral follows the trust center's honest-history posture: address directly, point to the current published commitments, and route legal specifics to Legal under NDA. Collateral never denies or minimizes a matter of public record. Sales acknowledges and routes; Legal leads the substance.

## What this is not

- Not marketing detached from evidence.
- Not a place where sales improvises sensitive answers.
- Not updated by a model without human review.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC2.2, CC2.3 |
| ISO/IEC 27001:2022 | 7.4 |
| NIST CSF 2.0 | GV.OC, GV.RR |
