# Process assumptions

Each part of this workflow compensates for a limitation that may not last. Review
this list at each `retro` and when switching models. Remove a part when evidence
shows it no longer earns its cost; restore it if the failure returns.

| Part | Compensates for | Evidence it still helps | Revisit when |
|---|---|---|---|
| Vision in files (`DESIGN.md`, build prompt) | Coding agents lose intent across sessions and compaction | Fresh coder sessions build to the design without re-explaining | Agents reliably keep intent across long sessions |
| One-shot first build; rebuild on big changes | Steering a drifted codebase costs more than regenerating it | Rebuilds that landed closer to the design than patches would have | Patches routinely fix drift cheaply |
| Fresh coder session per ticket | Long sessions accumulate stale context and drift | Tickets that land without carrying over earlier mistakes | Long sessions stop drifting |
| Role line at the top of every coder prompt | A Claude Code session reads `CLAUDE.md` and defaults to the Director role | Coder sessions that stayed in scope | The tool gains per-session role settings |
| Coder flags assumptions instead of asking | Stopping for every small gap stalls a one-shot build | Assumptions the designer accepted as-is | The designer rejects most flagged assumptions |
| Tuning file and event-driven juice layer | Feel is found by adjusting numbers and feedback, not rewriting rules | Feel fixes made through tuning or juice alone | — |
| Values, not adjectives; no model picks a visual value | Models default to a generic look; 2D graphics is the weakest task class in benchmarks (research, 2026-09) | Builds that matched the bible without a redo | A model matches a reference image unaided |
| Look checklist instead of a score | A single visual score hides broken interaction and invites optimizing the number (research, 2026-09) | Reviews whose failed items led straight to a fix | — |
| Separate Director reviews of a committed build | Builders grade their own output generously; live sessions make findings unattributable | Findings the coder missed, tied to a commit | Reviews find nothing actionable |
| Build checks: tests, scenarios, state dumps, screenshots | Canvas pixels are hard to assert; images hide rule bugs; the Director cannot play | Rule bugs caught by tests, visual issues by screenshot review | — |
| Commit before checking | Results about uncommitted work are not attributable | Findings traced to exact commits | Never; this is cheap |
| Ticket tiers and the escalation ladder | The strongest model is wasted on routine work; a cheap model stalls on hard tickets | Routine tickets landing on the cheaper model; escalations that resolved | One model does everything well at one price |
| Two rounds, then the designer decides | Review-and-fix loops run on without converging | Flat spots resolved in two rounds; loops stopped early | Loops converge reliably on their own |
| Friction log in `STATE.md` | Process problems are forgotten by the retro | Retro proposals traced to logged lines | — |
| File-based handoffs | Sessions share no memory; agents from different vendors share no channel | Tickets and reviews picked up without lost context | A verified shared channel exists |

Add rows when a retro introduces a new part.
