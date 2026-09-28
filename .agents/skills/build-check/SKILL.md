---
name: build-check
description: Check a finished build before handing it back — commit it, run rule tests and scripted scenarios, save screenshots of the named moments, and record results in STATE.md. Use at the end of a one-shot build, a ticket, a juice pass, or a rebuild.
---

# Build check

Give the Director and designer evidence about one exact build. Checks show that
rules and wiring work; they do not show the game is fun. Only the designer's play
decides that. Do not fix anything mid-check; fix afterwards and check again.

## Run

1. **Commit** the build as a local checkpoint so results point at an exact
   version. Record the commit and engine version in `STATE.md`.
2. **Build:** import, parse, and launch smoke. Read the error log; new errors are
   failures.
3. **Rules:** run the automated tests. Record counts and every failure.
4. **Scenarios:** run each scenario from `BUILD_PROMPT.md` or the ticket with its
   seed and scripted inputs, and assert the expected state. Read runtime
   diagnostics too; passing assertions can hide unrelated script errors.
5. **Screenshots:** capture each named moment at the stated resolution into
   `docs/captures/<build>/<short-name>.png`, where `<build>` is `v1`, `rebuild-2`,
   `T-004`, and so on. For motion and juice, save a short frame sequence or several
   stills; the Director cannot watch video. Keep full sequences in ignored
   `work/`. Look at every image yourself to catch empty or wrong frames.

The engine kit's skill (for example `$godot`) has the test, scenario, and capture
commands.

## Record

Update `STATE.md`: the Checks section (results, failures, the screenshots folder,
what could not be checked and why), then what exists, assumptions, known issues,
and next steps. For a ticket, set its status to done with the commit.

Never weaken or skip a failing check to get a pass. A failure is a known issue in
`STATE.md`, not something to hide.
