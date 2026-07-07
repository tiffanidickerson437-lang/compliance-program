# Committee Charter

**Pillar:** 00-governance
**Owner:** governance function
**Status:** Scaffold. Confirm membership and cadence in Phase 1 discovery.
**Seeded by:** `config.example.yaml`. `company.size` sets the default cadence.

---

## 1. Purpose

The Security Steering Committee governs this program operationally: it runs the program month to
month, clears the decisions within its authority, and escalates anything that exceeds the risk
appetite or carries board-level risk to the governing body. The governing body accepts residual
risk that exceeds the stated appetite and ratifies this charter, the program charter, and the risk
appetite statement; its own structure and cadence are set outside this document. The escalation
path below keeps the two connected so the governing body sees one current picture, not several
partial ones.

---

## 2. Security Steering Committee (operational governance)

### Mandate
Steer the program between governing-body cycles: review control health, clear exceptions within
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
- Escalate to the governing body any item that exceeds appetite or carries board-level risk.

### Outputs
- A decision log committed to the repository.
- An updated remediation backlog with owners and dates.
- An escalation packet for the governing body when required.

### Quorum
The chair plus the accountable functions for the items on the agenda. Security and Engineering
are required for any control or change decision.

---

## 3. Escalation path

1. The Security Steering Committee clears what is within its authority and logs it.
2. Anything that exceeds appetite, breaches a hard limit, or carries board-level risk is
   packaged into an escalation and sent to the governing body.
3. The governing body decides, and its direction returns to the Security Steering Committee
   for execution.
4. A Sev1 incident or a hard-limit breach does not wait for the next cycle; it triggers an
   out-of-band session with the governing body.

## 4. How `config.example.yaml` governs cadence and structure

- `company.size` sets the default Security Steering Committee cadence (monthly at enterprise).
- `ai-products: true` adds the AI governance standing input and a Product seat.
- `frameworks` and `regulated-jurisdictions` set the regulatory-calendar input.

Change the config and re-ratify, and the committee structure and inputs re-render to match.
