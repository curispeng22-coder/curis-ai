# Model Gateway AI Task Executor MVP Local/Demo First-Version Release Record

Date: 2026-07-08

Status: closeout package ready for quality verification.

Release type: local/demo first version only; not hosted production SaaS.

Source issue: `issues/076_model_gateway_post_rc_next_phase_gate.md`

Accepted release-candidate package: `docs/release/model-gateway-local-demo-rc.md`

Accepted release-candidate evidence: `reviews/072_model_gateway_local_demo_release_candidate_review.md`

## Release Closeout Decision Package

This closeout package records the model-gateway-enabled AI Task Executor MVP as ready for local/demo first-version closeout verification.

It does not approve:

- hosted production deployment;
- Admin Platform implementation;
- billing, ROI, packages, or marketplace;
- secret persistence or secret display;
- provider SDK or direct provider calls;
- New API source changes or New API internal database dependency;
- Task API payload, persistence/schema, execution-loop, or runtime behavior changes.

## Included Local/Demo Capability

The local/demo first-version closeout covers:

- New API local deployment as the first model gateway.
- Workspace model execution constrained to `ModelGatewayAdapter`.
- Official model catalog metadata reads.
- Official tool catalog metadata reads.
- UsageEvent model-call fields limited to approved non-secret meter fields.
- ADR-0029 runtime secret guardrails.
- Tenant-scoped default model preference backend APIs.
- Workspace operation-console model preference selector.
- Local E2E evidence for preference read/save/reset and content-only task creation.

## Evidence Record

| Area | Evidence |
| --- | --- |
| Original local/demo v0.1 release record | `docs/release/ai-task-executor-mvp-v0.1-release-record.md` |
| Model gateway local/demo RC package | `docs/release/model-gateway-local-demo-rc.md` |
| Model gateway local/demo RC acceptance | `reviews/072_model_gateway_local_demo_release_candidate_review.md` |
| New API local deployment | `docs/deployment/new-api-local.md`, `reviews/065_new_api_local_deployment_review.md` |
| ModelGatewayAdapter path | `issues/065_workspace_model_gateway_adapter.md`, `reviews/062_workspace_model_gateway_adapter_review.md` |
| Official model catalog | `issues/066_workspace_official_model_catalog.md`, `reviews/063_workspace_official_model_catalog_review.md` |
| Official tool catalog | `issues/067_workspace_official_tool_catalog.md`, `reviews/064_workspace_official_tool_catalog_review.md` |
| Model gateway security boundary | `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`, `reviews/066_model_gateway_production_security_boundary_review.md` |
| Runtime secret guardrails | `issues/070_model_gateway_runtime_secret_guardrails.md`, `reviews/067_model_gateway_runtime_secret_guardrails_review.md` |
| Tenant model preference backend | `issues/072_workspace_tenant_model_preference_first_slice.md`, `reviews/069_workspace_tenant_model_preference_first_slice_review.md` |
| Workspace model preference UI | `issues/073_workspace_model_preference_ui_gate.md`, `reviews/070_workspace_model_preference_ui_review.md` |
| Local E2E preference/task evidence | `issues/074_workspace_model_preference_local_e2e_evidence.md`, `reviews/071_workspace_model_preference_local_e2e_review.md` |

## Restore Points

- Original AI Task Executor MVP v0.1 verified restore point: `c5011acd`.
- Model-gateway-enabled local/demo release-candidate package commit: `9bfc7d8b`.

The first-version closeout package should be treated as the documentation/evidence closeout layer over the accepted model-gateway RC package. Any rollback must use the non-destructive project-approved git workflow.

## Operator Handoff Summary

Primary runbook:

- `docs/release/model-gateway-local-demo-rc.md`
- `docs/deployment/new-api-local.md`

Local backend:

```bash
cd backend
CURIS_DB=data/curis.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:3000 \
CURIS_MODEL_GATEWAY_ID=newapi-local \
CURIS_MODEL_GATEWAY_MODEL=<model-name-enabled-in-new-api> \
CURIS_MODEL_GATEWAY_API_KEY=<new-api-token> \
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Local frontend:

```bash
cd frontend
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000 npm run dev -- --hostname 127.0.0.1 --port 3000
```

New API local gateway:

```bash
cd deploy/new-api
docker compose up -d
```

Local secret handling:

- Keep New API tokens, provider keys, session secrets, and Authorization values outside Git.
- Use ignored local env files, shell environment, local password manager, New API local configuration, or New API local data only.
- Do not store New API tokens or provider credentials in Curis database rows.

## Final Local/Demo Checklist

Before final closeout acceptance, 质量运行席 should verify or confirm accepted evidence for:

- backend regression;
- focused model gateway, runtime guardrail, and tenant preference tests;
- frontend view-model tests, lint, and build;
- local preference read/save/reset;
- content-only Task API payload;
- UsageEvent model-call field allowlist;
- official model/tool catalog non-secret metadata;
- model calls constrained to `ModelGatewayAdapter`;
- documentation package diff hygiene;
- no backend/frontend behavior-file drift for closeout;
- source-of-truth status alignment.

## Known Gap Confirmation

Local/demo non-blockers:

- Local CORS origin must include the active frontend port when not using the default.
- New API local setup depends on operator-owned upstream provider configuration outside Curis source control.
- Docker, Colima, and New API local state can affect local E2E availability.
- FastAPI Python deprecation warning remains deferred unless separately reopened.

Hosted-production blockers:

- Hosted production deployment remains unapproved.
- Production secret-manager retrieval remains blocked pending a separate security-approved issue.
- Billing, ROI, tenant packages, marketplace, Admin Platform implementation, provider-specific execution, and production rollout remain blocked.
- New API source changes, New API internal database dependency, provider SDK/direct provider calls, and Curis DB credential persistence remain blocked.

Future product scope, not this closeout:

- Model optimization.
- Per-department or per-employee model policy.
- Package selection or marketplace.
- Hosted tenant onboarding.
- Production operations dashboard.

## Next Backlog Decision

After quality verification and product acceptance of this closeout package, 产品规划席 should choose the next bounded gate.

The next gate must preserve:

- model-gateway security boundary;
- local/demo versus hosted-production separation;
- Task API payload shape `{ content }`;
- Tool System v1.8 execution-loop boundary;
- no ROI, billing, package, marketplace, Admin Platform implementation, Employee CRUD/expansion, business modules, multi-agent routing, or agent abstraction unless separately approved.

## Closeout Boundary

This closeout package is documentation/evidence only. It is ready for 质量运行席 verification and does not itself introduce implementation behavior.
