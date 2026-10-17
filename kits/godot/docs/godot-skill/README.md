# Godot skill provenance

This project-local skill adapts [haxqer/godot-skill](https://github.com/haxqer/godot-skill),
pinned to `1aec6d436f6a35044fe2f269637a339c2b8749b4`. The upstream MIT license is
retained in the skill folder. [upstream.json](upstream.json) records the upstream
archive SHA-256 and every upstream payload file hash. Against that record, the
files that differ from upstream are `SKILL.md`, `agents/openai.yaml`, and
`scripts/debug/run_project.py`; everything else is byte-identical (checked
2026-10-16).

## Lineage

1. **Rust Bucket installation (2026-09).** Local changes, verified there on Windows
   with Godot 4.7.2 and Python 3.14.7:
   - Replaced the 55 KB entrypoint with scoped instructions; the original is kept
     as `references/upstream-workflows.md`.
   - `scripts/debug/run_project.py` checks the process exit code before reporting
     success, uses Windows process-tree termination on timeout, and decodes output
     as UTF-8 with replacement.
   - Added `scripts/dispatch.py` to pass JSON through Python argument lists,
     including `--params-file`, avoiding PowerShell quoting differences.
   - Added Windows command guidance, cache ignore rules, `.gdignore`, and LF
     checkout rules. Set `agents/openai.yaml` to allow automatic invocation.
   Rust Bucket's `docs/godot-skill/README.md` holds that verification evidence.
2. **Game Dev Template kit (2026-09-25).** Documentation-only changes:
   - `SKILL.md` generalized: Rust Bucket deck specifics removed; evidence-run and
     architecture pointers added.
   - `references/windows.md` generalized to placeholder project paths; added
     G0/G1/G2 command groups and Movie Maker frame-sequence capture.
   - Added `references/game-architecture.md`.
   Kit check (2026-09-25, Windows PowerShell 5.1, Godot 4.7.2): the dispatcher
   `help` operation ran on a scratch project with `--params-file`; the inline
   `--params` form failed there because 5.1 strips JSON quotes.
3. **Game-director workflow (2026-09-28).** Documentation-only changes for the
   template's switch from milestone contracts and evidence runs to one-shot
   builds, tickets, and the build check:
   - `SKILL.md`: evidence-run pointers replaced with build-check pointers.
   - `references/windows.md`: command groups renamed (build, rules, scenarios);
     screenshots go to `docs/captures/<build>/`.
   - `references/game-architecture.md`: added tuning file, event-driven juice
     layer, and debug hotkeys; contract references now point to the build prompt.
   Scripts unchanged; no commands rerun.
4. **Claude-first template (2026-10-16).** Documentation-only changes:
   - Install path is now `.claude/skills/godot/`, because Claude Code discovers
     project skills there only (its docs, checked 2026-10-16). Codex gets a mirror
     through `tools/sync-codex-skills.ps1`. `references/windows.md` sets `$skill`
     accordingly; `SKILL.md` names `/build-check` and `$build-check`.
   - Kit check rerun on a scratch project (Godot 4.7.2, Python 3.14.7, run
     directly from Python): dispatcher `help` with `--params-file`, and a
     rendered scenario with a `ui_report` step and a `screenshot` step with
     `expect.not_blank`. Both passed and the PNG showed the scene's label. The
     scenario is kept as `kits/godot/examples/boot-scenario.json`. Movie Maker
     was not rerun. Scripts unchanged.

## Updating

1. Download a chosen upstream revision into an ignored work directory.
2. Compare its payload with `upstream.json` and inspect upstream changes.
3. Reapply only local changes still needed. Preserve the MIT license and record the
   new revision, archive hash, and file hashes.
4. Rerun the checks above: runtime regression tests for the patched scripts, the
   example scenario with its screenshot, and the skill validator.
5. Update this record in the template, then in projects that adopt the update.
