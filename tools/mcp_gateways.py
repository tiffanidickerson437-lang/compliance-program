#!/usr/bin/env python3
"""MCP evidence-gateway resolver: read-only drift signals with fixture fallback.

The repo-root .mcp.json declares one MCP gateway per system of record named in
02-controls/control-library.yaml ci_mapping / evidence sources:

  jira-evidence    ticket + incident tracker (Jira)   -> CHG-02 linked tickets,
                                                          IRO-01 incident records
  aws-evidence     cloud provider (AWS)               -> CRY-01 encryption/key
                                                          inventory, MON-01 forwarding
  github-evidence  GitHub branch protection/merge API -> CHG-02 merges to production

Each gateway authenticates on-behalf-of (OBO) the running user via an OAuth
bearer token supplied by environment variable. No live credentials ship with
the repo; when the env vars are absent the caller falls back to the committed
drift-signals fixture (06-evidence-and-audit/drift-signals*.yaml). That
fallback IS the supported degraded mode, not an error.

Security posture (see 06-evidence-and-audit/mcp-gateway-security.md):
  - Streamable HTTP transport only; stdio gateways are refused.
  - HTTPS only, and gateway URLs are validated against SSRF targets
    (loopback, private ranges, link-local, cloud-metadata endpoints).
  - Tokens are sent only to their own gateway; never forwarded downstream.
  - This module is READ-ONLY: it fetches drift signals. Every MCP write
    (Issue, ticket, PR) goes through a human-in-the-loop step.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import socket
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MCP_CONFIG = REPO_ROOT / ".mcp.json"

# Env var carrying the OBO OAuth token per gateway (matches .mcp.json headers).
GATEWAY_TOKEN_ENV = {
    "jira-evidence": "JIRA_MCP_OAUTH_TOKEN",
    "aws-evidence": "AWS_MCP_OAUTH_TOKEN",
    "github-evidence": "GITHUB_MCP_OAUTH_TOKEN",
}

# Hostnames that are cloud-metadata or otherwise never legitimate gateways.
_BLOCKED_HOSTS = {
    "metadata.google.internal",
    "metadata.goog",
    "localhost",
}

_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _expand_env(value: str) -> str | None:
    """Expand ${VAR} references; return None if any referenced var is unset."""
    missing = False

    def sub(match: re.Match) -> str:
        nonlocal missing
        val = os.environ.get(match.group(1))
        if val is None:
            missing = True
            return ""
        return val

    expanded = _ENV_REF.sub(sub, value)
    return None if missing else expanded


def validate_gateway_url(url: str) -> bool:
    """True only for an HTTPS URL whose host is not an SSRF target.

    Rejects: non-HTTPS schemes, loopback, private (RFC 1918), link-local
    (169.254.0.0/16, which includes the 169.254.169.254 cloud-metadata
    endpoint), unique-local/reserved addresses, and known metadata hostnames.
    Resolves hostnames so a public name pointing at an internal IP is refused.
    """
    try:
        from urllib.parse import urlsplit

        parts = urlsplit(url)
    except ValueError:
        return False
    if parts.scheme != "https" or not parts.hostname:
        return False
    host = parts.hostname.lower()
    if host in _BLOCKED_HOSTS or host.endswith(".internal") or host.endswith(".local"):
        return False
    try:
        addrs = {info[4][0] for info in socket.getaddrinfo(host, parts.port or 443)}
    except (socket.gaierror, OSError):
        # Unresolvable now (offline / not yet provisioned): allow the config to
        # exist, but the fetch itself will fail closed to the fixture.
        try:
            addrs = {str(ipaddress.ip_address(host))}
        except ValueError:
            return True
    for addr in addrs:
        try:
            ip = ipaddress.ip_address(addr.split("%")[0])
        except ValueError:
            return False
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
            return False
    return True


def load_gateways() -> dict:
    """Return the mcpServers mapping from the repo-root .mcp.json ({} if absent)."""
    if not MCP_CONFIG.exists():
        return {}
    return json.loads(MCP_CONFIG.read_text()).get("mcpServers", {})


def resolve_gateway(name: str, server: dict) -> tuple[str, str] | None:
    """Resolve one gateway to (url, token); None if unconfigured or unsafe.

    Unconfigured means: transport is not streamable HTTP, an env var in the
    URL or the OBO token env var is unset, or the URL fails SSRF validation.
    """
    if server.get("type") != "http" or "command" in server:
        return None  # stdio or non-HTTP transport: refused by policy.
    url = _expand_env(server.get("url", ""))
    if not url or not validate_gateway_url(url):
        return None
    token = os.environ.get(GATEWAY_TOKEN_ENV.get(name, ""), "")
    if not token:
        return None
    return url, token


def fetch_drift_signals(timeout: int = 20) -> tuple[list, list[str]]:
    """Query every resolvable gateway for drift signals.

    Returns (drifting_entries, notes). When no gateway resolves (the shipped
    state: no live credentials), returns ([], notes) and the caller falls back
    to the drift-signals fixture. Each gateway is called with its own token
    only (never another gateway's token, never forwarded downstream).

    The call is a single JSON-RPC tools/call for "compliance_drift_signals",
    a tool name this program defines as its contract; the gateway (or a thin
    proxy in front of the vendor MCP server) must expose it. This client does
    not run the full MCP initialize handshake; any protocol or transport
    error fails closed to the fixture.
    """
    notes: list[str] = []
    drifting: list = []
    for name, server in load_gateways().items():
        resolved = resolve_gateway(name, server)
        if resolved is None:
            notes.append("gateway {}: unconfigured (no OBO token / env)".format(name))
            continue
        url, token = resolved
        payload = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": "compliance_drift_signals", "arguments": {}},
        }).encode()
        req = urllib.request.Request(
            url, data=payload, method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Authorization": "Bearer " + token,
            })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode())
        except Exception as exc:  # noqa: BLE001 - fail closed to fixture
            notes.append("gateway {}: fetch failed ({}); ignoring".format(
                name, exc.__class__.__name__))
            continue
        result = (body.get("result") or {})
        entries = result.get("structuredContent", {}).get("drifting", [])
        for entry in entries:
            if isinstance(entry, dict) and entry.get("control"):
                entry.setdefault("signal_source", name)
                drifting.append(entry)
        notes.append("gateway {}: {} drift signal(s)".format(name, len(entries)))
    return drifting, notes
