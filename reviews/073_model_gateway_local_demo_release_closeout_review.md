# Review 073: Model Gateway Local/Demo First-Version Release Closeout

Date: 2026-07-08

Issue: `issues/076_model_gateway_post_rc_next_phase_gate.md`

Owner: 系统交付席

Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now close out the model-gateway-enabled AI Task Executor MVP as a local/demo first-version package with release decision evidence, operator handoff, final checklist, and known-gap confirmation.

## Delivery Result

PASS for documentation/evidence closeout package preparation.

No implementation or behavior change was made for this issue.

## Closeout Artifacts

- `docs/release/model-gateway-local-demo-first-version-release-record.md`
- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `issues/076_model_gateway_post_rc_next_phase_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/073_model_gateway_local_demo_release_closeout_review.md`

## Closeout Coverage

The package covers:

- release decision record;
- operator handoff summary;
- final local/demo checklist;
- known-gap confirmation;
- source-of-truth status updates;
- next backlog decision boundary after closeout.

## Evidence Summary

Accepted release-candidate package:

- `docs/release/model-gateway-local-demo-rc.md`
- `reviews/072_model_gateway_local_demo_release_candidate_review.md`
- Commit `9bfc7d8b`

Included accepted capability evidence:

- New API local gateway: `docs/deployment/new-api-local.md`, `reviews/065_new_api_local_deployment_review.md`
- ModelGatewayAdapter path: `issues/065_workspace_model_gateway_adapter.md`, `reviews/062_workspace_model_gateway_adapter_review.md`
- Official model catalog: `issues/066_workspace_official_model_catalog.md`, `reviews/063_workspace_official_model_catalog_review.md`
- Official tool catalog: `issues/067_workspace_official_tool_catalog.md`, `reviews/064_workspace_official_tool_catalog_review.md`
- ADR-0029 security boundary: `docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`, `reviews/066_model_gateway_production_security_boundary_review.md`
- Runtime secret guardrails: `issues/070_model_gateway_runtime_secret_guardrails.md`, `reviews/067_model_gateway_runtime_secret_guardrails_review.md`
- Tenant model preference backend: `issues/072_workspace_tenant_model_preference_first_slice.md`, `reviews/069_workspace_tenant_model_preference_first_slice_review.md`
- Workspace model preference UI: `issues/073_workspace_model_preference_ui_gate.md`, `reviews/070_workspace_model_preference_ui_review.md`
- Local E2E evidence: `issues/074_workspace_model_preference_local_e2e_evidence.md`, `reviews/071_workspace_model_preference_local_e2e_review.md`

## Verification Performed

Documentation/package whitespace check:

```bash
git diff --check
```

Result: passed.

Documentation closeout package diff guard:

```bash
git diff --cached --name-only -- docs/release issues/076_model_gateway_post_rc_next_phase_gate.md reviews/073_model_gateway_local_demo_release_closeout_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Result: package changes are release docs, issue/review, and source-of-truth status/context files only.

Staged behavior-file scope guard:

```bash
git diff --cached --name-only -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
```

Result: no backend/frontend behavior files changed.

Closeout package secret-placeholder scan:

```bash
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}|(api[_-]?key|authorization|bearer)\s*[:=]\s*[A-Za-z0-9._-]{16,}' docs/release/model-gateway-local-demo-first-version-release-record.md docs/release/ai-task-executor-mvp-v0.1-release-record.md issues/076_model_gateway_post_rc_next_phase_gate.md reviews/073_model_gateway_local_demo_release_closeout_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Expected result: no matches.

Observed result: no matches.

## Verification Checklist For 质量运行席

Confirm:

- closeout package is documentation/evidence only;
- release decision record points to the accepted model-gateway RC package and evidence;
- operator handoff summary keeps local secrets outside Git and Curis DB;
- final checklist covers backend, frontend, local E2E, UsageEvent, catalog, gateway, and source-of-truth evidence;
- known gaps separate local/demo non-blockers from hosted-production blockers;
- next backlog decision is routed to 产品规划席 after closeout rather than decided by this package;
- behavior-file guard shows no backend/frontend behavior drift.

## Known Gaps

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

## Scope Check

- No new implementation was added.
- No backend/frontend behavior change was made.
- No hosted production deployment was introduced.
- No Admin Platform implementation was added.
- No billing, ROI, packages, marketplace, secret persistence/display, provider SDK/direct provider calls, New API source/internal DB dependency, Task API payload change, execution-loop change, persistence/schema change, or runtime behavior change was introduced.

## Quality Verification

Quality Result: PASS.

Commands: commit diff check, behavior-file scope guard, secret scan, release-record section scan, evidence-reference existence check, and source-of-truth status check.

Evidence: commit `0801231d` contains release docs, issue/review, and source-of-truth status/context files only; no backend/frontend behavior files entered the commit; closeout record covers release decision, operator handoff, final checklist, known gaps, and next backlog boundary.

Risks: hosted production, Admin Platform, billing/ROI/packages/marketplace, secret persistence/display, provider SDK/direct provider calls, New API source/internal DB dependency, Task API payload changes, persistence/schema changes, execution-loop changes, and runtime behavior changes remain blocked.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

Fresh documentation/evidence closeout verification was run by 质量运行席 against implementation commit `0801231d`.

Commands:

```bash
git show --name-only --oneline 0801231d
git diff --check 0801231d^ 0801231d
git diff --name-only 0801231d^ 0801231d
git diff --name-only 0801231d^ 0801231d -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
git diff --name-only 0801231d -- PROJECT_STATUS.md TASKS.md docs/release/ai-task-executor-mvp-v0.1-release-record.md docs/release/model-gateway-local-demo-first-version-release-record.md issues/076_model_gateway_post_rc_next_phase_gate.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md reviews/073_model_gateway_local_demo_release_closeout_review.md
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}|(api[_-]?key|authorization|bearer)\s*[:=]\s*[A-Za-z0-9._-]{16,}' docs/release/model-gateway-local-demo-first-version-release-record.md docs/release/ai-task-executor-mvp-v0.1-release-record.md issues/076_model_gateway_post_rc_next_phase_gate.md reviews/073_model_gateway_local_demo_release_closeout_review.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
rg -n "Release Closeout Decision Package|Accepted release-candidate package|Accepted release-candidate evidence|Operator Handoff Summary|Local secret handling|Final Local/Demo Checklist|Known Gap Confirmation|Hosted-production blockers|Next Backlog Decision|Closeout Boundary|Task API payload shape|Tool System v1.8" docs/release/model-gateway-local-demo-first-version-release-record.md
```

Evidence:

- Commit `0801231d` contains release docs, issue/review, and source-of-truth status/context files only.
- Commit diff hygiene passed.
- Behavior-file scope guard returned no backend app/tests, frontend app, Admin Platform, Workspace, shared, deploy, tools, or data behavior files.
- Current workspace package files match commit `0801231d` before quality-status updates.
- Closeout package secret-placeholder scan returned no real secret-like values.
- Release decision record points to the accepted model-gateway RC package and evidence.
- Operator handoff keeps New API tokens, provider keys, session secrets, and Authorization values outside Git and Curis database rows.
- Final checklist covers backend, frontend, local E2E, UsageEvent, catalog, gateway, documentation diff hygiene, behavior-file drift, and source-of-truth status alignment.
- Known-gap classification separates local/demo non-blockers from hosted-production blockers.
- Next backlog decision is routed to 产品规划席 after closeout rather than decided by the package.

Quality Result: PASS; no blockers found.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: close local/demo first-version release milestone.

Scope: documentation/evidence-only local/demo first-version release closeout for the model-gateway-enabled AI Task Executor MVP.

Acceptance Criteria:

- release decision record is present and points to accepted RC evidence;
- operator handoff is present and keeps local secrets outside Git and Curis DB;
- final local/demo checklist and known-gap classification are present;
- hosted production, Admin Platform, billing/ROI/packages/marketplace, secret persistence/display, provider SDK/direct provider calls, Task API changes, persistence/schema changes, execution-loop changes, and runtime behavior changes remain blocked;
- quality verification passed with no blockers.

Source Of Truth Updates: `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark T-186 accepted and the local/demo first-version release closeout completed.

Next Seat: main thread closeout.

Open Questions: none for this closeout.

## Handoff

Issue: `issues/076_model_gateway_post_rc_next_phase_gate.md`
Objective: Close out documentation/evidence-only local/demo first-version release package after product acceptance.
Special Constraints: Local/demo first version is accepted only for local/demo operation. Hosted production and future commercial scope remain blocked until separate gates.
Next Seat: main thread closeout

Handoff: final closeout
