# RD Phase 2B Pre-Implementation Audit

**Status:** Review  
**Date:** 2026-08-16  
**Mode:** Read-only pre-implementation audit. This document does not authorize implementation.  
**Scope:** Multi-Employee, Artifact Review Request, true Handoff and P7 readiness after accepted RD Phase 0/1, Phase 2A Design Fidelity, and closed long-running execution reliability.

## 1. Authority and evidence boundary

### Current authority

- `docs/00_Context/CURRENT_STATE.md`
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` — Frozen P1–P7
- `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` — RD Instance Approved
- `docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md`
- `docs/03_Design/Curis_RD_Workspace_UI_Drift_Audit_v1.md`
- `issues/RD-WORKSPACE-INSTANCE-001.md`
- `reviews/RD-WORKSPACE-INSTANCE-001_review.md`
- `docs/reviews/CURIS_WORKTREE_RECONCILIATION_DECISIONS.md`
- `docs/reviews/CURIS_WORKTREE_REMAINING_RECONCILIATION.md`

### Accepted starting point

This audit accepts, without re-testing or extending, the following current facts:

1. RD Phase 0/1 proves a real chain from Project/Cycle through Employee, Codex,
   real file change, Artifact, Evidence, Result Reference and restart persistence.
2. RD Phase 2A Design Fidelity is accepted for the professional Employee Workstation
   surface.
3. Long-running execution reliability is accepted and closed: submission returns before
   final Codex completion, Runtime owns the execution, duplicate active submission is
   guarded, and final truth survives restart.
4. Computer Access remains truthful: requested, configured and effective are distinct;
   unknown or unverified effective access is not promoted to granted.
5. Phase 2B Multi-Employee, Artifact Review Request, true Handoff and RD P7 have not
   been implemented or accepted.

### Repository evidence boundary

- Audited HEAD: `6f03b5772e3f457e3b423b8b2445138e6715ce3b`.
- The Preserved Development Baseline is a large dirty snapshot. Core RD/shared files are
  modified or untracked and contain mixed XHS, RD and shared Runtime work.
- Code existence is classified separately from safe reuse. An existing shared-looking
  function is not considered a cleanly owned Phase 2B change boundary.
- No Runtime, source, Issue, Review, database, staging area or commit was changed by this
  audit. No acceptance tests were run because this is not an implementation acceptance.

## 2. Executive finding

Phase 2B is feasible without a new Workflow Engine, DAG, Agent system, approval system,
Artifact store or Result model. The current Core already has the execution and identity
substrates needed for a bounded two-employee review slice.

The actual missing capability is narrower:

> One real developer remains the Responsibility Holder while one real reviewer receives
> a persisted, Cycle-scoped Artifact Review Request, runs an existing Employee-bound Task
> against selected Artifact/Evidence, returns a review Result Reference, and does not
> create a Handoff or CEO Decision.

True responsibility Handoff and P7 are both reusable shared primitives, but neither
belongs in the first Phase 2B implementation Issue. Combining all three semantics would
hide whether review, responsibility transfer and CEO judgment are independently correct.

The recommended sequence is therefore:

1. **Phase 2B-1:** Multi-Employee Artifact Review Request.
2. **Phase 2B-2:** one genuine Responsibility Handoff scenario.
3. **Phase 2B-3:** one high-risk RD P7 Decision scenario.

## 3. Current Runtime facts

### 3.1 Accepted single-employee RD execution

The current RD Cycle stores a real `workContext` with Object Owner,
`responsibilityEmployeeRef`, `currentExecutorRef`, activity and status. The accepted
execution path creates a real Task, selects a real Employee/Capability binding, calls the
Codex Adapter, stores changed files/diff/test facts, links Artifact/Evidence/Result refs,
and clears Current Executor after completion or failure.

Two independent places currently enforce a single executable RD assignment:

- `WorkspaceRuntime._rd_execution_assignment()` requires exactly one active Agent Runtime
  assignment for the Cycle.
- `execute_runtime_business()` requires exactly one eligible Company Employee for the
  selected agent capability.

This is correct for the accepted primary execution slice. It is not a reusable
Multi-Employee collaboration model and must not be relaxed into “pick any employee”.

### 3.2 Existing Employee and Task substrate

The current code already persists and scopes:

- `AI_EMPLOYEE`, `ROLE_SLOT`, `CAPABILITY_BINDING` Runtime entities;
- Company Employee instances, affiliations and Employee capability bindings;
- Tasks with Company, Project, Employee, role, capability and status;
- executions, Codex session references, Artifacts and ResultStore evidence/audit facts;
- Workspace projection of employees, roles, bindings, Cycles, handoffs, decisions and
  evidence.

This is enough to execute a reviewer as a second real Employee. It is not evidence that
review assignment, review lifecycle or review UI already exists.

### 3.3 Existing shared Handoff

The shared Runtime has a persisted `HANDOFF` entity and state machine:

```text
CREATED → SENT → ACKNOWLEDGED → COMPLETED
                  ↘ RETURNED / REJECTED
```

XHS uses this primitive for a real content responsibility transfer. The generic
Simulation adapter also contains older handoff-shaped output-to-CEO data, but that is not
the accepted P5 responsibility-transfer contract and must not be reused as RD peer review.

No accepted RD path currently creates a genuine Employee A → Employee B transfer of the
same Responsibility.

### 3.4 Existing shared P7 Decision

The shared Runtime has a persisted `DECISION_PACKET` state machine and XHS has accepted
P7 evidence for one packet shared by Conversation, Banner and Detail, with provenance and
automatic continuation.

RD `close_operating_cycle()` currently creates and applies a simpler close decision in a
single command. It does not leave a durable `WAITING_CEO` interaction and does not satisfy
the full P7 plain-package/provenance contract. It is a post-acceptance close operation,
not the future RD Needs CEO implementation.

## 4. Phase 2B gap matrix

| Capability | Status | Current evidence | Phase 2B implication |
| --- | --- | --- | --- |
| Workspace Employee roster | **EXISTS + REUSABLE** | Workspace snapshot projects real Employees, roles and capability bindings. | Reuse; do not create RD-only Employee records. |
| Employee-bound Task execution | **EXISTS + REUSABLE** | ResultStore/Orchestrator/Agent Adapter accept a real Employee and capability. | Reuse for reviewer execution. |
| Primary Responsibility Holder | **EXISTS + REUSABLE** | Accepted Cycle `workContext` persists holder independently of executor. | Keep developer as holder throughout Artifact Review. |
| Current Executor truth | **EXISTS + REUSABLE** | Primary execution sets/clears executor around real Codex activity. | Review needs its own truthful executor projection; do not overwrite holder. |
| Multiple Employee Workstations | **PARTIAL** | UI can render multiple Cycles/stations and the Workspace can contain multiple Employees. | This does not prove two Employees collaborating on one Cycle/Artifact. |
| Multi-Employee assignment | **PARTIAL / P0 GAP** | Primary path intentionally requires exactly one active agent assignment. | Add explicit reviewer selection/validation; do not weaken primary assignment uniqueness. |
| Artifact and Evidence | **EXISTS + REUSABLE** | Real code-change Artifact, diff, test evidence and session refs persist. | Review selected immutable refs; do not copy terminal output into Conversation. |
| Result Reference | **EXISTS + REUSABLE** | Phase 2A Utility and Conversation reference real results. | Add review Result Reference to the same Cycle/workstation. |
| Artifact Review Request | **MISSING / P0 GAP** | No Runtime command, persisted request record, API, UI or focused test exists. | Implement one Cycle-scoped request with stable identity and lifecycle. |
| Reviewer context assembly | **MISSING / P0 GAP** | Current RD executor builds implementation context from Cycle instruction/files/tests. | Reviewer receives only selected Artifact/Evidence, acceptance context and relevant files. |
| Reviewer result/evidence | **MISSING / P0 GAP** | No peer-review result type or Cycle link exists. | Persist reviewer Task, status, review summary, Result refs and evidence. |
| Review idempotency | **MISSING / P0 GAP** | Long-running duplicate guard covers active primary execution only. | Same Cycle + same Artifact version must not create two active review Tasks. |
| Artifact Review UI | **MISSING / P0 GAP** | No send-for-review action, reviewer state or review result surface. | Add only to the existing RD Workstation/Utility hierarchy. |
| True Responsibility Handoff | **EXISTS SHARED / MISSING IN RD** | Shared entity/machine exists; RD does not use it for a real transfer. | Defer to Phase 2B-2; never use it for Artifact Review. |
| P7 Decision Packet | **EXISTS SHARED / MISSING IN RD** | Shared/XHS implementation exists; RD close packet is not a waiting P7 flow. | Defer to Phase 2B-3 and use one real high-risk decision. |
| Restart persistence | **PARTIAL** | Employee/Task/Artifact/Evidence/Cycle persist; no review object exists to recover. | Prove request/reviewer Task/result survive same isolated SQLite restart. |
| Failure truth | **PARTIAL** | Primary Codex failure truth is accepted. | Review failure must preserve request and evidence without changing holder or creating Handoff. |

## 5. Recommended Runtime composition

### 5.1 Reuse; do not rebuild

Use the existing:

- Cycle as the stable RD Responsibility/work object;
- `workContext` for the original Responsibility Holder and primary Current Executor;
- Company Employee, Role and Capability binding validation;
- Task/Orchestrator/Codex path for the reviewer execution;
- ResultStore Artifact/Execution/audit facts;
- Runtime `EVIDENCE` and P6 Result Reference projection;
- long-running submit/observe/duplicate-protection pattern;
- isolated SQLite persistence and restart reconciliation.

### 5.2 Minimal new Phase 2B-1 semantics

Add one persisted **Cycle-scoped Artifact Review Request record**, not a new generic
workflow subsystem. It needs only:

- stable request ref;
- Cycle/work item ref;
- selected Artifact and Evidence refs;
- author/original Responsibility Holder ref;
- reviewer Employee ref;
- reviewer Task/session refs;
- status: requested, reviewing, approved, changes requested or failed;
- review summary and Result/Evidence refs;
- created/updated timestamps.

The first implementation should prefer a small record on the existing Cycle Runtime
data plus a real reviewer Task ref. A new global Runtime entity/table is not justified
until independent querying, multiple concurrent reviews or cross-Workspace reuse is a
proven requirement.

### 5.3 Responsibility and executor rules

For Artifact Review:

```text
Original Cycle Responsibility Holder = developer (unchanged)
Original Cycle Current Executor       = none after implementation completes
Review Request reviewer               = reviewer Employee
Review Request Current Executor       = reviewer only while reviewer Task runs
HANDOFF count                         = 0
DECISION_PACKET count                 = 0
```

If the reviewer requests changes, the developer still holds the original Responsibility;
the Runtime returns the review result to that workstation. No responsibility “return” is
required because no transfer happened.

### 5.4 Minimal reviewer context

The reviewer Task should receive only:

- the selected immutable Artifact/diff reference;
- relevant test Evidence and acceptance expectation;
- the minimum relevant file refs;
- the current Project/Cycle identity and review question;
- truthful Computer Access request/configuration/effective snapshot.

Do not inject the full Project history, all Conversations or every Artifact. Do not ask
the reviewer to modify files in the first review slice; the first slice is read/review and
returns a real review result.

## 6. Handoff and P7 follow-on boundaries

### 6.1 Phase 2B-2 — true Handoff only

A later bounded Issue may prove one explicit transfer:

```text
Employee A holds Cycle Responsibility
→ persisted HANDOFF CREATED/SENT
→ Employee B ACKNOWLEDGES
→ holder changes to Employee B
→ Current Executor remains none until B actually starts
```

Rejected/returned handoff must keep or restore the original holder. Review requests,
CEO escalation and generic Simulation output must not be counted as this proof.

### 6.2 Phase 2B-3 — RD P7 only

A later bounded Issue should use one genuinely high-risk RD decision and reuse the shared
`DECISION_PACKET`:

- Conversation, Layer 0 Banner and Layer 1 Detail reference the same packet;
- Layer 0 offers `查看方案 / 暂缓`, not direct approval;
- impact/risk/cost/recommendation carry FACT/POLICY/EVIDENCE/EST/UNK provenance;
- professional evidence remains in P6 Utility;
- CEO choice automatically resumes the original Responsibility;
- no new Handoff is created.

The existing synchronous Cycle close packet is not the implementation shortcut for this
flow.

## 7. Mixed-source risk

### 7.1 Current mixed seams

The following Phase 2B-adjacent files are already mixed or untracked in the Preserved
Development Baseline:

- `backend/app/main.py` — tracked modification; contains provider, Task, RD execution and
  multiple initiative seams.
- `backend/app/runtime/states.py`, `backend/app/runtime/registry.py` — tracked shared
  Runtime modifications.
- `backend/app/runtime/foundation.py`, `backend/app/runtime/workspace.py`,
  `backend/app/runtime/execution_adapter.py` — untracked shared/domain Runtime source.
- `backend/app/api/runtime_foundation_router.py` — untracked XHS/RD/shared API surface.
- `frontend/lib/runtimeApi.js`, `frontend/components/workspace/`,
  `frontend/components/rd/` — untracked shared and RD UI source.
- Current RD and XHS focused tests and Issue/Review records are also untracked.

### 7.2 Consequences

- Do not reset, clean, checkout, replace whole files or stage whole mixed files.
- Do not treat “the file exists” as a clean base or accepted ownership boundary.
- The next Issue must record exact pre-change hashes and identify owned functions/hunks,
  not just file names.
- A successful Phase 2B test does not make unrelated mixed changes committable.
- Shared `states.py`/`registry.py` changes should be avoided in Phase 2B-1; a new generic
  `ARTIFACT_REVIEW_REQUEST` machine would expand both semantics and reconciliation risk.
- `main.py` is the highest-risk seam. Reuse its existing execution callback with the
  smallest bounded reviewer branch only if no existing service command can perform the
  Task; do not refactor the app factory during this Issue.

## 8. P0 blockers before implementation

| Blocker | Why it blocks truthful Phase 2B-1 | Required precondition |
| --- | --- | --- |
| No persisted review request | UI state alone cannot survive restart or prevent duplicates. | Cycle-scoped request record and status transition contract. |
| No explicit reviewer selection | Relaxing “exactly one assignment” would select ambiguously. | Validate one real reviewer Employee and its capability without changing primary holder selection. |
| No review execution context | Primary implementation prompt is not a review contract. | Minimal selected Artifact/Evidence/acceptance payload. |
| No review result link | Reviewer text could be mistaken for Evidence. | Real reviewer Task + Result/Evidence refs linked to the Cycle request. |
| Mixed-source baseline | Whole-file changes could absorb unrelated work. | Bounded Issue with exact functions/hunks, isolated DB and no whole-file staging. |

Handoff and P7 are not Phase 2B-1 blockers because they are intentionally excluded from
the first slice.

## 9. Recommended next minimum Issue

### Proposed Issue

`RD-PHASE-2B-ARTIFACT-REVIEW-001`

### Goal

Prove one real two-employee Artifact Review chain without transferring the original
Responsibility:

```text
Accepted RD Cycle with real developer Artifact/Evidence
→ select one real reviewer Employee
→ create one persisted Cycle-scoped Artifact Review Request
→ submit one real reviewer Task through existing Employee/Agent binding
→ observe requested/reviewing/completed-or-failed truth
→ persist review Evidence and Result Reference
→ return review result to the original developer workstation
→ restart and read the same request/task/result
```

### Recommended bounded files

The Issue should start with these candidates and narrow them further to exact owned
functions/hunks after preflight:

```text
backend/app/runtime/workspace.py
backend/app/api/runtime_foundation_router.py
backend/app/main.py                         # reviewer execution branch only, if unavoidable
backend/tests/test_rd_artifact_review.py    # new focused test
frontend/components/rd/RdWorkspacePhaseTwo.js
frontend/components/rd/RdArtifactReview.js # optional focused component; only if it reduces mixed edits
frontend/lib/runtimeApi.js
frontend/tests/rdArtifactReview.test.mjs    # new focused test
issues/RD-PHASE-2B-ARTIFACT-REVIEW-001.md
reviews/RD-PHASE-2B-ARTIFACT-REVIEW-001_review.md
```

Do not include `states.py`, `registry.py` or `foundation.py` unless implementation proves
that a Cycle-scoped record cannot satisfy persistence/idempotency. That discovery must
pause the Issue for a focused Runtime architecture review rather than silently creating
a new shared primitive.

### Explicit exclusions

- true Responsibility Handoff;
- CEO Decision P7;
- Queue/Bottleneck or Organization Router;
- multiple concurrent reviewers or review rounds;
- reviewer file modification/auto-fix;
- new Workflow Engine, DAG or generic approval/review engine;
- Computer Access P1/P2 or Full Access;
- XHS, TTK, Frozen contracts, Product Blueprint and active databases.

### Minimum acceptance

1. Two distinct real Employees are visible in the same RD Workspace and are bound to the
   correct existing capabilities.
2. Developer remains original Cycle Responsibility Holder before, during and after review.
3. One request creates one reviewer Task; duplicate active submission returns the same
   request/Task and starts no second agent session.
4. Reviewer Current Executor exists only while the real reviewer Task is active.
5. Review result is backed by real Task output/Evidence and appears through a Result
   Reference, not as fabricated Conversation truth.
6. Approved, changes-requested and failed review outcomes are distinguishable and durable.
7. Handoff count remains zero and Decision Packet count remains zero for this slice.
8. Same isolated SQLite stop/restart restores request, employees, reviewer Task, result and
   truthful inactive executor state.
9. Primary RD execution, long-running reliability, Computer Access truth and accepted XHS
   behavior do not regress.

## 10. Review decision requested

Approve only the bounded **Phase 2B-1 Artifact Review** Issue above. Do not authorize
Handoff or P7 in the same implementation batch.

`RD PHASE 2B PRE-IMPLEMENTATION AUDIT REVIEW REQUIRED`
