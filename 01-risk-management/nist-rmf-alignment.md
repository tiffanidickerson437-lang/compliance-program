# NIST RMF Alignment

**Pillar:** 01-risk-management
**Owner:** GRC function
**Status:** Scaffold.
**Scope note:** This file aligns the FAIR register to the NIST Risk Management Framework
(SP 800-37, seven steps). The NIST AI RMF (Govern, Map, Measure, Manage) is a different
framework; its crosswalk lives in the 04-ai-governance pillar. The two are complementary and
are not the same thing.

---

## 1. Purpose

The FAIR register quantifies risk. The RMF is the process that turns those numbers into
decisions and keeps them current. This document shows how each RMF step reads from and writes
to the repository, so the register is not a static spreadsheet but a feed into a running
process. The GitHub-native operating model supplies the mechanics: a check computes health, a
drift Issue is the due-diligence record, and a Pull Request is the authorization.

## 2. The seven steps, mapped to the program

| RMF step | What the program does | Reads from | Writes to |
|----------|------------------------|------------|-----------|
| Prepare | Establish context, roles, appetite, and the quantified register. | `config.example.yaml`, program-charter, RACI, risk-appetite-statement | `risk-register.yaml` populated and owned |
| Categorize | Categorize systems and data by impact. Precise location and minors are highest impact. | `config.example.yaml` `data-types`, register `asset_at_risk` | Impact tier per scenario and per system |
| Select | Select controls for each categorized risk, filtered to the in-scope frameworks. | `02-controls/control-library.yaml`, `framework-crosswalk.yaml` | `linked_controls` per scenario |
| Implement | Implement controls as code and as sprint work; evidence is a byproduct of shipping. | control library, secure-development pillar | Operating controls, computed evidence |
| Assess | Assess control effectiveness against the evidence schema; Internal Audit tests independently. | `06-evidence-and-audit/evidence-schemas`, monitoring output | Control health, assessment results |
| Authorize | The business accepts residual risk; the merge is the authorization of record. | residual ALE vs appetite bands | Signed treatment decision, Git history |
| Monitor | Continuously compute health; drift opens an Issue; the register is reviewed quarterly. | `MON-01`, scheduled checks | Drift Issues, updated residual risk |

## 3. Step detail

**Prepare.** `config.example.yaml` sets the context: industry, frameworks, data types, AI posture,
listings. The charter sets authority, the RACI sets ownership, and the appetite statement sets
the bands. The FAIR register is populated. This is the standing groundwork the other steps
build on.

**Categorize.** Each scenario names the asset at risk and an impact tier. Because `data-types`
includes precise-location and minors, those assets categorize as highest impact, which raises
the bar for the controls selected to protect them.

**Select.** Controls are selected from the owned library, already filtered to the frameworks in
`config.example.yaml`. Selection is a mapping exercise, not authoring: the control exists once and is
linked to the scenarios it treats. The crosswalk answers "what satisfies COPPA security" or
"what satisfies SOC 2 access" in seconds.

**Implement.** Controls ship as policy-as-code and as engineering work. Evidence is emitted as
a byproduct of shipping rather than assembled later. The secure-development pillar carries the
SDLC gates that make this true.

**Assess.** Effectiveness is assessed against the evidence schema for each control. Continuous
checks compute health; Internal Audit tests independently for assurance. AI may draft the
assessment narrative; a human approves it before it becomes record.

**Authorize.** Authorization is explicit and owned by the business. Where residual risk sits
inside appetite, the business signs. Where it exceeds appetite or breaches a hard limit, the
governing body decides. In the operating model the authorization is concrete: the Pull Request
that records the decision, and the merge, are the authorization, with Git history as the trail.

**Monitor.** Monitoring is continuous, not annual. MON-01 computes control health from the
systems of record; a failed check opens a drift Issue that is the evidence of due diligence.
The register is re-scored quarterly and on any material change, and residual ALE is updated so
the board always sees current exposure.

## 4. The RMF loop in the operating model

```
Prepare ─▶ Categorize ─▶ Select ─▶ Implement ─▶ Assess ─▶ Authorize ─▶ Monitor
   ▲                                                                      │
   └──────────────── drift Issue re-enters at Assess / Select ◀──────────┘
```

Monitoring is not the end of a line; it is the start of the next loop. A drift Issue or a
re-scored scenario re-enters the cycle at Assess or Select, and a changed `config.example.yaml`
re-enters at Prepare. The framework is a loop because risk is not static.

## 5. Authorization and appetite

RMF authorization is where the business owns the decision. GRC supplies the residual ALE and
the options; the business signs. This is the same boundary stated in the charter and the
appetite statement: GRC provides the model, the data, and the options; the business accepts the
risk. The register's `risk_owner` field names where that signature sits.

## 6. Relationship to NIST AI RMF

For AI scenarios (RISK-003 and the agentic location-graph controls), the seven-step RMF here runs
in parallel with the NIST AI RMF functions in the 04-ai-governance pillar:

- RMF **Categorize / Select** corresponds to AI RMF **Map** (context and risk identification).
- RMF **Assess / Monitor** corresponds to AI RMF **Measure** (analysis and tracking).
- RMF **Authorize / Monitor** corresponds to AI RMF **Manage** (treatment and response).
- AI RMF **Govern** is the standing governance layer, held in the charter and the AI pillar.

One owned control set feeds both frameworks. Adding the AI RMF view is a mapping, not a second
program.
