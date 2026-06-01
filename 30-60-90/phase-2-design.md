# Phase 2: Design (Days 31 to 60)

**Pillar:** 30-60-90
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).
**Constraint:** Design and architecture. Build the spine, do not yet declare it operating.

**Tag legend:**
- **[PUBLIC]** established for the example configuration; answerable from outside the organization.
- **[INSIDER]** requires internal access; confirmed during Phase 1.

---

## Objectives

1. Stand up one owned control library, defined once and crosswalked to every in-scope
   framework, so a single piece of evidence satisfies many.
2. Define the evidence schema for each control: what audit-ready proof looks like and which
   system of record produces it.
3. Design the first collect-once evidence pipelines from the systems named in `config.example.yaml`.
4. Wire controls into the developer workflow so evidence is a byproduct of shipping.
5. Run a gap analysis against the validated baseline and build the remediation backlog.
6. Put the program into the business rhythm: committee cadence, reporting templates, exception
   process live.

## Tie to the example situation forces

- Compliance cannot sit on the critical path of shipping at this growth stage, so controls are
  designed as policy-as-code and sprint tickets, not as a separate review gate. **[PUBLIC]**
- One sensitive-data access control maps to COPPA, GDPR, and CCPA at once, so location and
  family data obligations are met from a single definition. **[PUBLIC]**
- Multiple public listings mean the design must produce clean, computed ITGC inputs for access,
  change, and operations rather than a quarter-end scramble. **[PUBLIC]**

## Activities by week

**Week 5: Control architecture and crosswalk**
- Define the owned control spine from the seed controls and the families they imply.
- Crosswalk each control to SOC 2, ISO 27001, the COPPA security-program requirement, and SOX
  ITGC (framework-mapped). The crosswalk is the proof of the framework-agnostic claim.
- Confirm ownership per control against the RACI. Owners are **[INSIDER]**, confirmed in
  Phase 1.

**Week 6: Evidence schemas and collect-once pipelines**
- Define the evidence schema per control: fields, source system, and what makes a record
  audit-ready versus incomplete.
- Design the first computed pipelines from the validated stack (identity provider, source
  control, logging). Whether each integration exists today is **[INSIDER]**.
- Set the rule that AI-generated content presented as evidence is rejected by schema.

**Week 7: Developer-workflow integration and AI design**
- Translate controls into branch-protection settings and sprint tickets so the Pull Request is
  the gate and the merge is the evidence (CHG-02 pattern).
- Begin the AI governance design: agent identity, least-privilege tokens, human-oversight
  gates, and the OWASP LLM control set, mapped to NIST AI RMF and ISO 42001. The agentic bet is
  **[PUBLIC]**; the current agent inventory is **[INSIDER]**.
- Design the consent-service check that every minor-data path and agent calls (PRI-03.13).

**Week 8: Gap analysis and program rhythm**
- Run the gap analysis: for each control, the distance between the validated baseline and the
  designed target, scored against the FAIR register.
- Build the remediation backlog with owners and dates; route any near-term deviation through
  the exception process.
- Stand up the Security Steering Committee cadence and the reporting templates; schedule the
  first Audit and Risk Committee input.

## Deliverables (end of day 60)

| Deliverable | Done looks like |
|-------------|-----------------|
| Owned control library | Each in-scope control defined once, with owner, statement, and guidance. |
| Framework crosswalk | One control mapped to every framework it satisfies; queryable in seconds. |
| Evidence schemas | A schema per control naming the source system and the audit-ready bar. |
| Collect-once pipeline design | The first computed evidence flows specified against the real stack. |
| Developer-workflow integration | Branch protection and sprint-ticket patterns defined and agreed with engineering. |
| AI governance design | Agent identity, human-oversight gates, and the OWASP LLM set mapped to NIST AI RMF and ISO 42001. |
| Gap analysis and backlog | Scored gaps with owners, dates, and any exceptions recorded. |
| Program rhythm | Committee cadence live; reporting templates and exception process operating. |

## Maturity signal

Defined. One control satisfies many frameworks from a single piece of evidence, and the
manual-evidence count is on a path to fall. The spine exists; the next phase makes it run.

## Explicit non-claims

- A designed control is not an operating control. Nothing is declared operating in Phase 2.
- SOX ITGC design is framework mapping; operating effectiveness is established later, with
  Internal Audit.
- Pipeline designs assume the stack validated in Phase 1; any integration not yet present is a
  backlog item, not a claim.

## Exit criteria for Phase 3

- Control library and crosswalk reviewed and owned.
- Evidence schemas approved and the first pipelines specified.
- Developer-workflow integration agreed with engineering.
- Remediation backlog prioritized against the FAIR register.
- Program-owner approval to begin operating.
