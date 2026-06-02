# How I built this with AI

I build the way I think a modern GRC function should run: **AI does the heavy lifting, and I own
the judgment.** This repository — the controls-as-code engine, the onboarding generator that
renders a tailored program per company, and the briefs that sit on top — was built by directing AI
under governance, not by hand and not on autopilot. That division of labor *is* the skill I'm
selling, so here it is in the open.

## What AI did

- Drafted control narratives, framework crosswalks, and gap analysis from the control library and
  the computed evidence schema.
- Generated the first pass of the Python tooling (`scaffold.py`, `onboard_company.py`,
  `draft_narrative.py`) and the Rego policy, against a spec I set.
- Researched each target company's **public** posture and drafted the company-specific value
  content, with every load-bearing claim cited.
- Rendered the per-company program payloads and the site from one configuration file.

## What I did

- Set the architecture: one canonical control set, framework views as a *resolution* over it,
  evidence computed from systems of record, the pull request as the human gate.
- Made the judgment calls AI can't be trusted with: **which control satisfies which requirement**,
  where a draft was wrong, what to cut, and what never ships.
- Drew and held the hard line: **evidence is computed, never AI-authored.** The schema rejects
  `ai_generated: true`; AI drafts the narrative around the evidence, never the evidence itself.
- Owned accuracy. When research surfaced a widely-repeated "FTC order" against a target that I
  could not primary-source, I refused to assert it. When a tool claim was an overstatement, I
  softened it to what the public record supports.

## Why it's governed, not vibes

Every AI-drafted artifact passes a human gate before it becomes record — the same pull-request gate
the program describes for its own controls. The provenance is in the Git history: who decided what,
when, and why. AI is leverage here, not authority. Knowing exactly where to put that boundary —
fast drafting on one side, computed evidence and human accountability on the other — is the
difference between leverage and an audit finding.

## The point

"I used AI" isn't the claim. The claim is that I can direct AI to do a senior GRC team's high-judgment
work in a fraction of the time, **and** keep the program defensible while doing it. That's what this
repo demonstrates — built the way I'd build it for you.
