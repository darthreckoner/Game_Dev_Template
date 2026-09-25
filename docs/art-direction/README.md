# Art-direction handoffs

The orchestrator and the Art Director exchange work through files, so either can
start from a fresh session and the record survives. The orchestrator writes
requests; the Art Director writes reviews and updates the request status.

## Request: `requests/AD-###-short-slug.md`

```markdown
---
id: AD-001
status: open            # open | answered | withdrawn
type: review            # review | spec | bible | asset | question
milestone: M1
run_id: m1-2026-10-02-a # reviews only: the frozen evidence run
commit: <sha>           # reviews only
created: 2026-10-02
---

## Ask
One or two sentences: what decision this review or asset supports.

## Evidence
- docs/evidence/M1/m1-2026-10-02-a.md (record) and its captures/ folder
- Review moments: link to the contract section that names them

## Constraints
Contract scope, placeholder vs final art, budget, formats, deadlines.
```

Number requests sequentially. One ask per request; split unrelated asks.

## Review: `reviews/AD-###.md`

The Art Director follows `.claude/skills/art-direction/` and answers with:

- the request id, run id, and commit reviewed
- per review moment: observations first, then an anchored 0–4 score
- findings `AD-###-F1…`, each with severity (blocker, major, minor, polish),
  the capture that shows it, and a suggested direction (not code)
- anything that could not be judged from the evidence, and what capture would help

Then the Art Director sets the request's `status: answered`. The orchestrator
copies gate scores and finding ids into the evidence record, decides fixes within
the contract, and takes any disagreement about scope or taste to the user.

## Running the Art Director

**Manual (works without extra installs):** open Claude Code in the project folder
and ask it to process open art-direction requests. Tell the user a request is
waiting when you file one.

**Scripted (optional):** requires the Claude Code CLI installed and signed in on
this machine. The orchestrator may then run, with the user's approval for network
access from its sandbox:

```powershell
claude -p "/art-direction AD-001" --permission-mode dontAsk `
  --allowedTools "Read,Glob,Grep,Edit(docs/art-direction/**)"
```

Verify the command on the machine before relying on it, and record the result in
the project's README. Reviews never need write access outside `docs/art-direction/`.
