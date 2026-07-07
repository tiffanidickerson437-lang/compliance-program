# Roles and Responsibilities (RACI)

**Pillar:** 00-governance
**Owner:** governance function
**Status:** Scaffold. Confirm function owners in Phase 1 discovery.
**Principle:** Accountability attaches to a function, never to an individual. Titles are
used only where they are standard and certain; otherwise the function is named.

---

## 1. The three lines

- **First line (own and operate):** the functions that run systems and execute controls.
  Engineering, IT, Security operations, Product, Sales, HR.
- **Second line (set and oversee):** the functions that define the program and monitor it.
  GRC, Privacy, Legal, and Security in its policy-setting role.
- **Third line (independent assurance):** Internal Audit. It tests the first and second
  lines and does not build or operate controls, which preserves its independence.

The governing body sits above the three lines and accepts residual risk that exceeds the
stated appetite.

## 2. RACI legend

- **R - Responsible:** performs the work.
- **A - Accountable:** owns the outcome and signs. Exactly one per row.
- **C - Consulted:** provides input before the work is final.
- **I - Informed:** receives the result.

## 3. Function glossary

| Function | What it owns in this program |
|----------|------------------------------|
| GRC | The control library, crosswalk, evidence schemas, monitoring design, reporting |
| Security | Access, logging, monitoring, incident response, security policy and enforcement |
| Engineering | Change control, secure development, evidence emitted as a byproduct of shipping |
| Legal | Regulatory interpretation, breach-notification decisions, contracts |
| Privacy | Consent, data-subject rights, COPPA obligations, DPIAs |
| Product | Consent and disclosure flows, AI feature design within guardrails |
| IT | Identity provider operations, access provisioning and deprovisioning |
| HR | Joiner, mover, leaver feed; awareness and acknowledgment |
| Sales | Trust-center first answers; routes sensitive items to GRC under NDA |
| Finance | Control cost and budget |
| Internal Audit | Independent testing; audit liaison |
| Board | Residual-risk acceptance; oversight reporting |

## 4. RACI by pillar

| Pillar | GRC | Security | Engineering | Legal/Privacy | IT | Product | Sales | Finance | Internal Audit | Board |
|--------|-----|----------|-------------|---------------|----|---------|-------|---------|----------------|-------|
| 00 Governance | A | C | C | C | I | I | I | C | C | A* |
| 01 Risk management | R | C | C | C | I | C | I | C | C | A |
| 02 Controls | A | R | R | C | C | C | I | I | C | I |
| 03 Third-party risk | A | C | C | R | I | C | I | C | I | I |
| 04 AI governance | A | R | R | C | R | C | I | I | C | I |
| 05 Secure development | C | C | A | I | I | C | I | I | I | I |
| 06 Evidence and audit | A | C | C | C | C | I | I | I | R | I |
| 07 Stakeholder management | A | C | C | C | I | C | R | C | I | I |

\* Governance: GRC is accountable for operating the program; the Board is accountable for
ratifying the charter, the risk appetite, and the committee structure. Risk appetite sign-off
is a Board outcome; the rest of governance operation is a GRC outcome.

## 5. RACI by recurring activity

| Activity | GRC | Security | Engineering | Legal/Privacy | IT | HR | Internal Audit | Board |
|----------|-----|----------|-------------|---------------|----|----|----------------|-------|
| Author or amend a control | A | C | C | C | I | I | C | I |
| Compute and collect evidence | A | R | R | C | R | I | I | I |
| Triage drift Issue and remediate | C | A | R | C | R | I | I | I |
| Approve an exception | A | C | C | C | I | I | C | I |
| Sign a risk-treatment decision | C | C | C | C | I | I | C | A |
| Quarterly access recertification | C | A | R | I | R | C | I | I |
| Production change via Pull Request | I | A | R | I | C | I | I | I |
| Breach-notification decision | C | C | I | A | I | I | I | I |
| Verifiable parental consent enforcement | C | C | R | A | I | I | I | I |
| Approve a new AI agent and its scope | C | A | R | C | R | I | I | I |
| High-impact AI action on a minor account | C | A | R | C | I | I | I | I |
| Vendor tiering and assessment | A | C | C | R | I | I | I | I |
| Board and committee reporting | A | C | I | C | I | I | C | I |
| Audit liaison and evidence delivery | R | C | C | C | C | I | A | I |

## 6. Control-level RACI is rendered, not re-authored

Each control in `02-controls/control-library.yaml` carries its own per-function RACI in a
Translate view, so one control statement renders into the specific ask for each function.
The matrices above are the program defaults; a control may refine them. For example, control
AAT-01 (agent authorization on the location graph) makes Security accountable for the
authorization broker, Engineering responsible for binding each location read to a purpose
token, and Legal accountable for the lawful basis and the DPIA. Control PRI-03.13 makes
Privacy accountable for what verifiable consent requires and Engineering responsible for
checking the consent service before processing a minor's data.

## 7. Standing rule on independence and appetite

- Internal Audit tests; it does not own or operate the controls it tests.
- The business owns risk appetite and signs treatment decisions. GRC supplies the model,
  the data, and the options. GRC does not accept risk on the business's behalf.
- AI drafts narratives and gap analyses. A named function reviews and approves before
  anything becomes record.
