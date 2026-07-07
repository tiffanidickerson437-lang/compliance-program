#!/usr/bin/env python3
"""Unit D test: MCP evidence gateways (AEHR drift loop, fixture fallback).

Plain-python3 runnable, no pytest. Asserts:

1. DONE-CONDITION: the exact validation logic that
   .github/workflows/evidence-validator.yml runs rejects (non-zero exit) a
   crafted evidence record with ai_generated: true. The embedded validator
   script is extracted from the workflow itself, so this exercises the real
   validation step, not a copy.
2. A shareable .mcp.json exists at the repo root with one gateway per system
   of record (Jira / AWS / GitHub), on streamable HTTP transport (never
   stdio), configured behind env vars with no inline secrets, and without
   alwaysLoad: true on any toolset.
3. The gateway resolver rejects SSRF-prone endpoints (loopback, private
   ranges, cloud-metadata) and refuses non-HTTPS gateway URLs.
4. tools/check_control_health.py falls back to the drift-signals fixture when
   gateway credentials are absent (the pre-made no-live-creds decision), and
   renders drift Issue titles with the "[drift]" prefix.

Run:  python3 tests/test_mcp_evidence.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print("[{}] {}{}".format(status, name, (" -- " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)


def extract_validator_script() -> str:
    """Pull the embedded python validator out of evidence-validator.yml."""
    wf_path = REPO_ROOT / ".github" / "workflows" / "evidence-validator.yml"
    wf = yaml.safe_load(wf_path.read_text())
    steps = wf["jobs"]["validate"]["steps"]
    for step in steps:
        run = step.get("run", "")
        if "<<'PY'" in run and "ai_generated" in run:
            lines = run.splitlines()
            start = next(i for i, l in enumerate(lines) if "<<'PY'" in l) + 1
            end = next(i for i in range(len(lines) - 1, start, -1)
                       if lines[i].strip() == "PY")
            return "\n".join(lines[start:end])
    raise AssertionError("validator script not found in evidence-validator.yml")


def test_validator_rejects_ai_generated_true() -> str:
    script = extract_validator_script()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        records_dir = tmp_path / "06-evidence-and-audit" / "evidence-records"
        records_dir.mkdir(parents=True)
        # Crafted test record: envelope complete, but ai_generated: true.
        (records_dir / "crafted-test-record.yaml").write_text(
            "control: IAC-17\n"
            "period: 2026-06\n"
            "source: Okta IGA + Workday HRIS\n"
            "ai_generated: true\n"
        )
        # Give the validator the real schemas so schema loading is exercised.
        schema_src = REPO_ROOT / "02-controls" / "evidence-schemas"
        schema_dst = tmp_path / "02-controls" / "evidence-schemas"
        schema_dst.mkdir(parents=True)
        for f in schema_src.glob("*.yaml"):
            (schema_dst / f.name).write_text(f.read_text())

        proc = subprocess.run(
            [sys.executable, "-c", script],
            cwd=tmp_path, capture_output=True, text=True,
        )
    out = proc.stdout + proc.stderr
    check("validator exits non-zero on ai_generated: true", proc.returncode != 0,
          "exit={}".format(proc.returncode))
    check("validator names the ai_generated violation",
          "ai_generated=True" in out and "must be false" in out)
    check("validator declares the failure", "EVIDENCE VALIDATION FAILED" in out)
    return out


def test_mcp_json_gateways() -> None:
    mcp_path = REPO_ROOT / ".mcp.json"
    check(".mcp.json exists at repo root", mcp_path.exists())
    if not mcp_path.exists():
        return
    cfg = json.loads(mcp_path.read_text())
    servers = cfg.get("mcpServers", {})
    raw = mcp_path.read_text().lower()
    for system in ("jira", "aws", "github"):
        match = [n for n in servers if system in n.lower()]
        check("gateway configured for {}".format(system), bool(match))
        for name in match:
            s = servers[name]
            check("{}: streamable HTTP transport, not stdio".format(name),
                  s.get("type") == "http" and "command" not in s,
                  "type={}".format(s.get("type")))
            url = s.get("url", "")
            check("{}: url uses env expansion (no hardcoded endpoint creds)".format(name),
                  url.startswith("${") or url.startswith("https://"))
            hdrs = json.dumps(s.get("headers", {}))
            check("{}: no inline secrets in headers".format(name),
                  ("${" in hdrs) or hdrs == "{}")
    check("no alwaysLoad: true anywhere in .mcp.json", '"alwaysload": true' not in raw)


def test_ssrf_guard() -> None:
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    try:
        import mcp_gateways
    except ImportError:
        check("tools/mcp_gateways.py importable", False, "module missing")
        return
    bad = [
        "https://169.254.169.254/latest/meta-data/",
        "https://metadata.google.internal/computeMetadata/v1/",
        "https://127.0.0.1:8443/mcp",
        "https://10.0.0.5/mcp",
        "https://192.168.1.10/mcp",
        "http://mcp.atlassian.com/v1/sse",  # not HTTPS
    ]
    for url in bad:
        try:
            ok = mcp_gateways.validate_gateway_url(url)
        except Exception:
            ok = False
        check("SSRF guard rejects {}".format(url), ok is False)
    check("SSRF guard accepts a public https endpoint",
          mcp_gateways.validate_gateway_url("https://mcp.atlassian.com/v1/sse") is True)


def test_fixture_fallback_and_drift_prefix() -> None:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("JIRA_", "AWS_", "GITHUB_MCP_", "MCP_"))}
    proc = subprocess.run(
        [sys.executable, "tools/check_control_health.py",
         "--source", "auto",
         "--signals", "06-evidence-and-audit/drift-signals.example.yaml"],
        cwd=REPO_ROOT, capture_output=True, text=True, env=env,
    )
    out = proc.stdout + proc.stderr
    check("health check runs with gateways unconfigured", proc.returncode == 0,
          "exit={}".format(proc.returncode))
    check("health check reports fixture fallback", "fallback" in out.lower())
    check("drift Issue titles carry the [drift] prefix",
          "[drift] Control drift:" in out)


def main() -> int:
    print("== Unit D: MCP evidence gateways ==")
    test_validator_rejects_ai_generated_true()
    test_mcp_json_gateways()
    test_ssrf_guard()
    test_fixture_fallback_and_drift_prefix()
    print("=" * 50)
    if FAILURES:
        print("FAILED: {} check(s): {}".format(len(FAILURES), ", ".join(FAILURES)))
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
