# AAT-01: AI and autonomous technologies governance

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/AAT-01.yaml`](../evidence-schemas/AAT-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | AAT (Artificial Intelligence & Autonomous Technologies) |
| Class | SCF |
| NIST CSF function | Govern |
| Family | AI governance |
| Owner (by function) | GRC + Security (Legal/Privacy joint on lawful basis) |
| Automation | partial |
| Review cadence | continuous; governance review quarterly, DPIA on material change |

## Why this control

An agentic layer acting on a real-time location graph of tens of millions of members, including children, needs a control for autonomous systems that read sensitive data and take consequential actions. This is the hero control: it governs how an agent is identified, scoped, gated, and revoked.

## Control statement

Policies for AI and autonomous-technology risk are defined, owned, and enforced. Autonomous agents read precise location or minor data only under purpose-bound authorization, at minimum scope, with full decision logging, and with human accountability for high-impact actions. No agent holds standing access to sensitive production data.

## Implementation guidance

Treat every autonomous agent as a sponsored non-human identity with a named human-function sponsor, a declared purpose, and a defined data scope. No agent holds standing access to precise location or minor data; access is brokered at the moment of need and expires automatically. The unit of evidence is the authorization decision, not a screenshot or an assertion. Place a central authorization broker, expressed as policy-as-code (for example Open Policy Agent), in front of every sensitive read. The broker evaluates each request against the requesting agent's identity, the declared purpose, the live consent state read from the consent system of record, and the data-minimization rule for that purpose. Default is deny. On a grant, bind the access to a purpose token with a short time-to-live so it cannot be reused outside the triggering event, release only the fields the purpose requires, and record the fields withheld, because demonstrable minimization is itself evidence. Stop any irreversible action, and any action on a minor's account, at a human gate: a named function approves before the action proceeds, and the approval is recorded against the decision. Map agent risks to the OWASP Top 10 for LLM Applications, in particular excessive agency, insecure output handling, and sensitive-information disclosure, and carry those mappings into the AI control set in 04-ai-governance. Maintain a kill-switch path that revokes all agent tokens and halts autonomous action within a defined interval, owned by a named function, and re-run the data protection impact assessment on any material change to agent scope, model, or purpose.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Purpose-token time-to-live ceiling | 300 seconds | A grant on precise location or minor data expires no later than this; tune down per purpose, never up. |
| Actions requiring a human gate | location_disclosure, action_on_minor_account, irreversible_write | Each listed action stops for a named-function approval recorded against the decision. |
| Kill-switch revocation interval | 5 minutes | Maximum interval from kill-switch activation to full token revocation and halt of autonomous action. |
| DPIA re-assessment trigger | material change to agent scope, model, or purpose | Any trigger forces a refreshed data protection impact assessment before the change ships. |

## Control enhancements

- **AAT-01(1) Deny-by-default brokered authorization.** Every sensitive read passes a central authorization broker that defaults to deny and evaluates identity, purpose, and live consent state.
- **AAT-01(2) Purpose-bound, time-boxed access.** Grants are bound to a declared purpose and a short-lived token; standing access to precise location or minor data is not permitted.
- **AAT-01(3) Human gate for irreversible or minor-account actions.** Irreversible actions, and any action on a minor's account, require a recorded approval by a named function before execution.
- **AAT-01(4) Kill-switch and revocation path.** A named function can revoke all agent tokens and halt autonomous action within the defined interval, exercised in test at least annually.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. Every agent with access to precise location or minor data is registered as a sponsored non-human identity with a named sponsor and no standing production-data access.
2. Every sensitive read is brokered deny-by-default against the live consent state.
3. Grants are purpose-bound, time-boxed within the TTL ceiling, and minimized to the fields the purpose requires.
4. Irreversible actions and minor-account actions pass a recorded human gate before execution.
5. A kill-switch with a named owner exists and revokes within the defined interval.
6. A current DPIA covers the agent scope and model in effect for the period.

## Assessment methods

**Examine**

- The AI and autonomous-technology policy, the agent registry, and the broker policy bundle in effect for the period.
- The data protection impact assessment and the lawful-basis determination for processing precise location and minor data.
- The kill-switch runbook and its most recent test record.

**Interview**

- The authorization-broker owner (Security) on deny-by-default behavior and TTL enforcement.
- Legal/Privacy on lawful basis, the DPIA, and the limits on minor-data use.
- Engineering on how each sensitive read is bound to a purpose token, and the kill-switch owner on the revocation path.

**Test**

- Replay a sample of broker decisions for agents with location or minor scope; confirm deny-by-default, TTL enforcement, and field minimization against the purpose rule.
- Drive a test account to consent-withdrawn state and confirm the broker denies the read.
- Attempt an irreversible action on a minor test account and confirm it blocks until the human gate is satisfied.
- Activate the kill-switch in a controlled test and confirm tokens revoke and autonomous action halts within the interval.

## Evidence

Broker decision record joined to the consent store: trigger, lawful basis, fields released, fields withheld, token TTL, consent state, human-gate status, and grant or deny.

- Record shape: [`evidence-schemas/AAT-01.yaml`](../evidence-schemas/AAT-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A daily job reads the broker decision store joined to the consent service and computes: percent of sensitive reads that were brokered, count of grants exceeding the TTL ceiling, count of grants issued while consent was withdrawn or absent, and count of irreversible minor-account actions with no recorded human gate.
- Drift Issue: Any nonzero count on the last three measures opens a control-drift Issue tagged AAT-01 with the offending decision IDs, the owning function (Security), and the framework impact (NIST AI RMF, ISO 42001, EU AI Act).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| NIST AI RMF 1.0 | GOVERN 1.0, GOVERN 2.1, GOVERN 4.1, MAP 3.5 | framework-mapped |
| ISO/IEC 42001:2023 | 5.1, 8.1, A.2.2, A.6.2.2 | framework-mapped |
| SOC 2 (TSC 2017) | CC6.1, CC6.2, CC6.3 | framework-mapped |
| EU AI Act (2024) | Art.17(1)(c) | framework-mapped |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own the authorization broker and deny-by-default policy; certify no agent holds standing location entitlement outside an active safety event. |
| Engineering | R | Bind every location read to a purpose token with a TTL and emit the decision record; the broker log is the evidence, not screenshots. |
| Legal/Privacy | A | Name the lawful basis for processing precise location, sign the DPIA, and confirm minor-data use is limited to the requested service. |
| C-Suite / Board | I | Accept the residual risk of an agent touching sensitive location data, with the kill-switch owner named. This is a board-visible risk. |
| Customer | I | Receive plain-language notice of what the safety agent accesses and the consent toggle; the consent state feeds the control. |
| Auditor | I | Receive the computed decision log plus the DPIA and policy version; sample against the log, not a live demo. |
