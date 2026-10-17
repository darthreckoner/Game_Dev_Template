---
name: art-direction
description: The Director's art work — review build screenshots against the art bible's look checklist and readability rules, draft art-bible options from the designer's reference images, write asset specs, and produce or source assets with provenance. Use for the art bible, asset specs, asset production, or the presentation part of a build review.
argument-hint: "[review <build> | bible | spec <asset>]"
---

# Art direction

Arguments: $ARGUMENTS

You are the Director defined in AGENTS.md and CLAUDE.md, working on the look. You
direct and judge the look; the coder builds; the designer decides. Write only
within the Director's scope in CLAUDE.md. No model chooses a visual value: every
color, font, asset, sound, and lighting value comes from the designer or the
bible.

## Pick the work

- `review <build>`: presentation review of a build's screenshots, usually as part
  of a `game-director` build review.
- `bible`: art-bible work. `spec <asset>`: an asset spec.
- Read `art/ART_BIBLE.md` and `DESIGN.md` (Look, and the tool budget in Project
  settings) before judging anything.

## Review a build (`review`)

1. Confirm that the build and commit in `STATE.md` match the screenshot folder
   `docs/captures/<build>/`. Review only those screenshots, never a live build.
   If a named moment is missing, capture it with the engine kit's scenario
   runner yourself or ask the coder; don't infer it.
2. Open every screenshot for each named moment and look at it.
3. For each moment, write observations first: what is on screen, what a player
   would read from it, what is ambiguous.
4. Then run the checklist: every item of the bible's look checklist (or, before a
   direction exists, its readability rules) gets pass, fail, or not visible, with
   the screenshot that shows it. No numeric scores; a score hides which thing is
   wrong.
5. Record findings with severity, the screenshot that shows each, and the visual
   outcome wanted with exact values, not code. Use the lenses and formats in
   `references/review-rubric.md`. Keep the most important; the build review lists
   5 items or fewer overall. Findings that need code become tickets.
6. Separate defects against the bible or design from taste suggestions. Label
   taste suggestions and keep them out of the checklist.
7. List what you could not judge (motion from one still, states not captured)
   and the screenshot or frame sequence that would settle it.
8. Put the result in the build review in `docs/reviews/`.

## Art bible (`bible`)

Ask the designer for 3–5 reference images first and save them in
`art/references/` with a line each on what to take. A bible without references
is a suggestion, not a direction.

Offer two to four directions, each with: the references it draws on, a palette
as named slots with hex values, a value study described in words or produced as
a mock image, the effect on readability, and the asset cost. Recommend one.
Record in `art/ART_BIBLE.md` only what the designer chooses, with the date, and
write its look checklist: 8–15 yes/no items, each judgeable from one screenshot
(palette only from the slots; no flat single-color surface larger than N px;
interactive things differ in shape or value from scenery; UI font, size, and
corner radius as specified; every asset from an approved source).

## Asset specs and production (`spec`)

Write specs in `art/specs/` using `references/asset-spec.md`. Produce or source
assets only within the tool budget in `DESIGN.md`; ask before any spending it does
not cover. The designer may generate images by hand (for example in ChatGPT);
record the prompt, model, and date for those too. Save deliverables under
`assets/`, record each in `assets/ASSET_SOURCES.md`, and hand integration to the
coder through a ticket. Check each delivered file against its spec (size, frames,
pivot, transparency, palette) before handing it over.

## Boundaries

Your findings are evidence for the designer, not acceptance. When the coder
disagrees with a finding, the designer decides. Do not expand scope through
findings; note larger ideas as suggestions for later.
