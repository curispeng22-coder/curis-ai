# Issue: Sprint 1 Visualization First Slice

## Owner

系统交付席

## Context

Sprint 1 company visualization gate is approved.

Architecture boundaries are defined in `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`.

Quality verification planning is recorded in `reviews/004_sprint_1_architecture_boundaries_review.md`.

Product accepted the recommended first slice: compact task list plus selected task detail.

## Objective

Implement the first Sprint 1 visualization slice so the user can inspect existing v1.8 task execution records without changing the execution loop.

## Scope

Allowed:

- Compact task history/list.
- Selected task detail.
- Task status and result display.
- Workflow timeline from existing workflow records.
- Tool trace and fallback evidence from existing trace records.
- Learning/meta-development evidence when available.
- Evolution decision evidence when available.
- Minimal operating labels derived from existing persisted state.
- Existing task creation and run actions may remain.
- Read-only backend aggregation only if existing endpoints cannot support the selected task detail cleanly.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Complex UI or advanced dashboard customization.
- Company CRUD.
- New execution behavior.
- New automatic evolution behavior.
- New persistence tables unless a read-model gap is documented and approved first.

## Allowed Files

- `frontend/app/**`
- `backend/app/**` only for read-only aggregation if needed.
- `backend/tests/**` only if backend files change.
- `docs/sprints/sprint-1-company-visualization.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `reviews/005_sprint_1_visualization_first_slice_review.md`

## Acceptance Criteria

- [x] User can select a task from compact task history/list.
- [x] Selected task detail shows task status and result.
- [x] Selected task detail shows workflow steps in order.
- [x] Selected task detail shows tool trace and fallback evidence when available.
- [x] Selected task detail shows learning/meta-development evidence when available.
- [x] Selected task detail shows evolution decision evidence when available.
- [x] Labels are derived from existing persisted execution state.
- [x] Existing v1.8 task create/run behavior remains unchanged.
- [x] No forbidden scope enters implementation.
- [x] Frontend lint and build pass if frontend files change.
- [x] Backend tests pass if backend files change.
- [x] UI evidence is captured or summarized in the review.

## Verification

Required if frontend changes:

```bash
cd frontend
pnpm lint
pnpm build
```

Required if backend changes:

```bash
cd backend
.venv/bin/python -m unittest discover -s tests
```

Scope drift scan:

```bash
rg -n "ROI|business module|agent abstraction|multi-agent|Employee CRUD|employee-management|mock data|simulation mode|uncontrolled architecture|automatic evolution" backend/app backend/tests frontend/app
```

## Completion Notes

Implemented by 系统交付席 on 2026-07-06.

Evidence: `reviews/005_sprint_1_visualization_first_slice_review.md`.

Backend files changed: No.

Handoff: sent to 质量运行席.

Quality verification: PASS by 质量运行席 on 2026-07-06.

Product acceptance: ACCEPTED by 产品规划席 on 2026-07-06.

Closeout: main thread user-facing closeout.
