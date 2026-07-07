#!/usr/bin/env bash
in=$(cat); cmd=$(jq -r '.tool_input.command // ""' <<<"$in")
br=$(git -C "$(jq -r '.cwd // "."' <<<"$in")" branch --show-current 2>/dev/null)
block(){ echo "BLOCKED: $1 Changes reach main only via a human-approved PR." >&2; exit 2; }
echo "$cmd" | grep -Eq 'git +push( +[^ ]+)? +(main|master)( |$)' && block "Direct push to main."
[ "$br" = "main" ] && echo "$cmd" | grep -Eq 'git +push *$' && block "Bare push while on main."
echo "$cmd" | grep -Eq 'git +push +(-f|--force)' && block "Force-push."
[ "$br" = "main" ] && echo "$cmd" | grep -Eq 'git +commit' && block "Commit on main."
echo "$cmd" | grep -Eq 'rm +-rf' && block "Destructive rm -rf."
exit 0
