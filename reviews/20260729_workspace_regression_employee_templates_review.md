# Workspace Regression — Department Delete Contract Review

Issue: `issues/20260729_workspace_regression_employee_templates.md`

Status: `PASS`

## 结论

PASS。

`delete_department_instance()` 已恢复既有 `active employees` 错误语义，同时保留在职员工、employee affiliations 与 projects 三类部门非空保护。先前 Workspace 全量唯一失败已解除；主线程完成的唯一一次 Backend 全量、Frontend、官方启动证据全部通过。

Local Owner、Google OAuth、JWT、Session、Gateway 与前端认证文件未产生本 Issue 增量。

## 证据

### 来源与范围

- HEAD：`a66177ccce8e8d6b437df188502e2fdfb615d866`
- 唯一代码范围：`backend/app/employee_templates.py`
- 当前错误契约：
  - `department not empty: {emp_count} active employees, {aff_count} affiliations, {proj_count} projects`
- `git diff --check -- backend/app/employee_templates.py`：PASS
- Local Owner 认证边界检查：
  - `backend/app/local_google_oidc.py`
  - `backend/tests/test_local_owner_auth.py`
  - `deploy/curis/start-local.sh`
  - `deploy/curis/gateway/docker-compose.yml`
  - `deploy/curis/gateway/envoy.yaml.template`
  - `frontend/app/login/page.js`
  - `frontend/app/onboarding/page.js`
  - `frontend/lib/api.js`
  - `frontend/lib/auth.mjs`
  - `frontend/tests/mvp-p0-auth-onboarding.test.mjs`
  - 相对当前 HEAD 的工作树增量：无

### 根因复核

- 旧失败要求 422 detail 包含 `active`。
- 扩展部门非空保护后，文案曾变为 `department not empty: 1 employees, 0 projects`，遗漏既有契约词。
- 当前修复仅恢复错误语义并分别输出三类计数，没有删除或绕过任何非空检查。
- 既有测试未被修改以迁就实现。

### 独立单项

- 命令：
  - `.venv/bin/python -m pytest -q backend/tests/test_employee_directory_qa.py::TestDepartmentDelete::test_delete_department_has_active_employees_422`
- 结果：`1 passed`

### 已完成的唯一全量与前端证据

按工作流复用主线程在本次代码证据上的唯一执行结果，不重复运行：

- Backend 全量：`1155 passed, 2 skipped, 0 failed`
- Frontend tests：`7 passed`
- Frontend lint：PASS
- Frontend build：PASS
- 官方启动：`CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh` → PASS

### 当前启动现状

- `GET http://127.0.0.1:8080/health`：`200`
- `GET http://127.0.0.1:3001/gateway/api/auth/local/status`：`200`
- Local Owner：`mode=local_desktop`、`initialized=true`
- 数据源：`data/curis.sqlite`
- Frontend：`3001`
- Workspace：容器内部 `8002`
- Gateway：`8080`

## 阻塞项

无。

## 建议

- 关闭本 Regression Issue。
- 解除 Workspace 整体 Gate 的既有全量回归阻塞。
- 不重复认证浏览器、Frontend 或 Backend 全量验证；后续仅在相关实现证据变化时重新进入质量席。

Handoff: sent to 产品规划席；建议接受并关闭本 Issue。
