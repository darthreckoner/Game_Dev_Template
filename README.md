# Game dev template

Repository: [Game_Dev_Template](https://github.com/darthreckoner/Game_Dev_Template).
Companion tool library: [Game_Dev_Library](https://github.com/darthreckoner/Game_Dev_Library).

A starting point for solo games built with AI agents: you design, Claude
directs, and a fresh coder session builds. The vision lives in files, so every
coder session starts from the same intent, and every check leaves evidence a
reviewer can read.

## How work flows

Designer (you) → Director (Claude) → Coder (fresh session, model by ticket tier)

1. **Design.** With Claude, run the design interview → `DESIGN.md`.
2. **Build prompt.** Claude writes `BUILD_PROMPT.md` and the first `STATE.md`.
3. **One-shot.** A fresh coder session takes the "One-shot build" prompt from
   `CODER_PROMPTS.md`. It installs the engine kit, builds, and runs the build
   check: rule tests, scenarios, and screenshots of named moments.
4. **Play.** Note what feels flat. Claude can prepare a playtest session.
5. **Iterate.** Claude reviews the build and writes tickets in `docs/tickets/`,
   each with a tier that names the coder's model. A fresh session implements
   each with the "Iterate on a ticket" prompt.
6. **Big change?** Update the docs and rebuild instead of patching. Two review
   rounds on the same flat spot, then you decide.

The seats, tiers, feel rules, and stop rules are in `AGENTS.md`.

For an adopted, source-linked workflow with saved-candidate gates, use the
[game conductor](docs/process/GAME_WORKFLOW.md): `/game-conductor status` in
Claude Code or `$game-conductor status` in Codex after skill sync. It integrates
the shared Designing Games reference without adding a second acceptance owner.
Setup prepares a project proposal; engine checks and human gates require actual
project commissioning.

## Start a project

From PowerShell in this folder:

```powershell
.\tools\new-game.ps1 -Name "My Game" -Dest C:\Dev\My_Game
```

It copies the starter without `.git`, `work/`, `docs/research/`, and itself,
writes the game name into `DESIGN.md` and `BUILD_PROMPT.md`, and makes the first
commit. (Or create a repository from this one on GitHub and delete those
folders.) Then:

- Open the new folder in Claude Code and ask for the design interview. Claude is
  the Director there by default (`CLAUDE.md`).
- For each coder step, open a fresh Claude Code session, pick the model the
  prompt names, and paste the prompt from `CODER_PROMPTS.md`. The prompt tells
  the session it is the coder.
- Using Codex or ChatGPT for a ticket or a second-opinion review? Codex reads
  `AGENTS.md` natively; run `tools/sync-codex-skills.ps1` once so `$build-check`
  and the engine skill exist in `.agents/skills/`. ChatGPT gets the prompt plus
  the files it names.
- After the engine is chosen, the coder follows its kit README and replaces the
  section below.

## Run and check

This starter contains documentation only. When the engine is chosen, replace this
section with:

- the pinned engine version and exact executable paths
- how to launch the game and each test or scenario
- the commands the build check uses (build, rules, scenarios, screenshots) and
  the manual check of the main interaction
- how to build or export

A passing check does not establish game feel or visual quality; only the
designer's play does.

## What belongs here

| Path | Purpose |
|---|---|
| `AGENTS.md` | Shared rules: roles, seats, loop, tickets, feel, checks, stop rules |
| `CLAUDE.md` | Which role Claude holds in a session, and its write scope |
| `DESIGN.md` | The vision and the designer's decisions, with a dated change log |
| `BUILD_PROMPT.md` | Self-contained prompt for a one-shot build |
| `STATE.md` | What exists, checks, assumptions, friction, next steps |
| `CODER_PROMPTS.md` | Prompts to paste into fresh coder sessions, each naming its seat |
| `docs/tickets/` | One file per change for the coder, copied from `TEMPLATE.md` |
| `docs/captures/`, `docs/reviews/`, `docs/playtests/` | Build screenshots, Director reviews, play sessions; created on first use |
| `.claude/skills/` | Director skills (`game-director`, `art-direction`, `retro`) and coder skills (`build-check`, `context-maintenance`, `token-waste`) |
| `.claude/settings.json` | Claude Code project settings every game inherits: auto memory off, so the files above are the only continuity |
| `art/ART_BIBLE.md`, `art/references/` | Approved visual direction, look checklist, and the reference images you chose |
| `assets/ASSET_SOURCES.md` | Provenance and permissions for every asset |
| `docs/process/ASSUMPTIONS.md` | Why each process step exists; reviewed at retros |
| `docs/research/` | The research behind this template; source material, not copied into games |
| `kits/` | Engine and service material, copied in only when chosen |
| `tools/` | `new-game.ps1` (start a project), `sync-codex-skills.ps1` (mirror coder skills for Codex) |

## Improving the template

Claude owns the template's structure. Improvements come from project retros
(`docs/process/template-candidates.md` in a project). Promote a change here only
with evidence that it helped and with project-specific content removed. Existing
projects adopt template updates deliberately; nothing syncs automatically.

The research in `docs/research/` records the tool landscape and the evidence
behind the workflow. Its Appendix A goes stale fastest; refresh it before
choosing an engine or an asset service for a new project. The sibling
[Game_Dev_Library](https://github.com/darthreckoner/Game_Dev_Library) holds the
dated research archive.
