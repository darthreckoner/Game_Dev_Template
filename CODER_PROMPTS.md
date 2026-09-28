# Coder prompts (Codex / other agent) — start each in a FRESH session

Paste one into a new coder session. The Director says which to use.

## One-shot build
Read BUILD_PROMPT.md and AGENTS.md. Build the complete first playable
version exactly as specified. Run $build-check, then update STATE.md.

## Iterate on a ticket
Read AGENTS.md, DESIGN.md, STATE.md. Implement docs/tickets/[T-###-name].md.
First restate the intended player feeling, list 3 ways to achieve it,
pick one, and build the smallest playable version. Run $build-check and
update STATE.md.

## Juice pass
Read DESIGN.md. Add juice to [mechanic] via the event layer only.
Aim for exaggerated, readable feedback. Don't touch game logic.
Run $build-check with frame sequences of the new feedback.

## Drift check
Compare the current build to DESIGN.md. List where it has drifted from
the pillars, the anti-goals, or each mechanic's intended feeling. Don't fix
anything yet.

## Player critique
Play through [scenario] turn by turn in your head. Where is it boring,
confusing, or unfair? What's the most memorable moment? Propose fixes,
tuning-file changes first.

## Rebuild
Read the updated BUILD_PROMPT.md and AGENTS.md. Build a fresh version
from scratch on branch [rebuild-N]. Reuse old code only where it
exactly matches the new spec. Run $build-check and update STATE.md.
