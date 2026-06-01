# Model change management

Change control for the AI system itself. A model swap, a version upgrade, a prompt edit, or a tool-grant change is a configuration change to production, and it moves through the same gate as any other change: a peer-reviewed pull request with required checks passing. This document specializes CHG-02 (configuration change control) for AI-specific changes and ties them back to AAT-01.

Governing controls: CHG-02 (the change gate) and AAT-01 (agent scope and tool grants). Companion: IRO-01 (rollback and incident path).

## What counts as a change

Any of the following is a tracked change and cannot reach production by a direct push:

- Model swap: replacing one foundation model or provider with another.
- Version upgrade: moving to a new version of the same model, including silent provider updates that must be pinned and reviewed.
- Prompt change: edits to system prompts, instructions, or guardrail prompts.
- Tool-grant change: adding, widening, or removing a tool or data scope an agent may call. This is also an AAT-01 registry change.
- Retrieval or embedding change: changes to the vector store, embedding model, or retrieval policy.
- Parameter change: changes to temperature, max tokens, or other inference parameters that affect behavior or cost.

## The gate

The pull request is the gate. Branch protection is the technical enforcement (CHG-02). A change reaches production only when:

1. It is a peer-reviewed pull request linked to a tracked work item.
2. The pre-deploy evaluation passes.
3. The drift check passes.
4. A rollback plan is attached.
5. A human in the accountable role approves. For tool-grant or data-scope changes that touch minors or precise location, the AAT-01 human gate applies and Legal/Privacy is a required reviewer.

Direct pushes to the protected branch are blocked. Emergency changes follow a documented after-the-fact review and are reconciled as exceptions.

## 1. Pre-deploy evaluation

No model or prompt change ships without an evaluation against a held-out suite. The eval gate is a required check on the pull request.

Evaluation dimensions:

- Safety: refusal and guardrail behavior on prohibited and sensitive prompts, including minors and precise location.
- Quality and regression: task performance against the prior baseline, so a change does not silently degrade the behavior users depend on.
- Prompt-injection resistance: behavior under adversarial inputs (OWASP LLM01).
- Output handling: structured-output conformance and unsafe-output rates (OWASP LLM05).
- Cost and latency: token consumption and response time, to catch unbounded-consumption regressions (OWASP LLM10).

The eval result is recorded and attached to the pull request. A failing eval blocks the merge.

## 2. Drift check

Models and providers change underneath a pinned integration, and behavior drifts even when configuration does not. The program checks drift in two places:

- Pre-deploy drift: the candidate is compared to the current baseline on the eval suite, and a material behavior change is flagged for explicit human acceptance even if absolute scores pass.
- In-production drift: scheduled re-runs of the eval suite against the live model detect provider-side changes. A drift beyond threshold opens a tracked issue (the MON-01 drift-opens-an-issue mechanism) and triggers a review.

## 3. Rollback

Every change carries a rollback plan before it merges.

- The prior model version, prompt version, and tool-grant set are pinned and retained so a revert is a known-good state, not a reconstruction.
- Rollback is executable through the same pull-request path, or faster through the kill-switch when an agent is acting out of scope (see `agent-governance.md`).
- The rollback trigger conditions are stated in the change: which eval or drift signal, which incident severity, which owner decides.

## 4. Human approval gate

A named human approves the change. Approval is not a formality:

- For prompt and parameter changes: an independent engineering reviewer plus the model owner.
- For model swaps and version upgrades: the model owner plus Security, with a TPM-01 check on the provider's terms (training-on-customer-data, region, retention, sub-processor chain, model-update notice, exit).
- For tool-grant or data-scope changes touching minors or precise location: the AAT-01 human gate, with Legal/Privacy as a required reviewer and a DPIA review on material change.

## 5. Evidence

The evidence is the CHG-02 merge record, plus the AI-specific artifacts attached to it. See `02-controls/evidence-schemas/CHG-02.yaml`.

```yaml
control: CHG-02
period: 2026-05
source: GitHub (branch protection + merge API)
merges_to_prod: 138
with_linked_ticket: 138
with_independent_review: 137
direct_pushes_blocked: 6
exceptions_without_review: 1
ai_generated: false
```

For AI changes specifically, the merge carries the eval result, the drift comparison, the rollback plan, and, where applicable, the AAT-01 registry diff and the human-gate approval. The merge record is pulled from the source-control API, not reconstructed. Evidence is a byproduct of how the change shipped.

## 6. Provider risk linkage

A model swap or new provider is also a third-party event (TPM-01). The provider is tiered by what it can touch, and a current SOC 2 Type II or ISO 27001 plus the AI-specific terms are on record before the change merges. AI drafts the gap analysis from the provider's report; a human GRC owner validates the tier before it is recorded.

## 7. RACI

| Role | RACI | Ask |
|------|------|-----|
| Engineering | R | Ship model, prompt, and tool-grant changes only through a reviewed pull request with passing eval and drift checks and an attached rollback plan. |
| Security | A | Own the change-control policy and the eval gate configuration; reconcile emergency changes as exceptions. |
| Model owner | A | Own the evaluation suite and the acceptance thresholds; sign the change. |
| Legal/Privacy | C | Required reviewer for tool-grant or data-scope changes touching minors or precise location; confirm DPIA currency. |
| Auditor | I | Receive the computed merge log with attached eval and drift artifacts; no screenshots of individual pull requests. |
