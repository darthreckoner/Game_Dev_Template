---
name: retro
description: Review how the workflow went and propose at most three tested improvements to skills, templates, roles, seats, or tools, marking which are template candidates. Use after the designer accepts a build, after a rebuild, or when the Friction log shows the same problem twice.
---

# Retro

Improve the process with evidence, not impressions. This skill proposes changes;
the designer approves them. It does not edit other skills on its own authority.

## Gather

- `STATE.md`, especially its Friction log, and its Git history; reviews in
  `docs/reviews/`, tickets in `docs/tickets/`, and sessions in `docs/playtests/`.
- Designer corrections: places where the designer redirected, rejected, or redid
  work.
- Drift: tickets that re-explained something already in `DESIGN.md`, assumptions
  the designer rejected, and rebuilds with what triggered them.
- Seats: tickets that escalated, and whether the cheaper model would have done.
- Friction: failed commands, tools that misbehaved, missing standards, waits on
  handoffs, tickets that changed nothing, time or token costs if known.
- `docs/process/ASSUMPTIONS.md`.

## Record every lesson (required, before proposing)

Every lesson from this project goes into the template's lessons ledger, all of
them, not only the ones this retro acts on (designer, 2026-10-31). The ledger is
`docs/process/LESSONS_LEDGER.md` in the template source (`C:\Dev\Game_Dev_Template`).
- One row per lesson: the lesson in general terms, an evidence pointer
  (project and file), and the template change as Applied, Proposed or Rejected.
- Engine-specific pitfalls also go into that engine kit's pitfalls reference
  (for Godot: `kits/godot/skill/godot/references/pitfalls.md`), with a ledger row.
- Audit the template against the ledger: every Applied row still guarded, every
  Proposed row still listed. Add a dated line to the ledger's Audit log.

A retro is not complete until the ledger rows and the audit line are committed
in the template source. Report how many lessons were recorded.

## Propose (at most three)

For each proposal, state:

1. **Problem** and the evidence that shows it (link or quote a line).
2. **Change:** the exact edit to a skill, template, role rule, seat default, or
   tool, or a removal.
3. **Test:** how to tell whether it worked — a replay of the failing situation, a
   small eval prompt with expected behavior, or the thing to watch in the next
   build.
4. **Scope:** this project only, or a template candidate.

Prefer removing a step that no longer earns its cost over adding a new one. Check
the assumption register: did any part stop compensating for anything?

## After approval

Apply approved changes within the Director's write scope and add or update
assumption rows. Changes to `AGENTS.md` or the seat defaults in a game project
need the designer's agreement; changes to code or tests go to the coder as a
ticket. Prune the Friction log in `STATE.md` to what is still open.

When a change is promoted into the template, mark its ledger row Applied with
the file and commit.

For template candidates, write a short note in
`docs/process/template-candidates.md` with the evidence. Promotion into the
template is a separate step: the designer approves it, and Claude applies it in
the template source with project-specific content removed. Genre lessons become
proposed playbook updates in `.claude/skills/game-director/references/genres/`,
without project-specific names.
