# Godot kit

Install after the user chooses Godot for a project.

## Install

1. Copy `skill/godot/` to the project's `.claude/skills/godot/`. Claude Code
   finds it there. If Codex will take tickets, run `tools/sync-codex-skills.ps1`
   afterwards to mirror it into `.agents/skills/godot/`.
2. Copy `docs/godot-skill/` to the project's `docs/godot-skill/`.
3. Add to the project's `.gitignore`:

   ```gitignore
   # Godot
   .godot/
   *.translation
   export_presets.cfg
   /builds/
   ```

   Keep `export_presets.cfg` ignored only if it may contain credentials; otherwise
   track it once export settings are chosen.
4. In the project README, record the pinned Godot version, the exact executable
   paths, and the setup, launch, test, and scenario commands after running them once.
5. In `DESIGN.md` Project settings, set "Engine kit installed: godot (Godot
   4.7.2; kit from Game_Dev_Template <commit>)".

## Verify the install

```powershell
$project = 'C:\Dev\<Project>'
$skill = Join-Path $project '.claude\skills\godot'
$python = 'C:\Program Files\Python\Python314\python.exe'
$godot = 'C:\Program Files\Godot 4\Godot_v4.7.2-stable_win64_console.exe'
New-Item -ItemType Directory -Force "$project\work" | Out-Null

# 1. Dispatcher help (a JSON help listing confirms the helpers run)
$params = "$project\work\help-params.json"
Set-Content -Path $params -Encoding ascii -Value '{"op":"inspect_scene"}'
& $python "$skill\scripts\dispatch.py" $project help --params-file $params --godot-bin $godot

# 2. Rendered scenario with a UI report and a screenshot
# Copy examples/boot-scenario.json to $project\tests\scenarios\boot.json, set
# scene_path to a scene with at least one Control, and set the screenshot path.
& $python "$skill\scripts\debug\run_scenario.py" $project "$project\tests\scenarios\boot.json" --godot-bin $godot --pretty
```

The scenario result must say `"ok": true`, the `ui_report` must list the
control, and the PNG must not be blank. Look at the image. Verified on
2026-10-16 on a scratch project (Godot 4.7.2, Python 3.14.7): both steps passed
and the capture showed the scene's label. Under Windows PowerShell 5.1, pass
JSON through `--params-file`; inline `--params` loses its quotes there.

## Contents

- `skill/godot/`: the skill. Adapted from haxqer/godot-skill via Rust Bucket's
  verified installation; see `docs/godot-skill/README.md` for provenance.
- `skill/godot/references/game-architecture.md`: template defaults for
  simulation/presentation split, scenarios, direct tests, and captures.
- `examples/boot-scenario.json`: the smoke scenario from the verification above.
