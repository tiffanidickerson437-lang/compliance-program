# FAIR Monte Carlo Simulation

- Register: /Users/tiffanidickerson/Downloads/_CLAUDE/HEX/_work/compliance-program/.claude/worktrees/wf_74235c0b-902-1/01-risk-management/risk-register.yaml
- Iterations: 10,000 per risk (BetaPERT sampling, lambda=4; vulnerability point estimates passed through as constants)
- Seed: not fixed (fresh entropy)
- Generated: 2026-07-07T02:13:17+00:00

FAIR outputs are distributions and probabilities. Read every figure as a
percentile of a simulated distribution, never as an exact prediction. Inputs
are the register's calibrated estimates (illustrative basis; see the register
header). Qualitative bands in the register are context only — the simulation
uses the quantitative ranges and never averages qualitative labels.

## RISK-001 — Precise-location exposure of members

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $5,898,985/yr   p90: $12,822,576/yr   p95: $15,210,138/yr   (mean: $6,896,985/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $1,086,982/yr
   95.0% chance of losses >= $1,801,316/yr
   90.0% chance of losses >= $2,370,932/yr
   75.0% chance of losses >= $3,647,980/yr
   50.0% chance of losses >= $5,898,985/yr
   25.0% chance of losses >= $9,179,656/yr
   10.0% chance of losses >= $12,822,576/yr
    5.0% chance of losses >= $15,210,138/yr
    1.0% chance of losses >= $20,900,589/yr

## RISK-002 — Processing minors' data without verifiable parental consent

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $8,330,693/yr   p90: $17,860,844/yr   p95: $21,230,379/yr   (mean: $9,658,014/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $1,645,511/yr
   95.0% chance of losses >= $2,622,607/yr
   90.0% chance of losses >= $3,402,765/yr
   75.0% chance of losses >= $5,249,792/yr
   50.0% chance of losses >= $8,330,693/yr
   25.0% chance of losses >= $12,668,169/yr
   10.0% chance of losses >= $17,860,844/yr
    5.0% chance of losses >= $21,230,379/yr
    1.0% chance of losses >= $28,536,733/yr

## RISK-003 — Agentic AI acts out of scope on the location graph

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $10,683,984/yr   p90: $24,365,085/yr   p95: $29,271,547/yr   (mean: $12,793,778/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $1,695,269/yr
   95.0% chance of losses >= $3,029,106/yr
   90.0% chance of losses >= $4,073,099/yr
   75.0% chance of losses >= $6,525,426/yr
   50.0% chance of losses >= $10,683,984/yr
   25.0% chance of losses >= $17,017,280/yr
   10.0% chance of losses >= $24,365,085/yr
    5.0% chance of losses >= $29,271,547/yr
    1.0% chance of losses >= $40,991,844/yr

## RISK-004 — Vendor or subprocessor breach exposing sensitive data

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $4,200,432/yr   p90: $8,723,712/yr   p95: $10,217,430/yr   (mean: $4,776,813/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $836,609/yr
   95.0% chance of losses >= $1,314,827/yr
   90.0% chance of losses >= $1,681,815/yr
   75.0% chance of losses >= $2,597,211/yr
   50.0% chance of losses >= $4,200,432/yr
   25.0% chance of losses >= $6,350,966/yr
   10.0% chance of losses >= $8,723,712/yr
    5.0% chance of losses >= $10,217,430/yr
    1.0% chance of losses >= $13,757,349/yr

## RISK-005 — Unauthorized or unreviewed production change

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $3,010,616/yr   p90: $6,737,951/yr   p95: $8,082,315/yr   (mean: $3,567,159/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $533,618/yr
   95.0% chance of losses >= $916,165/yr
   90.0% chance of losses >= $1,190,485/yr
   75.0% chance of losses >= $1,893,394/yr
   50.0% chance of losses >= $3,010,616/yr
   25.0% chance of losses >= $4,685,012/yr
   10.0% chance of losses >= $6,737,951/yr
    5.0% chance of losses >= $8,082,315/yr
    1.0% chance of losses >= $10,953,745/yr

## RISK-006 — Access not removed at role change or departure

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $3,895,439/yr   p90: $8,362,811/yr   p95: $10,109,582/yr   (mean: $4,525,741/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $708,902/yr
   95.0% chance of losses >= $1,157,770/yr
   90.0% chance of losses >= $1,512,549/yr
   75.0% chance of losses >= $2,372,116/yr
   50.0% chance of losses >= $3,895,439/yr
   25.0% chance of losses >= $6,066,099/yr
   10.0% chance of losses >= $8,362,811/yr
    5.0% chance of losses >= $10,109,582/yr
    1.0% chance of losses >= $13,695,346/yr

## PORTFOLIO — per-iteration sum across 6 risks (scenarios sampled independently)

ALE percentiles (annualized loss exposure, USD/yr — a distribution, not a point estimate):
  p50: $40,716,588/yr   p90: $58,603,685/yr   p95: $64,782,497/yr   (mean: $42,218,489/yr)

Loss-exceedance curve — P(loss >= $X) per year:
   99.0% chance of losses >= $20,094,942/yr
   95.0% chance of losses >= $24,834,346/yr
   90.0% chance of losses >= $27,889,320/yr
   75.0% chance of losses >= $33,423,100/yr
   50.0% chance of losses >= $40,716,588/yr
   25.0% chance of losses >= $49,436,378/yr
   10.0% chance of losses >= $58,603,685/yr
    5.0% chance of losses >= $64,782,497/yr
    1.0% chance of losses >= $76,641,621/yr

