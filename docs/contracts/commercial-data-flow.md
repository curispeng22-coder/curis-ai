# Commercial Data Flow

Status: Phase-7.7 Billing Readiness Contract

Owner: Admin Platform owns future commercial flow implementation. Workspace supplies redacted runtime evidence through approved events.

## Purpose

Define the future commercial data path for Curis Hybrid pricing without implementing Billing, payment, invoice generation, Marketplace, ROI, or runtime changes.

## Primary Flow

```text
Subscription
  ↓
Plan
  ↓
Quota
  ↓
Usage Event
  ↓
Billing Event
  ↓
Invoice
```

Meaning:

- `Subscription`: future tenant enrollment into a plan.
- `Plan`: Free / Pro / Enterprise commercial package.
- `Quota`: plan limits for tokens, seats, workflows, capabilities, and connectors.
- `Usage Event`: Workspace runtime consumption evidence.
- `Billing Event`: future Admin-rated commercial interpretation.
- `Invoice`: future customer-facing billing document.

Phase-7.7 stops at contract definition. It does not generate BillingEvent or Invoice.

## Value Flow

```text
Value Event
  ↓
Future Value Pricing
```

Meaning:

- `Value Event` records estimated value created by tasks, workflows, or AI employees.
- `Future Value Pricing` may use validated value evidence in a later gate.

Current rule:

- Value Event does not enter Billing now.
- AI must not self-declare invoiceable value.
- Value Event must not contain token/model cost fields.

## Evidence Boundaries

| Evidence | Answers | Owner | Billing Role |
| --- | --- | --- | --- |
| `UsageEvent` | How much did AI consume? | Workspace writes; Admin observes. | Input signal only. |
| `ValueEvent` | What value did AI create? | Future gated commercial validation layer. | Future optional input only. |
| `BillingEvent` | What should be commercially rated? | Future Admin Billing. | Billing preparation. |
| `Invoice` | What should be issued to customer? | Future Admin Billing/Finance. | Settlement document. |

## Guardrails

- Do not mutate `UsageEvent` to add billing-rated amounts.
- Do not use `estimated_cost` as authoritative invoice amount.
- Do not include plaintext credentials in any commercial record.
- Do not let Workspace runtime call `/api/platform/*`.
- Do not let Admin read tenant_private plaintext credentials.
- Do not enforce commercial limits in Workflow, Employee Runtime, Credential Vault, or Task Execution during Phase-7.7.

## Future Gate Mapping

| Gate | Commercial Step | Notes |
| --- | --- | --- |
| G0 | Usage observation | Current foundation. |
| G1 | Plans + model/token quota billing | Candidate Phase-8 Billing MVP. |
| G2 | AI employee seats | Uses EmployeeSeat contract. |
| G3 | Marketplace revenue share | Depends on package governance. |
| G4 | Value-based pricing | Depends on validated Value Event maturity. |
