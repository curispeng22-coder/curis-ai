---
issue: "074"
title: "Workspace Model Preference Local E2E Evidence"
status: "done"
owner: "质量运行席"
date: "2026-07-08"
depends_on: "issues/073_workspace_model_preference_ui_gate.md"
---

# Workspace Model Preference Local E2E Evidence

## Objective

Verify the accepted Workspace model preference selector against a real local backend/frontend runtime.

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/073_workspace_model_preference_ui_gate.md`
- `reviews/070_workspace_model_preference_ui_review.md`
- `docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md`

## Scope

- Start or reuse the local Workspace backend.
- Start or reuse the local Workspace frontend.
- Verify the operation console can read model preference state.
- Verify save/reset uses only existing Workspace preference APIs.
- Verify Task API payload remains `{ content }`.
- Capture evidence in a review.

## Non-Goals

- No new product feature.
- No backend semantic change.
- No frontend design expansion.
- No Admin UI.
- No billing, ROI, tenant package, marketplace, model optimization, or provider integration.
- No secret display, secret input, credential persistence, or New API source/internal database dependency.
- No execution-loop, tool-routing, workflow, or Task API behavior change.

## Allowed Files

- `reviews/071_workspace_model_preference_local_e2e_review.md`
- `issues/074_workspace_model_preference_local_e2e_evidence.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

If verification exposes a blocking defect, stop and open a separate implementation issue instead of fixing inside this evidence issue.

## Acceptance Criteria

- Local backend health or equivalent API smoke passes.
- Local frontend renders the operation console.
- Model preference UI reads available official model options from `GET /api/workspace/model-preference`.
- Save uses `PUT /api/workspace/model-preference` with `{ "model_key": "..." }`.
- Reset uses `DELETE /api/workspace/model-preference`.
- Task creation still sends `{ "content": "..." }`.
- No secret-like metadata is visible in the model preference UI.
- Evidence is recorded in `reviews/071_workspace_model_preference_local_e2e_review.md`.

## Verification

- Backend API smoke.
- Frontend runtime smoke.
- Browser or HTTP evidence for preference read/save/reset.
- Task payload boundary evidence.
- Scope guard for no implementation file changes beyond allowed evidence/status files.

## Completion Notes

Local E2E verification passed with evidence in `reviews/071_workspace_model_preference_local_e2e_review.md`.

Handoff: final closeout
