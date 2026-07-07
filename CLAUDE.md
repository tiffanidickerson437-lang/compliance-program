# CLAUDE.md — how AI works inside this repository

This file is guidance for any AI session working in this repo. Guidance is not
enforcement: the enforcement layer is the hooks in `.claude/hooks/` (local
pre-write gate) plus the CI gates in `.github/workflows/` (notably
`evidence-validator.yml`). Keep both — belt and suspenders. A hook exit code 2
blocks the tool call and feeds its stderr back to the model; a `deny` rule or an
exit-2 hook overrides even `--dangerously-skip-permissions`, and when rules
conflict the most restrictive wins.

Never fabricate evidence or citations; all evidence traces to a system of record.

## The operating model (NoteRise Nucleus)

Four pillars, each grounded in files that already exist here:

1. **Ghost-Advisor.** AI drafts, a human approves every PR. The merge is the
   authorization. Encoded in `policy/change_control.rego` (PR-only, independent
   reviewer, no direct push to a protected branch) and mirrored locally by
   `.claude/hooks/guard_git.sh`. Committed prompt templates live in
   `ai/prompts/`; `ai/AI-USAGE.md` states where AI drafts and where it is
   forbidden.
2. **Truth-First.** AI drafts due diligence; it never fabricates due care.
   Evidence is computed deterministically from systems of record and is never
   AI-authored: the schemas in `02-controls/evidence-schemas/` require
   `ai_generated: false` as a constant, `evidence-validator.yml` rejects
   `ai_generated: true` in CI, and `.claude/hooks/guard_evidence.py` rejects it
   before the file is even written.
3. **Git-native System of Record.** The repository is the program of record:
   controls in `02-controls/control-library.yaml` (+ its OSCAL rendering
   `control-library.oscal.json`), framework views as OSCAL profile resolutions
   in `02-controls/profiles/`, risk in `01-risk-management/`, policy-as-code in
   `policy/`, executables in `tools/`, rendered output in `generated/`.
4. **Framework-agnostic controls-as-code.** A control is defined once; every
   framework gets its view from the same source via
   `02-controls/framework-crosswalk.yaml` and the OSCAL profiles. Adding a
   framework is a mapping, never a new control.

The program's content is organized into eight pillar directories
(`00-governance/` through `07-stakeholder-management/`); see `README.md`.

## The 5-phase build order

1. **Guardrails** — hooks, permissions, CI gates (this `.claude/` workspace,
   `policy/`, `.github/workflows/`).
2. **SCF + OSCAL spine** — the owned control library and its OSCAL catalog and
   profiles in `02-controls/`.
3. **STRM coverage** — set-theory relationship mappings from owned controls to
   external frameworks (drafts land in `mappings/`, e.g.
   `mappings/iso42001.draft.yaml`; approved mappings in
   `02-controls/framework-crosswalk.yaml`).
4. **FAIR risk** — quantified risk in `01-risk-management/risk-register.yaml`
   with Monte Carlo simulation tooling under `tools/`.
5. **MCP/CI automation** — agents and workflows that operate the program
   continuously under the same human-approval gate.

## Hard rules for AI sessions

- **Never push to main. Never force-push. Never commit on main.** One unit of
  work = one branch = one PR. A human approves every PR; no self-review.
- **Never author evidence.** Never write `ai_generated: true` anywhere under
  `02-controls/evidence-schemas/`, `06-evidence-and-audit/`, or `generated/`.
  Drafting narratives, gap analyses, and crosswalk proposals is allowed and
  expected; the computed evidence record is not yours to write.
- **Never invent control IDs, framework requirement text, or numbers.** Ground
  every claim in a file in this repo or a named external source.
- **Brownfield discipline.** Read a file before writing it; edit in place;
  never scaffold over existing work.
- **Canonical paths.** `00-governance/`, `01-risk-management/`, `02-controls/`,
  `06-evidence-and-audit/`, `mappings/`, `policy/`, `tools/`, `generated/`,
  `.github/workflows/`. Do not create `evidence/`, `catalog/`, or `policies/`.

## Hook mechanics (what runs when)

Each hook receives JSON on stdin: `session_id`, `cwd`, `hook_event_name`,
`tool_name`, `tool_input` (`tool_input.command` for Bash;
`tool_input.file_path` + `content`/`new_string` for Write/Edit).

| Hook | Event | Job |
|------|-------|-----|
| `guard_evidence.py` | PreToolUse (Write/Edit/MultiEdit) | Exit 2 on `ai_generated: true` bound for an evidence path. |
| `guard_git.sh` | PreToolUse (Bash) | Exit 2 on push-to-main, force-push, commit-on-main, `rm -rf`. Branch is derived from the hook's stdin `cwd` (the session's own worktree), not `CLAUDE_PROJECT_DIR`. |
| `audit_log.sh` | PostToolUse | Appends date + tool + path to `.claude/audit.log` (gitignored). Always exits 0, silent on stderr. |
| `setup_deps.sh` | SessionStart (startup/resume) | Ensures numpy/scipy for the FAIR simulation; always exits 0. |

## Skills and agents

Skills live in `.claude/skills/` (gap-analysis, crosswalk, draft-narrative,
risk-sim). Agents in `.claude/agents/` are draft-only: `permissionMode: plan`,
isolated worktrees, and instructions that mirror the tested rules of
`policy/change_control.rego` at the harness layer. Their outputs are proposals;
nothing becomes record until a human merges it.
