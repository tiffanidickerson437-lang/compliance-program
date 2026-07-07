#!/usr/bin/env python3
"""Unit C test: STRM linter + per-framework coverage report.

Plain python3 runnable (no pytest). Asserts the unit's done-condition:
  1. mappings/strm-schema.yaml declares the canonical STRM directionality ONCE.
  2. tools/strm_lint.py passes on the repo's mappings/ (exit 0).
  3. tools/strm_lint.py FAILS on known-bad fixtures (invalid control ID, bad
     relationship type, out-of-range strength, missing references).
  4. tools/strm_coverage.py generates the per-framework coverage %/delta report
     under generated/, and the coverage % matches the pre-made formula exactly:
       score = strength/10 if equal-to|subset-of
               0.5 * strength/10 if superset-of|intersects-with
               0 if no-relationship or unmapped
       framework coverage % = mean of requirement scores * 100
  5. tools/draft_framework_mapping.py is explicit-STRM only: no keyword/NLP
     heuristic remains, catalog default is 02-controls/control-library.yaml,
     and drafted templates carry strm_parameters for a human to author.
  6. Directionality is not inverted anywhere: no mapping-related file still
     labels the lean-control->broader-NIST-family direction as subset-of.
"""
import os
import re
import subprocess
import sys
import tempfile

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable or "python3"

FAILURES = []


def check(name, cond, detail=""):
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        FAILURES.append(name)


def run(args, **kw):
    return subprocess.run([PY] + args, cwd=REPO, capture_output=True, text=True, **kw)


# ---------------------------------------------------------------- 1. schema
print("[1] canonical STRM schema")
schema_path = os.path.join(REPO, "mappings", "strm-schema.yaml")
check("mappings/strm-schema.yaml exists", os.path.isfile(schema_path))
schema = {}
if os.path.isfile(schema_path):
    schema = yaml.safe_load(open(schema_path, encoding="utf-8")) or {}
    s = schema.get("strm_schema", {})
    rels = s.get("relationship_types", {})
    check("declares exactly the 5 relationship types",
          set(rels) == {"equal-to", "subset-of", "superset-of",
                        "intersects-with", "no-relationship"},
          f"got {sorted(rels)}")
    sub = str(rels.get("subset-of", {}).get("definition", "")).lower()
    sup = str(rels.get("superset-of", {}).get("definition", "")).lower()
    check("subset-of = framework requirement NARROWER (full coverage)",
          "narrower" in sub and "full" in sub, sub[:120])
    check("superset-of = framework requirement BROADER (gap/delta)",
          "broader" in sup and ("gap" in sup or "delta" in sup), sup[:120])
    strength = s.get("relationship_strength", {})
    check("strength scale is integer 1-10",
          strength.get("minimum") == 1 and strength.get("maximum") == 10)

# ---------------------------------------------------------------- 2. linter passes on repo
print("[2] linter passes on the repo's mappings")
lint = run(["tools/strm_lint.py"])
check("tools/strm_lint.py exits 0 on mappings/", lint.returncode == 0,
      (lint.stdout + lint.stderr)[-400:])

# ---------------------------------------------------------------- 3. linter catches bad fixtures
print("[3] linter fails on known-bad fixtures")


def bad_fixture(entry):
    d = tempfile.mkdtemp(prefix="strm_bad_")
    doc = {"strm_mapping": {"framework_id": "testfw",
                            "framework_name": "Test Framework",
                            "status": "DRAFT_PENDING_HUMAN_APPROVAL",
                            "entries": [{"mapping": entry}]}}
    with open(os.path.join(d, "testfw.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False)
    return d


GOOD = {"master_control_id": "AAT-01",
        "external_framework": "Test Framework",
        "external_requirement_id": "T.1",
        "strm_parameters": {"relationship_type": "intersects-with",
                            "relationship_strength": 5},
        "references": ["frameworks/iso-42001.requirements.yaml"]}

cases = {
    "invalid control ID rejected": dict(GOOD, master_control_id="ZZZ-99"),
    "invalid relationship_type rejected":
        dict(GOOD, strm_parameters={"relationship_type": "maps-to",
                                    "relationship_strength": 5}),
    "strength out of range rejected":
        dict(GOOD, strm_parameters={"relationship_type": "equal-to",
                                    "relationship_strength": 11}),
    "non-integer strength rejected":
        dict(GOOD, strm_parameters={"relationship_type": "equal-to",
                                    "relationship_strength": 5.5}),
    "missing references rejected": {k: v for k, v in GOOD.items()
                                    if k != "references"},
}
for name, entry in cases.items():
    d = bad_fixture(entry)
    r = run(["tools/strm_lint.py", "--mappings-dir", d])
    check(name, r.returncode != 0)

sane = run(["tools/strm_lint.py", "--mappings-dir", bad_fixture(GOOD)])
check("control fixture (valid entry) passes", sane.returncode == 0,
      (sane.stdout + sane.stderr)[-400:])

# ---------------------------------------------------------------- 4. coverage report
print("[4] per-framework coverage %/delta report generates")
cov = run(["tools/strm_coverage.py"])
check("tools/strm_coverage.py exits 0", cov.returncode == 0,
      (cov.stdout + cov.stderr)[-400:])
md_path = os.path.join(REPO, "generated", "framework-coverage.md")
yml_path = os.path.join(REPO, "generated", "framework-coverage.yaml")
check("generated/framework-coverage.md exists", os.path.isfile(md_path))
check("generated/framework-coverage.yaml exists", os.path.isfile(yml_path))

# Recompute expected coverage for iso42001 independently, straight from the
# spec formula, and compare with the generated report.
FULL = {"equal-to", "subset-of"}
PARTIAL = {"superset-of", "intersects-with"}


def spec_score(rel, strength):
    if rel in FULL:
        return strength / 10.0
    if rel in PARTIAL:
        return 0.5 * strength / 10.0
    return 0.0


if os.path.isfile(yml_path):
    report = yaml.safe_load(open(yml_path, encoding="utf-8")) or {}
    fw_reports = {f["framework_id"]: f for f in report.get("frameworks", [])}
    check("iso42001 present in coverage report", "iso42001" in fw_reports)

    reqs = yaml.safe_load(open(os.path.join(
        REPO, "frameworks", "iso-42001.requirements.yaml"),
        encoding="utf-8"))["requirements"]
    mapping_doc = yaml.safe_load(open(os.path.join(
        REPO, "mappings", "iso42001.draft.yaml"), encoding="utf-8"))
    entries = mapping_doc["strm_mapping"]["entries"]
    best = {}
    for e in entries:
        m = e["mapping"]
        p = m["strm_parameters"]
        sc = spec_score(p["relationship_type"], p["relationship_strength"])
        rid = m["external_requirement_id"]
        best[rid] = max(best.get(rid, 0.0), sc)
    scores = [best.get(r["id"], 0.0) for r in reqs]
    expected_pct = round(100.0 * sum(scores) / len(scores), 1)

    if "iso42001" in fw_reports:
        got = fw_reports["iso42001"]
        check("coverage %% matches the spec formula",
              round(float(got.get("coverage_percent", -1)), 1) == expected_pct,
              f"expected {expected_pct}, got {got.get('coverage_percent')}")
        deltas = {d["requirement_id"] for d in got.get("delta", [])}
        expected_deltas = {r["id"] for r in reqs if best.get(r["id"], 0.0) < 1.0}
        check("delta list = every requirement scoring < 1.0",
              deltas == expected_deltas,
              f"expected {sorted(expected_deltas)}, got {sorted(deltas)}")

if os.path.isfile(md_path):
    md = open(md_path, encoding="utf-8").read()
    check("markdown report names ISO/IEC 42001", "42001" in md)
    check("markdown report states coverage semantics",
          "reuse evidence" in md and "new control" in md.lower())

# ---------------------------------------------------------------- 5. mapper rewritten, heuristic gone
print("[5] draft_framework_mapping.py is explicit-STRM only")
mapper_src = open(os.path.join(REPO, "tools", "draft_framework_mapping.py"),
                  encoding="utf-8").read()
for forbidden in ("ai_draft_match", "matched_on", "keyword", "confidence"):
    check(f"no heuristic remnant: {forbidden!r}",
          forbidden not in mapper_src.lower())
check("catalog default is 02-controls/control-library.yaml",
      "control-library.yaml" in mapper_src
      and "owned-controls.yaml" not in mapper_src)

with tempfile.TemporaryDirectory(prefix="strm_tpl_") as td:
    tpl_out = os.path.join(td, "tpl.yaml")
    r = run(["tools/draft_framework_mapping.py",
             "--framework", "frameworks/iso-42001.requirements.yaml",
             "--out", tpl_out])
    check("mapper drafts a template file", r.returncode == 0 and
          os.path.isfile(tpl_out), (r.stdout + r.stderr)[-400:])
    if os.path.isfile(tpl_out):
        tpl = yaml.safe_load(open(tpl_out, encoding="utf-8"))
        tentries = tpl["strm_mapping"]["entries"]
        check("template has one entry per requirement", len(tentries) == 7)
        first = tentries[0]["mapping"]
        check("template entries carry strm_parameters for human authoring",
              "strm_parameters" in first
              and first["strm_parameters"]["relationship_type"] is None)

    # validate mode delegates to the linter checks
    v = run(["tools/draft_framework_mapping.py",
             "--validate", "mappings/iso42001.draft.yaml"])
    check("mapper --validate accepts the migrated repo mapping",
          v.returncode == 0, (v.stdout + v.stderr)[-400:])

# ---------------------------------------------------------------- 6. directionality not inverted
print("[6] no inverted subset-of direction remains")
owned = open(os.path.join(REPO, "02-controls", "owned-controls.yaml"),
             encoding="utf-8").read()
check("owned-controls.yaml: lean-control->NIST-family flipped to superset-of",
      "rel: subset-of" not in owned)
oscal = open(os.path.join(REPO, "02-controls", "owned-controls.oscal.json"),
             encoding="utf-8").read()
check("owned-controls.oscal.json: remarks flipped to superset-of",
      '"remarks": "subset-of"' not in oscal)
migrated = yaml.safe_load(open(os.path.join(
    REPO, "mappings", "iso42001.draft.yaml"), encoding="utf-8"))
check("iso42001 mapping migrated to strm_mapping/strm_parameters",
      "strm_mapping" in migrated)
check("iso42001 mapping has no legacy confidence fields",
      "confidence" not in open(os.path.join(
          REPO, "mappings", "iso42001.draft.yaml"), encoding="utf-8").read())

# ----------------------------------------------------------------
print()
if FAILURES:
    print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
    sys.exit(1)
print("ALL CHECKS PASSED")
