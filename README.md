# Compliance Program (framework-agnostic, controls-as-code GRC engine)

A mature compliance program that lives in Git. Controls are defined once, evidenced from
systems of record, and rendered into every framework a program needs from a single source of
truth. This is not a GRC tool. It is the operational backbone that feeds whatever GRC tool a
program chooses. The repository owns the evidence; the tool is the audit-facing interface.

Compliance built for the audit is a tax. Built for the business, it is infrastructure. This is
the second kind.

**What this is:** a real, framework-agnostic GRC program authored as controls-as-code. The
framework-agnostic property is engineering substance, not a slogan: a control is defined once
and a framework view is a resolution over that definition, so the same program scales to many
frameworks without a parallel control set per framework.

**How it is configured:** every environment-specific value is read from a configuration file.
[`config.example.yaml`](config.example.yaml) is an illustrative, program-neutral example that
describes a consumer location-safety service which processes minors' data. The example values
are illustrative and make no claim about any real organization's internal posture.

**Voice:** declarative and principle-led. Accountability attaches to functions and roles, never
to named individuals.

---

## Two layers: a scan summary and the program of record

The program is read at two depths that point at each other:

| Layer | Where | What it is | Who reads it |
|------|-------|------------|--------------|
| Scan | A summary site | A fast, visual summary: situation forces, pillars, a few controls, the roadmap. | Someone deciding in two minutes whether the depth is real. |
| Depth | This repository | The full program: every control defined once, crosswalked, evidenced, governed, and operated. | Someone who clicks in to verify the depth exists. |

The summary is the highlight reel. The repository is the program of record, where the claims
are backed. Any environment-specific tailoring is presentation on the summary layer; the
repository stays the neutral engine.

---

## The GitHub-native operating model

The program runs as a system, not a binder. The mechanism, end to end:

```
config.example.yaml
    │  (one config file: frameworks, data types, AI posture, listings, stack)
    ▼
GitHub Action scaffolds the program
    │  filters the control library to the configured frameworks
    │  turns on the pillars and families the config requires
    ▼
Daily checks compute control health from the systems of record
    │
    ├─ healthy ─▶ status stays green, evidence is recorded
    │
    └─ drift ─▶ a GitHub Issue is opened automatically
                   (control ID, drift type, owner, framework impact, evidence needed)
                   ── the Issue IS the evidence of due diligence ──
                          │
                          ▼
                   the human gate is a Pull Request
                   (AI drafts the remediation and the narrative,
                    a named function reviews, the merge is the authorization)
                          │
                          ▼
                   on merge the control status updates
                   ── git history is the audit trail ──
```

Read in one line: code decides pass or fail, the system of record supplies the evidence, AI
drafts the narrative and the gap analysis, and a human approves before anything becomes record.

Why each step matters:

- **Controls as code.** Every control is defined once in Git: versioned, peer-reviewed, and
  diffable. A framework view is a rendering of the same control, never a second copy.
- **Drift opens an Issue.** A failed check files a timestamped, retained GitHub Issue. That
  Issue is the proof that the program noticed and acted, which is the evidence of due diligence.
- **The Pull Request is the gate.** Nothing becomes record without a human approval. The merge
  is the authorization, and the commit history records who decided what, when, and why.
- **Git history is the audit trail.** The trail is immutable and already exists, so audit prep
  is a query, not a reconstruction.

---

## `config.example.yaml`: the single input

One file customizes the entire program. Everything else is filtered or generated from it.
Editing the configuration and re-running the scaffold re-renders the program. Adding a framework
is a mapping in the crosswalk, never a new control.

| Field | What it drives |
|-------|----------------|
| `frameworks` | Filters the control library and crosswalk to exactly the regimes in scope. One control, every framework it satisfies. |
| `data-types` | Turns on mandatory control families: `minors` turns on verifiable parental consent (PRI-03.13); `precise-location` turns on agent authorization (AAT-01). |
| `ai-products` | Turns on the 04-ai-governance pillar, the OWASP LLM Top 10 set, agent-identity controls, and the NIST AI RMF and ISO 42001 crosswalk. |
| `listings` | A non-empty value turns on SOX ITGC scope and the Audit and Risk Committee cadence. |
| `stack` | Names the evidence source systems, the drift-check endpoints, and the notification routes. |
| `risk.appetite` | Seeds the tolerance bands in the risk register and the appetite statement. |
| `regulated-jurisdictions` | Selects which privacy regimes appear in the obligation register. |

[`config.example.yaml`](config.example.yaml) ships as the illustrative, program-neutral example.
To run the program for a real environment, supply a file of the same shape with real values.

---

## How to configure and run

1. **Provide configuration.** Copy the example and set values:
   `cp config.example.yaml config.yaml`, then replace each illustrative value with a real one
   from the allowed set documented inline.
2. **Re-render the scaffold.** Run the scaffold Action so the control library and pillars
   filter to the frameworks, data types, AI posture, and listings declared in the config.
3. **Run Phase 1 discovery.** Work through [`30-60-90/phase-1-discover.md`](30-60-90/phase-1-discover.md)
   before marking any control operating. Validate the config against reality first.
4. **Wire the systems of record.** Point the checks at the systems named in `stack`. Until then
   the program runs manually; the model does not depend on any one integration.
5. **Operate the loop.** Let drift open Issues, approve remediation by Pull Request, and let Git
   history accumulate as the audit trail.

---

## The eight pillars

| # | Pillar | Purpose |
|---|--------|---------|
| 00 | [Governance](00-governance/) | Who owns the program, how decisions get made, where authority sits, and how SOX ITGC scope is held for a publicly listed company. |
| 01 | [Risk management](01-risk-management/) | Quantified risk in business terms (FAIR), with treatment owned by the business and the highest-leverage risks steering the roadmap. |
| 02 | [Controls](02-controls/) | The engine. One control defined once; every framework gets its view from the same source. Collect evidence once, satisfy many. |
| 03 | [Third-party risk](03-tprm/) | Right-size diligence to what a vendor can touch; reuse trust evidence instead of restarting questionnaires. |
| 04 | [AI governance](04-ai-governance/) | Govern autonomous agents on real-time location, including minors: identity, least privilege, logging, human gates. |
| 05 | [Secure development](05-secure-development/) | Security in the SDLC as gates that produce evidence as a byproduct of shipping. |
| 06 | [Evidence and audit](06-evidence-and-audit/) | Evidence pre-validated before it reaches the auditor; audit-readiness as a continuous state, not a sprint. |
| 07 | [Stakeholder management](07-stakeholder-management/) | One posture, every audience. The same control rendered into the language each function speaks. |

Cross-cutting directories:

- [`30-60-90/`](30-60-90/) the discover, design, operate plan and the
  [maturity roadmap](30-60-90/maturity-roadmap.md) from day one to a mature program.
- `.github/workflows/` the automations: drift monitor, evidence validator, and report
  generator. Stubs until endpoints and schemas are configured.

### Governance pillar (00) at a glance

- [`program-charter.md`](00-governance/program-charter.md) purpose, scope, authority, operating model.
- [`policy-hierarchy.yaml`](00-governance/policy-hierarchy.yaml) every policy, owner, cadence, version.
- [`roles-and-responsibilities.md`](00-governance/roles-and-responsibilities.md) RACI by function and by activity.
- [`risk-appetite-statement.md`](00-governance/risk-appetite-statement.md) appetite by category, owned by the business.
- [`sox-itgc-scope.md`](00-governance/sox-itgc-scope.md) access, change, and operations ITGC, framework-mapped from home lab, scoped with Internal Audit.
- [`exceptions-process.md`](00-governance/exceptions-process.md) request, approve, track, expire, close.
- [`committee-charter.md`](00-governance/committee-charter.md) Security Steering and Audit and Risk Committee cadence.

### Risk pillar (01) at a glance

- [`risk-register.yaml`](01-risk-management/risk-register.yaml) FAIR-structured scenarios for precise-location exposure, minors' data, agentic AI behavior, vendor breach, change failure, and access.
- [`fair-model.md`](01-risk-management/fair-model.md) how quantification is applied, with a worked example.
- [`nist-rmf-alignment.md`](01-risk-management/nist-rmf-alignment.md) how the register feeds the seven RMF steps.
- [`risk-treatment-templates.md`](01-risk-management/risk-treatment-templates.md) accept, mitigate, transfer, avoid.

---

## The deliberate seven controls (full depth in the library)

Seven SCF-mapped controls, each specified at senior assessment depth (statement, multi-paragraph
implementation guidance, parameters, enhancements, assessment objectives, EXAMINE / INTERVIEW /
TEST methods, a field-level evidence schema, and a CI mapping). The deep narrative for each lives
under [`02-controls/controls/`](02-controls/controls/).

| ID | Family | Focus |
|----|--------|-------|
| AAT-01 | AI governance | Agent authorization on the real-time location graph and precise location |
| PRI-03.13 | Privacy | Verifiable parental consent (COPPA) |
| IAC-17 | Access | Periodic privilege review and SOX ITGC access |
| CHG-02 | Change | Pull-request-based production change control |
| MON-01 | Monitoring | Continuous logging and drift detection |
| TPM-01 | Third party | Vendor tiering and assurance |
| IRO-01 | Incident | Incident response including AI-scope incidents |

---

## Hard constraints and guardrails

- No claim is made about any real organization's internal security posture. The example
  configuration is illustrative and states what a mature program would look like.
- SOX ITGC is framework-mapped from home-lab work and scoped with Internal Audit. It is never
  represented as a completed public-company SOX audit. See
  [`sox-itgc-scope.md`](00-governance/sox-itgc-scope.md).
- Evidence is computed from systems of record. AI-generated content presented as evidence is
  rejected by schema. AI drafts narratives; it does not author evidence.
- Functions and roles are named, never individuals. Accountability attaches to a function.
- Example evidence in the library is illustrative. Replace it with computed exports from the
  real systems before any audit submission.
- The program is a scaffold, not production infrastructure; nothing here requires ongoing
  maintenance to stay functional.

---

## Validating the artifacts

Every YAML and JSON file in the program parses. To check after editing, from the repository root:

```bash
# YAML
python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('**/*.yaml', recursive=True)]" && echo "all YAML parses"

# JSON (OSCAL catalog and profiles)
node -e "const fs=require('fs');for(const f of require('child_process').execSync('find 02-controls -name \"*.json\"').toString().trim().split('\n'))JSON.parse(fs.readFileSync(f));console.log('all JSON parses')"
```

If PyYAML is not installed, the YAML check runs under Node with `js-yaml`.

---

## License and use

A program for demonstration and for configuring against a real environment. Replace the example
evidence with computed exports from your systems of record before relying on it for an audit.
