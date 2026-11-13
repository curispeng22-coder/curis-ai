# MVP P0 — Local Desktop Owner

Status: CLOSED — PASS（Issue Scope）

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_p0_local_desktop_owner_review.md`

## Objective

将 Curis MVP 认证入口收敛为 Local Desktop 单用户流程：

`启动 Curis → 创建本地 Owner → 生成 HttpOnly Session → Onboarding → Workspace → Company → Employee → Project`

## Product And Security Boundary

- MVP 默认启动不依赖 Google OAuth、外部网络或外部凭据。
- 保留现有 Google OAuth/JWT 扩展代码与生产 trusted gateway 边界，但不作为 Local Desktop 入口。
- 不新增 Workspace/Admin 体系，不修改 Curis v1.0 业务架构。
- 本地 Owner 只在 local/development Workspace 且经 loopback Gateway 时启用。
- Session 使用既有随机、HttpOnly、SameSite Cookie；前端不保存身份令牌。
- 未认证受保护请求继续统一跳转登录页并保存安全原路径。

## Tasks

- T037：增加 Local Owner 状态、首次初始化、重新进入与退出接口。
- T038：官方本地启动链默认启用 Local Owner、禁用 Google OAuth。
- T039：登录页改为创建/进入 Local Owner，不再要求 OAuth 凭据。
- T040：首次 Owner Session 进入 Onboarding，并复用现有 Workspace/Company。
- T041：验证新库启动后的 Owner → Company → Employee → Project 链路。

## Allowed Files

- `issues/20260729_mvp_p0_authentication_onboarding.md`
- `issues/20260729_mvp_p0_local_desktop_owner.md`
- `reviews/20260729_mvp_p0_local_desktop_owner_review.md`
- `backend/app/local_google_oidc.py`
- `backend/tests/test_local_owner_auth.py`
- `deploy/curis/start-local.sh`
- `deploy/curis/gateway/docker-compose.yml`
- `deploy/curis/gateway/envoy.yaml.template`
- `frontend/app/login/page.js`
- `frontend/app/onboarding/page.js`
- `frontend/app/projects/[project_id]/page.js`
- `frontend/tests/mvp-p0-auth-onboarding.test.mjs`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 新库首次启动后，未认证用户进入 Local Owner 初始化页。
2. 创建 Owner 后签发 HttpOnly Session，并进入 Onboarding。
3. 再次启动时不重复创建 Owner，可直接生成新的本地 Session。
4. 未认证访问受保护页面不显示 `Failed to fetch`，并保存安全原路径。
5. Onboarding 完成后可创建或完善 Company，并继续创建 Employee、Project。
6. 默认本地启动不需要 Google OAuth Client ID、Secret 或网络。
7. 现有 OAuth/JWT 扩展入口、生产 trusted gateway 与租户隔离保持可用且 fail-closed。
8. Backend 聚焦测试、Frontend test/lint/build、官方启动与真实浏览器主路径通过。

## Verification

- Backend Local Owner、Google OIDC、trusted identity：`33 passed`。
- Frontend Authentication：`4 passed`；lint/build PASS。
- 官方启动、401 原路径、首次 Owner、HttpOnly Session、Onboarding、Company、Employee、Project 与重启后新 Session：真实浏览器 PASS。
- 安全边界：PASS；生产 JWT/trusted gateway 与未来 Google OAuth 扩展保持 fail-closed。
- Review：`reviews/20260729_mvp_p0_local_desktop_owner_review.md`。
- Workspace 全量回归：`1 failed, 1153 passed, 2 skipped`；唯一失败来自本 Issue 范围外的 `backend/app/employee_templates.py` 现有改动，不阻塞本 Issue 接受，但继续阻塞 Workspace 整体 Gate。
