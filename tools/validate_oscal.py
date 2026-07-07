#!/usr/bin/env python3
"""Validate the OSCAL layer: Catalog, Profiles, and SSP.

Two legs, both required to exit 0:

1. Schema leg (compliance-trestle / OSCAL Compass Python SDK, when installed):
   each document is parsed into trestle's typed OSCAL models
   (trestle.oscal.catalog.Catalog, profile.Profile, ssp.SystemSecurityPlan),
   which enforces the OSCAL schema field-by-field. If trestle is not
   installed the leg is reported as SKIPPED and does not fail the run —
   CI installs trestle, so the PR gate always exercises it.

2. Deterministic cross-reference leg (always runs, stdlib + PyYAML only):
   - metadata: title, last-modified, version, oscal-version present.
   - UUIDs: every "uuid"-keyed value in repo-authored documents is a
     well-formed RFC-4122 v4-format UUID (version nibble 4, variant 10) and
     unique within its document. (The vendor SCF catalog is not held to v4 —
     it is third-party reference data, validated for schema only.)
   - Catalog: control IDs unique.
   - Profiles: every import href resolves to an existing catalog file, and
     every with-id resolves to a control in that catalog.
   - SSP: import-profile href resolves; every implemented-requirement
     control-id is selected by the imported profile; every statement-id is a
     statement part of that control in the catalog; every by-component
     component-uuid is a defined component; every party-uuid is a defined
     party; every set-parameter param-id is a parameter of that control; and
     every responsible role-id is a defined role.

Scope: 02-controls/control-library.oscal.json, every profile under
02-controls/profiles/, generated/ssp.oscal.json, and (schema leg only)
02-controls/scf/SCF-OSCAL-Catalog-2026.1.json.

Run:  python3 tools/validate_oscal.py
Exit: 0 all checks pass, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "02-controls" / "control-library.oscal.json"
PROFILES_DIR = REPO_ROOT / "02-controls" / "profiles"
SSP_PATH = REPO_ROOT / "generated" / "ssp.oscal.json"
SCF_CATALOG_PATH = REPO_ROOT / "02-controls" / "scf" / "SCF-OSCAL-Catalog-2026.1.json"

UUID_V4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)

ERRORS: list[str] = []
CHECKS = {"pass": 0}


def ok(msg: str) -> None:
    CHECKS["pass"] += 1
    print("PASS  " + msg)


def fail(msg: str) -> None:
    ERRORS.append(msg)
    print("FAIL  " + msg)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


# ---------------------------------------------------------------- schema leg
def trestle_schema_check(docs: list[tuple[Path, str]]) -> None:
    try:
        from trestle.oscal.catalog import Catalog
        from trestle.oscal.profile import Profile
        from trestle.oscal.ssp import SystemSecurityPlan
    except ImportError:
        print("SKIP  schema leg: compliance-trestle not installed "
              "(pip install compliance-trestle); cross-reference leg still runs")
        return

    model_for = {
        "catalog": (Catalog, "catalog"),
        "profile": (Profile, "profile"),
        "system-security-plan": (SystemSecurityPlan, "system-security-plan"),
    }
    for path, kind in docs:
        cls, key = model_for[kind]
        try:
            cls(**json.loads(path.read_text())[key])
            ok("schema (trestle {}): {}".format(kind, rel(path)))
        except Exception as exc:  # noqa: BLE001 - report, don't crash
            fail("schema (trestle {}): {}: {}".format(kind, rel(path), str(exc)[:400]))


# ------------------------------------------------------- deterministic checks
def collect_uuids(node, acc: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "uuid" and isinstance(value, str):
                acc.append(value)
            collect_uuids(value, acc)
    elif isinstance(node, list):
        for item in node:
            collect_uuids(item, acc)


def check_metadata(doc_root: dict, path: Path) -> None:
    metadata = doc_root.get("metadata", {}) or {}
    missing = [f for f in ("title", "last-modified", "version", "oscal-version")
               if not metadata.get(f)]
    if missing:
        fail("metadata: {} missing {}".format(rel(path), ", ".join(missing)))
    else:
        ok("metadata complete: {}".format(rel(path)))


def check_uuids_v4(doc_root: dict, path: Path) -> None:
    uuids: list[str] = []
    collect_uuids(doc_root, uuids)
    bad = [u for u in uuids if not UUID_V4_RE.match(u.lower())]
    dupes = sorted({u for u in uuids if uuids.count(u) > 1})
    if bad:
        fail("uuid: {} has {} non-RFC-4122-v4 uuid(s), e.g. {}".format(
            rel(path), len(bad), bad[0]))
    elif dupes:
        fail("uuid: {} has duplicate uuid(s), e.g. {}".format(rel(path), dupes[0]))
    else:
        ok("uuid: {} — {} uuids, all RFC-4122 v4-format and unique".format(
            rel(path), len(uuids)))


def walk_controls(node: dict, acc: dict) -> None:
    for control in node.get("controls", []) or []:
        acc.setdefault(control["id"], control)
        walk_controls(control, acc)
    for group in node.get("groups", []) or []:
        walk_controls(group, acc)


def statement_part_ids(control: dict) -> set[str]:
    out: set[str] = set()

    def collect(part: dict) -> None:
        if part.get("id"):
            out.add(part["id"])
        for sub in part.get("parts", []) or []:
            collect(sub)

    for part in control.get("parts", []) or []:
        if part.get("name") == "statement":
            collect(part)
    return out


def check_catalog(path: Path) -> dict:
    catalog = json.loads(path.read_text())["catalog"]
    check_metadata(catalog, path)
    check_uuids_v4(catalog, path)
    controls: dict = {}
    seen: list[str] = []

    def walk_dupes(node: dict) -> None:
        for control in node.get("controls", []) or []:
            seen.append(control["id"])
            walk_dupes(control)
        for group in node.get("groups", []) or []:
            walk_dupes(group)

    walk_dupes(catalog)
    walk_controls(catalog, controls)
    dupes = sorted({c for c in seen if seen.count(c) > 1})
    if dupes:
        fail("catalog: duplicate control id(s): {}".format(", ".join(dupes)))
    else:
        ok("catalog: {} controls, ids unique: {}".format(len(controls), rel(path)))
    return controls


def check_profile(path: Path, catalog_controls: dict) -> list[str]:
    profile = json.loads(path.read_text())["profile"]
    check_metadata(profile, path)
    check_uuids_v4(profile, path)
    selected: list[str] = []
    for imp in profile.get("imports", []) or []:
        href = imp.get("href", "")
        target = (path.parent / href).resolve()
        if not target.exists():
            fail("profile {}: import href does not resolve: {}".format(rel(path), href))
            continue
        if target != CATALOG_PATH.resolve():
            fail("profile {}: import href points outside the catalog: {}".format(rel(path), href))
            continue
        ok("profile {}: import resolves to {}".format(rel(path), rel(CATALOG_PATH)))
        for inc in imp.get("include-controls", []) or []:
            for cid in inc.get("with-ids", []) or []:
                selected.append(cid)
                if cid not in catalog_controls:
                    fail("profile {}: with-id {} not in catalog".format(rel(path), cid))
    missing = [c for c in selected if c not in catalog_controls]
    if not missing:
        ok("profile {}: all {} with-ids resolve in the catalog".format(rel(path), len(selected)))
    return selected


def check_ssp(path: Path, catalog_controls: dict,
              selected_by_profile: dict[Path, list[str]]) -> None:
    if not path.exists():
        fail("ssp: {} does not exist (run tools/generate_ssp.py)".format(rel(path)))
        return
    ssp = json.loads(path.read_text())["system-security-plan"]
    check_metadata(ssp, path)
    check_uuids_v4(ssp, path)

    href = (ssp.get("import-profile", {}) or {}).get("href", "")
    profile_path = (path.parent / href).resolve()
    if not profile_path.exists():
        fail("ssp: import-profile href does not resolve: {}".format(href))
        return
    if profile_path not in selected_by_profile:
        fail("ssp: import-profile href {} is not one of the validated profiles under {}".format(
            href, rel(PROFILES_DIR)))
        return
    ok("ssp: import-profile resolves to {}".format(rel(profile_path)))
    profile_ids = set(selected_by_profile[profile_path])

    metadata = ssp.get("metadata", {}) or {}
    party_uuids = {p.get("uuid") for p in metadata.get("parties", []) or []}
    role_ids = {r.get("id") for r in metadata.get("roles", []) or []}
    impl = ssp.get("system-implementation", {}) or {}
    component_uuids = {c.get("uuid") for c in impl.get("components", []) or []}

    problems = 0
    for rp in metadata.get("responsible-parties", []) or []:
        if rp.get("role-id") not in role_ids:
            fail("ssp: responsible-party role-id {} not defined".format(rp.get("role-id")))
            problems += 1
        for pu in rp.get("party-uuids", []) or []:
            if pu not in party_uuids:
                fail("ssp: responsible-party party-uuid {} not defined".format(pu))
                problems += 1
    for user in impl.get("users", []) or []:
        for rid in user.get("role-ids", []) or []:
            if rid not in role_ids:
                fail("ssp: user role-id {} not defined".format(rid))
                problems += 1

    reqs = (ssp.get("control-implementation", {}) or {}).get("implemented-requirements", []) or []
    for req in reqs:
        cid = req.get("control-id", "")
        control = catalog_controls.get(cid)
        if control is None:
            fail("ssp: implemented-requirement control-id {} not in catalog".format(cid))
            problems += 1
            continue
        if cid not in profile_ids:
            fail("ssp: control-id {} not selected by the imported profile".format(cid))
            problems += 1
        valid_smts = statement_part_ids(control)
        param_ids = {p.get("id") for p in control.get("params", []) or []}
        for smt in req.get("statements", []) or []:
            if smt.get("statement-id") not in valid_smts:
                fail("ssp: {} statement-id {} is not a statement part of the catalog control".format(
                    cid, smt.get("statement-id")))
                problems += 1
            for by in smt.get("by-components", []) or []:
                if by.get("component-uuid") not in component_uuids:
                    fail("ssp: {} by-component component-uuid {} not a defined component".format(
                        cid, by.get("component-uuid")))
                    problems += 1
        for sp in req.get("set-parameters", []) or []:
            if sp.get("param-id") not in param_ids:
                fail("ssp: {} set-parameter param-id {} not a parameter of the catalog control".format(
                    cid, sp.get("param-id")))
                problems += 1
        for rr in req.get("responsible-roles", []) or []:
            if rr.get("role-id") not in role_ids:
                fail("ssp: {} responsible-role {} not defined".format(cid, rr.get("role-id")))
                problems += 1
            for pu in rr.get("party-uuids", []) or []:
                if pu not in party_uuids:
                    fail("ssp: {} responsible-role party-uuid {} not defined".format(cid, pu))
                    problems += 1
    if problems == 0:
        ok("ssp: {} implemented-requirements; every control-id, statement-id, "
           "component-uuid, party-uuid, and param-id resolves".format(len(reqs)))


def main() -> int:
    profiles = sorted(PROFILES_DIR.glob("*.profile.oscal.json"))

    docs: list[tuple[Path, str]] = [(CATALOG_PATH, "catalog")]
    if SCF_CATALOG_PATH.exists():
        docs.append((SCF_CATALOG_PATH, "catalog"))
    docs += [(p, "profile") for p in profiles]
    if SSP_PATH.exists():
        docs.append((SSP_PATH, "system-security-plan"))

    trestle_schema_check(docs)

    catalog_controls = check_catalog(CATALOG_PATH)
    selected_by_profile: dict[Path, list[str]] = {}
    for profile in profiles:
        selected_by_profile[profile.resolve()] = check_profile(profile, catalog_controls)
    check_ssp(SSP_PATH, catalog_controls, selected_by_profile)

    print()
    if ERRORS:
        print("RESULT: FAIL ({} error(s), {} check(s) passed)".format(len(ERRORS), CHECKS["pass"]))
        return 1
    print("RESULT: PASS ({} checks — catalog, {} profiles, and SSP validate)".format(
        CHECKS["pass"], len(profiles)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
