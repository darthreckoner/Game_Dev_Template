---
name: godot
description: Inspect, edit, run, test, and capture Godot 4 scenes, scripts, and resources with portable helpers — including scripted scenarios, state assertions, and named-moment screenshots for build checks. Use for Godot implementation and verification tasks in this project.
---

# Godot

Follow the project AGENTS.md, DESIGN.md, the current build prompt or ticket, and
current user decisions. Use this skill's helpers where they reduce scene-editing, diagnostic,
or capture work. Upstream playbooks, architecture, and templates are optional
references for an agreed task, not defaults to impose.

## Work loop

1. Read the relevant project guide and inspect the scene or script being changed.
   Preserve unrelated edits and authored layouts.
2. For command setup, read [Windows commands](references/windows.md). Discover an
   operation with dispatcher `help` before using an unfamiliar parameter. Treat
   scoped linting as diagnostic advice; confirm findings against Godot and the
   project's conventions before changing code.
3. Make the bounded change. Scene and resource operations can instantiate scripts
   and run tool code. Test unfamiliar mutations on a disposable copy first, and
   save or coordinate open editor edits before changing their files externally.
4. Run the project's tests relevant to the change, then capture runtime diagnostics
   for the changed scene. Report unrelated warnings separately rather than
   expanding the task into a cleanup.
5. Inspect rendered changes and exercise the affected interaction. Image statistics
   and clean logs cannot establish appearance, usability, or playtest acceptance.
   Report automated results, visual inspection, remaining gaps, and delivery state.

## New projects and systems

Read [game architecture](references/game-architecture.md) before scaffolding a
project or a new gameplay system. It sets the defaults that make build checks
possible: a simulation core testable without rendering, a tuning file, an
event-driven juice layer, debug hotkeys, deterministic scenarios, direct GDScript
tests, and named-moment screenshots.

## Build checks

For `$build-check`, use direct tests for rules, `scripts/debug/run_scenario.py`
for scenario assertions and screenshots, and Movie Maker PNG sequences for motion
and juice. Commands are in [Windows commands](references/windows.md).

## Save and scope boundaries

Full game runs can access player saves. Use fixture-configured saves or an isolated
project identity for automation. Installation does not authorize publishing,
changing engine versions, choosing an art style, or adding a test framework.

## References by task

- Scene/resource operations and scenarios: [automation API](references/automation_api.md).
- Runtime failures: [debugging](references/debugging.md).
- Hand-edited scene/resource syntax: [text formats](references/tscn_format.md).
- GDScript guidance: [conventions](references/gdscript_conventions.md), applied to the
  current project rather than as a broad style rewrite.
- UI work: [UI reference](references/game_ui.md), within the approved art bible.
- Content integration: [asset pipeline](references/asset_pipeline.md), with recorded
  asset provenance.
- Export work when requested: [export targets](references/export_targets.md).
- Other helper examples: [upstream workflows](references/upstream-workflows.md).
  Paths there are relative to this skill root. Its mandatory template, playbook,
  style, and whole-project cleanup defaults are replaced by the work loop above.

For provenance, local patches, and upgrades, read `docs/godot-skill/README.md` in
the project. Keep the upstream revision pinned; review and retest updates before
replacing the installed files.
