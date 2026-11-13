---
issue: "073"
title: "Workspace Model Preference UI Gate"
status: "done"
owner: "总控决策席"
date: "2026-07-08"
depends_on: "issues/072_workspace_tenant_model_preference_first_slice.md"
---

# Workspace Model Preference UI Gate

## Objective

Approve or reject a bounded Workspace UI slice that exposes the accepted tenant-scoped default model preference in the existing AI Task Executor operation console.

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/071_workspace_tenant_model_preference_gate.md`
- `issues/072_workspace_tenant_model_preference_first_slice.md`
- `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md`
- `reviews/069_workspace_tenant_model_preference_first_slice_review.md`

## Product Intent

Curis Workspace now has backend-only tenant model preference APIs and runtime preference resolution. The next product step is to let the CEO see and set the tenant default model from the Workspace operation console, using only approved official model catalog metadata.

This is a usability bridge for the commercial two-product logic:

- Admin Platform supplies official model/gateway metadata and owns capability supply.
- Workspace lets each tenant choose from supplied official capabilities.
- Workspace does not manage provider secrets, billing, packages, marketplace, or platform governance.

## Scope For Gate Decision

- Allow or block a minimal Workspace UI selector for tenant default model preference.
- UI must stay inside the existing operation console shell.
- UI may read:
  - `GET /api/workspace/model-preference`
  - existing official model catalog metadata returned by that API.
- UI may write:
  - `PUT /api/workspace/model-preference` with `{ "model_key": "..." }`
  - `DELETE /api/workspace/model-preference` for reset.
- UI may show current preference, available official model options, save/reset state, and non-secret validation errors.
- UI copy should be Chinese.

## Non-Goals

- No Admin Platform page.
- No Workspace complex dashboard.
- No billing, ROI, tenant package, marketplace, or platform governance.
- No secret display, secret input, credential storage, credential reference editing, provider account editing, or New API channel editing.
- No provider SDK, direct provider call, New API source change, or New API internal database dependency.
- No model optimization, recommendation engine, A/B selection, per-department policy, per-employee policy, or automatic model switching.
- No Task API payload change.
- No execution-loop, tool-routing, workflow, persistence-schema, or backend semantic change unless separately approved.

## Gate Questions

- Is a minimal Workspace model preference selector allowed after backend-only preference acceptance?
- Should this UI be frontend-only over the existing preference APIs?
- What visual boundary keeps it operational and not a complex dashboard?
- What evidence is required to prove no secret exposure and no execution-path drift?

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Approved scope:

- A minimal Workspace model preference selector is allowed after backend-only preference acceptance.
- The first implementation must be frontend-only unless 系统交付席 documents a blocker.
- The UI must stay inside the existing Workspace operation console shell.
- The UI may only use existing Workspace preference APIs:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference` with `{ "model_key": "..." }`
  - `DELETE /api/workspace/model-preference`
- The UI may show current preference, available official model options, save/reset/loading/error states, and Chinese copy.
- Displayed metadata must remain non-secret official model catalog/preference metadata only.

Required verification:

- Prove frontend changes are limited to the existing Workspace operation console.
- Prove the UI calls only existing Workspace preference APIs and does not change Task API payloads.
- Prove no backend, Admin Platform, shared runtime, deployment, model gateway, or execution-loop files are changed unless separately approved.
- Prove UI copy/output does not expose credential-like fields, secret values, credential references, Authorization headers, prompts, outputs, raw gateway payloads, New API internal ids, provider account metadata, billing, ROI, packages, marketplace, model optimization, department policy, or employee policy.
- Prove ADR-0030, ADR-0029, runtime secret guardrails, official model catalog metadata boundary, and `ModelGatewayAdapter`-only execution are preserved.

## Acceptance Criteria

- Gate decision states approved or blocked.
- If approved, first implementation is frontend-only unless 系统交付席 documents a blocker.
- UI scope is limited to current preference, official model options, save/reset action, loading/error states, and Chinese copy.
- Gate preserves ADR-0030, ADR-0029, runtime secret guardrails, official model catalog metadata boundary, and `ModelGatewayAdapter`-only execution.
- Gate blocks Admin UI, complex UI, billing/ROI/package scope, secret handling scope, provider integration scope, model optimization scope, and execution behavior changes.

## Verification

- Frontend lint/build or project-standard frontend verification.
- UI diff guard proves no backend/Admin/shared/runtime-deploy changes unless separately approved.
- Text scan for credential-like fields in UI output.
- Manual or automated evidence that UI calls only Workspace preference APIs and displays only non-secret metadata.

## Completion Notes

Approved. Route to 系统交付席 for frontend-only implementation planning and delivery.

Handoff: HANDOFF_REQUIRED

Target seat: 系统交付席

Compact payload:

- Issue: `issues/073_workspace_model_preference_ui_gate.md`
- Objective: Implement a minimal frontend-only Workspace model preference selector inside the existing operation console.
- Special Constraints: Use only existing preference APIs; preserve ADR-0030, ADR-0029, runtime secret guardrails, official model catalog metadata boundary, current Task API payloads, and `ModelGatewayAdapter`-only execution.
- Allow: current preference display, official model options, save/reset/loading/error states, and Chinese copy inside the existing Workspace operation console.
- Forbid: Admin UI, complex dashboard, billing/ROI/packages, secret handling, provider integration, model optimization, backend semantic changes, Task API payload changes, execution behavior changes, backend persistence/schema changes, New API source/internal DB dependency, provider SDK, direct provider calls, per-department/per-employee policy, and execution path drift.
- Next Seat: 系统交付席.

## Implementation Notes

Implemented by 系统交付席 on 2026-07-08.

- Added a minimal frontend-only default model selector inside the existing Workspace operation console.
- Used only existing Workspace preference APIs:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference` with `{ "model_key": "..." }`
  - `DELETE /api/workspace/model-preference`
- Preserved the existing Task API payload shape `{ content }`.
- Added deterministic view-model tests for official model options, non-secret display metadata, and preference payload shape.
- Evidence is recorded in `reviews/070_workspace_model_preference_ui_review.md`.

Handoff: sent to 质量运行席

## Product Acceptance

Accepted by 产品规划席 on 2026-07-08.

- Quality verification passed in `reviews/070_workspace_model_preference_ui_review.md` for commit `5727410f`.
- Frontend-only scope stayed inside `frontend/app`.
- UI uses only existing Workspace preference APIs.
- Task API payload remains `{ content }`.
- Backend/Admin/shared/runtime execution paths were not changed.

Handoff: final closeout
