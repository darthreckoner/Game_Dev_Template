# Asset specs and providers

## Spec template (`art/specs/<asset>.md`)

```markdown
# <asset name>
Status: draft | approved (<who>, <date>) | delivered
Used in: <scene/system> · Build or ticket: <v1 / T-###>
Purpose: what the player must read from it
Form: sprite | sprite sheet | tileset | 3D mesh | UI | audio
Size: <px or units>; pixel/texel density: <…>; camera distance: <…>
Frames/states: <list with timing>; directions: <4/8/none>
Pivot/origin: <…>; transparency: <yes/no>; palette: <art bible slots or limits>
Poly/texture budget (3D): <…>; formats: <png/glb/…>
Style references: <art/references/ files + what to take>
Acceptance: the checks the delivered file must pass
Placeholder allowed: yes/no
```

## Provider notes

Use a service only when the Project settings in `DESIGN.md` list it in the tool
budget. Record every result in `assets/ASSET_SOURCES.md`, including the plan
tier's terms at generation time. Service capabilities change often; check current
docs before relying on these notes.

- **Placeholders:** simple shapes drawn in-engine or as small PNGs. Free and
  deterministic; prefer them until a direction is approved.
- **Hand-run image generation (ChatGPT, or any image model the designer uses):**
  the designer generates from the spec and drops the file in `assets/`. Record
  the model, prompt, and date; keep the prompt with the spec so a regeneration
  matches. No configuration needed.
- **Pixel art:** PixelLab (official MCP: directional characters and animations,
  Wang/sidescroller/isometric tiles, map objects); Retro Diffusion (hosted MCP,
  many styles); Aseprite for editing and deterministic sheet export.
- **Concept, UI, icons:** a strong general image model; keep the prompt and seed.
- **3D:** Tripo or Meshy (official MCPs; rigging and animation presets). Free tiers
  may be non-commercial or attribution-only. Normalize scale, orientation, and
  pivot before handoff, ideally with a Blender script.
- **Audio:** ElevenLabs (official MCP) for SFX and music; sfxr-style generators for
  deterministic retro SFX.

The template's `kits/assets/` has example MCP configuration for services the user
approves. Keep keys in environment variables. Free tiers are a licensing trap
for a later commercial release, and Steam requires disclosure of AI-generated
content; record terms at generation time.
