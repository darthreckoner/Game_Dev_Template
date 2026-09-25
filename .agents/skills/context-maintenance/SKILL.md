---
name: context-maintenance
description: Audit or clean up bloated startup context, continuity notes, and duplicate project summaries while preserving source records and unresolved decisions. Use for requested context-maintenance work, not routine status updates or general code cleanup.
---

# Context maintenance

Make project context easier to load without losing decisions or evidence. Work
within the current repository or checkout and use repository-relative references.
Follow its approval, documentation, and delivery rules. This skill supplies a
procedure; it does not change authority or require a separate agent.

## Scope the request

For an audit or recommendation request, inspect and report without changing
project files. For a cleanup request, perform the bounded documentation changes
below. A routine continuity update does not need this full procedure.

Inspect applicable instructions, Git status when available, and the existing
continuity entry point. Identify the documents actually loaded at startup and
their character counts. Search larger records by topic; avoid loading all history.
Reuse existing paths and distinguish task-local scratch files from distributable
project records. If context is already concise, report that finding without
creating a replacement structure.

## Preserve before restructuring

Before condensing or relocating a document, preserve its exact current bytes,
including uncommitted content. Use the project's existing archive convention, or
a dated folder under `.agent/context-history/` when none exists. Record source
paths and matching SHA-256 hashes in a short archive index. Keep historical
snapshots outside the startup reading path and subject to existing privacy and
ignore rules. A prior commit is sufficient only if verified to contain the exact
current version; otherwise create the snapshot.

Capture source hashes before preparing changes and recheck them before replacing
files. If a source changed concurrently, incorporate the new state or pause that
file rather than overwriting the other work.

## Condense current context

Keep one authoritative continuity entry point. Aim for at most 8,000 characters
unless the project sets a different limit or preserving essential information
requires an explained exception. Other summaries should serve distinct purposes
and point to authoritative records. Do not relocate excess text into another
document every task must read.

Keep current priorities, active work, blockers, open decisions, pending approvals,
verification status, and next actions visible. Distinguish accepted decisions from
proposals or experiments, and implementation from testing and user acceptance.
Retain unknowns, source provenance, canonical paths, and material rationale. Use
evidence to identify superseded statements; age alone never closes an open item.

Move completed detail behind links. Prefer existing topic records; create a new
one only when it gives detailed live context a useful home. Each pointer must say
what it covers and when to read it. Preserve a concise section-to-destination map
so every original section remains recoverable. Material unresolved obligations
must be represented in current context, not discoverable only in an archive.

Keep canonical requirements, design records, business records, and governance
lifecycle artifacts in place. Their size alone does not justify rewriting them.
If maintenance reveals a semantic conflict, preserve it and identify the needed
decision. Limit edits to context documents and directly necessary loading
instructions; code, assets, user data, and global configuration are outside this
skill's cleanup scope.

## Verify and report

Check archive hashes, section coverage, references, current obligations, and the
final diff. Verify that the normal startup path avoids loading the archives. Run
checks appropriate to the changed documents and preserve repository-required
checks; cleanup alone is not a reason to run an application's full test suite.

Report changed files, before/after character counts, archive locations, checks,
remaining uncertainty, and exact delivery state. Do not equate character reduction
with measured token savings. Keep tool results to relevant findings and excerpts;
save full diagnostics in scratch files and narrow queries when output truncates.
