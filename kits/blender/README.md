# Blender kit

Install when a project makes, fixes, or exports 3D models through Blender. It is
a tool kit, not an engine kit: it sits beside the engine kit and feeds it.

Five skills, local Blender only. Nothing here uses a cloud service or spends
money.

| Skill | Use |
|---|---|
| `blender-core` | Start here. Runs scripts in headless Blender, Blender 5 API rules, routes to the others |
| `blender-scene-setup` | Units, naming, collections, file tidiness audit |
| `blender-asset-qa` | Pass/fail model check and multi-angle review pictures |
| `blender-game-optimization` | Triangle, material and texture counts against a budget; lower-detail versions |
| `blender-export-pipelines` | Export presets for Godot, Unity, Unreal, Roblox, web, with a re-read of the result |

Twenty-three more skills exist upstream and are not installed.
`skills/blender-core/references/more-skills.md` says what each does, when a
design calls for it, and how to add it. The Director checks that list when the
design or art bible first calls for 3D work beyond checking and exporting.

## Install

1. Copy each folder in `skills/` to the project's `.claude/skills/`. If Codex
   will take tickets, run `tools/sync-codex-skills.ps1` afterwards.
2. Copy `docs/blender-skills/` to the project's `docs/blender-skills/`.
3. In the project README, record the Blender version, the executable path, and
   the commands below after running them once.
4. In `DESIGN.md` Project settings, add "Blender kit installed (Blender 5.2 LTS;
   kit from Game_Dev_Template <commit>)".

Needs Blender 5.2 LTS or newer and Python 3.9 or newer on the host.

## Verify the install

```powershell
$project = 'C:\Dev\<Project>'
$skills = Join-Path $project '.claude\skills'
$python = 'C:\Program Files\Python\Python314\python.exe'
$run = "$skills\blender-core\scripts\run_in_blender.py"
New-Item -ItemType Directory -Force "$project\work" | Out-Null

# 1. Finds Blender and reports the environment
& $python $run --which
& $python $run "$skills\blender-core\scripts\env_report.py"

# 2. Model check, budget, audit on Blender's default cube
& $python $run "$skills\blender-asset-qa\scripts\qa_check.py" -- --objects Cube --profile game
& $python $run "$skills\blender-game-optimization\scripts\mesh_stats.py" -- --objects Cube --budget pc
& $python $run "$skills\blender-scene-setup\scripts\scene_audit.py"

# 3. Export and review pictures
& $python $run "$skills\blender-export-pipelines\scripts\export_asset.py" -- --preset godot --objects Cube --out "$project\work\cube.glb"
& $python $run "$skills\blender-asset-qa\scripts\review_shots.py" -- --objects Cube --mode random --out "$project\work\cube.png"
```

Expected: the check says `"pass":true` with one warning that the cube is not
resting on the ground; the export says `"ok":true` with 12 triangles;
`work\cube.png` shows a cube from four angles. Look at the picture. Verified
2026-11-21 on a scratch project (Windows 11, PowerShell 5.1, Blender 5.2.2 LTS,
Python 3.14.7): every step above passed. `--cloud` was refused with exit code 2,
and a `pch` command on the PATH did not change where the scripts ran.

Set `$env:BLENDER_EXE` to a `blender.exe` to pin one of several installs. In Git
Bash, pass Windows-style paths (`C:/...`) and set `MSYS_NO_PATHCONV=1`.

## Use it well

Lessons from the trial on a shipped vehicle (recorded in the skills too):

- Pass `--objects` to the check every time, one asset at a time, parts in their
  real positions, from the source `.blend` where there is one.
- The check counts overlapping faces but does not locate them. Budget a
  follow-up look for each finding.
- The project's own budgets, origin, and naming rules override the skills'
  defaults. `blender-scene-setup` suggests `SM_`/`T_`/`M_` names; a project that
  already has a convention keeps it.
- The glTF presets export no tangents. Add `--set export_tangents=True` when the
  project's files carry them.
- These skills check and export. They choose no colors, materials, or looks;
  those come from `art/ART_BIBLE.md`.

## Contents

- `skills/`: the five skills, adapted from patch-gg/cloud-blender-skills (MIT).
  See `docs/blender-skills/README.md` for provenance and what was changed.
- `docs/blender-skills/upstream.json`: the pinned commit and the upstream hash
  of every file.
