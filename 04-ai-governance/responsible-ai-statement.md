# Responsible-AI statement (trust-center collateral)

A one-page, customer-facing statement written to sit on a trust center, next to the SOC 2 and ISO badges, not buried in a policy repository. It is generated from the control set, and a companion traceability table maps every public claim back to an enforced internal control, so the marketing line and the audit evidence never diverge.

This is collateral: a publishable statement in the organization's voice. The traceability note below it is in program voice and is the proof behind the statement.

---

## How we use AI responsibly

We build AI to make families safer, and we govern it so that safety is never the cost of the feature.

**Where a human stays accountable.** Our AI can detect, draft, and act quickly, but a person stays accountable for decisions that matter. Any high-impact or irreversible action on a child's account, and any sharing of precise location, requires a named human to approve it. AI does the heavy lifting; people own the consequential call.

**What trains our models, and what does not.** Children's data and precise-location data are restricted. They are not used to train foundation models by default, and they are never sent to an AI system we do not govern. When an AI feature needs sensitive data to do its job, it gets only the specific fields it needs, only for the moment it needs them.

**How location and children's data are bounded.** An AI agent never holds standing access to your location. Each time a feature needs location, it requests a time-limited, purpose-specific authorization that expires in seconds, and every request is logged. For a child's data, that request is denied unless verifiable parental consent is active. Withdraw consent and access stops immediately.

**You can see and control it.** What an AI feature accesses is disclosed in plain language, and the consent and location controls are yours to set. When you change them, the system honors the change right away.

**If something goes wrong.** We monitor AI behavior continuously and can disable any agent immediately. AI-specific incidents are handled by the same incident-response program as any other, with notification to you and to regulators when the law requires it.

---

## Companion note: every claim traces to a control

The statement above is not marketing copy written in isolation. Each public claim is backed by an enforced control and a computed evidence record, so a customer's security team, an auditor, and the trust center are looking at the same truth.

| Public claim | Enforced control | Evidence |
|--------------|------------------|----------|
| A human approves high-impact or irreversible actions on a child's account and precise-location sharing | AAT-01 human oversight gate | Broker decision records showing the satisfied human gate |
| Children's and precise-location data are restricted and not used to train models by default | AAT-01 data boundaries; AI data classification | Restricted-class configuration; data-provenance records (OWASP LLM04) |
| AI gets only the fields it needs, only when it needs them | AAT-01 least-privilege purpose tokens | Decision records with `data_released`, `data_withheld`, and `token_ttl_seconds` |
| A child's data is denied without active parental consent, and withdrawal stops access immediately | PRI-03.13 consent enforcement | Consent register; broker deny events on withdrawn consent |
| What an AI feature accesses is disclosed and controllable | AAT-01 customer RACI; consent toggle | Consent state feeding the control; the disclosure notice |
| AI behavior is monitored continuously and any agent can be disabled immediately | MON-01; AAT-01 kill-switch | Coverage report; revocation events and time-to-revoke |
| AI incidents are handled and notified per law | IRO-01 | Incident records with notification decision and basis |

## Why this matters

A trust statement that cannot be traced to a control is a liability: it is a promise with no enforcement behind it. This statement is the readable surface of controls the program already operates and already evidences. The customer reads one paragraph; the auditor samples the same control; the claim and the proof are the same object. That is the program working as designed, with the public site as the highlight reel pointing at evidence the program owns.
