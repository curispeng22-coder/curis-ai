# Issue: Sprint 2 Unified Task Console First Slice

## Owner

系统交付席

## Context

Sprint 2 unified task console gate is approved.

Architecture boundaries are defined in `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`.

Quality verification planning passed in `reviews/007_sprint_2_architecture_boundaries_review.md`.

产品规划席 accepted the architecture-boundary verification plan on 2026-07-06.

## Objective

Implement the smallest Sprint 2 unified task console slice.

## Scope

Allowed:

- Existing task composer.
- Compact task history.
- Existing run action.
- Accepted Sprint 1 selected-task detail.
- Minimal review signals derived from existing task, workflow, trace, meta-development, and evolution-decision state.

## Non-Goals

- No ROI system.
- No business modules.
- No Employee CRUD or employee expansion.
- No multi-agent behavior.
- No agent abstraction layer.
- No complex UI.
- No Company CRUD.
- No new execution behavior.
- No automatic evolution behavior.
- No backend changes unless an approved read-model gap is documented first.
- No new persistence tables.
- No status filters or presentation preferences unless they remain purely local UI state and do not expand scope.

## Allowed Files

- `frontend/app/**`
- `reviews/008_sprint_2_unified_task_console_first_slice_review.md`
- `TASKS.md`
- `PROJECT_STATUS.md`
- `knowledge/CURRENT_CONTEXT.md`

Backend files are blocked unless 系统交付席 documents a read-model gap and routes back for approval before changing backend code.

## Acceptance Criteria

- [x] User can create a task from the unified console using existing task creation behavior.
- [x] User can see compact task history.
- [x] User can select a task without losing console context.
- [x] User can run the selected task through the existing Run API.
- [x] Accepted Sprint 1 selected-task detail remains available and readable.
- [x] Review signals are derived from existing state only.
- [x] No backend files are changed unless an approved read-model gap exists.
- [x] No forbidden scope enters implementation.
- [x] Frontend tests for review-signal derivation and console state helpers pass.
- [x] `cd frontend && pnpm lint` passes.
- [x] `cd frontend && pnpm build` passes.
- [x] Scope drift scan passes.
- [x] Manual UI evidence is captured in the review file.

## Verification

```bash
cd frontend
node --test app/taskViewModel.test.mjs
pnpm lint
pnpm build
```

Scope drift scan:

```bash
rg -n "ROI|business module|agent abstraction|multi-agent|Employee CRUD|employee-management|mock data|simulation mode|uncontrolled architecture|automatic evolution" backend/app backend/tests frontend/app
```

Backend guard:

```bash
git diff --name-only HEAD -- backend
```

## Next Seat

Main thread closeout.

## Completion Notes

Implemented by 系统交付席 on 2026-07-06.

Verified by 质量运行席 against commit `b799041`.

Product acceptance: ACCEPTED by 产品规划席 on 2026-07-06.

Review evidence:

- `reviews/008_sprint_2_unified_task_console_first_slice_review.md`
