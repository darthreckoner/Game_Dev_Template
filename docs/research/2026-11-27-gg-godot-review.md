# gg-godot review (2026-11-27)

Reviewed at the designer's request: [Richy-was-here/gg-godot](https://github.com/Richy-was-here/gg-godot),
commit `c300a07` (2026-11-24), MIT license. A Claude Code plugin for Godot 4 with
seven agent roles, 19 commands, a `.gamedev/` document layout, ten verification
gates and an unattended mode. About 155 KB of text and scripts; read in full
except its CHANGELOG.

## Verdict

Not adopted as a plugin. It is a whole workflow that overlaps this template
(Designer → Director → Coder, `DESIGN.md`, tickets, game-conductor) instead of
adding to it, and its ban on Python in agent shell calls would break
`tools/game_workflow.py` and the Godot kit's helper scripts.

The designer chose to borrow four ideas (2026-11-27). Each is adapted, not copied:

| Idea in gg-godot | What the template now has | Why it fits here |
|---|---|---|
| `gg-guard` PreToolUse hook enforcing shell rules (`bin/gg-guard.js`) | `tools/shell_guard.py`, wired in `.claude/settings.json`; tests in `tools/test_shell_guard.py` | Ledger row 91: the heredoc pitfall recurred about nine times while documented. Narrowed to evidenced patterns: heredocs (git/gh allowed, for commit messages) and `python -` from stdin. gg's wider bans (all redirection, `tee`, `sed -i`, every interpreter) were left out for lack of evidence here. |
| `gg-qa` blind QA agent against a per-subsystem contract, with personas and a hunt list (`agents/gg-qa.md`) | `.claude/agents/blind-tester.md`; ticket field `Promises`; `build-check` step 5; guard rules for that agent | Makes "expected results come from the design, not the implementation" a step that runs. Promises replace gg's contract file: the Director writes them in the ticket. The guard limits the agent to `tests/blind/`; a GDScript test could still open files, so the agent's instructions forbid it. |
| `gg-check` gates 3 (stubs) and 9 (artifacts), plus leftover checks (`bin/gg-check`) | `kits/godot/skill/godot/scripts/test/hygiene_check.py` with tests; `build-check` step 6 | Cheap and mechanical. Not taken: gg's rule that any `print` fails, because the kit's scenarios log through `print` on purpose. Added: `class_name` counts as a reference, and `# hygiene: keep` marks a deliberate line. |
| `[AI]` marker on creative placeholder text (`rules/code.md`) | `AGENTS.md` "Choices"; the hygiene check lists `[AI]` lines | AI-made art and sound were already tracked in `assets/ASSET_SOURCES.md`; AI-written game text had no marker. |

## Not taken

- `.gamedev/` layout, roadmap, decision ids with scope (`M2-P3-D-01`): the
  template keeps `DESIGN.md` Changes, `STATE.md` and tickets.
- File check-out locks between agents: worktrees already isolate parallel work.
- `/gg:autonomous`: game-conductor and the designer's acceptance cover this.
- Document-format gate (field lists, line limits): `context-maintenance` and the
  8,000-character `STATE.md` limit cover the same risk with less machinery.

## Not yet tried in a game

All four changes are tested only by their own unit tests in this template. The
first game ticket that uses them is the real trial; log friction from it in the
project's friction log and in the ledger rows 114-117.
