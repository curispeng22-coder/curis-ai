# Phase-6 Workflow MVP

Status: Draft for gate review

Owner Seat: 产品规划席 for product scope; 总控决策席 for gate approval; 系统交付席 only after approval.

Source chain:

- Roadmap review: `docs/release/phase55-post-g2-roadmap-review.md`
- Runtime contract: `docs/contracts/workflow-runtime-contract.md`
- Prior template contract: `docs/contracts/workflow-template-contract.md`
- Employee contract: `docs/contracts/employee-template-contract.md`
- Capability contract: `docs/contracts/capability-type-contract.md`
- Adopted decisions: `docs/research/decisions/adopted-patterns.md`
- Rejected decisions: `docs/research/decisions/rejected-patterns.md`

## 1. Background

Phase-4 delivered Software R&D employee templates, employee instances, employee capability binding, selected-employee task execution, and employee-attributed usage_event.

Phase-5 G2 delivered tenant_private credential_ref resolver safety for private capability execution, with redacted usage_event and audit_event attribution.

The current product still behaves as single-employee task execution. Phase-6 should make the R&D department feel like an AI company team by adding a bounded sequential SOP workflow.

## 2. Goal

Implement the minimum Software R&D Workflow MVP:

```text
CEO creates requirement
-> Tech Lead receives and starts workflow
-> Product Manager clarifies requirement
-> Architect produces technical plan
-> Frontend Engineer executes frontend step if assigned
-> Backend Engineer executes backend step if assigned
-> QA Engineer verifies
-> Tech Lead summarizes final report
-> CEO views workflow status, step outputs, and final report
```

The first version is sequential only and must preserve existing Task Execution compatibility.

## 3. Non-Goals

- Do not implement complex DAG orchestration.
- Do not implement visual workflow editor.
- Do not implement cross-department workflows.
- Do not implement content operations, investment, ecommerce, HR, or other departments.
- Do not implement automatic employee recruiting.
- Do not implement arbitrary autonomous self-planning.
- Do not implement ROI.
- Do not implement Billing.
- Do not implement Marketplace.
- Do not implement production queue scheduler unless separately approved.
- Do not modify Admin Platform governance.
- Do not let Admin read tenant_private plaintext credentials.
- Do not let Workspace runtime call `/api/platform/*`.
- Do not break Phase-4 AI Employee System.
- Do not break Phase-5 Credential Vault.

## 4. Data Model Draft

Implement according to `docs/contracts/workflow-runtime-contract.md`.

Minimum records:

- `WorkflowTemplate`
- `WorkflowInstance`
- `WorkflowRun`
- `WorkflowStep`
- `StepAssignment`
- `StepResult`

Minimum WorkflowRun fields:

- `id`
- `tenant_id`
- `task_id`
- `workflow_instance_id`
- `workflow_template_id`
- `department_id`
- `status`
- `current_step_id`
- `final_report`
- `error_code`
- `created_at`
- `started_at`
- `completed_at`
- `updated_at`

Minimum WorkflowStep fields:

- `id`
- `tenant_id`
- `workflow_run_id`
- `step_index`
- `step_type`
- `name`
- `description`
- `required_employee_role`
- `required_capability_types`
- `status`
- `input_summary`
- `output_summary`
- `error_code`
- `started_at`
- `completed_at`
- `created_at`
- `updated_at`

## 5. API Draft

Workspace APIs:

- `GET /api/workspace/workflow-templates`
- `POST /api/workspace/workflows`
- `GET /api/workspace/workflows`
- `GET /api/workspace/workflows/{workflow_run_id}`
- `POST /api/workspace/workflows/{workflow_run_id}/run-next-step`
- `POST /api/workspace/workflows/{workflow_run_id}/cancel`

Rules:

- Existing `POST /api/task` payload remains backward-compatible.
- Workflow creation may reference an existing `task_id`.
- `run-next-step` executes only the next pending sequential step.
- Step execution must use assigned employee capability binding.
- Workspace runtime must not call `/api/platform/*`.

## 6. UI Draft

Add minimal Workflow area inside existing Workspace operation console:

- Show "R&D Workflow" entry from selected task detail.
- Show ordered SOP steps.
- Show step owner employee.
- Show step status.
- Show step output summary.
- Show final report.
- Provide a bounded "Run next step" action.

Do not add:

- Workflow canvas.
- Drag/drop editor.
- Org chart.
- Multi-department dashboard.
- Marketplace template picker.

## 7. Workflow State Machine

WorkflowRun:

```text
draft -> ready -> running -> completed
                  |-> failed
                  |-> cancelled
```

WorkflowStep:

```text
pending -> assigned -> running -> completed
                       |-> failed
                       |-> skipped
```

Transition rules:

- Run can start only when ordered steps exist.
- Step can run only when previous required step is completed.
- Failed step stops the run in Phase-6.
- Completed step cannot rerun in Phase-6.
- Cancelled run cannot resume in Phase-6.

## 8. Employee / Capability Reuse

Reuse existing:

- Software R&D DepartmentInstance.
- EmployeeInstance.
- EmployeeCapabilityBinding.
- Tech Lead default routing.
- official and tenant_private capability selector.
- Credential Resolver for tenant_private credential_ref.
- Model Gateway Adapter-only model execution.

Assignment rule:

- Each step maps to a required role.
- The system selects an enabled employee in the same tenant and department with that role.
- If multiple employees match, use explicit assignment if provided; otherwise use deterministic first enabled match.
- The assigned employee must have an enabled capability binding matching the step's required capability type.

## 9. usage_event Extensions

When a workflow step uses a model/tool/connector, usage_event must include:

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
- `credential_id` if credential_ref was used
- `credential_ref_digest` if credential_ref was used
- `status`
- `error_code`
- `created_at`

No plaintext secret material may enter usage_event.

## 10. audit_event Extensions

Allowed event types:

- `workflow.created`
- `workflow.started`
- `workflow.step_assigned`
- `workflow.step_started`
- `workflow.step_completed`
- `workflow.step_failed`
- `workflow.completed`
- `workflow.cancelled`

Allowed payload fields:

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

No plaintext secret, raw provider sensitive response, or restorable external config may enter audit_event.

## 11. Test Requirements

Backend:

- WorkflowTemplate read tests.
- WorkflowRun creation tests.
- Ordered WorkflowStep creation tests.
- StepAssignment role matching tests.
- Sequential `run-next-step` tests.
- Same-tenant employee assignment tests.
- Cross-tenant employee rejection tests.
- Employee capability binding requirement tests.
- tenant_private credential resolver path tests for private model step.
- usage_event workflow/step/employee attribution tests.
- audit_event workflow state allowlist tests.
- Regression: existing task create/run remains compatible.

Frontend:

- View model tests for ordered workflow step display.
- Run-next-step loading/success/error state tests.
- Existing task console tests remain passing.

Guards:

- `git diff --check`
- Workspace runtime `/api/platform/*` scan
- secret scan
- backend full regression
- frontend test / lint / build

## 12. Acceptance Criteria

- CEO can create or start a Software R&D workflow from a task.
- Workflow creates ordered R&D SOP steps.
- Each step has an assigned enabled employee.
- Step execution uses assigned employee capability binding.
- tenant_private private model step uses resolver and does not expose plaintext credential.
- Steps execute sequentially through `run-next-step`.
- StepResult records output summary.
- WorkflowRun reaches completed state and produces final report.
- usage_event records workflow_run_id, workflow_step_id, employee, capability, and redacted credential attribution where applicable.
- audit_event records workflow state changes with allowlisted payload.
- Existing single task execution remains intact.
- Workspace runtime does not call `/api/platform/*`.
- All existing tests continue to pass.

## Recommendation

Enter Phase-6 Workflow MVP development after 总控决策席 approves this issue.
