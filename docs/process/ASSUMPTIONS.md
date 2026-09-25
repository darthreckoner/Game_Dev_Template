# Process assumptions

Each part of this workflow compensates for a limitation that may not last. Review
this list at each `$retro` and when switching models. Remove a part when evidence
shows it no longer earns its cost; restore it if the failure returns.

| Part | Compensates for | Evidence it still helps | Revisit when |
|---|---|---|---|
| Separate Art Director reviews | Builders grade their own output generously | Findings the builder missed | A milestone's reviews find nothing actionable |
| Contracts before building | Scope drift; untestable goals | Criteria that caught a regression or stopped creep | Contracts are routinely rewritten mid-build |
| Two-round fix budget | Critique loops plateau without converging | Round 3 would have changed the verdict | Defects keep closing in round 2 |
| Frozen candidates for review | Live dev builds make verdicts unattributable | Findings traced to exact commits | Never; this is cheap |
| File-based handoffs | No direct channel between Codex and Claude | Requests answered without lost context | A scripted channel is verified |
| State-based tests plus image review | Canvas pixels are hard to assert; images hide rule bugs | Rule bugs caught by tests, visual bugs by review | — |

Add rows when a retro introduces a new part.
