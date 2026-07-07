# Maturity Roadmap

**Pillar:** 30-60-90
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization)
**Status:** Scaffold. Month zero is the program start date; every milestone is relative to it.

---

## 1. The arc, in one line

The program matures along a dependency chain: discover the ground truth, define a common-control
spine, compute continuous evidence from that spine, govern the agentic AI layer on top of that
evidence, then let measured risk drive what gets hardened next. The chain is unchanged from a
traditional program. What changes is the pace: AI collapses the drafting, mapping, and narrative
authoring that stretch a conventional build to twelve or eighteen months, so the arc reaches an
operating program in about ninety days and an optimizing one at about six months.

## 2. Why AI compresses the curve

A traditional program spends most of its calendar on documentation: authoring an obligation
register, mapping controls to frameworks one clause at a time, writing control descriptions, and
drafting auditor narratives. That authoring is exactly what a model does in minutes instead of
weeks. Removing it does not remove the program; it removes the typing.

What remains sets the pace, and it is not text:

- **Human decisions.** A drafted obligation register, crosswalk, or control is a proposal. A named
  function still validates it, decides what is in scope, and approves it by merge. AI does not
  shorten the decision; it shortens the wait for something to decide on.
- **Wiring systems of record.** Computed continuous evidence depends on instrumenting the source
  systems that produce it. That is integration work across teams, paced by how fast a source can
  be connected, and a model does not accelerate it.
- **Fixed external dates.** A statutory compliance date does not move because drafting is faster.
  It is a hard milestone the program plans toward regardless of pace.

So the compression is real but bounded. The pace-setter shifts from how fast prose can be written
to how fast humans can decide and how fast systems of record can be wired.

## 3. Maturity model

| Level | Meaning |
|-------|---------|
| Baseline | One shared picture exists; the program knows what it does and does not know. |
| Defined | Controls are defined once and crosswalked; one control satisfies many frameworks. |
| Managed | Control health is computed continuously from systems of record, not reconstructed at audit. |
| Quantitatively managed | Risk and AI behavior are measured; agents run inside live, logged guardrails. |
| Optimizing | Risk decides what gets hardened next; trust shortens enterprise reviews. |

## 4. Stages and the boundary that ends each one

| Timing | Level | Stage | What AI drafts, what a human owns | The boundary that ends the stage |
|--------|-------|-------|-----------------------------------|----------------------------------|
| Weeks 1 to 3 | Baseline | Discover | AI drafts the regulatory obligation register and the data-flow map for precise location and minors' data. A human validates each against reality. | One validated baseline exists: the obligation set and the data flows are confirmed, not assumed. |
| Weeks 4 to 8 | Defined | Common-control spine | AI generates the SCF crosswalks and the first control drafts. A named function decides scope, owner, and evidence source, and approves by merge. | Every in-scope control is defined once, crosswalked, owned by a function, and assigned an evidence source. |
| Months 2 to 4 | Managed | Computed continuous evidence | AI drafts the narratives; the evidence itself is computed, never AI-authored. Wiring the systems of record is the real pace-setter. | Control health is computed continuously from systems of record rather than reconstructed at audit. This is the operating milestone, reached at about ninety days. |
| Months 3 to 5 (overlapping) | Quantitatively managed | Agentic AI governance | AI drafts the AI management-system documents and the gap log; engineering wires the broker, the kill-switch, and agent logging. | The agentic layer operates inside live, measured guardrails. The boundary is a fixed external regulatory date, not a drafting speed. |
| Month 6 onward | Optimizing | Risk-driven, revenue-enabling | AI drafts the risk and trust narratives; the risk signal is computed from the evidence and the agent logs. | The program emits a measured risk signal that sets the hardening backlog. Ongoing. |

The agentic stage overlaps the computed-evidence stage on purpose: it consumes the monitoring
substrate the Managed stage builds, so its engineering can begin as soon as the substrate exists
rather than waiting for the stage to close.

## 5. Why each boundary sits where it does

The boundaries are precedence constraints, not a calendar drawn first and filled in afterward.
Each later stage is impossible, or produces rework, without the earlier one.

- **Discover before Define.** A common control cannot be defined without first knowing the
  obligation set and the data flows for precise location and minors' data. AI drafts that baseline
  in days, but designing a control library on an unvalidated picture still guarantees a second
  pass, so the Baseline stage ends only when a human has validated the drafted baseline.

- **Define before Manage.** A control cannot be monitored continuously until it has been defined
  once, owned by a function, and pointed at an evidence source. AI generates the crosswalks and the
  control drafts quickly, but continuous evidence computes against a control's required state, so
  there is nothing to compute against until the definition and the source are settled and approved.

- **Manage before AI governance.** Governing an autonomous agent means proving it stayed in scope,
  and that proof is the continuous logging and computed evidence built in the Managed stage.
  Standing up agent governance first would mean governing on assertions rather than on evidence.

- **AI governance before Optimize.** Letting the risk register, rather than the audit calendar,
  set the backlog requires a measured risk signal across the controls and the agentic layer. That
  signal does not exist until the prior stages produce it.

The strongest boundary is Define before Manage. It is the point where evidence stops being
assembled by hand for an audit and starts being computed continuously from systems of record. AI
moves the program to that point faster; it does not let the program skip it.

## 6. Total duration, and why it is about six months

The arc reaches the operating milestone at about ninety days and the Optimizing inflection at
about month six, after which Optimizing is continuous. The figure is set by what AI cannot
compress:

- The drafting inside Discover and Define collapses from weeks to days, which is why the first two
  stages fit inside the first two months rather than the first two quarters.
- The floor on the operating milestone is wiring systems of record for continuous evidence in the
  Managed stage. That is integration work, paced by how fast source systems can be instrumented,
  not by how fast a control can be drafted, so it holds the operating milestone near ninety days
  regardless of drafting speed.
- The agentic AI governance stage is paced by a fixed external regulatory date and by the
  engineering of the broker, the kill-switch, and agent logging, so it runs into months three to
  five even though its documents draft quickly.

A shorter headline would require compressing the integration work or the fixed external date,
neither of which moves because prose is faster to produce. Six months is the honest figure for an
AI-accelerated program reaching the point where it optimizes itself, against twelve to eighteen
months when the drafting is done by hand.

## 7. Regulatory and business drivers that pace the curve (generic)

The shape of the curve is universal; specific drivers move the milestones earlier or later for a
given configuration:

- A children's-privacy rule with a fixed compliance date pulls the evidenced privacy pack to the
  front of the Managed stage.
- An annual certification cycle for the primary frameworks (for example SOC 2 and ISO 27001) sets
  the audit-readiness milestone inside the Managed stage.
- High-risk AI obligations with a statutory start date set the deadline the agentic AI governance
  stage must meet, not merely plan toward. This is the fixed date that paces months three to five.

## 8. How the 30-60-90 connects

- Phase 1 (Discover) is weeks 1 to 3 of the Baseline stage.
- Phase 2 (Design) builds the Defined stage's common-control spine across weeks 4 to 8.
- Phase 3 (Operate) opens the Managed stage, where computed evidence begins and the operating
  milestone is reached at about ninety days.

The first quarter does not finish the journey, but with AI compressing the drafting it now reaches
the operating milestone rather than only an operational baseline.

## 9. How the configuration drives the roadmap

- `frameworks` sets which obligations and audit milestones appear on the curve.
- `ai-products: true` puts the agentic-AI-governance stage on the curve at all; a non-AI program
  would not carry the months 3 to 5 stage as written.
- `regulated-jurisdictions` sets which privacy regimes pace the early stages.

Change the configuration and the milestones re-render. The shape of the curve, set by the
dependency chain, is the program; the pace and the drivers are the instance.

## 10. The throughline

The program matures from standing itself up to carrying the business's goals, and it does so in
about six months because AI removes the documentation tax while the human decisions and the
systems-of-record wiring set the floor. By the Optimizing inflection the risk register, not the
audit calendar, decides what gets hardened next, and the trust the program computes is cited in
closing enterprise deals. Compliance built for the audit is a tax. Built for the business, it is
infrastructure, and this roadmap is the dependency-ordered, AI-accelerated path that gets there.
