# Godot kit

Install after the user chooses Godot for a project.

## Install

1. Copy `skill/godot/` to the project's `.agents/skills/godot/`.
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
5. Add `- Godot work: use .agents/skills/godot/SKILL.md.` to the project's
   AGENTS.md skills list.

## Verify the install

```powershell
$project = 'C:\Dev\<Project>'
$python = 'C:\Program Files\Python\Python314\python.exe'
$godot = 'C:\Program Files\Godot 4\Godot_v4.7.2-stable_win64_console.exe'
$params = "$project\work\help-params.json"
New-Item -ItemType Directory -Force "$project\work" | Out-Null
Set-Content -Path $params -Encoding ascii -Value '{"op":"inspect_scene"}'
& $python "$project\.agents\skills\godot\scripts\dispatch.py" $project help --params-file $params --godot-bin $godot
```

A JSON help listing confirms the helpers run. This was verified on 2026-09-25 on a
scratch project under Windows PowerShell 5.1; the params file avoids 5.1's quoting
problem. Before the first `$build-check`, also run one scenario with a screenshot
step and look at the image.

## Contents

- `skill/godot/`: the skill. Adapted from haxqer/godot-skill via Rust Bucket's
  verified installation; see `docs/godot-skill/README.md` for provenance.
- `skill/godot/references/game-architecture.md`: template defaults for
  simulation/presentation split, scenarios, direct tests, and captures.
