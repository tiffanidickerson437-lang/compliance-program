#!/usr/bin/env bash
# PostToolUse audit logger. Appends one line per tool call to .claude/audit.log.
# ALWAYS exits 0 and writes nothing to stderr: PostToolUse stderr is surfaced to
# the model even on exit 0, so a chatty logger becomes per-turn noise.
{
  in=$(cat)
  tool=$(jq -r '.tool_name // "?"' <<<"$in")
  fp=$(jq -r '.tool_input.file_path // .tool_input.command // ""' <<<"$in")
  dir="${CLAUDE_PROJECT_DIR:-.}"
  mkdir -p "$dir/.claude"
  printf '%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tool" "$fp" >> "$dir/.claude/audit.log"
} >/dev/null 2>&1
exit 0
