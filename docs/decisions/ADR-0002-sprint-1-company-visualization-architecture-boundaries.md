# ADR-0002: Sprint 1 Company Visualization Architecture Boundaries

## Status

Accepted by 系统交付席 for 质量运行席 verification planning.

## Context

Sprint 1 - 公司运行可视化 is approved for architecture boundary definition before any UI implementation. Tool System v1.8 is the accepted execution kernel and must remain the source of truth.

The protected loop remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Decision

Sprint 1 visualization is a read-only observability layer over accepted v1.8 execution records. It may make existing task creation and run actions easier to inspect, but it must not change orchestration, routing, tool execution, learning, meta-development, or evolution-governor behavior.

The first architecture slice should use the existing frontend shape: compact task history plus selected task detail. This matches the current minimal frontend and avoids introducing a complex dashboard shell before verification planning.

## Boundary Rules

### Backend Boundary

- Existing APIs remain valid: task create/run/status/history, trace, workflow, meta-development, and evolution decisions.
- New backend work is limited to read-only visualization adapters when existing endpoints cannot provide a coherent task-detail payload.
- A visualization adapter may aggregate existing records but must not write execution data, trigger tools, reroute workflow steps, change evolution decisions, or create new runtime state.
- Any required read-only API gap must be documented before implementation and verified by 质量运行席.

### Frontend Boundary

- The first screen must remain an execution workspace, not a landing page or management dashboard.
- The allowed information architecture is:
  - task history / selector,
  - selected task status and result,
  - workflow timeline,
  - tool trace and fallback evidence,
  - learning / meta-development evidence,
  - evolution decision evidence,
  - minimal derived status labels.
- Frontend labels must be derived from persisted execution state.
- Frontend may hide raw JSON behind compact sections, but the displayed data must remain inspectable.

### Persistence Boundary

- Sprint 1 must reuse v1.8 persistence tables.
- New persistence tables are not allowed for visualization unless a verified read-model gap is approved through a follow-up issue.
- Derived UI labels are computed at read time from existing task, workflow, trace, learning, meta-development, and evolution records.

### Execution Boundary

- Visualization must not introduce new orchestration, tool routing, tool execution, fallback, learning, meta-development, or evolution-governor behavior.
- Evolution proposals remain records only; Sprint 1 UI must not apply or schedule code changes.
- Architecture locks and rollback records are displayed as evidence only.

### Product Boundary

- Architecture recommends the first slice as compact task list plus selected task detail.
- If 产品规划席 wants a different first slice, that is a product decision and must be routed back before UI implementation.
- Visual hierarchy can be minimal sections and labels; advanced dashboard customization remains out of scope.

## Verification Planning Boundary

质量运行席 should plan verification around:

- Backend tests still passing when backend read adapters are added.
- Frontend lint/build passing when frontend files are changed.
- API evidence for task status, workflow, trace, meta-development, and evolution decisions.
- Scope drift scan covering forbidden implementation terms in `backend/app`, `backend/tests`, and `frontend/app`.
- Manual UI evidence only after UI implementation begins.

## Consequences

Positive:

- Sprint 1 can make v1.8 visible without destabilizing the execution kernel.
- The first UI slice can reuse current frontend structure.
- Verification remains focused on observability, not new behavior.

Trade-offs:

- Some UX polish waits until after the first verified visualization slice.
- If existing endpoints are too fragmented, a read-only aggregation API may be needed before frontend work.
