# Curis · Channel × Channel Account 矩阵模型

> **状态**：CONTENT GROWTH ARCHITECTURE DELTAS APPLIED（DELTA 1/2/3 已应用）
> **类型**：Reference Only · 关系与数据模型草案（非权威、非最终）
> **配套**：`Curis_Content_Growth_Operating_Model.md`（A/C/D 节）、`Curis_Organization_Routing_Architecture.md`、`Curis_Content_Growth_Company_Evolution_Model.md`

本文定义 **Channel / Channel Account / Office / Account Pool / Target Account** 的关系模型、字段与矩阵示例。**不预设最终结构正确** —— 末尾列开放问题。

---

## 1. 三层关系总览

```
Company
├ Business / Operating Context
│   └─ Office ×M（业务经营单元：目标/定位/受众/策略/Knowledge/Growth Context）
│         └─ Account Pool（该 Office 的 Channel Account 绑定集合，1..N）
│               └─ OfficeAccountBinding（Office ↔ Channel Account 关系，非严格 ownership）
│                     └─ Channel Account ×N ─（FK→Channel）平台上的实际经营账号
└ Organization（与 Office 正交）
    ├ Department
    ├ Team
    ├ Role
    └ Employee（经 Responsibility Assignment 服务 N 个 Office）

Content Intent（跨 Office/Account 共享的「一次推理」）
  └─ Target Accounts（从相关 Office 的 Account Pool 选子集）
        └─ Account-aware Production → Content Variant ×K（每 Account 可多份）
              └─ Publication ×M（每次发布一份）
                    ├─ Engagement（per-Account 真相源）
                    └─ Analytics（per-Account 真相源）
```

**关键分界**：
- `Company / Business·Operating Context / Office / Account Pool` → **经营层**（谁在经营、为谁、讲什么）
- `Organization（Department/Team/Role/Employee）` → **组织结构层**（与 Office 正交；谁在结构里、如何指派）
- `Channel` → **平台事实层**（平台允许/要求什么）
- `Channel Account` → **账号经营层**（这个号做什么/什么风格）
- `Content Intent / Variant / Publication / Engagement / Analytics` → **内容/运行层**

> **DELTA 1**：Office 与 Organization 是 Company 下**两轴正交**——Office 表达经营（为谁），Organization 表达结构（谁在）。Employee 经 Responsibility Assignment 服务 Office，**不隶属于 Office**。

---

## 2. Channel（平台本身）

| 字段 | 说明 |
|---|---|
| `id` | 平台标识：`DOUYIN` / `XHS` / `TIKTOK` / `BILIBILI` / `YOUTUBE` |
| `capabilities` | 平台能力集（发布/评论/私信/数据/Webhook…），见 Douyin Research |
| `policy_context` | 平台政策事实（AI disclosure 字典、审核规则、自动化边界） |
| `constraints` | 平台硬约束（ratio/duration/resolution/copyright/scheduling 支持度） |

> Channel **不含任何用户账号信息**。它只回答「这个平台能做什么、要求什么」。`Curis_Multi_Channel_Architecture_Review.md` §G 的平台差异矩阵即 Channel 层的知识来源。

---

## 3. Channel Account（用户实际经营账号）

**归属关系（DELTA 1）**：Channel Account 与 Office 是 **OfficeAccountBinding / Account Pool 关系**，非严格 ownership。首版推荐：一个 Channel Account 通常属于**一个** Office 的 Account Pool（因其 `positioning` 与 Office 定位一致）；但数据模型以 **binding** 实现，结构上支持未来 **N:N**（如联名号 / 跨 Office 共享账号）。一个 Channel 上可存在多个不同 Channel Accounts。

| 字段 | 说明 |
|---|---|
| `id` | |
| `channel` | 所属平台（FK → Channel） |
| `account_bindings[]` | OfficeAccountBinding 列表（office_id, role, binding_state）；首版通常单绑定，结构上支持 N:N |
| `identity` | 账号身份（昵称/Handle/平台 UID） |
| `positioning` | 账号定位（角色：品牌号/产品号/IP号/区域号/员工号…） |
| `niche_pillars[]` | 内容支柱 / 垂直领域 |
| `audience` | 受众定义（人群/场景/转化路径） |
| `tone_style` | 语气 / 视觉风格 |
| `language` | 语言（zh-CN / en…） |
| `format_preference` | 形态偏好（口播/图文/教程/竖屏/横屏） |
| `publishing_rhythm` | 发布节奏（频次/时段） |
| `growth_goals` | 增长目标（涨粉/线索/转化/完播…） |
| `historical_performance` | 历史表现（指标基线，供 Target 推荐与反馈） |
| `authorization_state` | 授权状态（OAuth/企业号/经营号/Scope/白名单） |
| `connected_capabilities[]` | 已连接能力（Connector/Skill/Tool 引用） |
| `platform_policy_context` | 该账号适用的政策细则（如企业号 IM 权限） |
| `brand_knowledge_refs[]` | 引用的 Brand / Knowledge |

> **Channel Account 决定「这个账号应该做什么 / 用什么风格经营」**。同一 Channel 上两个 Account 的 `positioning/audience/tone_style` 可完全不同（如 Douyin AI科普号 vs 个人IP号）。

---

## 4. Office（业务经营单元）

| 字段 | 说明 |
|---|---|
| `id` | |
| `company_id` | 所属 Company |
| `name` | 经营单元名（如「AI工具内容」） |
| `business_goals` | 共享经营目标 |
| `positioning` | 统一定位（前端分散、后端承接统一） |
| `audience` | 共享受众定义 |
| `content_strategy` | 内容策略 / pillars |
| `knowledge_refs[]` | 专属 Knowledge / Brand / Evidence |
| `growth_context` | 增长上下文（历史复盘、反馈沉淀） |
| `account_pool[]` | 绑定的 Channel Account 集合（FK 列表） |
| `default_target_account_set[]` | 默认 Target Account 子集（常规发布目标） |

> Office **拥有 Account Pool**，但**不拥有 Production 工具 / Channel Connector**（那些是 Capability Provider，由运行层调用）。Office 是「经营意图」的容器，不是「能力」的容器。

---

## 5. Target Account（Distribution Targets，前置）

**不是 Platform，是 Account。**

| 字段 | 说明 |
|---|---|
| `content_intent_id` | 来源 Intent |
| `selected_accounts[]` | 从相关 Office 的 Account Pool 选出的**本次实际目标账号子集** |
| `selection_basis` | `DEFAULT_SET` / `AI_RECOMMENDED` / `MANUAL` |
| `production_requirements` | 由 selected_accounts 推导的 Account-aware Production Requirements（ratio 并集、时长下限、copyright 占位、disclosure 字典、publishAt 占位等） |

**规则**：
- `selected_accounts` ⊆ 相关 Office 的 `account_pool`（不能选 Office 不拥有的账号）。
- 绑定 N 账号 ≠ 每条内容群发 N 账号（见 §6 示例）。
- `default_target_account_set` 由 Office 记忆；AI 据内容与历史推荐，用户**不必每条勾选**。

---

## 6. 矩阵示例（采用本轮候选）

```
Company：Curis
├ Office A：个人 IP
│   account_pool: [ Douyin·个人IP号 ]
│
├ Office B：AI工具内容
│   account_pool: [ Douyin·AI工具号, XHS·AI工具号, Bilibili·AI教程号, TikTok·AI Tools ]
│   default_target: [ Douyin, XHS, Bilibili ]   （TikTok 按需）
│
└ Office C：生活方式
    account_pool: [ Douyin·生活号, XHS·生活号 ]
    default_target: [ Douyin, XHS ]

Content #101（Office B, AI工具教程）
  selected_accounts: [ Douyin·AI工具号, XHS·AI工具号, Bilibili·AI教程号 ]
  TikTok ✕（本次不发）
  → 3 个 Content Variant（HIGH REUSE：同母版改 caption/cover/metadata）

Content #102（Office B, AI工具海外向）
  selected_accounts: [ Douyin·AI工具号, TikTok·AI Tools ]
  XHS ✕ / Bilibili ✕
  → FULL DIVERGENCE：Douyin 中文口播 + TikTok 英文短视频

Content #201（Office A, 个人IP观点）
  selected_accounts: [ Douyin·个人IP号 ]
  → 1 个 Content Variant（60秒个人观点）
```

**印证**：抖音矩阵「一次拍摄多次拆解」= HIGH REUSE；「图文转视频/视频转图文、和而不同」= DIVERGENCE；各账号「指标分开复盘」= Engagement/Analytics per-Account。

---

## 7. 与组织层 / 运行层的衔接

- **Office 在组织层**：Company → Office（部门/业务线级）→ Employee/Team。
- **Account Pool 与 Employee 解耦**：Employee（如字幕员工）跨 Office 服务，不复制；由 Org Router 按 Account Context 分配（见 Org Routing 文档）。
- **Channel Account 是运行层 Content Growth 闭环的「发布终点」**：Target Accounts → Production → Variant → Publication（per Account）。

---

## 8. 开放问题（留设计期）

1. **（DELTA 1 已定）一个 Channel Account 能否属于两个 Office？** 首版推荐 **1 Account : 1 Office**（因其 `positioning` 与单一 Office 定位一致），但数据模型以 `OfficeAccountBinding` 实现，**结构上支持未来 N:N**（联名号 / 共享账号场景）。不预设「永远只能属于一个 Office」。（见 §3）
2. Office 的 `account_pool` 跨 Company 复用（多品牌共用某账号）是否允许？
3. `default_target_account_set` 与 AI 推荐的冲突如何处理（用户否决 AI 推荐？）？
4. Channel Account 的 `historical_performance` 由谁写入（Analytics 回流 / 手动）？
5. 账号解绑 / 重新授权时，其下 Publication/Engagement/Analytics 历史是否保留？
6. `authorization_state` 失效（OAuth 过期 / Scope 撤销）时，运行层如何降级（暂停该 Account 的发布）？

---

## DELTA 1 应用记录（本轮批准）

- **Office 与 Organization 正交**：取消 `Company → Office → Employee/Team`；改为 Company 下 `Business/Operating Context → Office` 与 `Organization → (Department/Team/Role/Employee)` 两轴正交（见 §1、§7）。
- **Channel Account ownership → binding**：`office_id` 严格归属改为 `OfficeAccountBinding` / Account Pool 关系，首版 1:1 推荐、结构支持 N:N（见 §3、§8）。
- DELTA 2/3 主要涉及组织路由与 Capacity，见 Doc 3 / Doc 1 §L。

---

*数据模型草案，未固化。字段集将在 Office / Intent / Org Routing Contract 设计中最终裁定。*
