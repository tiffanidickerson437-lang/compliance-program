# policy/ : policy-as-code

Machine-enforceable policy that encodes control rules as code, so a control is
checked by an engine rather than asserted in prose. The policies tie directly to
the control library: the thresholds here (the token TTL ceiling, the human-gate
action set, the consent rule, the independent-review rule, the recertification
sign-off bar) are the same parameters defined in
[`02-controls/control-library.yaml`](../02-controls/control-library.yaml).

## What is here

| Policy | Control | Rule in one line |
|--------|---------|------------------|
| [`agent_access.rego`](agent_access.rego) | AAT-01, PRI-03.13 | Deny standing entitlement to sensitive data; require a purpose-bound, time-boxed grant within the TTL ceiling, active verifiable parental consent for a minor's data, and a recorded human gate for high-impact actions. |
| [`change_control.rego`](change_control.rego) | CHG-02 | Require a linked work item, an approver independent of the author, and passing checks on a protected branch; block direct pushes; allow an emergency change only with a documented after-the-fact review. |
| [`access_review.rego`](access_review.rego) | IAC-17 | Block recertification sign-off while any account is unreviewed or overdue, an orphan lacks an exception, a service account is unreviewed, a leaver SLA is breached, or a segregation-of-duties conflict is open. |

Each policy has a self-contained Rego test (`*_test.rego`) and a set of input
fixtures under [`fixtures/`](fixtures/) carrying both an input and its expected
decision (allow and deny cases).

## How it runs (two engines, one source of truth)

Rego is the canonical, machine-enforceable form. The policy executes in any
environment through one evaluator:

- When `opa` is on PATH, [`tools/policy_eval.py`](../tools/policy_eval.py) shells
  out to `opa eval`, so the Rego itself is the engine and is the single source of
  truth.
- When `opa` is not installed, the evaluator runs a Python port of the same
  rules, kept in lockstep with the Rego rule for rule, so the policy still runs
  and the tests still gate.

Both engines return the same shape, `{allow, deny[]}`, and the test suite has
been confirmed to agree across both.

## Run it

```bash
# Native Rego tests (requires opa). Fixtures are JSON inputs for the Python
# harness, not Rego data, so they are ignored here.
opa test policy/ --ignore '*.json' -v

# The gate. Runs every fixture through the evaluator and fails on any mismatch.
# Works with or without opa installed.
python3 policy/policy_test.py

# Evaluate a single input. Exit code is 0 for allow, 1 for deny.
python3 tools/policy_eval.py --policy agent_access \
    --input policy/fixtures/agent_access/deny_standing_entitlement.json
```

## The operating model

A policy denial is not a dead end. It is the input to the human gate: a denied
change opens a tracked Issue, a named function reviews, and the fix lands by pull
request. AI may draft the remediation narrative; the policy decision and the
evidence behind it are computed, never AI-authored. The merge is the
authorization, and Git history is the audit trail.
