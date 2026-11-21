# Blender skills trial (2026-11-21)

Trial of the `cloud-blender-skills` pack as the source for the unbuilt Blender
kit. Status: **trial complete, awaiting the designer's decision**. Nothing is
installed in the template.

## Source

- Page: <https://patch.gg/rehan/cloud-blender-skills>
- Repo: <https://github.com/patch-gg/cloud-blender-skills>, commit `d659b96`
  (2026-11-18). MIT. A fork of EL4CTEO's `blender-skills` 1.3.2 (MIT) with one
  added skill, `blender-cloud`, for Patch's paid cloud Blender.
- 29 skills, about 13,000 lines of Python, 1.6 MB. The four of interest
  (`blender-core`, `blender-asset-qa`, `blender-export-pipelines`,
  `blender-game-optimization`) total about 340 KB.

## Designer's decisions (2026-11-21)

- Run the trial on local Blender, not the cloud.
- Use Backcountry Expedition's Crowell Colt as the real model.
- Show the results before any kit is built.
- Open: whether the kit lives in the Template or the Library.

## Setup

- Blender 5.2.2 LTS, Windows 11, RTX 3070, Python 3.14 on the host.
- `pch` (Patch's CLI) is not installed and `BAS_BACKEND=local` was set, so
  nothing ran in the cloud and nothing was spent.
- Model: the eleven shipped `.glb` files in Backcountry's
  `assets/vehicles/crowell_colt/` (Backcountry commit `5fa67d49`), imported into
  one scratch `.blend`. Backcountry was read only; nothing there was changed.

## Results

| Step | Result |
|---|---|
| Pack's own suite (`tools/run_tests.py`) | 73 passed, 0 failed, 0 skipped ([log](suite-results.log)) |
| `env_report.py` | Worked. Correct version, GPU, units |
| `qa_check.py`, 22 meshes, `game` profile | Ran in 9.6 s. Fail: 32 errors, 64 warnings ([output](colt-check-output.json)) |
| `mesh_stats.py`, `pc` budget | 109,846 triangles, 16 materials, 27 textures, 285 MB uncompressed |
| `scene_audit.py` | Clean |
| `review_shots.py` | Worked ([sheet](colt-review-sheet.png)). `material` mode rendered plain grey, not the textures |
| `export_asset.py --preset godot`, body | Same 85,134 triangles, 18 nodes, 6 materials, 7 images and mount-point positions as the shipped file. **Dropped tangents**: 8.2 MB against 10.6 MB shipped |

### What the check found on the Colt

Real, cross-checked with a separate script written for this trial:

- **Collapsed triangles.** The check reports 38 in `body`; the separate count
  found 33 below 1e-10 m². Also 3 to 6 each in both doors, liftglass, tailgate.
- **Doubled faces in the same place, facing the same way** (flicker risk). The
  separate count found 278 pairs within 0.5 mm in `body` (one cluster at
  x -0.152, y 1.851, z 0.496 m) and 188 in `panel_tailgate`. The check's own
  count is higher (1,204 and 14) because it measures overlap differently.
- **Hidden back-to-back faces**: 5,408 pairs in `body`, 2,338 in `hardtop`
  (check's figure; the separate count at 0.5 mm found 79 and 146).

Not cross-checked: zero-area texture faces (291 in `body`).

False alarms and noise:

- Every wheel-against-wheel "z-fighting" error (14 of the 32). The four wheels
  ship at the origin and the game places them; assembling them in one file made
  them overlap. The check needs one asset's parts in their real positions.
- "UV overlap" on every trim-sheet part. Overlap is how a trim sheet works.
- "Duplicate verts" on everything. A `.glb` splits vertices at seams.
- "Not resting on the ground". Backcountry's origin is deliberate.
- The `pc` prop budget (50,000 triangles, 6 materials). A generic figure, not
  Backcountry's.

## Assessment

- The scripts run on local Blender 5.2 on Windows without changes.
- The check finds real geometry defects in seconds. It does not say **where**
  z-fighting is, only how many pairs, so each finding needs a follow-up look.
- It is noisy on a shipped multi-part vehicle. A kit needs a note on how to feed
  it (one asset, parts in place, source file rather than exported file) and
  which warnings a project may accept.
- The Godot export preset is not a drop-in for a project that ships tangents.
- No finding here is an instruction to Backcountry. The Colt results go to that
  project's Director as evidence.

## If adopted

- Take four skills, strip `blender-cloud` and every "cloud by default" line,
  pin `BAS_BACKEND=local`, record provenance and the MIT notice.
- Do not use the plugin installer; it loads all 29 skills.
