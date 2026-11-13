# Sprint 0 Architecture Convergence Review

Status: PASS

Issue: `issues/20260729_sprint0_architecture_convergence.md`

Date: 2026-07-29

## Result

- 唯一前端源码、构建、CI 与本地运行入口已收敛到 `frontend/`。
- 旧 Workspace 的 Google 登录与 Project Runtime 路由已原样迁入 `frontend/`；旧 Admin 路由此前已存在于 `frontend/app/platform/`。
- `frontend-admin/`、`frontend-workspace/` 源码已删除；未跟踪的 `.next` / `node_modules` 已移到 macOS 废纸篓，可恢复。
- 默认运行数据库固定为宿主 `data/curis.sqlite` / 容器 `/srv/curis/data/curis.sqlite`。
- 旧 `admin.sqlite`、`workspace.sqlite` 与备份库未自动合并或删除，避免数据损失；后续由独立数据迁移 Task 处理。
- 默认启动链不启动 Admin 后端、FreeLLMAPI 或 selfuse；D1 为 `FROZEN=1`、`EXECUTE_ENABLED=0`。

## Evidence

| Check | Result |
| --- | --- |
| `pnpm --dir frontend lint` | PASS |
| `pnpm --dir frontend build` | PASS，26 个静态页面生成；`/login`、`/projects/[project_id]` 均进入构建路由 |
| Project Runtime view-model | 7 passed |
| Workspace identity + local Google OIDC | 21 passed |
| Gateway Compose config | PASS |
| Shell syntax + legacy/experimental reference scan | PASS |
| `git diff --check` | PASS |
| 唯一启动命令 | PASS；Frontend 3001、Gateway 8080 均 HTTP 200 |
| 容器运行配置 | `CURIS_DB=/srv/curis/data/curis.sqlite`，D1 双保险禁用 |
| Browser | `/` 收敛到 `/ceo-office`；真实登录页与 Project Runtime 未登录错误态可达 |

## Notes

- 首次启动发现根路径返回 307，旧健康检查只接受 200；检查地址已改为 `/ceo-office`。
- 首次容器启动遇到遗留 JWKS 容器名冲突，现有错误清理流程已清除，重跑通过。
- 浏览器未执行 Google 外部登录或凭据注入；这不属于 Sprint 0。
- 主前端 lint 原先误扫只读 `frontend/ceo-evidence/` 子应用，已改为全局忽略该独立证据目录。

## Change Summary

- 删除两套旧前端和重复锁文件。
- 迁入两条仍有真实用户价值的旧 Workspace 路由。
- 将 CI、发布脚本、本地启动脚本改为单前端。
- 固定主数据库路径并对实验能力 fail-closed。
- 更新运行说明、发布检查清单与接管状态。
