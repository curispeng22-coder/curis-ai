# RD-PHASE-2B-P7-DECISION-001 Review

**Status:** IMPLEMENTED / INTEGRATION PASS / REAL PROVIDER REPLAY PENDING
**Date:** 2026-08-17
**Issue:** `issues/RD-PHASE-2B-P7-DECISION-001.md`

## Implemented boundary

- one shared `DECISION_PACKET`, not a new RD approval primitive;
- exact lifecycle `DRAFT → READY → WAITING_CEO → DECIDED → APPLIED`;
- high-risk Layer 0 contains only `VIEW_OPTIONS / DEFER`;
- Layer 1 persists review before a choice can apply;
- options carry impact/risk/cost provenance; recommendation and reason also carry provenance;
- defer remains `WAITING_CEO` and starts no execution;
- applied choice keeps the original Responsibility Holder, archives prior Task/Artifact/
  Result/Review refs, and starts the existing asynchronous RD execution path;
- Current Executor is the holder only while that execution is running and returns to `none`;
- no Handoff is created.

## Evidence

All backend invocations set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to one fresh
temporary SQLite before pytest import.

Final focused backend regression:

```text
21 passed
backend/tests/test_rd_p7_decision.py
backend/tests/test_rd_responsibility_handoff.py
backend/tests/test_rd_artifact_review.py
backend/tests/test_rd_workspace_real_execution.py
backend/tests/test_xhs_calendar_note_runtime.py
backend/tests/test_runtime_foundation_state_contracts.py
backend/tests/test_backend_test_db_safety.py
```

P7-specific evidence proves:

- duplicate packet creation returns one Decision ref;
- unreviewed high-risk choice returns `409`;
- defer remains pending and executor call count does not change;
- invalid provenance returns `422`;
- review is idempotent;
- apply returns asynchronous `RUNNING` with Current Executor equal to the original holder;
- deterministic executor call count increases exactly once;
- terminal state is `COMPLETED`, Current Executor is `none`, Decision is `APPLIED`;
- prior Task and Artifact Review are retained in history;
- repeated choice creates no second Task/executor call;
- restart restores the same Decision, result and holder;
- transition log is exactly `DRAFT → READY → WAITING_CEO → DECIDED → APPLIED`;
- Handoff count remains zero.

Frontend/source contracts:

```text
17 passed
frontend/tests/rdP7Decision.test.mjs
frontend/tests/rdResponsibilityHandoff.test.mjs
frontend/tests/rdArtifactReview.test.mjs
frontend/tests/rdWorkspaceExecution.test.mjs
frontend/tests/runtimeWorkspaceUi.test.mjs
```

Production frontend build passed: Next.js compiled and generated all `45/45` pages.
Layer 0 has no direct approval action; Layer 1 shows compact options and provenance, while
professional code/test Evidence stays in the existing Utility path.

Existing FastAPI lifespan and Node module-type warnings remain unchanged.

## Active database safety

Before and after tests/build:

```text
path=data/curis.sqlite
size=1232896
mtime=1786873339
sha256=2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
```

## Post-change mixed-source hashes

| Path | SHA-256 |
| --- | --- |
| `backend/app/runtime/workspace.py` | `2688bd3a174d82714f6bc99b2c37787559ea762540f2b53d970c9171f52dcdc1` |
| `backend/app/api/runtime_foundation_router.py` | `0e4abf4f6cd214f13ded6cc28b143ab8264a0effbf3371496cca733f43f4a789` |
| `frontend/components/rd/RdWorkspacePhaseTwo.js` | `b23650202de57dab25a04bc8b90f0b4b7952686beca452fe0488c0eb74764ee7` |
| `frontend/lib/runtimeApi.js` | `57c6450224f4d2e6f1a65d36fd0348b3c99934ae238f179f569542ce409e59a0` |

These accepted mixed/untracked source files are not safe whole-file commit candidates; the
commit contains only independently owned P7 files and formal records.

## Remaining evidence gap

`RD_P7_REAL_PROVIDER_CONTINUATION_REPLAY_PENDING`

The new P7 path is proven through the real Runtime execution adapter boundary with a
deterministic executor, and the accepted real Codex RD test set passes unchanged. A fresh
provider-native Codex run starting specifically from an applied P7 choice was not executed.
This is an RD evidence gap, not permission to alter Provider/Core.

## Decision

`IMPLEMENTED / INTEGRATION PASS / REAL PROVIDER REPLAY PENDING`
