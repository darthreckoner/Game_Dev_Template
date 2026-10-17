# Template audit — 2026-10-16

Requested by the designer: audit the whole folder and make it the best AI
game-dev template it can be. The same day the designer retired Astra (the Codex
orchestrator and coder) and gave Claude ownership of the template and every
seat by default, with ChatGPT kept as an occasional second seat for image
generation, outside code review, and easy tickets.

This record is the before-and-after. The workflow itself is in `AGENTS.md`.

## Summary

The template's core idea was sound: the vision lives in files, one-shot builds,
fresh sessions per ticket, light checks with screenshots. What was wrong was
around it: two agents owned the structure through a side channel, the coder
skills sat where Claude Code cannot see them, two research documents at the root
described a different process in a different vocabulary, and the workflow had
no seats, tiers, stop rules, or friction capture. All of that is fixed below.
The Godot kit was reverified end to end on this machine today.

## Findings

Severity: blocker (would break a session), major (would cost a round or a
rebuild), minor (clutter or drift).

1. **Blocker · Coder skills invisible to Claude Code.** `build-check`,
   `context-maintenance`, and `token-waste` lived in `.agents/skills/`. Claude
   Code loads project skills from `.claude/skills/` only (its docs, checked
   today). With Claude as the default coder, `/build-check` did not exist.
2. **Blocker · No role switch for a Claude coder session.** `CLAUDE.md` made
   every Claude Code session the Director and forbade editing code. A coder
   session would have refused its own job.
3. **Major · Split ownership through a dead channel.** `.coordination/`, the
   README, `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, and the sibling library all
   routed structural changes through Astra. Three of Astra's assignments had
   been open since 2026-09-25 with no reply.
4. **Major · Two process vocabularies at the root.** `AI-Solo-Game-Dev-Kit.md`
   and `AI-Game-Dev-Model-Guide.md` (untracked, 68 KB) named files and gates the
   template does not have: `PROJECT.md`, `docs/BRIEF.md`, `DECISIONS.md`,
   `tickets/<milestone>/`, G0–G6, evidence records, milestone contracts. Any
   agent reading the root would have tried to follow both.
5. **Major · No seats, tiers, or escalation.** Nothing said which model takes
   which work, so every ticket would have gone to whatever model was open, and
   a stuck ticket had no next step.
6. **Major · No stop rule.** Review-and-fix loops had no round cap; the research
   the designer commissioned documents such a loop burning about 20M tokens
   without converging.
7. **Major · Presentation review scored 0–4.** The same research shows a single
   visual score hiding broken interaction and inviting optimization of the
   number. The art bible had no palette values and no reference images, so the
   coder would have chosen colors.
8. **Minor · No friction capture.** The `retro` skill asked for friction
   evidence that nothing recorded.
9. **Minor · Stale pointers.** `token-waste` and `context-maintenance` referred
   to `.agent/CONTINUITY.md` and `.agent/context-history/`, which this template
   never had. The README pointed at research in the Railroad Wars repo. The
   engine matrix lacked Roblox, which the designer uses.
10. **Minor · Leftovers.** Empty `.agent/`, `docs/art-direction/requests/`,
    `docs/art-direction/reviews/` from the pre-2026-09-28 template; an ignored,
    superseded Astra letter in `docs/process/`.
11. **Minor · Kit verification stale.** The Godot kit's scenario, UI report, and
    screenshot path had never been rerun as a kit; only `help` had.
12. **Minor · No scripted project start.** Starting a game meant copying by hand
    and remembering what to leave out.

## Changes

| Area | Before | After |
|---|---|---|
| Ownership | Astra coordinates structure via `.coordination/`; Claude is Art Director | Claude owns the template, all seats by default; channel archived to ignored `work/archive/astra-coordination/` |
| Roles in `CLAUDE.md` | Always Director | Director by default; Coder when the first message is a `CODER_PROMPTS.md` prompt; may run kit checks for evidence |
| Skills | Director in `.claude/skills/`, coder in `.agents/skills/` | All in `.claude/skills/`; `tools/sync-codex-skills.ps1` mirrors coder skills for Codex |
| Seats | Unrecorded except "Opus 5.5, Codex (Astra)" | Seats table in `AGENTS.md` (Fable Director, Opus/Sonnet/Haiku coder tiers, ChatGPT optional); defaults in `DESIGN.md` |
| Tickets | No tier, no file scope | Tier, read-first list, files it may touch, exact values; escalation ladder |
| Stop rules | None | Two rounds then the designer decides; rebuild after two failed rounds; budget line in `DESIGN.md` Scope |
| Friction | None | Friction log in `STATE.md`, read by `retro`, pruned at retros |
| Art bible | Readability rules only | Placeholder palette with hex slots, references in `art/references/`, Direction with engine-setting values, 8–15 item look checklist |
| Presentation review | Anchored 0–4 score | Checklist pass/fail/not visible plus observations and severity; review document format |
| Coder prompts | Generic | Each opens "You are the Coder", names its seat; added Chores, Second-opinion review, read-only critique prompts |
| Build prompt | Good | Adds role line, seat, automation path (scenario load, state dump JSON), "choose nothing visual", report format |
| Research | Two docs at the root in their own vocabulary | `docs/research/` with a README and a vocabulary map; excluded from new games |
| Kits | Install to `.agents/skills/godot/`; help verified 2026-09-25 | Install to `.claude/skills/godot/`; help and rendered scenario verified today; example scenario shipped; provenance lineage entry 4 |
| Tools | None | `tools/new-game.ps1` (copy, name, first commit), `tools/sync-codex-skills.ps1` |
| Clutter | Empty old folders, dead ignores | Removed; `.gitignore` trimmed |
| Assumptions register | 9 rows | 15 rows, each naming the limitation it covers and when to revisit |

## Verified today

- Claude Code skill discovery: project skills load from `.claude/skills/` only
  (official docs, fetched 2026-10-16). After the move, Claude Code listed all
  six skills in this session.
- Godot kit on this machine (Godot 4.7.2 at `C:\Program Files\Godot 4\`,
  Python 3.14.7): dispatcher `help` with `--params-file`, then a rendered
  scenario with a `ui_report` step and a `screenshot` step with
  `expect.not_blank` on a scratch project. Result `ok: true`, the UI report
  listed the label, and the PNG showed it. Movie Maker was not rerun.
- Godot kit provenance: against `upstream.json`, only `SKILL.md`,
  `agents/openai.yaml`, and `scripts/debug/run_project.py` differ from
  upstream, as the lineage says.
- `tools/new-game.ps1` into a scratch folder: copied the starter without
  `.git`, `work/`, `docs/research/`, and itself; wrote the name into both
  files; made the first commit; nothing uncommitted.
- `tools/sync-codex-skills.ps1` in that copy: mirrored `build-check`,
  `context-maintenance`, `token-waste` into `.agents/skills/`.
- Every relative Markdown link and every root-level path named in backticks
  resolves, except one link inside the designer's research document to a
  "Fable Cities" review that is not in this repository or the library.
- No remaining references to Astra, the coordination channel, or the old gate
  vocabulary outside `docs/research/` and the kit's own lineage history.

## Decisions made under the designer's direction (confirm or change)

- **Seats.** Director: Claude Code, Fable 5.1 or the strongest model available
  (the 2026-09-25 choice was Opus 5.5). Coder: fresh Claude Code sessions, Opus
  5.5 for one-shot builds, rebuilds, and complex tickets; Sonnet 5.5 for
  standard tickets; Haiku 5.5 for chores. ChatGPT or Codex optional for outside
  review, routine tickets, image generation.
- **Skill layout.** One source of truth in `.claude/skills/`; Codex gets a
  generated mirror. The template ships without `.agents/`.
- **Scores to checklist.** Presentation review is now a per-item checklist with
  observations. The 0–4 scale is gone.
- **Research kept in the template source** under `docs/research/`, not copied
  into games. The library keeps the dated archive.
- **Astra's channel archived, not deleted**, in ignored `work/archive/`. Delete
  it when you no longer want the history.

## Not done, and open

- `C:\Dev\Game_Dev_Library` (a separate repository) still names Astra and the
  retired channel in its README, `AGENTS.md`, and `CLAUDE.md`. Outside this
  repository, so untouched.
- `C:\Dev\Railroad Wars` still runs the pre-2026-09-28 template with Claude as
  Art Director only. Migrating it is the designer's call.
- Genre playbooks are still empty by design; they grow from retros.
- The tool landscape in `docs/research/` dates from 2026-09-25. Refresh before
  choosing an engine or asset service for a new project.
- Nothing is pushed. Changes are committed locally on `main`.
