# Curis · Channel / Channel Account / Account Pool Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch A — Operating Foundation，未 Frozen）
> **类型**：Content Growth Domain（执行经 Capability·Connector）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 2）、上一轮 `Curis_Channel_Account_Matrix_Model.md`（DELTA 1 已落地）、抖音官方能力研究（重归类为 Douyin Channel Capabilities）
> **FROZEN 指针（2026-08-16）**：② Channel / Channel Account / OfficeAccountBinding / Account Pool 语义已正式冻结于 `Curis_Content_Growth_Domain_Authority.md` §1.2。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化三件事的语义分界（继承前序结论）：

- **Channel** = 平台本身（**事实层**因）。定义「平台**允许什么 / 要求什么**」。
- **Channel Account** = 用户在该平台实际经营的账号（**经营层**）。定义「这个号**做什么 / 什么风格**」。
- **OfficeAccountBinding / Account Pool** = Office 与账号的绑定关系与派生池（DELTA 1）。

**Capability Truth 铁律**（用户约束 5）：
- Channel **只引用已验证的平台能力**。
- 未验证 → `UNKNOWN`
- 受账号 / Scope 影响 → `CONDITIONAL`
- **不**因第三方 SaaS 能而写成 Channel 原生能力。
- 平台具体 Connector 实现**不进入本轮**（仅引用）。

---

## 1. Channel（Content Growth Domain · 事实层）

### Object semantics
平台本身。是**事实层**，不是账号、不是连接器实现。Channel 描述该平台客观允许/要求的能力与约束。

### Identity
- `id`（枚举式：`DOUYIN` / `XHS` / `TIKTOK` / `BILIBILI` / `YOUTUBE`）
- `name`（展示名）

### Relationships
- `Channel 1 — * Channel Account`（一个平台含多个账号）
- `Channel → capabilities_ref`（指向 Capability·Connector 能力目录，**引用不拥有**）

### Ownership
- 定义属 **Content Growth Domain**；能力**执行**属 **Capability·Connector**（不在此定义）。

### Lifecycle
- `registered`（平台纳入支持范围）→ `active` → `deprecated`（平台不再支持）

### Required / Optional information
**必填**：`id`、`name`
**可选**：
- `policy_context`（平台政策上下文引用）
- `constraints_catalog`（平台级约束：ratio / duration / resolution / copyright / scheduling 支持度 —— 仅记录**已验证**事实）
- `capability_refs`（指向 Connector 能力，按能力状态枚举标注）

### Invariants（硬约束）
1. Channel **只引用 VERIFIED 能力**。能力状态枚举：
   - `VERIFIED`（官方源确认可用）
   - `CONDITIONAL`（依赖账号类型 / Scope / 企业资质，运行期按账号解析）
   - `UNKNOWN`（尚未以官方源验证，**不得**假定可用）
   - `UNAVAILABLE`（官方确认不支持）
2. **不**将第三方 SaaS 能力写成 Channel 原生能力。
3. Channel 不含发布逻辑；发布由 Connector 执行。
4. Channel 与 Channel Account 严格分离：一个 Channel 可含 N 个 Account，账号间定位可不同。

### Cross-object references
- → Channel Account（子账号）
- → Capability·Connector（能力执行方，**引用不拥有**，Connector 内部不在本契约）

### Failure / Unknown semantics（能力状态样例）
- 抖音官方发布 API **无定时发布参数** → `scheduling.publishAt = UNKNOWN`（非第三方工具博客所述即认定可用）。
- YouTube `publishAt` → `VERIFIED`。
- Bilibili 强制 `copyright` 字段 → `VERIFIED`（约束，非能力）。
- 抖音完播率仅在经营号授权层可得，OpenAPI 层仅计数 → 该指标对普通号 `CONDITIONAL` / 对未授权经营号 `UNKNOWN`。
- 评论回复仅限「自己视频」、私信 `receive_msg` 仅企业号 → 互动能力对普通号 `CONDITIONAL`。

### Example scenarios
- **CASE 5（某账号 OAuth 失效）**：失效的是 **Channel Account** 的 `authorization_state`，**Channel（DOUYIN）定义不受影响**，其余 DOUYIN 账号照常。

---

## 2. Channel Account（Content Growth Domain · 账号经营层）

### Object semantics
用户在该平台**实际经营的账号**。是「这个号**做什么 / 什么风格经营**」的载体。一个 Channel 上可存在多个定位不同的 Channel Account（CASE 1）。

### Identity
- `id`（全局唯一）
- `channel`（FK → Channel）

### Relationships
- `Channel Account *—1 Channel`
- `Channel Account *—* Office`（经 **OfficeAccountBinding**，DELTA 1：首版推荐 1:1，结构支持 N:N）
- `Channel Account → authorization_ref`（→ Connector 凭据引用，**不在此定义凭据本身**）
- `Channel Account → platform_policy_context`

### Ownership
- 账号是 **Company 资产**（公司拥有该经营身份）。经 Binding 服务于 Office(s)，不是 Office 的「组织下属」。

### Lifecycle
`connected`（已连接）→ `authorized`（已授权）→ `active` → `expired` / `revoked`（凭据失效，**仍保留账号与历史**）→ `disconnected`（用户解绑，历史保留）

### Required / Optional information
**必填**：`id`、`channel`、`identity`（平台 handle / 显示名）、`positioning`（账号定位）
**可选**（长期复用经营语义）：
- `niche_pillars[]`（内容支柱）
- `audience`（受众）
- `tone_style`（语气/风格）
- `language`
- `format_preference`（格式偏好）
- `publishing_rhythm`（发布节奏）
- `growth_goals`（增长目标）
- `historical_performance`（历史表现摘要）
- `authorization_ref`（→ Connector 凭据引用）
- `platform_policy_context`（平台政策适用上下文）
- `brand_knowledge_refs[]`（绑定 Brand / Knowledge 引用）

### Invariants（硬约束）
1. **Channel Account ≠ Channel**。一个 Channel 含多 Account，定位可不同（CASE 1：Douyin AI科普号 vs 个人IP号）。
2. **账号存在独立于 OAuth 健康**（CASE 5）：OAuth 失效 → 账号保留、`authorization_state=expired`、当前执行能力降级、**历史 Publication 保留**；不删除账号、不删除历史。
3. **首版推荐 1 Account : 1 Office**（结构支持 N:N，留待联名号/共享账号/特殊矩阵启用）。
4. 账号 `positioning` / `tone_style` 是**每账号**属性，可与其同平台兄弟账号不同。

### Cross-object references
- → Channel（父平台）
- → OfficeAccountBinding（→ Office）
- → Publication（历史发布记录，契约 5 后续）
- → Content Variant（账号级变体，契约 5 后续）
- → authorization_ref（→ Connector 凭据）

### Failure / Unknown semantics
- `authorization_state`：`ACTIVE` / `EXPIRED` / `REVOKED` / `NEVER`
- 当 `EXPIRED` / `REVOKED`：
  - 账号仍可查询、历史 Publication 仍保留；
  - 当前 publish / engage / analytics **执行降级**为该账号 `UNAVAILABLE`；
  - **不级联删除**账号或历史；
  - 该账号自动从相关 Office 的 **Effective Target Account Set** 移除（本次内容实例），不阻断其他账号。

### Example scenarios
- **CASE 1**：`Douyin · AI科普号` 与 `Douyin · 个人IP号` 是两个不同 Channel Account，不同 `positioning`，各归不同 Office。
- **CASE 5**：`Douyin · Curis AI` 的 OAuth 过期 → 账号保留、历史发布保留、本账号发布降级、其他账号不受影响。

---

## 3. OfficeAccountBinding（Content Growth Domain · 绑定关系 · DELTA 1）

### Object semantics
Office 与 Channel Account 之间的**绑定关系对象**。用以替代「Channel Account 上写 `office_id` 外键」的旧表达，支持未来 N:N（联名号 / 共享账号 / 特殊矩阵关系）。

### Identity
- 复合键：`office_id` + `channel_account_id`

### Required / Optional information
**必填**：`office_id`、`channel_account_id`
**可选**：
- `role`（`PRIMARY` / `SECONDARY` / `SHARED`）
- `binding_state`（`ACTIVE` / `INACTIVE`）

### Invariants
1. **首版 UX 推荐 1 Account : 1 Office**（典型路径：一个账号主要归属一个 Office）。
2. **数据结构不堵死 N:N**：联名号（一账号服务多 Office）、共享账号（多 Office 共用一账号）通过多行 Binding 表达。
3. Binding **不授予** Organization 成员资格（Employee 不因此「属于」Office）。

### Cross-object references
- → Office（契约 1）
- → Channel Account（本节 §2）

---

## 4. Account Pool（派生集合 · 非必存实体）

### Object semantics
某 Office 当前**可经营的账号集合** = 该 Office 下 `binding_state=ACTIVE` 的 OfficeAccountBinding 所指向的 Channel Account 全集。

### 组成
- `office_id`
- `members[]` = `{ channel_account_id ... }`（来自 Active Bindings）

### 设计建议（Batch A）
- **首版派生**，不从 Binding 额外物化存储；仅当性能需要再物化。
- 是 Target Account Set（契约 4）的**候选来源**。

### Example scenarios
- **CASE 2**：`Office · Curis AI` 的 Account Pool = `{ Douyin·Curis AI, XHS·Curis AI, Bilibili·Curis AI, TikTok·Curis AI }`。

---

## 5. 归属层

| 对象 | 归属层 | 执行方 |
|------|--------|--------|
| Channel | Content Growth Domain | 能力执行 → Capability·Connector |
| Channel Account | Content Growth Domain | 凭据/发布 → Capability·Connector |
| OfficeAccountBinding | Content Growth Domain | — |
| Account Pool | Content Growth Domain（派生） | — |

---

## 6. 与现有权威文档的关系

- **P1–P7**：不冲突。本契约为业务对象（平台/账号），与责任/员工/系统语义正交。
- **XHS Instance**：当前 XHS 实例绑定单一 XHS 账号，是该契约的 1 Office·1 Account 退化形态；新模型支持其未来扩展为多 Office·多账号。当前实例不变。
- **Connector 不开发**：`authorization_ref` / `capabilities_ref` 仅作引用；OAuth / Scope / 发布 / 互动 / 数据的具体实现在 Connector 设计期另行规划（不在本契约）。

---

*本文件为 Contract Candidate，未 Frozen。以 Review 批准后的修订版为准。*

---

*CONTENT GROWTH CONTRACT BATCH A — APPROVED CANDIDATE*
