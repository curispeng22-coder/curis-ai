# ADR-0028 Phase-1 Shared Contract Handoff

| Field | Value |
| --- | --- |
| Commit | `cf4c6296` |
| Status | co-signed-with-conditions |
| Audience | Curis Workspace 团队（Next Seat: Workspace 系统交付席） |
| Date | 2026-07-08 |

## Accepted Contract
- `official` / `tenant_private` / `marketplace` — 三态能力来源模型，已定义
- `/api/catalog/*` — Workspace 侧**只读**官方能力目录通道
- `/api/platform/*` — Admin Platform 侧**写/管理**通道（非替代分工）
- UsageEvent **必须由 Workspace 写入**（tenant_id + ceo_id 打标、幂等去重）
- `X-Ceo-Id` 仅为 Phase-1 **占位**，非正式 CEO 鉴权

## Workspace Must Implement
- 读取官方 catalog（`GET /api/catalog/*`，`source=official`）
- 保留 `tenant_private` 扩展能力（本租户内可见可用）
- 写入 UsageEvent（带 `tenant_id` / `ceo_id`，缺省 fail-closed 拒绝）
- 强制 `tenant_private` 命名空间（复合唯一键 `(tenant_id, name)`，不与 official 冲突）

## Forbidden
- 计费计算（BillingEvent 仅落形状，金额/ROI 计算 ⚠️ 待 gate）
- 连接器凭证（OAuth/APIKey 持久化与真实调用 ⚠️ 待 gate）
- marketplace 实现（跨租户共享/安装/分成 ⚠️ 待 gate）
- 私有 model/tool 凭证持久化（自带 key/endpoint ⚠️ 待 gate）
- CEO auth 实现（`X-Ceo-Id` 仅占位，正式机制单独立 ADR）

## Open Risks
- UsageEvent 写入点（执行落库路径的接入位置与重试幂等）
- `tenant_private` 唯一键（命名空间前缀约束与冲突检测）
- `source` ↔ `is_system` 兼容性（additive 列，DDL 向后兼容）

## Next Seat
- **Workspace 系统交付席**（原 Curis Workspace 团队）
