# Research behind the template

Source material for template maintenance. Not copied into games by
`tools/new-game.ps1`; the sibling
[Game_Dev_Library](https://github.com/darthreckoner/Game_Dev_Library) keeps the
dated archive. Read it when choosing an engine or an asset service, when a retro
questions a process step, or before building a new kit. Appendix A of the kit
document goes stale fastest; refresh before relying on a tool claim older than
six months.

| File | What it is |
|---|---|
| `2026-09-25-ai-solo-game-dev-kit.md` | The evidence and tool landscape: why evidence loops beat process, why the agent must see and drive the game, why builder, judge, and acceptance stay separate, the engine and asset-service tables |
| `2026-10-16-model-per-stage-guide.md` | Which model takes which seat at each stage, and the thirteen rules that matter more than model choice |

## Vocabulary map

The research describes a fuller staged process than this template runs. The
template kept the parts the evidence supports and the designer chose (light
checks, one-shot builds, tickets) and dropped milestone contracts and formal
gate records. When the research names a file or gate, read it as:

| Research says | This template has |
|---|---|
| `PROJECT.md` pitch card, `docs/BRIEF.md` | `DESIGN.md` |
| `docs/ARCHITECTURE.md`, contract, `tickets/M1/` | Architecture and Checks sections of `BUILD_PROMPT.md`; `docs/tickets/` |
| `DECISIONS.md` | The Changes section of `DESIGN.md`; Assumptions in `STATE.md` |
| `docs/ART_BIBLE.md`, `docs/references/`, G3 checklist, `docs/STYLE_TILE.md` | `art/ART_BIBLE.md` (Direction and Look checklist), `art/references/` |
| Gates G0 build, G1 rules, G2 behavior, G5 performance | The `build-check` skill: build, rule tests, scenarios with state assertions |
| G3 presentation, G4 UX | The Director's review with the look checklist (`art-direction`) |
| G6 play, `accepted: true` | The playtest and the Designer's verdict in `STATE.md` |
| Evidence record `docs/evidence/<milestone>/` | Checks section of `STATE.md` plus `docs/captures/<build>/` and `docs/reviews/` |
| Ticket tiers, escalation, two-round cap, kill rule | Tickets and "Rounds and stop rules" in `AGENTS.md` |
| Friction notes, assumption register | Friction log in `STATE.md`; `docs/process/ASSUMPTIONS.md` |
| `evidence-run`, `critique`, `prototype-brief` skills | `build-check`, `art-direction` + `game-director` Phase 3, `game-director` Phase 1 |
| `tools/sync-skills.ps1` | `tools/sync-codex-skills.ps1` |

Model names in the guide are paired with OpenAI equivalents in parentheses; the
template's defaults are the Claude seats in `AGENTS.md`.
