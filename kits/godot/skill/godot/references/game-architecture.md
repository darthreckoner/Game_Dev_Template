# Game architecture defaults

Defaults for new Godot projects and systems in this template. They exist to make
rules testable without rendering and presentation reviewable from captures. Depart
from them when the game's needs differ; record the reason in PROJECT.md.

## Simulation core, presentation shell

- Put game rules in plain GDScript classes (`RefCounted`, or `Resource` for data)
  with no dependency on nodes, scenes, input, or rendering. Examples: route graphs,
  economies, inventories, turn resolution, AI decisions.
- Advance the simulation with an explicit fixed step (`step(delta)` with a constant
  delta) so a run is reproducible. Use a seeded `RandomNumberGenerator` owned by
  the simulation, never global randomness.
- Make simulation state serializable to a Dictionary, for saves, state dumps, and
  test assertions.
- Scenes present the state and forward player intent as commands to the
  simulation ("call down, signal up"). Scenes may interpolate visually between
  simulation steps but must not own rule state.
- Keep tuning values in data (`.tres` resources or JSON under `data/`), not
  scattered constants.
- Use autoloads sparingly: one for the game session is common; avoid global
  mutable state elsewhere. Prefer typed GDScript and treat warnings as defects.

## Scenarios

A scenario is data: initial setup (map, placed objects, resources), a seed, a list
of commands with the step or time they occur, and expected outcomes. Keep them in
`tests/scenarios/`. The same scenario should run three ways:

1. **Headless simulation only** for rules tests (fast, no scene).
2. **Headless with scenes** through the scenario runner for wiring checks.
3. **Rendered** for review-moment screenshots and Movie Maker sequences.

Name review moments to match the milestone contract (`R1`, `R2`, …) and capture
them at the contract's resolution and UI scale.

## Direct GDScript tests (no framework)

```gdscript
extends SceneTree
# Run: godot --headless --path <project> --script res://tests/test_routes.gd
const RouteGraph = preload("res://sim/route_graph.gd")
var failures: Array[String] = []
var checks := 0

func _initialize() -> void:
	call_deferred("run")

func check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)
		push_error(message)

func run() -> void:
	var graph := RouteGraph.new()
	# … arrange, act, assert with check(…) …
	if failures.is_empty():
		print("ROUTES_PASS checks=", checks); quit(0)
	else:
		print("ROUTES_FAIL checks=", checks, " failures=", failures); quit(1)
```

Expected values come from the contract or an independent worked example, not from
running the implementation. Add GUT or GdUnit4 only if the user chooses to.

## Saves and isolation

Automation must never touch real player saves. Pass save paths into the systems
that use them, and give tests fixture paths under `user://test/` or an isolated
project identity. Reset tests prove the state is actually cleared, not just hidden.

## Performance checks

When a contract sets a budget, measure a fixed rendered scenario after warm-up
with the scenario runner's performance assertions, on the stated device, with no
other builds running. Record renderer, resolution, and hardware.
