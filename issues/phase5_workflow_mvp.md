# Phase-5 Workflow MVP

Status: Draft

Owner Seat: 产品规划席 for product scope; 总控决策席 for gate; 系统交付席 after approval.

## Background

Phase-4 created R&D employee templates, employee instances, capability binding, selected employee task execution, and employee-attributed usage events. The current product still behaves like single-employee task execution, not a multi-employee AI company workflow.

## Goal

Implement the minimum Software R&D Workflow MVP so a CEO requirement can move through a bounded SOP:

```text
CEO creates requirement
-> Tech Lead breaks down work
-> Architect designs
-> Frontend / Backend execute
-> QA verifies
-> Tech Lead / Product Manager reports
```

## Non-Goals

- Do not implement unbounded autonomous multi-agent collaboration.
- Do not implement arbitrary workflow graphs.
- Do not add content operations, investment, ecommerce, HR, or other departments.
- Do not implement ROI or billing.
- Do not implement marketplace.
- Do not implement real credential vault.
- Do not modify Admin Platform governance.
- Do not break existing Task API compatibility.
- Do not bypass Model Gateway Adapter.

## Data Model Impact

Proposed minimum models:

- `WorkflowRun`
  - `id`
  - `tenant_id`
  - `task_id`
  - `department_id`
  - `workflow_template_id`
  - `status`
  - `created_at`
  - `updated_at`
- `WorkflowStep`
  - `id`
  - `tenant_id`
  - `workflow_run_id`
  - `step_type`
  - `owner_employee_id`
  - `owner_employee_role`
  - `status`
  - `input_summary`
  - `output_summary`
  - `created_at`
  - `started_at`
  - `completed_at`
- `WorkflowTrace`
  - `id`
  - `tenant_id`
  - `workflow_run_id`
  - `workflow_step_id`
  - `event_type`
  - `payload`
  - `created_at`

Constraints:

- First version supports Software R&D only.
- First version supports sequential process only.
- Step execution must use bound employee capabilities.
- usage_event should include workflow/step attribution if a model/tool call occurs.

## API Impact

Proposed API draft:

- `POST /api/workspace/workflows`
- `GET /api/workspace/workflows`
- `GET /api/workspace/workflows/{workflow_run_id}`
- `POST /api/workspace/workflows/{workflow_run_id}/run-next-step`

Rules:

- Existing `POST /api/task` must remain backward-compatible.
- Existing task execution must not be removed.
- No `/api/platform/*` Workspace runtime calls.

## UI Impact

Proposed minimum UI:

- In Workspace task detail, show workflow status.
- Show ordered SOP steps.
- Show step owner employee.
- Show step status and output summary.
- Provide one bounded run-next-step action.

Not in scope:

- Complex visual workflow builder.
- Org chart.
- Drag/drop step editor.
- Multi-department dashboard.

## Security Boundary

- Workflow must not store raw secrets.
- Workflow must not expose credential_ref/config_ref values.
- Workflow must preserve tenant isolation.
- Workflow must preserve Model Gateway Adapter-only model calls.
- If tenant_private capabilities are used, real runtime secret usage depends on G2.

## Test Requirements

- Unit tests for WorkflowRun / WorkflowStep creation.
- Unit tests for sequential step progression.
- Regression test that existing task create/run still works.
- Test that step owner must be an employee in the same tenant.
- Test that step capability selection uses only employee-bound capabilities.
- Test usage_event includes task and employee attribution; workflow/step attribution if implemented.
- Frontend tests for workflow view model.
- `git diff --check`.
- Workspace `/api/platform/*` runtime scan.
- Secret scan.

## Acceptance Criteria

- CEO can create or start a Software R&D workflow from a task.
- Tech Lead, Architect, Frontend/Backend, QA, and report steps are visible.
- Each step is owned by the correct employee role.
- Steps execute in a bounded sequential order.
- Step output is recorded.
- Task result remains readable.
- usage_event remains complete and tenant-scoped.
- Existing Phase-4 employee demo remains intact.

## Recommended Priority

P1.

Reason: this is the next major product step from employee attribution to AI company collaboration. It should follow or coordinate with G2 because real tenant_private workflow execution needs secret resolution.
