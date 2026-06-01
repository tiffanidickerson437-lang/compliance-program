# SOX ITGC Scope

**Pillar:** 00-governance
**Owner of the SOX program:** Internal Audit (third line)
**Author of this scope mapping:** GRC function
**Status:** Scaffold. Validate scope with Internal Audit before any reliance.

---

## 1. Basis and explicit non-claim

This document maps IT general controls (ITGC) to the program's controls on a
**framework-mapped, home-lab basis**. It demonstrates the control patterns that a SOX ITGC
program relies on, built and exercised in a home lab and mapped to recognized framework
references.

It does **not** claim that a public-company SOX audit was performed, and it does not assert
operating effectiveness of any control in the organization's production environment. No statement here
should be read as a completed Section 404 assessment or as reliance an external auditor could
place. Operating effectiveness in a live environment is established only through testing scoped
and owned by Internal Audit. This scaffold is framework mapping and design, not an audit
result.

## 2. Why ITGC is in scope for this configuration

`config.example.yaml` carries a non-empty `listings` block (two public exchanges; illustrative
example listings). A public listing brings IT general controls, Internal Audit, and Audit Committee
reporting into scope. That single configuration fact turns on this document and the Audit and
Risk Committee cadence in `committee-charter.md`. A private company would delete the `listings`
block and this scope would not apply.

ITGC matters because the application controls and the financial reports that auditors rely on
sit on top of the IT environment. If access, change, and operations over the financially
relevant systems are not reliable, the controls and the numbers above them cannot be relied on.

## 3. The three ITGC domains and how they map

SOX ITGC is conventionally organized into access, change, and operations. Each maps to a
control already defined once in `02-controls/control-library.yaml`, so ITGC is a rendering of
the owned control set, not a separate library.

| ITGC domain | ITGC assertion | Program control | Framework references (illustrative) |
|-------------|----------------|-----------------|--------------------------------------|
| Access to programs and data | Access is granted on least privilege, reviewed on a cadence, and removed on role change or departure. Privileged and service accounts are governed the same as human accounts. | IAC-17 (periodic review of account privileges) | SOC 2 CC6.2, CC6.3; ISO 27002 5.15, 5.18, 8.2 |
| Program changes | Changes reach production only through reviewed, traceable, segregated approval. Direct pushes to protected branches are blocked. Emergency changes are reconciled after the fact. | CHG-02 (configuration change control) | SOC 2 CC3.4, CC8.1; ISO 27002 8.19, 8.32; NIST CSF ID.RA-07 |
| Computer operations | Security and operational events are logged to an append-only store with retention and integrity protection. Privileged activity is monitored. Failures open a tracked Issue. | MON-01 (continuous monitoring and event logging) | SOC 2 CC7.2; ISO 27002 8.15, 8.16; NIST CSF DE.CM-01, DE.CM-03 |

The SOX ITGC mappings in the control library are tagged `partial` and annotated
`framework-mapped, home lab`. That tag is the program's honest marker that the mapping is
design and home-lab evidence, not an audited result.

## 4. Scoping approach (to be performed with Internal Audit)

Scope is set top-down from the financial statements, not bottom-up from every system:

1. **Identify significant accounts and disclosures** with Finance and the external auditor.
2. **Trace to the applications** that generate or process those numbers (billing, revenue,
   general ledger, the data pipelines that feed them).
3. **Identify the supporting infrastructure** for those applications: the identity provider,
   the source-control and deployment path, the logging and monitoring stack.
4. **Scope ITGC to that infrastructure.** Systems with no path to a financially relevant
   number are out of ITGC scope, even if they are in scope for security or privacy.
5. **Define reliance.** Internal Audit decides which automated controls auditors can rely on
   and what residual manual testing remains.

Scoping is owned by Internal Audit with Finance and GRC consulted. GRC supplies the control
mappings and the computed evidence path; Internal Audit decides scope and reliance.

## 5. Segregation of duties

- The function that develops a change does not approve its own production release. CHG-02
  enforces this through an independent reviewer on the Pull Request.
- The function that operates the controls (first line) is not the function that tests them
  (Internal Audit, third line).
- GRC designs and maps; Internal Audit tests and opines. GRC does not test its own design for
  SOX reliance.

## 6. What the home lab demonstrates, and what it does not

| Demonstrated in the home lab (design and pattern) | Requires the live environment and Internal Audit |
|----------------------------------------------------|---------------------------------------------------|
| Branch protection enforcing reviewed, ticket-linked merges (CHG-02 pattern) | Operating effectiveness across the real change population for a period |
| Access recertification driven from an identity provider joined to an HR feed (IAC-17 pattern) | The true account population, leaver-feed latency, and exception rate |
| Append-only logging with retention and integrity checks (MON-01 pattern) | Real source coverage counts and alert-acknowledgement SLAs |
| Evidence computed from system APIs rather than screenshots | Auditor reliance decisions and the scoped system boundary |

## 7. Evidence model

Evidence for ITGC is computed from the systems of record named in `config.example.yaml`, never
reconstructed by hand and never authored by a model:

- Access: a recertification attestation joined to the identity provider and HR snapshot
  (account, owner, reviewer, decision, revocation time).
- Change: the source-control merge record (linked ticket, independent reviewer, passing
  checks, merge timestamp).
- Operations: the logging coverage report (forwarding sources, retention, integrity checks,
  alert-acknowledgement times).

A failed check opens a GitHub Issue (the due-diligence record); the fix is a Pull Request a
human approves; the merge updates status; Git history is the audit trail.

## 8. Roadmap to validation

1. Confirm the financially relevant systems with Finance and Internal Audit.
2. Replace home-lab patterns with computed evidence from the scoped production systems.
3. Internal Audit tests operating effectiveness over a defined period and sets reliance.
4. Only after that testing is any statement of operating effectiveness appropriate, and it is
   Internal Audit's to make, not GRC's.
