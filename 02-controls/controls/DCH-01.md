# DCH-01: Data classification and protection

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/DCH-01.yaml`](../evidence-schemas/DCH-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | DCH (Data Classification & Handling) |
| Class | SCF |
| NIST CSF function | Identify / Protect |
| Family | data protection |
| Owner (by function) | Legal/Privacy (Security and Engineering enforce) |
| Automation | partial |
| Review cadence | continuous handling checks; classification scheme review annually |

## Why this control

Every other data control inherits its scope from this one. Precise location and minor data are the crown jewels; if they are not classified, inventoried, and bound to handling and retention rules, then encryption, access review, consent, and the agent broker are all guarding a boundary no one has drawn. This control draws the boundary: it names the highest-sensitivity classes, holds them to minimization and retention limits, and makes deletion a recorded event.

## Control statement

Data is classified by sensitivity, and precise location and minor data are designated the highest-sensitivity class. Handling, retention, and disposal rules attach to the classification and are enforced. Data is minimized to what the declared purpose requires and deleted or restricted when the lawful basis ends. Cleartext flows of the highest-sensitivity classes are inventoried so every other control knows its scope.

## Implementation guidance

Define a classification scheme with a small number of levels and an unambiguous top class for precise location and minor data. Attach handling rules to the class rather than to the system, so a new store inherits the rule the moment its data is classified. Maintain an inventory of where the highest-sensitivity classes live and flow, because that inventory is the scoping input for CRY-01 encryption, IAC-17 access review, AAT-01 agent brokering, and PRI-03.13 consent. Enforce minimization at collection and at use: collect only what the declared purpose needs, and where the AI layer or analytics consume location data, prefer aggregation or tokenization over raw cleartext. Set retention limits per class and make deletion a recorded, verifiable event tied to consent withdrawal, account closure, or the end of the lawful basis, not a background process no one can attest to. Treat the appearance of a highest-sensitivity class in an unapproved store or an unclassified flow as drift that opens an Issue, because an unknown copy of location data is the failure this control exists to catch.

## Parameters

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Highest-sensitivity classes | precise location, minor data | Inherit the tightest handling, retention, and access rules. |
| Minor-data retention limit | shortest interval that serves the declared purpose | Held tighter than adult data; deletion fires on consent withdrawal or account closure. |
| Deletion evidence | recorded and verifiable per request | Disposal is an evidenced event, not an assumed background job. |
| Unclassified sensitive flow | drift, opens an Issue | A highest-sensitivity class in an unapproved or unclassified store surfaces, never sits silent. |

## Control enhancements

- **DCH-01(1) Top-class designation for location and minor data.** Precise location and minor data are designated the highest-sensitivity class and inherit the tightest rules.
- **DCH-01(2) Sensitive-data flow inventory.** The locations and flows of the highest-sensitivity classes are inventoried and serve as the scope input to CRY-01, IAC-17, AAT-01, and PRI-03.13.
- **DCH-01(3) Minimization at collection and use.** Collection is limited to the declared purpose; the AI and analytics layers prefer aggregation or tokenization over raw cleartext.
- **DCH-01(4) Recorded deletion on end of basis.** Deletion or restriction is a recorded, verifiable event on consent withdrawal, account closure, or end of lawful basis.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. A classification scheme exists and precise location and minor data are the highest-sensitivity class.
2. Handling, retention, and disposal rules attach to classification and are enforced.
3. An inventory of the highest-sensitivity data and its flows exists and scopes the dependent controls.
4. Minimization is applied at collection and use, and deletion on end-of-basis is recorded and verifiable.

## Assessment methods

**Examine**

- The classification scheme, the handling and retention rules per class, and the sensitive-data flow inventory.
- The minimization rules applied to the AI and analytics pipelines.
- The deletion and restriction records tied to consent withdrawal and account closure.

**Interview**

- Legal/Privacy on the scheme, retention limits, and lawful-basis-driven deletion.
- Engineering on how classification drives handling and how deletion is recorded and verified.

**Test**

- Sample stores and confirm the highest-sensitivity classes are classified, inventoried, and held to the handling rule.
- Trigger a deletion case (consent withdrawal or closure) and confirm the data is deleted or restricted with a record.
- Search for a highest-sensitivity class in an unapproved store and confirm it surfaces as drift.

## Evidence

Per highest-sensitivity data store and flow: classification, retention rule, approved/unapproved status, and deletion records for end-of-basis cases.

- Record shape: [`evidence-schemas/DCH-01.yaml`](../evidence-schemas/DCH-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from the data inventory and deletion logs; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A daily job reconciles the sensitive-data inventory and computes: highest-sensitivity classes in unapproved or unclassified stores (target zero), records past the retention limit, and end-of-basis deletions completed versus due.
- Drift Issue: Any unapproved sensitive store, any over-retained record, or any missed end-of-basis deletion opens an Issue tagged DCH-01 naming Legal/Privacy as owner with the framework impact (SOC 2, ISO 27001, GDPR, CCPA/CPRA).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | C1.1, C1.2 | framework-mapped |
| ISO/IEC 27002:2022 | 5.12, 5.13, 8.10, 8.12 | framework-mapped |
| NIST CSF 2.0 | ID.AM-07, PR.DS-01 | framework-mapped |
| GDPR | Art. 5(1)(c), Art. 5(1)(e), Art. 32 | framework-mapped |
| CCPA / CPRA (2026) | Civil Code §1798.100(c) | framework-mapped |

## RACI asks by audience

| Audience | RACI | Ask |
|----------|------|-----|
| Legal/Privacy | A | Own the classification scheme and retention limits; define lawful-basis-driven deletion for minor and location data. |
| Engineering | R | Enforce handling by classification, maintain the sensitive-data inventory, and record deletions as evidence. |
| Security | C | Confirm the highest-sensitivity inventory scopes encryption, access review, and the agent broker. |
| Auditor | I | Receive the computed inventory and deletion records; sample against the store, not an attestation. |
