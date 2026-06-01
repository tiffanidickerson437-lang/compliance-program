# Vendor Tiering Model

**Pillar:** 03-tprm
**Control anchor:** [`TPM-01`](../02-controls/control-library.yaml), Third-party management
**Owner (function):** GRC (accountable). Legal and Privacy on contract terms. Security and Engineering consulted on real data and access.
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).

## Purpose

Right-size third-party diligence so the depth of an assessment matches what a vendor can actually touch, not how large the contract is or how loudly the business wants the deal closed. The tier a vendor lands in decides one thing: which intake route it follows in [`tiered-intake-workflow.md`](./tiered-intake-workflow.md). Tiering is the gate that prevents a full assessment from becoming the default.

## The principle that governs every assignment

Criticality is one input, not the gate. A vendor that is critical to operations but cannot touch sensitive data and holds no production access does not earn a deep review. A small subprocessor that ingests precise location for tens of thousands of accounts does, even on a modest contract. Tier follows exposure. Spend, brand, and urgency do not move a tier on their own.

## The four scoring dimensions

Every vendor is scored on four dimensions. Each dimension is scored independently before any tier is proposed. No single business stakeholder owns more than one dimension, so no one function can inflate or deflate a tier alone.

### 1. Data sensitivity (what classification the vendor can touch)

| Band | Score | Definition for this configuration |
|------|-------|-----------------------------------|
| Restricted | 4 | Precise/real-time location, children's or minors' data, the location relationship graph, government ID, or biometric data. |
| Confidential | 3 | Adult PII, account credentials, payment data, support content containing personal data. |
| Internal | 2 | Pseudonymized or aggregated analytics, non-personal operational telemetry, internal business data. |
| Public | 1 | Only data already published or fully anonymized with no re-identification path. |
| None | 0 | No access to any company or customer data. |

Data sensitivity is the dominant dimension. Restricted data is the single strongest signal in the model. See the override rule below.

### 2. Access level (what the vendor can reach and do)

| Band | Score | Definition |
|------|-------|------------|
| Privileged / write | 4 | Standing production write, admin, or infrastructure control; can change systems or move data at will. |
| Production read | 3 | Standing read into production data stores or live customer data. |
| Scoped / brokered | 2 | Time-bound or purpose-bound access through a broker, no standing entitlement. |
| Metadata / integration | 1 | Receives derived events or metadata only; no direct store access. |
| None | 0 | No system access; offline or commercial relationship only. |

Standing access scores higher than brokered access by design. A vendor reached only through a purpose-bound, short-lived token (the pattern enforced for agents in `AAT-01`) is lower exposure than one holding a standing entitlement to the same data.

### 3. Business dependency (how hard the vendor is to replace or live without)

| Band | Score | Definition |
|------|-------|------------|
| Irreplaceable / single-source | 4 | No substitute; outage halts a core service; switching takes quarters. |
| High | 3 | Substitutes exist but switching is costly or slow. |
| Moderate | 2 | Replaceable within weeks with planning. |
| Low | 1 | Commodity; swap is routine. |
| None | 0 | Discretionary; removal has no operational effect. |

This dimension informs continuity and concentration planning, captured in [`continuous-monitoring.md`](./continuous-monitoring.md) and the fourth-party note. On its own it never forces a Tier 1. A single-source vendor that touches no sensitive data and holds no production access is a continuity risk to manage, not a deep-review trigger.

### 4. Breach impact (blast radius if the vendor is compromised)

| Band | Score | Definition |
|------|-------|------------|
| Severe | 4 | Compromise exposes restricted data at scale, triggers regulatory notification (COPPA, GDPR, CCPA), or enables takeover of customer accounts. |
| High | 3 | Compromise exposes confidential PII or enables material service disruption. |
| Moderate | 2 | Limited personal-data exposure or recoverable disruption. |
| Low | 1 | Contained operational impact, no personal data. |
| Negligible | 0 | No realistic harm to customers or the company. |

Breach impact is scored against the worst credible scenario, not the expected case. For a vendor touching children's location data, the worst credible scenario is severe by definition.

## From scores to tier

Compute the tier from the dimension scores using the rules below, applied in order. The first rule that matches assigns the tier.

1. **Restricted-data override.** If data sensitivity is Restricted (4) **or** access level is Privileged/write (4) into systems holding personal data, the vendor is **Tier 1**. This override exists so that touching precise location or children's data, or holding write access over it, cannot be argued down by a low score elsewhere.
2. **Severe breach impact.** If breach impact is Severe (4), the vendor is at least **Tier 1** unless data sensitivity is None and access level is None, in which case it is **Tier 2** and flagged for concentration review.
3. **Weighted band for the rest.** For vendors not pinned by rules 1 or 2, compute a weighted score:

   `weighted = (data_sensitivity x 0.40) + (access_level x 0.30) + (breach_impact x 0.20) + (business_dependency x 0.10)`

   | Weighted score | Tier |
   |----------------|------|
   | >= 3.0 | Tier 1 |
   | 2.0 to 2.99 | Tier 2 |
   | 1.0 to 1.99 | Tier 3 |
   | < 1.0 | Tier 4 |

The weights encode the principle: data sensitivity and access together carry 70 percent of the weighted decision; business dependency carries 10 percent. Criticality cannot, by arithmetic alone, lift a low-exposure vendor into deep review.

## Tier definitions and the route each takes

| Tier | Meaning | Intake route | Reference |
|------|---------|--------------|-----------|
| Tier 1 | Touches restricted data or holds privileged access; severe blast radius. | Deep review. | [`tier1-deep-review.md`](./tier1-deep-review.md) |
| Tier 2 | Touches confidential PII or holds production read; high but bounded blast radius. | Attestation review first; light questionnaire only for gaps the attestation does not cover. | [`attestation-reuse-register.yaml`](./attestation-reuse-register.yaml) |
| Tier 3 | Limited PII or scoped/brokered access. | Light questionnaire (SIG Lite), or attestation review if a current report exists. | [`siglite-low-tier.md`](./siglite-low-tier.md) |
| Tier 4 | No sensitive data, no production access. | Attestation acceptance or inherent-risk screen; SIG Lite only if any doubt. | [`siglite-low-tier.md`](./siglite-low-tier.md) |

Nobody gets a full custom questionnaire by default. The full SIG Core and data-flow review are reserved for Tier 1.

## Restricted-data anchoring (this configuration)

Tier 1 is anchored to vendors and subprocessors that touch precise location or children's data (the location graph), where breach impact is severe, and to foundation-model providers whose terms govern whether customer data trains a model. Tier 1 is not anchored to contract size. A high-spend marketing or finance tool that never receives location-graph data is Tier 2 or lower. A small analytics subprocessor that ingests real-time location is Tier 1. The published subprocessor list stays in sync with this register so the public trust center and the internal tier never diverge (see [`continuous-monitoring.md`](./continuous-monitoring.md)).

## Worked examples

| Vendor profile | Data | Access | Dependency | Breach | Tier | Why |
|----------------|------|--------|------------|--------|------|-----|
| Location-analytics subprocessor (real-time coordinates) | 4 | 3 | 2 | 4 | Tier 1 | Restricted-data override fires; exposure, not size. |
| Foundation-model API provider on the location-graph agent | 4 | 2 | 3 | 4 | Tier 1 | Restricted data plus model-training terms; deep review on data-use and exit. |
| Enterprise CRM holding adult PII | 3 | 3 | 3 | 3 | Tier 2 | Confidential PII and production read; attestation reuse fits. |
| High-spend ad-measurement tool (aggregated only) | 2 | 1 | 3 | 2 | Tier 3 | High dependency, but no sensitive data; criticality does not promote it. |
| Office-supplies vendor | 0 | 0 | 1 | 0 | Tier 4 | No data, no access; inherent-risk screen only. |

The ad-measurement row is the point of the model: high business dependency, low exposure, no deep review.

## The human gate (AI drafts, human validates)

AI drafts the gap analysis from the vendor's SOC 2 Type II or ISO 27001 report, extracts the scope and exception list, and proposes the four dimension scores and a tier. The draft is a proposal, never a record. A human GRC owner validates data sensitivity and access against what the vendor actually receives, confirms the scope and exceptions, and sets the tier. The tier becomes a record only on a merged pull request to the third-party register. The pull request is the gate; the merge is the authorization; git history is the audit trail. This mirrors the program-wide operating model and the `TPM-01` constraint.

## Reassessment triggers (a tier is not permanent)

Re-tier on any of the following, tracked through [`continuous-monitoring.md`](./continuous-monitoring.md):

- The vendor begins receiving a higher data classification or gains broader access.
- A security-rating drop or breach disclosure changes breach impact.
- A subprocessor or model-training term changes.
- Renewal, where the prior tier and its evidence are re-confirmed.

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC1.4, CC2.3 | Vendor risk identification and assessment. |
| ISO/IEC 27002:2022 | 5.19, 5.21, 8.3 | Supplier relationships and ICT supply chain. |
| NIST CSF 2.0 | GV.SC-04, GV.SC-06, GV.SC-07 | Supplier criticality, pre-engagement assessment. |
| NIST AI RMF 1.0 | MANAGE 3.0 | Third-party and model-provider risk. |
| CCPA / CPRA (2026) | §7052(a) | Service-provider and contractor obligations. |
| SOX ITGC | Vendor access in scope | Framework-mapped, home lab, never audited. |
