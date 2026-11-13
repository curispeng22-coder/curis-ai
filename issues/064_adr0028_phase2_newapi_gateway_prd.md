---
title: "Curis Admin Platform · New API 网关与官方模型目录管理 功能 PRD"
status: "DRAFT — 产品规划席产出，待主理人验收 + 总控决策席确认 G2 gate 后进入架构设计"
based_on: "ADR-0028 co-signed-with-conditions + Phase-2 PRD (issue 063)"
author: "许清楚（Xu）· 产品经理"
date: "2026-07-08"
hard_constraints: "不碰 G1/G3/G4；X-Ceo-Id 仅占位；UsageEvent 仅计量投影无金额；约束6/7(Admin 不写 Workspace 执行/不接管模型调用)；G2 仅在形状+credential_ref 外部引用，凭证持久化须 gate"
g2_gate_blocker: "网关管理 token / 上游 provider key 凭证持久化 = G2 禁止区，须 总控决策席 + 安全边界席 gate 解锁"
next_seat: "架构师（高见远）— 系统设计+任务拆解（G2 部分须 gate 后）"
---

# Curis Admin Platform · 功能 PRD：「New API 网关与官方模型目录管理」

> **文档性质**：功能 PRD（feature PRD）——聚焦本新需求，**不重写** Phase-2 整体 PRD，作为 issue 063 的**扩展切片**。
> **依据契约**：ADR-0028 Phase-1 共享基础契约（co-signed-with-conditions，2026-07-08）
> **关联文档**：Phase-2 Admin Platform MVP PRD（issue 063）
> **作者**：许清楚（Xu）· 产品经理　**日期**：2026-07-08
> **硬约束**：不碰 G1/G3/G4；X-Ceo-Id 仅占位；UsageEvent 仅计量投影无金额；约束 6/7（Admin 不写 Workspace 执行、不接管模型调用）；**G2 凭证仅定义形状 + `credential_ref` 外部引用，绝不持久化密钥**。

---

## 1. 功能目标

**一句话**：在 Phase-2 Admin Platform MVP 骨架之上，新增「官方模型网关配置（newapi 首批）+ 官方模型目录维护 + 模型启用/停用 + 按 tenant_id 查看 usage_event」四类能力，使平台运营者能安全定义模型供给侧元数据，而**全程不写 Workspace 执行路径、不接管模型调用、不持久化任何凭证**。

**定位**：本功能是 Phase-2 的**扩展切片**，不是完整平台重写；聚焦「模型网关 + 官方模型目录管理 + usage 查看增强」三件事，复用 Phase-2 既有切片（尤其 R-03/切片 C 用量投影），避免重复实现。

**目标分解（5 条）**
- **A**：平台运营者可配置并纳管官方模型网关（首批 newapi 类型），仅定义形状与 base_url，凭证以 `credential_ref` 外部引用占位（⚠️待 gate）。
- **B**：平台运营者可维护官方模型目录（`source=official`），条目可关联网关、可启用/停用，复用 `department_types` 同款 `source` 兼容范式。
- **C**：平台运营者可按 `tenant_id` 查看 Workspace 产生的 usage_event 计量投影（复用 Phase-2 R-03/切片 C），仅计量、无金额。
- **D**：明确 Admin ↔ Workspace 边界——Admin 只定义元数据、只读计量，绝不写 Workspace 执行路径、绝不接管模型调用（对应约束 6/7）。
- **E**：凡涉及密钥/凭证之处，仅以「⚠️ 待 gate 占位」呈现，绝不新建凭证存储（G2 边界清晰）。

---

## 2. 用户故事（平台运营者视角）

- **US-1**：作为平台运营者，我希望在后台配置一个 newapi 类型的官方模型网关（填名称/base_url/类型，凭证以外部引用占位），以便为后续官方模型统一纳管入口。
- **US-2**：作为平台运营者，我希望维护官方模型目录（新增官方模型、标注 `source=official`、关联网关），以便 CEO 侧 Workspace 能经只读 catalog 安装使用。
- **US-3**：作为平台运营者，我希望对官方模型做启用/停用切换（状态机），以便在不删除记录的前提下临时下线某个模型。
- **US-4**：作为平台运营者，我希望按 `tenant_id` 查看各租户的 usage_event 计量投影（调用次数/token/分钟），以便掌握平台活跃度而不接触任何费用。
- **US-5**：作为平台运营者，我希望在配置网关/模型时，凡涉及密钥/凭证之处仅显示「⚠️ 待 gate 占位」，以便清楚知道禁区边界、绝不误建凭证存储。
- **US-6**：作为平台运营者，我希望后台明确标注「Admin 只定义网关/目录元数据，模型调用由 Workspace 执行」，以便架构与审计可追溯、不越界。

---

## 3. 需求池（P0 / P1 / P2）

> 优先级：P0=本功能必须 / P1=应有 / P2=占位后续。凡落入禁止区项标注 ⚠️ G2 待 gate。

### P0（必须）

- **R-01｜官方模型网关配置（GatewayConfig）**
  Admin 经 `/api/platform/*` 写，Workspace 经 `/api/catalog/*` 只读可见其 base_url/type（不含凭证）。形状字段：

  | 字段 | 类型 | 必填 | 说明 |
  | --- | --- | --- | --- |
  | `gateway_id` | string PK | ✅ | 如 `gw_newapi_prod` |
  | `name` | string | ✅ | 展示名 |
  | `type` | enum | ✅ | 首批 `newapi`（见 R-02） |
  | `base_url` | string | ✅ | 网关基础地址（非凭证配置） |
  | `status` | enum | ✅ | `active`/`inactive` |
  | `credential_ref` | string | ❌ | **外部密钥托管引用标识**（指向 KMS/vault，不存密钥本身）⚠️ G2 待 gate |
  | `created_at` | datetime | ✅ | |

  **凭证持久化字段显式排除**：网关管理 token、上游 provider key 等任何密钥值字段 **MUST NOT persist**；如需引用，仅允许 `credential_ref`（外部引用），其背后密钥存储实现 ⚠️ G2 待 gate（见第 6 节）。
  - *验收*：`gateway_id/name/type/base_url/status/created_at` 可写可读；`credential_ref` 仅作为不透明引用字符串保存，后台/表结构**无任何密钥值列**；写入/读取路径零凭证值；`type` 取值受枚举约束。
  - *禁止区*：**`credential_ref` 背后密钥存储 + 网关管理 token 持久化 = G2 ⚠️ 待 gate（仅形状/引用，实现须 gate）**。

- **R-02｜网关类型枚举（首批 newapi）**
  `type` 枚举首个值为 `newapi`，仅定义形状，预留未来类型。
  - *验收*：`type` 枚举至少含 `newapi`；新增类型须经独立评估；本功能仅实现 newapi 的形状占位，不含 newapi 内部调用/鉴权逻辑。
  - *禁止区*：否（仅形状）。但 newapi 网关若需持久化管理 token/上游 key，落入 G2（见 R-01 / 第 6 节）。

- **R-03｜官方模型目录维护（Model Catalog，`source=official`）**
  复用并扩展 Phase-2 R-06（官方模型目录 Admin 最小录入入口，ADR-0028 §3.1/§3.2）。官方模型目录条目 additive 加 `source=official`，并新增 `gateway_ref`（→ GatewayConfig.gateway_id）、`status`（active/inactive，见 R-05）。沿用 `department_types` 同款 `source` additive 兼容 `is_system` 范式（§2.1/§6 条件#4）。
  - *验收*：后台可新增官方模型条目（`source=official` 默认）；条目可关联 `gateway_ref`；`auth_type` 仅取 `none`/`oauth`/`apikey` 形状占位，不持久化任何 key；不触发 G2；与 `department_types` 的 `source` 兼容规则一致。
  - *禁止区*：API key 真实存储/调用 = G2（显式排除真实凭证，仅形状）；上游 provider key 托管 ⚠️ G2 待 gate。

- **R-04｜usage_event 按 tenant_id 查看**
  直接复用 Phase-2 R-03 / 切片 C——`GET /api/platform/usage?tenant_id=`（admin-only）只读投影 `evolution_events` 中 UsageEvent，仅计量读数（`scope_type`/`quantity`/`unit`/`capability_ref`/`raw_meter_value`），不含金额。
  - *验收*：仅 admin token 可访问；支持 `tenant_id` 维度查询；返回纯计量无 `amount`/`currency`/`ROI`；`tenant_id` 缺失 fail-closed。
  - *禁止区*：否（金额 G1 已排除，本功能不新增计费）。*注*：本功能**不重写**该能力，直接复用 Phase-2 实现；如 Phase-2 已含则本功能零新增工作量。

- **R-05｜模型启用/停用状态机**
  官方模型目录条目采用 `status` 状态机 `active`↔`inactive`，类比 S4 `department_type_status` 启用态范式。Admin 可启用/停用，不变更历史记录。
  - *验收*：`status` 仅取 `active`/`inactive`；停用后该官方模型在 catalog 对 Workspace 不可见/不可安装（读接口按 status 过滤）；启用/停用操作写 AuditEvent（append-only，命名空间 `capability.*`）；无物理删除路径。
  - *禁止区*：否（状态机为配置型，非凭证/非计费）。

### P1（应有）

- **R-06｜边界声明：Admin 不写 Workspace 执行路径**
  以产品约束 + 架构边界双重确认——Admin Platform 仅定义网关/模型元数据（写 `/api/platform/*`、读 `/api/catalog/*`），**绝不**在 Admin 侧实现任何模型调用、网关代理、请求转发代码；模型执行调用完全由 Workspace 拥有。
  - *验收*：本功能交付物中**无任何**指向网关实际调用/模型推理的代码路径或任务拆解；PRD 明确声明 Admin 与 Workspace 的执行边界（对齐 ADR-0028 §8.3）；架构评审需确认 Admin 模块不 import Workspace 执行层。
  - *禁止区*：否（属边界约束，防止越界）。

- **R-07｜边界声明：Admin 不接管 Workspace 内部模型调用逻辑**
  Admin 不修改/接管 Workspace 的模型路由、provider 选择、fallback 等内部调用逻辑；官方网关/模型对 Workspace 仅为「可读目录供给」，Workspace 自行决定如何使用。
  - *验收*：官方模型目录对 Workspace 是只读安装关系（§8.1 条件#3），Workspace 可安装/卸载但不依赖 Admin 执行；Admin 侧不提供任何影响 Workspace 运行时调用逻辑的写接口；`marketplace` 来源显式排除（G3 ⚠️ 待 gate）。
  - *禁止区*：否（但 marketplace 跨租户共享若扩展则 G3 ⚠️ 待 gate）。

### P2（占位/后续）

- **R-08｜网关管理 token 托管机制（G2）**：仅占位——定义「网关管理 token 经 `credential_ref` 指向外部密钥托管」的形状，不实现托管/读取。⚠️ G2 待 gate。
- **R-09｜上游 provider key 托管（G2/G4）**：仅占位——newapi 上游 openai/anthropic 等 key 的托管机制形状，不实现持久化/调用。⚠️ G2 待 gate。
- **R-10｜多网关类型扩展**：预留 `type` 枚举未来值（如自有网关），本期仅 newapi；评估路线独立。

---

## 4. UI 设计稿（基于 S4 三标签页 + Phase-2 新增标签页扩展）

**承接基线**：S4 `frontend/app/platform/page.js` 3 标签页（部门类型目录 / 跨公司策略·全局护栏 / 租户总览）+ Phase-2 新增「官方能力目录 / 用量投影 / 审计轨迹」标签页。本功能**新增 2 个标签页**，并复用 Phase-2「用量投影」标签页：

- **新增标签页 G「模型网关」**（基于 R-01/R-02）：
  - 左栏：网关列表（列 `gateway_id` / `name` / `type`[newapi 徽标] / `base_url` / `status`[active·inactive 状态点] / `created_at`）；操作：启用/停用、查看。
  - 右栏「新增网关」表单：字段 `name` / `type`(枚举, 首批 newapi) / `base_url` / `status`；**`credential_ref` 仅显示「⚠️ 待 gate：密钥托管引用（KMS/vault）」占位输入框（存引用字符串，不存密钥值）**；**无任何 token/key 明文输入控件**。
  - 禁用说明条：「Admin 仅定义网关元数据，不执行模型调用」。

- **新增标签页 H「官方模型目录」**（基于 R-03/R-05）：
  - 左栏：官方模型列表（列：模型名 / `source=official` 徽标 / `gateway_ref`[关联网关名] / `auth_type`[形状] / `status`[active·inactive]）；每行带「启用/停用」开关（状态机，无删除）。
  - 右栏「新增官方模型」表单：`name` / `display_name` / `supported_models[]` / `gateway_ref`(下拉选网关) / `auth_type`(none/oauth/apikey 形状，无 key 输入) / 默认 `status=active`。
  - 提交即写 official 模型定义（source=official, is_system 语义等价），Workspace 经 `/api/catalog/models` 只读可见。

- **复用标签页 E「用量投影」**（基于 R-04，完全复用 Phase-2 R-03/切片 C）：顶部 `tenant_id` 选择器 + 聚合维度切换；中部计量表格（scope_type/quantity/unit/capability_ref/raw_meter_value）；标注「仅计量读数，不含金额」。本功能不重做。

```mermaid
flowchart TD
    A[平台管理后台 /api/platform/* + admin token] --> B[部门类型目录·沿用]
    A --> C[跨公司策略/护栏·沿用]
    A --> D[租户总览·沿用]
    A --> G[模型网关·R-01/R-02 写 gateway 元数据 + credential_ref占位]
    A --> H[官方模型目录·R-03/R-05 写 official 模型 + 启用停用]
    A --> E[用量投影·R-04 复用 Phase-2 只读 /api/platform/usage]
    A --> F[审计轨迹·沿用]
    G -. base_url/type 只读 .-> CAT[/api/catalog/* Workspace 读]
    H -. official 模型 只读 .-> CAT
    W[Workspace 执行模型调用·自有逻辑] -. 写 UsageEvent .-> E
    GW[(⚠️ G2 待gate: credential_ref 指向 KMS/vault 外部托管)]
    G -. credential_ref 仅引用 .-> GW
    style GW stroke-dasharray: 5 5
```

> 注：模型网关/官方模型目录的**执行调用完全在 Workspace 侧**，Admin 仅供给元数据（虚线表示只读供给，非调用）。`credential_ref` 指向的外部托管为 G2 待 gate，Admin 不落密钥。

---

## 5. 与 Phase-2（issue 063）的关系

明确本 PRD 与 Phase-2 MVP PRD 的边界，避免重复实现：

| 能力 | 关系 | 说明 |
| --- | --- | --- |
| usage_event 按 tenant_id 查看（R-04） | **直接复用** Phase-2 R-03 / 切片 C | 零新增；Phase-2 已实现 admin-only 计量投影，本功能仅引用，UI 复用「用量投影」标签页。 |
| 官方模型目录（R-03） | **扩展** Phase-2 R-06 | R-06 已定义官方模型 Admin 最小录入入口（§3.1）；本功能在其上 additive 加 `gateway_ref` + `status`，并强化 `source=official` 兼容范式。建议合并实现（见待确认 c）。 |
| 模型状态机（R-05） | **类比** S4 `department_type_status` | 沿用既有启用/停用状态机范式，非新机制。 |
| 网关配置（R-01/R-02） | **全新** | Phase-2 无网关概念；本功能新增 GatewayConfig 形状（newapi 首批）。 |
| 边界声明（R-06/R-07） | **强化** Phase-2 §8.1/§8.3 | 非新能力，针对本功能（网关/模型供给）显式重申 Admin 不写执行路径、不接管调用。 |
| 凭证引用（credential_ref） | **对齐** ADR-0028 §9 G2 | 与 §5 Connector 的 `config_placeholder`（仅引用非凭证）同范式；实现须 gate。 |

**避免重复**：不重写 UsageEvent 投影（R-04 复用）；不另起模型目录录入（R-03 扩展 R-06）；状态机复用 `department_type_status` 范式（R-05）。唯一净新增为 GatewayConfig（R-01/R-02）。

---

## 6. G2 gate 待解锁清单（关键专节）

本功能落入「外部连接器与凭证」禁止区（ADR-0028 §9 G2）的部分，统一标注「仅定义形状/引用，实现须经 **总控决策席 + 安全边界席 gate** 解锁；本 PRD 不定义其实现逻辑」：

| # | G2 项 | 本 PRD 已定义 | 被锁定实现（须 gate） | 建议 gate 路径 |
| --- | --- | --- | --- | --- |
| G2-1 | 网关管理 token 持久化 | ✅ `credential_ref`（外部引用标识，不存 token 值） | ❌ 网关管理 token 真实存储、Admin 用其调用 newapi | 独立 ADR（网关凭证保管）+ 安全边界席评审 + KMS/密钥托管方案评估 |
| G2-2 | 上游 provider key 托管机制 | ✅ `credential_ref` 形状占位、`auth_type` 仅形状 | ❌ openai/anthropic 等上游 key 持久化与真实调用 | 同 G2 gate；与 §3.2/§5 G4 合并评估 |
| G2-3 | `credential_ref` 背后密钥存储实现 | ✅ 仅「引用标识符」概念（指向 KMS/vault） | ❌ 密钥实际存储/读取/轮换/审计实现 | KMS/密钥托管方案专项评估（不沿用 tenants 无凭证列之外的任何持久化） |

**统一声明**：凡 G2-1~G2-3，本 PRD **只定义数据形状与外部引用**，绝不设计任何密钥值字段或存储逻辑；实现前须提交独立 ADR，经总控决策席 + 安全边界席双签 gate 解锁。本期可交付部分仅限「形状 + `credential_ref` 引用占位」。

---

## 7. 待确认问题

- **(a) `credential_ref` 背后的密钥托管机制选型**（须 gate）：采用 KMS（如云厂商 KMS）、独立 vault（如 HashiCorp Vault），还是临时 env 注入？该选型决定 `credential_ref` 的引用格式与解析协议，且属 G2，须 gate 后定。
- **(b) 网关管理 token 是否本期必须**：若本期仅通过 `base_url` + 手动运维（人工在 newapi 侧配置）即可满足，则可暂不引入 `credential_ref`，降低 G2 暴露面；若必须 Admin 自动纳管网关，则 `credential_ref` 为必填，G2 gate 须同步启动。
- **(c) 模型目录与 Phase-2 R-06 是否合并实现**：建议将本功能 R-03 与 Phase-2 R-06 合并为同一「官方模型目录」录入能力（additive 加 `gateway_ref`+`status`），避免两套模型录入入口；需确认 Phase-2 切片是否同步调整。
- **(d)（补充）网关 `type` 枚举未来扩展**：除 newapi 外是否预留 other 类型、是否在本功能预留枚举位，还是严格仅 newapi。

---

### 契约对齐声明
本功能 PRD 全部锚定 ADR-0028（§3 模型契约仅形状、§8.1 catalog 读 ≠ platform 写、§8.3 Admin 边界、§9 G2 禁止区）；`credential_ref` 仅外部引用、无任何凭证持久化；UsageEvent 仅计量投影无金额（G1 不触及）；不引入 marketplace（G3）/ 私有能力自带凭证（G4）；X-Ceo-Id 仅占位；约束 6/7（不写 Workspace 执行、不接管模型调用）以 R-06/R-07 显式落地。
