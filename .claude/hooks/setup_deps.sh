#!/usr/bin/env bash
# SessionStart (startup|resume): make sure the FAIR Monte Carlo deps exist.
# Idempotent fast path: import check first, install only on a miss.
# ALWAYS exits 0 — SessionStart hooks cannot block; they only report via stdout.
if python3 -c 'import numpy,scipy' 2>/dev/null; then
  echo "deps ok: numpy + scipy present"
else
  echo "installing numpy + scipy for tools/fair_montecarlo.py ..."
  pip install -q numpy scipy || echo "pip install failed; risk-sim runs will need numpy/scipy installed manually"
fi
exit 0
