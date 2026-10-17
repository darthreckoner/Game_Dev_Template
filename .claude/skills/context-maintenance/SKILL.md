---
name: context-maintenance
description: Audit or condense bloated startup context — STATE.md, duplicate summaries, stale pointers — while preserving decisions, open items, and evidence. Use when STATE.md passes 8,000 characters or a session start loads more than it needs, not for routine status updates or code cleanup.
---

# Context maintenance

Make project context easier to load without losing decisions or evidence. The
continuity file is `STATE.md`; the decisions file is `DESIGN.md`. History lives
in Git, so no separate archive is needed: commit before condensing.

## Scope the request

For an audit, inspect and report without changing files. For a cleanup, make the
bounded documentation changes below. A routine `STATE.md` update at the end of a
session does not need this procedure.

Identify what actually loads at session start (`AGENTS.md`, `CLAUDE.md`,
`DESIGN.md`, `STATE.md`, the prompt or ticket) and their character counts. If
context is already concise, say so and stop.

## Condense

1. Commit the current `STATE.md` so its exact bytes are recoverable.
2. Keep one continuity entry point. Aim for at most 8,000 characters in
   `STATE.md`. Do not move excess text into another document every session must
   read.
3. Keep visible: the current build and commit, what exists, the last checks and
   what was unverified, open assumptions, known issues, open tickets and reviews,
   the Friction log, next steps, and the designer's verdict. Distinguish accepted
   decisions from proposals, and implementation from checks and acceptance.
4. Drop resolved items and superseded statements, using evidence (a commit, a
   review, a verdict) to decide; age alone never closes an open item. Completed
   detail that still matters moves behind a link to the review, ticket, or commit
   that holds it.
5. Leave `DESIGN.md`, tickets, reviews, and playtest records in place. Their size
   alone does not justify rewriting them. If you find a conflict between files,
   preserve it and name the decision needed.

Limit edits to context documents; code, assets, saves, and global configuration
are outside this skill.

## Verify and report

Check that every open obligation still appears in `STATE.md`, that links resolve,
and that nothing in the startup path points at a removed file. Report changed
files, before and after character counts, what was dropped and where its
evidence lives, and the exact delivery state. Character reduction is not a
measured token saving; don't claim one.
