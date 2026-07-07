#!/usr/bin/env python3
"""Generate the OSCAL System Security Plan (SSP) for the example system.

Emits generated/ssp.oscal.json: a real OSCAL 1.1.3 System Security Plan that
imports one OSCAL Profile (default: the SOC 2 profile) and provides an
implemented-requirement for every control that profile selects from the
Living Control Set catalog (02-controls/control-library.oscal.json).

The SSP describes the ILLUSTRATIVE example archetype from config.example.yaml
(a consumer location-safety service). It makes no claim about any real
organization's posture; every narrative is carried verbatim from the Living
Control Set's control statements, which are themselves illustrative.

OSCAL rules baked in:
  - Every element that OSCAL identifies carries an RFC-4122 UUID in v4 format
    (version nibble 4, variant bits 10). UUIDs are DERIVED deterministically
    from a content fingerprint, so an unchanged input set reproduces the file
    byte-for-byte, and ANY content change regenerates every UUID including the
    document root uuid and bumps last-modified.
  - Control statements map to the catalog's specific statement part IDs
    (e.g. aat-01_smt), never to narrative blobs.
  - Organization-Defined Parameters are expressed as set-parameters carrying
    the values the catalog defines for the example archetype, never as prose.
  - Every cross-reference the SSP makes (component-uuid, control-id,
    party-uuid, statement-id, param-id) resolves; tools/validate_oscal.py
    checks this in CI.

Run:

    python3 tools/generate_ssp.py            # writes generated/ssp.oscal.json
    python3 tools/generate_ssp.py --profile 02-controls/profiles/soc2.profile.oscal.json

Idempotence: if the regenerated content fingerprint matches the committed
file's fingerprint prop, the file is left untouched (last-modified stays
stable). Otherwise the file is rewritten with a fresh last-modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required. Install it with: pip install pyyaml\n")
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "02-controls" / "control-library.oscal.json"
LIBRARY_PATH = REPO_ROOT / "02-controls" / "control-library.yaml"
CONFIG_PATH = REPO_ROOT / "config.example.yaml"
DEFAULT_PROFILE = REPO_ROOT / "02-controls" / "profiles" / "soc2.profile.oscal.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "ssp.oscal.json"

OSCAL_VERSION = "1.1.3"
NS = "https://github.com/tiffanidickerson437-lang/compliance-program/ns/oscal"
FINGERPRINT_PROP = "content-fingerprint"

# uuid() placeholder marker: keys are replaced by derived UUIDs after the
# content fingerprint is computed, so the fingerprint covers content only.
UUID_KEY_PREFIX = "uuid:"


def uid(key: str) -> str:
    """Stable placeholder for a UUID, resolved after fingerprinting."""
    return UUID_KEY_PREFIX + key


def derive_uuid_v4_format(fingerprint: str, key: str) -> str:
    """Derive an RFC-4122 v4-format UUID from the content fingerprint + key.

    The 128 bits come from SHA-256 of the fingerprint and the element key,
    with the version nibble forced to 4 and the variant bits to 10, so the
    result is a well-formed v4-format UUID that is reproducible for identical
    content and different for ANY content change.
    """
    digest = hashlib.sha256((fingerprint + "|" + key).encode()).digest()
    b = bytearray(digest[:16])
    b[6] = (b[6] & 0x0F) | 0x40  # version 4
    b[8] = (b[8] & 0x3F) | 0x80  # variant 10
    h = b.hex()
    return "-".join((h[0:8], h[8:12], h[12:16], h[16:20], h[20:32]))


def walk_controls(node: dict, acc: dict) -> None:
    for control in node.get("controls", []) or []:
        acc[control["id"]] = control
        walk_controls(control, acc)
    for group in node.get("groups", []) or []:
        walk_controls(group, acc)


def statement_part_ids(control: dict) -> list[str]:
    """Return the IDs of the control's statement parts (incl. nested items)."""
    out: list[str] = []

    def collect(part: dict) -> None:
        if part.get("id"):
            out.append(part["id"])
        for sub in part.get("parts", []) or []:
            collect(sub)

    for part in control.get("parts", []) or []:
        if part.get("name") == "statement":
            collect(part)
    return out


def profile_control_ids(profile_doc: dict) -> list[str]:
    ids: list[str] = []
    for imp in profile_doc["profile"].get("imports", []) or []:
        for inc in imp.get("include-controls", []) or []:
            ids.extend(inc.get("with-ids", []) or [])
    return ids


def build_ssp(profile_path: Path, out_dir: Path) -> dict:
    catalog = json.loads(CATALOG_PATH.read_text())["catalog"]
    library = yaml.safe_load(LIBRARY_PATH.read_text())
    config = yaml.safe_load(CONFIG_PATH.read_text())
    profile_doc = json.loads(profile_path.read_text())

    controls_by_id: dict[str, dict] = {}
    walk_controls(catalog, controls_by_id)
    statements_by_lib_id = {
        (c.get("id") or "").lower(): (c.get("statement") or "").strip()
        for c in library.get("controls", []) or []
    }

    company = config.get("company", {}) or {}
    system_name = company.get("name", "Example System")
    profile_title = profile_doc["profile"]["metadata"]["title"]
    # href is relative to the SSP's own directory so it resolves wherever the
    # output lands (default: generated/).
    profile_href = os.path.relpath(profile_path, out_dir).replace("\\", "/")

    party_org = uid("party:organization")
    comp_system = uid("component:this-system")
    role_system_owner = "system-owner"
    role_control_owner = "control-owner"

    implemented = []
    for control_id in profile_control_ids(profile_doc):
        control = controls_by_id.get(control_id)
        if control is None:
            raise SystemExit(
                "profile selects {} which is not in the catalog".format(control_id)
            )
        narrative = statements_by_lib_id.get(control_id.lower(), "")
        statements = []
        for smt_id in statement_part_ids(control):
            statements.append(
                {
                    "statement-id": smt_id,
                    "uuid": uid("statement:{}:{}".format(control_id, smt_id)),
                    "by-components": [
                        {
                            "component-uuid": comp_system,
                            "uuid": uid("by-component:{}:{}".format(control_id, smt_id)),
                            "description": (
                                narrative
                                or "Implemented as specified by catalog control {}.".format(control_id)
                            )
                            + " (Illustrative: carried verbatim from the Living Control "
                            "Set statement for the example archetype; not a claim about "
                            "a real organization.)",
                        }
                    ],
                }
            )
        req: dict = {
            "uuid": uid("implemented-requirement:" + control_id),
            "control-id": control_id,
            "statements": statements,
            "responsible-roles": [
                {"role-id": role_control_owner, "party-uuids": [party_org]}
            ],
        }
        set_params = []
        for param in control.get("params", []) or []:
            values = param.get("values") or []
            if values:
                set_params.append({"param-id": param["id"], "values": list(values)})
        if set_params:
            req["set-parameters"] = set_params
        implemented.append(req)

    ssp = {
        "system-security-plan": {
            "uuid": uid("root"),
            "metadata": {
                "title": "System Security Plan — {} (illustrative)".format(system_name),
                "last-modified": "@LAST_MODIFIED@",
                "version": "1.0.0",
                "oscal-version": OSCAL_VERSION,
                "props": [
                    {"name": "scf-version", "ns": NS,
                     "value": (library.get("metadata", {}) or {}).get("scf_version", "")},
                    {"name": FINGERPRINT_PROP, "ns": NS, "value": "@FINGERPRINT@"},
                ],
                "remarks": (
                    "Illustrative SSP for the example archetype in config.example.yaml "
                    "(a consumer location-safety service). Generated by "
                    "tools/generate_ssp.py from the Living Control Set catalog and the "
                    "{} selection. Makes no claim about any real organization's "
                    "posture. UUIDs are RFC-4122 v4-format, derived deterministically "
                    "from the content fingerprint: any content change regenerates the "
                    "root uuid and every element uuid and bumps last-modified."
                ).format(profile_title),
                "roles": [
                    {"id": role_system_owner, "title": "System owner (by function)"},
                    {"id": role_control_owner, "title": "Control owner (by function)"},
                ],
                "parties": [
                    {
                        "uuid": party_org,
                        "type": "organization",
                        "name": company.get("legal_entity", system_name),
                        "remarks": "Illustrative archetype organization from config.example.yaml.",
                    }
                ],
                "responsible-parties": [
                    {"role-id": role_system_owner, "party-uuids": [party_org]},
                    {"role-id": role_control_owner, "party-uuids": [party_org]},
                ],
            },
            "import-profile": {"href": profile_href},
            "system-characteristics": {
                "system-ids": [{"id": "example-location-safety-service"}],
                "system-name": system_name,
                "description": (
                    "Illustrative archetype: a privately held consumer location-safety "
                    "service that processes precise location and minors' data and runs "
                    "an agentic AI layer on a real-time location graph. Defined in "
                    "config.example.yaml; not a real system."
                ),
                "security-sensitivity-level": "high",
                "system-information": {
                    "information-types": [
                        {
                            "uuid": uid("information-type:location-graph"),
                            "title": "Real-time location graph (members incl. minors)",
                            "description": (
                                "Precise geolocation and account data for members, "
                                "including children, plus derived safety events. "
                                "Illustrative data description for the example archetype."
                            ),
                            "confidentiality-impact": {"base": "high"},
                            "integrity-impact": {"base": "high"},
                            "availability-impact": {"base": "moderate"},
                        }
                    ]
                },
                "security-impact-level": {
                    "security-objective-confidentiality": "high",
                    "security-objective-integrity": "high",
                    "security-objective-availability": "moderate",
                },
                "status": {
                    "state": "other",
                    "remarks": "Illustrative example system; no operational status is claimed.",
                },
                "authorization-boundary": {
                    "description": (
                        "The example service's production environment: the location "
                        "graph data stores, the agentic AI layer, and the supporting "
                        "identity, logging, and consent systems named in "
                        "config.example.yaml. Illustrative boundary for the archetype."
                    )
                },
            },
            "system-implementation": {
                "users": [
                    {
                        "uuid": uid("user:system-owner"),
                        "title": "System owner (by function)",
                        "role-ids": [role_system_owner],
                    }
                ],
                "components": [
                    {
                        "uuid": comp_system,
                        "type": "this-system",
                        "title": system_name,
                        "description": (
                            "The example location-safety service as a whole; the single "
                            "component every control statement is implemented by in this "
                            "illustrative SSP."
                        ),
                        "status": {"state": "under-development"},
                        "responsible-roles": [
                            {"role-id": role_system_owner, "party-uuids": [party_org]}
                        ],
                    }
                ],
            },
            "control-implementation": {
                "description": (
                    "One implemented-requirement per control selected by {} from the "
                    "Living Control Set. Statement narratives are carried verbatim from "
                    "02-controls/control-library.yaml; parameters are set from the "
                    "catalog's defined values (set-parameter, never prose)."
                ).format(profile_title),
                "implemented-requirements": implemented,
            },
        }
    }
    return ssp


def resolve_uuids(ssp: dict) -> tuple[dict, str]:
    """Fingerprint the content, then replace every uuid placeholder."""
    canonical = json.dumps(ssp, sort_keys=True, separators=(",", ":"))
    fingerprint = hashlib.sha256(canonical.encode()).hexdigest()

    def sub(node):
        if isinstance(node, dict):
            return {k: sub(v) for k, v in node.items()}
        if isinstance(node, list):
            return [sub(v) for v in node]
        if isinstance(node, str):
            if node.startswith(UUID_KEY_PREFIX):
                return derive_uuid_v4_format(fingerprint, node[len(UUID_KEY_PREFIX):])
            if node == "@FINGERPRINT@":
                return fingerprint
        return node

    return sub(ssp), fingerprint


def existing_fingerprint(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        doc = json.loads(path.read_text())
        for prop in doc["system-security-plan"]["metadata"].get("props", []) or []:
            if prop.get("name") == FINGERPRINT_PROP:
                return prop.get("value")
    except (json.JSONDecodeError, KeyError):
        return None
    return None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        default=str(DEFAULT_PROFILE),
        help="OSCAL profile the SSP imports (default: the SOC 2 profile)",
    )
    parser.add_argument("--out", default=str(OUTPUT_PATH))
    args = parser.parse_args(argv)

    profile_path = Path(args.profile).resolve()
    out_path = Path(args.out)

    ssp, fingerprint = resolve_uuids(build_ssp(profile_path, out_path.resolve().parent))

    if existing_fingerprint(out_path) == fingerprint:
        print("ssp unchanged (fingerprint {}); {} left untouched".format(fingerprint[:12], out_path))
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def stamp_last_modified(node):
        if isinstance(node, dict):
            return {k: stamp_last_modified(v) for k, v in node.items()}
        if isinstance(node, list):
            return [stamp_last_modified(v) for v in node]
        if node == "@LAST_MODIFIED@":
            return stamp
        return node

    ssp = stamp_last_modified(ssp)
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(ssp, indent=2) + "\n")
    reqs = len(ssp["system-security-plan"]["control-implementation"]["implemented-requirements"])
    print(
        "wrote {} ({} implemented-requirements; root uuid {}; fingerprint {})".format(
            out_path, reqs, ssp["system-security-plan"]["uuid"], fingerprint[:12]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
