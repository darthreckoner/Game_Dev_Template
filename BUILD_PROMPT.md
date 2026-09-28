# One-shot build prompt — [Game Name]

You are building the first complete playable version of [Game Name].
Read this whole prompt before writing code. Everything you need is here.

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
- Readability: [paste the rules from art/ART_BIBLE.md]

## Architecture (required)
- Stack: [engine and pinned version]. Install its kit from `kits/<engine>/` as
  its README says, and follow the kit's architecture defaults.
- Game rules run without rendering, on a fixed step with a seeded random
  generator, so tests and scenarios can check them.
- All tunable numbers live in `tuning.[ext]`. Never hardcode them.
- Gameplay emits events (e.g. `onX`, `onY`). A separate juice layer
  reacts with visuals and sound hooks. Game logic never calls effects directly.
- Debug hotkeys: [spawn state, speed up time, toggle overlay of key values].

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
STATE.md under "Assumptions".

## Done when
- The game is playable start to finish with the core loop working.
- Every tuning knob is exposed.
- `$build-check` has run: checks pass, or each failure is listed in STATE.md.
- STATE.md is updated: what exists, checks, assumptions, known issues, next steps.
