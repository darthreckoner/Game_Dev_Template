---
name: game-pitch
description: Turn a raw game idea or major pivot into a pitch card, ranked risks, two to four concept variants, and after the user chooses, a prototype brief with milestones. Use when the user brainstorms a new game, reshapes an existing one, or asks what to build first.
---

# Game pitch

Help the user find the game worth prototyping. The user makes the creative choices;
you structure them, surface risks, and bring relevant experience from playbooks.

## 1. Capture

Record the idea in the user's words before shaping it. Ask only questions whose
answers would change direction: player fantasy, platform, session length, reference
games, and what excites them most. Keep unanswered items as open, not assumed.

## 2. Consult playbooks

Read `references/genres/README.md` and any playbook matching the idea. Use their
pitfalls and decisive prototype questions as input, not as rules. Mention when a
playbook's lesson came from a different project.

## 3. Pitch card

Fill the pitch fields in `PROJECT.md` using `references/pitch-card.md`. Mark each
item as the user's choice, a proposal, or open. Keep it to one screen.

## 4. Risks

Rank the largest unknowns in fun, technology, art, and scope. State the top fun risk
as a question a small playable build can answer. A moving object demonstrates
technology; a repeatable loop with a consequence demonstrates the beginning of a game.

## 5. Variants

Offer two to four concept or scope variants with practical differences, costs, and
a recommendation. Wait for the user's choice. If no engine is chosen, present engine
options using the matrix in `references/pitch-card.md`.

## 6. Prototype brief

After the user chooses, write a brief (in `docs/` or linked from `PROJECT.md`):
the question to answer, proposed reversible settings, milestones each with
"pass when" criteria, what is deferred, and what remains open. Label proposals as
proposals. Brainstorm ideas stay available but do not become requirements.

Each milestone then gets a contract through `$milestone-contract`.

## After the project

When a project teaches something reusable about its genre, propose a playbook
update during `$retro`. Keep project-specific names out of shared playbooks.
