# Workspace R1 统一运行基线 Review

日期：2026-07-17  
验证席：质量运行席  
Issue：`issues/20260717_workspace_r1_unified_runtime_baseline.md`

## 结论

**PASS。** 固定分支、固定提交上的启动、停止、端口、双数据库、Admin 弱令牌边界、聚焦测试、全量回归和两个前端构建均已独立复核。R1 可交产品规划席验收；本 Review 不授权进入 R2。

## 固定基线

- 分支：`feat/roadmap-r1r2`
- Commit：`306b9a1182d2a8a510154cdb6883009459e70728`
- 启动：`./deploy/curis/start-local.sh`
- 停止：`./deploy/curis/stop-local.sh`
- 重复启动：exit 1，明确报告 `端口 3000 已占用`。
- `git diff --check`：通过。

## 运行证据

| 组件 | 地址 | 结果 |
|---|---|---:|
| Admin Backend | `127.0.0.1:8001/health` | 200 |
| Workspace Gateway | `127.0.0.1:8080/health` | 200 |
| Admin Frontend | `127.0.0.1:3100/platform` | 200 |
| Workspace Frontend | `127.0.0.1:3000/` | 200 |
| Workspace App 原始端口 | 宿主 `127.0.0.1:8002` | 不可达 |
| Admin 无令牌 | `8001/api/platform/tenants` | 401 |

- Admin DB：`data/admin.sqlite`，inode `19047968`。
- Workspace DB：`deploy/curis/gateway/.generated/data/quality.sqlite`，inode `20044611`。
- 两个数据库路径和 inode 均不同。
- `stop-local.sh` 后 3000、3100、8001、8002、8080 均关闭；再次执行 `start-local.sh` 后四个公开入口均恢复 200。
- `curis-new-api` 因 3000 端口冲突保持停止；R1 使用 Workspace Frontend 占用 3000。

## 测试与构建

- 聚焦测试：`test_admin_token_policy.py + test_workspace_identity_membership.py`，**10 passed**。
- 全量后端：**599 passed / 19 failed / 0 skipped**，50.71s。
- 19 项与前一固定分支质量基线一致，没有 R1 新增失败；仍为 Admin token 旧测试、tenant `default/selfuse` 旧断言、Department/Platform 旧失败、vector/前端标签检查和 Docker Compose 插件环境失败。
- `frontend-admin`：`pnpm build` 通过。
- `frontend-workspace`：`pnpm build` 通过。
- Admin 边界：未配置令牌返回 401；错误令牌返回 401；`ADMIN_STRICT=true` 且无令牌时拒绝启动；聚焦测试通过。

## 最终状态

R1：**PASS**。  
R2：**未授权，保持未开始**。

Handoff: sent to 产品规划席
