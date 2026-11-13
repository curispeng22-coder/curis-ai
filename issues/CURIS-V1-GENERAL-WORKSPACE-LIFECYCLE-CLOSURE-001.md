# CURIS-V1-GENERAL-WORKSPACE-LIFECYCLE-CLOSURE-001

Status: Review
Disposition: IMPLEMENTED / ACCEPTED — bounded lifecycle and native navigation/restart verified; global experience follow-ups recorded in final Review. CEO / ChatGPT review requested; no commit/push.
Authority Class: CURRENT / IMPLEMENTATION ISSUE
Owner: Main Development Session
Date: 2026-09-08

## Goal

### Final native projection correction — 2026-09-08

Fresh restart exposed a cancelled Work with no current executor but a historical
RUNNING execution snapshot. Owned scope: existing GeneralWorkspaceOperating.js
progress expression and EXECUTING label, plus its focused regression. Consume
current executor presence before claiming live execution; do not mutate Runtime
history or expand lifecycle semantics. Final package must be rebuilt and checked.
Pre-change working hashes for these owned hunks:
GeneralWorkspaceOperating.js `7ae820b39d16269a22f4ee14ff1a8d3abe245238cb1d88a3cab786e84cadf03e`;
v1GeneralWorkspaceOperating.test.mjs `23da2b3adf0b4c1fda4941bb645c2c599cbfe8222e9e0228486baaa8284c0edb`.

### Native CEO Desk 404 closure — 2026-09-08

CEO authorizes diagnosis, a minimal root-cause correction and fresh packaged
re-acceptance. Additional owned file:
`backend/tests/test_v1_packaged_ceo_routes.py` (real app route registration,
local CEO ownership, canonical empty projections and restart regression).
No permission guard relaxation is allowed. Current source mounts both routes;
the prior external fixture has tenant `selfuse` but CEO `ceo`, whereas Desktop
uses `selfuse-ceo`. Full-app positive/negative tests verified this scope mismatch;
it was not a missing route. Build outputs remain generated; no staging/commit/push.
Use a new external root and legal founding/materialization commands rather
than transplanting identity rows from the prior test fixture. Prior synthetic
Workspace B is not eligible as canonical acceptance evidence.

Close the General Workspace lifecycle/control gap over the existing canonical
`CYCLE` / `WORK`, Responsibility Routing, Execution, Result, Evidence, P7 and
Conversation primitives. Work lifecycle, responsibility state and provider
execution state must remain separate and truthful after reload and restart.

## Current Gap

The accepted General Workspace operating surface can create, execute, wait,
fail, route and decide over canonical Work, but it has no bounded product
controls for persistent pause/resume/archive/restore. The Team Operating
execution entry also needs to honor a paused or archived Work record before
provider launch. Existing cancellation is reusable but is not exposed through
the General Workspace product route with a durable Work lifecycle projection.

## Allowed Files

### Backend

- `backend/app/runtime/child_work.py` — extend the existing Work lifecycle
  transition table and add atomic control helpers; no second state machine.
- `backend/app/runtime/general_workspace_delivery.py` — General Workspace
  command adapter for lifecycle controls, reusing canonical Work and routing.
- `backend/app/api/shared_workspace_router.py` — bounded General lifecycle
  HTTP commands.
- `backend/app/api/team_operating_router.py` — owned execution guard only:
  reject provider launch for paused/archived/cancelled General Work.
- `backend/app/shared_workspace_projection.py` — project Work lifecycle,
  execution status and recovery actions without creating a read/write authority.
- `backend/tests/test_v1_general_workspace_lifecycle_closure.py` — isolated
  lifecycle, scope, idempotency, restart and failure acceptance.
- `backend/tests/test_v1_general_workspace_p1_operating_closure.py` — only if
  a focused regression assertion must be adjusted without changing its scope.

### Frontend

- `frontend/lib/runtimeApi.js` — wrappers for the bounded General lifecycle
  commands only.
- `frontend/components/v1/GeneralWorkspaceOperating.js` — product-language
  lifecycle controls and truthful state refresh; no new UI system.
- `frontend/tests/v1GeneralWorkspaceOperating.test.mjs` — focused contract
  assertions for controls and user wording.

### Delivery

- this Issue;
- `docs/reviews/CURIS_V1_GENERAL_WORKSPACE_LIFECYCLE_CLOSURE_REVIEW.md`.

Current-state/backlog documents are updated only after acceptance evidence.

## Pre-change Hashes

These are working-tree hashes at Issue creation. The files are already dirty
from preserved initiatives; only new semantic hunks owned by this Issue may be
added.

| File | SHA-256 |
|---|---|
| `backend/app/runtime/child_work.py` | `163523fa3752177dcb7fe00567245b7983261c52703407d06a631908285f438b` |
| `backend/app/runtime/general_workspace_delivery.py` | `8acd1f45e5930ab6a4f1b9fa7e84adf565ed8e9287ba30e9f95b69eb6359d7eb` |
| `backend/app/api/shared_workspace_router.py` | `ba90daa74e06c6b5ec95f222c751898f51942b7f52364ff5459c1532083fafa2` |
| `backend/app/api/team_operating_router.py` | `8db32a7d480d8be105cfe1dc96f13753daedac1dbb4af918f47cbbb24f812ff9` |
| `backend/app/shared_workspace_projection.py` | `8ab73561abfb97429eb1c70162e7f2453794f11a655c687297a0e76397f52888` |
| `frontend/lib/runtimeApi.js` | `6e70277513595cb90758f060e3ab1a81db0317bcf0a9681e4afef5f496556b8d` |
| `frontend/components/v1/GeneralWorkspaceOperating.js` | `201efd32aeec1d1278f0be972cf4f0426c5385739f94260dac7b3b514703cbaf` |
| `backend/tests/test_v1_general_workspace_p1_operating_closure.py` | `750a04eed73e00685a8b909764d3be77609a751cb55f4f4eddc6a14a62e55849` |
| `frontend/tests/v1GeneralWorkspaceOperating.test.mjs` | `48d9504830bb12d1dfc83cf42286ce35469196acf817b16e4d65def3cb1a5c05` |

## Explicit Exclusions

- no new Work, Task, Cycle, Execution, Responsibility, Result, Attention,
  Conversation or P7 system;
- no new schema or global Runtime primitive unless a real stop gate appears;
- no Meeting, XHS, RD, TTK, Knowledge, Provider, Computer Access or Usage
  expansion;
- no Workflow/DAG/scheduler/organization router;
- no fake execution, result, evidence or permission state;
- no Product Blueprint/Frozen Contract redesign;
- no active SQLite access, migration or initialization;
- no reset, clean, stash, stage, commit or push.

## Lifecycle Contract

- `PLANNED → READY → ACTIVE → WAITING/BLOCKED/FAILED/COMPLETED/CANCELLED`
  remains the canonical Work lifecycle, with bounded `PAUSED` and
  `ARCHIVED` controls added only to the existing Work primitive.
- Pause is durable and does not mean provider execution is still running.
  Resume returns the Work to its pre-pause actionable state; an active external
  execution remains governed by its own execution truth.
- Cancel is terminal for Work and preserves prior Result/Evidence history.
- Archive hides a terminal Work from the active operating list without deleting
  it; restore only restores the archived projection and never re-runs Work.
- Result/Execution/Responsibility/P7 semantics remain their existing states.

## Acceptance

1. Create one canonical General Work idempotently; no duplicate Cycle/Work.
2. Read Work, Responsibility Holder and Current Executor separately.
3. Pause persists, blocks new provider launch, and is visible after reload.
4. Resume persists, restores the pre-pause actionable Work state, and is
   idempotent without duplicate execution.
5. Cancel is persistent, idempotent, terminal, and retains evidence/history.
6. Archive/restore are persistent, non-destructive and never auto-run Work.
7. Real failure remains failed/waiting with reason and recovery action; no
   fake Completed/Result is produced.
8. Existing P7 and Conversation/Result references continue to use the same
   canonical objects; no new packet or conversation is created.
9. Cross-company/workspace access and lifecycle commands fail closed before
   execution and all tests use one repository-external isolated SQLite selected
   by `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB`.

## Verification / Stop Gates

Run focused backend/frontend tests, relevant no-regression tests, Python
compile, ESLint/build where affected, Browser and fresh packaged Desktop
flows, restart/no-replay, and before/after fingerprints for repository and
default App databases. Stop on a schema/authority conflict, active DB
mutation, ambiguous ownership, or inability to preserve idempotency.

## Status

Implementation starts only after this bounded Issue is recorded. Final status
must be evidence-based: `IMPLEMENTED / ACCEPTED CANDIDATE`, `IMPLEMENTED /
PARTIAL`, or a named stop gate.

## Current Verification (2026-09-08)

- Browser acceptance passed against `http://localhost:3013` and external
  `/tmp/curis-general-browser.r5P6Cq/isolated.sqlite`: real UI create,
  pause, resume, cancel, archive, restore-view and refresh persistence.
- Isolated Runtime evidence contains one canonical Work and durable
  `PLANNED → READY → ACTIVE → PAUSED → ACTIVE → CANCELLED → ARCHIVED →
  CANCELLED` transitions. No execution/result was fabricated; the seeded
  acceptance state had no provider model and therefore did not attempt a real
  provider call.
- Focused/regression backend run: `45 passed`; frontend Node contract tests:
  `3 passed`; scoped ESLint, Python compile and Next production build passed.
- Fresh source runtime and Tauri application build passed. The packaged app was
  launched with an external data root after the fixed ports were confirmed
  free. Native Desktop navigation still rendered the existing CEO Desk error
  because its conversation/attention requests returned 404; it was not
  promoted to Packaged Desktop PASS.
- Protected active databases remained byte-identical and integrity-valid. The
  remaining gate is specifically packaged Desktop execution in an environment
  where those fixed ports are free; no code or Runtime blocker was inferred.

## Final Packaged Desktop Gate (2026-09-08)

- Preflight passed: the default instance was not running, and ports `3010`,
  `8002` and `8080` were free before launch. The fresh package was launched
  with `CURIS_DESKTOP_DATA_ROOT=/tmp/curis-general-packaged.Rv8KHP`.
- The packaged native window and all three sidecars started successfully. The
  isolated runtime served the canonical company/workspace data after the
  fixture was aligned to the packaged `selfuse` tenant.
- Packaged runtime/browser-surface checks passed for the same package and root:
  Work pause, reload persistence, resume, stop/cancel, archive/restore-view,
  A→B→A workspace navigation, no console errors, full exit, same-root restart,
  and reread of the same Work/Cycle identities. Final isolated counts were
  `runtime_entities=17`, `runtime_transition_log=18`, `tasks=0`,
  `executions=0`, `artifacts=0`, `step_results=0`.
- Native Desktop acceptance is **not** promoted to PASS. The native WebView
  restored `/ceo-office` and rendered `暂时无法读取 CEO 工作台`; the current
  packaged frontend requests `/api/workspace/v1/companies/{company}/attention`
  and `/conversations`, while the packaged Workspace Runtime returns 404 for
  those pre-existing routes. Consequently the native window could not reach
  the General Workspace route through product navigation. The direct route was
  verified only against the packaged frontend server in Chrome and is not a
  substitute for native Desktop acceptance.
- Final isolated root remained external and valid: `/tmp/curis-general-packaged.Rv8KHP/data/curis.sqlite`,
  `size=1331200`, `integrity=ok`. The package was then stopped; no package
  process or listener remained on `3010/8002/8080`.
- The three protected active databases retained their recorded size, mtime,
  SHA-256 and `integrity_check=ok` values. No source, Runtime or database code
  was changed in this gate.
