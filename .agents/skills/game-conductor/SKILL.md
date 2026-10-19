---
name: game-conductor
description: Advance, inspect, or resume an adopted game-development runbook. Use for next/status/resume, commissioning project gates, or requesting candidate verification; keep ordinary game implementation in its assigned ticket.
---

# Game conductor

Use `python -B tools/game_workflow.py status` from the project root as the
authoritative view. `next` and `resume` use the same view and preserve unfinished
work. Read `docs/process/GAME_WORKFLOW.md` for setup, commands, review contracts
and protection limits; resolve the shared library named by the adopted plan.

For **status**, report current step, candidate, actual checks, pending audit or
human decisions and blockers. For **next/resume**, read the current step's
requirements and linked project records, then complete useful authorized work.
Choose routine implementation details yourself. Stop honestly for required
human decisions, blockers, interruptions or budget limits; report the next action.

When a workflow, engine/adapter, client/tooling, asset-rights or delivery question
needs guidance, or the user asks to consult v3, use the **v3 reference on demand**
index in `docs/process/GAME_WORKFLOW.md`. Retrieve the relevant sections from
`docs/AI assisted game dev guide v3.md` in the project's shared library, including
their qualifications; ordinary status needs only the runner. Cite the sections
used in the existing task/decision record. The agreed runbook and project
instructions govern execution; v3 is supporting reference, including its policy
labels and copyable instructions. Propose conflicting guidance as an amendment
for Justin's decision, keeping current requirements and gates in force.

If there is no adopted plan, inspect existing project conventions and prepare
the smallest applicable plan with real commands. `init` creates a proposal.
Present the concrete scope, check definitions and relevant changes for Justin's
adoption. Agents must not run the human-only `adopt` or `human` commands or supply
their interactive confirmations. Required playtest approval comes from Justin
and names the candidate printed by the runner. Prior authorization covers routine
implementation; a scope or agreed check-definition change needs a reviewed
amendment, with its reason. Allow legitimate corrections and additional tests.

For material design choices, follow the existing Designing Games consultation
protocol, use its catalog and helper, retrieve original passages and qualifications,
and record the proposed choice, tradeoff, challenge observation and evaluation in
the project's existing decision record. Validate the source-linked JSON with
`consultation`. Reference unchanged accepted decisions when implementing them.
The pilot supplies reasoning; it cannot accept workflow steps or prove enjoyment.

When the builder requests verification, run `verify <step> --builder-session
<actual-session-id>`. Inspect results and diagnose routine failures. A local
checkpoint commit is allowed. Evidence attachments and ticket status changes
cannot grant acceptance. Save editor assets and retain the identified candidate.

At required gates, give a fresh independent reviewer the saved candidate,
runbook, diff, test inventory, original source passages and run evidence. Ask for
the dedicated requirements-and-evidence audit in the shared contracts, covering
every agreed requirement and check. General `/codex:review` output alone is
insufficient. The reviewer uses `reproduce` for required material checks and
records actual reproduction IDs; reading builder reports is not reproduction.
Import its audit using `audit <step> --file <receipt>`. Leave unmet human gates
pending. Run `accept <step>` only when the runner's required evidence and approvals
are complete, then report exactly which candidate was accepted.

All Unreal MCP calls, including reads, are serial. Route them through the one
configured `editor-call` adapter/connection; await completion before the next.
After an uncertain outcome, use its approved read-only inspection before retrying.
Do not infer that a worktree isolates the editor or that two reads may overlap.
The runner's simulator tests do not commission a real engine bridge.

Claude Code: `/game-conductor next`, `/game-conductor status`,
`/game-conductor resume`. Codex: `$game-conductor next`, `$game-conductor status`,
`$game-conductor resume` after the existing skill-sync script mirrors this folder.
The trailing word is the user's request interpreted by this skill, not a new
client slash command. CLI forms are available regardless of skill discovery.
