# ADR-0036: Workspace And Admin Boundary

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-07-30

Module: Workspace / Admin

## Decision

当前 Curis 不运行第二套独立 Workspace/Admin 产品体系。

当前方案：

- 唯一前端为 `frontend/`
- Workspace 是 Owner 的日常产品入口
- Platform/Admin 能力保持权限边界，但不以第二套默认前端和数据库运行
- 当前主数据库为 `data/curis.sqlite`

未来拆分方向：

- 只有在商业多租户、平台运营、独立部署和安全边界明确后才评估物理拆分
- 拆分必须先定义身份、Tenant、API、数据所有权、部署、审计和迁移契约
- 未来拆分不得重新引入两套不一致产品事实

## Reason

- 历史独立 Admin/Workspace 造成重复前端、数据库和文档事实
- 当前阶段优先完成 Owner 产品闭环
- 逻辑权限边界不要求立即物理拆分

## Consequences

- `frontend-admin/` 和 `frontend-workspace/` 是废弃运行方向
- 旧拆分文档保留为历史资料
- 新 Admin 功能不能在没有独立 Issue 和安全契约时进入默认产品
- 未来拆分是规划方向，不是当前已完成能力
