# Tests for the access review policy (IAC-17).
# Run with: opa test policy/ -v

package compliance.access_review_test

import data.compliance.access_review
import rego.v1

# A clean cycle, full coverage and no open findings, may sign off.
test_allow_clean_cycle if {
	access_review.allow with input as {
		"campaign": "2026-Q2",
		"accounts_in_scope": 412,
		"accounts_reviewed": 412,
		"accounts_overdue": 0,
		"orphaned_accounts": 0,
		"orphaned_with_exception": 0,
		"service_accounts_in_scope": 38,
		"service_accounts_reviewed": 38,
		"leaver_deprovision_breaches": 0,
		"sod_conflicts_open": 0,
	}
}

# A cycle with overdue accounts and an uncovered orphan cannot sign off.
test_deny_overdue_and_orphan if {
	not access_review.allow with input as {
		"campaign": "2026-Q3",
		"accounts_in_scope": 412,
		"accounts_reviewed": 405,
		"accounts_overdue": 7,
		"orphaned_accounts": 3,
		"orphaned_with_exception": 1,
		"service_accounts_in_scope": 38,
		"service_accounts_reviewed": 36,
		"leaver_deprovision_breaches": 2,
		"sod_conflicts_open": 1,
	}
}

# An unresolved segregation-of-duties conflict alone blocks sign-off.
test_deny_open_sod_conflict if {
	not access_review.allow with input as {
		"campaign": "2026-Q3",
		"accounts_in_scope": 100,
		"accounts_reviewed": 100,
		"accounts_overdue": 0,
		"orphaned_accounts": 0,
		"orphaned_with_exception": 0,
		"service_accounts_in_scope": 10,
		"service_accounts_reviewed": 10,
		"leaver_deprovision_breaches": 0,
		"sod_conflicts_open": 1,
	}
}
