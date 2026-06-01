#!/usr/bin/env python3
"""Scaffold engine: resolve the program from one configuration file.

This is the executable behind the "re-render the scaffold" step. It reads a
configuration file of the shape of config.example.yaml, filters the owned
control library to the declared frameworks, data types, AI posture, and
listings, and writes a tailored selection under generated/.

Run:

    python3 tools/scaffold.py config.example.yaml

The control library (02-controls/control-library.yaml) is the single source of
truth. This engine selects a view over it and never redefines a control. Adding
a framework is a crosswalk mapping, never a new control, so the output is a
resolution and not a parallel control set.

Output (written to generated/):
  - in-scope-controls.yaml : the tailored control selection with the reason each
    control is in scope and the frameworks it satisfies.
  - profile-selection.yaml : the per-framework OSCAL profile selection, machine
    readable, matching the profiles under 02-controls/profiles/.

The run is deterministic, so the committed sample output stays stable until the
configuration or the control library changes.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "PyYAML is required. Install it with: pip install pyyaml\n"
    )
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTROL_LIBRARY = REPO_ROOT / "02-controls" / "control-library.yaml"
CROSSWALK = REPO_ROOT / "02-controls" / "framework-crosswalk.yaml"
OUTPUT_DIR = REPO_ROOT / "generated"

# Maps a framework slug as written in the configuration to the key used in
# framework-crosswalk.yaml. A slug with no owned control mapped resolves to an
# empty selection and is reported honestly rather than dropped silently.
FRAMEWORK_KEY_BY_SLUG = {
    "soc2": "soc2",
    "iso27001": "iso27001",
    "iso42001": "iso42001",
    "nist-ai-rmf": "nist_ai_rmf",
    "nist-csf": "nist_csf",
    "coppa": "coppa",
    "ccpa": "ccpa_cpra",
    "ccpa-cpra": "ccpa_cpra",
    "gdpr": "gdpr",
    "eu-ai-act": "eu_ai_act",
    "sox-itgc": "sox_itgc",
}

# Data-type triggers turn on mandatory control families regardless of which
# frameworks are named, because the obligation follows the data, not the audit.
DATA_TYPE_TRIGGERS = {
    "minors": ["PRI-03.13"],
    "precise-location": ["AAT-01"],
}

# A non-empty listings block brings the SOX ITGC pillars into scope.
SOX_ITGC_CONTROLS = ["IAC-17", "CHG-02", "MON-01"]

# ai-products turns on the agent governance control and the AI governance pillar.
AI_PRODUCT_CONTROLS = ["AAT-01"]


def load_yaml(path: Path) -> dict:
    with path.open() as handle:
        return yaml.safe_load(handle) or {}


def configured_frameworks(config: dict) -> list[str]:
    """Flatten the frameworks block (primary, emerging, financial) to slugs."""
    block = config.get("frameworks", {}) or {}
    slugs: list[str] = []
    for group in ("primary", "emerging", "financial"):
        for slug in block.get(group, []) or []:
            if slug not in slugs:
                slugs.append(slug)
    return slugs


def controls_for_framework(crosswalk: dict, key: str) -> list[str]:
    """Return the control IDs that satisfy a framework key in the crosswalk."""
    by_framework = crosswalk.get("by_framework", {}) or {}
    entry = by_framework.get(key)
    if entry is None:
        return []
    # The SOX ITGC entry is a mapping with a nested controls list; every other
    # entry is a list of {control, refs} rows.
    if isinstance(entry, dict):
        return [row["control"] for row in entry.get("controls", []) if "control" in row]
    return [row["control"] for row in entry if isinstance(row, dict) and "control" in row]


def resolve(config: dict, library: dict, crosswalk: dict) -> dict:
    controls_by_id = {c["id"]: c for c in library.get("controls", [])}

    # selection maps a control ID to the ordered, de-duplicated reasons it is in
    # scope, so the output explains itself.
    selection: dict[str, list[str]] = {}

    def add_reason(control_id: str, reason: str) -> None:
        selection.setdefault(control_id, [])
        if reason not in selection[control_id]:
            selection[control_id].append(reason)

    framework_views: list[dict] = []
    framework_registry = crosswalk.get("frameworks", {}) or {}
    triggers_fired: list[str] = []

    # 1. Framework selection: each in-scope framework contributes its controls.
    for slug in configured_frameworks(config):
        key = FRAMEWORK_KEY_BY_SLUG.get(slug)
        name = framework_registry.get(key, {}).get("name", slug) if key else slug
        profile = framework_registry.get(key, {}).get("profile") if key else None
        ids = controls_for_framework(crosswalk, key) if key else []
        for control_id in ids:
            add_reason(control_id, "framework: {}".format(name))
        framework_views.append(
            {
                "slug": slug,
                "key": key,
                "name": name,
                "profile": profile,
                "controls": ids,
                "note": None if ids else "no owned control mapped yet; tracked as a forward target",
            }
        )

    # 2. Data-type triggers: the obligation follows the data.
    for data_type in config.get("data-types", []) or []:
        for control_id in DATA_TYPE_TRIGGERS.get(data_type, []):
            add_reason(control_id, "data-type: {}".format(data_type))
            triggers_fired.append("data-type {} -> {}".format(data_type, control_id))

    # 3. AI posture: ai-products turns on the agent control and the AI pillar.
    ai_on = bool(config.get("ai-products"))
    if ai_on:
        for control_id in AI_PRODUCT_CONTROLS:
            add_reason(control_id, "ai-products: true")
            triggers_fired.append("ai-products -> {}".format(control_id))

    # 4. Listings: a non-empty block brings SOX ITGC into scope.
    listings = (config.get("company", {}) or {}).get("listings") or []
    sox_on = bool(listings)
    if sox_on:
        for control_id in SOX_ITGC_CONTROLS:
            add_reason(control_id, "listings: SOX ITGC scope")
            triggers_fired.append("listings -> {} (SOX ITGC)".format(control_id))

    # Build the per-control output, ordered by the library's own order.
    in_scope_controls = []
    for control_id, control in controls_by_id.items():
        if control_id not in selection:
            continue
        mappings = control.get("framework_mappings", []) or []
        in_scope_controls.append(
            {
                "id": control_id,
                "title": control.get("title", ""),
                "family": control.get("family", ""),
                "owner": control.get("owner", ""),
                "automation": control.get("automation", ""),
                "selected_because": selection[control_id],
                "frameworks_satisfied": [m.get("framework") for m in mappings],
            }
        )

    # Pillars enabled: a small, defensible derivation from what is in scope.
    pillars = ["00-governance", "01-risk-management", "02-controls"]
    if any(c["id"] == "TPM-01" for c in in_scope_controls):
        pillars.append("03-tprm")
    if ai_on:
        pillars.append("04-ai-governance")
    pillars.append("05-secure-development")
    pillars.append("06-evidence-and-audit")
    pillars.append("07-stakeholder-management")

    provenance = config.get("provenance", {}) or {}

    summary = {
        "frameworks_in_scope": [v["name"] for v in framework_views],
        "controls_in_scope_count": len(in_scope_controls),
        "controls_in_scope": [c["id"] for c in in_scope_controls],
        "pillars_enabled": pillars,
        "sox_itgc_scope": sox_on,
        "sox_itgc_basis": provenance.get("sox_itgc_basis", "home-lab-framework-mapping"),
        "ai_governance_enabled": ai_on,
        "triggers_fired": triggers_fired,
    }

    return {
        "in_scope": {
            "metadata": {
                "generated_by": "tools/scaffold.py",
                "source_control_library": "02-controls/control-library.yaml",
                "note": (
                    "Tailored view resolved from the configuration. The control "
                    "library is the single source of truth; this file selects a "
                    "view and redefines nothing. Regenerate with "
                    "python3 tools/scaffold.py <config>."
                ),
                "provenance": {
                    "basis": provenance.get("basis", "illustrative-example"),
                    "sox_itgc_basis": provenance.get(
                        "sox_itgc_basis", "home-lab-framework-mapping"
                    ),
                    "evidence_in_repo": provenance.get("evidence_in_repo", "illustrative"),
                },
            },
            "summary": summary,
            "in_scope_controls": in_scope_controls,
        },
        "profiles": {
            "metadata": {
                "generated_by": "tools/scaffold.py",
                "source_crosswalk": "02-controls/framework-crosswalk.yaml",
                "note": (
                    "Per-framework OSCAL profile selection. Each framework view is "
                    "a profile resolution over the one control library, not a copy."
                ),
            },
            "frameworks": [
                {
                    "slug": v["slug"],
                    "name": v["name"],
                    "profile": v["profile"],
                    "controls": v["controls"],
                    "note": v["note"],
                }
                for v in framework_views
            ],
        },
    }


def print_summary(result: dict, config_path: Path) -> None:
    summary = result["in_scope"]["summary"]
    print("Scaffold resolved from: {}".format(config_path))
    print("-" * 68)
    print("Frameworks in scope ({}):".format(len(summary["frameworks_in_scope"])))
    for name in summary["frameworks_in_scope"]:
        print("  - {}".format(name))
    print("")
    print("Controls in scope ({}):".format(summary["controls_in_scope_count"]))
    for control in result["in_scope"]["in_scope_controls"]:
        reasons = "; ".join(control["selected_because"])
        print("  - {:<10} {}".format(control["id"], control["title"]))
        print("      because: {}".format(reasons))
    print("")
    print("Pillars enabled: {}".format(", ".join(summary["pillars_enabled"])))
    print("SOX ITGC scope: {} (basis: {})".format(
        "on" if summary["sox_itgc_scope"] else "off", summary["sox_itgc_basis"]))
    print("AI governance enabled: {}".format("on" if summary["ai_governance_enabled"] else "off"))
    print("")
    print("Triggers fired:")
    for trigger in summary["triggers_fired"]:
        print("  - {}".format(trigger))
    print("-" * 68)
    print("Wrote generated/in-scope-controls.yaml and generated/profile-selection.yaml")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: python3 tools/scaffold.py <config.yaml>\n")
        return 2
    config_path = Path(argv[1])
    if not config_path.exists():
        sys.stderr.write("config not found: {}\n".format(config_path))
        return 2

    config = load_yaml(config_path)
    library = load_yaml(CONTROL_LIBRARY)
    crosswalk = load_yaml(CROSSWALK)

    result = resolve(config, library, crosswalk)

    OUTPUT_DIR.mkdir(exist_ok=True)
    with (OUTPUT_DIR / "in-scope-controls.yaml").open("w") as handle:
        yaml.safe_dump(result["in_scope"], handle, sort_keys=False, width=88)
    with (OUTPUT_DIR / "profile-selection.yaml").open("w") as handle:
        yaml.safe_dump(result["profiles"], handle, sort_keys=False, width=88)

    print_summary(result, config_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
