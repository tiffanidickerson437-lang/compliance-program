# OWASP LLM Top 10 (2025) control mapping

One control and one evidence test per item. The OWASP Top 10 for LLM Applications (2025) is the practitioner's risk list for generative and agentic AI. Each item below maps to a control in the owned library, a concrete mitigation, an accountable function, and a test that produces evidence. Where an item is governed by the agent spec, it points to `agent-governance.md`.

Governing control across the set: AAT-01. Companions: CHG-02, MON-01, TPM-01, IRO-01, PRI-03.13.

## Summary table

| ID | Risk | Primary control | Evidence test |
|----|------|-----------------|---------------|
| LLM01 | Prompt Injection | AAT-01, CHG-02 | Injection eval suite result on the pull request |
| LLM02 | Sensitive Information Disclosure | AAT-01, PRI-03.13 | Broker decision records show minimum-scope release and consent checks |
| LLM03 | Supply Chain | TPM-01, CHG-02 | Provider tier with current SOC 2 or ISO 27001; pinned model versions |
| LLM04 | Data and Model Poisoning | TPM-01, CHG-02 | Training-data provenance and eval-gate result before deploy |
| LLM05 | Improper Output Handling | AAT-01, CHG-02 | Output-handling eval; human gate on irreversible actions |
| LLM06 | Excessive Agency | AAT-01 | Purpose-token TTL and human-gate records; agent registry |
| LLM07 | System Prompt Leakage | AAT-01, MON-01 | No secrets in prompts attestation; leakage eval |
| LLM08 | Vector and Embedding Weaknesses | AAT-01, IAC-17 | Access scoping on the vector store; embedding-change review |
| LLM09 | Misinformation | AAT-01, CHG-02 | Grounding and quality eval; human review on customer-facing output |
| LLM10 | Unbounded Consumption | MON-01, CHG-02 | Rate and cost limits; consumption regression in the eval gate |

## LLM01: Prompt Injection

Risk: crafted input overrides instructions or smuggles a malicious instruction through retrieved content, steering the model to act against policy.

Mitigation: treat all model input as untrusted; separate system instructions from user and retrieved content; constrain the agent so a successful injection still cannot exceed its registered purpose and least-privilege scope (`agent-governance.md`); run an injection eval suite as a required check on every prompt or model change (CHG-02).

Owner: Engineering (R), Security (A).

Evidence test: the injection eval result attached to the pull request, plus broker decision records showing that even on a triggered action the released scope stayed within the registered ceiling.

## LLM02: Sensitive Information Disclosure

Risk: the model reveals sensitive data, including precise location or a minor's data, in an output or to a party that should not receive it.

Mitigation: minimum-scope field release at the authorization broker; consent enforcement (PRI-03.13) so a minor's data is never released without active consent; restricted data classes (children's data, precise location) never enter an ungoverned model; the broker records what was released and what was withheld.

Owner: Security (A), Legal/Privacy (A on lawful basis), Engineering (R).

Evidence test: AAT-01 broker decision records showing `data_released` and `data_withheld`, joined to consent state; the consent register (PRI-03.13).

## LLM03: Supply Chain

Risk: a compromised or untrustworthy model, library, or provider enters the system through the AI supply chain.

Mitigation: foundation-model providers are tiered under TPM-01 by what they can touch, with current SOC 2 Type II or ISO 27001 plus AI-specific terms (training-on-customer-data, region, retention, sub-processor chain, model-update notice, exit) on record; model versions are pinned and changed only through CHG-02; dependencies are inventoried and monitored.

Owner: GRC (A), Engineering (R).

Evidence test: the TPM-01 register entry for each provider with assurance-evidence expiry; the pinned-version configuration in the change record.

## LLM04: Data and Model Poisoning

Risk: training, fine-tuning, or retrieval data is manipulated to bias or backdoor model behavior.

Mitigation: provenance and integrity controls on any data used for training, fine-tuning, or retrieval; restricted classes excluded from training by default; the pre-deploy eval gate (CHG-02) detects behavior changes before a poisoned candidate reaches production; drift checks catch post-deploy shifts (MON-01).

Owner: Model owner (A), Engineering (R).

Evidence test: data-source provenance record; the eval-gate result and drift comparison on the change.

## LLM05: Improper Output Handling

Risk: model output is passed to a downstream system without validation, enabling injection, unsafe actions, or data leakage in the consuming system.

Mitigation: treat model output as untrusted input to the next system; validate and encode before use; the human oversight gate (AAT-01) stands in front of irreversible actions; an output-handling eval is a required check on changes (CHG-02).

Owner: Engineering (R), Security (A).

Evidence test: output-handling eval result; broker records showing the human gate on irreversible actions.

## LLM06: Excessive Agency

Risk: an agent has more capability, permission, or autonomy than its purpose requires, so a fault or manipulation causes harmful action. This is the central risk for an agent on a family-safety location graph.

Mitigation: the full agent spec in `agent-governance.md`: sponsored non-human identity, registered bounded purpose, no standing access, least-privilege purpose tokens with a short TTL, a human gate on irreversible or minor-account actions, full delegation logging, and a kill-switch.

Owner: Security (A), Engineering (R), Legal/Privacy (A on lawful basis).

Evidence test: AAT-01 broker decision records (token TTL, scope, human gate, decision); the agent registry showing `standing_access: none`; the kill-switch tabletop result.

## LLM07: System Prompt Leakage

Risk: the system prompt is extracted, revealing instructions, guardrails, or, in a poorly built system, secrets.

Mitigation: no secrets, credentials, or sensitive data in system prompts as a hard rule; secrets come from a secrets manager, not the prompt; a leakage eval probes for extraction; prompt content is a CHG-02 change and is reviewed; monitoring flags anomalous extraction attempts (MON-01).

Owner: Engineering (R), Security (A).

Evidence test: the no-secrets-in-prompts review check on prompt changes; the leakage eval result.

## LLM08: Vector and Embedding Weaknesses

Risk: weaknesses in the vector store or embedding pipeline allow unauthorized retrieval, cross-tenant leakage, or embedding inversion that recovers sensitive source data.

Mitigation: access scoping and tenant isolation on the vector store enforced through the access model (IAC-17 for the human and service accounts that touch it); restricted data classes excluded from embeddings; embedding and retrieval changes pass review (CHG-02); the broker mediates retrieval that touches sensitive data (AAT-01).

Owner: Engineering (R), Security (A).

Evidence test: access scoping configuration and the IAC-17 recertification for accounts with vector-store access; the embedding-change review record.

## LLM09: Misinformation

Risk: the model produces confident, wrong, or fabricated output that a person or system relies on.

Mitigation: grounding and retrieval for claims that must be accurate; a quality and grounding eval as a required check (CHG-02); a human review gate on customer-facing or high-impact output; clear scoping so the agent does not answer outside its purpose.

Owner: Model owner (A), Product (C), Engineering (R).

Evidence test: the grounding and quality eval result on the change; the human-review record for customer-facing output.

## LLM10: Unbounded Consumption

Risk: uncontrolled inference volume drives denial of wallet or denial of service through cost or resource exhaustion, including model-extraction by high-volume querying.

Mitigation: rate limits and quotas per agent and per purpose; cost and token budgets monitored (MON-01) with an alert and a drift issue when a budget is breached; consumption regression is part of the eval gate (CHG-02); anomalous volume is an incident candidate (IRO-01).

Owner: Engineering (R), Security (A).

Evidence test: rate-limit and budget configuration; MON-01 alerts and drift issues for consumption; the consumption regression line in the eval result.

## How this renders to other frameworks

Each mitigation above is an instance of an owned control, so the same evidence answers NIST AI RMF (MEASURE and MANAGE in particular) and ISO/IEC 42001 Annex A operational controls without a second control set. See `nist-ai-rmf-alignment.md` and `iso-42001-alignment.md`.
