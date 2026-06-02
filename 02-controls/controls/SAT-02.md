# SAT-02: Security awareness and role-based training

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/SAT-02.yaml`](../evidence-schemas/SAT-02.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | SAT (Security Awareness & Training) |
| Class | SCF |
| NIST CSF function | Protect |
| Family | awareness and training |
| Owner (by function) | Security (People/HR delivers) |
| Automation | partial |
| Review cadence | annual baseline; role-based on assignment and on material change |

## Why this control

This is the control that legitimately sits at SOC 2 CC1.4 — commitment to competence — which is why AAT-01 was moved off it. People are the control surface that no broker covers: the engineer who mishandles a location export, the support agent who is socially engineered into disclosing a minor's data. A workforce trained to the specific risks of precise location, minor data, and an agentic AI layer is a control, and its absence is the soft spot a determined attacker targets first.

## Control statement

Personnel complete security and privacy awareness training on hire and on a recurring cadence, and role-based training is delivered to functions with elevated access or specific obligations. Training covers the risks specific to this service: precise-location and minor-data handling, social-engineering resistance, and the governance of the agentic AI layer. Completion is tracked, and non-completion for in-scope roles is an exception with a named owner.

## Implementation guidance

Deliver a baseline to everyone and a sharper, role-based module to the functions that carry elevated risk: engineers who can touch the location graph, support staff who field account requests, and the functions accountable for the AI layer and for consent. Tie the role-based content to the actual controls — what verifiable parental consent requires (PRI-03.13), what an agent is and is not allowed to do on a minor's account (AAT-01), how to handle a sensitive-data export (DCH-01) — so training reinforces the program rather than running parallel to it. Make completion a computed state drawn from the learning system of record keyed to the HRIS, so the in-scope population is current as people join, move, and leave, and a role change re-triggers the module its new access requires. Treat non-completion for an in-scope role as a tracked exception with an owner and an expiry, not a number that quietly drifts. Refresh content on material change — a new regulation, a new AI capability, a recurring incident theme — so the training tracks the risk rather than the calendar.

## Parameters

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Baseline cadence | on hire, then annually | All personnel; completion tracked against the HRIS population. |
| Role-based trigger | on assignment to an elevated-access or obligation-bearing role, and on material change | Engineers on the location graph, support, AI-layer and consent owners. |
| Completion SLA (new hires) | 30 days from start | Maximum interval before baseline completion for a new joiner. |
| Non-completion handling | tracked exception, named owner, expiry | In-scope non-completion surfaces, never sits silent. |

## Control enhancements

- **SAT-02(1) Role-based modules tied to controls.** Elevated-access and obligation-bearing roles receive training mapped to PRI-03.13, AAT-01, and DCH-01, reinforcing the program's own controls.
- **SAT-02(2) HRIS-keyed completion state.** Completion is computed from the learning system of record keyed to the HRIS, so the in-scope population stays current through joins, moves, and leaves.
- **SAT-02(3) Re-trigger on role change.** A move into an elevated role re-triggers the module that role requires before access is exercised.
- **SAT-02(4) Content refresh on material change.** New regulation, new AI capability, or a recurring incident theme refreshes content out of the annual cycle.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. All personnel complete baseline awareness training on hire and on the recurring cadence.
2. Role-based training reaches the elevated-access and obligation-bearing functions, tied to the controls they operate.
3. Completion is computed from a system of record keyed to the current workforce population.
4. Non-completion for in-scope roles is carried as a tracked, time-bound exception.

## Assessment methods

**Examine**

- The training curriculum, the role-to-module mapping, and the completion records keyed to the HRIS.
- The content-refresh history against regulatory and incident triggers.
- The exception register for in-scope non-completion.

**Interview**

- Security on the curriculum and how role-based content maps to the controls.
- People/HR on how completion is tracked against joins, moves, and leaves.

**Test**

- Sample new hires and confirm baseline completion within SLA.
- Sample an elevated-access role and confirm the role-based module was assigned and completed on assignment.
- Confirm no in-scope role sits non-complete without a tracked, unexpired exception.

## Evidence

Per person in scope: role, assigned modules, completion status and date, and exception status for any non-completion.

- Record shape: [`evidence-schemas/SAT-02.yaml`](../evidence-schemas/SAT-02.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from the learning and HR systems of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A daily job joins the learning system of record to the HRIS and computes: in-scope personnel without current baseline completion, elevated-access roles without their role-based module, and new hires past the completion SLA.
- Drift Issue: Any nonzero count opens an Issue tagged SAT-02 naming Security as owner with the framework impact (SOC 2, ISO 27001, NIST CSF).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC1.4, CC2.2 | framework-mapped |
| ISO/IEC 27002:2022 | 6.3 | framework-mapped |
| NIST CSF 2.0 | PR.AT-01, PR.AT-02 | framework-mapped |

## RACI asks by audience

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own the curriculum and the role-to-control mapping; certify the in-scope population is current. |
| People/HR | R | Deliver training and keep completion keyed to the live workforce through joins, moves, and leaves. |
| Engineering | C | Confirm role-based content matches what each elevated role actually does on the location graph. |
| Auditor | I | Receive the computed completion state; sample against the learning record, not a sign-in sheet. |
