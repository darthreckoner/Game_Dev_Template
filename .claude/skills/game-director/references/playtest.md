# Playtest

Human play is the acceptance evidence for fun, comprehension, and feel. Prepare a
session that shows what a new player understands without help. At the end of a
slice, the designer's own playtest always uses the sheet in "End-of-slice
playtest sheet" below.

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
## End-of-slice playtest sheet (designer, 2026-11-24)

Every end-of-slice playtest gets a fill-in HTML sheet, built from
`slice-playtest-sheet.html` beside this file. It puts every drive, every look and
every open decision on one page, with one-click answers, notes, autosave and an
answers file the Director reads back (first used on Backcountry Expedition,
2026-11-24: "I want this to become the standard moving forward for all end of
slice play tests").

1. Copy the shell to `docs/playtests/<date>-slice-playtest-sheet.html`. Edit only
   its `CONFIG`, `STOPS`, `PICKS` and `TAKEN` blocks and the setup list marked
   FILL; the layout, autosave and export stay as they are.
2. **Setup:** how to get the build and which launcher on which machine, the keys
   the designer needs, and the exact commit.
3. **Stops:** every open line of the end-of-slice drive list
   (`docs/playtests/end-of-slice-drive-list.md`, if the project keeps one) and
   every drive or look owed in `STATE.md`, grouped by place in the order that saves the most travel. Each
   item keeps the line's where, vehicle, range, what to try, and what scripts
   reported (marked as background, not a verdict), with pictures from
   `docs/captures/` where a look is judged.
4. **Decisions per drive:** each pending pick a drive settles (from the
   pending-picks file, `DESIGN.md` and the reviews) sits on that drive
   as one-click options. Mark today's setting or the Director's pick with ★.
5. **Whole slice:** the verdict, and the three things that felt flattest.
6. **Picks not tied to the drive,** at the bottom: each with its options, a
   gains/costs table, the Director's recommendation, and pictures or sounds
   wherever there is something to look at or hear. Held picks say so.
7. **Already taken for you:** the Director's provisional picks, each with a box
   to swap it.
8. Check every picture and sound path exists, open the sheet once, link the
   sheet from the drive list, commit and push it so every machine has it.
9. The designer saves `<date>-slice-playtest-answers.json` into
   `docs/playtests/`. The Director records every decision in its home in the
   same turn, tickets the findings, clears the answered drive-list lines and
   writes the verdict to `STATE.md` in the designer's words.
