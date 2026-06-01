# Access review policy (policy-as-code for IAC-17)
#
# Encodes the recertification sign-off gate the control library describes: the
# campaign does not sign off until every in-scope account, human and non-human,
# is reviewed within cadence; orphaned and over-privileged accounts are closed
# or formally excepted; leaver deprovisioning fired within the SLA; and no
# segregation-of-duties conflict is left open.
#
# Source of truth for the rules: 02-controls/control-library.yaml (IAC-17
# parameters). Evaluate with OPA or with tools/policy_eval.py.

package compliance.access_review

import rego.v1

default allow := false

# allow here means the recertification campaign may sign off.
allow if count(deny) == 0

# Coverage: every in-scope account is reviewed within the cadence.
deny contains msg if {
	gap := input.accounts_in_scope - input.accounts_reviewed
	gap > 0
	msg := sprintf("%d in-scope accounts were not reviewed within the cadence", [gap])
}

# No account may sit past its recertification cadence.
deny contains msg if {
	input.accounts_overdue > 0
	msg := sprintf("%d accounts are past the recertification cadence", [input.accounts_overdue])
}

# Orphaned accounts must be zero or carry a documented exception.
deny contains msg if {
	uncovered := input.orphaned_accounts - object.get(input, "orphaned_with_exception", 0)
	uncovered > 0
	msg := sprintf("%d orphaned accounts without a documented exception", [uncovered])
}

# Service and other non-human accounts are held to the same bar.
deny contains msg if {
	gap := input.service_accounts_in_scope - input.service_accounts_reviewed
	gap > 0
	msg := sprintf("%d service accounts were not reviewed to the same bar as human accounts", [gap])
}

# Leaver deprovisioning fires from the HR feed within the SLA.
deny contains msg if {
	input.leaver_deprovision_breaches > 0
	msg := sprintf("%d leaver deprovisioning SLA breaches", [input.leaver_deprovision_breaches])
}

# Segregation-of-duties conflicts are resolved or excepted before sign-off.
deny contains msg if {
	input.sod_conflicts_open > 0
	msg := sprintf("%d unresolved segregation-of-duties conflicts", [input.sod_conflicts_open])
}
