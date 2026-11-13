# CURIS AUTONOMOUS OPERATING V1 — PHASE 2 SINGLE-CYCLE EXECUTION REVIEW

**Authority Class:** REVIEW
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-21
**Issue:** `issues/20260821_autonomous_operating_v1_phase2_single_cycle_execution_001.md`
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## 1. Scope and ownership

Phase 2 changed only four bounded files:

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/tests/test_autonomous_operating_phase2.py`
3. `issues/20260821_autonomous_operating_v1_phase2_single_cycle_execution_001.md`
4. this Review.

No Team Operating, Responsibility Router, Provider bridge, ResultStore, Schema, state registry, API, frontend or Domain file changed. Preserved unrelated worktree changes were not staged or absorbed.

## 2. Implemented chain

```text
deterministic TRIGGER_CLAIM
→ Phase-1 existing CYCLE
→ approved bounded Plan pin
→ existing RESPONSIBILITY_WORKFLOW
→ same CYCLE used as Team Operating Work
→ real RESPONSIBILITY_ASSIGNMENT / AI_EMPLOYEE
→ existing Employee execution bridge
→ ResultStore Provider Task
→ Provider Session + verified callback provenance
→ Result ref + Artifact + Provider evidence event
→ existing EVIDENCE
→ existing ACCEPTANCE
→ existing Cycle transitions to CLOSED
```

The Series remains `ACTIVE`; `currentCycleRef` is cleared and `lastCycleRef` records the closed Cycle. `successorCycleRef` stays `null`.

## 3. Pre-execution truth

Before Team Operating release, the control bridge verifies:

- Series is `ACTIVE`;
- canonical resolved Workspace and active Business still exist;
- Workspace and Business Goal hashes still match the Phase-1 pins;
- applied Trigger Claim points to the same Cycle;
- Strategy/Envelope control pins remain intact;
- the existing Workspace Leader Assignment remains valid;
- an existing pinned Team Operating workflow resolves exactly that Leader;
- every planned Employee is available;
- every planned Employee has exactly one enabled execution capability binding;
- the bound Provider capability is active;
- no current Employee execution conflicts;
- the Plan is approved, versioned, hashed and has approval provenance.

An enabled Employee capability binding is the existing permission grant used by Team Operating. Capability availability and Employee permission are tested as separate failures. No new permission engine was introduced.

## 4. Result, Evidence and close truth

- Result truth remains the completed ResultStore Provider Task reference.
- Artifact truth remains the Artifact generated from that completed Task.
- Provider evidence remains the verified `usage.task_execution` callback event.
- Phase 2 creates one deterministic existing `EVIDENCE` entity that references Series, Cycle, Workspace, Goal pin, Plan pin, Leader Assignment, Result, Artifact and Provider evidence.
- One deterministic existing `ACCEPTANCE` references that Evidence and result set.
- CEO Acceptance uses the existing Acceptance/Cycle state machines; it is not a Decision Packet and not a next-cycle decision.
- Replays return the same Cycle/Evidence/Acceptance and do not create duplicate Provider Tasks.

## 5. Failure truth

Verified fail-closed cases:

- missing Team Operating workflow;
- unavailable Employee;
- missing/ambiguous Employee permission binding;
- unavailable Provider capability;
- cross-tenant access;
- Provider timeout/failure;
- Provider success with an invalid Result contract, retaining partial Task/Artifact/callback facts;
- duplicate execution/close replay.

Technical failure transitions the same Cycle to `FAILED`, preserves available partial refs, leaves the Series `ACTIVE`, creates no Decision Packet and creates no successor.

Provider in-flight external-process liveness is not invented. Restart proof covers Trigger/Cycle persistence, released Work, completed Result, closed Cycle and failed Cycle. Existing Team Operating restart tests continue to own multi-step in-flight continuation semantics.

## 6. Isolated evidence

All runs used repository-external temporary SQLite with `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` set to the same path before import.

```text
Phase 2 focused E2E
7 passed in 2.81s

Phase 1 + Responsibility Routing + Team Operating Real Employee E2E + DB Safety
26 passed in 7.31s

Python compileall
PASS

git diff --check
PASS
```

The successful controlled-provider E2E produced exactly:

- 1 Cycle;
- 1 Provider Task;
- 1 Provider Session evidence path;
- 1 Artifact;
- 1 EVIDENCE entity;
- 1 ACCEPTANCE entity;
- 0 Decision Packets;
- 0 successor Cycles.

The controlled Provider is an isolated deterministic provider running through the accepted real Employee/Task/Session/callback path. It does not prove external live-model quality, latency or cost.

## 7. Active DB safety

Final fingerprints match the Phase 2 pre-change baseline:

| Path | Size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

Two malformed shell temp-path attempts were rejected by the existing three-variable DB safety guard before test import. They did not initialize repository databases.

## 8. Required answers

1. **Trigger 是否真实启动 existing Cycle？** Yes. The applied canonical Claim owns the same Phase-1 Cycle released to Team Operating.
2. **是否通过真实 Team Operating？** Yes. The existing workflow, Work routing and execute endpoint are used.
3. **是否解析真实 Leader / Employee？** Yes. The Series Leader Assignment must match the workflow Leader and canonical Employee.
4. **是否走真实 Router？** Yes. Existing ResponsibilityRoutingRuntime starts and routes the same Cycle Work.
5. **是否创建真实 Provider Task / Session？** Yes, through the accepted Employee execution bridge and ResultStore. External live-provider quality is not claimed.
6. **是否生成 existing Result？** Yes, a completed ResultStore Task reference.
7. **是否生成 existing Evidence？** Yes, verified callback evidence plus one existing `EVIDENCE` entity.
8. **是否回链 Series/Cycle/Workspace？** Yes; Evidence also pins Goal, Plan, Leader, Result and Artifact refs.
9. **Cycle 是否正常 Close？** Yes, through existing `WAITING_CEO → ACCEPTED → REVIEWING → CLOSED` and Acceptance transitions.
10. **Series 是否保持持续责任？** Yes, `ACTIVE` after success and failure.
11. **failure 是否 fail-closed？** Yes; no false completion or successor.
12. **restart 是否不重复执行？** Yes for released/completed/failed/closed states; accepted Team Operating regression covers multi-step restart continuation.
13. **是否创建第二套 Runtime？** No.
14. **是否执行 Learning？** No.
15. **是否应用 Next-cycle Decision？** No; Acceptance is not a next-cycle Decision.
16. **是否创建 successor？** No; ref remains `null`.
17. **Phase 3 剩什么？** Evaluation/next-cycle decision application, successor authorization, Learning boundaries and cross-domain proof—none are implemented here.

## 9. Git state

No files were staged, committed or pushed. After CEO acceptance, this Phase 2 scope can be committed only with the accepted Phase 1 dependency or after Phase 1 is first archived as its own bounded baseline.

```text
CURIS AUTONOMOUS OPERATING V1
— PHASE 1 ACCEPTED
— PHASE 2 SINGLE-CYCLE REAL EXECUTION IMPLEMENTED
— TRIGGER → CYCLE VERIFIED
— TEAM OPERATING REUSED
— REAL EMPLOYEE / CONTROLLED PROVIDER PATH VERIFIED
— RESULT / EVIDENCE VERIFIED
— CYCLE CLOSE VERIFIED
— SERIES CONTINUES
— RESTART / REPLAY IDEMPOTENCY VERIFIED
— NO LEARNING
— NO NEXT-CYCLE DECISION
— NO SUCCESSOR
— REVIEW REQUIRED
```
