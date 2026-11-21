# Blender skills provenance

These project-local skills adapt
[patch-gg/cloud-blender-skills](https://github.com/patch-gg/cloud-blender-skills),
pinned to `d659b96ee43518693ec3e2ea5062211da43720b9` (2026-11-18). That repository
is a fork of [EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills)
1.3.2 with fixes and one added skill for Patch's paid cloud Blender. Both are
MIT; the upstream license is kept in each skill folder.
[upstream.json](upstream.json) records the upstream hash of every file.

## What was taken

Five of the 29 skills: `blender-core`, `blender-scene-setup`, `blender-asset-qa`,
`blender-game-optimization`, `blender-export-pipelines`. The designer chose this
set on 2026-11-21, with a list of the others for agents to draw on when a design
calls for them.

Left out on purpose: `blender-cloud` (paid, and upstream makes it the default
runner whenever its `pch` tool is installed) and the plugin and script
installers (they install all 29).

## What was changed

Against `upstream.json`, four files differ and one is new (checked 2026-11-21):

- `blender-core/scripts/run_in_blender.py`: cloud backend removed. Local Blender
  is the only backend; `--cloud` and `BAS_BACKEND=cloud` are refused with exit
  code 2; `--local` is accepted and ignored.
- `blender-core/SKILL.md`: description, routing table and Execute section
  rewritten for local Blender; routing lists the installed skills and points to
  the list of the rest.
- `blender-core/references/more-skills.md` (new): what each uninstalled skill
  does, when to add it, and how.
- `blender-asset-qa/SKILL.md`: added "Feeding the check", from the trial.
- `blender-export-pipelines/SKILL.md`: added the tangents gotcha, from the trial.

Everything else is byte-identical to upstream apart from line endings.

## Evidence

The trial that led to the kit, on Backcountry Expedition's Crowell Colt, and the
tool entry are in the Game Dev Library:
`C:\Dev\Game_Dev_Library\docs\tools\blender-skills.md` and
`C:\Dev\Game_Dev_Library\docs\research\2026-11-21-blender-skills-trial\`.

Kit check (2026-11-21, Windows 11, PowerShell 5.1, Blender 5.2.2 LTS, Python
3.14.7): the kit README's verify steps all passed on a scratch project.
Upstream's own suite passed 73 of 73 on the same machine before the changes
above; it was not rerun afterwards because the changed script is the host-side
runner, which the kit check exercises directly.

## Updating

Refresh from upstream only with a reason (a Blender version change, a needed
fix). Diff the new upstream files against `upstream.json`, reapply the changes
above, rerun the kit check, and update the pin here and in `more-skills.md`.
