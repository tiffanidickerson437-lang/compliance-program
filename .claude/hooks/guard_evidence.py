#!/usr/bin/env python3
import json, sys, re
d = json.load(sys.stdin); ti = d.get("tool_input", {})
path = ti.get("file_path", "") or ""
content = ti.get("content", "") or ti.get("new_string", "") or ""
EVIDENCE = ("02-controls/evidence-schemas/", "06-evidence-and-audit/", "generated/")
if any(s in path for s in EVIDENCE) and re.search(r"ai_generated:\s*true", content, re.I):
    print("BLOCKED: evidence is deterministically collected; ai_generated:true is rejected. AI drafts, humans author evidence.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
