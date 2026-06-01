# Maturity Roadmap

**Pillar:** 30-60-90
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization)
**Status:** Scaffold. Month zero is the program start date; every month is relative to it.

---

## 1. The arc, in one line

The program matures along a dependency chain: discover the ground truth, define a common-control
spine, compute continuous evidence from that spine, govern the agentic AI layer on top of that
evidence, then let measured risk drive what gets hardened next. Each stage exists because the
next one cannot start without it. The dates are an instance; the precedence is the program.

## 2. Maturity model

| Level | Meaning |
|-------|---------|
| Baseline | One shared picture exists; the program knows what it does and does not know. |
| Defined | Controls are defined once and crosswalked; one control satisfies many frameworks. |
| Managed | Control health is computed continuously from systems of record, not reconstructed at audit. |
| Quantitatively managed | Risk and AI behavior are measured; agents run inside live, logged guardrails. |
| Optimizing | Risk decides what gets hardened next; trust shortens enterprise reviews. |

## 3. Stages and the boundary that ends each one

| Months | Level | Stage | What ships | The boundary that ends the stage |
|--------|-------|-------|------------|----------------------------------|
| 1 to 2 | Baseline | Discover | Control inventory, regulatory obligation register, real-time location-graph data-flow map for location and minors' data, and a map of where compliance slows engineering. | One validated baseline exists: the control universe, the obligation set, the data flows, and the friction points are known and agreed. |
| 2 to 5 | Defined | Common-control spine | One owned control library crosswalked to the in-scope frameworks, the OSCAL profiles that resolve each framework view, and the first collect-once evidence pipelines wired into the developer workflow. | Every in-scope control is defined once, crosswalked, owned by a named function, and assigned an evidence source. |
| 5 to 9 | Managed | Computed continuous evidence | Continuous control monitoring with exception aging, the drift-opens-an-Issue loop, and a fully evidenced children's-privacy pack. | Control health is computed continuously from systems of record rather than reconstructed at audit, and the highest-obligation pack sits at zero open items. |
| 9 to 15 | Quantitatively managed | Agentic AI governance | An AI control set grounded in ISO 42001 and NIST AI RMF: model inventory, data-use boundaries, agent-action logging, human gates, a kill-switch path, and a customer-facing AI trust statement. | The agentic layer operates inside live, measured guardrails, and every agent decision is logged and reviewable against the monitoring substrate built in the prior stage. |
| 15 onward | Optimizing | Risk-driven, revenue-enabling | A live risk register that prioritizes hardening by leverage, metrics that feed back into control design, and trust artifacts that shorten enterprise security reviews. | Ongoing. Risk leverage, not the audit calendar, sets the backlog. |

## 4. Why each boundary sits where it does

The phase boundaries are not a calendar drawn first and filled in afterward. Each one is a
precedence constraint: the later stage is impossible, or produces rework, without the earlier
one.

- **Discover before Define.** A common control cannot be defined without first knowing the
  control universe, the regulatory obligation set, the data flows for location and minors' data,
  and where compliance currently slows engineering. Designing a control library on an
  unvalidated picture guarantees a second pass once reality is confirmed, so the Baseline stage
  ends only when one validated baseline exists.

- **Define before Manage.** A control cannot be monitored continuously until it has been defined
  once, assigned an owning function, and pointed at an evidence source. Continuous evidence is
  computed against a control's required state; with no single definition and no named source
  system, there is nothing to compute against. The Defined stage therefore ends when every
  in-scope control is defined, crosswalked, owned, and sourced, and not before.

- **Manage before AI governance.** Governing an autonomous agent means proving it stayed in
  scope, and that proof is the continuous logging, drift detection, and computed evidence built
  in the Managed stage. Standing up agent governance first would mean governing on assertions
  rather than on evidence. The agentic stage consumes the monitoring substrate, so it follows
  the stage that creates it.

- **AI governance before Optimize.** Letting the risk register, rather than the audit calendar,
  decide what gets hardened next requires a measured risk signal across both the controls and
  the agentic layer. That signal does not exist until the prior stages produce it. Optimization
  is the inflection where quantitative inputs are finally rich enough to set the backlog, which
  is why it comes last and then continues indefinitely.

The strongest of these is Define before Manage. It is the boundary auditors and engineers both
feel, because it is the point where evidence stops being assembled by hand for an audit and
starts being computed continuously from systems of record.

## 5. Total duration, and why it is about fifteen months

The arc reaches the Optimizing inflection at roughly month 15, and Optimizing is then
continuous. The total is set by the dependency chain, not by preference:

- The Discover, Define, and Manage boundaries cannot be parallelized away, because each strictly
  depends on the one before it. The floor on calendar time is the slowest dependency to satisfy,
  which is wiring systems of record for continuous evidence in the Managed stage. That is
  integration work across teams, paced by how fast source systems can be instrumented, not by
  how fast a policy can be written.
- The AI governance stage is given a six-month window because it spans policy (an AI management
  system), engineering (the authorization broker, the kill-switch, agent logging), and legal
  (the data protection impact assessment, lawful basis, and high-risk AI readiness), and it must
  absorb at least one external regulatory milestone that has a fixed start date rather than a
  flexible one.

A shorter headline number would require either compressing a dependency that cannot be
compressed or declaring a stage complete before its boundary condition is met. Fifteen months is
the honest figure for reaching the point where the program optimizes itself.

## 6. Regulatory and business drivers that pace the curve (generic)

The shape of the curve is universal; specific drivers move the milestones earlier or later for a
given configuration:

- A children's-privacy rule with a fixed compliance date pulls the evidenced privacy pack to the
  front of the Managed stage.
- An annual certification cycle for the primary frameworks (for example SOC 2 and ISO 27001)
  sets the audit-readiness milestone inside the Managed stage.
- A publicly listed company's IT general controls and Audit and Risk Committee cadence place the
  SOX ITGC readiness milestone alongside the certification cycle.
- High-risk AI obligations with a statutory start date set the deadline the AI governance stage
  must meet, not merely plan toward.

## 7. How the 30-60-90 connects

- Phase 1 (Discover) is months 1 to 2 of the Baseline stage.
- Phase 2 (Design) builds the Defined stage's common-control spine, beginning at month 2.
- Phase 3 (Operate) opens the Managed stage, where computed evidence begins.

The first quarter does not finish the journey; it reaches the operational baseline from which
the program starts compounding.

## 8. How the configuration drives the roadmap

- `frameworks` sets which obligations and audit milestones appear on the curve.
- `ai-products: true` puts the agentic-AI-governance stage on the curve at all; a non-AI program
  would not carry the months 9 to 15 stage as written.
- `listings` places the SOX ITGC readiness milestone on the curve; a private program would not
  carry it.
- `regulated-jurisdictions` sets which privacy regimes pace the early stages.

Change the configuration and the milestones re-render. The shape of the curve, set by the
dependency chain, is the program; the dates and the drivers are the instance.

## 9. The throughline

The program matures from standing itself up to carrying the business's goals. By the Optimizing
inflection the risk register, not the audit calendar, decides what gets hardened next, and the
trust the program computes is cited in closing enterprise deals. Compliance built for the audit
is a tax. Built for the business, it is infrastructure, and this roadmap is the dependency-
ordered path that gets there.
