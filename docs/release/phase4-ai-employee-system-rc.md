# Phase-4 AI Employee System MVP RC

Date: 2026-07-09

Status: RC verified, pending product acceptance.

## Product Progress

Curis Workspace can now configure a minimal Software R&D department, create tenant-local R&D employees from templates, bind official or tenant_private capabilities to employees, select an employee when creating a task, and write employee-attributed usage events after execution.

## Completed Capabilities

- Official Software R&D `DepartmentTemplate`.
- Official R&D `EmployeeTemplate` set:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
- Tenant-local `DepartmentInstance`.
- Tenant-local `EmployeeInstance`.
- `EmployeeCapabilityBinding` for official and tenant_private capabilities.
- Task creation with optional `employee_id`.
- Default employee routing to Tech Lead when no employee is selected.
- Employee capability resolution before execution.
- Employee-attributed `usage_event` fields:
  - `employee_id`
  - `employee_role`
  - `employee_name`
- Workspace UI area for minimal R&D employee management.

## Acceptance Flow

1. Read official employee templates from `GET /api/workspace/employee-templates`.
2. Confirm all six R&D roles are present and active.
3. Confirm official templates carry `source=official`.
4. Confirm tenant_private template rows are tenant-scoped and not visible to another tenant.
5. Confirm `marketplace` remains source-schema reserved only; it is not activated because marketplace is outside the Phase-4 gate.
6. Create a Software R&D department instance.
7. Create an employee instance from the Tech Lead template.
8. Confirm employee instance fields:
   - `tenant_id`
   - `company_id`
   - `department_id`
   - `instructions_override`
   - `enabled`
   - `status`
9. Create a tenant_private model capability.
10. Bind the employee to one tenant_private model and one official tool.
11. Confirm unbound explicit capability selection is rejected.
12. Create a task with selected employee.
13. Run the task.
14. Confirm task output reaches `COMPLETED`.
15. Confirm `usage_event` contains employee and capability attribution.
16. Confirm task without explicit employee defaults to Tech Lead.
17. Confirm another tenant cannot read the employee or bindings.
18. Confirm `/api/catalog/*` does not expose tenant_private capabilities.
19. Confirm Workspace runtime does not call `/api/platform/*`.
20. Confirm Admin usage projection can read employee-attributed usage events by `tenant_id`.

## Test Commands And Results

### Phase-4 RC Smoke

Command:

```bash
cd backend && .venv/bin/python - <<'PY'
# TestClient smoke covered employee templates, tenant_private isolation,
# department and employee creation, official/private capability binding,
# selected employee task execution, Tech Lead default routing,
# usage_event attribution, and catalog isolation.
PY
```

Result:

```text
PASS phase4_rc_smoke
roles ['architect', 'backend_engineer', 'frontend_engineer', 'product_manager', 'qa_engineer', 'tech_lead']
template_sources ['official', 'tenant_private'] marketplace_schema_reserved True
department dept-0d24e5d4-3a85-4897-bf2e-6253184e5809 phase4-tenant-a company-rc
employee emp-1d7a7066-4f9e-46ec-aa85-9d38c35d8732 phase4-tenant-a tech_lead idle True
bindings [('tenant_private', 'model', 'phase4-private-model', 1, True), ('official', 'tool', 'claude_tool', 20, True)]
task 88c3a336-c44c-4c15-b09c-1c76045cbc58 emp-1d7a7066-4f9e-46ec-aa85-9d38c35d8732 tenant_private phase4-private-model COMPLETED
default_employee_role tech_lead
usage_event {'tenant_id': 'phase4-tenant-a', 'task_id': '88c3a336-c44c-4c15-b09c-1c76045cbc58', 'employee_id': 'emp-1d7a7066-4f9e-46ec-aa85-9d38c35d8732', 'employee_role': 'tech_lead', 'capability_source': 'tenant_private', 'capability_type': 'model', 'capability_id': 'phase4-private-model', 'model_gateway_id': 'newapi', 'model_name': 'phase4-rc-model', 'status': 'success', 'created_at': '2026-07-09 03:29:59'}
```

### Backend Regression

Command:

```bash
cd backend && .venv/bin/python -m unittest discover tests
```

Result:

```text
Ran 306 tests in 11.137s
OK
```

### Frontend View-Model Tests

Command:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
```

Result:

```text
tests 30
pass 30
fail 0
```

### Frontend Lint

Command:

```bash
cd frontend && npm run lint
```

Result:

```text
eslint .
PASS
```

### Frontend Build

Command:

```bash
cd frontend && npm run build
```

Result:

```text
Compiled successfully
Route (app)
/
/_not-found
/platform
```

### Diff Whitespace Check

Command:

```bash
git diff --check -- backend/app/database.py backend/app/employee_templates.py backend/app/evolution_event_log.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/tests/test_employee_template_contract.py backend/tests/test_model_gateway_adapter.py backend/tests/test_phase4_employee_system.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs issues/phase4_ai_employee_system_mvp.md knowledge/CURRENT_CONTEXT.md reviews/084_phase4_ai_employee_system_mvp_review.md
```

Result:

```text
PASS
```

### Workspace Runtime Platform API Scan

Command:

```bash
! rg -n "/api/platform/" frontend/app/page.js backend/app/employee_templates.py backend/app/orchestrator.py backend/app/result_store.py frontend/app/taskViewModel.mjs
```

Result:

```text
PASS
```

### Scoped Secret Scan

Command:

```bash
! rg -n "sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|api[_-]?key\s*=|credential_ref\s*[:=]\s*['\"][^'\"]*(sk-|key|secret)" backend/app/database.py backend/app/employee_templates.py backend/app/evolution_event_log.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/tests/test_employee_template_contract.py backend/tests/test_phase4_employee_system.py frontend/app/page.js frontend/app/taskViewModel.mjs issues/phase4_ai_employee_system_mvp.md reviews/084_phase4_ai_employee_system_mvp_review.md
```

Result:

```text
PASS
```

### Live API Template Smoke

Command:

```bash
curl -sS -H 'X-Tenant-Id: demo-tenant' http://127.0.0.1:8000/api/workspace/employee-templates | python3 -c 'import json,sys; p=json.load(sys.stdin); print(len(p["employee_templates"]), sorted(i["role"] for i in p["employee_templates"]))'
curl -sS -H 'X-Tenant-Id: demo-tenant' http://127.0.0.1:8000/api/workspace/department-templates | python3 -c 'import json,sys; p=json.load(sys.stdin); print([(i["id"], i["department_type"]) for i in p["department_templates"]])'
```

Result:

```text
6 ['architect', 'backend_engineer', 'frontend_engineer', 'product_manager', 'qa_engineer', 'tech_lead']
[('official.department.software_rnd', 'software_rnd')]
```

## Governance Checks

- Workspace runtime did not call `/api/platform/*`.
- Workspace did not add official-template write APIs.
- tenant_private employee template visibility stayed tenant-scoped.
- tenant_private capability rows did not appear in `/api/catalog/*`.
- Admin remained read-only for Workspace employee instances and only read usage projection by `tenant_id`.
- No Admin Platform governance logic was changed.

## Fixes During RC

- No functional fix was required during RC verification.
- No new product feature was added during RC verification.

## Known Limits

- Phase-4 uses minimal employee attribution and capability selection; it is not a full workflow engine.
- The first department is Software R&D only.
- Marketplace source is schema/contract-reserved but not active in Workspace because capability marketplace is out of scope.
- Employee templates are official read models plus tenant-scoped metadata; Workspace does not edit official templates.
- No complex org chart, multi-department UI, employee memory, autonomous hiring, ROI, billing, marketplace, or real credential custody.

## Not Doing In This Phase

- ROI or cost optimization system.
- Content operations, investment, ecommerce, HR, or other departments.
- Capability marketplace.
- Real credential_ref storage or secret custody.
- Admin Platform governance changes.
- Complex workflow engine or multi-agent orchestration.

## Release Candidate Decision

Phase-4 AI Employee System MVP is suitable to enter Phase-4 Demo Freeze after product acceptance.
