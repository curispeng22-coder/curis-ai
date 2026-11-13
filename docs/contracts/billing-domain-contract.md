# Billing Domain Contract

Status: Phase-7.7 Billing Readiness Contract

Owner: Admin Platform owns future Billing implementation. Workspace supplies approved `usage_event`, `audit_event`, and future `value_event` evidence only through contracts.

## Purpose

Convert the frozen Hybrid commercial model into a technical Billing domain contract before any Billing implementation.

This document is a contract baseline only. It does not implement Billing, payment, invoice generation, invoice UI, pricing calculation, Usage Event changes, Workspace execution-chain changes, Employee Runtime changes, Workflow changes, Credential Vault changes, or Admin Platform runtime changes.

## Commercial Boundary

Curis separates cost, value, charge, and settlement:

| Layer | Object | Meaning | Current Phase |
| --- | --- | --- | --- |
| Cost evidence | `UsageEvent` | How much AI consumed. | Existing evidence input. |
| Value evidence | `ValueEvent` | What value AI created or helped create. | Contract / validation evidence only. |
| Charge interpretation | `BillingEvent` | How Admin-rated commercial logic interprets usage/value. | Future Billing MVP. |
| Settlement document | `Invoice` | What is issued to customer. | Future, not approved now. |

Rules:

- `UsageEvent` is not `BillingEvent`.
- `ValueEvent` is not `BillingEvent`.
- `BillingEvent` is not payment.
- `Invoice` is not approved in Phase-7.7.
- `estimated_cost` is not authoritative billing amount.

## BillingSubject

`BillingSubject` is the unified object that can be priced, metered, packaged, or reserved for future billing.

Supported `subject_type`:

- `subscription`
- `usage`
- `capability_package`
- `employee_seat`
- `connector`
- `template`
- `future_value`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `subject_id` | string | Yes | Stable billing subject id. |
| `subject_type` | enum | Yes | One of the supported subject types above. |
| `tenant_id` | string nullable | Conditional | Required for tenant-scoped subjects; nullable for global official catalog definitions. |
| `source` | enum | Yes | `official` / `tenant_private` / `marketplace` / `system`. |
| `status` | enum | Yes | `draft` / `active` / `disabled` / `deprecated`. |

Boundary:

- Admin owns future billing interpretation of `BillingSubject`.
- Workspace may reference tenant-owned subjects only through approved usage/value evidence.
- `tenant_private` subjects must not become official subjects unless a marketplace/governance gate approves it.

## Plan Contract

`Plan` defines the subscription package.

Supported tiers:

- `free`
- `pro`
- `enterprise`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `plan_id` | string | Yes | Stable plan id. |
| `name` | string | Yes | Human-readable plan name. |
| `tier` | enum | Yes | `free` / `pro` / `enterprise`. |
| `features` | string[] | Yes | Feature keys enabled by the plan. |
| `quota_rules` | object[] | Yes | Plan quota definitions or references. |
| `enabled` | boolean | Yes | Whether the plan is selectable/active. |
| `created_at` | datetime | Yes | Creation timestamp. |

Rules:

- Plan lifecycle is Admin-owned in future Billing MVP.
- Workspace must not write Plan records.
- Plan enforcement is not implemented in Phase-7.7.

## Quota Contract

`Quota` defines tenant or plan limits.

Supported `quota_type`:

- `token_limit`
- `employee_seat_limit`
- `workflow_limit`
- `capability_limit`
- `connector_limit`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `quota_id` | string | Yes | Stable quota id. |
| `tenant_id` | string | Yes | Tenant receiving the quota. |
| `plan_id` | string | Yes | Plan that grants the quota. |
| `quota_type` | enum | Yes | One of the supported quota types above. |
| `limit_value` | number | Yes | Maximum allowed amount. |
| `period` | enum | Yes | `monthly` / `annual` / `custom` / `lifetime`. |
| `current_usage` | number | Yes | Usage counted for the current period. |

Rules:

- `current_usage` may be derived from `UsageEvent` aggregation in future Billing MVP.
- Quota counting must not mutate original `UsageEvent` records.
- Phase-7.7 does not enforce quotas.

## Usage Meter Contract

Usage Meter defines how runtime usage can enter commercial metering without becoming billing authority.

Supported usage sources:

- model usage
- tool usage
- connector usage
- workflow execution
- employee execution

Mapping rules:

| Usage Source | Candidate `UsageEvent` Signals | Future BillingSubject |
| --- | --- | --- |
| model usage | `model_gateway_id`, `model_name`, token fields | `usage` |
| tool usage | `capability_type=tool`, `capability_id` | `usage` / `capability_package` |
| connector usage | `capability_type=connector`, `capability_id` | `connector` / `usage` |
| workflow execution | `workflow_run_id`, `workflow_step_id` | `usage` |
| employee execution | `employee_id`, `employee_role` | `employee_seat` / `usage` |

Rules:

- `UsageEvent` records execution consumption and attribution.
- `BillingEvent` records Admin-rated commercial interpretation.
- Runtime systems must not write billing-rated amounts into `UsageEvent`.
- Usage Meter must preserve credential redaction and tenant isolation.

## Billing Event Contract

`BillingEvent` defines future rated commercial events.

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `billing_event_id` | string | Yes | Stable billing event id. |
| `tenant_id` | string | Yes | Tenant being rated. |
| `subject_type` | enum | Yes | Billing subject type being rated. |
| `subject_id` | string | Yes | Billing subject id being rated. |
| `usage_source` | enum | Yes | `model_usage` / `tool_usage` / `connector_usage` / `workflow_execution` / `employee_execution` / `future_value`. |
| `amount` | number | Yes | Rated amount or quantity depending on event stage. |
| `currency` | string | Conditional | Required when `amount` is monetary. |
| `status` | enum | Yes | `draft` / `calculated` / `issued` / `paid` / `cancelled`. |
| `created_at` | datetime | Yes | Creation timestamp. |

Rules:

- Future Admin billing logic generates `BillingEvent`.
- `BillingEvent` may reference `UsageEvent`.
- `BillingEvent` may reference `ValueEvent` only in future value-pricing gates.
- `BillingEvent` must not contain plaintext credentials, raw provider sensitive responses, or tenant_private secret material.
- `paid` status is reserved for future payment integration and is not implemented in Billing MVP unless a separate payment gate approves it.

## Value Event Link

`ValueEvent` currently supports:

- commercial value analysis,
- future value-pricing preparation,
- validation of AI employee/workflow outcomes.

Current rule:

- `ValueEvent` does not enter Billing in Phase-7.7.
- `ValueEvent` is not invoice authority.
- `ValueEvent` must remain user-confirmed or externally validated before any future value-pricing gate.

## Invoice Reserve

`Invoice` and `InvoiceLineItem` remain future Billing/finance objects.

Reserved relationship:

- one `Invoice` may include many `InvoiceLineItem`,
- one `InvoiceLineItem` may reference one `BillingEvent`.

Not approved now:

- invoice generation,
- invoice UI,
- payment collection,
- automatic deduction,
- tax calculation,
- payment-provider integration.

## Commercial Data Flow

```text
Subscription
  -> Plan
  -> Quota
  -> Usage Event
  -> Billing Event
  -> Invoice

Value Event
  -> Future Value Pricing
```

Detailed flow contract: `docs/contracts/commercial-data-flow.md`.

## Admin / Workspace Boundary

- Admin owns future Plan, Quota, BillingSubject, BillingEvent, Invoice, and InvoiceLineItem.
- Workspace owns runtime execution evidence through `usage_event`.
- Future Value Event ownership must be approved by a separate gate before implementation.
- Workspace runtime must not call `/api/platform/*`.
- Admin must not read tenant_private plaintext credentials.
- Billing contracts must not change Workflow, Employee Runtime, Credential Vault, or Task Execution.

## Not Approved In Phase-7.7

- Billing implementation.
- Payment implementation.
- Invoice generation or invoice UI.
- Marketplace revenue share.
- Value-based charging.
- ROI system.
- Usage Event structure change.
- Workflow Runtime change.
- Employee Runtime change.
- Credential Vault change.
- Workspace execution-chain change.
- Admin Platform runtime change.
