# CURIS FIGMA MAKE — CURRENT DESIGN CONTEXT PACK

> Status: Review  
> Authority Class: RESEARCH / DESIGN CONTEXT  
> Disposition: Figma Make input only; not a new Authority  
> Updated: 2026-08-24

## 1. Curis 是什么

Curis 是 **AI Company Operating Product**：把成熟 AI 工作能力组织成一家公司，让普通用户能够表达意图、看到责任、消费结果，并在重要判断处介入。

主要用户是小白 CEO / 公司经营者。CEO 主要提供：

- Intent
- Reference
- Constraint
- Relevant Decision

AI Employee 负责专业研究、策略、配置、操作、评估与学习。CEO 默认消费 Result、Value、Recommendation、Risk、Decision，不管理 Workflow、Agent 或专业参数。

Curis 不是 Dashboard、SaaS 后台、文件库、Task Manager、Agent 控制台或单纯聊天产品。

## 2. Curis 整体结构

```text
Company → Business → Workspace
```

- Business 表达业务范围与业务级方向。
- Workspace 是独立专业经营环境，也是唯一 canonical user/product identity。
- Channel / Account 是 Workspace 内的外部经营对象，不是 Workspace。
- Content Growth 是 Professional Workspace Candidate，不是 Verified Professional Workspace。

### Four-Pane Product Framework

四区是稳定的职责模型，不是四根永久可见的物理栏：

| 区域 | 职责 |
|---|---|
| Navigation | Curis 全局 / 产品导航，回答“我在哪里” |
| Context | Main 左侧按需上下文：Workspace、Domain、当前对象、Work、决策支撑 |
| Main | 核心工作区域：selected Professional Surface + Shared Work Area |
| Utility | Main 右侧按需辅助：Detail、Editor、Preview、Evidence、Tool、Action |

默认主要可见 Navigation + Main；Context / Utility 可折叠、收起、按需展开。Main 始终保持 Primary Focus。

### Shared Shell vs Domain

Shared Shell 提供空间职责、Conversation、Employee Pattern、Composer、Context 连续性与通用返回逻辑。Domain 只提供 selected Surface、Domain objects、Result projection、Domain actions 与 bounded Context。

## 3. Shared Patterns

- **Universal Conversation**：Curis Shared capability，不是 Content Growth 独立页面。
- **Employee 三入口**：直接对话、当前工作、员工资料；同一 Employee identity 连续存在，不是三套产品。
- **Conversation-first Employee Workstation**：进入具体 Employee 后，Main 显示自然 Conversation、工作状态、Tool / Action 状态、Result / Artifact、Composer。
- **Result / Context / Evidence**：先看 Result 与行动；Context、Evidence、Source、History 按需展开。
- **Quick Path**：CEO 可直接说“帮我做这个”，不必先理解专业 IA；结果回到原对象 / 经营结果。
- Employee Workstation / Conversation 不进入 Context Sidebar；Employee Detail 不包含 Conversation。

## 4. Content Growth 实例

Content Growth 是一个 AI Employee 团队帮助 CEO 经营内容业务的 Professional Workspace Candidate。

### 默认经营结果面

Main 默认优先呈现：当前最值得 CEO 关注的 Result / Decision / Action。

- 0–3 个高价值事项是候选表达，不是固定 Runtime contract。
- Quiet experience 表示当前没有需要 CEO 处理的事项。
- Result 支持：查看依据、问负责员工并携带 Context、按建议继续。
- 不做 Dashboard、固定 8 态 / 4 桶或大卡片墙。

### Domain objects

| 对象 | 默认表达 |
|---|---|
| Topic / 选题 | 选题、为什么值得做、Goal 关系、风险、建议 |
| Research / 调研 | 结论、意味着什么、风险 / Unknown、建议；Evidence / Source 按需 |
| Source / 来源 | Employee 工具；对话表达意图，主动进入时才 Deep View 管理 |
| Content / Version / Asset | 推荐成品优先；版本、推荐版本、素材按需展开；Content 与 Asset 合并表达 |
| Publishing | Employee 推荐发哪里、哪个账号、何时、为什么；复杂结构按需查看 |
| Evaluation / Feedback | 先看经营结论、Goal 关系与下一步；Metric / Feedback / Evidence 按需 |
| Employee Current Work | 在做什么、为什么、已有 Result / Evidence、下一步、等待与 Handoff |

### Core object relationship

```text
Signal / Opportunity → Topic → Research → Content → Variant → Publication
       → Feedback → Evaluation → Next Work / Topic
```

关联对象包括 Source、Evidence、Asset、Employee、Result、Work；这只是 IA 关系，不新增 Runtime primitive。

## 5. Visual Goal

- 简洁但不能寡淡。
- 每个视口有一个明确 Primary Focus。
- 信息丰富，但通过层级与 progressive disclosure 按需展开。
- 让人感觉“一家 AI 公司正在替我经营”。
- 不像 Dashboard、SaaS 后台、文件库、Agent 控制台、Task Manager 或 CMS。
- Shared visual candidate language：**Calm Surface / Strong Focus / Rich Work**。
- 对话是自然阅读流，不是气泡墙；Employee 是责任主体，不是监控对象。

## 6. Current Capability Truth

Figma 必须诚实表达：

- 五个平台没有任何 audited `VERIFIED` capability。
- 不伪造 Connected account、Live Publish、Published URL、Live Analytics、Live Comments、Multi-account。
- Auth 为 `PARTIAL` 不等于 OAuth / 账号归属已验证。
- Publish 为 `CONDITIONAL`，没有 live publication evidence。
- XHS 部分 Schedule / Status / Receipt / Comments 为 `PARTIAL`，Analytics 为 `UNAVAILABLE`。
- 其他平台相关能力按 `UNKNOWN` 或 Audit 原值表达。
- Multi-account 为 `UNAVAILABLE`。

目标能力可以展示，但必须标：

`TARGET SCENARIO / NOT CURRENT CAPABILITY`

## 7. Language

用户界面以中文为主。Topic、Research、Evidence、Source、Evaluation、Publication、Variant、Handoff、Responsibility 等英文只可作为设计标注或必要的专业辅助，不要堆成小白用户的主要产品语言。

## 8. Figma Freedom

### Locked

- Company / Business / Workspace hierarchy。
- Four-Pane responsibilities 与 Context / Utility adaptive / collapsible 行为。
- Shared Shell vs Domain ownership。
- Main、Universal Conversation、Employee 三入口、Conversation-first Workstation。
- Content Growth object relationship、Result-first IA、Current Capability Truth。
- 不新增 Shell、Employee system、Work system、Result truth 或 Runtime truth。

### Free to explore

layout、grid、spacing、typography、density、content width、surface treatment、component geometry、focus、progressive disclosure、transition、motion idea、accent / color strategy。

现有 Low-Fidelity HTML 只提供结构关系；不要模仿其配色、Card、badge、bottom nav、spacing、density 或 typography。

