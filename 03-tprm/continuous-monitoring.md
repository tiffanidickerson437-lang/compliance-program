# Continuous Monitoring (Third Parties)

**Pillar:** 03-tprm
**Control anchor:** [`TPM-01`](../02-controls/control-library.yaml), Third-party management, joined to [`MON-01`](../02-controls/control-library.yaml), Continuous monitoring
**Owner (function):** GRC (accountable). Security on rating signals. Procurement on renewal dates.
**Depends on:** [`vendor-tiering-model.md`](./vendor-tiering-model.md), [`tier1-deep-review.md`](./tier1-deep-review.md), [`attestation-reuse-register.yaml`](./attestation-reuse-register.yaml)

## Purpose

A point-in-time assessment proves posture on the day it was signed. Continuous monitoring closes the gap between that signed attestation and what a vendor's posture actually looks like the rest of the year. Reviews run on a tier-driven cadence and are cross-referenced against live security ratings, so drift between what a vendor attested and what is observable is caught and recorded, not discovered at the next renewal.

## The drift this catches

| Attested state | Observable drift | Signal |
|----------------|------------------|--------|
| Clean SOC 2, no exceptions | Security rating drops on exposed services or expired certificates | Rating feed |
| Subprocessor list fixed at assessment | New subprocessor touching restricted data appears | Subprocessor-change notice or trust-center diff |
| Certificate in force | Certificate lapses or report goes stale beyond currency window | Expiry tracking |
| Breach-notice commitment in contract | Public breach disclosure naming the vendor | Breach feed |
| Model-provider no-train term | Terms-of-service change to data-use or retention | Terms-change notice |

When attested and observable diverge, the divergence is the finding.

## Tier-driven cadence

| Tier | Scheduled reassessment | Security-rating cross-reference | Attestation refresh |
|------|------------------------|---------------------------------|---------------------|
| Tier 1 | Quarterly, plus event-driven | Continuous (daily rating poll) | Annual report, bridge letter for any gap |
| Tier 2 | Annual, plus event-driven | Weekly rating poll | Annual report |
| Tier 3 | Every 18 to 24 months | Monthly rating poll | At renewal |
| Tier 4 | At renewal only | Quarterly screen | At renewal if offered |

Event-driven review overrides the schedule. A rating drop, breach disclosure, subprocessor change, or material terms change pulls a vendor into off-cycle review regardless of tier.

## How the cross-reference works

1. A daily check pulls security-rating signals for monitored vendors from configured feeds.
2. The signal is joined to the vendor's record: tier, last assessment, attestation currency, subprocessor list.
3. A rule set compares observable posture to the attested baseline. A material divergence, an expiring attestation, or a new restricted-data subprocessor trips the rule.
4. A tripped rule opens a GitHub Issue labeled `evidence`. That Issue is the evidence of due diligence: it records the vendor, the drift type, the tier, the framework impact, and the evidence needed to close.
5. AI drafts the remediation narrative and proposes next steps. A human GRC owner reviews. The resolution lands through a pull request, and the merge updates the vendor's status. Git history is the audit trail.

This is the `MON-01` drift-opens-an-issue mechanism applied to third parties. The same automation pattern is wired in `.github/workflows/control-drift-monitor.yml`.

## Subprocessor and trust-center reconciliation

The published subprocessor list and the internal third-party register are reconciled on cadence. A subprocessor that appears internally but not publicly, or publicly but not internally, opens an Issue. For this configuration, Tier 1 subprocessors that touch precise location or children's data are reconciled against the public trust center every cycle so the customer-facing list and the internal tier never diverge. Trust-center generation is owned in 06-evidence-and-audit; this pillar supplies the vendor truth it renders.

## Concentration and fourth-party risk

Monitoring tracks where many Tier 1 services depend on the same upstream subprocessor or model provider. Concentration is a continuity and blast-radius signal, surfaced to risk management for the register, not a reason to re-tier a single vendor on its own. The fourth-party note maps each Tier 1 vendor's critical subprocessors so concentration is visible before an upstream outage makes it visible.

## What gets recorded

Each monitoring cycle produces a computed record, never an authored one:

- Vendors monitored, by tier.
- Rating signals ingested and divergences flagged.
- Issues opened for drift, and Issues closed by merged pull requests.
- Attestations expiring inside the next cycle.
- Reassessments due and overdue.

Overdue reassessments are exceptions with a closure path, consistent with the `TPM-01` example evidence. The record is `ai_generated: false`; AI drafts narrative, it does not author evidence.

## Framework mapping

| Framework | Reference |
|-----------|-----------|
| SOC 2 (TSC 2017) | CC2.3, CC7.2, CC9.2 |
| ISO/IEC 27002:2022 | 5.19, 5.22, 8.16 |
| NIST CSF 2.0 | GV.SC-07, GV.SC-08, DE.CM-09 |
| NIST AI RMF 1.0 | MANAGE 3.0, MEASURE 2.0 |
