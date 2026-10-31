# Lessons ledger

Every lesson learned on every game made from this template is recorded here. The designer decided this on 2026-10-31. The ledger exists so the template can be audited against past mistakes.

## Rules

- **One row per lesson.** Each row says what went wrong (or right), the evidence, and the project and file the evidence lives in. Strip project-specific detail from the lesson itself, but keep the pointer.
- **Engine kits too.** Engine-specific pitfalls go into that kit's pitfalls reference (for example `kits/godot/skill/godot/references/pitfalls.md`), with a ledger row pointing at it.
- **Every project feeds the ledger.** After each designer gate or retro, the Director adds that project's lessons here, all of them, not only the ones a retro chooses to act on.
- **The Template change column has three states:**
  - **Applied**, with the file and commit;
  - **Proposed**, with the target file;
  - **Rejected**, with the designer's reason.
- **Auditing the template means:**
  - read every row whose change is not Applied;
  - check the template still guards against every Applied row (the rule is still there and still followed);
  - record the audit date and its result in "Audit log" below.
- **Promote only tested changes.** Changes to skills, prompts or templates follow the retro process: test in a project first, then the designer approves promotion. A recorded lesson with its change still Proposed is fine; an unrecorded lesson is not.

## Lessons

| # | Lesson | Evidence (project, file) | Template change |
|---|---|---|---|
| 1 | Checks must reach state through the player's input. Defects found only by hand slipped past checks that set state directly. | Backcountry Expedition, `docs/process/retro-2026-10-26-p0-gate.md` | Proposed: `docs/tickets/TEMPLATE.md` Check; `build-check` step 4 |
| 2 | Right-size playtests. A designer playing a prototype solo needs only a launch command, a log path and questions afterwards. | Same retro | Proposed: `game-director/references/playtest.md` |
| 3 | `STATE.md` grows past its limit whenever coders log evidence in it and several coders merge into it. Prose rules didn't hold in two runs. | Backcountry Expedition: same retro, plus `docs/process/2026-10-31-comparison-slice-lessons.md` L11 and L12 | Proposed: make STATE an index (one line per open ticket with a pointer; evidence in ticket reports; only the Director edits it at merge; plain prose). Targets: `STATE.md`, `CODER_PROMPTS.md`, `context-maintenance` |
| 4 | Don't run full test suites in parallel behind one GPU or engine lock. They queue for hours and time out. Coders run focused checks; one integration run follows the merges. | Backcountry Expedition, comparison-slice lessons L1 | Proposed: `build-check`, `CODER_PROMPTS.md`, orchestration guidance |
| 5 | Serialize engine launches with one named lock, and take timings only when no other engine process is running. | Same file, "What worked" | Proposed: engine kit README and `build-check` |
| 6 | Size parallel agent waves to the usage that remains. Use the strongest model only where judgment is the job. | Same file, L2 (three usage-limit stops) | Proposed: `AGENTS.md` Seats and orchestration guidance |
| 7 | Coders hand back while their own background work is still running, even when the brief forbids it. | Same file, L3 (at least eight times) | Proposed: a mechanical guard in `CODER_PROMPTS.md`, `build-check` or the tooling |
| 8 | A friction note in prose doesn't stop a repeated tooling trap. Example: `python -` with redirected stdin hangs. | Same file, L4 (three recurrences) | Proposed: a wrapper or lint in `tools/` |
| 9 | Check a ticket's thresholds against that ticket's own exclusions before release. | Same file, L5 (an 85% coverage target that counted land the same ticket ruled out) | Proposed: the ticket step in the `game-director` skill and `docs/tickets/TEMPLATE.md` |
| 10 | Write visibility and readability requirements as sampled, measurable checks with named viewpoints. | Same file, L6 | Proposed: `docs/tickets/TEMPLATE.md` |
| 11 | When a visual model changes, re-check every camera that depends on it in the same ticket. | Same file, L7 (a cockpit view took three rounds) | Proposed: `docs/tickets/TEMPLATE.md` Check prompts |
| 12 | Tickets that pass their own focused checks can still fail together. Run an integration suite after each pair of parallel merges. | Same file, L8 (five combined failures) | Proposed: orchestration guidance |
| 13 | For any comparison or parity goal, ask up front for the quality bar, the reference build and one reference screenshot per aspect. | Same file, L9 and L10 (a late bar added twelve tickets) | Proposed: `game-director` design interview, `art-direction` |
| 14 | Keep ticket status to one line. Put history in reviews, not in the status line. | Same file, L12 | Proposed: `docs/tickets/TEMPLATE.md` |
| 15 | What worked: domain agents with dossiers; advisory research before tickets; measure-then-decide gates; Director capture review before every merge. | Same file, "What worked" | Proposed: an agents folder and the `game-director` skill |
| 16 | Godot engine and tooling pitfalls (about 30: import cache, headless timing, pause counters, physics monitor semantics, GPU contention, Jolt body limit, height-field squares, visibility range, SDFGI, shader derivatives, system fonts, SDL3 pad limits) | Backcountry Expedition, per-row evidence in the reference | Applied: `kits/godot/skill/godot/references/pitfalls.md`, linked from the kit's `SKILL.md` work loop |
| 17 | A rule that exists only as prose gets skipped: the 2026-10-26 template candidates were never promoted. Put rules into the skills' required steps, and back them with a test. | Backcountry Expedition, `docs/process/template-candidates.md` | Applied: required ledger step in the `retro` skill and in the `game-director` Retro section; `LessonsLedger` tests in `tools/test_game_workflow.py` |

## Audit log

| Date | Auditor | Result |
|---|---|---|
| 2026-10-31 | Director | Ledger created. Rows 1–16 recorded; row 16 (Godot pitfalls) Applied in the kit, rows 1–15 Proposed. The next audit follows the Backcountry Expedition retro. |
| 2026-10-31 | Director | Hardened: the retro and game-director skills require the ledger, and `LessonsLedger` tests (4) pass. Rows 16–17 Applied; 1–15 Proposed. |
