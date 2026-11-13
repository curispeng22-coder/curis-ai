# Phase-4 AI Employee System MVP Review

Status: PASS

Date: 2026-07-09

Issue: `issues/phase4_ai_employee_system_mvp.md`

## Product Progress

Curis Workspace can now configure a minimal Software R&D department, create tenant-local R&D employees, bind official or tenant_private capabilities to employees, select an execution employee when creating a task, and write employee-attributed usage events after execution.

## Scope Delivered

- Official Software R&D DepartmentTemplate.
- Official R&D EmployeeTemplates:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
- Tenant-scoped DepartmentInstance create/list API.
- Tenant-scoped EmployeeInstance create/list API.
- EmployeeCapabilityBinding set/list API.
- Task create payload supports optional `employee_id`.
- Unselected tasks default to Tech Lead role metadata.
- Selected employee tasks use the employee's preferred enabled capability binding when no explicit capability is selected.
- usage_event payload and Admin projection include `employee_id`, `employee_role`, and `employee_name`.
- Workspace UI includes a minimal `研发部员工` management area and execution employee selector.

## Boundary Checks

- No ROI implementation.
- No content operations, investment, ecommerce, HR, or other department implementation.
- No capability marketplace.
- No real credential custody.
- No Admin Platform governance change.
- No direct provider SDK calls.
- Workspace UI runtime does not call `/api/platform/*`.
- Official templates remain read-only from Workspace; tenant-owned rows are `tenant_private`.

## Verification

- `backend/.venv/bin/python -m unittest tests.test_phase4_employee_system`: PASS, 3 tests.
- `backend/.venv/bin/python -m unittest discover tests`: PASS, 306 tests.
- `frontend/node --test app/taskViewModel.test.mjs`: PASS, 30 tests.
- `frontend/npm run lint`: PASS.
- `frontend/npm run build`: PASS.
- `git diff --check`: PASS on Phase-4 changed files.

## Known Gaps

- Runtime remains a minimal employee attribution and capability-selection path, not a full multi-employee workflow engine.
- WorkflowTemplate is still metadata/read-model only.
- No organization chart, multi-department UI, marketplace, billing, ROI, employee memory, or autonomous hiring.
- Local dirty worktree contains pre-existing unrelated changes; final commit should stage only Phase-4 files if a commit is requested.

## Next Seat

产品规划席 for final acceptance.

Handoff: final closeout
