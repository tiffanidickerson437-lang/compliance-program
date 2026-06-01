# Agent governance control spec

The implementation specification for AAT-01 where it is sharpest: an autonomous agent acting on a real-time location graph, including the location of minors. This document defines how an agent authenticates, what it is scoped to touch, what gets logged, where a human stands in the path, and how the agent is stopped. It is written once and renders into ISO 42001, NIST AI RMF, and the OWASP LLM Top 10 at once.

Governing control: AAT-01. Companion controls: PRI-03.13 (consent), IRO-01 (incident response), CHG-02 (change control for prompts and tool grants).

## Principle

Deny by default. An agent holds no standing entitlement to production data. Access is granted per action, scoped to the minimum fields, time-boxed by a token TTL, logged as a decision record, and gated by a named human when the action is irreversible or touches a minor's account or precise location. The broker decision record is the evidence, not a screenshot and not a model-written narrative.

## 1. Agent identity

Every agent is a managed non-human identity, registered before it can request anything.

Registry entry, required fields:

- `agent_id`: stable identifier, for example `safety-alert-agent`.
- `human_sponsor`: the role accountable for this agent. A role, never standing as an individual in this repository.
- `purpose`: the bounded reason the agent exists. An agent scoped to crash detection cannot be repurposed without a change request.
- `allowed_triggers`: the events that may initiate a sensitive read.
- `data_scope`: the maximum field set the agent may ever request, enforced as a ceiling by the broker.
- `standing_access`: must be `none` for production data.
- `kill_switch_owners`: roles that can revoke this agent immediately.

Rules:

- No agent runs without a registry entry and a named human sponsor.
- Agent credentials are non-human identity credentials, short-lived, and rotated automatically. No shared accounts, no long-lived tokens, no hardcoded secrets.
- An unregistered identity requesting sensitive data is a MON-01 alert and an IRO-01 incident candidate.

## 2. Least privilege and purpose-bound tokens

The agent does not hold the data scope it is registered for. It requests authorization per action, and the authorization broker (policy as code, for example Open Policy Agent) decides.

Flow:

1. A registered trigger fires (for example, a high-confidence crash detection).
2. The agent requests a purpose token from the broker, naming the trigger, the lawful basis, and the minimum fields it needs.
3. The broker evaluates policy: is the agent registered, is the trigger allowed, is consent active, is the requested scope within the registered ceiling, is a human gate required.
4. On grant, the broker issues a purpose token with a finite TTL (for example, 120 seconds). The token authorizes exactly the named fields for exactly that window.
5. On deny, the agent gets nothing and the denial is logged.

The token is purpose-bound: it authorizes one purpose, one scope, one window. There is no refresh into standing access. When the TTL expires, the authorization is gone and a new action requires a new decision.

## 3. The broker decision record (the evidence)

Every decision, grant or deny, writes one record. This is the AAT-01 evidence, defined in `02-controls/evidence-schemas/AAT-01.yaml`.

```yaml
control: AAT-01
period: 2026-Q2
source: Agent Authorization Broker (OPA) + Consent Service
agent_id: safety-alert-agent
trigger: crash_detection_high_confidence
lawful_basis: consent on record + vital interests
data_released: [lat, lon, timestamp]
data_withheld: [location_history, place_labels, contacts]
token_ttl_seconds: 120
consent_state: active
human_gate: required for irreversible action on minor account
decision: granted
ai_generated: false
```

The record proves minimum scope (what was released and what was withheld), time-boxing (the TTL), lawful basis, consent state at decision time, and whether a human gate applied. It is computed from the broker log joined to the consent store. `ai_generated` is always false; a model-authored record is rejected by schema.

## 4. The human oversight gate

Autonomy stops where the stakes are highest. A named human approves before the action proceeds in these cases:

- Any irreversible action on a minor's account.
- Disclosure of precise location to a third party or across a trust boundary.
- Any action the registry marks high-impact.

The gate is enforced at the broker, not left to the agent's discretion. When a gate applies, the broker withholds final authorization until a human in the accountable role approves, and the approval (role, timestamp, decision) joins the decision record. A gate that is required and not satisfied is a hard deny.

This is the line between automation and accountability. AI does the detection and the drafting at machine speed; a person owns the decision that cannot be undone.

## 5. Consent enforcement

For any read of a minor's data, the broker checks the consent service (PRI-03.13) at decision time. If consent is absent or withdrawn, the decision is deny, regardless of trigger. Consent withdrawal propagates immediately because the consent service is the system of record every read consults, so there is no cache of stale authorization. The consent state is recorded in the decision record.

## 6. Kill-switch

Any agent can be stopped immediately. The kill-switch is a first-class control, not an afterthought.

- Trigger: a kill-switch owner (a sponsor role or the SOC) invokes revocation, or an automated guardrail trips on anomalous agent behavior.
- Effect: the broker revokes the agent's ability to obtain new purpose tokens, and existing tokens are short-lived enough to expire on their own within the TTL window. The identity provider disables the agent's non-human identity.
- Evidence: the revocation event and the time from trigger to revoke are logged (MON-01) and, where an incident applies, recorded against IRO-01.
- Runbook: the kill-switch path lives in the AI-incident runbook so it is exercised, not theoretical. It is tested in the annual tabletop.

## 7. Delegation and full logging

When an agent calls a tool or hands off to another agent, the delegation is logged: which identity, which scope, under which purpose token, for which action. Tool grants are part of the agent's registered scope and change only through CHG-02. Full delegation logging is what makes excessive agency detectable rather than invisible.

## 8. Mapping to OWASP LLM excessive agency and output risks

This spec is the program's answer to OWASP LLM06 (Excessive Agency) and a contributor to LLM05 (Improper Output Handling) and LLM02 (Sensitive Information Disclosure). The full mapping is in `owasp-llm-top10-mapping.md`. In short:

- Excessive agency is bounded by registered purpose, least-privilege purpose tokens, and the human gate.
- Sensitive-information disclosure is bounded by minimum-scope field release and the consent check.
- Output handling is bounded by the human gate on irreversible actions and by delegation logging.

## 9. RACI (from AAT-01)

| Role | RACI | Ask |
|------|------|-----|
| Security | A | Own the authorization broker and deny-by-default policy; certify no agent holds standing location entitlement outside an active safety event. |
| Engineering | R | Bind every location read to a purpose token with a TTL and emit the decision record; the broker log is the evidence, not screenshots. |
| Legal/Privacy | A | Name the lawful basis for processing precise location, sign the DPIA, and confirm minors' data use is limited to the requested service. |
| C-Suite / Board | I | Accept the residual risk of an agent touching sensitive location data, with the kill-switch owner named. This is a board-visible risk. |
| Customer | I | Receive plain-language notice of what the safety agent accesses and the consent toggle; the consent state feeds the control. |
| Auditor | I | Receive the computed decision log plus the DPIA and policy version; sample against the log, not a live demo. |

## 10. What an auditor or assessor receives

- The agent registry, showing every agent has a sponsor, a bounded purpose, and `standing_access: none`.
- A sample of broker decision records for the period, reconciled to the DPIA and the policy version in effect.
- The consent-enforcement evidence (PRI-03.13) showing denies on withdrawn consent.
- The kill-switch test result from the annual tabletop.

No live demo, no reconstructed narrative. The evidence already exists because the broker produced it as a byproduct of operating.
