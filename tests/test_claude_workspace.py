#!/usr/bin/env python3
"""Guardrail-hook tests for the .claude/ workspace.

Runs with plain python3 (no pytest). Pipes hook-protocol JSON into the two
PreToolUse guard hooks and asserts the block/allow exit codes:

  - guard_evidence.py exits 2 for a Write into an evidence path whose content
    claims ai_generated: true, and 0 for a non-evidence write.
  - guard_git.sh exits 2 for `git push origin main`, and 0 for an innocent
    command.
"""

import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(REPO, ".claude", "hooks")

FAILURES = []


def run_hook(argv, payload):
    proc = subprocess.run(
        argv,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    return proc


def check(name, argv, payload, want_exit):
    proc = run_hook(argv, payload)
    ok = proc.returncode == want_exit
    status = "PASS" if ok else "FAIL"
    print("{}: {} (exit {}, wanted {})".format(status, name, proc.returncode, want_exit))
    if proc.stderr.strip():
        print("       stderr: {}".format(proc.stderr.strip()))
    if not ok:
        FAILURES.append(name)


def main():
    guard_evidence = os.path.join(HOOKS, "guard_evidence.py")
    guard_git = os.path.join(HOOKS, "guard_git.sh")

    for path in (guard_evidence, guard_git):
        if not os.path.isfile(path):
            print("FAIL: hook missing: {}".format(path))
            FAILURES.append("missing " + path)
    if FAILURES:
        print("\n{} failure(s).".format(len(FAILURES)))
        return 1

    # 1. Evidence guard BLOCKS an AI-authored evidence write (exit 2).
    check(
        "guard_evidence blocks ai_generated:true under an evidence path",
        ["python3", guard_evidence],
        {
            "tool_name": "Write",
            "tool_input": {
                "file_path": "06-evidence-and-audit/evidence-records/CHG-02.evidence.yaml",
                "content": "control: CHG-02\nperiod: 2026-Q2\nsource: github\nai_generated: true\n",
            },
        },
        want_exit=2,
    )

    # 2. Evidence guard ALLOWS a non-evidence write (exit 0).
    check(
        "guard_evidence allows a non-evidence write",
        ["python3", guard_evidence],
        {
            "tool_name": "Write",
            "tool_input": {
                "file_path": "docs/notes.md",
                "content": "ai_generated: true appears here but this is not an evidence path\n",
            },
        },
        want_exit=0,
    )

    # 3. Git guard BLOCKS a direct push to main (exit 2).
    check(
        "guard_git blocks 'git push origin main'",
        ["bash", guard_git],
        {"cwd": REPO, "tool_input": {"command": "git push origin main"}},
        want_exit=2,
    )

    # 4. Git guard ALLOWS an innocent command (exit 0).
    check(
        "guard_git allows an innocent command",
        ["bash", guard_git],
        {"cwd": REPO, "tool_input": {"command": "git status"}},
        want_exit=0,
    )

    # 5. Git guard BLOCKS a force-push (exit 2).
    check(
        "guard_git blocks 'git push --force origin feature'",
        ["bash", guard_git],
        {"cwd": REPO, "tool_input": {"command": "git push --force origin feature"}},
        want_exit=2,
    )

    if FAILURES:
        print("\n{} failure(s).".format(len(FAILURES)))
        return 1
    print("\nAll guardrail hook tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
