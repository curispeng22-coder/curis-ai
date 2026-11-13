# Curis · Content Opportunity / Intent Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch A — Operating Foundation，未 Frozen）
> **类型**：Content Growth Domain（Company 级 Growth Context）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 3）、上一轮 `Curis_Content_Growth_Operating_Model.md`（E/F 节：Intent 为跨账号共享上游对象）、用户约束 3（Intent 不过度实体化）
> **FROZEN 指针（2026-08-16）**：③ Content Opportunity / Content Intent 语义已正式冻结于 `Curis_Content_Growth_Domain_Authority.md` §1.3。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化「**准备讲什么 / 为什么做 / 服务什么目标**」的载体 —— **Content Intent**。

**核心结论（继承前序）**：真正跨平台 / 跨账号共享的对象，是 **Content Intent / Opportunity**（一次推理），而**不是**最终母版视频。Intent 允许后续**动态分流**（HIGH REUSE + FULL DIVERGENCE，CASE 4 验证）。

**用户约束 3（Intent 不过度实体化）**：
- Intent **只保存长期追踪与复用的业务语义**（why / what / goal）。
- **禁止**将以下内容塞入 Contract：
  - AI 推理过程
  - Prompt
  - 临时 Chain-of-Thought
  - 中间草稿
- 这些内容属于**运行期执行**，不进入 Intent 对象。

本契约只定义对象语义 / 关系 / 归属 / 生命周期 / 必填·可选 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

---

## 1. Content Opportunity（Content Growth Domain · 信号）

### Object semantics
「**什么值得做**」—— 来自 Growth Intelligence（趋势 / 搜索 / 评论 / Analytics / Knowledge）的一个候选信号。是尚未承诺生产的**候选**。

### Identity
- `id`
- `source`（信号源类型：TREND / SEARCH / COMMENT / ANALYTICS / KNOWLEDGE）
- `topic`
- `score`（机会评分）
- `rationale`（为什么值得做）
- `suggested_offices[]`（建议服务的 Office）

### Ownership
- **Company 级 Growth Context**（共享），非 Office 私有。

### Lifecycle
`detected` → `evaluated` → `converted`（转为 Intent） / `dismissed`

### Required / Optional
- 必填：`source`、`topic`
- 可选：`score`、`rationale`、`suggested_offices[]`

### Invariants
- Opportunity 是**信号**，不是承诺；不绑定具体账号/平台。

### Cross-object references
- → Content Intent（转化目标）
- → Growth Intelligence（来源与回流）

---

## 2. Content Intent / Package（Content Growth Domain · 共享上游对象）

### Object semantics
「**我们准备讲什么 / 为什么做 / 服务什么目标**」。

Intent **表达**：
- 为什么做（business_goal）
- 准备讲什么（topic / core_message）
- 服务什么目标（business_goal / cta_intent）

Intent **不表达**：
- 最终视频已经长什么样
- 各平台具体剪辑参数
- 任何账号特定形态

### Identity
- `id`
- `linked_opportunity_id?`（来源 Opportunity，可选）

### Required information（核心必填）
- `topic`（准备讲什么）
- `core_message`（核心表达）
- `business_goal`（服务什么目标 / 为什么做）

### Optional information（仅长期复用业务语义）
- `audience_hypothesis`（受众假设）
- `verified_facts`（已核实事实）
- `source_material`（素材引用）
- `brand_requirements`（品牌要求）
- `cta_intent`（行动号召意图）
- `available_assets`（可用素材）
- `knowledge_evidence_refs[]`（Knowledge / 证据引用）

### ❌ EXCLUDED FROM CONTRACT（明确不存入 Intent 对象）
以下内容属于**运行期执行产物**，不进入 Intent 契约（用户约束 3）：
- AI 推理过程 / Reasoning trace
- Prompt / 指令原文
- 临时 Chain-of-Thought
- 中间草稿 / 未定稿脚本版本
- 生产工具调用日志

> 它们应存在于执行上下文（Conversation / Runtime），Intent 只沉淀**结论性业务语义**。

### Relationships
- `Content Intent *—1 Content Opportunity?`（弱来源链接）
- `Content Intent *—* Office`（**弱服务关系**：Intent 可为多个 Office 服务，不被单一 Office 拥有；经 Target Account 再分流）
- `Content Intent 1 — * Target Account Set`（每个内容实例一次选择，见契约 4）
- `Content Intent 1 — * Content Variant`（分流后的账号级变体，见契约 5 后续 Batch）

### Ownership
- **Company 级 Growth Context（共享）**，不被 Office 独占、不被 Organization 层拥有。

### Lifecycle
`drafted`（初步想法）→ `briefed`（core_message / goal 已定）→ `targeted`（Target Accounts 已选）→ `produced`（变体已生产）→ `published` → `feedback`（回流 Opportunity / Growth Intelligence）

### Invariants（硬约束）
1. Intent 表达 **WHY / WHAT / GOAL**，不表达最终资产形态。
2. **单 Intent 可产分歧性生产**（CASE 4）：同 Intent → Douyin 30s 口播 / XHS 图文 / Bilibili 8min 教程。
3. Intent **不过度实体化**：不存推理/Prompt/CoT/中间草稿。
4. Intent 与 Office 是**弱链接**（可跨 Office 复用同一母题），非所有权。

### Cross-object references
- → Content Opportunity（来源）
- → Target Account Set（契约 4）
- → Content Variant / Publication（契约 5 后续）
- → Office（弱服务链接，契约 1）
- → Growth Intelligence（反馈汇）

### Failure / Unknown semantics
- 若 Intent 选定的某账号其 Channel 能力为 `UNKNOWN` / `CONDITIONAL` → **生产要求推导必须标记缺口**，不得假定能力可用。
- Intent 若**无确认 Target Accounts** → 停留在 `briefed` / `targeted` 草稿态，**不被强制群发**。
- Intent 引用的 `verified_facts` 失效（如数据过期）→ 标记为 `(UNK) 待复核`，不删除 Intent。

### Example scenarios
- **CASE 4（同 Intent 分歧生产）**：
  - Intent：「AI 工具提效」核心信息，goal=获客。
  - Douyin 账号 → 30 秒快节奏口播变体
  - XHS 账号 → 图文笔记变体
  - Bilibili 账号 → 8 分钟教程变体
  - TikTok 账号 → 英文短视频变体
  - **Intent 保持共享**，Production 后续允许 Divergence。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Content Opportunity | Content Growth Domain（Company Growth Context） |
| Content Intent | Content Growth Domain（Company Growth Context） |

---

## 4. 与现有权威文档的关系

- **P1–P7**：不冲突。Intent 是业务对象；与责任/员工语义正交。
- **XHS Instance**：当前 XHS 实例的「选题库·信号」对应本契约的 Content Opportunity 上游；XHS 未来纳入时，其选题库作为 Growth Intelligence 信号源之一，XHS Note 生产消费 Intent → Target Account → Variant。当前实例不变。
- **Contract 3 ↔ 契约 1/2/4 的依赖**：Intent 弱链接 Office（契约 1）；后续生产要求推导依赖 Channel Account 约束（契约 2）；经 Target Account（契约 4）分流到具体账号。

---

*本文件为 Contract Candidate，未 Frozen。以 Review 批准后的修订版为准。*

---

*CONTENT GROWTH CONTRACT BATCH A — APPROVED CANDIDATE*
