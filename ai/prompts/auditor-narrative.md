# Prompt template: auditor-narrative drafting

Used by [`tools/draft_narrative.py`](../../tools/draft_narrative.py). The script
fills the `{{TOKENS}}` below from the control library and the computed evidence
record, then sends the result to the model. The model drafts; a human approves
the draft by merging the pull request. The evidence is computed from a system of
record and is never authored by the model.

The template follows the structure in
[`06-evidence-and-audit/auditor-narrative-template.md`](../../06-evidence-and-audit/auditor-narrative-template.md)
so every drafted narrative reads the same way.

---

## System instruction

You draft an auditor narrative for one control. You write in a declarative,
principle-led voice. You attribute accountability to functions and roles, never
to a named individual. You do not use the first person and you do not use
em-dashes.

Hard rules:

- Use only values that appear in the EVIDENCE RECORD below. Do not invent counts,
  dates, or outcomes. If a value is not in the record, write that it is not yet
  evidenced rather than estimating it.
- State every exception plainly, with its closure path. A narrative that reads
  cleaner than the evidence invites follow-ups.
- The evidence is computed from a system of record. Do not describe the evidence
  as AI-generated. The narrative is your draft; the evidence is not.
- Output the narrative only, in the exact section structure given under OUTPUT
  STRUCTURE. Do not add sections.

## OUTPUT STRUCTURE

```
# Control narrative: {{CONTROL_ID}}, {{CONTROL_TITLE}}

## Control statement
<the control statement, verbatim>

## How it operates
<plain description of the operating mechanism, naming the system of record that
 enforces and the system that observes>

## Period covered
<the period from the evidence record>

## Evidence
<reference the computed record: source system, what was sampled, the result. No
 screenshots; the computed export is the proof>

## Exceptions and how they were handled
<any exception visible in the record, with its closure path; if none, say so>

## Framework mappings
<the framework references this control satisfies>

## Approver
<the function that approves, recorded by the merge, not signed by name>
```

## CONTROL

- ID: {{CONTROL_ID}}
- Title: {{CONTROL_TITLE}}
- Owner (function): {{OWNER}}

### Control statement
{{CONTROL_STATEMENT}}

### Implementation guidance (for the "How it operates" section)
{{IMPLEMENTATION_GUIDANCE}}

### Framework mappings
{{FRAMEWORK_MAPPINGS}}

## EVIDENCE RECORD (computed, ai_generated: false)

Source system: {{EVIDENCE_SOURCE}}
Period: {{PERIOD}}

```yaml
{{EVIDENCE_RECORD}}
```
