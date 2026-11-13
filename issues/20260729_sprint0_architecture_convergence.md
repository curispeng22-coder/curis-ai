# Sprint 0 — 项目架构收敛

Status: APPROVED — USER_DIRECTED

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_sprint0_architecture_convergence_review.md`

## Objective

在不重写产品、不改变 Curis v1.0 架构、不新建 Workspace/Admin 体系的前提下，完成迁移 M0：

1. `frontend/` 成为唯一前端源码、构建和本地运行入口。
2. 旧 `frontend-admin/`、`frontend-workspace/` 在确认有效路由已收敛后删除。
3. `data/curis.sqlite` 成为唯一默认运行数据库；旧库只保留为迁移证据，不自动合并或删除用户数据。
4. FreeLLMAPI、D1、selfuse 等实验能力不进入默认启动链；D1 默认 fail-closed。
5. 唯一启动命令可稳定拉起 Workspace 前端、可信网关与后端。

## Tasks

- T-S0-01：核对并收敛前端入口、CI、发布脚本。
- T-S0-02：固定数据库默认路径并保留旧库只读边界。
- T-S0-03：建立实验能力禁用清单，确认默认启动链不引用实验服务。
- T-S0-04：运行 focused 测试、前端 lint/build、启动与浏览器验证，记录 Review。
- T-S0-05：更新当前状态并提交代码、测试结果和变更说明。

## Constraints

- 不新增依赖、ORM、Router、Workspace 或 Admin 服务。
- 不修改产品页面、产品信息架构或 Curis v1.0 核心对象。
- 不改写或合并 SQLite 业务数据；旧库删除留到独立数据迁移 Task。
- 保留可信网关、OIDC、租户隔离与脱敏边界。
- 现有未提交改动不得混入 Sprint 0 提交。

## Allowed Files

- `issues/20260729_sprint0_architecture_convergence.md`
- `reviews/20260729_sprint0_architecture_convergence_review.md`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `README.md`
- `.github/workflows/curis-isolation.yml`
- `frontend/eslint.config.mjs`
- `frontend/app/login/**`（旧 Workspace 真实登录路由迁入）
- `frontend/app/projects/[project_id]/**`（旧 Workspace 真实项目运行路由迁入）
- `frontend-admin/**`（删除）
- `frontend-workspace/**`（删除）
- `deploy/curis/start-local.sh`
- `deploy/curis/stop-local.sh`
- `deploy/curis/build-release.sh`
- `deploy/curis/README.md`
- `deploy/curis/release-checklist.md`
- `deploy/curis/workspace.env.example`
- `deploy/curis/gateway/docker-compose.yml`
- `experimental/README.md`

## Acceptance

1. 仓库运行、CI、发布脚本只引用 `frontend/`。
2. `frontend-admin/`、`frontend-workspace/` 不再是源码目录，且其唯一业务路由在 `frontend/` 有对应入口或明确延期。
3. 默认 Workspace 数据库为 `/srv/curis/data/curis.sqlite`，宿主映射到 `data/curis.sqlite`。
4. 默认启动不拉起 Admin 后端、FreeLLMAPI、selfuse；D1 显式冻结且禁止真实执行。
5. `frontend` lint/build、后端 focused 测试、配置检查、`git diff --check` 通过。
6. 浏览器可从唯一前端入口进入真实 Workspace；若本地环境阻塞，Review 记录精确阻塞。

## Verification

```bash
pnpm --dir frontend lint
pnpm --dir frontend build
(cd 'frontend/app/projects/[project_id]' && node --test projectRuntimeViewModel.test.mjs)
.venv/bin/python -m pytest -q backend/tests/test_workspace_identity_membership.py backend/tests/test_local_google_oidc.py
docker-compose -f deploy/curis/gateway/docker-compose.yml config
rg -n 'frontend-admin|frontend-workspace' .github deploy/curis --glob '!releases/**'
rg -n 'freellmapi|start-selfuse|CURIS_D1_EXECUTE_ENABLED=1' deploy/curis
git diff --check
```

Browser hard gate: yes.
