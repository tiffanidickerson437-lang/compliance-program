#!/usr/bin/env python3
"""Unit B done-condition test: OSCAL SSP layer + SCF 2026.1 Living Control Set.

Plain python3, no pytest. Asserts the three legs of the done-condition:

  1. tools/scaffold.py renders generated/ from config.example.yaml.
  2. Catalog + Profiles + SSP all pass OSCAL validation (tools/validate_oscal.py).
  3. A repo-wide grep finds zero remaining references to owned-controls.yaml
     (excluding .git and this test file).

Run:  python3 tests/test_unit_b.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THIS_FILE = Path(__file__).resolve()

FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print("{} {}".format("PASS" if ok else "FAIL", label))
    if detail:
        for line in detail.rstrip().splitlines():
            print("     | " + line)
    if not ok:
        FAILURES.append(label)


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=REPO, capture_output=True, text=True, timeout=600
    )


def test_scaffold_renders() -> None:
    proc = run([sys.executable, "tools/scaffold.py", "config.example.yaml"])
    check(
        "scaffold: tools/scaffold.py config.example.yaml exits 0",
        proc.returncode == 0,
        (proc.stdout + proc.stderr)[-2000:] if proc.returncode != 0 else "",
    )
    for rel in ("generated/in-scope-controls.yaml", "generated/profile-selection.yaml"):
        check("scaffold: {} rendered".format(rel), (REPO / rel).is_file())


def test_oscal_validation() -> None:
    validator = REPO / "tools" / "validate_oscal.py"
    check("validator: tools/validate_oscal.py exists", validator.is_file())
    if not validator.is_file():
        return
    proc = run([sys.executable, "tools/validate_oscal.py"])
    tail = (proc.stdout + proc.stderr)[-4000:]
    check(
        "validator: Catalog + Profiles + SSP pass OSCAL validation (exit 0)",
        proc.returncode == 0,
        tail,
    )
    check("ssp: generated/ssp.oscal.json exists", (REPO / "generated" / "ssp.oscal.json").is_file())


def test_no_owned_controls_references() -> None:
    needle = "owned-controls"
    hits: list[str] = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            path = Path(root) / name
            if path == THIS_FILE:
                continue
            try:
                text = path.read_text(errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if needle in line:
                    hits.append("{}:{}: {}".format(path.relative_to(REPO), lineno, line.strip()[:120]))
    check(
        "grep: zero repo-wide references to owned-controls.yaml/.oscal.json (excluding .git and this test)",
        not hits,
        "\n".join(hits[:40]),
    )
    for legacy in ("02-controls/owned-controls.yaml", "02-controls/owned-controls.oscal.json"):
        check("deleted: {} no longer present".format(legacy), not (REPO / legacy).exists())


def main() -> int:
    test_scaffold_renders()
    test_oscal_validation()
    test_no_owned_controls_references()
    print()
    if FAILURES:
        print("RESULT: FAIL ({} failing check(s))".format(len(FAILURES)))
        return 1
    print("RESULT: PASS (scaffold renders; catalog, profiles, and SSP validate; zero owned-controls references)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
