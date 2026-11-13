# Value Event Generation Flow

Status: Phase-7.5 design only

No runtime implementation is approved by this document.

## Goal

Define where Value Event should be produced in theory without modifying Task Execution, Workflow Runtime, Employee Runtime, or Credential Vault.

## Theoretical Chain

```text
Task / Workflow / Employee completes
        ↓
Execution Result is available
        ↓
System prepares Value Event draft
        ↓
User reviews and confirms estimated_value
        ↓
Confirmed Value Event is saved
```

## Who Produces Value Event?

### Employee Produces?

Not recommended for first version.

Reason:

- AI employees may overstate their own value.
- Employee-generated value risks hallucinated commercial claims.
- Employee runtime should stay focused on task execution.

### Workflow Summary Produces?

Recommended as draft source only.

Reason:

- Workflow has full step context.
- Workflow can map results to employee roles and step outputs.
- Workflow can draft candidate `value_type` and `value_source`.

Boundary:

- Workflow must not auto-finalize `estimated_value`.
- Workflow must not claim ROI.

### User Confirms?

Recommended first-version final authority.

Reason:

- Business value is contextual.
- CEO/operator is responsible for confirming whether output saved time, avoided cost, or assisted revenue.
- User confirmation prevents AI from inventing value.

## Recommended First Version

```text
Execution Result
        ↓
Generate Value Event draft
        ↓
User confirms value_type, estimated_value, value_source
        ↓
Save Value Event
```

First version rules:

- System may prefill `tenant_id`, `task_id`, `workflow_run_id`, `employee_id`, and `created_at`.
- System may suggest `value_type`.
- System may suggest `value_source = workflow_result` or `default_assumption`.
- User must confirm `estimated_value`.
- User may override `value_type` and `value_source`.

## Draft Payload Example

```json
{
  "tenant_id": "default",
  "task_id": "task-123",
  "workflow_run_id": "wfr-123",
  "employee_id": "emp-tech-lead",
  "value_type": "time_saved",
  "estimated_value": null,
  "value_source": "workflow_result",
  "created_at": "2026-07-09T10:00:00Z",
  "status": "draft"
}
```

`status` is shown here as a future implementation helper only. It is not part of the Phase-7.5 required contract.

## Confirmation Payload Example

```json
{
  "value_type": "time_saved",
  "estimated_value": 2.5,
  "value_source": "manual_estimate"
}
```

## Boundary Rules

- Do not modify Task Execution.
- Do not modify Workflow Runtime.
- Do not modify Employee Runtime.
- Do not modify Credential Vault.
- Do not let AI finalize estimated value without user confirmation.
- Do not store ROI output.
- Do not create billing_event from Value Event in Workspace.

## Future Gate Questions

Before implementation, decide:

- Should Value Event drafts be per employee step, per workflow, or both?
- Should user confirmation happen in Workspace or Admin?
- Should `estimated_value` represent hours, currency, score, or typed unit?
- Should an `assumption_id` be required for default assumptions?
- Should Value Events be editable after confirmation?
