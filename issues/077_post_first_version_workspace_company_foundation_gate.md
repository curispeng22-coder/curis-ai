---
issue: "077"
title: "Post First-Version Workspace Company Foundation Gate"
status: "implemented"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/076_model_gateway_post_rc_next_phase_gate.md"
---

# Post First-Version Workspace Company Foundation Gate

## Objective

Decide the next bounded Workspace development phase after the model-gateway-enabled AI Task Executor MVP local/demo first version was closed out.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `docs/release/model-gateway-local-demo-first-version-release-record.md`
- `reviews/073_model_gateway_local_demo_release_closeout_review.md`

## Product Context

Curis Workspace has a local/demo first version of the AI Task Executor MVP with:

- task creation, run, status, history, selected detail, and operation-console UI;
- New API as the first local model gateway;
- model execution constrained to `ModelGatewayAdapter`;
- UsageEvent model-call fields and runtime secret guardrails;
- official model/tool catalog reads;
- tenant default model preference backend and operation-console selector;
- local/demo release evidence and operator handoff.

The final product remains a commercial multi-tenant AI Company System. The next Workspace phase should begin moving from "task executor" toward "company operating shell" without jumping into hosted production, billing/ROI, marketplace, complex company organization, Employee CRUD, business modules, or uncontrolled evolution.

## Product Recommendation

Recommended next phase: approve Option A, a Workspace Company Foundation boundary gate.

Rationale:

- The AI Task Executor first version is closed out, so the next product gap is no longer "can the system execute a task"; it is "can a CEO see and configure the first minimal company workspace frame around execution".
- Existing accepted foundations already include tenant id reservation, department catalog/department instance groundwork, official capability catalog reads, model gateway execution, and tenant model preference.
- The next safe step is boundary definition only: define the minimal company/workspace shell and department-entry scope before any implementation.
- This keeps the roadmap aligned to the AI Company System while preserving all current future-layer locks.

## Options

### Option A: Workspace Company Foundation Boundary

Approve architecture/product boundary definition for the first minimal Workspace company foundation.

Allowed:

- Define a minimal company/workspace shell boundary for the CEO-facing Workspace.
- Define how existing tenant id, company identity, department catalog/instances, model preference, task console, and Project Memory appear as one bounded Workspace frame.
- Define the first implementation slice and verification plan.
- Keep the first slice compatible with Admin Platform catalog/usage contracts.
- Preserve local/demo operation unless a separate production gate is approved.

Forbidden:

- Implementation in this gate.
- Hosted production deployment.
- Admin Platform implementation.
- Billing, ROI, packages, marketplace, or L6 economy.
- Employee CRUD or employee expansion.
- Complex company organization, departments/reporting-line expansion, staffing, permissions, or org charts.
- Business modules or external business-platform connectors.
- Secret persistence/display.
- Provider SDK/direct provider calls.
- New API source/internal DB dependency.
- Task API payload changes unless separately approved.
- Execution-loop or automatic evolution behavior changes.

### Option B: Local/Demo Reliability Hardening

Open a narrow local/demo reliability gate before product expansion.

Allowed examples:

- improve local runbook clarity;
- standardize local smoke commands;
- classify remaining local environment warnings.

Risk:

- This may slow progress toward the AI Company System unless a real blocker is found.

### Option C: Admin/Workspace Contract Follow-up

Open a shared-contract follow-up only if the Admin Platform team needs a Workspace-side contract change before the Workspace company foundation can proceed.

Allowed examples:

- read-only catalog contract clarification;
- UsageEvent field compatibility clarification;
- CEO/tenant identity placeholder clarification.

Risk:

- This should not become Admin Platform implementation inside Workspace.

## Acceptance Criteria

- 总控决策席 selects Option A, B, or C.
- Decision states whether Workspace can proceed to company-foundation boundary definition.
- Decision preserves local/demo, model-gateway, secret, Admin/Workspace separation, and future-layer locks.
- If Option A is selected, route to 系统交付席 for architecture boundary definition only.
- If Option B or C is selected, define the exact next issue and forbidden scope.

## Verification

Gate-only review. No implementation verification is required.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Selected option: Option A - Workspace Company Foundation Boundary.

Reason:

- The model-gateway-enabled local/demo first version is already closed out.
- The next bounded Workspace gap is defining the minimal CEO-facing company/workspace frame around existing execution capabilities.
- Option A is boundary-only and preserves the current local/demo, model-gateway, Admin/Workspace separation, secret, and future-layer locks.

Approved scope:

- Architecture/product boundary definition only for the first minimal Workspace company foundation.
- Define how existing tenant id, company identity, department catalog/instances, model preference, task console, and Project Memory appear as one bounded Workspace frame.
- Define the first implementation slice and verification plan.

Forbidden scope remains:

- Implementation or behavior change in this gate.
- Hosted production deployment.
- Admin Platform implementation.
- Billing, ROI, packages, marketplace, or L6 economy.
- Employee CRUD or employee expansion.
- Complex company organization, departments/reporting-line expansion, staffing, permissions, or org charts.
- Business modules or external business-platform connectors.
- Secret persistence/display.
- Provider SDK/direct provider calls.
- New API source/internal DB dependency.
- Task API payload changes unless separately approved.
- Execution-loop or automatic evolution behavior changes.

## Completion Notes

Approved Option A. Route to 系统交付席 for Workspace Company Foundation architecture/product boundary definition only.

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload:

- Issue: `issues/077_post_first_version_workspace_company_foundation_gate.md`
- Objective: Define Workspace Company Foundation architecture/product boundaries before implementation.
- Special Constraints: Option A approved. Boundary definition only; no implementation or behavior change. Preserve local/demo, model-gateway security boundary, Admin/Workspace separation, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no complex organization, no business modules, no secret persistence/display, and no execution-loop/runtime behavior change.
- Next Seat: 系统交付席.

## Implementation Notes

Implemented by 系统交付席 on 2026-07-08.

- Defined Workspace Company Foundation architecture/product boundaries in `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`.
- Recorded delivery evidence in `reviews/074_workspace_company_foundation_boundaries_review.md`.
- Updated source-of-truth status files for quality verification handoff.
- No backend/frontend behavior files were changed for this issue.

Handoff: sent to 质量运行席

## Product Acceptance Notes

Accepted by 产品规划席 on 2026-07-08 after 质量运行席 verification passed with no blockers.

- ADR-0031 is accepted as the Workspace Company Foundation architecture/product boundary.
- Boundary acceptance does not approve implementation or behavior change.
- First implementation must be opened as a separate gate.
- Hosted production, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, direct provider calls, Task API changes, execution-loop/runtime changes, and automatic evolution behavior remain blocked.

Handoff: final closeout
