---
name: draft-narrative
description: Draft an auditor-facing control narrative from the OSCAL control definition and a computed evidence record. Human-triggered only; the draft is approved by merge.
disable-model-invocation: true
---

# Auditor narrative drafting (human-triggered, draft-only)

Draft one auditor narrative for one control. This skill never fires on its own:
a human invokes it, and a human approves the resulting draft by merging the
pull request. Follow the committed prompt template
`ai/prompts/auditor-narrative.md` and the structure in
`06-evidence-and-audit/auditor-narrative-template.md`; the deterministic path
is `tools/draft_narrative.py` — prefer running it when it covers the case.

## Inputs

- Control definition: the control's entry in
  `02-controls/control-library.oscal.json` (statement, guidance,
  assessment-objective, assessment-method parts; params; props). The bundled
  schema `templates/oscal-control.schema.json` describes the exact shape a
  control entry has and any drafted or edited control JSON must match.
- Evidence record: a computed record with `ai_generated: false`. If no record
  exists for the period, the narrative says the item is not yet evidenced. You
  never author, edit, or backfill an evidence record.

## Rules

- Quote the control statement verbatim from the library; do not paraphrase it
  in the "Control statement" section.
- Use only values present in the evidence record. No invented counts, dates,
  or outcomes.
- Declarative voice, no first person, no em-dashes, accountability to
  functions and roles, never named individuals.
- State every exception plainly with its closure path.
- The evidence is computed from a system of record; never describe it as
  AI-generated. The narrative is the draft; the evidence is not.
- Output lands as a Markdown draft in a PR. Nothing is a record until merged.
