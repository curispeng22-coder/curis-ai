# CURIS V1 — GENERAL WORKSPACE LIFECYCLE CLOSURE REVIEW

Status: Review
Authority Class: REVIEW / IMPLEMENTATION EVIDENCE
Issue: `CURIS-V1-GENERAL-WORKSPACE-LIFECYCLE-CLOSURE-001`
Date: 2026-09-08

## Scope and decision

### Current final verdict — 2026-09-08

Status: Review. Authority Class: REVIEW / IMPLEMENTATION EVIDENCE.
Disposition: **IMPLEMENTED / ACCEPTED** for the bounded General Workspace
lifecycle/native entry scope, with recorded experience follow-ups below.
Source: CEO native404/final Desktop instructions and this turn's actual evidence.
Owner: Main Development. Next Gate: CEO / ChatGPT final review; not release.
All dated Partial/no-model/no-package checkpoints below are historical.

CEO DESK PACKAGED ROUTING / CONVERSATION-ATTENTION ROUTES / NATIVE NAVIGATION:
VERIFIED. Work A RUNNING→Pause→full restart→Paused→Resume→Archive/Restore:
VERIFIED. Work B RUNNING→Cancel: VERIFIED. Canonical A/B/A: VERIFIED.
P7/Conversation are unchanged, not reimplemented or re-created in this fixture.

Final package rebuilt after the two-line progress correction:
`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`.
BUILD-MANIFEST builtAt `2026-09-07T21:47:25Z`, HEAD
`bb72916daba3ae9555914d03bdb7fcea9953ab9c` plus preserved working changes;
log `/tmp/curis-ceo-native.ydOJRf/final-build.log`.
This is a fresh working-source package, NOT a clean-checkout claim.
The executable SHA is `fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d`;
the manifest and native corrected text distinguish it from the prior build.

Actual new-package startup→CEO Desk→Business→B displayed CANCELLED with
“当前没有员工执行” and zero result/evidence/artifact for the cancelled attempt.
Normal Command-Q, all sidecars stopped, 3010/8002/8080 free; same package/root
restarted via explicit binary and all four external-root environment settings.
CEO Desk→Business→A→Business→B again recovered the same work/results/status.
Final normal quit also freed all ports; no default App was launched.
Screenshots `native-corrected-restart-b.png`,
`native-corrected-same-package-a.png`, `native-corrected-same-package-b.png`.

**No replay:** before/after final same-package restart full row digests unchanged
for tasks(4), executions(3), artifacts(3), ai_usage_records(4), runtime_entities(20),
runtime_links(9), runtime_transition_log(31), workspaces(2), canonical_businesses(2).
WORK=4, CYCLE=4, AI_EMPLOYEE=2 remained. Event count93→98 only added five
`credential.resolved` audit events; execution_started=4, execution_completed=3,
usage.model_call=4 and result.viewed=1 unchanged. No Conversation or canonical
DECISION_PACKET exists in this fixture: zero→zero is no-creation proof, not a
new Conversation/P7 interaction claim. Earlier accepted regression covers them.
Legacy `decision`/`simulation` event names are existing executor audit vocabulary;
they are not substituted for the actual DeepSeek calls and results observed here.
Both Attention and Conversations returned200 directly8002 and via Gateway8080
for the real Company after final restart.

**Final checks:** 55 backend PASS; final route negative regression1 PASS
(a rerun, not an additional unique test); frontend15 PASS after added execution
projection assertion; focused ESLint, Python compile, production Next build,
PyInstaller sidecars, Cargo/Tauri package, git diff --check PASS.
Only production edits this pass: existing GeneralWorkspaceOperating progress
predicate and EXECUTING label. Added test plus existing frontend test changes;
no backend production/identity permission relaxation.

**Protected DB before = after:**

| Path | Size | mtime_ns | SHA-256 | Integrity |
|---|---:|---:|---|---|
| `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite` | 1232896 | 1786873339955841838 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `/Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite` | 1277952 | 1786783659967572836 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |
| `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite` | 1536000 | 1788614881473263746 | `d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617` | ok |

No stage/commit/push/reset/clean or unrelated cleanup. Generated package remains
local technical artifact, not public release. Current remaining P1:
GLOBAL UI / SEVEN-AREA FINAL PRODUCT ACCEPTANCE, including the explicitly
recorded synchronous control UX and wording issues; not started.

### Final native cloud continuation — 2026-09-08

Status: Review. Authority Class: EVIDENCE. Owner: Main Development.
This section supersedes the earlier no-model/no-cloud checkpoint below.
User configured DeepSeek through native Keychain UI in the new external root;
default model `deepseek-v4-pro`. No credential was requested in chat/read into
test code. All inputs explicitly described isolated test facts, not customers.

| Proof | Actual canonical object / outcome |
|---|---|
| A initial result | Work `work-41dfb25dfbad7f6e90d05e35a597cade`; Task `d439caec-2f7e-4551-a805-33cb75ac786d`; real cloud completion, one Result/Evidence/Artifact; native result open wrote one viewed receipt. |
| A running pause | Work `work-dfc54bd7ee46baa37e48eabfa22107fc`; Task `4836f366-1854-4a5e-b07c-fb831b78f3dc`; actual RUNNING observed, native Pause applied; cloud return did not erase PAUSED. Full quit/ports free/restart retained PAUSED and existing result; native Continue reused that result, then Archive/Restore retained same Work. |
| B first cancel race | Work `work-856234372b9b9758e7bd0c2bb1396456`; model completed 21:37:55Z before cancel 21:37:59Z. NOT counted as in-flight cancellation. Existing result retained, not deleted. |
| B true running cancel | Work `work-63db6f10ec45def52724484e1ee8fb11`; Task `4445678c-fcb1-46b4-94eb-ba6640ba0c6a`; started 21:38:42Z, native cancel 21:39:06Z; Task/Work CANCELLED, executor none, zero Result/Evidence/Artifact for this attempt. No claim that remote provider transport was physically killed. |

Native A/B/A navigation uses canonical Business directories, not SQL-cloned
Workspaces. B was created through existing founding/materialization API and
then opened through native Business navigation. A Employee 小策
`emp-d8d05499-324a-4925-a9fd-f132e59bd1bd`; B 小查
`emp-c06371e9-26b7-4a17-8abc-512a3c43e725`; both recruited through native UI.
A assignment used native form; B used the existing lawful assignment API,
then native projection. Same Employee across both Workspace scopes was rejected
by existing scope validation; that capability is NOT claimed.

**Observed UI correction:** final restart displayed an obsolete RUNNING snapshot
as live progress despite `current_executor_ref = null` and cancelled Task.
The only production delta in this pass is GeneralWorkspaceOperating's progress
expression checking current executor first, plus EXECUTING user-language label.
No lifecycle state, cancellation mechanism or Runtime snapshot was rewritten.
Added runnable frontend assertion covers null executor/RUNNING and real executor.

**Recorded follow-ups:** initiating synchronous execution keeps controls disabled
until return or ordinary navigation away/back. Actual pause/cancel above used
normal Business→Workspace navigation while execution continued, not DOM forcing
or direct cancel API. Global async submission UX, scope-conflict error wording,
internal responsibility labels and CEO Desk result-title formatting remain for
the global experience closure. Cmd-R was not independently observed to reload;
full native exit/restart and route remount were used instead. Native Console was
not independently certified; scoped Browser Console was empty. Old user Browser
tabs polling obsolete fixture Companies produce unrelated scope404 logs.

Evidence root `/tmp/curis-ceo-native.ydOJRf`: `native-work-paused.png`,
`native-paused-after-restart.png`, `native-work-archived.png`,
`native-cancel-running.png`, `native-result.png`, `native-final-restart-a.png`,
`native-final-restart-b.png` (the last captures the pre-correction stale label).
Fresh corrected package recheck and final safety verdict follow below.

### Current correction — Native CEO Desk 404 diagnosis, 2026-09-08

Authority Class: EVIDENCE. Status: Review. Owner: Main Development.
Disposition: routing/native entry VERIFIED; full General acceptance NOT yet claimed.
This correction supersedes the earlier claim below that the package lacked
Conversation/Attention routes. No production permission or routing change was
necessary. Neither a missing route nor a stale package was established by the
earlier 404-only log inspection.

**REQUEST:** `GET http://127.0.0.1:8080/api/workspace/v1/companies/{company}/attention`
and `GET .../conversations`. The former is called by
`CeoDeskOperating.load → getCompanyAttention`; the latter by the canonical
recent Conversation sidebar through `v1FrontendApi.js`. `workspaceFetch` applies
the packaged API base. Gateway forwards the same path to `127.0.0.1:8002`.

**EXPECTED / ACTUAL:** Both same-prefix routes are mounted by `main.create_app`
via `build_frontend_v1_router` and `build_conversation_router`. Both return 200
from the newly built Workspace sidecar directly AND through the Gateway for
the native-created Company. No fallback array or legacy API was added.

**ROOT CAUSE (F + G):** The prior external test DB
`/tmp/curis-general-packaged.Rv8KHP/data/curis.sqlite` has Company tenant `selfuse`
but CEO `ceo`. Desktop authorizes `selfuse-ceo`. `ResultAttention.actor` rejects
that mismatch; both canonical projections use that guard and translate its
scope exception into business 404. The added full-app regression reproduces
the mismatch and checks that the body is not route-level `Not Found`.
The prior Browser run bypassed CEO Desk; it therefore did not prove this entry
worked. Browser and native use the same backend identity boundary.

**Correction:** New empty external root `/tmp/curis-ceo-native.ydOJRf`, not an
identity-rewritten copy. All three DB variables plus `CURIS_DESKTOP_DATA_ROOT`
point to this root. Actual native Welcome → create Company → CEO Desk → business
proposal → create first Workspace completed through product commands.
Company `company-fabe96d4-efaa-4e51-8ce9-4875d96e4c36` persisted with
`selfuse` / `selfuse-ceo`; Workspace is
`workspace-first-e351167fdcce4e4abe28d8ed`. Native clicks then verified
CEO Desk → main navigation Business → directory → same Workspace, with no
deep-link-only substitution. A normal Command-Q exited app and sidecars;
8002/8080/3010 were free. Same-root launch restored CEO Desk and the same
navigation path and canonical parent. Browser CEO Desk and Conversation empty
entry also loaded; captured Browser warning/error list was empty.

**Fresh package:** `desktop/target/release/bundle/macos/Curis.app`, rebuilt in
this turn including Next standalone, PyInstaller sidecars and Cargo/Tauri.
Build log `/tmp/curis-ceo-route-build.TWFKoH/build.log`; build timestamp
`2026-09-07T21:22:53Z`. Executable SHA remains
`fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d`
(unchanged Rust binary alone is not source proof). New packaged Workspace SHA
`3ab8ffd156cc8394842011b0f965cbf802976ef8a5871cf7bfe08b9470cb57e2`,
Gateway SHA `7975e4c352d608f8a6ec959f3ee2fd9d1e9fd5805b9a97ec63fd285211a94e6c`.
Actual mounted routes additionally verified by direct/Gateway requests.

**Screenshots:** in that external root: `native-ceo-desk.png`,
`native-workspace.png`, `native-restart-ceo.png`, `native-restart-workspace.png`.

**Checks:** backend scoped suite 55 PASS; final ownership-negative route test
rerun 1 PASS; frontend 14 PASS; focused ESLint, Python compile, production build,
fresh package and `git diff --check` PASS. Backend log:
`/tmp/curis-ceo-full-regression.FljfuC/tests.log`. Only added code is
`backend/tests/test_v1_packaged_ceo_routes.py`; no production behavior changed.

**Remaining evidence:** new root has no verified model or Employee assignment.
Do not claim a real RUNNING pause/resume/cancel chain from an ACTIVE Work whose
executor is none. Earlier synthetic Workspace B, made by SQL cloning with
unresolved Employee identity, is not canonical cross-Workspace proof. The new
native lifecycle/Work A/B gate remains pending; legal model connection requested
through native Keychain UI, never via chat. No cloud call performed this turn.

**Restart scope:** one Company, one Business, one Workspace, one CEO Assistant,
two founding runs unchanged. Tasks/executions/artifacts/usage/evolution events
all remained zero across this entry restart. This proves no bootstrap duplication,
NOT no-replay of an executed Work/result/receipt. No acceptance registration or
next initiative started. No stage/commit/push.

This review covers the bounded General Workspace lifecycle controls added on
the existing canonical Work, Responsibility Routing and execution seams. It
does not reopen Conversation, Meeting, Knowledge, Organization, Talent,
Provider or P7 implementation.

Verdict: `IMPLEMENTED / PARTIAL`

The Runtime and Browser closure passed. The fresh packaged Desktop could be
built, but could not be safely launched because a pre-existing default Curis
instance occupied the fixed packaged ports `3010`, `8002` and `8080`. The
default instance was not killed or displaced, so Packaged Desktop acceptance
remains the one named environment gate.

## Lifecycle result

| Area | Result | Evidence |
|---|---|---|
| Create | PASS | Browser created one canonical General Work from the existing workspace form. |
| Start / active projection | PASS | Existing Work and responsibility projection showed the created work and employee holder. |
| Pause | PASS | Real UI button produced durable `PAUSED`; execution launch remains blocked. |
| Resume | PASS | Same Work returned to its pre-pause actionable state; no new Work was created. |
| Cancel / stop | PASS | Real UI produced durable `CANCELLED`; holder and history remained. |
| Archive | PASS | Real UI produced durable `ARCHIVED`; Work remained readable. |
| Restore / reopen | PASS | “恢复查看” returned the same Work to its prior `CANCELLED` state and did not rerun it. |
| Failure truth | PASS | Focused test preserved failed execution evidence and did not mark Work completed. |
| P7 / Conversation / Result | NO CHANGE | Existing canonical seams remain referenced; no second packet or conversation was introduced. |

## Runtime evidence

The external acceptance SQLite was:

`/tmp/curis-general-browser.r5P6Cq/isolated.sqlite`

The final read-only query returned one Work:

`work-55f60358643edc8f2cfe73b83255f825`, lifecycle `CANCELLED`.

Its transition log recorded:

`PLANNED → READY → ACTIVE → PAUSED → ACTIVE → CANCELLED → ARCHIVED → CANCELLED`.

The final projection retained the responsibility holder `employee-v1-general`,
cleared the current executor, retained archive/pause timestamps and retained
the Work identity. The acceptance seed had no configured model, so no provider
execution was claimed and no fake Result/Evidence was created.

The separate Runtime guard rejects new execution for `PAUSED`, `CANCELLED` and
`ARCHIVED` Work before provider launch. Work lifecycle, responsibility status
and execution status remain separate projection fields.

## Browser evidence

Environment: `http://localhost:3013`, API `127.0.0.1:8421`, external SQLite
above. Real browser operations were performed through the product UI:

1. Entered General Workspace and submitted a real problem plus expected result.
2. Clicked `暂停`; the Work rendered `已暂停` and `继续工作`.
3. Clicked `继续工作`; the same Work rendered `正在处理`/actionable controls.
4. Clicked `停止`; the Work rendered `已停止` with history retained.
5. Clicked `归档`; the Work rendered `已归档` and `恢复查看`.
6. Clicked `恢复查看`; the same Work rendered `已停止` without a new execution.
7. Reopened the URL and read the same persisted Work and state.

The final screenshot showed the user-language General Workspace with the same
Work card, `已停止`, `归档`, retained responsibility and no internal UUIDs in
the primary surface. Browser console logs contained no unexpected errors.

## Tests and build

- Backend focused and bounded regression: `45 passed`.
- Additional XHS / Employee Conversation / Operating Cycle regression:
  `17 passed`.
- Frontend focused Node contract tests: `3 passed`.
- Scoped ESLint: PASS.
- Python compile for touched backend modules: PASS.
- Frontend production build: PASS, 47 routes generated.
- Fresh runtime build: PASS; Workspace, Gateway, Guardian and Recovery
  sidecars rebuilt from current source.
- Fresh Tauri `Curis.app` build: PASS.
- `git diff --check`: PASS.
- The first test invocation without the repository root in `PYTHONPATH` failed
  during collection with `ModuleNotFoundError: backend`; the corrected,
  established isolated invocation passed and no implementation defect was
  indicated.

## Packaged Desktop gate

Fresh package path:

`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`

Main binary SHA-256:

`fe66764ff1ae6e2e62aa29ccd534be5ebb26ac82027373989baf7d24d160bd1d`

Launch was intentionally not attempted. Read-only port inspection found an
existing default Curis instance listening on:

- `127.0.0.1:3010` — packaged frontend
- `127.0.0.1:8002` — Workspace Runtime
- `127.0.0.1:8080` — Trusted Gateway

The packaged source uses these fixed ports and has no bounded per-instance
override available in this Issue. Killing or displacing the default instance
was outside authorization. Therefore Browser PASS is not promoted to
Packaged Desktop PASS.

## Protected database safety

All tests and Browser acceptance used an external isolated SQLite. The three
protected active databases were read through immutable/read-only SQLite access
before and after the run:

| Path | Size | mtime ns | SHA-256 | integrity |
|---|---:|---:|---|---|
| `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite` | 1232896 | 1786873339955841838 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `/Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite` | 1277952 | 1786783659967572836 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |
| `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite` | 1536000 | 1788614881473263746 | `d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617` | ok |

No active DB was initialized, migrated or written by this task.

## Changed files owned by this Issue

- `backend/app/runtime/child_work.py` — existing Work states, transitions,
  durable pause/archive metadata, idempotent controls.
- `backend/app/runtime/general_workspace_delivery.py` — General Work control
  adapter and execution cancellation/archive gates.
- `backend/app/api/shared_workspace_router.py` — bounded lifecycle command.
- `backend/app/api/team_operating_router.py` — pre-launch lifecycle guard.
- `backend/app/shared_workspace_projection.py` — lifecycle/responsibility/
  execution separation and recovery projection.
- `frontend/lib/runtimeApi.js` — lifecycle command wrapper.
- `frontend/components/v1/GeneralWorkspaceOperating.js` — user-language
  controls and status translations.
- `backend/tests/test_v1_general_workspace_lifecycle_closure.py` — isolated
  lifecycle, failure and idempotency coverage.
- `frontend/tests/v1GeneralWorkspaceOperating.test.mjs` — focused UI contract.
- `issues/CURIS-V1-GENERAL-WORKSPACE-LIFECYCLE-CLOSURE-001.md` — Issue record.

No commit, stage, push, reset, clean or stash was performed. Other dirty and
untracked worktree content was preserved.

## Final Packaged Desktop Gate (2026-09-08)

The previous fixed-port blocker was cleared without touching the default
instance. A fresh packaged `Curis.app` was launched using the external root
`/tmp/curis-general-packaged.Rv8KHP`; the native app and Workspace/Gateway/
Frontend/Guardian sidecars started, and all listeners were released after the
run.

The packaged runtime/browser surface passed the bounded lifecycle checks:

- Work A: `ACTIVE → PAUSED`, reload retained `PAUSED`, `RESUME` returned the
  same Work to actionable state, then `CANCELLED → ARCHIVED → CANCELLED`
  through the real UI controls.
- Work B: an independent canonical Work in Workspace B was readable; A→B→A
  navigation retained independent Work identities and did not create or replay
  execution, Result, or Conversation records.
- Same-root restart reread the same Work/Cycle identities and statuses. Final
  isolated counts were `runtime_entities=17`, `runtime_transition_log=18`,
  `tasks=0`, `executions=0`, `artifacts=0`, `step_results=0`; packaged page
  console error log was empty.

Native Desktop acceptance remains **FAIL / EXACT GATE OPEN**, so the Issue is
not promoted to Accepted. The native WebView restored `/ceo-office` and
rendered `暂时无法读取 CEO 工作台`. Its current packaged frontend requested
`/api/workspace/v1/companies/{company}/attention` and `/conversations`, but
the packaged Workspace Runtime returned 404 for those routes. The native
window therefore could not reach General Workspace through product
navigation. The direct General Workspace route was verified only in Chrome
against the packaged frontend server; that is supplementary evidence and does
not replace native Desktop evidence.

The remaining gate is therefore precise: make the packaged native entry able
to navigate from CEO Desk to General Workspace (or provide an already
authorized packaged navigation path) without changing lifecycle semantics.
No implementation code was changed during this acceptance gate.

## Protected database final evidence

The external package root was `/tmp/curis-general-packaged.Rv8KHP`; its SQLite
integrity check was `ok`. The protected active databases remained unchanged:

| Path | Size | mtime ns | SHA-256 | integrity |
|---|---:|---:|---|---|
| `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite` | 1232896 | 1786873339955841838 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `/Users/yy/Documents/Curis AI Workspace/backend/data/curis.sqlite` | 1277952 | 1786783659967572836 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |
| `/Users/yy/Library/Application Support/com.curis.desktop/data/curis.sqlite` | 1536000 | 1788614881473263746 | `d80dbe64a35ae85b3c3384dccdaf2d52d338deaa06246a52d4b5b71a58f7f617` | ok |

## Final status

`IMPLEMENTED / PARTIAL` — Runtime and Browser acceptance remain passed; the
only open gate is native packaged Desktop navigation/interaction from the
native entry surface. No new lifecycle feature or cloud-model test is
required to close this Issue.

Global UI/seven-area final product acceptance remains the next V1 P1 after
this closure; it was not started here.
