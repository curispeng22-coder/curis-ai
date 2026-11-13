# Review 067: Model Gateway Runtime Secret Guardrails

Date: 2026-07-08

Issue: `issues/070_model_gateway_runtime_secret_guardrails.md`

## Delivery Result

PASS.

Curis Workspace now has the ADR-0029 runtime guardrail slice required before production external-model operation can move to quality verification.

## Implemented

- Startup/runtime validation: partial model gateway env configuration fails closed before default runtime gateway execution is enabled.
- Runtime redaction: `ModelGatewayAdapter` redacts bearer tokens, API-key-like strings, prompt text, and raw response-like text from gateway error surfaces.
- UsageEvent guardrail: model gateway UsageEvent payloads remain allowlisted to approved meter fields plus existing non-secret tenant/CEO envelope and idempotency fields; secret-like values in allowed string fields are redacted.
- Gateway/model metadata guardrail: gateway and official-model metadata writes reject secret-like values before persistence or platform/catalog API exposure.
- Workspace model calls remain constrained to `ModelGatewayAdapter`.

## Changed Files

- `backend/app/model_gateway.py`
- `backend/app/main.py`
- `backend/app/result_store.py`
- `backend/app/model_catalog.py`
- `backend/tests/test_model_gateway_adapter.py`
- `backend/tests/test_d5_qa_boundary.py`
- `issues/070_model_gateway_runtime_secret_guardrails.md`
- `reviews/067_model_gateway_runtime_secret_guardrails_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Verification

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_model_gateway_adapter tests.test_d5_qa_boundary
../backend/.venv/bin/python -m unittest discover tests
cd ..
git diff --check
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}' . -g '!deploy/new-api/.env' -g '!deploy/new-api/data/**' -g '!backend/data/**' -g '!backend/tests/**' -g '!backend/.venv/**' -g '!frontend/node_modules/**' -g '!.git/**'
rg -n "ROI|billing|tenant package|provider SDK|calciumion/new-api|New API internal DB|Employee CRUD|multi-agent" backend/app/model_gateway.py backend/app/main.py backend/app/result_store.py backend/app/model_catalog.py
git diff --name-only -- frontend
```

Evidence:

- Focused guardrail tests: 16 tests passed.
- Backend regression: 203 tests passed.
- TDD red check: the new guardrail tests failed before implementation for missing startup validation, missing error redaction, missing UsageEvent redaction, and metadata accepting secret-like values.
- `git diff --check`: passed.
- Secret pattern scan outside ignored local files and backend test/runtime data: no matches.
- Scope drift scan across implementation files: no forbidden scope matches.
- Frontend diff guard: no frontend files changed.

## Scope Check

- No UI files changed.
- No billing, ROI, tenant package, provider SDK, New API source change, New API internal DB dependency, or Curis DB credential persistence was added.
- No new provider path was added; runtime model execution remains behind `ModelGatewayAdapter`.

## Known Gaps

- Production secret-manager retrieval remains out of scope and blocked pending a separate security-approved issue.
- Live external smoke remains opt-in and dependent on protected local/CI secret injection.

## Quality Verification

PASS.

Fresh verification was run by 质量运行席 on commit `b01edfd4`.

Commands:

```bash
cd backend
../backend/.venv/bin/python -m unittest tests.test_model_gateway_adapter tests.test_d5_qa_boundary
../backend/.venv/bin/python -m unittest discover tests
cd ..
git diff --check
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}' . -g '!deploy/new-api/.env' -g '!deploy/new-api/data/**' -g '!backend/data/**' -g '!backend/tests/**' -g '!backend/.venv/**' -g '!frontend/node_modules/**' -g '!.git/**'
rg -n "ROI|billing|tenant package|provider SDK|calciumion/new-api|New API internal DB|Employee CRUD|multi-agent" backend/app/model_gateway.py backend/app/main.py backend/app/result_store.py backend/app/model_catalog.py
git diff --name-only -- frontend
rg -n "openai|requests|httpx|aiohttp|urllib|calciumion|new-api|NEW_API|CURIS_MODEL_GATEWAY|Authorization|Bearer" backend/app -g '*.py'
```

Evidence:

- Focused runtime guardrail tests: 16 tests ran and passed.
- Backend regression: 203 tests ran and passed.
- `git diff --check`: passed.
- Secret pattern scan outside ignored local files and backend test/runtime data: no matches.
- Forbidden-scope scan across implementation files: no matches.
- Frontend diff guard: no frontend files changed.
- Model-call constraint scan found outbound HTTP implementation only in `backend/app/model_gateway.py`; runtime app wiring still routes default LLM tools through `ModelGatewayAdapter`.

Acceptance Check:

- Startup/runtime env validation is covered by focused tests and `ModelGatewayAdapter.validate_runtime_config`.
- Runtime error redaction is covered by focused tests and `redact_model_gateway_text`.
- UsageEvent allowlist regression is covered by focused tests and `ResultStore._record_usage_event`.
- Gateway/model metadata no-secret regression is covered by focused tests and metadata rejection in `model_catalog.py`.
- ADR-0029 forbidden scope stayed outside this change.

Quality Result: PASS; no blockers found.

## Product Acceptance

ACCEPTED by 产品规划席 on 2026-07-08.

Reason:

- The implementation satisfies ADR-0029 bounded follow-up scope.
- Quality verification passed on commit `b01edfd4`.
- External service and secret boundary stayed intact.
- No UI, billing, ROI, tenant package, New API source change, Curis DB credential persistence, provider SDK, or New API internal DB dependency was added.
- Workspace model execution remains constrained to `ModelGatewayAdapter`.

## Handoff

Delivery Handoff: sent to 质量运行席

Next Seat: 产品规划席

Handoff: sent to 产品规划席

Payload sent:

```text
Issue: issues/070_model_gateway_runtime_secret_guardrails.md
Objective: Accept ADR-0029 runtime guardrail quality verification for commit b01edfd4.
Special Constraints: Quality verification passed with no blockers. External service + secret boundary preserved; no UI, billing, ROI, tenant package, New API source change, Curis DB credential persistence, provider SDK, or New API internal DB dependency found. Model calls remain constrained to ModelGatewayAdapter.
Next Seat: main thread closeout after acceptance.
```
