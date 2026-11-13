# Value Event Contract

Status: Validated for Phase-7.5 Commercial Validation

Owner: Workspace may produce value-event drafts only after a future implementation gate; user confirmation remains required for `estimated_value` in the recommended first version. Admin may later consume aggregated Value Events for commercial analytics. No ROI system, charging, payment, Billing implementation, or execution-chain change is approved by this contract.

## Purpose

Value Event records estimated business value created or cost saved by an AI employee, task, or workflow. It is a commercial validation evidence layer, not a billing ledger and not an ROI engine.

## Contract Fields

| Field | Type | Required | Source | Phase-7.5 Lifecycle | Future Lifecycle | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `tenant_id` | string | yes | System generated | Contract validation only | Implementation field | Tenant that owns the work and value estimate. |
| `task_id` | string | no | System generated | Contract validation only | Implementation field | Source task id when value is attributed to a task. |
| `workflow_run_id` | string | no | System generated | Contract validation only | Implementation field | Source workflow run id when value is attributed to a workflow. |
| `employee_id` | string | no | System generated | Contract validation only | Implementation field | Employee instance that contributed to the value estimate. |
| `value_type` | enum string | yes | System suggested, user confirmable | Contract validation only | Implementation field | Type of value estimate. See `docs/contracts/value-event-type-contract.md`. |
| `estimated_value` | decimal | yes | User confirmed | Contract validation only | Implementation field; future pricing input only after review | Estimated value amount. This is non-authoritative and must be treated as an estimate. |
| `value_source` | enum string | yes | System suggested or user confirmed | Contract validation only | Implementation field | Source of estimate. Recommended first values: `manual_estimate`, `default_assumption`, `workflow_result`, `usage_derived`, `external_import`. |
| `created_at` | datetime string | yes | System generated | Contract validation only | Implementation field | Creation timestamp in ISO 8601 format. |

## Future Reserved Fields

These fields are not part of the Phase-7.5 required contract and must not be implemented without a future gate:

| Field | Type | Source | Future Purpose |
| --- | --- | --- | --- |
| `revenue_assisted` | decimal | User confirmed or external import | Track revenue that an AI workflow helped create. |
| `business_metric_id` | string | Admin/Workspace configured | Link value estimate to a defined business metric. |
| `external_reference` | string | External import | Link to CRM, ticket, order, document, or analytics record. |
| `confidence_score` | decimal | System calculated or user confirmed | Indicate confidence of estimate. |
| `assumption_id` | string | Admin/Workspace configured | Link to rate card or value assumption set. |

## Field Rules

- `tenant_id` is always required and must be used for isolation.
- At least one of `task_id`, `workflow_run_id`, or `employee_id` should be present.
- `estimated_value` must be numeric and non-negative.
- `estimated_value` must be user-confirmed in the recommended first implementation.
- `estimated_value` must not be used as authoritative billing, pricing, or ROI output.
- `value_source` must be explicit so users can distinguish manual estimates from computed estimates.
- Value Event must not contain prompt text, raw provider responses, plaintext credentials, API keys, tokens, or secrets.

## Source Classification

System generated:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `employee_id`
- `created_at`

User confirmed:

- `estimated_value`
- `value_type`
- `value_source` when the source is manual or assumption-based

Future extension:

- `revenue_assisted`
- `business_metric_id`
- `external_reference`
- `confidence_score`
- `assumption_id`

## Phase Classification

Phase-7.5 uses:

- Contract definition only.
- Field validation.
- Boundary design.
- Commercial value research.

Future implementation may use:

- Runtime Value Event draft generation.
- User confirmation UI.
- Value Event persistence.
- Admin commercial analytics aggregation.

Future Billing/Pricing may reference:

- aggregated Value Events,
- value assumptions,
- confirmed business metrics,
- but only through a separate Admin-owned pricing/billing gate.

## Relation To usage_event

usage_event answers:

```text
How much did AI consume?
```

Value Event answers:

```text
What value did AI create?
```

usage_event remains runtime metering evidence. Value Event remains commercial validation evidence. Billing should not directly charge from either without an Admin-owned billing_event/rating layer.

## Admin / Workspace Boundary

Workspace:

- May later generate Value Event drafts after task/workflow completion.
- Must require user confirmation for `estimated_value` in the first version.
- Must keep Value Events redacted and tenant-scoped.
- Must not implement billing, payment, invoice, or ROI system under this contract.

Admin:

- May later aggregate confirmed Value Events for commercial analytics.
- Must not treat Value Event as invoice authority.
- Must not read tenant_private plaintext credentials.

## Validation Result

The field design is reasonable for Phase-7.5 because it separates:

- execution attribution from value estimation,
- system-generated identity fields from user-confirmed value fields,
- commercial validation from billing/ROI.

The main open risk is estimate quality. The first implementation must avoid automatic value claims by requiring user confirmation.

## Phase-7.5 Scope

Allowed:

- Contract documentation.
- Value Event design documentation.
- Billing readiness assessment.
- Commercial value research.

Forbidden:

- Runtime implementation.
- Execution-chain modification.
- ROI system.
- Billing/payment implementation.
- Marketplace implementation.
- New AI employee, Workflow, or business department implementation.
