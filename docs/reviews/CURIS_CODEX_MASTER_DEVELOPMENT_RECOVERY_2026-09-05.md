# CODEX MASTER DEVELOPMENT RECOVERY — 2026-09-05

Status: Review
Authority Class: REVIEW / EVIDENCE
Disposition: RECOVERED / IMPLEMENTED PARTIAL — STOP: DEFAULT APP DATABASE MUTATION INCIDENT
Owner: Codex Main Development Session
Source: CEO recovery instruction; current source; Git; WorkBuddy task records; named Meeting reviews
Next Gate: Final isolated packaged cloud E2E (CEO has accepted the recorded incident; historical audit verdict preserved below)

This report was established before any production-source modification in this recovery run. Historical test claims below are not new acceptance. No reset, clean, stash, merge, stage, commit, push or process termination was performed.

## CURRENT GIT TRUTH

- Actual cwd: `/Users/yy/Documents/Curis AI Workspace`; branch `main`.
- HEAD: `bb72916daba3ae9555914d03bdb7fcea9953ab9c`.
- `git status --porcelain=v1 -uall`: 1,387 entries = 118 unstaged modified + 2 unstaged deleted + 1,267 untracked files. Staged = 0. Untracked count includes evidence/prototypes; it is not a source-change count.
- Existing deletions: `docs/01_Product/Curis_Product_Master_Map_v2.0.md`, `docs/01_Product/Curis_Product_UI_Blueprint_v1.0.html`. Preserved, not restored or attributed to this recovery.
- One pre-existing stash on `feat/093-readonly-catalog-routes` remains untouched.
- 23 registered worktrees: main + 17 existing other worktrees + 5 missing `/private/tmp` registrations. No pruning.
- Existing other trees have normal-status entry counts: 95a9=6, 98d0=9, aeb0=15, shared-runtime-snapshot=0, d126=202, rd-current-root=2, rd-migration-dd77=0, rd-shared-runtime=2, ttk-current-root=2, ttk-shared-runtime=5, xhs-current-root=2, xhs-dd77=3, xhs-shared-runtime=5; four nested `.worktrees` = 1/2/0/0. These are `-unormal` counts, not comparable to main's `-uall` count.
- None of those 17 has `backend/app/meeting_service.py` or a Meeting-named dirty entry. Unmerged unrelated work exists; no evidence justifies importing it. No registered WorkBuddy-specific tree was found. WorkBuddy Meeting team config places all eight seats in this main cwd.
- Main Meeting service and two committed tests match current HEAD. Integration still depends on preserved untracked `backend/app/api/meeting_router.py`, other untracked shared modules and unstaged `main.py`/`database.py`/frontend seams. WorkBuddy commits do NOT establish a standalone clean-checkout product baseline.

## WORKBUDDY CHANGES

Git proves four commits since the previous Codex baseline `c797db840bad285d7e9f1962d06eac61aa28508b`:

| Commit | Source delta | Classification |
|---|---|---|
| `2be1d0ec1` | `desktop/src/lib.rs`: readiness timeout 45→90 seconds | KEEP source; fresh package validation outstanding |
| `225ae5b4a` | Adds previously untracked whole `meeting_service.py`, including pre-existing Codex core plus employee self-judgment and 30-call limit | KEEP core / PARTIAL closure; not all 1,431 added lines originated in WorkBuddy |
| `5e7c3656e` | Adds autonomous discussion and employee self-judgment tests | KEEP bounded regression, deterministic tests only |
| `bb72916da` | Checks budget again before speaker and Leader calls | KEEP; does not prove every call path is bounded |

Current mtime scan since 09-03 additionally identifies untracked edge tests and cloud driver; three 09-04 reviews, 09-03 master state, and `.workbuddy/memory/2026-09-03.md` / `2026-09-04.md`. mtimes identify candidates, not authorship. No evidence attributes older main.py/database.py/frontend mixed deltas to WorkBuddy.

WorkBuddy persistent sources inspected: repository memory; `~/.workbuddy/tasks/software-meeting-closure/{1..10}.json`; team config/runtime metadata. T1/T2/T8/T9/T10 are recorded completed; T3 Credential, T4 setup, T5 complete Meeting E2E, T6 restart and T7 final regression remain pending. Team runtime says active but seats are paused/completed, not proof of live execution. No team tasks were dispatched or altered.

| Additional artifact | Disposition |
|---|---|
| Master bootstrap 09-03 / env prep 09-04 | KEEP historical evidence; old processes/paths no longer current |
| Autonomy adjudication | DOC-ONLY historical pre-T8 analysis; does not describe current self-gate |
| Self-judgment design | DOC-ONLY design plus implemented subset; claim that gate creates no Work/Result contradicts `_run_employee`→canonical Child Work |
| `test_v1_meeting_self_judgment_edge.py` | KEEP untracked regression; preserve ownership |
| `backend/scripts/e2e_meeting_real_deepseek.py` | UNVERIFIED external headless report; CONFLICT with required credential/packaged acceptance procedure; do not run |

WorkBuddy already committed before recovery. No reset/rewrite of these commits is authorized. Remote publication during WorkBuddy is UNVERIFIED; this run has not contacted/pushed a remote.

## MEETING RUNTIME CURRENT TRUTH

Statuses distinguish source implementation from final live acceptance. Existing tests are locatable evidence, not a claim of rerun until the verification addendum.

| Capability | Truth | Actual path and evidence / limit |
|---|---|---|
| 1 Meeting identity | IMPLEMENTED | `MeetingService.create`; existing `strategy_meetings`; productization tests |
| 2 Participants | IMPLEMENTED | `_participants`, canonical employee_instances, same-company validation |
| 3 Conversation | IMPLEMENTED | same persisted timeline/conversation_id, `_save`; productization restart tests |
| 4 Leader orchestration | IMPLEMENTED | `_team_truth`, `_leader_prompt`, bounded outcome allowlist; autonomous tests |
| 5 Candidate evaluation | IMPLEMENTED | `_candidate_evaluation`: explainable deterministic secondary ordering |
| 6 Speaker selection | PARTIAL | self-nominated non-Leaders filtered then ranked; no round-robin; Leader is excluded from visible self-nomination |
| 7 Employee SPEAK/STAY_SILENT | PARTIAL | `_employee_self_judgment`→canonical Work/Task→same real execution bridge, not score-only; invalid boolean/coercion and terminal-round projection boundaries need verification |
| 8 Explicit @Employee | PARTIAL | add_message resolves canonical name; score +100, but self-silence can still filter the target and Leader is skipped; current test proves only willing non-Leader priority |
| 9 Leader-directed request | PARTIAL | requestedSpeakerRef persists, same filtered candidate path; not unconditional speaking |
| 10 Evidence | IMPLEMENTED | legal `_context`, bounded Knowledge/ref input, REQUEST_EVIDENCE and sync; not fabricated external research |
| 11 Proposal | IMPLEMENTED | Leader UPDATE_PROPOSAL saves ResultStore Artifact; existing deterministic canonical proof |
| 12 P7 Gate | IMPLEMENTED | one DECISION_PACKET, provenance normalization, high-risk Layer 1, WAITING_CEO |
| 13 Decision→Responsibility/Work | PARTIAL | GeneralWorkspaceDelivery with stable idempotency key; APPLIED-before-create failure recovery still requires precise recheck |
| 14 Result return | IMPLEMENTED | sync projects canonical routing refs into same timeline; linked Work execution exists |
| 15 No-progress stop | IMPLEMENTED | duplicate hashes/noProgress/maxTurns; all-silent round consumes event without a persisted turn-level silence record |
| 16 Provider-call budget | PARTIAL | 30 global Meeting counter; gate/response/Leader post-return increment; linked Work lacks pre-call check; exception/replay accounting needs recovery proof |
| 17 Token/cost budget | PARTIAL | 8,000 confirmed tokens / USD1 counter from Usage, unknown metering kept unknown; post-call limits, not guaranteed monetary cap or cancellation mid-call |
| 18 Concurrency/idempotency | PARTIAL | transactional active claim, stable release/execution keys; turn-interruption/close race and event replay need more than completed-turn proof |
| 19 Restart | PARTIAL | completed truth persists; stale claim becomes BLOCKED after elapsed threshold; not a process-liveness oracle |
| 20 CEO leave→background | IMPLEMENTED | router FastAPI BackgroundTasks owns run; UI polls GET every5s; no guarantee while backend is exited |
| 21 Real-cloud packaged E2E | UNVERIFIED | no surviving current packaged cloud full-chain evidence |

Runtime integration: `main.py:4931` execute_runtime_business / `team_employee:auto` validates identity/binding, creates one ResultStore Task with canonical workspace/work/execution refs, invokes Orchestrator, verifies callback. `main.py:5558` registers Meeting router. `database.py:1603–1619,6297–6450` extends the existing row. `model_gateway.py` / `ai_usage.py` remain the provider and single-ledger implementation. Frontend `meeting/page.js` consumes persistent API rather than generating employee replies.

## EMPLOYEE SPEAK / STAY SILENT STATUS

**Implemented production call path exists.** `_employee_self_judgment` uses `_run_employee(purpose='self-judgment', expected_type='meeting-self-judgment')`, canonical Child Work, assignment/binding, provider Task, verified callback, Result and Usage. A unit-test fake is not the production path.

Context includes role responsibility/key, current event, recent10 messages including other employees, selected refs (12), up to3 Knowledge excerpts, Proposal and Decision state. No whole-history hydration. Explicit current Employee Work projection is not assembled: Work/Result references can be present, but the design's claim of complete Current Work context is overstated.

Non-Leader employees can self-decline and re-enter on a later event. Ranking remains deterministic among eligible volunteers, which by itself is not round-robin. Identical model speaker sequences across two runs do not mathematically prove deterministic authority; judge persisted self-decisions and actual ordering inputs.

Current implementation excludes the Leader from this gate and from normal visible nomination. Latest CEO request says every Employee and explicit high-priority @ override; do not silently declare this edge accepted. No unrelated redesign or second identity is indicated.

## PROVIDER BUDGET STATUS

Actual `LIMITS`: maxProviderCalls30; maxTurns6; maxConsecutiveTurns1; maxNoProgress2; maxConfirmedTokens8000; maxConfirmedCost1.00; maxElapsedSeconds300. Existing meetings carry their saved `limits`, so new constant does not automatically migrate an old12-call meeting.

Gate, response and Leader normal returns each call `_merge_usage`. With Leader excluded, a three-participant meeting normally uses 2 gates+response+Leader=4 calls per round, not the comment's5. Linked post-Decision Work is merged but is executed before the turn-loop budget check. Exception handler reloads saved state, potentially losing in-flight increments; resuming cached tasks can also double-count if counters are not task-idempotent. These are concrete source risks, to reproduce before editing.

`maxElapsedSeconds` is checked between awaited operations; it is not an interrupt timer. Confirmed tokens and known cost are post-call observability/enforcement; unknown cost must not be presented as guaranteed budget safety. Do not raise limits further to force E2E success.

## REAL CLOUD MODEL STATUS

09-03 bootstrap recorded a configured isolated DeepSeek default `deepseek-v4-pro`, but had not executed the completion. 09-04 WorkBuddy memory/T10 reports headless `deepseek-chat` calls, speech/silence/re-intervention, counts5/10/10. The script is inspectable but its `/tmp/curis_e2e` database and `/tmp/curis_e2e_run4_*` logs are not present now.

The driver reads a deploy `.env` credential, injects a process environment secret and SQL-overrides model/gateway configuration; it is not the approved packaged Model Management→native Keychain route. This recovery neither reads that `.env` nor executes the script. Explicit CEO-message injection and scripted Decision choice in it are not autonomous evidence/CEO interaction proof. No raw credential logs were opened.

Thus: latest real completion is historically reported, independently UNVERIFIED; packaged health/discovery/default, 3+ cloud Employees, Evidence→Proposal→CEO leave→P7→Work→Result, full restart/no replay remain unproven. Earlier deterministic Browser/Desktop proof remains historical reusable evidence, not latest cloud acceptance.

## RUNNING INSTANCES

At recovery, listener/process inspection found no Curis/Workspace/Gateway/Guardian and no listeners on8002/8080/3010. WorkBuddy app/helpers exist; recorded paused/completed tasks are not running Curis evidence. No process was killed.

The named isolated roots `/private/tmp/curis-meeting-cloud-e2e.XbOY79`, `/private/tmp/curis-meeting-closure.YJn5C5`, `/private/tmp/curis_e2e` are absent. Do not resurrect their metadata or credentials by guess. Existing repo `.app` remains an artifact, not proof it contains T8/T9/latest changes; a fresh build is required.

## DATABASE SAFETY

Read-only SQLite integrity plus file hashing; no app/Runtime imports used for this inventory. No WAL/SHM present at these three paths.

| Absolute path | Bytes | mtime UTC | SHA-256 | integrity |
|---|---:|---|---|---|
| `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite` |1232896|2026-08-16T09:42:19.956Z|`2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`|ok|
| `/Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite` |1277952|2026-08-15T08:47:39.968Z|`a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`|ok|
| `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite` |1507328|2026-09-02T10:55:30.527Z|`80c8ff225cdd5fc90cc55516daf541f0d356d4edee6f77f987873ac3f5909c70`|ok|

These match the historical bootstrap fingerprints. That proves observed current byte/mtime agreement, not every intervening action. Absent isolated DBs have no current fingerprint; do not confuse them with default or repo DBs.

## CONFLICTS / RISKS

- `CURRENT_STATE`/Pointer/Backlog still say Meeting implementation pending; current Issue/Review/source prove implementation with incomplete cloud acceptance. Registration lag, not permission to discard code.
- `CLAUDE.md` is absent from repository root; no substitute third-party CLAUDE instructions consumed.
- WorkBuddy T10 summary overstates final acceptance; T3–T7 pending and missing packaged proof win the implementation evidence question.
- Design assertion “gate does not create Work/Result” conflicts with actual reuse of canonical execution; preserve canonical reuse, correct evidence description, do not invent a new call path.
- Raw cloud-driver credentials procedure is excluded. No secret extraction/relocation permitted to recover lost isolated metadata.
- Frozen product files are untouched. Current latest CEO instructions supersede old Issue deterministic-only phrasing; no need to create parallel authority.

### Pre-change source hashes (owned boundary)

| Path | SHA-256 |
|---|---|
| `backend/app/meeting_service.py` |`e0ab4102021e3acf94be9e8b694bf5672f3658e48b54b8fcb88f9e613dacc734`|
| `backend/app/api/meeting_router.py` |`4f84963ad2a44e950655c9a4b7cb082c2571ad114bac2556b2d2cd6bb9e60146`|
| `backend/app/database.py` |`4217798848d4308da84bdb0dc8fa67be9c43090ac832d81d0c1f067da454e65b`|
| `backend/app/main.py` |`e9b0de5b3919dda0946f845aee459b30c8688040d057bcc23908f77677d49299`|
| `frontend/app/ceo-office/meeting/page.js` |`999a393471a642f185c800c5c1c49b6c73f0cedbb8410ddda487f833b3753fea`|
| `backend/tests/test_v1_meeting_employee_self_judgment.py` |`ab8d551fe36baf6de227454ecb370f8624ada4f823b40de7cbfc58009b80a0ea`|
| `backend/tests/test_v1_meeting_self_judgment_edge.py` |`93385cb069542d168f00500eea5de7adeda851827b866af923f358d0571b3503`|

## EXACT REMAINING GAP

1. Verify/fix accepted bounded semantics: call budget on all Meeting execution paths; accounting on failure/restart; self-judgment/explicit request edges; no duplicate messages/Work/results after interrupted advancement.
2. Preserve valid T8/T9 implementation, rerun isolated focused/regressions, production build and fresh package. No deterministic provider is cloud acceptance.
3. Recover a legal isolated packaged model configuration through UI/Keychain; old isolated metadata is absent. If credential input is required, CEO alone supplies it in UI. No active/default DB writes.
4. Execute final full cloud chain and same-root restart, or retain PARTIAL with the exact unresolved gate.

## SAFE RESUME PLAN

Proceed in existing `CURIS-V1-MEETING-ROOM-PRODUCTIZATION-001`, not a new system. First run existing Meeting/self-gate/edge/DB safety tests with external SQLite and all three environment variables; capture results. Reproduce narrow source risks. Before any fix, amend existing Issue with exact Meeting service/test owned hunks and this pre-change record. No main/database/frontend/global Runtime modification unless an exact necessity is established and allowed.

Then bounded correction and regressions; build using existing declared local dependencies. Package must be newly built from current source; no default app launch or secret workaround. On real Authority conflict/unsafe data operation/credential gate, stop and report. Update this evidence record and existing Review with actual results; no commit/push.

Recovery verdict: CODEX MASTER DEVELOPMENT RECOVERED. Meeting Autonomous Discussion remains IMPLEMENTED / PARTIAL, not yet accepted.

## Recovery execution addendum — actual results, after the read-only report

### Bounded implementation and verification

Existing baseline regression: **19 passed** (Meeting base, autonomous, self-judgment, edge, DB Safety), external root `/private/tmp/curis-codex-meeting-recovery.uV2GlG` with all three DB variables aligned. No production import targeted repository/default databases.

Two newly reproduced failures, then minimum service fixes:

1. At providerCallCount30, an applied Decision still initiated two real canonical test-provider Tasks along the existing Work routing. Added budget check before each linked Work execution. Regression now proves zero calls and no result at exhausted budget.
2. A provider response with invalid JSON produced one Usage row but Meeting providerCallCount0 and an unclosed execution. Parse rejection now goes through existing failed execution finalization, retains usage and clears Current Executor. No model output is fabricated as accepted.

Owned implementation diff: `backend/app/meeting_service.py` 12 added /1 removed lines. New file: `backend/tests/test_v1_meeting_recovery.py`. Existing Issue amended before the fix; no shared primitive/Schema/main/frontend changes.

- New repro before fixes: **2 failed**, expected and retained under isolated `repro/`.
- New repro after fixes: **2 passed**, isolated `fix1/`.
- Combined Meeting / DB Safety / RD P7 / Team real-Employee / canonical Usage regression: **42 passed**, `regression/`, 21,411 existing FastAPI/Python deprecation warnings. Deterministic regression is not live external acceptance.
- Frontend Meeting tests: **2 passed**.
- Focused ESLint: PASS.
- Production Next build: PASS, 46 routes.
- Fresh PyInstaller Workspace/Gateway/Guardian/Recovery and Cargo/Tauri app build: PASS.
- Build log: `/private/tmp/curis-codex-meeting-recovery.uV2GlG/package-build.log`.
- Fresh app: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`.
- New native binary SHA-256: `fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d`.
- Owned tracked diff whitespace check: PASS. Separate standalone Python compile gate not run; Python code was imported by regressions and bundled by PyInstaller.
- No live cloud model was called by this recovery. No key was read or supplied by the agent.

### ACTIVE DEFAULT APP DB INCIDENT — STOP GATE

After the safe build, the agent called the native computer tool `cua.getApp` with the exact new app path to locate its window **before launching it with an isolated data-root environment**. The tool returned `timeoutReached` but automatically launched the application. The newly returned tool documentation states that getApp auto-launches applications. The launch therefore used the default App runtime root. This was an agent error, not a Provider failure or evidence of a Keychain bug.

The default database changed. This violates this task's active-DB boundary. Further Runtime/acceptance actions stopped immediately; subsequent operations were read-only fingerprint/count checks and this incident record. No attempt was made to restore a backup, delete data, clean the DB, or declare the incident accepted.

| Default database fingerprint | Before | After |
|---|---|---|
| Path | `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite` | same |
| Size | 1,507,328 | 1,536,000 |
| mtime UTC | 2026-09-02T10:55:30.527Z | 2026-09-05T13:28:01.473Z |
| SHA-256 | `80c8ff225cdd5fc90cc55516daf541f0d356d4edee6f77f987873ac3f5909c70` | `d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617` |
| integrity_check | ok | ok |

After-state has110 tables, companies1, employee_instances0, workspaces0, canonical_businesses0, runtime_entities0, strategy_meetings0, tasks0, artifacts0, ai_usage_records0, knowledge_entries0. **There is no current pre-launch row/schema snapshot**, only the recorded file fingerprint and historical bootstrap report. Therefore it is NOT valid to claim that every change was empty-schema initialization or that company data was unchanged. No irreversible rollback is authorized.

Both repository databases retain the exact preflight size, nanosecond-derived mtime and SHA, integrity_check=ok. Default App DB is a distinct third database and is NOT unchanged.

The launched native process was PID10820, with packaged sidecars. It was not killed because the user explicitly forbids killing a default instance. No additional UI interaction, model configuration, Meeting creation or cloud E2E was performed. The user should close this app; further scoped incident audit/remediation requires CEO direction. Build completed naturally with exit0; no build left running.

### Final current verdict and uncompleted gates

`CODEX MASTER DEVELOPMENT RECOVERED`

`MEETING AUTONOMOUS DISCUSSION: IMPLEMENTED / PARTIAL`

`MEETING ROOM: IMPLEMENTED / PARTIAL` (historical base accepted-candidate proof retained)

`CURRENT STOP GATE: DEFAULT APP DATABASE MUTATION — CEO REVIEW REQUIRED`

Remaining after this explicit stop: review default DB incident; resume remaining interrupted-turn/call-accounting/self-judgment edges; run new package in a confirmed external isolated root; CEO-configured native Keychain model; full3+ Employee cloud chain, Evidence/Proposal/leave/P7/Work/Result; full restart/no replay and final secret audit. Fresh build PASS must not be relabeled packaged E2E PASS. The two fixes close only their reproduced defects, not every recovery risk in the original matrix.

No stage/commit/push/reset/clean/stash/merge occurred. HEAD remains `bb72916daba3ae9555914d03bdb7fcea9953ab9c`; index remains empty. Previous unrelated work and WorkBuddy commits preserved.

Registration: this report is referenced by the existing Meeting Issue and Review. No Frozen Product Authority / Pointer / CURRENT_STATE broad rewrite was performed; the evidence does not authorize a new accepted implementation status.

STOP FOR CEO / CHATGPT CODEX MASTER DEVELOPMENT REVIEW.

## DEFAULT APP DB INCIDENT AUDIT

Status: Review  
Authority Class: REVIEW / EVIDENCE  
Audit date: 2026-09-05  
Disposition: **DEFAULT DB INCIDENT: DATA CHANGE UNKNOWN / NO SAFE ROLLBACK**  
Owner: Codex Main Development Session  
Source: CEO read-only incident instruction; stopped-process observation; SQLite read-only queries; dated WorkBuddy evidence; current packaged startup source.  
Next Gate: **STOP FOR CEO REVIEW**. This audit does not accept the incident and does not authorize resuming Meeting E2E.

### 1. Exit confirmation and audit method — PROVEN

Before the CEO's “已退出”, PID10820 and packaged guardians/workspace/gateway remained present, with8002/8080/3010 listening. After that message, a fresh `ps -axo pid,ppid,comm` filter and `lsof -nP -iTCP:8002 -iTCP:8080 -iTCP:3010 -sTCP:LISTEN` returned no matching process/listener. No process was killed by the agent. Default workspace error-log mtime is2026-09-05T13:38:27.289Z and includes shutdown records; these are supplementary, not a substitute for process verification.

All database inspection used native `sqlite3 -readonly`, SELECT and read-only PRAGMAs; no Curis Python module was imported, no Runtime opened, no app or provider launched. All three DBs had no `-wal` or `-shm` sidecars. Filesystem hashing used read-only Node buffers. No backup, SQL dump restoration, VACUUM, checkpoint, migration, insert, update, deletion or journal-mode change was executed.

### 2. Fingerprints and SQLite metadata

The default file remains the incident AFTER image; quitting did not restore the BEFORE image.

| Database | Bytes | mtime UTC | SHA-256 |
|---|---:|---|---|
| Default BEFORE (recorded, preimage not found) | 1507328 | 2026-09-02T10:55:30.527Z | `80c8ff225cdd5fc90cc55516daf541f0d356d4edee6f77f987873ac3f5909c70` |
| Default current | 1536000 | 2026-09-05T13:28:01.473Z | `d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617` |
| Repo `data/curis.sqlite` | 1232896 | 2026-08-16T09:42:19.956Z | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` |
| Repo `backend/data/curis.sqlite` | 1277952 | 2026-08-15T08:47:39.968Z | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` |

Absolute default path: `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite`. Repo paths above are under `/Users/yy/Documents/Curis AI Workspace/`.

All three `integrity_check` results = `ok`. Default `foreign_key_check` returned0 rows; repo `data/` returned0. Repo `backend/data/` returned12 violations, each child rowid2 referencing `tasks`, FK index0: artifacts, workflow_metrics, evolution_decisions, auto_workflows, development_strategies, meta_development_reports, tool_traces, workflows, workflow_traces, evolution_simulations, execution_scores, rollback_records. Because that file is byte-identical to the recorded pre-incident file, these violations are existing truth, not a new default-launch mutation. Integrity check does not mean referential integrity. No repair attempted.

| PRAGMA | Default current | Repo data | Repo backend/data |
|---|---:|---:|---:|
| user_version | 1 | 1 | 1 |
| application_id | 0 | 0 | 0 |
| schema_version | 315 | 246 | 237 |
| page_size | 4096 | 4096 | 4096 |
| page_count | 375 | 301 | 312 |
| freelist_count | 0 | 0 | 0 |
| journal_mode | delete | delete | delete |

Default size increased28672 bytes =7 current-size pages. That arithmetic does not identify individual writes. No pre-incident schema_version/page allocation map was found.

### 3. Historical evidence and snapshot search

1. `docs/04_Development/CURIS_MASTER_DEVELOPMENT_STATE_2026-09-03.md:62–73` explicitly records the BEFORE SHA,109 tables, companies1 (`Curis AI Company`, selfuse), employee_instances0, knowledge_entries0, workspaces0, departments0, strategy_meetings0. It also records tool_templates115, default_capability_definitions106, skill_templates55, workflow_contents36, workflow_templates18, employee_templates13, business_metrics9, department_types7, persona_templates6. These counts match current queries. This corrects the earlier report's overly broad “only fingerprint” statement: **partial pre-launch counts exist**, but no complete pre-launch schema/row-content image exists in the located evidence.
2. `docs/reviews/CURIS_V1_MEETING_CLOSURE_ENV_PREP_2026-09-04.md:24–28` independently records the same default BEFORE size/mtime/SHA and integrity. It does not supply a full schema or row dump.
3. `.workbuddy/memory/2026-09-03.md` repeats the shortened fingerprint; it is historical corroboration, not an independent binary snapshot.
4. Bounded search covered the default app root; repository docs, WorkBuddy memory, artifacts and named backup files; and existing `/private/tmp/curis*` roots matching meeting/backup/release/install (depth3, excluding app/build/dependency trees). No BEFORE-SHA binary or archive was located in that search. This is not a claim that no copy can exist anywhere on the machine.
5. `data/backups/curis-before-workspace-p0-guard-repair-20260816.sqlite` is1232896 bytes, SHA `ad350ba0a5634d0b75c3c4ef48ea1db23ccae620f603e7bbaf5e88109d2253ba`; it is a different repository incident, not this default DB preimage. `backend/tests/data/curis.sqlite` is also a different test DB. Existing recovery test SQLite files are isolated regression fixtures, not the default file's history; none may be substituted.
6. `CURIS_V1_RELEASE_DISTRIBUTION_RECOVERY_REVIEW.md` records an isolated backup/restore proof (103 tables,269 rows), not a backup of this109-table default image. No restore was attempted.
7. Current default logs were read only for metadata/startup-shutdown markers and sanitized HTTP method/path/status aggregates (no query values, headers, bodies or secrets). They contain historical accumulated GET traffic and no matching mutation HTTP method records. They are neither a SQL audit log nor an isolated incident-time request ledger; GET endpoints/startup can write, and absence of POST is not evidence of no DB mutation.

### 4. Current schema and changed-object truth

Current sqlite_master: **110 tables (including sqlite_sequence),185 indexes,8 triggers,0 views**. All SQL definitions were read and hashed. Ordered schema fingerprint `SHA256(JSON.stringify(rows))` over `SELECT type,name,tbl_name,rootpage,sql FROM sqlite_master ORDER BY type,name`:

`52c70df215dd94daafa9c53f664a942556a3091813477cc2e09a60c06ae0cbd0`

This is a reproducible current fingerprint, **not** a before/after schema diff.

| Candidate changed object | Current evidence | Classification |
|---|---|---|
| typed_object_references | Empty table, rootpage369; SQL matches database.py1119–1132 | LIKELY newly initialized |
| sqlite_autoindex_typed_object_references_1 / _2 | PK/unique indexes, rootpages370/371 | LIKELY new with table |
| idx_typed_object_references_source / target | Rootpages372/373; tenant-scoped source/target/relation indexes | LIKELY new with table |
| idx_knowledge_entries_canonical_target | Rootpage375; tenant/company/target/lifecycle/updated_at index | LIKELY newly initialized |
| knowledge_entries_referenced_no_delete | Present trigger blocks deleting referenced Knowledge; source database.py1138–1146 | Current existence PROVEN; historical addition UNKNOWN |
| Knowledge company_id/target_type/target_ref/lifecycle_status/archived_at columns | Current schema and _ensure_column path present at database.py1406–1415 | Current existence PROVEN; exact added-column delta UNKNOWN |

The old file size was368 pages at the current page size; current object roots369–375 and historical table count109→110 strongly support the Knowledge-reference initialization explanation. They do **not** prove a complete changed-object list: B-tree roots are allocation facts, not creation timestamps; no old sqlite_master exists here to rule out concurrent additions/deletions/rebuilds. Page374 cannot be assigned to an exact changed semantic object by this audit.

No new dated entry was found in `schema_migrations`: one row, version1, `integration-v1-schema-baseline`, applied2026-08-09 09:46:34. This does not prove no additive schema migration ran: most `_ensure_column`/CREATE paths are not separately journaled there.

### 5. Row truth, catalogs and credential metadata

**PROVEN current observations:**

- Companies1, same historically recorded name/tenant; current created_at and updated_at both2026-08-19 05:12:44. Historical count1 matches. Exact content equality of every Company field is UNKNOWN; it must not be claimed “no Company mutation”.
- Current Meeting rows0. Current Employee, Business, Workspace, Project, Task, Execution, Artifact, AI Usage, Knowledge and runtime_entities rows0. No persisted canonical Decision/Work/Responsibility/Result can be read from an empty runtime_entities table. A separate conversation-named table is absent in this schema; current Meeting and assistant identity rows are0. This does not prove those records were never changed or removed.
- Nine business_metrics rows exist, matching the historical count; their current updated_at is2026-08-19 05:13:50. Two evolution_events exist, both `business.metrics_computed`, dated2026-08-19. These are real pre-existing business/operating records, not grounds to call this database an “empty DB”.
- credential_metadata0; capability_connections0; capability_health_checks0; tenant_private_capabilities0; tenant_model_preferences0; platform_bootstrap_runs0. Current model_gateway credential_ref is NULL. These are metadata-only observations; macOS Keychain was not opened or inspected. No statement about secret deletion/preservation is inferred.
- Current model_gateways1 (`newapi`) and official_models1 (`official.openai.gpt-5.4-mini-2026-03-17`) have created_at2026-09-05 13:28:01. Official updated_at has that same time.
- All18 workflow_templates rows have updated_at2026-09-05 13:28:01.
- plan_free and plan_pro have updated_at2026-09-05 13:28:01; plan_enterprise retains2026-08-09 09:46:34.
- Default capability catalog releases5, definitions106 and migrations4 have dates in2026-08-11–13; version1.4.0 is ACTIVE, prior versions SUPERSEDED. Current migration rows are APPLIED. These old timestamps/counts are not cryptographic content equality.
- Launch-time timestamps corroborate real catalog/default refresh writes, **not just file metadata touch**. Prior exact row values are unavailable. No evidence proves a new Meeting/business execution took place; equally, the audit cannot certify no hidden historical row changes.

Complete current table counts are in Appendix A. Counts are not a substitute for before/after values.

### 6. Static startup path and likely mutation source

No source path below was executed by this audit.

| Source | Automatic behavior / boundary | Incident interpretation |
|---|---|---|
| desktop/src/lib.rs35–45,105–132 | Missing CURIS_DESKTOP_DATA_ROOT selects default app_data_dir; passes default DB to Workspace and CURIS_PRODUCT=workspace | Default-root path consistent with observed launch/process and changed file |
| desktop/runtime/backend_entry.py | Imports main.app, then runs Uvicorn | App import reaches create_app before user interaction |
| backend/app/main.py1005–1051 | Database.initialize, then _prune_product_private_data and _seed_r3_approved_model_catalog | Launch does more than read schema |
| backend/app/database.py226 onward | CREATE IF NOT EXISTS; indexes/triggers; _ensure_column; task/usage/domain compatibility paths and seed updates | Can modify an existing compatible DB, not just a new DB |
| database.py1119–1146,1406–1424 | Knowledge typed-reference table/indexes/trigger; canonical columns/index; task execution timestamp backfill | Best match to new-page objects; exact historical columns unknown |
| database.py1642 onward | Default tenant insert-or-ignore and department/model/employee/skill/workflow/asset/tool catalog seeding | Catalog existence and definition refresh; not Company/Employee instance creation |
| database.py2960–2970,3305–3321 | Workflow-template upserts update definitions/status/updated_at | Matches all18 launch-time updated_at values; content delta not recoverable |
| database.py1928–1935 | Overwrites Free/Pro price mirrors and updated_at on every initialization | Matches two Plan timestamps; previous prices unknown |
| main.py932–968 | Workspace prune deletes billing_events, dashboard_templates, dashboard_widget_catalog, model_gateways, official_models, platform_policies, pricing_rules, quota_rules; deletes non-allowlisted capability/company packages/templates | **Potential destructive startup scope exists**. Current zero/allowlisted rows do not prove what was deleted. No before row images for these tables |
| main.py971–1001 | Reseeds R3 gateway/model (credential_ref=NULL), updates model timestamp | Matches gateway/model creation timestamps; current code does not prove former catalog was identical |
| main.py4918–4924 / workspace_quickstart_api.py72–150 | Missing department type/template and employee TEMPLATE insert-or-ignore | Catalog seed, not a newly hired Employee |
| company_project_runtime.py18–24,218–241 | Constructor does not create Company; list_companies may ensure a default Company only if none exists | Historical Company already existed; no evidence of a newly created Company in this launch |
| runtime/foundation.py74–77 | Constructor stores DB reference; entity creation is command-driven | No basis to infer new Work/Decision on construction; entities currently0 |
| database.py2146–2189 | Version governance; old version<1 drops only empty retired tables; incompatible tasks schema can drop legacy task/execution tables | Such conditional branches exist. Prior complete schema/version missing; current intact version1 does not retrospectively establish every branch taken |

There is no startup SQL write journal with per-statement affected-row preimages. Matching timestamps and code are a strong causal explanation for schema/catalog refresh, but cannot bound **all** writes or exclude prune-related loss. No arbitrary restoration is safe.

### 7. Proven / likely / unknown and final decision

**PROVEN:** the default DB bytes changed in the erroneous launch; current integrity is ok; historical109 tables versus current110; partial historical counts match; current launch-time catalog timestamps; repository DB bytes are unchanged; app and ports exited before this audit; this audit performs no DB writes.

**LIKELY:** Knowledge-reference schema/index initialization accounts for much of the7-page increase; workflow/Plan refresh and Workspace prune+model seed explain launch-time rows.

**UNKNOWN:** exact changed schema list; all old row values; whether pruned catalog/policy/billing rows existed before startup; unchanged Company/business-metric contents; any overwritten/deleted data not present in current tables. No business data mutation has been positively identified from matched pre/post row evidence, so verdict C is not justified. “Only initialization” is not proved, so verdict A is also not justified.

**Final incident verdict: DEFAULT DB INCIDENT: DATA CHANGE UNKNOWN / NO SAFE ROLLBACK.**

Rollback recommendation: **NONE unless CEO explicitly authorizes**, with a validated source snapshot and separately reviewed scope. Do not replace this database with the repository backup or an isolated test DB. Incident acceptance is a CEO decision, not granted by this report.

This turn changes only this report. Existing implementation, WorkBuddy changes, tests and dirty/untracked files are preserved. No test run, production source change, app launch, cloud E2E, stage, commit or push. HEAD remains `bb72916daba3ae9555914d03bdb7fcea9953ab9c`; index empty. No Current Product Authority / Pointer / CURRENT_STATE rewrite; this remains an evidence addendum to the existing recovery record.

Final read-only recheck after writing this addendum: all three files match this audit's opening size, exact mtimeMs and SHA; all integrity checks remain `ok`, encoding `UTF-8`, no WAL/SHM files. The default matches the incident AFTER SHA, **not** its BEFORE SHA. No Curis process or listener on8002/8080/3010 reappeared. `database.py`, `main.py`, `meeting_service.py` hashes match pre-edit values. Index remains empty; Git status inventory hash is unchanged (`a0306cc299debb67c8ec38af108c7606721fb4e1a0178b289d71847f24721560`,119 modified/2 deleted/1269 untracked); an unchanged status inventory is not a claim that report contents are unchanged. No other file was edited by this audit.

### Appendix A — complete CURRENT table counts

| Table | Rows |
|---|---:|
| `ai_usage_records` | 0 |
| `architecture_locks` | 0 |
| `artifacts` | 0 |
| `assistant_identities` | 0 |
| `attributions` | 0 |
| `auto_workflows` | 0 |
| `billing_events` | 0 |
| `business_directions` | 0 |
| `business_metrics` | 9 |
| `cadences` | 0 |
| `canonical_businesses` | 0 |
| `capability_connections` | 0 |
| `capability_health_checks` | 0 |
| `capability_lessons` | 0 |
| `capability_packages` | 1 |
| `commitments` | 0 |
| `companies` | 1 |
| `company_department_state` | 0 |
| `company_package_workflow_bridges` | 1 |
| `company_packages` | 1 |
| `company_templates` | 1 |
| `content_publish_packages` | 0 |
| `content_workflow_runs` | 0 |
| `context_packages` | 0 |
| `credential_metadata` | 0 |
| `d1_execution_log` | 0 |
| `dashboard_templates` | 0 |
| `dashboard_widget_catalog` | 0 |
| `default_capability_catalog_migrations` | 4 |
| `default_capability_catalog_releases` | 5 |
| `default_capability_definitions` | 106 |
| `department_instances` | 0 |
| `department_observations` | 0 |
| `department_templates` | 3 |
| `department_type_status` | 0 |
| `department_types` | 7 |
| `departments` | 0 |
| `development_strategies` | 0 |
| `employee_affiliations` | 0 |
| `employee_capabilities` | 0 |
| `employee_capability_bindings` | 0 |
| `employee_instances` | 0 |
| `employee_skill_bindings` | 0 |
| `employee_templates` | 13 |
| `evolution_decisions` | 0 |
| `evolution_events` | 2 |
| `evolution_simulations` | 0 |
| `execution_patterns` | 0 |
| `execution_scores` | 0 |
| `executions` | 0 |
| `failure_logs` | 0 |
| `governance_proposals` | 0 |
| `guide_sessions` | 0 |
| `installed_workspace_packages` | 0 |
| `knowledge_entries` | 0 |
| `memory_entries` | 0 |
| `meta_development_reports` | 0 |
| `model_gateways` | 1 |
| `official_models` | 1 |
| `outcomes` | 0 |
| `persona_templates` | 6 |
| `plans` | 3 |
| `platform_bootstrap_runs` | 0 |
| `platform_policies` | 0 |
| `pricing_rules` | 0 |
| `projects` | 0 |
| `quota_rules` | 0 |
| `quotas` | 0 |
| `rollback_records` | 0 |
| `runtime_entities` | 0 |
| `runtime_links` | 0 |
| `runtime_simulation_runs` | 0 |
| `runtime_trace_event` | 0 |
| `runtime_transition_log` | 0 |
| `runtime_workspace_versions` | 0 |
| `scheduled_runs` | 0 |
| `schema_migrations` | 1 |
| `skill_templates` | 55 |
| `sqlite_sequence` | 1 |
| `step_assignments` | 0 |
| `step_results` | 0 |
| `strategy_meetings` | 0 |
| `system_evolution_log` | 0 |
| `system_settings` | 0 |
| `tasks` | 0 |
| `template_version_snapshots` | 0 |
| `tenant_department_activations` | 0 |
| `tenant_memberships` | 0 |
| `tenant_model_preferences` | 0 |
| `tenant_private_capabilities` | 0 |
| `tenants` | 1 |
| `tool_performance` | 0 |
| `tool_templates` | 115 |
| `tool_traces` | 0 |
| `tools` | 5 |
| `typed_object_references` | 0 |
| `workflow_contents` | 36 |
| `workflow_instances` | 0 |
| `workflow_metrics` | 0 |
| `workflow_runs` | 0 |
| `workflow_steps` | 0 |
| `workflow_templates` | 18 |
| `workflow_traces` | 0 |
| `workflows` | 0 |
| `workspace_package_activities` | 0 |
| `workspace_package_instances` | 0 |
| `workspace_package_lifecycle_events` | 0 |
| `workspace_package_migration_journal` | 0 |
| `workspace_package_objects` | 0 |
| `workspaces` | 0 |

### Appendix B — complete CURRENT index inventory

Includes SQLite-generated PK/unique indexes. Names prove current presence only; historical changed/unchanged classification remains unknown without the preimage. SQL definitions were included in the ordered schema fingerprint above.

| Parent table | Index names |
|---|---|
| `employee_affiliations` | `idx_aff_dept`, `idx_aff_proj`, `sqlite_autoindex_employee_affiliations_1`, `sqlite_autoindex_employee_affiliations_2` |
| `ai_usage_records` | `idx_ai_usage_tenant_company`, `idx_ai_usage_tenant_department`, `idx_ai_usage_tenant_occurred`, `idx_ai_usage_tenant_project`, `idx_ai_usage_tenant_work`, `idx_ai_usage_tenant_workspace`, `sqlite_autoindex_ai_usage_records_1`, `sqlite_autoindex_ai_usage_records_2` |
| `artifacts` | `idx_artifacts_tenant_task`, `sqlite_autoindex_artifacts_1`, `sqlite_autoindex_artifacts_2` |
| `billing_events` | `idx_billing_events_tenant_period`, `sqlite_autoindex_billing_events_1` |
| `canonical_businesses` | `idx_canonical_business_scope`, `sqlite_autoindex_canonical_businesses_1`, `sqlite_autoindex_canonical_businesses_2` |
| `capability_connections` | `idx_capability_connections_scope`, `sqlite_autoindex_capability_connections_1`, `sqlite_autoindex_capability_connections_2` |
| `capability_health_checks` | `idx_capability_health_connection`, `sqlite_autoindex_capability_health_checks_1` |
| `capability_lessons` | `idx_capability_lessons_signature` |
| `capability_packages` | `idx_capability_packages_availability`, `idx_capability_packages_status`, `sqlite_autoindex_capability_packages_1` |
| `companies` | `idx_companies_tenant_default`, `idx_companies_tenant_status`, `sqlite_autoindex_companies_1` |
| `context_packages` | `idx_context_packages_tenant_task`, `sqlite_autoindex_context_packages_1` |
| `content_publish_packages` | `idx_cpp_tenant`, `sqlite_autoindex_content_publish_packages_1` |
| `company_package_workflow_bridges` | `idx_cpw_bridge_resolution`, `sqlite_autoindex_company_package_workflow_bridges_1`, `sqlite_autoindex_company_package_workflow_bridges_2` |
| `content_workflow_runs` | `idx_cwr_tenant`, `sqlite_autoindex_content_workflow_runs_1` |
| `default_capability_definitions` | `idx_default_capability_defs_release`, `sqlite_autoindex_default_capability_definitions_1`, `sqlite_autoindex_default_capability_definitions_2` |
| `default_capability_catalog_releases` | `idx_default_catalog_one_active`, `sqlite_autoindex_default_capability_catalog_releases_1`, `sqlite_autoindex_default_capability_catalog_releases_2` |
| `employee_capabilities` | `idx_employee_capabilities_tenant`, `sqlite_autoindex_employee_capabilities_1` |
| `guide_sessions` | `idx_guide_sessions_tenant`, `sqlite_autoindex_guide_sessions_1` |
| `knowledge_entries` | `idx_knowledge_entries_canonical_target`, `idx_knowledge_entries_local_source`, `idx_knowledge_entries_tenant_updated`, `idx_knowledge_entries_tenant_workspace`, `sqlite_autoindex_knowledge_entries_1` |
| `memory_entries` | `idx_memory_entries_employee`, `idx_memory_entries_project`, `idx_memory_entries_runtime_source`, `idx_memory_entries_tenant_type_updated`, `sqlite_autoindex_memory_entries_1` |
| `model_gateways` | `idx_model_gateways_status`, `sqlite_autoindex_model_gateways_1` |
| `official_models` | `idx_official_models_type_status`, `sqlite_autoindex_official_models_1` |
| `plans` | `idx_plans_code`, `sqlite_autoindex_plans_1`, `sqlite_autoindex_plans_2` |
| `pricing_rules` | `idx_pricing_rules_plan_status`, `idx_pricing_rules_subject`, `sqlite_autoindex_pricing_rules_1` |
| `projects` | `idx_projects_tenant_company_status`, `sqlite_autoindex_projects_1` |
| `quota_rules` | `idx_quota_rules_plan`, `idx_quota_rules_plan_type_active`, `idx_quota_rules_status`, `sqlite_autoindex_quota_rules_1` |
| `quotas` | `idx_quotas_tenant`, `sqlite_autoindex_quotas_1` |
| `runtime_transition_log` | `idx_rtl_at`, `idx_rtl_entity` |
| `scheduled_runs` | `idx_runs_biz_status`, `idx_runs_cadence`, `sqlite_autoindex_scheduled_runs_1` |
| `runtime_entities` | `idx_runtime_entities_scope`, `idx_runtime_launch_check_version`, `idx_runtime_one_agent_runtime_profile`, `idx_runtime_one_ceo_assistant`, `idx_runtime_one_execution_exception`, `idx_runtime_one_local_ceo_profile`, `idx_runtime_one_welcome_brief`, `idx_runtime_one_workspace_capability_gap`, `sqlite_autoindex_runtime_entities_1` |
| `runtime_links` | `idx_runtime_links_source`, `idx_runtime_links_target`, `sqlite_autoindex_runtime_links_1`, `sqlite_autoindex_runtime_links_2` |
| `runtime_simulation_runs` | `idx_runtime_simulation_scope`, `sqlite_autoindex_runtime_simulation_runs_1` |
| `runtime_trace_event` | `idx_runtime_trace_run`, `sqlite_autoindex_runtime_trace_event_1` |
| `strategy_meetings` | `idx_sm_tenant`, `sqlite_autoindex_strategy_meetings_1` |
| `tenant_memberships` | `idx_tenant_memberships_lookup`, `sqlite_autoindex_tenant_memberships_1`, `sqlite_autoindex_tenant_memberships_2` |
| `template_version_snapshots` | `idx_tvs_instance`, `idx_tvs_template`, `sqlite_autoindex_template_version_snapshots_1` |
| `typed_object_references` | `idx_typed_object_references_source`, `idx_typed_object_references_target`, `sqlite_autoindex_typed_object_references_1`, `sqlite_autoindex_typed_object_references_2` |
| `workspace_package_activities` | `idx_workspace_package_activities_scope`, `sqlite_autoindex_workspace_package_activities_1` |
| `workspace_package_lifecycle_events` | `idx_workspace_package_lifecycle_scope`, `sqlite_autoindex_workspace_package_lifecycle_events_1` |
| `workspace_package_migration_journal` | `idx_workspace_package_migration_scope`, `sqlite_autoindex_workspace_package_migration_journal_1` |
| `workspace_package_objects` | `idx_workspace_package_objects_scope`, `sqlite_autoindex_workspace_package_objects_1` |
| `architecture_locks` | `sqlite_autoindex_architecture_locks_1` |
| `assistant_identities` | `sqlite_autoindex_assistant_identities_1` |
| `attributions` | `sqlite_autoindex_attributions_1` |
| `auto_workflows` | `sqlite_autoindex_auto_workflows_1` |
| `business_directions` | `sqlite_autoindex_business_directions_1` |
| `business_metrics` | `sqlite_autoindex_business_metrics_1`, `uq_business_metrics` |
| `cadences` | `sqlite_autoindex_cadences_1` |
| `commitments` | `sqlite_autoindex_commitments_1` |
| `company_department_state` | `sqlite_autoindex_company_department_state_1` |
| `company_packages` | `sqlite_autoindex_company_packages_1` |
| `company_templates` | `sqlite_autoindex_company_templates_1` |
| `credential_metadata` | `sqlite_autoindex_credential_metadata_1` |
| `dashboard_templates` | `sqlite_autoindex_dashboard_templates_1` |
| `dashboard_widget_catalog` | `sqlite_autoindex_dashboard_widget_catalog_1` |
| `default_capability_catalog_migrations` | `sqlite_autoindex_default_capability_catalog_migrations_1` |
| `department_instances` | `sqlite_autoindex_department_instances_1` |
| `department_observations` | `sqlite_autoindex_department_observations_1` |
| `department_templates` | `sqlite_autoindex_department_templates_1` |
| `department_type_status` | `sqlite_autoindex_department_type_status_1` |
| `department_types` | `sqlite_autoindex_department_types_1` |
| `departments` | `sqlite_autoindex_departments_1` |
| `employee_capability_bindings` | `sqlite_autoindex_employee_capability_bindings_1`, `sqlite_autoindex_employee_capability_bindings_2` |
| `employee_instances` | `sqlite_autoindex_employee_instances_1` |
| `employee_skill_bindings` | `sqlite_autoindex_employee_skill_bindings_1`, `sqlite_autoindex_employee_skill_bindings_2` |
| `employee_templates` | `sqlite_autoindex_employee_templates_1` |
| `governance_proposals` | `sqlite_autoindex_governance_proposals_1` |
| `installed_workspace_packages` | `sqlite_autoindex_installed_workspace_packages_1` |
| `outcomes` | `sqlite_autoindex_outcomes_1` |
| `persona_templates` | `sqlite_autoindex_persona_templates_1` |
| `platform_bootstrap_runs` | `sqlite_autoindex_platform_bootstrap_runs_1`, `sqlite_autoindex_platform_bootstrap_runs_2` |
| `platform_policies` | `sqlite_autoindex_platform_policies_1`, `sqlite_autoindex_platform_policies_2` |
| `runtime_workspace_versions` | `sqlite_autoindex_runtime_workspace_versions_1`, `sqlite_autoindex_runtime_workspace_versions_2` |
| `schema_migrations` | `sqlite_autoindex_schema_migrations_1` |
| `skill_templates` | `sqlite_autoindex_skill_templates_1`, `sqlite_autoindex_skill_templates_2` |
| `step_assignments` | `sqlite_autoindex_step_assignments_1` |
| `step_results` | `sqlite_autoindex_step_results_1` |
| `system_settings` | `sqlite_autoindex_system_settings_1` |
| `tasks` | `sqlite_autoindex_tasks_1` |
| `tenant_department_activations` | `sqlite_autoindex_tenant_department_activations_1` |
| `tenant_model_preferences` | `sqlite_autoindex_tenant_model_preferences_1` |
| `tenant_private_capabilities` | `sqlite_autoindex_tenant_private_capabilities_1` |
| `tenants` | `sqlite_autoindex_tenants_1` |
| `tool_performance` | `sqlite_autoindex_tool_performance_1` |
| `tool_templates` | `sqlite_autoindex_tool_templates_1`, `sqlite_autoindex_tool_templates_2` |
| `tools` | `sqlite_autoindex_tools_1` |
| `workflow_contents` | `sqlite_autoindex_workflow_contents_1` |
| `workflow_instances` | `sqlite_autoindex_workflow_instances_1` |
| `workflow_runs` | `sqlite_autoindex_workflow_runs_1` |
| `workflow_steps` | `sqlite_autoindex_workflow_steps_1`, `sqlite_autoindex_workflow_steps_2` |
| `workflow_templates` | `sqlite_autoindex_workflow_templates_1` |
| `workflows` | `sqlite_autoindex_workflows_1` |
| `workspace_package_instances` | `sqlite_autoindex_workspace_package_instances_1`, `sqlite_autoindex_workspace_package_instances_2`, `sqlite_autoindex_workspace_package_instances_3` |
| `workspaces` | `sqlite_autoindex_workspaces_1` |

### Appendix C — CURRENT triggers and SQL fingerprints

| Trigger | Parent | SHA-256 of sqlite_master.sql |
|---|---|---|
| `ai_usage_records_no_delete` | `ai_usage_records` | `237fd7203d244edb018b5723d121006043c96fa4f35f25c95c8a05c344ef8754` |
| `ai_usage_records_no_update` | `ai_usage_records` | `4c7f7bbcd074c39987f9c8a023e2e4508d491111d62a84cefbd22e52d5cb0839` |
| `knowledge_entries_referenced_no_delete` | `knowledge_entries` | `4a9df24c244e59c5edd891dcf82941569a72cf4dd8825ae5aa2aa1d6de6f2a84` |
| `trg_canonical_business_delete_guard` | `canonical_businesses` | `d284b19ecf11b25b125c510bcdc39f7640c980cfd4f683d831eb2b747db29eda` |
| `trg_canonical_business_parent_insert` | `canonical_businesses` | `ee6256850364ffc66fc5dab69b2012cec66f1c2362f7da778c447ba86cf67e92` |
| `trg_canonical_business_parent_update` | `canonical_businesses` | `721ff83fd4d2f974ada75d24122c5545447cb544f4f99fcadf3f24e471b0b007` |
| `trg_workspace_business_resolved_insert` | `workspaces` | `32a56615b91acf29fdee0a8811b5817d633e082bd661cff34968e4838b2af576` |
| `trg_workspace_business_resolved_update` | `workspaces` | `5c10818c7c29e2ee93d250d16baf6bc7f0e9fdf94565be7f7cb8028e2d19e458` |

**STOP FOR CEO REVIEW. Meeting Cloud E2E remains paused.**

## CEO-authorized final cloud E2E resume — 2026-09-05

Historical credential pause (superseded by final evidence below): **WAITING_CEO_NATIVE_DEEPSEEK_KEY_INPUT**. Direct isolated launch succeeded (initial PID20087, then a clean quit/reopen of the same root, PID22398). This preparatory reopen was NOT Meeting restart acceptance. Process lock was under the isolated root; no getApp used. Before CEO input, isolated companies0 / strategy_meetings0 / credential_metadata0. No source change, stage, commit or push.

Status: Review. Authority Class: REVIEW / EVIDENCE.

CEO ACCEPTED AS RECORDED INCIDENT; INCIDENT CLOSED FOR DEVELOPMENT CONTINUATION. DATA CHANGE UNKNOWN / NO SAFE ROLLBACK remains unchanged. No rollback authorized. Historical stop statements above describe their dated state.

Before launching: no Curis/sidecar process or8002/8080/3010 listener. Protected DB fingerprints reconfirmed identical to incident-audit end: repo data1232896 /1786873339955.8418 /`2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`; repo backend/data1277952 /1786783659967.5728 /`a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`; default1536000 /1788614881473.2637 /`d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617`. All integrity=ok. mtime values are milliseconds since epoch.

Fresh package: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`; manifest builtAt2026-09-05T13:26:31Z. Native SHA`fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d`; Workspace sidecar SHA`b41aa6935c44e32d89af7073abe14c5b863ac08e8407397a187fa8ebbed20161`. Read-only PyInstaller archive extraction compared normalized compiled Meeting source to embedded bytecode: equal. No app imports executed. Packaged dotenv path absent. Reuse authorized recovery build; neither CurisCopy nor old isolated package.

Pre-created external root: `/private/tmp/curis-meeting-final-cloud-e2e.k3BJ4k`. Expected SQLite: `/private/tmp/curis-meeting-final-cloud-e2e.k3BJ4k/data/curis.sqlite`. Current Rust application_data resolves explicit CURIS_DESKTOP_DATA_ROOT; spawn_workspace resolves root/data/curis.sqlite. All three DB variables set to that same path before launch. Logs/state remain under root. Launch with minimal allowlisted OS environment and no inherited Provider credentials; no native getApp locator. This is pre-launch resolution evidence, not a post-launch assumption.

### Final real-cloud evidence — credential gate resolved, budget gate reached

Status: Review. Authority Class: EVIDENCE / REVIEW. Disposition: IMPLEMENTED / PARTIAL.

CEO completed native credential input; DeepSeek/pro Health/discovery/default and a real completion succeeded. A real native Start Meeting overlay created `meeting-25cf9207-a854-4038-807d-bff342e3bac2` with three canonical Employees and a clearly labeled fictional Knowledge source. While CEO was away, two employee self-judgment calls returned SPEAK and one real technical contribution was persisted. Three successful model Tasks, three Artifacts and three usage rows total8723 confirmed tokens. Cost unknown, not free.

Existing8000 token threshold blocked Leader evaluation; no override or source change. STAY_SILENT/re-entry, @Employee, Proposal/P7 and decision-linked Work/Result remain unproved. The artifact-backed visible contribution must not be mistaken for a completed orchestration round: turnCount0/turns[] and pending event persist.

Full quit of isolated package/sidecars followed by same-root direct relaunch PID41874 preserved identical normalized Meeting state. Tasks/usage/Artifacts remain3 each. No replay observed. Isolated integrity=ok, FK check empty. Protected repo data, repo backend/data and default App DB size/mtime/SHA match the pre-launch fingerprints above; all integrity=ok. The historical default incident verdict remains unchanged.

Final selected regression44 passed/1 failed (legacy newapi registry fixture returns422). Frontend Meeting2 passed, compile/diff check/build46routes PASS; whole-tree ESLint4 errors/5 warnings in non-Meeting files. No unrelated fixes. Bounded recognizable credential-pattern scan0 hits; exact Key comparison not attempted. Full evidence and exact remaining gates: `CURIS_V1_MEETING_AUTONOMOUS_DISCUSSION_REVIEW.md` §24.

CODEX MASTER DEVELOPMENT RECOVERED. MEETING AUTONOMOUS DISCUSSION IMPLEMENTED / PARTIAL. STOP FOR CEO REVIEW; no further model calls or budget modification, no commit/push.
