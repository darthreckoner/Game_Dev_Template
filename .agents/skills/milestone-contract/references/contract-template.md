# M<n> — <name>

Status: draft | approved (<who>, <date>) | closed
Brief: <link to the brief's milestone entry>

## Question

What this milestone must demonstrate, in one or two sentences.

## Scope

In: …
Out (deferred, not criteria): …

## Pass criteria

Each criterion is binary and names its verification (automated test, scenario
assertion, art review, human playtest).

| ID | Criterion | Verified by |
|---|---|---|
| C1 | … | test `…` |

A failure in any rules or behavior criterion blocks acceptance.

## Scenarios

| ID | Setup | Inputs | Expected state | Review moments captured |
|---|---|---|---|---|
| S1 | … | … | … | R1, R2 |

Scenarios are deterministic: fixed seed, fixed step, scripted inputs.

## Review moments (art direction)

| ID | Moment | What the Art Director judges | Expectation for this milestone |
|---|---|---|---|
| R1 | … | readability of … | meets rule … of the art bible |

Capture settings: resolution, UI scale, and frame sequence vs still.

## Budgets

Performance (device, scenario, frame-time limit) if relevant. Token/time budget
for the milestone. Paid generation: none unless listed with a limit.

## Rounds

Critique/fix rounds: 2 (default). After that, or when the same defects persist,
the orchestrator stops and asks the user.

## Human playtest

Who plays, the task given, what is observed. See `$playtest-kit`.

## Change log

- <date>: <change> — approved by <who>
