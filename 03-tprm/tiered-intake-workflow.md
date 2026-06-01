# Tiered Intake Workflow

**Pillar:** 03-tprm
**Control anchor:** [`TPM-01`](../02-controls/control-library.yaml), Third-party management
**Owner (function):** GRC (accountable). Procurement initiates intake. Engineering and Security confirm real data and access. Legal and Privacy on terms.
**Depends on:** [`vendor-tiering-model.md`](./vendor-tiering-model.md)

## Purpose

One intake form routes every vendor to exactly one of three review depths: attestation review, light questionnaire, or deep review. The route is decided by tier, and the tier is decided by exposure. Nobody gets a full assessment by default. The intake exists to make the cheap path the common path and to reserve effort for the few vendors that can actually cause harm.

## The single intake

A requester (any function procuring a third party) completes one short form before access or contract signature. The intake captures only what is needed to tier and route:

1. Vendor name, the service, and the business requester (function, not a person).
2. What data the vendor will receive, by classification (restricted, confidential, internal, public, none). Engineering confirms; the requester does not self-certify down.
3. What access the vendor will hold (privileged/write, production read, scoped/brokered, metadata, none).
4. Business dependency and whether a substitute exists.
5. Whether the vendor processes data on the location graph, precise location, or children's/minors' data.
6. Whether the vendor is a subprocessor or a foundation-model provider.
7. Existing assurance the vendor can provide (SOC 2 Type II, ISO 27001, pen-test letter, CAIQ).

The intake opens a tracked work item in the ticketing system of record. From this point the item is the case file; its state and history are the evidence that diligence happened.

## Routing logic

```text
intake submitted
   |
   v
score 4 dimensions  -->  vendor-tiering-model.md
   |
   v
assign tier (human-validated)
   |
   +-- Tier 1  --> DEEP REVIEW            (tier1-deep-review.md)
   |                full SIG Core, data-flow review, encryption and
   |                access evidence, documented remediation path
   |
   +-- Tier 2  --> ATTESTATION REVIEW     (attestation-reuse-register.yaml)
   |                accept current SOC 2 Type II or ISO 27001 + pen-test
   |                letter; light questionnaire only for uncovered gaps
   |
   +-- Tier 3  --> LIGHT QUESTIONNAIRE    (siglite-low-tier.md)
   |                SIG Lite; or attestation review if a current report exists
   |
   +-- Tier 4  --> INHERENT-RISK SCREEN   (siglite-low-tier.md)
                    attestation acceptance or short screen; SIG Lite only on doubt
```

## What each route requires

### Attestation review (Tier 2 default)

The default path for the largest share of vendors. The reviewer accepts a current SOC 2 Type II or ISO 27001 certificate plus a pen-test attestation letter in lieu of a custom questionnaire, then reads the report for scope fit, exceptions, complementary user-entity controls, and the bridge-letter gap. Only the items the attestation does not cover become a short, targeted follow-up. The reuse decision, scope, and exceptions are logged in [`attestation-reuse-register.yaml`](./attestation-reuse-register.yaml). This is the mechanism that keeps full questionnaires rare.

### Light questionnaire (Tier 3)

SIG Lite as the screen for vendors with limited or scoped data access. If the vendor already holds a current attestation, the reviewer uses attestation review instead and skips the questionnaire. Detail in [`siglite-low-tier.md`](./siglite-low-tier.md).

### Deep review (Tier 1 only)

Reserved for vendors that touch restricted data or hold privileged access. Full SIG Core, a data-flow review, encryption and access evidence, and a documented remediation path with owners and dates. Detail in [`tier1-deep-review.md`](./tier1-deep-review.md).

## The human gate and the record

AI drafts at three points: it proposes the tier from the intake and any uploaded report, it produces the gap analysis on an attestation, and it drafts the risk summary. None of these is a record. A human GRC owner reviews each, and the assessment becomes a record only when a pull request to the third-party register is merged.

- Drift or a missed reassessment opens a GitHub Issue. That Issue is the evidence of due diligence.
- The assessment outcome and tier land through a pull request. The merge is the authorization. Git history is the audit trail.

This is the same operating model the whole program runs on, applied to vendors.

## Service-level expectations by route

| Route | Target time to decision | Human effort | Reused evidence |
|-------|------------------------|--------------|-----------------|
| Inherent-risk screen (Tier 4) | 1 to 2 business days | Minimal | Attestation if offered |
| Attestation review (Tier 2) | 3 to 5 business days | Read report, log scope and exceptions | SOC 2 / ISO + pen-test |
| Light questionnaire (Tier 3) | 5 to 10 business days | Review SIG Lite responses | Attestation if offered |
| Deep review (Tier 1) | 2 to 4 weeks | Full assessment and evidence validation | Attestation as input, not a substitute |

## Pre-access rule

No vendor receives access to systems or personal data before its route completes and the assessment record is merged. Emergency access follows the exceptions process in `00-governance/exceptions-process.md` with an after-the-fact review and a closure SLA, the same pattern `CHG-02` uses for emergency change.

## Handoffs to other pillars

- Contract terms (DPA, breach-notice window, processing limits, subprocessor flow-down) go to Legal and Privacy and are tracked against the executed contract, consistent with the `TPM-01` evidence schema.
- Tier 1 outcomes feed the cadence in [`continuous-monitoring.md`](./continuous-monitoring.md).
- Subprocessor and foundation-model entries reconcile to the public subprocessor list and the trust center in 06-evidence-and-audit.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC1.4, CC2.3, CC9.2 |
| ISO/IEC 27002:2022 | 5.19, 5.20, 5.21 |
| NIST CSF 2.0 | GV.SC-04, GV.SC-06, GV.SC-07 |
| CCPA / CPRA (2026) | §7051, §7052 |
