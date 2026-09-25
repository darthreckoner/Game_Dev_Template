# Pitch card and engine matrix

## Pitch card fields

- **Player fantasy:** who the player gets to be or what they get to do, in one line.
- **Core verbs:** three to five actions the player performs most.
- **Core loop at three timescales:** the second-to-second action, the minute-to-minute
  goal, and what a session builds toward.
- **Pillars:** three experience goals that decide trade-offs. **Anti-pillars:** what
  the game deliberately is not.
- **References:** each reference game with the specific thing to take from it.
- **Scope class:** jam (days), prototype (answers one question), or vertical slice
  (one representative portion at intended quality).
- **Top fun risk:** the question the first playable build must answer.

A useful lens when the loop feels vague: describe the intended player experience
first, then the moment-to-moment behavior that produces it, then the rules that
produce that behavior (the MDA framework).

## Engine matrix for agent-driven work

| | Godot | Unity | Unreal | three.js / web |
|---|---|---|---|---|
| Agent can read and diff content | Yes (text scenes, GDScript) | C# yes; scenes verbose YAML | C++ yes; Blueprints binary | All code |
| Headless tests and CI | Straightforward | Workable; license activation | Heavy | Easiest |
| Agent bridge | Community MCPs; template kit exists | Official (paid beta) and community | Official (experimental) and community | Browser tools plus game hooks |
| Best fit | 2D, small-to-mid 3D, solo speed | Cross-platform, mobile, ecosystem | High-fidelity 3D | Web distribution, jams |

Prefer the engine with an installed kit unless the game's needs clearly outweigh
the cost of building a new one. The research behind this matrix is in the template
history; recheck tooling claims older than six months.
