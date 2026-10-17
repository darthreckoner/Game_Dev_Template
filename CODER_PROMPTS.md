# Coder prompts — start each in a FRESH session

Paste one into a new coder session with the model its seat names. The Director
says which to use. Each prompt opens by naming the role, so a Claude Code session
knows it is the coder, not the Director. In Claude Code the check skill is
`/build-check`; in Codex it is `$build-check` (run `tools/sync-codex-skills.ps1`
first).

## One-shot build
Seat: Opus 5.5.

You are the Coder for this project (roles in AGENTS.md). Read BUILD_PROMPT.md
and AGENTS.md. Build the complete first playable version exactly as specified.
Install the engine kit from kits/ as its README says. Run /build-check, update
STATE.md, and report what changed, what was checked, what is unverified,
your assumptions, and the exact delivery state.

## Iterate on a ticket
Seat: the model the ticket's tier names (AGENTS.md "Tickets").

You are the Coder for this project (roles in AGENTS.md). Read AGENTS.md,
DESIGN.md, STATE.md, then implement docs/tickets/[T-###-name].md and nothing
else. First restate the intended player feeling, list 3 ways to achieve it,
pick one, and build the smallest playable version. Touch only the files the
ticket allows; flag anything else. Run /build-check, update STATE.md, and
report.

## Juice pass
Seat: Sonnet 5.5.

You are the Coder for this project (roles in AGENTS.md). Read DESIGN.md and
STATE.md. Add juice to [mechanic] via the event layer only, using the timings
and values in the ticket or art bible. Aim for exaggerated, readable feedback.
Don't touch game logic. Run /build-check with frame sequences of the new
feedback, update STATE.md, and report.

## Rebuild
Seat: Opus 5.5.

You are the Coder for this project (roles in AGENTS.md). Read the updated
BUILD_PROMPT.md and AGENTS.md. Build a fresh version from scratch on branch
[rebuild-N]. Reuse old code only where it exactly matches the new spec. Run
/build-check, update STATE.md, and report.

## Chores
Seat: Haiku 5.5.

You are the Coder for this project (roles in AGENTS.md). Do only: [rename to
convention / format / move tunables into the tuning file / condense STATE.md to
under 8,000 characters keeping every open item]. Change no behavior. Run
/build-check if any code changed, and report.

## Drift check (any model, read-only)
You are a reviewer, not the coder. Compare the current build at commit [sha] to
DESIGN.md. List where it has drifted from the pillars, the anti-goals, or each
mechanic's intended feeling, with file and line. Don't fix anything.

## Second-opinion code review (any model, read-only)
You are a reviewer, not the coder. Read AGENTS.md, DESIGN.md, STATE.md, and
docs/tickets/[T-###-name].md (or BUILD_PROMPT.md for the first build). Review
commit [sha] against them: correctness bugs, hardcoded tunables, effects called
from game logic, tests whose expected values came from the implementation, and
drift from the pillars. Report findings with file and line, most severe first,
each with the fix you would make. Change nothing.

## Player critique (any model, read-only)
Play through [scenario] turn by turn in your head, or drive it with the engine
kit's scenario runner and read the state dumps. Where is it boring, confusing,
or unfair? What's the most memorable moment? Propose fixes, tuning-file changes
first. Change nothing.
