# Phase-8 Workspace Billing Support Implementation Report

Status: Implemented and locally verified, pending acceptance

## Product Progress

Curis Workspace can now provide Admin Billing with redacted, tenant-scoped usage evidence and read-only Usage Meter aggregates without implementing Billing.

## Implemented Scope

- Added `UsageMeterService` as a read-only aggregation layer over existing `usage.*` events.
- Added Admin-read-only `GET /api/platform/usage-meter`.
- Kept `tenant_id` fail-closed for usage-meter aggregation.
- Extended usage-event projection with:
  - `token_usage`
  - `cost_metadata`
- Extended usage-event write payload with token and cost metadata derived from existing model/tool execution usage.
- Added Phase-8 Workspace Billing Support issue.

## Not Implemented

- Billing UI.
- Payment.
- Invoice.
- BillingEvent generation.
- Charging logic.
- Plan or Quota management.
- Marketplace revenue share.
- Value Pricing.
- Credential Vault changes.
- Workflow Runtime changes.
- Employee Runtime changes.
- Task Execution chain changes.
- Workspace runtime calls to `/api/platform/*`.

## Data Shape

Usage Event supports:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `workflow_step_id`
- `employee_id`
- `capability_id`
- `capability_source`
- `model_gateway_id`
- `model_name`
- `prompt_tokens`
- `completion_tokens`
- `total_tokens`
- `token_usage`
- `estimated_cost`
- `cost_metadata`
- `status`
- `created_at`

## Usage Meter API

Endpoint:

- `GET /api/platform/usage-meter?tenant_id=...`

Filters:

- `capability_type`
- `capability_source`
- `model_gateway_id`
- `model_name`
- `status`
- `since`
- `until`

Response groups:

- `totals`
- `by_capability_source`
- `by_capability_type`
- `by_model`
- `by_employee`
- `by_workflow`

Boundary:

- Admin-read-only.
- `tenant_id` required.
- Does not create BillingEvent.
- Does not create Invoice.
- Does not mutate UsageEvent.

## Admin / Workspace Boundary

- Workspace continues to produce Usage Event and Value Event evidence.
- Admin remains responsible for Plan, Quota, and future BillingEvent logic.
- Workspace runtime does not call `/api/platform/*`.
- Credential Vault, Workflow Runtime, and Employee Runtime are unchanged.

## Verification

Commands executed:

```bash
cd backend && ../backend/.venv/bin/python -m unittest tests.test_phase8_workspace_billing_support
cd backend && ../backend/.venv/bin/python -m unittest tests.test_phase8_workspace_billing_support tests.test_adr0028_workspace_integration tests.test_d5_workspace_integration tests.test_phase6_workflow_mvp
cd backend && ../backend/.venv/bin/python -m unittest discover tests
node --test frontend/app/taskViewModel.test.mjs
cd frontend && pnpm lint
cd frontend && pnpm build
git diff --check -- backend/app/usage_meter.py backend/app/evolution_event_log.py backend/app/result_store.py backend/app/main.py backend/tests/test_phase8_workspace_billing_support.py backend/tests/test_model_gateway_adapter.py docs/release/phase8-workspace-billing-support-implementation-report.md issues/phase8_workspace_billing_support.md knowledge/CURRENT_CONTEXT.md
rg -n "/api/platform/" frontend/app --glob '!frontend/app/platform/**'
```

Result:

- 2 tests passed.
- 37 targeted integration/workflow tests passed.
- 315 backend regression tests passed.
- 32 frontend view-model tests passed.
- Frontend lint passed.
- Frontend build passed.
- Scoped `git diff --check` passed.
- Workspace frontend runtime `/api/platform/*` scan passed.
- Scoped secret scan passed.

## Known Limits

- Usage Meter is aggregation-only and not a billing ledger.
- `estimated_cost` remains non-authoritative.
- BillingEvent generation remains Admin-owned future work.
- Invoice and payment remain future-gated.

## RC Recommendation

This slice can proceed to Phase-8 Workspace Billing Support RC verification.
