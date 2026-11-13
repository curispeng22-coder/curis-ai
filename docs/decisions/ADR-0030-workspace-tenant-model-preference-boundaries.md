# ADR-0030: Workspace Tenant Model Preference Foundation Boundaries

Date: 2026-07-08

Status: Proposed for quality verification

Issue: `issues/071_workspace_tenant_model_preference_gate.md`

## Context

Curis Workspace has accepted the Model Gateway production security boundary and completed the runtime secret guardrails required by ADR-0029. The official model catalog is available as metadata-only Workspace input, and default model execution is already constrained to:

```text
Workspace runtime -> ModelGatewayAdapter -> New API OpenAI-compatible API
```

The next bounded slice lets a tenant choose a default model from approved official catalog metadata without changing the execution path or storing credentials.

## Decision

Workspace may add a tenant-scoped default model preference foundation as metadata-only state. The preference may reference only active `source=official` model catalog entries and their approved gateway/model metadata.

The preference is not a model marketplace, model optimizer, tenant package, billing feature, department policy, employee policy, or provider credential feature. It is only a tenant-owned default-model reference used by Workspace runtime resolution.

All runtime model execution remains constrained to `ModelGatewayAdapter`. The preference layer may choose adapter configuration metadata, but it must not call New API directly, call provider SDKs, add provider-specific execution paths, mutate tool routing, or change the Tool System v1.8 execution loop.

## Source Of Truth And Ownership

- Admin Platform owns official model and gateway metadata.
- Workspace owns tenant preference storage and runtime preference resolution.
- ADR-0029 owns secret handling and external-service boundaries.
- Runtime secret guardrails from `issues/070_model_gateway_runtime_secret_guardrails.md` remain mandatory.

Workspace preference writes must validate against the current active official catalog. If the referenced model is not active, not `source=official`, missing, or has no usable default model name, the write must fail closed with a non-secret error.

Runtime resolution must revalidate the stored preference against active official catalog metadata before use. If a stored preference becomes inactive or invalid, runtime must fail closed or fall back only to the existing approved default gateway behavior as explicitly defined by the implementation issue; it must not silently choose another model by optimization.

## Persistence Boundary

First implementation may add a single metadata-only preference record per tenant.

Allowed persisted fields:

- `tenant_id`
- `model_key`
- `gateway_ref`
- `model_name`
- `source`
- `updated_at`

The persisted `model_name` and `gateway_ref` must be derived from an active `source=official` catalog row at write time. Runtime must still revalidate against the official catalog before use.

Forbidden persisted fields:

- API keys, bearer tokens, provider credentials, admin passwords, session secrets, Authorization headers, raw HTTP payloads, prompts, outputs, credential values, New API internal ids, New API channel ids, provider account ids, billing fields, ROI fields, package fields, department policy fields, employee policy fields, or automatic optimization state.

No Curis DB credential persistence is approved.

## API And Read Model Boundary

Backend-first implementation is allowed. Workspace UI implementation is not approved by this ADR.

Allowed API shape:

- `GET /api/workspace/model-preference`
  - Tenant-scoped read using the existing tenant context.
  - Returns the current preference and active official model options needed by a future UI.
  - Returns only non-secret catalog/preference fields.
- `PUT /api/workspace/model-preference`
  - Tenant-scoped write with payload `{ "model_key": "..." }`.
  - Validates `model_key` against active `source=official` catalog metadata.
  - Persists only metadata-only preference fields.
- `DELETE /api/workspace/model-preference`
  - Tenant-scoped clear operation if the implementation issue chooses to support reset.

Allowed read model fields:

- `tenant_id`
- `model_key`
- `gateway_ref`
- `model_name`
- `display_name`
- `provider_id`
- `source`
- `status`
- `updated_at`
- `available_models` containing active official catalog entries with the existing non-secret catalog shape.

The API must not expose `credential_ref` to Workspace, secret values, Authorization headers, prompts, outputs, raw gateway payloads, New API internal ids, or provider account metadata.

## Runtime Resolution Boundary

Future implementation may add a deterministic resolver used by the existing Workspace runtime path:

```text
TenantContext -> TenantModelPreferenceResolver -> official_models metadata -> ModelGatewayAdapter
```

Resolver responsibilities:

- Read only the current tenant preference.
- Revalidate the preference against active `source=official` metadata.
- Provide `gateway_id` and `model_name` to `ModelGatewayAdapter`.
- Return a non-secret blocker if the preference is invalid or unavailable.

Resolver non-responsibilities:

- No tool routing.
- No workflow mutation.
- No automatic model optimization.
- No model A/B selection.
- No provider SDK.
- No direct New API call.
- No credential retrieval beyond the already approved environment-based adapter behavior.
- No per-department, per-employee, or role-based policy.

## Verification Requirements

Implementation verification must prove:

- Preferences can reference only active `source=official` model catalog entries.
- Preference reads/writes are tenant-scoped.
- Preference persistence has no secret columns and stores no secret-like values.
- Workspace preference APIs expose no credentials, Authorization headers, prompts, outputs, raw HTTP payloads, New API internal ids, billing fields, ROI fields, tenant-package fields, marketplace fields, department-policy fields, employee-policy fields, or optimization state.
- Runtime model execution remains constrained to `ModelGatewayAdapter`.
- No direct provider calls, provider SDK, New API source change, or New API internal DB dependency is introduced.
- No Admin UI, Workspace complex UI, billing, ROI, tenant package, marketplace, automatic model optimization, per-department/per-employee model policy, credential persistence/exposure, or execution path drift is introduced.

Recommended first implementation issue:

```text
issues/072_workspace_tenant_model_preference_first_slice.md
```

Recommended first implementation files:

- `backend/app/database.py`
- `backend/app/model_preferences.py`
- `backend/app/main.py`
- `backend/tests/test_tenant_model_preference.py`
- `issues/072_workspace_tenant_model_preference_first_slice.md`
- `reviews/069_workspace_tenant_model_preference_first_slice_review.md`

## Consequences

Tenant model preference becomes a bounded Workspace metadata capability. It advances multi-tenant product readiness without introducing Admin UI, provider credentials, model marketplace behavior, model optimization, billing, ROI, tenant packages, department policy, employee policy, or execution path drift.
