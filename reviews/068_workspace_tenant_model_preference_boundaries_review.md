# Review 068: Workspace Tenant Model Preference Foundation Boundaries

Date: 2026-07-08

Issue: `issues/071_workspace_tenant_model_preference_gate.md`

## Delivery Result

PASS-FOR-QUALITY-PLANNING.

Workspace Tenant Model Preference Foundation boundaries are defined in `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md`.

## Boundary Defined

- Tenant-scoped default model preference is metadata-only state over active `source=official` model catalog entries.
- Admin Platform remains owner of official model/gateway metadata.
- Workspace owns tenant preference storage and deterministic runtime preference resolution only.
- ADR-0029 and runtime secret guardrails remain mandatory.
- Runtime model execution remains constrained to `ModelGatewayAdapter`.
- Backend-first implementation is allowed; Workspace UI selector remains blocked unless separately approved.

## Allowed First Slice

- A tenant-scoped preference table with non-secret metadata only.
- A backend preference resolver that validates active official catalog metadata before runtime use.
- Workspace preference API/read model:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference`
  - optional `DELETE /api/workspace/model-preference`
- Focused backend tests for tenant isolation, catalog validation, no-secret persistence/exposure, and execution-path preservation.

## Blocked Scope

- Admin UI.
- Workspace complex UI.
- Billing, ROI, tenant package, marketplace, or automatic model optimization.
- Secret storage, credential persistence/exposure, provider SDK, direct provider calls, New API source changes, or New API internal DB dependency.
- Per-department or per-employee model policy.
- Tool routing, workflow mutation, Tool System v1.8 loop changes, or execution path drift.

## Verification Plan

Required quality checks for the boundary:

```bash
git diff --check -- docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md reviews/068_workspace_tenant_model_preference_boundaries_review.md issues/071_workspace_tenant_model_preference_gate.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/003_Architecture.md knowledge/PROJECT_MEMORY.md
rg -n "secret|credential|Authorization|provider SDK|direct provider|New API internal|ROI|billing|tenant package|marketplace|automatic model optimization|per-department|per-employee|ModelGatewayAdapter" docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md reviews/068_workspace_tenant_model_preference_boundaries_review.md
git diff --name-only -- docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md reviews/068_workspace_tenant_model_preference_boundaries_review.md issues/071_workspace_tenant_model_preference_gate.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/003_Architecture.md knowledge/PROJECT_MEMORY.md
git diff --cached --name-only -- backend frontend
```

Expected evidence:

- Documentation diff only for boundary/review/source-of-truth files.
- Boundary explicitly preserves ADR-0029, runtime secret guardrails, official model catalog metadata boundary, and `ModelGatewayAdapter`.
- Boundary blocks UI, billing, ROI, tenant package, secret storage, provider SDK, New API source/internal DB dependency, marketplace, automatic model optimization, per-department/per-employee policy, direct provider calls, and execution path drift.
- Staged boundary delivery contains no backend or frontend implementation files.

Delivery evidence:

- `git diff --cached --check`: passed.
- Keyword boundary scan returned the expected explicit preserve/block references in ADR-0030 and this review.
- Staged backend/frontend implementation guard returned no files.
- Staged files are limited to the boundary ADR, review, issue, and source-of-truth context updates.

## Recommended Next Issue

```text
issues/072_workspace_tenant_model_preference_first_slice.md
```

First implementation should remain backend-only and TDD-driven.

## Known Gaps

- No implementation is included in this boundary task.
- Exact fallback behavior for invalid stored preference must be locked in the implementation issue before code changes.

## Quality Verification

PASS.

Fresh boundary verification was run by 质量运行席 on commit `9dd75340`.

Commands:

```bash
git diff --check 9dd75340^ 9dd75340
git diff --name-only 9dd75340^ 9dd75340
git diff --name-only 9dd75340^ 9dd75340 -- backend frontend admin-platform workspace shared deploy plugins tools data
rg -n "ADR-0029|runtime secret guardrails|official model catalog|source=official|active|ModelGatewayAdapter|metadata-only|secret|credential|Authorization|provider SDK|direct provider|New API source|New API internal DB|ROI|billing|tenant package|marketplace|automatic model optimization|per-department|per-employee|execution path drift|Admin UI|Workspace complex UI" docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md reviews/068_workspace_tenant_model_preference_boundaries_review.md issues/071_workspace_tenant_model_preference_gate.md
rg -n "ModelGatewayAdapter|provider SDK|direct New API|direct provider|tool routing|workflow mutation|Tool System v1.8|execution loop|execution path" docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md reviews/068_workspace_tenant_model_preference_boundaries_review.md
git show --stat --oneline 9dd75340
```

Evidence:

- Boundary diff hygiene passed for commit `9dd75340`.
- Commit files are limited to boundary ADR, issue/review evidence, and source-of-truth status/context updates.
- Backend/frontend/shared runtime implementation guard returned no files.
- Boundary scan confirmed explicit preservation of ADR-0029, runtime secret guardrails, active `source=official` catalog source, metadata-only tenant preference state, and `ModelGatewayAdapter` as the constrained execution path.
- Scope scan confirmed explicit blocks for Admin UI, Workspace complex UI, billing, ROI, tenant package, secret storage, provider SDK, direct provider calls, New API source/internal DB dependency, marketplace, automatic model optimization, per-department/per-employee policy, credential persistence/exposure, tool routing/workflow mutation, Tool System v1.8 loop changes, and execution path drift.

Acceptance Check:

- Boundary-only requirement is satisfied; no implementation file entered the boundary commit.
- Tenant preference persistence is bounded to metadata-only state over approved active `source=official` model catalog entries.
- Future implementation verification requirements cover tenant isolation, no-secret persistence/exposure, catalog validation, and execution-path preservation.
- No blocker found.

Quality Result: PASS.

## Product Acceptance

ACCEPTED by 产品规划席 on 2026-07-08.

Reason:

- Boundary verification passed for commit `9dd75340`.
- Boundary-only scope was preserved with no backend/frontend implementation files.
- ADR-0029, runtime secret guardrails, official model catalog metadata boundary, and `ModelGatewayAdapter` execution path are preserved.
- Recommended first slice is accepted as backend-only implementation in `issues/072_workspace_tenant_model_preference_first_slice.md`.

## Handoff

Delivery Handoff: sent to 质量运行席

Next Seat: 产品规划席

Handoff: sent to 产品规划席

Payload sent:

```text
Issue: issues/071_workspace_tenant_model_preference_gate.md
Objective: Accept Workspace Tenant Model Preference Foundation architecture-boundary verification for commit 9dd75340.
Special Constraints: Boundary verification passed with no blockers. Boundary-only scope preserved; no backend/frontend implementation files entered the commit. ADR-0029, runtime secret guardrails, official model catalog metadata boundary, and ModelGatewayAdapter-only execution path are preserved.
Next Seat: 系统交付席 for first-slice issue only after product acceptance.
```
