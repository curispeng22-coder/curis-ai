# Phase-7 Billing Usage Contract Gate

Status: Draft for cross-team gate review

Owner Seat: 产品规划席 for product scope; Admin Platform team for billing implementation ownership; Workspace team for usage_event compatibility review.

Source review: `docs/release/phase65-post-workflow-roadmap-review.md`

## Background

Curis is moving toward a commercial multi-tenant AI company system. Workspace now emits usage_event records with tenant, task, workflow, step, employee, capability, model, token, cost estimate, status, and credential digest attribution.

These records are useful for usage analytics, but not yet billing-grade settlement.

## Goal

Define a Billing Usage Contract that lets Admin Platform plan billing without moving billing authority into Workspace.

## Non-Goals

- Do not implement Billing in Workspace.
- Do not implement invoice, payment, tax, refund, or subscription lifecycle in this gate.
- Do not change Workflow runtime behavior.
- Do not implement Marketplace.
- Do not implement ROI.
- Do not expose tenant_private plaintext credentials.
- Do not let Workspace runtime call `/api/platform/*`.

## Data Model Impact

Draft only; no implementation approved.

Candidate Admin-owned models:

- `billing_event`
- `billing_period`
- `plan`
- `quota`
- `invoice`
- `invoice_line_item`

Workspace-owned data should remain usage_event/audit_event attribution only.

## API Impact

Draft only; no implementation approved.

Candidate Admin APIs:

- `GET /api/platform/billing/usage`
- `GET /api/platform/billing/periods`
- `GET /api/platform/billing/invoices`

Workspace should not call these APIs at runtime.

## UI Impact

Admin Platform may later add billing views.

Workspace should not add billing UI in this gate.

## Security Boundary

- Billing aggregation must not contain plaintext credentials.
- Billing aggregation must not expose raw provider sensitive responses.
- Cost authority must be defined by Admin Platform, not Workspace estimates alone.
- Tenant isolation is mandatory.

## Workspace Compatibility Requirements

Workspace must preserve or map these usage dimensions:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `workflow_step_id`
- `employee_id`
- `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `model_gateway_id`
- `model_name`
- `prompt_tokens`
- `completion_tokens`
- `total_tokens`
- `estimated_cost`
- `credential_id`
- `credential_ref_digest`
- `status`
- `created_at`

## Test Requirements

- Contract tests for tenant isolation.
- Aggregation tests for workflow/step/employee/capability dimensions.
- Redaction tests for credential fields.
- Fail-closed tests when `tenant_id` is missing.
- Workspace runtime `/api/platform/*` scan.

## Acceptance Criteria

- Admin and Workspace agree on billing input fields.
- Workspace does not own billing implementation.
- Admin can build usage aggregation without reading tenant_private plaintext.
- No runtime behavior change is introduced by this gate.

## Recommended Priority

P1/P2.

Reason: commercial readiness needs billing, but implementation should be Admin-led and should not interrupt Workspace demo hardening.
