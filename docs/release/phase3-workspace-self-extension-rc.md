# Phase-3 Workspace Self-Extension Release Candidate Report

Date: 2026-07-09

Status: RC verification passed with one fix applied in Workspace frontend request headers.

Latest implementation commit before RC: `ac9dadb6 feat(workspace): add private capability management UI`

Release scope: local/demo Workspace Self-Extension MVP only.

## Scope

This RC verifies:

- Workspace private model, private tool, and private connector UI.
- Workspace official + tenant_private capability selector.
- Task creation with selected tenant_private capability.
- Task execution through Model Gateway Adapter.
- Admin-readable `usage_event` attribution for tenant_private model/tool/task execution.
- Admin/Workspace boundary: official catalog remains Admin-owned; tenant_private remains tenant-scoped.

This RC does not add new product features.

## Acceptance Flow

Browser-click verification completed:

1. Opened Workspace operation console at `http://127.0.0.1:3000`.
2. Added a tenant_private private model through the UI:
   - `rc-private-model-719968`
   - `credential_ref=env:TENANT_MODEL_KEY`
3. Added a tenant_private private tool through the UI:
   - `rc-private-tool-719968`
   - `config_ref=env:TENANT_TOOL_CONFIG`
4. Added a tenant_private private connector through the UI:
   - `rc-private-connector-719968`
   - `config_ref=env:TENANT_CONNECTOR_CONFIG`
5. Confirmed the Workspace capability selector displayed both:
   - `official`
   - `tenant_private`
6. Created a task from the UI with a selected tenant_private capability.

Issue found during browser-click execution:

- Running the task from the UI failed with `X-Ceo-Id is required to write UsageEvent`.
- Root cause: Workspace frontend task execution requests did not send the required CEO context header.

Fix applied:

- Added local/demo Workspace request context headers for mutating requests:
  - `X-Tenant-Id`
  - `X-Ceo-Id`
- Kept GET catalog/read requests as simple requests to avoid local CORS preflight instability during parallel reads.
- Added frontend test coverage confirming the page wires these headers and still does not call `/api/platform/*`.

Post-fix E2E completion:

- The in-app browser automation surface became unstable after reload/new-tab operations and repeatedly timed out.
- The full execution/admin evidence was completed with the same running backend/frontend environment through HTTP E2E.
- The HTTP E2E used a local OpenAI-compatible fake gateway at `http://127.0.0.1:18080` and the same temporary SQLite DB.

## Admin ↔ Workspace E2E Evidence

HTTP E2E command result summary:

```json
{
  "task_id": "9893f279-deb5-4cd3-ab95-ae1514833706",
  "selector_sources": ["official", "tenant_private"],
  "selector_has_private_tool": true,
  "official_catalog_has_private_tool": false,
  "tenant_b_sees_private_tool": false,
  "task_status": "COMPLETED",
  "task_output_contains_gateway_response": true,
  "admin_usage_status": 200,
  "usage_private_event_count": 3,
  "admin_edit_private_as_official_status": 422
}
```

Verified:

- Admin can read official capability catalog.
- Workspace can read official capabilities through `/api/catalog/*`.
- Workspace can create tenant_private model/tool/connector.
- tenant_private entries do not appear in `/api/catalog/capabilities`.
- tenant B cannot read tenant A/default private tool.
- Task execution with tenant_private tool completed.
- Admin can query tenant usage through `/api/platform/usage?tenant_id=default`.
- Admin usage response included tenant_private usage events for:
  - `usage.model_call`
  - `usage.tool_call`
  - `usage.task_execution`
- Admin official capability update route does not modify tenant_private capability as official.

UsageEvent fields verified in Admin response:

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

## Security Boundary Verification

Passed:

- Workspace frontend runtime scan found no `/api/platform/*` calls.
- Workspace execution/runtime scan found no `/api/platform/*` calls in execution path files.
- `credential_ref` and `config_ref` remain `scheme:reference` placeholders.
- UI payload builders reject secret-like `credential_ref` values.
- tenant_private does not leak into official catalog.
- tenant_private is tenant-scoped.
- Admin usage projection exposes metering fields; sensitive config is not required or exposed in top-level usage fields.

Secret scan notes:

- Scan matches in `backend/app/model_gateway.py` are expected redaction/auth-boundary code.
- Scan matches in `backend/app/main.py` are expected Admin bearer-token parsing and secret-rejection helpers.
- Scan matches in `frontend/app/taskViewModel.test.mjs` include a negative test value `sk-real-secret-value-123456` used to verify rejection.

No real credential storage was added.

## Commands And Results

Frontend unit tests:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
```

Result: 28 tests passed.

Frontend lint:

```bash
cd frontend && npm run lint
```

Result: passed.

Frontend build:

```bash
cd frontend && npm run build
```

Result: passed.

Backend full regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: 298 tests passed.

Note: FastAPI emitted an upstream Python 3.14 deprecation warning for `asyncio.iscoroutinefunction`; tests still passed.

Diff hygiene:

```bash
git diff --check
```

Result: passed.

Workspace frontend `/api/platform/*` runtime scan:

```bash
rg -n "/api/platform/" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: no matches.

Workspace execution/runtime `/api/platform/*` scan:

```bash
rg -n "/api/platform/" backend/app/result_store.py backend/app/orchestrator.py backend/app/tool_executor.py backend/app/model_gateway.py frontend/app/page.js
```

Result: no matches.

Secret scan:

```bash
rg -n "api_key|password|secret|Authorization|Bearer|sk-[A-Za-z0-9_-]{10,}|credential_ref\s*[:=]\s*['\"]sk-|config_ref\s*[:=]\s*['\"]sk-" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs backend/app/main.py backend/app/database.py backend/app/result_store.py backend/app/model_gateway.py
```

Result: no unexpected real secret storage.

## Problems Found

1. Browser-click task execution failed before usage_event write.

Cause:

- `X-Ceo-Id` was missing from Workspace frontend task execution requests.
- Backend correctly failed closed because UsageEvent requires CEO context.

Fix:

- Added `apiHeaders()` in Workspace frontend with local/demo defaults:
  - `NEXT_PUBLIC_CURIS_TENANT_ID || "default"`
  - `NEXT_PUBLIC_CURIS_CEO_ID || "local-demo-ceo"`
- Applied the headers to mutating requests, including task creation and task execution.

2. Browser automation plugin instability.

Cause:

- In-app browser automation repeatedly timed out on reload/new-tab after the first click-flow segment.

Disposition:

- Not a Curis product code defect.
- Browser-click evidence exists for private capability creation and selector visibility.
- Full execution/admin closure was verified through HTTP E2E in the same local environment.

## Current Release Decision

Current state: can be used as a local/demo release candidate.

Reason:

- Core Workspace Self-Extension flows work.
- tenant_private usage_event attribution works.
- Admin can read tenant usage.
- official catalog is not polluted.
- private capability isolation passed.
- required frontend/backend build and regression checks passed.

Release note:

- Before a public demo, repeat the final click-through task execution once with a stable browser automation surface or manually in the visible browser to capture screenshot evidence after the header fix.

## Still Not Included

This RC still does not implement:

- ROI system.
- Employee system.
- Department system expansion.
- Business modules.
- Capability marketplace.
- Real credential hosting.
- Tenant package or billing logic.
- Admin Platform governance changes.
- Provider SDK or direct provider calls.
- New API source changes.
- Curis dependency on New API internal database.

## Handoff

Next seat: 产品规划席 for RC acceptance decision.

If accepted, the next step is local/demo release closeout documentation or a separate gate for production-readiness planning.
