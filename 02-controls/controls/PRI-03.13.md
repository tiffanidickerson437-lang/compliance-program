# PRI-03.13: Parent or guardian opt-in consent for minors

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/PRI-03.13.yaml`](../evidence-schemas/PRI-03.13.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | PRI (Data Privacy) |
| Class | SCF |
| NIST CSF function | Protect |
| Family | privacy |
| Owner (by function) | Legal/Privacy (Security enforces) |
| Automation | partial |
| Review cadence | continuous consent state; policy and flow review quarterly |

## Why this control

A consumer location-safety service at this scale processes the data of children. The amended COPPA Rule and the minor provisions of CCPA/CPRA require verifiable parental consent before that data is processed. This control proves consent is on record and authoritative. The amended Rule (published April 22, 2025; compliance date April 22, 2026) adds a separate-consent requirement for third-party disclosure.

## Control statement

Minor personal data processes only after verifiable parent or guardian opt-in consent is recorded. Consent state is authoritative: absent or withdrawn consent blocks processing and disclosure, and a separate verifiable consent is required before any disclosure of a child's data to a third party.

## Implementation guidance

Capture consent as a first-class record keyed to the child account, carrying the verification method, the scope of processing it authorizes, and the timestamp. Make the consent service the single system of record that every feature, integration, and agent checks before processing a minor's data, so that a withdrawal propagates everywhere at once rather than feature by feature. The record, not a policy assertion, is the evidence. Use a verification method that meets the standard set by the amended COPPA Rule for the processing in question, and record which method was used. Disclosure of a child's data to a third party requires a separate verifiable consent, recorded distinctly from the consent to operate the service. Hold minor data to a tighter minimization and retention rule than adult data, and delete or restrict it when consent is withdrawn or the lawful basis ends. Treat any processing observed without active consent as an exception that surfaces, not as a silent gap: it opens a tracked Issue, names the owning function, and carries a remediation path. The consent service is also the input to AAT-01: an agent's read of a minor's data is brokered against the same consent state, so the privacy control and the agent control cannot disagree about whether consent is present.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Withdrawal propagation SLA | near-real-time (under 1 hour to full propagation) | Time from a recorded withdrawal to processing and disclosure being blocked across all paths. |
| Minor age threshold | under 13 (COPPA); broader where local law sets a higher age | Drives which accounts fall in scope for verifiable parental consent. |
| Accepted verification methods | methods recognized under 16 CFR 312.5(b) for the processing in question | Record the specific method used per account; weaker methods do not satisfy stronger processing. |
| Separate consent for third-party disclosure | required | Disclosure to a third party needs a distinct verifiable consent, not the operating consent. |

## Control enhancements

- **PRI-03.13(1) Consent service as authoritative gate.** Every feature, integration, and agent checks the consent service before processing a minor's data; the service is the single system of record.
- **PRI-03.13(2) Separate consent before third-party disclosure.** Disclosure of a child's data to a third party requires a separate, distinctly recorded verifiable consent.
- **PRI-03.13(3) Immediate withdrawal propagation.** A recorded withdrawal blocks processing and disclosure across all paths within the propagation SLA.
- **PRI-03.13(4) Minor data minimization and retention limit.** Minor data is held to a tighter minimization and retention rule and is deleted or restricted when consent ends.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. Every in-scope minor account has a recorded verifiable parental consent before processing.
2. The verification method used meets the standard for the processing it authorizes.
3. No third-party disclosure of a child's data occurs without a separate recorded consent.
4. Withdrawals are honored within the propagation SLA and block processing and disclosure.
5. Processing is denied when consent is absent or withdrawn.

## Assessment methods

**Examine**

- The consent register and the verification-method configuration for minor accounts in scope.
- The COPPA and CCPA/CPRA obligation mapping and the third-party disclosure flow design.
- The minor-data retention and deletion rule.

**Interview**

- Legal/Privacy on what verifiable consent requires and which processing needs a separate consent.
- Engineering on where the consent check sits in the request path and how withdrawal propagates.
- Product on the consent and disclosure flow design and the absence of dark patterns.

**Test**

- Sample minor accounts and confirm a recorded verifiable parental consent with a valid method before processing.
- Withdraw consent on a test account and confirm processing and disclosure are blocked within the SLA.
- Attempt a third-party disclosure without a separate consent and confirm the path denies it.

## Evidence

Consent register per minor: verification method, scope, state, third-party disclosures without active consent, and withdrawals honored within SLA.

- Record shape: [`evidence-schemas/PRI-03.13.yaml`](../evidence-schemas/PRI-03.13.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A daily job exports the consent register and computes: minor accounts in scope, accounts with verified parental consent, third-party disclosures without active consent (target zero), and the ratio of withdrawals honored within the propagation SLA.
- Drift Issue: Any third-party disclosure without active consent, or any positive delta between in-scope accounts and accounts with verified consent, opens an Issue tagged PRI-03.13 naming Legal/Privacy as owner with the framework impact (COPPA, CCPA/CPRA).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| COPPA (amended 2025) | 16 CFR 312, §6502(b)(1)(A)(ii) | framework-mapped |
| CCPA / CPRA (2026) | §7070(a) | framework-mapped |
| GDPR | Art. 8 | framework-mapped |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| Legal/Privacy | A | Define what verifiable consent requires and which processing needs separate consent; own the COPPA obligation mapping. |
| Engineering | R | Check the consent service before processing a minor's data and honor withdrawal immediately. The consent record is the evidence. |
| Product | C | Design the consent and disclosure flows to match reasonable parental expectations, with no dark patterns. |
| Security | C | Enforce that no agent or integration can read a minor's data when consent is absent or withdrawn. |
| Auditor | I | Receive the computed consent register; sample against the consent store, not a screenshot. |
