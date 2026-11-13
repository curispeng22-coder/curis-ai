# Phase 1 AI Company Runtime Foundation Report

Status: verified implementation complete

Date: 2026-07-10

## Product Progress

Curis Workspace can now model a tenant AI company through Company, Engineering Department, Project, Employee, Skill, and Tool runtime records while retaining Task and Workflow as execution substrate.

## Implemented Scope

- Company Runtime supports tenant-scoped create, list, read, update, default-company initialization, and optional template-origin lineage.
- Department Runtime supports a company-owned Software R&D department, optional same-company manager, mission, lifecycle status, and template-origin lineage.
- Project Runtime remains the preferred CEO work container and validates Company, Department, and optional owner employee lineage.
- Employee instances now retain immutable template-origin lineage and are normalized to the selected department's company.
- Task records can carry optional `company_id` and `project_id`; `POST /api/workspace/projects/{project_id}/tasks` creates the internal task through a Project entry point.
- Workflow instances and runs carry additive Company/Project/template correlation. Workflow sequencing and state behavior are unchanged.
- Skill Runtime supplies source-scoped templates and employee skill bindings. Only sanitized, bounded, non-authoritative skill guidance reaches the existing prompt path.
- Tool Runtime provides a normalized read-only view. EmployeeToolBinding is a filtered projection of existing `EmployeeCapabilityBinding` records, not a second authority model.

## Data Model

| Runtime area | Additive state |
| --- | --- |
| Company | `created_from_template_id` lineage |
| Department | manager, mission, status, template lineage |
| Project / Task | Company and Project association for task context |
| Employee | template-origin lineage |
| Skill | `skill_templates`, `employee_skill_bindings` |
| Tool | tool template lineage and normalized runtime read model |
| Workflow | Company, Project, and template lineage associations |

## API Surface

- `GET`, `POST` `/api/workspace/companies`
- `GET`, `PATCH` `/api/workspace/companies/{company_id}`
- `GET`, `POST` `/api/workspace/companies/{company_id}/departments`
- `GET`, `PATCH` `/api/workspace/departments/{department_id}`
- `GET`, `POST` `/api/workspace/projects`
- `GET`, `PATCH` `/api/workspace/projects/{project_id}`
- `POST` `/api/workspace/projects/{project_id}/tasks`
- `GET`, `POST` `/api/workspace/skills/templates`
- `GET`, `PUT` `/api/workspace/employees/{employee_id}/skills`
- `GET`, `PUT` `/api/workspace/employees/{employee_id}/tools`
- `GET` `/api/workspace/tools/runtime`
- `GET` `/api/workspace/tools/runtime/{tool_runtime_id}`

## Security And Tenant Boundary

- Every new Company, Department, Project, Employee, Skill, and Tool read/write stays tenant-scoped.
- Skill guidance rejects secret-like and runtime-selection content. It cannot select a tool, model, or credential.
- Tenant-private credentials remain resolver-only; this work introduces no plaintext storage, client response field, or direct provider call.
- Workspace has no runtime dependency on `/api/platform/*`.
- Usage and audit event schemas and existing attribution behavior are unchanged.

## Verification

Run after implementation:

```bash
cd backend
.venv/bin/python -m unittest tests.test_employee_template_contract tests.test_phase1a_ai_company_runtime_foundation tests.test_phase1a_company_project_runtime tests.test_phase4_employee_system tests.test_phase5_credential_vault tests.test_phase6_workflow_mvp -v
.venv/bin/python -m unittest discover tests -v
```

The focused Phase 1A / Employee / Credential Vault / Workflow regression suite passes 23 tests. The full backend regression passes 452 tests. `git diff --check`, scoped secret scanning, and the Workspace runtime `/api/platform/*` scan pass. Independent review found and the implementation fixed three P1 risks: company-scoped default employee selection, cross-company Task/Workflow correlation, and credential-URI rejection in Skill guidance.

## Deliberately Not Implemented

- CEO Office, Meeting, or Secretary UI.
- CompanyTemplate, DepartmentTemplate, EmployeeTemplate, Skill, Tool, or Workflow marketplace runtime.
- Billing, Payment, Invoice, ROI, or commercial configuration.
- New provider SDKs, direct provider calls, or Credential Vault changes.
- Workflow lifecycle redesign, complex DAG, or visual workflow editor.

## Next Stage

The next bounded backend slice should expose the new Company/Project aggregates in the CEO-facing product shell and then add only the minimum approved Department/Employee operational UI. It must not reintroduce Task as the top-level product entry.
