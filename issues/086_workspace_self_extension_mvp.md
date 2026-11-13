---
issue: "086"
title: "Workspace Self-Extension MVP"
status: "done"
owner: "系统交付席"
date: "2026-07-09"
depends_on: "issues/085_workspace_admin_contract_integration_completion.md"
---

# Workspace Self-Extension MVP

## Objective

Implement Phase-3 Workspace Self-Extension MVP so each tenant can configure and select tenant-private model/tool/connector metadata inside Workspace without polluting Admin official catalogs.

## Minimal Context

- `AGENTS.md`
- `issues/085_workspace_admin_contract_integration_completion.md`
- `reviews/082_workspace_admin_contract_integration_completion_review.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Scope

Owner seat: 系统交付席.

Allowed:

- CEO can add tenant-private model configuration in Workspace.
- CEO can add tenant-private tool configuration in Workspace.
- CEO can add tenant-private connector configuration in Workspace.
- Workspace can read a unified capability selector containing official and tenant-private entries.
- Task creation may optionally reference a selected capability using `capability_source`, `capability_type`, and `capability_id`.
- Private capability execution records `capability_source=tenant_private` in usage events.
- Existing official catalog reads remain `/api/catalog/*`.
- Tenant-private configuration stays tenant-scoped and metadata-only.

Allowed files:

- `backend/app/main.py`
- `backend/app/database.py`
- `backend/app/result_store.py`
- `backend/app/orchestrator.py`
- `backend/tests/test_adr0028_workspace_integration.py`
- `backend/tests/test_d5_workspace_integration.py`
- `issues/086_workspace_self_extension_mvp.md`
- `reviews/083_workspace_self_extension_mvp_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Non-Goals

- Capability marketplace.
- ROI system.
- Complex employee system.
- Multi-business modules.
- Admin Platform page implementation.
- Workspace writes to `/api/platform/*`.
- Official catalog mutation from Workspace.
- Real credential hosting or secret resolution.
- Provider SDKs or direct provider calls outside the existing gateway boundary.
- New API source changes or New API internal DB dependency.

## Acceptance Criteria

- CEO can add a tenant-private model with:
  - `tenant_id`
  - `name`
  - `provider_type`
  - `base_url`
  - `model_name`
  - `credential_ref`
  - `enabled`
  - `source=tenant_private`
- CEO can add a tenant-private tool with:
  - `tenant_id`
  - `name`
  - `type`
  - `description`
  - `config_ref`
  - `enabled`
  - `source=tenant_private`
- CEO can add a tenant-private connector with:
  - `tenant_id`
  - `name`
  - `connector_type`
  - `config_ref`
  - `enabled`
  - `source=tenant_private`
- Workspace can read official and tenant-private capabilities in one selector with source labels.
- Task execution can select a tenant-private capability.
- usage events for tenant-private execution include tenant/task/capability/source/status timestamps through the existing Admin-compatible projection.
- Tenant A cannot read Tenant B private capabilities.
- Tenant-private entries do not appear in `/api/catalog/*`.
- Admin official capability code does not reference or mutate tenant-private capability metadata.
- All backend tests pass.

## Verification

Required:

- `cd backend && ./.venv/bin/python -m unittest tests/test_adr0028_workspace_integration.py`
- `cd backend && ./.venv/bin/python -m unittest tests/test_model_gateway_adapter.py tests/test_tenant_model_preference.py tests/test_d5_workspace_integration.py tests/test_adr0028_workspace_integration.py`
- `cd backend && ./.venv/bin/python -m unittest tests/test_execution_engine.py`
- `cd backend && ./.venv/bin/python -m unittest discover tests`
- `git diff --check -- backend/app/main.py backend/app/database.py backend/app/result_store.py backend/app/orchestrator.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_d5_workspace_integration.py`
- Runtime scope scan for `/api/platform/*`.
- Secret scan for changed backend files and tests.

## Completion Notes

Completed on 2026-07-09.

- Added Workspace typed tenant-private model/tool/connector endpoints.
- Added Workspace unified capability selector.
- Added optional task capability selection fields while keeping `content` backward-compatible.
- Private capability selection forces existing execution through the model gateway tool and rewrites task-selected capability attribution to the tenant-private capability id/source.
- usage events preserve Admin-compatible projection and record `capability_source=tenant_private` for private execution.
- Tenant-private metadata remains isolated in `tenant_private_capabilities`.
- `credential_ref` and `config_ref` remain opaque `scheme:reference` placeholders.
- Evidence is recorded in `reviews/083_workspace_self_extension_mvp_review.md`.

Next Seat: main thread closeout.

Handoff: final closeout
