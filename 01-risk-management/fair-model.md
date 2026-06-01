# FAIR Model: How Quantification Is Applied

**Pillar:** 01-risk-management
**Owner:** GRC function (model); the business (decisions)
**Status:** Scaffold. Estimates are illustrative until calibrated with internal data in Phase 1.

---

## 1. Why FAIR

FAIR (Factor Analysis of Information Risk) expresses risk as money and probability instead of a
color on a heat map. That lets the board compare a location-exposure scenario to a change-
failure scenario on one axis, dollars per year, and lets risk, not the audit calendar, decide
what gets hardened next. The register in `risk-register.yaml` is structured to this model so
every scenario is quantified the same way.

## 2. The decomposition

Risk is broken into frequency and magnitude, and each is broken down further:

```
Risk (ALE)
├── Loss Event Frequency (LEF)              events per year
│   ├── Threat Event Frequency (TEF)        attempts per year
│   │   ├── Contact Frequency               how often the threat reaches the asset
│   │   └── Probability of Action           how often contact becomes an attempt
│   └── Vulnerability                       probability an attempt becomes a loss
│       ├── Threat Capability               how strong the threat is
│       └── Resistance Strength             how strong the control is
└── Loss Magnitude (LM)                     dollars per event
    ├── Primary Loss                        direct: response, investigation, restoration
    └── Secondary Loss                      fallout: fines and judgments, reputation,
                                            lost revenue, regulatory action
```

The two working equations:

- **Loss Event Frequency** = Threat Event Frequency x Vulnerability
- **Annualized Loss Exposure (ALE)** = Loss Event Frequency x Loss Magnitude

## 3. Forms of loss

Loss Magnitude is summed across the forms that actually apply to a scenario:

| Form | What it captures |
|------|------------------|
| Response | Incident handling, forensics, legal hours, communications. |
| Replacement / restoration | Restoring systems, data, or service. |
| Fines and judgments | Regulatory penalties and legal liability. |
| Reputation | Churn and acquisition drag from lost trust. |
| Lost revenue | Deals stalled or lost, downtime impact. |
| Regulatory action | Consent decrees, audits, mandated changes. |

For a consumer service holding precise location and children's data, the secondary loss
(reputation, regulatory action, lost revenue) usually dominates the primary loss. The model
makes that explicit instead of hiding it.

## 4. How estimates are made

Each factor is estimated as a calibrated range, not a single number:

- **min** (lower bound), **most_likely** (the mode), **max** (upper bound).
- Ranges express honest uncertainty. A wide range is a signal to gather better data, not a
  reason to avoid quantifying.
- A PERT or triangular distribution over the range, sampled with a Monte Carlo run, produces a
  loss-exposure distribution. The register records the min, most-likely, and max so the method
  is transparent without requiring the simulation tooling to read it.
- Estimates are calibrated against internal data where it exists and against public base rates
  where it does not. In this configuration every estimate is illustrative and tagged as such.

## 5. How the model maps to the register fields

| Register field | FAIR factor |
|----------------|-------------|
| `threat_event_frequency_per_year` | TEF |
| `vulnerability.estimate` | Vulnerability |
| `loss_event_frequency_per_year` | LEF = TEF x Vulnerability |
| `loss_magnitude_usd.primary` / `.secondary` | Primary and Secondary Loss |
| `annualized_loss_exposure_usd` | ALE = LEF x LM |
| `residual_risk.annualized_loss_exposure_usd` | ALE recomputed after treatment |
| `treatment.decision` | The business decision the ALE informs |

## 6. Worked example: RISK-001, precise-location exposure

Using the most-likely values from the register:

1. **Threat Event Frequency.** Location is a high-value target; attempts against APIs and
   tokens are frequent. TEF most-likely = **4 attempts/year**.
2. **Vulnerability.** With deny-by-default authorization and short-lived, purpose-bound agent
   tokens, most attempts are expected to fail. Vulnerability = **0.15**.
3. **Loss Event Frequency.** LEF = 4 x 0.15 = **0.6 loss events/year**.
4. **Loss Magnitude.** Primary (response, investigation, notification) most-likely =
   **\$900,000**. Secondary (fines and judgments, reputation, lost revenue, regulatory action)
   most-likely = **\$6,000,000**. LM = 900,000 + 6,000,000 = **\$6,900,000 per event**.
5. **Annualized Loss Exposure.** ALE = 0.6 x 6,900,000 = **\$4,140,000/year** (most-likely).
   The range runs from **\$125,000** (min LEF 0.1 x min LM 1,250,000) to **\$56,000,000** (max
   LEF 2.0 x max LM 28,000,000).
6. **Compare to appetite.** Precise-location exposure breaches a hard limit in
   `risk-appetite-statement.md`, so it is out of appetite by definition. The decision is
   **mitigate**, not accept.
7. **Recompute residual.** With AAT-01, MON-01, and IAC-17 operating, the residual ALE
   most-likely falls to **\$700,000/year**, inside appetite after treatment. The delta between
   inherent and residual ALE is the value the controls produce, stated in dollars.

The same seven steps run for every scenario in the register.

## 7. Applying appetite

Appetite turns an ALE into a decision. For each scenario:

- If the residual ALE sits inside the band for its category and breaches no hard limit, the
  business may accept it with a signature.
- If the residual ALE sits above the band, or the scenario breaches a hard limit, it requires
  treatment (mitigate, transfer, or avoid) or an explicit governing-body acceptance.
- The bands live in `risk-appetite-statement.md`; the business owns where they sit.

## 8. Running a new scenario

1. Name the scenario, the asset at risk, and the threat community.
2. Estimate TEF as a min / most-likely / max range, with a rationale.
3. Estimate Vulnerability with the current controls in place, with a rationale.
4. Compute LEF.
5. Estimate Primary and Secondary Loss across the forms that apply.
6. Compute ALE (inherent), then ALE (residual) after the proposed treatment.
7. Compare residual ALE to appetite, propose a treatment, and route the decision to the
   business owner to sign.
8. Add the scenario to `risk-register.yaml` and feed it into the NIST RMF steps per
   `nist-rmf-alignment.md`.

## 9. Calibration note

Every frequency and magnitude in this configuration is an illustrative estimate, not internal
data. Calibration with the business in Phase 1 replaces these
ranges with defensible ones. The model is sound before calibration; only the inputs change.
