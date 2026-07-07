# Program Charter

**Pillar:** 00-governance
**Configuration:** illustrative example in `config.example.yaml` (neutral; not a real organization).
**Program owner:** GRC function
**Status:** Scaffold. Ratify and date after Phase 1 discovery and a sign-off by the governing body.
**Review cadence:** Annual, and on any material change to `config.example.yaml`.

---

## 1. Purpose

This charter establishes a framework-agnostic compliance program whose controls are
defined once, evidenced from systems of record, and rendered into every applicable
framework from a single source of truth in this repository. The program is operational
infrastructure for the business, not paperwork assembled for an audit. Compliance built
for the audit is a tax. Built for the business, it is infrastructure. This program is the
second kind.

## 2. Thesis

One owned control set, defined once, rendered into the language every function speaks. The
repository is the program of record and holds the depth. A separate scan layer summarizes
it for fast reading. The repository is the nucleus; the summary is the highlight reel.

## 3. Scope

In scope:

- All frameworks named in `config.example.yaml`. For this configuration: SOC 2, ISO 27001, GDPR, CCPA
  as amended by CPRA, the amended COPPA Rule, NIST AI RMF, ISO 42001, and the EU AI Act.
- The consumer family-safety and location service, the location-graph data domain, and the
  agentic AI layer that operates on it.
- Every pillar under `compliance-program/` as the operational backbone: governance, risk,
  controls, third-party risk, AI governance, secure development, evidence and audit, and
  stakeholder management.
- People and non-human identities, including service accounts and AI agents, that touch
  in-scope systems or data.

Out of scope:

- Any assertion about the organization's current internal control posture. This program is
  illustrative and states what a mature program would look like, not what exists.

## 4. Authority and decision rights

- The GRC function owns the control library, the framework crosswalk, the evidence schemas,
  and the design of continuous monitoring. GRC defines how a control is stated and measured.
- The business owns risk appetite and every risk-treatment decision. GRC supplies the model,
  the data, and the options. The business signs. See `risk-appetite-statement.md`.
- Security, Engineering, Legal, Privacy, IT, Product, and other functions own execution of
  the controls assigned to them under the RACI in `roles-and-responsibilities.md`.
- Internal Audit keeps independent third-line testing. Internal Audit does not build or
  operate controls, so its independence is preserved.
- The governing body accepts residual risk that exceeds the stated appetite and receives the
  reporting defined in `committee-charter.md`.

## 5. Operating model (GitHub-native)

The program runs as a system, not a binder. The mechanism:

1. **Config drives the scaffold.** `config.example.yaml` names the frameworks, data types, AI
   posture, listings, and stack. A GitHub Action filters the control library to those
   frameworks and turns on the pillars and families those values require.
2. **Controls as code.** Every control is defined once in Git: versioned, peer-reviewed,
   and diffable. A framework view is a rendering of the same control, never a copy.
3. **Continuous checks.** Automated checks compute control health from the systems of
   record named in `stack`.
4. **Drift opens an Issue.** A failed check files a GitHub Issue with the control ID, drift
   type, owning function, framework impact, and the evidence needed to close. That Issue,
   timestamped and retained, is the evidence of due diligence.
5. **The Pull Request is the human gate.** AI drafts the remediation and the narrative. A
   named function reviews. The merge is the authorization. Nothing becomes record without
   the human gate.
6. **Git history is the audit trail.** On merge the control status updates. The commit
   history is the immutable record of who decided what, when, and why.

Code decides pass or fail. The system of record supplies the evidence. AI drafts the
narrative and the gap analysis. A human approves before anything becomes record.

## 6. How `config.example.yaml` governs this charter

This charter is configuration-driven. Company-specific scope is not written into prose; it is read
from `config.example.yaml`. The frameworks list above is the current value of `frameworks`. The AI
governance scope exists because `ai-products` is true. Change the config and re-run the scaffold,
and the in-scope statements re-render. This keeps the charter true to the program as configured
rather than drifting from it.

## 7. Guardrails

- No claim is made about current internal security posture without verification.
- Evidence is computed from systems of record. AI-generated content that is presented as
  evidence is rejected by schema. AI drafts narratives; it does not author evidence.
- Functions and roles are named, never individuals. Accountability attaches to a function.
- The repository is the system of record for evidence. A GRC tool is the audit-facing
  interface. If the tool is unavailable, the evidence still lives here.

## 8. Definitions

- **Control:** a single, owned statement of required behavior, defined once and mapped to
  every framework it satisfies.
- **Evidence:** a record computed from a system of record that demonstrates a control is
  operating.
- **Drift:** a measured deviation from a control's required state, detected by an automated
  check.
- **Human gate:** the point where autonomous action stops and a named function approves.
- **Function:** an accountable role in the business (governance, security, engineering,
  legal, privacy, product, sales, finance, IT, HR, internal audit, board, customer).

## 9. Ratification

This charter takes effect when the governing body approves it and Phase 1 discovery has
validated `config.example.yaml`. Until then it is a scaffold. Amendments follow the change process
for Tier 0 documents in `policy-hierarchy.yaml`.
