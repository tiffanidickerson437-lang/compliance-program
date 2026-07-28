#!/usr/bin/env python3
"""Tests that the fidelity checker catches what it claims to catch.

Belongs at tests/test_framework_fidelity.py on engine main.

The first version of this checker reported two findings that were not real: it
joined the registry to the profile selection on slug, and slugs drift between
those files, so it invented drops out of spelling. It also reported one name
mismatch twice, once from each side. Both bugs made the output louder and less
true, which is the failure mode that gets a checker ignored.

So the control test here matters as much as the mutation tests: a clean engine
must produce zero findings. A checker that always fires is discarded exactly as
fast as one that never does.

    python3 tests/test_framework_fidelity.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# The checker lives in tools/ on the engine; this test lives in tests/. Import
# it from tools/ (the staged patch co-located the two files; on main they split).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from framework_fidelity import audit, granularity  # noqa: E402

R: list[tuple[bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    R.append((cond, name if cond else f"{name} -- {detail}"))


def fires(findings, token):
    return any(token in f for f in findings)


# A clean miniature engine: 2 frameworks, registered, rendered, mapped, agreeing.
def cw(frameworks):
    return {"frameworks": frameworks}


def sel(entries):
    return {"frameworks": entries}


def lib(mappings):
    return {"controls": [{"id": "X-01", "framework_mappings": mappings}]}


CLEAN_CW = cw({
    "soc2": {"name": "SOC 2 (TSC 2017)"},
    "pci": {"name": "PCI DSS v4"},
})
CLEAN_SEL = sel([
    {"slug": "soc2", "name": "SOC 2 (TSC 2017)"},
    {"slug": "pci", "name": "PCI DSS v4"},
])
CLEAN_LIB = lib([
    {"framework": "SOC 2 (TSC 2017)", "references": ["CC6.1", "CC6.2"]},
    {"framework": "PCI DSS v4", "references": ["1.2.1"]},
])

# == the control: a faithful engine must be silent =========================
f, _ = audit(CLEAN_CW, CLEAN_SEL, CLEAN_LIB)
check("a faithful engine produces zero findings", f == [], f"got {f}")

# == the severe one: registered, mapped, not rendered ======================
f, facts = audit(CLEAN_CW, sel([{"slug": "soc2", "name": "SOC 2 (TSC 2017)"}]), CLEAN_LIB)
check("catches a registered+mapped framework the renderer drops",
      fires(f, "COMPLETENESS") and fires(f, "pci"), f"got {f}")
check("reports how much mapped work the drop discards",
      "1 control refs mapped" in " ".join(f), f"got {f}")

# == phantom: registered, rendered, mapped by nobody =======================
f, _ = audit(
    cw({"soc2": {"name": "SOC 2 (TSC 2017)"}, "hipaa": {"name": "HIPAA Security Rule"}}),
    sel([{"slug": "soc2", "name": "SOC 2 (TSC 2017)"},
         {"slug": "hipaa", "name": "HIPAA Security Rule"}]),
    lib([{"framework": "SOC 2 (TSC 2017)", "references": ["CC6.1"]}]),
)
check("catches a registry entry no control maps", fires(f, "PROVENANCE"), f"got {f}")

# == undeclared: mapped by controls, registered by nobody ==================
f, _ = audit(
    cw({"soc2": {"name": "SOC 2 (TSC 2017)"}}),
    CLEAN_SEL,
    lib([{"framework": "SOC 2 (TSC 2017)", "references": ["CC6.1"]},
         {"framework": "FedRAMP Rev5", "references": ["AC-2"]}]),
)
check("catches a framework mapped but never registered", fires(f, "DECLARATION"), f"got {f}")

# == name mismatch reported ONCE, not once per side =======================
f, _ = audit(
    cw({"gdpr": {"name": "EU GDPR"}}),
    sel([{"slug": "gdpr", "name": "EU GDPR"}]),
    lib([{"framework": "GDPR", "references": ["Art.32"]}]),
)
check("a name mismatch fires NAME MISMATCH", fires(f, "NAME MISMATCH"), f"got {f}")
check("a name mismatch is one finding, not two",
      len(f) == 1 and not fires(f, "PROVENANCE") and not fires(f, "DECLARATION"), f"got {f}")

# == slug drift is not a drop =============================================
f, _ = audit(
    cw({"ccpa_cpra": {"name": "CCPA / CPRA (2026)"}}),
    sel([{"slug": "ccpa", "name": "CCPA / CPRA (2026)"}]),
    lib([{"framework": "CCPA / CPRA (2026)", "references": ["1798.100"]}]),
)
check("slug drift fires SLUG DRIFT, not COMPLETENESS",
      fires(f, "SLUG DRIFT") and not fires(f, "COMPLETENESS"), f"got {f}")

# == fail closed ==========================================================
for name, args in [
    ("no registry", ({}, CLEAN_SEL, CLEAN_LIB)),
    ("empty selection", (CLEAN_CW, {"frameworks": []}, CLEAN_LIB)),
    ("empty library", (CLEAN_CW, CLEAN_SEL, {"controls": []})),
]:
    try:
        audit(*args)
        check(f"refuses to check with {name}", False, "returned a verdict anyway")
    except Exception:
        check(f"refuses to check with {name}", True)

# == the checker names no framework: swap them all and behaviour is identical ==
# This is the scaling claim as a test. If renaming every framework changed the
# verdict, the logic would have a favourite -- and a checker with a favourite
# framework cannot defend a claim about all of them.
SWAP_CW = cw({"a": {"name": "Framework Alpha"}, "b": {"name": "Framework Beta"}})
SWAP_SEL = sel([{"slug": "a", "name": "Framework Alpha"}])
SWAP_LIB = lib([{"framework": "Framework Alpha", "references": ["1.1"]},
                {"framework": "Framework Beta", "references": ["2.2"]}])
f_real, _ = audit(CLEAN_CW, sel([{"slug": "soc2", "name": "SOC 2 (TSC 2017)"}]), CLEAN_LIB)
f_swap, _ = audit(SWAP_CW, SWAP_SEL, SWAP_LIB)
check("verdict is identical for invented frameworks (no favourites)",
      len(f_real) == len(f_swap) and fires(f_swap, "COMPLETENESS"), f"real={f_real} swap={f_swap}")

# == granularity is reported honestly =====================================
check("enhancement depth detected", granularity(["AC-2(1)"]) == "enhancement", granularity(["AC-2(1)"]))
check("base depth detected", granularity(["AC-2"]) == "base", granularity(["AC-2"]))
check("family depth detected", granularity(["GOVERN"]) == "family", granularity(["GOVERN"]))


if __name__ == "__main__":
    passed = sum(1 for ok, _ in R if ok)
    for ok, name in R:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{passed}/{len(R)} tests passed")
    if passed != len(R):
        print("\nThe fidelity checker does not check fidelity. Failing closed.", file=sys.stderr)
        sys.exit(1)
    print("The checker fires on real defects, stays silent on a clean engine, and has no favourite framework.")
