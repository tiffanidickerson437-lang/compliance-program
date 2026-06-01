# AI control set

The centerpiece of the program. This is the AI governance control set, grounded in the hero control AAT-01 (AI and autonomous technologies governance) and rendered into the AI-specific frameworks the business will be asked about: ISO/IEC 42001, NIST AI RMF, the OWASP LLM Top 10, and the EU AI Act.

The thesis holds here as everywhere: one owned control, defined once in `02-controls/control-library.yaml`, evidenced once, satisfies many frameworks. This directory does not redefine AAT-01. It implements it, decomposes it into operating sub-controls, and shows how it answers each AI framework.

## The governing control

AAT-01 is the spine.

> Policies for AI and autonomous-tech risk are defined, owned, and enforced. Agents read location or minor data only under purpose-bound authorization, minimum scope, full logging, and human accountability for high-impact actions.

Owner: GRC + Security, with Legal/Privacy joint on lawful basis. Automation: partial. Review: continuous, with quarterly governance review and a DPIA on material change.

Crosswalk (real references, from the control library):

| Framework | References |
|-----------|-----------|
| NIST AI RMF 1.0 | GOVERN 1.0, GOVERN 2.1, GOVERN 4.1, MAP 3.5 |
| ISO/IEC 42001:2023 | 5.1, 8.1, A.2.2, A.6.2.2 |
| SOC 2 (TSC 2017) | CC1.4 |
| EU AI Act (2024) | Art.17(1)(c) |

The companion control for minors is PRI-03.13 (verifiable parental consent), and the companion control for AI incidents is IRO-01 (incident response operations, AI scope breaches in scope). AI vendor and model-provider risk runs through TPM-01. AI change control runs through CHG-02 and is detailed in `model-change-management.md`.

## Why this is the hardest AI-governance problem in consumer tech

An autonomous agent acting on a real-time location graph, including the whereabouts of minors, at machine speed, is the sharp end of AI governance. The blast radius is a child's physical location. The velocity is autonomous. The regulatory clock is running: the amended COPPA Rule applies from April 2026, and EU AI Act high-risk obligations land from August 2 2026. The control set is built to govern that, not a chatbot.

## The sub-controls that operate AAT-01

AAT-01 is one library control. In operation it decomposes into a set of enforceable sub-controls, each with an owner, an enforcement point, and a computed evidence record. None of these is a new SCF control; they are the implementation surface of AAT-01 and its companions.

| Sub-control | What it enforces | Enforcement point | Evidence | Detailed in |
|-------------|------------------|-------------------|----------|-------------|
| Agent identity | Every agent is a sponsored non-human identity with a human sponsor | Identity provider, agent registry | Registry entry, sponsor of record | `agent-governance.md` |
| Least privilege and purpose-bound tokens | No standing access to production data; each sensitive read uses a short-lived purpose token | Authorization broker (policy as code) | Broker decision record with token TTL | `agent-governance.md` |
| Human oversight gate | A named human approves irreversible or high-impact actions on a minor account or precise-location disclosure | Authorization broker, workflow gate | Gate decision joined to the action | `agent-governance.md` |
| Consent enforcement | No agent reads a minor's data when consent is absent or withdrawn | Consent service, broker | Consent state at decision time (PRI-03.13) | `agent-governance.md` |
| Kill-switch | Any sponsor or the SOC can revoke an agent's access immediately | Broker, identity provider | Revocation event, time to revoke | `agent-governance.md` |
| Model and prompt change control | Model swaps, version upgrades, prompt and tool-grant changes pass evaluation, drift check, and a human approval gate | Pull request, eval gate (CHG-02) | Merge record, eval result, rollback plan | `model-change-management.md` |
| AI incident response | AI scope breaches are detected, contained with the kill-switch, and reviewed | IR platform (IRO-01) | Incident record with kill-switch action | `agent-governance.md`, IRO-01 |

## Data boundaries

AI data is classified into tiers, and the most sensitive classes are carved out as restricted: children's data and precise-location data. Restricted classes never enter an ungoverned model, never train a foundation model by default, and are released to an agent only through the authorization broker under an active purpose token. Training data, prompts, embeddings, outputs, and inference logs each carry their own handling rule. The boundary is enforced at the broker and the data-access layer, not asserted in a policy PDF.

## How the set answers each AI framework

Each AI framework is a view over the same control set. The detail lives in the aligned documents.

- ISO/IEC 42001:2023, the AI management system layer, named honestly as a forward target. See `iso-42001-alignment.md`.
- NIST AI RMF 1.0, mapped across GOVERN, MAP, MEASURE, and MANAGE. See `nist-ai-rmf-alignment.md`.
- OWASP LLM Top 10 (2025), one control and one evidence test per item. See `owasp-llm-top10-mapping.md`.
- EU AI Act (2024), use-case classification and a gap log against the high-risk and GPAI obligations. See `eu-ai-act-readiness.md`.

## Collateral

Two customer-facing and internal-facing pieces are generated from this control set, so the public claim and the enforced control never diverge:

- `responsible-ai-statement.md`: the one-page statement that belongs on a trust center.
- `ai-acceptable-use-policy-summary.md`: the internal AI acceptable-use policy in summary form.

## Constraints honored

- Functions and roles only. No individual is named.
- No claim is made about any real organization's internal AI posture. This is an illustrative working model.
- AI drafts narratives and gap analyses; a human approves before anything becomes a record. Evidence is computed from systems of record, never authored by a model.
- Human approval stands in front of any high-impact agent action on a child's account or a precise-location disclosure.
