---
issue: "071"
title: "Workspace Tenant Model Preference Foundation Gate"
status: "approved"
owner: "总控决策席"
date: "2026-07-08"
depends_on: "issues/070_model_gateway_runtime_secret_guardrails.md"
---

# Workspace Tenant Model Preference Foundation Gate

## Objective

Approve or reject the next bounded Workspace slice: tenant-scoped default model preference over approved official model catalog metadata.

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/066_workspace_official_model_catalog.md`
- `issues/070_model_gateway_runtime_secret_guardrails.md`
- `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`

## Product Intent

Curis Workspace has verified New API + DeepSeek model execution and accepted runtime secret guardrails. The next product step is to move from local environment-selected runtime model toward tenant-owned Workspace selection from platform-provided official model metadata.

This supports the commercial multi-tenant product logic:

- Admin Platform supplies official model/gateway capability metadata.
- Workspace consumes approved capabilities and lets each tenant choose a default model.
- Runtime execution resolves the model preference without exposing or storing secrets.

## Scope For Boundary Definition

- Define a tenant-scoped default model preference foundation.
- Use only approved official model catalog metadata as selectable source.
- Allow Workspace runtime to resolve a default model from tenant preference when available.
- Preserve `ModelGatewayAdapter` as the only model execution path.
- Preserve ADR-0029 secret guardrails and no-secret metadata rules.
- Define required API/read-model shape before implementation.

## Non-Goals

- No Admin Platform UI.
- No Workspace complex UI.
- No billing, ROI, tenant package, or platform governance implementation.
- No secret storage in Curis DB.
- No provider SDK.
- No New API source-code modification.
- No New API internal database dependency.
- No model marketplace.
- No automatic model selection or optimization.
- No per-department/per-employee model policy.

## Gate Questions

- Is tenant-scoped default model preference inside the current Workspace/Admin shared-contract direction?
- Is persistence for a tenant preference allowed as metadata-only state?
- Should implementation be backend-only first, or is a minimal Workspace UI selector allowed later under a separate issue?
- What verification is required to prove no secret exposure and no execution-path drift?

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Approved scope:

- Tenant-scoped default model preference is inside the current Workspace/Admin shared-contract direction when it consumes only approved official model catalog metadata.
- Persistence for tenant preference is allowed as metadata-only state, limited to tenant/model/gateway references and no credential values.
- The next step is architecture boundary definition by 系统交付席 before implementation.
- Implementation should be backend-first for preference storage/resolution; any minimal Workspace UI selector requires a separate approved issue after the backend boundary is accepted.

Required verification:

- Prove selected models come only from active `source=official` model catalog metadata.
- Prove no API keys, tokens, passwords, credential values, provider credentials, Authorization headers, prompts, outputs, raw HTTP payloads, or New API internal ids are stored or exposed.
- Prove runtime model execution remains constrained to `ModelGatewayAdapter`.
- Prove no New API source-code modification, no New API internal database dependency, no provider SDK, and no direct provider execution path.
- Prove no Admin UI, Workspace complex UI, billing, ROI, tenant package, marketplace, automatic model optimization, or per-department/per-employee model policy is introduced.

## Acceptance Criteria

- Gate decision states approved or blocked.
- If approved, next seat is 系统交付席 for architecture boundary definition.
- Gate keeps model execution constrained to `ModelGatewayAdapter`.
- Gate explicitly preserves ADR-0029 and runtime guardrail boundaries.
- Gate explicitly blocks UI, billing, ROI, tenant package, provider SDK, New API source changes, New API internal DB dependency, and credential persistence.

## Completion Notes

Approved. Route to 系统交付席 for architecture boundary definition.

Architecture boundary definition completed by 系统交付席:

- Boundary ADR: `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md`
- Boundary evidence: `reviews/068_workspace_tenant_model_preference_boundaries_review.md`
- Recommended implementation issue: `issues/072_workspace_tenant_model_preference_first_slice.md`
- Boundary status: ready for 质量运行席 verification.
- Handoff: sent to 质量运行席.

Handoff: sent to 质量运行席

Compact payload:

- Issue: `issues/071_workspace_tenant_model_preference_gate.md`
- Objective: Verify Workspace Tenant Model Preference Foundation architecture boundaries before implementation.
- Special Constraints: Preserve ADR-0029, runtime secret guardrails, official model catalog metadata boundary, and `ModelGatewayAdapter` as the only execution path. Tenant preference persistence is allowed only as metadata-only state over approved active `source=official` model catalog entries.
- Forbid: Admin UI, Workspace complex UI, billing, ROI, tenant package, secret storage, provider SDK, New API source changes, New API internal DB dependency, marketplace, automatic model optimization, per-department/per-employee model policy, credential persistence/exposure, direct provider calls, and execution path drift.
- Next Seat: 质量运行席.
