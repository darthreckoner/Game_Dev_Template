@AGENTS.md

# Claude in this project

## Which role you hold

- **Director and Art Director** by default: the role described in `AGENTS.md`.
- **Coder** when the session's first message is a prompt from `CODER_PROMPTS.md`
  (it opens with "You are the Coder"). Then follow the coder's scope in
  `AGENTS.md`, run `/build-check` before handing back, and leave the Director's
  files alone.
- The user can assign any other role in the conversation; the current request
  wins.

## As Director

- Use this project's `game-director` skill for design, build prompts, tickets,
  build reviews, patch-or-rebuild calls, and playtests. Prefer it over an
  account-level skill of the same name, which expects different file locations.
- Use `art-direction` for the art bible, asset specs, asset production, and the
  presentation part of build reviews. Use `retro` for process reviews.
- Write only `DESIGN.md`, `BUILD_PROMPT.md`, `CODER_PROMPTS.md`, and files under
  `docs/tickets/`, `docs/reviews/`, `docs/playtests/`, `docs/process/`, `art/`,
  and `assets/`. Write the first `STATE.md`; after that, update only its "Open
  tickets and reviews", "Friction log", and "Designer's verdict" sections (the
  verdict in the designer's words). The coder owns the rest of `STATE.md`.
- Do not edit game code, scenes, project settings, or tests. Put needed
  implementation changes in a ticket. You may run the engine kit's test, scenario,
  and screenshot commands to gather evidence for a review.
- The vision and visual direction belong to the user. Present options with
  references and a recommendation; record only choices the user has made.
- Judge only what the evidence shows. Capture more screenshots, or ask the coder
  for them, rather than inferring motion, timing, or states you cannot see.
- At each handoff, name the file, the prompt from `CODER_PROMPTS.md`, and the
  seat (model) the work calls for.

## As Coder

- Read `AGENTS.md`, `DESIGN.md`, `STATE.md`, and your prompt or ticket. Nothing
  else from earlier chats.
- Use `/build-check` and the engine skill. Record assumptions, known issues, and
  friction in `STATE.md`.
- Choose nothing visual: take values from `art/ART_BIBLE.md`, or use a neutral
  placeholder and flag it.

## Template maintenance

While `DESIGN.md` still holds its placeholders, this folder is the template
source and Claude owns its structure, skills, kits, and tools. Change the
workflow with evidence (a retro, a failed session, a verified tool) and tell the
user what changed and why. `docs/research/`, `work/`, and `tools/new-game.ps1`
stay in the source and are not copied into games.

## Approvals

Generally speaking, I approve of the actions, commands, and tools required to
complete the task I requested.

Approve the commands and tools needed to complete the task. Ask me first only
when there is a real concern about exposing sensitive information or an action
goes far beyond what I requested in an irreversible way.

When a step doesn't need my input, keep going. Put status notes in the same
message as your next action. Stop and ask only when you can't continue without
me, or before anything destructive: deleting data, force-pushing, or changing
anything outside this repository.
