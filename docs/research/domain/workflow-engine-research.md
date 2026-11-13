# Curis Workflow Engine Research

Status: Phase-3.5 research conclusion

## Decision

Curis Phase-4 should not implement a full workflow engine. It should reserve workflow contracts and, at most, implement minimal task assignment and trace metadata for the Software R&D department.

## Evidence

- ChatDev's YAML DAG is powerful but too heavy for Phase-4.
- CrewAI's sequential process is a good first mental model.
- MetaGPT's SOP chain is useful as a fixed sequence.
- Paperclip's issue hierarchy and documents show how to preserve traceable work artifacts.

## Task to Workflow Conversion

Future conversion:

```text
Task
-> select DepartmentTemplate
-> create WorkflowInstance from WorkflowTemplate
-> create WorkflowStep records
-> assign each step to EmployeeInstance
-> bind capabilities
-> execute or collect outputs
-> write WorkflowTrace
```

Phase-4 should only do:

```text
Task
-> optional department/employee context metadata
-> no main execution flow change unless separately approved
```

## WorkflowTemplate Recommended Fields

| Field | Type | Phase-4 |
| --- | --- | --- |
| `id` | string | reserve |
| `slug` | string | reserve |
| `name` | string | reserve |
| `description` | string | reserve |
| `department_type` | string | reserve |
| `process_type` | enum: sequential / gated / hierarchical | reserve |
| `step_templates` | string[] | reserve |
| `source` | official / tenant_private / marketplace | reserve |
| `tenant_id` | string nullable | reserve |
| `enabled` | boolean | reserve |
| `created_at` | datetime | reserve |

## WorkflowStep Recommended Fields

| Field | Type | Phase-4 |
| --- | --- | --- |
| `id` | string | reserve |
| `workflow_template_id` | string | reserve |
| `step_type` | string | reserve |
| `name` | string | reserve |
| `description` | string | reserve |
| `owner_employee_template_id` | string | reserve |
| `input_contract` | object/text | reserve |
| `output_contract` | object/text | reserve |
| `required_capability_types` | string[] | reserve |
| `context_step_ids` | string[] | reserve |
| `max_iterations` | int | reserve |
| `next_step_ids` | string[] | reserve |
| `enabled` | boolean | reserve |

## WorkflowTrace Recommended Fields

| Field | Type | Phase-4 |
| --- | --- | --- |
| `id` | string | reserve |
| `tenant_id` | string | reserve |
| `task_id` | string | reserve |
| `workflow_template_id` | string | reserve |
| `workflow_step_id` | string | reserve |
| `employee_id` | string | reserve |
| `capability_source` | official / tenant_private / marketplace | reserve |
| `capability_type` | model / tool / connector | reserve |
| `capability_id` | string | reserve |
| `status` | pending / running / succeeded / failed / skipped | reserve |
| `input_summary` | text | reserve |
| `output_summary` | text | reserve |
| `error_summary` | text | reserve |
| `started_at` | datetime | reserve |
| `finished_at` | datetime | reserve |

## ChatChain / SOPChain / CrewProcess Decision

| Candidate | Decision | Reason |
| --- | --- | --- |
| ChatChain | reserve | too chat-heavy and graph-heavy for Phase-4 |
| SOPChain | adopt conceptually | good fixed sequence for Software R&D |
| CrewProcess sequential | adopt conceptually | easiest first mental model |
| CrewProcess hierarchical | reserve | needs manager routing and more safety |
| Full DAG | reject for Phase-4 | complex UI/runtime and risk to current Task Execution |

## Phase-4 Implement

- minimal R&D SOP metadata
- step ownership metadata if needed
- trace contract only
- no automatic workflow execution engine

## Phase-4 Reserve

- automatic Task -> Workflow expansion
- step scheduler
- conditional edges
- human approval nodes
- retry loops
- majority voting
- arbitrary code/tool nodes

## Guardrail

The current Task Execution path remains the source of runtime truth. Workflow research must not silently mutate:

```text
Task -> Orchestrator -> ModelGatewayAdapter/New API -> Result -> usage_event
```
