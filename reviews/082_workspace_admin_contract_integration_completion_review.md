# Review 082: Workspace Admin Contract Integration Completion

Date: 2026-07-09
Owner: 系统交付席 / 质量运行席 / 产品规划席
Issue: `issues/085_workspace_admin_contract_integration_completion.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now execute tasks through the model gateway and emit Admin-compatible usage events for model calls, tool calls, and task executions, while keeping tenant-private capabilities isolated from the official catalog.

## Scope

- Backend-only contract completion for Workspace <-> Admin联调.
- Preserves official capability reads through `/api/catalog/*`.
- Adds tenant-private capability metadata under `/api/workspace/capabilities/private`.
- Preserves Admin-protected `/api/platform/*` write boundary.
- Preserves `ModelGatewayAdapter` as the only model execution path.
- Does not add Admin UI, Workspace complex UI, billing, ROI, packages, marketplace governance, provider SDKs, direct provider calls, New API source changes, New API internal DB dependency, or Curis credential persistence.

## Changed Files

- `backend/app/database.py`
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

Existing verified contract surfaces:

- `backend/app/main.py` exposes the current Admin/catalog/workspace routes used by this verification.
- `backend/app/evolution_event_log.py` exposes the Admin usage projection used by this verification.

## Implementation Evidence

UsageEvent write points:

- `usage.model_call` is written for the model gateway call.
- `usage.tool_call` is written for the selected tool execution.
- `usage.task_execution` is written for the task execution result.

Admin-compatible usage fields:

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

Tenant-private namespace:

- Workspace private capability metadata is stored in `tenant_private_capabilities`.
- Private capabilities require `tenant_id`.
- Supported private capability types: `model`, `tool`, `connector`.
- Private capabilities default to `source=tenant_private`.
- Private capabilities are visible only to the owning tenant.
- Private capabilities do not appear in official `/api/catalog/*` responses.

Official capability boundary:

- Workspace runtime/execution files do not call `/api/platform/*`.
- Official capability reads stay on `/api/catalog/*`.
- Admin `/api/platform/*` routes remain protected by admin token checks.

Model Gateway chain:

```text
Task
-> Workspace Orchestrator
-> Model Gateway Adapter
-> New API-compatible gateway
-> Result
-> usage_event
```

## Test Results

TDD red run before implementation:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_adr0028_workspace_integration.py
```

Expected failures confirmed:

```text
AssertionError: 1 != 3
AssertionError: 404 != 201
```

Focused integration run after implementation:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_adr0028_workspace_integration.py
```

Result:

```text
Ran 7 tests
OK
```

Gateway/catalog/preference focused regression:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_model_gateway_adapter.py tests/test_tenant_model_preference.py tests/test_d5_capability_catalog.py tests/test_d5_newapi_gateway.py tests/test_adr0028_workspace_integration.py
```

Result:

```text
Ran 50 tests
OK
```

Execution-engine regression:

```text
cd backend && ./.venv/bin/python -m unittest tests/test_execution_engine.py
```

Result:

```text
Ran 38 tests
OK
```

Full backend regression:

```text
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 279 tests
OK
```

Whitespace check:

```text
git diff --check -- backend/app/model_gateway.py backend/app/tool_executor.py backend/app/orchestrator.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/database.py backend/app/main.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_model_gateway_adapter.py
```

Result: passed.

## Required联调 Evidence

创建任务测试结果:

- Covered by `tests/test_adr0028_workspace_integration.py`.
- `POST /api/task` returns `200`.
- Created task is tenant-scoped through `X-Tenant-Id`.

执行任务测试结果:

- Covered by `tests/test_adr0028_workspace_integration.py`.
- `POST /api/task/{task_id}/run` returns `200`.
- Task execution uses the injected gateway-compatible execution path and persists execution output.

usage_event 写入结果:

- Same test verifies three usage events for one execution:
  - `usage.model_call`
  - `usage.tool_call`
  - `usage.task_execution`
- Each event includes Admin-compatible flat fields plus original payload.

Admin 侧 tenant_id 查询结果:

- Same test queries:

```text
GET /api/platform/usage?tenant_id=tenant-acme
```

- Result includes only `tenant-acme` usage events and exposes the required Admin-compatible fields.

tenant_private 能力隔离测试结果:

- Same test creates tenant A private capability through:

```text
POST /api/workspace/capabilities/private
```

- Tenant A can read the private capability.
- Tenant B cannot read Tenant A private capability.
- `GET /api/catalog/capabilities` does not include the tenant-private capability.

Official catalog protection result:

- Tenant request to `POST /api/platform/capabilities` without admin token returns `401`.
- Official catalog remains readable through `/api/catalog/capabilities`.

## Scope Checks

Runtime platform endpoint scan:

```text
rg -n "/api/platform/" frontend/app backend/app/result_store.py backend/app/orchestrator.py backend/app/tool_executor.py backend/app/model_gateway.py backend/tests/test_adr0028_workspace_integration.py
```

Result:

- Runtime execution files do not call `/api/platform/*`.
- Expected matches are Admin UI/Admin routes and tests that verify the protected Admin projection.

Usage and namespace scan:

```text
rg -n "usage.model_call|usage.tool_call|usage.task_execution|tenant_private_capabilities|/api/workspace/capabilities/private" backend/app backend/tests/test_adr0028_workspace_integration.py backend/tests/test_model_gateway_adapter.py
```

Result:

- Required usage events and tenant-private namespace implementation are present.

Secret scan:

```text
rg -n "api_key|password|secret|Authorization|Bearer|sk-[A-Za-z0-9_-]{10,}" backend/app/model_gateway.py backend/app/result_store.py backend/app/evolution_event_log.py backend/app/main.py backend/app/database.py backend/tests/test_adr0028_workspace_integration.py backend/tests/test_model_gateway_adapter.py
```

Result:

- Matches are expected guarded matches in gateway redaction/env handling, admin auth handling, schema comments, and negative tests.
- No new Curis DB credential persistence was introduced.

## Known Gaps

- This pass verifies Admin-readable projection through the local Curis Admin-compatible `/api/platform/usage` route; it does not perform hosted Admin Platform deployment verification.
- Tenant-private capability storage is metadata-only. Runtime use of private model/tool/connector capabilities remains future-gated.
- Billing, packages, marketplace governance, and production tenant identity remain future-gated.

## Quality Result

Quality Result: PASS.

Commands: focused integration tests, gateway/catalog/preference regression, execution-engine regression, full backend regression, whitespace check, endpoint scope scan, usage/namespace scan, and secret scan.

Evidence: task creation, task execution, usage event writes, Admin tenant usage query, tenant-private isolation, official catalog protection, and ModelGatewayAdapter-only runtime boundary are covered.

Risks: Worktree contains unrelated pre-existing dirty files from previous accepted work; they were not used as evidence for this issue.

Blocked / Pass: Pass; no blockers found.

Next Seat: main thread closeout.

Handoff: final closeout
