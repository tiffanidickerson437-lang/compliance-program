#!/usr/bin/env python3
"""draft_framework_mapping.py — onboard ANY framework as an explicit STRM mapping
over the owned control set.

Adding a framework means authoring a mapping from its requirements to controls we
ALREADY OWN — never rewriting controls. This tool works with explicit STRM only
(mappings/strm-schema.yaml): it drafts EMPTY template entries for a human to
author and validates existing mapping files. It never guesses relationships —
no NLP, no scoring of text overlap. The human authors every relationship_type
and relationship_strength; the pull-request merge is the authorization.

Every mapping entry carries exactly one of the 5 relationship types
(equal-to, subset-of, superset-of, intersects-with, no-relationship) plus an
integer relationship strength 1-10 (1 nominal, 5 moderate, 10 strongest).
Directionality is declared once in mappings/strm-schema.yaml: the owned control
is the Reference document, the framework requirement is the Focal document.

Usage:
  # Draft a template with one unauthored entry per requirement:
  python3 tools/draft_framework_mapping.py --framework frameworks/iso-42001.requirements.yaml

  # Validate an existing mapping file (same checks as tools/strm_lint.py):
  python3 tools/draft_framework_mapping.py --validate mappings/iso42001.draft.yaml
"""
import argparse
import os
import sys
from pathlib import Path

import yaml

import strm_lint

REPO = Path(__file__).resolve().parent.parent


def draft_template(framework_path, catalog_path, out_path, force=False):
    controls = yaml.safe_load(open(catalog_path, encoding="utf-8"))["controls"]
    fw = yaml.safe_load(open(framework_path, encoding="utf-8"))
    fwid, fwname = fw["framework"]["id"], fw["framework"]["name"]
    fw_rel = os.path.relpath(framework_path, REPO)

    entries = []
    for req in fw["requirements"]:
        entries.append({"mapping": {
            "master_control_id": None,   # HUMAN: a control id from the catalog
            "external_framework": fwname,
            "external_requirement_id": req["id"],
            "requirement_title": req.get("title"),
            "strm_parameters": {
                "relationship_type": None,      # HUMAN: one of the 5 types in strm-schema.yaml
                "relationship_strength": None,  # HUMAN: integer 1-10
            },
            "references": [f"{fw_rel}#{req['id']}"],
        }})

    out = out_path or str(REPO / "mappings" / f"{fwid}.draft.yaml")
    if os.path.exists(out) and not force:
        sys.exit(f"REFUSING to overwrite existing mapping: {out}\n"
                 f"A mapping file may already carry human-authored entries. "
                 f"Pass --out for a different path, or --force to overwrite.")
    if os.path.dirname(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
    yaml.safe_dump({"strm_mapping": {
        "framework_id": fwid,
        "framework_name": fwname,
        "status": "TEMPLATE_PENDING_HUMAN_AUTHORING",
        "schema": "mappings/strm-schema.yaml",
        "requirements_source": fw_rel,
        "method": ("Explicit STRM template drafted by tools/draft_framework_mapping.py — "
                   "a human authors every relationship_type and relationship_strength; "
                   "review and approve via pull request, the merge is the authorization"),
        "entries": entries,
    }}, open(out, "w", encoding="utf-8"), sort_keys=False, allow_unicode=True, width=100)

    print(f"Framework template drafted: {fwname}")
    print(f"Requirements: {len(entries)}   controls in catalog: {len(controls)}   controls modified: 0")
    print(f"Template written: {out}")
    print("Every entry is UNAUTHORED (relationship_type/strength are null) and will")
    print("fail tools/strm_lint.py until a human authors it. That is the gate:")
    print("nothing maps until a human says how, and the PR merge is the authorization.")


def validate(mapping_path, catalog_path):
    catalog_ids = strm_lint.load_catalog_ids(catalog_path)
    findings, _ = strm_lint.lint_file(Path(mapping_path), catalog_ids)
    if findings:
        print(f"INVALID — {len(findings)} finding(s):")
        for f in findings:
            print(f"  {f}")
        sys.exit(1)
    print(f"VALID — {mapping_path} passes the STRM checks "
          f"(schema: mappings/strm-schema.yaml)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", help="path to a framework requirements YAML; drafts a template")
    ap.add_argument("--validate", help="path to an existing STRM mapping file to validate")
    ap.add_argument("--catalog",
                    default=str(REPO / "02-controls" / "control-library.yaml"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing mapping file when drafting")
    a = ap.parse_args()

    if bool(a.framework) == bool(a.validate):
        ap.error("provide exactly one of --framework (draft a template) or --validate")
    if a.framework:
        draft_template(a.framework, a.catalog, a.out, force=a.force)
    else:
        validate(a.validate, a.catalog)


if __name__ == "__main__":
    main()
