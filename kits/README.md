# Kits

A kit holds engine- or tool-specific material that a project copies in only after
the user chooses that engine or service. Nothing here loads at startup.

| Kit | Status | Contents |
|---|---|---|
| `godot/` | Ready (Godot 4.7.2, Windows) | `godot` skill with helpers, architecture defaults, provenance |
| `assets/` | Examples only | MCP configuration examples for asset services |
| Unity, Unreal, web/three.js, Blender | Not built | Build when a project chooses one; check current tooling first |

Candidate sources for unbuilt kits, from the 2026-09-25 research in Railroad Wars
(`docs/research/ai-solo-gamedev-environment-2026-09-25.md`):

- **Unity:** official Unity MCP (needs Unity AI plan) or CoplayDev/unity-mcp; Unity
  Test Framework in batch mode.
- **Unreal:** UE 5.8 experimental MCP plugin or chongdashu/unreal-mcp; Automation
  framework. Blueprints are binary, so agents depend on the editor bridge.
- **three.js/web:** Playwright for driving, an exposed `window.__game` test API for
  state, seeded simulation; skill packs such as threejs-game-skills for reference.
- **Blender:** the official Blender Lab MCP for exploration; headless
  `blender -b -P` scripts for repeatable normalize/export steps.

A new kit copies the Godot kit's shape: one scoped skill, an architecture defaults
reference, verified Windows commands, and a provenance record for anything adapted
from upstream.
