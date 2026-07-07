#!/usr/bin/env python3
"""FAIR Monte Carlo simulator: loss-exceedance curve + ALE percentiles.

Reads the FAIR-structured risk register at 01-risk-management/risk-register.yaml
and runs a Monte Carlo simulation (default 10,000 iterations) over each risk
scenario and over the portfolio (the per-iteration sum across risks):

    LEF = TEF x Vulnerability          (loss events / year)
    LM  = Primary Loss + Secondary Loss (USD per event)
    ALE = LEF x LM                      (USD / year)

Each {min, most_likely, max} triple in the register is treated as a calibrated
expert estimate and mapped to a BetaPERT distribution (the standard FAIR
practice: a Beta distribution stretched over [min, max] whose mode is the
most-likely value). Vulnerability is a point estimate in the register and is
passed through as a constant probability.

Outputs, per risk and portfolio-wide, printed to stdout AND written to
generated/fair-simulation-report.md:

  * ALE percentiles p50 / p90 / p95 (plus mean for context)
  * A loss-exceedance curve: P(annualized loss >= $X) at a ladder of
    probability levels, phrased probabilistically ("10% chance of >= $X/yr")

FAIR results are distributions, never a single "exact" number, and this tool
never averages qualitative labels; the qualitative `band` fields in the
register are ignored by the math and reported only as input context.

Run:

    python3 tools/fair_montecarlo.py                 # defaults to the register
    python3 tools/fair_montecarlo.py --register path/to/register.yaml
    python3 tools/fair_montecarlo.py --iterations 50000 --seed 7

Dependencies: numpy, scipy (pip install numpy scipy) and PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required. Install it with: pip install pyyaml\n")
    raise SystemExit(2)

try:
    import numpy as np
    from scipy import stats
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "numpy and scipy are required for the Monte Carlo simulation.\n"
        "Install them with: pip install numpy scipy\n"
    )
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTER = REPO_ROOT / "01-risk-management" / "risk-register.yaml"
DEFAULT_REPORT = REPO_ROOT / "generated" / "fair-simulation-report.md"

# PERT shape parameter (lambda). 4 is the conventional default: it weights the
# most-likely value as four "virtual observations" relative to the endpoints.
PERT_LAMBDA = 4.0

# Exceedance ladder for the printed loss-exceedance curve.
EXCEEDANCE_PROBS = [0.99, 0.95, 0.90, 0.75, 0.50, 0.25, 0.10, 0.05, 0.01]


def pert_samples(rng: np.random.Generator, low: float, mode: float, high: float, n: int) -> np.ndarray:
    """Sample n draws from a BetaPERT(low, mode, high) distribution."""
    if high < low:
        raise ValueError(f"PERT bounds inverted: min={low} > max={high}")
    if not (low <= mode <= high):
        raise ValueError(f"PERT mode {mode} outside [{low}, {high}]")
    if high == low:
        return np.full(n, float(low))
    alpha = 1.0 + PERT_LAMBDA * (mode - low) / (high - low)
    beta = 1.0 + PERT_LAMBDA * (high - mode) / (high - low)
    draws = stats.beta.rvs(alpha, beta, size=n, random_state=rng)
    return low + draws * (high - low)


def triple(node: dict, context: str) -> tuple[float, float, float]:
    """Extract a {min, most_likely, max} triple, failing loudly if absent."""
    try:
        return float(node["min"]), float(node["most_likely"]), float(node["max"])
    except (KeyError, TypeError) as exc:
        raise ValueError(f"{context}: expected min/most_likely/max, got {node!r}") from exc


def simulate_risk(risk: dict, rng: np.random.Generator, iterations: int) -> np.ndarray:
    """Return an array of simulated annualized losses (USD/yr) for one risk."""
    rid = risk.get("id", "<unknown>")

    tef = pert_samples(rng, *triple(risk["threat_event_frequency_per_year"], f"{rid} TEF"), n=iterations)

    vuln_node = risk.get("vulnerability", {})
    vuln = float(vuln_node.get("estimate", 1.0))  # point estimate -> constant
    lef = tef * vuln

    lm_node = risk["loss_magnitude_usd"]
    primary = pert_samples(rng, *triple(lm_node["primary"], f"{rid} primary loss"), n=iterations)
    secondary = pert_samples(rng, *triple(lm_node["secondary"], f"{rid} secondary loss"), n=iterations)
    lm = primary + secondary

    return lef * lm


def fmt_usd(x: float) -> str:
    return f"${x:,.0f}"


def percentile_block(ale: np.ndarray) -> dict[str, float]:
    p50, p90, p95 = np.percentile(ale, [50, 90, 95])
    return {"p50": float(p50), "p90": float(p90), "p95": float(p95), "mean": float(ale.mean())}


def exceedance_rows(ale: np.ndarray) -> list[tuple[float, float]]:
    """(probability, loss) pairs: probability chance annual loss >= loss."""
    rows = []
    for p in EXCEEDANCE_PROBS:
        loss = float(np.percentile(ale, 100 * (1 - p)))
        rows.append((p, loss))
    return rows


def render_section(name: str, title: str, ale: np.ndarray) -> str:
    pcts = percentile_block(ale)
    lines = [
        f"## {name} — {title}",
        "",
        "ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):",
        f"  p50: {fmt_usd(pcts['p50'])}/yr   p90: {fmt_usd(pcts['p90'])}/yr   p95: {fmt_usd(pcts['p95'])}/yr   (mean: {fmt_usd(pcts['mean'])}/yr)",
        "",
        "Loss-exceedance curve — P(loss >= $X) per year:",
    ]
    for p, loss in exceedance_rows(ale):
        lines.append(f"  {p * 100:5.1f}% chance of losses >= {fmt_usd(loss)}/yr")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER,
                        help=f"risk register YAML (default: {DEFAULT_REGISTER.relative_to(REPO_ROOT)})")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT,
                        help=f"markdown report output (default: {DEFAULT_REPORT.relative_to(REPO_ROOT)})")
    parser.add_argument("--iterations", type=int, default=10_000, help="Monte Carlo iterations (default 10000)")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducible runs")
    args = parser.parse_args()

    if not args.register.exists():
        sys.stderr.write(f"Risk register not found: {args.register}\n")
        return 2

    register = yaml.safe_load(args.register.read_text())
    risks = register.get("risks", [])
    if not risks:
        sys.stderr.write(f"No risks found in {args.register}\n")
        return 2

    rng = np.random.default_rng(args.seed)

    sections: list[str] = []
    portfolio = np.zeros(args.iterations)
    for risk in risks:
        ale = simulate_risk(risk, rng, args.iterations)
        portfolio += ale
        sections.append(render_section(risk["id"], risk.get("title", ""), ale))

    sections.append(render_section(
        "PORTFOLIO",
        f"per-iteration sum across {len(risks)} risks (scenarios sampled independently)",
        portfolio,
    ))

    header = (
        "# FAIR Monte Carlo Simulation\n\n"
        f"- Register: {args.register}\n"
        f"- Iterations: {args.iterations:,} per risk (BetaPERT sampling, lambda={PERT_LAMBDA:g}; "
        "vulnerability point estimates passed through as constants)\n"
        f"- Seed: {args.seed if args.seed is not None else 'not fixed (fresh entropy)'}\n"
        f"- Generated: {_dt.datetime.now(_dt.timezone.utc).isoformat(timespec='seconds')}\n\n"
        "FAIR outputs are distributions and probabilities. Read every figure as a\n"
        "percentile of a simulated distribution, never as an exact prediction. Inputs\n"
        "are the register's calibrated estimates (illustrative basis; see the register\n"
        "header). Qualitative bands in the register are context only — the simulation\n"
        "uses the quantitative ranges and never averages qualitative labels.\n"
    )

    body = header + "\n" + "\n".join(sections)
    print(body)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(body + "\n")
    print(f"Report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
