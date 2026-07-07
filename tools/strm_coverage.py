#!/usr/bin/env python3
"""strm_coverage.py — per-framework coverage % and delta list from the STRM mappings.

Reads every STRM mapping file in mappings/ (directionality per
mappings/strm-schema.yaml) and the framework requirement lists in frameworks/,
then emits generated/framework-coverage.md and generated/framework-coverage.yaml.

Scoring formula (declared in strm-schema.yaml, applied verbatim):
  per external requirement:
    score = strength/10          if relationship is equal-to or subset-of
    score = 0.5 * strength/10    if relationship is superset-of or intersects-with
    score = 0                    if no-relationship or unmapped
  (where a requirement has multiple mapping entries, the max score counts)
  framework coverage % = mean of requirement scores * 100

Coverage semantics:
  equal-to / high-strength subset-of  -> complete coverage, reuse evidence
  superset-of / intersects-with       -> partial; compute the delta, human design required
  no-relationship / unmapped          -> new control needed

The delta list names every requirement scoring < 1.0, with its relationship and
what is missing.

Usage:
  python3 tools/strm_coverage.py
  python3 tools/strm_coverage.py --mappings-dir mappings/ --frameworks-dir frameworks/ --out-dir generated/
"""
import argparse
import datetime
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
FULL = {"equal-to", "subset-of"}
PARTIAL = {"superset-of", "intersects-with"}
SKIP_FILES = {"strm-schema.yaml"}

MISSING_TEXT = {
    "equal-to": "relationship strength below 10 — confirm the control fully "
                "matches the requirement or raise/author the delta",
    "subset-of": "relationship strength below 10 — the requirement is narrower "
                 "than the control; confirm full coverage or raise the strength",
    "superset-of": "the requirement is BROADER than the control — compute the "
                   "uncovered remainder; human control design required",
    "intersects-with": "partial overlap — each side covers ground the other "
                       "does not; compute the delta; human design required",
    "no-relationship": "no overlap — a new control is needed",
    "unmapped": "no mapping entry exists for this requirement — new control "
                "or new mapping needed",
}


def score(rel, strength):
    if rel in FULL:
        return strength / 10.0
    if rel in PARTIAL:
        return 0.5 * strength / 10.0
    return 0.0


def load_requirement_universe(frameworks_dir):
    """framework_id -> ordered list of requirement dicts, from frameworks/*.requirements.yaml."""
    universe = {}
    for path in sorted(Path(frameworks_dir).glob("*.requirements.yaml")):
        doc = yaml.safe_load(open(path, encoding="utf-8"))
        fw = (doc or {}).get("framework") or {}
        if fw.get("id"):
            universe[fw["id"]] = {"source": str(path.relative_to(REPO))
                                  if path.is_relative_to(REPO) else str(path),
                                  "requirements": doc.get("requirements") or []}
    return universe


def analyze(mappings_dir, frameworks_dir):
    universe = load_requirement_universe(frameworks_dir)
    frameworks = []
    for path in sorted(Path(mappings_dir).glob("*.yaml")):
        if path.name in SKIP_FILES:
            continue
        doc = yaml.safe_load(open(path, encoding="utf-8"))
        strm = (doc or {}).get("strm_mapping")
        if not strm:
            continue
        fwid = strm.get("framework_id")
        # best (max) score per requirement, plus the entry that achieved it
        best = {}
        for entry in strm.get("entries") or []:
            m = entry.get("mapping") or {}
            p = m.get("strm_parameters") or {}
            rel = p.get("relationship_type")
            strength = p.get("relationship_strength") or 0
            rid = m.get("external_requirement_id")
            sc = score(rel, strength)
            if rid not in best or sc > best[rid]["score"]:
                best[rid] = {"score": sc, "relationship": rel,
                             "strength": strength,
                             "control": m.get("master_control_id")}
        uni = universe.get(fwid)
        if uni:
            req_ids = [r["id"] for r in uni["requirements"]]
            titles = {r["id"]: r.get("title", "") for r in uni["requirements"]}
            denominator_note = f"all {len(req_ids)} requirements in {uni['source']}"
        else:
            req_ids = sorted(best)
            titles = {}
            denominator_note = (f"no requirements file found under {frameworks_dir} "
                                f"for '{fwid}' — coverage computed over the "
                                f"{len(req_ids)} mapped requirement(s) only; the "
                                f"true denominator may be larger")
        scores, delta = [], []
        for rid in req_ids:
            b = best.get(rid, {"score": 0.0, "relationship": "unmapped",
                               "strength": None, "control": None})
            scores.append(b["score"])
            if b["score"] < 1.0:
                delta.append({"requirement_id": rid,
                              "requirement_title": titles.get(rid, ""),
                              "relationship": b["relationship"],
                              "strength": b["strength"],
                              "mapped_control": b["control"],
                              "score": round(b["score"], 3),
                              "missing": MISSING_TEXT.get(
                                  b["relationship"],
                                  "invalid relationship_type — run "
                                  "tools/strm_lint.py and fix the mapping")})
        pct = round(100.0 * sum(scores) / len(scores), 1) if scores else 0.0
        frameworks.append({"framework_id": fwid,
                           "framework_name": strm.get("framework_name"),
                           "mapping_file": path.name,
                           "status": strm.get("status"),
                           "requirements_counted": len(req_ids),
                           "denominator": denominator_note,
                           "coverage_percent": pct,
                           "delta": delta})
    return frameworks


def write_yaml(frameworks, out_dir):
    out = Path(out_dir) / "framework-coverage.yaml"
    payload = {
        "generated_by": "tools/strm_coverage.py",
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema": "mappings/strm-schema.yaml",
        "formula": ("per requirement: strength/10 if equal-to|subset-of; "
                    "0.5*strength/10 if superset-of|intersects-with; 0 if "
                    "no-relationship|unmapped; max per requirement; "
                    "coverage % = mean of requirement scores * 100"),
        "frameworks": frameworks,
    }
    yaml.safe_dump(payload, open(out, "w", encoding="utf-8"),
                   sort_keys=False, allow_unicode=True, width=100)
    return out


def write_markdown(frameworks, out_dir):
    out = Path(out_dir) / "framework-coverage.md"
    lines = [
        "# Per-Framework Coverage Report",
        "",
        "Generated by `tools/strm_coverage.py` from the explicit STRM entries in",
        "`mappings/` (directionality per `mappings/strm-schema.yaml`). Do not edit",
        "by hand; regenerate instead.",
        "",
        "**Formula** — per external requirement: `strength/10` if equal-to or",
        "subset-of; `0.5 x strength/10` if superset-of or intersects-with; `0` if",
        "no-relationship or unmapped (max across a requirement's entries).",
        "Framework coverage % = mean of requirement scores x 100.",
        "",
        "**Coverage semantics** — equal-to / high-strength subset-of = complete",
        "coverage, reuse evidence. superset-of / intersects-with = partial:",
        "compute the delta, human design required. no-relationship / unmapped =",
        "new control needed.",
        "",
    ]
    for fw in frameworks:
        lines += [f"## {fw['framework_name']} — {fw['coverage_percent']}% coverage",
                  "",
                  f"- Mapping file: `mappings/{fw['mapping_file']}` "
                  f"(status: {fw['status']})",
                  f"- Requirements counted: {fw['requirements_counted']} "
                  f"({fw['denominator']})",
                  ""]
        if fw["delta"]:
            lines += [f"### Delta — {len(fw['delta'])} requirement(s) scoring < 1.0",
                      "",
                      "| Requirement | Title | Relationship | Strength | Score |"
                      " Mapped control | What is missing |",
                      "|---|---|---|---|---|---|---|"]
            for d in fw["delta"]:
                lines.append(
                    f"| {d['requirement_id']} | {d['requirement_title']} | "
                    f"{d['relationship']} | {d['strength'] if d['strength'] is not None else '—'} | "
                    f"{d['score']} | {d['mapped_control'] or '—'} | {d['missing']} |")
            lines.append("")
        else:
            lines += ["No delta: every requirement scores 1.0 "
                      "(complete coverage, reuse evidence).", ""]
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mappings-dir", default=str(REPO / "mappings"))
    ap.add_argument("--frameworks-dir", default=str(REPO / "frameworks"))
    ap.add_argument("--out-dir", default=str(REPO / "generated"))
    a = ap.parse_args()

    frameworks = analyze(a.mappings_dir, a.frameworks_dir)
    if not frameworks:
        print("strm_coverage: no STRM mapping files found — nothing to report")
        sys.exit(1)
    Path(a.out_dir).mkdir(parents=True, exist_ok=True)
    ypath = write_yaml(frameworks, a.out_dir)
    mpath = write_markdown(frameworks, a.out_dir)
    for fw in frameworks:
        print(f"strm_coverage: {fw['framework_name']}: "
              f"{fw['coverage_percent']}% over {fw['requirements_counted']} "
              f"requirement(s); delta items: {len(fw['delta'])}")
    print(f"strm_coverage: wrote {ypath} and {mpath}")


if __name__ == "__main__":
    main()
