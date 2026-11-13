---
issue: "084"
title: "Workspace Department Activation UI Gate"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/083_workspace_department_activation_first_slice.md"
---

# Workspace Department Activation UI Gate

## Objective

Approve and implement a minimal frontend-only Workspace Department Activation display/selector inside the existing company frame.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md`
- `issues/083_workspace_department_activation_first_slice.md`
- `reviews/080_workspace_department_activation_first_slice_review.md`

## Product Context

Curis Workspace now has backend-only tenant-local department activation metadata over active official department type metadata. The next product step is to expose that backend state in the existing company frame so a CEO can see and save which official department foundations are enabled for the current Workspace.

This remains a minimal local/demo Workspace company foundation slice. It is not department CRUD, not department instance management, not staffing, not workflow routing, not Admin Platform management, and not a business module.

## Approved Scope

Owner seat: 系统交付席.

Allowed:

- Frontend-only UI inside the existing company frame.
- Use existing `GET /api/workspace/departments/activation`.
- Use existing `PUT /api/workspace/departments/activation`.
- Show current active department count and active labels.
- Let CEO select/unselect active official department type references with checkboxes.
- Save selected keys with payload `{ "department_type_keys": [...] }`.
- Loading/error/saving states in Chinese.
- Frontend view-model tests.
- Update source-of-truth files and review evidence.

Allowed files:

- `frontend/app/page.js`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`
- `issues/084_workspace_department_activation_ui_gate.md`
- `reviews/081_workspace_department_activation_ui_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Non-Goals

- Backend/API/schema/persistence changes.
- New department APIs.
- Department CRUD, department instance creation or management.
- Department workflow routing, task routing, tool routing, or model routing policy.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Admin Platform implementation or platform policy management.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Execution-loop, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.

## Acceptance Criteria

- UI uses only existing department activation APIs.
- UI shows selected active department count and labels.
- UI allows selecting/unselecting official department type references and saving them.
- Payload shape is `{ "department_type_keys": [...] }`.
- UI exposes no secret-like metadata.
- No backend/Admin/shared/runtime behavior files are changed for this issue.
- Task API payload remains `{ content }`.
- Frontend tests, lint, and build pass.

## Verification

Required:

- `cd frontend && node --test app/taskViewModel.test.mjs`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- API usage scan confirms only existing activation APIs were added.
- Secret/scope scan for frontend files.
- Backend/Admin/shared/runtime behavior guard.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Approved / Blocked: Approved for frontend-only UI/display implementation.

Reason:

- The backend-only department activation first slice is accepted.
- This slice makes the accepted activation state visible and editable from the existing company frame without changing backend semantics or runtime behavior.
- Scope is bounded to frontend use of existing APIs.

Next Seat: 系统交付席.

Handoff: sent to 系统交付席

## Completion Notes

Implementation, verification, and product acceptance completed on 2026-07-08.

- Added frontend-only department activation display/selector inside the existing `公司工作区` frame.
- Used existing `GET /api/workspace/departments/activation`.
- Used existing `PUT /api/workspace/departments/activation`.
- Saved payload `{ "department_type_keys": [...] }`.
- Added frontend view-model tests for activation summary states and payload shape.
- No backend/API/schema/persistence change, new department API, department instance, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business module, secret, Task API, Project Memory runtime write, or runtime behavior change was introduced for this issue.
- Evidence is recorded in `reviews/081_workspace_department_activation_ui_review.md`.
- Current-state correction is recorded in `reviews/081_workspace_department_activation_ui_review.md`: page-level selector wiring was missing from `frontend/app/page.js`; it is now added with regression coverage. Verification passed with 22 frontend tests, lint, build, and focused backend activation tests.

Next Seat: main thread closeout.

Handoff: final closeout
