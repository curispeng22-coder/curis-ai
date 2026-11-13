# CURIS TEAM OPERATING REAL EMPLOYEE E2E REVIEW

Status: ACCEPTED
Authority Class: REVIEW
Issue: `CURIS-TEAM-OPERATING-REAL-EMPLOYEE-E2E-001`

## Verdict

`IMPLEMENTED / ACCEPTED`

The Workspace content-growth slice closes the previously missing control/data loop. Evidence uses an approved deterministic local provider, not an external live model, but it traverses the production Runtime path: canonical Employee identity, enabled capability binding, ResultStore Task, Orchestrator, provider session evidence, Artifact, callback verification, result-contract validation and automatic Responsibility routing.

## Acceptance answers

1. **Router starts execution:** `POST .../works/{work_ref}/execute` reads the pinned Assignment and asks the already-injected Runtime execution callable to submit/run that Assignment's canonical Employee.
2. **Existing bridge:** `EmployeeExecutionIdentity + ResultStore + Orchestrator + TaskExecutionControlService`; no Executor or Task/Result store was added.
3. **Provider Task/Session:** yes. The accepted content Work created 4 persisted Tasks and 4 distinct persisted provider session references.
4. **Callback provenance:** yes. All 4 callbacks were `VERIFIED` against Company Employee, enabled binding, Task assignment and `usage.task_execution` evidence.
5. **Result contract:** provider output is normalized to `ACCEPTED/REJECTED/FAILED`, checked against the pinned Assignment `resultType`, Task completion and verified callback. A provider-success/malformed-result test leaves Work `WAITING` and does not route.
6. **Automatic Router wake-up:** yes. Accepted result calls the existing deterministic Router immediately; no manual route API is needed.
7. **Automatic next Employee:** yes. Default content flow completed across topic, research and copy Employees; Leader consult was also a real provider execution.
8. **Consult truth:** research remained Holder while Leader was Current Executor; one real consult Task/Session returned a persisted result to research; Handoff count did not increase for Consult.
9. **Return truth:** a real quality Employee rejected once; Router atomically handed responsibility back to copy; copy re-executed; quality re-executed and accepted. Four Tasks, three Handoffs, one Work.
10. **Work cost:** accepted content Work: 4 Employee executions, 4 Tasks, 4 sessions, 2 Handoffs, 1 Consult, 3,411 context chars / 3,535 bytes / 22 refs, 0 hydrated bodies, no Conversation history copy. Provider-reported token count was synthetic local-test metadata and is not presented as external-model usage.
11. **Restart:** after topic accepted and responsibility moved to research, Runtime/App restart restored pinned version, Holder, result and Handoff. Resume created only the remaining Tasks; re-reading/executing the completed Work created no duplicate Task.
12. **Stop/Cancel:** both between-Assignment cancellation and cancellation during a blocking real provider Task were exercised. Task became `CANCELLED`, Work became `CANCELLED`, Current Executor cleared, no next Employee or orphan Task appeared, prior truth remained.
13. **Loop guard:** `maxReturns` stopped an always-rejected revision loop in `WAITING` after the bounded count; the Work-level provider execution ceiling is persisted and fail-closed.
14. **Content Growth:** yes; complete multi-Employee Runtime closure to a ready-to-publish content package contract. No XHS publishing side effect was attempted.
15. **RD:** Shared/Business routing no-regression passes, but provider-native Business-scope RD execution was not added because the accepted identity bridge currently resolves Workspace-scoped Runtime Employees. No unsafe scope widening was guessed.
16. **Active DB:** untouched. Both repository SQLite files retained size, mtime and SHA-256; both returned `integrity_check=ok`.
17. **New Runtime:** none. The existing Responsibility Router gained persisted execution records/guards; the app closure gained one shared execution-ref branch over existing Task/Orchestrator primitives.
18. **Original断点:** closed for Workspace-scoped Team Operating. Router now both selects the Employee and runs the Employee through the trusted provider path.

## Runtime evidence

Isolated evidence database: `/tmp/curis-team-evidence.bKlerH/e2e.sqlite`

```text
status=COMPLETED
pinned_version=1
holder_after_restart_point=employee-research
employee_executions=4
provider_tasks=4
provider_sessions=4
verified_callbacks=4
handoffs=2
consults=1
context_chars=3411
context_bytes=3535
context_refs=22
hydrated_bodies=0
conversation_copied=false
integrity=ok
```

This proves the real Runtime path, not an external paid/live model call.

## Tests

- `backend/tests/test_team_operating_real_employee_e2e.py`: **7 passed**
  - content Work + restart + Consult + completion
  - duplicate-safe completed Work
  - cancellation between Employees
  - real Return/revision/recheck
  - bounded Return guard
  - provider success rejected by invalid Result Contract
  - missing capability fail-closed
  - active provider Task cancellation
- Shared/RD/DB-safety regression: **14 passed**
  - `test_team_operating_adapter.py`
  - `test_responsibility_routing_runtime.py`
  - `test_employee_execution_identity.py`
  - `test_rd_phase2b_e2e_closure.py`
  - `test_backend_test_db_safety.py`
- Python compile: passed.
- `git diff --check`: passed.

## Active database proof

| Database | Size | mtime | SHA-256 | Integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1,232,896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1,277,952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

## Changed files

- `backend/app/main.py` — owned `team_employee:auto` branch only; mixed-source neighbors preserved.
- `backend/app/api/runtime_foundation_router.py`
- `backend/app/api/team_operating_router.py`
- `backend/app/runtime/responsibility_routing.py`
- `backend/tests/test_team_operating_real_employee_e2e.py`
- `issues/CURIS-TEAM-OPERATING-REAL-EMPLOYEE-E2E-001.md`
- `docs/reviews/CURIS_TEAM_OPERATING_REAL_EMPLOYEE_E2E_REVIEW.md`

## Remaining boundary

- Business-scope provider execution needs an approved identity-scope extension before an RD autonomous slice can be truthful.
- External live provider quality/cost is unverified and was deliberately not invoked.
- No frontend redesign or token dashboard was added; existing Team Operating projection already exposes Holder, Current Executor and Work status.
- Workspace-scoped Real Employee Execution is accepted. Business-scope Provider Execution is not implemented; external live provider quality/cost remains unverified. The deterministic local provider is evidence for the real persisted execution path, not an external live model.
- The bounded baseline commit is local only and is not pushed.
