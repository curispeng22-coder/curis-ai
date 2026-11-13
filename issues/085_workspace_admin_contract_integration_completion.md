---
issue: "085"
title: "Workspace Admin Contract Integration Completion"
status: "done"
owner: "系统交付席"
date: "2026-07-09"
depends_on: "issues/062_adr0028_phase1_shared_contract.md"
---

# Workspace Admin Contract Integration Completion

## Objective

Complete the Workspace-side integration gaps for the Workspace <-> Admin shared contract after Admin Platform Phase-2 MVP.

## Minimal Context

- `AGENTS.md`
- `issues/062_adr0028_phase1_shared_contract.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Scope

Owner seat: 系统交付席.

Allowed:

- Ensure Workspace task execution writes Admin-compatible `usage_event` records for model calls, tool calls, and task execution.
- Preserve the execution chain:

```text
Task -> Workspace Orchestrator -> Model Gateway Adapter -> New API -> Result -> usage_event
```

- Add Workspace-side `tenant_private` namespace support for private model/tool/connector metadata with tenant isolation.
- Keep official capability reads through read-only `/api/catalog/*`.
- Keep Admin `/api/platform/*` writes admin-protected and outside Workspace runtime execution.
- Add backend regression tests covering task creation, run execution, usage event projection, tenant lookup, private capability isolation, and official catalog protection.

Allowed files:

- `backend/app/database.py`
- `backend/app/evolution_event_log.py`
- `backend/app/main.py`
- `backend/app/model_gateway.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`
- `backend/app/tool_executor.py`
- `backend/tests/test_adr0028_workspace_integration.py`
- `backend/tests/test_model_gateway_adapter.py`
- `issues/085_workspace_admin_contract_integration_completion.md`
- `reviews/082_workspace_admin_contract_integration_completion_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Non-Goals

- Admin Platform page implementation.
- Tenant packages, billing, ROI, marketplace governance, or platform policy expansion.
- New API source changes or dependency on New API internal database.
- Provider SDK or direct provider calls outside `ModelGatewayAdapter`.
- Credential persistence or secret display in Curis DB/API/UI.
- Workspace writes to official capability definitions.
- Workspace runtime calls to Admin `/api/platform/*` write endpoints.

## Acceptance Criteria

- Every accepted task execution persists three usage events:
  - `usage.model_call`
  - `usage.tool_call`
  - `usage.task_execution`
- Admin usage projection exposes at least:
  - `id`
  - `tenant_id`
  - `task_id`
  - `capability_type`
  - `capability_id`
  - `capability_source`
  - `model_gateway_id`
  - `model_name`
  - `prompt_tokens`
  - `completion_tokens`
  - `total_tokens`
  - `estimated_cost`
  - `status`
  - `created_at`
- `tenant_private` capability metadata is tenant-scoped and supports private `model`, `tool`, and `connector` entries.
- `tenant_private` entries are visible only to the owning tenant.
- `tenant_private` entries do not appear in official `/api/catalog/*` responses.
- Workspace cannot modify official capability definitions.
- Workspace execution code does not call `/api/platform/*`.
- Backend regression passes.

## Verification

Required:

- `cd backend && ./.venv/bin/python -m unittest tests/test_adr0028_workspace_integration.py`
- `cd backend && ./.venv/bin/python -m unittest tests/test_model_gateway_adapter.py tests/test_tenant_model_preference.py tests/test_d5_capability_catalog.py tests/test_d5_newapi_gateway.py tests/test_adr0028_workspace_integration.py`
- `cd backend && ./.venv/bin/python -m unittest tests/test_execution_engine.py`
- `cd backend && ./.venv/bin/python -m unittest discover tests`
- `git diff --check -- backend/app/model_gateway.py backend/app/tool_executor.py backend/app/orchestrator.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/database.py backend/app/main.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_model_gateway_adapter.py`
- Runtime/scope scans for `/api/platform/*`, usage event types, `tenant_private`, and secret-like values.

## Completion Notes

Completed on 2026-07-09.

- Workspace task persistence now records Admin-compatible `usage_event` records for model call, tool call, and task execution.
- Model gateway token metrics now preserve `prompt_tokens`, `completion_tokens`, and `total_tokens` through `ModelGatewayAdapter`, `ToolExecutor`, `Orchestrator`, and `ResultStore`.
- Admin usage projection now flattens Admin-required fields while preserving the original payload.
- Workspace now has tenant-scoped private capability metadata endpoints under `/api/workspace/capabilities/private`.
- Tenant-private capability metadata is isolated by tenant and does not pollute official catalog responses.
- Workspace official catalog reads remain `/api/catalog/*`; `/api/platform/*` remains Admin-protected.
- Evidence is recorded in `reviews/082_workspace_admin_contract_integration_completion_review.md`.

Next Seat: main thread closeout.

Handoff: final closeout
