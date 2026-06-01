# IAC-17: Periodic review of account privileges

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/IAC-17.yaml`](../evidence-schemas/IAC-17.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | IAC (Identification & Authentication) |
| Class | SCF |
| NIST CSF function | Detect |
| Family | access management |
| Owner (by function) | Security (IAM) |
| Automation | partial |
| Review cadence | quarterly; monthly for production and sensitive-data systems |

## Why this control

A public, multi-listed company carries SOX IT general controls. Periodic access review is the access pillar of ITGC and the control auditors test first. The same review limits standing access to precise location and minor data, so it serves privacy as well as financial-reporting integrity.

## Control statement

Privileges for people and service accounts are reviewed on a fixed cadence against role and employment, and unjustified access is removed. Leaver deprovisioning fires from the human-resources system of record, not a manual ticket. Service and other non-human accounts are held to the same bar as human accounts.

## Implementation guidance

Drive the recertification campaign from the identity provider joined to the human-resources information system, so every account maps to a live employment status and a named owner. An account with no live owner or employment match is an orphan and an exception, not a finding to defer. Treat service accounts and other non-human identities exactly as human accounts: each has an owner, a justification, and a recertification record. The evidence is the revocation event in the log, joined to the entitlement snapshot, not a reviewer's after-the-fact assertion that access looked reasonable. Fire leaver and role-change deprovisioning from the human-resources feed on the same business day as the event, because a manual ticket is the gap auditors find. Run the review quarterly for general systems and monthly for production and sensitive-data systems, where the blast radius is larger. Include a segregation-of-duties and toxic-combination check in the review: an account that can both develop a change and approve its release, or both create a vendor and pay it, is a finding regardless of employment status. Orphaned and over-privileged accounts carry a closure SLA, and the campaign does not sign off until every flagged account is closed or documented as an approved exception.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Recertification cadence, general systems | quarterly | Maximum interval between recertification cycles for in-scope general systems. |
| Recertification cadence, production and sensitive-data systems | monthly | Tighter cadence where access reaches production, precise location, or minor data. |
| Leaver deprovisioning SLA | same business day as the HR event | Interval from the HR termination or role-change event to access revocation. |
| Orphan and over-privilege closure SLA | 5 business days | Maximum time to close or formally except a flagged orphaned or over-privileged account. |

## Control enhancements

- **IAC-17(1) HRIS-driven recertification.** The campaign is driven from the identity provider joined to the HRIS so every account maps to a live employment status and owner.
- **IAC-17(2) Non-human accounts in scope at the same bar.** Service accounts and other non-human identities have an owner and a recertification record and are reviewed to the same standard as human accounts.
- **IAC-17(3) HR-triggered leaver deprovisioning.** Deprovisioning fires from the human-resources feed on the same business day as the event, not from a manual ticket.
- **IAC-17(4) Segregation-of-duties and toxic-combination review.** The review flags accounts holding conflicting entitlements regardless of employment status.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. 100 percent of in-scope accounts, human and non-human, were reviewed within the cadence.
2. Each revocation reconciles to a revocation event in the log.
3. Orphaned and over-privileged accounts are zero or are documented exceptions under the closure SLA.
4. Leaver deprovisioning fired from the HR feed within the SLA.
5. Segregation-of-duties conflicts were identified and resolved or excepted.

## Assessment methods

**Examine**

- The recertification policy, the identity-provider-to-HRIS join design, and the cycle attestation for the period.
- The exception log for orphaned, over-privileged, and segregation-of-duties findings.

**Interview**

- Security on the revocation SLA and the cycle sign-off bar.
- Human Resources on the timeliness of the termination and role-change feed.
- Engineering on entitlement decisions for systems their team owns.

**Test**

- Pull the entitlement snapshot at cycle start and confirm every in-scope account, including service accounts, was reviewed.
- Trace a sample of revocations to revocation events in the log.
- Pick a recent leaver and confirm deprovisioning fired from the HR event within the SLA.
- Test the population for orphaned, over-privileged, and toxic-combination accounts.

## Evidence

Recertification attestation joined to the identity-provider and HRIS snapshot: accounts in scope, reviewed, revoked, orphaned, and service accounts recertified.

- Record shape: [`evidence-schemas/IAC-17.yaml`](../evidence-schemas/IAC-17.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A scheduled job reconciles identity-provider entitlements to HRIS active status and computes: accounts in scope, accounts reviewed in the cadence, revocations reconciled to log events, orphaned accounts, and leaver-to-deprovision latency breaches.
- Drift Issue: Any account past its cadence, any orphaned account, or any leaver-to- deprovision latency breach opens an Issue tagged IAC-17 naming Security as owner with the SOX ITGC access pillar flagged.
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC6.2, CC6.3 | framework-mapped |
| ISO/IEC 27002:2022 | 5.15, 5.18, 8.2 | framework-mapped |
| SOX ITGC | Access to programs and data | framework-mapped, home lab (never audited) |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own the recertification campaign and the revocation SLA; sign the cycle once every flagged account is closed. |
| IT | R | Run the campaign in the IdP and push deprovisioning; the revocation event in the log is the evidence. |
| HR | C | Keep termination and role-change dates current so the leaver feed fires the same day. That feed is the trigger. |
| Engineering | R | Confirm or revoke each entitlement to systems your team owns within the window. |
| Auditor | I | Receive the computed attestation-plus-snapshot export; no live screen-shares. |
