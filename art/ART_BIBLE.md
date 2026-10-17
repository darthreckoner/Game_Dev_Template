# Art bible

Owned by the Director as Art Director; every direction here is a choice the
designer approved. Proposals live in reviews until approved. Keep it short enough
to read before any review. No model chooses a visual value: what is not written
here is a placeholder, flagged, until the designer decides.

## Status

Placeholder phase: no visual direction chosen. Until then, apply only the
readability rules below, the placeholder palette, and the current build prompt
or ticket.

## Readability rules (apply in every phase)

- R1 The player's current goal, selection, and next valid action are visible at
  the gameplay camera distance without reading text.
- R2 Interactive and non-interactive elements differ in shape or value, not hue
  alone.
- R3 State changes that matter (loaded, damaged, delivered, blocked) have a
  visible signal that survives a grayscale check.
- R4 Text is legible at the target resolution and UI scale.

## Placeholder palette (until a direction is chosen)

Named slots the build prompt can cite. Replace the values when a direction is
approved; keep the slot names.

| Slot | Hex | Used for |
|---|---|---|
| background | #2B2B2B | play field |
| scenery | #5A5A5A | non-interactive shapes |
| interactive | #E8E8E8 | things the player can act on |
| player | #F2C14E | the player's avatar or selection |
| goal | #4EC9B0 | the current objective |
| danger | #D9534F | threats, failure states |
| ui-text | #FFFFFF on #1A1A1A | HUD and menus |

## References (the designer's choice)

Files in `art/references/`, one line each: what to take from it.

-

## Direction (after the designer chooses)

- Chosen on: [date]
- Look pillars (three):
- Camera, scale, and pixel or texel density:
- Palette: slots and hex values (replaces the placeholder table)
- Lighting as engine settings, not adjectives:
- Shape language and silhouettes:
- UI style: font, size, corner radius, outline, layout grid:
- Animation timing and feedback:
- Approved asset sources (packs, authors, generators):
- Do / don't:

## Look checklist (after the designer chooses)

8–15 yes/no items, each judgeable from one screenshot. Reviews mark every item
pass, fail, or not visible. Examples to adapt:

- L1 Every color on screen is one of the palette slots.
- L2 No flat single-color surface larger than [N] px without texture or value change.
- L3 Interactive things differ from scenery in shape or value (R2 holds).
- L4 UI uses the specified font, size, and corner radius.
- L5 Every asset on screen comes from an approved source in `assets/ASSET_SOURCES.md`.
- L6 Lighting values match the Direction section.
- L7 The silhouette of each type is distinguishable at gameplay distance.

## Asset specs

Index of specs under `art/specs/`, with status.

## Open visual choices

The overall style is not chosen.
