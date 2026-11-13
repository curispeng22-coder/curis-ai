---
issue: "079"
title: "Workspace Company Foundation Local Demo Evidence Gate"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/078_workspace_company_foundation_first_slice_gate.md"
---

# Workspace Company Foundation Local Demo Evidence Gate

## Objective

Decide whether to approve a verification-only local/demo evidence pass for the accepted Workspace Company Foundation first slice.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/078_workspace_company_foundation_first_slice_gate.md`
- `reviews/075_workspace_company_foundation_first_slice_review.md`

## Product Context

Curis Workspace now has an accepted frontend-only local/demo company frame inside the existing operation console. Quality verification passed for commit `dfd60689`, but browser screenshot/runtime interaction evidence was not captured and was classified as non-blocking.

The next useful step is to verify the accepted company frame in a real local/demo runtime without changing product behavior. This keeps momentum toward a visible CEO-facing first version while preserving the AI Task Executor MVP and ADR-0031 boundaries.

## Product Recommendation

Recommended next phase: approve Option A, a verification-only local/demo evidence pass.

Rationale:

- The first company frame is accepted, but the product still needs operator-visible evidence that the frame renders correctly in local/demo runtime.
- This is an evidence issue, not a feature issue.
- It closes the only known non-blocking quality gap from `reviews/075_workspace_company_foundation_first_slice_review.md`.

## Options

### Option A: Local/Demo Company Frame Evidence

Approve a verification-only local/demo pass for the accepted company frame.

Allowed:

- Start or reuse local backend and frontend.
- Verify the operation console renders the `公司工作区` frame.
- Verify company identity, local/demo status, model preference summary, task summary, and source-of-truth links are visible.
- Verify no secret-like metadata is visible.
- Verify task creation still sends `{ "content": "..." }`.
- Capture screenshot or browser-visible evidence.
- Record evidence in a review file.
- Update source-of-truth status files.

Forbidden:

- New product feature.
- Frontend design expansion beyond evidence-only corrections.
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

### Option B: Defer Runtime Evidence

Defer local/demo evidence and move to a new implementation slice.

Use only if 总控决策席 decides runtime evidence is not needed before the next product slice.

### Option C: Stabilization Before Evidence

Open a stabilization issue only if the accepted first slice has a blocker defect that prevents local/demo verification.

Any behavior-changing fix must use a separate approved implementation issue.

## Acceptance Criteria

- 总控决策席 selects Option A, B, or C.
- Decision states whether verification may proceed.
- If Option A is selected, route to 质量运行席 for verification-only evidence.
- If Option B is selected, route back to 产品规划席 for the next product slice.
- If Option C is selected, define the blocker and route to the responsible seat.
- Decision preserves ADR-0031, the accepted frontend-only first-slice boundary, Task API payload `{ content }`, model-gateway security boundary, Admin/Workspace separation, local/demo scope, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no complex organization, no business modules, no secrets, and no execution-loop/runtime behavior change.

## Verification

Gate-only review. No implementation verification is required at this decision step.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Selected option: Option A - Local/Demo Company Frame Evidence.

Reason:

- The Workspace Company Foundation first slice is already accepted, and the remaining gap is browser-visible local/demo evidence.
- Option A is verification-only and does not change product behavior, APIs, schema, persistence, execution, routing, model selection, Project Memory, or runtime behavior.
- The evidence pass preserves ADR-0031, the accepted frontend-only boundary, model-gateway security, Admin/Workspace separation, and local/demo scope.

Approved scope:

- Verification-only local/demo evidence for the accepted company frame.
- Start or reuse local backend and frontend.
- Verify the operation console renders the `公司工作区` frame.
- Verify company identity, local/demo status, model preference summary, task summary, and source-of-truth links are visible.
- Verify no secret-like metadata is visible.
- Verify task creation still sends `{ "content": "..." }`.
- Capture screenshot or browser-visible evidence.
- Record evidence in a review file and update source-of-truth status files.

Forbidden scope remains:

- New product feature.
- Frontend design expansion beyond evidence-only corrections.
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

Approved Option A. Route to 质量运行席 for verification-only local/demo evidence.

Handoff: sent to 质量运行席

Target seat: 质量运行席

Compact payload:

- Issue: `issues/079_workspace_company_foundation_local_demo_evidence_gate.md`
- Objective: Verify local/demo browser-visible evidence for the accepted Workspace Company Foundation company frame.
- Special Constraints: Option A approved. Verification-only local/demo evidence; preserve ADR-0031, accepted frontend-only first-slice boundary, Task API payload `{ content }`, model-gateway security, Admin/Workspace separation, local/demo scope, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no complex organization, no business modules, no secrets, and no execution-loop/runtime behavior change.
- Next Seat: 质量运行席.

## Evidence Notes

Local/demo evidence verification passed with browser-visible evidence in `reviews/076_workspace_company_foundation_local_demo_evidence_review.md` and screenshot artifact `reviews/076_workspace_company_foundation_local_demo_evidence.png`.

Handoff: final closeout
