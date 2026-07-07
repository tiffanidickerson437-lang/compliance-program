# Exceptions and Risk Acceptance Process

**Pillar:** 00-governance
**Owner:** GRC function (process); the business (risk acceptance)
**Status:** Scaffold. Confirm approval authorities in Phase 1 discovery.

---

## 1. Purpose

An exception is a recorded, time-bound deviation from a control or policy, granted only with a
compensating measure and an owner. The process exists so that the business can move when a
control cannot yet be met, without losing the record of the decision or the path back to
compliance. An exception is a managed risk, never a quiet one.

## 2. Principles

- **Time-bound.** Every exception has an expiry. None is permanent. An expired exception that
  is still needed is re-justified and re-approved, not auto-renewed.
- **Compensating control.** An exception is granted only with a documented measure that reduces
  the residual risk while the gap is open.
- **Owned.** Every exception names an accountable function and a remediation owner.
- **Visible.** Open exceptions appear in the register and in committee reporting. Nothing is
  hidden in a spreadsheet.
- **Appetite-bounded.** An exception that breaches a hard limit in
  `risk-appetite-statement.md` cannot be approved at the working level; it escalates to the
  governing body or is refused.

## 3. Roles

| Role | Function | Responsibility |
|------|----------|----------------|
| Requestor | any first-line function | Raises the request, proposes the compensating control and a remediation date. |
| Reviewer | GRC | Validates scope, scores residual risk, confirms the compensating control, routes to the right approver. |
| Approver | by risk tier (see section 5) | Accepts the residual risk for the exception window, or refuses. |
| Remediation owner | the owning function | Closes the underlying gap before expiry. |
| Internal Audit | third line | Samples the register for completeness and approval discipline. |

## 4. Lifecycle

1. **Request.** The requestor opens an exception with the control or policy ID, the reason, the
   business need, the proposed compensating control, and a target remediation date.
2. **Triage.** GRC confirms the request is complete and identifies the affected controls and
   framework impact.
3. **Risk assessment.** GRC scores the residual risk with the compensating control in place,
   using the FAIR bands in `01-risk-management`. The score sets the approval authority.
4. **Approval.** The approver for that risk tier accepts or refuses. A hard-limit breach
   escalates to the governing body.
5. **Implement.** The compensating control is put in place and verified before the exception is
   relied on.
6. **Track.** The exception enters the register with its expiry. Aging is reported to the
   Security Steering Committee.
7. **Expire or renew.** At expiry the exception closes automatically unless re-justified and
   re-approved. Renewal is a new decision, not a default.
8. **Close.** When the underlying gap is remediated, the exception closes and the control
   returns to its standard state. The closure is recorded.

## 5. Approval authority by residual risk

| Residual risk after compensating control | Approver | Maximum window |
|-------------------------------------------|----------|----------------|
| Low | GRC | 180 days |
| Moderate | Security (or the accountable function leader) | 90 days |
| High | Security and Legal/Privacy jointly | 60 days |
| Breaches a hard limit in the appetite statement | Governing body | 30 days, with active remediation |

One approval per tier. A higher tier may approve a lower-tier exception; a lower tier may not
approve a higher-tier exception.

## 6. Exception register fields

The register is the system of record for open and closed exceptions. Each entry carries:

| Field | Meaning |
|-------|---------|
| id | Unique exception identifier. |
| control_or_policy | The control or policy being excepted (for example IAC-17). |
| requestor_function | The function that raised it. |
| reason | The business need and why the control cannot currently be met. |
| residual_risk | Score after the compensating control, in the FAIR bands. |
| compensating_control | The measure reducing risk while the gap is open. |
| approver_function | Who accepted the residual risk. |
| approved_on | Approval date. |
| expires_on | Hard expiry. |
| remediation_owner | The function closing the underlying gap. |
| status | open, expired, or closed. |
| framework_impact | Frameworks affected, for crosswalk and audit visibility. |

## 7. GitHub-native mechanism

The process runs in the same operating model as the rest of the program:

- An exception request is a GitHub Issue with an `exception` label and the fields above.
- The risk score and compensating control are added by GRC in the Issue.
- Approval is a Pull Request that adds the exception to the register; the merge is the
  authorization, and Git history records who approved what and when.
- A scheduled check reads expiry dates and opens a reminder Issue ahead of expiry, then flags
  any exception past expiry as a drift item.
- The register and its history are the due-diligence record an auditor samples.

## 8. Service levels

| Step | Target |
|------|--------|
| Triage after request | 2 business days |
| Risk assessment | 3 business days |
| Approval decision | 5 business days from a complete request |
| Reminder before expiry | 14 days |
| Escalation of an expired, still-open exception | next business day |

## 9. Metrics

- Count of open exceptions by risk tier and by owning function.
- Average age of open exceptions and count past expiry.
- Exceptions that breached a hard limit, with governing-body decisions.
- Closure rate against target remediation dates.

These feed the Security Steering Committee per
`committee-charter.md`. Rising exception age is treated as a program signal, not a clerical
detail.
