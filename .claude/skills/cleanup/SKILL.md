---
name: cleanup
description: The Director's disk cleanup - survey what is taking space (finished worktrees, merged branches, stale scratch and backups), show the designer the full delete list, and only after their go dispatch a ticket that saves unsaved files before removing anything. Use when the designer asks to clean up, free disk space, or remove old worktrees, when the drive is running low, or in the weekly retro's straggler sweep.
---

# Cleanup

Every worktree is a full copy of the project's tracked files, so worktrees
that outlive their ticket are where the disk goes. The first run of this
process (Backcountry Expedition, 2026-11-27) found 62 worktrees holding
473 GB with 57 GB free, and freed about 410 GB without losing a file.

The Director surveys and sorts. The designer approves the list. A Coder
removes. Nothing is deleted before the designer's go.

## Order

1. **Check who is working.** List live sessions, and read the open tickets in
   `STATE.md`. A worktree with a live session, an open ticket, or a file or
   commit from the last 24 hours is kept (`AGENTS.md`, "Protect work and
   access").
2. **Survey.** Run the script; it reads only and can take several minutes:
   `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\cleanup\scripts\survey.ps1`
   It writes `worktrees.csv`, `branches.csv` and `folders.txt` to
   `work/cleanup-survey/`. Read `STATE.md` for worktrees it says to keep.
3. **Sort every worktree** into one group (table below). Open each row with
   `RealDirty` above 0 and name what the files are; do not guess from the count.
4. **Sort the folders.** Look at the largest entries in `work/`, untracked
   folders in the main checkout, and backups (`*.bak*`). For each, search the
   repository for its path (`git grep -F "work/<name>"`) to learn what made it
   and whether a tracked script or report still reads it.
5. **Show the designer the list** (format below) and stop for their answer.
   Record the answer in the ticket's Status line, in their words.
6. **Ticket and dispatch.** Write the ticket (below) and dispatch a Coder at
   the Standard tier in the main checkout. Tell the designer not to open the
   engine or start another session in the project until it finishes: a locked
   file makes the Coder skip that worktree.
7. **Review the report** against the ticket's Check line, push `main`, fold the
   result into `STATE.md`, and tell the designer the free space before and
   after.

## Sorting worktrees

| Group | Test | Action |
|---|---|---|
| A. Merged, nothing unsaved | `Merged` true, `RealDirty` 0 | Remove the worktree, `git branch -d` |
| B. Merged, tool leftovers | `Merged` true, `RealDirty` above 0, and every file is something a tool wrote (extracted textures, a test's rewritten output, an editor-rewritten resource) | Zip the leftovers, then as A |
| C. Not merged, nothing lost | `NotInMain` 0, or the ticket merged from another branch, or the worktree is clean and `OnRemote` shows its commits on the remote | Remove the worktree, keep the branch |
| D. Parked or stopped work | Unmerged, and the ticket is parked, stopped or held in `STATE.md` | Zip loose files, remove the worktree, keep the branch. Tell the designer when the branch exists only on this machine |
| Keep | Open ticket, live session, activity in the last 24 hours, named as a keep in `STATE.md`, the designer's current play build | Leave alone |

A worktree that fits no group is kept and shown to the designer as a question.

## What is never proposed

- Anything tracked in `main`, including evidence under `docs/captures/`. If
  tracked evidence is the problem, that is a separate question for the
  designer.
- Earlier cleanups' archives (`work/cleanup-*`).
- Player saves and source assets.
- Anything outside this repository and its worktrees. Mention large
  neighbours (another project's folder); do not put them in the ticket.
- Scratch that may not be rebuildable goes on the list as optional with
  default keep, with what it would cost to recreate.

## The list for the designer

One table: group, what it is in plain words, count, space, and what is kept
(branch, zip, remote). Then: optional items with a default, what is kept and
why, and the total freed against free space now. No hashes or folder IDs in
the reply; those live in the ticket.

## The ticket

It must carry:

- The method: record the starting state; for each worktree re-check HEAD and
  status against the ticket, zip every modified or untracked file that is not
  an import byproduct (and git-ignored logs and evidence) with the diffs as
  patches, verify the zip by SHA-256, write `preservation.json` under
  `work/cleanup-<date>/`, then `git worktree remove --force`.
- Each group with its folders and branches, and the loose files group D must
  capture, named one by one.
- The keep list and the never-delete list, by path.
- Stop rules: a moved HEAD, a file newer than the survey, unsaved files the
  ticket does not mention, or a locked file means skip and report. Never
  `git branch -D`, never force-push, never kill a process to free a file.
- An age guard on every rule-based group: no branch, worktree or folder
  created or changed in the last 24 hours is removed, and group lists are
  rebuilt at run time, not taken from the survey. (The first run deleted a
  branch made for a dispatch an hour earlier, because "merged, no worktree"
  matched it; it was restored at the same commit.)
- "Empty" folders are checked for files at run time; one that holds anything
  is skipped and reported.
- `main` may move forward during the run (the Director or another session
  commits); the run stops only if `main` is rewound or rewritten.
- The Check line: `main` HEAD unchanged or moved forward only, and the hashes
  of the main checkout's own modified and untracked files unchanged at the
  end; `git worktree list` shows only the kept set; `git fsck --no-dangling`
  clean; kept branches resolve to their recorded HEADs.
- Done when: a dated report under `docs/process/` listing what was removed
  (folder, branch, HEAD), what was preserved and where, what was skipped and
  why, free space before and after, and how to bring a checkout back.

While the Coder runs, new files the Director adds to the main checkout are
named to the Coder, so its end-state check leaves them out. New dispatches can
go ahead; the age guard protects their branches and worktrees.

## Afterwards

- A pile of merged worktrees means the merge step was skipped: one line in
  `docs/process/FRICTION_LOG.md` with the count and the dates.
- Whatever the run teaches goes into this skill and
  `docs/process/LESSONS_LEDGER.md`.

## Engine note

`scripts/survey.ps1` treats Godot's import byproducts (`*.import`, `*.uid`,
`.godot/`, `*.TMP`) as not unsaved work. For another engine, change the
`$byproduct` pattern at the top of the script.
