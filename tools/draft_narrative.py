#!/usr/bin/env python3
"""Draft an auditor narrative for a control from its computed evidence record.

This is the visible AI-usage step. It takes a control and a computed evidence
record, fills the committed prompt template in ai/prompts/auditor-narrative.md,
and asks a model to draft the auditor narrative. The boundary is enforced in
code:

  - The evidence is computed from a system of record. This script refuses to run
    if the evidence record is not marked ai_generated: false, because AI never
    authors evidence.
  - The model drafts the narrative only. The draft is not a record until a human
    approves it by merging a pull request. The merge is the authorization.

Run it now, with no network and no key, to see the filled prompt and a stub
draft:

    python3 tools/draft_narrative.py --control CHG-02 --dry-run

Use a real evidence export instead of the illustrative example in the library:

    python3 tools/draft_narrative.py --control AAT-01 --evidence record.yaml --dry-run

For a live draft, set OPENAI_API_KEY (and optionally OPENAI_MODEL, default
gpt-4o-mini) and drop --dry-run. The live path posts the same filled prompt to
the model and prints the returned draft. The draft still has to pass the human
gate before it becomes a record.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required. Install it with: pip install pyyaml\n")
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTROL_LIBRARY = REPO_ROOT / "02-controls" / "control-library.yaml"
PROMPT_TEMPLATE = REPO_ROOT / "ai" / "prompts" / "auditor-narrative.md"

ENVELOPE_FIELDS = {"control", "period", "source", "ai_generated"}

# Field names that, when present and nonzero, signal an exception to surface in
# the narrative. Keeping this explicit avoids inventing exceptions the record
# does not contain.
EXCEPTION_FIELDS = {
    "exceptions_without_review": "production changes merged outside the reviewed path",
    "third_party_disclosures_without_consent": "disclosures of a child's data without active consent",
    "overdue_reassessment": "third-party reassessments past cadence",
    "orphaned": "orphaned accounts",
    "integrity_checks_failed": "log-store integrity check failures",
}


def load_control(control_id: str) -> dict:
    with CONTROL_LIBRARY.open() as handle:
        library = yaml.safe_load(handle)
    for control in library.get("controls", []):
        if control.get("id") == control_id:
            return control
    raise SystemExit("control not found in control-library.yaml: {}".format(control_id))


def load_evidence(control: dict, evidence_path: str | None) -> dict:
    if evidence_path:
        path = Path(evidence_path)
        with path.open() as handle:
            if path.suffix in (".json",):
                record = json.load(handle)
            else:
                record = yaml.safe_load(handle)
        # Accept either a bare record or a wrapper holding it.
        if isinstance(record, dict) and "example" in record and "ai_generated" not in record:
            record = record["example"]
        return record
    # Fall back to the illustrative computed record carried in the library.
    record = control.get("example_evidence")
    if not record:
        raise SystemExit(
            "no evidence record. Pass --evidence <file> with a computed record."
        )
    return record


def assert_computed_evidence(record: dict, control_id: str) -> None:
    """Enforce the boundary: evidence is computed, never AI-authored."""
    if record.get("ai_generated") is not False:
        raise SystemExit(
            "refusing to draft from evidence with ai_generated={!r} for {}. "
            "Evidence must be computed from a system of record (ai_generated: false); "
            "AI drafts the narrative, never the evidence.".format(
                record.get("ai_generated"), control_id
            )
        )


def framework_mappings_text(control: dict) -> str:
    lines = []
    for mapping in control.get("framework_mappings", []) or []:
        refs = ", ".join(mapping.get("references", []) or [])
        basis = " (framework-mapped, home lab, never audited)" if mapping.get("basis") else ""
        lines.append("- {}: {}{}".format(mapping.get("framework", "?"), refs, basis))
    return "\n".join(lines) if lines else "- none recorded"


def fill_prompt(control: dict, record: dict) -> str:
    template = PROMPT_TEMPLATE.read_text()
    guidance = " ".join((control.get("implementation_guidance") or "").split())
    record_yaml = yaml.safe_dump(record, sort_keys=False).strip()
    tokens = {
        "{{CONTROL_ID}}": control.get("id", "?"),
        "{{CONTROL_TITLE}}": control.get("title", ""),
        "{{OWNER}}": str(control.get("owner", "")),
        "{{CONTROL_STATEMENT}}": " ".join((control.get("statement") or "").split()),
        "{{IMPLEMENTATION_GUIDANCE}}": guidance,
        "{{FRAMEWORK_MAPPINGS}}": framework_mappings_text(control),
        "{{EVIDENCE_SOURCE}}": str(record.get("source", "system of record")),
        "{{PERIOD}}": str(record.get("period", "the reporting period")),
        "{{EVIDENCE_RECORD}}": record_yaml,
    }
    filled = template
    for token, value in tokens.items():
        filled = filled.replace(token, value)
    return filled


def first_sentence(text: str) -> str:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return ""
    end = cleaned.find(". ")
    return cleaned[: end + 1] if end != -1 else cleaned


def evidence_summary(record: dict) -> str:
    body = {k: v for k, v in record.items() if k not in ENVELOPE_FIELDS}
    parts = ["{}: {}".format(k, v) for k, v in body.items()]
    return "; ".join(parts) if parts else "no body fields in the record"


def exceptions_summary(record: dict) -> str:
    found = []
    for field, label in EXCEPTION_FIELDS.items():
        value = record.get(field)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and value > 0:
            found.append("{} ({}: {})".format(label, field, value))
    if found:
        return (
            "The record surfaces: "
            + "; ".join(found)
            + ". Each is recorded as an exception with a closure path and is stated here "
            "rather than hidden."
        )
    return (
        "No exception is visible in this record for the period. Any exception would be "
        "stated plainly with its closure path."
    )


def stub_draft(control: dict, record: dict) -> str:
    """A deterministic draft assembled without a model, for the dry run.

    It uses only values present in the record, so it demonstrates the shape a
    live model is asked to produce while inventing nothing.
    """
    lines = []
    lines.append("# Control narrative: {}, {}".format(control.get("id"), control.get("title")))
    lines.append("")
    lines.append("> AI draft, pending human approval. Published only when a human reviews and")
    lines.append("> merges the pull request. The evidence below is computed (ai_generated: false);")
    lines.append("> this narrative is the draft, not the evidence.")
    lines.append("")
    lines.append("## Control statement")
    lines.append(" ".join((control.get("statement") or "").split()))
    lines.append("")
    lines.append("## How it operates")
    lines.append(first_sentence(control.get("implementation_guidance", "")))
    lines.append("")
    lines.append("## Period covered")
    lines.append(str(record.get("period", "the reporting period")))
    lines.append("")
    lines.append("## Evidence")
    lines.append(
        "Source: {}. For {}, the computed record reports: {}. The computed export is the "
        "proof; no screenshots.".format(
            record.get("source", "system of record"),
            record.get("period", "the period"),
            evidence_summary(record),
        )
    )
    lines.append("")
    lines.append("## Exceptions and how they were handled")
    lines.append(exceptions_summary(record))
    lines.append("")
    lines.append("## Framework mappings")
    lines.append(framework_mappings_text(control).replace("- ", "").replace("\n", "; "))
    lines.append("")
    lines.append("## Approver")
    lines.append(
        "Approved by {} via merged pull request; the merge is the authorization.".format(
            control.get("owner", "the owning function")
        )
    )
    return "\n".join(lines)


def call_model(filled_prompt: str) -> str:
    """Live path: post the filled prompt to the model and return the draft."""
    import urllib.request

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "OPENAI_API_KEY is not set. Set it for a live draft, or pass --dry-run "
            "to render the filled prompt and a stub draft with no network."
        )
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You draft auditor narratives from computed evidence. You never invent "
                    "values and you never author evidence."
                ),
            },
            {"role": "user", "content": filled_prompt},
        ],
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer {}".format(api_key),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control", required=True, help="control ID, for example CHG-02")
    parser.add_argument("--evidence", help="path to a computed evidence record (yaml or json)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="render the filled prompt and a stub draft with no network or key",
    )
    args = parser.parse_args(argv)

    control = load_control(args.control)
    record = load_evidence(control, args.evidence)
    assert_computed_evidence(record, args.control)
    filled = fill_prompt(control, record)

    if args.dry_run:
        print("=" * 78)
        print("DRY RUN. No model call. Evidence is computed (ai_generated: false).")
        print("=" * 78)
        print("")
        print("----- FILLED PROMPT (sent to the model in a live run) -----")
        print("")
        print(filled)
        print("")
        print("----- STUB DRAFT (assembled locally, no model) -----")
        print("")
        print(stub_draft(control, record))
        print("")
        print("----- NEXT STEP -----")
        print(
            "A live run sends the filled prompt to the model and opens a pull request with "
            "the draft. A human reviews the draft against the computed record and merges. "
            "The merge is the authorization."
        )
        return 0

    draft = call_model(filled)
    print("# AI-drafted narrative for {} (pending human approval)".format(args.control))
    print("")
    print(draft)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
