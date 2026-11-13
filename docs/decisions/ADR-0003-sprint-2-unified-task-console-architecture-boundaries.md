# ADR-0003: Sprint 2 Unified Task Console Architecture Boundaries

## Status

Accepted by 系统交付席 for 质量运行席 verification planning.

## Context

Sprint 2 - 统一任务操作台 is approved for architecture boundary definition before implementation. Tool System v1.8 remains the active execution kernel, and the accepted Sprint 1 selected-task detail boundary remains the reusable evidence surface.

The protected loop remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Decision

Sprint 2 unified task console is a frontend composition boundary over existing task creation, run, history, status, and Sprint 1 selected-task detail evidence. It may improve daily operating flow, but it must not change task orchestration, workflow generation, tool routing, tool execution, learning, meta-development, evolution-governor behavior, or persistence.

The first implementation slice should include:

- Existing task composer.
- Compact task history.
- Existing run action.
- Accepted Sprint 1 selected-task detail.
- Minimal review signals derived from existing execution state.

Status filters and local presentation preferences are deferred unless they remain purely local UI state and do not expand the console into a complex dashboard. New backend work is not part of the first slice because existing read APIs cover the required task, workflow, trace, meta-development, and evolution-decision evidence.

## Boundary Rules

### Backend Boundary

- Existing APIs remain the source of truth: task create, task run, task status, task history, workflow, trace, meta-development, and evolution decisions.
- Rerun, if shown, must call the existing Run API for the selected existing task; it is not a retry engine.
- Backend changes are not allowed for the first implementation slice.
- If implementation finds a required read-model gap, 系统交付席 must document the gap and route back for approval before adding any read-only adapter.
- Any approved read adapter must aggregate existing records only and must not create runtime state, trigger tools, reroute workflows, alter evolution decisions, or create new persistence tables.

### Frontend Boundary

- The console remains an operating workspace, not a landing page, department console, or complex dashboard.
- The allowed information architecture is:
  - task composer,
  - compact task history,
  - selected task state,
  - run or rerun action using the existing Run API,
  - accepted Sprint 1 selected-task detail,
  - minimal review signals.
- The accepted Sprint 1 detail components and view-model helpers should remain the detail source; Sprint 2 should compose around them instead of replacing the evidence model.
- Review signals must be derived from existing task, workflow, trace, meta-development, and evolution-decision records.
- Raw records may remain inspectable behind existing detail affordances.

### Review Signal Boundary

Allowed review signals:

- Failed or blocked from task status, task error, or failed workflow steps.
- Running or pending from existing task status and workflow current step.
- Result ready from task output.
- Learning recorded from existing meta-development report.
- Evolution evaluated from existing evolution decision.
- User decision needed only when an existing blocker, postponed evolution, rollback record, or approval-required proposal is already present.

Not allowed:

- Mock review states.
- Business priority, ROI, company operating score, department ownership, or employee-management state.
- Signals that cause execution, rerouting, evolution, or persistence writes.

### Persistence Boundary

- Sprint 2 reuses v1.8 persistence tables.
- New persistence tables are forbidden unless a required read-model gap is approved through a follow-up issue.
- Local UI state may hold selected task or temporary presentation state, but it must not become backend persistence.

### Execution Boundary

- The only execution action remains the accepted task Run API.
- The console must not introduce new orchestration, retry engine, scheduling, tool selection, workflow mutation, learning behavior, meta-development behavior, or evolution behavior.
- Evolution proposals remain records only; the UI must not apply, schedule, or simulate code changes.

### Product Boundary

- Sprint 2 may unify the task composer, history, run action, selected detail, and review signals in one minimal console.
- Sprint 2 must not add ROI, business modules, Employee CRUD or expansion, multi-agent behavior, agent abstraction layer, complex UI, Company CRUD, new execution behavior, automatic evolution behavior, or unapproved persistence.
- If 产品规划席 requires status filters in the first implementation slice as product scope, that should be confirmed before implementation; otherwise filters stay deferred.

## Verification Planning Boundary

质量运行席 should plan verification around:

- No backend files changed for the first implementation slice unless a read-model gap is separately approved.
- Frontend tests for derived review signals and console state helpers.
- Frontend lint and build.
- Scope drift scan covering forbidden implementation terms in `backend/app`, `backend/tests`, and `frontend/app`.
- Manual UI evidence after implementation showing create, run, select previous task, inspect accepted Sprint 1 detail, and see review signals derived from existing state.

## Consequences

Positive:

- Sprint 2 can improve daily operation without destabilizing Tool System v1.8.
- The accepted Sprint 1 selected-task detail remains the evidence anchor.
- Implementation can stay frontend-scoped unless a real read-model gap appears.

Trade-offs:

- Status filters and presentation preferences may wait until the minimal console is verified.
- Fragmented frontend state may need local composition helpers before any backend aggregation is considered.
