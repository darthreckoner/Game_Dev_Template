# Godot pitfalls learned in projects

These are engine and tooling behaviours that each cost a project real time. Every row was verified in a project, and the evidence column says where. Read this before automating tests, measuring performance or building large worlds. New rows come from every project, through the template's `docs/process/LESSONS_LEDGER.md`.

Versions: Godot 4.7.2, Forward+, Jolt, Windows, unless a row says otherwise.

## Project setup and source control

| Pitfall | Do this | Evidence |
|---|---|---|
| A fresh checkout or worktree has no `.godot/` import cache, so headless tests time out silently. | Run `godot --headless --editor --import --quit` once in every new checkout or worktree before any test. | Backcountry Expedition (BE) STATE friction log; recurred across every parallel worktree |
| Opening the editor or importing rewrites line endings in many `.import` files and `default_bus_layout.tres`, which creates noise diffs. | Leave that churn unstaged and commit only intended files. Consider `.gitattributes` for these paths. | BE, T-043–T-052 reports |
| Committed data files (JSON, raw) get CRLF on a Windows checkout, which breaks byte-identity tests. | Mark generated data `-text` or `eol=lf` in `.gitattributes`. | BE T-033 and T-034 |
| Python's `write_text()` on Windows defaults to cp1252, so non-ASCII text becomes invalid UTF-8 in GDScript. | Always pass `encoding="utf-8"`. | BE T-033 friction |
| Git Bash heredocs break GDScript, and `python -` with redirected stdin opens a REPL that hangs. | Write scripts to an ignored `work/` folder and run them as files. | BE friction log, which recorded three recurrences |
| Two Godot instances on one project folder corrupt `.godot/` and scenes. | Give each coder its own worktree, and never run two editors on one folder. | BE agent lineup |
| Git ignores a scratch folder, but Godot still discovers its GDScript and registers duplicate global classes. | Put `.gdignore` in the scratch folder before copying `.gd` files there; rebuild the import/class cache after a duplicate-class startup. A Git ignore is not an engine ignore. | BE, `docs/captures/T-044/diagnostics/FRICTION.md`, invalid C startup |
| A Windows PowerShell `Tee-Object` log was UTF-16 while its collector assumed UTF-8, stopping evidence collection. | Detect the BOM when reading existing logs, or explicitly control the writer's encoding. Check the decoded result before using it to drive a dependent step. | BE, same T-044 friction log; `C:/Dev/Backcountry Expedition Playtest/docs/playtests/2026-11-02-controls-audio.md`, finalization friction |
| A pinned Godot executable exists but `godot` is absent from the shell's PATH; discovering this after a long queue wastes the slot. | Resolve and check the configured executable before requesting an engine slot. | BE, `docs/captures/T-086/REPORT.md`, Friction: the bare command waited 38 minutes before exit 127; the coder prompt now names the installed executable. |
| A literal newline inside a GDScript string changed when Git checked it out as CRLF, corrupting generated shader directives. An LF worktree passed. | Use explicit newline escapes in generated source. Exercise both LF and CRLF input and compile the generated shader in the receiving checkout. | BE, `docs/captures/T-081/REPORT.md`: 42 checks and a deliberately malformed directive rejected by the shader compiler. |
| Type inference from a dynamically typed world or untyped Array element can prevent a GDScript from loading; a scenario may report only a missing node. | Declare the concrete type at the dynamic boundary and read the engine parse log before diagnosing downstream scenario state. | BE, `docs/captures/T-078/REPORT.md`, Friction; `T-101/REPORT.md`, Friction; `T-126/REPORT.md`, live collision probe. |

## Headless testing and scenarios

| Pitfall | Do this | Evidence |
|---|---|---|
| Headless frames outrun physics, so a hold measured in frames is far too short. | Time holds with `wait_seconds` or physics steps. | BE T-028 |
| `Engine.get_physics_frames()` keeps counting while the tree is paused. | Assert pause with your own counter that only advances in an unpaused `_physics_process`. | BE T-036 |
| `RenderingServer.frame_post_draw` doesn't fire headless. | Count frames differently in headless runs, and label which counter you used. | BE T-039 |
| A one-frame `wait` finishes at once, so an `until` straight after a teleport reads the previous frame's metrics. | Wait two frames after any instant state change before asserting. | BE T-028 and T-033 |
| A test can pass every check and still exit with "RID allocations leaked" or "resources still in use". Runners that check stderr then mark it failed. | Free what the test creates before `quit()`. | BE integration run, T-052 |
| A test whose scenario finished but whose process never exits hangs the runner. | Give every test a timeout, and make the runner record a timeout as a failure and continue. | BE integration run, T-052 |
| Godot 4.7.2 maps `ui_accept` and `ui_cancel` to no gamepad buttons by default. | Bind pad buttons to the UI actions yourself. | BE T-036 |
| An editor import can crash with no logged errors, or exit zero while logging errors. | Check exit status and decoded diagnostics independently. A crashed import invalidates dependent checks; retain the failed invocation when recording a clean retry. | BE, `docs/captures/T-071/REPORT.md` (exit `0xC0000005`); `T-126/REPORT.md` (zero-exit `f.is_null()` errors). |
| A wall-clock settle and a gap between input programs allow different numbers of physics steps, changing a creeping vehicle's start under load. | Stage with physics steps, hold the vehicle through program boundaries, and assert pose, speed and contacts at launch. Preserve real-time waits where paused UI or audio actually requires them. | BE, `docs/captures/T-115/REPORT.md` and `T-116/REPORT.md`; setup exceptions for S52 and S131 remain explicit. |
| A repeat-run script deleted every `ra-*` sandbox, including another active run's files, producing 49 invalid failures. | Clean only the exact sandbox owned by that run. Concurrent runs in one checkout still need separate artifact paths. | BE, `docs/captures/T-121/REPORT.md`, invalid merge-tier attempt; its loop now uses its own sandbox path. |
| Editing generated scenario JSON alone loses assertions on the next regeneration. | Update its generator and regenerate; inspect the resulting diff for preserved assertions. If no generator exists, identify that limitation instead of claiming reproducibility. | BE, `docs/captures/T-116/REPORT.md`, Findings: S121 had assertions absent from `make_t091.py`; S8 and S74 had no generators. |

## Performance measurement

| Pitfall | Do this | Evidence |
|---|---|---|
| `Performance.TIME_PHYSICS_PROCESS` is the largest step in the last second, refreshed once a second. It is not a per-step time, so reading it every step shows false 13–24 ms "spikes". | Time steps yourself with `Time.get_ticks_usec()`. | BE T-034 and T-039 |
| GPU timings taken while another Godot instance runs are invalid. | Hold one named OS mutex for every engine launch, and time only when no other Godot process exists. Log that check. | BE comparison slice |
| In a window, `--disable-vsync` may still lock to the display rate. | Use GPU ms (`viewport_get_measured_render_time_gpu`) as the budget metric, not fps. | BE T-039 |
| `--max-fps 60` shows a frame-time p99 of about 19 ms of limiter jitter even when the GPU is idle. | Don't judge a 60 fps budget from a capped run on a higher-refresh display. | BE T-039 |
| Light GPU shots, around 1 ms, can swing 30%+ between runs. | Compare heavy shots for repeatability, and report run-to-run spread. | BE T-039 |
| Autosaving on the main thread caused a 7–8 ms hitch. | Write saves on a worker thread. | BE T-039 |
| A successful process exit can measure a paused game or a decorated window smaller than the required viewport. | For each qualifying interval, verify actual window/viewport/texture dimensions and render scale; reject pauses and require the intended physics progress and travel. Keep invalid invocations as diagnostics. | BE, `docs/captures/T-044/diagnostics/FRICTION.md`, 1920x1061 preflights and paused C2 invocation |
| Serializing every headless check behind the rendering lock creates a queue even when isolated checks can share the machine. | Permit bounded headless concurrency only after per-step user data, artifacts, timeout/child cleanup and serial/parallel verdict equivalence are verified. Keep rendering, GPU timing and native-audio qualification exclusive; synchronize wrapper versions across worktrees. | BE, `docs/captures/T-107/REPORT.md` and `T-110/REPORT.md`: sandboxed engine slots and equivalent verdicts; old-wrapper transition and import churn remain documented limitations. |

## Rendering

| Pitfall | Do this | Evidence |
|---|---|---|
| Hand-built terrain meshes with the wrong winding render lit upside down, and skirts show through LOD gaps as pale dots. | Check winding with a lit test render, and shade skirts like the surface above them. | BE T-033 |
| `visibility_range` is measured to the centre of the node's AABB, so a cell-sized node can't honour a short range tier. | Use script-managed per-variant buffers for short near tiers. | BE T-034 |
| SDFGI with a flat-colour ambient and no sky adds strong bounce light that washes near ground toward white. | Re-measure the calibrated look before enabling SDFGI, and keep it behind a key. | BE T-039 |
| `dFdx`/`dFdy` inside per-pixel branches spike where a 2×2 quad straddles two branches, giving dark seams at material boundaries. | Skip derivative-based terms in quads where the branch flags differ, or compute them outside the branches. | BE T-051 |
| Alpha to Coverage does nothing without MSAA. | Expect hard cut-out edges unless MSAA 3D is on. | BE T-034 research |
| A headless material test cannot read the rendered texture through `ImageTexture.get_image()` in the tested path; a metadata value checks configuration only. | Use headless rules for configuration and a rendered capture/readback for the visible material claim. | BE, `docs/captures/T-079/REPORT.md`, Friction: empty headless image; rust-strength assertion uses metadata. |

## Physics (Jolt)

| Pitfall | Do this | Evidence |
|---|---|---|
| `HeightMapShape3D` must have `map_width == map_depth` to become a Jolt height field; otherwise it becomes a slow mesh. | Use square, padded chunks. | BE T-033 |
| Jolt's default `max_bodies` is 10,240. Scattering one body per tree or rock overflows it silently: creation fails, with one error. | Use compound static bodies per cell, streamed in a ring around each vehicle, or raise the limit. | BE T-034 |
| A tyre model with no static friction lets a parked vehicle creep downhill. | Add an explicit parking hold. | BE T-035 |
| A float32 `Vector2` intermediate can round a point just below a grid midpoint into the next surface sample. | Match the authoritative scalar grid arithmetic and test both axes and surface orderings against an independent raw-grid example. Do not add an exclusion margin to hide the mismatch. | BE, `docs/captures/T-045/REPORT.md`, Clearance diagnosis: three grass-on-talus records |

## UI and input

| Pitfall | Do this | Evidence |
|---|---|---|
| Windows system fonts (Bahnschrift, Segoe UI, Consolas) can't be redistributed. | Load them by name with `SystemFont`, never copy the files, and keep a fallback chain. | BE T-041 research |
| Godot 4.5+ uses SDL3, which gives no DualSense adaptive triggers and no lightbar effects. | Plan rumble only, gated on `has_joy_vibration()`. | BE ui-input dossier F1 |
| Closing a menu with a button that is also a gameplay action fires that action. | Wait until the button is released before resuming play. | BE T-036 |

## Audio

| Pitfall | Do this | Evidence |
|---|---|---|
| Headless audio rules use the Dummy driver, so a passing rule test does not exercise the native audio device or scheduling. | Record the actual audio driver; run playback/phase checks through the native backend when that is the claim. Keep subjective sound quality as a separate listening result. | BE combined preview, `C:/Dev/Backcountry Expedition Playtest/docs/playtests/2026-11-02-controls-audio.md`: Dummy rule run and 36 WASAPI checks; listening pending |
| A raw pitch step per rendered frame changes with frame duration, so a long headless frame can fail a smooth-rate limit. | Record elapsed time and express the measurement at the specified time base. Replay hand-worked short/long-frame cases and a real excessive jump; preserve the stated rate limit. | BE, `docs/captures/T-120/REPORT.md` and `T-121/REPORT.md`: recorder-only normalization, nine rule checks and 25 reported S74 passes; native sound unchanged by that measurement fix. |
