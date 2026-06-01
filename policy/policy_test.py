#!/usr/bin/env python3
"""Fixture-driven policy tests. The gate for policy-as-code.

Runs every fixture under policy/fixtures/<policy>/*.json through the evaluator
and compares the decision to the expectation declared in the fixture. A fixture
carries both its input and its expected decision:

    {
      "expect": { "allow": false, "deny_contains": ["standing entitlement"] },
      "input": { ... }
    }

This harness runs with or without OPA installed, because tools/policy_eval.py
uses OPA when present and a Python port of the same rules otherwise. It exits
non-zero on any mismatch, so CI fails on a policy violation or a policy regression.

Run:

    python3 policy/policy_test.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import policy_eval  # noqa: E402  (path set above)

FIXTURE_DIR = REPO_ROOT / "policy" / "fixtures"


def run() -> int:
    engine = policy_eval.engine_in_use("auto")
    print("Policy tests (engine: {})".format(engine))
    print("=" * 72)

    fixtures = sorted(FIXTURE_DIR.glob("*/*.json"))
    if not fixtures:
        print("No fixtures found under policy/fixtures/. Nothing to test.")
        return 1

    failures: list[str] = []
    passed = 0

    for fixture_path in fixtures:
        policy_name = fixture_path.parent.name
        with fixture_path.open() as handle:
            fixture = json.load(handle)
        expect = fixture.get("expect", {})
        document = fixture.get("input", fixture)

        result = policy_eval.evaluate(policy_name, document, engine="auto")
        rel = fixture_path.relative_to(REPO_ROOT)

        problems: list[str] = []
        if "allow" in expect and result["allow"] != expect["allow"]:
            problems.append(
                "expected allow={}, got allow={}".format(expect["allow"], result["allow"])
            )
        for needle in expect.get("deny_contains", []) or []:
            if not any(needle in reason for reason in result["deny"]):
                problems.append("expected a deny reason containing {!r}".format(needle))

        verdict = "ALLOW" if result["allow"] else "DENY"
        if problems:
            failures.append(str(rel))
            print("  FAIL  [{}] {}".format(verdict, rel))
            for problem in problems:
                print("          {}".format(problem))
            for reason in result["deny"]:
                print("          deny: {}".format(reason))
        else:
            passed += 1
            print("  PASS  [{}] {}".format(verdict, rel))

    print("=" * 72)
    print("{} passed, {} failed, {} total".format(passed, len(failures), len(fixtures)))
    if failures:
        print("POLICY TESTS FAILED")
        return 1
    print("POLICY TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
