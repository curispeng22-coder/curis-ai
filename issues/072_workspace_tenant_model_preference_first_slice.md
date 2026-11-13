---
issue: "072"
title: "Workspace Tenant Model Preference First Slice"
status: "done"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/071_workspace_tenant_model_preference_gate.md"
---

# Workspace Tenant Model Preference First Slice

## Objective

Implement the backend-only first slice for tenant-scoped default model preference over active official model catalog metadata.

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md`
- `reviews/068_workspace_tenant_model_preference_boundaries_review.md`
- `issues/066_workspace_official_model_catalog.md`
- `issues/070_model_gateway_runtime_secret_guardrails.md`

## Scope

- Add metadata-only tenant model preference persistence.
- Add a backend resolver that validates preferences against active `source=official` official model catalog metadata.
- Add backend Workspace APIs:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference`
  - `DELETE /api/workspace/model-preference` if reset is cheap and fully covered.
- Ensure runtime model resolution may use the tenant preference when available and valid.
- Preserve `ModelGatewayAdapter` as the only model execution path.
- Add focused backend tests for tenant isolation, catalog validation, no-secret persistence/exposure, runtime resolution, and execution-path preservation.

## Non-Goals

- No Admin UI.
- No Workspace complex UI.
- No billing, ROI, tenant package, marketplace, or automatic model optimization.
- No secret storage, credential persistence/exposure, provider SDK, direct provider calls, New API source change, or New API internal database dependency.
- No per-department/per-employee model policy.
- No tool routing, workflow mutation, Tool System v1.8 loop change, or execution path drift.

## Allowed Files

- `backend/app/database.py`
- `backend/app/model_preferences.py`
- `backend/app/main.py`
- `backend/app/model_gateway.py` only if dependency injection of resolved model metadata is required.
- `backend/tests/test_tenant_model_preference.py`
- `reviews/069_workspace_tenant_model_preference_first_slice_review.md`
- `issues/072_workspace_tenant_model_preference_first_slice.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Acceptance Criteria

- Preference write accepts only active `source=official` model catalog entries.
- Preference read/write/delete are tenant-scoped.
- Persisted preference stores only `tenant_id`, `model_key`, `gateway_ref`, `model_name`, `source`, and `updated_at`.
- Workspace preference API exposes no credential values, Authorization headers, prompts, outputs, raw HTTP payloads, New API internal ids, billing fields, ROI fields, tenant-package fields, marketplace fields, department-policy fields, employee-policy fields, or optimization state.
- Runtime resolution revalidates stored preference against official catalog metadata before use.
- Invalid stored preference behavior is explicit and covered by tests.
- Model execution remains constrained to `ModelGatewayAdapter`.
- Backend regression passes.

## Verification

- TDD red evidence for preference validation and no-secret exposure.
- Focused backend tests for tenant model preference.
- Backend regression: `../backend/.venv/bin/python -m unittest discover tests` from `backend/`.
- Secret pattern scan outside ignored local files and backend test/runtime data.
- Frontend diff guard shows no UI files changed.

## Completion Notes

- Implemented metadata-only tenant model preference persistence in `tenant_model_preferences`.
- Implemented backend resolver in `backend/app/model_preferences.py` that validates preferences against active `source=official` model catalog metadata before read/write/runtime use.
- Added backend Workspace APIs:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference`
  - `DELETE /api/workspace/model-preference`
- Runtime model execution remains behind `ModelGatewayAdapter`; valid tenant preference supplies adapter metadata only, and invalid/stale preference falls back to the existing default adapter metadata.
- Added focused TDD backend coverage in `backend/tests/test_tenant_model_preference.py`.
- Delivery evidence recorded in `reviews/069_workspace_tenant_model_preference_first_slice_review.md`.
- Focused tests: 4 passed.
- Backend regression: 207 tests passed.
- Handoff: sent to 质量运行席.
