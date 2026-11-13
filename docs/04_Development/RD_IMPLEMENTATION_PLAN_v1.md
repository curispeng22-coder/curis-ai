# RD Implementation Plan v1

**Status:** Review  
**Date:** 2026-08-16  
**Precondition:** Review together with `RD_IMPLEMENTATION_GAP_AUDIT.md`, the Frozen Shell/Shared P1–P7 contract and the Approved RD Instance Spec.  
**Authority effect:** This plan authorizes no production change by itself. Formal implementation requires a bounded Issue, Allowed Files, Review record and isolated Runtime Simulation.  
**Non-goals:** No Product Blueprint/Frozen contract/RD Approved Spec/XHS/TTK change; no Computer Access P1/P2; no Workflow Engine, DAG, fake Codex run or fake Evidence.

## 1. Target first vertical slice

The first slice proves one real responsibility end to end before multi-employee
collaboration or complete RD product breadth:

```text
进入 RD Workspace
→ 选择一个真实 Company Project / Cycle work object
→ 一名真实 AI Employee 接受 Responsibility
→ Composer 提交一条 bounded instruction
→ Existing Execution Binding selects Codex
→ New Codex session records truthful Computer Access snapshot
→ Codex works only inside the declared workspace boundary
→ Runtime verifies actual file/diff/test postconditions
→ Existing ResultStore persists Task / Execution / Artifact / Usage
→ Workspace Runtime links Evidence and Result Reference to the same Cycle
→ Employee execution ends; Current Executor becomes none
→ reload / Runtime restart restores the same Project, Cycle, Employee and result chain
```

The slice may end in completed, waiting or failed. A failed truthful execution with a
durable recovery path is acceptable evidence; a fabricated success is not.

### First-slice exclusions

- No multi-employee automatic choreography.
- No Artifact Review Request until the single-executor result chain is proven.
- No high-risk P7 decision unless the chosen scenario actually requires CEO judgment.
- No Full Computer Access.
- No XHS Calendar/Note code and no generic Workflow editor.

## 2. Minimal runtime composition

### Business and execution objects

| Layer | Object | Role in RD |
| --- | --- | --- |
| RD domain | Company `Project` | Stable project identity and goal. Existing model; no new RD project table. |
| RD Runtime | `CYCLE` | First-slice work object and stable Responsibility ID. Stores project ref, title, outcome, holder/executor work context and child refs. |
| Company OS shared | `AI_EMPLOYEE`, `ROLE_SLOT`, `CAPABILITY_BINDING` | Real responsible employee and legal execution supply. |
| Execution substrate | `Task`, `Execution`, Codex session | Performs the bounded instruction. Not the Workspace entry or business object. |
| Result substrate | Task `Artifact`, Runtime `EVIDENCE` | Actual output/file/test facts and their verification status. |
| Company OS shared | `HANDOFF`, `DECISION_PACKET` | True responsibility transfer and P7 CEO decision only when their semantics apply. |
| RD domain | Artifact Review Request | Reviewer request/response without changing Responsibility Holder. Stored in existing Runtime entity graph. |

### Required links

```text
Workspace
  → Project reference
  → CYCLE (Responsibility ID)
    → Responsibility Holder (AI_EMPLOYEE)
    → Current Executor (AI_EMPLOYEE only while Task is active)
    → Task
      → Execution / Codex session
      → Artifact
      → Computer Access snapshot / Usage audit
    → EVIDENCE / Result Reference
    → Artifact Review Request OR HANDOFF
    → DECISION_PACKET when Needs CEO
```

Do not add a new table for this graph. Use current `runtime_entities`, `runtime_links`,
Task/Artifact storage and their existing Company/tenant scope. If atomic scoping cannot
be proven during Phase 0, stop implementation and open a focused architecture review
instead of weakening isolation.

## 3. Shared reuse boundary

### Reuse from accepted XHS

- `WorkspacePaneShell`: layout, pane headers, T1/T2/T3, continuous pointer resize,
  adaptive surface, compact overlays, per-Workspace preference, Utility maximize.
- Shared Employee Presence, responsibility projection, Handoff Event, Result Reference,
  System Activity and P7 Decision components/runtime semantics.
- Persistence/testing pattern: isolated SQLite, Browser + packaged Desktop, reload and
  Runtime restart, same-object proof.

### Do not copy from XHS

- Calendar, Month View, Note Split, Note editor or ContentItem fields.
- ContentItem lifecycle, review rules, scheduling, publishing or analytics.
- XHS Context title/content, XHS Utility preview or XHS wording.
- XHS-specific Runtime command names or domain payloads.

The shared shell currently embeds XHS labels. The implementation may replace those
strings with props while retaining the current XHS values as defaults. It may not fork
the file or alter accepted XHS behavior.

## 4. Phase plan

### Phase 0 — Migration safety and bounded Issue

| Item | Plan |
| --- | --- |
| Modify directories | `issues/`, `reviews/`, `docs/04_Development/`, focused test fixtures only. No production code until the Issue is approved. |
| Proposed modules | `RD-WORKSPACE-INSTANCE-001` Issue; Review skeleton; exact Allowed Files; isolated SQLite and temporary repository fixture; current RD/XHS/TTK route baseline. |
| Dependencies | This plan; Frozen Shell/P1–P7; Approved RD Spec; XHS acceptance; accepted Computer Access P0. |
| Risks | The working tree is heavily dirty/untracked. Existing changes belong to the user and cannot be overwritten or treated as a clean baseline. Some accepted implementation files are untracked in this checkout. |
| Acceptance | Issue excludes activity DB, Blueprint, Frozen design files, XHS domain files, TTK and global TerraShell refactor; fresh DB/repo paths are explicit; current RD/XHS/TTK focused tests are recorded before edits. |

Candidate Allowed Files must be narrowed, not expanded casually:

```text
frontend/app/ceo-office/workspace/software/page.js
frontend/components/workspace/WorkspacePaneShell.js
frontend/components/workspace/<shared accepted semantic components only>
frontend/components/rd/**
frontend/lib/runtimeApi.js
frontend/tests/<rd and shared-shell focused tests>
backend/app/runtime/workspace.py
backend/app/runtime/foundation.py            # only if RD review-request entity registration is required
backend/app/runtime/registry.py              # only its bounded review-request transitions
backend/app/api/runtime_foundation_router.py
backend/app/main.py                          # narrow existing Task/Orchestrator callback injection only
backend/tests/<rd workspace focused tests>
issues/RD-WORKSPACE-INSTANCE-001.md
reviews/RD-WORKSPACE-INSTANCE-001_review.md
```

Explicit exclusions:

```text
data/curis.sqlite
docs/01_Product/Curis_Product_Blueprint.html
docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md
docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md
frontend/components/xhs/**
frontend/app/ceo-office/workspace/xhs/**
frontend/app/ceo-office/workspace/shortvideo/**
frontend/components/terra/TerraShell.js
curis-ui-prototype/**
Computer Access P1/P2 and non-Codex adapters
```

### Phase 1 — Shared shell migration for the RD route

| Item | Plan |
| --- | --- |
| Modify directories | RD route, `frontend/components/rd/`, the existing shared shell, focused frontend tests. |
| New/modified modules | `RdWorkspaceInstance`; prop-based shell titles/actions; RD Context container; RD Utility container; real-object search provider over currently loaded scoped data. |
| Dependencies | Accepted shared shell and design tokens; real Workspace selection from current Runtime snapshot. |
| Risks | Forking the shell, changing global navigation, retaining XHS labels, or calling a placeholder search “implemented”. |
| Acceptance | RD alone opens in the shared four-pane shell; pane-local headers, T1/T2/T3, resize, Utility maximize and compact behavior work; XHS tests remain green; search returns only real scoped objects or an honest empty state; no RD project/result mock data. |

Phase 1 presents a truthful empty/legacy-migration state if no RD work object exists. It
does not expose generic Simulation cards as the approved office.

### Phase 2 — RD Project, Cycle and Employee Workstation

| Item | Plan |
| --- | --- |
| Modify directories | `frontend/components/rd/`, Runtime API client, Workspace Runtime/router, focused backend/frontend tests. |
| New/modified modules | Project/Cycle selector; `RdEmployeeWorkstation`; Conversation/Composer shell; RD Context (project/current responsibility/files/recent objects); RD Utility tabs (Source/Diff/Preview) with honest empty states; Cycle work-context commands/projection. |
| Dependencies | Real Company Project, Operating RD Workspace, one active Role Slot/AI Employee/Binding. |
| Risks | Treating all Workspace employees as current executors; reviving fixed `完善 Curis`; displaying nonexistent files/diffs/tests. |
| Acceptance | CEO selects or creates a real project/work object with a supplied goal; Cycle ID is stable Responsibility ID; holder is a real employee; executor is none before execution; waiting and idle are distinguishable; reload restores selection and context; no code execution yet required. |

Minimum Cycle data additions use existing `data_json`, not schema columns:

```text
projectRef
workItemTitle
workContext:
  objectOwnerRef
  responsibilityEmployeeRef
  currentExecutorRef
  status
  activity
  systemActivity
  taskRef
  resultRefs
  updatedAt
```

### Phase 3 — First real Codex vertical slice

| Item | Plan |
| --- | --- |
| Modify directories | Workspace Runtime/router, narrow `main.py` injection, RD components/API client and focused tests. ResultStore/Orchestrator should remain unchanged unless a proven missing fact cannot be read. |
| New/modified modules | Cycle execution command that creates a Company/Project/Employee/Capability-bound Task through the existing factory; child Task/Execution/Artifact projection; Result Reference and failure/recovery card. |
| Dependencies | Detected/available Codex binding, real employee binding, writable temporary repo, declared target scope/test command, Computer Access P0. |
| Risks | Directly invoking Codex outside binding; manual `workflow_run`; fallback to another tool; claiming effective permission; creating Evidence on failure; losing task/session refs on restart. |
| Acceptance | One Cycle starts one real Task; one real employee is Current Executor only while running; Codex new-session snapshot is preserved as requested/configured/UNKNOWN-effective; actual file hash/diff/test evidence is recorded; completed/failed/waiting produces no fake facts; executor becomes none at terminal/waiting; same Cycle/Task/Artifact/Evidence survive Runtime restart. |

Computer Access acceptance in this phase:

- `ASK_WHEN_NEEDED` may inspect under `read-only`; a write attempt must fail honestly.
- `AUTO_WITHIN_BOUNDARY` may request `workspace-write`; actual changed files and tests are
  verified separately while effective access remains `UNKNOWN`.
- Resume never inherits effective state and remains
  `NOT_CONFIGURABLE / UNVERIFIED / UNKNOWN` where Codex cannot inspect it.
- Full request is `UNSUPPORTED` before process launch, with no fallback.

Phase 3 is the first product-bearing implementation milestone. Passing Shell or static
workstation tests alone is not Phase 3 completion.

### Phase 4 — Multi-employee collaboration, Artifact Review and Handoff

| Item | Plan |
| --- | --- |
| Modify directories | Existing Runtime entity registration/state machine only as needed, Workspace Runtime/router, RD components and focused tests. |
| New/modified modules | Minimal `ARTIFACT_REVIEW_REQUEST` Runtime entity; reviewer request/response; multi-workstation stack; true responsibility Handoff command/view. |
| Dependencies | Phase 3 real Artifact/Result refs and at least two real Workspace employees. |
| Risks | Making review a Handoff; changing holder while a reviewer only comments; using Agent execution state as employee presence; introducing a generic review/workflow engine. |
| Acceptance | Developer remains holder during review; reviewer presence is tied to the review request and Artifact refs; response returns findings without ownership transfer; only explicit A → B transfer creates one persisted Handoff; waiting preserves holder and clears executor; restart preserves review and handoff history. |

Minimal Artifact Review Request states:

```text
REQUESTED → IN_REVIEW → RESPONDED → CLOSED
                     ↘ FAILED
```

These are RD-domain states in the current Runtime graph, not Company OS Handoff states
and not a new approval system.

### Phase 5 — P7 Decision, System Activity and complete Result Utility

| Item | Plan |
| --- | --- |
| Modify directories | Shared P7/Result/System Activity components only if they are already domain-neutral; RD Runtime command/projection and RD UI/tests. |
| New/modified modules | RD P7 package builder using the existing single `DECISION_PACKET`; Conversation decision reference; high-risk Banner; automatic continuation; Source/Diff/Preview evidence projection; build/test System Activity where no employee executes. |
| Dependencies | Phase 3 result chain and Phase 4 collaboration semantics. |
| Risks | Creating a second RD decision; exposing CLI/stack in Conversation; fabricating time/cost/risk; Layer 0 approving irreversible work; treating test/index activity as an employee. |
| Acceptance | Banner, Conversation and Detail reference one packet; high-risk Layer 0 only 查看方案/暂缓; Impact/Risk/Cost/Recommendation/Reason carry FACT/POLICY/EVIDENCE/EST/UNK provenance; CEO choice applies a legal transition and Runtime automatically restores the original responsibility; executor remains none during CEO wait; Utility opens only real Artifact/Evidence. |

### Phase 6 — Acceptance and no-regression

| Item | Plan |
| --- | --- |
| Modify directories | Focused tests, bounded Review and evidence paths only. No feature work. |
| Modules | Full isolated Runtime Simulation, Browser, current-source packaged Desktop, restart/recovery and no-regression checks. |
| Dependencies | Phases 1–5. |
| Risks | Reusing old screenshots/DB, browser hitting another service, static UI accepted as Runtime, Desktop build from a different source root, XHS regression hidden by route-only checks. |
| Acceptance | Complete approved path is exercised with fresh ports, fresh isolated SQLite and a temporary repo; same DB/source manifest is recorded; Browser and packaged Desktop show no route/IPC/resource/console errors; restart preserves the same object IDs and evidence; XHS accepted slice and TTK legacy route have no regression. |

## 5. Runtime transition rules

### Responsibility and executor

| Situation | Holder | Executor | Status | Rule |
| --- | --- | --- | --- | --- |
| Work assigned, not running | Employee A | none | idle | Assignment is not execution. |
| Codex Task running for A | Employee A | Employee A | working | Executor exists only with a real active Task/session. |
| Waiting for input/capability | Employee A | none | waiting | Preserve owner, dependency, next action and resume point. |
| Codex failed | Employee A | none | failed | No success Artifact/Evidence; preserve same Cycle/Task and recovery facts. |
| Artifact review by B | Employee A | B only while B is actively reviewing | working/waiting | Review request does not transfer holder. |
| True handoff A → B | Employee B after acknowledgement | none or B if execution begins | waiting/working | One persisted Handoff changes the holder. |
| Needs CEO | Employee holder remains | none | needs_ceo | CEO is not executor. |
| Completed | Employee holder may remain as historical owner | none | completed | Employee presence must not imply the Agent is still running. |

### P7 decision

Needs CEO is derived from a work object that remains at its legal RD checkpoint plus a
linked `DECISION_PACKET=WAITING_CEO`. It is not a new global Cycle state.

One Decision Packet supplies:

- Conversation: CEO-readable summary + reference only.
- Layer 0 Banner: attention and complexity-appropriate actions.
- Layer 1: plain package with happened, non-automatic reason, options,
  impact/risk/cost, recommendation/reason, CEO choice and automatic continuation.
- Layer 2: existing Result Reference / Utility evidence.

Decision is never a Handoff. Artifact Review Request is neither Decision nor Handoff.

## 6. Focused acceptance scenarios

1. **Empty RD office:** no project/cycle means no default `完善 Curis`, no mock employee,
   no fake file or test result; CEO receives one clear creation action.
2. **Read-only new session:** real Codex session records requested/configured/UNKNOWN;
   no file mutation is claimed; executor clears on completion/failure.
3. **Bounded write new session:** temporary repo change and test create real Task,
   Execution, Artifact, access snapshot and Cycle Evidence refs. Actual diff/test is
   verified while effective access stays `UNKNOWN`.
4. **Failure/recovery:** failed Codex/task keeps the same Cycle/Task, holder, failure,
   return point and retry boundary; no success Evidence; restart and retry do not spawn
   a replacement responsibility.
5. **Resume truth:** resume does not reuse old sandbox/effective state; snapshot remains
   NOT_CONFIGURABLE/UNVERIFIED/UNKNOWN when provider verification is unavailable.
6. **Full fail-closed:** request is rejected before Codex launch; no downgrade/fallback.
7. **Artifact review:** reviewer responds to real Artifact refs while original holder
   remains; no Handoff entity is created.
8. **True Handoff:** explicit transfer creates one Handoff and changes holder only after
   acknowledgement.
9. **P7 high risk:** Banner/Conversation/Detail share one packet; Layer 0 has no approve;
   provenance is preserved; CEO choice auto-resumes the original responsibility.
10. **Persistence/isolation:** Company A cannot read Company B Project/Cycle/Task refs;
    Runtime restart preserves history but does not re-verify Computer Access.
11. **No regression:** XHS Calendar/Note/Handoff/P7/resize/Decision acceptance tests and
    RD/TTK route checks remain green; no XHS or TTK source changes.

## 7. Test and evidence plan

### Focused backend

- Cycle creation contains no fixed task and enforces Company/Workspace/Project scope.
- Single-holder start and task-bound executor projection.
- Real injected Task/Orchestrator success, failure, waiting and restart paths.
- Artifact/Evidence link integrity and no success evidence on failure.
- Computer Access new/resume/full truth carried unchanged.
- Artifact Review Request versus Handoff invariants.
- One P7 packet, provenance and automatic continuation.
- Cross-tenant/company/workspace rejection.

### Focused frontend

- Shared shell props preserve XHS defaults.
- RD four-pane, pane titles, T1/T2/T3, pointer resize, maximize, compact layout.
- Real search results/empty state.
- Holder/executor/waiting/failed/idle rendering.
- Conversation/Composer loading, failure and stop states.
- Artifact review, Handoff and high-risk P7 actions.
- Utility real/unknown evidence states.

### Runtime/Browser/Desktop

- Fresh temporary SQLite; never `data/curis.sqlite`.
- Fresh temporary repository with explicit allowed files and test command.
- Browser uses recorded fresh ports and confirms the selected Company/Workspace.
- Stop/restart backend on the same DB, then read the same object IDs.
- Build/launch packaged Desktop from the same source manifest.
- Capture no Secret, private prompt or raw sensitive CLI output.

## 8. Risks and controls

| Risk | Control |
| --- | --- |
| Dirty source tree obscures ownership | Phase 0 records exact pre-existing status and only edits approved files; no reset/checkout/stage/commit/push. |
| XHS regression from shared shell change | Props with current XHS values as defaults; accepted XHS focused tests and Desktop smoke before RD acceptance. |
| Cycle and Task scope drift | Validate tenant/company/project/workspace before creation and every read; persist explicit refs; reject cross-scope IDs. |
| Effective permission overclaim | Store the accepted P0 snapshot unchanged; outcome evidence is separate from permission evidence. |
| Legacy fixture mistaken for real execution | Do not route the new RD slice through fixed RealRD evidence fixtures; use real bound Codex and temporary repo. |
| Review/Handoff conflation | Separate entity and state transitions; tests assert no Handoff on review request. |
| Over-generalization | One Cycle-to-Task bridge, one RD review-request entity, no DAG/factory/general workflow abstraction. |

## 9. Review decision required

Approval should authorize only Phase 0 and the first bounded implementation Issue.
Phase 3 is the first point at which a product-bearing vertical slice can be claimed.
Phases 4–6 continue only after the same Issue or explicitly bounded follow-up scope
preserves the approved authority and Allowed Files.

No `RD_RUNTIME_ARCHITECTURE_REVIEW.md` accompanies this plan because the current gaps
are implementable by extending existing primitives. If Phase 0 disproves atomic scope
or result-link feasibility, implementation must stop and request that review rather
than inventing a parallel Runtime.

**RD IMPLEMENTATION PLAN REVIEW REQUIRED**
