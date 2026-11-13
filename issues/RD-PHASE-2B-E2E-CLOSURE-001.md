# RD-PHASE-2B-E2E-CLOSURE-001

**Status:** IMPLEMENTED / E2E ACCEPTED
**Date:** 2026-08-17
**Owner:** RD Domain

## Objective

Close one bounded RD Phase 2B business loop without redefining accepted Phase 2B-1, 2B-2
or 2B-3:

```text
accepted Developer result + approved Review
→ P7 CEO Decision
→ same-holder Codex continuation
→ new Artifact / Evidence / Result
→ Reviewer CHANGES_REQUESTED
→ same-holder revision
→ Reviewer APPROVED
→ restart recovery of the same Cycle and history
```

The batch also proves provider failure, retry, restart and idempotency without duplicate
Task/Execution creation. Artifact Review remains distinct from Responsibility Handoff.

## Authority and accepted baseline

1. Frozen `docs/00_Context/CURRENT_STATE.md` preserved-development baseline.
2. Frozen `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`.
3. Approved `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md`.
4. `RD-PHASE-2B-ARTIFACT-REVIEW-001` accepted baseline, commit `523ec49e0`.
5. `RD-PHASE-2B-HANDOFF-001` bounded baseline, commit `a31504216`.
6. `RD-PHASE-2B-P7-DECISION-001` bounded baseline, commit `e2be70459`.

Git HEAD at authorization: `a9a9105a5e68a840be78115a3aedff2416924f79`.

## Baseline protection

| Path | Pre-change SHA-256 |
| --- | --- |
| `backend/app/runtime/workspace.py` | `2688bd3a174d82714f6bc99b2c37787559ea762540f2b53d970c9171f52dcdc1` |
| `backend/app/api/runtime_foundation_router.py` | `0e4abf4f6cd214f13ded6cc28b143ab8264a0effbf3371496cca733f43f4a789` |
| `backend/tests/test_rd_artifact_review.py` | `62919541697e2f784d07aa80a61b504f4759e372eb8cfb1c9bca3f1fb918051a` |

Active DB baseline:

```text
path=data/curis.sqlite
size=1232896
mtime=1786873339
sha256=2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
integrity_check=ok
```

All backend imports and tests must first set `CURIS_DB`, `CURIS_DB_PATH` and
`CURIS_WORKSPACE_DB` to the same repository-external fresh SQLite path.

## Allowed files

- `backend/app/runtime/workspace.py`: one same-Cycle review-revision preparation command.
- `backend/app/api/runtime_foundation_router.py`: one bounded revision endpoint reusing the
  accepted asynchronous RD executor.
- `backend/tests/test_rd_artifact_review.py`: test executor sequencing support only.
- `backend/tests/test_rd_phase2b_e2e_closure.py`: new focused end-to-end regression.
- this Issue and `reviews/RD-PHASE-2B-E2E-CLOSURE-001_review.md`.

Fresh provider/Desktop acceptance may use repository-external temporary projects, SQLite,
HOME and evidence files. It must not change product source outside this boundary.

## Runtime contract

1. Revision is permitted only for the current terminal `CHANGES_REQUESTED` Review on a
   completed, inactive RD execution.
2. The Review request ref is an explicit idempotency key.
3. Responsibility Holder remains the original Developer. Current Executor is `none` before
   revision, the Developer only while revision runs, then `none` again.
4. The prior Task, Artifact, Result and Review move into existing history fields before the
   accepted RD executor starts one new Task.
5. Revision instruction is the existing bounded instruction plus persisted Reviewer summary;
   resource refs, test command, access intent and capability binding are reused unchanged.
6. Duplicate revision requests for the same Review create no second Task/Execution.
7. A new Review targets only the new Artifact/Evidence and uses the real Reviewer Employee.
8. Review never creates or changes a Handoff. P7 continuation creates no second Cycle.
9. Restart recovers the same Cycle, Holder, history and terminal Review truth.
10. Provider failure remains durable and retryable through the same bounded revision command;
    retry never duplicates an active Task.

## Explicit exclusions

- Shared/Core identity, provider callback authentication or Handoff state-machine changes;
- a generic revision Workflow, queue, retry scheduler or new execution primitive;
- Frozen Authority, schema migrations, active database, final visual redesign;
- automatic Provider-native Handoff acknowledgement while
  `SHARED_EMPLOYEE_PROVIDER_CALLBACK_IDENTITY_MISSING` remains unresolved;
- reset, clean, destructive worktree operations or push.

## Acceptance

1. One isolated full chain reaches second Review `APPROVED` after an earlier
   `CHANGES_REQUESTED` result.
2. Primary execution produces distinct Task/Artifact/Result refs for original, P7 continuation
   and Developer revision work.
3. Both Review rounds produce distinct Reviewer Task/Evidence refs and preserve Reviewer
   identity without changing the Holder.
4. Histories and identity truth survive application restart.
5. Deterministic provider failure/retry/restart/idempotency coverage proves no duplicate active
   Task/Execution.
6. One fresh production `create_app` run uses the real Codex CLI after P7 choice, or records the
   exact external blocker without downgrading deterministic acceptance.
7. Existing RD/XHS/Shared Runtime and Backend Test DB Safety regression remains green.
8. Active database size/mtime/hash/integrity remains unchanged.

## Implementation outcome

- Added one bounded `artifact-review/revise` command. It archives the terminal
  `CHANGES_REQUESTED` Review and prior Task/Artifact/Result refs, preserves the Developer as
  Responsibility Holder, and starts the accepted asynchronous RD executor on the same Cycle.
- Corrected RD failure recovery so only the real degraded Developer returns to `AVAILABLE` before
  retry; the independent Reviewer is not treated as a failed executor. Failed Task/Artifact/Result
  refs move into history before one retry Task starts.
- Added end-to-end coverage for P7 continuation, multi-round Review, failure/retry, duplicate
  revision/resume, restart and identity truth.
- During this batch Shared Runtime accepted `SHARED-EMPLOYEE-EXECUTION-TRUST-001` in commit
  `d6d47bcf7`. RD adopted its `verify_handoff_ack()` interface without changing Shared/Core:
  Provider-native ACK now requires persisted target Employee Task/session provenance and records
  the verified receipt on the existing Handoff before the existing transition completes.
- Fresh production `create_app` evidence used real Codex CLI sessions for Developer, Reviewer,
  P7 continuation, Developer revision and final Reviewer approval. A final real Reviewer callback
  then completed one Provider-native Responsibility Handoff ACK and survived restart.
- New packaged/Desktop acceptance was not run because this batch adds no approved UI command for
  revision or Provider ACK. Existing Phase 2A packaged evidence remains valid but is not upgraded
  into Phase 2B Desktop acceptance.

Formal evidence and exact IDs are recorded in
`reviews/RD-PHASE-2B-E2E-CLOSURE-001_review.md`.
