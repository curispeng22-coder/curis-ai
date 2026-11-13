# Department Runtime Contract

Status: Phase 1A backend foundation contract

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace is defining Department as the company-level operating unit that owns employees, skills, and project execution lanes instead of exposing Task as the main product entry.

## Boundary

Department Runtime builds on the existing DepartmentTemplate / DepartmentInstance foundation. It clarifies the runtime aggregate needed for AI Company OS.

Department Runtime preserves:

- existing `department_templates` and `department_instances`,
- existing Software R&D department MVP,
- existing Workflow Runtime,
- existing Employee Runtime.

Department Runtime does not add:

- content, investment, ecommerce, HR, or other business departments,
- complex org chart UI,
- cross-department workflow routing,
- Billing, ROI, Marketplace, or quota enforcement.

## DepartmentRuntime Fields

| Field | Type | Required | Default | Source Range | Phase 1A | Admin / Workspace Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `department_id` | string | yes | generated id | tenant_private | already partially implemented / align | Workspace-owned department runtime id |
| `tenant_id` | string | yes | current tenant | tenant_private | already implemented | tenant isolation |
| `company_id` | string | yes | selected company | tenant_private | align as required | department belongs to CompanyRuntime |
| `template_id` | string | yes | software R&D template | official / tenant_private | already implemented | official read-only; tenant_private Workspace-owned |
| `name` | string | yes | template name | tenant_private | already implemented | CEO-facing name |
| `department_type` | enum | yes | `software_rnd` | tenant_private | first value only | new types require future gate |
| `manager_employee_id` | string nullable | no | null | tenant_private | implement foundation | optional same-company employee manager; no reporting-line automation |
| `mission` | text | no | empty string | tenant_private | implement foundation | department goal/context; not autonomous planning |
| `status` | enum | yes | `active` | tenant_private | implement foundation | `draft` / `active` / `disabled` / `archived` |
| `created_from_template_id` | string nullable | no | `template_id` | official / tenant_private | implement lineage | records DepartmentTemplate origin only |
| `enabled_employee_template_ids` | string[] | yes | template defaults | tenant_private | already implemented | controls allowed employee templates |
| `default_workflow_template_id` | string nullable | no | template default | official / tenant_private | reserve/already referenced | references WorkflowTemplate |
| `created_at` | datetime | yes | current timestamp | tenant_private | already implemented | system generated |
| `updated_at` | datetime | yes | current timestamp | tenant_private | already implemented | system generated |

## Runtime Rules

- Every DepartmentRuntime must belong to one CompanyRuntime.
- Phase 1 AI R&D Company MVP supports only `software_rnd`.
- Department owns employee membership and default SOP entry.
- Department does not directly execute work; it routes through Employee + Workflow + Task substrate.
- DepartmentTemplate is a catalog/template; DepartmentRuntime is tenant-owned runtime state.

## API Contract Draft

| API | Purpose | Phase 1A |
| --- | --- | --- |
| `GET /api/workspace/companies/{company_id}/departments` | list company departments | foundation |
| `POST /api/workspace/companies/{company_id}/departments` | create/activate department | foundation |
| `GET /api/workspace/departments/{department_id}` | get department runtime summary | foundation |
| `PATCH /api/workspace/departments/{department_id}` | update metadata/status | foundation |

## Invariants

- Workspace cannot modify official DepartmentTemplate definitions.
- DepartmentRuntime cannot contain provider secrets.
- DepartmentRuntime cannot enforce commercial plan/seat quotas.
- DepartmentRuntime cannot bypass employee capability binding.
