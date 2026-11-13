# Project Runtime Contract

Status: Phase 1A backend foundation contract

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace is introducing Project as the CEO-facing work container so AI company work starts from a project/request, while Task remains an internal execution substrate.

## Boundary

Project Runtime is the missing bridge between Company OS and the existing Task / Workflow execution layer.

Project Runtime preserves:

- existing Task table and execution APIs as substrate,
- existing WorkflowRun / WorkflowStep records,
- existing EmployeeCapabilityBinding,
- existing usage_event / audit_event attribution.

Project Runtime does not implement:

- project management SaaS complexity,
- Kanban/sprint boards,
- multi-business modules,
- billing or ROI,
- external customer delivery portals.

## ProjectRuntime Fields

| Field | Type | Required | Default | Source Range | Phase 1A | Admin / Workspace Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `project_id` | string | yes | generated id | tenant_private | implement foundation | Workspace-owned project id |
| `tenant_id` | string | yes | current tenant | tenant_private | implement foundation | tenant isolation |
| `company_id` | string | yes | selected company | tenant_private | implement foundation | project belongs to CompanyRuntime |
| `department_id` | string nullable | no | null | tenant_private | implement foundation | may reference an enabled software R&D department when selected |
| `name` | string | yes | none | tenant_private | implement foundation | CEO-facing project name |
| `goal` | text | yes | none | tenant_private | implement foundation | CEO request / project goal |
| `description` | text | no | empty string | tenant_private | implement foundation | supplementary project context |
| `project_type` | enum | yes | `software_development` | tenant_private | implement first value | new types require future gate |
| `status` | enum | yes | `planned` | tenant_private | implement foundation | `planned` / `active` / `blocked` / `completed` / `archived` |
| `owner_employee_id` | string nullable | no | null | tenant_private | implement foundation | optional enabled employee in the selected company/department |
| `primary_workflow_run_id` | string nullable | no | null | tenant_private | implement/reference | links to WorkflowRun |
| `root_task_id` | string nullable | no | null | tenant_private | reserve/reference | internal Task substrate link |
| `final_report` | text | no | empty string | tenant_private | reserve | CEO-facing final result |
| `created_at` | datetime | yes | current timestamp | tenant_private | implement foundation | system generated |
| `updated_at` | datetime | yes | current timestamp | tenant_private | implement foundation | system generated |

## Runtime Rules

- Project is the preferred product entry for AI R&D Company work.
- New product flows should create/select Company -> Department -> Project before Task execution.
- Task should not be presented as the primary user object.
- WorkflowRun may be created from Project brief.
- Task ids may remain as internal correlation ids for Orchestrator, execution, and usage_event.

## API Contract Draft

| API | Purpose | Phase 1A |
| --- | --- | --- |
| `GET /api/workspace/projects` | list tenant projects | foundation |
| `POST /api/workspace/projects` | create project from CEO brief | foundation |
| `GET /api/workspace/projects/{project_id}` | get project runtime summary | foundation |
| `PATCH /api/workspace/projects/{project_id}` | update project metadata/status | foundation |
| `POST /api/workspace/projects/{project_id}/start-workflow` | start approved SOP workflow | future first implementation gate |

## Invariants

- Project cannot store secrets.
- Project cannot call tools directly.
- Project cannot generate billing events.
- Project cannot bypass Workflow Runtime or Task execution substrate.
- Project must keep `tenant_id` and `company_id` scope on all reads and writes.
