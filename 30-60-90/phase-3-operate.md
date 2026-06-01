# Phase 3: Operate (Days 61 to 90)

**Pillar:** 30-60-90
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).
**Constraint:** Turn the designed spine into a running system. Declare operational only against
computed evidence, never against an assertion.

**Tag legend:**
- **[PUBLIC]** established for the example configuration; answerable from outside the organization.
- **[INSIDER]** requires internal access; exercised here with the real systems.

---

## Objectives

1. Turn on the collect-once evidence pipelines so control health is computed from systems of
   record.
2. Run continuous monitoring; prove the drift-opens-an-Issue mechanism end to end.
3. Run the first full reporting cycle to every stakeholder function from one source.
4. Run an audit-readiness assessment and close the gaps it surfaces.
5. Declare the program operational and set the trajectory to the next maturity stage.

## Tie to the example situation forces

- Audit prep that does not scramble: evidence is computed continuously, so audit readiness is a
  dashboard check, not a fire drill. **[PUBLIC]**
- A COPPA security program that can be evidenced, with the amended Rule compliance date of
  2026-04-22 in view. **[PUBLIC]**
- A trust center that reflects a state the program computes and owns, so the auditor confirms
  what is already known and the customer sees current posture. **[PUBLIC]**
- Sales can answer the routine majority of security questions from prevetted content and route
  the sensitive remainder to GRC under NDA. **[PUBLIC]**

## Activities by week

**Week 9: Evidence pipelines live**
- Turn on the computed pipelines for access (IAC-17), change (CHG-02), and logging (MON-01).
  Each emits a record against its schema. **[INSIDER]**
- Validate the first records against the audit-ready bar; reject anything incomplete or
  model-authored.

**Week 10: Monitoring and drift**
- Run continuous control-health checks. Prove the loop end to end: a failed check opens a
  GitHub Issue with control ID, drift type, owner, and framework impact, and that Issue is the
  due-diligence record. **[INSIDER]**
- Operate the exception process with live aging; surface anything past expiry.

**Week 11: First reporting cycle**
- Render the same control state for every function from one source: the board view in dollars,
  the executive view, the engineering view, and the prevetted sales content.
- Generate trust-center content from the control library and route it through human review
  before anything is public.
- Assemble the COPPA evidence pack from the consent system of record (PRI-03.13). **[INSIDER]**

**Week 12: Audit readiness and declaration**
- Run the audit-readiness checklist across SOC 2, ISO 27001, and the SOX ITGC mapping; every
  item green before any fieldwork. SOX operating effectiveness remains Internal Audit's to
  test, not GRC's to assert.
- Close the gaps the checklist surfaces or record them as exceptions with owners and dates.
- Declare the program operational and brief the Security Steering Committee and the Audit and
  Risk Committee.

## Deliverables (end of day 90)

| Deliverable | Done looks like |
|-------------|-----------------|
| Live evidence pipelines | Access, change, and logging evidence computed from systems of record. |
| Continuous monitoring | Health checks running; the drift-to-Issue loop proven end to end. |
| Exception register in use | Open items aged; nothing past expiry without escalation. |
| First reporting cycle | One control state rendered for board, executive, engineering, and sales. |
| COPPA evidence pack | Consent register computed and audit-ready. |
| Trust-center content | Generated from the library, human-reviewed, ready to publish. |
| Audit-readiness assessment | Checklist green across SOC 2, ISO 27001, and the SOX ITGC mapping. |
| Operational declaration | Program declared operating, with the maturity trajectory set. |

## Maturity signal

Managed, entering. Control health is monitored continuously rather than reconstructed at audit.
The program produces evidence as a byproduct of operating, and the next stage extends this to
agentic AI governance and to risk-driven prioritization. See `maturity-roadmap.md`.

## Explicit non-claims

- Operational means the program runs and computes evidence; it does not assert a passed external
  audit.
- SOX ITGC operating effectiveness is established by Internal Audit testing, not by this
  declaration.
- Evidence shipped in the repository as examples is illustrative until replaced by computed
  exports from the real systems.

## Handoff to the maturity roadmap

Phase 3 ends at the start of the maturity curve, not its end. `maturity-roadmap.md` carries the
trajectory from this operational baseline through continuous evidence, agentic AI governance,
and a risk-driven, revenue-enabling program.
