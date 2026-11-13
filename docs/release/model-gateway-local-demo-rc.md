# Model Gateway Local/Demo Release Candidate

Date: 2026-07-08

Status: documentation/evidence package ready for quality verification.

Source issue: `issues/075_model_gateway_local_demo_release_candidate_gate.md`

Release baseline: AI Task Executor MVP local/demo v0.1 plus accepted model-gateway capability slices.

This package does not approve hosted production deployment. It does not change backend behavior, frontend behavior, API semantics, persistence/schema, task payloads, execution-loop behavior, or runtime model routing.

## Included Local/Demo Capability

The model-gateway-enabled local/demo release candidate covers:

- New API local deployment as the first model gateway.
- Workspace model calls constrained to `ModelGatewayAdapter`.
- Official model catalog read model with active `source=official` model metadata.
- Official tool catalog read model with active official tool metadata.
- UsageEvent model-call accounting fields limited to approved non-secret meter fields.
- ADR-0029 runtime secret guardrails.
- Tenant-scoped default model preference backend APIs.
- Workspace operation-console model preference selector.
- Local E2E evidence for preference read/save/reset and ordinary task creation.

## Evidence Map

| Capability | Evidence | Accepted result |
| --- | --- | --- |
| New API local deployment | `docs/deployment/new-api-local.md`, `reviews/065_new_api_local_deployment_review.md` | Local New API container reached, `/v1/models` verified, smoke script succeeded, Workspace task execution wrote `usage.model_call`. |
| Model gateway adapter | `issues/065_workspace_model_gateway_adapter.md`, `reviews/062_workspace_model_gateway_adapter_review.md` | Default model calls route through New API-compatible `ModelGatewayAdapter`; backend regression passed. |
| Official model catalog | `issues/066_workspace_official_model_catalog.md`, `reviews/063_workspace_official_model_catalog_review.md` | Workspace reads active official model metadata without credential values. |
| Official tool catalog | `issues/067_workspace_official_tool_catalog.md`, `reviews/064_workspace_official_tool_catalog_review.md` | Workspace reads active official tool metadata without credential values. |
| Production security boundary | `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`, `reviews/066_model_gateway_production_security_boundary_review.md` | New API remains gateway-only; Curis DB stores no credential values; Workspace calls stay behind `ModelGatewayAdapter`. |
| Runtime secret guardrails | `issues/070_model_gateway_runtime_secret_guardrails.md`, `reviews/067_model_gateway_runtime_secret_guardrails_review.md` | Partial gateway env fails closed, gateway errors are redacted, UsageEvent payloads are allowlisted/redacted, metadata rejects secret-like values. |
| Tenant model preference backend | `issues/072_workspace_tenant_model_preference_first_slice.md`, `reviews/069_workspace_tenant_model_preference_first_slice_review.md` | Tenant-scoped read/write/delete APIs and runtime preference resolution passed focused tests and backend regression. |
| Model preference UI | `issues/073_workspace_model_preference_ui_gate.md`, `reviews/070_workspace_model_preference_ui_review.md` | Existing operation console can view/save/reset default model preference using existing APIs only; frontend tests/lint/build passed. |
| Local E2E evidence | `issues/074_workspace_model_preference_local_e2e_evidence.md`, `reviews/071_workspace_model_preference_local_e2e_review.md` | Real local backend/frontend verified preference read/save/reset and Task API content-only task creation. |

## Canonical Verification Commands

Run from the repository root unless a command starts with `cd`.

Backend regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Focused model gateway and preference tests:

```bash
cd backend && ./.venv/bin/python -m unittest tests.test_model_gateway_adapter tests.test_d5_qa_boundary tests.test_tenant_model_preference
```

Frontend operation-console checks:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
```

Documentation/package scope guards:

```bash
git diff --check
git diff --name-only HEAD -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}' . -g '!deploy/new-api/.env' -g '!deploy/new-api/data/**' -g '!backend/data/**' -g '!backend/tests/**' -g '!backend/.venv/**' -g '!frontend/node_modules/**' -g '!.git/**'
```

Expected results:

- Backend regression passes.
- Focused guardrail/preference tests pass.
- Frontend tests, lint, and build pass.
- Documentation/package diff contains no backend/frontend behavior files unless a separate approved stabilization issue exists.
- Secret scan returns no real secret-like values outside ignored local files and test/runtime data.

## Local Startup Runbook

Start or verify New API:

```bash
cd deploy/new-api
cp .env.example .env
docker compose up -d
```

Required local secret rule:

- Put the Curis New API token only in ignored local environment files, shell environment, local password manager, or New API local configuration.
- Do not commit tokens, provider keys, session secrets, Authorization headers, prompts, raw provider responses, or New API internal row ids.

Workspace backend:

```bash
cd backend
CURIS_DB=data/curis.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:3000 \
CURIS_MODEL_GATEWAY_ID=newapi-local \
CURIS_MODEL_GATEWAY_MODEL=<model-name-enabled-in-new-api> \
CURIS_MODEL_GATEWAY_API_KEY=<new-api-token> \
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Workspace frontend:

```bash
cd frontend
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000 npm run dev -- --hostname 127.0.0.1 --port 3000
```

If the frontend uses a non-default port, include it in backend CORS:

```bash
CURIS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:<frontend-port>
```

## Local/Demo E2E Checklist

1. Confirm backend health:

```bash
curl -s http://127.0.0.1:8000/health
```

2. Confirm model preference read:

```bash
curl -s -H 'X-Tenant-Id: tenant-demo' http://127.0.0.1:8000/api/workspace/model-preference
```

Expected boundary:

- Response contains `preference` and `available_models`.
- Available models are active official model metadata only.
- Response does not expose credential values, provider accounts, Authorization headers, prompts, raw gateway payloads, or New API internal ids.

3. Save tenant model preference:

```bash
curl -s -H 'Content-Type: application/json' -H 'X-Tenant-Id: tenant-demo' \
  -X PUT http://127.0.0.1:8000/api/workspace/model-preference \
  -d '{"model_key":"official.newapi.default"}'
```

4. Reset tenant model preference:

```bash
curl -s -H 'X-Tenant-Id: tenant-demo' \
  -X DELETE http://127.0.0.1:8000/api/workspace/model-preference
```

5. Verify ordinary task creation still uses content-only payload:

```bash
curl -s -H 'Content-Type: application/json' \
  -X POST http://127.0.0.1:8000/api/task \
  -d '{"content":"模型网关本地发布候选验证任务"}'
```

6. Run the returned task id when New API local gateway is configured:

```bash
curl -s -X POST http://127.0.0.1:8000/api/task/<task_id>/run \
  -H 'X-Tenant-Id: tenant-demo' \
  -H 'X-Ceo-Id: ceo-local'
```

7. Confirm UsageEvent model-call fields:

```bash
curl -s 'http://127.0.0.1:8000/api/platform/usage?tenant_id=tenant-demo' \
  -H 'X-Platform-Admin-Token: platform-admin-dev'
```

Allowed UsageEvent model-meter fields:

- `tenant_id`
- `task_id`
- `model_gateway_id`
- `model_name`
- `token`
- `estimated_cost`
- `status`

## Known-Gap Classification

Local/demo non-blockers:

- Local CORS origin must include the active frontend port when not using the default.
- New API local setup requires an operator-owned upstream provider account/key configured outside Curis source control.
- FastAPI Python deprecation warning remains a deferred known gap from the v0.1 release record unless separately reopened.
- Local/demo verification may depend on local Docker/Colima/New API state.

Hosted-production blockers:

- Hosted production deployment is not approved by this release candidate.
- Production secret-manager retrieval is not implemented and remains blocked pending a separate security-approved issue.
- Billing, ROI, tenant packages, marketplace, Admin Platform implementation, provider-specific execution, and production rollout remain blocked.
- New API source changes, New API internal database dependency, provider SDK/direct provider calls, and Curis DB credential persistence remain blocked.

Future product scope, not local/demo RC scope:

- Model optimization, per-department policy, per-employee policy, package selection, marketplace, hosted tenant onboarding, and production operations dashboards.

## Release Decision Boundary

This document prepares a quality-verifiable release-candidate package. It does not itself declare product acceptance.

Acceptance requires 质量运行席 to verify the checklist and 产品规划席 or the main thread to accept the evidence.
