---
issue: "070"
title: "Model Gateway Runtime Secret Guardrails"
status: "done"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/069_model_gateway_production_security_boundary.md"
---

# Model Gateway Runtime Secret Guardrails

## Objective

Implement the bounded runtime guardrails required by ADR-0029 before production external-model operation.

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`
- `reviews/066_model_gateway_production_security_boundary_review.md`
- `issues/065_workspace_model_gateway_adapter.md`

## Scope

- Add startup/runtime validation for required model gateway environment configuration when the runtime model gateway path is enabled.
- Add redaction guards for model gateway error surfaces so API keys, tokens, Authorization headers, prompts, outputs, raw HTTP payloads, and secret-like values are not exposed.
- Add UsageEvent allowlist regression for model gateway metering fields.
- Add no-secret regression around gateway/model metadata and catalog surfaces.
- Keep model execution constrained to `ModelGatewayAdapter`.

## Non-Goals

- No UI.
- No billing, ROI, tenant package, or platform governance implementation.
- No New API source-code modification.
- No New API internal database dependency.
- No Curis Workspace database persistence of credentials.
- No provider-specific SDK.
- No new provider path beyond the existing New API OpenAI-compatible adapter.
- No Admin Platform implementation.

## Allowed Files

- `backend/app/model_gateway.py`
- `backend/app/main.py`
- `backend/app/result_store.py`
- `backend/app/model_catalog.py`
- `backend/tests/test_model_gateway_adapter.py`
- `backend/tests/test_d5_newapi_gateway.py`
- `backend/tests/test_d5_qa_boundary.py`
- New focused backend tests if needed.
- `reviews/067_model_gateway_runtime_secret_guardrails_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Acceptance Criteria

- Missing required model gateway runtime env config fails closed with a clear non-secret error when gateway execution is enabled.
- Model gateway exceptions and API responses do not expose API keys, bearer tokens, Authorization headers, prompt text, output text, or raw HTTP payloads.
- UsageEvent payloads for model gateway execution include only approved model-meter fields plus existing non-secret envelope/idempotency fields.
- `model_gateways`, `official_models`, `/api/catalog/models`, `/api/platform/gateways`, and `/api/platform/models` do not expose secret values.
- Tests prove secret-like values are redacted or absent from runtime errors and UsageEvent payloads.
- Backend regression passes.

## Verification

- Focused backend tests for model gateway runtime guardrails.
- Secret pattern scan outside ignored local files and runtime/test data.
- Backend regression: `../backend/.venv/bin/python -m unittest discover tests` from `backend/`.

## Completion Notes

- Implemented startup/runtime model gateway config validation in `backend/app/model_gateway.py` and `backend/app/main.py`; partial runtime env config now fails closed without echoing values.
- Implemented model gateway request/response error redaction for bearer tokens, API-key-like values, prompt text, raw response text, and secret-like strings.
- Implemented UsageEvent redaction for allowed gateway meter fields while preserving the existing non-secret envelope/idempotency fields.
- Implemented gateway/model metadata guardrails in `backend/app/model_catalog.py` to reject secret-like metadata values before persistence or API exposure.
- Added regression coverage in `backend/tests/test_model_gateway_adapter.py` and `backend/tests/test_d5_qa_boundary.py`.
- Delivery evidence recorded in `reviews/067_model_gateway_runtime_secret_guardrails_review.md`.
- Backend regression: 203 tests passed.
- Handoff: sent to 质量运行席.
