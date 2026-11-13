# CONTENT GROWTH — CHANNEL / ACCOUNT / PUBLISHING MODEL
### 统一 Channel 模型 · 多账号管理 · 发布目标选择 · Channel Variant · Publishing 真实状态 · Calendar

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_FUNCTIONAL_INTERACTION_MODEL.md`（主模型 §2.11–2.13）· `CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md` · `CONTENT_GROWTH_CONTENT_EMPLOYEE_INTERACTION_MODEL.md`
前置：Shared vs Channel Matrix（XHS/Douyin=Channel，4 Module + N Connector）；Product Mapping（Channel=Channel 对象+Module+Connector，不新 primitive）；Product Experience §6（Channel 4 形式）。

---

## 0. 红线
- **XHS/Douyin/TikTok/YouTube/Bilibili/公众号/视频号 = Channel**（Content Growth Workspace 下的对象），**不是独立 Workspace / Tab**。
- **统一 Channel 模型**：所有平台走同一套「Channel 对象 + Module + Connector」，不为每平台重造产品。
- **发布真相 per-Account**：绝不伪造单一「整体成功」；每个账号独立状态，由 Connector 回填。
- **合规硬约束**（沿用 XHS 研究 §O.3.4）：私信/评论引流红线、频率限制、多账号同质化禁令；自动发布仅三条件齐备（开放平台发布权限 + 合规预审通过 + 养号达标）才受控自动，且留审计可回滚。

---

## 1. CHANNEL MANAGEMENT（§10，统一模型）

### 1.1 支持平台
XHS / Douyin / TikTok / YouTube / Bilibili / 公众号 / 视频号。统一对象字段：名称、平台类型、连接状态、账号数、最近发布、合规策略。

### 1.2 操作
- **添加 Channel**：渠道 Surface / 设置区 → 选平台 → 官方 OAuth/API 授权 → 成为 Channel 对象。
- **连接 / 断开 / 重新授权**：断开保留历史；授权失效走平台重授权。
- **删除**：彻底移除（谨慎，保留历史发布记录快照）。
- **查看状态**：Connected / Not Connected / Unavailable / Needs Permission / Failed（诚实表达）。
- **Channel-specific 能力如何出现**：以 **Channel Module** 形式挂载（格式适配 / 平台分析 / 渠道反馈 / 发布执行），由 Channel Operator + Connector 在后台驱动，用户多不感知。
- **平台不支持 Connector 怎么办**：标 Unavailable + 提供替代（官方开放平台 API 若未开放则建议 RPA/手动，并明确「非官方、合规风险自担」）。

### 1.3 CEO 感知
CEO 仅在 **选渠道、看 per-Account 发布真相、处理渠道反馈、渠道权限未就绪** 时意识到 Channel；格式适配/发布执行/数据回收/防封 → 系统后台自动。

---

## 2. MULTI-ACCOUNT MANAGEMENT（§11，本轮最高优先级之一）

### 2.1 结构示例
```
XHS
 ├ AI科技主号
 ├ AI工具测评号
 └ 个人IP号
Douyin
 ├ 主号
 └ 视频实验号
TikTok
 ├ US
 └ SEA
```

### 2.2 操作逐项
- **账号新增**：Channel 详情 → 「加账号」→ 平台授权 → 配置。
- **命名**：用户自定义（建议「平台+定位」）。
- **归属 Business/Brand**：账号挂在对应 Office/Business 下（Office⊥Organization `[CURIS-AUTH]`）。
- **定位配置**：账号定位（Persona）、Audience、Tone/Brand Context 在账号级配置。
- **默认账号**：每 Channel 设一个默认账号（发布默认勾选）。
- **切换**：发布时选；日常 Context 显示当前账号。
- **批量选择**：发布目标多选/全选。
- **分组**：账号可分组成「矩阵组」（如 KOS 矩阵），用于协同但**遵守同质化红线**（内容需差异）。
- **授权状态**：显示 Connected/Expired/Needs Permission。
- **掉线/权限失效**：标红 → 提示重授权 → **自动暂停该账号发布**（不动其他账号）。
- **账号自身历史**：账号详情看历史内容 + 表现（不污染其他账号 Context）。
- **跨账号 Context 污染防护**：每个账号的定位/受众/调性独立；Variant 生成时只用目标账号 Context，禁止串号。

---

## 3. PUBLISH TARGET SELECTION（§12）

### 3.1 选择关系
```
Channel
 └ Account
     └ Variant（同一 Content Intent 的账号变体）
```
用户说「发到小红书和抖音」→ 系统展开 Channel→Account→Variant 树。

### 3.2 选择 UI 逻辑（非最终 UI，定义行为）
```
发布到
☑ 小红书
   ☑ AI科技主号
   ☐ 个人IP号
☑ 抖音
   ☑ AI科技主号
```
- **默认选择逻辑**：上次使用账号 / 推荐账号（匹配内容定位）/ 默认账号自动勾选。
- **多选 / 全选**：支持；可只选部分账号。
- **账号不 Eligible**（如定位不匹配）：灰显 + 理由，不可勾或需确认覆盖。
- **账号未连接**：标「未连接」，勾选时提示先连接。
- **账号权限不足**（如不可发布）：标「需授权」，阻断该账号发布。
- **账号内容定位不匹配**：提示「该内容与账号定位偏差大，确认发布？」。

### 3.3 原则
不让用户记忆账号细节；系统推荐 + 用户确认；复杂选择后台由 Channel Operator 处理。

---

## 4. CHANNEL VARIANT（§13）

### 4.1 同一 Content Intent 发不同账号时的三档
| 档位 | 适用 | 行为 |
|---|---|---|
| **轻适配** | 同平台同调性账号 | 自动改标题/标签/封面微调 |
| **重生成** | 跨平台/调性差异大 | 基于 Intent 重新生成文本/结构 |
| **完全不同** | 账号定位迥异（如主号 vs 个人 IP） | 独立 Draft，仅共享 Intent 核心 |

### 4.2 谁看到什么
- **CEO 默认**：只见发布结果（同其他账号一致投影），不强制看所有 Variant。
- **Employee Working View**：全部 Variant 列表 + 对比（Comparison Utility）+ 单 Variant 编辑（改一个不影响其他账号）。
- **比较 / 修改局部**：Comparison Utility 并排；点某 Variant 改 → 仅该账号 Variant 变更。

---

## 5. PUBLISHING（§14，真实状态）

### 5.1 状态机（per-Account）
| 状态 | 含义 |
|---|---|
| Ready | 已就绪待发 |
| Needs Review | 待人工审核（合规/品牌） |
| Needs Permission | 待授权（账号/平台） |
| Scheduled | 已定时 |
| Publishing | 发布中 |
| Published | 已发布（平台回执确认） |
| Failed | 失败（附原因） |
| Platform Reviewing | 平台审核中 |
| Rejected | 平台驳回（附原因） |

### 5.2 操作
- **发布前预览**：各账号 Variant 预览 + 风险检查（合规/频率/定位）。
- **发布时间**：立即 / 定时（每账号可不同）。
- **批量**：多账号一次提交，但 **per-Account 独立回执**。
- **修改 / 撤销 / 重试**：Scheduled 可改/撤；Failed 可重试（看原因）；Rejected 需改后重提。
- **失败原因 / 平台回执 / 真实 URL**：来自 Connector 回填，进 Publication Result；真实 URL 可点击回平台。
- **多账号不伪造整体成功**：发布 Result 保持 per-Account truth；驾驶舱⑥「发布结果」显示每账号状态（如「XHS 阅读中 / 抖音审核中」）。

### 5.3 Human-in-the-loop 默认
- 默认需人类确认（风险检查通过后点「发布」）。
- 仅三条件齐备才受控自动发布（开放平台发布权限 + 合规预审通过 + 养号达标），留审计 + 可回滚。

---

## 6. CALENDAR（§15）

### 6.1 为什么需要（不是因为别人有）
- 统一看 **多 Channel / 多 Account** 的 Draft / Scheduled / Published / Campaign，发现 **Gap（内容空白）/ Conflict（冲突/超限）**。
- **Employee 更需要**（Producer/Channel Operator）；**CEO 通常不需要**（驾驶舱已给发布结果）。

### 6.2 视图内容
- 时间轴：各渠道各账号排期 + 已发布 + Campaign 标记 + Gap/Conflict 提示。
- 操作：拖拽排期 / 改时间 / 看某天详情 / 发现空白。
- 层级（OPEN QUESTION Z1/Z7，待 CEO 裁决）：建议作为「内容」Surface 内视图，非独立 L1 导航；专家异议（Calendar 独立 L1）已记录待裁决。

---

## 7. 与 FINAL ACCEPTANCE 对应（本轮 §22 子集）
- Q12 连接各平台 → §1.2
- Q13 多账号管理 → §2
- Q14 发布选具体账号 → §3
- Q15 多账号 Variant → §4
- Q16 账号掉线 → §2.2「掉线/权限失效」
- Q17 多账号发布状态 → §5.2
- Q18 Calendar 解决什么 → §6

---

*CONTENT GROWTH CHANNEL / ACCOUNT / PUBLISHING MODEL — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
