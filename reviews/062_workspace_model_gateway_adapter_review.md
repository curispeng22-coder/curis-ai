# Review 062: Workspace Model Gateway Adapter

Date: 2026-07-08

Issue: `issues/065_workspace_model_gateway_adapter.md`

## Quality Result

PASS.

## Scope Verified

- `ModelGatewayAdapter` posts OpenAI-compatible chat-completions payloads to the configured New API gateway base URL.
- Default AI Task Executor runtime uses `model_gateway_tool` and routes through the adapter.
- `CodexExecutor` no longer performs direct OpenAI calls; it is a compatibility wrapper over `ModelGatewayAdapter`.
- UsageEvent payload now includes `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, and `status`.
- No Admin Platform page, tenant package, billing, ROI, governance, marketplace, private credential, or credential persistence was added.

## Commands

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_model_gateway_adapter
../backend/.venv/bin/python -m unittest tests.test_execution_engine
../backend/.venv/bin/python -m unittest tests.test_adr0028_workspace_integration
../backend/.venv/bin/python -m unittest discover tests
git diff --check -- backend/app/model_gateway.py backend/app/codex_executor.py backend/app/main.py backend/app/tool_executor.py backend/app/tool_router.py backend/app/orchestrator.py backend/app/result_store.py backend/tests/test_model_gateway_adapter.py backend/tests/test_execution_engine.py backend/tests/test_adr0028_workspace_integration.py issues/065_workspace_model_gateway_adapter.md reviews/062_workspace_model_gateway_adapter_review.md TASKS.md PROJECT_STATUS.md knowledge/CURRENT_CONTEXT.md knowledge/003_Architecture.md knowledge/PROJECT_MEMORY.md
```

## Evidence

- Targeted model gateway tests: 2 tests passed.
- Execution engine regression: 38 tests passed.
- ADR-0028 Workspace integration tests: 4 tests passed.
- Backend regression: 161 tests passed.

## Known Gaps

- Gateway config is environment-based: `CURIS_MODEL_GATEWAY_BASE_URL`, `CURIS_MODEL_GATEWAY_API_KEY`, `CURIS_MODEL_GATEWAY_ID`, and `CURIS_MODEL_GATEWAY_MODEL`.
- No gateway credential persistence or Admin Platform management is implemented.
- Existing FastAPI/Python 3.14 deprecation warning remains out of scope.

## Handoff

Next Seat: 产品规划席

Handoff: final closeout
