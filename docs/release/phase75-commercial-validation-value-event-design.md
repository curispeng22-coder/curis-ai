# Phase-7.5 Commercial Validation: Value Event Design

Date: 2026-07-09

Status: design and contract preparation only.

Contract: `docs/contracts/value-event-contract.md`

## Product Progress

Curis Workspace can now demonstrate AI employees completing a Software R&D SOP workflow; Phase-7.5 adds the commercial validation basis for estimating what that work may be worth without implementing Billing or ROI.

## 1. Why Value Event Exists

Curis already records usage_event and audit_event. These show what happened, who did it, which capability was used, and which workflow/step/employee produced the activity.

Commercial validation needs a different question:

```text
What value did this AI employee or workflow likely create?
```

Value Event is the first contract for answering that question in a controlled way.

## 2. Usage Event vs Value Event

| Event | Primary Question | Example Fields | Ownership | Not For |
| --- | --- | --- | --- | --- |
| usage_event | What was used? | tenant, task, workflow, employee, capability, tokens, estimated cost | Workspace runtime evidence, Admin observability | Invoice authority by itself |
| audit_event | What state/security action happened? | workflow state changes, credential actions, redacted audit payload | Workspace/Admin observability | Value or billing calculation |
| value_event | What value was likely created? | tenant, task, workflow, employee, value_type, estimated_value, value_source | Future commercial validation layer | ROI system or billing by itself |
| billing_event | What billable amount should be rated? | billing period, metric, quantity, rate, amount | Future Admin-owned billing layer | Runtime execution evidence |

## 3. How To Estimate AI Employee Value

Initial value estimates should be conservative and explainable.

Recommended sources:

- Manual estimate by CEO or operator.
- Default assumption per employee role.
- Workflow result metadata.
- usage_event-derived activity count.
- External business system import in a future gate.

Recommended formula pattern:

```text
estimated_value = quantity * assumption_rate
```

Examples:

- Tech Lead decomposes a task: `time_saved = 0.5 hours`.
- Product Manager clarifies requirements: `time_saved = 0.75 hours`.
- Architect drafts technical plan: `time_saved = 1.0 hour`.
- Frontend/Backend Engineer outputs implementation plan or patch: `time_saved = 1.5 hours`.
- QA Engineer finds issue before release: `quality_improved` estimate.

The first version should prefer transparent assumptions over complex scoring.

## 4. How To Estimate Cost Saved

Cost avoided can be derived from estimated human time saved:

```text
cost_avoided = estimated_hours_saved * assumed_hourly_cost
```

Example:

```text
3.0 hours saved * 50 USD/hour = 150 USD estimated cost_avoided
```

Rules:

- The hourly cost assumption must be visible.
- The result is an estimate, not an accounting figure.
- It must not be used for invoices.
- It must not be mixed with provider model cost without labels.

## 5. How This Supports Future ROI

Future ROI needs at least two sides:

```text
ROI input = estimated value created
ROI cost = usage/billing cost
```

Phase-7.5 does not build ROI. It only prepares the value side of the future model.

Future ROI could compare:

- Value Event `estimated_value`.
- usage_event token/capability cost signals.
- Admin billing_event rated amounts.
- Human-reviewed business outcomes.

The system should not claim ROI until both value and cost are validated through separate gates.

## 6. Recommended Initial Value Types

- `time_saved`
- `cost_avoided`
- `output_generated`
- `quality_improved`
- `revenue_assisted`

## 7. Recommended Initial Value Sources

- `manual_estimate`
- `default_assumption`
- `workflow_result`
- `usage_derived`
- `external_import`

## 8. Example Value Events

Time saved by Architect step:

```json
{
  "tenant_id": "default",
  "task_id": "task-123",
  "workflow_run_id": "wfr-123",
  "employee_id": "emp-architect",
  "value_type": "time_saved",
  "estimated_value": 1.0,
  "value_source": "default_assumption",
  "created_at": "2026-07-09T10:00:00Z"
}
```

Cost avoided by full workflow:

```json
{
  "tenant_id": "default",
  "task_id": "task-123",
  "workflow_run_id": "wfr-123",
  "employee_id": null,
  "value_type": "cost_avoided",
  "estimated_value": 150.0,
  "value_source": "workflow_result",
  "created_at": "2026-07-09T10:05:00Z"
}
```

## 9. Generation Flow

Recommended first version:

```text
Execution Result
        ↓
Generate Value Event draft
        ↓
User confirms value_type, estimated_value, value_source
        ↓
Save Value Event
```

Reason:

- AI employees should not self-declare commercial value.
- Workflow can provide context for a draft.
- User confirmation prevents invented value claims.

## 10. Boundaries

Phase-7.5 does not approve:

- Value Event runtime storage.
- Value Event API.
- Billing implementation.
- Payment implementation.
- ROI system.
- Execution-chain modification.
- New employees.
- New workflows.
- New business departments.

## 11. Next Gate Recommendation

If accepted, the next gate should be either:

- Value Event read/write planning gate, if the user wants commercial validation inside Workspace.
- Billing readiness gate, if the user wants Admin-side commercial planning first.

Implementation must not start until a separate issue is approved.
