# Tooling maintenance handoff — 2026-10-19

Authorized scope: shared game runbook/conductor integration with the existing
Designing Games pilot. This is template maintenance; `DESIGN.md` and `STATE.md`
remain game starters, not another acceptance store. No game was modified.

- Started on template `main` with clean status. Library `main` already had
  untracked `books/`, `docs/AI assisted game dev guide v3.md` and
  `docs/designing_games_pilot/`; preserve them and do not stage them with this work.
- Actual pilot is an uninstalled reference package; global instructions already
  route to it. Original helper baseline passes (415 pages, 10 principles,
  54 references, 10 self-test cases). Original source/catalog/examples are intact.
- Exact revised Page retrieved: page_668a068e0e848191a33b8c5c531abae4,
  sequence 1, 217 blocks. Saved in library `docs/game_workflow/source/`;
  every original block hash matches. The older local guide stays untouched.
- Implemented `tools/game_workflow.py`, disposable commissioning tests,
  `game-conductor` skill, source-linked shared definitions and contracts,
  source-linked tooling decision, targeted Claude hooks and starter exclusions.
  One SQLite event ledger owns execution/acceptance per opted-in project.
- Latest run: 29 tests pass, including actual Git Bash hook commands from another
  working directory and the shared verification/editor queue. Human actions are simulated only in disposable
  fixtures; no real project plan/playtest was approved. Live Unreal unavailable;
  simulator proves queued reads and timeout-before-retry reconciliation only.
- Skill mirror succeeded for existing coder skills and the conductor. Supplied
  skill validator needed PyYAML; installed only in ignored `work/validation-deps`.
  Skill frontmatter validation passes. Runner has no third-party dependencies.
- Installed Codex app-server `skills/list` discovers the enabled repo skill;
  installed Claude help confirms `/skill-name`. No model call was made to probe
  dispatch. Full hook suite needs normal Windows process access because the
  restricted sandbox denies Git Bash's shared object startup.
- Friction resolved: sandbox system temp incompatible with Git fixtures (moved
  into ignored work); SQLite context manager did not close handles (explicitly
  closed); Windows byte lock initialized without reading a held byte; missing
  consultation now records failed verification. Python reads use explicit UTF-8.

- Independent audit of initial e06b893/e5a0c478 reproduced all 28 original tests
  and found one P1 prerequisite acceptance gap. Fixed by binding dependent runs
  to exact prerequisite acceptance IDs and revalidating the transitive chain.
  Added same-candidate failure, restoration and downstream re-verification coverage;
  all 29 tests pass locally. Initial report is in `docs/reviews/`.

Next: commit the fix and updated shared contract, obtain independent follow-up on
those exact commits, then record final delivery state and remaining gaps.
No push, release, publication or global configuration change is authorized.
