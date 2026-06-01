# Trust Center Content

**Pillar:** 06-evidence-and-audit
**Owner (function):** GRC (accountable). Security and Legal/Privacy review before public. Sales consumes.
**Depends on:** [`evidence-architecture.md`](./evidence-architecture.md), [`auditor-narrative-template.md`](./auditor-narrative-template.md)

## Purpose

The trust center is the customer-facing view of the same controls the auditor sees. It is rendered from the control library and the computed evidence, not written separately, so the public posture and the audit evidence cannot diverge. The customer sees current state, not a quarter-end assembly. Trust-collateral generation for sales is detailed in 07-stakeholder-management; this file defines what the trust center says and how it is produced.

## The principle

One control, many renderings. The auditor narrative and the trust-center entry are two views of one control. The trust center is the public, summarized view; the auditor narrative is the detailed, evidence-referenced view. Both render from the same source, so a claim on the trust center is always backed by an enforced control and a computed record. The marketing line and the audit evidence never diverge.

## What renders to the public trust center

| Section | Rendered from | Example for this configuration |
|---------|---------------|-------------------------------|
| Certifications | Control library status + attestation register | SOC 2 Type II, ISO 27001 status; reports on request under NDA |
| Subprocessor list | Third-party register (03-tprm), reconciled | Current subprocessors and residency posture |
| Data handling | `PRI-03.13`, `AAT-01` statements | Verifiable parental consent governs children's data; agent access scoped and logged |
| Access control | `IAC-17` statement | Least-privilege, periodic access reviews, logging |
| Monitoring and IR | `MON-01`, `IRO-01` statements | Continuous monitoring; incident-response program and breach-notification commitment |
| Responsible AI | Responsible-AI statement (04-ai-governance) | What data does and does not train models; where a human stays accountable |

Each section is a summary-level statement. The detail that would expose a gap, a remediation timeline, or sensitive architecture stays out of the public view and routes to GRC under NDA, consistent with the sales FAQ in 07-stakeholder-management.

## How content is generated and published

1. A control moves to operating status and passes evidence validation.
2. The trust-center renderer reads the control statement and current status from the library.
3. AI drafts the customer-facing summary from the control statement. The draft is not public.
4. Security and Legal/Privacy review the diff for accuracy and for anything that should not be public.
5. The change is published only through a merged pull request. The human reviews the diff before it goes public; the merge is the authorization.

This is the `trust-center-updater` pattern: a control moving to operating triggers a proposed trust-center update, and a human reviews the diff before it goes live. No public claim updates itself without review.

## The claim-to-control trace

Every public claim carries an internal trace back to the control and the computed record that backs it. The trace is not published, but it exists, so that any claim can be defended:

```text
public claim ("verifiable parental consent governs children's data")
   -> control PRI-03.13 (statement)
      -> computed evidence (consent register, ai_generated: false)
         -> auditor narrative (detailed view)
```

If a control's evidence drifts (a check fails, an Issue opens via `MON-01`), the trace is what flags that a public claim may no longer hold, prompting review before the next render.

## Honest history (this configuration)

For matters of public record, the trust center addresses rather than denies. Where there has been public scrutiny, the customer-facing posture points to the current, published commitments and routes legal specifics to Legal under NDA. The trust center never minimizes a matter of public record; it states the current commitment and lets the controls and evidence carry it. The handling of such questions in a sales setting is specified in the sales FAQ.

## What the trust center is not

- It is not a place for internal readiness assessments or open remediation. Those route under NDA.
- It is not authored marketing detached from evidence. Every line traces to a control.
- It is not updated by a model without human review.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC2.2, CC2.3 |
| ISO/IEC 27001:2022 | 7.4 |
| NIST CSF 2.0 | GV.OC, GV.OV |
