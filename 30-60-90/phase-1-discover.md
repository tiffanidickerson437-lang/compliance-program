# Phase 1: Discover (Days 1 to 30)

**Pillar:** 30-60-90
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).
**Constraint:** 100 percent discovery. No assumptions about internal state beyond what external
research and interviews establish. No building.

**Tag legend:**
- **[PUBLIC]** established for the example configuration; answerable from outside the organization.
- **[INSIDER]** requires internal access; the example configuration cannot establish it.

---

## Objectives

1. Establish one shared baseline so every function works from the same picture, not several
   partial ones.
2. Validate `config.example.yaml` against reality: frameworks, data types, AI posture, stack,
   listings.
3. Map the location graph data flows for location and minors' data, including agent touchpoints.
4. Map where compliance slows engineering today.
5. Separate what external research answers from what only an insider can confirm, and prioritize
   the insider questions for the interview.

## Tie to the example situation forces

- Real-time location for tens of millions, including children: COPPA, GDPR, and CCPA apply
  together. **[PUBLIC]**
- An agentic AI bet on the location graph while audit frameworks for autonomous systems are still
  forming. **[PUBLIC]**
- Enterprise security reviews increasingly gate deals on AI and data handling. **[PUBLIC]**
- Public scrutiny and litigation over historical location-data practices set the context for
  current commitments. **[PUBLIC]**

## Activities by week

**Week 1: Business and stakeholders**
- Meet the functions: security leadership, engineering leadership, legal and privacy, finance,
  and sales and go-to-market leadership. **[INSIDER]**
- Record what each function wants from GRC and how it wants to receive the signal. **[INSIDER]**
- Confirm the stated company goals: agentic AI on the location graph and COPPA readiness. The
  goals are **[PUBLIC]**; their internal priority and timing are **[INSIDER]**.

**Week 2: Systems and data**
- Validate the `stack` assumptions in `config.example.yaml`: cloud, identity, code host, ticketing,
  docs, comms, and GRC tool. The likely stack is **[PUBLIC]** inference; the actual stack is
  **[INSIDER]**.
- Walk the location and minors' data paths. Identify the consent service, the authorization
  broker, the logging sources, and the vendor register. **[INSIDER]**
- List subprocessors and foundation-model providers from public trust materials. The public
  list is **[PUBLIC]**; the complete current list and contract terms are **[INSIDER]**.

**Week 3: Controls and frameworks**
- For each seed control in `02-controls/control-library.yaml` (AAT-01, PRI-03.13, IAC-17,
  CHG-02, MON-01, TPM-01, IRO-01), determine operating, partial, or unknown, with an owner and
  an evidence source. **[INSIDER]**
- Run crosswalk queries against `framework-crosswalk.yaml`: what satisfies the COPPA security
  program, what satisfies SOC 2 access. The mapping is **[PUBLIC]**; the operating state is
  **[INSIDER]**.
- Mark nothing operating without a validated evidence path.

**Week 4: Gaps and the interview backlog**
- Publish discovery findings split into known from external research and requires insider
  confirmation.
- Prioritize the insider-only questions below.
- Hold the build phase until Phase 1 sign-off.

## Insider-only questions (require internal access)

1. Where is verifiable parental consent enforced in the request path for every minor-account
   feature and every agent? **[INSIDER]**
2. Does an agent authorization broker exist with deny-by-default and TTL-bound purpose tokens
   for location reads? **[INSIDER]**
3. What is the real logging source-coverage count and the alert-acknowledgement SLA?
   **[INSIDER]**
4. How many vendors are high-risk, and how many are overdue for reassessment on the live
   register? **[INSIDER]**
5. What is the leaver-feed latency from the HR system to identity-provider deprovisioning?
   **[INSIDER]**
6. For the last production-merge period, how many changes lacked a linked ticket or independent
   review? **[INSIDER]**
7. Who owns the kill-switch for autonomous agents acting on minors' accounts? **[INSIDER]**

## Deliverables (end of day 30)

| Deliverable | Done looks like |
|-------------|-----------------|
| Validated `config.example.yaml` | Frameworks, data types, AI posture, stack, and listings confirmed with the business. |
| Stakeholder map | Every function, what it wants from GRC, and its escalation path, signed. |
| Control inventory | Each seed control marked operating, partial, or unknown, with an owner and an evidence source. |
| Regulatory obligation register | COPPA (compliance date 2026-04-22), GDPR, CCPA and CPRA, and EU AI Act timeline. |
| Location-graph data-flow map | Location, minors' data, and agent touchpoints, with public subprocessors and models flagged. |
| Engineering friction map | Where compliance slows deploys, and which gates are manual versus already in CI/CD. |

## Maturity signal

Baseline. Everyone shares one baseline instead of several partial ones. The program can state,
with an owner and an evidence source per control, what is known and what is still an open
question for the interview.

## Explicit non-claims

- No statement about current compliance posture or control deficiencies.
- No assertion that existing programs have gaps.
- Nothing that requires internal access to verify is presented as verified.

## Exit criteria for Phase 2

- Signed stakeholder map and validated `config.example.yaml`.
- Control inventory with an owner and an evidence source per seed control.
- Regulatory register and data-flow map reviewed by legal and privacy.
- Engineering friction map reviewed by engineering leadership.
- Program-owner approval to begin design.
