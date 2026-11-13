# Issue 070 · ADR-0028 Phase-2 官方能力目录（合并 R-03 模型目录 + R-06 能力目录）增量 PRD

> **起草说明**：本 PRD 由主理人齐活林代拟。原因：产品经理代理（许清楚 / `software-product-manager`）在本会话连续 2 次 spawn 均 0 秒报 `Task agent ... is not available`，不可用；经总控决策席授权（2026-07-08），由主理人代拟以保证 Phase-2 进度。后续架构设计 / 实现 / 验证仍由对应成员（高见远 / 寇豆码 / 严过关）执行，主理人仅做编排与汇编。

## 1. 产品目标

将 Admin Platform 的「官方能力目录」统一为**单一管理面**，覆盖三类官方能力：**模型(model) / 工具(tool) / 连接器(connector)**，支撑：

- Admin 在一个界面内维护全部官方能力（录入、启用/停用、关联网关）；
- Workspace 经 `/api/catalog/*` **只读**消费（不含任何凭证/引用串），用于其执行时的能力发现与编排；
- 全程**零凭证落地**、Admin **不参与** Workspace 执行、不调用任何上游。

## 2. 用户故事

- 作为**平台管理员**，我希望在一个「官方能力目录」页里按类型查看 / 新增 / 启停 model / tool / connector，而不必在「模型目录」和「能力目录」两个入口间切换。
- 作为 **Workspace（CEO 的 AI 公司系统）**，我希望通过只读 catalog 接口发现官方提供的 model / tool / connector 及其启用状态，用于任务编排，且**不接触任何凭证**。

## 3. 需求池（标注「已实现 issue 065」/「本期新增」）

### P0
- [已实现 issue 065] 模型网关配置（`model_gateways` 表，gateway_type 严格仅 `newapi`，`credential_ref` 仅 `scheme:reference` 占位，DB 零密钥列）
- [已实现 issue 065] 官方模型目录写路径（`official_models` 表 + `save/get/list/set_status` + `gateway_ref` 存在性校验（缺失→422）+ `source=official` 兼容范式）
- [已实现 issue 065] Admin 写 API：`GET/POST /api/platform/models`、`PUT /api/platform/models/{key}`(enable|disable)；只读 `GET /api/catalog/models`（不含 `credential_ref`）；`/api/platform/gateways`、`/api/catalog/gateways`、`/api/platform/usage`（复用）
- [本期新增] **统一官方能力目录数据模型**：`type` enum(`model|tool|connector`)，共享列（`capability_key` PK / `name` / `provider_id` / `display_name` / `source` 固定 `official`（additive 兼容 `is_system`）/ `gateway_ref`（仅 model 关联 newapi 网关，可空）/ `auth_type` 仅形状(`none|oauth|apikey`，**不存真实凭证**）/ `status` enum(`active|inactive`) / `created_at` / `updated_at`）；**明确零密钥值列**
- [本期新增] 官方能力目录 Admin 写 API：`GET/POST /api/platform/capabilities`、`PUT /api/platform/capabilities/{key}`(enable|disable)
- [本期新增] 官方能力目录只读 API：`GET /api/catalog/capabilities`（Workspace 只读投影，**排除任何凭证/引用列**）
- [本期新增] 前端「官方能力目录」**统一标签页**（替代现「官方模型目录」页），按 `type` 分组展示 model/tool/connector，统一新增 / 启用停用交互

### P1
- [本期新增] tool / connector 条目录入（`auth_type` 仅形状；connector 可关联外部系统但**不存凭证**）
- [已实现 issue 065] `status` 状态机 + `capability.*` 审计（扩展至 tool / connector）

### P2
- [本期新增] 目录条目搜索 / 分页（如数据量大时）
- 目录与网关关联的视觉校验提示

## 4. UI 设计稿（官方能力目录标签页）

```
┌─────────────────────────────────────────────────────────────┐
│  官方能力目录                          [+ 新增能力]           │
│  ┌─────────┬─────────┬─────────┐ 禁用说明条：               │
│  │ 模型    │ 工具    │ 连接器  │ Admin 仅定义能力元数据，    │
│  └─────────┴─────────┴─────────┘ 不执行模型/工具/连接器调用 │
│  列表：                                                   │
│  ┌────────┬──────┬──────────┬──────────┬────────┬──────┐  │
│  │ 名称   │ type │ 关联网关 │ auth_type│ 状态   │ 操作 │  │
│  ├────────┼──────┼──────────┼──────────┼────────┼──────┤  │
│  │ gpt-4  │ model│ newapi   │ apikey   │ [启用] │ 编辑 │  │
│  │ web_search│tool│ —       │ none     │ [启用] │ 编辑 │  │
│  │ slack  │ conn │ —        │ oauth    │ [停用] │ 编辑 │  │
│  └────────┴──────┴──────────┴──────────┴────────┴──────┘  │
│  新增抽屉/表单：                                            │
│   type(下拉) name provider_id display_name                  │
│   gateway_ref(仅 model 显示, 下拉自 /api/platform/gateways) │
│   auth_type(none|oauth|apikey 仅形状) status(默认 active)  │
└─────────────────────────────────────────────────────────────┘
```
- 复用既有 `apiFetch` + Bearer token 范式；**不引入 MUI / 状态库**。
- `credential_ref` 仅在「模型网关」标签页出现，且仅占位输入框（不在此页）。

## 5. 待确认问题（交 总控 / 原 Workspace 团队）

1. tool / connector 的 `auth_type` 形状是否需更多枚举（如 `oauth2`/`bearer`）？本期建议保持 `none|oauth|apikey` 仅形状。
2. **统一目录存储策略**（由架构师在设计中定，须向后兼容既有 `/api/catalog/models` 消费）：
   - 方案 A：新增 `official_capabilities` 表（`type` 列），将 `official_models` 现有模型作为 `type='model'` 初始数据迁移；或
   - 方案 B：additive 扩展 `official_models` 加 `type` 列（model 默认 `'model'`）。
3. R-06 与 issue 063 中其他 Phase-2 切片（tenants 扩展 / UsageEvent 投影 / AuditEvent 投影）的优先级——**本期只做统一能力目录**。
4. capability 与 model 是否共用同一审计事件类型（`capability.*`）？建议共用。

## 6. 已排除 / 待 gate

- **排除（硬性）**：G1 金额/ROI（usage 纯计量）；G2 真实密钥托管（`credential_ref` 仅占位、DB 零密钥列、绝不出站/解析）；G3 marketplace 跨租户共享；G4 私有能力自带凭证；X-Ceo-Id 正式 auth；Admin 执行/代理调用上游。
- **待 gate**：`credential_ref` 真实密钥托管机制（KMS / vault / env）单列 gate，须 **总控决策席 + 安全边界席** review 后才做，不在本期。

## 7. 边界与依赖

- 复用 issue 065 已验证范式：`source=official` additive 兼容 `is_system`、`gateway_ref` 存在性校验、`status` 状态机、`capability.*` 审计、`catalog` 只读投影、`Admin 写 /api/platform/*` 且 `catalog 读 ≠ platform 写`。
- 依赖：
  - `model_gateways`（issue 065 已建，newapi 首批）
  - `official_models`（issue 065 已建，本期按 §5.2 扩展或迁移为统一目录）
- 与 ADR-0028 契约严格对齐（§2.1 / §6 source 兼容；§8.1 catalog 读≠platform 写；§9 G2 禁止区）。
