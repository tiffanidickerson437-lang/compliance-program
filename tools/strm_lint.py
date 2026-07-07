#!/usr/bin/env python3
"""strm_lint.py — lint every STRM mapping file in mappings/ against the canonical schema.

Directionality and entry shape are declared ONCE in mappings/strm-schema.yaml;
this linter enforces that declaration mechanically:

  - master_control_id exists in the control catalog (02-controls/control-library.yaml)
  - strm_parameters.relationship_type is exactly one of the 5 canonical types
  - strm_parameters.relationship_strength is an integer 1-10
  - references (citations) are present and non-empty for every mapping entry
  - required entry fields are present (external_framework, external_requirement_id)

Exit code 0 = all mappings pass; 1 = at least one finding. Findings are printed
one per line as  <file>: <entry locator>: <problem>.

Usage:
  python3 tools/strm_lint.py
  python3 tools/strm_lint.py --mappings-dir mappings/ --catalog 02-controls/control-library.yaml
"""
import argparse
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent

RELATIONSHIP_TYPES = {"equal-to", "subset-of", "superset-of",
                      "intersects-with", "no-relationship"}
STRENGTH_MIN, STRENGTH_MAX = 1, 10
REQUIRED_ENTRY_FIELDS = ("master_control_id", "external_framework",
                         "external_requirement_id", "strm_parameters",
                         "references")
SKIP_FILES = {"strm-schema.yaml"}


def load_catalog_ids(catalog_path):
    doc = yaml.safe_load(open(catalog_path, encoding="utf-8"))
    return {c["id"] for c in doc.get("controls", [])}


def lint_entry(mapping, where, catalog_ids, findings):
    for field in REQUIRED_ENTRY_FIELDS:
        if field not in mapping:
            findings.append(f"{where}: missing required field '{field}'")
    cid = mapping.get("master_control_id")
    if cid is not None and cid not in catalog_ids:
        findings.append(f"{where}: master_control_id '{cid}' not in the control catalog")
    params = mapping.get("strm_parameters") or {}
    rel = params.get("relationship_type")
    if rel not in RELATIONSHIP_TYPES:
        findings.append(f"{where}: relationship_type {rel!r} is not one of "
                        f"{sorted(RELATIONSHIP_TYPES)}")
    strength = params.get("relationship_strength")
    if not isinstance(strength, int) or isinstance(strength, bool) \
            or not (STRENGTH_MIN <= strength <= STRENGTH_MAX):
        findings.append(f"{where}: relationship_strength {strength!r} must be an "
                        f"integer {STRENGTH_MIN}-{STRENGTH_MAX}")
    refs = mapping.get("references")
    if "references" in mapping and (
            not isinstance(refs, list) or not refs
            or not all(isinstance(r, str) and r.strip() for r in refs)):
        findings.append(f"{where}: references must be a non-empty list of citations")


def lint_file(path, catalog_ids):
    """Lint one STRM mapping file; returns (findings, entry_count)."""
    findings = []
    try:
        doc = yaml.safe_load(open(path, encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"{path.name}: not parseable YAML — {e}"], 0
    if not isinstance(doc, dict) or "strm_mapping" not in doc:
        return ([f"{path.name}: no 'strm_mapping' top-level key — not a valid STRM file"], 0)
    strm = doc["strm_mapping"]
    for meta in ("framework_id", "framework_name", "status"):
        if not strm.get(meta):
            findings.append(f"{path.name}: strm_mapping.{meta} is missing")
    entries = strm.get("entries")
    if not isinstance(entries, list) or not entries:
        findings.append(f"{path.name}: strm_mapping.entries is missing or empty")
        return findings, 0
    for i, entry in enumerate(entries):
        mapping = (entry or {}).get("mapping")
        if not isinstance(mapping, dict):
            findings.append(f"{path.name}: entries[{i}]: missing 'mapping' key")
            continue
        where = (f"{path.name}: entries[{i}] "
                 f"({mapping.get('master_control_id')} -> "
                 f"{mapping.get('external_requirement_id')})")
        lint_entry(mapping, where, catalog_ids, findings)
    return findings, len(entries)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mappings-dir", default=str(REPO / "mappings"))
    ap.add_argument("--catalog",
                    default=str(REPO / "02-controls" / "control-library.yaml"))
    a = ap.parse_args()

    catalog_ids = load_catalog_ids(a.catalog)
    mdir = Path(a.mappings_dir)
    files = sorted(p for p in mdir.glob("*.yaml") if p.name not in SKIP_FILES)
    if not files:
        print(f"strm_lint: no mapping files found in {mdir}")
        sys.exit(1)

    all_findings = []
    entry_count = 0
    for path in files:
        findings, n = lint_file(path, catalog_ids)
        all_findings.extend(findings)
        entry_count += n

    if all_findings:
        print(f"strm_lint: {len(all_findings)} finding(s) across {len(files)} file(s):")
        for f in all_findings:
            print(f"  {f}")
        sys.exit(1)
    print(f"strm_lint: OK — {len(files)} mapping file(s), {entry_count} entries, "
          f"0 findings (catalog: {Path(a.catalog).name}, "
          f"{len(catalog_ids)} controls)")


if __name__ == "__main__":
    main()
