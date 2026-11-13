# Usage Event And Value Event Boundary

Status: Phase-7.5 design only

## Boundary Summary

Usage Event records AI consumption.

Value Event records AI-created value estimates.

They must remain separate.

```text
Usage Event: How much did AI consume?
Value Event: What value did AI create?
```

## Usage Event

Usage Event records:

- model calls,
- tool calls,
- connector calls,
- token consumption,
- API cost estimates,
- execution resource consumption,
- task/workflow/step/employee/capability attribution,
- status and error metadata.

Usage Event may include:

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

Usage Event must not include:

- value_type,
- estimated business value,
- revenue assisted,
- ROI,
- user-confirmed value assumptions.

## Value Event

Value Event records:

- task output value estimate,
- time saved,
- cost avoided,
- output generated,
- quality improvement,
- revenue assisted estimate,
- value source,
- tenant/task/workflow/employee attribution.

Value Event may include:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `employee_id`
- `value_type`
- `estimated_value`
- `value_source`
- `created_at`

Value Event must not include:

- model token fields,
- API cost fields,
- provider raw response,
- credential fields,
- API key,
- token,
- secret,
- model_gateway_id,
- model_name.

## Relationship

Usage Event can support Value Event drafting by showing what work happened.

Value Event can support future commercial validation by showing estimated value.

Neither event is sufficient by itself for authoritative billing.

Future Billing should use Admin-owned billing_event and rating rules.

## Forbidden Coupling

- Do not write value fields into usage_event.
- Do not write model cost fields into value_event.
- Do not calculate ROI directly from usage_event in Workspace.
- Do not calculate invoices directly from value_event.
- Do not expose tenant_private credentials in either event stream.
