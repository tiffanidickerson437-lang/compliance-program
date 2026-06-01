# Security Policy

## Scope
This repository is a controls-as-code GRC program: Python tooling, Rego policy, and YAML/JSON
control definitions. It holds no production secrets and runs against committed fixtures.

## Reporting a vulnerability
Report suspected vulnerabilities **privately** via GitHub → **Security → Advisories → Report a
vulnerability**, or by email to the maintainer. Include affected files, reproduction steps, and
impact. Do **not** open a public issue for an unfixed vulnerability.

## What to expect
- Acknowledgement within **3 business days**.
- A triage decision (accept / need-more-info / out-of-scope) within **7 business days**.
- Coordinated disclosure: a fix or mitigation is merged before public discussion.

## Supported versions
The `main` branch is the only supported version; fixes land there.

## How fixes are handled
Consistent with this program's own controls, security fixes follow the same gate as every other
change: AI may draft the remediation narrative, but a human reviews and the **merge is the
authorization**. Evidence is computed, never AI-generated.
