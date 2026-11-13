# Issue: Sprint 4 Multi-Entry UI First Slice

## Owner

系统交付席

## Context

Sprint 4 multi-entry and advanced UI architecture-boundary verification planning was accepted by 产品规划席 on 2026-07-06.

The current launch scope remains AI Task Executor MVP under Tool System v1.8.

This issue approves only a narrow frontend-only first slice inside the existing AI Task Executor web product shell. It does not approve backend/API changes, persistence, new execution behavior, external channels, dashboards, role selectors, business modules, Employee expansion, company organization, or future-layer scope.

## Objective

Implement a bounded multi-entry UI first slice that helps the CEO user start task execution from a few operational entry affordances while preserving the existing task composer, Task API behavior, run action, task history, selected detail, and review signals.

## Scope To Implement

- Frontend-only changes under `frontend/app`.
- Keep the existing freeform task composer.
- Add bounded entry affordances that prefill or structure ordinary task content only.
- Entry affordances must not create a new task type, hidden route, role selection, backend metadata, or execution behavior.
- Preserve selected task detail, existing run action, task history, and review signals.
- Add or update frontend view-model tests when logic is extracted or changed.

## Recommended First Slice

- Define a small source-controlled set of local task-entry starters for existing AI Task Executor work.
- Selecting a starter should only update the existing composer content or local presentation state.
- Submitted tasks must still use the existing `POST /api/task` payload shape: `{ content }`.
- Existing task history and selected detail remain the primary review surface.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Company organization, departments, reporting lines, staffing, or ownership model.
- Multi-agent routing.
- Agent abstraction layer.
- External entry channels or third-party platform integrations.
- Complex UI, role dashboard, analytics dashboard, or company dashboard.
- Role selector or role-management UI.
- New task execution behavior.
- API semantic changes or new API routes.
- Backend metadata, persistence, new tables, or task-role association.
- Task evidence attachment.
- Runtime prompt integration beyond separately approved role-context helper behavior.
- Automatic evolution behavior.
- Vector database, embeddings, external role service, or external memory service.

## Acceptance Criteria

- UI remains inside the existing AI Task Executor product shell.
- First slice is frontend-only; no backend files are changed.
- Existing Task API payload shape remains `{ content }`.
- Entry affordances only prefill or structure ordinary task content.
- Existing composer, run action, task history, selected detail, and review signals remain available.
- No external channels, dashboards, role selectors, persistence, API drift, execution-loop drift, new task semantics, or future-layer scope are introduced.
- Delivery evidence is recorded in `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`.
- `knowledge/CURRENT_CONTEXT.md`, `PROJECT_STATUS.md`, `TASKS.md`, and `knowledge/PROJECT_MEMORY.md` are updated after delivery.

## Evidence To Review

- `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`
- `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md`
- `docs/sprints/sprint-4-multi-entry-advanced-ui.md`
- `frontend/app/page.js`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`

## Handoff

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload sent on 2026-07-06:

- Objective: implement frontend-only Sprint 4 multi-entry UI first slice.
- Evidence: `reviews/015_sprint_4_multi_entry_architecture_boundaries_review.md`.
- Product acceptance commit: `c320ca0`.
- Next seat after delivery: 质量运行席.

## Delivery Notes

Status: implemented by 系统交付席 on 2026-07-06.

Delivery evidence: `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`.

Implemented scope:

- Added bounded local task-entry starters inside the existing AI Task Executor shell.
- Starter selection only updates ordinary composer content and local selected-starter presentation state.
- Task submission preserves the existing `POST /api/task` payload shape: `{ content }`.
- Existing task composer, run action, task history, selected task detail, and review signals remain available.

Verification performed:

- `cd frontend && node --test app/taskViewModel.test.mjs`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- `git diff --name-only HEAD -- backend`
- `git diff --name-only HEAD -- frontend/app`
- `git diff --check`
- Forbidden-scope scan over `frontend/app`

Completion handoff:

Handoff: sent to 质量运行席

## Quality And Product Acceptance

Quality status: PASS by 质量运行席 on 2026-07-06.

Product status: ACCEPTED by 产品规划席 on 2026-07-06.

Accepted scope:

- Frontend-only task-entry starters inside the existing AI Task Executor shell.
- Existing Task API payload shape remains `{ content }`.
- Existing composer, run action, task history, selected task detail, and review signals remain available.
- Future expansion requires a separate approved issue.
