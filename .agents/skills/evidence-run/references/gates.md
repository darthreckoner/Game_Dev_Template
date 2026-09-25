# Gates and evidence record

| Gate | Evidence | Judge | Result |
|---|---|---|---|
| G0 Build | Import, launch, parse; error log | Script | pass / fail |
| G1 Rules | Automated tests on simulation rules | Script | pass / fail, counts |
| G2 Behavior | Scripted scenarios with state assertions | Script | pass / fail per scenario |
| G3 Presentation | Review-moment captures vs art bible and contract | Art Director | 0–4 per moment + findings |
| G4 UI readability | Captures of UI states; readability rules | Art Director | 0–4 per moment + findings |
| G5 Performance | Fixed scenario on the stated device | Script | within / over budget |
| G6 Play | Uncoached human playtest | User | accepted / not, with notes |

Scores are never averaged across gates. A G0–G2 failure blocks acceptance whatever
G3–G5 say. Only the user sets G6.

## Anchored 0–4 scale (G3, G4)

- **0 Missing:** the expected element or state is not present.
- **1 Unusable:** present, but a player would misread it or fail because of it.
- **2 Confusing:** works, but with substantial hesitation or ambiguity.
- **3 Meets:** meets this milestone's stated expectation.
- **4 Exceeds:** clearly better than the milestone needs.

Scores need written observations. A score without the observation behind it is
not evidence. Judge against the milestone's expectation, not final-game quality.

## Record template

```markdown
# <run_id>

Milestone: M<n> (<contract link>) · Follows: <previous run or none>
Commit: <sha> · Engine: <name version> · Device: <cpu/gpu/os, for G5>
Date: <date> · Operator: <agent/model>

| Gate | Result | Notes |
|---|---|---|
| G0 | pass | 0 errors, 2 known warnings (…) |
| G1 | pass | 14/14 |
| G2 | fail | S2 expected 1 delivery, got 2 (state dump: …) |
| G3 | pending AD-004 | |
| G4 | n/a | |
| G5 | n/a | |
| G6 | not played | |

## Defects
- <id>: <description> — evidence: <capture/dump/log line> — severity

## Captures
- R1-<slug>.png — <moment>, <settings>

## Unverified
What could not be checked and why.

## Human
played: no · accepted: — · notes: —
```
