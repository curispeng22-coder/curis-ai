# Workflow Runtime Contract

Status: Phase-5.5 contract prepared for Phase-6 Workflow MVP.

Source chain:

- Research: `docs/research/competitors/metagpt.md`, `docs/research/competitors/chatdev.md`, `docs/research/competitors/crewai.md`
- Domain: `docs/research/domain/software-dev-sop-research.md`, `docs/research/domain/workflow-engine-research.md`
- Decision: `docs/research/decisions/adopted-patterns.md`
- Prior contract: `docs/contracts/workflow-template-contract.md`
- Roadmap review: `docs/release/phase55-post-g2-roadmap-review.md`

Boundary: Phase-6 may implement a minimal sequential Software R&D Workflow MVP. This contract does not approve complex DAG, visual workflow editor, cross-department workflow, marketplace workflow template, Billing, ROI, or production queue scheduler.

## Admin / Workspace Boundary

| Area | Admin Platform | Workspace |
| --- | --- | --- |
| official workflow templates | May provide future official templates | Read-only consumption |
| tenant_private workflow runtime | No ownership | Owns WorkflowInstance, WorkflowRun, WorkflowStep, StepAssignment, StepResult |
| tenant_private credentials | Must not read plaintext | Uses resolver only |
| usage_event | Reads redacted attribution | Writes tenant/workflow/step/employee attribution |
| audit_event | Reads redacted audit | Writes workflow state events |
| `/api/platform/*` | Platform-owned | Workspace runtime must not call |

## WorkflowTemplate

| Field | Type | Required | Default | Phase-6 | Future Reserve | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated / stable official id | implement | no | Stable template id. |
| `source` | enum: official / tenant_private / marketplace | yes | official | implement official only | tenant_private / marketplace | Phase-6 only ships official Software R&D template. |
| `tenant_id` | string nullable | conditional | null | no for official | yes | Required only for future tenant_private templates. |
| `name` | string | yes | none | implement | no | CEO-facing name. |
| `description` | text | no | empty | implement | no | Explains SOP purpose. |
| `department_type` | string | yes | `software_rnd` | implement | no | Phase-6 supports only Software R&D. |
| `process_type` | enum: sequential / gated / hierarchical / dag | yes | sequential | implement sequential only | gated / hierarchical / dag | Complex flow types blocked. |
| `step_template_ids` | string[] | yes | official R&D steps | implement | no | Ordered step templates. |
| `enabled` | boolean | yes | true | implement | no | Disabled templates cannot start runs. |
| `created_at` | datetime | yes | now | implement | no | System generated. |

## WorkflowInstance

| Field | Type | Required | Default | Phase-6 | Future Reserve | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated | implement | no | Tenant-local workflow instance. |
| `tenant_id` | string | yes | current tenant | implement | no | Tenant isolation boundary. |
| `company_id` | string nullable | no | current company shell | implement | no | Links to Workspace company context. |
| `project_id` | string nullable | no | null | implement association | no | Optional same-tenant ProjectRuntime correlation; does not change workflow state behavior. |
| `created_from_template_id` | string nullable | no | workflow template id | implement lineage | no | Immutable template-origin record. |
| `department_id` | string | yes | selected Software R&D department | implement | no | Must belong to same tenant. |
| `workflow_template_id` | string | yes | official Software R&D template | implement | no | First version official only. |
| `name` | string | yes | template name | implement | no | CEO-facing runtime label. |
| `status` | enum: draft / ready / disabled | yes | ready | implement | no | Instance lifecycle, not run state. |
| `enabled` | boolean | yes | true | implement | no | Disabled instance cannot start runs. |
| `created_at` | datetime | yes | now | implement | no | System generated. |

## WorkflowRun

| Field | Type | Required | Default | Phase-6 | Future Reserve | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated | implement | no | One execution of a workflow. |
| `tenant_id` | string | yes | current tenant | implement | no | Tenant isolation. |
| `task_id` | string | yes | none | implement | no | CEO requirement anchor. |
| `workflow_instance_id` | string | yes | none | implement | no | Runtime instance reference. |
| `workflow_template_id` | string | yes | none | implement | no | Template used to create run. |
| `department_id` | string | yes | none | implement | no | Must be same tenant. |
| `company_id` | string nullable | no | instance company | implement association | no | Same-tenant company correlation. |
| `project_id` | string nullable | no | null | implement association | no | Same-tenant ProjectRuntime correlation. |
| `created_from_template_id` | string nullable | no | workflow template id | implement lineage | no | Immutable template-origin record. |
| `status` | enum | yes | draft | implement | no | See state enum below. |
| `current_step_id` | string nullable | no | null | implement | no | Active step pointer. |
| `final_report` | text nullable | no | null | implement | no | Tech Lead summary after completion. |
| `error_code` | string nullable | no | null | implement | no | Redacted failure code. |
| `created_at` | datetime | yes | now | implement | no | System generated. |
| `started_at` | datetime nullable | no | null | implement | no | Set when first step starts. |
| `completed_at` | datetime nullable | no | null | implement | no | Set on completed/cancelled/failed. |
| `updated_at` | datetime | yes | now | implement | no | Updated on state changes. |

## WorkflowStep

| Field | Type | Required | Default | Phase-6 | Future Reserve | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated | implement | no | Runtime step id. |
| `tenant_id` | string | yes | current tenant | implement | no | Tenant isolation. |
| `workflow_run_id` | string | yes | none | implement | no | Parent run. |
| `step_index` | int | yes | ordered index | implement | no | Sequential order. |
| `step_type` | string | yes | none | implement | no | e.g. `requirement_clarification`. |
| `name` | string | yes | template step name | implement | no | UI label. |
| `description` | text | no | empty | implement | no | Step purpose. |
| `required_employee_role` | string | yes | template role | implement | no | Product Manager, Architect, etc. |
| `required_capability_types` | string[] | no | `["model"]` | implement | no | First version model-first. |
| `status` | enum | yes | pending | implement | no | See state enum below. |
| `input_summary` | text nullable | no | null | implement | no | Redacted prior context summary. |
| `output_summary` | text nullable | no | null | implement | no | Redacted step output summary. |
| `error_code` | string nullable | no | null | implement | no | Redacted failure code. |
| `started_at` | datetime nullable | no | null | implement | no | Set when running. |
| `completed_at` | datetime nullable | no | null | implement | no | Set on terminal status. |
| `created_at` | datetime | yes | now | implement | no | System generated. |
| `updated_at` | datetime | yes | now | implement | no | Updated on state changes. |

## StepAssignment

| Field | Type | Required | Default | Phase-6 | Future Reserve | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated | implement | no | Assignment id. |
| `tenant_id` | string | yes | current tenant | implement | no | Tenant isolation. |
| `workflow_run_id` | string | yes | none | implement | no | Parent run. |
| `workflow_step_id` | string | yes | none | implement | no | Parent step. |
| `employee_id` | string | yes | role-matched employee | implement | no | Must be same tenant and enabled. |
| `employee_role` | string | yes | employee role | implement | no | Copied for attribution. |
| `assignment_reason` | text nullable | no | role match | implement | no | Redacted explanation. |
| `status` | enum: assigned / running / completed / failed / skipped | yes | assigned | implement | no | Assignment status. |
| `created_at` | datetime | yes | now | implement | no | System generated. |

## StepResult

| Field | Type | Required | Default | Phase-6 | Future Reserve | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated | implement | no | Result id. |
| `tenant_id` | string | yes | current tenant | implement | no | Tenant isolation. |
| `workflow_run_id` | string | yes | none | implement | no | Parent run. |
| `workflow_step_id` | string | yes | none | implement | no | Parent step. |
| `employee_id` | string | yes | none | implement | no | Executor identity. |
| `employee_role` | string | yes | none | implement | no | Executor role. |
| `capability_source` | enum: official / tenant_private / marketplace | no | selected binding source | implement official / tenant_private | marketplace | Marketplace remains reserved. |
| `capability_type` | enum: model / tool / connector | no | model | implement | no | Capability used. |
| `capability_id` | string nullable | no | null | implement | no | Binding id used. |
| `output_summary` | text | yes | none | implement | no | CEO-readable output. |
| `raw_output_ref` | string nullable | no | null | no | yes | Future external artifact ref. |
| `status` | enum: completed / failed / skipped | yes | completed | implement | no | Terminal result state. |
| `error_code` | string nullable | no | null | implement | no | Redacted. |
| `created_at` | datetime | yes | now | implement | no | System generated. |

## State Enums

WorkflowRun status:

```text
draft -> ready -> running -> completed
                  |-> failed
                  |-> cancelled
```

WorkflowStep status:

```text
pending -> assigned -> running -> completed
                       |-> failed
                       |-> skipped
```

Allowed transition rules:

- A WorkflowRun can start only when it has at least one ordered WorkflowStep.
- A WorkflowStep can run only when all earlier required steps are completed or skipped by an explicit system decision.
- A completed WorkflowStep cannot be rerun in Phase-6.
- A failed WorkflowStep stops the run unless a future retry gate is approved.
- A cancelled WorkflowRun cannot resume in Phase-6.

## usage_event Field Rules

When a workflow step calls a model/tool/connector, usage_event must include:

- `tenant_id`
- `task_id`
- `workflow_run_id`
- `workflow_step_id`
- `employee_id`
- `employee_role`
- `capability_source`
- `capability_type`
- `capability_id`
- `model_gateway_id` if model call
- `model_name` if model call
- `prompt_tokens`
- `completion_tokens`
- `total_tokens`
- `estimated_cost`
- `credential_id` when credential_ref was used
- `credential_ref_digest` when credential_ref was used
- `status`
- `error_code`
- `created_at`

usage_event must not include:

- plaintext API key
- token
- secret
- credential value
- raw Authorization header
- raw sensitive provider response

## audit_event Field Rules

Allowed workflow audit events:

- `workflow.created`
- `workflow.started`
- `workflow.step_assigned`
- `workflow.step_started`
- `workflow.step_completed`
- `workflow.step_failed`
- `workflow.completed`
- `workflow.cancelled`

Allowed audit payload fields:

- `tenant_id`
- `workflow_run_id`
- `workflow_step_id`
- `task_id`
- `employee_id`
- `employee_role`
- `action`
- `status`
- `reason`
- `timestamp`

audit_event must not include:

- plaintext credentials
- hidden prompt secrets
- raw provider sensitive response
- restorable external configuration

## Phase-6 Implementation Scope

Implement:

- One official Software R&D WorkflowTemplate.
- Tenant-local WorkflowInstance and WorkflowRun.
- Ordered WorkflowStep records.
- StepAssignment and StepResult.
- Sequential `run-next-step` execution.
- Employee assignment from existing EmployeeInstance records.
- Employee capability binding reuse.
- usage_event workflow/step/employee attribution.
- audit_event workflow state changes.
- Minimal Workspace workflow status UI.

Do not implement:

- Complex DAG.
- Visual workflow editor.
- Cross-department workflows.
- Marketplace workflow templates.
- Billing.
- ROI.
- Production queue scheduler.
- Automatic employee recruiting.
- Arbitrary autonomous self-planning.

## Future Reserve Fields

Reserved, not Phase-6 implementation:

- `parallel_group_id`
- `depends_on_step_ids`
- `retry_policy`
- `approval_policy`
- `human_review_required`
- `artifact_refs`
- `quality_score`
- `cost_budget`
- `marketplace_template_id`
- `external_queue_job_id`
