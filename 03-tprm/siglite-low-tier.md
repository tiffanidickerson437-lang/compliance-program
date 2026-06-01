# SIG Lite: Low-Tier Screen

**Pillar:** 03-tprm
**Control anchor:** [`TPM-01`](../02-controls/control-library.yaml), Third-party management
**Owner (function):** GRC (accountable). Procurement initiates. Security consulted on flagged answers.
**Applies to:** Tier 3 vendors, and Tier 4 vendors only when an inherent-risk screen leaves doubt.
**Depends on:** [`vendor-tiering-model.md`](./vendor-tiering-model.md), [`tiered-intake-workflow.md`](./tiered-intake-workflow.md)

## Purpose

SIG Lite is the lightweight questionnaire for vendors with limited or scoped data access. It exists so that a low-exposure vendor is screened proportionally, not subjected to the full SIG Core reserved for Tier 1. If a vendor already holds a current SOC 2 Type II or ISO 27001 report, the reviewer uses attestation review instead and does not send a questionnaire at all.

## When SIG Lite is the right instrument

| Situation | Instrument |
|-----------|------------|
| Tier 3, no current attestation | SIG Lite |
| Tier 3, current attestation on file | Attestation review (see register), skip SIG Lite |
| Tier 4, no data and no access | Inherent-risk screen, no questionnaire |
| Tier 4 with any residual doubt | SIG Lite |
| Tier 1 or Tier 2 with restricted data | Not SIG Lite; escalate to deep review or attestation review |

SIG Lite is never the instrument for a vendor that touches precise location or children's data. That exposure pins the vendor to Tier 1 under the restricted-data override and routes it to deep review.

## What SIG Lite covers (domain checklist)

A right-sized subset of the Standardized Information Gathering domains, scaled to low exposure. The reviewer collects vendor answers and supporting artifacts where the answer is material.

1. **Security policy and governance:** documented information-security policy, named security owner (function).
2. **Access control:** role-based access, MFA on administrative access, joiner-mover-leaver process.
3. **Data handling:** what data classes the vendor receives, where stored, retention, deletion on termination.
4. **Encryption:** encryption in transit and at rest for any data the vendor holds.
5. **Vulnerability and patch:** patching cadence, a recent vulnerability-scan or pen-test summary if available.
6. **Logging and monitoring:** basic event logging and alerting on the service.
7. **Incident response:** an IR process and a contractual breach-notification commitment.
8. **Business continuity:** backup and recovery sufficient for the dependency level.
9. **Subprocessors:** onward subprocessors that would touch company data.
10. **Compliance:** applicable certifications or attestations, even if not used in lieu here.

## How the screen runs

1. Intake assigns Tier 3 (or Tier 4 with doubt) and routes here.
2. SIG Lite goes to the vendor; responses return into the case work item.
3. AI drafts a summary: which domains are satisfied, which answers are missing or weak, and a proposed risk rating. The draft is not a record.
4. A human GRC owner reviews flagged answers, decides accept, accept-with-conditions, or escalate, and records the outcome through a pull request.
5. Any condition (for example, enable MFA on admin access before go-live) becomes a tracked item with an owner and date.

## Escalation out of the low tier

Re-tier upward and leave the SIG Lite path when any of the following surfaces:

- The vendor will receive more sensitive data than the intake declared.
- Answers reveal standing production access not previously disclosed.
- A subprocessor in the chain touches restricted data.
- A material gap (no encryption at rest for personal data, no IR process) appears.

Escalation opens a GitHub Issue recording why the tier changed; the new route (attestation review or deep review) proceeds from there. The Issue is the due-diligence record that the change was caught and acted on.

## Outcome and reuse

A clean SIG Lite result is recorded with its date and the next reassessment per [`continuous-monitoring.md`](./continuous-monitoring.md). If the vendor later produces a SOC 2 or ISO report, the next cycle switches to attestation review and logs the reuse in [`attestation-reuse-register.yaml`](./attestation-reuse-register.yaml), retiring the questionnaire for that vendor.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC1.4, CC2.3 |
| ISO/IEC 27002:2022 | 5.19, 5.20 |
| NIST CSF 2.0 | GV.SC-04, GV.SC-06 |
