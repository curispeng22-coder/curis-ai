# Phase-4 AI Employee System Demo Freeze Report

Date: 2026-07-09

Status: demo freeze verified, pending product acceptance.

Demo script: `docs/demo/phase4-ai-employee-demo-script.md`

RC evidence: `docs/release/phase4-ai-employee-system-rc.md`

## Product Progress

Curis Workspace can now demonstrate a minimal Software R&D employee operating loop: configure an R&D department, create a tenant-local employee, bind official and tenant_private capabilities, select the employee for task execution, and inspect employee-attributed usage events.

## Current Demo Capability

- View official Software R&D employee templates:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
- Create a tenant-local Software R&D department instance.
- Create a tenant-local employee instance from an official template.
- Preserve employee fields:
  - `tenant_id`
  - `company_id`
  - `department_id`
  - `instructions_override`
  - `status`
  - `enabled`
- Bind official capabilities to employees.
- Bind tenant_private capabilities to employees.
- Create a task with a selected employee.
- Route unselected tasks to Tech Lead by default.
- Execute task through the existing model gateway path.
- Write `usage_event` with employee attribution.
- Query Admin usage projection by `tenant_id`.
- Preserve tenant_private isolation from `/api/catalog/*`.

## Demo Flow

Use `docs/demo/phase4-ai-employee-demo-script.md` as the operator script.

High-level flow:

1. Start local model gateway.
2. Start backend.
3. Start frontend.
4. Open Workspace.
5. View R&D employee templates.
6. Add tenant_private model/tool/connector demo data.
7. Create Software R&D department instance.
8. Create Tech Lead employee instance.
9. Bind official and tenant_private capabilities to the employee.
10. Create a task and select the employee.
11. Run the task.
12. Confirm task result.
13. Query Admin usage events and confirm employee attribution.

## Screenshot Checklist

Required screenshots:

- Workspace `研发部员工` template list.
- Workspace employee instance list.
- Workspace employee capability binding panel.
- Workspace task creation form with selected employee.
- Workspace task execution result.
- Admin usage_event query result showing `employee_id` or `employee_role`.

## Stability Verification

Frontend unit tests:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
```

Result: 30 tests passed.

Frontend lint:

```bash
cd frontend && npm run lint
```

Result: passed.

Frontend build:

```bash
cd frontend && npm run build
```

Result: passed.

Backend full regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: 306 tests passed.

Diff check:

```bash
git diff --check -- backend/app/database.py backend/app/employee_templates.py backend/app/evolution_event_log.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/tests/test_employee_template_contract.py backend/tests/test_model_gateway_adapter.py backend/tests/test_phase4_employee_system.py frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs issues/phase4_ai_employee_system_mvp.md knowledge/CURRENT_CONTEXT.md reviews/084_phase4_ai_employee_system_mvp_review.md docs/release/phase4-ai-employee-system-rc.md reviews/085_phase4_ai_employee_system_rc_review.md docs/demo/phase4-ai-employee-demo-script.md docs/release/phase4-ai-employee-demo-freeze-report.md
```

Result: passed.

Workspace runtime `/api/platform/*` scan:

```bash
rg -n "/api/platform/" frontend/app/page.js backend/app/employee_templates.py backend/app/orchestrator.py backend/app/result_store.py frontend/app/taskViewModel.mjs
```

Result: no matches.

Secret scan:

```bash
rg -n "sk-[A-Za-z0-9]{16,}|BEGIN (RSA|OPENSSH|EC|PRIVATE)|api[_-]?key\s*=|credential_ref\s*[:=]\s*['\"][^'\"]*(sk-|key|secret)" backend/app/database.py backend/app/employee_templates.py backend/app/evolution_event_log.py backend/app/main.py backend/app/orchestrator.py backend/app/result_store.py backend/tests/test_employee_template_contract.py backend/tests/test_phase4_employee_system.py frontend/app/page.js frontend/app/taskViewModel.mjs issues/phase4_ai_employee_system_mvp.md reviews/084_phase4_ai_employee_system_mvp_review.md docs/release/phase4-ai-employee-system-rc.md reviews/085_phase4_ai_employee_system_rc_review.md docs/demo/phase4-ai-employee-demo-script.md docs/release/phase4-ai-employee-demo-freeze-report.md
```

Result: no matches.

Phase-4 RC smoke:

```bash
cd backend && ./.venv/bin/python <phase4_rc_smoke>
```

Result: passed.

Evidence:

```text
roles ['architect', 'backend_engineer', 'frontend_engineer', 'product_manager', 'qa_engineer', 'tech_lead']
template_sources ['official', 'tenant_private'] marketplace_schema_reserved True
bindings [('tenant_private', 'model', 'phase4-private-model', 1, True), ('official', 'tool', 'claude_tool', 20, True)]
task ... tenant_private phase4-private-model COMPLETED
default_employee_role tech_lead
usage_event includes tenant_id, task_id, employee_id, employee_role, capability_source, capability_type, capability_id, model_gateway_id, model_name, status, created_at
```

## Known Limits

- This is local/demo only, not hosted production.
- Phase-4 demonstrates minimal employee attribution and capability selection, not a full workflow engine.
- First department is Software R&D only.
- Marketplace source is reserved in schema/contracts, but capability marketplace is not active.
- Employee templates are read-only official metadata plus tenant-scoped extensions; Workspace does not modify official templates.
- No organization chart, multi-department UI, employee memory, autonomous hiring, ROI, billing, marketplace, or real credential custody.
- Browser screenshot capture remains a manual demo step.

## Temporarily Not Included

Demo Freeze does not include:

- ROI system.
- Content operations, investment, ecommerce, HR, or other departments.
- Capability marketplace.
- Real `credential_ref` hosting or secret custody.
- Admin Platform governance changes.
- Complex workflow engine.
- New business modules.
- Provider SDK or direct provider calls.
- New API source changes.
- Curis dependency on New API internal database.

## Freeze Decision

Phase-4 AI Employee System MVP can be frozen as the local/demo version after product acceptance.

Next recommended step: capture the six screenshots listed above from a clean `/tmp/curis_phase4_demo.sqlite` demo database.
