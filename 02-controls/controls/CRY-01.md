# CRY-01: Use of cryptographic controls

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/CRY-01.yaml`](../evidence-schemas/CRY-01.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | CRY (Cryptographic Protections) |
| Class | SCF |
| NIST CSF function | Protect |
| Family | cryptography |
| Owner (by function) | Security (Engineering implements) |
| Automation | partial |
| Review cadence | continuous posture; algorithm and key-policy review annually |

## Why this control

A service holding real-time precise location and minor data must make that data unreadable to anyone without authorization, at rest and in transit. The public trust material already claims TLS in transit and AES at rest; this control is what turns that claim into a tested, evidenced state rather than a marketing line. It also underwrites every other control: the consent gate, the access review, and the agent broker all assume the underlying data is encrypted and the keys are governed.

## Control statement

Sensitive and regulated data is protected with cryptographic controls that meet a defined standard, in transit and at rest. Keys are generated, stored, rotated, and revoked under a documented key-management process, separated from the data they protect. Weak or deprecated algorithms and protocols are not used, and exceptions are tracked and time-bound.

## Implementation guidance

Define the cryptographic standard once, as policy-as-code where it can be enforced: the approved algorithms, minimum key lengths, and protocol versions, plus the explicit deny-list of deprecated ones. Encrypt precise location and minor data at rest with authenticated encryption and in transit with current TLS, and treat any endpoint negotiating a deprecated protocol as drift, not an accepted state. Keep keys in a managed key store or HSM, never in source, configuration, or application logs, and separate the duty to manage keys from the duty to access the data those keys protect. Rotate keys on a defined cadence and on any suspected compromise, and make revocation fast enough that a compromised key is a bounded event. Where the AI layer or an analytics pipeline processes location data, prefer minimization and tokenization so the cleartext is exposed to the fewest systems possible. The evidence is the computed configuration state — cipher in use per data store, protocol per endpoint, key age and rotation status — not a policy assertion that encryption is "enabled."

## Parameters

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Data-at-rest standard | authenticated encryption, AES-256 or stronger | Applies to precise location and minor data stores; tune up per data class, never down. |
| Data-in-transit standard | TLS 1.2 minimum, TLS 1.3 preferred; deprecated protocols denied | Any endpoint negotiating below the floor is drift. |
| Key rotation interval | 365 days maximum, or immediately on suspected compromise | Maximum age before a key must rotate; shorter for the highest-sensitivity stores. |
| Key/data duty separation | required | The function that manages keys is not the function that reads the protected data. |

## Control enhancements

- **CRY-01(1) Approved-algorithm enforcement.** An enforced standard names approved algorithms, key lengths, and protocol versions and denies deprecated ones; violations surface as drift.
- **CRY-01(2) Managed key custody and separation of duties.** Keys live in a managed key store or HSM, never in source or logs, and key management is separated from data access.
- **CRY-01(3) Scheduled and event-driven rotation.** Keys rotate on cadence and immediately on suspected compromise, with revocation bounded by a defined interval.
- **CRY-01(4) Minimization of cleartext exposure.** Location and minor data are tokenized or minimized so the fewest systems, including the AI layer, ever hold cleartext.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. Precise location and minor data are encrypted at rest and in transit to the defined standard.
2. No in-scope endpoint or store uses a deprecated algorithm or protocol outside a tracked, time-bound exception.
3. Keys are held in a managed store, separated from data-access duties, and absent from source and logs.
4. Keys rotate within the defined interval and revoke within the defined window on compromise.

## Assessment methods

**Examine**

- The cryptographic standard and the approved/deny algorithm and protocol lists.
- The key-management process, the key inventory, and the rotation and revocation records.
- The encryption configuration for the precise-location and minor-data stores.

**Interview**

- Security on the standard, the deny-list, and how violations surface as drift.
- Engineering on where keys live, how rotation runs, and how cleartext exposure is minimized in the data and AI pipelines.

**Test**

- Sample data stores and confirm authenticated encryption at the defined strength.
- Probe a sample of endpoints and confirm none negotiate a deprecated protocol.
- Pull the key inventory and confirm rotation within interval and no keys present in source or logs.

## Evidence

Per data store and endpoint: cipher or protocol in use, key reference, key age, last rotation, and any deprecated-protocol negotiation observed.

- Record shape: [`evidence-schemas/CRY-01.yaml`](../evidence-schemas/CRY-01.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from configuration state and the key store; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A daily job inventories encryption configuration across in-scope stores and endpoints and computes: stores below the at-rest standard (target zero), endpoints negotiating a deprecated protocol (target zero), and keys past the rotation interval.
- Drift Issue: Any store below standard, any deprecated-protocol endpoint, or any overdue key opens an Issue tagged CRY-01 naming Security as owner, with the framework impact (SOC 2, ISO 27001, GDPR).
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC6.1, CC6.7 | framework-mapped |
| ISO/IEC 27002:2022 | 8.24 | framework-mapped |
| NIST CSF 2.0 | PR.DS-01, PR.DS-02 | framework-mapped |
| GDPR | Art. 32 | framework-mapped |

## RACI asks by audience

| Audience | RACI | Ask |
|----------|------|-----|
| Security | A | Own the cryptographic standard and key-management process; certify no in-scope store or endpoint runs below the floor. |
| Engineering | R | Implement encryption to standard, keep keys out of source and logs, and emit the configuration state as evidence. |
| Legal/Privacy | C | Confirm the standard meets the security-of-processing bar for precise location and minor data. |
| Auditor | I | Receive the computed configuration and key inventory; sample against the store, not a screenshot. |
