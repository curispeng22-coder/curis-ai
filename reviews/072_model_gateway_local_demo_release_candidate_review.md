# Review 072: Model Gateway Local/Demo Release Candidate Package

Date: 2026-07-08

Issue: `issues/075_model_gateway_local_demo_release_candidate_gate.md`

Owner: 系统交付席

Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now package the model-gateway-enabled AI Task Executor MVP as a local/demo release candidate with mapped evidence, runbook commands, and known-gap classification.

## Delivery Result

PASS for documentation/evidence package preparation.

No implementation or behavior change was made for this issue.

## Package Artifacts

- `docs/release/model-gateway-local-demo-rc.md`
- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `docs/deployment/new-api-local.md`
- `issues/075_model_gateway_local_demo_release_candidate_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/072_model_gateway_local_demo_release_candidate_review.md`

## Coverage

The package covers:

- New API model gateway local/demo path.
- Official model/tool catalog metadata reads.
- UsageEvent model-call fields.
- ADR-0029 runtime secret guardrails.
- Tenant model preference backend APIs.
- Workspace model preference UI.
- Local E2E evidence for preference read/save/reset and content-only task creation.
- Verification checklist and startup/runbook commands.
- Known local/demo gaps versus hosted-production blockers.

## Evidence Map

| Scope | Evidence |
| --- | --- |
| New API local deployment | `docs/deployment/new-api-local.md`, `reviews/065_new_api_local_deployment_review.md` |
| ModelGatewayAdapter-only execution | `issues/065_workspace_model_gateway_adapter.md`, `reviews/062_workspace_model_gateway_adapter_review.md` |
| Official model catalog metadata | `issues/066_workspace_official_model_catalog.md`, `reviews/063_workspace_official_model_catalog_review.md` |
| Official tool catalog metadata | `issues/067_workspace_official_tool_catalog.md`, `reviews/064_workspace_official_tool_catalog_review.md` |
| Production security boundary | `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`, `reviews/066_model_gateway_production_security_boundary_review.md` |
| Runtime secret guardrails | `issues/070_model_gateway_runtime_secret_guardrails.md`, `reviews/067_model_gateway_runtime_secret_guardrails_review.md` |
| Tenant model preference backend | `issues/072_workspace_tenant_model_preference_first_slice.md`, `reviews/069_workspace_tenant_model_preference_first_slice_review.md` |
| Workspace model preference UI | `issues/073_workspace_model_preference_ui_gate.md`, `reviews/070_workspace_model_preference_ui_review.md` |
| Local E2E evidence | `issues/074_workspace_model_preference_local_e2e_evidence.md`, `reviews/071_workspace_model_preference_local_e2e_review.md` |

## Verification Performed

Documentation/package whitespace check:

```bash
git diff --check
```

Result: passed.

Documentation package diff guard:

```bash
git diff --cached --name-only -- docs/release docs/deployment issues/075_model_gateway_local_demo_release_candidate_gate.md reviews/072_model_gateway_local_demo_release_candidate_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Result: package changes are documentation, issue/review, and source-of-truth status/context files only.

Staged behavior-file scope guard:

```bash
git diff --cached --name-only -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
```

Result: no backend/frontend behavior files changed.

Package secret-placeholder scan:

```bash
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}|(api[_-]?key|authorization|bearer)\s*[:=]\s*[A-Za-z0-9._-]{16,}' docs/release/model-gateway-local-demo-rc.md docs/release/ai-task-executor-mvp-v0.1-release-record.md docs/deployment/new-api-local.md issues/075_model_gateway_local_demo_release_candidate_gate.md reviews/072_model_gateway_local_demo_release_candidate_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Result: no matches.

## Verification Checklist For 质量运行席

Run or confirm accepted evidence for:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
cd backend && ./.venv/bin/python -m unittest tests.test_model_gateway_adapter tests.test_d5_qa_boundary tests.test_tenant_model_preference
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
git diff --check
```

Local/demo runtime checks:

- New API local gateway is running when model execution smoke is required.
- Workspace backend starts with approved model gateway env vars from `docs/deployment/new-api-local.md`.
- Workspace frontend points to the local backend through `NEXT_PUBLIC_API_BASE`.
- Preference read/save/reset uses only `/api/workspace/model-preference`.
- Task creation still sends `{ "content": "..." }`.
- UsageEvent model-call payload exposes only approved meter fields.

## Known-Gap Classification

Local/demo non-blockers:

- Local CORS origin must include the active frontend port when not using the default.
- New API local setup depends on operator-owned upstream provider configuration outside Curis source control.
- FastAPI Python deprecation warning remains deferred unless separately reopened.
- Docker/Colima/New API local state can affect local E2E availability.

Hosted-production blockers:

- Hosted production deployment is not approved.
- Production secret-manager retrieval remains blocked pending a separate security-approved issue.
- Billing, ROI, tenant packages, marketplace, Admin Platform implementation, provider-specific execution, and production rollout remain blocked.
- New API source changes, New API internal database dependency, provider SDK/direct provider calls, and Curis DB credential persistence remain blocked.

## Scope Check

- No new product feature was added.
- No backend/frontend behavior change was made.
- No Admin Platform implementation was added.
- No hosted production deployment was introduced.
- No billing, ROI, packages, marketplace, model optimization, provider SDK/direct provider calls, New API source/internal DB dependency, Task API payload change, execution-loop change, or runtime behavior change was introduced.

## Quality Verification

PASS.

Fresh documentation/evidence package verification was run by 质量运行席 against implementation commit `9bfc7d8b`.

Commands:

```bash
git show --name-only --oneline 9bfc7d8b
git diff --check 9bfc7d8b^ 9bfc7d8b
git diff --name-only 9bfc7d8b^ 9bfc7d8b
git diff --name-only 9bfc7d8b^ 9bfc7d8b -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}|(api[_-]?key|authorization|bearer)\s*[:=]\s*[A-Za-z0-9._-]{16,}' docs/release/model-gateway-local-demo-rc.md docs/release/ai-task-executor-mvp-v0.1-release-record.md docs/deployment/new-api-local.md issues/075_model_gateway_local_demo_release_candidate_gate.md reviews/072_model_gateway_local_demo_release_candidate_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
rg -n "backend behavior|frontend behavior|API semantics|persistence/schema|task payloads|execution-loop|runtime model routing|Evidence Map|Canonical Verification Commands|Local Startup Runbook|Local/Demo E2E Checklist|Known-Gap Classification|Release Decision Boundary|Hosted-production blockers|Local/demo non-blockers" docs/release/model-gateway-local-demo-rc.md
```

Evidence:

- Commit `9bfc7d8b` contains documentation/release/status files only: release docs, deployment doc addendum, issue/review, and source-of-truth updates.
- Commit diff hygiene passed.
- Behavior-file scope guard returned no backend app/tests, frontend app, Admin Platform, Workspace, shared, deploy, tools, or data behavior files.
- Package secret-placeholder scan returned no real secret-like values.
- Evidence map references were present and all referenced evidence files exist in the workspace.
- Runbook/checklist sections are present for canonical verification commands, local startup, local/demo E2E checks, UsageEvent field checks, and release decision boundary.
- Known-gap classification separates local/demo non-blockers from hosted-production blockers.
- Source-of-truth status files record documentation/evidence-only RC scope and blocked behavior/product changes.

Quality Result: PASS; no blockers found.

## Product Acceptance

Decision: ACCEPTED by 产品规划席 on 2026-07-08.

Rationale:

- The package matches the approved documentation/evidence-only RC scope.
- Quality verification passed for commit `9bfc7d8b` with no blockers.
- Evidence map, runbook/checklist, known-gap classification, source-of-truth status, secret scan, and behavior-file scope guard are verified.
- No backend/frontend behavior change, Task API payload change, execution-loop change, Admin Platform implementation, hosted production deployment, billing/ROI/package/marketplace scope, secret persistence/display, provider SDK/direct provider call, or New API source/internal DB dependency entered the package.

Product result: the model-gateway-enabled AI Task Executor MVP is accepted as a local/demo release-candidate package, not as a hosted production release.

## Handoff

Issue: `issues/075_model_gateway_local_demo_release_candidate_gate.md`
Objective: Close documentation/evidence-only model-gateway local/demo release-candidate package after product acceptance.
Special Constraints: Accepted package is local/demo only; hosted production release and future-layer scope remain blocked unless separately approved.
Next Seat: main thread closeout

Handoff: final closeout
