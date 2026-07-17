#!/usr/bin/env python3
"""onboard_company.py — render a company-tailored data.json for the portfolio site.

Takes a company config (the config.example.yaml shape), filters the engine's
control library and crosswalk to that company's frameworks, and emits the
`window.GRC`-shaped JSON the React/Next site consumes — one standalone payload
per company.

The boundary is the same one draft_narrative.py enforces: EVIDENCE IS COMPUTED,
never AI-authored. Every evidence record carries ai_generated: false, and this
tool refuses to emit one that does not. AI may draft narrative prose (the pillar
"why", the control "why"); it never authors an evidence value.

    ENGINE_ROOT=/path/to/compliance-program \\
    python3 tools/onboard_company.py --config companies/1password.config.yaml --slug 1password --dry-run

Output: generated/companies/<slug>/data.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    raise SystemExit(2)

# Engine repo root (where control-library.yaml lives). When this file is copied
# into the engine repo's tools/, the default resolves correctly; from staging,
# set ENGINE_ROOT explicitly.
ENGINE_ROOT = Path(os.environ.get("ENGINE_ROOT") or Path(__file__).resolve().parent.parent)
OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT") or ENGINE_ROOT)
REPO_SLUG = "tiffanidickerson437-lang/compliance-program"

# ---- Framework registry: fw_id -> display. Mirrors data.js. ----
FRAMEWORKS = {
    "soc2":        {"name": "SOC 2",       "full": "SOC 2 (TSC 2017)",           "kind": "primary"},
    "iso27001":    {"name": "ISO 27001",   "full": "ISO/IEC 27001:2022",         "kind": "primary"},
    "iso27017":    {"name": "ISO 27017",   "full": "ISO/IEC 27017:2015",         "kind": "cloud"},
    "iso27018":    {"name": "ISO 27018",   "full": "ISO/IEC 27018:2019",         "kind": "cloud"},
    "iso27701":    {"name": "ISO 27701",   "full": "ISO/IEC 27701:2019",         "kind": "privacy"},
    "iso42001":    {"name": "ISO 42001",   "full": "ISO/IEC 42001:2023",         "kind": "ai"},
    "nist_ai_rmf": {"name": "NIST AI RMF", "full": "NIST AI RMF 1.0",            "kind": "ai"},
    "nist_csf":    {"name": "NIST CSF",    "full": "NIST CSF 2.0",               "kind": "core"},
    "nist_800_53": {"name": "NIST 800-53", "full": "NIST SP 800-53 Rev.5",       "kind": "core"},
    "nist_800_171": {"name": "NIST 800-171", "full": "NIST SP 800-171 Rev 2",     "kind": "gov"},
    "coppa":       {"name": "COPPA",       "full": "COPPA (amended 2025)",       "kind": "privacy"},
    "ccpa_cpra":   {"name": "CCPA / CPRA", "full": "CCPA / CPRA",                "kind": "privacy"},
    "gdpr":        {"name": "GDPR",        "full": "EU GDPR",                    "kind": "privacy"},
    "eu_ai_act":   {"name": "EU AI Act",   "full": "EU AI Act (2024)",           "kind": "ai"},
    "pci_dss":     {"name": "PCI DSS",     "full": "PCI DSS v4.0",               "kind": "financial"},
    "csa_star":    {"name": "CSA STAR",    "full": "CSA STAR",                   "kind": "cloud"},
    "tx_ramp":     {"name": "TX-RAMP",     "full": "TX-RAMP",                    "kind": "gov"},
}

# Normalize a config/library framework token to a registry fw_id.
def fw_id(token: str) -> str:
    t = (token or "").strip().lower()
    t = t.replace(" ", "-").replace("/", "-").replace(".", "-")
    table = {
        "soc-2": "soc2", "soc2": "soc2",
        "iso-27001": "iso27001", "iso27001": "iso27001", "iso-iec-27001-2022": "iso27001",
        "iso-27002": "iso27001", "iso27002": "iso27001", "iso-iec-27002-2022": "iso27001",
        "iso-27017": "iso27017", "iso27017": "iso27017",
        "iso-27018": "iso27018", "iso27018": "iso27018",
        "iso-27701": "iso27701", "iso27701": "iso27701",
        "iso-42001": "iso42001", "iso42001": "iso42001", "iso-iec-42001-2023": "iso42001",
        "nist-ai-rmf": "nist_ai_rmf", "nist-ai-rmf-1-0": "nist_ai_rmf",
        "nist-csf": "nist_csf", "nist-csf-2-0": "nist_csf",
        "nist-800-53": "nist_800_53", "nist-sp-800-53": "nist_800_53",
        "nist-800-171": "nist_800_171", "nist-sp-800-171": "nist_800_171",
        "coppa": "coppa",
        "ccpa": "ccpa_cpra", "cpra": "ccpa_cpra", "ccpa-cpra": "ccpa_cpra",
        "gdpr": "gdpr",
        "eu-ai-act": "eu_ai_act",
        "pci-dss": "pci_dss", "pci": "pci_dss",
        "csa-star": "csa_star",
        "tx-ramp": "tx_ramp",
    }
    if t in table:
        return table[t]
    # substring fallback for control-library full names ("NIST AI RMF 1.0")
    for key, fid in (
        ("ai rmf", "nist_ai_rmf"), ("42001", "iso42001"), ("27002", "iso27001"), ("27001", "iso27001"),
        ("soc 2", "soc2"), ("soc2", "soc2"), ("eu ai act", "eu_ai_act"),
        ("coppa", "coppa"), ("ccpa", "ccpa_cpra"), ("cpra", "ccpa_cpra"),
        ("csf", "nist_csf"), ("800-171", "nist_800_171"), ("800-53", "nist_800_53"),
        ("gdpr", "gdpr"), ("27017", "iso27017"), ("27018", "iso27018"),
        ("27701", "iso27701"), ("pci", "pci_dss"),
    ):
        if key in (token or "").lower():
            return fid
    return t.replace("-", "_")

# ---- The 8 pillars (neutral structure; engine dirs + files). ----
PILLARS = [
    {"id": "00", "dir": "00-governance", "name": "Governance",
     "what": "Who owns the program and where authority sits.",
     "reads": "Board · Audit & Risk · Internal Audit",
     "files": [["program-charter.md", "Purpose, scope, authority, operating model."],
               ["policy-hierarchy.yaml", "Every policy, its owner, cadence, version."],
               ["roles-and-responsibilities.md", "RACI by function and by activity."],
               ["risk-appetite-statement.md", "Appetite by category — owned by the business."],
               ["committee-charter.md", "Security Steering Committee cadence."]]},
    {"id": "01", "dir": "01-risk-management", "name": "Risk management",
     "what": "Risk quantified in dollars, owned by the business.",
     "reads": "C-Suite · Board · GRC",
     "files": [["risk-register.yaml", "FAIR scenarios, highest-leverage risks first."],
               ["fair-model.md", "How quantification is applied, with a worked example."],
               ["nist-rmf-alignment.md", "How the register feeds the seven RMF steps."],
               ["risk-treatment-templates.md", "Accept, mitigate, transfer, avoid."]]},
    {"id": "02", "dir": "02-controls", "name": "Controls", "hero": True,
     "what": "The engine. One control defined once; every framework gets its view.",
     "reads": "Auditors · Security · Engineering",
     "files": [["control-library.yaml", "Controls in full depth — statement, guidance, evidence schema."],
               ["framework-crosswalk.yaml", "One control, every framework it satisfies."],
               ["control-library.oscal.json", "The machine-readable, OSCAL-aligned catalog."],
               ["profiles/", "OSCAL profiles — one per framework view."],
               ["evidence-schemas/", "Field-level schema per control; evidence is computed."]]},
    {"id": "03", "dir": "03-tprm", "name": "Third-party risk",
     "what": "Right-size diligence to what a vendor can actually touch.",
     "reads": "GRC · Legal/Privacy · Procurement",
     "files": [["vendor-tiering-model.md", "Tier by data access, not by vendor size."],
               ["tiered-intake-workflow.md", "Intake routes to the right depth of review."],
               ["attestation-reuse-register.yaml", "Reuse a current SOC 2 / ISO cert."],
               ["continuous-monitoring.md", "Reassess high-risk parties on cadence and change."]]},
    {"id": "04", "dir": "04-ai-governance", "name": "AI governance", "hero": True,
     "what": "Govern autonomous agents on sensitive data.",
     "reads": "Security · Legal/Privacy · Board · Customers",
     "files": [["ai-control-set.md", "AAT-01 as the spine, decomposed into sub-controls."],
               ["agent-governance.md", "Agent identity, purpose-bound tokens, human gate, kill-switch."],
               ["owasp-llm-top10-mapping.md", "Each OWASP LLM Top 10 item → control → test."],
               ["responsible-ai-statement.md", "Customer-facing claims, each traced to a control."]]},
    {"id": "05", "dir": "05-secure-development", "name": "Secure development",
     "what": "Security in the SDLC as gates that produce evidence as a byproduct of shipping.",
     "reads": "Engineering · Security",
     "files": [["sdlc-control-gates.md", "Where security gates sit in the pipeline."],
               ["code-review-policy.md", "Independent review, enforced by code-owner rules."],
               ["secure-pipeline.md", "Build/test/security checks as required status checks."]]},
    {"id": "06", "dir": "06-evidence-and-audit", "name": "Evidence and audit",
     "what": "Evidence pre-validated before it ever reaches the auditor.",
     "reads": "Auditors · GRC",
     "files": [["evidence-architecture.md", "How evidence is computed from systems of record."],
               ["continuous-evidence.md", "Readiness as a standing state, not a sprint."],
               ["poam-as-issues.md", "Plan of action & milestones, tracked as GitHub Issues."],
               ["trust-center-content.md", "What goes in the public trust center."]]},
    {"id": "07", "dir": "07-stakeholder-management", "name": "Stakeholder management",
     "what": "One posture, every audience.",
     "reads": "Sales · Board · Customers · Every function",
     "files": [["stakeholder-map.yaml", "Every audience, what they need, how they read it."],
               ["sales-faq.yaml", "The security questions deals actually ask."],
               ["trust-collateral.md", "Reusable trust artifacts that shorten reviews."]]},
]

ROOT_FILES = [
    {"name": "README.md", "note": "The program of record. Start here."},
    {"name": "config.example.yaml", "note": "The single input. One file customizes the entire program.", "config": True},
    {"name": "config.yaml", "note": "Your copy of the example, with real values."},
    {"name": "30-60-90/", "note": "Discover → Design → Operate, plus the maturity roadmap.", "folder": True},
    {"name": ".github/workflows/", "note": "Drift monitor, evidence validator, report generator.", "folder": True},
]

# The operating-model flow is the same for every company.
FLOW = [
    {"key": "config", "label": "company.yaml", "kind": "input", "title": "One config file",
     "body": "Frameworks, data types, AI posture, listings, stack. Edit this one file and re-run the scaffold — the whole program re-renders. Adding a framework is a crosswalk mapping, never a new control.", "tag": "the single input"},
    {"key": "scaffold", "label": "GitHub Action", "kind": "machine", "title": "The scaffold renders",
     "body": "An Action filters the control library to the company's frameworks and turns on the pillars and families the config requires.", "tag": "code, not a binder"},
    {"key": "checks", "label": "Daily checks", "kind": "machine", "title": "Control health is computed",
     "body": "Scheduled jobs read the systems of record and compute pass or fail for each control. Code decides; the system of record supplies the evidence.", "tag": "evidence is computed"},
    {"key": "branch", "label": "healthy / drift", "kind": "branch", "title": "Green, or a drift Issue",
     "body": "Healthy → status stays green and evidence is recorded. Drift → a GitHub Issue opens automatically with the control ID, owner, framework impact, and evidence needed.", "tag": "the Issue IS the due diligence"},
    {"key": "ai", "label": "AI drafts", "kind": "ai", "title": "AI drafts the fix and the narrative",
     "body": "AI proposes the remediation and writes the auditor-facing narrative and gap analysis. It never authors evidence; evidence is computed from systems of record and rejected by schema if model-generated.", "tag": "leverage, not authority"},
    {"key": "pr", "label": "Pull Request", "kind": "human", "title": "A human gate: the Pull Request",
     "body": "A named function reviews the AI-drafted remediation. The merge is the authorization. Nothing becomes record without a human approving it first.", "tag": "the human gate"},
    {"key": "trail", "label": "git history", "kind": "record", "title": "Git history is the audit trail",
     "body": "On merge, the control status updates and the commit records who decided what, when, and why. The trail is immutable and already exists — audit prep is a query, not a reconstruction.", "tag": "the immutable trail"},
]

ROADMAP = [
    {"months": "1–2", "level": "Baseline", "stage": "Discover",
     "ships": "Control inventory, regulatory obligation register, a data-flow map, and a map of where compliance slows engineering.",
     "boundary": "One validated baseline exists — control universe, obligations, data flows, and friction points are known and agreed."},
    {"months": "2–5", "level": "Defined", "stage": "Common-control spine",
     "ships": "One owned control library crosswalked to the in-scope frameworks, the OSCAL profiles that resolve each view, and the first collect-once evidence pipelines.",
     "boundary": "Every in-scope control is defined once, crosswalked, owned by a named function, and assigned an evidence source."},
    {"months": "5–9", "level": "Managed", "stage": "Computed continuous evidence",
     "ships": "Continuous control monitoring with exception aging and the drift-opens-an-Issue loop.",
     "boundary": "Control health is computed continuously from systems of record rather than reconstructed at audit."},
    {"months": "9–15", "level": "Quantitatively managed", "stage": "Agentic AI governance",
     "ships": "An AI control set grounded in ISO 42001 and NIST AI RMF: model inventory, data-use boundaries, agent-action logging, human gates, a kill-switch, and a customer-facing AI trust statement.",
     "boundary": "The agentic layer operates inside live, measured guardrails; every agent decision is logged and reviewable."},
    {"months": "15+", "level": "Optimizing", "stage": "Risk-driven, revenue-enabling",
     "ships": "A live risk register that prioritizes hardening by leverage, and trust artifacts that shorten enterprise security reviews.",
     "boundary": "Ongoing. Risk leverage, not the audit calendar, sets the backlog."},
]

# Generic AI-expedited 30/60/90 used when a company has no value.json overlay.
DEFAULT_3060_90 = [
    {"window": "0–30", "theme": "Baseline the control surface",
     "milestones": ["Inventory the control universe and regulatory obligation register.",
                    "Map the in-scope frameworks to the existing control library.",
                    "Stand up the repo as system of record; confirm the GRC-tool sink.",
                    "Data-flow map; pinpoint where compliance slows engineering."],
     "aiAccelerates": "AI drafts the control-to-framework crosswalk and the baseline narrative in an afternoon vs ~2 weeks by hand; the inventory stays computed from systems of record."},
    {"window": "30–60", "theme": "Computed continuous evidence",
     "milestones": ["Wire daily checks so control health is computed, not reconstructed.",
                    "Turn on the drift-opens-an-Issue loop.",
                    "Ship the priority control's audit-ready evidence, crosswalked to every in-scope framework.",
                    "Route exceptions to the GRC sink with control ID, owner, and framework impact."],
     "aiAccelerates": "AI drafts the auditor narratives and the crosswalk in an afternoon vs ~3 weeks; evidence stays deterministically computed and is schema-rejected if model-generated."},
    {"window": "60–90", "theme": "Audit-ready and the trust story",
     "milestones": ["Run a gap assessment for the next target framework off existing mappings.",
                    "Publish trust-center collateral and reusable security-questionnaire answers.",
                    "Extend incident response to AI-agent-scope incidents.",
                    "Hand leadership a resourced readiness view by framework."],
     "aiAccelerates": "AI drafts the gap workpapers, crosswalk, and first trust collateral in days vs ~4 weeks, with a named function approving before anything becomes record."},
]


def load_value(config_path: str, slug: str) -> dict:
    """Per-company VALUE overlay (friction points, real 30/60/90, collateral)."""
    p = Path(config_path).parent / slug / "value.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


ENVELOPE = {"control", "period", "source", "ai_generated", "lawful_basis", "human_gate"}


def load_yaml(path: Path) -> dict:
    with path.open() as fh:
        return yaml.safe_load(fh)


def flatten_frameworks(cfg: dict) -> list[str]:
    fw = cfg.get("frameworks", {}) or {}
    out: list[str] = []
    for bucket in ("primary", "emerging", "financial"):
        for t in (fw.get(bucket) or []):
            fid = fw_id(t)
            if fid not in out:
                out.append(fid)
    return out


def build_company(cfg: dict, in_scope: list[str], slug: str) -> dict:
    c = cfg.get("company", {}) or {}
    topics = [slug, "grc", "compliance-as-code", "ai-governance"]
    for fid in in_scope:
        nm = fid.replace("_", "-")
        if nm not in topics:
            topics.append(nm)
    return {
        "name": c.get("name", slug),
        "legal": c.get("legal_entity", c.get("name", slug)),
        "repo": REPO_SLUG,
        "listings": c.get("listings", []) or [],
        "description": " ".join((c.get("description", "") or "").split()),
        "topics": topics[:12],
    }


def build_frameworks(in_scope: list[str]) -> list[dict]:
    out = []
    for fid in in_scope:
        meta = FRAMEWORKS.get(fid, {"name": fid, "full": fid, "kind": "other"})
        out.append({"id": fid, "name": meta["name"], "full": meta["full"], "kind": meta["kind"]})
    return out


# The engine's control narratives are written in the example archetype (precise
# location, minors). For a company whose data types don't match that archetype,
# re-contextualize the prose so no foreign-archetype language leaks in.
def company_context(cfg: dict) -> tuple[str, str]:
    surface = ((cfg.get("ai", {}) or {}).get("product_surface", "") or "").replace("-", " ").strip()
    surface = surface or "its production systems"
    dt = set(cfg.get("data-types", []) or [])
    nouns = []
    if "credentials-and-secrets" in dt: nouns.append("credentials and secrets")
    if "pii" in dt: nouns.append("personal data")
    if "enterprise-customer-data" in dt: nouns.append("customer data")
    if "precise-location" in dt: nouns.append("precise location")
    if "minors" in dt: nouns.append("minors' data")
    sensitive = ", ".join(nouns) if nouns else "sensitive data"
    return surface, sensitive


WHY_BY_FAMILY = {
    "ai": "{name} operates an agentic layer over its {surface}. Autonomous systems that hold privileged access need a control for identity, least privilege, decision logging, and a human gate on high-impact actions — the hero control.",
    "access": "Periodic access review is the access pillar of {pillar}, the control auditors test first. It limits standing access to {sensitive}.",
    "change": "Change control is a pillar of {pillar}. In a source-control-native program the pull request is the gate, and the evidence is a byproduct of shipping rather than reconstructed for an audit.",
    "monitor": "Continuous monitoring turns a point-in-time audit into a standing program. It is the engine of the drift-opens-an-Issue loop that makes due diligence visible.",
    "third": "Sensitive data flows to subprocessors and model providers. Diligence depth must match what a party can touch across {surface}, and trust evidence a vendor already produced should be reused, not re-collected.",
    "incident": "When an agent exceeds its scope or a breach clock starts, the response has to be rehearsed and the timeline defensible — including incidents that involve autonomous-agent scope on {sensitive}.",
    "privacy": "Regulated personal data is processed only on a lawful basis, with the data subject's rights honored end to end across {surface}.",
}


def _fam_key(fam: str):
    f = (fam or "").lower()
    if "ai" in f or "autonomous" in f: return "ai"
    if "access" in f: return "access"
    if "change" in f: return "change"
    if "monitor" in f: return "monitor"
    if "third" in f or "vendor" in f or "supplier" in f: return "third"
    if "incident" in f: return "incident"
    if "privacy" in f or "consent" in f: return "privacy"
    return None

_SUBS = [
    ("precise location or minor data", "{sensitive}"),
    ("precise location and minor data", "{sensitive}"),
    ("minor personal data", "regulated data"),
    ("minor data", "regulated data"),
    ("real-time location graph", "{surface}"),
    ("location graph", "{surface}"),
    ("family graph", "{surface}"),
    (", including children", ""),
    (" including children", ""),
    ("including minors", ""),
    ("precise location", "{sensitive}"),
    ("minors", "regulated data subjects"),
    ("children", "regulated data subjects"),
    ("tens of millions of members", "its user base"),
]


def why_for(control: dict, surface: str, sensitive: str, name: str) -> str:
    pillar = "identity and operations governance"
    key = _fam_key(control.get("family", ""))
    tmpl = WHY_BY_FAMILY.get(key) if key else None
    if not tmpl:
        return f"{control.get('title','')} — defined once and rendered into every in-scope framework's view."
    return tmpl.format(name=name, surface=surface, sensitive=sensitive, pillar=pillar)


def substitute_archetype(text: str, surface: str, sensitive: str) -> str:
    import re as _re
    for needle, repl in _SUBS:
        text = _re.sub(_re.escape(needle), repl.format(surface=surface, sensitive=sensitive), text, flags=_re.I)
    return " ".join(text.split())


def build_controls(cfg: dict, in_scope: list[str]) -> list[dict]:
    lib = load_yaml(ENGINE_ROOT / "02-controls" / "control-library.yaml")
    data_types = set(cfg.get("data-types", []) or [])
    emphasis = cfg.get("emphasis", {}) or {}
    hero_control = emphasis.get("hero_control")
    in_scope_set = set(in_scope)
    # Use the engine's narratives verbatim only when the company matches the
    # example archetype (precise location + minors); otherwise re-contextualize.
    archetype = ("precise-location" in data_types) and ("minors" in data_types)
    surface, sensitive = company_context(cfg)
    name = cfg.get("company", {}).get("name", "the organization")
    out = []
    for c in lib.get("controls", []):
        cid = c.get("id")
        # Drop the minors-consent control unless the company processes minors' data.
        if cid == "PRI-03.13" and "minors" not in data_types:
            continue
        # Filter framework mappings to in-scope frameworks.
        crosswalk = []
        for m in (c.get("framework_mappings") or []):
            fid = fw_id(m.get("framework", ""))
            if fid in in_scope_set:
                crosswalk.append({"fw": fid, "refs": m.get("references", []) or []})
        if not crosswalk:
            continue  # control not in scope for any of this company's frameworks
        # Evidence — computed only; the boundary is enforced when sample evidence
        # is present. Controls without committed example_evidence simply render no
        # sample rows (the boundary still forbids AI-authored evidence when present).
        ev = c.get("example_evidence", {}) or {}
        if ev and ev.get("ai_generated") is not False:
            raise SystemExit(
                f"refusing to emit {cid}: example_evidence.ai_generated must be false "
                f"(evidence is computed, never AI-authored)."
            )
        rows = [[k, str(v)] for k, v in ev.items() if k not in ENVELOPE and not isinstance(v, (dict, list))]
        out.append({
            "id": cid,
            "family": c.get("family", ""),
            "title": c.get("title", ""),
            "owner": c.get("owner", ""),
            "automation": c.get("automation", "partial"),
            "hero": (cid == hero_control) or (cid == "AAT-01"),
            "why": (" ".join((c.get("why", "") or "").split()) if archetype
                    else why_for(c, surface, sensitive, name)),
            "statement": (" ".join((c.get("statement", "") or "").split()) if archetype
                          else substitute_archetype(" ".join((c.get("statement", "") or "").split()), surface, sensitive)),
            "crosswalk": crosswalk,
            "evidence": {"source": ev.get("source", "system of record"), "rows": rows},
        })
    return out


def build_stack(cfg: dict) -> list[dict]:
    stack = cfg.get("stack", {}) or {}
    role = {
        "cloud": "cloud — evidence source for access, change, ops",
        "identity": "identity — drives access-review evidence",
        "code": "code — the operating model lives here; change evidence is the merge",
        "ticketing": "ticketing — the remediation work order",
        "docs": "docs — stakeholder reports render here after review",
        "comms": "comms — drift, TPRM, and deadline notifications route here",
        "grc-tool": "GRC tool — the audit-facing interface; this repo stays the system of record",
    }
    out = []
    for key, items in stack.items():
        for name in (items or []):
            out.append({"name": str(name), "role": role.get(key, key)})
    return out


def build_guardrails(cfg: dict) -> list[str]:
    name = cfg.get("company", {}).get("name", "this organization")
    g = [
        f"Built from public research only. No claim is made about {name}'s internal security posture.",
        "AI drafts narratives and remediations; a human approves before anything becomes record. Evidence is computed from systems of record, never authored by a model.",
        "Functions and roles are named — never individuals. Accountability attaches to a function.",
    ]
    return g


def build_stats(num_controls: int, num_frameworks: int) -> list[dict]:
    return [
        {"n": "1", "label": "config file", "sub": "company.yaml drives everything"},
        {"n": str(num_controls), "label": "controls", "sub": "defined once, rendered per framework"},
        {"n": str(num_frameworks), "label": "frameworks", "sub": "one control set, every view"},
        {"n": "8", "label": "pillars", "sub": "governance to stakeholders"},
    ]


def build_pillars(cfg: dict) -> list[dict]:
    name = cfg.get("company", {}).get("name", "the organization")
    emphasis = cfg.get("emphasis", {}) or {}
    hero_dir = emphasis.get("hero_pillar")
    out = []
    for p in PILLARS:
        why = f"How {name}'s program handles {p['name'].lower()} — defined once and rendered into every framework's view."
        out.append({
            "id": p["id"], "dir": p["dir"], "name": p["name"], "what": p["what"],
            "why": why, "reads": p["reads"],
            "hero": bool(p.get("hero")) or (p["dir"] == hero_dir),
            "files": [{"name": n, "note": nt} for n, nt in p["files"]],
        })
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True, help="path to a company .config.yaml")
    ap.add_argument("--slug", required=True, help="company slug, e.g. 1password")
    ap.add_argument("--dry-run", action="store_true", help="print a summary instead of only writing")
    args = ap.parse_args(argv)

    cfg = load_yaml(Path(args.config))
    in_scope = flatten_frameworks(cfg)
    controls = build_controls(cfg, in_scope)
    val = load_value(args.config, args.slug)
    # No "every framework, every view" chip may resolve to 0 controls: show a
    # framework only if at least one control actually maps to it.
    used_fw = {cw["fw"] for c in controls for cw in c.get("crosswalk", [])}
    frameworks = [f for f in build_frameworks(in_scope) if f["id"] in used_fw]

    grc = {
        "company": build_company(cfg, in_scope, args.slug),
        "stats": build_stats(len(controls), len(frameworks)),
        "frameworks": frameworks,
        "pillars": build_pillars(cfg),
        "rootFiles": ROOT_FILES,
        "flow": FLOW,
        "frictionPoints": val.get("frictionPoints", []),
        "controls": controls,
        "roadmap": val.get("roadmap") or DEFAULT_3060_90,
        "collateral": val.get("collateral", []),
        "guardrails": build_guardrails(cfg),
        "stack": build_stack(cfg),
        "contact": {
            "name": "Tiffani Dickerson",
            "role": "GRC — governance, risk & compliance",
            "email": "tiffanidickerson437@gmail.com",
            "repoUrl": f"https://github.com/{REPO_SLUG}",
        },
        "meta": {"slug": args.slug, "generated_by": "onboard_company.py", "ai_generated": False},
    }

    out_path = OUTPUT_ROOT / "generated" / "companies" / args.slug / "data.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(grc, indent=2, ensure_ascii=False) + "\n")

    if args.dry_run:
        print(f"slug={args.slug}  frameworks={len(in_scope)}  controls={len(controls)}")
        print("frameworks:", ", ".join(in_scope))
        print("controls:  ", ", ".join(c["id"] for c in controls))
        print(f"wrote {out_path}")
    else:
        print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
