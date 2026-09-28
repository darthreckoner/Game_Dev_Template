# Process assumptions

Each part of this workflow compensates for a limitation that may not last. Review
this list at each `retro` and when switching models. Remove a part when evidence
shows it no longer earns its cost; restore it if the failure returns.

| Part | Compensates for | Evidence it still helps | Revisit when |
|---|---|---|---|
| Vision in files (`DESIGN.md`, build prompt) | Coding agents lose intent across sessions and compaction | Fresh coder sessions build to the design without re-explaining | Agents reliably keep intent across long sessions |
| One-shot first build; rebuild on big changes | Steering a drifted codebase costs more than regenerating it | Rebuilds that landed closer to the design than patches would have | Patches routinely fix drift cheaply |
| Fresh coder session per ticket | Long sessions accumulate stale context and drift | Tickets that land without carrying over earlier mistakes | Long sessions stop drifting |
| Coder flags assumptions instead of asking | Stopping for every small gap stalls a one-shot build | Assumptions the designer accepted as-is | The designer rejects most flagged assumptions |
| Tuning file and event-driven juice layer | Feel is found by adjusting numbers and feedback, not rewriting rules | Feel fixes made through tuning or juice alone | — |
| Separate Director reviews | Builders grade their own output generously | Findings the coder missed | Reviews find nothing actionable |
| Build checks: tests, scenarios, screenshots | Canvas pixels are hard to assert; images hide rule bugs; the Director cannot play | Rule bugs caught by tests, visual issues by screenshot review | — |
| Commit before checking | Results about uncommitted work are not attributable | Findings traced to exact commits | Never; this is cheap |
| File-based handoffs | No direct channel between Codex and Claude | Tickets and reviews picked up without lost context | A scripted channel is verified |

Add rows when a retro introduces a new part.
