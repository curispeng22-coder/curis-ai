---
issue: "069"
title: "Model Gateway Production Security Boundary"
status: "done"
owner: "安全边界席"
date: "2026-07-08"
depends_on: "issues/068_new_api_local_deployment.md"
---

# Model Gateway Production Security Boundary

## Objective

Define the production-safe boundary for Curis Workspace model gateway configuration after local New API + DeepSeek verification.

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/068_new_api_local_deployment.md`
- `reviews/065_new_api_local_deployment_review.md`
- `docs/deployment/new-api-local.md`

## Scope

- Define secret-handling rules for New API admin credentials, Curis New API token, and upstream provider API keys.
- Define the boundary between Admin Platform-owned official gateway/channel configuration and Workspace-owned runtime consumption.
- Define local, test, and production configuration expectations.
- Define minimum key rotation, disable, and incident response rules.
- Define what Workspace may log in `usage_event` and what must never be logged.
- Define whether any follow-up implementation is needed before broader Workspace/Admin parallel development.

## Non-Goals

- No Admin Platform UI.
- No billing, tenant packages, ROI, or platform governance implementation.
- No new model provider implementation beyond the verified New API OpenAI-compatible path.
- No New API source-code modification.
- No dependency on New API internal database tables.
- No credential persistence in Curis Workspace database.

## Allowed Files

- `issues/069_model_gateway_production_security_boundary.md`
- `reviews/066_model_gateway_production_security_boundary_review.md`
- `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`
- `docs/deployment/new-api-local.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Acceptance Criteria

- Security boundary states where each credential may live for local/test/production.
- Security boundary states which credentials must never enter Git, docs, logs, UsageEvent payloads, or Curis Workspace database.
- Admin Platform vs Workspace responsibility split is explicit.
- New API remains a model gateway only, not Curis primary system.
- Workspace model calls remain constrained to `ModelGatewayAdapter`.
- UsageEvent allowed fields are confirmed: `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, `status`.
- Any required follow-up implementation issue is named and routed.

## Verification

- Secret-scan evidence for supplied upstream key outside ignored local files and New API local data.
- Scope check confirms no UI, billing, ROI, tenant package, or New API source changes.
- Boundary review is recorded in `reviews/066_model_gateway_production_security_boundary_review.md`.

## Completion Notes

- Production security boundary accepted in `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`.
- Review evidence recorded in `reviews/066_model_gateway_production_security_boundary_review.md`.
- New API remains a model gateway only; Curis must not modify New API source code or depend on New API internal database tables.
- Secret values must never enter Git, docs, logs, UsageEvent payloads, traces, task payloads/results, or Curis Workspace database tables.
- Local New API token and New API local data remain limited to ignored local paths; production secrets require env/secret-manager/KMS/Vault injection.
- Admin Platform owns official gateway/model metadata and enable/disable decisions only; Workspace owns runtime consumption through `ModelGatewayAdapter` only.
- UsageEvent model-meter fields are confirmed as `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, and `status`; prompts, outputs, Authorization headers, raw HTTP payloads, and secrets are forbidden.
- Broader Workspace/Admin parallel development may proceed inside this boundary.
- Required production follow-up before external-model production operation: `issues/070_model_gateway_runtime_secret_guardrails.md`, routed to 系统交付席 when opened.
- Handoff: sent to 系统交付席 with compact payload in `reviews/066_model_gateway_production_security_boundary_review.md`.
