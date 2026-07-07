# MCP Evidence Gateway Security Note

The repo-root `.mcp.json` declares one MCP gateway per system of record named
in `02-controls/control-library.yaml` (`ci_mapping` / evidence `source`
fields): `jira-evidence` (ticket + incident tracker), `aws-evidence` (cloud
provider inventory), `github-evidence` (branch protection + merge API). The
config is project-scoped so it travels with the repo when an auditor clones
it. `tools/mcp_gateways.py` is the only resolver; the drift monitor consumes
it through `tools/check_control_health.py`.

## Posture (enforced in code or config, not aspiration)

1. **Streamable HTTP transport only, never stdio.** Every server in
   `.mcp.json` is `type: http`. The resolver refuses any server carrying a
   `command` (stdio) entry.
2. **OBO OAuth, one client per user.** Each gateway authenticates
   on-behalf-of the running user with a bearer token from an environment
   variable (`JIRA_MCP_OAUTH_TOKEN`, `AWS_MCP_OAUTH_TOKEN`,
   `GITHUB_MCP_OAUTH_TOKEN`). Never reuse one OAuth client ID across users;
   each operator registers their own client with the gateway's IdP.
3. **No token forwarding.** A token is sent only to its own gateway
   (`Authorization` header on that gateway's URL) and is never forwarded to
   any downstream system. The resolver has no code path that attaches one
   gateway's token to another host.
4. **SSRF validation.** `mcp_gateways.validate_gateway_url` requires HTTPS
   and resolves the host, rejecting loopback, RFC 1918 private ranges,
   link-local (which includes the 169.254.169.254 cloud-metadata endpoint),
   reserved ranges, and metadata hostnames (`metadata.google.internal`,
   `*.internal`, `*.local`). Any URL configured for a gateway — including an
   OAuth discovery endpoint, if one is configured as the gateway URL — must
   pass this same validator before it is contacted.
5. **No live credentials in the repo.** Tokens come only from the
   environment (repository secrets in CI). When absent, the check falls back
   to the committed drift-signals fixture — the supported degraded mode.
6. **Reads are automated; every write is human-in-the-loop.** The gateway
   code in this repo is read-only (drift signals): no MCP write path exists.
   Policy for any future MCP write — creating a ticket, commenting, opening
   a PR — is that it must gate on an explicit human confirmation before it
   executes. Rationale: a hidden instruction embedded in a Jira ticket or
   PR body can hijack an agent (indirect prompt injection), so agent-read
   external text must never be able to trigger an unreviewed write. Drift
   Issues opened by the scheduled Action carry a note telling agents to
   treat quoted external text as data, not instructions.
7. **Tool deferral stays at its default (on).** Do not set
   `alwaysLoad: true` on any gateway toolset (the AWS toolset is large);
   `.mcp.json` sets no `alwaysLoad` keys.
8. **Acceptance gate unchanged.** Evidence records fetched through gateways
   still pass the evidence validator: `ai_generated` must be `false`
   (schema `const`), or the record is rejected and the PR fails.

## AEHR loop (Automated Evidence, Human Review)

Gateway (or fixture) signal → `check_control_health.py` computes drift →
the daily Action opens a GitHub Issue titled `[drift] Control drift: <ID>
(<type>)` — the Issue is the timestamped evidence of due diligence → AI may
draft the remediation narrative → a human reviews and lands the fix by pull
request → the merge is the authorization and flips the control status.
`tests/test_mcp_evidence.py` exercises the validator rejection, the SSRF
guard, the fixture fallback, and the `[drift]` title contract.
