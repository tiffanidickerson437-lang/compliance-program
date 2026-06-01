# POA&M as Issues

**Pillar:** 06-evidence-and-audit
**Owner (function):** GRC (accountable). Finding owners (function) remediate.
**Mechanism:** [`MON-01`](../02-controls/control-library.yaml), drift opens an Issue; remediation lands by pull request.

## Purpose

A Plan of Action and Milestones (POA&M) is the discipline of tracking a finding from discovery to closure with an owner, a corrective action, and a date. This program implements that discipline natively: a finding is a GitHub Issue, its remediation is a pull request, and its closure is a merge. The Issue is the evidence of due diligence, and git history is the audit trail.

## A clarification on scope

This is POA&M the concept, not a federal POA&M artifact. The program borrows the rigor of the POA&M model (every finding owned, tracked, and closed) without producing a FedRAMP or FISMA POA&M document. If a future framework requires that specific artifact, it is rendered from the same Issues, the same way any framework view is rendered from the one control set. The concept is owned here; the federal format is a mapping if and when it is needed.

## The lifecycle

```text
finding discovered
   |  (drift check, audit, pen test, vendor review, self-identified)
   v
GitHub Issue opened, labeled "evidence"
   |  control ID, finding type, owner (function), framework impact,
   |  severity, corrective action, target date, evidence-to-close
   v
remediation work
   |  AI drafts the remediation plan and narrative; human reviews
   v
pull request opened
   |  the fix and the updated evidence/status
   v
human review + merge
   |  the merge is the authorization; status flips
   v
Issue closed, linked to the merging PR
   (git history is the audit trail)
```

## The finding record (Issue fields)

Every finding Issue carries the fields a POA&M would, so the Issue is a complete record on its own:

| Field | Meaning |
|-------|---------|
| Control ID | Which control the finding relates to (e.g., `CHG-02`) |
| Finding type | Drift, exception, audit finding, vendor gap, vulnerability |
| Owner (function) | Who is accountable for closing it; never a personal name |
| Severity | Risk-rated; feeds prioritization |
| Framework impact | Which frameworks the gap touches, from `framework-crosswalk.yaml` |
| Corrective action | What will be done to close it |
| Target date | When closure is due |
| Evidence to close | The computed record that will prove closure |
| Status | Open, in remediation, in review (PR open), closed |

## Why the Issue is the evidence

An auditor asking "how do you handle findings?" receives the Issue history: every finding, when it opened, who owned it, what was done, and the merge that closed it, all timestamped and immutable. There is no separate tracker to reconcile and no narrative to reconstruct. The due-diligence record is a byproduct of doing the work in the open. This is the `MON-01` drift-opens-an-issue mechanism, generalized to every finding source.

## Aging and exception handling

- Open findings age against their target date. Aging is reported in 07-stakeholder-management and surfaced on the executive view.
- An overdue finding is itself a signal; it does not silently roll forward. The aging report makes overdue items visible to the owning function and to GRC.
- A finding accepted as residual risk rather than remediated becomes an exception under `00-governance/exceptions-process.md`, with the business owning the acceptance, consistent with the risk-appetite split: the business decides, GRC informs.

## Integration with intake and drift

| Source of finding | How it arrives |
|-------------------|----------------|
| Control drift | `.github/workflows/control-drift-monitor.yml` opens the Issue automatically |
| Failed evidence validation | `.github/workflows/evidence-validator.yml` fails the build; the gap becomes a finding |
| Vendor monitoring | 03-tprm continuous monitoring opens an Issue on attestation/observable drift |
| Audit or pen test | Logged as a finding Issue with the same fields |
| Self-identified | Anyone opens an Issue with the finding template |

All converge on one lifecycle: Issue to PR to merge.

## What this prevents

- Findings tracked in a spreadsheet that drifts from reality.
- A remediation claimed but not evidenced; closure requires the merged PR carrying the proof.
- A model closing its own finding; the human gate is the merge.

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC4.2, CC3.4 | Remediation of deficiencies. |
| ISO/IEC 27001:2022 | 10.1, 10.2 | Nonconformity and corrective action. |
| NIST SP 800-53 | CA-5 | Plan of action and milestones. |
| NIST CSF 2.0 | ID.IM, GV.OV | Improvement and oversight. |
| SOX ITGC | Deficiency tracking | Framework-mapped, home lab, never audited. |
