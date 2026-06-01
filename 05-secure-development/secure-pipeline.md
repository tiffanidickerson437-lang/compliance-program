# Secure Pipeline

**Pillar:** 05-secure-development
**Control anchor:** [`CHG-02`](../02-controls/control-library.yaml), Configuration change control, supported by [`MON-01`](../02-controls/control-library.yaml)
**Owner (function):** Engineering (runs the pipeline). Security owns the required-check policy. IT keeps the CI/CD identity locked.

## Purpose

The pipeline is where the SDLC gates become technical enforcement. Branch protection, required checks, SBOM generation, secrets scanning, and SAST/DAST are configured so that the only way to ship is the secure way, and the act of shipping produces the evidence. This file specifies the controls the pipeline enforces and the evidence each emits. It does not hand-write automation; the program is a scaffold, and the wiring lives in `.github/workflows/`.

## Branch protection (the technical enforcement of CHG-02)

Protected branches enforce the change-control policy in `CHG-02`:

- No direct pushes to protected branches; all change arrives by pull request.
- At least one independent reviewer approval required; the author cannot approve their own change.
- Required status checks must pass before merge (build, SAST, secrets scan, SBOM, tests).
- Linear history and dismissal of stale approvals on new commits.
- Administrators are subject to the same rules; no bypass.
- A linked work item is required so every merge maps to tracked intent.

**Evidence emitted:** the branch-protection configuration is the supporting artifact; the merge record is the operating evidence, pulled from the source-control merge API. This is the `CHG-02` evidence schema verbatim: merges to production, linked ticket, independent reviewer, passing checks, merge timestamp.

## Required checks

| Check | Stage | Blocks merge when | Evidence emitted |
|-------|-------|-------------------|------------------|
| Build and unit tests | Build | Build fails or tests fail | Build result |
| SAST | Build/Test | New finding at or above threshold | SAST report with severities |
| Secrets scanning | Build | A secret is detected | Secrets-scan result |
| SBOM generation | Build | SBOM cannot be produced | SBOM artifact |
| Dependency / vulnerability scan | Build/Operate | Known high-severity CVE with a fix | Dependency report |
| DAST (network-exposed services) | Test | High-severity dynamic finding | DAST report |
| Evidence schema validation | Deploy | Control evidence fails its schema | Validator result |

The evidence-schema validation check is owned with 06-evidence-and-audit and wired in `.github/workflows/evidence-validator.yml`. A pull request that marks a control operating without schema-valid evidence fails the build.

## Software bill of materials (SBOM)

- An SBOM is generated on every build in a standard format (for example CycloneDX or SPDX).
- The SBOM is retained as a build artifact and is the inventory the operate-stage vulnerability monitoring runs against.
- When a new vulnerability is disclosed, triage joins the CVE to the SBOM to find affected services without guesswork. This is the A06 (vulnerable components) and A08 (integrity) enforcement from the SDLC gates.

## Secrets management

- Secrets scanning runs pre-commit (developer machine) and as a required check in CI.
- No hardcoded credentials, no long-lived tokens, no shared accounts in code.
- Application secrets are issued from a managed secret store with rotation; pipeline identities use short-lived, least-privilege credentials, the same posture `AAT-01` requires of agents.
- A detected secret blocks the merge and opens a tracked remediation (rotate the exposed secret, not just delete the line).

## SAST and DAST

- **SAST** runs on commit and as a required check. Findings carry a severity; findings at or above the threshold block merge or require a time-boxed exception.
- **DAST** runs against a deployed test build for network-exposed services before the deploy gate.
- Findings flow to the same tracker engineering already uses; the finding is the work order, with the control ID and acceptance criteria attached.

## Pipeline identity integrity

The CI/CD identity and the check configuration are locked so the gate cannot be bypassed. This is the IT ask in the `CHG-02` stakeholder mapping: keep the CI/CD identity and check configuration locked. A change to the pipeline configuration is itself a change subject to `CHG-02` review.

## How evidence reaches the auditor

No screenshots of individual pull requests. The auditor receives the computed merge log and the check results for the period, exported from the source-control API, consistent with the `CHG-02` test procedure. The pipeline is the source of record; the export is the evidence.

## What the scaffold does and does not do

This file specifies the enforcement. The actual jobs are placeholders in `.github/workflows/` until the team wires real scanners and stores. Nothing here requires ongoing hand-maintenance to stay valid; it describes the contract the pipeline must meet.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC8.1, CC7.1, CC6.8 |
| ISO/IEC 27002:2022 | 8.25, 8.28, 8.29, 8.31, 8.9 |
| NIST SSDF (SP 800-218) | PS.1, PW.4, PW.6, PW.8, RV.1 |
| NIST CSF 2.0 | PR.PS, ID.RA-07 |
| SOX ITGC | Change management, segregation of dev and approver | Framework-mapped, home lab, never audited. |
