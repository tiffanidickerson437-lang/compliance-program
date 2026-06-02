#!/usr/bin/env python3
"""
draft_framework_mapping.py — onboard ANY framework as a mapping over the owned control set.

This is the engine behind "scales to any framework." Adding a framework means drafting a
mapping from its requirements to controls we ALREADY OWN — never rewriting controls. A new
regulation, a customer's bespoke questionnaire, an emerging AI standard: same move.

Flow:
  1. Load the owned control library (owned-controls.yaml) — the single source of truth.
  2. Load the target framework's requirements.
  3. AI-DRAFT STEP: per requirement, propose which owned controls satisfy it and the
     set-theory relationship. In production this is an LLM call; here a transparent keyword
     heuristic stands in so the pipeline runs offline and deterministically.
  4. Emit a DRAFT mapping. A human reviews and approves via pull request — the merge is the
     authorization. Nothing is auto-accepted; the control catalog is never modified.

Usage:
  python3 tools/draft_framework_mapping.py --framework frameworks/iso-42001.requirements.yaml
"""
import argparse, os, re, yaml
from pathlib import Path

STOP = set("the a an of to and or for in on with is are be shall should which that this its by "
           "as at from into used use within throughout across their them they not no".split())


def tokens(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in STOP and len(w) > 2}


def ai_draft_match(req, controls):
    """STAND-IN for the AI mapping step — replace with an LLM call in production.

    Returns up to 3 candidate owned controls ranked by semantic overlap with the requirement.
    """
    rt = tokens(req["title"]) | tokens(req["text"])
    scored = []
    for c in controls:
        ct = tokens(c["title"]) | tokens(c.get("statement", "")) | tokens(c["domain"])
        overlap = rt & ct
        if not overlap:
            continue
        score = len(overlap) / ((len(rt) ** 0.5) or 1)
        scored.append((score, c["id"], sorted(overlap)))
    scored.sort(reverse=True)
    return scored[:3]


def rel_for(score):
    return "subset-of" if score >= 2.2 else "intersects-with"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", required=True, help="path to a framework requirements YAML")
    ap.add_argument("--catalog", default=str(Path(__file__).resolve().parent.parent / "02-controls" / "owned-controls.yaml"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    controls = yaml.safe_load(open(a.catalog, encoding="utf-8"))["controls"]
    fw = yaml.safe_load(open(a.framework, encoding="utf-8"))
    fwid, fwname = fw["framework"]["id"], fw["framework"]["name"]

    drafted = []
    for req in fw["requirements"]:
        cands = ai_draft_match(req, controls)
        entries = [{"control": cid, "relationship": rel_for(sc),
                    "confidence": round(min(sc / 3, 0.99), 2), "matched_on": ov}
                   for sc, cid, ov in cands]
        drafted.append({"requirement": req["id"], "requirement_title": req["title"],
                        "candidates": entries or [{"control": None,
                                                   "note": "no candidate — author a new control or map manually"}]})

    out = a.out or str(Path(a.framework).resolve().parent.parent / "mappings" / f"{fwid}.draft.yaml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    yaml.safe_dump({"mapping": {
        "framework": fwid, "framework_name": fwname,
        "status": "DRAFT_PENDING_HUMAN_APPROVAL",
        "method": "AI-drafted (keyword heuristic stand-in for an LLM); review and approve via pull request — the merge is the authorization",
        "controls_in_catalog": len(controls), "controls_modified": 0,
        "entries": drafted,
    }}, open(out, "w", encoding="utf-8"), sort_keys=False, allow_unicode=True, width=100)

    covered = sum(1 for d in drafted if d["candidates"][0].get("control"))
    print(f"Framework onboarded as a mapping: {fwname}")
    print(f"Requirements: {len(drafted)}   drafted with >=1 candidate: {covered}/{len(drafted)}")
    print(f"Controls in catalog: {len(controls)}   controls modified: 0   <-- scales to any framework")
    print(f"Draft written: {out}")
    print("Status: DRAFT — a human reviews and approves via pull request (the human gate).\n")
    for d in drafted:
        top = d["candidates"][0]
        cid = top.get("control")
        line = f"   {d['requirement']:8s} {d['requirement_title'][:34]:34s} -> "
        line += f"{cid:8s} [{top['relationship']}, conf {top['confidence']}]" if cid else "(needs new control)"
        print(line)


if __name__ == "__main__":
    main()
