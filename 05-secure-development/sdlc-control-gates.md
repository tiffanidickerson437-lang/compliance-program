# SDLC Control Gates

**Pillar:** 05-secure-development
**Control anchor:** [`CHG-02`](../02-controls/control-library.yaml), Configuration change control (the pull request is the gate)
**Owner (function):** Engineering (accountable for executing gates). Security owns the gate policy. GRC owns the evidence schema.
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).

## Purpose

Security is built into the way software ships, not bolted on at audit time. Each phase of the development lifecycle has a gate, and each gate produces evidence as a byproduct of passing it. The goal is that an auditor never asks the team to assemble proof; the proof already exists because the gate ran. Compliance joins the sprint instead of taxing it.

## The operating principle

Evidence is a byproduct of shipping. A control that requires extra work to evidence will decay. A control whose evidence is emitted automatically when an engineer does the normal thing (open a pull request, pass a check, deploy through the pipeline) stays alive on its own. Every gate below is designed so the evidence is the artifact the engineer already produces.

## The gates

```text
DESIGN ----> BUILD ----> TEST ----> DEPLOY ----> OPERATE
  |            |           |           |            |
 threat      secure      SAST/DAST   PR gate     drift
 model       deps + SBOM  + secrets  + checks    monitor
 + data      + SAST       + DAST      (CHG-02)    (MON-01)
 review      on commit    coverage    branch
                                      protection
```

### Gate 1: Design

**What must pass before build starts.**

- A threat model exists for any feature that changes the trust boundary, touches precise location, or processes children's data. The model names assets, entry points, and abuse cases.
- A data review confirms the data classes the feature processes and the lawful basis where personal data is involved, consistent with `PRI-03.13` (consent for minors) and `AAT-01` (agent access to location).
- Privacy-by-design is recorded for features touching restricted data: minimization, retention, and the consent or authorization check in the request path.

**Evidence emitted:** the threat-model document and data-review record, linked to the work item. The link is the evidence; the existence of the linked record is what the gate checks.

### Gate 2: Build

**What must pass as code is written and committed.**

- Dependencies resolve against an allowed source; a software bill of materials (SBOM) is generated on build.
- Static analysis (SAST) runs on commit; new high-severity findings block the merge later at the PR gate.
- No secrets in code; secrets scanning runs pre-commit and in CI.

**Evidence emitted:** the SBOM artifact, the SAST result, and the secrets-scan result, attached to the build. See [`secure-pipeline.md`](./secure-pipeline.md) for the wiring.

### Gate 3: Test

**What must pass before a change is eligible to deploy.**

- SAST findings at or above the severity threshold are resolved or have an accepted, time-boxed exception.
- Dynamic analysis (DAST) runs against a deployed test build for services exposed to the network.
- Security-relevant test coverage exists for the abuse cases named in the threat model.

**Evidence emitted:** the test and scan results joined to the change, with severities and exceptions recorded.

### Gate 4: Deploy

**What must pass to reach production. This is `CHG-02`.**

- The change reaches production only through a peer-reviewed pull request linked to a tracked work item, with required checks passing.
- Direct pushes to protected branches are blocked by branch protection.
- Emergency changes follow a documented after-the-fact review with a closure SLA.

**Evidence emitted:** the merge record, carrying the linked ticket, independent reviewer, passing checks, and merge timestamp, pulled from the source-control API. This is exactly the `CHG-02` evidence schema. The PR is the gate; the merge is the authorization; git history is the audit trail. The same gate, viewed from the change-control control, is the program's central enforcement point.

### Gate 5: Operate

**What runs continuously after deploy.**

- Control-health checks compute posture from the systems of record; drift opens a GitHub Issue (`MON-01`).
- New vulnerabilities in deployed dependencies are triaged against the SBOM and tracked to closure.

**Evidence emitted:** the continuous-monitoring coverage record and the vulnerability-aging record.

## OWASP mapping

The build, test, and deploy gates map to the OWASP Top 10 (web) and corroborate the OWASP LLM Top 10 controls owned in 04-ai-governance. Representative mapping:

| OWASP Top 10 (2021) | Gate that addresses it | Mechanism |
|---------------------|------------------------|-----------|
| A01 Broken access control | Design, Deploy | Threat model, reviewed PR, access tests |
| A02 Cryptographic failures | Design, Test | Data review, DAST, dependency checks |
| A03 Injection | Build, Test | SAST, DAST |
| A05 Security misconfiguration | Deploy, Operate | PR review, drift monitor |
| A06 Vulnerable and outdated components | Build, Operate | SBOM, dependency monitoring |
| A07 Identity and authentication failures | Design, Test | Threat model, access tests |
| A08 Software and data integrity failures | Build, Deploy | SBOM, signed artifacts, branch protection |
| A09 Logging and monitoring failures | Operate | `MON-01` logging coverage |
| A10 Server-side request forgery | Build, Test | SAST, DAST |

For the LLM-specific risks (prompt injection, excessive agency, sensitive-info disclosure), the gates here enforce the supply-chain and output-handling items; the agent-behavior items are owned by `AAT-01` and the OWASP LLM controls in 04-ai-governance.

## Exceptions

A gate can be bypassed only through a tracked exception with an owner (function), a justification, and a closure date, following `00-governance/exceptions-process.md`. An emergency production change with after-the-fact review is the canonical example, reconciled the same way `CHG-02` reconciles its one un-reviewed exception per period.

## Framework mapping

| Framework | Reference | Note |
|-----------|-----------|------|
| SOC 2 (TSC 2017) | CC8.1, CC3.4 | Change management and risk in development. |
| ISO/IEC 27002:2022 | 8.25, 8.28, 8.29, 8.31 | Secure development lifecycle and testing. |
| NIST SSDF (SP 800-218) | PW.1, PW.7, PW.8, RV.1 | Secure software development practices. |
| NIST CSF 2.0 | ID.RA-07, PR.PS | Change and platform security. |
| SOX ITGC | Change management | Framework-mapped, home lab, never audited. |
