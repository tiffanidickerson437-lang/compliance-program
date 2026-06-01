# Continuous Evidence

**Pillar:** 06-evidence-and-audit
**Control anchor:** [`MON-01`](../02-controls/control-library.yaml), Continuous monitoring
**Owner (function):** GRC (accountable). Source-system owners (Security, Engineering, IT, Legal/Privacy) keep feeds live.
**Depends on:** [`evidence-architecture.md`](./evidence-architecture.md), [`poam-as-issues.md`](./poam-as-issues.md)

## Purpose

Make audit readiness a standing state instead of a sprint. Evidence is computed continuously from systems of record, validated against schema, and surfaced as control health. When a control drifts, an Issue opens. When it is fixed, a merge flips the status. Audit prep becomes a dashboard check because the evidence was never allowed to go stale.

## The loop

```text
systems of record
   |  (continuous)
   v
compute evidence  -->  validate against schema (ai_generated: false)
   |                        |
   |                        +-- fails --> build fails / Issue opens (finding)
   v
control health updated
   |
   +-- healthy --> trust center + auditor narrative render current state
   |
   +-- drift --> GitHub Issue (the due-diligence record) --> PR --> merge --> status flips
```

This is the operating model from the program charter, expressed as the evidence loop: continuous check, drift opens an Issue, the PR is the gate, status flips on merge, git history is the audit trail.

## Continuous versus point-in-time

| Dimension | Point-in-time | Continuous (this program) |
|-----------|---------------|---------------------------|
| When evidence exists | Assembled at audit | Always, computed from source |
| What audit prep is | A scramble | A dashboard check |
| How drift is found | At the next audit | The day it happens, via an Issue |
| What the auditor gets | Reconstructed narratives | Computed records for the period |
| First-submission acceptance | Hoped for | The design goal |

## Control-health computation

Each control's health is computed from its named system of record (the per-control source map in [`evidence-architecture.md`](./evidence-architecture.md)):

- A control is **healthy** when its current computed record passes schema and shows no breached threshold.
- A control is **drifting** when a check trips (a key not rotated, retention changed, an access review overdue, a vendor rating dropped, an attestation expired).
- Drift opens an Issue labeled `evidence` via `.github/workflows/control-drift-monitor.yml`. The Issue carries control ID, drift type, owner (function), framework impact, and the evidence needed to close.

## Exception aging

Continuous evidence includes the aging of open exceptions and findings, tracked as Issues per [`poam-as-issues.md`](./poam-as-issues.md). Aging is computed, not estimated: each open item carries its open date and target date, and the age is the difference. The aging view is what turns a quiet backlog into a visible obligation and feeds the executive and board reporting in 07-stakeholder-management.

## Readiness as a computed score

Audit readiness is a computed roll-up, not a feeling:

- Percentage of in-scope controls with a current, schema-valid evidence record.
- Count of open drift Issues by severity and age.
- Count of exceptions past target date.
- Attestations and certificates expiring within the next cycle (from 03-tprm and the control library).

When the roll-up is green across the in-scope framework set, fieldwork can start. The audit-readiness checklist is this roll-up made explicit; every item green before fieldwork begins.

## What stays human

Computation and validation are automated. The seam stays human:

- A human approves the auditor narrative before it leaves the building.
- A human reviews and merges every status change and trust-center update.
- A human, on behalf of the business, accepts any residual risk rather than remediating.

AI drafts and computes; a person decides what matters and where accountability stays. The evidence loop never lets a model author evidence or approve its own work.

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC4.1, CC4.2, CC7.2 | Ongoing monitoring of controls. |
| ISO/IEC 27001:2022 | 9.1, 9.2, 9.3 | Monitoring, internal audit, management review. |
| NIST SP 800-53 | CA-7 | Continuous monitoring. |
| NIST CSF 2.0 | DE.CM, GV.OV | Continuous monitoring and oversight. |
| SOX ITGC | Ongoing evidence of control operation | Framework-mapped, home lab, never audited. |
