# NIST AI RMF 1.0 alignment

How the owned control set answers the NIST AI Risk Management Framework across its four functions: GOVERN, MAP, MEASURE, and MANAGE. The framework is a view over controls that already exist, so one control set answers an RMF questionnaire without rewriting controls.

Direct catalog crosswalk (real references from `02-controls/framework-crosswalk.yaml`):

| Control | NIST AI RMF references |
|---------|------------------------|
| AAT-01 | GOVERN 1.0, GOVERN 2.1, GOVERN 4.1, MAP 3.5 |
| TPM-01 | MANAGE 3.0 |
| IRO-01 | GOVERN 6.2, MANAGE 2.4 |

The sections below show how program activities satisfy each function. The MEASURE function is answered operationally through the evaluation gate and the OWASP LLM mapping; the direct catalog references sit where the crosswalk records them.

## GOVERN

The culture, accountability, and policy layer. This is where AAT-01 lives most directly.

- GOVERN 1.0 (policies, processes, procedures for AI risk are in place, transparent, and implemented): AAT-01 defines, owns, and enforces AI and autonomous-tech risk policy. Governance review is quarterly, with a DPIA on material change.
- GOVERN 2.1 (roles and responsibilities are documented and accountability is clear): the AAT-01 RACI names the accountable function for the broker, the lawful basis, residual-risk acceptance, and the kill-switch. Functions and roles, never individuals.
- GOVERN 4.1 (a culture of risk management and a commitment to safety): deny-by-default authorization and the human gate on irreversible actions on minors encode safety into the operating model, not into a slogan.
- GOVERN 6.2 (incident response and recovery plans for AI are in place): IRO-01 covers AI scope breaches, with a kill-switch path in the AI-incident runbook and a post-incident review on every incident.

Evidence: the AI policy and DPIA versions, the agent registry, the AAT-01 broker decision records, and the IRO-01 incident records.

## MAP

Establishing context and identifying risk for each AI use case.

- MAP 3.5 (AI risks and benefits are mapped, including impacts on individuals and groups): each use case is mapped to its data classes and its affected population, with children's data and precise location carved out as restricted. The hardest case, an agent acting on the real-time location of minors, is mapped explicitly and governed by AAT-01.

The EU AI Act use-case classification in `eu-ai-act-readiness.md` is the same mapping exercise rendered for that regime, so the MAP work is done once and reused.

Evidence: the use-case classification and data-class mapping; the DPIA that records affected individuals and lawful basis.

## MEASURE

Analyzing, assessing, and tracking AI risk.

The measurement surface is the evaluation gate in `model-change-management.md` and the OWASP LLM Top 10 tests in `owasp-llm-top10-mapping.md`. Before any model, prompt, or tool-grant change ships, it is measured for safety, quality and regression, prompt-injection resistance, output handling, and consumption. In production, scheduled drift checks re-measure against the baseline and open a tracked issue on a material shift (MON-01).

Evidence: eval-gate results attached to change records (CHG-02); drift issues opened by MON-01; the OWASP test results per item.

## MANAGE

Prioritizing and acting on risk, including third-party and incident risk.

- MANAGE 2.4 (mechanisms are in place to sustain the value of deployed AI, and to supersede, disengage, or deactivate systems that demonstrate performance or outcomes inconsistent with intended use): the kill-switch and the rollback path are the disengage mechanism. An agent acting out of scope is revoked immediately, and a degraded model is rolled back to a pinned known-good state.
- MANAGE 3.0 (AI risks from third parties and supply chain are managed): TPM-01 tiers foundation-model and subprocessor risk by what each can touch, with current assurance evidence and AI-specific contract terms on record.

Evidence: the kill-switch tabletop result and any production revocation events (IRO-01, MON-01); rollback records on change (CHG-02); the TPM-01 provider register.

## One mapping, many uses

The same activities that satisfy NIST AI RMF satisfy ISO/IEC 42001 and the OWASP LLM Top 10, because all three resolve to the same owned controls. Adding the next AI framework is a crosswalk and a profile, not a new program. See `02-controls/README.md` for the mechanism.
