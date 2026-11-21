# More Blender skills (not installed)

The kit installs five skills: `blender-core`, `blender-scene-setup`,
`blender-asset-qa`, `blender-game-optimization`, `blender-export-pipelines`.
The same upstream pack has 23 more. They stay out by default so a session does
not load descriptions it will not use.

## When to add one

Check this list whenever the work changes shape:

- The Director, when `DESIGN.md`, the art bible, or an asset spec first calls for
  a kind of work below (characters, hand-authored wear, terrain, a toon look).
  Name the skill in the ticket.
- The Coder, when a ticket needs it and it is missing. Install it, record the
  install under Assumptions in `STATE.md`, and carry on.

Add a skill when the design asks for the work, not because it might be useful
later. Only the five installed skills were run on a real game model; treat the
others as tested by their own suite only until a project has used them.

## The list

### Building and surfacing a model

| Skill | What it does | Add it when |
|---|---|---|
| `blender-hardsurface-modeling` | Props, vehicles, weapons, buildings: blockout to detail, bevels, booleans, clean shading | Models are built in Blender, not bought or generated |
| `blender-sculpting` | Organic shapes: creatures, rocks, characters; turning a sculpt into a game mesh | The game needs organic models or bake sources |
| `blender-retopology-uv` | Turns a dense or messy mesh into a clean game mesh and lays out its texture coordinates | Using scans, sculpts or AI-generated meshes |
| `blender-pbr-materials` | Wires texture sets into correct materials; color space and channel-packing rules | Any model with real textures |
| `blender-texturing` | Edge wear, grime, dust, rust, decals, trim sheets, hand painting | Surfaces need to look used, or parts share a trim sheet |
| `blender-texture-baking` | Transfers detail from a dense model onto a light one as texture maps | A high-detail source and a low-detail game mesh both exist |
| `blender-geometry-nodes` | Rule-driven models from a short description: scattering, parametric parts | Many variants of one thing, or procedural props |
| `blender-stylized-npr` | Toon and anime shading, outlines, line art | The art bible picks a non-realistic look |

### Characters

| Skill | What it does | Add it when |
|---|---|---|
| `blender-character-rigging` | Skeletons, skinning, engine-ready rigs, deformation stress tests | Anything with a skeleton |
| `blender-animation` | Keyframes, loops, motion-capture retargeting, root motion, per-clip export | Any animated model |
| `blender-facial-shapekeys` | Facial expressions and lip-sync shapes | Characters talk or emote up close |
| `blender-clothing` | Garments that follow the body without poking through; swappable outfits | Characters wear separate or changeable clothes |
| `blender-hair-grooming` | Hair, fur, beards, game hair cards | Characters or animals need hair |

### Worlds

| Skill | What it does | Add it when |
|---|---|---|
| `blender-environment-kits` | Terrain, heightmaps, biome scatter, modular building kits with grid and seam checks | Levels or landscapes are authored in Blender |
| `blender-simulation` | Rigid bodies, cloth, fluids, smoke, baked to keyframes | Pre-baked destruction, drapes or flags |
| `blender-weather-fx` | Rain, snow, puddles, wet surfaces, lightning, weather masks for engines | Weather is authored in Blender rather than in the engine |
| `blender-time-of-day` | Sky, sun, night, fog and mood lighting setups | Mood or key-art renders; the engine lights the game itself |

### Pictures and presentation

| Skill | What it does | Add it when |
|---|---|---|
| `blender-lighting-lookdev` | Studio lighting, HDRI, cameras, turntables | Review renders or store art of an asset |
| `blender-rendering` | Render engines, quality presets, denoising, batch renders | Any still or animation rendered in Blender |
| `blender-video-editing` | Cuts clips together, titles, music; camera tracking | Trailers or capture edits |

### Pipeline

| Skill | What it does | Add it when |
|---|---|---|
| `blender-pipeline-automation` | Batch jobs over folders of files, format conversion | Dozens of assets need the same step |
| `blender-addon-development` | Writing Blender add-ons | The project needs its own Blender tool |
| `blender-workflow-recipes` | Start-to-finish playbooks chaining the other skills (prop, character, cleanup of a downloaded asset) | Several of the above are installed; it assumes they are |

## Install one

From the project root, in PowerShell. The commit is the one this kit was built
and tested from; use it, not the branch tip.

```powershell
$tmp = Join-Path $env:TEMP 'cloud-blender-skills'
if (-not (Test-Path $tmp)) { git clone https://github.com/patch-gg/cloud-blender-skills $tmp }
git -C $tmp checkout d659b96ee43518693ec3e2ea5062211da43720b9
$name = 'blender-pbr-materials'   # the skill to add
Copy-Item -Recurse "$tmp\skills\$name" ".claude\skills\$name"
Copy-Item "$tmp\LICENSE" ".claude\skills\$name\LICENSE"
```

Rules:

- **Never copy `blender-cloud`.** It is a paid service and upstream makes it the
  default runner. Never install the `pch` tool for this.
- **Never overwrite `blender-core`.** The kit's copy is the local-only one.
- Do not use the upstream plugin installer or `install.ps1`; both install all 29.
- Record the added skill and the commit in the project README's Blender section.
- If Codex takes tickets, rerun `tools/sync-codex-skills.ps1`.
- Every skill says "the execution model is in `blender-core`". That means the
  kit's local runner; nothing else is needed.
