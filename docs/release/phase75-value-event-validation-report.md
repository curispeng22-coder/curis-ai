# Phase-7.5 Value Event Validation Report

Date: 2026-07-09

Status: contract validation, data-boundary design, and commercial-value research only.

## Product Progress

Curis Workspace is ready to evolve from an AI consumption record system toward an AI consumption + AI value record system, while keeping ROI, Billing, payment, and execution-chain changes out of scope.

## 1. Value Event Contract Validation

Contract path:

```text
docs/contracts/value-event-contract.md
```

Required fields are confirmed:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `employee_id`
- `value_type`
- `estimated_value`
- `value_source`
- `created_at`

Validation result:

- Field set is sufficient for first commercial validation.
- System-generated identity fields are separated from user-confirmed value fields.
- Future fields are reserved without entering implementation.
- Contract avoids mixing value estimates with usage cost or billing settlement.

## 2. Field Source Validation

System generated:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `employee_id`
- `created_at`

User confirmed:

- `estimated_value`
- `value_type`
- `value_source` when manual or assumption-based

Future extension:

- `revenue_assisted`
- `business_metric_id`
- `external_reference`
- `confidence_score`
- `assumption_id`

## 3. Field Lifecycle Validation

Phase-7.5:

- Contract definition only.
- Field validation only.
- Boundary design only.
- Commercial value research only.

Future implementation:

- Value Event draft generation.
- User confirmation UI/API.
- Value Event persistence.
- Admin analytics aggregation.

Future Billing/Pricing:

- May reference confirmed Value Events as input signals.
- Must not treat Value Event as invoice authority.

## 4. Generation Flow Validation

Generation-flow path:

```text
docs/contracts/value-event-generation-flow.md
```

Validated first-version flow:

```text
Execution Result
        ↓
Generate Value Event draft
        ↓
User confirms estimated_value
        ↓
Save Value Event
```

Decision:

- Employee should not finalize value.
- Workflow may draft value context.
- User confirmation is required to avoid AI-invented value claims.

## 5. Value Type Validation

Type contract path:

```text
docs/contracts/value-event-type-contract.md
```

First-version types:

- `time_saved`
- `cost_avoided`
- `output_generated`
- `quality_improved`
- `revenue_assisted`

Validation result:

- Covers productivity value, cost avoidance, deliverable creation, quality improvement, and revenue assistance.
- Does not implement automatic ROI, revenue prediction, or financial settlement.

## 6. Usage / Value Boundary Validation

Boundary path:

```text
docs/contracts/usage-value-event-boundary.md
```

Validated boundary:

```text
Usage Event: How much did AI consume?
Value Event: What value did AI create?
```

Rules:

- Usage Event must not contain value fields.
- Value Event must not contain model cost fields.
- Neither event is sufficient by itself for authoritative billing.

## 7. Commercial Value Research

Research path:

```text
docs/research/domain/value-measurement-research.md
```

Recommendation:

- Curis should pursue a hybrid commercial model.
- Near-term: usage_event for usage/cost awareness, value_event for commercial value narrative.
- Mid-term: Admin-owned billing_event for billing interpretation.
- Long-term: combine company scale, usage, capability packs, and validated value analytics.

## 8. Billing Readiness Assessment

Assessment path:

```text
docs/research/domain/billing-readiness-assessment.md
```

Decision:

- Curis is ready to enter Billing Readiness planning.
- Curis is not ready to enter Billing implementation.

Reason:

- usage_event foundation exists.
- Value Event contract defines value-side evidence.
- Admin/Workspace boundary is clear.
- billing_event, plan/quota, invoice, rating, and payment contracts are not implemented or approved.

## 9. Strict Non-Goals Confirmed

This phase does not:

- build ROI Dashboard,
- build ROI calculation system,
- build Billing,
- build payment,
- modify Workflow Runtime,
- modify Employee Runtime,
- modify Credential Vault,
- modify Task Execution,
- add AI employees,
- add Workflow,
- add business departments,
- add Marketplace.

## 10. Verification

Required checks:

- `git diff --check`
- scoped secret scan
- changed-file scope review
