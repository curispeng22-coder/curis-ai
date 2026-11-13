# Company Runtime Contract

Status: Phase 1A backend foundation contract

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace is moving the product root from direct Task execution to a Company OS runtime where Company is the CEO-facing entry point and Task becomes an internal execution record.

## Boundary

This contract defines the backend foundation for Company Runtime. It does not replace existing Task, Orchestrator, Tool Router, Model Gateway, or Credential Vault internals.

Company Runtime must preserve:

- existing Task persistence as execution substrate,
- Orchestrator execution path,
- Tool Router / Tool Executor,
- Model Gateway Adapter,
- Credential Vault resolver,
- usage_event / audit_event redacted attribution.

Company Runtime must not:

- make Task the product main entry,
- implement Billing, Pricing, Quota, Payment, Invoice, or ROI,
- let Workspace call `/api/platform/*`,
- expose tenant_private plaintext secrets,
- bypass existing Credential Vault or Model Gateway boundaries.

## Runtime Position

```text
Tenant
  -> Company
    -> Department
      -> Employee
        -> Skill
          -> Tool / Model / Connector
    -> Project
      -> WorkflowRun
        -> WorkflowStep
          -> Task execution substrate
```

## CompanyRuntime Fields

| Field | Type | Required | Default | Source Range | Phase 1A | Admin / Workspace Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `company_id` | string | yes | generated id | tenant_private | implement foundation | Workspace-owned tenant company root |
| `tenant_id` | string | yes | current tenant | tenant_private | implement foundation | tenant isolation boundary |
| `ceo_id` | string | yes | current CEO | tenant_private | implement foundation | Workspace actor context; formal auth remains separate gate |
| `name` | string | yes | none | tenant_private | implement foundation | CEO-facing company name |
| `description` | string | no | empty string | tenant_private | implement foundation | display metadata |
| `company_type` | enum | yes | `software_rnd_company` | tenant_private | implement first value | first runtime company type only |
| `status` | enum | yes | `active` | tenant_private | implement foundation | `draft` / `active` / `disabled` / `archived` |
| `created_from_template_id` | string nullable | no | null | official / tenant_private | implement lineage | optional future CompanyTemplate lineage; does not create a CompanyTemplate runtime |
| `default_department_ids` | string[] | no | `[]` | tenant_private | implement metadata | references DepartmentRuntime records |
| `default_project_id` | string nullable | no | null | tenant_private | reserve | optional current work entry |
| `created_at` | datetime | yes | current timestamp | tenant_private | implement foundation | system generated |
| `updated_at` | datetime | yes | current timestamp | tenant_private | implement foundation | system generated |

## Runtime Rules

- Company is the first Workspace runtime aggregate for the CEO.
- Project and Department must belong to a Company.
- Employee must belong to a Department and Company.
- Task must belong to a Project or WorkflowRun before becoming visible in the product flow.
- Direct task console may remain as an internal/debug route only until UI migration is complete.
- Company Runtime does not own official templates; Admin supplies official template catalogs in future gates.

## API Contract Draft

| API | Purpose | Phase 1A |
| --- | --- | --- |
| `GET /api/workspace/companies` | list tenant companies | foundation |
| `POST /api/workspace/companies` | create tenant company | foundation |
| `GET /api/workspace/companies/{company_id}` | get company runtime summary | foundation |
| `PATCH /api/workspace/companies/{company_id}` | update metadata/status | foundation |

## Invariants

- `tenant_id` must scope every company read/write.
- Company cannot mutate Admin official catalogs.
- Company cannot store credentials.
- Company cannot compute billing or quota.
- Company is a product/runtime aggregate, not a commercial tenant object.
