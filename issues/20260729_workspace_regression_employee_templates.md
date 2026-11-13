# Workspace Regression — Department Delete Contract

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_workspace_regression_employee_templates_review.md`

## Objective

修复 Workspace 全量回归唯一失败：

`backend/tests/test_employee_directory_qa.py::TestDepartmentDelete::test_delete_department_has_active_employees_422`

## Root Cause

`delete_department_instance()` 扩展了部门非空保护，新增 employee affiliations 与 projects 检查，但同时把既有错误契约：

`department still has active employees`

改为：

`department not empty: N employees, N projects`

新文案遗漏 `active`，导致既有 API 契约测试失败；删除保护本身仍正确。

## Boundary

- 代码修改仅限 `backend/app/employee_templates.py`。
- 不修改 Local Owner、Google OAuth、JWT、Session、Gateway 或前端认证。
- 保留员工、多归属与项目三类非空保护。
- 不修改既有测试以迁就实现。

## Acceptance

1. 在职员工阻止部门删除时，422 detail 保留 `active employees` 语义。
2. employee affiliations 与 projects 继续阻止部门删除。
3. Backend 全量测试全部通过。
4. Frontend 测试、lint/build 与官方启动链通过。

## Verification

- 目标回归：`2 passed`（在职员工拒删、仅 disabled 员工可删）。
- Backend 全量：`1155 passed, 2 skipped, 0 failed`。
- Frontend tests：`7 passed`；lint/build PASS。
- 官方启动、Gateway `/health` 与 Local Owner status：PASS。
- Review：`reviews/20260729_workspace_regression_employee_templates_review.md`。
