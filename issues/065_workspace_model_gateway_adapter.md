---
issue: "065"
title: "Workspace Model Gateway Adapter"
status: "implemented-and-verified"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/064_adr0028_phase2_newapi_gateway_prd.md"
---

# Workspace Model Gateway Adapter

## Objective

Implement the Workspace-side Model Gateway Adapter and route AI Task Executor model calls through the configured New API OpenAI-compatible gateway.

## Minimal Context

- `AGENTS.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- `issues/064_adr0028_phase2_newapi_gateway_prd.md`

## Scope

- Add `ModelGatewayAdapter` for OpenAI-compatible `/v1/chat/completions`.
- Route default AI Task Executor model execution through the adapter.
- Keep default runtime tool selection provider-neutral with `model_gateway_tool`.
- Preserve existing Task API payloads and frontend behavior.
- Extend UsageEvent payload with required gateway metrics.

## Non-Goals

- No Admin Platform page.
- No tenant package, billing, ROI, or platform governance.
- No model gateway credential persistence.
- No direct OpenAI, Claude, or Codex provider implementation.
- No marketplace, tenant-private credential, or connector credential implementation.

## Allowed Files

- `backend/app/model_gateway.py`
- `backend/app/codex_executor.py`
- `backend/app/main.py`
- `backend/app/tool_executor.py`
- `backend/app/tool_router.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`
- `backend/tests/`
- status/context/review files.

## Acceptance Criteria

- Model calls in the default AI Task Executor path go through `ModelGatewayAdapter`.
- Adapter supports New API's OpenAI-compatible chat-completions interface.
- Default runtime selected tool is `model_gateway_tool`, not a provider-specific tool.
- UsageEvent payload includes `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, and `status`.
- Missing gateway config fails closed before external calls.
- Existing ADR-0028 UsageEvent behavior remains compatible.

## Verification

- Write failing tests before implementation.
- Run targeted model gateway adapter tests.
- Run execution engine regression.
- Run ADR-0028 Workspace integration tests.
- Run full backend regression.

## Completion Notes

- Implemented `backend/app/model_gateway.py`.
- Replaced default runtime model executor with `ModelGatewayAdapter`.
- Converted `CodexExecutor` into a compatibility wrapper over the adapter.
- Added provider-neutral `model_gateway_tool` for default runtime execution.
- Extended UsageEvent payload with gateway metrics.
- Verification recorded in `reviews/062_workspace_model_gateway_adapter_review.md`.
