# AI Solo Game-Development Kit

Tool landscape researched 2026-09-25. Structure revised 2026-10-16.
Companion: **AI Game Development Guide: Which Claude Model for Each Stage** (same folder). The kit defines the roles, loops, gates, standards and files. The guide says which model takes each seat at each stage. File names, gate names and ticket tiers are shared between the two.

**Method and limits.** The tool research is web research only; no tool below was installed or run. Capabilities, tool counts, prices and dates come from project READMEs, vendor pages, papers and articles. Several articles come from vendors selling a competing product (StraySpark, Ludus AI, Meshy); their claims are marked. GitHub star counts are approximate figures from search results on 2026-09-25. Everything labeled a proposal is a recommendation for the template, not an adopted decision. The Railroad Wars brief, GDD and templates were not changed by this document.

## Summary

1. **More process does not make better games; evidence loops do.** The largest public Claude Code game-studio template (about 49 agents and 70+ skills) measured its own process tiers. Its heavier tier cost several times more to reach working code and ranked last on play quality. It now defaults to its lightest mode. Anthropic's long-running harness work reached a similar conclusion: keep the components that fix an observed model limitation, remove the rest when models improve. This kit therefore starts minimal (§1) and grows only through the retro loop (§4.3).
2. **The agent must see and drive the running game.** Visual feedback raised a frontier model from 41.1% to 52.0% on a 333-task game-development benchmark. Pairing a coding agent with a separate playtester agent beat an agentic-coding baseline by 14.6 points. Engine bridges, headless runs, recordings and a game-side automation API matter more than extra agents.
3. **Keep the builder, the judge and the human acceptance gate separate.** Models grade their own work generously. The best model found only 48% of verified game bugs in a QA benchmark. Agent critique finds problems; it cannot sign off a milestone. Deterministic checks gate correctness, a checklist judges presentation, and you decide whether the game is fun.
4. **Art direction stays human-controlled.** 2D graphics tasks scored 33% in the same benchmark, the lowest category, and the recurring failure across this template's projects is a generic "AI-built" look. The art bible is a required input to the first build, reference images are mandatory, every visual value is chosen by a person, and presentation is judged against a binary checklist, never a score.
5. **Make it portable and opt-in.** Use Agent Skills (the SKILL.md open standard), MCP, and one AGENTS.md so the same kit works in Codex and Claude Code. Engine-specific material lives in per-engine kits that a project copies in only after choosing its engine. This matches the Hobby Template's rule of no agent framework by default.
6. **For Railroad Wars now:** pin Godot, split the train simulation from its presentation, drive scenarios headlessly, record clips for critique, and run the Milestone 1 benchmark pack through three small skills under a fixed budget (§7). Hold off on 3D, audio generation and multi-agent building until a milestone needs them.

## 1. The minimum kit

Nothing beyond this exists until a retro produces evidence that it is needed.

| Piece | What it is | Why it earns its place |
|---|---|---|
| `prototype-brief` skill | Pitch card → milestones with "pass when" criteria → scenario list → contract | Agreed pass criteria before building is the one process step every source agrees on |
| `evidence-run` skill | Freeze a commit → run gates G0–G5 → write an evidence record | Scripts decide correctness; the record is what you and the critic read |
| `critique` skill | Separate-context critic runs the art-bible checklist and UX checklist on a frozen build; produces observations, not edits | Builders grade themselves generously; a fresh context shares fewer blind spots |
| One engine bridge | Godot CLI plus one free MCP (§A.1) | The agent must run the game and see output |
| Six files | `PROJECT.md`, `docs/BRIEF.md`, `docs/ART_BIBLE.md`, `DECISIONS.md`, `docs/STYLE_TILE.md`, `docs/evidence/` | The files between sessions are the product; they replace memory |

Explicitly deferred until a retro asks for them: parallel builders, an integrator role, asset-generation skills, the `retro` skill itself (run it by hand the first two times), per-engine kits for engines no project uses, and any paid bridge.

## 2. Evidence that shapes the design

| Source | Finding | Design implication |
|---|---|---|
| [Anthropic, *Harness design for long-running application development*](https://anthropic.com/engineering/harness-design-long-running-apps) (Mar 24, 2026) | Planner, generator and evaluator roles. The evaluator was calibrated with few-shot scored examples and weighted criteria. Generator and evaluator agreed a "sprint contract" before each sprint. On a 2D retro game-maker task, a solo run took 20 min and $9 and its core was broken; the harness took 6 h and $200 and worked end to end. Later they removed sprint decomposition and moved the evaluator to one final pass as models improved. Its key principle: "every component encodes an assumption about model limitations worth stress-testing." | Separate generation from evaluation. Calibrate critics with anchored examples. Agree pass criteria before building. Record which model limitation each harness part compensates for, and retest when models change. |
| [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) (MIT, ~25k★) | 49 agents in a director/lead/specialist hierarchy, 70+ slash-command skills, 14 hooks, 13 path-scoped rules, 39 templates and a `modes.rigor` knob. The project reports building four games from one brief at different rigor levels. Blind reviewers and a human playtest ranked the heavier "standard" build last; its extra documents added traceability but not quality. Minimal is now the default. | Borrow its path-scoped rules, templates, validation hooks and skill-testing ideas. Don't adopt the org chart. Note the limits of this evidence: one brief, self-reported. |
| [Fable Cities review](fable-cities-benchmark-review-2026-09-25.md) (this repo) | Builder, critic and integrator loops ran about 20M output tokens without any module clearing its threshold. Single visual scores hid broken interaction, and reviewing a live dev server made verdicts hard to attribute. | Separate gates instead of one score. Review a frozen build. Bound the iteration count. Keep human acceptance separate. Add a kill rule. |
| [GameDevBench](https://arxiv.org/abs/2602.11103) (Feb/Jun 2026) | 333 tutorial-derived tasks. Best success was 53.8%. Visual feedback raised GPT-5.4 from 41.1% to 52.0%. Gameplay tasks scored 51.4% and 2D graphics tasks 33.0%. | Give agents screenshots and recordings. Expect graphics and asset work to need the most human control. |
| [Play2Code / PlaytestArena](https://arxiv.org/abs/2605.28258) (May 2026) | A coding agent and a GUI playtester agent shared memory across play-test cycles. The pair reached a 66.8% rubric pass rate, 14.6 points above an agentic-coding baseline and 37.1 above single-pass generation. | Treat the playtester as a first-class role, and have it play the real build. |
| [GBQA](https://arxiv.org/abs/2604.02648) (Apr 2026) | 30 games with 124 verified bugs. The best model (named in the paper as Claude 4.6 Opus, thinking; verify the exact name against the paper) found 48.39% of them. | Agent QA is a discovery aid, not an acceptance gate. |
| Playwright MCP [#1148](https://github.com/microsoft/playwright-mcp/issues/1148), Chrome DevTools MCP [#403](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/403) | Browser automation can locate the `<canvas>` element but cannot see or target objects inside it. | Every game exposes a small automation API: load a scenario, send actions, query state, dump state as JSON. Tests and critics use state; pixels are for presentation review. |

## 3. Roles

A few roles, not a studio org chart. The "Model" column is the guide's assignment; the guide has the reasoning.

| Role | Realized as | Model (OpenAI equivalent) | Sees | Writes | Runs when |
|---|---|---|---|---|---|
| Director | You, plus the main session with AGENTS.md | You decide; Fable (Astra) drafts | Whole project | Everything in scope | Always |
| Designer | `prototype-brief` skill | Opus (6.1 Sol) for the pitch, Fable (Astra) for the brief, bible and contract | Design docs, genre playbooks | Design docs only | Ideation and each milestone start |
| Builder | Main session; parallel sessions in git worktrees only for independent modules | Sonnet (6 Sol); Opus (6.1 Sol) for Complex tickets | Code and assets for its ticket | Its ticket's files | Implementation |
| Integrator | A step the main session runs when more than one builder exists | Opus (6.1 Sol) | All modules | Merges, contract fixes | Only with parallel builders |
| Rules verifier | Scripts and automated tests, not an LLM | — | Build and scenarios | Test results | Every change |
| Playtester critic | Separate-context agent with input and screenshot tools | Fable (Astra) | Frozen build, scenario list | An evidence record | Milestone candidates |
| Presentation/UX critic | Separate-context agent, optionally a different model family | Fable (Astra), or Astra when the builder was Claude | Screenshots, clips, art bible checklist, UX checklist | Item-by-item results and observations | Milestone candidates |
| Evidence clerk | `evidence-run` skill, mechanical step | Haiku (Luna) | Test output, screenshots, your notes | The evidence record | Every candidate |
| Asset producer | `asset-request` procedure | You pick; Sonnet (6 Sol) normalizes | Asset spec, art bible | Assets and a provenance record | On request |
| Process critic | `retro` skill | Fable (Astra) | Evidence records, continuity, corrections | At most three proposed skill/standard edits | End of milestone |

Notes:

- **Parallelism is optional.** Claude Code subagents report to a parent and suit read-only critique. [Agent teams](https://code.claude.com/docs/en/agent-teams), available since February 2026, let peer sessions message each other and suit parallel independent modules. Neither is needed for a Milestone 1 prototype. AGENTS.md already allows delegation "when applicable project or skill instructions call for it," so a critique skill can require a separate context without changing that rule.
- **Cross-model critique is worth testing.** Both Codex and Claude are available. A critic from a different model family may share fewer blind spots with the builder. This is a hypothesis to measure in the pilot (§7), not an established result.
- **Critics produce evidence, not edits.** A critic that fixes what it found is grading its own work again.

## 4. The loops

### 4.1 Idea to first playable

Confidence comes from three sources: standards that load at the right step, lessons carried over from earlier projects, and an explicit ranking of risks. The Railroad Wars brief is already a strong example of the final output.

1. **Capture.** Record the raw idea without filtering. Ask only what changes the direction: player fantasy, platform, session length, reference games.
2. **Pitch card** (one page at the top of `PROJECT.md`): player fantasy and core verbs; the core loop at three timescales (seconds, minutes, session); three pillars and at least one anti-pillar; reference games and what to take from each; scope class (jam, prototype, vertical slice).
3. **Risk ranking.** List the largest unknowns in fun, technology, art and scope. The first playable must answer the top fun risk; see Railroad Wars' "first question to answer".
4. **Variants.** Present two to four concept or scope options with their trade-offs, then wait for the human's choice, as the Hobby Template requires.
5. **Engine choice.** Only if not yet decided; use the matrix in §A.2.
6. **Brief** (`docs/BRIEF.md`). Milestones with "pass when" criteria, a scenario list per milestone, a deferred list, and an explicit rule not to silently turn brainstorm ideas into requirements.
7. **Art bible** (`docs/ART_BIBLE.md`), written in a separate session. See §5 for required contents. It ends with the G3 checklist.
8. **Contract** for Milestone 1: the pass criteria and scenario list restated as tests a script can run, approved by you before any ticket is written.
9. **Benchmark pack** for Milestone 1, in the format from the Fable Cities review.

**Genre playbooks** (`prototype-brief/references/genres/*.md`) are where cross-project learning builds up. Each covers typical core-loop shapes, known pitfalls, useful references, and prototype questions that proved decisive. Railroad Wars would seed a "logistics/transport + tactical" playbook. For commercial ambitions, an optional market check can use [Ludo.ai](https://ludo.ai/features/game-ideator) (API and MCP in beta since March 2026) or manual Steam comparables.

### 4.2 Build, evidence, critique, decide

This is the Fable Cities loop with the fixes from the review applied.

```
contract ──► build ──► freeze candidate ──► gates G0–G6 ──► evidence record ──► you: accept / fix / rescope
   ▲                                                                                  │
   └──────────── fix the top supported defects (max 2 rounds, then you decide) ◄──────┘
```

- **Contract.** Before building, write the milestone's pass criteria and scenario list and have them approved. This is the "sprint contract" from Anthropic's harness and the "Pass when" lines in the brief.
- **Freeze.** Test an immutable commit, never a hot-reloading dev session.
- **Gates.** Scores are never averaged across gates. A failure in G1 or G2 blocks acceptance whatever G3 says.

| Gate | Evidence | Judge |
|---|---|---|
| G0 Build | Builds and launches; error log is empty | Script |
| G1 Rules | Unit and scenario tests on the simulation core | Script (pass/fail) |
| G2 Behavior | Scripted scenarios with state assertions, plus recordings | Script, then clips for review |
| G3 Presentation | Screenshots and clips against the art bible's checklist: each item pass/fail, with written observations. No numeric score. | Critic agent, fresh context |
| G4 UX and accessibility | Checklist and a critic walkthrough | Critic agent, fresh context |
| G5 Performance | Fixed scenario on the target device, against a budget set before judging, with no concurrent builders | Script |
| G6 Play | Uncoached human playtest | You (only you set `accepted`) |

Why G3 is a checklist and not a 0–4 scale: the Fable Cities review found that a single visual score hid broken interaction and invited proxy optimization. A checklist of 8 to 15 binary items, each checkable from a screenshot (palette only from the list; no flat single-color surface larger than N units; lighting values match the bible; every asset from an approved source; UI font and radius as specified), can be argued with item by item. The critic adds observations; it does not add up points.

- **Budget.** Two critique/fix rounds per candidate, then a human decision. Stop early at a plateau: when the same defect IDs persist across rounds.
- **Kill rule.** A milestone that fails acceptance after two full rounds is rescoped or shelved. The loop does not run a third time against the same contract. This is the rule Fable Cities lacked.
- **Evidence record.** One file per run in `docs/evidence/<milestone>/`:

```yaml
run_id: m1-2026-10-02-a
commit: <sha>              # frozen candidate
engine: godot 4.7.x        # plus renderer/device profile for G5
scenario: m1/two-station-loop@v2   # seed and input script included
gates: {G0: pass, G1: pass, G2: fail, G3: 11/13 items, G4: n/a, G5: pass}
g3_failed_items: [palette-only, no-flat-surfaces]
defects: [RW-012 cars leave track on tight curve (clip 00:14)]
critic: {model: <id>, checklist: art-bible@v1, confidence: medium}
artifacts: [clips/m1-a.avi sha256:…, shots/*.png]
round: 1                   # of 2
human: {played: false, accepted: null}
```

### 4.3 Improving the process itself

1. **Capture friction as it happens.** When you correct the agent, a tool fails, a standard is missing, or tokens are wasted, add one line to the continuity file or the evidence record.
2. **Retro at each milestone.** The `retro` skill (by hand for the first two milestones) reads the evidence records, the friction lines and the git log. It proposes at most three changes. Each change states the observed problem and its evidence; the edit to a skill, standard or tool; how to test the edit (a replay of the failing situation or a small eval prompt); and whether it applies to this project only or is a template candidate.
3. **Test the skills themselves.** Each skill gets two or three eval prompts with expected behavior. Precedents: Claude Code Game Studios' `/skill-test` and `/skill-improve`; GodotPrompter's validator, which enforces a 16 KB budget per SKILL.md; the skill-creator eval workflow.
4. **Promote deliberately.** A change moves into the Hobby Template only after you approve it, it demonstrably helped in a project, and project-specific content is removed. This matches the template's rule that updates require deliberate adoption.
5. **Keep an assumption register** (`docs/ASSUMPTIONS.md` in the template). One line per harness component naming the model limitation it compensates for and the evidence. Remove components when a model upgrade makes them unnecessary; add them back if failures return. Seed it with the rows below.

| Component | Model limitation it covers | Evidence |
|---|---|---|
| Separate critic context | Builders grade their own work generously | Anthropic harness; GBQA 48% |
| Contract before build | Models invent requirements under ambiguity | Anthropic harness; Fable Cities |
| Automation API, state over pixels | Browser tools cannot see inside a canvas | Playwright #1148, DevTools #403 |
| Screenshots and clips to the critic | Text-only agents miss visual defects | GameDevBench +10.9 points with visual feedback |
| Binary G3 checklist | Single visual scores hide broken interaction and invite proxy optimization | Fable Cities review |
| Human-chosen visual values | Models default to a generic look; 2D graphics is the weakest task class | GameDevBench 33%; this template's own projects |
| Two-round cap and kill rule | Loops run indefinitely without clearing thresholds | Fable Cities ~20M tokens |
| One ticket per session | Context compaction loses the spec; drift accumulates | Hobby Template experience |

## 5. The standards pack

Each item is a short file inside the skill that uses it. L2 standards never load at startup; the Agent Skills standard's progressive disclosure keeps them cheap until a skill fires.

- **Design** (`prototype-brief`): pitch-card template, pillar and anti-pillar guidance, core-loop timescales, risk-ranking method, milestone and pass-criteria template, contract template, deferred-ideas rule, genre playbooks.
- **Art direction** (`prototype-brief/references/art-bible.md`, required before the first build):
  - palette as hex values with named slots (ground, accent, UI dark, etc.), and the rule that no color outside the list appears
  - shape language and silhouette rules; camera, scale and pixel or texel density
  - lighting as exact engine settings, not adjectives
  - material set, and the approved asset sources (store authors, packs, generators) with the rule that the builder never picks an asset not on the list
  - UI style: font, corner radius, outline, layout grid; a named avoid list
  - 3 to 5 reference images in `docs/references/`, chosen by a person
  - the G3 checklist: 8 to 15 yes/no items, each checkable from a screenshot
  - asset-spec template and engine import settings (for example, nearest filtering for pixel art)
- **Cross-engine architecture** (engine kits): a deterministic simulation core separated from presentation; fixed timestep and seeded RNG; tuning values in one data file (`Config`); an automation API for loading scenarios, sending actions, querying state and dumping JSON; a debug overlay; save versioning.
- **Engine specifics:** Godot: composition over inheritance; "call down, signal up"; sparing autoloads; Resources for data; typed GDScript with warnings escalated. Unity: assembly definitions, ScriptableObjects for data, Input System. Unreal: C++ core with Blueprint content, subsystems, Gameplay Ability System only when warranted. three.js: systems or ECS over a fixed-step simulation loop.
- **Testing**, the game test pyramid: pure-logic unit tests; scenario tests with scripted input and state assertions; recorded runs for critique; a human playtest protocol (uncoached, think-aloud, observer does not help, hints counted).
- **UI/UX:** feedback and "juice" checklist; onboarding by doing; readable at target resolution; input remapping; text scaling; color-blind-safe signaling; subtitles. The basic level of the Game Accessibility Guidelines is the floor. This becomes the G4 checklist.
- **Budgets:** target device, frame-time budget, memory or draw-call ceilings, all set before judging. This is the G5 budget.
- **Evidence-record schema** (§4.2) and the **asset provenance** format (§A.3).
- **Ticket template:** inputs, done condition including the test that proves it, files it may touch, and a difficulty tier (Routine, Standard, Complex, Ambiguous) that maps to a model per the guide.
- **Session-start protocol** (one line in AGENTS.md): every build session begins with the one-page brief summary, `DECISIONS.md`, `docs/STYLE_TILE.md` and one ticket, and nothing else.

## 6. Files and template layout

### 6.1 Shared file map

These names are used by both this kit and the guide.

| Artifact | File | Owner |
|---|---|---|
| Pitch card, deferred ideas | `PROJECT.md` | You |
| Design brief, milestones, scenario lists, contracts | `docs/BRIEF.md` | Fable drafts, you approve |
| Art bible with G3 checklist; reference images | `docs/ART_BIBLE.md`, `docs/references/` | You choose every value |
| Architecture note | `docs/ARCHITECTURE.md` | Fable |
| Decisions log, one dated line per choice | `DECISIONS.md` | Every session appends |
| Tickets, contract at the top | `tickets/<milestone>/` | Opus writes, you approve |
| Style tile record: lighting values, materials, asset IDs that passed | `docs/STYLE_TILE.md` | Stage 3 |
| Evidence records | `docs/evidence/<milestone>/` | `evidence-run` |
| Asset provenance | `assets/ASSET_SOURCES.md` | Asset procedure |
| Assumption register | `docs/ASSUMPTIONS.md` | Retro |
| Release notes | `docs/RELEASE.md` | Shipping |
| Friction notes, session summaries | the continuity file | Haiku appends |

### 6.2 Layout

Additions to the Hobby Template. Nothing engine-specific loads until a project opts in. Items marked *later* are not built until a retro asks for them.

```
AGENTS.md                    (+ "Game projects" section: which skill when; session-start protocol; bridge and asset rules)
CLAUDE.md                  + one line, "@AGENTS.md", so Claude Code and Codex share one instruction file
PROJECT.md                   (+ pitch-card fields: fantasy, pillars/anti-pillars, first-playable question)
DECISIONS.md
docs/
  BRIEF.md  ART_BIBLE.md  ARCHITECTURE.md  STYLE_TILE.md  ASSUMPTIONS.md  RELEASE.md
  references/               reference images
  evidence/<milestone>/     evidence records, clips, shots
tickets/<milestone>/
assets/ASSET_SOURCES.md
.agents/skills/
  context-maintenance/       (existing)
  prototype-brief/         + pitch card → brief → art bible → contract; references/genres/*.md, references/art-bible.md
  evidence-run/            + freeze → G0–G5 → evidence record; references/evidence-schema.md
  critique/                + separate-context critic; references/checklists/{presentation,ux,feel}.md
  playtest-kit/            later: human playtest script and observation form
  asset-request/           later: spec → generate → normalize → validate → provenance; references/providers/*.md
  retro/                   later: friction → at most 3 skill/standard edits, each with a test
kits/                      + copied into a project only after an engine is chosen
  godot/                   + now (Railroad Wars)
  unity/  unreal/  web-threejs/  blender/   later
    skill: engine-<name>/ (architecture, testing, automation API, capture, import settings, docs version)
    tools/ (run-tests, run-scenario, capture, export scripts)
    mcp.example.json (recommended bridges; keys read from environment variables)
tools/sync-skills.ps1      + mirrors .agents/skills → .claude/skills (see §8 step 0)
```

Per project, after setup: `.mcp.json` (Claude Code) and Codex `config.toml` entries listing only the bridges this project uses; `docs/evidence/<milestone>/`; `assets/ASSET_SOURCES.md`; the kit's `tools/`.

## 7. Applying it to Railroad Wars (the pilot)

Proposals, consistent with the prototype brief and the Fable Cities review. Nothing has been adopted.

1. **Pin the engine.** Check the installed Godot version against the 4.7 line and record it in the brief or README.
2. **Split simulation from presentation.** Make routes, the track graph, train movement, cargo, contracts and turn resolution plain GDScript classes that run headless at a fixed step. Scenes render state and forward input. The M1 criteria then become headless tests: delivery registers once; invalid routes cannot dispatch; reset removes stale state; two different valid layouts produce corresponding journeys.
3. **Scenario files.** Each describes a map, placed track and orders. One entry point runs a scenario headlessly and dumps final state as JSON for G1/G2. The same scenario with rendering and `--write-movie` produces the clips for G3 (for example, cars following curves).
4. **Art bible first.** Before any visual work, write the art bible with reference images and the G3 checklist, even for placeholder art. Placeholders still have a palette.
5. **Bridges.** Start with the Godot CLI and Coding-Solo/godot-mcp (free; runs the project and captures debug output). Add a screenshot and input bridge (godot-ai, GDAI MCP or Godot MCP Pro) only if agent-driven editor work proves worth it.
6. **Assets.** Keep the placeholders the brief calls for. After an art direction is chosen, trial PixelLab's Wang tilesets and map objects against simple hand-made shapes, and record provenance.
7. **Pilot budget (proposal).** The subscription plans make tokens close to free at this scale, so the budget is in attention and rounds: 3 build sessions for M1 tickets, 2 critique/fix rounds, roughly 10 hours of your time, 2 calendar weeks. If M1 is not accepted inside that, the kill rule applies and the retro answers why.
8. **Measure.** Which gates caught real issues; rounds used; sessions and wall-clock per ticket; how often you corrected the agent; whether the cross-model critic found anything the same-model critic missed. That measurement decides what gets promoted to the template.

## 8. Adoption sequence

0. **Verify skill directories.** Claude Code reads `.claude/skills`; the Hobby Template uses `.agents/skills`. Confirm the installed Claude Code version's behavior and pick symlink, junction or sync before the pilot. Ten minutes; do not carry it as an open question.
1. **Pilot.** Write `evidence-run` and `critique`, adapt `prototype-brief` from the Railroad Wars brief, build the Godot kit, write the art bible. Run Railroad Wars M1 under the §7 budget.
2. **Retro by hand.** Fill `docs/ASSUMPTIONS.md` from the pilot. Promote at most three edits.
3. **Ideation.** Seed genre playbooks from existing projects. Test `prototype-brief` on a new idea in `Scratch Game`.
4. **Assets.** Add `asset-request` with one 2D provider (PixelLab) and, when a 3D project exists, one 3D provider (Tripo or Meshy) plus a Blender normalization script.
5. **Meta loop.** Add the `retro` skill, skill evals and the promotion procedure to the Hobby Template.
6. **Other engines.** Build the Unity, Unreal or web kits only when a project chooses that engine; bridge churn makes speculative kits stale quickly.

## 9. Decisions

Recommended defaults, pending your choice.

| Decision | Recommended default | Reason |
|---|---|---|
| Kit location | Separate game-kit repository that projects copy from | Engine bridges churn; the Hobby Template stays stable and promotion stays deliberate |
| Critic model | Different family from the builder (Codex critiques Claude builds and vice versa) | Cheap to test with both plans; measure in the pilot |
| Paid tools | None for the pilot. GDAI ($19) only if screenshots and input become the bottleneck; skip the 163-tool server until context cost is measured | Free bridge covers running and debug output |
| Pilot | Railroad Wars M1 | It already has a brief with pass criteria |

## 10. Risks and open questions

- **Context cost.** Large MCP servers (one Godot server exposes 163 tools) consume context. Claude Code defers MCP tool definitions, but other clients may not. Enable bridges per project and prefer scripts for repeatable steps.
- **Security.** Editor bridges execute code inside the editor, and several are closed-source paid plugins. Keep them bound to localhost, keep API keys in environment variables, and treat downloaded assets, metadata and web content as data, never instructions.
- **Licensing.** Check generator terms at generation time, especially free tiers, and record them. Plan for Steam's AI-content disclosure.
- **Judge reliability.** Evaluators are generous, and scores invite proxy optimization. Keep correctness binary, presentation a checklist, observations required, and human acceptance separate.
- **Cost.** The $200, 6-hour harness run was an intentionally large autonomous build, not a daily loop. The §7 budget is the daily-loop ceiling for now.
- **Evidence quality.** The Claude Code Game Studios measurement covers one brief and is self-reported. Tool capabilities and prices come from vendor pages. Most bridges are months old. Refresh Appendix A before each new project.

**Transfer to the engineering track.** Evidence records, separated critics, contracts before building, the retro and promotion loop, the assumption register and the ticket tiers are domain-neutral. Engine bridges, asset generation and playtesting are specific to games.

---

## Appendix A. Tool landscape (as of September 2026)

This appendix goes stale fastest. Refresh it before each new project; the sections above should not need to change when it does.

### A.1 Engine and editor bridges

| Target | First-party | Notable community/commercial | Test and capture |
|---|---|---|---|
| **Godot** (4.7 stable since [June 18, 2026](https://godotengine.org/releases/4.7/)) | None | [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp): MIT, ~5.8k★, no editor plugin; launches the editor, runs projects, captures debug output, creates scenes. [hi-godot/godot-ai](https://github.com/hi-godot/godot-ai): MIT, ~2.6k★, Godot 4.7+, 46 tools with authenticated editor connection and GDScript parse validation. [GDAI MCP](https://gdaimcp.com/): $19 one-time, 4.2+, editor and game screenshots, input simulation, debugger errors. [Godot MCP Pro](https://godotengine.org/asset-library/asset/4961): $15, proprietary, 4.4+, 163 tools including runtime input, screenshot compare, testing and profiling. | [GUT](https://github.com/bitwes/Gut) or [gdUnit4](https://github.com/godot-gdunit-labs/gdUnit4) (headless CLI, JUnit XML, GitHub Action). [PlayGodot](https://github.com/Randroids-Dojo/PlayGodot) (Playwright-style input and screenshots). Movie Maker mode (`--write-movie`) for fixed-frame-rate recordings. |
| **Unity** | [Official MCP server](https://unity.com/blog/unity-ai-mcp-how-to-get-started) in the Unity AI assistant package 2.11+. Requires Unity 6 and a Unity AI trial or subscription. Open beta started May 4, 2026, with an AI Gateway for bringing your own models. Unity says it may change. | [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp): MIT, ~13.8k★, Unity 2021.3–6.x, 40+ tools including `run_tests`, profiling and builds. | Unity Test Framework in batch mode. CI needs license activation (GameCI handles it). |
| **Unreal** | UE 5.8 (June 17, 2026) ships an **experimental** [first-party MCP plugin](https://www.strayspark.studio/blog/epic-official-mcp-plugin-ue5-8-vs-third-party). The server runs inside the editor at `127.0.0.1:8000/mcp` with a deliberately minimal toolset. | [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp): Blueprint creation, node wiring, compile. [Ludus AI](https://ludusengine.com/blog/unreal-engine-mcp-alternative): commercial whole-project index; speed and cost claims are the vendor's. StraySpark Unreal MCP: $129; tool counts are the vendor's claim. | Automation framework and Gauntlet. Blueprints are binary assets, so the agent needs the editor bridge to read or change them. |
| **three.js / web** | n/a (the browser is the bridge) | [Playwright MCP](https://github.com/microsoft/playwright-mcp) to drive the game; [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) for performance traces. Neither sees inside the canvas. [Needle Inspector](https://needle.tools/needle-inspector-devtools-for-threejs) adds three.js scene inspection with MCP. | Playwright plus an exposed `window.__game` test API. Seeded RNG and deterministic ticks. |
| **Blender** | [Blender Lab MCP](https://projects.blender.org/lab/blender_mcp): official, v1.0.3 on Sep 11, 2026. Python API access, blend-file forensics, viewport screenshots and thumbnail renders, API/manual search. | [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp): ~25k★; integrates Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin and Hunyuan3D. | Headless `blender -b -P script.py` for repeatable normalize/export steps. |

**Guidance.** Use MCP for exploratory work and editor manipulation. Use scripts and CLIs for anything repeatable (tests, exports, asset normalization) because scripts are deterministic, cheaper and reviewable. Official Unity and Unreal bridges are beta or experimental, so keep engine specifics isolated in kits and expect churn.

### A.2 Choosing an engine for agent-driven work

Analysis, not a measured benchmark.

| | Godot | Unity | Unreal | three.js | Roblox |
|---|---|---|---|---|---|
| Can the agent read and diff the content? | Yes: `.tscn`/`.tres` and GDScript are text | C# yes; scenes and prefabs are verbose YAML with GUID references | C++ yes; Blueprints and assets are binary `.uasset` | Everything is code | Luau yes; the place file is editor-bound unless Rojo syncs it to disk |
| Headless tests and CI | Straightforward | Workable, with licensing friction | Heavy | Easiest | Limited; TestEZ in Studio, run-in-Studio automation via MCP or Open Cloud |
| Agent bridge maturity | Community only, but many options | Official (paid, beta) plus a strong community option | Official (experimental) plus community and commercial options | Generic browser tools plus hooks you write | Built-in Studio MCP (used via Codex); Rojo for file sync |
| Best fit | 2D, small-to-mid 3D, fast solo iteration | Cross-platform or mobile, Asset Store ecosystem | High-fidelity 3D | Web distribution, jams, full code control | Built-in multiplayer and distribution; kids' audience already there |
| Agent friction | Low | Medium | High | Low for code; you build the engine features | Medium; lowest with Rojo plus the Studio MCP |

For Railroad Wars (top-down 2D, Windows first, solo), Godot remains the right call. The Roblox column was added 2026-10-16 from direct use, not from the September research; verify Open Cloud and TestEZ details before relying on them.

### A.3 Asset generation

| Need | Tools | Agent access | Notes |
|---|---|---|---|
| Pixel-art characters, tiles, objects | [PixelLab](https://www.pixellab.ai/mcp) | Official remote MCP | 4- or 8-direction characters and animations; Wang (top-down) and sidescroller tilesets; isometric tiles; map objects with transparent backgrounds and style matching; inpainting |
| Pixel art in many styles | [Retro Diffusion](https://retrodiffusion.ai/) | Hosted MCP | 90+ styles, free cost estimates, true-grid output |
| Sprite editing and sheets | Aseprite with a community MCP (e.g. [MalloyTheDev/aseprite-mcp](https://github.com/MalloyTheDev/aseprite-mcp)) or the Aseprite CLI | Headless Lua | Use the CLI for deterministic sheet export |
| Concept art, UI, icons | GPT Image 1.5/2, Gemini Nano Banana Pro | API | One [third-party benchmark](https://vibedex.ai/blog/best-ai-image-generator-game-art-2026) favors GPT Image for character sheets and Nano Banana Pro for props. Single source. |
| Style-consistent 2D at volume | [Scenario](https://www.scenario.com/) (custom style models) | API; community and preview MCPs | Worth it once an art bible exists |
| 3D props and characters | [Tripo](https://developers.tripo3d.ai/en) | Official [MCP](https://github.com/vast-ai-research/tripo-mcp); Tripo CLI installs an agent skill | Text, image or multiview to 3D; retopology, segmentation, auto-rig, 100+ preset motions, retargeting; GLB/FBX/OBJ/USDZ; $0.01 per credit, 10–30 credits per model. Free tier reported as non-commercial. |
| | [Meshy](https://github.com/meshy-dev/meshy-mcp-server) | Official MCP (~20 tools) | Remesh, retexture, rig, 500+ animation presets, low-poly "Smart Topology". Free-tier outputs reported as CC BY 4.0. |
| | Hunyuan3D (open weights), TRELLIS 2 (MIT), Rodin (paid hero assets) | Self-hosted or via blender-mcp | Hunyuan3D needs a large GPU and has its own license; read it before commercial use |
| Sound effects, music, voice | [ElevenLabs](https://github.com/elevenlabs/elevenlabs-mcp) | Official MCP (expanded Sep 14, 2026) | SFX of 0.5–22 s with looping, music, voice. Procedural sfxr/jsfxr is free and deterministic for retro SFX. |
| Rigging and animation | Tripo or Meshy auto-rig; Mixamo | API or manual | Retarget in-engine |

**Asset pipeline rule** (proposal):

1. A person chooses the source. The builder never picks an asset that is not on the art bible's approved list.
2. Every generation goes through an asset spec: size, frame count, pivot, palette or texel density, poly budget, and style references.
3. Normalize in a script: scale, orientation, pivot, LODs, import settings.
4. Validate: dimensions, transparency, triangle count, naming, colors within the palette.
5. Record provenance in `assets/ASSET_SOURCES.md`: tool, model version, prompt, seed, plan tier and license at generation time, date and cost.

Free tiers are a licensing trap for later commercial release. Steam requires disclosure of AI-generated content.

### A.4 Skill packs and templates to borrow from

| Project | Take | Leave |
|---|---|---|
| [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | Path-scoped rules (`src/ui/**` owns no game state; `design/gdd/**` requires sections); commit hooks that flag hard-coded values and missing doc sections; a gap-detection hook; the rigor knob; skill tests; its measurement results | The 49-agent hierarchy and heavy documentation defaults |
| [GodotPrompter](https://github.com/jame581/GodotPrompter) (MIT, 56 skills) | SessionStart hook that detects `project.godot`; 16 KB skill budget with a validator; GUT/gdUnit4 guidance; coverage of Godot 4.5–4.7 features | Loading all 56 skills when a project uses five |
| [vl4dt/godot-skills](https://github.com/vl4dt/godot-skills) | 12 compact Godot 4.7 skills as reference material | — |
| [threejs-game-skills](https://github.com/majidmanzarpour/threejs-game-skills) (MIT) | A director that scales verification to the size of the change; Playwright smoke, visual-regression and bot-playtest templates; canvas pixel metrics; seeded RNG; evidence manifests; procedural fallback when API keys are missing | "AAA" framing in its rubrics |
| [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills), [webgpu-claude-skill](https://github.com/dgreenheck/webgpu-claude-skill) | three.js API correctness (r183+ WebGPU) | — |
| [meshy-dev/game-asset-pipeline](https://github.com/meshy-dev/game-asset-pipeline) | Per-engine import checklists for scale, materials and rigs | Vendor lock-in |
| Anthropic harness article | Sprint contracts, calibrated evaluator, handoff files for context resets, assumption register | Fixed sprint decomposition on current models |

### A.5 Knowledge and documentation

- **Version-specific docs:** [Context7](https://context7.com/docs/overview) injects library documentation at query time. The Blender Lab MCP searches the Python API and manual. For Godot, pin the engine version in PROJECT.md and point the engine skill at the matching docs, because models often mix Godot 3 and 4 APIs.
- **Design and UX references** belong in skill references as links with short digests, not copied text: [Game Programming Patterns](https://gameprogrammingpatterns.com/) · the [MDA framework](https://users.cs.northwestern.edu/~hunicke/MDA.pdf) · [Game UI Database](https://www.gameuidatabase.com/) · [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/) · [Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/gaming/accessibility/guidelines)

## Sources

Orchestration and evidence: [Anthropic harness article](https://anthropic.com/engineering/harness-design-long-running-apps) · [InfoQ summary](https://infoq.com/news/2026/04/anthropic-three-agent-harness-ai/) · [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) · [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams) · [Agent Skills spec](https://github.com/agentskills/agentskills) · [GameDevBench](https://arxiv.org/abs/2602.11103) · [GUI Agents for Continual Game Generation](https://arxiv.org/abs/2605.28258) · [GBQA](https://arxiv.org/abs/2604.02648) · [LLM agents for automated game testing](https://arxiv.org/pdf/2509.22170)

Engines: [Godot 4.7 release](https://godotengine.org/releases/4.7/) · [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) · [hi-godot/godot-ai](https://github.com/hi-godot/godot-ai) · [GDAI MCP](https://gdaimcp.com/) · [Godot MCP Pro](https://godotengine.org/asset-library/asset/4961) · [StraySpark Godot MCP guide (vendor)](https://www.strayspark.studio/blog/godot-mcp-setup-claude-code-2026) · [gdUnit4](https://github.com/godot-gdunit-labs/gdUnit4) · [PlayGodot](https://github.com/Randroids-Dojo/PlayGodot) · [Unity MCP blog](https://unity.com/blog/unity-ai-mcp-how-to-get-started) · [Unity AI open beta coverage](https://app.cinevva.com/news/2026-05-04-unity-ai-open-beta) · [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) · [Epic UE 5.8 MCP overview (vendor)](https://www.strayspark.studio/blog/epic-official-mcp-plugin-ue5-8-vs-third-party) · [Ludus AI UE 5.8 MCP post (vendor)](https://ludusengine.com/blog/unreal-mcp-plugin-ue5-8-setup) · [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp) · [Blender Lab MCP](https://projects.blender.org/lab/blender_mcp) · [Blender MCP overview](https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/blender-mcp) · [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) · [Playwright vs DevTools MCP](https://stevekinney.com/writing/driving-vs-debugging-the-browser) · [Needle Inspector](https://needle.tools/needle-inspector-devtools-for-threejs)

Skills: [GodotPrompter](https://github.com/jame581/GodotPrompter) · [vl4dt/godot-skills](https://github.com/vl4dt/godot-skills) · [threejs-game-skills](https://github.com/majidmanzarpour/threejs-game-skills) · [webgpu-claude-skill](https://github.com/dgreenheck/webgpu-claude-skill) · [Sharing skills across Codex and Claude Code](https://docs.kanaries.net/articles/codex-vs-claude-code-skills) · [Context7](https://context7.com/docs/overview)

Assets: [PixelLab MCP](https://www.pixellab.ai/mcp) · [pixellab-mcp](https://github.com/pixellab-code/pixellab-mcp) · [Retro Diffusion](https://retrodiffusion.ai/) · [MalloyTheDev/aseprite-mcp](https://github.com/MalloyTheDev/aseprite-mcp) · [Scenario](https://www.scenario.com/) · [Tripo developers](https://developers.tripo3d.ai/en) · [tripo-mcp](https://github.com/vast-ai-research/tripo-mcp) · [tripo-cli](https://pkg.go.dev/github.com/vast-enterprise/tripo-cli) · [Meshy MCP](https://github.com/meshy-dev/meshy-mcp-server) · [meshy game-asset-pipeline](https://github.com/meshy-dev/game-asset-pipeline) · [3D generator comparison](https://trellis2.app/blog/best-ai-3d-model-generator) · [ElevenLabs MCP](https://github.com/elevenlabs/elevenlabs-mcp) · [ElevenLabs MCP expansion](https://www.testingcatalog.com/elevenlabs-mcp-can-now-generate-voice-music-images-video/) · [VibeDex game-art benchmark](https://vibedex.ai/blog/best-ai-image-generator-game-art-2026) · [Ludo.ai API/MCP beta](https://www.gamespress.com/Ludoai-launches-API-and-MCP-beta-to-bring-AI-game-asset-creation-into-)
