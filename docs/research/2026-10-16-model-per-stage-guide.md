# AI Game Development Guide: Which Claude Model for Each Stage

2026-10-16

## How to use this guide

Use the most capable model where a wrong call is expensive, and the cheapest model that follows a spec reliably everywhere else. The stage decides the model; the model never decides the stage.

The one rule that beats any model choice: **separate deciding from building**. A model that designs and codes in the same session drifts toward its defaults. Write decisions to a file, then build from the file in a fresh session.

| Model | Role in the pipeline | Reach for it when |
| --- | --- | --- |
| Fable 5.1 (GPT-6 Astra) | Director and critic | The decision shapes weeks of work, or taste and judgment are the point |
| Opus 5.5 (GPT-6.1 Sol) | Lead designer and senior engineer | Complex systems, design iteration, second-tier review, hard debugging |
| Sonnet 5.5 (GPT-6 Sol) | Implementer | A clear spec exists and the job is to build it well |
| Haiku 5.5 (GPT-6 Luna) | Assistant | Mechanical, repetitive, or high-volume work |

This guide pairs with the **AI Solo Game-Development Kit** in the same template folder. The kit defines the roles, loops, gates, standards and files; this guide says which model takes each seat at each stage. The files named below are the kit's, so the two can be followed together.

OpenAI equivalents are in parentheses, matched by role in the pipeline rather than by benchmark, so the same stage rules apply if a Codex seat takes the job.

| Artifact | File | Made in |
| --- | --- | --- |
| Pitch card | `PROJECT.md` | Stage 0 |
| Design brief, milestones, contract | `docs/BRIEF.md` | Stages 1–2 |
| Art bible with G3 checklist | `docs/ART_BIBLE.md`, `docs/references/` | Stage 1 |
| Architecture note | `docs/ARCHITECTURE.md` | Stage 2 |
| Decisions log | `DECISIONS.md` | Stage 2 onward |
| Tickets | `tickets/<milestone>/` | Stage 2 |
| Style tile record | `docs/STYLE_TILE.md` | Stage 3 |
| Evidence records | `docs/evidence/<milestone>/` | Stage 5 onward |
| Asset provenance | `assets/ASSET_SOURCES.md` | Stage 6 |
| Release notes | `docs/RELEASE.md` | Stage 8 |

Each stage below names the model, what it owns, what it should not touch, and the file it hands to the next stage.

## Stage 0 — Brainstorm and pitch card

**Model: Opus (6.1 Sol).** Brainstorming rewards range and a human feel for fun more than depth, and most of it gets thrown away. Save Fable for narrowing, not generating.

What comes out: the pitch card at the top of `PROJECT.md`, one page: player fantasy and core verbs; the core loop at three timescales (seconds, minutes, session); three pillars and at least one anti-pillar; reference games and what to take from each; scope class (jam, prototype, vertical slice); and a ranked list of the biggest unknowns in fun, tech, art and scope. The top fun risk is the question the first playable must answer.

How to run it:

1. Give Opus the constraints first: who plays, on what device, how long a session, what you will not build.
2. Ask for 5 to 10 distinct concepts, five lines each. Reject anything that reads as generic.
3. Pick one. Ask Opus to attack it: what is boring, what is too big, what a player would skip.
4. Ask for 2 to 4 scope variants with their trade-offs, then choose. The model does not choose.
5. Write the pitch card yourself in your own words. Your voice here is what keeps the project from looking AI-made later.

Hand-off: `PROJECT.md` with the pitch card. If it does not fit on one page, it is not ready.

## Stage 1 — Design brief and art bible

**Model: Fable (Astra).** These are the two most expensive documents to get wrong. Every later stage builds from them, and vague words here are what let generic defaults in.

Two documents, written in separate sessions so they do not blur:

**The brief (`docs/BRIEF.md`).** Player loop, world layout, each system's rules and failure cases, scope boundaries, milestones with "pass when" criteria, a scenario list per milestone, and a deferred-ideas list. Fable is good at the part most models skip: recovery rules, open decisions, and what the game will not do. A brainstorm idea is not a requirement until it is written here.

**The art bible (`docs/ART_BIBLE.md`).** Palette with hex values, shape language, lighting values, material rules, camera and scale, UI style, a named avoid list, and 3 to 5 reference images you chose, saved in `docs/references/`. It ends with the **G3 checklist**: 8 to 15 yes/no items that can each be judged from a screenshot (palette only from the list; no flat single-color surface larger than N units; lighting values match; every asset from an approved source; UI font and corner radius as specified). That checklist is how presentation is judged from Stage 3 on, so it replaces any score. A bible without reference images is a suggestion, not a direction.

How to run it:

1. Paste the pitch card and ask Fable to draft the brief with every number marked proposed, not decided.
2. Have Fable interview you on the open decisions before it fills them in. Answer in your words.
3. In a fresh session, give Fable the reference images and ask for the art bible and its checklist. Every hex value and asset source it proposes is yours to keep or replace.
4. Ask Fable for a one-page summary of both. That summary is what later sessions get pasted.

Rule: no model chooses a visual value, now or later. Colors, fonts, assets, sounds and lighting come from you or the bible.

Hand-off: `docs/BRIEF.md`, `docs/ART_BIBLE.md`, `docs/references/`, with the one-page summary at the top of the brief.

## Stage 2 — Architecture, contract and tickets

**Model: Fable (Astra) for architecture and the contract, Opus (6.1 Sol) for the task list.** Architecture decisions are hard to reverse. Breaking them into tickets is detailed but mechanical.

What comes out: an architecture note, the approved Milestone 1 contract, and tickets small enough that one Sonnet session finishes one without compaction.

How to run it:

1. Fable reads the brief and writes `docs/ARCHITECTURE.md`: folder layout, module boundaries, a deterministic simulation core separated from presentation, fixed timestep and seeded RNG, where tuning values live, what the server validates, naming conventions. Ask it to list the three decisions it is least sure of.
2. Fable starts `DECISIONS.md`: a dated log of every choice made so far, one line each. This file is pasted into every later session.
3. Fable writes the Milestone 1 **contract**: the brief's pass criteria and scenario list restated as tests a script can run. You approve it before any ticket is written. Building against an unapproved contract is the main cause of wasted rounds.
4. Opus turns Milestone 1 into tickets. Each ticket names its inputs, its done condition including the test that proves it, the files it may touch, and a difficulty tier with the model that tier maps to: Routine → Haiku (Luna), Standard → Sonnet (6 Sol), Complex (cross-module, physics feel, networking, validation) → Opus (6.1 Sol), Ambiguous (the spec itself is in doubt) → Fable (Astra). A ticket with no tier is not ready to run. Nothing outside Milestone 1 gets a ticket yet.
5. Two tickets go first: a `Config` module holding every tunable number (speeds, jump height, camera lag, grid size), and the **automation API** (load a scenario, send actions, query state, dump state as JSON). Every gate in Stage 5 depends on the second one.

Hand-off: `docs/ARCHITECTURE.md`, `DECISIONS.md`, and `tickets/M1/` with the contract at the top and one file per ticket.

## Stage 3 — Style tile and feel prototype

**Model: Opus (6.1 Sol) builds, Fable (Astra) critiques, you decide.** The slice is one small scene that proves the game looks and feels right before anything else exists. This is where the generic look is caught or locked in.

What comes out: one frozen commit with final lighting, one landmark, the character, the main verb or vehicle, and the core interaction, passing every item on the G3 checklist. No saves, no menus beyond what the slice needs.

How to run it:

1. Opus builds the **style tile** first: a 30 by 30 patch with ground, one prop, one sign, the character and the vehicle, under the lighting values from the art bible. Nothing else until it passes.
2. Look at it on the real device. Not the editor, not the desktop build.
3. Fable, in a fresh session with no build context, runs the G3 checklist on the screenshot and returns item-by-item results plus observations. Ask for a diff with values, not an opinion.
4. Opus applies the diff. Repeat until every item passes. Then Opus builds the rest of the slice to match the tile.
5. Opus wires `Config` and the core verbs. Tune feel by editing values with the game running, not by asking for code changes.

Stop rule: if the tile needs more than three review loops, the bible is unclear. Fix the words before the scene.

Hand-off: the frozen commit, and `docs/STYLE_TILE.md` with the exact lighting values, material names and asset IDs that passed. Every later asset is checked against it.

## Stage 4 — Systems implementation

**Model: Sonnet (6 Sol) by default, Opus (6.1 Sol) for Complex tickets.** With an approved contract, a style tile and tiered tickets, Sonnet does most of this well and cheaply.

What comes out: the Milestone 1 tickets closed, each with its test passing, one ticket per session.

How to run it:

1. Start every session with the same four pastes: the one-page brief summary, `DECISIONS.md`, `docs/STYLE_TILE.md`, and the one ticket, opened in the model its tier names. Nothing else from the brief.
2. One ticket per session. End the session when it closes. A second ticket in the same context is where drift starts.
3. A ticket is done when its test passes, not when the code looks right. The tests written here are what gates G1 and G2 run in Stage 5.
4. The model writes code only. If it wants to pick a color, a font, a sound or an asset, the ticket was missing a value. Stop, add the value to the ticket or the style tile, restart.
5. Any new decision made during a ticket goes into `DECISIONS.md` before the session ends.
6. Haiku (Luna) handles the chores between tickets: renaming to convention, config boilerplate, formatting, summarizing the session log into the continuity file.

Escalation rule: a ticket Sonnet fails twice goes to Opus with both attempts attached. A ticket Opus fails twice goes to Fable as a design question, not a coding one, because the spec is probably wrong.

Hand-off: a Milestone 1 candidate commit and an updated `DECISIONS.md`.

## Stage 5 — Evidence, critique and acceptance (the gate loop)

**Model: scripts for correctness, Haiku (Luna) assembles the record, Fable (Astra) critiques presentation and UX, you accept.** Models grade their own work generously and find about half of real bugs, so correctness is decided by scripts and acceptance by you. The top model sees screenshots and clips because judging intent is the hardest task in the pipeline; it produces observations, never a score and never a fix.

What comes out: one evidence record per candidate build in `docs/evidence/<milestone>/`, with a result per gate and a ranked defect list, each defect tied to a brief rule or a checklist item.

| Gate | Evidence | Judge |
| --- | --- | --- |
| G0 Build | Builds and launches; error log empty | Script |
| G1 Rules | Unit and scenario tests on the simulation core | Script, pass/fail |
| G2 Behavior | Scripted scenarios with state assertions, plus recordings | Script, then clips for review |
| G3 Presentation | Screenshots and clips against the art bible's checklist, each item pass/fail with observations | Fable (Astra), fresh session |
| G4 UX and accessibility | Checklist and a critic walkthrough | Fable (Astra), fresh session |
| G5 Performance | Fixed scenario on the target device against a budget set beforehand | Script |
| G6 Play | Uncoached human playtest | You, and only you |

How to run it:

1. Freeze a commit. Never review a live dev session; verdicts become impossible to attribute.
2. Scripts run G0, G1, G2 and G5 through the automation API. Haiku collects the results, screenshots, clips and your playtest notes into the evidence record, one line per observation, no interpretation.
3. Fable gets the record, 4 to 6 screenshots, the clips, the G3 checklist and the UX checklist. Its output: G3 and G4 item by item, observations, and the three highest-leverage fixes with exact values.
4. Play it yourself on the target device. If kids are the audience, watch them and count hints; do not coach. That is G6.
5. Fixes become tiered tickets and go through Stage 4. At most two critique-and-fix rounds per candidate, then you decide: accept, fix, or rescope.

Rules:

- Scores are never averaged across gates. A G1 or G2 failure blocks acceptance whatever G3 says.
- Critics produce evidence, not edits. A critic that fixes what it found is grading its own work again.
- Plateau rule: when the same defect IDs persist across two rounds, stop and decide.
- Kill rule: a milestone that fails acceptance after two full rounds gets rescoped or shelved. The loop does not run a third time on the same contract.
- Only you set `accepted: true` in the record.

Hand-off: the evidence record, and new tickets in `tickets/<milestone>/`.

## Stage 6 — Content expansion and polish

**Model: Sonnet (6 Sol) for volume, Opus (6.1 Sol) for hero items, Fable (Astra) only at the batch gate.** Content is where cost adds up and where the look drifts back toward defaults. Keep the top model out of production and at the gate.

What comes out: new areas, props, cosmetics, vehicles and stations, added in small batches that each pass the Stage 5 gates.

How to run it:

1. Opus writes a batch plan: 5 to 10 items, each with its asset source, palette slots from the bible, and the brief rule it serves. No item exists because it was easy.
2. You pick or buy the assets, or generate them through the kit's asset procedure: spec first (size, pivot, palette or texel density, poly budget, style references), normalize by script, validate, record provenance in `assets/ASSET_SOURCES.md`. Give Sonnet asset IDs, not asset descriptions. A model choosing from a store is where the sameness comes from.
3. Sonnet places, wires and scripts each item against `docs/STYLE_TILE.md`. One batch per session.
4. Opus handles what players look at closely: the character, the main vehicle, the UI, the first thing seen on load.
5. Haiku runs the batch checks: naming, missing collision, colors outside the palette, tunables not in `Config`, assets without provenance.
6. The batch is a candidate build and goes through the Stage 5 gates like any other. Nothing merges without an evidence record.

Polish rule: polish is tuning values in `Config`, lighting, sound timing and animation speed, done by you with the game running. If polish needs new code, it is a ticket.

Hand-off: the batch merged; `DECISIONS.md`, `docs/STYLE_TILE.md` and `assets/ASSET_SOURCES.md` updated.

## Stage 7 — Hardening, persistence and QA

**Model: Opus (6.1 Sol) designs the save and security model, Sonnet (6 Sol) implements and writes tests, Fable (Astra) for the bugs that survive both.** Saves, permissions and server validation are where a cheap shortcut costs a player their work. This is the one place to spend on engineering quality over art.

What comes out: persistence that survives the brief's failure tests, server-side validation on every shared action, and a test suite that runs as part of G1 before each build.

How to run it:

1. Opus writes the data model and the failure matrix: what happens on disconnect, double-submit, stale session, schema change, load failure. Each row gets a required outcome.
2. Sonnet implements the save layer and one test per matrix row. Tests before features; they join G1.
3. Sonnet audits every client-to-server call against one question: what if the client lies? Fix the server, never the client.
4. Haiku runs the repetitive checks: 20 leave-and-return cycles, log diffing, asset budget counts, G5 samples on the oldest target device for a full session length. Results go into the evidence record.
5. Anything that fails twice after a Sonnet fix goes to Opus. Anything that fails after Opus goes to Fable with the full log, as a design question.

Rules:

- Persistence is a player-facing feature with visible states (saving, saved, retry). Its UI is part of the ticket.
- The editor hides thermal throttling and memory pressure. G5 runs on the device.
- No new content during hardening. The surface area is frozen until the matrix passes.

Hand-off: a passing test suite, the milestone's evidence record, and a build you would hand to a stranger.

## Stage 8 — Shipping, retro and post-launch

**Model: Sonnet (6 Sol) for the release work, Haiku (Luna) for the checklist, Fable (Astra) once for go/no-go and once for the retro.** Shipping is mostly procedure. The two judgment calls are whether to ship and what the project taught the template, and those deserve the top model with everything in front of it.

What comes out: a released build, the platform listing, a retro that improves the kit, and a post-launch loop that feeds back into Stage 5.

How to run it:

1. Haiku generates the release checklist from the brief's acceptance tests and the platform's requirements, and ticks it off from logs. Anything it cannot verify from a log goes to you.
2. Sonnet handles the release mechanics: build config, version bump, platform settings, privacy and access settings, store text from the one-page summary. Platform rules (ratings, child accounts, chat defaults, AI-content disclosure) are fetched and cited from current documentation, never recalled.
3. Fable gets the checklist, the latest evidence records and 5 screenshots. One question: ship, or what blocks it. Accept the answer.
4. Ship to the smallest audience first (family, friends, private listing). Collect one week of play before widening.
5. **Retro.** Fable reads the evidence records, the friction notes in the continuity file and the git log, and proposes at most three edits to a skill, standard or tool. Each edit states the observed problem and its evidence, the change, how to test it, and whether it is project-only or a template candidate. You approve what gets promoted to the template.
6. Post-launch, bug reports and observations go through Haiku into the observation list, and the Stage 5 loop runs on a cadence you set.

Rules:

- No new features in the shipping branch. Ideas go into the deferred list in `PROJECT.md` for the next cycle.
- Keep `DECISIONS.md` going after launch. The second version is built from it.
- A retro edit that didn't help in a real project does not enter the template.

Hand-off: the live build, `docs/RELEASE.md` with version, date and known issues, and the retro's approved edits applied to the template.

## Quick reference

| Stage | Primary model | Support | Why | Hand-off |
| --- | --- | --- | --- | --- |
| 0 Pitch card | Opus (6.1 Sol) | — | Range and feel for fun; output is disposable | `PROJECT.md` |
| 1 Brief + art bible | Fable (Astra) | You (references, every visual value) | Most expensive documents to get wrong | `docs/BRIEF.md`, `docs/ART_BIBLE.md` |
| 2 Architecture + contract + tickets | Fable (Astra) | Opus (6.1 Sol) writes tiered tickets | Hard to reverse; tickets are mechanical | `docs/ARCHITECTURE.md`, `DECISIONS.md`, `tickets/M1/` |
| 3 Style tile + slice | Opus (6.1 Sol) builds | Fable (Astra) runs the G3 checklist | Catches the generic look before it spreads | Frozen commit, `docs/STYLE_TILE.md` |
| 4 Systems | Sonnet (6 Sol) | Opus (6.1 Sol) Complex tickets, Haiku (Luna) chores | Contract exists; cost matters | Candidate commit |
| 5 Gate loop | Scripts (G0–G2, G5), you (G6) | Fable (Astra) G3–G4, Haiku (Luna) record | Correctness is scripted, taste is a checklist, acceptance is yours | `docs/evidence/<milestone>/` |
| 6 Content | Sonnet (6 Sol) | Opus (6.1 Sol) hero items, Fable (Astra) batch gate | Volume work; top model only at the gate | Merged batch, `assets/ASSET_SOURCES.md` |
| 7 Hardening | Opus (6.1 Sol) design | Sonnet (6 Sol) tests, Fable (Astra) stubborn bugs | Engineering quality over art | Passing suite, evidence record |
| 8 Shipping + retro | Sonnet (6 Sol) | Haiku (Luna) checklist, Fable (Astra) go/no-go and retro | Procedure, plus two judgment calls | `docs/RELEASE.md`, template edits |

## Rules that matter more than model choice

1. **Decide in one session, build in another.** Design and code in the same context always drifts toward defaults. The file between them is the product.
2. **Every session starts from the same four pastes:** the one-page brief summary, `DECISIONS.md`, `docs/STYLE_TILE.md`, and one ticket. Not the whole brief, not the last chat.
3. **One ticket per session.** End the session when it closes. Context that survives a ticket carries the previous ticket's habits into the next.
4. **Models choose nothing visual.** Colors, fonts, assets, sounds and lighting values come from you or the art bible. A model picking from a store is where the sameness comes from.
5. **Specify values, not adjectives.** Hex codes, stud sizes, seconds, asset IDs. "Punchy" and "clean" produce the default.
6. **The critic never built it, and never fixes it.** Review in a fresh session with no build context, against the written checklist. Critics produce evidence; builders produce edits.
7. **Correctness is scripted, taste is a checklist, acceptance is yours.** Scores are never averaged across gates; a correctness failure blocks acceptance whatever presentation looks like.
8. **Two rounds, then decide.** Two critique-and-fix rounds per candidate, then accept, fix or rescope. A milestone that fails after two full rounds is rescoped or shelved.
9. **Rebuild, don't patch, after three strikes.** Repeated patches accumulate the old look.
10. **Real device, real player, early.** The editor hides thermal, touch and memory problems; you hide the hints you give your kids.
11. **Escalate up the ladder with evidence.** Start at the model the ticket's tier names; Sonnet fails twice, Opus gets both attempts. Opus fails twice, Fable gets a design question, not a coding one.
12. **Spend the top model on decisions, not output.** Fable at the gates (brief, contract, critique, go/no-go, retro) and nowhere in the production line.
13. **Every process step names the model weakness it covers.** Keep that list in the kit. When a model upgrade makes a step unnecessary, remove the step; if the failures return, put it back.
