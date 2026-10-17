# Review rubric

## Look checklist, not scores

Once a direction is approved, `art/ART_BIBLE.md` carries a look checklist: 8–15
yes/no items, each judgeable from one screenshot. In a review every item gets
**pass**, **fail**, or **not visible**, with the screenshot that shows it. Before
a direction exists, the bible's readability rules are the checklist.

No numeric scores. A single score hides which thing is wrong and invites
optimizing the number; a failed item can be argued about and fixed.

Calibrate once per project: in the first review, write one sentence per item
describing what a pass looks like in this game, and reuse those sentences in
later reviews so verdicts stay comparable across builds.

## Lenses (for observations beyond the checklist)

- **Readability:** can the player tell what matters, what is interactive, and what
  state things are in, at gameplay distance and without reading text?
- **Hierarchy:** does the eye land on the goal and the player's agency first?
- **Value and color:** does the image still read in grayscale? Is meaning carried
  by hue alone anywhere (a colour-blind risk)?
- **Silhouette and scale:** are types distinguishable by shape? Is scale consistent?
- **Feedback:** does each important action or state change have a visible response?
- **Consistency:** does the moment follow the art bible and match earlier
  screenshots the designer approved?
- **UI:** legibility at target resolution, alignment, grouping, and whether UI
  obscures play.

## Severity

- **Blocker:** a player would fail or misunderstand a core action; fix before the
  next play session.
- **Major:** substantial confusion or a clear art-bible violation.
- **Minor:** noticeable but does not affect understanding.
- **Polish:** improvement beyond what this build needs.

## Finding format

```markdown
### F1 · major · curve-follow.png
Checklist item: L4 (moving things stay on their path) — fail
Observed: the last two cars overlap the track edge on the inner curve.
Why it matters: reads as derailment; DESIGN.md says cars follow the route.
Direction: cars stay centered on the rail line through the curve; if art
changes are needed later, car sprites 24 px instead of 32 px would cut overhang.
Confidence: medium — one still; a 5-frame sequence would confirm.
```

## Review document (`docs/reviews/<date>-<build>.md`)

```markdown
# Review — <build> (<commit>) — <date>
Round: 1 of 2 for <flat spot or ticket> · Screenshots: docs/captures/<build>/

## What this build set out to show
One line per named moment, from the build prompt or ticket.

## Moments
### <short-name>.png
Observed: …
Checklist: L1 pass · L2 fail · L3 not visible · R1 pass …

## Findings (most important first, 5 or fewer)
### F1 · <severity> · <screenshot>
…

## Assumptions for the designer
- <assumption> → accept into DESIGN.md / reject into a ticket

## Could not judge
- <what> — <the screenshot or frame sequence that would settle it>

## Next
- Tickets to write, each with its tier.
```
