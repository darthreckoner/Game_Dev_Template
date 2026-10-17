# Kits

A kit holds engine- or tool-specific material that a project copies in only after
the user chooses that engine or service. Nothing here loads at startup.

| Kit | Status | Contents |
|---|---|---|
| `godot/` | Ready (Godot 4.7.2, Windows; dispatcher and a rendered scenario screenshot verified 2026-10-16) | `godot` skill with helpers, architecture defaults, example scenario, provenance |
| `assets/` | Examples only | MCP configuration examples for asset services |
| Unity, Unreal, web/three.js, Blender, Roblox | Not built | Build when a project chooses one; check current tooling first |

Candidate sources for unbuilt kits are in the source template's
`docs/research/2026-09-25-ai-solo-game-dev-kit.md`, Appendix A (tool landscape
as of September 2026; refresh before use):

- **Unity:** official Unity MCP (needs Unity AI plan) or CoplayDev/unity-mcp; Unity
  Test Framework in batch mode.
- **Unreal:** UE 5.8 experimental MCP plugin or chongdashu/unreal-mcp; Automation
  framework. Blueprints are binary, so agents depend on the editor bridge.
- **three.js/web:** Playwright for driving, an exposed `window.__game` test API for
  state, seeded simulation; skill packs such as threejs-game-skills for reference.
- **Blender:** the official Blender Lab MCP for exploration; headless
  `blender -b -P` scripts for repeatable normalize/export steps.
- **Roblox:** the Studio MCP plus Rojo for file sync; verify Open Cloud and TestEZ
  details first.

A new kit copies the Godot kit's shape: one scoped skill installed to
`.claude/skills/<engine>/`, an architecture defaults reference, verified Windows
commands, an example scenario, and a provenance record for anything adapted from
upstream.
