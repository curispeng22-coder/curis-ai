---
issue: "075"
title: "Model Gateway Local Demo Release Candidate Gate"
status: "implemented"
owner: "总控决策席"
date: "2026-07-08"
depends_on: "issues/074_workspace_model_preference_local_e2e_evidence.md"
---

# Model Gateway Local Demo Release Candidate Gate

## Objective

Approve or reject a local/demo release-candidate track for the AI Task Executor MVP after the New API model gateway, official capability catalog, usage event, tenant model preference, and model preference UI slices.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `issues/064_workspace_capability_integration_phase_1.md`
- `issues/065_workspace_model_gateway_adapter.md`
- `issues/066_workspace_official_model_catalog.md`
- `issues/067_workspace_official_tool_catalog.md`
- `issues/068_new_api_local_deployment.md`
- `issues/069_model_gateway_production_security_boundary.md`
- `issues/070_model_gateway_runtime_secret_guardrails.md`
- `issues/071_workspace_tenant_model_preference_gate.md`
- `issues/072_workspace_tenant_model_preference_first_slice.md`
- `issues/073_workspace_model_preference_ui_gate.md`
- `issues/074_workspace_model_preference_local_e2e_evidence.md`

## Product Intent

The accepted local/demo v0.1 release record predates the model gateway and multi-tenant model preference work. Curis Workspace now has enough verified capability to prepare a next local/demo release-candidate evidence package focused on:

- New API as the first model gateway.
- Official model/tool metadata consumption.
- UsageEvent model-call accounting fields.
- Runtime secret guardrails.
- Tenant default model preference backend and UI.
- Local end-to-end evidence for model preference read/save/reset and task creation.

This remains inside AI Task Executor MVP. It is not a hosted production SaaS release and does not introduce Admin Platform implementation scope.

## Scope For Gate Decision

- Decide whether to start a local/demo release-candidate track for the model-gateway-enabled AI Task Executor MVP.
- Allow release-candidate documentation, verification checklist, startup/runbook updates, evidence mapping, and known-gap classification.
- Allow quality verification against existing backend/frontend behavior and New API local deployment.
- Allow updating source-of-truth status and release docs if the candidate is accepted.

## Non-Goals

- No new product feature.
- No backend semantic change.
- No frontend feature/design expansion.
- No Admin Platform UI or implementation.
- No hosted production deployment.
- No billing, ROI, tenant package, marketplace, model optimization, or platform governance.
- No new secret storage, credential display, credential persistence, provider SDK, direct provider call, New API source change, or New API internal database dependency.
- No execution-loop, tool-routing, workflow, Task API payload, persistence-schema, or runtime behavior change unless separately approved.

## Gate Questions

- Should the post-v0.1 model-gateway-enabled capability set enter a local/demo release-candidate track now?
- Should the next seat produce a release-candidate package rather than new implementation?
- Which verification commands and evidence are required for acceptance?
- Which known gaps remain non-blocking for local/demo but blocking for hosted production?

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Approved scope:

- The post-v0.1 model-gateway-enabled capability set may enter a local/demo release-candidate track now.
- The next seat must produce a documentation/evidence-only release-candidate package, not new implementation.
- Scope includes New API model gateway, official model/tool catalogs, UsageEvent model-call fields, runtime secret guardrails, tenant model preference backend/UI, and local E2E evidence.
- Release-candidate work may include documentation, verification checklist, startup/runbook updates, evidence mapping, known-gap classification, local/demo verification commands, and source-of-truth status updates.

Required verification/evidence:

- Backend regression and focused model-gateway/tenant-preference tests from the accepted local environment.
- Frontend view-model tests, lint, and build for the operation console.
- API/local E2E evidence for preference read/save/reset, task creation, and content-only Task API payload boundary.
- Evidence that UsageEvent model-call fields remain non-secret and allowlisted.
- Evidence that official model/tool catalogs expose only approved non-secret metadata.
- Evidence that ADR-0029 runtime secret guardrails and `ModelGatewayAdapter`-only execution remain intact.
- Evidence map for known local/demo gaps versus hosted-production blockers.

Known local/demo non-blockers to classify:

- Local CORS origin must include the active frontend port when not using the default.
- Hosted production deployment remains out of scope.
- Production secret-manager retrieval remains out of scope.
- Billing, ROI, tenant packages, marketplace, Admin Platform implementation, provider-specific execution, and production rollout remain blocked.

## Acceptance Criteria

- Gate decision states approved or blocked.
- If approved, next work is documentation/evidence only unless 总控决策席 separately approves implementation.
- Release-candidate scope clearly includes model gateway, usage events, official catalog reads, tenant model preference, model preference UI, and local E2E evidence.
- Release-candidate scope clearly blocks production billing, ROI, packages, marketplace, Admin Platform implementation, secret persistence, and provider-specific execution drift.
- Next seat and handoff payload are recorded.

## Verification

Gate-only review. No implementation verification is required at this step.

## Completion Notes

Approved. Route to 系统交付席 for documentation/evidence-only release-candidate package.

Handoff: HANDOFF_REQUIRED

Target seat: 系统交付席

Compact payload:

- Issue: `issues/075_model_gateway_local_demo_release_candidate_gate.md`
- Objective: Prepare a documentation/evidence-only local/demo release-candidate package for the model-gateway-enabled AI Task Executor MVP.
- Special Constraints: Gate-only approval; no implementation. Cover New API model gateway, official model/tool catalogs, UsageEvent model-call fields, runtime secret guardrails, tenant model preference backend/UI, and local E2E evidence.
- Allow: release-candidate documentation, verification checklist, startup/runbook updates, evidence mapping, known-gap classification, local/demo verification commands, and source-of-truth status updates.
- Forbid: new product features, backend/frontend behavior change, Admin Platform implementation, hosted production deployment, billing/ROI/packages/marketplace, secret persistence/display, provider SDK/direct provider calls, New API source/internal DB dependency, Task API payload changes, execution-loop changes, and runtime behavior changes.
- Next Seat: 系统交付席.

## Implementation Notes

Implemented by 系统交付席 on 2026-07-08.

- Prepared documentation/evidence-only release-candidate package in `docs/release/model-gateway-local-demo-rc.md`.
- Added model-gateway RC addendum to `docs/release/ai-task-executor-mvp-v0.1-release-record.md`.
- Added release-candidate reference to `docs/deployment/new-api-local.md`.
- Evidence and handoff are recorded in `reviews/072_model_gateway_local_demo_release_candidate_review.md`.
- No backend/frontend behavior files were changed for this issue.

Handoff: sent to 质量运行席
