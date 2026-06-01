# Auditor Narrative Template

**Pillar:** 06-evidence-and-audit
**Owner (function):** GRC (accountable for the narrative leaving the building). AI drafts; a human approves.
**Depends on:** [`evidence-architecture.md`](./evidence-architecture.md)

## Purpose

An auditor narrative explains a control to an auditor: what the control does, how it operates, and where the evidence proves it. The narrative is drafted by AI from the computed evidence and approved by a human before it leaves the building. The narrative is written once and reused so the auditor confirms what the program already knows, which is what produces zero follow-ups and first-submission acceptance.

## The division of labor

| Step | Who | Output |
|------|-----|--------|
| Supply the proof | System of record (code) | Computed evidence record, `ai_generated: false` |
| Draft the narrative | AI | A narrative referencing the record |
| Approve and own | Human (GRC, function) | The narrative as a record, via merged pull request |

AI drafts the prose. It never produces the underlying evidence and never approves its own draft. The human gate is the merge. This is the program's operating model applied to audit deliverables.

## The template

Each narrative follows the same structure so an auditor can navigate any control the same way.

```markdown
# Control narrative: <CONTROL-ID>, <name>

## Control statement
<The statement from control-library.yaml, verbatim. What the control commits to.>

## How it operates
<Plain description of the operating mechanism, drawn from implementation_guidance.
 Names the system of record that enforces and the system that observes.>

## Period covered
<e.g., 2026-Q2>

## Evidence
<Reference to the computed record(s). Source system, what was sampled, the result.
 No screenshots; the computed export is the proof.>

## Exceptions and how they were handled
<Any exception in the period, with the closure path. Stating exceptions plainly is
 what removes follow-ups; a clean narrative that hides an exception invites them.>

## Framework mappings
<From framework-crosswalk.yaml: every framework reference this control satisfies.>

## Approver
<Function that approved. Recorded by the merge, not signed by name here.>
```

## Worked example (CHG-02)

A drafted narrative, shown to illustrate the shape. The evidence values come from the `CHG-02` computed record, not from the model.

```markdown
# Control narrative: CHG-02, Configuration change control

## Control statement
Technical configuration change reaches production only through a peer-reviewed pull
request linked to a tracked work item, with required checks passing. Direct pushes to
protected branches are blocked, and emergency changes follow a documented after-the-fact
review.

## How it operates
Branch protection on the source-control platform is the technical enforcement. Every
production change arrives as a pull request with an independent reviewer, a linked work
item, and passing required checks. The merge record is pulled from the source-control
merge API; it is the evidence, not a reconstruction.

## Period covered
2026-05

## Evidence
Source: source-control branch protection plus merge API. For the period: 138 merges to
production, 138 with a linked ticket, 137 with independent review, 6 direct pushes blocked.
Sampled the merge log; no screenshots.

## Exceptions and how they were handled
One change merged without independent review under the emergency path. It was recorded as
an exception, reviewed after the fact within the SLA, and closed. The exception is stated,
not hidden.

## Framework mappings
SOC 2 CC3.4, CC8.1; ISO/IEC 27002 8.19, 8.32; NIST CSF ID.RA-07; SOX ITGC change
management (framework-mapped, home lab, never audited).

## Approver
Approved by GRC via merged pull request; merge is the authorization.
```

## Why exceptions are stated, not hidden

The fastest route to auditor follow-ups is a narrative that reads cleaner than the evidence. The narrative states every exception plainly, with its closure path, so the auditor sees that the program found and handled it. A stated, closed exception is a sign the control is alive. A hidden one, discovered in sampling, costs the whole submission its credibility.

## The approval gate

The drafted narrative is a proposal until a human approves it through a merged pull request. The pull request diff is reviewed against the computed evidence: every claim in the narrative must trace to a record. A claim with no backing record is removed before merge. This is the same gate the responsible-AI work in 04-ai-governance describes, where every public claim traces to an enforced internal control.

## Reuse

A narrative per control, per framework, is written once and re-rendered each period with the period's computed values. The structure does not change; only the evidence values and the exception list do. This is what turns audit prep into a dashboard check rather than an authoring sprint.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC4.1, CC4.2 |
| ISO/IEC 27001:2022 | 9.1, 9.2 |
| NIST CSF 2.0 | GV.OV |
