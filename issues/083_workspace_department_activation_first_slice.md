---
issue: "083"
title: "Workspace Department Activation First Slice"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/082_workspace_department_activation_boundary_gate.md"
---

# Workspace Department Activation First Slice

## Objective

Approve and implement the first backend-only Workspace Department Activation slice.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md`
- `reviews/079_workspace_department_activation_boundaries_review.md`

## Product Context

ADR-0032 defines future tenant-local department activation as metadata-only selection over active official department type metadata. The next product step is a backend-first read/write foundation so a future Workspace UI can show which official department types are active for a tenant.

This is not department CRUD. It does not create department instances, employees, staffing, permissions, org charts, workflow routing, task routing, Admin Platform management, billing, ROI, marketplace, business modules, or runtime behavior changes.

## Approved Scope

Owner seat: 系统交付席.

Allowed:

- Backend-only tenant-local department activation metadata.
- Validate requested `department_type_key` values against active official department type metadata.
- Store tenant-local activation references only.
- Return a non-secret read model combining active official department type metadata with tenant-local enabled state.
- Add focused backend tests.
- Update source-of-truth files and review evidence.

Allowed files:

- `backend/app/database.py`
- `backend/app/department_activation.py`
- `backend/app/main.py`
- `backend/tests/test_department_activation.py`
- `issues/083_workspace_department_activation_first_slice.md`
- `reviews/080_workspace_department_activation_first_slice_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Non-Goals

- Frontend UI selector.
- Admin Platform implementation or platform policy management.
- New official department type supply.
- Department CRUD beyond tenant-local activation references.
- Department instance creation or management.
- Department workflow routing, task routing, tool routing, model policy, or runtime behavior change.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Project Memory writes from runtime.

## Acceptance Criteria

- `GET /api/workspace/departments/activation` returns tenant-local activation state plus active official department options.
- `PUT /api/workspace/departments/activation` accepts `{ "department_type_keys": [...] }`.
- Writes reject unknown, inactive, or non-official department type keys.
- Reads/writes are tenant-scoped.
- Persistence is metadata-only and contains no secret, prompt, output, credential, billing, ROI, staffing, permission, routing, model-policy, or external-platform fields.
- API response exposes only non-secret official department metadata and tenant-local enabled state.
- Task API payload remains `{ content }`.
- No execution-loop, workflow, tool routing, model selection, Project Memory, Admin Platform, Employee, billing, business-module, secret, or runtime behavior change is introduced.

## Verification

Required:

- `cd backend && ./.venv/bin/python -m unittest tests/test_department_activation.py`
- `cd backend && ./.venv/bin/python -m unittest discover tests`
- Secret/scope scan for new activation files and API response fields.
- Frontend behavior guard: no frontend files changed for this issue.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Approved / Blocked: Approved for backend-only first-slice implementation.

Reason:

- ADR-0032 is accepted and recommends a backend-first metadata activation slice.
- The slice advances CEO-configurable company structure while preserving the current AI Task Executor runtime.
- The approved scope is metadata-only, tenant-scoped, and official-catalog-validated.

Next Seat: 系统交付席.

Handoff: sent to 系统交付席

## Completion Notes

Implementation, verification, and product acceptance completed on 2026-07-08.

- Added backend-only tenant-local department activation metadata.
- Added `GET /api/workspace/departments/activation`.
- Added `PUT /api/workspace/departments/activation`.
- Added focused TDD tests in `backend/tests/test_department_activation.py`.
- Validation accepts only active official department type metadata.
- Persistence remains metadata-only.
- No frontend selector, Admin Platform implementation, department instance, workflow routing, Employee CRUD, billing/ROI/packages/marketplace, business module, secret, Task API, Project Memory runtime write, or runtime behavior change was introduced.
- Evidence is recorded in `reviews/080_workspace_department_activation_first_slice_review.md`.

Next Seat: main thread closeout.

Handoff: final closeout
