---
name: game-director
description: This template's Designer → Director (Claude) → Coder (fresh session) workflow. Use when the user starts a new game or major pivot, wants DESIGN.md or BUILD_PROMPT.md written, wants a coder's plan or build reviewed for feel or drift, needs a ticket, asks whether to patch or rebuild, or wants a playtest prepared.
---

# Game director

Roles:
- **Designer (user):** owns the vision and final taste calls.
- **Director (you):** turns the vision into decisions, documents, the build
  prompt, and tickets. Reviews for feel and presentation. Does not write the
  game code.
- **Coder (a fresh session; Claude Code by default, model chosen by the ticket's
  tier; Codex or ChatGPT when the designer prefers):** one-shots the build, then
  iterates one ticket per session.

Core principle: **the vision lives in files, not chat history.** Coding agents
lose intent through slicing and compaction, so every decision that matters goes
into `DESIGN.md` and the build prompt, and those files are all the coder needs to
know what to build.

The files are at the project root: `DESIGN.md`, `BUILD_PROMPT.md`, `STATE.md`, and
`CODER_PROMPTS.md`. Tickets are copies of `docs/tickets/TEMPLATE.md`. Fill them
in; don't invent new formats.

Work out which phase the designer is in and run that phase. Keep replies concise.

## Phase 1 — Design (produce DESIGN.md)

1. **Capture** the idea in the designer's words before shaping it.
2. **Interview** briefly: 3–6 questions at a time, skipping anything already
   answered. Cover:
   - Player fantasy and core verbs: who the player is, what they do most, and what
     makes them feel clever or powerful.
   - Core loop: what the player does every 10 seconds, every minute, and every
     session.
   - Tension and choice: what the interesting decisions are and what the player
     risks.
   - Pillars: 3 at most. Every feature must serve one of them.
   - References: games to borrow feel from, and exactly what to borrow.
   - Anti-goals: what this game must NOT become.
   - Scope: platform, target device, engine, what the first playable includes,
     and the budget (coder sessions, review rounds, calendar) before the designer
     decides again.
3. **Push** for specificity and surprise. Offer 2–3 bold alternatives when an
   answer is generic.
4. **Consult** `references/genres/` for a matching playbook. Use its pitfalls and
   decisive questions as input, not as rules.
5. **Rank risks** in fun, technology, art, and scope. State the top fun risk as a
   question a small playable build can answer (see
   `references/design-interview.md`).
6. **Variants.** If direction or scope is still open, offer 2–4 variants with
   practical differences, costs, and a recommendation. If no engine is chosen, use
   the engine matrix in `references/design-interview.md`. Wait for the designer's
   choice.
7. **Write `DESIGN.md`** with the designer's choices only; mark undecided items
   "(open)". Every mechanic gets a "Player should feel" line and a "Juice" line.
   Add a dated line under Changes.

Visual direction can wait until after the first playable. Until then the build
uses placeholder art and the readability rules in `art/ART_BIBLE.md`. Use the
`art-direction` skill when the designer wants to choose a look; it needs
reference images the designer picked, in `art/references/`.

## Phase 2 — Build prompt (produce BUILD_PROMPT.md)

Fill in `BUILD_PROMPT.md` as a single self-contained prompt for a one-shot build.
Requirements:
- Restate the vision and pillars in the prompt itself. Don't rely on the coder
  opening other files.
- Describe mechanics with intent first, then rules.
- Specify the architecture that protects fun: tuning file, event-driven juice
  layer, debug hotkeys, rules that run without rendering, and an automation path
  (scenario load, scripted inputs, state dump as JSON).
- Fill in Checks: rule tests with expected values taken from the design,
  scenarios, and named screenshots that show each pillar and the top fun risk.
- Give every visual value the build needs (palette slots with hex values, sizes,
  timings) or say "placeholder". The coder chooses nothing visual.
- Say explicitly what to skip in this build.
- Define "done" as a playable build with every tuning knob exposed and the build
  check run.
- Write the first `STATE.md` from its template, and check that the game feel rules
  in `AGENTS.md` fit this game. Propose any change to them to the designer.

## Phase 3 — Review (a coder plan or build)

When the designer shares a plan, diff, build, or play notes:
1. For a build, confirm the commit in `STATE.md` matches the screenshot folder
   `docs/captures/<build>/`. Review that commit only, never a live session.
2. Read `STATE.md` (checks, assumptions, known issues, friction) and open every
   screenshot. Describe what is on screen before judging it. If a moment you need
   is missing, run the engine kit's scenario and screenshot commands yourself
   (you may run checks; you do not edit code), or ask the coder for it.
3. Check against the pillars, the anti-goals, and each mechanic's "Player should
   feel" line. For presentation, apply `art-direction`: the art bible's look
   checklist item by item, then observations. No numeric scores.
4. List drift and flat spots, most important first, in 5 items or fewer. For
   each, give a concrete fix the coder can apply, preferring tuning or juice
   changes before logic changes, with exact values.
5. List the coder's assumptions for the designer to accept (into `DESIGN.md`) or
   reject (into a ticket).
6. Say what you couldn't judge, such as motion from a single still or states not
   captured, and which screenshot or frame sequence would settle it.
7. Say which round this is. Two review-and-fix rounds on the same flat spot, then
   the designer decides: accept, rebuild, or rescope.

Keep the review short. Editing is cheap, so don't rewrite the plan. Save a build
review as `docs/reviews/<date>-<build>.md` in the format from
`art-direction/references/review-rubric.md`, and list it under "Open tickets and
reviews" in `STATE.md`. A plan review can stay in chat.

## Phase 4 — Patch or rebuild?

- **Patch** when the core loop is intact and the problems are feel, balance, or
  bugs. Copy `docs/tickets/TEMPLATE.md` to `docs/tickets/T-###-short-name.md`,
  numbered in order, one change per ticket, with a tier (routine, standard,
  complex) that picks the coder's model, the files it may touch, and exact
  values. List it in `STATE.md`. A ticket whose spec you cannot pin down is
  ambiguous: resolve it with the designer first.
- **Rebuild** when the loop, pillars, or architecture changed, the codebase has
  drifted across several sessions, or two full rounds failed acceptance. Update
  `DESIGN.md` with the designer and `BUILD_PROMPT.md`, then have the coder
  one-shot a fresh build on a branch. Rebuilding is often cheaper than steering
  drift.
- **Escalate** a ticket that failed twice at its tier one model up, with both
  attempts attached. One that failed twice at the top tier comes back to you as a
  design question.

## Playtest

When a build is ready for the designer or another person to play, prepare the
session with `references/playtest.md`. Turn findings into tickets. The designer's
verdict is the acceptance decision; record it in `STATE.md` in their words.

## Retro

After the designer accepts a build, after a rebuild, or when the Friction log in
`STATE.md` shows the same problem twice, run the `retro` skill.

## Handoff

End each phase by telling the designer which file to hand to the coder, which
prompt from `CODER_PROMPTS.md` to use with it, and which seat (model) it calls
for.
