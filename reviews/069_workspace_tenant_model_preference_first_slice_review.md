# Review 069: Workspace Tenant Model Preference First Slice

Date: 2026-07-08

Issue: `issues/072_workspace_tenant_model_preference_first_slice.md`

## Delivery Result

PASS.

Curis Workspace now has the backend-only first slice for tenant-scoped default model preference over active official model catalog metadata.

## Implemented

- Added metadata-only `tenant_model_preferences` persistence with fields limited to `tenant_id`, `model_key`, `gateway_ref`, `model_name`, `source`, and `updated_at`.
- Added `TenantModelPreferenceResolver` for tenant-scoped read/write/delete and runtime resolution against active `source=official` official model catalog metadata.
- Added Workspace backend APIs:
  - `GET /api/workspace/model-preference`
  - `PUT /api/workspace/model-preference`
  - `DELETE /api/workspace/model-preference`
- Runtime execution remains constrained to `ModelGatewayAdapter`; tenant preference only supplies `gateway_id` and `model_name` metadata to the adapter.
- Invalid or stale stored preferences are treated as unavailable and runtime falls back to the existing default adapter metadata, not to automatic model optimization.

## Changed Files

- `backend/app/database.py`
- `backend/app/model_preferences.py`
- `backend/app/main.py`
- `backend/app/model_gateway.py`
- `backend/tests/test_tenant_model_preference.py`
- `issues/072_workspace_tenant_model_preference_first_slice.md`
- `reviews/069_workspace_tenant_model_preference_first_slice_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## TDD Evidence

Red check:

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_tenant_model_preference
```

Expected and observed before implementation:

- 4 focused tests failed with missing `/api/workspace/model-preference` behavior.

Green checks:

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_tenant_model_preference
../backend/.venv/bin/python -m unittest discover tests
```

Evidence:

- Focused tenant preference tests: 4 tests passed.
- Backend regression: 207 tests passed.

## Scope Check

- Backend-only slice; no frontend files changed.
- No Admin UI, Workspace complex UI, billing, ROI, tenant package, marketplace, automatic model optimization, secret storage, credential persistence/exposure, provider SDK, direct provider calls, New API source/internal DB dependency, per-department/per-employee policy, tool routing/workflow mutation, Tool System v1.8 loop change, or execution path drift was added.
- Preference APIs expose only non-secret catalog/preference metadata.
- Model execution stays behind `ModelGatewayAdapter`.

## Verification

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_tenant_model_preference
../backend/.venv/bin/python -m unittest discover tests
cd ..
git diff --check
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}' . -g '!deploy/new-api/.env' -g '!deploy/new-api/data/**' -g '!backend/data/**' -g '!backend/tests/**' -g '!backend/.venv/**' -g '!frontend/node_modules/**' -g '!.git/**'
rg -n "provider SDK|direct provider|New API source|New API internal DB|automatic model optimization|per-department|per-employee|execution path drift|tenant package|marketplace" backend/app/database.py backend/app/model_preferences.py backend/app/main.py backend/app/model_gateway.py
git diff --name-only -- frontend
```

Evidence:

- `git diff --check`: passed.
- Secret pattern scan outside ignored local files and backend test/runtime data: no matches.
- Forbidden-scope scan across implementation files: no matches.
- Frontend diff guard: no frontend files changed.

## Known Gaps

- Workspace UI selector remains blocked unless separately approved.
- Production secret-manager retrieval remains out of scope under ADR-0029.

## Quality Verification

PASS.

Fresh implementation verification was run by 质量运行席 on commit `a0d3a54b`.

Commands:

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_tenant_model_preference
../backend/.venv/bin/python -m unittest discover tests
cd ..
git diff --check a0d3a54b^ a0d3a54b
git diff --name-only a0d3a54b^ a0d3a54b
git diff --name-only a0d3a54b^ a0d3a54b -- frontend admin-platform workspace shared deploy plugins tools data
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}' . -g '!deploy/new-api/.env' -g '!deploy/new-api/data/**' -g '!backend/data/**' -g '!backend/tests/**' -g '!backend/.venv/**' -g '!frontend/node_modules/**' -g '!.git/**'
rg -n "provider SDK|direct provider|New API source|New API internal DB|automatic model optimization|per-department|per-employee|execution path drift|tenant package|marketplace|billing|ROI|Admin UI|Workspace complex UI|credential persistence|secret storage|tool routing|workflow mutation|Tool System v1.8 loop" backend/app/database.py backend/app/model_preferences.py backend/app/main.py backend/app/model_gateway.py backend/tests/test_tenant_model_preference.py
rg -n "requests|httpx|aiohttp|openai|anthropic|urllib\\.request|urlopen|Authorization|Bearer|CURIS_MODEL_GATEWAY|New API|newapi|provider" backend/app/database.py backend/app/model_preferences.py backend/app/main.py backend/app/model_gateway.py
git diff a0d3a54b^ a0d3a54b -- backend/app/database.py backend/app/main.py backend/app/model_gateway.py backend/app/model_preferences.py | rg -n "^\\+.*(requests|httpx|aiohttp|openai|anthropic|urlopen|urllib\\.request|New API|provider SDK|direct provider)"
```

Evidence:

- Focused tenant preference tests: 4 tests ran and passed.
- Backend regression: 207 tests ran and passed.
- Commit diff hygiene passed.
- Commit changed files are limited to backend implementation/test files, the issue/review, and source-of-truth status/context updates; no frontend/Admin/shared/runtime-deploy UI files entered the commit.
- Secret pattern scan outside ignored local files and backend test/runtime data returned no matches.
- Forbidden-scope scan found only existing database comments and test negative assertions; no implementation drift was found.
- Direct provider call/provider SDK diff scan returned no matches; model execution remains behind `ModelGatewayAdapter`.

Acceptance Check:

- Preference write is limited to active `source=official` official model catalog entries.
- Preference read/write/delete are tenant-scoped and covered by focused tests.
- `tenant_model_preferences` stores only `tenant_id`, `model_key`, `gateway_ref`, `model_name`, `source`, and `updated_at`.
- Workspace preference API evidence covers no-secret read model exposure.
- Runtime resolution revalidates stored preferences; invalid/stale preferences fall back to existing default adapter metadata, not automatic model optimization.
- ADR-0030, ADR-0029, runtime secret guardrails, and `ModelGatewayAdapter`-only execution path are preserved.

Quality Result: PASS; no blockers found.

## Product Acceptance

ACCEPTED by 产品规划席 on 2026-07-08.

Reason:

- Quality verification passed for commit `a0d3a54b`.
- Backend-only first slice stayed inside ADR-0030 and ADR-0029 boundaries.
- Runtime preference resolution remains behind `ModelGatewayAdapter`.
- No frontend/Admin/shared/runtime-deploy UI files entered the commit.
- No forbidden scope or secret exposure was found.

## Handoff

Delivery Handoff: sent to 质量运行席

Quality Handoff: sent to 产品规划席

Next Seat: main thread closeout

Handoff: final closeout

Quality payload sent:

```text
Issue: issues/072_workspace_tenant_model_preference_first_slice.md
Objective: Accept backend-only tenant-scoped default model preference first-slice verification for commit a0d3a54b.
Special Constraints: Quality verification passed with no blockers. Backend-only first slice preserved; no frontend/Admin/shared/runtime-deploy UI files entered the commit. ADR-0030, ADR-0029, runtime secret guardrails, and ModelGatewayAdapter-only execution path are preserved.
Next Seat: main thread closeout after acceptance.
```
