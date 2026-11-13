---
issue: "081"
title: "Workspace Department Catalog Local Demo Evidence Gate"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/080_workspace_company_department_catalog_summary_gate.md"
---

# Workspace Department Catalog Local Demo Evidence Gate

## Objective

Decide whether to approve a verification-only local/demo evidence pass for the accepted Workspace Company Department Catalog Summary slice.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/080_workspace_company_department_catalog_summary_gate.md`
- `reviews/077_workspace_company_department_catalog_summary_review.md`

## Product Context

Curis Workspace now has an accepted frontend-only `部门目录` summary inside the existing company frame. Automated verification passed, but browser-visible local/demo evidence was not captured in that implementation pass.

The next useful step is to verify the accepted department summary in a real local/demo runtime without changing product behavior. This keeps the CEO-facing company foundation visibly grounded while preserving the current AI Task Executor MVP and ADR-0031 boundaries.

## Product Recommendation

Recommended next phase: approve Option A, a verification-only local/demo evidence pass.

Rationale:

- The accepted department summary should be proven visible in the actual local/demo operation console.
- This is an evidence issue, not a feature issue.
- It closes the known non-blocking evidence gap from `reviews/077_workspace_company_department_catalog_summary_review.md`.

## Options

### Option A: Local/Demo Department Catalog Evidence

Approve a verification-only local/demo pass for the accepted department catalog summary.

Allowed:

- Start or reuse local backend and frontend.
- Verify the operation console renders the existing `公司工作区` frame.
- Verify the `部门目录` summary is visible.
- Verify active official department type count, category summary, and non-secret department labels are visible when returned by the existing API.
- Verify no secret-like metadata is visible.
- Verify task creation still sends `{ "content": "..." }`.
- Capture screenshot or browser-visible evidence.
- Record evidence in a review file.
- Update source-of-truth status files.

Forbidden:

- New product feature.
- Frontend design expansion beyond evidence-only corrections.
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

### Option B: Defer Runtime Evidence

Defer local/demo evidence and move to a new implementation slice.

Use only if 总控决策席 decides runtime evidence is not needed before the next product slice.

### Option C: Stabilization Before Evidence

Open a stabilization issue only if the accepted department summary has a blocker defect that prevents local/demo verification.

Any behavior-changing fix must use a separate approved implementation issue.

## Acceptance Criteria

- 总控决策席 selects Option A, B, or C.
- Decision states whether verification may proceed.
- If Option A is selected, route to 质量运行席 for verification-only evidence.
- If Option B is selected, route back to 产品规划席 for the next product slice.
- If Option C is selected, define the blocker and route to the responsible seat.
- Decision preserves ADR-0031, the accepted company frame, the accepted department summary boundary, Task API payload `{ content }`, model-gateway security boundary, Admin/Workspace separation, local/demo scope, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no department CRUD/workflow routing, no complex organization, no business modules, no secrets, and no execution-loop/runtime behavior change.

## Verification

Gate-only review. No implementation verification is required at this decision step.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Selected option: Option A - Local/Demo Department Catalog Evidence.

Reason:

- The Workspace Company Department Catalog Summary slice is already accepted, and the remaining gap is browser-visible local/demo evidence.
- Option A is verification-only and does not change product behavior, APIs, schema, persistence, execution, routing, model selection, Project Memory, or runtime behavior.
- The evidence pass preserves ADR-0031, the accepted frontend-only boundary, model-gateway security, Admin/Workspace separation, and local/demo scope.

Approved scope:

- Verification-only local/demo evidence for the accepted department catalog summary.
- Start or reuse local backend and frontend.
- Verify the operation console renders the `公司工作区` frame and `部门目录` summary.
- Verify active official department type count, category summary, and non-secret department labels are visible when returned by the existing API.
- Verify no secret-like metadata is visible.
- Verify task creation still sends `{ "content": "..." }`.
- Capture screenshot or browser-visible evidence.
- Record evidence in a review file and update source-of-truth status files.

Forbidden scope remains:

- New product feature.
- Frontend design expansion beyond evidence-only corrections.
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

Approved Option A. Verification-only local/demo evidence passed with browser-visible evidence in `reviews/078_workspace_department_catalog_local_demo_evidence_review.md` and screenshot artifact `reviews/078_workspace_department_catalog_local_demo_evidence.png`.

Handoff: final closeout
