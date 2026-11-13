---
issue: "080"
title: "Workspace Company Department Catalog Summary Gate"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/079_workspace_company_foundation_local_demo_evidence_gate.md"
---

# Workspace Company Department Catalog Summary Gate

## Objective

Decide whether to approve the next bounded Workspace Company Foundation slice: a frontend-only department catalog summary inside the existing company frame.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`
- `issues/079_workspace_company_foundation_local_demo_evidence_gate.md`
- `reviews/076_workspace_company_foundation_local_demo_evidence_review.md`

## Product Context

Curis Workspace now has a verified local/demo company frame. The next product step should make the frame more useful for the future AI Company System without opening full company organization, Employee CRUD, department CRUD, workflow routing, or Admin Platform scope.

Workspace already exposes an existing read-only department type catalog through `GET /api/catalog/department-types`. A frontend-only summary can make the company foundation visible while preserving current boundaries.

## Product Recommendation

Recommended next phase: approve Option A, a frontend-only department catalog summary using the existing read-only catalog API.

Rationale:

- This advances the product from a static company frame toward the L5 company foundation without implementing full L5 organization.
- It reuses existing read-only catalog metadata instead of adding backend/API/schema/persistence work.
- It gives the CEO a visible sense of available department foundations while keeping creation, staffing, permissions, workflow routing, and business modules blocked.

## Options

### Option A: Frontend-Only Department Catalog Summary

Approve a minimal frontend-only summary inside the existing company frame.

Allowed:

- Use existing `GET /api/catalog/department-types`.
- Show active department type count.
- Show a small summary of official department types and categories.
- Show only non-secret catalog metadata already returned by the existing API.
- Chinese UI copy inside the existing operation console.
- Loading/error/empty states for the summary.
- Frontend view-model tests and local/demo evidence.

Forbidden:

- Backend/API/schema/persistence changes.
- New department APIs.
- Department CRUD, department instance creation, department enable/disable controls, staffing, permissions, reporting lines, org charts, or workflow routing.
- Employee CRUD or employee expansion.
- Admin Platform implementation or platform policy management.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.

### Option B: Architecture Boundary First

Defer frontend implementation and ask 系统交付席 to define a stricter department-catalog summary boundary first.

Use if 总控决策席 finds that showing department catalog metadata risks blurring future L5 organization scope.

### Option C: Pause Department Summary

Pause department summary and return to 产品规划席 for a different next product slice.

Use if 总控决策席 decides the next slice should focus on another verified Workspace surface.

## Acceptance Criteria

- 总控决策席 selects Option A, B, or C.
- Decision states whether implementation may proceed.
- If Option A is selected, route to 系统交付席 for frontend-only implementation.
- If Option B is selected, route to 系统交付席 for boundary definition only.
- If Option C is selected, route back to 产品规划席.
- Decision preserves ADR-0031, local/demo scope, accepted company frame, existing Task API payload `{ content }`, existing model-gateway boundaries, Admin/Workspace separation, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no department CRUD/workflow routing, no complex organization, no business modules, no secrets, and no execution-loop/runtime behavior change.

## Verification

Gate-only review. No implementation verification is required.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Selected option: Option A - Frontend-Only Department Catalog Summary.

Reason:

- The company frame is verified in local/demo runtime, and the existing read-only `GET /api/catalog/department-types` API can make department foundations visible without adding backend scope.
- Option A keeps the next slice inside the accepted Workspace Company Foundation frame and does not unlock department CRUD, department instances, staffing, workflow routing, Employee CRUD, Admin Platform, or L6 economy scope.
- The slice preserves ADR-0031, local/demo scope, Task API payload `{ content }`, model-gateway boundaries, Admin/Workspace separation, and runtime behavior.

Approved scope:

- Frontend-only department catalog summary inside the existing company frame.
- Use existing `GET /api/catalog/department-types` only.
- Show active department type count.
- Show a small summary of official department types and categories.
- Show only non-secret catalog metadata already returned by the existing API.
- Chinese UI copy inside the existing operation console.
- Loading/error/empty states for the summary.
- Frontend view-model tests and local/demo evidence.

Forbidden scope remains:

- Backend/API/schema/persistence changes.
- New department APIs.
- Department CRUD, department instance creation, department enable/disable controls, staffing, permissions, reporting lines, org charts, or workflow routing.
- Employee CRUD or employee expansion.
- Admin Platform implementation or platform policy management.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.

## Completion Notes

Approved Option A. Route to 系统交付席 for frontend-only department catalog summary implementation inside the existing company frame.

Implementation and acceptance completed on 2026-07-08.

- Added a frontend-only `部门目录` summary inside the existing company frame.
- Used existing `GET /api/catalog/department-types` only.
- Shows active official department type count, category summary, non-secret department labels, and loading/error/empty states.
- Preserved Task API payload `{ content }`, existing model preference/task APIs, model gateway boundaries, and runtime behavior.
- Quality and product acceptance evidence is recorded in `reviews/077_workspace_company_department_catalog_summary_review.md`.
- Verification: `cd frontend && node --test app/taskViewModel.test.mjs`; `cd frontend && npm run lint`; `cd frontend && npm run build`; `git diff --check`; API usage scan; forbidden-scope scan.

Next Seat: main thread closeout.

Handoff: final closeout

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload:

- Issue: `issues/080_workspace_company_department_catalog_summary_gate.md`
- Objective: Implement a frontend-only department catalog summary inside the existing company frame.
- Special Constraints: Option A approved. Use existing `GET /api/catalog/department-types` only. Preserve ADR-0031, accepted company frame, local/demo scope, Task API payload `{ content }`, model-gateway boundaries, Admin/Workspace separation, no backend/API/schema/persistence changes, no new department APIs, no department CRUD/instances/routing, no Employee CRUD, no Admin Platform implementation, no billing/ROI/packages/marketplace, no complex organization, no business modules, no secrets, and no runtime behavior change.
- Next Seat: 系统交付席.
