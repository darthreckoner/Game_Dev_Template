---
name: blender-core
description: Foundation for any Blender 5.2+ task an agent drives - running bpy headless on the local Blender or live via MCP, context overrides, locale-safe node lookup, enum discovery, 5.x API changes, verification. Use first for any Blender, bpy, .blend or 3D-asset request; routes to the installed blender-* skills and lists the ones a project can add.
license: MIT
compatibility: Blender 5.2 LTS or newer, verified on 5.3. Optional blender-mcp server for live sessions.
metadata:
  author: blender-agent-skills
  version: "1.2.0"
---

# Blender Core (5.2 LTS+, 5.3)

## Route to the specialized skill
Installed with this kit:
| Task | Skill |
|---|---|
| Units, collections, naming, linking, asset libraries | `blender-scene-setup` |
| Poly budgets, LODs, draw calls, cleanup | `blender-game-optimization` |
| Export: glTF/FBX/USD to Roblox, Unity, Unreal, Godot, web | `blender-export-pipelines` |
| Checking a mesh/asset before delivery (always) | `blender-asset-qa` |

**More skills exist and are not installed.** The same pack has 23 others: modeling, sculpting, UVs, materials, texturing, baking, rigging, animation, clothing, hair, environments, weather and more. When the game's design or a ticket calls for that kind of work, read [references/more-skills.md](references/more-skills.md), pick the ones that fit, and install them as it describes. Do this before improvising the same work by hand. A skill named in this kit that is missing from the project's skills folder (for example `blender-texture-baking`) is one of these.

## Execute
**Default: headless, on this machine's Blender.** `run_in_blender.py` finds Blender (`$BLENDER_EXE`, then PATH, then the standard install folders), runs the script, and prints only the script's JSON (`@@JSON@@` lines):
```
python <skills_dir>/blender-core/scripts/run_in_blender.py --blend in.blend <script.py> -- --objects Chair --save out.blend
python <skills_dir>/blender-core/scripts/run_in_blender.py --expr "import bpy; print(len(bpy.data.objects))"
```
Each call is a fresh Blender: nothing stays between calls except what a script saves. This kit has no cloud backend; the upstream pack's paid cloud runner was removed, so nothing here spends money.
**Live (blender-mcp `execute_blender_code`)**, for the person's open Blender: work in small steps and print only what you need. To call a skill script, import it:
```python
import sys, importlib; sys.path.insert(0, r"<skills_dir>/blender-asset-qa/scripts")
import qa_check; importlib.reload(qa_check); print(qa_check.run(objects=["Chair"]))
```
Each MCP call runs in a **fresh namespace**: re-`import` in every call. That's cheap because modules stay cached in `sys.modules`. `reload` only after editing a script.
**Windows + Git Bash**: MSYS rewrites `//out.png` to `/out.png` (→ `C:\out.png`). Prefix with `MSYS_NO_PATHCONV=1` and pass skill paths as `$(cygpath -m ~/.claude/skills)/...` (or use PowerShell).
Raw form: `blender -b in.blend --factory-startup --python-exit-code 1 -P x.py -- args`. Every script here exposes `run(**kw) -> dict` and the same flags after `--`.
**First call in a session**: `scripts/env_report.py`, which returns the version, engines, GPU, add-ons, units, color management and scene counts.

## Rules
- **Data API over operators**: use `bpy.data`, `bmesh`, `mesh.attributes`, and `foreach_get/set` with numpy. Operators depend on context and selection, and many need a 3D View, which background mode doesn't have.
- If an operator is unavoidable: `with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]): bpy.ops...`. Check that the result is `{'FINISHED'}`.
- **Edit mode isolation**: `ob.data` isn't updated while in Edit Mode. Use `bmesh.from_edit_mesh` + `bmesh.update_edit_mesh`, or switch to OBJECT mode before reading.
- **Nodes**: find them by `type` (`n.type == "BSDF_PRINCIPLED"`), never by `name`, because names are localized. Sockets by English name or `identifier` are fine.
- **Enums**: read the valid values with `[i.identifier for i in T.bl_rna.properties[p].enum_items]`. Dynamic enums (`render.engine`, `view_transform`, `look`) under-report, so assign them inside `try/except TypeError` (the message lists the valid values).
- **Engines**: `BLENDER_EEVEE`, `CYCLES`, `BLENDER_WORKBENCH`. Cycles device: `scene.cycles.device = "GPU"` + preferences `compute_device_type`.
- **Evaluated data**: use `ob.evaluated_get(depsgraph)`, then `.to_mesh()`, then always `.to_mesh_clear()`. Call `view_layer.update()` before reading `matrix_world` after a change.
- **Freed data**: applying or removing a modifier, or removing an object or ID, frees it. Collect names first (`[m.name for m in ob.modifiers]`) and never touch the old Python reference afterward, because it returns garbage or crashes.
- **Never trust default names** ("Cube.001"). Keep object references, rename explicitly, and look objects up via `bpy.data.objects[name]`.
- **Scale**: 1 unit = 1 m. Apply rotation/scale (`transform_apply`) before bevels, modifiers with distances, rigging, physics, baking and export.
- **Paths**: `bpy.path.abspath("//textures/x.png")` resolves relative to the .blend. Save explicitly; use `save_as_mainfile(filepath=..., copy=True)` for backups.
- **Live sessions are the user's work**: never `read_factory_settings`, never delete data you didn't create, and save a backup copy before destructive batch edits.
- **GPU module in background**: call `gpu.init()` first (5.2+). `bgl` no longer exists.
- **Big meshes**: no per-vertex `bpy.ops`. Use numpy `foreach_get` (see references/bpy-patterns.md).

## 5.x API changes that break old tutorials/LLM memory
`action.fcurves` → channelbags · `scene.node_tree` → `scene.compositing_node_group` · `material.use_nodes` is deprecated (new materials already have nodes) · `mod["Socket_2"]` → `mod.properties.inputs.Socket_2.value` (5.2) · `BLENDER_EEVEE_NEXT` → `BLENDER_EEVEE` · Boolean `FAST` → `FLOAT` · bone layers → bone collections · `bl_info` add-ons → extensions (`blender_manifest.toml`) · `bpy.props` values are no longer dict-accessible (`scene["cycles"]`) · 5.3: compositor effects stack, glTF WebP options → compressed-image options, VSE `EXPAND` → `RIPPLE`. Full table: [references/api-changes-5x.md](references/api-changes-5x.md).

## Verify (required before saying "done")
1. Numbers, not adjectives: report tris, objects, materials, dimensions (`ob.dimensions`) and the output files written.
2. Geometry changed → run `blender-asset-qa` `qa_check.py` (z-fighting, detached parts, non-manifold, flipped normals, scale).
3. Look at it: MCP `look` (`mode="angles"`, shading `material`/`wireframe`). Headless: `blender-asset-qa/scripts/review_shots.py` renders contact sheets.
4. Re-read your own output: confirm that exported files exist and that their size is non-zero.

## References
- [references/api-changes-5x.md](references/api-changes-5x.md): 4.x→5.3 migration table. Load it when code fails with AttributeError/KeyError.
- [references/bpy-patterns.md](references/bpy-patterns.md): verified snippets for bmesh, attributes, numpy, temp_override, depsgraph, drivers, append/link, handlers and timers.
