# VPM-01: Vulnerability and patch management

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/VPM-01.yaml`](../evidence-schemas/VPM-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | VPM (Vulnerability & Patch Management) |
| Class | SCF |
| NIST CSF function | Identify / Protect |
| Family | vulnerability management |
| Owner (by function) | Security (Engineering remediates) |
| Automation | automated |
| Review cadence | continuous scanning; SLA review quarterly |

## Why this control

Every auditor expects a vulnerability and patch program, and its absence is the gap a security questionnaire probes first. For a service on a multi-cluster cloud estate shipping continuously, unpatched dependencies and exposed services are the most common path to the precise-location data this program exists to protect. This control makes finding and fixing known weaknesses a measured, time-bound loop rather than a periodic scramble.

## Control statement

Technical vulnerabilities across code, dependencies, images, and infrastructure are discovered continuously, triaged by severity and exposure, and remediated within defined service levels. Internet-facing and sensitive-data systems carry the tightest timelines. Unremediated vulnerabilities past SLA are tracked as exceptions with a named owner and a closure plan.

## Implementation guidance

Discover vulnerabilities from more than one vantage point: dependency and container scanning in the pipeline, infrastructure and external-surface scanning in the running estate, and the intake of vendor and CISA advisories. Normalize findings into one queue with a severity and an exposure dimension, because a critical on an internet-facing system holding location data is not the same risk as the same critical on an isolated internal tool. Set remediation SLAs by that combination and enforce them as the aging clock on the queue, not as a guideline. Patch through the same governed change path as any other production change (CHG-02), so the fix carries its own evidence. When a fix cannot ship inside the SLA, it becomes a tracked exception with a compensating control, a named owning function, and an expiry, never a silent overdue. Feed the highest-exposure findings into the risk register so the program is steered by real weakness, not only by audit cadence.

## Parameters

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Critical remediation SLA (internet-facing / sensitive data) | 15 days | Maximum from confirmed finding to remediation for the highest-exposure systems. |
| High remediation SLA | 30 days | Tune by exposure; sensitive-data systems trend toward the critical timeline. |
| Scan cadence | continuous in pipeline; external surface at least weekly | Discovery is continuous, not a quarterly event. |
| Exception ceiling | time-bound, compensating control required | No vulnerability sits overdue without a tracked exception and an expiry. |

## Control enhancements

- **VPM-01(1) Multi-source continuous discovery.** Pipeline dependency/image scanning, running-estate and external-surface scanning, and advisory intake feed one normalized queue.
- **VPM-01(2) Exposure-weighted SLAs.** Remediation timelines are set by severity and exposure together; internet-facing and sensitive-data systems carry the tightest clocks.
- **VPM-01(3) Patch through the change gate.** Remediations ship via the governed pull-request change path (CHG-02), so the fix produces its own evidence.
- **VPM-01(4) Tracked, expiring exceptions.** A miss past SLA becomes an exception with a compensating control, a named owner, and an expiry.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. Vulnerabilities are discovered continuously across code, dependencies, images, and infrastructure.
2. Findings are triaged by severity and exposure and assigned the corresponding SLA.
3. Remediations are delivered within SLA, or carried as a tracked, time-bound exception with a compensating control.
4. Internet-facing and sensitive-data systems receive the tightest remediation timelines.

## Assessment methods

**Examine**

- The vulnerability-management policy, the SLA matrix, and the scanner and advisory-source inventory.
- The current finding queue with severity, exposure, age, and disposition.
- The exception register with compensating controls and expiries.

**Interview**

- Security on triage, the SLA model, and how exposure is weighted.
- Engineering on how patches ship through the change path and how exceptions are tracked.

**Test**

- Sample findings and confirm triage, SLA assignment, and on-time remediation or a valid exception.
- Confirm an internet-facing sample carries the critical SLA and was met or exception-tracked.
- Confirm no overdue finding exists without a tracked, unexpired exception.

## Evidence

Per finding: source, severity, exposure class, affected asset, age, SLA, disposition, and exception status.

- Record shape: [`evidence-schemas/VPM-01.yaml`](../evidence-schemas/VPM-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from the scanner and ticketing systems of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A daily job reads the normalized finding queue and computes: criticals past SLA on internet-facing or sensitive-data systems (target zero), highs past SLA, and overdue findings without a tracked exception.
- Drift Issue: Any nonzero count opens an Issue tagged VPM-01 naming Security as owner with the affected assets and the framework impact (SOC 2, ISO 27001, NIST CSF).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC7.1 | framework-mapped |
| ISO/IEC 27002:2022 | 8.8 | framework-mapped |
| NIST CSF 2.0 | ID.RA-01, PR.PS-02 | framework-mapped |

## RACI asks by audience

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own discovery, triage, and the SLA model; certify no overdue critical on an exposed or sensitive-data system. |
| Engineering | R | Remediate within SLA through the change gate; the merge is the fix evidence. |
| GRC | C | Carry exposure-weighted findings into the risk register so leverage steers remediation. |
| Auditor | I | Receive the computed finding queue and exception register; sample against the scanner, not a report. |
