# 04-ai-governance: the centerpiece

Govern AI at the point of highest velocity and largest blast radius: ship fast, stay defensible, keep humans in the loop where it matters. This pillar governs autonomous agents acting on a real-time location graph, including the location of minors, which is the hardest AI-governance problem in consumer tech.

Everything here is grounded in one owned control, AAT-01 (AI and autonomous technologies governance), defined once in `02-controls/control-library.yaml`. This pillar implements that control, decomposes it into operating sub-controls, and renders it into every AI framework the business will be asked about. No control is redefined; the AI frameworks are views over the same definition.

## Read in this order

1. `ai-control-set.md`: the umbrella. AAT-01 as the spine, the operating sub-controls, the data boundaries, and how the set answers each AI framework.
2. `agent-governance.md`: the deep implementation spec. Agent identity, least privilege, purpose-bound tokens with a TTL, the human oversight gate on minors and precise location, consent enforcement, and the kill-switch.
3. `model-change-management.md`: change control for model swaps, version upgrades, prompt edits, and tool-grant changes, with evaluation, drift check, rollback, and a human approval gate.

## Framework alignments

- `owasp-llm-top10-mapping.md`: each OWASP LLM Top 10 (2025) item mapped to a control, a mitigation, and an evidence test.
- `nist-ai-rmf-alignment.md`: GOVERN, MAP, MEASURE, MANAGE.
- `iso-42001-alignment.md`: the AI management system layer, named honestly as a forward target.
- `eu-ai-act-readiness.md`: use-case classification and a gap log against the August 2 2026 high-risk obligations and GPAI transparency duties.

## Collateral (generated from the control set)

- `responsible-ai-statement.md`: the customer-facing trust statement, with a table tracing every public claim to an enforced control.
- `ai-acceptable-use-policy-summary.md`: the internal AI acceptable-use policy in operative summary form.

## The controls behind this pillar

| Control | Role here |
|---------|-----------|
| AAT-01 | The governing control. Agent authorization, least privilege, human gate, logging. |
| PRI-03.13 | Consent enforcement for any read of a minor's data. |
| CHG-02 | The change gate for model, prompt, and tool-grant changes. |
| TPM-01 | AI vendor and foundation-model provider risk. |
| MON-01 | Continuous monitoring of AI behavior and the kill-switch evidence. |
| IRO-01 | AI-incident response, including agent scope breaches. |

## Constraints honored throughout

- Functions and roles only. No individual is named.
- No claim is made about any real organization's internal AI posture. This is an illustrative working model.
- AI drafts; a human approves before anything becomes a record. Evidence is computed from systems of record, never authored by a model.
- A named human stands in front of any high-impact agent action on a child's account or a precise-location disclosure.
