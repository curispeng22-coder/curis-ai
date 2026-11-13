# MVP P0 — Authentication & Onboarding Recovery

Status: SUPERSEDED — LOCAL DESKTOP OWNER

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_p0_authentication_onboarding_review.md`

## Objective

恢复 Curis 首次进入与返回访问的真实用户链路：

`打开 Curis → 未认证跳转登录 → Google 登录 → 返回原页面 / 首次进入 Onboarding → 确认 Workspace → 创建或选择 Company → 进入首页`

并验证登录后可继续完成 Department、Employee、Project 与 Task 创建。

## Root Cause Baseline

- 唯一本地启动链以 production/gateway 模式启动 Workspace，但未启用既有 local Google OIDC；因此认证路由虽然在 Envoy 免 JWT，后端仍进入 trusted gateway 身份校验并返回 `trusted_identity_missing`。
- 前端共享 API 层未处理 `401`，页面把未认证显示为 `Failed to fetch`。
- local Google OIDC callback 固定跳转旧 Project Runtime，不保存原访问页面，也没有首次登录 Onboarding。
- 登录页关键布局完全依赖异步样式，冷启动时可能短暂压缩为不可用窄列。

## Product And Security Boundary

- 不重写认证架构；保留生产 JWT + trusted gateway 校验，以及仅限 local/development 的 server-side Google OIDC session。
- 不创建第二套 Workspace/Admin；Onboarding 只确认当前个人 Workspace，并复用现有 Company API。
- 不在前端保存 JWT、Google token、Client Secret 或 Subject；session 继续使用 HttpOnly Cookie。
- `next` 只允许当前前端的相对路径，禁止绝对 URL、协议相对 URL和开放重定向。
- 生产环境继续 fail-closed；本地 OIDC 仅由官方本地启动链显式启用。
- OAuth Client Secret 继续通过现有受控注入流程进入进程内存，不写入仓库、日志或浏览器。
- 不修改数据库 schema，不弱化 issuer/audience/nonce/state/exp/subject/membership 校验。

## Tasks

- T031：修复官方本地启动链，使 `/api/auth/google/*` 进入既有 local/development OIDC 路径。
- T032：共享 API 层检测 `401`，保存安全的原访问路径并跳转 `/login`。
- T033：Google callback 安全返回原页面；首次 Owner 激活进入 Onboarding。
- T034：新增首次使用 Onboarding，确认当前 Workspace，创建或选择 Company 后进入首页。
- T035：修复登录页 Desktop 冷启动关键布局并显示 Owner 绑定状态。
- T036：运行认证聚焦测试、Frontend lint/build、网关配置检查和真实浏览器主路径。

## Allowed Files

- `issues/20260729_mvp_p0_authentication_onboarding.md`
- `reviews/20260729_mvp_p0_authentication_onboarding_review.md`
- `backend/app/local_google_oidc.py`
- `backend/tests/test_local_google_oidc.py`
- `deploy/curis/start-local.sh`
- `frontend/next.config.js`
- `frontend/lib/auth.mjs`
- `frontend/lib/api.js`
- `frontend/app/login/page.js`
- `frontend/app/onboarding/page.js`
- `frontend/tests/mvp-p0-auth-onboarding.test.mjs`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 未认证访问任一受保护页面时不再显示 `Failed to fetch`，而是进入 `/login?next=<原页面>`。
2. 登录成功后返回安全的原访问页面；首次 Owner 激活先进入 `/onboarding`。
3. Onboarding 不新增 Workspace 模型，只显示当前个人 Workspace，并允许确认/完善预授权 Company；无 Company 时复用现有 API 创建。
4. 登录与 callback 不存在开放重定向；OAuth state/nonce/issuer/audience/exp/subject 与 membership 校验保持不变。
5. 缺少 Owner 绑定时登录页显示可执行说明，不返回 `trusted_identity_missing`。
6. 登录页在 Desktop 1280×720 和 Mobile 390×844 均无窄列、溢出或不可达操作。
7. 登录后用户可继续创建 Department、Employee、Project 和 Task。
8. 生产 JWT/trusted gateway 流程、租户隔离和伪造 Header 拒绝行为无回归。
9. 聚焦测试、Frontend lint/build、启动检查与浏览器 E2E 通过。

## Verification Status

- 实现、聚焦测试、Frontend lint/build、官方启动、未认证跳转、Desktop/Mobile 登录布局与安全检查：PASS。
- 真实 Google → Onboarding → Company → Department → Employee → Project → Task 浏览器闭环：`WAIT_FOR_OWNER_INJECTION`。
- 当前共享工作树全量后端回归：`1 failed, 1149 passed, 2 skipped`；失败来自本 Issue 范围外的 `backend/app/employee_templates.py` 现有改动。
- 独立 Review：`reviews/20260729_mvp_p0_authentication_onboarding_review.md`。
- 产品决定：Google OAuth 不再作为 Local Desktop MVP 入口；后续执行 `issues/20260729_mvp_p0_local_desktop_owner.md`。
