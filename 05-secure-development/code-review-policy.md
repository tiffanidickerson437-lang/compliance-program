# Code Review Policy

**Pillar:** 05-secure-development
**Control anchor:** [`CHG-02`](../02-controls/control-library.yaml), Configuration change control (the pull request is the gate)
**Owner (function):** Engineering (performs reviews). Security owns the policy and the security-review criteria.

## Purpose

Peer review on a pull request is the human half of the change-control gate. Branch protection enforces that a review happened; this policy defines what a review must check so that the review is meaningful and not a rubber stamp. The reviewed, merged pull request is the evidence for `CHG-02`.

## The rule

Every change to production reaches the protected branch only through a pull request that has:

1. An independent reviewer approval. The author cannot approve their own change.
2. A linked tracked work item, so the change maps to intent.
3. All required checks passing (build, SAST, secrets scan, SBOM, tests, evidence validation).

Direct pushes to protected branches are blocked. This is the technical enforcement specified in [`secure-pipeline.md`](./secure-pipeline.md).

## What a reviewer checks

### Standard review (every pull request)

- The change matches the linked work item and does only what it claims.
- Tests exist and pass for the new behavior.
- No secrets, credentials, or tokens introduced.
- No obvious injection, unsafe deserialization, or unvalidated input on a trust boundary.
- Dependencies added are from an allowed source and appear in the SBOM.

### Security-focused review (triggered changes)

A heavier review is required when the change touches a security-sensitive area. Triggers:

- Authentication, authorization, or session handling.
- Precise location or children's/minors' data paths (`PRI-03.13`, `AAT-01`).
- The agent authorization broker, consent service, or any purpose-token logic.
- Cryptography, key handling, or secrets management.
- The CI/CD pipeline configuration itself.
- A new third-party integration or data egress.

Security-focused review adds checks against the threat model from the design gate, confirms the consent or authorization check is in the request path, and confirms logging is sufficient for `MON-01` to observe the behavior. The security owner (function) or a delegate is a required reviewer for these changes.

## Reviewer independence and segregation

Independence is the point. The reviewer is not the author. For changes to the most sensitive paths, the reviewer is from a different sub-team where staffing allows. This is the segregation-of-duties intent behind the SOX ITGC change-management mapping, held here as framework mapping only, home lab, never audited.

## Emergency changes

An emergency change may merge with an after-the-fact review when waiting would cause customer harm. It is recorded as an exception under `00-governance/exceptions-process.md` with an owner, the justification, and a closure date, then reviewed within the SLA. This is the documented after-the-fact path `CHG-02` requires; the one un-reviewed exception per period in the `CHG-02` example evidence is exactly this case, reconciled and closed.

## The evidence

The review produces no separate artifact to file. The merged pull request is the evidence: it carries the reviewer, the linked ticket, the passing checks, and the merge timestamp, all pulled from the source-control API. The auditor receives the computed merge log for the period, not screenshots of individual reviews, consistent with the `CHG-02` test procedure.

## Metrics that keep the gate honest

Tracked through `MON-01` and reported in 07-stakeholder-management:

- Percentage of merges with an independent review and a linked ticket (target: 100 percent).
- Direct pushes blocked (should be the only path attempts take that fail).
- Exceptions without review per period, each reconciled to closure.
- Security-focused reviews triggered and their outcomes.

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC8.1, CC3.4 | Change authorization and review. |
| ISO/IEC 27002:2022 | 8.28, 8.31, 8.32 | Secure coding, separation of environments, change management. |
| NIST SSDF (SP 800-218) | PW.7, PW.8 | Review and analysis of human-readable code. |
| NIST CSF 2.0 | ID.RA-07 | Change risk assessment. |
| SOX ITGC | Change management, segregation of duties | Framework-mapped, home lab, never audited. |
