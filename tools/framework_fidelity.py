#!/usr/bin/env python3
"""Prove the scaling claim, or fail. Belongs at tools/framework_fidelity.py on engine main.

THE CLAIM THIS CHECKS

    "One control set, rendered into every framework. Adding a framework is a
    mapping exercise, never a rebuild."

That is the engine's whole thesis, and today it is an assertion. Assertions are
what this program exists to replace. So this computes it.

WHAT IT FOUND, THE DAY IT WAS WRITTEN (2026-07-17, live main)

    12 frameworks registered in the crosswalk.
     8 rendered into profile-selection.yaml.
     4 dropped -- nist_csf, hipaa, nist80053, pci -- silently, no error, exit 0.

A registry that drops a third of its entries without complaint is not a scaling
mechanism; it is a scaling claim. This is the same fail-open class as the
evidence validator (adversarial finding #2) and the same defect the whole
program is branded against: a step that reports success without having done the
work. It is worse here than anywhere else, because "we render every framework"
is the sentence the engine is sold on.

THE FOUR AXES

    1. COMPLETENESS   every registered framework is rendered. No silent drops.
    2. PROVENANCE     every registered framework is actually mapped by at least
                      one control. A registry entry nobody maps is a phantom.
    3. DECLARATION    every framework a control maps to is registered. Rendering
                      a framework nobody declared is drift in the other direction.
    4. GRANULARITY    per framework, at what depth are the references written --
                      family, base control, or control-with-enhancement? Reported,
                      never scored, because depth is a fact about the mapping and
                      the honest answer is what makes it usable. A framework
                      mapped at family granularity is not assessable by a 3PAO,
                      and saying so in the artifact is worth more than a number.

WHY IT IS FRAMEWORK-AGNOSTIC ON PURPOSE

    No framework is named in the logic. There is no headline framework and no
    demoted one. CMMC, FedRAMP, SOC 2, PCI and whatever ships next are all just
    registry entries that must prove themselves the whole way through. The
    moment a check has to special-case a framework, the scaling claim is dead --
    so this one cannot.

FAILURE MODE: CLOSED. Unreadable source, moved schema, zero frameworks parsed:
all exit 2. A checker that cannot check does not report a pass.

    ENGINE_ROOT=~/src/compliance-program python3 tools/framework_fidelity.py
    python3 tools/framework_fidelity.py --remote      # read public main over https
    python3 tools/framework_fidelity.py --check       # exit code only
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL[2]: pyyaml missing. Cannot read the crosswalk, so cannot check.", file=sys.stderr)
    sys.exit(2)

RAW = "https://raw.githubusercontent.com/tiffanidickerson437-lang/compliance-program/main"
CROSSWALK = "02-controls/framework-crosswalk.yaml"
SELECTION = "generated/profile-selection.yaml"
LIBRARY = "02-controls/control-library.yaml"


class CannotCheck(Exception):
    """The check could not run. Always exit 2. Never a pass."""


# ------------------------------------------------------------------ sources --
def read(rel: str, remote: bool, root: Path | None) -> str:
    if remote:
        try:
            req = urllib.request.Request(f"{RAW}/{rel}", headers={"User-Agent": "framework-fidelity"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    raise CannotCheck(f"{rel}: HTTP {r.status}")
                return r.read().decode()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            raise CannotCheck(f"could not fetch {rel}: {e}") from e
    p = (root or Path(".")) / rel
    if not p.is_file():
        raise CannotCheck(f"{p} not found. Set ENGINE_ROOT or pass --remote.")
    return p.read_text()


def load(rel: str, remote: bool, root: Path | None):
    try:
        d = yaml.safe_load(read(rel, remote, root))
    except yaml.YAMLError as e:
        raise CannotCheck(f"{rel} is not valid YAML: {e}") from e
    if d is None:
        raise CannotCheck(f"{rel} parsed to nothing")
    return d


def normalize(s: str) -> str:
    """Slug comparison that survives underscore/hyphen drift between files."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


# -------------------------------------------------------------- granularity --
def granularity(refs: list[str]) -> str:
    """Depth of a reference set: the honest answer about what a mapping can carry.

    enhancement  AC-2(1), A.8.2.3, CC6.1.2  -- assessable at the depth a 3PAO reads
    base         AC-2, A.8.2, CC6.1         -- identifies the control, not the enhancement
    family       AC, GOVERN, A.5            -- identifies the family only
    """
    if not refs:
        return "none"
    depth = set()
    for r in refs:
        r = str(r).strip()
        if re.search(r"\(\d+\)", r) or len(re.findall(r"\.\d+", r)) >= 2:
            depth.add("enhancement")
        elif re.search(r"[-.]\d", r):
            depth.add("base")
        else:
            depth.add("family")
    for level in ("family", "base", "enhancement"):  # report the shallowest present
        if level in depth:
            return level if len(depth) == 1 else f"{level}..{sorted(depth)[-1]}"
    return "unknown"


# ------------------------------------------------------------------- checks --
def audit(crosswalk: dict, selection: dict, library: dict) -> tuple[list[str], dict]:
    """The whole audit, as a pure function. No I/O, so it is testable."""
    reg = crosswalk.get("frameworks")
    if not isinstance(reg, dict) or not reg:
        raise CannotCheck("crosswalk has no 'frameworks' registry -- the schema moved")

    registered = {k: v.get("name", k) for k, v in reg.items()}

    # Join on the framework NAME, not the slug. Both files carry the name, and
    # slugs drift between them (the registry says ccpa_cpra, the selection says
    # ccpa). Joining on slug invents drops that are really spelling. An early
    # version of this checker did exactly that and reported two false findings;
    # a checker that cries wolf gets ignored as fast as one that never fires.
    sel_entries = selection.get("frameworks") or []
    if not isinstance(sel_entries, list) or not sel_entries:
        raise CannotCheck("profile-selection has no 'frameworks' list -- broken parse, not an empty program")
    sel_names = {e.get("name") for e in sel_entries if isinstance(e, dict) and e.get("name")}
    sel_slugs = {e.get("slug") for e in sel_entries if isinstance(e, dict) and e.get("slug")}
    if not sel_names:
        raise CannotCheck("profile-selection frameworks carry no names -- the schema moved")
    sel = sel_slugs

    ctrls = library.get("controls", library)
    ctrls = list(ctrls.values()) if isinstance(ctrls, dict) else ctrls
    if not ctrls:
        raise CannotCheck("control library parsed to zero controls")

    # framework display-name -> refs, gathered across every control
    mapped: dict[str, list[str]] = {}
    for c in ctrls:
        for m in c.get("framework_mappings", []) or []:
            mapped.setdefault(m.get("framework", "?"), []).extend(m.get("references", []) or [])

    sel_names_n = {normalize(n) for n in sel_names}
    findings: list[str] = []

    def mapped_refs_for(name: str) -> list[str] | None:
        """Refs a control library carries for a registered framework, name-joined.

        Registry names are long-form ('ISO/IEC 27001:2022 (controls per ...)')
        while control mappings use the short form ('ISO 27001:2022'). Match on
        the leading token run so the two forms reconcile without hand-maintaining
        an alias table that would rot.
        """
        n = normalize(name)
        for m, refs in mapped.items():
            mn = normalize(m)
            if mn == n or mn.startswith(n[:12]) or n.startswith(mn[:12]):
                return refs
        return None

    # axis 1 -- completeness. The severe one.
    dropped = []
    for slug, name in sorted(registered.items()):
        if normalize(name) not in sel_names_n:
            refs = mapped_refs_for(name)
            dropped.append((slug, name, len(refs) if refs else 0))
    if dropped:
        detail = ", ".join(f"{s} ({n} control refs mapped)" for s, _, n in dropped)
        findings.append(
            f"COMPLETENESS: {len(dropped)} of {len(registered)} registered frameworks are not "
            f"rendered into the profile selection, and the scaffold exits 0 anyway: {detail}. "
            "The mappings exist and the registry declares them -- the renderer drops them in "
            "silence. That is not a missing framework; it is finished work being thrown away by "
            "a step that reports success."
        )

    # axes 2 and 3 -- provenance and declaration.
    # An unmapped registry entry and an unregistered mapping are usually the same
    # defect seen from both sides: the two files spell one framework differently
    # ('EU GDPR' in the registry, 'GDPR' in the library). Reporting that twice
    # inflates the count and trains the reader to discount the list, so pair them
    # first and report a name mismatch once. Only genuinely orphaned entries
    # survive as phantoms.
    reg_names = list(registered.values())
    phantom = [(s, n) for s, n in sorted(registered.items()) if mapped_refs_for(n) is None]
    undeclared = []
    for m in sorted(mapped):
        mn = normalize(m)
        if not any(mn == normalize(r) or mn.startswith(normalize(r)[:12]) or normalize(r).startswith(mn[:12])
                   for r in reg_names):
            undeclared.append(m)

    mismatches, used = [], set()
    for slug, name in phantom:
        for m in undeclared:
            if m in used:
                continue
            # same framework if either name contains the other's distinctive token
            toks = {t for t in re.split(r"[^A-Za-z0-9]+", name) if len(t) > 2}
            if any(t.lower() in m.lower() for t in toks):
                mismatches.append((slug, name, m, len(mapped[m])))
                used.add(m)
                break
    paired_slugs = {x[0] for x in mismatches}

    if mismatches:
        detail = "; ".join(f"{s}: registry says {n!r}, library says {m!r} ({c} refs)"
                           for s, n, m, c in mismatches)
        findings.append(
            f"NAME MISMATCH: {len(mismatches)} framework(s) are spelled differently in the registry "
            f"and the control library, so nothing joins them: {detail}. The mapping work exists on "
            "both sides and neither file is wrong on its own -- they simply do not agree, and every "
            "tool that reconciles them will mis-resolve or invent a gap."
        )

    real_phantom = [f"{s} ({n!r})" for s, n in phantom if s not in paired_slugs]
    if real_phantom:
        findings.append(
            f"PROVENANCE: {len(real_phantom)} registered framework(s) are mapped by no control at "
            f"all: {', '.join(real_phantom)}. A registry entry nobody maps renders an empty profile "
            "that still reports coverage."
        )

    real_undeclared = [f"{m!r} ({len(mapped[m])} refs)" for m in undeclared if m not in used]
    if real_undeclared:
        findings.append(
            f"DECLARATION: {len(real_undeclared)} framework(s) are mapped by controls but not "
            f"registered: {', '.join(real_undeclared)}. Coverage is being computed for a framework "
            "nobody declared."
        )

    # slug drift -- real, minor, and worth naming so it is not mistaken for a drop
    drift = sorted(s for s in registered if s not in sel_slugs and normalize(registered[s]) in sel_names_n)
    if drift:
        findings.append(
            f"SLUG DRIFT: {len(drift)} framework(s) are rendered under a different slug than the "
            f"registry declares: {', '.join(drift)}. Rendered, so not a drop -- but the two files "
            "disagree on the identifier, and anything joining them on slug will invent a finding."
        )

    facts = {
        "registered": registered,
        "selected": sorted(sel_slugs),
        "dropped": [d[0] for d in dropped],
        "dropped_detail": dropped,
        "controls": len(ctrls),
        "granularity": {n: (granularity(r), len(r)) for n, r in sorted(mapped.items())},
        "checked_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    return findings, facts


# ------------------------------------------------------------------ receipt --
def render(findings: list[str], f: dict) -> str:
    ok = not findings
    L = [
        "# Framework fidelity receipt",
        "",
        "Machine-generated by [`tools/framework_fidelity.py`](../tools/framework_fidelity.py). "
        "Do not edit; the next run overwrites it.",
        "",
        f"## {'FAITHFUL' if ok else 'THE SCALING CLAIM DOES NOT HOLD'}",
        "",
        "| | |",
        "|---|---|",
        f"| **Frameworks registered** | {len(f['registered'])} |",
        f"| **Frameworks rendered** | {len(f['selected'])} |",
        f"| **Silently dropped** | {len(f['dropped'])} |",
        f"| **Controls in library** | {f['controls']} |",
        f"| **Findings** | {len(findings)} |",
        f"| **Checked** | {f['checked_at']} |",
        "",
    ]
    if ok:
        L += [
            "Every registered framework is rendered, every registered framework is mapped by at "
            "least one control, and every framework the controls map to is registered. The claim "
            "*one control set, rendered into every framework* is computed here, not asserted.",
            "",
        ]
    else:
        L += ["### Findings", ""] + [f"{i}. {x}" for i, x in enumerate(findings, 1)] + [""]

    L += [
        "### Mapping granularity, per framework",
        "",
        "Reported, never scored. Depth is a fact about the mapping, and the honest answer is what "
        "makes it usable: a framework mapped at **family** granularity is not assessable at the "
        "depth an assessor reads, and a coverage percentage computed over it would be true and "
        "useless at the same time.",
        "",
        "| Framework | Granularity | References |",
        "|---|---|---:|",
    ]
    for name, (g, n) in f["granularity"].items():
        L.append(f"| {name} | {g} | {n} |")

    L += [
        "",
        "---",
        "",
        "### Why this check has no favourite framework",
        "",
        "No framework is named in the logic above. There is no headline framework and no demoted "
        "one -- CMMC, FedRAMP, SOC 2, PCI and whatever ships next are registry entries that must "
        "prove themselves through completeness, provenance and declaration alike. The moment this "
        "check has to special-case a framework, the claim it exists to defend is already dead. "
        "That constraint is the feature.",
        "",
    ]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit the engine's framework scaling claim.")
    ap.add_argument("--remote", action="store_true", help="read public main over https")
    ap.add_argument("--check", action="store_true", help="exit code only; write no receipt")
    ap.add_argument("--out", type=Path, default=Path("generated/framework-fidelity-receipt.md"))
    args = ap.parse_args()

    root = Path(os.environ["ENGINE_ROOT"]) if os.environ.get("ENGINE_ROOT") else None
    try:
        findings, facts = audit(
            load(CROSSWALK, args.remote, root),
            load(SELECTION, args.remote, root),
            load(LIBRARY, args.remote, root),
        )
    except CannotCheck as e:
        print(f"FAIL[2] could not check: {e}", file=sys.stderr)
        print("Failing closed. A checker that cannot check does not report a pass.", file=sys.stderr)
        return 2

    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(render(findings, facts))
        print(f"receipt -> {args.out}")

    print(f"{len(facts['registered'])} registered, {len(facts['selected'])} rendered, "
          f"{len(facts['dropped'])} dropped")

    if findings:
        print(f"\nSCALING CLAIM FAILS: {len(findings)} finding(s)", file=sys.stderr)
        for i, x in enumerate(findings, 1):
            print(f"  {i}. {x}", file=sys.stderr)
        return 1

    print("\nFAITHFUL: every registered framework is rendered, mapped, and declared.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
