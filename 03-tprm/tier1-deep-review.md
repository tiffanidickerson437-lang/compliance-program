# Tier 1 Deep Review

**Pillar:** 03-tprm
**Control anchor:** [`TPM-01`](../02-controls/control-library.yaml), Third-party management
**Owner (function):** GRC (accountable). Security on technical evidence. Legal and Privacy on terms. Engineering confirms real data flow.
**Reserved for:** Tier 1 vendors only.
**Depends on:** [`vendor-tiering-model.md`](./vendor-tiering-model.md), [`tiered-intake-workflow.md`](./tiered-intake-workflow.md)

## Purpose

Deep review is the heaviest diligence the program runs, and it is reserved for the few vendors that can cause the most harm: those that touch restricted data (precise location, children's or minors' data, the location relationship graph), hold privileged or write access, or whose compromise would force regulatory notification. A current attestation is an input to deep review, never a substitute for it.

## What pins a vendor to Tier 1

A vendor reaches deep review through the tiering model when any of these is true:

- Data sensitivity is Restricted (precise location or children's data), which fires the restricted-data override.
- Access level is Privileged/write into systems holding personal data.
- Breach impact is Severe (regulatory-notification trigger or account takeover at scale).
- The weighted score is at or above 3.0.

For this configuration, deep review concentrates on location-data subprocessors, children's-data processors, and foundation-model providers whose terms decide whether customer data trains a model.

## The deep-review package

### 1. Full SIG Core

The complete Standardized Information Gathering questionnaire across all domains, not the Lite subset. The vendor's answers are read against evidence, not accepted at face value. A current SOC 2 Type II or ISO 27001 report is used to pre-fill and corroborate answers, and its scope, exceptions, and complementary user-entity controls are logged in [`attestation-reuse-register.yaml`](./attestation-reuse-register.yaml) as input to, not closure of, the review.

### 2. Data-flow review

A mapped diagram of exactly what data the vendor receives, where it travels, where it rests, and who downstream can reach it:

- Data classes received, confirmed by Engineering against the real integration, not the contract aspiration.
- Storage regions and whether restricted data leaves an agreed jurisdiction.
- Onward subprocessors and the fourth-party chain (see the fourth-party note).
- Whether precise location or children's data is in scope, and the lawful basis, consistent with `PRI-03.13` and `AAT-01`.
- Retention and the deletion path on termination, validated later through offboarding evidence.

### 3. Encryption and access evidence

Evidence, not assertions:

- Encryption in transit and at rest, with key-management ownership stated.
- Access model into any company or customer data: standing versus brokered, MFA, least privilege, and whether the vendor's staff can read restricted data.
- Logging of vendor access sufficient to reconstruct who reached what and when.
- For a model provider: whether customer data trains the model, retention of prompts and outputs, and the inference subprocessor chain.

### 4. Documented remediation path

Every gap that is not a hard stop is written down with an owner (function), a corrective action, a due date, and the evidence that will close it. Hard stops (restricted data exported to an un-agreed region, no encryption at rest for personal data, training on customer data without opt-out) block onboarding until resolved. Open items are tracked the same way the program tracks its own findings: as GitHub Issues, so the Issue is the due-diligence record.

## The human gate and the record

AI drafts the gap analysis from the SIG Core responses and the attestation, proposes a risk rating, and produces a remediation list. None of this is a record. A human GRC owner validates the data-flow against what Engineering confirms, accepts or rejects each remediation, and signs the risk decision. The assessment becomes a record only on a merged pull request to the third-party register. The merge is the authorization; git history is the audit trail. Tier 1 outcomes feed the high-cadence path in [`continuous-monitoring.md`](./continuous-monitoring.md).

## Contract terms that must land (Legal and Privacy)

Deep review does not close until the executed contract carries:

- A data-processing agreement with processing limited to the stated purpose.
- A breach-notification window short enough to meet the company's own statutory clocks (`IRO-01`).
- Subprocessor flow-down and a change-notice obligation.
- Audit or evidence rights proportional to the exposure.
- For model providers: a no-train-on-customer-data term where available, retention limits, model-update notice, and exit and data-return terms.

The executed clauses are the evidence, pulled from the contract system of record, consistent with the `TPM-01` schema.

## Reassessment

Tier 1 vendors reassess on the shortest cadence and are continuously cross-referenced against security ratings. A rating drop, a breach disclosure, or a subprocessor change triggers an off-cycle review through [`continuous-monitoring.md`](./continuous-monitoring.md).

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC1.4, CC2.3, CC9.2 | Vendor assessment and management. |
| ISO/IEC 27002:2022 | 5.19, 5.20, 5.21, 5.22, 8.3 | Supplier relationships, ICT supply chain, access restriction. |
| NIST CSF 2.0 | GV.SC-04, GV.SC-06, GV.SC-07, GV.SC-10 | Critical-supplier assessment and lifecycle. |
| NIST AI RMF 1.0 | MANAGE 3.0 | Foundation-model and third-party AI risk. |
| GDPR | Art. 28 | Processor obligations and subprocessor flow-down. |
| CCPA / CPRA (2026) | §7052(a) | Service-provider and contractor terms. |
