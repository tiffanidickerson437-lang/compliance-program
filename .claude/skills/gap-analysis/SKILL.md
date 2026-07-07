---
name: gap-analysis
description: Compute the control-coverage delta against a target framework from the live mapping and scaffold data, then draft a gap analysis for a human GRC owner to validate. Use when asked "what are we missing for <framework>", "coverage gap", or "gap analysis".
context: fork
agent: Explore
---

# Gap analysis (draft-only)

Draft a coverage gap analysis. The output is a proposal; a human GRC owner
decides what is a real gap and records the decision by pull request. Follow the
committed prompt template `ai/prompts/control-gap-analysis.md`: declarative
voice, no first person, no invented counts or dates, never assert a gap closed.

## Live coverage numbers (injected at invocation)

Controls in scope (from the scaffolded view):

!`grep -A1 "controls_in_scope_count" generated/in-scope-controls.yaml | head -2`

Owned controls in the library:

!`grep -c "^  - id:" 02-controls/control-library.yaml 2>/dev/null || grep -c "scf-id" 02-controls/control-library.oscal.json`

Draft STRM mappings pending human approval (per mappings/ file — requirements
mapped and candidate relationships proposed):

!`for f in mappings/*.yaml; do echo "$f: $(grep -c 'requirement:' "$f") requirements, $(grep -c 'relationship:' "$f") candidate relationships, status=$(grep -m1 'status:' "$f" | sed 's/.*status: *//')"; done`

Approved crosswalk (frameworks registered in the source of truth):

!`grep -A2 "^frameworks:" 02-controls/framework-crosswalk.yaml | head -3 && grep -c "profile: profiles/" 02-controls/framework-crosswalk.yaml`

## Method

1. Read `02-controls/framework-crosswalk.yaml` and the relevant OSCAL profile
   under `02-controls/profiles/` for the target framework.
2. Read any draft in `mappings/` for that framework; treat DRAFT entries as
   unapproved — they cover nothing until merged.
3. Compute the delta: target-framework requirements with no approved owned
   control mapping. Use only the STRM relationship types recorded in the
   files (equal-to, subset-of, superset-of, intersects-with, no-relationship);
   an `intersects-with` or `subset-of` mapping is partial coverage, not full.
4. For each uncovered or partially covered requirement, state: the requirement
   ID as written in the profile/mapping file, what exists today (file + line
   basis), and the single most useful next step.
5. Output a table (requirement, coverage status, basis, next step) plus a
   three-sentence summary. Mark the whole output DRAFT_PENDING_HUMAN_APPROVAL.

Do not modify any file. Do not invent requirement IDs or framework text — if a
requirement's text is not in the repo, cite only its ID and flag it for human
verification against the framework source.
