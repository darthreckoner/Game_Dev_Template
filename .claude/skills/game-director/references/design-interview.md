# Design interview aids

## When the loop feels vague

Describe the intended player experience first, then the moment-to-moment behavior
that produces it, then the rules that produce that behavior (the MDA framework).

## Scope class

- **Jam:** days. One mechanic, rough edges accepted.
- **Prototype:** answers one question, usually the top fun risk.
- **Vertical slice:** one representative portion at intended quality.

## Budget

Tokens are cheap on subscription plans; attention and rounds are not. Set, before
the first build: how many coder sessions, how many review-and-fix rounds, and how
much calendar time the first playable gets. When it runs out, the designer
decides (accept, rescope, rebuild) rather than letting the loop run on.

## Top fun risk

Rank the largest unknowns in fun, technology, art, and scope. State the top fun
risk as a question a small playable build can answer, and name the screenshots
and play notes that would answer it. A moving object demonstrates technology; a
repeatable loop with a consequence demonstrates the beginning of a game.

## Engine matrix for agent-driven work

| | Godot | Unity | Unreal | three.js / web | Roblox |
|---|---|---|---|---|---|
| Agent can read and diff content | Yes (text scenes, GDScript) | C# yes; scenes verbose YAML | C++ yes; Blueprints binary | All code | Luau yes; place file editor-bound unless Rojo syncs it |
| Headless tests and CI | Straightforward | Workable; license activation | Heavy | Easiest | Limited; Studio-bound |
| Agent bridge | Community MCPs; template kit exists and is verified | Official (paid beta) and community | Official (experimental) and community | Browser tools plus game hooks | Built-in Studio MCP; Rojo for files |
| Best fit | 2D, small-to-mid 3D, solo speed | Cross-platform, mobile, ecosystem | High-fidelity 3D | Web distribution, jams | Built-in multiplayer and distribution |

Prefer the engine with an installed kit in `kits/` unless the game's needs
clearly outweigh the cost of building a new one. The matrix dates from
2026-09-25 (Roblox column 2026-10-16); the research behind it is in the source
template's `docs/research/`. Recheck tooling claims older than six months.
