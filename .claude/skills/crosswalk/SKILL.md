---
name: crosswalk
description: Draft STRM (set-theory relationship mapping) entries from owned controls to an external framework's requirements. Use when asked to "map <framework>", "crosswalk", "draft STRM", or when a new framework comes into scope.
---

# Crosswalk drafting (STRM, draft-only)

Draft candidate mappings from owned controls to one external framework. Follow
the committed prompt template `ai/prompts/crosswalk-suggestion.md`. Adding a
framework is a mapping, never a new control; nothing is recorded until a human
validates each reference against the framework text and merges the change.

## Rules

- Source controls: `02-controls/control-library.yaml` only. Never invent a
  control ID; never restate a control's existing mappings from
  `02-controls/framework-crosswalk.yaml`.
- Never quote external framework requirement text from memory. Use the
  requirement ID plus a title only if it appears in a file in this repo or a
  source the human supplies; otherwise flag `title_unverified: true`.
- Each drafted entry MUST validate against the bundled schema
  `templates/strm-entry.schema.json` in this skill directory. Validate with:
  `python3 -c "import json,sys; ..."` or any JSON Schema validator before
  presenting the draft.
- Relationship type is one of exactly five STRM values: `equal-to`,
  `subset-of`, `superset-of`, `intersects-with`, `no-relationship`.
- Relationship strength is an integer 1-10. Ground it in the overlap between
  the control statement and the requirement; a strength you cannot ground is
  low, and low is flagged for human verification.
- Write drafts to `mappings/<framework>.draft.yaml` with
  `status: DRAFT_PENDING_HUMAN_APPROVAL` (same shape as
  `mappings/iso42001.draft.yaml`). Never write to
  `02-controls/framework-crosswalk.yaml` or `02-controls/profiles/` — those
  change only by human-approved PR.

## Output

One draft mapping file (or a patch to an existing draft) plus a short summary
table: control, requirement, relationship type, strength, one-line rationale.
