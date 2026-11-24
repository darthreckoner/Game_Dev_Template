# Tool candidates

Open-source tools reviewed for this template, sorted by what a project should do
with them. Nothing here is installed. The Director checks this list when a design
first calls for one of the needs below, and the designer approves any install,
because each one pins the engine build or adds a dependency to every later
session.

Reviewed 2026-11-24 from each repository's README and latest release (designer's
list of ten). Versions and engine support go stale; recheck the repository before
installing anything older than six months.

## Already covered: use what the engine has

| Tool | What the template uses instead | When to look again |
|---|---|---|
| [Jolt Physics](https://github.com/jrouwe/JoltPhysics) (MIT, v5.7.0) | Built into Godot since 4.4 as an engine module; Godot kit projects already set `3d/physics_engine="Jolt Physics"`. Jolt rules live in `godot/skill/godot/references/pitfalls.md` (square height fields, 10,240-body default). | Never install the separate [godot-jolt](https://github.com/godot-jolt/godot-jolt) extension: it is in maintenance mode and supports Godot 4.3 to 4.6 only. The built-in module lacks some joint classes (for example `JoltHingeJoint3D`); use the generic `HingeJoint3D` family. |
| [Recast Navigation](https://github.com/recastnavigation/recastnavigation) (Zlib, v1.6.0) | Godot's own navigation (`NavigationRegion3D`, `NavigationAgent3D`, `NavigationServer3D`) bakes its navigation meshes with Recast. Agent avoidance is built in. | Only for a custom engine. In Godot, bake the region in a scenario and assert the path state; don't add the library. |
| [meshoptimizer](https://github.com/zeux/meshoptimizer) (MIT, v1.3) | Godot uses it on import to generate mesh LODs ("Generate LODs" import option). The Blender kit's glTF export can use its compression. | `gltfpack`, its command-line tool, shrinks and compresses `.glb` files. Worth a trial for a web export or a download-size budget; give it its own check (file size before and after, model still passes the Blender kit check). |
| [FastNoise2](https://github.com/Auburn/FastNoise2) (MIT, v1.1.1) | Godot's built-in `FastNoiseLite` and `NoiseTexture2D`, already used for camera shake. | Only if a measured profile shows noise generation is the bottleneck (the author's benchmark claims about 6x faster with AVX2). No maintained Godot binding was found. Its node editor (desktop or the web version at auburn.github.io/FastNoise2) can help the designer pick a noise look; record the chosen values in the tuning file, not the tool's file. |

## Candidates: install when a design calls for it

| Need in the design | Tool | Fit for agent-driven work | Check before adopting |
|---|---|---|---|
| Large outdoor landscapes: sculpted terrain, painted ground textures, heightmap import, foliage with levels of detail | [Terrain3D](https://github.com/TokisanGames/Terrain3D) (MIT, v1.1.0, GDExtension, "Godot 4.5-4.8+", Asset Library) | Medium. Sculpting and painting are editor work for the designer or artist; whether a script can build or edit terrain headlessly was not confirmed (the API docs are on readthedocs). Heightmap import gives agents a file-based route. | Confirm the project's renderer is supported (Backcountry Expedition runs GL Compatibility). Confirm collision becomes a square Jolt height field (see the Jolt pitfalls). Run the headless test suite and one rendered scenario with the extension loaded. Compare against the hand-built terrain a project already has before switching; that is a rebuild-level change. |
| Procedural textures and materials made from nodes, or painting on a model | [Material Maker](https://github.com/RodZill4/material-maker) (MIT, 1.8, standalone app built on Godot 4.7.2; itch.io, Steam, Scoop, Chocolatey) | High. It has a command-line export: `--export` (or `--export-material`) with `-t` target (default "Godot/Godot 4 Standard"), `-o` output folder, `--output-file`, `--size` (default 2048). A `.ptex` graph in the repository can be re-exported by an agent. | Keep inputs as local `.ptex` files: `website:` inputs download at export time, which breaks repeatable builds. Whether it runs with `--headless` is unconfirmed; test once. Record each exported material in `assets/ASSET_SOURCES.md`. Colors and values come from the art bible. |
| Showpiece 3D effects (explosions, spells, impacts) beyond what `GPUParticles3D` gives easily | [Effekseer](https://github.com/effekseer/Effekseer) editor (MIT, 1.80.8) with [EffekseerForGodot4](https://github.com/effekseer/EffekseerForGodot4) (MIT, 1.80.5.1) | Low. Effects are authored in a desktop editor with no command line, so agents can place and trigger them but not author them. | Use the editor version that matches the plugin (1.80.5 for plugin 1.80.5.1, not the newer 1.80.8). The plugin is native code; confirm it loads in Godot 4.7.2 (its notes mention a 4.7 script fix) and on every export target, including web. Effects still play from the juice layer on gameplay events. Godot's built-in particles stay the default. |
| 3D props, set pieces and nature (rocks, trees, grass, moss) made by agents rather than an artist, for a flat-colour or low-poly art bible | [sand3d](https://github.com/Sandflow-ai/sand3d) (Apache-2.0, v1.7.0, Python library over Blender's `bpy`; reviewed 2026-11-24, designer request) | High: built for language models. A model is a short Python program (parts reached by name, same program gives the same mesh), so an agent can write, re-run and revise one. Exports `.glb` with materials, and joints in the node extras. | Colour is one RGB per face, with no UVs or textures, so on its own it suits an art bible that wants flat or vertex colour. Textures can be added afterwards, in three levels of effort: (1) natural surfaces (rock, ground, bark, rough metal) take a tiling Godot material with triplanar mapping (`uv1_triplanar`), which needs no UVs; (2) a scripted Blender pass (automatic UV unwrap, then a Material Maker or tiling material) covers most props; (3) hand-painted or one-off textures need clean UVs that an automatic unwrap won't give, so that is artist work. Not tested here. Nature verbs and `displace`/`field` can make millions of triangles (its own budget allows 4 M): run every export through the Blender kit's `mesh_stats.py` budget and `qa_check.py`, and set a cell or step size in the program. Units are millimetres; confirm scale lands in metres in Godot. Needs Python 3.13 with the `bpy` 5.2 wheel (no 3.12), separate from the Blender kit's installed Blender; pin the version, since the project was three weeks old with releases every few days. Joints in GLB extras are not read by Godot; rebuild moving parts as scenes. Record each program in `assets/ASSET_SOURCES.md` as the model's source. Not yet run here. |
| Worlds the player digs through or destroys: caves, tunnels, overhangs, streamed voxel terrain | [Voxel Tools](https://github.com/Zylann/godot_voxel) (MIT, v1.7, August 2026) | Medium. Generators are scriptable, but the main release is a custom Godot build. | This is a pillar-level, engine-level choice for the designer. The Windows release is a custom Godot 4.7.2 build with the module compiled in; the extension version exists but its README still lists "Make GDExtension work" on the roadmap. Adopting it replaces the pinned editor in the Godot kit's commands and in CI. |

## Not for this template

| Tool | Why |
|---|---|
| [ozz-animation](https://github.com/guillaumeblanc/ozz-animation) (MIT, 0.17.0) | A runtime for people writing their own engine. Godot's `AnimationPlayer` and `AnimationTree` already load, play and blend animations. |
| [The Forge](https://github.com/ConfettiFX/The-Forge) (Apache-2.0) | Graphics groundwork for a custom engine; no physics, sound or networking. Development moved to codeberg.org/The-Forge after v1.63 (March 2025). Revisit only if a project builds its own engine. |

## Adding a tool

When a project adopts one: record the version, licence and source in the
project's README and `assets/ASSET_SOURCES.md` (for content tools), add the
install step and a verified check command, and note it in `DESIGN.md` Project
settings. If it works well across a project, the retro proposes promoting it to
a kit here.
