# Review rubric

## Anchored scale

- **0 Missing:** the expected element or state is not present in the screenshot.
- **1 Unusable:** present, but a player would misread it or fail because of it.
- **2 Confusing:** works, but with substantial hesitation or ambiguity.
- **3 Meets:** meets what this build set out to show.
- **4 Exceeds:** clearly better than this build needs.

Calibrate before scoring: in the first review for a project, write one sentence
for what a 2, a 3, and a 4 would look like for each moment. Reuse and refine those
anchors in later reviews so scores stay comparable across builds.

## Lenses (use those the moment calls for)

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
Observed: the last two cars overlap the track edge on the inner curve.
Why it matters: reads as derailment; DESIGN.md says cars follow the route.
Direction: cars should stay centered on the rail line through the curve; if art
changes are needed later, shorter car sprites would reduce overhang.
Confidence: medium — one still; a 5-frame sequence would confirm.
```
