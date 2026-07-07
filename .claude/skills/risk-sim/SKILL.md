---
name: risk-sim
description: Run the FAIR Monte Carlo simulation over the risk register and summarize loss-exceedance results in business terms. Use when asked to "run the risk sim", "quantify risk", "FAIR simulation", or "loss exceedance".
allowed-tools: Bash(python3:*)
---

# FAIR risk simulation

Run the FAIR Monte Carlo tool over the risk register and report the results.
The simulation is deterministic tooling over human-owned inputs; the register
itself (`01-risk-management/risk-register.yaml`) is authored by humans and
changed only by pull request — never edit it from this skill.

## Run

```
python3 tools/fair_montecarlo.py
```

The tool reads `01-risk-management/risk-register.yaml`. It requires numpy and
scipy; the SessionStart hook `.claude/hooks/setup_deps.sh` installs them if
missing. If `tools/fair_montecarlo.py` is not present on this branch yet, say
so and stop — do not create it or simulate results by hand.

## Report

- Present the tool's actual output numbers only. Never estimate, extrapolate,
  or round in a way the output does not support; a simulation number that was
  not printed does not exist.
- Frame results in business terms per the risk pillar: annualized loss
  exposure, loss exceedance at the percentiles the tool reports, and which
  register entries dominate the tail.
- Any recommendation (treatment, prioritization) is a draft for the risk
  owner; treatment decisions are recorded by humans via PR.
