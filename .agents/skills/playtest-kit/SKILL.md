---
name: playtest-kit
description: Prepare and record a human playtest of a milestone build — the task given, a no-coaching observation script, an observation form, and follow-up questions. Use when a milestone is ready for the user or another person to play.
---

# Playtest kit

Human play is the acceptance evidence for fun, comprehension, and feel. Prepare a
session that shows what a new player understands without help.

## Prepare

- Build: the frozen candidate from the latest evidence run; note its commit.
- Task: one sentence from the contract's human-playtest section, stated as a goal
  ("deliver cargo to the east station"), not as instructions.
- Save state: a separate test save; never the player's real saves.
- Write the session file `docs/evidence/<milestone>/playtest-<date>-<tester>.md`
  from the form below. Give the user the observer script.

## Observer script

- Give the task, then stay quiet. Do not explain controls or rules unless the
  tester is stuck for two minutes or asks to stop; record every intervention.
- Ask the tester to think aloud. Note what they say they are trying to do.
- Note moments of hesitation, wrong guesses, surprise, and delight, with times.

## Observation form

```markdown
Build: <commit> · Tester: <who, prior familiarity> · Date: <date>
Task given: …
Completed: yes / no / with help · Time: …

| Time | What happened | What the tester said | Interpretation |
|---|---|---|---|

Interventions: …
After play: What was the game about? What was hardest? What did you want to do
that you couldn't? Would you play another round, and why?
Observer verdict (user only): accepted / not yet — reasons
```

## After

Summarize findings as defects or questions linked to the contract criteria. The
tester's opinions are data; the user's verdict is the acceptance decision.
