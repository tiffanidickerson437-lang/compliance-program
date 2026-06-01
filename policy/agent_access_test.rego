# Tests for the agent access policy (AAT-01 and PRI-03.13).
# Run with: opa test policy/ -v

package compliance.agent_access_test

import data.compliance.agent_access
import rego.v1

# A brokered safety-event read with active consent, a finite TTL within the
# ceiling, a declared purpose, and a satisfied human gate is allowed.
test_allow_brokered_safety_event if {
	agent_access.allow with input as {
		"agent_id": "safety-alert-agent",
		"data_class": "precise-location",
		"subject_is_minor": true,
		"purpose": "crash_detection_high_confidence",
		"standing_access": false,
		"token_ttl_seconds": 120,
		"consent_state": "active",
		"action": "location_disclosure",
		"human_gate": "satisfied",
	}
}

# Standing access to sensitive data is denied.
test_deny_standing_entitlement if {
	not agent_access.allow with input as {
		"agent_id": "analytics-agent",
		"data_class": "precise-location",
		"purpose": "analytics",
		"standing_access": true,
		"token_ttl_seconds": 120,
		"consent_state": "active",
	}
}

# Withdrawn consent denies a read of a minor's data.
test_deny_withdrawn_consent_for_minor if {
	not agent_access.allow with input as {
		"agent_id": "safety-alert-agent",
		"data_class": "minor-data",
		"subject_is_minor": true,
		"purpose": "crash_detection_high_confidence",
		"standing_access": false,
		"token_ttl_seconds": 120,
		"consent_state": "withdrawn",
	}
}

# A high-impact action without a satisfied human gate is denied.
test_deny_minor_action_without_human_gate if {
	not agent_access.allow with input as {
		"agent_id": "safety-alert-agent",
		"data_class": "minor-data",
		"subject_is_minor": true,
		"purpose": "account_action",
		"standing_access": false,
		"token_ttl_seconds": 120,
		"consent_state": "active",
		"action": "action_on_minor_account",
		"human_gate": "pending",
	}
}

# A TTL above the ceiling is denied.
test_deny_ttl_over_ceiling if {
	not agent_access.allow with input as {
		"agent_id": "safety-alert-agent",
		"data_class": "precise-location",
		"purpose": "crash_detection_high_confidence",
		"standing_access": false,
		"token_ttl_seconds": 3600,
		"consent_state": "active",
	}
}
