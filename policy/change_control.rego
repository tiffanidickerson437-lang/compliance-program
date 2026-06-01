# Change control policy (policy-as-code for CHG-02)
#
# Encodes the production-change gate the control library describes: change
# reaches a protected branch only through a reviewed pull request linked to a
# tracked work item, with required checks passing and an approver independent of
# the author. Direct pushes are blocked. An emergency change may bypass review
# at merge time only when a documented after-the-fact review is committed.
#
# Source of truth for the rules: 02-controls/control-library.yaml (CHG-02
# parameters). Evaluate with OPA or with tools/policy_eval.py.

package compliance.change_control

import rego.v1

default allow := false

allow if count(deny) == 0

is_protected if input.protected == true

is_emergency if input.emergency == true

# Direct pushes to a protected branch are blocked at the platform.
deny contains msg if {
	is_protected
	input.direct_push == true
	msg := "direct push to a protected branch is blocked; change must arrive by reviewed pull request"
}

# Every production change links to a tracked work item.
deny contains msg if {
	is_protected
	not has_ticket
	msg := "no linked work item; each production change links to a tracked ticket"
}

has_ticket if {
	is_string(input.linked_ticket)
	input.linked_ticket != ""
}

# A non-emergency change requires an approving reviewer who is not the author.
deny contains msg if {
	is_protected
	not is_emergency
	count(independent_reviewers) < 1
	msg := "no independent approving review; the approver must not be the author"
}

independent_reviewers contains r if {
	some r in input.reviewers
	r != input.author
}

# A non-emergency change requires passing status checks.
deny contains msg if {
	is_protected
	not is_emergency
	input.checks_passed != true
	msg := "required status checks did not pass; failing checks block the merge"
}

# An emergency change must carry a documented after-the-fact review.
deny contains msg if {
	is_protected
	is_emergency
	not has_after_the_fact_review
	msg := "emergency change without a documented after-the-fact review within the reconciliation window"
}

has_after_the_fact_review if {
	is_string(input.after_the_fact_review)
	input.after_the_fact_review != ""
}
