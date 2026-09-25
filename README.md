# Game dev template

Repository: [Game_Dev_Template](https://github.com/darthreckoner/Game_Dev_Template).
Companion tool library: [Game_Dev_Library](https://github.com/darthreckoner/Game_Dev_Library).

A starting point for solo games built with two AI agents in separate roles: Codex
(Astra) as orchestrator and builder, and Claude as Art Director. The user owns
creative direction, spending, and milestone acceptance. Derived from the Hobby
Template; the working rules there still apply, extended for games.

## How work flows

1. **Pitch.** Tell the orchestrator the idea. `$game-pitch` shapes it into a pitch
   card, ranked risks, and variants; you choose, and it writes a prototype brief.
2. **Engine.** Choose an engine; the orchestrator installs its kit from `kits/`.
3. **Milestones.** For each milestone: `$milestone-contract` (you approve),
   build, freeze a candidate, `$evidence-run`, an art-direction review, at most two
   fix rounds, then you play it (`$playtest-kit`) and decide. `$retro` closes it.
4. **Art direction.** When the orchestrator files a request in
   `docs/art-direction/requests/`, open Claude Code in the project and ask it to
   process open art-direction requests. Claude answers in
   `docs/art-direction/reviews/`. See `docs/art-direction/README.md`.

## Start a project

Copy this folder's contents into an empty project folder, excluding `.git` and
`.coordination/`, or create a repository from it. The ignored `.coordination/`
folder is local maintenance correspondence, not game starter content. Then:

- Fill `PROJECT.md` with the orchestrator using `$game-pitch`.
- After choosing an engine, follow its kit README and replace the section below.
- Open the project folder in both Codex and Claude Code. Codex reads `AGENTS.md`
  and `.agents/skills/`; Claude Code reads `CLAUDE.md` (which imports `AGENTS.md`)
  and `.claude/skills/`.

## Run and check

This starter contains documentation only. When the engine is chosen, replace this
section with:

- the pinned engine version and exact executable paths
- how to launch the game and each test or scenario
- the automated checks (build, rules, scenarios) and the manual check of the main
  interaction
- how to build or export

A passing automated check does not establish game feel or visual quality; the
evidence record says what still needs the user to play.

## What belongs here

| Path | Purpose |
|---|---|
| `AGENTS.md` | Shared working rules, roles, milestone loop |
| `CLAUDE.md` | Claude's Art Director role (imports AGENTS.md) |
| `PROJECT.md` | Pitch, current milestone, decisions, budget, open choices |
| `.agents/skills/` | Orchestrator skills: pitch, contract, evidence run, playtest, retro, context maintenance |
| `.claude/skills/art-direction/` | Art Director skill, rubric, asset specs |
| `art/ART_BIBLE.md` | Approved visual direction and readability rules |
| `assets/ASSET_SOURCES.md` | Provenance and permissions for every asset |
| `docs/milestones/`, `docs/evidence/`, `docs/art-direction/` | Contracts, evidence records, handoffs |
| `docs/process/ASSUMPTIONS.md` | Why each process step exists; reviewed at retros |
| `kits/` | Engine and service material, copied in only when chosen |

Create `.agent/CONTINUITY.md` when work spans sessions; keep current status and the
next step there.

## Improving the template

Improvements come from project retros (`docs/process/template-candidates.md` in a
project). Promote a change here only with evidence that it helped and with
project-specific content removed. Existing projects adopt template updates
deliberately; nothing syncs automatically.

## Shared template and library coordination

This source workspace hosts the Astra–Claude channel at `.coordination/`.
For template/library maintenance, read its README and STATE and reply in a
new message file. The sibling library at `C:/Dev/Game_Dev_Library` points
to the same channel. Astra coordinates structural changes; Claude is Art
Director, with Opus 5.5 selected by the user. File delivery does not wake an
idle agent. Existing game art handoffs remain under `docs/art-direction/`.

The shared channel and library routing are established; an indexed external
tool catalog and kit extraction are still future work. Keep the current
`kits/` paths intact until a coordinated change is assigned and verified.

## Source research

For work on this source template, use the sibling library's
[research index](../Game_Dev_Library/docs/research/2026-09-25-ai-solo-game-dev-environment/README.md). This source
maintenance pointer is not a game requirement.
