---
name: evidence-run
description: Freeze a milestone candidate, run its gates (build, rules, scenarios, performance), capture the contract's review moments, write one evidence record, and file the art-direction request. Use when a milestone candidate is ready for judgment or a fix round needs rechecking.
---

# Evidence run

Produce evidence about one exact build. Do not fix anything during the run; fixes
happen afterwards and get a new run.

## Before running

- The milestone contract is approved. Read its criteria, scenarios, review moments,
  budgets, and round count, and `references/gates.md`.
- Commit the candidate. Evidence about uncommitted work is not attributable; if a
  commit is not authorized, stop and ask. Record the commit and engine version.
- Stop other builders and live-reload servers that could change the build or
  compete for the machine during performance checks.

## Run

1. **G0 Build:** import, launch smoke, parse check. Capture the error log.
2. **G1 Rules:** run the automated tests. Record counts and every failure.
3. **G2 Behavior:** run each contract scenario with its seed and scripted inputs.
   Assert expected state; save state dumps. Read runtime diagnostics too — passing
   assertions can hide unrelated script errors.
4. **Captures:** run the scenarios rendered at the contract's capture settings and
   save each review moment into `docs/evidence/<milestone>/<run_id>/captures/`,
   named `R<n>-<slug>.png`. Motion moments need a short frame sequence or several
   stills; the Art Director cannot watch video.
5. **G5 Performance:** only if the contract sets a budget; measure the fixed scenario
   on the stated device after warm-up.
6. Look at every capture yourself before filing it, to catch empty or wrong frames.

## Record and hand off

- Write `docs/evidence/<milestone>/<run_id>.md` from the template in
  `references/gates.md`. Never average gates; a G1 or G2 failure blocks acceptance.
- If presentation is in scope, file `docs/art-direction/requests/AD-###-…md` for
  this run (see `docs/art-direction/README.md`) and tell the user it is waiting.
- When the review arrives, copy its scores and finding ids into the record's G3/G4
  lines without rewording them, then decide fixes within the contract.
- Update continuity: run id, gate results, open request, next step.

## Fix rounds

Fix the highest-impact supported defects first, rerun the same scenarios under a
new run id, and link the previous record. Stop after the contract's round budget or
when the same defect ids persist, and ask the user how to proceed.
