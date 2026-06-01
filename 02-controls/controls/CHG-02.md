# CHG-02: Configuration change control

> Defined once in [`control-library.yaml`](../control-library.yaml) and rendered into every framework through [`framework-crosswalk.yaml`](../framework-crosswalk.yaml) and the OSCAL profiles. The machine-readable form is [`control-library.oscal.json`](../control-library.oscal.json). Evidence is computed per [`evidence-schemas/CHG-02.yaml`](../evidence-schemas/CHG-02.yaml).

| Attribute | Value |
|-----------|-------|
| SCF domain | CHG (Change Management) |
| Class | SCF |
| NIST CSF function | Protect |
| Family | change management |
| Owner (by function) | Engineering (Security owns the policy) |
| Automation | automated |
| Review cadence | per change; policy and exceptions quarterly |

## Why this control

Change is a pillar of SOX IT general controls. In a source-control-native program, the pull request is the gate and the evidence is a byproduct of shipping, so the control is enforced by configuration rather than by reminder.

## Control statement

Technical configuration change reaches production only through a peer-reviewed pull request linked to a tracked work item, with required checks passing. Direct pushes to protected branches are blocked, the reviewer is independent of the author, and emergency changes follow a documented after-the-fact review.

## Implementation guidance

Make branch protection the technical enforcement of the policy rather than a written rule people are asked to follow. The protected production branch requires a pull request, at least one approving review from a reviewer who is not the author, a linked work item, and a passing set of required status checks. Direct pushes are blocked at the platform, so the bypass path does not exist rather than being discouraged. The evidence is the merge record pulled from the source-control API: the linked ticket, the independent reviewer, the passing checks, and the merge timestamp. This is collected, not reconstructed, and it is the same record that satisfies the SOX change assertion of segregation between the function that develops a change and the function that approves its release. Enforce that independence through code-owner rules so the approver cannot be the author. Provide an explicit emergency-change path for the rare case where a fix must ship before normal review. The emergency change is logged at the time, and it carries a documented after-the-fact review within the reconciliation window. Any change that reaches production outside the reviewed path is an exception that surfaces in the evidence with a closure path, so the exception rate is visible rather than hidden.

## Parameters

These are the assignable values the control is tuned with. They are set for the example configuration and are adjusted per environment.

| Parameter | Value | Guidance |
|-----------|-------|----------|
| Minimum independent approvals | 1 (reviewer not equal to author) | Required approving reviews on a protected-branch pull request, none from the author. |
| Protected branches | production release branches | Branches where direct pushes are blocked and the reviewed-PR gate is enforced. |
| Required status checks | build, automated tests, and security checks must pass | Checks that must pass before merge is permitted; failing checks block the merge. |
| Emergency-change review window | 3 business days | Maximum time from an emergency change to its documented after-the-fact review. |

## Control enhancements

- **CHG-02(1) Branch protection blocks direct pushes.** The protected production branch rejects direct pushes so change can reach production only through a reviewed pull request.
- **CHG-02(2) Independent review for segregation of duties.** At least one approving reviewer is not the author, enforced through code-owner rules, satisfying the SOX change-segregation assertion.
- **CHG-02(3) Work-item linkage per change.** Each merged change links to a tracked work item so the reason for the change is recorded.
- **CHG-02(4) Emergency-change after-the-fact review.** Emergency changes are logged at the time and reviewed within the reconciliation window.

## Assessment objectives

The control operates effectively when an assessor can determine that:

1. Production changes reached production only through a reviewed, ticket-linked pull request with passing checks.
2. Direct pushes to protected branches were blocked.
3. The approving reviewer was independent of the author.
4. Each emergency change was reconciled by an after-the-fact review within the window.

## Assessment methods

**Examine**

- The branch-protection configuration, the code-owner rules, and the required-checks configuration for the protected branch.
- The emergency-change log and the after-the-fact reviews for the period.

**Interview**

- Security on the change policy and the emergency-change path.
- Engineering on merge discipline and how independence is enforced.
- IT on locking the CI/CD identity and check configuration against bypass.

**Test**

- Attempt a direct push to the protected branch and confirm it is blocked.
- Sample merges and confirm a linked work item, an independent reviewer, and passing checks for each.
- Reconcile each emergency change to a documented after-the-fact review within the window.

## Evidence

Source-control merge record: linked work item, independent reviewer, passing checks, merge timestamp, direct pushes blocked, and exceptions without review.

- Record shape: [`evidence-schemas/CHG-02.yaml`](../evidence-schemas/CHG-02.yaml)
- Collection: computed
- `ai_generated`: false. Evidence is computed from a system of record; model-authored evidence is rejected by schema.

**Automation and CI mapping**

- Health check: A scheduled job queries the merge API for the protected production branch and computes: merges to production, merges with a linked ticket, merges with an independent reviewer, direct pushes blocked, and exceptions without review.
- Drift Issue: Any merge without an independent reviewer or a linked ticket, or any exception without a closure path, opens an Issue tagged CHG-02 naming Engineering as owner with the SOX ITGC change pillar flagged.
- Workflow: `.github/workflows/control-drift-monitor.yml`

## Framework crosswalk

One control, every framework it satisfies. References are real and are kept in lineage with the crosswalk.

| Framework | References | Basis |
|-----------|------------|-------|
| SOC 2 (TSC 2017) | CC3.4, CC8.1 | framework-mapped |
| ISO/IEC 27002:2022 | 8.19, 8.32 | framework-mapped |
| NIST CSF 2.0 | ID.RA-07 | framework-mapped |
| SOX ITGC | Change management, segregation of dev and approver | framework-mapped, home lab (never audited) |

## RACI asks by audience

The same control rendered into what each function is accountable, responsible, consulted, or informed for.

| Audience | RACI | Ask |
|----------|------|-----|
| Engineering | R | Merge only via a reviewed PR linked to a ticket. The PR is the evidence. |
| Security | A | Own the branch-protection policy and the emergency-change path; reconcile the one un-reviewed exception this period. |
| IT | C | Keep the CI/CD identity and check configuration locked so the gate cannot be bypassed. |
| Auditor | I | Receive the computed merge log; no screenshots of individual PRs. |
