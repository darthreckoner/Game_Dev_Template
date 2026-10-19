# Independent game-workflow requirements and evidence audit

Date: 2026-10-19. Reviewer: fresh `workflow_audit` agent context. This is tooling evidence, not Justin's acceptance or a game playtest.

**Current verdict after review round 2: pass for the documented local tooling scope.** The original P1 is independently reproduced as rejected on the fixed candidate. All 29 commissioning tests pass with normal Windows process access. Transitive invalidation, recovery, incomplete prerequisites, stale downstream audits and stale human approvals were additionally checked. No remaining blocking finding was established. Engine adapters, live skill dispatch and actual human experience retain the commissioning limits below.

Current audited immutable candidates:

- Template: `0799b6452b94fd16b2b440af3e70cc6ca570d118`.
- Library: `4878e8cf27513b90e904af0abe6311224b86f5d4`.

## Round 2: independent fix verification

The template delta from the initial candidate changes only the runner, its tests and tooling continuity. The library delta adds four contract lines describing prerequisite-run binding and downstream invalidation. I inspected both committed diffs and the actual assertions before running the checks; the implementer's supplied result was not substituted for reproduction.

The fix introduces [accepted_chain():344](C:/Dev/Game_Dev_Template/tools/game_workflow.py:344), which walks the approved dependency order and requires each completed step's latest verification to have a matching acceptance and the exact prerequisite run IDs. [verify():365](C:/Dev/Game_Dev_Template/tools/game_workflow.py:365) records those IDs. [evidence():492](C:/Dev/Game_Dev_Template/tools/game_workflow.py:492) checks the chain and recorded IDs before evidence can be audited, approved or accepted. Completion/status therefore cannot silently revive old dependent runs when a prerequisite gets a new acceptance. [CONTRACTS.md:113](C:/Dev/Game_Dev_Library/docs/game_workflow/CONTRACTS.md:113) now states this behavior explicitly. These locations refer to the fixed commits.

| Independently performed follow-up | Observed outcome |
| --- | --- |
| `python -B -X utf8 tools/test_game_workflow.py`, normal Windows process access | **29/29 pass**, 43.606 s, exit 0; installed Git Bash hook test included |
| Original two-step same-candidate failure sequence against immutable `0799b645...` source | `accept(second)` rejected with `Prerequisite acceptance superseded or incomplete`; neither step reported current acceptance |
| Three accepted steps, then a newer same-candidate failure of the root prerequisite | Both descendants rejected; all current-acceptance flags false; current step returns to the root; attempting downstream verification also blocked |
| Root restored, verified, audited and newly accepted | Only root completed; current step becomes `second`; old downstream evidence remains invalid |
| Attempted reuse of old downstream audit, acceptance and human-approval command after root recovery | Each rejected with `Prerequisite acceptance changed`; no silent revival |
| Fresh downstream verification and audit, with only the old run's simulated human approval present | Both dependent steps still rejected with `Justin's identified-build approval pending` until fresh simulated identified-run approval was supplied |
| Fresh verification, audit, simulated human approval and acceptance in dependency order | All three steps completed and reported current acceptance again |
| New root `verification_started` event with no finish, simulating an interrupted process/turn | Root rejected as interrupted/incomplete; both descendants rejected; all current flags false |
| `library-validate`, source-linked `consultation`, original pilot `validate` and `self-test` | All pass: 217 preserved guide blocks; `TOOLING-METHOD-001` valid; 415 pages, 10 principles, 54 references; all 10 pilot self-test cases pass |
| Whitespace checks of both fixed deltas | Both `git diff --check` commands pass |

The independent follow-up command is:

```powershell
python -B -X utf8 work/workflow-audit-2026-10-19/followup-probes.py
```

It extracts the exact fixed runner from Git and reuses the original independent disposable harness. Its [followup-probe-results.json](C:/Dev/Game_Dev_Template/work/workflow-audit-2026-10-19/followup-probe-results.json) records the observed states and rejection reasons. Human confirmations are explicitly simulated only in removed fixture repositories. The supplied new regression at [test_game_workflow.py:282](C:/Dev/Game_Dev_Template/tools/test_game_workflow.py:282) covers same-candidate failure and restored dependency runs; the independent probe additionally checks interruption and fresh human approvals.

No implementation was changed, and no repository commit or push was made by this audit. The prior report and immutable initial reproduction below are preserved as history. P1 is closed for the fixed commits; no third review round is requested. This passing tooling audit is evidence, not human adoption of a real project plan or acceptance of a game.

## Initial audit: preserved historical record

Initial audited immutable candidates:

- Template: `e06b893fa5326e2ff42cd8ef4784dadf7dd46391`, changes from its first parent.
- Library: `e5a0c478a9672d28d60dcd8dff8ad3154d314d44`, changes from its first parent.

**Initial verdict: revision required.** The 28 supplied commissioning tests pass with normal Windows process access. One additional independent reproduction demonstrates that a dependent step can be accepted after its prerequisite has a newer failed verification. No other material implementation defect was established in the initial audit. File/line locations in the historical sections below identify the initial commits. Round 2 above identifies the separate fixed candidates and verification.

## Initial blocking finding — closed in round 2

### P1 — Recheck prerequisite acceptance when accepting a dependent step

Locations: [tools/game_workflow.py:344](C:/Dev/Game_Dev_Template/tools/game_workflow.py:344), [tools/game_workflow.py:348](C:/Dev/Game_Dev_Template/tools/game_workflow.py:348), [tools/game_workflow.py:478](C:/Dev/Game_Dev_Template/tools/game_workflow.py:478), [tools/game_workflow.py:575](C:/Dev/Game_Dev_Template/tools/game_workflow.py:575), [tools/game_workflow.py:601](C:/Dev/Game_Dev_Template/tools/game_workflow.py:601).

`verify()` checks prerequisites once before starting a run. `evidence()`, `acceptance_errors()` and `accept()` do not recheck them. `completed_steps()` does remove a step when its newest verification has no matching acceptance, but it does not propagate that loss through accepted dependents.

Independent reproduction, using only disposable simulator files:

1. Adopt two steps, `second` requiring `first`.
2. Verify, audit and accept `first`.
3. Verify and audit `second`.
4. Rerun `first` with a deliberate assertion failure. The candidate ID remains identical. The latest verification is `failed`, and `first` is absent from `completed_steps()`.
5. Call `accept('second')`.

Observed: an `accepted` event is recorded for `second`; its `accepted_current_candidate` is `true`, while `status().current_step` is `first`. This is an acceptance-path defect, independent of the documented distinction between historical prerequisites and later source changes. A required check has been rerun and failed on the same saved candidate, yet the dependent acceptance still succeeds. A subsequent step could then use that dependent's completion as its prerequisite.

Consequence: the controller can report and extend acceptance past a known failed prerequisite. This conflicts with rejecting failed/incomplete required evidence and honoring the adopted dependency sequence.

Required correction: reject dependent evidence/acceptance when a prerequisite has a newer unaccepted, failed or incomplete run, and propagate the invalidation transitively through completion/status. Preserve historical records and the documented ability to build later candidates; do not require every earlier phase to match all later source bytes. Add same-candidate failure, incomplete-run and transitive-dependency regressions.

Reproduction command:

```powershell
python -B -X utf8 work/workflow-audit-2026-10-19/probes.py
```

The probe extracts the runner directly from immutable commit `e06b893...`, so subsequent working-tree fixes do not alter this finding. Inspect [probe-results.json](C:/Dev/Game_Dev_Template/work/workflow-audit-2026-10-19/probe-results.json) and [prerequisite-evidence.json](C:/Dev/Game_Dev_Template/work/workflow-audit-2026-10-19/prerequisite-evidence.json). The deliberately hidden failure flag is solely a fault injector in the disposable simulator, not a proposed project-input design or game verification.

## Initial independent checks

| Check performed | Observed result | Claim supported |
| --- | --- | --- |
| Branch, status, HEAD and both committed change inventories | Both candidates matched the specified commits at audit start; template clean; library retained pre-existing untracked `books/`, older guide and pilot | Exact review scope and preservation baseline |
| `python -B -X utf8 tools/test_game_workflow.py`, restricted sandbox | 28 executed; 27 passed; one hook test failed at Git Bash startup, `NtCreateDirectoryObject ... 0xC0000022`; 43.803 s | Environment failure isolated from the other checks |
| Same full command with bounded permission escalation for normal process access | **28/28 passed**, 36.133 s, exit 0 | Supplied commissioning suite, including installed hook command strings from a different working directory |
| Original `book_reference.py validate` | Pass: 415 pages, 10 principles, 54 source references | Existing pilot/reference integrity |
| Original `book_reference.py self-test` | All 10 cases pass, including deliberate source/citation/acceptance misclaims and restored pass | Pilot validator's stated negative controls |
| `python -B tools/game_workflow.py library-validate --library C:\Dev\Game_Dev_Library` | Pass; 217 blocks; preserved rendered guide and all manifest fingerprints match | Preserved guide, pilot and contract byte integrity |
| `python -B tools/game_workflow.py consultation docs/process/game-workflow-decision.json --library C:\Dev\Game_Dev_Library` | `TOOLING-METHOD-001` valid | Exact existing catalog IDs/references and record completeness |
| Independent guide-link enumeration | 178 unique valid source blocks linked by six runbook steps; 39 remaining blocks inspected | Source-link coverage, with qualifications below |
| Independent disposable checkpoint commit | Candidate ID unchanged; current acceptance retained | Content identity survives a checkpoint commit |
| Independent reproduction-log alteration | Rejected: `Reproduction evidence changed` | Independent evidence is revalidated at acceptance |
| Independent prerequisite failure probe | Dependent still accepted; repeated against the immutable runner | Blocking finding above |
| Committed diff whitespace check | `git diff --check e06b893^ e06b893` passes | Patch whitespace only |
| Local client/runtime inspection | Python 3.14.7; Codex CLI 0.163.0-alpha.10.2; Claude Code 2.1.228 | Actual installed version claims |
| Skill inspection | Claude/Codex conductor copies have identical SHA-256; Codex session exposes `game-conductor`; installed Claude help explicitly supports `/skill-name` | Discovery and syntax, not an end-to-end dispatched model turn |

The pilot commands above used `C:\Dev\Game_Dev_Library\docs\designing_games_pilot\tools\book_reference.py`. Tests created disposable repositories only under ignored `work/`; no game, existing save, real human approval or live editor was involved. The checkpoint commit occurred only in a temporary fixture repository, which was removed. No commit or push was made to either reviewed repository by this audit.

The 28 tests were inspected, not merely counted. Their failure matrix covers assertion failure, skipped/missing/duplicate/wrong IDs, stale attempt identity, incomplete completion, zero-exit raw engine diagnostics, structured diagnostics, timeout, nonzero exit, missing report/artifact and restoration to pass. Other tests exercise source/new-asset/deletion drift, protected definitions, external input pins, report/log/snapshot/capture alteration, missing/stale/self/incomplete audits, reproduction, human binding, ledger corruption, honest stops and the documented hook bypass. The suite had no multiple-step prerequisite invalidation regression, which explains why its pass does not cover the finding.

## Initial requirement coverage

| Requirement | Evidence and assessment |
| --- | --- |
| Preserve the exact revised guide; derive steps, prerequisites and evidence duties | [source/source_manifest.json](C:/Dev/Game_Dev_Library/docs/game_workflow/source/source_manifest.json), original 217 Page blocks and unchanged hashes, rendered guide equality, and [runbook.json:19](C:/Dev/Game_Dev_Library/docs/game_workflow/runbook.json:19). Covered as an unactivated source-linked starter. |
| Cover the guide's complete workflow without turning its example into generic game scope | Six steps cover profile/scope, workspace, harness, slice/recovery, experience, and delivery. Their requirements include target/performance conditions, production input, raw evidence, source review, rights/submission, packaging and human judgment. The 39 blocks without direct step links comprise six introductory blocks, 24 illustrative-example blocks, and nine copyable-instruction/brief blocks. Introductory duties and duplicate briefs are represented elsewhere; orb/gate/tower requirements remain explicitly illustrative. Project adoption still must state applicability reasons for actual omitted duties, as [CONTRACTS.md:10](C:/Dev/Game_Dev_Library/docs/game_workflow/CONTRACTS.md:10) requires. |
| Conductor next/status/resume with real client syntax | [GAME_WORKFLOW.md:3](C:/Dev/Game_Dev_Template/docs/process/GAME_WORKFLOW.md:3), identical skill copies and CLI dispatch. `/game-conductor <word>` and `$game-conductor <word>` are skill invocations, with the word interpreted by the skill. CLI fallback exists. Live model dispatch was not tested. |
| One acceptance owner; approved definitions separate from mutable execution | Adoption records complete definitions/protected hashes in the ledger; execution and acceptance events live in SQLite; the adopted file is rechecked. Skill and build-check delegate acceptance to the runner. Covered within the documented cooperative-local threat model. |
| Builder requests verification; tickets, dashboards and checkpoints do not accept | [game-conductor/SKILL.md:34](C:/Dev/Game_Dev_Template/.claude/skills/game-conductor/SKILL.md:34), runner commands and forged-dashboard test. Covered. |
| Bind evidence and approvals to saved source, assets, configuration and runner | Candidate ZIP/manifests include Git-visible saved bytes, deletions, new assets, plan/configuration, runner/Python identities and declared external hashes. Fresh run/attempt bindings and hashes are revalidated. Covered for declared saved inputs; unsaved editor state and undeclared/ignored external inputs remain explicit limits. |
| Reject stale, missing, skipped, failed, incomplete and mismatched required evidence | `check_errors()`, evidence hashes, audit/reproduction validation and failure matrix cover the individual run. **Initial dependency-level gap: P1 above; closed by independent round 2 verification.** |
| Honest blocker, human-input, interruption and budget stops | CLI stop reasons persist without acceptance; interrupted verification remains incomplete; Stop hook allows stopping. Covered. These controls record a stop; they do not authenticate intent or implement an automatic resource budget. |
| Protect agreed outcomes/checks while allowing reviewed corrections and new tests | `protected_outcomes`, `definition_files`, adoption reason and plan identity; correction/addition tests invalidate old acceptance and allow renewed verification. Covered for explicitly declared protected definitions. Completeness of that declaration requires plan review. |
| Local checkpoint commits remain separate from acceptance | Documentation plus independently reproduced content-identical checkpoint behavior. Covered. |
| Hooks enforce only tested paths and state their limitations | Actual installed Bash commands pass normal-process tests. Named Edit/Write/MultiEdit paths and direct Unreal names are guarded; Stop is nonblocking. Shell writes, alternate names/tools/clients, disabled hooks and same-user manual editing are explicitly admitted bypasses. Gate-time drift checks are tested. No untested Codex hook API is configured. Covered within those bounds. |
| Dedicated complete requirements-and-evidence audit | Every adopted step requires the special audit kind, matching bindings, full requirement/check inventory, distinct reviewer context, no blockers, and source-qualification declarations where applicable. Material reproduction uses actual runner records and validates their hashes. Ordinary `/codex:review` is explicitly insufficient. Covered structurally; honest semantic inspection remains the reviewer's duty. |
| Human decisions for scope/definition amendments; autonomous routine implementation | Human-only interactive adoption and skill instructions distinguish material amendments from routine work. Existing scope can be implemented autonomously. Covered as cooperative policy; terminal/session strings are not authenticated identity. |
| All Unreal MCP calls serial, including reads; shared connection and timeout reconciliation | Connection-keyed OS lock, shared check/editor queue, unknown marker, identity checks and required read-only reconciliation; four simulator cases cover cross-process reads, timeout-before-retry, shared verification/editor serialization and wrong identity. **Simulator commissioning only.** No live Unreal bridge or project adapter was available. |
| Only Justin approves required experience gates of identified builds | Human command prints candidate/run/questions, requires terminal confirmation and observations; acceptance matches run/candidate and actor. Starter experience/delivery have explicit human questions. Covered in simulated fixtures; no real approval was supplied. |
| Reuse the existing pilot; qualify author guidance; no duplicate book or automated fun claim | Original pilot/catalog/helper remain unchanged; source-linked consultation uses `DG-PROC-05`; no new book corpus is introduced. Protocol and contracts separate author advice, project adaptation, workflow acceptance and player observation. Covered. |

## Source interpretation and limits

I independently retrieved the tooling decision's original book pages with the existing helper: printed 321 (PDF 329), 366 (PDF 374) and 288 (PDF 296), then inspected the catalog's `DG-PROC-05` qualifications. These support adaptable knowledge creation, proportionate decision effort and longer planning horizons when established knowledge warrants them. They do not prescribe this runner, schema, ledger or hooks. The decision correctly labels those as project adaptations and preserves mandatory workflow duties and human experience judgment. No diagram or absent book figure was inferred.

The preserved guide was checked against its committed Page blocks and recorded checksums, not independently fetched a second time from the remote Page. This audit validates the requested committed source, not subsequent remote edits. The pre-existing untracked pilot, book directory and older guide were read where necessary and were neither edited nor staged.

No game adapter, renderer, normal-input playable route, performance target, packaged game, asset-rights inventory or actual human playtest was commissioned. Those are project gates described by the starter. Engine adapters must inspect native reports/logs, account for child processes, confirm the actual editor before mutation and pin their real dependencies; a simulator that echoes expected IDs does not establish those capabilities. No automated check proves enjoyment.

Local terminal confirmations, reviewer session strings, hook checks and SQLite hash chains are cooperative controls. The contracts explicitly exclude authenticated identity and resistance to a same-user adversary; this audit does not upgrade those claims. Skill discovery, help output and subprocess hook tests do not establish a live Claude/Codex model's successful dispatch and execution of the skill.

## Initial required follow-up — completed in round 2

The initial audit required correcting P1, adding multi-step failure/incompletion/transitive regression coverage, committing a new candidate, independently rerunning the affected checks plus the full tooling suite, and rechecking the original reproduction against the new implementation. Round 2 above completes that follow-up and identifies its exact commits. Neither round constitutes Justin's acceptance.
