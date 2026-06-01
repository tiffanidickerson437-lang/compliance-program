# ai/ : where AI is used, and where it is not

This is the thesis of the program stated plainly. AI is used at one layer and
forbidden at another, and the line between them is enforced in code, not in a
policy that asks people to behave.

## The one-line boundary

AI drafts. Humans decide. Code computes the evidence.

- **AI drafts** the prose: auditor narratives, control-gap analyses, and
  crosswalk suggestions for a new framework.
- **Humans decide** by reviewing the draft and merging a pull request. The merge
  is the authorization. Nothing becomes a record without it.
- **Evidence is computed** from systems of record and is never AI-generated.
  Every evidence record carries `ai_generated: false`, and a record marked
  otherwise is rejected by schema.

## Where AI is used (drafting only)

| Use | What AI produces | What is committed | The artifact |
|-----|------------------|-------------------|--------------|
| Auditor narrative | A draft narrative for a control, from its computed evidence record | The narrative, after a human approves the pull request | [`prompts/auditor-narrative.md`](prompts/auditor-narrative.md), [`../tools/draft_narrative.py`](../tools/draft_narrative.py) |
| Control-gap analysis | A draft comparison of a control's evidence against its assessment objectives | The validated gap decision, recorded by merge | [`prompts/control-gap-analysis.md`](prompts/control-gap-analysis.md) |
| Crosswalk suggestion | Candidate framework references when a framework comes into scope | The human-verified references in the crosswalk | [`prompts/crosswalk-suggestion.md`](prompts/crosswalk-suggestion.md) |
| Stakeholder report | A draft report rendered from computed control statuses | The published report, after approval | [`../.github/workflows/stakeholder-report-generator.yml`](../.github/workflows/stakeholder-report-generator.yml) |

The prompt templates are committed, so the instruction the model receives is
itself reviewable and version-controlled, not hidden in a script.

## Where AI is forbidden

- **Authoring evidence.** Evidence is computed from a system of record. The
  drafting tool refuses to run on a record that is not `ai_generated: false`, and
  the evidence validator fails the build on any record marked `ai_generated:
  true`. A model never supplies a count, a date, or an outcome that an auditor
  samples.
- **Approving its own draft.** A draft is a proposal. The human gate is the pull
  request, and a model does not merge.
- **Deciding a policy outcome of record.** Policy-as-code under
  [`../policy/`](../policy/) computes allow or deny from the input. A model may
  draft the remediation narrative for a denial; it does not decide the denial.

## How AI drafting wires into the workflow

The drafting step sits inside the operating model the rest of the program already
uses, which is the drift-opens-an-Issue, fix-by-pull-request loop:

```
computed evidence (ai_generated: false)
    |
    v
AI drafts the narrative / gap analysis / crosswalk           <- ai/ and tools/draft_narrative.py
    |
    v
a pull request opens with the draft                          <- the human gate
    |
    +-- a named function reviews the draft against the record
    |     every claim must trace to a computed value; an unbacked claim is removed
    v
the merge publishes the narrative and is the authorization   <- git history is the audit trail
```

The same gate governs the auditor narrative, the stakeholder report, and any
remediation a policy denial triggers. AI makes the drafting fast. The human
decision, and the computed evidence behind it, are what make it a record.

## Run the AI step now

No key and no network are needed for the demonstration path:

```bash
# Render the filled prompt and a stub draft for a control, from its computed
# evidence record. The tool refuses any record not marked ai_generated: false.
python3 tools/draft_narrative.py --control CHG-02 --dry-run
```

For a live draft, set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`, default
`gpt-4o-mini`) and drop `--dry-run`. The live path sends the same committed
prompt to the model and returns a draft that still has to pass the human gate.
