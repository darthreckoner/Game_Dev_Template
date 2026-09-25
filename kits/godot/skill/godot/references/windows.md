# Windows commands

Run from the project directory in PowerShell. Set the four paths once per session;
record the verified values in the project README. No global PATH or
execution-policy change is needed.

```powershell
$project = 'C:\Dev\<Project>'
$skill = Join-Path $project '.agents\skills\godot'
$godot = 'C:\Program Files\Godot 4\Godot_v4.7.2-stable_win64_console.exe'
$python = 'C:\Program Files\Python\Python314\python.exe'
& $godot --version
& $python --version
```

Use the `_console` executable for automation so output reaches the terminal.

## Dispatcher

The Python launcher accepts JSON inline or from a file. Use an absolute project path.

```powershell
& $python "$skill/scripts/dispatch.py" $project help --params '{"op":"inspect_scene"}' --godot-bin $godot
& $python "$skill/scripts/dispatch.py" $project inspect_scene --params '{"scene_path":"main.tscn","include_properties":false}' --godot-bin $godot
```

Inline `--params` JSON works in PowerShell 7. Windows PowerShell 5.1 strips the
inner quotes and the dispatcher fails with a JSON error (seen 2026-09-25 on 5.1.26100).
There, and for larger mutations, save the JSON in an ignored work file and pass
`--params-file <absolute-file>`. Operations may execute project initialization or
tool code; inspection is not a security sandbox.

## G0: import, parse, launch smoke

```powershell
& $godot --headless --path $project --editor --import --quit
& $python "$skill/scripts/debug/lint_project.py" $project --pretty
& $python "$skill/scripts/debug/run_project.py" $project 'res://main.tscn' --godot-bin $godot --quit-after 120 --timeout 60 --pretty
```

## G1: direct tests

```powershell
& $godot --headless --path $project --script res://tests/test_<system>.gd
```

Exit code 0 means pass. See the test pattern in [game architecture](game-architecture.md).
If the project adopts GUT or GdUnit4, `scripts/test/run_tests.py` detects and runs it.

## G2 and captures: scenarios

```powershell
& $python "$skill/scripts/debug/run_scenario.py" $project "$project\tests\scenarios\S1.json" --godot-bin $godot --pretty
```

A scenario with a `screenshot` step runs rendered; without one it runs headless.
Read both the scenario result and its runtime diagnostics. Screenshot paths must
be absolute or `res://`/`user://`; write evidence captures under
`docs/evidence/<milestone>/<run_id>/captures/`.

## Motion: Movie Maker frame sequences

```powershell
& $godot --path $project --write-movie "$project\work\movie\R2\frame.png" --fixed-fps 30 --resolution 1280x720 --quit-after 150 res://tests/scenarios/s2_scene.tscn
```

A `.png` path writes a numbered PNG sequence (plus WAV audio); `.avi` writes MJPEG
video. `--quit-after` counts frames. Copy a handful of representative frames into
the evidence captures folder for the Art Director; keep the full sequence in
ignored `work/` and record its hash. Movie Maker renders at fixed time steps, so
it suits deterministic scenes driven by scripted input, not live play.
