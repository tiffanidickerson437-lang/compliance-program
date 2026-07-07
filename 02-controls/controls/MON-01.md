# MON-01: Continuous monitoring and event logging

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/MON-01.yaml`](../evidence-schemas/MON-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | MON (Continuous Monitoring) |
| Class | SCF |
| NIST CSF function | Govern |
| Family | monitoring |
| Owner (by function) | Security (SOC) |
| Automation | automated |
| Review cadence | continuous; coverage and retention quarterly |

## Why this control

Continuous monitoring turns a point-in-time audit into a standing program. It is a foundational operations control and the engine of the drift-opens-an-Issue mechanism that makes due diligence visible.

## Control statement

Enterprise monitoring computes control health continuously. Security events ship to a central append-only store with retention and integrity protection. Logs establish what, when, where, source, outcome, and identity, and defined event types alert a monitored queue with an acknowledgement SLA.

## Implementation guidance

Forward every in-scope source to a central store, and protect that store with write-once or object-lock integrity so records cannot be silently altered after the fact. The coverage target is the source inventory itself: a source that is in the inventory and not forwarding is a gap that surfaces, not a number quietly left out of the denominator. Each record establishes what happened, when, where, from which source, with what outcome, and under which identity, so an investigator can reconstruct a sequence without guessing. Drive control-health checks off these logs rather than off a separate console. A failed check opens a tracked Issue, and that Issue, timestamped and retained, is the evidence of due diligence: it shows the program noticed and acted. Route defined event types to a monitored queue with an acknowledgement SLA tuned by severity, and treat a missed acknowledgement as an exception rather than a number to round away. Set a retention floor that meets or exceeds the longest obligation in scope, and verify integrity on a cadence so an altered or missing record is itself an alert. This control is the substrate the other controls compute against: AAT-01 broker decisions, IAC-17 revocations, CHG-02 merges, and IRO-01 incident timelines all land in this store.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Retention floor | 365 days; longer where an obligation in scope requires it | Minimum retention for the central store; the longest in-scope obligation sets the actual floor. |
| Alert acknowledgement SLA, high severity | 30 minutes | Maximum time to acknowledge a high-severity alert in the monitored queue. |
| Source coverage target | 100 percent of the source inventory | Every in-scope source forwards; a non-forwarding in-scope source is an exception. |
| Integrity-check cadence | daily | Frequency of write-once or object-lock integrity verification on the central store. |

## Control enhancements

- **MON-01(1) Append-only integrity protection.** The central store uses write-once or object-lock so records cannot be silently altered, verified on the integrity cadence.
- **MON-01(2) Full source coverage against inventory.** Coverage is measured against the source inventory, and a non-forwarding in-scope source is an exception.
- **MON-01(3) Alerting with acknowledgement SLA.** Defined event types route to a monitored queue with a severity-tuned acknowledgement SLA.
- **MON-01(4) Drift-opens-an-Issue control-health computation.** A failed control-health check opens a tracked Issue that serves as the evidence of due diligence.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. 100 percent of in-scope sources forward to the central store.
2. Integrity protection prevents silent alteration and that integrity checks pass.
3. Retention meets or exceeds the floor for the period.
4. Defined alerts are acknowledged within the SLA.
5. Failed control-health checks opened tracked Issues.

## Assessment methods

**Examine**

- The source inventory against the forwarding configuration, the retention setting, and the object-lock configuration.
- The alert ruleset and the history of drift Issues for the period.

**Interview**

- The SOC on the alert ruleset and the retention standard.
- IT on source forwarding and integrity controls.
- Engineering on emission of the agreed security-event schema.

**Test**

- Compare forwarding to the source inventory and identify any gap.
- Attempt to alter a stored record and confirm the object-lock prevents it.
- Inject a test alert and confirm acknowledgement within the SLA.
- Force a control-health failure and confirm a tracked Issue opens.

## Evidence

SIEM coverage report: forwarding sources against inventory, retention, integrity checks, alert acknowledgement times, and drift Issues opened.

- Record shape: [`evidence-schemas/MON-01.yaml`](../evidence-schemas/MON-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A scheduled job computes: ratio of in-scope sources forwarding, retention days applied, integrity checks failed, ratio of alerts acknowledged within SLA, and drift Issues opened in the period.
- Drift Issue: Coverage below inventory, any failed integrity check, or acknowledgements outside SLA open an Issue tagged MON-01 naming Security as owner.
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC7.2 | framework-mapped |
| ISO/IEC 27002:2022 | 8.15, 8.16 | framework-mapped |
| NIST CSF 2.0 | DE.CM-01, DE.CM-03, DE.CM-09 | framework-mapped |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own the alert ruleset and the retention standard; account for the two alerts that missed acknowledgement SLA. |
| IT | R | Keep every in-scope source forwarding with integrity controls enabled. The coverage report is the evidence. |
| Engineering | C | Emit the agreed security event schema from your services so the SOC can parse and alert on it. |
| Auditor | I | Receive the computed coverage-and-integrity report; sample against the log store, not a console. |
