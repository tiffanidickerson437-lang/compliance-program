# IRO-01: Incident response operations

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/IRO-01.yaml`](../evidence-schemas/IRO-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | IRO (Incident Response) |
| Class | SCF |
| NIST CSF function | Govern |
| Family | incident response |
| Owner (by function) | Security (Legal/Privacy on notification) |
| Automation | partial |
| Review cadence | per incident; tabletop and plan review annually |

## Why this control

Incident response is where regulatory clocks become real: breach notification within statutory timelines, and AI-specific incidents such as an autonomous agent acting out of scope on the location graph.

## Control statement

Incidents are detected, triaged, contained, and recorded against a governed plan, including AI scope breaches. Legal/Privacy owns notification within statutory timelines, and every incident receives a post-incident review.

## Implementation guidance

Generate the incident record from the paging and tracking tooling rather than reconstructing a narrative after the fact. The record carries the detection time, the severity, the containment and resolution timestamps, the notification decision and its basis, and a link to the post-incident review. Because the record is sourced from tooling, the timeline is defensible: it shows when the program detected, decided, and acted, not when someone remembered to write it down. Run a severity scale that sets containment expectations by level, and route severity-1 incidents to a named escalation including the board where the obligation requires it. Legal/Privacy owns the notification decision: whether a statutory or contractual threshold is met, and if so, that the regulator and affected parties are notified within the clock that applies. The decision and its basis are logged, because the decision not to notify is as much a record as the decision to notify. Keep an AI-incident runbook for the case where an autonomous agent acts out of scope on the location graph, with a kill-switch path that ties back to AAT-01. Every incident, regardless of severity, gets a post-incident review that feeds control design, and the program tabletops at least annually, including an AI-scope scenario, so the plan is exercised before it is needed.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Severity scale | Sev1 through Sev4 | Severity levels that set containment expectations and escalation paths. |
| Regulatory notification clock | 72 hours where GDPR applies; the applicable statutory window otherwise | The notification window for a threshold-meeting incident, set by the regime in scope. |
| Containment SLA, severity-1 | defined per the severity scale | Target interval from triage to containment for the highest severity. |
| Tabletop cadence | at least annual, including an AI-scope scenario | Frequency of exercising the plan, including an autonomous-agent scenario. |

## Control enhancements

- **IRO-01(1) AI-scope incident handling and kill-switch.** An AI-incident runbook covers an agent acting out of scope on the location graph, with a kill-switch path tied to AAT-01.
- **IRO-01(2) Notification decision log with statutory clock.** Legal/Privacy logs the notification decision and its basis, and meets the statutory clock when a threshold is met.
- **IRO-01(3) Mandatory post-incident review.** Every incident receives a post-incident review that feeds back into control design.
- **IRO-01(4) Annual tabletop including an AI scenario.** The plan is exercised at least annually, including an autonomous-agent scope scenario.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. Incident records carry complete timeline fields sourced from tooling.
2. Every incident received a post-incident review.
3. Threshold-meeting incidents carry a decision log and met the statutory timeline.
4. AI-scope incidents reference the kill-switch action taken.

## Assessment methods

**Examine**

- The incident response plan, the severity scale, the breach-decision log, and the post-incident reviews for the period.
- The AI-incident runbook and the most recent tabletop record.

**Interview**

- Security on the plan, the severity scale, the containment SLA, and the tabletop.
- Legal/Privacy on notification decisions and the statutory clocks.
- Engineering on containment and recovery on their services.

**Test**

- Sample incidents and confirm complete timeline fields sourced from the tracker.
- Verify a post-incident review exists for each sampled incident.
- For a threshold-meeting incident, confirm the decision basis and the statutory timeline were met.
- Tabletop an AI-scope agent incident and confirm the kill-switch path executes.

## Evidence

IR platform record: detection, severity, containment, resolution, notification decision, statutory timeline, and post-review link.

- Record shape: [`evidence-schemas/IRO-01.yaml`](../evidence-schemas/IRO-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A scheduled job reads the incident tracker and the breach-decision log and computes: incidents, severity-1 count, AI-scope incidents, median detect-to-triage minutes, incidents meeting a notification threshold, regulator notified within the clock, and post-incident reviews completed.
- Drift Issue: Any incident missing a post-incident review, or any threshold-meeting incident missing a decision basis, opens an Issue tagged IRO-01 naming Security and Legal/Privacy as owners.
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC7.3, CC7.4 | framework-mapped |
| ISO/IEC 27002:2022 | 5.24 | framework-mapped |
| NIST CSF 2.0 | DE.AE, RS.MI | framework-mapped |
| NIST AI RMF 1.0 | GOVERN 6.2, MANAGE 2.4 | framework-mapped |
| CCPA / CPRA (2026) | Civil Code §1798.82, §7123(c)(17) | framework-mapped |
| GDPR | Art. 33, Art. 34 | framework-mapped |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own the IR plan, the severity scale, and the containment SLA; run the post-incident review and the annual tabletop. |
| Engineering | R | Execute containment and recovery on your services and feed timestamps to the incident record. That record is the evidence. |
| Legal/Privacy | A | Own the breach-notification decision and timeline; determine when statutory thresholds are met and document the basis. |
| C-Suite / Board | I | Receive Sev1 notification and the post-incident summary. Major-incident escalation is a board-visible obligation. |
| Customer | I | Receive breach notification when the threshold is met, within the statutory window. |
| Auditor | I | Receive the computed incident records with timelines and review links; no reconstructed narratives. |
