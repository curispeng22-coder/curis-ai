# Phase-8 Workspace Billing Support

Status: Implemented for verification

Owner Seat: 系统交付席

Source contracts:

- `docs/contracts/billing-domain-contract.md`
- `docs/contracts/commercial-data-flow.md`
- `issues/phase8_billing_mvp.md`

## Background

G1 Billing Gate has passed for Workspace support work. Admin owns Plan, Quota, and future BillingEvent logic. Workspace must provide accurate redacted usage evidence and Billing-query-ready aggregation without implementing Billing.

## Goal

Provide Admin Billing with accurate Workspace usage data.

## Scope

- Ensure `usage_event` projection supports tenant/task/workflow/step/employee/capability/model/token/cost metadata.
- Add read-only Usage Meter Service over existing `usage_event`.
- Reserve Admin-readable usage-meter API for future Billing queries.

## Non-goals

- Billing UI.
- Payment.
- Invoice.
- BillingEvent generation.
- Charging logic.
- Credential Vault changes.
- Workflow Runtime changes.
- Employee Runtime changes.
- Task Execution chain changes.
- Workspace runtime calls to `/api/platform/*`.

## Data Contract

Usage Event must expose:

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

## API

Admin-read-only reserved endpoint:

- `GET /api/platform/usage-meter?tenant_id=...`

Supported filters:

- `capability_type`
- `capability_source`
- `model_gateway_id`
- `model_name`
- `status`
- `since`
- `until`

Rules:

- `tenant_id` is required and fail-closed.
- Endpoint returns aggregates only; it does not generate BillingEvent or Invoice.
- Workspace frontend/runtime must not call this endpoint.

## Acceptance Criteria

- Usage Event projection contains Billing Readiness fields.
- Usage Meter aggregates Usage Events by tenant.
- Usage Meter provides totals and dimensions for capability source/type, model, employee, and workflow.
- Admin can read Usage Meter with platform token.
- Missing tenant_id returns 422.
- Missing admin token returns 401.
- Tenant isolation holds.
- No Billing UI, Payment, Invoice, BillingEvent generation, or charge logic is introduced.
