---
name: retro
description: Review how the last milestone's process worked and propose at most three tested improvements to skills, standards, roles, or tools, marking which are template candidates. Use at the end of each milestone or when the same process problem recurs.
---

# Retro

Improve the process with evidence, not impressions. This skill proposes changes;
the user approves them. It does not edit other skills on its own authority.

## Gather

- Evidence records, art-direction requests and reviews, and the playtest file for
  the milestone.
- Continuity notes and git history for the milestone period.
- User corrections: places where the user redirected, rejected, or redid work.
- Friction: failed commands, tools that misbehaved, missing standards, waits on
  handoffs, rounds that changed nothing, time or token costs if known.
- `docs/process/ASSUMPTIONS.md`.

## Propose (at most three)

For each proposal, state:

1. **Problem** and the evidence that shows it (link or quote a line).
2. **Change:** the exact edit to a skill, standard, contract template, role rule,
   or tool, or a removal.
3. **Test:** how to tell whether it worked — a replay of the failing situation, a
   small eval prompt with expected behavior, or the metric to watch next milestone.
4. **Scope:** this project only, or a template candidate.

Prefer removing a step that no longer earns its cost over adding a new one. Check
the assumption register: did any part stop compensating for anything?

## After approval

Apply approved project changes and add or update assumption rows. For template
candidates, write a short note under `docs/process/template-candidates.md` with the
evidence; promotion into the game-dev template is a separate, deliberate step the
user performs or authorizes. Genre lessons become proposed playbook updates for
`$game-pitch`, without project-specific names.
