# 02-controls: the engine

One control, defined once, rendered into the language every framework and every team speaks. This directory is the nucleus of the program. Everything downstream (evidence, audit, stakeholder reporting) resolves from the files here.

## Why SCF as the control spine

The Secure Controls Framework (SCF) is the unifying taxonomy. SCF 2025.4 carries 1,468 controls across 33 domains and publishes crosswalks to 200+ authoritative sources (SOC 2, ISO 27001/27002, ISO 42001, NIST CSF, NIST AI RMF, COPPA, CCPA/CPRA, EU AI Act, and more). Mapping a program to one meta-framework, instead of maintaining a separate control set per framework, is what makes "collect once, satisfy many" real rather than aspirational.

This program does not invent SCF taxonomy. The eleven control IDs used here (AAT-01, PRI-03.13, IAC-17, CHG-02, MON-01, TPM-01, IRO-01, CRY-01, VPM-01, DCH-01, SAT-02) are real SCF identifiers, selected deliberately. Eleven from 1,468 is the point: choose what matters for a consumer location-safety service that processes minors' data, runs an agentic AI layer on a real-time location graph, and carries public-company IT general controls, rather than padding a count. Depth per control is the deliverable; breadth of list is not.

## Why OSCAL as the machine-readable format

OSCAL (the NIST Open Security Controls Assessment Language) is the machine-readable form of the control set. The choice is deliberate, and it is close to free: SCF publishes itself as an OSCAL catalog, so adopting SCF as the spine means the OSCAL representation arrives with the taxonomy rather than as a separate build. That keeps the human-readable YAML and the machine-readable JSON in the same lineage.

The honest tradeoff: OSCAL adoption is still emerging. Tooling maturity varies, and many auditors do not consume OSCAL directly yet. The bet here is that defining controls, profiles, parameters, and assessment objectives in an open, versionable schema pays off as that ecosystem matures, and costs little today because the YAML view stays readable for humans in the meantime. This is a forward position, named as one, not a claim that the market has arrived.

## How deep each control goes

Each of the eleven controls is specified at senior assessment depth. A control carries:

- A full control **statement** and multi-paragraph **implementation guidance** that is concrete about mechanism, not generic policy language.
- Assignable **parameters** (for example a purpose-token TTL ceiling, a recertification cadence, a retention floor) so the control is tuned rather than rewritten.
- **Control enhancements** that name the sub-parts that make the control real (deny-by-default brokering, segregation of duties, immediate consent withdrawal, and so on).
- **Assessment objectives** (what an assessor must be able to determine) and **assessment methods** split into EXAMINE, INTERVIEW, and TEST with specific procedures.
- A field-level **evidence schema** where every field names its source system and how it is computed, and where `ai_generated: false` is a required constant.
- An **automation and CI mapping**: the check that computes control health and the condition that opens a drift Issue.
- The **framework crosswalk** with real references, and the **RACI asks** per audience.

The deep, human-readable version of each control lives under [`controls/`](controls/), one file per control.

## One definition, many views

The control is defined exactly once. A framework view is a resolution over that single definition, never a second copy.

```
control-library.yaml         single definition per control (human-readable, the working source)
control-library.oscal.json   the same controls as an OSCAL 1.1.3 catalog (params, enhancements,
                             assessment objectives and methods)
framework-crosswalk.yaml     queryable map: control -> frameworks, and framework -> controls
controls/                    one deep, human-readable narrative per control
profiles/                    one OSCAL profile per framework; each imports the catalog and
                             selects control IDs (profile resolution, not redefinition)
evidence-schemas/            one audit-ready, field-level evidence record shape per control
```

The mechanism:

1. A control's statement, guidance, parameters, enhancements, assessment objectives and methods, owner, automation status, and props live once in `control-library.yaml` and `control-library.oscal.json`.
2. `framework-crosswalk.yaml` records which framework requirements that one control satisfies, with real references, in both directions.
3. Each file in `profiles/` is an OSCAL profile that imports the catalog and includes the relevant control IDs. Resolving the SOC 2 profile yields the SOC 2 control set; resolving the ISO 27001 profile yields the ISO set; the control objects are the same objects, not duplicates.
4. Evidence is computed once per control from systems of record (`evidence-schemas/`), then it answers every framework that maps to that control.

So AAT-01 is authored a single time and simultaneously answers NIST AI RMF, ISO 42001, SOC 2, and the EU AI Act. The evidence record is collected once and satisfies all four.

## How to add a framework

Adding a framework is a mapping, not a rebuild. No control is rewritten.

1. Add the framework's references to each relevant control under `by_control` in `framework-crosswalk.yaml`, and add the reverse entries under `by_framework`.
2. Register the framework in the `frameworks` block with its display name and profile path.
3. Create `profiles/<framework>.profile.oscal.json` that imports `../control-library.oscal.json` and lists the control IDs (lowercased) the framework needs.
4. If the framework introduces an obligation that no existing control covers, add one new SCF-mapped control to the library. That is the only case that touches the control definitions, and even then existing controls are untouched.

The cost of the next framework is the cost of a crosswalk and a profile, measured in minutes, not a parallel control library. This is the framework-agnostic property as engineering substance: the control set scales to many frameworks because a framework is a view, not a copy.

## Files in this directory

| File | What it is |
|------|------------|
| `control-library.yaml` | Single definition of all 11 controls: id, SCF domain, class, title, statement, multi-paragraph implementation guidance, parameters, enhancements, assessment objectives, assessment methods (EXAMINE / INTERVIEW / TEST), owner by function, automation, review cadence, framework mappings, evidence schema, CI mapping, example evidence, props, and RACI asks. |
| `control-library.oscal.json` | The same 11 controls as an OSCAL 1.1.3 catalog: metadata, controls with lowercased ids, class `SCF`, params, props, parts for statement and guidance, an assessment-objective part with itemized objectives, assessment-method parts (EXAMINE / INTERVIEW / TEST), and enhancements as nested controls. |
| `controls/` | One deep, human-readable narrative per control (`AAT-01.md` through `SAT-02.md`). |
| `framework-crosswalk.yaml` | Real references for every framework each control satisfies, queryable by control and by framework. SOX ITGC lines are marked framework-mapped, home lab. |
| `profiles/*.profile.oscal.json` | One OSCAL profile per framework (soc2, iso27001, iso42001, nist-ai-rmf, nist-csf, coppa, ccpa-cpra, eu-ai-act, sox-itgc, gdpr). Each imports the catalog and selects control IDs. |
| `evidence-schemas/*.yaml` | One audit-ready, field-level evidence record shape per control. Each field names its source system, type, and how it is computed; the schema defines what makes a record audit-ready and what gets rejected. |

## The deliberate eleven

| ID | Domain | Control | Why it is here |
|----|--------|---------|----------------|
| AAT-01 | AAT | AI and autonomous technologies governance | The hero control. Governs agents acting on a real-time location graph of tens of millions, including children. |
| PRI-03.13 | PRI | Parent or guardian opt-in consent for minors | Verifiable parental consent before processing; the amended COPPA Rule applies. |
| IAC-17 | IAC | Periodic review of account privileges | The access pillar of SOX ITGC, and the control auditors test first. |
| CHG-02 | CHG | Configuration change control | The change pillar of SOX ITGC. The pull request is the gate; evidence is a byproduct of shipping. |
| MON-01 | MON | Continuous monitoring and event logging | The operations pillar of SOX ITGC, and the drift-opens-an-issue mechanism. |
| TPM-01 | TPM | Third-party management | Diligence depth matched to what a vendor or model provider can touch on the location graph. |
| IRO-01 | IRO | Incident response operations | Where regulatory clocks get real, including AI scope breaches. |
| CRY-01 | CRY | Use of cryptographic controls | Makes the at-rest and in-transit encryption claim a tested, evidenced state and governs the keys. |
| VPM-01 | VPM | Vulnerability and patch management | The program every security questionnaire probes first; exposure-weighted remediation SLAs. |
| DCH-01 | DCH | Data classification and protection | Draws the boundary every other data control inherits its scope from; minimization and retention. |
| SAT-02 | SAT | Security awareness and role-based training | The competence control at SOC 2 CC1.4; the people surface no broker covers. |

## Hard rules honored here

- Controls name functions and roles, never individuals.
- SOX ITGC associations are framework mapping only (home lab) and are never represented as audited. Look for the `framework-mapped, home lab` markers in the crosswalk and the `sox-itgc-basis` props in the catalog.
- Example evidence is illustrative and is not a claim about any real organization's internal posture.
- Evidence is computed from systems of record, never authored by a model. Every evidence schema requires `ai_generated: false` and rejects model-authored records.
