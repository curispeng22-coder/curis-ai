# RD-PHASE-2B-HANDOFF-001

**Status:** IMPLEMENTED / BACKEND RUNTIME PASS / PROVIDER CALLBACK GAP
**Date:** 2026-08-17
**Owner:** Curis main development / RD Workspace

## Goal

Implement one truthful RD Responsibility transfer without confusing Artifact Review,
executor activity or CEO Decision:

```text
Employee A holds one accepted RD Cycle Responsibility
→ persist HANDOFF CREATED
→ send the same HANDOFF
→ Employee B ACKNOWLEDGES
→ complete the same HANDOFF
→ Cycle Responsibility Holder becomes Employee B
→ Current Executor remains none
```

`RETURNED` and `REJECTED` keep the original holder. Artifact Review remains a separate,
already accepted Cycle-scoped record.

## Authority

1. `docs/00_Context/CURRENT_STATE.md`
2. `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` P1/P5/P6
4. `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` §1a/§6
5. `docs/04_Development/RD_PHASE_2B_PRE_IMPLEMENTATION_AUDIT.md` §6.1
6. accepted `RD-WORKSPACE-INSTANCE-001` and `RD-PHASE-2B-ARTIFACT-REVIEW-001` Reviews

## Preserved baseline

Audited Git HEAD: `fe55ff5d5`.

| Path | Pre-change SHA-256 |
| --- | --- |
| `backend/app/runtime/workspace.py` | `971e16fbfe38c67e835048df1d1f6b007727ad4c9f2c3267040a4cdfd0e6365a` |
| `backend/app/api/runtime_foundation_router.py` | `732eb4fffe484e73e2c2383389cfbf88dffde6260f512ce051dafe15084a1f53` |
| `frontend/components/rd/RdWorkspacePhaseTwo.js` | `4a704f9380d14b007ad1ec559a2e23708b6095b4881675cfff92537705869e25` |
| `frontend/lib/runtimeApi.js` | `825d8cb84ba053562a191c9078b77971c8bd21ab608d0410eeda2759387cd654` |

Accepted active-database read-only baseline before this Issue:

```text
data/curis.sqlite
size=1232896
mtime=1786873339
sha256=2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
```

All tests must set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to one fresh
temporary SQLite path before Python/pytest import.

## Owned implementation boundary

- `backend/app/runtime/workspace.py`: RD Cycle handoff create/send/respond commands only.
- `backend/app/api/runtime_foundation_router.py`: bounded DTOs and three RD handoff endpoints.
- `frontend/lib/runtimeApi.js`: those endpoint wrappers only.
- `frontend/components/rd/RdWorkspacePhaseTwo.js`: lightweight P5 projection/action only.
- new focused backend/frontend tests, this Issue and its Review.

No shared state machine, registry, Foundation, Shell, XHS/TTK source, Frozen Authority,
Product Blueprint or active database may change.

## Runtime contract

1. Source and target are distinct persisted `AI_EMPLOYEE` objects in the same RD Workspace.
2. The source must still be the Cycle `responsibilityEmployeeRef`; `currentExecutorRef`
   must be `none` before transfer.
3. One active transfer per Cycle. Repeating create/send/respond for the same target and
   outcome returns the same HANDOFF and creates no duplicate transition/entity.
4. `CREATED` and `SENT` do not change the Cycle holder.
5. `ACKNOWLEDGED → COMPLETED` changes the holder atomically to the target and keeps
   Current Executor `none` until a later real execution explicitly starts.
6. `RETURNED` or `REJECTED` keeps the original holder and records the reason.
7. Artifact Review, Task, Result, Artifact and Evidence refs remain intact.
8. No `DECISION_PACKET` or `ACCEPTANCE` is created.
9. Restart restores the same terminal HANDOFF and holder truth; no execution is inferred.

## Explicit exclusions

- Artifact Review redesign or repeated review rounds;
- automatic target execution, routing-policy redesign or capability reassignment;
- P7 CEO Decision;
- new Handoff primitive/state/registry;
- Workflow/DAG/Queue/Organization Router work;
- Computer Access changes;
- final visual redesign, packaged Desktop acceptance, staging or push.

If correct target execution requires Shared Organization Routing changes, record an
Integration Gap; do not widen this Issue.

## Acceptance

1. `CREATED → SENT → ACKNOWLEDGED → COMPLETED` uses one shared HANDOFF object.
2. Holder changes only after acknowledgement/completion; Current Executor remains none.
3. `RETURNED` and `REJECTED` preserve the original holder.
4. Duplicate commands are idempotent.
5. Artifact Review remains present and distinct; Decision count remains zero.
6. Same isolated SQLite restart preserves Handoff/history/holder.
7. Accepted RD execution, Artifact Review, XHS and shared Runtime state tests do not regress.

## Implementation outcome

The bounded RD Runtime/API/UI projection is implemented. One shared `HANDOFF` object now
persists `CREATED → SENT → ACKNOWLEDGED → COMPLETED`; transfer changes the Cycle holder only
at terminal acknowledgement, while return/reject keep the original holder. Duplicate
commands reuse the same object and transition history. Artifact Review and Decision remain
separate.

The ordinary-user RD UI can create/send the transfer and read the truthful state, but it
does not impersonate the receiving Employee. Current Shared identity infrastructure has no
trusted Employee-origin/provider callback boundary for the final response. The response
command is backend-covered for Runtime integration, but provider-native acknowledgement is
not accepted until that Shared gap is closed by a separate Issue.
