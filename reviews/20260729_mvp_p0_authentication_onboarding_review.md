# MVP P0 Authentication & Onboarding Review

Issue: `issues/20260729_mvp_p0_authentication_onboarding.md`

Status: `BLOCKED_L2`

## 结论

认证与 Onboarding 的本地代码契约、未认证跳转、缺少 Owner 绑定时的可执行提示、登录页 Desktop/Mobile 布局、前端构建及安全边界均通过独立检查。

当前不能判定 Issue 完成：

1. 官方启动后的 `/api/auth/google/status` 明确返回 `owner_binding_ready=false`，因此真实 Google 登录、首次登录进入 Onboarding、登录后返回原页面，以及浏览器内 Company → Department → Employee → Project → Task 真链尚未执行。Owner OAuth 受控注入是唯一外部阻塞。
2. 当前共享工作树的唯一一次全量后端回归有 1 个 Issue 外失败，未满足 Acceptance 9。失败来自未列入本 Issue Allowed Files 的 `backend/app/employee_templates.py` 当前改动，其部门非空错误文案不再包含既有测试要求的 `active`。

## 证据

### 运行来源

- HEAD：`1591a0dda87bec504cd465fe84823f030a1869d2`
- 工作树：包含用户既有未提交改动；本 Review 不把这些改动归入本 Issue。
- 启动：`CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh`
- 启动结果：PASS；Frontend `3001`、Workspace 容器内部 `8002`、Gateway `8080`。
- 数据源：`data/curis.sqlite`
- 本地租户：`local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4`
- `GET http://127.0.0.1:8080/health`：`200`
- `GET http://127.0.0.1:3001/gateway/api/auth/google/status`：`200`，`owner_binding_ready=false`、`authenticated=false`
- 无 session 访问受保护 API：`401`
- 缺少 Owner 绑定时访问 Google 登录入口：`303` 到 `/login?error=owner_binding_not_ready`，未返回 `trusted_identity_missing`

### 测试与构建

- 认证聚焦后端：`.venv/bin/python -m pytest -q backend/tests/test_local_google_oidc.py` → `20 passed`
- 认证前端：`node --test frontend/tests/mvp-p0-auth-onboarding.test.mjs` → `4 passed`
- Frontend lint：`pnpm --dir frontend lint` → PASS
- Frontend build：`pnpm --dir frontend build` → PASS，`28` 个静态页面生成，包含 `/login` 与 `/onboarding`
- Issue 范围 `git diff --check`：PASS
- 安全边界席独立回传：PASS；Backend 身份与 OIDC `28 passed`，Frontend Authentication/Onboarding `4 passed`，生产 JWT、trusted gateway、租户隔离继续 fail-closed。
- 唯一一次全量后端回归：`.venv/bin/python -m pytest -q backend/tests` → `1 failed, 1149 passed, 2 skipped`
  - 失败：`backend/tests/test_employee_directory_qa.py::TestDepartmentDelete::test_delete_department_has_active_employees_422`
  - 现象：期望响应包含 `active`，当前响应为 `department not empty: 1 employees, 0 projects`
  - 来源：`backend/app/employee_templates.py:275` 当前工作树改动；该文件不在本 Issue Allowed Files。

### Desktop 浏览器

- 未认证打开 `/ceo-office/projects?view=active`：
  - 自动进入 `/login?next=%2Fceo-office%2Fprojects%3Fview%3Dactive`
  - 未显示 `Failed to fetch`
- Workspace、Department、Employee、Project、Task、Capability 的已知受保护入口均进入 `/login?next=<原路径>`。
- 未认证打开 `/onboarding?next=%2Fceo-office` 也被保护并进入登录页。
- 登录页 `1280×720`：
  - 文档宽度 `1280 = clientWidth 1280`
  - 登录卡片 `448×288`，位于 `x=416, y=216`
  - 无窄列与横向溢出
- 登录页 `390×844`：
  - 文档宽度 `390 = clientWidth 390`
  - 登录卡片 `350×284`，位于 `x=20, y=280`
  - 提示文字完整可读，无横向溢出
- 页面显示可执行 Owner 绑定说明：`deploy/curis/启用本地 Owner 绑定.command`

### 本地契约覆盖

- callback 首次 Owner 激活进入 `/onboarding?next=<安全原路径>`
- 返回 Owner 登录后回到原访问页面
- 前后端均拒绝绝对 URL、协议相对 URL、反斜杠、TAB、CRLF 与跨 Origin return path
- Onboarding 复用当前个人 Workspace 与既有 Company API；没有新增 Workspace/Admin 模型
- 已认证 TestClient 真实写 API 链覆盖 Company、Department、Employee、Project、Task 创建
- OAuth state、nonce、issuer、audience、exp、subject、membership 校验保持覆盖

## 阻塞项

1. `BLOCKED_L2 / WAIT_FOR_OWNER_INJECTION`：Owner 需通过既有受控流程向当前本地进程注入 Google OAuth Client ID、Client Secret 与 bootstrap material；不得写入仓库、日志或浏览器。
2. 当前共享工作树全量回归失败 1 项。应由拥有 `backend/app/employee_templates.py` 改动的既有任务修复测试兼容性或回收该改动后，质量席再按新证据安排回归；本 Issue 不得越界修改该文件。

## 建议

- Owner 完成受控注入后，从 `/ceo-office/projects?view=active` 发起一次真实 Google 登录，记录 callback → Onboarding → 原页面，以及 Company → Department → Employee → Project → Task 浏览器闭环。
- 先由相关任务处理 Issue 外回归失败；在实现证据变化后再申请质量复核。
- 在以上两项完成前，不关闭本 Issue，不用 mock、TestClient 或静态页面代替真实浏览器登录链。

Handoff: sent to 系统交付席；完成 Owner 注入与 Issue 外回归恢复后回到质量运行席复核。
