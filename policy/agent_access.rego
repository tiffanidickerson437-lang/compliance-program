# Agent access policy (policy-as-code for AAT-01 and PRI-03.13)
#
# Encodes the authorization broker rules the control library describes in prose:
# no standing entitlement to sensitive data, purpose-bound and time-boxed grants
# within the TTL ceiling, active verifiable consent before any read of a minor's
# data, and a recorded human gate in front of high-impact actions. The default
# is deny; an allow is produced only when no rule objects.
#
# Source of truth for the thresholds: 02-controls/control-library.yaml (AAT-01
# parameters aat-01_prm_token_ttl_ceiling and aat-01_prm_human_gate_actions, and
# PRI-03.13 consent rules). Evaluate with OPA or with tools/policy_eval.py, which
# mirrors these rules when OPA is not installed.

package compliance.agent_access

import rego.v1

# Purpose-token time-to-live ceiling in seconds (AAT-01 parameter).
ttl_ceiling := 300

# Actions that stop for a recorded human gate (AAT-01 parameter).
high_impact_actions := {"location_disclosure", "action_on_minor_account", "irreversible_write"}

# Data classes that may only be read through a brokered, time-boxed grant.
sensitive_classes := {"precise-location", "minor-data"}

default allow := false

allow if count(deny) == 0

is_sensitive if input.data_class in sensitive_classes

touches_minor if input.data_class == "minor-data"

touches_minor if input.subject_is_minor == true

# Standing access to sensitive data is never permitted; access is brokered per
# request and expires automatically.
deny contains msg if {
	is_sensitive
	input.standing_access == true
	msg := sprintf("standing entitlement to %s is not permitted; access must be brokered per request", [input.data_class])
}

# A sensitive read must carry a finite, time-boxed purpose token.
deny contains msg if {
	is_sensitive
	not positive_ttl
	msg := "sensitive read has no positive purpose-token TTL; grants must be time-boxed"
}

positive_ttl if {
	is_number(input.token_ttl_seconds)
	input.token_ttl_seconds > 0
}

# The grant must not outlive the TTL ceiling.
deny contains msg if {
	is_sensitive
	is_number(input.token_ttl_seconds)
	input.token_ttl_seconds > ttl_ceiling
	msg := sprintf("token TTL %ds exceeds the %ds ceiling", [input.token_ttl_seconds, ttl_ceiling])
}

# A sensitive read must be bound to a declared purpose.
deny contains msg if {
	is_sensitive
	not has_purpose
	msg := "no declared purpose; access to sensitive data must be purpose-bound"
}

has_purpose if {
	is_string(input.purpose)
	input.purpose != ""
}

# A minor's data may be processed or disclosed only under active verifiable
# parental consent (PRI-03.13).
deny contains msg if {
	touches_minor
	input.consent_state != "active"
	msg := sprintf("consent is %v; processing or disclosure of a minor's data is denied without active verifiable parental consent", [object.get(input, "consent_state", "absent")])
}

# A high-impact action requires a recorded, satisfied human gate (AAT-01).
deny contains msg if {
	input.action in high_impact_actions
	input.human_gate != "satisfied"
	msg := sprintf("%s requires a recorded human gate; gate state is %v", [input.action, object.get(input, "human_gate", "missing")])
}
