#!/usr/bin/env python3
"""Control health check: compute drift and render the Issue it would open.

This is the runnable local form of the control drift monitor. A real run reads
each control's named system of record through the MCP evidence gateways
declared in the repo-root .mcp.json (see tools/mcp_gateways.py and ci_mapping
in the control library) and computes whether the control drifted. When no
gateway credentials are configured -- the shipped state -- the check falls back
to a drift-signals fixture holding the computed result, enriches each entry
with the owning function and framework impact from the control library, and
renders the GitHub Issue that the daily Action opens.

The Issue is the evidence of due diligence: it is timestamped and retained, it
names the owner and the framework impact, and it is the start of the
fix-by-pull-request loop. AI may draft the remediation narrative; a human
approves it by merging; the merge flips the control status.

Run:

    # Uses the committed sample signals so the path is demonstrable now.
    python3 tools/check_control_health.py

    # Try the MCP gateways first, fall back to the fixture (default mode).
    python3 tools/check_control_health.py --source auto

    # Gateways only (exit non-zero if none are configured) / fixture only.
    python3 tools/check_control_health.py --source gateway
    python3 tools/check_control_health.py --source fixture

    # Point at a real computed signals file.
    python3 tools/check_control_health.py --signals path/to/drift-signals.yaml

    # Exit non-zero when any control is drifting (for use as a gate).
    python3 tools/check_control_health.py --fail-on-drift

    # Write pipe-delimited drift rows for the Action's Issue-opening step.
    python3 tools/check_control_health.py --emit-rows drift-rows.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required. Install it with: pip install pyyaml\n")
    raise SystemExit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcp_gateways  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTROL_LIBRARY = REPO_ROOT / "02-controls" / "control-library.yaml"
DEFAULT_SIGNALS = REPO_ROOT / "06-evidence-and-audit" / "drift-signals.example.yaml"

# Every drift Issue title carries this prefix so the AEHR loop (Automated
# Evidence, Human Review) is queryable: gh issue list --search "[drift]".
ISSUE_TITLE_PREFIX = "[drift]"


def load_controls() -> dict:
    with CONTROL_LIBRARY.open() as handle:
        library = yaml.safe_load(handle)
    return {c["id"]: c for c in library.get("controls", [])}


def framework_impact_from_library(control: dict) -> str:
    refs = []
    for mapping in control.get("framework_mappings", []) or []:
        refs.append(mapping.get("framework", "?"))
    return ", ".join(refs) if refs else "see framework-crosswalk.yaml"


def render_issue(entry: dict, control: dict) -> str:
    cid = entry.get("control", "UNKNOWN")
    drift_type = entry.get("drift_type", "unspecified")
    owner = str(control.get("owner", "unassigned"))
    framework_impact = entry.get("framework_impact") or framework_impact_from_library(control)
    evidence_needed = entry.get("evidence_needed", "computed record from the system of record")
    detail = entry.get("detail")

    lines = []
    lines.append("Title: {} Control drift: {} ({})".format(
        ISSUE_TITLE_PREFIX, cid, drift_type))
    lines.append("Labels: evidence, control-drift")
    lines.append("")
    lines.append("## Control drift detected")
    lines.append("")
    lines.append("- Control: {}".format(cid))
    lines.append("- Drift type: {}".format(drift_type))
    lines.append("- Owner (function): {}".format(owner))
    lines.append("- Framework impact: {}".format(framework_impact))
    lines.append("- Evidence needed to close: {}".format(evidence_needed))
    if detail:
        lines.append("- Detail: {}".format(detail))
    lines.append("")
    lines.append("### Why this Issue exists")
    lines.append(
        "This Issue is the evidence of due diligence. It is timestamped and retained. "
        "AI drafts the remediation narrative; a human reviews it; remediation lands by "
        "pull request. The merge is the authorization and flips the control status. Git "
        "history is the audit trail."
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--signals",
        default=str(DEFAULT_SIGNALS),
        help="path to a drift-signals file (default: the committed example)",
    )
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="exit non-zero when any control is drifting",
    )
    parser.add_argument(
        "--source",
        choices=["auto", "gateway", "fixture"],
        default="auto",
        help="where drift signals come from: MCP gateways with fixture "
             "fallback (auto, default), gateways only, or fixture only",
    )
    parser.add_argument(
        "--emit-rows",
        metavar="PATH",
        help="also write pipe-delimited drift rows to PATH "
             "(control|drift_type|owner|framework_impact|evidence_needed) "
             "for the Action's Issue-opening step",
    )
    args = parser.parse_args(argv)

    controls = load_controls()
    signals_path = Path(args.signals)

    drifting = []
    signal_origin = None

    if args.source in ("auto", "gateway"):
        drifting, notes = mcp_gateways.fetch_drift_signals()
        for note in notes:
            print(note)
        if drifting:
            signal_origin = "MCP gateways (.mcp.json)"
        elif args.source == "gateway":
            print("No MCP gateway is configured (no OBO OAuth token in the "
                  "environment) and --source gateway forbids the fixture.")
            return 2
        else:
            print("No gateway returned signals; falling back to the "
                  "drift-signals fixture (the supported degraded mode).")

    if signal_origin is None:
        if not signals_path.exists():
            if args.emit_rows:
                Path(args.emit_rows).write_text("")
            print("No drift-signals fixture at {}.".format(signals_path))
            print("All checked controls are healthy. No Issue would open.")
            return 0
        with signals_path.open() as handle:
            signals = yaml.safe_load(handle) or {}
        drifting = signals.get("drifting", []) or []
        signal_origin = "fixture fallback: {}".format(signals_path)

    print("Control health check")
    print("Signals: {}".format(signal_origin))
    print("Controls checked against the library: {}".format(len(controls)))
    print("=" * 72)

    if args.emit_rows:
        rows = []
        for entry in drifting:
            cid = entry.get("control") or "UNKNOWN"
            control = controls.get(cid, {})
            rows.append("|".join([
                cid,
                entry.get("drift_type", "unspecified"),
                str(control.get("owner", "unassigned")),
                entry.get("framework_impact")
                or framework_impact_from_library(control),
                entry.get("evidence_needed",
                          "computed record from the system of record"),
            ]))
        # Trailing newline matters: the Action reads this with `while read`,
        # which drops a final line that lacks one.
        Path(args.emit_rows).write_text("\n".join(rows) + "\n" if rows else "")
        print("Drift rows written to {} ({} row(s)).".format(
            args.emit_rows, len(rows)))

    if not drifting:
        print("All checked controls are healthy. No Issue would open.")
        return 0

    for entry in drifting:
        cid = entry.get("control")
        control = controls.get(cid, {})
        if not control:
            print("WARNING: drift references unknown control {}".format(cid))
        print("")
        print("----- GitHub Issue the daily Action would open -----")
        print(render_issue(entry, control))
        print("")

    print("=" * 72)
    print("{} control(s) drifting. Each opens an Issue that starts the".format(len(drifting)))
    print("fix-by-pull-request loop. Locally this renders the Issue; the Action opens it.")

    if args.fail_on_drift:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
