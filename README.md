# Game dev template

Repository: [Game_Dev_Template](https://github.com/darthreckoner/Game_Dev_Template).
Companion tool library: [Game_Dev_Library](https://github.com/darthreckoner/Game_Dev_Library).

A starting point for solo games built with two AI agents: you design, Claude
directs, and Codex codes. The vision lives in files, so every fresh coder session
starts from the same intent. Derived from the Hobby Template and the
game-director workflow.

## How work flows

Designer (you) → Director (Claude) → Coder (Codex)

1. **Design.** With Claude, run the design interview → `DESIGN.md`.
2. **Build prompt.** Claude writes `BUILD_PROMPT.md` and the first `STATE.md`.
3. **One-shot.** Codex, fresh session → the "One-shot build" prompt in
   `CODER_PROMPTS.md`. It installs the engine kit, builds, and runs
   `$build-check`: rule tests, scenarios, and screenshots of named moments.
4. **Play.** Note what feels flat. Claude can prepare a playtest session.
5. **Iterate.** Claude reviews the build and writes tickets in `docs/tickets/`.
   Codex implements each in a fresh session with the "Iterate on a ticket" prompt.
6. **Big change?** Update the docs and rebuild instead of patching.

## Start a project

Copy this folder's contents into an empty project folder, excluding `.git` and
`.coordination/`, or create a repository from it. The ignored `.coordination/`
folder is local maintenance correspondence, not game starter content. Then:

- Open the folder in Claude Code and ask it to start the design interview.
- Open the same folder in Codex for coding steps. Codex reads `AGENTS.md` and
  `.agents/skills/`; Claude Code reads `CLAUDE.md` (which imports `AGENTS.md`) and
  `.claude/skills/`.
- After the engine is chosen, the coder follows its kit README and replaces the
  section below.

## Run and check

This starter contains documentation only. When the engine is chosen, replace this
section with:

- the pinned engine version and exact executable paths
- how to launch the game and each test or scenario
- the commands `$build-check` uses (build, rules, scenarios, screenshots) and the
  manual check of the main interaction
- how to build or export

A passing check does not establish game feel or visual quality; only the
designer's play does.

## What belongs here

| Path | Purpose |
|---|---|
| `AGENTS.md` | Shared rules: roles, loop, game feel, checks, safety |
| `CLAUDE.md` | Claude's Director role (imports AGENTS.md) |
| `DESIGN.md` | The vision and the designer's decisions |
| `BUILD_PROMPT.md` | Self-contained prompt for a one-shot build |
| `STATE.md` | What exists, checks, assumptions, next steps |
| `CODER_PROMPTS.md` | Prompts to paste into fresh coder sessions |
| `docs/tickets/` | One file per change for the coder, copied from `TEMPLATE.md` |
| `docs/captures/`, `docs/reviews/`, `docs/playtests/` | Build screenshots, Director reviews, play sessions; created on first use |
| `.claude/skills/` | Director skills: game-director, art-direction, retro |
| `.agents/skills/` | Coder skills: build-check, context-maintenance |
| `art/ART_BIBLE.md` | Approved visual direction and readability rules |
| `assets/ASSET_SOURCES.md` | Provenance and permissions for every asset |
| `docs/process/ASSUMPTIONS.md` | Why each process step exists; reviewed at retros |
| `kits/` | Engine and service material, copied in only when chosen |

## Improving the template

Improvements come from project retros (`docs/process/template-candidates.md` in a
project). Promote a change here only with evidence that it helped and with
project-specific content removed. Existing projects adopt template updates
deliberately; nothing syncs automatically.

## Shared template and library coordination

This source workspace hosts the Astra–Claude channel at `.coordination/`.
For template/library maintenance, read its README and STATE and reply in a
new message file. The sibling library at `C:/Dev/Game_Dev_Library` points
to the same channel. Astra coordinates structural changes; in games, Claude is
Director and Art Director, with Opus 5.5 selected by the user. File delivery
does not wake an idle agent.

The shared channel and library routing are established; an indexed external
tool catalog and kit extraction are still future work. Keep the current
`kits/` paths intact until a coordinated change is assigned and verified.

## Source research

For work on this source template, use the sibling library's
[research index](../Game_Dev_Library/docs/research/2026-09-25-ai-solo-game-dev-environment/README.md). This source
maintenance pointer is not a game requirement.
