# RD-PHASE-2B-E2E-CLOSURE-001 Review

**Status:** IMPLEMENTED / E2E ACCEPTED
**Date:** 2026-08-17
**Issue:** `issues/RD-PHASE-2B-E2E-CLOSURE-001.md`

## Decision

RD Phase 2B now has an accepted bounded end-to-end Runtime proof across P7 continuation,
multi-round Developer/Reviewer work, failure/retry/restart, exact Employee execution provenance
and Provider-native Responsibility Handoff ACK. This does not claim final UI or a new packaged
Desktop Phase 2B acceptance.

## Implemented boundary

1. `CHANGES_REQUESTED` can prepare one same-Cycle Developer revision using the Review request ref
   as its idempotency key.
2. Prior Task, Artifact, Result and Review refs move into existing history fields before the
   accepted asynchronous RD execution path starts.
3. RD resume returns only the actual degraded Developer to `AVAILABLE`; the Reviewer remains an
   independent Employee. Failed result refs are archived before retry.
4. Review still creates no Handoff. P7 continues the original Holder and creates no second Cycle.
5. After Shared commit `d6d47bcf7`, RD uses `EmployeeExecutionIdentity.verify_handoff_ack()`.
   A Provider-native ACK must prove the current SENT target, exact Runtime/Company Employee,
   Task, Capability Binding, usage event and Codex session before the existing Handoff transition.
6. Duplicate revision, resume and Provider ACK requests do not create another Task/Execution or
   transition.

## Fresh real Codex P7 continuation

Evidence root: `/tmp/curis-rd-phase2b-live.ojq3qd`

SQLite: `/tmp/curis-rd-phase2b-live.ojq3qd/runtime6.sqlite`

```text
Company: company-rd-phase2b-live
Workspace: workspace-e1637bf7-a0f2-42c5-9306-b56020aeea34
Cycle: cycle-5afd54e2-8f7d-47fc-b3bb-2a71fffe917c
Responsibility Holder: ai_employee-c1a999f5-dc85-4feb-aff7-fced7ccbfee2
```

Initial real Developer work:

```text
Task: 26e7ed3a-2550-447e-99ca-7c219c936f60
Codex session: 01a00ea3-c737-7eb0-a101-b797443d50d7
Artifacts: artifact-c846aa00-f5a5-46ed-8fb5-8dcba0380d1d,
           artifact-c28d7db0-2158-4531-a90d-efd375177daa
```

Independent real Reviewer:

```text
Task: 24d5d244-4834-4a17-b56b-17262cfe32f9
Codex session: 01a00ea4-38ed-78e3-8dec-7b184e94f805
Outcome: APPROVED
```

P7 and fresh continuation:

```text
Decision: decision_packet-6ef04ff7-f35a-493c-90b3-d55f688856f4
Choice: ADD_MULTIPLY
Continuation Task: 39cdd109-3edc-41c0-84bc-9a4cedf364c2
Continuation Codex session: 01a00ea4-95c6-7650-b10e-d3a758a0dfe2
Continuation Artifacts: artifact-0e62ff67-d342-4d44-a81a-e76173b0387a,
                        artifact-95e7df9d-89d6-45ad-8769-a8b3ea04faf2
Verification: python3 -m unittest -q, 2 tests, exit 0
```

All three Tasks are `COMPLETED`; each has exactly one `executions` row. The continuation retained
the same Cycle and Holder, set Current Executor only while work ran, produced new Artifact /
Evidence / Result refs, archived the initial Task/Review, and created zero Handoffs. A new
`create_app` over the same SQLite recovered the same Task, Holder, P7 Decision and history with
Current Executor `none`.

Computer Access remained truthful: requested `AUTO_WITHIN_BOUNDARY`, configured `CONFIGURED`,
native command mapping `APPLIED/workspace-write`, effective `UNKNOWN`, verification `UNVERIFIED`.

## Fresh real multi-round Reviewer closure

SQLite: `/tmp/curis-rd-phase2b-live.ojq3qd/runtime5.sqlite`

```text
Workspace: workspace-f50f0b63-91a3-4b1e-880d-860f427d8b30
Cycle: cycle-2d2ee6a5-5fd1-42b9-8439-1defd4ab4f8a
Developer Holder: ai_employee-b21c3fd3-c37a-4237-b376-90eb78d570e7
Reviewer: ai_employee-2fde4252-c849-4de2-a07a-9652d95680c3
```

First real Review:

```text
Task: 925734f6-2337-466d-88ba-2890f4d1d4d8
Codex session: 01a00ea3-38a5-79e0-b77f-e6c78746993d
Outcome: CHANGES_REQUESTED
Reason: add evidence passed, but multiply and its test were missing
Callback provenance: VERIFIED, callback actor = Reviewer Employee
```

Developer revision and second Review:

```text
Revision Task: 3f722d7b-4673-4bf4-938d-190570157e56
Revision Codex session: 01a00ea7-12a4-7f50-a2d6-3aab66e0c28b
Revision Artifacts: artifact-b2453289-ff10-4785-b2ff-33e055d4b727,
                    artifact-a2d2e6a3-f887-4922-bf15-f3ae099eaa11
Verification: python3 -m unittest -q, 2 tests, exit 0
Final Review Task: b2d9ce7f-4fd0-4edc-90ee-596997f3f0f7
Final Review Codex session: 01a00ea7-8d53-70e3-9249-db2ec215c685
Final outcome: APPROVED
Developer callback: VERIFIED, callback actor = Developer Employee
Reviewer callback: VERIFIED, callback actor = Reviewer Employee
```

The `CHANGES_REQUESTED` Review remains in `artifactReviewHistory`; the final `APPROVED` Review is
current. Responsibility stayed with the Developer and Current Executor returned to `none` through
both reviews. Review created no Handoff.

## Failure, retry, restart and idempotency

- Deterministic E2E injected one failed primary execution (`task-primary-3`), persisted
  `PAUSED/FAILED`, restarted, resumed and completed one retry (`task-primary-4`). Task history is
  exactly `task-primary-1/2/3`; duplicate revision and duplicate resume create no extra call.
- In the fresh production multi-round run, restart reconciliation disabled the temporary legacy
  execution Employee. Revision failed before Provider dispatch with
  `rd_execution_employee_binding_invalid`; the Cycle persisted one failure event and no fake Task.
  After restoring the exact-ID accepted binding, `/resume → /execute` resolved that event and
  started exactly one real revision Task.
- Runtime5 has four real Tasks (Developer, Reviewer, Developer revision, Reviewer re-review), each
  with exactly one `executions` row. Runtime6 has three real Tasks (Developer, Reviewer, P7
  continuation), each with exactly one `executions` row.
- No fresh network/provider outage was induced. Provider/adapter failure semantics are accepted by
  deterministic Runtime-boundary evidence; fresh production evidence covers fail-closed binding
  rejection and real Codex success after recovery.

## Provider-native Handoff ACK

Shared dependency: `d6d47bcf7 feat(runtime): verify employee execution identity` — accepted while
this batch was running.

RD created and sent one explicit post-review Responsibility Handoff, then verified the real final
Reviewer Task/session through the Shared verifier:

```text
Handoff: handoff-34e1ac6d-3338-46f4-b6db-e39719583ca6
Target / ACK actor: ai_employee-2fde4252-c849-4de2-a07a-9652d95680c3
Task: b2d9ce7f-4fd0-4edc-90ee-596997f3f0f7
Session: 01a00ea7-8d53-70e3-9249-db2ec215c685
Provider callback verification: VERIFIED
Transitions: CREATED → SENT → ACKNOWLEDGED → COMPLETED
```

The Holder changed from Developer to Reviewer only after verified ACK. Current Executor remained
`none`. A forged session returned `422` and left the Handoff `SENT` with the original Holder. A
duplicate valid Provider ACK returned the same Handoff without another transition. Restart
recovered one COMPLETED Handoff, the new Holder and the same VERIFIED provenance.

Manual/CEO Handoff response remains available but is not classified as Provider-native evidence.

## Automated verification

Every backend invocation set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to the same fresh
repository-external SQLite before pytest import.

Final focused/no-regression set:

```text
30 passed
backend/tests/test_rd_phase2b_e2e_closure.py
backend/tests/test_employee_execution_identity.py
backend/tests/test_shared_workspace_projection.py
backend/tests/test_rd_p7_decision.py
backend/tests/test_rd_responsibility_handoff.py
backend/tests/test_rd_artifact_review.py
backend/tests/test_rd_workspace_real_execution.py
backend/tests/test_runtime_operating_cycle.py
backend/tests/test_xhs_calendar_note_runtime.py
backend/tests/test_runtime_foundation_state_contracts.py
backend/tests/test_backend_test_db_safety.py
```

Warnings are existing FastAPI lifespan and Node/Python environment deprecations.

## Database and restart evidence

```text
runtime5.sqlite: size=1445888, integrity_check=ok, foreign_key_check=0 rows
runtime6.sqlite: size=1376256, integrity_check=ok, foreign_key_check=0 rows
```

Active database before and after all work:

```text
path=data/curis.sqlite
size=1232896
mtime=1786873339
sha256=2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
integrity_check=ok
```

## Mixed-source and commit boundary

Post-change SHA-256:

| Path | SHA-256 |
| --- | --- |
| `backend/app/runtime/workspace.py` | `99acd9519d62796a616d154cbba281228821ce13fc79a2f58add60b1fd14ae5e` |
| `backend/app/api/runtime_foundation_router.py` | `f8773324ebb2b2ab29e3ecb54057aff49af651e96bffbdfef58dd25d0fb9ec23` |
| `backend/tests/test_rd_artifact_review.py` | `90cb22e5ba16f8213ae4d9c61e986538b1e7cebe4843517c8d6cf54e5b8e849f` |
| `backend/tests/test_rd_phase2b_e2e_closure.py` | `800703386ad5b4386b8624ccc41fe9874570ceb2347fbc650f68e2bdc8323748` |

`workspace.py` and the Foundation router remain accepted mixed/untracked source seams inherited
from the preserved baseline. They are not safe whole-file commit candidates. The bounded commit
contains the tracked test-helper hunk, independently owned E2E test and formal Issue/Review; it is
an ordered integration commit against this preserved snapshot, not a standalone clean-branch
cherry-pick. Shared commit `d6d47bcf7` remains independently owned by Shared Runtime.

## Desktop boundary

Accepted Phase 2A packaged Desktop success/failure/restart evidence remains valid. This batch adds
no approved UI command for revision or Provider ACK, so no new packaged Desktop Phase 2B claim is
made. Production API, real Codex, persistence and full `create_app` restart evidence are accepted;
new Desktop UI acceptance remains a later UI-authorized batch.

## Final acceptance

`RD PHASE 2B BOUNDED E2E RUNTIME ACCEPTED`

Accepted: P7 fresh real Codex continuation, new Artifact/Evidence/Result, multi-round real Reviewer,
failure/retry/restart/idempotency, exact Developer/Reviewer callback provenance, Review/Handoff
separation and Provider-native Handoff ACK.

Not accepted by this Review: final Phase 2B UI or a new packaged Desktop E2E pass.
