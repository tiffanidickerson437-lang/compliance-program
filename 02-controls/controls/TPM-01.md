# TPM-01: Third-party management

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/TPM-01.yaml`](../evidence-schemas/TPM-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | TPM (Third-Party Management) |
| Class | SCF |
| NIST CSF function | Govern |
| Family | third-party risk |
| Owner (by function) | GRC (Legal/Privacy on terms) |
| Automation | partial, workflow-tracked |
| Review cadence | at onboarding and renewal; tiered reassessment for high risk |

## Why this control

Sensitive data flows to subprocessors and model providers. Diligence depth must match what a party can touch on the location graph, and trust evidence a vendor already produced should be reused rather than re-collected.

## Control statement

Third parties with system or personal-data access are tiered by what they can touch, assessed before onboarding, and bound by security, breach-notice, and processing terms. High-risk parties reassess on cadence, and vendor trust evidence is reused rather than re-questionnaired.

## Implementation guidance

Tier by data sensitivity and access first, business dependency and breach impact second. The restricted, highest tier is anchored to parties that touch precise location or children's data on the location graph, and to foundation-model providers whose terms govern whether customer data trains a model. Tier is not a function of contract size: a high-spend tool that never receives sensitive data sits in a lower tier, and a small subprocessor that ingests real-time location sits at the top. Accept a current SOC 2 Type II or ISO 27001 certificate in lieu of a custom questionnaire, recording the scope it covers and any exceptions, so the program reuses the assurance the vendor already produced instead of restarting diligence. Bind every in-scope party with a data processing agreement that carries a breach-notice window, processing limits, and subprocessor terms. Map Tier 1 subprocessors so concentration risk, where many critical paths share one provider, is visible. AI may draft the gap analysis from the vendor's report and propose a tier, which makes the analyst faster, but a human GRC owner validates scope, exceptions, and tier before anything is recorded. The recorded evidence is computed and human-validated, never model-authored. Reassess high-risk parties on cadence and on material change, and track overdue reassessments to closure rather than letting them age silently.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Tier scale | Tier 1 (restricted) through Tier 4 (minimal) | Tier set by data sensitivity and access first, dependency and breach impact second. |
| Reassessment cadence, Tier 1 | annual and on material change | High-risk parties reassess at least annually and whenever scope or posture changes materially. |
| Contractual breach-notice window | 72 hours or tighter | Maximum notice window required of an in-scope party in the data processing agreement. |
| Accepted assurance artifacts | current SOC 2 Type II or ISO 27001, scope recorded | Artifacts accepted in lieu of a custom questionnaire, with scope and exceptions logged. |

## Control enhancements

- **TPM-01(1) Touch-based tiering.** Tier is anchored to what a party can touch, with the restricted tier reserved for precise location, children's data, and model-training terms.
- **TPM-01(2) Assurance reuse.** A current SOC 2 Type II or ISO 27001 is accepted in lieu of a custom questionnaire, with scope and exceptions recorded.
- **TPM-01(3) AI-drafted gap analysis with human validation.** AI may draft the gap analysis and propose a tier, but a human GRC owner validates before anything is recorded.
- **TPM-01(4) Subprocessor and concentration mapping.** Tier 1 subprocessors are mapped so concentration risk across shared providers is visible.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. The vendor inventory reconciles to the tiering model.
2. High-risk parties hold current assurance evidence and an executed data processing agreement.
3. Reassessments occurred on cadence and overdue items are tracked to closure.
4. AI-proposed tiers and gap analyses were validated by a human GRC owner before being recorded.

## Assessment methods

**Examine**

- The tiering model, the vendor register, the executed data processing agreements, and the assurance artifacts with their expiries.

**Interview**

- GRC on the tiering bar and the assessment sign-off.
- Legal/Privacy on the data processing, breach-notice, and processing-limit clauses.
- Engineering on the data and access each party actually needs.

**Test**

- Reconcile the vendor inventory to the register and the tiering model.
- Sample high-risk parties and confirm current assurance evidence and an executed data processing agreement.
- Trace an AI-proposed tier to the human validation record.
- Check overdue reassessments to a closure path.

## Evidence

Third-party register: tier, assessment date and outcome, executed contract clauses, assurance-evidence expiry, and overdue reassessments.

- Record shape: [`evidence-schemas/TPM-01.yaml`](../evidence-schemas/TPM-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A scheduled job joins the vendor-risk tool to the contract system and computes: vendors in scope, ratio of high-risk parties with current assurance, ratio with an executed data processing agreement, count with a current SOC 2, and overdue reassessments.
- Drift Issue: Any high-risk party without current assurance, or any overdue reassessment without an exception, opens an Issue tagged TPM-01 naming GRC as owner with the framework impact (SOC 2, NIST CSF, CCPA/CPRA).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC9.2, CC2.3 | framework-mapped |
| ISO/IEC 27002:2022 | 5.19, 5.20, 5.22 | framework-mapped |
| NIST CSF 2.0 | GV.SC-04, GV.SC-06, GV.SC-07 | framework-mapped |
| NIST AI RMF 1.0 | MANAGE 3.0 | framework-mapped |
| CCPA / CPRA (2026) | §7052(a) | framework-mapped |
| GDPR | Art. 28 | framework-mapped |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| GRC | A | Own the tiering model and the assessment bar; sign off that high-risk parties have current assurance evidence. |
| Legal/Privacy | R | Land the DPA, breach-notice window, and processing-limit clauses in every in-scope contract. The executed clauses are the evidence. |
| Vendor | R | Provide a current SOC 2 or equivalent and complete intake before access; refresh on renewal. |
| Engineering | C | Confirm the data and access each party actually needs so the tier reflects real exposure. |
| Auditor | I | Receive the computed register; reconcile the two overdue reassessments. |
