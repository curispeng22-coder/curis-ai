# Phase 1A Company / Project Runtime Backend

Status: implementation report

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace can now manage a tenant-scoped AI Company and its Projects as the product runtime entry, while preserving Task and Workflow as internal execution substrates.

## Implemented Scope

- Added tenant-scoped `companies` persistence and a lazy default `Curis AI Company` for tenants without a Company runtime record.
- Added tenant-scoped `projects` persistence with Company ownership, optional Department and Employee owner references, and the `planned` / `active` / `blocked` / `completed` / `archived` lifecycle.
- Added Workspace-only Company APIs:
  - `GET /api/workspace/companies`
  - `POST /api/workspace/companies`
  - `GET /api/workspace/companies/{company_id}`
  - `PATCH /api/workspace/companies/{company_id}`
- Added Workspace-only Project APIs:
  - `GET /api/workspace/projects`
  - `POST /api/workspace/projects`
  - `GET /api/workspace/projects/{project_id}`
  - `PATCH /api/workspace/projects/{project_id}`
- Added Company / Project tenant isolation, Company ownership validation, enabled Department ownership validation, and optional Employee owner validation.

## Data Model

`companies` stores Company identity, tenant scope, CEO context, display metadata, Company type, lifecycle state, default marker, and default Department / Project references.

`projects` stores Project identity, tenant and Company scope, optional Department and owner Employee references, goal, description, Project type, lifecycle state, and future Workflow / Task reference fields. No Project API creates or executes a Task in this phase.

## Task And Workflow Relationship

Company and Project are now the intended Workspace product hierarchy:

```text
Company -> Project -> Department -> Employee / Skill / Tool -> Workflow / Task execution substrate
```

The existing direct Task API is preserved for internal and compatibility use. This phase does not alter Task execution, Workflow Runtime, Employee Runtime, Tool Router, Model Gateway, or Credential Vault.

## Tenant Isolation

- All Company and Project reads and writes scope through `TenantContext`.
- A tenant cannot retrieve another tenant's Company or Project identifier.
- A Project can reference only an enabled Department in the same tenant and Company.
- An optional Project owner must be an enabled Employee in the same tenant and Company, and in the selected Department when one is present.

## Not Implemented

- CEO Office, Meeting, Secretary, or Employee Persona UI.
- Department Runtime completion or multi-department expansion.
- Project-to-Workflow startup, Project-to-Task linking, project summary read models, or Project lifecycle propagation from workflow state.
- Billing, Pricing, Quota, Payment, Invoice, Marketplace, ROI, or Admin Commercial Configuration changes.

## Verification

Run from `backend/`:

```bash
.venv/bin/python -m unittest tests.test_phase1a_company_project_runtime -v
```

This focused suite covers default Company initialization, Company CRUD, tenant isolation, Project CRUD, Company and Department ownership validation, and the Workspace `/api/platform/*` dependency boundary.

Full backend regression and final source-control checks are recorded with the issue completion evidence.

## Known Limits

- Project has no automatic Department seed; `department_id` remains nullable until Department Runtime is implemented.
- Project does not yet start or summarize a WorkflowRun.
- `primary_workflow_run_id`, `root_task_id`, and `final_report` remain reserved runtime fields.

## Next Gate

The backend foundation is ready for the Department / Employee Runtime Backend issue, followed by Company / Project summary read models. Those follow-up issues must preserve the current execution and security boundaries.
