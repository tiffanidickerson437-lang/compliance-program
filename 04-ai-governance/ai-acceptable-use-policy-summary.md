# AI acceptable-use policy (summary)

The internal AI acceptable-use policy in summary form: the one-page version a new engineer reads on day one and a manager links in a channel. The full policy lives in governance; this is the operative summary, tied to the control set so the rules are enforced, not just published.

Governing control: AAT-01. Companions: PRI-03.13 (minors), TPM-01 (AI vendor intake), CHG-02 (prompt and tool-grant changes).

## Purpose

Internal AI adoption is near universal, and that is fine. The policy exists so AI accelerates the work without putting regulated data, customers, or the company at risk. It draws the line between sanctioned use and the two failure modes that matter: regulated data going into ungoverned models, and AI tools entering the company without review.

## Sanctioned models and data classes

Use AI through sanctioned models and routes only. A sanctioned model is one that has passed vendor intake (TPM-01) with acceptable terms on training-on-customer-data, region, retention, sub-processor chain, model-update notice, and exit.

Data classes and where they may go:

| Data class | Sanctioned model | Ungoverned model |
|------------|------------------|------------------|
| Public or non-sensitive internal data | Permitted | Discouraged |
| Confidential business data | Permitted with care | Prohibited |
| Regulated PII | Permitted only in an approved, governed configuration | Prohibited |
| Children's data | Restricted; governed path only, consent-gated (PRI-03.13) | Prohibited |
| Precise-location data | Restricted; governed path only, broker-mediated (AAT-01) | Prohibited |

Restricted classes (children's data, precise location) never enter an ungoverned model under any circumstance.

## Prohibited uses

- Putting regulated PII, children's data, or precise-location data into an ungoverned model or a personal AI account.
- Procuring or adopting an AI tool outside vendor intake (no shadow-AI procurement). A free trial that touches company or customer data is a procurement.
- Using AI to make a consequential decision about an individual without the human oversight required by AAT-01.
- Embedding secrets, credentials, or sensitive data in prompts (see OWASP LLM07).
- Shipping a model, prompt, or tool-grant change to production outside the change gate (CHG-02).

## Approval path

Approval is tied to vendor intake, so the policy is enforced at the point of adoption, not by reminder.

1. Want to use a new AI tool or model that touches company or customer data: route it through vendor intake (TPM-01). AI drafts the gap analysis from the vendor's SOC 2 or ISO report; a human GRC owner validates the tier and the terms before access is granted.
2. Want to change a prompt, model, or tool grant in a product: open a pull request through the change gate (CHG-02), with evaluation and a rollback plan (see `model-change-management.md`).
3. Want to use AI on restricted data classes: the governed path only, consent-gated and broker-mediated. Legal/Privacy is a required reviewer.

## Role-based expectations

- Engineering: ship AI changes only through the change gate; bind sensitive reads to purpose tokens; never embed secrets in prompts.
- Product: disclose AI interactions to users; design consent and disclosure flows without dark patterns.
- Security: own the authorization broker, the sanctioned-model list, and monitoring of AI use.
- Legal/Privacy: own lawful basis and the minors and precise-location review; required reviewer on restricted-data use.
- Everyone: keep regulated and restricted data out of ungoverned models, and route new AI tools through intake.

## How this is enforced

The policy is not honor-system. Sanctioned routes are the ones with access; ungoverned routes do not get restricted data because the broker and data-access layer deny it. New tools that skip intake do not get credentials. Prompt and model changes that skip the gate do not merge. The acceptable-use rules above each map to a control that enforces them, which is why this summary can be short: the system, not the document, holds the line.
