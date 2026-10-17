# One-shot build prompt — [Game Name]

You are the Coder for [Game Name] (roles in `AGENTS.md`). You are building the
first complete playable version. Read this whole prompt, then `AGENTS.md`, then
start. Everything you need is here; do not look for earlier chats.

Seat: fresh session, Opus 5.5 (or the model the designer names).

## Vision
[Paste from DESIGN.md]

## Pillars — every decision must serve these
1.
2.
3.

## Anti-goals — do not drift into these
-

## Core loop
[Paste from DESIGN.md]

## Mechanics (intent first, then rules)
### [Mechanic]
- The player should feel:
- Rules:
- Feedback / juice:
- Tuning knobs:

## Look
- Art: [placeholder shapes and colors, or the approved direction in brief]
- Palette: [the slots and hex values from art/ART_BIBLE.md, or the placeholder
  palette]
- Readability: [paste the rules from art/ART_BIBLE.md]
- Choose nothing visual. A value missing here gets a neutral placeholder and a
  line under Assumptions.

## Architecture (required)
- Stack: [engine and pinned version]. Install its kit from `kits/<engine>/` as
  its README says, and follow the kit's architecture defaults.
- Game rules run without rendering, on a fixed step with a seeded random
  generator, so tests and scenarios can check them.
- All tunable numbers live in `tuning.[ext]`. Never hardcode them.
- Gameplay emits events (e.g. `onX`, `onY`). A separate juice layer
  reacts with visuals and sound hooks. Game logic never calls effects directly.
- Automation path: load a scenario (setup, seed, scripted inputs), advance the
  simulation, query state, and dump the whole state as JSON. Tests and the
  Director's checks use state, not pixels.
- Debug hotkeys: [spawn state, speed up time, toggle overlay of key values],
  behind a debug flag that exports turn off.

## Checks
- Rule tests: [rules that must hold, with expected values from the design]
- Scenarios: [setup, seed, scripted inputs, expected state]
- Screenshots: [short-name: what should be on screen] at [resolution], saved to
  `docs/captures/v1/`. Use frame sequences for motion and juice.

## Skip in this build
-

## Before coding
Restate in 3 lines what the player should feel in this build. Then list
any decision you're unsure about and make your best call, marking it in
`STATE.md` under "Assumptions".

## Done when
- The game is playable start to finish with the core loop working.
- Every tuning knob is exposed.
- The build check has run (`/build-check`): checks pass, or each failure is
  listed in `STATE.md`.
- `STATE.md` is updated: what exists, checks, assumptions, known issues,
  friction, next steps.
- Your report says what changed, what was checked, what is unverified and why,
  and the exact delivery state (commit, branch, pushed or not).
