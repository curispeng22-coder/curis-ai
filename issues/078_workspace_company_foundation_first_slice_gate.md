---
issue: "078"
title: "Workspace Company Foundation First Slice Gate"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/077_post_first_version_workspace_company_foundation_gate.md"
---

# Workspace Company Foundation First Slice Gate

## Objective

Decide whether to approve the first bounded implementation slice for Workspace Company Foundation after ADR-0031 was quality-verified and accepted.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`
- `reviews/074_workspace_company_foundation_boundaries_review.md`

## Product Context

Curis Workspace has a local/demo AI Task Executor first version and an accepted Workspace Company Foundation boundary. The next product step is to make the CEO-facing Workspace shell visible without changing execution behavior or jumping into future company/economy scope.

## Product Recommendation

Recommended next phase: approve Option A, a frontend-only local/demo Workspace company frame in the existing operation console.

Rationale:

- The accepted boundary says the first slice may be a minimal local/demo company frame in the existing Workspace operation console or a separately approved read-model layer.
- A frontend-only frame gives the CEO a clearer "company workspace" surface using existing task console, model preference, Project Memory/status references, and local/demo release evidence.
- This advances the product toward the AI Company System while avoiding backend read-model gaps, new persistence, Employee CRUD, complex organization, and execution-loop changes.

## Options

### Option A: Frontend-Only Local/Demo Company Frame

Approve a minimal frontend-only Workspace company frame inside the existing operation console.

Allowed:

- Show company/workspace identity label using static local/demo copy or existing non-secret context.
- Show local/demo first-version status.
- Show current tenant/workspace context only from existing non-secret metadata.
- Show active model preference summary using existing preference/catalog APIs.
- Keep the existing task console entry point/status summary.
- Show Project Memory/source-of-truth pointers as read-only text/links.
- Show department foundation summary only if existing frontend-readable data is already available without backend/API/schema changes.
- Chinese UI copy inside the existing operation console.

Forbidden:

- Backend/API/schema/persistence changes.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.
- Admin Platform implementation.
- Billing, ROI, packages, marketplace, or L6 economy.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Department CRUD, platform policy management, or new department workflow routing.

### Option B: Read-Model Gap Definition First

Defer UI implementation and ask 系统交付席 to document any missing backend read-model gaps before implementation.

Use only if the existing frontend cannot show a coherent company frame without new read APIs.

### Option C: Pause Workspace Company Foundation

Pause this track and return to 产品规划席 for a different next product slice.

Use only if 总控决策席 finds the first-slice UI would blur forbidden company organization or future-layer scope.

## Acceptance Criteria

- 总控决策席 selects Option A, B, or C.
- Decision states whether implementation may proceed.
- If Option A is selected, route to 系统交付席 for a frontend-only implementation plan and slice.
- If Option B is selected, route to 系统交付席 for read-model gap documentation only.
- If Option C is selected, route back to 产品规划席.
- Decision preserves ADR-0031, local/demo, model-gateway security, Admin/Workspace separation, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no complex organization, no business modules, no secrets, and no execution-loop/runtime behavior change.

## Verification

Gate-only review. No implementation verification is required.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Selected option: Option A - Frontend-Only Local/Demo Company Frame.

Reason:

- ADR-0031 is accepted and explicitly allows a minimal local/demo company frame in the existing Workspace operation console as the first implementation slice.
- Option A makes the company/workspace frame visible without opening backend read-model gaps, new persistence, execution behavior changes, or future L5/L6 scope.
- The proposed slice preserves model-gateway security, Admin/Workspace separation, local/demo operation, and current Task API/runtime boundaries.

Approved scope:

- Frontend-only local/demo Workspace company frame inside the existing operation console.
- Use only existing non-secret state and existing preference/catalog APIs.
- Show company/workspace identity label, local/demo first-version status, current workspace context, active model preference summary, existing task console entry/status summary, and Project Memory/source-of-truth pointers.
- Department foundation summary is allowed only if already available from existing frontend-readable data without backend/API/schema changes.
- Chinese UI copy inside the existing operation console.

Forbidden scope remains:

- Backend/API/schema/persistence changes.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.
- Admin Platform implementation.
- Billing, ROI, packages, marketplace, or L6 economy.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Department CRUD, platform policy management, or new department workflow routing.

## Completion Notes

Approved Option A. Route to 系统交付席 for frontend-only local/demo Workspace company frame implementation inside the existing operation console.

Implementation completed by 系统交付席 on 2026-07-08.

- Added a frontend-only local/demo company frame to the existing operation console.
- Used existing local state and existing model preference API state only; no backend/API/schema/persistence files were changed for this slice.
- Preserved Task API payload shape `{ content }`, existing run action, existing model-selection behavior, execution loop, tool routing, workflow behavior, Project Memory ownership, and runtime behavior.
- Delivery evidence is recorded in `reviews/075_workspace_company_foundation_first_slice_review.md`.
- Verification: `cd frontend && node --test app/taskViewModel.test.mjs`; `cd frontend && npm run lint`; `cd frontend && npm run build` outside sandbox after sandbox port binding was blocked; frontend API/payload scope scan; forbidden-scope scan; diff whitespace check.

Next Seat: 质量运行席.

Handoff: sent to 质量运行席

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload:

- Issue: `issues/078_workspace_company_foundation_first_slice_gate.md`
- Objective: Implement the first Workspace Company Foundation slice as a frontend-only local/demo company frame in the existing operation console.
- Special Constraints: Option A approved. Preserve ADR-0031; no backend/API/schema/persistence changes; no Task API, execution-loop, tool routing, workflow, model-selection, Project Memory write, or runtime behavior changes; no hosted production, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, provider SDK/direct calls, New API source/internal DB dependency, or department CRUD/workflow routing.
- Next Seat: 系统交付席.
