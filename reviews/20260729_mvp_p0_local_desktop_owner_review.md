# MVP P0 Local Desktop Owner Review

Issue: `issues/20260729_mvp_p0_local_desktop_owner.md`

Status: `PASS（Issue Scope） / BLOCKED（Workspace Full Regression）`

## 结论

Local Desktop Owner 的 Issue 范围验收通过：

`启动 Curis → 未认证保存 next → 创建/进入 Local Owner → HttpOnly Session → Onboarding → Workspace/Company → Employee → Project`

真实浏览器链已通过；Google OAuth 不再是 MVP 默认启动依赖。Google OIDC、生产 JWT、trusted gateway、租户隔离与 Local logout Origin/CSRF 边界无回归。

当前共享工作树不能宣告全量回归全绿：唯一一次全量后端回归有 1 个 Issue 外失败。因此本 Review 可供产品席接受本 Issue 的认证入口，但 Workspace 整体 Gate 仍需相关任务修复既有回归后关闭。

## 证据

### 来源与运行

- HEAD：`ce1f9b2404eb4eddcf8b1b306b5f354038616323`
- 工作树：存在用户既有未提交改动；本 Review 仅将 Allowed Files 归入本 Issue。
- 官方启动：`CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh`
- 启动结果：PASS
  - Frontend：`3001`
  - Workspace：容器内部 `8002`
  - Gateway：`8080`
- 数据源：`data/curis.sqlite`
- 本地租户：`local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4`
- `GET /health`：`200`
- `GET /gateway/api/auth/local/status`：`200`，`mode=local_desktop`
- 默认启动后 `GET /api/auth/google/status`：`401`；Local Owner 仍可完整登录，证明 MVP 不依赖 Google Client ID、Secret 或外网。

### 新库与 Session

- 新临时 SQLite 聚焦验证：
  - 首次状态：`initialized=false`、`authenticated=false`
  - 未认证受保护 API：`401`
  - `POST /api/auth/local/initialize`：`201`
  - 返回：`/onboarding?next=%2Fceo-office%2Fprojects`
  - `Set-Cookie` 包含 `HttpOnly`
  - 同一新库继续真实创建 Company、Department、Employee、Project：PASS
- 实际运行 Session 响应：
  - `HTTP 200`
  - Cookie 属性：`HttpOnly; Max-Age=28800; Path=/; SameSite=lax`
  - 响应：`{"authenticated": true, "next": "/ceo-office"}`
- 重启验证：
  - 重启后旧内存 Session 失效，原 Project 页面进入 `/login?next=<原路径>`
  - 登录页显示“本地 Owner 已创建”，未重复初始化 Owner
  - 点击“进入 Curis”生成新 Session，并返回原 Project 页面

### 真实浏览器主路径

- 未认证打开 `/ceo-office/projects?view=active`：
  - 自动进入 `/login?next=%2Fceo-office%2Fprojects%3Fview%3Dactive`
  - 未显示 `Failed to fetch`
- Local Owner 登录页可创建或进入本地 Owner，不显示 Google 登录依赖。
- Onboarding 显示：
  - `个人 Workspace 已确认`
  - 当前 Company 确认/完善入口
- Company：`Curis Local Desktop 验收公司` 可在 Onboarding 确认并进入 Curis。
- Employee：
  - 主链证据：`Local Desktop 技术负责人`
  - 质量席独立创建：`质量验收员工 20260729`
  - ID：`emp-8c1d48dd-580c-42df-a2f5-cf2346398f83`
- Project：
  - 主链证据：`project-0de38228-86ae-4dab-ad72-4eff8a338e88`
  - 质量席独立创建：`质量验收项目 20260729`
  - ID：`project-030c562c-fa20-4ad8-bdf8-e418e0859b30`
  - Project 页面真实显示目标、部门与负责人。

### 安全与回归

- Backend 身份聚焦：
  - `backend/tests/test_local_owner_auth.py`
  - `backend/tests/test_local_google_oidc.py`
  - `backend/tests/test_workspace_identity_membership.py`
  - 结果：`33 passed`
- Frontend Authentication：`4 passed`
- Frontend lint：PASS
- Frontend build：PASS，`28` 个静态页面生成
- Issue 范围 `git diff --check`：PASS
- 安全边界席：PASS
  - 外域 Origin 无法初始化、生成 Session 或强制 Local logout
  - 合法本地 Origin 可注销
  - Local Owner 在 production 环境 fail-closed
  - Google OIDC/JWT/trusted gateway/租户隔离无回归
- 运行时外域 logout：`403`

### 全量回归

- 命令：`.venv/bin/python -m pytest -q backend/tests`
- 结果：`1 failed, 1153 passed, 2 skipped`
- 唯一失败：
  - `backend/tests/test_employee_directory_qa.py::TestDepartmentDelete::test_delete_department_has_active_employees_422`
  - 期望响应包含 `active`
  - 当前响应：`department not empty: 1 employees, 0 projects`
- 来源区分：
  - 失败来自当前工作树的 `backend/app/employee_templates.py` 改动
  - 该文件不在本 Issue Allowed Files
  - Local Owner、OAuth、JWT 与前端聚焦测试全部通过，未发现该失败由本 Issue 引入

## 阻塞项

- 本 Issue 范围：无阻塞。
- Workspace 整体 Gate：Issue 外 `backend/app/employee_templates.py` 与既有测试契约不兼容，导致全量回归未全绿。

## 建议

1. 产品席可接受 Local Desktop Owner Issue 范围，Google OAuth 不再作为 MVP Gate。
2. 由拥有 `backend/app/employee_templates.py` 改动的任务修复错误文案兼容或同步既有测试契约。
3. 该 Issue 外证据变化后，仅补一次针对失败项与所需全量回归，不重复认证浏览器链。

Handoff: sent to 产品规划席；Issue 范围可接受，Workspace 整体 Gate 待 Issue 外回归恢复。
