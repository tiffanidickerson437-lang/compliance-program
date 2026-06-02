# Evidence Architecture

**Pillar:** 06-evidence-and-audit
**Control anchors:** all eleven seed controls; mechanism is [`MON-01`](../02-controls/control-library.yaml)
**Owner (function):** GRC (accountable). Security, Engineering, IT, and Legal/Privacy own the source systems.
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).

## Purpose

Define how evidence is produced so it is audit-ready before it ever reaches an auditor. The architecture has one rule that governs everything else: evidence is computed from systems of record, never authored by a model. Audit readiness is a continuous state, not a sprint, and first-submission acceptance is the goal.

## The non-negotiable rule

`ai_generated: false` on every evidence record.

Evidence is collected from the system that already holds the truth: the source-control merge API, the identity provider joined to the HRIS, the consent service, the authorization broker, the SIEM, the vendor register. A model may draft the narrative that explains the evidence (see [`auditor-narrative-template.md`](./auditor-narrative-template.md)), but it may never produce the evidence itself. A record carrying `ai_generated: true` is rejected by schema and fails the build in `.github/workflows/evidence-validator.yml`. This is the line the whole program defends: code decides pass or fail, the record supplies the proof, AI drafts the explanation, a human approves.

## The shape of an evidence record

Every evidence record carries a common envelope plus a control-specific body. The envelope is what the validator checks; the body is what the auditor reads.

```yaml
control: TPM-01                 # which control this evidences
period: 2026-Q2                 # the period covered
source: Vendor Risk tool + CLM  # the system of record it came from
collected_at: 2026-07-01        # when it was computed
method: api_export              # api_export | query | attestation_join
ai_generated: false             # MUST be false; true is rejected
# --- control-specific body below ---
vendors_in_scope: 96
high_risk_current: 18/18
with_executed_dpa: 96/96
overdue_reassessment: 2
```

The envelope fields (`control`, `period`, `source`, `ai_generated`) are required for every record. The body fields are defined per control in the evidence schemas.

## Per-control source map

Each seed control names the system of record that produces its evidence. This is the spine of the architecture.

| Control | System of record | What it computes |
|---------|------------------|------------------|
| AAT-01 | Agent authorization broker + consent service | Broker decision records: trigger, basis, fields released/withheld, TTL, grant/deny |
| PRI-03.13 | Consent service + data-access broker | Consent register per minor account; disclosures without active consent |
| IAC-17 | Identity provider + HRIS | Recertification attestation joined to entitlement snapshot |
| CHG-02 | Source control (branch protection + merge API) | Merge records: linked ticket, independent review, passing checks |
| MON-01 | SIEM + immutable object-lock store | Source coverage, retention, integrity checks, alert acknowledgement |
| TPM-01 | Vendor risk tool + contract lifecycle | Third-party register: tier, assessment, DPA, assurance expiry |
| IRO-01 | Paging + incident tracker + breach-decision log | Incident records with full timeline and notification decision |

A control with no named system of record is not audit-ready. Naming the source is the first design step, not an afterthought.

## Evidence schemas

Per-control schemas live at [`../02-controls/evidence-schemas/`](../02-controls/evidence-schemas/), one file per control, each defining the fields a record must carry, the source system, what separates audit-ready from incomplete, and the `rejected_when` conditions (including `ai_generated: true`). The evidence pillar owns the schema concept; the files sit next to the control library so the control and its evidence contract stay together. Computed records land under `06-evidence-and-audit/evidence-records/`. A schema is the contract the validator enforces in `.github/workflows/evidence-validator.yml`: it checks the envelope, the schema-required fields, and every `const` (so `ai_generated` must equal false). The check is a required status check on any pull request that marks a control operating, so nothing is recorded as operating without passing validation.

## How a record comes to exist

1. A scheduled job or an on-demand query pulls from the system of record (the envelope `method` records which).
2. The raw export is shaped into the schema for that control.
3. The validator checks the envelope and body against the schema, including `ai_generated: false`.
4. A human reviews the computed record and the drafted narrative.
5. The record is recorded through a merged pull request. The merge is the authorization; git history is the audit trail.

A failed validation does not silently pass; it fails the build and lists the gap.

## What this prevents

- A polished narrative with no underlying record. The narrative cannot be filed without the computed evidence it references.
- Quarter-end assembly. The record exists continuously because the source system is always on; audit prep is a dashboard check, not a fire drill.
- Drift between claim and reality. The trust center and the auditor narrative both render from the same computed records, so the public claim and the audit evidence cannot diverge (see [`trust-center-content.md`](./trust-center-content.md)).

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC4.1, CC4.2 | Monitoring and evaluation of controls. |
| ISO/IEC 27001:2022 | 9.1, 9.2 | Monitoring, measurement, internal audit. |
| NIST CSF 2.0 | GV.OV, DE.CM | Oversight and continuous monitoring. |
| NIST SP 800-53 | CA-7 | Continuous monitoring of control effectiveness. |
| SOX ITGC | Evidence of control operation | Framework-mapped, home lab, never audited. |
