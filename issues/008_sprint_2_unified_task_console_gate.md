# Issue: Sprint 2 Unified Task Console Gate

## Owner

总控决策席

## Context

Sprint 1 CEO-readable visualization polish is implemented, verified, and accepted.

Sprint 2 product PRD slice is drafted in `docs/sprints/sprint-2-unified-task-console.md`.

Tool System v1.8 remains the active implementation gate.

## Objective

Decide whether Sprint 2 - 统一任务操作台 may open for architecture boundary definition by 系统交付席.

## Scope To Approve

- Compose existing task creation, run, history, status, and Sprint 1 task detail into one minimal operating console.
- Preserve the accepted v1.8 execution loop.
- Reuse existing Task API, Run API, Status API, History API, and execution evidence surfaces.
- Keep rerun as an affordance over the existing Run API only.
- Surface review signals from existing execution state.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Complex UI.
- Company CRUD.
- New execution behavior beyond the accepted v1.8 loop.
- Automatic evolution behavior.
- New persistence tables without an approved read-model gap.

## Decision Needed

- [x] Approve Sprint 2 gate and route to 系统交付席.
- [ ] Block Sprint 2 gate and list required product changes.
- [ ] Request user decision if scope exceeds current product direction.

## Evidence To Review

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/product/prd.md`
- `docs/sprints/sprint-2-unified-task-console.md`
- `reviews/006_sprint_1_ceo_readable_visualization_polish_review.md`

## Completion Notes

Decision: APPROVED by 总控决策席 on 2026-07-06.

Rationale:

- Sprint 2 scope is constrained to composing existing task creation, run, history, status, and accepted Sprint 1 selected-task detail surfaces into one minimal console.
- The PRD preserves Tool System v1.8 and the accepted Sprint 1 selected-task detail boundary.
- The issue explicitly forbids ROI, business modules, Employee CRUD/expansion, multi-agent behavior, agent abstraction layer, complex UI, Company CRUD, new execution behavior, automatic evolution behavior, and new persistence tables without an approved read-model gap.
- No implementation is approved at this gate; the next step is architecture boundary definition by 系统交付席.

Handoff: HANDOFF_REQUIRED

Target seat: 系统交付席

Compact payload:

- Issue: `issues/008_sprint_2_unified_task_console_gate.md`
- Objective: Define Sprint 2 unified task console architecture boundaries before implementation.
- Preserve: Tool System v1.8 loop and accepted Sprint 1 selected-task detail boundary.
- Allow: existing task composer, task history, run action, selected detail, and review signals derived from existing state.
- Forbid: ROI, business modules, Employee CRUD/expansion, multi-agent behavior, agent abstraction layer, complex UI, new execution behavior, automatic evolution behavior, and new persistence tables unless a read-model gap is approved.

Architecture boundary follow-up:

- 系统交付席 defined Sprint 2 architecture boundaries in `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`.
- Boundary evidence is recorded in `reviews/007_sprint_2_architecture_boundaries_review.md`.
- Handoff: sent to 质量运行席 thread `019f33c4-9517-7dd0-814b-d2e323b018f5`.
