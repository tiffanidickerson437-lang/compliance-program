# Committee Charter

**Pillar:** 00-governance
**Owner:** governance function
**Status:** Scaffold. Confirm membership and cadence in Phase 1 discovery.
**Seeded by:** `config.example.yaml`. A non-empty `listings` block turns on the Audit and Risk
Committee section; `company.size` sets the default cadence.

---

## 1. Purpose

Two bodies govern this program at two altitudes. The Security Steering Committee runs the
program month to month and clears the operational decisions. The Audit and Risk Committee
provides board-level oversight, owns the SOX program through Internal Audit, and accepts
residual risk that exceeds the stated appetite. The two are connected by a single escalation
path so the board sees one current picture, not several partial ones.

---

## 2. Security Steering Committee (operational governance)

### Mandate
Steer the program between board cycles: review control health, clear exceptions within
authority, prioritize remediation, and decide operational trade-offs that do not exceed the
risk appetite.

### Membership (by function)
| Function | Role on committee |
|----------|-------------------|
| GRC | Chair; sets agenda; owns the record |
| Security | Standing member; control health and incidents |
| Engineering | Standing member; change, secure development, evidence flow |
| Legal/Privacy | Standing member; regulatory calendar and consent obligations |
| IT | Standing member; identity and access operations |
| Product | Consulted member; AI features and consent flows |
| Internal Audit | Observer; preserves independence, does not vote |

### Cadence
Monthly for an enterprise-stage company (the configured size). A higher tempo is set during an
active audit or a Sev1 remediation.

### Standing inputs
- Control health from continuous monitoring and the count of open drift Issues.
- Exception register: open items by tier and any item past expiry.
- Risk register changes and any scenario now out of appetite.
- Third-party status: high-risk vendors without current assurance, overdue reassessments.
- AI governance: new agents approved, human-gate activity, model changes.
- Upcoming regulatory and audit dates.

### Decision rights
- Approve exceptions within the working-level authority in `exceptions-process.md`.
- Prioritize the remediation backlog and assign owning functions.
- Escalate to the Audit and Risk Committee any item that exceeds appetite or carries
  board-level risk.

### Outputs
- A decision log committed to the repository.
- An updated remediation backlog with owners and dates.
- An escalation packet for the board committee when required.

### Quorum
The chair plus the accountable functions for the items on the agenda. Security and Engineering
are required for any control or change decision.

---

## 3. Audit and Risk Committee (board-level oversight)

This section is active because `config.example.yaml` declares public listings (two public
exchanges; illustrative example listings). A private company would not run this committee.

### Mandate
Independent oversight of risk, compliance, and the SOX program. Acceptance of residual risk
beyond the stated appetite. Ratification of the charter and the risk appetite statement.

### Membership
| Function | Role on committee |
|----------|-------------------|
| Independent board directors | Members and chair; the only voting members |
| Internal Audit | Standing attendee; owns the SOX program and reports findings |
| GRC | Standing attendee; presents quantified risk and control health |
| Finance | Standing attendee; significant accounts and SOX scoping context |
| External auditor | Attends as needed for audit planning and results |

### Cadence
Quarterly, and on demand for a material incident, a material exception, or an audit milestone.

### Standing inputs
- Quantified top risks in business terms (dollar exposure), from
  `01-risk-management/risk-register.yaml`, rendered through the board reporting template in the
  stakeholder-management pillar.
- SOX ITGC status from Internal Audit per `sox-itgc-scope.md`, with the explicit reminder that
  home-lab mapping is design, not an audit result, until Internal Audit tests in the live
  environment.
- Material exceptions and any hard-limit breaches.
- Incident summary, including any AI-scope incident, and breach-notification decisions.
- The regulatory calendar: COPPA compliance date, EU AI Act obligations, and audit timing.

### Decision rights
- Accept or refuse residual risk that exceeds the appetite.
- Ratify and amend the charter, the risk appetite statement, and this committee charter.
- Direct Internal Audit's program priorities.

### Outputs
- Minuted decisions and residual-risk acceptances.
- Direction to the Security Steering Committee and to Internal Audit.
- The oversight record an external auditor and a regulator can rely on.

---

## 4. Escalation path

1. The Security Steering Committee clears what is within its authority and logs it.
2. Anything that exceeds appetite, breaches a hard limit, or carries board-level risk is
   packaged into an escalation and sent to the Audit and Risk Committee.
3. The Audit and Risk Committee decides, and its direction returns to the Security Steering
   Committee for execution.
4. A Sev1 incident or a hard-limit breach does not wait for the next cycle; it triggers an
   out-of-band session of the relevant committee.

## 5. How `config.example.yaml` governs cadence and structure

- `company.listings` non-empty turns on the Audit and Risk Committee and SOX reporting.
- `company.size` sets the default Security Steering Committee cadence (monthly at enterprise).
- `ai-products: true` adds the AI governance standing input and a Product seat.
- `frameworks` and `regulated-jurisdictions` set the regulatory-calendar input.

Change the config and re-ratify, and the committee structure and inputs re-render to match.
