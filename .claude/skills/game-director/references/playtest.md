# Playtest

Human play is the acceptance evidence for fun, comprehension, and feel. Prepare a
session that shows what a new player understands without help.

## Prepare

- Build: the latest checked build in `STATE.md`; note its commit.
- Task: one sentence tied to the top fun risk or the ticket being tested, stated
  as a goal ("deliver cargo to the east station"), not as instructions.
- Save state: a separate test save; never the player's real saves.
- Write the session file `docs/playtests/<date>-<tester>.md` from the form below.
  Give the designer the observer script.

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
Designer's verdict (designer only): accepted / not yet — reasons
```

## After

Compare findings with the pillars and each mechanic's "Player should feel" line.
Turn defects into tickets and open questions into items for the designer. The
tester's opinions are data; the designer's verdict is the acceptance decision.
