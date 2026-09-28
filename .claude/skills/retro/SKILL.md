---
name: retro
description: Review how the workflow went and propose at most three tested improvements to skills, templates, roles, or tools, marking which are template candidates. Use after the designer accepts a build, after a rebuild, or when the same process problem recurs.
---

# Retro

Improve the process with evidence, not impressions. This skill proposes changes;
the designer approves them. It does not edit other skills on its own authority.

## Gather

- `STATE.md` and its Git history; reviews in `docs/reviews/`, tickets in
  `docs/tickets/`, and sessions in `docs/playtests/`.
- Designer corrections: places where the designer redirected, rejected, or redid
  work.
- Drift: tickets that re-explained something already in `DESIGN.md`, assumptions
  the designer rejected, and rebuilds with what triggered them.
- Friction: failed commands, tools that misbehaved, missing standards, waits on
  handoffs, tickets that changed nothing, time or token costs if known.
- `docs/process/ASSUMPTIONS.md`.

## Propose (at most three)

For each proposal, state:

1. **Problem** and the evidence that shows it (link or quote a line).
2. **Change:** the exact edit to a skill, template, role rule, or tool, or a
   removal.
3. **Test:** how to tell whether it worked — a replay of the failing situation, a
   small eval prompt with expected behavior, or the thing to watch in the next
   build.
4. **Scope:** this project only, or a template candidate.

Prefer removing a step that no longer earns its cost over adding a new one. Check
the assumption register: did any part stop compensating for anything?

## After approval

Apply approved changes within the Director's write scope and add or update
assumption rows. Changes to `AGENTS.md`, coder skills, or code go to the coder as
a ticket. For template candidates, write a short note in
`docs/process/template-candidates.md` with the evidence; promotion into the
template is a separate step the designer performs or authorizes. Genre lessons
become proposed playbook updates in `.claude/skills/game-director/references/genres/`,
without project-specific names.
