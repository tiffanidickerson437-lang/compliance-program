#!/usr/bin/env python3
"""Unit A test: FAIR Monte Carlo simulator done-condition.

Runs `python3 tools/fair_montecarlo.py` with NO arguments and asserts stdout
contains, for every risk in 01-risk-management/risk-register.yaml AND for the
portfolio: a loss-exceedance curve and p50/p90/p95 ALE percentiles. Also
asserts the generated report file is written and that no result is phrased as
an exact single figure without probability framing.

Plain python3 runnable — no pytest dependency.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "fair_montecarlo.py"
REGISTER = REPO_ROOT / "01-risk-management" / "risk-register.yaml"
REPORT = REPO_ROOT / "generated" / "fair-simulation-report.md"

FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"  PASS: {message}")
    else:
        print(f"  FAIL: {message}")
        FAILURES.append(message)


def risk_ids_from_register() -> list[str]:
    """Read risk ids straight from the register text (no PyYAML dependency)."""
    ids = re.findall(r"^\s*-\s*id:\s*(RISK-\d+)", REGISTER.read_text(), re.MULTILINE)
    return ids


def main() -> int:
    check(SCRIPT.exists(), f"{SCRIPT.relative_to(REPO_ROOT)} exists")
    if not SCRIPT.exists():
        report()
        return 1

    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=300,
    )
    out = proc.stdout
    check(proc.returncode == 0, f"script exits 0 (got {proc.returncode}); stderr: {proc.stderr[:500]!r}")

    risk_ids = risk_ids_from_register()
    check(len(risk_ids) >= 1, f"register yields at least one risk id (got {len(risk_ids)})")

    sections = risk_ids + ["PORTFOLIO"]
    for rid in sections:
        check(rid in out, f"stdout contains a section for {rid}")
        # Slice out this section of stdout to scope the assertions.
        start = out.find(rid)
        segment = out[start:] if start >= 0 else ""
        next_starts = [segment.find(other, len(rid)) for other in sections if other != rid]
        next_starts = [n for n in next_starts if n > 0]
        if next_starts:
            segment = segment[: min(next_starts)]
        check(
            "Loss-exceedance" in segment or "loss-exceedance" in segment.lower(),
            f"{rid} section includes a loss-exceedance curve",
        )
        for pct in ("p50", "p90", "p95"):
            check(
                re.search(pct + r"\b", segment) is not None,
                f"{rid} section includes ALE {pct}",
            )
        check(
            re.search(r"chance of\s*(losses\s*)?>=\s*\$", segment) is not None
            or re.search(r"P\(loss\s*>=", segment) is not None,
            f"{rid} loss-exceedance rows are phrased probabilistically (chance of >= $X)",
        )

    check(REPORT.exists(), f"report emitted at {REPORT.relative_to(REPO_ROOT)}")
    if REPORT.exists():
        report_text = REPORT.read_text()
        for rid in sections:
            check(rid in report_text, f"report contains section for {rid}")
        check("p95" in report_text, "report contains ALE percentiles")

    report()
    return 1 if FAILURES else 0


def report() -> None:
    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED")
    else:
        print("All checks passed")


if __name__ == "__main__":
    raise SystemExit(main())
