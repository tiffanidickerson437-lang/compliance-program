# Risk Appetite Statement

**Pillar:** 00-governance
**Owner:** the business, through the governing body (Audit and Risk Committee)
**Author and steward:** GRC function populates this statement; the business ratifies it.
**Status:** Scaffold. The bands below are proposed defaults for the business to ratify.
**Seeded by:** `config.example.yaml` field `risk.appetite: growth-stage` and `risk.tolerance-statements`.

---

## 1. Ownership

Risk appetite is a business decision. GRC supplies the model, the data, and the options. The
business sets the appetite and signs each treatment decision. GRC does not accept risk on the
business's behalf. This statement is populated in the governance pillar for visibility, but
its authority comes from the governing body's ratification, not from GRC.

## 2. How `config.example.yaml` drives this statement

The configured appetite is `growth-stage`. That value sets the default posture below: room to
move quickly where data is not sensitive, and a low to zero tolerance where the business holds
precise location and children's data. The hard limits in section 5 are the
`risk.tolerance-statements` from `config.example.yaml`, rendered as enforceable thresholds. Change the
appetite in the config and re-ratify, and these bands re-render.

## 3. Overall appetite

The business pursues growth and ships quickly. It accepts measured operational and schedule
risk to do so. It does not accept risk to the safety, privacy, or lawful handling of precise
location and children's data, because that data is the trust the product is built on. Speed is
welcome on the routine path. On the sensitive path, a human gate is mandatory and a control may
stop a release.

## 4. Appetite by category

Appetite levels: **none**, **low**, **moderate**, **elevated**. Each category names the
tolerance threshold that triggers escalation and a treatment decision.

| Risk category | Appetite | What it means | Escalation trigger |
|---------------|----------|---------------|--------------------|
| Children's data and consent | none | No processing of a minor's data without verifiable parental consent. No dark patterns. | Any processing or disclosure without active consent. |
| Precise-location exposure | low | Location is accessed only under purpose-bound authorization with logging and a human gate on irreversible actions. | Any standing or unlogged location entitlement; any agent acting outside an active purpose. |
| Agentic AI behavior | low | Autonomous agents act inside least-privilege scopes; high-impact actions on minors or location pass a human gate. | An agent acting out of scope, or a high-impact action without a recorded human approval. |
| Regulatory and privacy compliance | low | Statutory obligations are met within their timelines (COPPA, GDPR, CCPA, EU AI Act). | A missed statutory deadline or a known unremediated obligation gap. |
| Security and breach | low | Defense in depth; rapid detection and containment; breach notification within statutory windows. | A Sev1 incident, or detection-to-triage time outside the agreed SLA. |
| Change and availability | moderate | Ship quickly through reviewed Pull Requests; tolerate measured change risk on the routine path. | A material unreviewed production change, or an emergency-change rate above the agreed bound. |
| Third-party and subprocessor | low | Diligence matches what a vendor can touch; highest scrutiny on parties touching location or minors' data. | A high-risk vendor without current assurance evidence, or a subprocessor breach. |
| Financial-reporting (SOX ITGC) | low | IT general controls over access, change, and operations are reliable and testable. | A control deficiency that could affect the reliability of financial reporting. |

## 5. Hard limits (zero tolerance)

These are the `risk.tolerance-statements` from `config.example.yaml`. They are not aspirational; they
are gates the program enforces and the register treats as out of appetite by definition:

1. Agent access to precise location or minors' data requires purpose-bound authorization and a
   human gate for irreversible actions.
2. Minor data processing is denied when verifiable parental consent is absent or withdrawn.
3. No regulated personal data enters an ungoverned AI model.

A condition that breaches a hard limit is escalated to the governing body and treated, never
silently accepted.

## 6. Connection to the FAIR register

Appetite is the line the quantified register is measured against. In
`01-risk-management/risk-register.yaml`, each scenario carries a residual loss-exposure range
computed FAIR-style. A residual exposure above the band for its category, or any breach of a
hard limit, is out of appetite and requires a treatment decision signed by the business.
Appetite turns a dollar figure into a decision: harden, transfer, avoid, or formally accept.

## 7. Review and change

- Reviewed at least annually by the governing body, and on any material change to
  `config.example.yaml`, the threat landscape, or the regulatory calendar.
- Amendments follow the Tier 0 change process in `policy-hierarchy.yaml`.
- The current ratified version and date are recorded by the governance function and reported to
  the Audit and Risk Committee per `committee-charter.md`.
