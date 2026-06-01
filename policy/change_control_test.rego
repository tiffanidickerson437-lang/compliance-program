# Tests for the change control policy (CHG-02).
# Run with: opa test policy/ -v

package compliance.change_control_test

import data.compliance.change_control
import rego.v1

# A reviewed, ticket-linked merge with passing checks and an independent
# approver is allowed.
test_allow_reviewed_merge if {
	change_control.allow with input as {
		"target_branch": "main",
		"protected": true,
		"direct_push": false,
		"linked_ticket": "TCK-1421",
		"author": "engineer-a",
		"reviewers": ["engineer-b"],
		"checks_passed": true,
		"emergency": false,
	}
}

# A merge with no linked work item is denied.
test_deny_no_linked_ticket if {
	not change_control.allow with input as {
		"protected": true,
		"direct_push": false,
		"linked_ticket": "",
		"author": "engineer-a",
		"reviewers": ["engineer-b"],
		"checks_passed": true,
		"emergency": false,
	}
}

# A self-approved merge (reviewer equals author) is denied.
test_deny_self_review if {
	not change_control.allow with input as {
		"protected": true,
		"direct_push": false,
		"linked_ticket": "TCK-1422",
		"author": "engineer-a",
		"reviewers": ["engineer-a"],
		"checks_passed": true,
		"emergency": false,
	}
}

# A direct push to a protected branch is denied.
test_deny_direct_push if {
	not change_control.allow with input as {
		"protected": true,
		"direct_push": true,
		"linked_ticket": "TCK-1423",
		"author": "engineer-a",
		"reviewers": ["engineer-b"],
		"checks_passed": true,
		"emergency": false,
	}
}

# An emergency change with a documented after-the-fact review is allowed.
test_allow_emergency_with_review if {
	change_control.allow with input as {
		"protected": true,
		"direct_push": false,
		"linked_ticket": "TCK-1424",
		"author": "engineer-a",
		"reviewers": [],
		"checks_passed": false,
		"emergency": true,
		"after_the_fact_review": "PIR-2026-05-14",
	}
}

# An emergency change with no after-the-fact review is denied.
test_deny_emergency_without_review if {
	not change_control.allow with input as {
		"protected": true,
		"direct_push": false,
		"linked_ticket": "TCK-1425",
		"author": "engineer-a",
		"reviewers": [],
		"checks_passed": false,
		"emergency": true,
	}
}
