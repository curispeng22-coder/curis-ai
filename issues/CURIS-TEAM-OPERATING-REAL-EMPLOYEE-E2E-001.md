# CURIS-TEAM-OPERATING-REAL-EMPLOYEE-E2E-001

Status: IMPLEMENTED / ACCEPTED
Authority Class: CURRENT

## Goal

Close the accepted Team Operating control plane against the existing real employee execution path:

`Work -> pinned Assignment -> canonical Employee -> capability binding -> ResultStore Task -> Orchestrator/provider session -> verified callback -> accepted result -> automatic routing -> next Employee -> final Work`.

The first acceptance slice is Workspace-scoped content growth with at least three distinct responsibility executions. A small Business-scoped RD slice is included only if the same bridge is safe after the content slice passes.

## Current gap

`ResponsibilityRoutingRuntime` persists who owns the next responsibility, but does not start that Employee's existing provider execution. Consult completion and routing currently require a second manual API call and tests may inject response references directly.

## Existing execution entry

- Company execution identity: `EmployeeExecutionIdentity`.
- Capability binding: enabled `employee_capability_bindings` for the resolved Company Employee; responsibility ownership is never selected by capability resolution.
- Provider Task/Session: `ResultStore.create_task()` + existing `Orchestrator.run()` + `usage.task_execution`.
- Callback trust: `EmployeeExecutionIdentity.verify_task_callback()`.
- Result/Artifact evidence: existing Task, Artifact, UsageEvent and routing Work record.
- Control plane: `ResponsibilityRoutingRuntime`; Provider output cannot choose the holder or mutate routing directly.

## Pre-change mixed-source protection

| File | Pre-change SHA-256 | Owned change |
|---|---|---|
| `backend/app/main.py` | `dc0ca996464c9ccb7bfb63bb0055c22a075aef71648086ff875c544f30d87583` | One generic employee-execution branch inside the existing `execute_runtime_business` closure only |
| `backend/app/api/runtime_foundation_router.py` | `04c64f3f6e4c641d34a14dc95e324029e2f2426f5ce20d177564cf255e628980` | Pass the already-injected execution callable into Team Operating router |
| `backend/app/api/team_operating_router.py` | `f26598cca50b09206caa012a9b6c42c5461d2eda53c958c1e337edaec4689b11` | Bounded run/cancel API adapter and automatic loop |
| `backend/app/runtime/responsibility_routing.py` | `ff1a8a9b8a7dc2c2de1ca22219a479bf9f16116339b2fc9790ab32234b7843a8` | Persist execution truth/result contract/idempotency/guards on the existing Work route |
| `backend/app/employee_execution_identity.py` | `dff98996ed6e8d148051a74ae09755034472217b11b112095ce33f9db7cd4499` | No planned change |

Unrelated existing hunks in mixed-source files remain owned by their original development lines and must not be overwritten or staged.

## Allowed files

- `backend/app/main.py` (only the owned generic execution branch)
- `backend/app/api/runtime_foundation_router.py`
- `backend/app/api/team_operating_router.py`
- `backend/app/runtime/responsibility_routing.py`
- `backend/tests/test_team_operating_real_employee_e2e.py`
- `issues/CURIS-TEAM-OPERATING-REAL-EMPLOYEE-E2E-001.md`
- `docs/reviews/CURIS_TEAM_OPERATING_REAL_EMPLOYEE_E2E_REVIEW.md`

## Explicit exclusions

- No new Executor, Provider Runtime, Task store, Result store, workflow engine or Domain lifecycle.
- No RD/XHS/TTK migration or accepted UI redesign.
- No external publishing, paid provider call, production credential, active database, schema migration or Frozen authority change.
- No manual test injection of Employee results.
- No push for this Issue.

## Runtime truth and guards

- Assignment chooses the responsible Employee; capability binding only chooses how that Employee executes.
- Current Executor is set only while a real provider Task is executing and is cleared afterward.
- Provider success is normalized and checked against the pinned Assignment output contract; only an accepted result advances routing.
- Default continuation, Consult return and revision routing are automatic control-plane actions.
- One durable Work may own multiple provider Tasks/Sessions; deterministic execution keys prevent duplicate active/completed execution.
- Bounded provider executions and return counts stop at WAIT instead of looping forever.
- Cancel preserves results/evidence and prevents the next Employee from starting.

## Acceptance

1. Assignment resolves the canonical Employee and its enabled capability binding.
2. Every Employee execution creates a real ResultStore Task and provider execution/session evidence.
3. Callback provenance is VERIFIED before a result can be accepted.
4. Output contract rejects malformed/wrong-type results and never advances routing.
5. Accepted result automatically routes and starts the next Assignment without a manual route API call.
6. Content growth executes at least three distinct Employees and completes one Work.
7. Consult executes a real Employee while the original holder remains unchanged and returns to that holder.
8. Return/revision executes the Developer again, then QA again, with bounded retry and no duplicate Work.
9. Restart resumes from persisted routing truth without repeating an accepted execution or Handoff.
10. Cancel stops continuation and preserves Task/Artifact/Evidence.
11. Pinned workflow version and reference-first bounded context remain stable; full Conversation history is not copied.
12. Existing routing, Shared identity, RD and XHS focused regressions pass on isolated SQLite; active databases remain byte-stable and integrity-valid.

## Implementation result

- Workspace content-growth: closed on the real Task/Orchestrator/session/callback path with three default responsibilities plus one real Leader consult execution.
- Revision loop: real Reviewer rejection returned responsibility to the producing Employee, then re-executed both producer and Reviewer before completion.
- Stop, result-contract failure, missing capability, restart and duplicate-safe read paths are covered.
- Business-scoped RD provider execution was not added: the accepted canonical identity bridge currently requires a Workspace-scoped Runtime Employee. The existing Business routing control plane remains covered by no-regression tests; widening identity scope belongs to a separate Shared authority decision.
- External live model was not called. The acceptance provider is deterministic/local but traverses the real persisted Task, Orchestrator, session usage event, Artifact and callback verification path.
