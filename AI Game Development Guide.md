# AI Game Development Guide: Which Claude Model for Each Stage

Oct 16, 2026 · @Justin

## How to use this guide

Use the most capable model where a wrong call is expensive, and the cheapest model that follows a spec reliably everywhere else. The stage decides the model; the model never decides the stage.

The one rule that beats any model choice: **separate deciding from building**. A model that designs and codes in the same session drifts toward its defaults. Write decisions to a file, then build from the file in a fresh session.

| Model | Role in the pipeline | Reach for it when |
| --- | --- | --- |
| Fable 5.1 (GPT-6 Astra) | Director and critic | The decision shapes weeks of work, or taste and judgment are the point |
| Opus 5.5 (GPT-6.1 Sol) | Lead designer and senior engineer | Complex systems, design iteration, second-tier review, hard debugging |
| Sonnet 5.5 (GPT-6 Sol) | Implementer | A clear spec exists and the job is to build it well |
| Haiku 5.5 (GPT-6 Luna) | Assistant | Mechanical, repetitive, or high-volume work |

Each stage below names the model, what it owns, what it should not touch, and the file it hands to the next stage. OpenAI equivalents are in parentheses, matched by role in the pipeline rather than by benchmark, so the same stage rules apply if a Codex seat takes the job.

## Stage 0 — Brainstorm and concept

**Model: Opus (6.1 Sol).** Brainstorming rewards range and a human feel for fun more than raw depth, and you will throw most of it away. Save Fable for narrowing, not generating.

What this stage produces: one page naming the player promise, the core verbs (move, build, drive, dress), the audience, the platform, and three reference games with what to take from each. Nothing else.

How to run it:

1. Give Opus the constraints first: who plays, on what device, how long a session, what you will not build (combat, monetization, etc.).
2. Ask for 5 to 10 distinct concepts, each in five lines. Reject anything that reads as generic.
3. Pick one. Ask Opus to attack it: what is boring, what is too big, what a kid would skip.
4. Rewrite the one page yourself in your own words. Your voice here is what keeps the project from looking AI-made later.

Hand-off file: `CONCEPT.md`. If it does not fit on one page, it is not ready.

## Stage 1 — Design doc and art direction

**Model: Fable (Astra).** This is the most expensive document to get wrong. Every later stage builds from it, and a vague GDD is what lets generic defaults creep in.

Two documents come out of this stage, written separately:

**The GDD.** Player loop, world layout, each system's rules and failure cases, scope boundaries, milestones, and acceptance tests. Fable is good at the part most models skip: writing recovery rules, open decisions, and what the game will not do.

**The art direction brief.** Palette with hex values, shape language, lighting settings, material rules, UI style, a named avoid list, and 3 to 5 reference images you chose. Fable writes it; you supply the references. A brief without reference images is a suggestion, not a direction.

How to run it:

1. Paste `CONCEPT.md` and ask Fable to draft the GDD with every number marked as proposed, not decided.
2. Have Fable interview you on the open decisions before it fills them in. Answer in your words.
3. Write the art brief in a separate session from the GDD so the two do not blur.
4. Ask Fable for a one-page summary of both at the end. That summary is what later sessions get pasted.

Hand-off files: `GDD.md`, `ART_DIRECTION.md`, `references/` folder of images. Keep the one-page summary at the top of `GDD.md`.

## Stage 2 — Spec, architecture and task breakdown

**Model: Fable (Astra) for architecture, Opus (6.1 Sol) for the task list.** Architecture decisions (engine, project layout, client/server split, save format, how tuning values are stored) are hard to reverse. Breaking them into tickets is detailed but mechanical.

What comes out: an architecture note and a set of tickets small enough that one Sonnet session finishes one without compaction.

How to run it:

1. Fable reads `GDD.md` and writes `ARCHITECTURE.md`: folder layout, module boundaries, where config lives, what the server validates, naming conventions. Ask it to list the three decisions it is least sure of.
2. Fable writes `DECISIONS.md`: a dated log of every choice made so far, one line each. This file is pasted into every later session.
3. Opus turns Milestone 1 of the GDD into tickets. Each ticket names its inputs, its done condition, the files it may touch, and a difficulty tier with the model that tier maps to: Routine → Haiku (Luna), Standard → Sonnet (6 Sol), Complex (cross-module, physics feel, networking, validation) → Opus (6.1 Sol), Ambiguous (the spec itself is in doubt) → Fable (Astra). A ticket with no tier is not ready to run. Nothing outside Milestone 1 gets a ticket yet.
4. One ticket at the top: a single `Config` module holding every tunable number (speeds, jump height, camera lag, grid size). Build it first so later tuning is editing values, not code.

Hand-off files: `ARCHITECTURE.md`, `DECISIONS.md`, `tickets/` with one file per ticket.

## Stage 3 — Vertical slice / feel prototype

**Model: Opus (6.1 Sol) builds, Fable (Astra) judges, you decide.** The slice is one small scene that proves the game looks and feels right before anything else exists. This is where the generic look is caught or locked in.

What comes out: one scene with final lighting, one landmark, the character, the main vehicle or verb, and the core interaction, all under the art brief. No saves, no menus beyond what the slice needs.

How to run it:

1. Opus builds the **style tile** first: a 30 by 30 patch with ground, one prop, one sign, the character, the vehicle, under the lighting settings from `ART_DIRECTION.md`. Nothing else until this looks right on the target device.
2. You look at it on the real device. Not the editor, not the desktop build.
3. Fable reviews a screenshot against the brief and the reference images. Ask for a diff, not an opinion: what to change, to what value.
4. Opus applies the diff. Repeat until you would show the tile to someone. Then Opus builds the rest of the slice to match it.
5. Opus wires the `Config` module and the core verbs. Tune feel by editing values with the game running, not by asking for code changes.

Stop rule: if the tile takes more than three review loops to match the brief, the brief is unclear. Go back to Stage 1 and fix the words before fixing the scene.

Hand-off: the slice itself, plus a `STYLE_TILE.md` with the exact lighting values, material names, and asset IDs that passed. Every later asset is checked against this file.

## Stage 4 — Systems implementation

**Model: Sonnet (6 Sol) by default, Opus (6.1 Sol) for the hard tickets.** With a spec, a style tile, and small tickets, Sonnet does most of this well and cheaply. Escalate a ticket to Opus when it touches physics feel, networking, placement validation, or anything that spans several modules.

What comes out: the Milestone 1 ticket list closed, one ticket per session.

How to run it:

1. Start every session the same way: paste the one-page GDD summary, `DECISIONS.md`, `STYLE_TILE.md`, and the one ticket, opened in the model its tier names. Nothing else from the GDD.
2. One ticket per session. When the ticket is done, end the session. A second ticket in the same context is where drift starts.
3. Sonnet writes code only. If it wants to pick a color, a font, a sound, or an asset, the ticket was missing a value. Stop, add the value to the ticket or the style tile, restart.
4. Any new decision made during a ticket goes into `DECISIONS.md` before the session ends.
5. Haiku handles the chores between tickets: renaming assets to convention, generating config boilerplate, formatting, summarizing the session log.

Escalation rule: a ticket Sonnet fails twice goes to Opus with both failed attempts attached. A ticket Opus fails twice goes to Fable as a design question, not a coding one, because the spec is probably wrong.

Hand-off: a working Milestone 1 build and an updated `DECISIONS.md`.

## Stage 5 — Review, critique and playtest loop

**Model: Fable (Astra) as critic, Haiku (Luna) as note-taker, you as the playtester.** This loop runs after every milestone and after any batch of content. It is the only stage where the top model should see screenshots and video, because judging feel against intent is the hardest thing in the pipeline.

What comes out: a short list of defects and diffs, ranked, each tied to a GDD rule or an art brief rule.

How to run it:

1. Play it on the target device. Record 2 to 3 minutes of real play. If kids are the audience, watch them play and count hints; do not coach.
2. Haiku turns your raw notes and the session log into a clean list of observations, one line each, no interpretation.
3. Fable gets the observations, 4 to 6 screenshots, the GDD acceptance tests, and the art brief. Ask it for three things: which acceptance tests failed, which art rules are broken, and the three highest-leverage fixes with exact values.
4. Fable's output becomes new tickets. Opus or Sonnet implements them per Stage 4.
5. Rerun the loop. Two clean passes in a row closes the milestone.

Rules:

- Fable reviews against the written brief, never against taste alone. If it suggests something the brief does not cover, that is a brief update first, a build change second.
- Never let the model that built a feature review it. Fresh session, no build context.
- If the same defect appears three times, stop patching. Rebuild that area from the style tile.

Hand-off: updated `tickets/` and a dated `PLAYTEST_LOG.md` with hint counts and failed tests.

## Stage 6 — Content expansion and polish

**Model: Sonnet (6 Sol) for volume, Opus (6.1 Sol) for anything the player will stare at, Fable (Astra) only at batch review.** Content is where cost adds up and where the look drifts back toward defaults. Keep the top model out of production and put it at the gate.

What comes out: new areas, props, cosmetics, vehicles, and stations, added in small batches that each pass the Stage 5 loop.

How to run it:

1. Opus writes a batch plan: 5 to 10 items, each with its asset source, palette slots from the brief, and the GDD rule it serves. No item exists because it was easy.
2. You pick or buy the assets. Give Sonnet asset IDs, not asset descriptions. A model choosing from a store is how everything ends up the same.
3. Sonnet places, wires, and scripts each item against `STYLE_TILE.md`. One batch per session.
4. Opus handles the items players look at closely: the player character, the main vehicle, the UI, the first thing seen on load.
5. Haiku runs the batch checks: naming, missing collision, assets outside the palette, tunables not in `Config`.
6. Fable reviews the batch once, as in Stage 5. Nothing merges without it.

Polish rule: polish is tuning values in `Config`, lighting, sound timing, and animation speed, done by you with the game running. If polish needs new code, it is a ticket, not polish.

Hand-off: the batch merged, `DECISIONS.md` and `STYLE_TILE.md` updated with any new approved asset or value.

## Stage 7 — Hardening, persistence and QA

**Model: Opus (6.1 Sol) designs the save and security model, Sonnet (6 Sol) implements and writes tests, Fable (Astra) for the bugs that survive both.** Saves, permissions, and server validation are where a cheap shortcut costs a child their town. This is the one place to spend on engineering quality over art.

What comes out: persistence that survives the GDD's failure tests, server-side validation on every shared action, and a test suite that runs before each build.

How to run it:

1. Opus writes the data model and the failure matrix: what happens on disconnect, double-submit, stale session, schema change, load failure. Each row gets a required outcome.
2. Sonnet implements the save layer and one test per matrix row. Tests before features.
3. Sonnet audits every client-to-server call against one question: what if the client lies? Fix the server, never the client.
4. Haiku runs the repetitive checks: 20 leave-and-return cycles, log diffing, asset budget counts, performance samples on the target device.
5. Anything that fails twice after a Sonnet fix goes to Opus. Anything that fails after Opus goes to Fable with the full log, as a design question.

Rules:

- Persistence is a player-facing feature with visible states (saving, saved, retry). Treat its UI as part of the ticket.
- Test on the oldest target device for the full session length. Thermal throttling and memory pressure do not show up in the editor.
- No new content during hardening. The surface area is frozen until the matrix passes.

Hand-off: a passing test suite, a `QA_LOG.md` with device, build, and results, and a build you would hand to a stranger.

## Stage 8 — Shipping and post-launch

**Model: Sonnet (6 Sol) for the release work, Haiku (Luna) for the checklist, Fable (Astra) once for the go/no-go.** Shipping is mostly procedure. The one judgment call is whether to ship at all, and that deserves the top model with everything in front of it.

What comes out: a released build, store or platform listing, and a post-launch loop that feeds back into Stage 5.

How to run it:

1. Haiku generates the release checklist from the GDD acceptance tests and the platform's requirements, and ticks it off from logs. Anything it cannot verify from a log goes to you.
2. Sonnet handles the release mechanics: build config, version bump, platform settings, privacy and access settings, store text from the one-page summary.
3. Fable gets the checklist, the latest `PLAYTEST_LOG.md`, `QA_LOG.md`, and 5 screenshots. Ask one question: ship, or what blocks it. Accept the answer.
4. Ship to the smallest audience first (family, friends, private listing). Collect one week of play before widening.
5. Post-launch, every bug report or observation goes through Haiku into the observation list, and the Stage 5 loop runs on a cadence you set.

Rules:

- No new features in the shipping branch. Feature ideas go into `CONCEPT.md` for the next cycle.
- The platform's own rules (ratings, child accounts, chat defaults, payment) are checked against current documentation, not model memory. Have Sonnet fetch and cite them.
- Keep `DECISIONS.md` going after launch. The second version is built from it.

Hand-off: the live build, a `RELEASE.md` with version, date, and known issues, and the next cycle's `CONCEPT.md` started.

## Quick reference

| Stage | Primary model | Support | Why | Hand-off file |
| --- | --- | --- | --- | --- |
| 0 Brainstorm | Opus (6.1 Sol) | — | Range and feel for fun; output is disposable | `CONCEPT.md` |
| 1 GDD + art brief | Fable (Astra) | You (references) | Most expensive document to get wrong | `GDD.md`, `ART_DIRECTION.md` |
| 2 Architecture + tickets | Fable (Astra) for architecture | Opus (6.1 Sol) for tickets | Hard to reverse; tickets are mechanical | `ARCHITECTURE.md`, `DECISIONS.md`, `tickets/` |
| 3 Feel prototype | Opus (6.1 Sol) builds | Fable (Astra) as critic | Catches the generic look before it spreads | `STYLE_TILE.md` |
| 4 Systems | Sonnet (6 Sol) | Opus (6.1 Sol) hard tickets, Haiku (Luna) chores | Spec exists; cost matters | Milestone build |
| 5 Review loop | Fable (Astra) as critic | Haiku (Luna) notes | Judging feel against intent is the hardest task | `PLAYTEST_LOG.md` |
| 6 Content | Sonnet (6 Sol) | Opus (6.1 Sol) hero items, Fable (Astra) batch gate | Volume work; top model only at the gate | Merged batch |
| 7 Hardening | Opus (6.1 Sol) design | Sonnet (6 Sol) tests, Fable (Astra) stubborn bugs | Engineering quality over art | `QA_LOG.md` |
| 8 Shipping | Sonnet (6 Sol) | Haiku (Luna) checklist, Fable (Astra) go/no-go | Mostly procedure, one judgment call | `RELEASE.md` |

## Rules that matter more than model choice

1. **Decide in one session, build in another.** Design and code in the same context always drifts toward defaults. The file between them is the product.
2. **Every session starts from the same four pastes:** one-page GDD summary, `DECISIONS.md`, `STYLE_TILE.md`, and one ticket. Not the whole GDD, not the last chat.
3. **One ticket per session.** End the session when it closes. Context that survives a ticket carries the previous ticket's habits into the next.
4. **Models choose nothing visual.** Colors, fonts, assets, sounds, and lighting values come from you or the brief. A model picking from a store is where the sameness comes from.
5. **Specify values, not adjectives.** Hex codes, stud sizes, seconds, asset IDs. "Punchy" and "clean" produce the default.
6. **The critic never built it.** Review in a fresh session with no build context, against the written brief.
7. **Rebuild, don't patch, after three strikes.** Repeated patches accumulate the old look.
8. **Real device, real player, early.** The editor hides thermal, touch, and memory problems; you hide the hints you give your kids.
9. **Escalate up the ladder with evidence.** Start at the model the ticket's tier names; Sonnet fails twice, Opus gets both attempts. Opus fails twice, Fable gets a design question, not a coding one.
10. **Spend the top model on decisions, not output.** Fable at the gates (brief, architecture, review, go/no-go) and nowhere in the production line.
