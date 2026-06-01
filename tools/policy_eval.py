#!/usr/bin/env python3
"""Policy evaluator: run the policy-as-code in policy/ against an input.

Rego under policy/ is the canonical, machine-enforceable form. This evaluator
runs that policy two ways so the policy executes in any environment:

  - If `opa` is on PATH, it shells out to `opa eval` so the Rego itself is the
    engine. The Rego is then the single source of truth.
  - If `opa` is not installed, it evaluates a Python port of the same rules so
    the policy still runs and the tests still gate. The port is kept in lockstep
    with the Rego, rule for rule.

Both paths return the same shape: {"allow": bool, "deny": [reasons]}.

Run a single input:

    python3 tools/policy_eval.py --policy agent_access \
        --input policy/fixtures/agent_access/deny_standing_entitlement.json

Add --explain to print the deny reasons. Exit code is 0 for an allow and 1 for
a deny, so the evaluator is usable directly as a gate in a shell pipeline.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_DIR = REPO_ROOT / "policy"

# Maps a policy name to its Rego file and the package document to query.
POLICIES = {
    "agent_access": {
        "rego": POLICY_DIR / "agent_access.rego",
        "query": "data.compliance.agent_access",
        "control": "AAT-01, PRI-03.13",
    },
    "change_control": {
        "rego": POLICY_DIR / "change_control.rego",
        "query": "data.compliance.change_control",
        "control": "CHG-02",
    },
    "access_review": {
        "rego": POLICY_DIR / "access_review.rego",
        "query": "data.compliance.access_review",
        "control": "IAC-17",
    },
}


def opa_available() -> bool:
    return shutil.which("opa") is not None


def evaluate_with_opa(policy: str, document: dict) -> dict:
    spec = POLICIES[policy]
    proc = subprocess.run(
        [
            "opa",
            "eval",
            "--format",
            "json",
            "--data",
            str(spec["rego"]),
            "--stdin-input",
            spec["query"],
        ],
        input=json.dumps(document),
        capture_output=True,
        text=True,
        check=True,
    )
    parsed = json.loads(proc.stdout)
    value = parsed["result"][0]["expressions"][0]["value"]
    return {
        "allow": bool(value.get("allow", False)),
        "deny": sorted(value.get("deny", []) or []),
    }


# --------------------------------------------------------------------------
# Python port of the Rego rules. Kept rule-for-rule with the policy/*.rego
# files so a host without OPA still runs the same policy.
# --------------------------------------------------------------------------

TTL_CEILING = 300
HIGH_IMPACT_ACTIONS = {"location_disclosure", "action_on_minor_account", "irreversible_write"}
SENSITIVE_CLASSES = {"precise-location", "minor-data"}


def _eval_agent_access(i: dict) -> list[str]:
    deny: list[str] = []
    is_sensitive = i.get("data_class") in SENSITIVE_CLASSES
    touches_minor = i.get("data_class") == "minor-data" or i.get("subject_is_minor") is True
    ttl = i.get("token_ttl_seconds")
    positive_ttl = isinstance(ttl, (int, float)) and not isinstance(ttl, bool) and ttl > 0

    if is_sensitive and i.get("standing_access") is True:
        deny.append(
            "standing entitlement to {} is not permitted; access must be brokered per request".format(
                i.get("data_class")
            )
        )
    if is_sensitive and not positive_ttl:
        deny.append("sensitive read has no positive purpose-token TTL; grants must be time-boxed")
    if is_sensitive and isinstance(ttl, (int, float)) and not isinstance(ttl, bool) and ttl > TTL_CEILING:
        deny.append("token TTL {}s exceeds the {}s ceiling".format(ttl, TTL_CEILING))
    if is_sensitive and not (isinstance(i.get("purpose"), str) and i.get("purpose") != ""):
        deny.append("no declared purpose; access to sensitive data must be purpose-bound")
    if touches_minor and i.get("consent_state") != "active":
        deny.append(
            "consent is {}; processing or disclosure of a minor's data is denied without active "
            "verifiable parental consent".format(i.get("consent_state", "absent"))
        )
    if i.get("action") in HIGH_IMPACT_ACTIONS and i.get("human_gate") != "satisfied":
        deny.append(
            "{} requires a recorded human gate; gate state is {}".format(
                i.get("action"), i.get("human_gate", "missing")
            )
        )
    return deny


def _eval_change_control(i: dict) -> list[str]:
    deny: list[str] = []
    is_protected = i.get("protected") is True
    is_emergency = i.get("emergency") is True
    independent_reviewers = [r for r in i.get("reviewers", []) or [] if r != i.get("author")]
    has_ticket = isinstance(i.get("linked_ticket"), str) and i.get("linked_ticket") != ""
    has_review = isinstance(i.get("after_the_fact_review"), str) and i.get("after_the_fact_review") != ""

    if is_protected and i.get("direct_push") is True:
        deny.append(
            "direct push to a protected branch is blocked; change must arrive by reviewed pull request"
        )
    if is_protected and not has_ticket:
        deny.append("no linked work item; each production change links to a tracked ticket")
    if is_protected and not is_emergency and len(independent_reviewers) < 1:
        deny.append("no independent approving review; the approver must not be the author")
    if is_protected and not is_emergency and i.get("checks_passed") is not True:
        deny.append("required status checks did not pass; failing checks block the merge")
    if is_protected and is_emergency and not has_review:
        deny.append(
            "emergency change without a documented after-the-fact review within the reconciliation window"
        )
    return deny


def _eval_access_review(i: dict) -> list[str]:
    deny: list[str] = []
    coverage_gap = i.get("accounts_in_scope", 0) - i.get("accounts_reviewed", 0)
    if coverage_gap > 0:
        deny.append("{} in-scope accounts were not reviewed within the cadence".format(coverage_gap))
    if i.get("accounts_overdue", 0) > 0:
        deny.append("{} accounts are past the recertification cadence".format(i.get("accounts_overdue")))
    uncovered_orphans = i.get("orphaned_accounts", 0) - i.get("orphaned_with_exception", 0)
    if uncovered_orphans > 0:
        deny.append("{} orphaned accounts without a documented exception".format(uncovered_orphans))
    svc_gap = i.get("service_accounts_in_scope", 0) - i.get("service_accounts_reviewed", 0)
    if svc_gap > 0:
        deny.append("{} service accounts were not reviewed to the same bar as human accounts".format(svc_gap))
    if i.get("leaver_deprovision_breaches", 0) > 0:
        deny.append("{} leaver deprovisioning SLA breaches".format(i.get("leaver_deprovision_breaches")))
    if i.get("sod_conflicts_open", 0) > 0:
        deny.append("{} unresolved segregation-of-duties conflicts".format(i.get("sod_conflicts_open")))
    return deny


_PYTHON_RULES = {
    "agent_access": _eval_agent_access,
    "change_control": _eval_change_control,
    "access_review": _eval_access_review,
}


def evaluate_with_python(policy: str, document: dict) -> dict:
    deny = _PYTHON_RULES[policy](document)
    return {"allow": len(deny) == 0, "deny": sorted(deny)}


def evaluate(policy: str, document: dict, engine: str = "auto") -> dict:
    """Evaluate a policy against an input document.

    engine: "auto" uses OPA when present, otherwise the Python port. "opa" or
    "python" force a specific engine.
    """
    if policy not in POLICIES:
        raise ValueError("unknown policy: {}".format(policy))
    if engine == "opa" or (engine == "auto" and opa_available()):
        return evaluate_with_opa(policy, document)
    return evaluate_with_python(policy, document)


def engine_in_use(engine: str = "auto") -> str:
    if engine == "opa" or (engine == "auto" and opa_available()):
        return "opa"
    return "python"


def _load_input(path: Path) -> dict:
    with path.open() as handle:
        doc = json.load(handle)
    # A fixture may wrap the policy input under "input" alongside an "expect"
    # block; accept either the wrapped or the bare form.
    if isinstance(doc, dict) and "input" in doc:
        return doc["input"]
    return doc


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a policy against an input document.")
    parser.add_argument("--policy", required=True, choices=sorted(POLICIES))
    parser.add_argument("--input", required=True, help="path to a JSON input or fixture")
    parser.add_argument("--engine", default="auto", choices=["auto", "opa", "python"])
    parser.add_argument("--explain", action="store_true", help="print deny reasons")
    args = parser.parse_args(argv)

    document = _load_input(Path(args.input))
    result = evaluate(args.policy, document, engine=args.engine)
    used = engine_in_use(args.engine)

    verdict = "ALLOW" if result["allow"] else "DENY"
    print("policy: {} ({})".format(args.policy, POLICIES[args.policy]["control"]))
    print("engine: {}".format(used))
    print("decision: {}".format(verdict))
    if args.explain or not result["allow"]:
        if result["deny"]:
            print("reasons:")
            for reason in result["deny"]:
                print("  - {}".format(reason))
    return 0 if result["allow"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
