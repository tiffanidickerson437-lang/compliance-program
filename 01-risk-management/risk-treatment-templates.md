# Risk Treatment Templates

**Pillar:** 01-risk-management
**Owner:** GRC function (templates); the business (the decision)
**Status:** Scaffold.

---

## 1. Purpose

Every scenario in `risk-register.yaml` ends in one of four treatments: accept, mitigate,
transfer, or avoid. This file gives one template for each so the decision is recorded the same
way every time, with the same fields, the same signature line, and the same path into the
register and the audit trail. GRC supplies the option and the quantified residual; the business
signs.

## 2. The four treatments

| Treatment | What it means | When it fits |
|-----------|---------------|--------------|
| Accept | Take no further action; carry the residual risk knowingly. | Residual ALE is inside appetite and no hard limit is breached. |
| Mitigate | Apply or strengthen controls to reduce frequency or magnitude. | Residual ALE is above appetite and controls can move it. |
| Transfer | Shift financial exposure to a third party (insurance, contract). | Residual remains after mitigation and can be priced and moved. |
| Avoid | Stop or change the activity that creates the risk. | The risk cannot be brought inside appetite at acceptable cost. |

Treatments combine. Many scenarios mitigate first and transfer the residual, as RISK-004 does.

## 3. Choosing a treatment

1. Read the inherent ALE from the register.
2. Check appetite. A hard-limit breach removes "accept" as an option at the working level.
3. Model the residual ALE under each candidate treatment.
4. Compare the cost of the treatment to the reduction in ALE it buys.
5. Recommend the treatment with the best risk-reduction-per-dollar that brings residual inside
   appetite, and route it to the business owner to sign.

The decision is the business's. GRC does not accept risk on the business's behalf.

## 4. Template: Accept (risk acceptance)

```
RISK ACCEPTANCE
  risk_id:               <RISK-00X>
  scenario:              <one line>
  residual_ale_usd:      min / most_likely / max
  appetite_alignment:    within-appetite        # must be true to accept at working level
  rationale:             <why accepting is the right call>
  compensating_context:  <existing controls that hold the residual>
  accepted_by_function:  <business owner that signs>
  approval_authority:    <per exceptions-process.md tier>
  accepted_on:           <date>
  review_on:             <date; acceptance is time-bound>
  recorded_in:           risk-register.yaml + Git history
```

An acceptance that would breach a hard limit cannot be signed at the working level; it
escalates to the governing body or the activity is avoided.

## 5. Template: Mitigate

```
RISK MITIGATION
  risk_id:               <RISK-00X>
  scenario:              <one line>
  inherent_ale_usd:      min / most_likely / max
  target_residual_ale:   min / most_likely / max
  controls_applied:      [<control IDs from 02-controls>]
  actions:
    - <specific action, owner function, due date>
  treatment_cost_est:    <one-time and run-rate>
  accountable_function:  <runs the treatment>
  risk_owner:            <business owner that signs>
  verification:          <evidence schema / check that confirms the residual>
  review_on:             <date>
  recorded_in:           risk-register.yaml + remediation backlog
```

Mitigation links to controls already defined once in the library. The verification is the
computed evidence that the residual was actually achieved, not an assertion that it was.

## 6. Template: Transfer

```
RISK TRANSFER
  risk_id:               <RISK-00X>
  scenario:              <one line>
  residual_after_mitigation_ale_usd: min / most_likely / max
  transfer_mechanism:    <cyber insurance | contractual indemnity | warranty>
  counterparty:          <insurer or counterparty function>
  coverage_scope:        <what is covered and the limit>
  exclusions:            <what is not covered; the retained residual>
  retained_residual_ale: min / most_likely / max
  cost:                  <premium or contractual cost>
  legal_review:          <Legal sign-off on terms>
  risk_owner:            <business owner that signs>
  review_on:             <renewal date>
  recorded_in:           risk-register.yaml + contract register
```

Transfer moves financial exposure, not accountability. The obligation to protect the data
remains with the company; insurance pays some of the loss, it does not remove the duty.

## 7. Template: Avoid

```
RISK AVOIDANCE
  risk_id:               <RISK-00X>
  scenario:              <one line>
  inherent_ale_usd:      min / most_likely / max
  activity_changed:      <the feature, integration, or data flow stopped or redesigned>
  business_impact:       <revenue, roadmap, or capability given up>
  alternative:           <the safer path chosen instead, if any>
  decided_by_function:   <business owner that signs; governing body if material>
  decided_on:            <date>
  recorded_in:           risk-register.yaml + product decision log
```

Avoidance is a real option, not a last resort. For a hard-limit risk that cannot be brought
inside appetite, changing the activity is the correct treatment.

## 8. From template to record

- The chosen template is filled in a Pull Request that updates the scenario's `treatment` and
  `residual_risk` in `risk-register.yaml`.
- The business owner approves the Pull Request; the merge is the authorization, and Git history
  records who signed and when.
- For an accept that is really a deviation from a control, the exception process in
  `00-governance/exceptions-process.md` applies, with its expiry and register.
- Treatment status and residual exposure feed the committee reporting in `committee-charter.md`.
