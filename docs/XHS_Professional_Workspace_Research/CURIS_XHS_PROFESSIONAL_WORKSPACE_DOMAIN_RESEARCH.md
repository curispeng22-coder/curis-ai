---
title: Curis XHS Professional Workspace — Domain Research
status: RESEARCH / EXPERT RECOMMENDATION
author: Social Media Growth & Content Operations Expert (lead) + 社媒互动增长专家团（signal-miner / brand-monitor / interaction-automator / ai-comment-specialist）
date: 2026-08-21
purpose: 从真实经营实践出发，研究一个真正专业的小红书账号经营工作台需要承载哪些专业能力 / 对象 / 工作区 / 信息架构；不设计 UI、不实现、不修改 Frozen Authority。
evidence_discipline: 每个重大结论标注 [REAL 真实经营实践] / [COMP 竞品证据·附URL] / [CURIS Curis 当前权威] / [INF 研究推断] / [CAND 候选建议]。平台具体数值标注 VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE。
upstream:
  - docs/03_Design/Curis_XHS_Workspace_Reference_Research.md（2026-08-15 · XHS READY FOR DESIGN）
  - docs/03_Design/Curis_XHS_Workspace_Design_Brief.md（Review）
  - docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md（XHS INSTANCE APPROVED CANDIDATE）
  - docs/03_Design/Curis_XHS_Workspace_Calendar_Pattern_Spec.md
  - docs/01_Product/Curis_Product_Blueprint.html（v5.1 · Single Current）
stop: STOP FOR CEO REVIEW（不自动更新 Authority / 不实现 Package / 不修改 Blueprint·Master Map·UI·Runtime·Schema·Prototype）
---

# A. Executive Summary

> 本文件是研究，不是设计稿，也不是实现。它回答一个问题：**如果一个专业运营团队接管一个小红书账号，从创建/接管的起点一直到持续增长、商业化、复盘、下一轮策略调整，他们每天/每周/每月真正需要完成哪些工作？最终一个 Professional Operating Environment 需要承载什么？**

## A.1 核心结论（先说结论）

1. **Workspace ≠ 一个 Surface，更 ≠ 一个 Calendar。** 当前 XHS Instance Spec 把「Calendar-Dominant（日历主导）」定为默认工作面，这把**内容发布排期**这一个阶段误提升为整个经营 Workspace 的代表面。研究确认：**Calendar 是「内容运营（Content Operating）」阶段的一等 Surface，但不应是一个专业经营 Workspace 的默认入口。**
2. **默认入口应是「经营语境恢复（Operating Overview）」**：进入即回答——现在处于什么阶段？当前目标？当前策略？最重要的专业工作？最新结果？哪里需要关注？下一步是什么？这不是 Dashboard，不暴露架构图，只恢复语境。 [CAND]
3. **真实经营生命周期远比「选题→制作→发布→数据」长**：它向前延伸到账号定位/用户研究/赛道研究/竞品研究/平台趋势/搜索需求/关键词，向后延伸到增长/粉丝画像/搜索流量/转化/复盘/策略调整/商业化/资料沉淀/团队协作。Calendar 只覆盖中间一段。 [REAL]
4. **专业对象应精简**：候选 21 个对象里，真正需要作为 Domain canonical object 长期存在的约 7–9 个；其余是 View / Artifact / Evidence / Runtime Work / Result / External provider object。避免重造系统。 [INF]
5. **Curis 的差异化不在「更大的社媒 SaaS」，而在 Autonomous Operating**：行业工具止步于「人类判断」环节（策略方向、品牌调性、合规风险、商业化报价、跨平台归因、因果判断）。Curis 作为 AI Company Operating System，应让 AI 员工在人类设定的规则内自主推进，只在 Decision Gate 出现。 [CAND]
6. **与 Curis 当前权威的关系（重要·待 CEO 裁决）**：本研究与 2026-08-15 的 `Curis_XHS_Workspace_Instance_Spec_v1.md` 的「Calendar-Dominant 默认」候选**存在张力**。Instance Spec 的「Content Object × Time 双主轴语义」是冻结语义契约（不破）；但「默认进入面 = Calendar」是 APPROVED **CANDIDATE**（未 Frozen），本研究发现它应降级为「内容运营阶段的主 Surface」，默认入口让位给 Operating Overview。此为 **OPEN QUESTION / CEO DECISION**，本研究不擅自改写权威。 [CURIS]

## A.2 证据来源分级（全文沿用）

- `[REAL]` 真实经营实践（行业 SOP / 团队运作常识 / 本研究验证）
- `[COMP]` 竞品真实功能（附 URL，来自 signal-miner / brand-monitor 专项报告）
- `[CURIS]` Curis 当前权威文档（Reference Research / Design Brief / Instance Spec / Calendar Pattern / Blueprint）
- `[INF]` 基于证据的研究推断
- `[CAND]` 候选建议（待 CEO / 设计裁决）

平台事实四态（对齐 Frozen Authority）：`VERIFIED`（官方已验证）/ `CONDITIONAL`（条件性·待核）/ `UNKNOWN`（当前无法确认）/ `UNAVAILABLE`（已确认当前不存在/不支持）。

---

# B. Real XHS Operating Lifecycle

> 方法：先列完整生命周期候选（来自 brief §3），再合并/删除/补充/重分类。

## B.1 完整生命周期（研究后重分类）

| 阶段 | 关键工作 | 真实载体 | 证据 |
|---|---|---|---|
| **0. 账号基建 / 接管** | 定位、人设、视觉规范、账号类型（个人/专业号/企业号）、授权连接 | Account + Brand Brief | [REAL] |
| **1. 用户研究** | 目标人群画像、需求痛点、决策语言 | Audience Research（Evidence） | [REAL] |
| **2. 赛道 / 竞品研究** | 赛道容量、竞品打法、爆款结构、差异化空位 | Competitor / Trend（External→Research） | [REAL] |
| **3. 平台趋势 / 搜索需求** | 平台算法变化、搜索词、意图分布、热点 | Trend / Keyword（External→Research） | [REAL][COMP] |
| **4. 内容策略** | Content Mix、选题标准、栏目规划、实验假设 | Content Strategy / Topic / Experiment | [REAL] |
| **5. 选题** | 选题库维护、信号转化（搜索词/评论/热点→选题）、配比 | Topic & Signal Library | [REAL][CURIS] |
| **6. 内容实验** | 假设提出（如「教程提升转粉」）、变量控制、对照 | Experiment / Hypothesis | [INF] |
| **7. 内容生产** | brief→素材→封面→标题→正文→标签→版本→审核 | Note（Content Object）+ Asset | [REAL][CURIS] |
| **8. 发布 / 排期** | 定时、队列、冷启动赛马、多平台 | Publishing Queue + Calendar（View） | [REAL][CURIS] |
| **9. 互动** | 评论、私信、社区维护、用户问题提炼 | Comment Insight（Evidence） | [REAL] |
| **10. 数据回收** | 单篇表现、账号趋势、粉丝画像、搜索流量 | Performance Record（Evidence/Result） | [REAL] |
| **11. 增长** | 什么有效/为什么/哪个受众/哪个模式/增长来源/恶化点 | Growth Signal → Evaluation | [REAL] |
| **12. 复盘** | 周期复盘、爆款拆解、策略调整建议 | Operating Decision（Event） | [REAL] |
| **13. 商业化** | 品牌合作、商单、报价、交付、回款、收入 | Brand Deal / Commercial Lead（Domain，可选模块） | [REAL][COMP] |
| **14. 资料沉淀** | 品牌资料、规范、素材、研究报告、方法论 | Knowledge / Material（Curis Global 视图） | [REAL] |
| **15. 团队协作** | 责任分工、Handoff、审批、ROI | Employee / Responsibility（Curis 组织层投影） | [REAL][CURIS] |

## B.2 关键洞察

- **Calendar 只覆盖阶段 7–8（生产末段 + 发布）**。把 Calendar 当整个 Workspace 的主面，等于把「排期」误认为「经营」。 [INF]
- **阶段 0–6（定位/研究/策略/选题/实验）是专业门槛最高的部分**，却恰恰是现有原型最弱的部分（当前仅在 Context 侧栏有「信号监测」）。 [CAND]
- **阶段 13（商业化）是成熟账号的营收命脉**，但当前权威将其列为 RESERVED；研究建议按经营阶段作为可选模块启用，而非永久隐藏。 [CAND]

---

# C. Operating Cadence

> 专业团队如何按时间经营？这决定默认入口、经营概览、Surface 优先级。

## C.1 节奏矩阵

| 节奏 | 关注 | 典型动作 | 触发 Surface |
|---|---|---|---|
| **Daily（每天）** | 发布执行、冷启动赛马、评论/私信、异常 | 发布、看 5/30/60 赛马、回评论、处理 Needs CEO | Content Operating（Calendar/Queue）、Feedback |
| **Weekly（每周）** | 内容节奏校准、选题补充、信号复盘 | 周选题会、补选题库、看周趋势 | Content Strategy、Research |
| **Monthly（每月）** | 经营复盘、策略调整、粉丝画像、增长来源 | 月报、爆款拆解、Mix 调整、实验复盘 | Performance & Growth、Operating Overview |
| **Campaign / Experiment Cycle（事件触发）** | 活动、实验、突发热点、危机 | 建实验、跟活动、危情 SOP | Content Strategy（Experiment）、Research |
| **Stage-transition（阶段切换）** | 从 Bootstrap→Growth→Stable→Commercial | 切换主 Surface、启用模块 | Operating Overview（动态主 Surface） |

## C.2 对 Workspace 的含义 [INF][CAND]

- **默认入口（Operating Overview）应承载「日度语境 + 阶段感知」**：每天进来先恢复「今天该盯什么、卡在哪、最新结果」。
- **Weekly/Monthly 不是独立 Surface**，而是 Overview 上「本周/本月」视角 + Performance & Growth 的复盘动作。
- **Calendar/Queue 是 Daily 的高频 Surface**，但不必是默认——默认应是「今天最重要的专业工作」的入口，而非「日历格」。

---

# D. Responsibility Map

> 研究每种 Responsibility 操作哪些对象、产生什么 Result、依赖什么 Evidence、和谁 Handoff。
> 注意：**不把行业岗位直接复制进 Curis**。Curis 的 Employee 是「动态调用能力的岗位」，不是固定 Agent。

## D.1 Responsibility → Work → Object → Result 矩阵（候选）

| Responsibility（职责，非固定岗） | 操作对象 | 产生 Result | 依赖 Evidence | Handoff 到 |
|---|---|---|---|---|
| 运营负责人 / Strategy Owner | 目标、策略、Mix、节奏 | 策略提案、Decision | 全链路数据 | CEO（结构性）/ 各员工 |
| 研究 / Insight | Competitor/Trend/Keyword/Audience | Insight 报告、信号 | 外部源、平台数据 | 选题、策略 |
| 选题 / Content Strategy | Topic、Experiment、Content Mix | 选题库、实验假设 | Insight、历史表现 | 内容生产 |
| 内容生产 / Creation | Note、Asset、Brief | 草稿笔记 | 选题、品牌规范 | 审核 |
| 审核 / Review | Note（合规/人设/品牌） | 审核报告、通过/阻塞 | 违禁词表、规范 | 发布 / Needs CEO |
| 发布 / Distribution | Note、Publishing Queue | 已发布 Result | 平台连接、排期 | 数据回收（系统） |
| 数据分析 / Growth | Performance Record | 增长洞察、实验结论 | 表现数据、受众 | 策略调整 |
| 社区 / Feedback | Comment、DM、User Question | 用户洞察、线索 | 评论/私信、搜索词 | 选题、策略 |
| 商务 / Commercial（可选） | Brand Deal、Commercial Lead | 商单交付、收入 | 粉丝画像、表现、报价 | 财务（外部） |

## D.2 关键裁定 [CURIS][CAND]

- **责任（Responsibility）≠ 固定员工**：同一职责可由同一虚拟员工/能力承担；Curis 用「三层责任」（Object Owner / Current Responsibility / Current Executor）表达，已 Frozen（Instance Spec §8）。
- **数据复盘不是员工岗位**：是系统自动阶段（System Activity，Current Executor = none），不造「数据分析员工」。 [CURIS]
- **Handoff = 责任转移事件**，不是新页面；审核阻塞升级为 Needs CEO（Decision Gate），不是 Handoff。 [CURIS]

---

# E. Professional Object Model

> 找出真正需要长期存在的专业对象；分类 A–G，避免重造系统。

## E.1 候选对象分类

| 候选对象 | 分类 | 理由 / 处理 |
|---|---|---|
| **Account（XHS 账号）** | A. Domain canonical | 经营主体；镜像外部 Provider 对象（专业号/企业号） |
| **Brand Brief / 定位** | A. Domain canonical | 账号定位、人设、视觉规范、违禁词表 |
| **Topic / Content Idea（选题）** | A. Domain canonical | 内容资产核心，可复用、可复盘 |
| **Experiment / Hypothesis（实验）** | A. Domain canonical（建议升格） | 增长需要「假设→验证」一等概念 [CAND] |
| **Note / Post（笔记）** | A. Domain canonical | Content Object，已 Frozen 为 XHS 自有 Pattern [CURIS] |
| **Brand Deal / Commercial Lead（商单）** | A. Domain canonical（可选模块） | 商业化阶段核心；小账号可隐藏 [CAND] |
| **Competitor（竞品）** | G. External provider object | 研究来源，非自有核心对象；以 Research 视图呈现 |
| **Trend / Keyword（趋势/关键词）** | G→A | 外部信号源，但「已采纳的关键词/选题方向」可沉淀为 Domain 对象 |
| **Audience / Fan Profile（粉丝画像）** | D. Evidence / View | 是 Performance 数据的投影，不独立建对象 [INF] |
| **Performance Record（表现记录）** | D. Evidence / F. Result | 数据证据/结果，绑定 Note |
| **Comment Insight（评论洞察）** | D. Evidence | 反馈提炼后的洞察，喂回 Topic |
| **Growth Signal（增长信号）** | D. Evidence → C. feeding Topic/Experiment | 信号，非持久对象 |
| **Asset / Material（素材/资料）** | C. Artifact | 归入 Curis Global Artifact System，不在 XHS 重建 |
| **Calendar Entry（日历项）** | B. View / Projection | = Note + 排期；不独立建对象 [CURIS] |
| **Review（审核）** | F. Result / Event | 审核结果事件，绑 Note |
| **Operating Decision（经营决策）** | F. Result / Event | Needs CEO / Handoff / 策略调整事件，Curis Shared |
| **Publishing Queue Item（队列项）** | B. View | = Note + 发布状态；绑真实 Note [CURIS] |

## E.2 分类结论 [INF][CAND]

- **Domain canonical（建议）**：Account、Brand Brief、Topic、Experiment、Note、Brand Deal（可选）。共 6–7 个。
- **View / Projection**：Audience（Performance 投影）、Calendar Entry、Publishing Queue Item、Competitor/Trend/Keyword（Research 视图）。
- **Artifact**：Asset / Material → 复用 Curis Global Artifact。
- **Evidence / Result**：Performance Record、Comment Insight、Growth Signal、Review、Operating Decision。
- **External provider object**：Competitor、平台原始数据。
- **避免重造**：不建「员工对象」「Dashboard 对象」「粉丝对象」为独立 canonical；粉丝是 Performance 的投影，员工是 Curis 组织层。

---

# F. Professional Capability Map

> 把对象映射到「能力区域」，作为后续 Surface 设计的能力清单（非 UI）。

| 能力区域 | 承载对象 | 关键能力 |
|---|---|---|
| 经营语境（Operating Context） | Account/Brand Brief/Goal/Stage | 阶段感知、目标、策略摘要、注意力、下一步 |
| 研究洞察（Research & Insight） | Competitor/Trend/Keyword/Audience(evidence) | 外部源采集、洞察提炼、信号→选题 |
| 内容策略（Content Strategy） | Topic/Experiment/Content Mix | 选题库、实验假设、Mix 配比、栏目 |
| 内容生产（Content Production） | Note/Asset/Brief | brief、素材、封面、标题、正文、版本、审核 |
| 内容计划/日历（Content Plan） | Note + Calendar View | 排期、状态、拖拽、队列 |
| 发布分发（Distribution） | Note/Publishing Queue/Account | 定时、多平台、外部连接、赛马 |
| 数据增长（Performance & Growth） | Performance Record/Audience(evidence) | 指标、趋势、受众、搜索流量、转化、归因 |
| 用户反馈（Feedback） | Comment/DM/User Question | 分类、线索、洞察回写、互动 |
| 商业化（Commercialization，可选） | Brand Deal/Commercial Lead | 合作、报价、交付、回款、收入 |
| 团队（Team，投影） | Curis Employee/Responsibility | Workspace-scoped 责任视图 |
| 资料（Knowledge，投影） | Curis Global Knowledge/Artifact | 品牌资料、规范、素材、研究报告 |

---

# G. Professional Surface Map

> 基于真实工作，而非菜单习惯，研究应存在什么 Professional Surface。合并/拆分/降维。

## G.1 候选 Surface（研究后建议）

| Surface | 是否一等 | 合并/拆分决策 | 理由 |
|---|---|---|---|
| **Operating Overview（经营概览）** | ✅ L1 默认 | 新增（提议） | 语境恢复，回答 7 问；非 Dashboard |
| **Research & Insight（研究洞察）** | ✅ L1 | 由 Context 侧栏「信号监测」升格为 Surface | 阶段 0–3 的专业面，当前最弱 |
| **Content Strategy & Topics（内容策略/选题）** | ✅ L1（或 L2 入 Overview） | 合并选题库+实验+Mix | 阶段 4–6 |
| **Content Operating（内容运营）** | ✅ L1 | **Calendar + Production + Plan 合并为此阶段主 Surface** | 阶段 7–8；Calendar 在此为一等，而非全局默认 |
| **Publishing & Distribution（发布分发）** | L2（Content Operating 内 / 或独立） | 与 Content Operating 合并或紧邻 | 阶段 8；依赖外部连接 |
| **Performance & Growth（数据增长）** | ✅ L1 | 由 Utility「数据看板」升格为 Surface | 阶段 10–12；当前仅 Utility 偏弱 |
| **User Feedback（用户反馈）** | L1/L2（候选） | 独立 Inbox 或并入 Insight | 阶段 9；高音量，建议独立轻 Surface [CAND] |
| **Commercialization（商业化）** | ⚪ 可选模块 | 按阶段启用 | 阶段 13；小账号隐藏 |
| **Team（团队，投影）** | L2 / Scoped | 复用 Curis Employee 投影 | 阶段 15 |
| **Knowledge & Materials（资料，投影）** | L2 / Scoped | 复用 Curis Global Knowledge/Artifact 视图 | 阶段 14 |

## G.2 关键裁定 [CAND]

- **Calendar 的正确位置**：作为 **Content Operating Surface 内部的一等视图**，不是 Workspace 默认面。进入 Workspace 先见 Overview，一键进 Content Operating 见 Calendar。 [CAND]
- **Research & Insight 必须升格**：当前原型把研究藏在 Context 侧栏，研究证明专业经营的前 30% 价值在研究与策略，不能降级为侧栏。 [CAND]
- **Performance & Growth 必须升格**：数据不是「Utility 预览」，是独立经营面。 [CAND]
- **Asset/Material/Team 不重建**：复用 Curis Global Artifact / Employee 投影。 [CURIS]

---

# H. Default Workspace Analysis

> 用户进入「AI 科技」账号，默认到底看到什么？不要假设 Calendar，也不要假设 Dashboard。

## H.1 专业运营负责人每天第一次进入，最需要恢复什么 Context？[REAL]

研究归纳的 7 问（来自 brief §8）：
1. 现在处于什么阶段？（Bootstrap / Growth Validation / Stable / Commercialization）
2. 当前目标是什么？（主/次）
3. 当前策略是什么？（Mix / 实验 / 节奏）
4. 最重要的专业工作是什么？（今天该发布？该复盘？该接商单？）
5. 最新结果是什么？（最近发布表现 / 赛马结果）
6. 哪里需要关注？（限流预警 / Needs CEO / 异常）
7. 下一步是什么？（系统建议 / 待决策）

## H.2 默认 Surface 职责建议 [CAND]

**Default = Operating Overview（经营概览）**，它承载上述 7 问的语义，但：
- **不是 Dashboard**（不堆指标）；
- **不暴露经营架构图**（飞轮/五层模型是内部视角，不给用户看）；
- **可一键进入各阶段 Surface**（如「今日发布」→ Content Operating；「本月复盘」→ Performance & Growth）。

## H.3 与当前权威的张力（OPEN QUESTION）[CURIS][CAND]

- 当前 `Curis_XHS_Workspace_Instance_Spec_v1.md` §3 规定：**默认进入面 = Publishing Calendar（Calendar-Dominant）**。
- 本研究认为：Calendar-Dominant 适合「日常发布执行」高频场景，但**不适合作为「专业经营 Workspace」的默认入口**——它跳过了语境恢复，直接把用户丢进排期格。
- **建议 CEO 裁决**：默认 = Operating Overview（轻量语境恢复），Calendar 作为 Content Operating 阶段主 Surface。若维持 Calendar-Dominant，则至少 Overview 应作为 Calendar 之上的一层语境条。
- 本研究**不擅自改写** Instance Spec；此张力列为 OPEN QUESTION（见 §Z）。

---

# I. Dynamic Primary Surface Analysis

> 验证假设：Primary Surface 是否应随 Operating Context 改变？

## I.1 假设（来自 brief §9）

| Operating Context | 建议主 Surface |
|---|---|
| Bootstrap（冷启动） | Research & Insight / Positioning |
| Growth Validation | Experiment / Content Strategy |
| Stable Operation | Content Operating |
| Performance Drop | Diagnosis / Performance & Growth |
| Commercialization | Commercial Opportunities |

## I.2 验证结论 [INF][CAND]

- **假设基本成立**，但需加约束：
  - **稳定 Default（Operating Overview）+ Navigation 不可废**：用户需要可预期的主锚点，不能每次进入都「跳到不同地方」造成迷失。
  - **推荐混合模型**：Default = Operating Overview 始终在；**「当前主工作 Surface」随阶段自适应建议**（如性能骤降时 Overview 顶部提示「建议进入诊断」并一键直达），但用户可固定偏好。
  - 过度动态（每次重排 Navigation）会伤害专业用户的肌肉记忆——**稳定 + 情境建议**优于完全动态。

---

# J. Research / Insight

> 小红书专业运营的 Research Surface 应包含什么？不要做成「AI 搜索框」。

## J.1 Research 输入域 [REAL]

- **行业**：赛道容量、趋势、平台政策变化
- **用户**：目标人群画像、需求痛点、决策语言（来自 Audience Research + 评论/搜索词）
- **竞品**：竞品账号打法、爆款结构、更新频率、差异化空位
- **趋势**：平台算法/功能变化、热点话题、季节性
- **关键词 / 搜索需求**：搜索词量级、意图分布（信息型 vs 交易型）、长尾机会
- **爆款结构**：封面/标题/正文/标签的可复用元素
- **历史账号数据**：自身表现沉淀

## J.2 Research → Insight → Strategy → Topic 链路 [INF][CAND]

```
外部源(竞品/趋势/搜索/平台) + 自身数据
   → Insight（可信信号 + 证据强度）
      → Strategy（Mix / 定位调整）
         → Topic / Experiment（可执行选题 + 假设）
```

- **不是 AI 搜索框**：Research Surface 应呈现「已消化的洞察 + 来源 + 置信」，而非把搜索框扔给用户。 [CAND]
- 当前原型仅在 Context 侧栏有「信号监测」，**严重低估**了研究价值（阶段 0–3）。 [CURIS][CAND]

---

# K. Strategy / Experiment

> 专业账号增长是否需要 Experiment / Hypothesis 作为一等经营概念？

## K.1 结论：需要，建议升格为 Domain canonical object [CAND]

真实增长是**假设驱动**的：
- 「教程内容是否提升关注转化？」
- 「真人场景是否提升收藏？」
- 「标题结构是否提升点击？」

## K.2 它是什么？[INF]

- **不是** 单纯 Artifact（不是一份文档）；
- **不是** 单纯 Work（不是一次性动作）；
- **建议** = **Domain Object（Experiment）+ Operating Method（实验流程）+ Evaluation Context（评估上下文）** 三者结合：
  - Experiment 对象承载：假设、变量、对照、周期、绑定 Note；
  - Operating Method 承载：如何跑（A/B、赛马、时段对照）；
  - Evaluation Context 承载：用 Performance 数据判定有效/无效、证据强度。

## K.3 与 Curis 自治运营映射 [CAND]

Experiment 应成为「AI 自主微调」的可审计单元：AI 在规则内提出实验假设 → 跑 → 学 → 反哺策略；结构性实验（新 Mix、新平台）仍走 Needs CEO。

---

# L. Content Production

> Content Production 到底需要哪些专业能力？

## L.1 能力清单（基于真实 SOP）[REAL]

- **选题池 / Topic**：从策略承接的具体选题
- **Brief**：给创作/AI 的员工指令（受众、角度、结构、禁区）
- **素材 / Asset**：图片、参考、品牌视觉（复用 Curis Artifact）
- **标题**：双关键词（搜索词 + 情绪词）、前 5 字核心词 [COMP·XHS 2026]
- **正文**：三段式（钩子→干货→互动）、≥100 字短种草 / ≥600 字干货 [COMP·XHS 2026]
- **封面**：3:4 竖版、主体占 60%+、文字≤8 个 [COMP·XHS 2026]
- **标签**：5–15 分层（核心词+长尾+场景词）[COMP·XHS 2026]
- **版本**：多版本对照（赛马）
- **审核**：违禁词/人设/品牌，可升级 Needs CEO
- **发布状态 / 排期**：绑 Publishing Queue
- **历史内容**：归档复用

## L.2 哪些属于 Surface / Detail / 外部 Provider？[INF][CAND]

- **Surface（Content Operating 内）**：Note 编辑、Brief、审核、版本。
- **Detail（Note 展开）**：单篇的完整编辑/预览/数据。
- **外部 Capability Provider**：AI 文案生成、AI 配图、素材库、违禁词检测 API——Curis 调用外部能力，不重建。 [CURIS 原则：能力可替换不写死]

---

# M. Publishing / Calendar

> 发布与日历的专业能力；Calendar 的正确位置。证据来自 interaction-automator 专项报告（[COMP]/[REAL]，URL 见 §S.6）。

## M.1 Publishing Workflow 与审批门禁 [REAL][COMP]

行业主干一致：**草稿 → 协作评审/改稿 → 审批门禁 → 定时 → 发布 → 监测/复盘**。

- **审批门禁（Approval Gate）三种成熟模式**：Hootsuite（分层自定义审批，可设第 2/3 层）、Sprout Social（多步+外部审批人，无需登录即可评审）、Planable（为审批而生的装配线）、Later（单层轻量）。[COMP: sproutsocial.com, blog.hootsuite.com, planable.io]
- **小红书真实发布链路**：① 原生 APP/创作服务平台定时发布（≤7 天、分钟级）；② 第三方 RPA/账号绑定工具（易媒助手等，含风控护栏）；③ 开放平台企业级笔记发布 API（品牌自营同步场景，需资质）；④ 微盟/有赞小程序店铺同步（电商向）。[REAL][COMP]
- **关键纠偏**：Later/Hootsuite/Buffer/Sprout **均不支持小红书发布**（无公开自助发布 API 是根本）；候斯特是**微信公众号生态工具 + 内容风格转换**，非小红书账号接管/自动发布——勿将其列为 XHS 发布竞品。[COMP/INF]

## M.2 Calendar 的正确定位（核心回答）[CAND][COMP]

- **行业事实**：成熟套件中日历几乎都是一等公民（Later「日历优先」、Sprout 日历为 Publishing 主视图），并叠加 账号/状态/活动/渠道 过滤器与着色——即「日历 = 一级 Surface + 多维过滤器」。[COMP: sproutsocial.com, planable.io]
- **本研究裁定（与 specialist 视图的调和）**：Calendar 应作为 **Content Operating（L1 Surface）的主视图**获得顶层 prominence，但**不是 Workspace 默认入口**——默认入口让位 Operating Overview（§H）。即：Calendar 在导航上「够高」（Content Operating 是一级），但不抢「默认第一眼」。
- **冻结语义不破**：承载「Note × 时间」双主轴；`Calendar_Pattern_Spec` 的「同天多篇 / Primary 优先级 / +N 收口」规则全部保留。
- **专家团异议记录**：interaction-automator 主张 Calendar 本身应为顶层导航项（一级 Surface）。本研究维持「默认=Overview、Calendar=Content Operating 主视图」的推荐，将「Calendar 导航层级」列为 OPEN QUESTION 子项（见 Z1/Z7），由 CEO 裁决 Calendar 是否独立 L1 还是 Content Operating 内主视图。

## M.3 AI 代理的发布/调度行为 [INF][CAND]

- **可自动化（技术可行）**：选题/草稿生成、跨平台风格适配、基于历史数据的智能排期、经开放平台「笔记发布」权限代表企业账号自动提交。
- **必须 Human-in-the-loop**：品牌/商业内容终审、带商品挂载/商业报备内容（蒲公英必须平台报备）、新号/低权重账号自动发布（需先养号）、触发验证码/风控异常的发布（转人工）。
- **Curis 建议**：AI 代理定位 = 起草 + 排期建议 + 风控预检；最终发布默认需人类确认；仅「企业已获开放平台笔记发布权限 + 内容通过合规预审 + 账号养号达标」三条件齐备时，才允许受控自动发布（留审计 + 可回滚）。

---

# N. Performance / Growth

> 专业数据工作面真正需要什么？不止曝光/点赞/收藏/评论。

## N.1 指标体系（目标挂钩，非默认播放量=成功）[REAL][CURIS]

- **广度**：曝光、阅读、CTR
- **互动**：赞/藏/评/转/关注（注意：2026 XHS 有效互动权重高，关注/评论/转发 >> 点赞）[COMP·XHS 2026，REFERENCE/NEEDS VERIFICATION]
- **转化**：搜索回搜、站外转化、商单转化
- **质量**：完读、深度互动、AI 语义匹配度
- **风险**：限流、合规触线、数据异动

## N.2 Metrics → Evidence → Evaluation → Decision [INF][CAND]

```
目标 → 核心指标 → 观察(什么数据/信号) → 判断(有效/无效·证据强度) → 策略建议(具体改什么·影响哪层·可回滚)
```

- **相关≠因果**：单次爆款不立项，需重复/实验验证（对齐 Content Growth 研究 Doc6）。
- 指标与阈值**可配置**，CES 仅示例模板（已 Frozen 降级）[CURIS]。

## N.3 平台事实（2026 XHS 算法，REFERENCE / NEEDS VERIFICATION）[COMP]

- 搜索流量占比显著提升（多方来源称 50%+，高客单行业更高）—— `CONDITIONAL`（多第三方来源一致，但非官方确认数值）。
- 新人/中小号流量倾斜、阶梯流量池（初始 ~100–500 曝光）、赛马（5/30/60 分钟）—— `CONDITIONAL`。
- CES 公式（赞×1+藏×1+评×4+转×4+关注×8）出现在多个第三方来源，但**非官方公布**—— `UNKNOWN`（具体权重不得写死进产品）。
- 合规红线（AI 内容强制标注、极限词、私域暗语、三品一械）—— `VERIFIED`（蒲公英官方规则 + 平台公告，多方一致）。

> **产品纪律**：上述数值仅为 REFERENCE / NEEDS VERIFICATION，Curis 须以**动态 Platform Facts 能力**（VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE）承载，由官方来源实时验证，不硬编码。 [CURIS]

---

# O. User Feedback

> 评论/私信/搜索词/用户问题/粉丝反馈 是否独立 Surface？

## O.1 反馈进入下一轮内容策略的闭环 [REAL]

```
评论 / 私信 / 搜索词 / 用户问题
   → 分类(咨询/购买意向/负面/建议/话题)
      → 用户洞察(高频问题/需求趋势)
         → Content Opportunity(变成下一轮选题)
```

## O.2 Surface 归属判断 [INF][CAND]

- 反馈**音量高、需及时响应**，建议设**独立轻量 Surface（Feedback Inbox）**，而非并入 Insight 被淹没。
- 但 Feedback 不「自成王国」：它的产出（用户洞察/线索）**回流到 Insight 与 Content Strategy**，闭环可见。
- 当前原型无此 Surface；建议在 Overview 暴露「高频问题 / 增长需求」摘要（阶段 9 可见性）。 [CAND]

> 以下 O.3 / O.4 由 ai-comment-specialist 专项报告回填（检索日 2026-08-16）。证据等级映射：ROP→[REAL]、CE→[COMP]、RI→[INF]、CR→[CAND]。

## O.3 详细反馈管理实践 [REF: ai-comment-specialist]

### O.3.1 Inbox 统一管理实践（行业模式归纳）

**西方 SaaS 已形成「统一收件箱（Unified Inbox）」作为独立一级模块的共识**。头部工具均将跨渠道私信（DM）、公开评论（Comments）、@提及（Mentions）、评价（Reviews）聚合进单一工作台，并配套标签、路由、快捷回复、分派、SLA、CSAT：

- **Sprout Social Smart Inbox**：聚合 DMs / 帖子评论 / 提及 / 评价，自动会话线程化（同一用户多条回复折叠为一条对话），支持按类型/网络/负责人/标签过滤。 [REAL] everestx.com/tutorials/sprout-social/set-up-sprout-smart-inbox ；support.sproutsocial.com/.../20104813531533
- **Hootsuite Inbox**：跨 FB / IG / WhatsApp / LinkedIn / X / TikTok 统一收件箱，支持「关键词评论→自动触发 DM」；Advanced Inbox（企业版）加情感/语言检测。 [REAL] hs-website-next-production.vercel.app/en-gb/platform/social-media-inbox
- **Brandwatch Engage**：将各大社交网络的互动汇入单一收件箱，按互动量/情感/垃圾检测标记，可指派给个人或团队，含优先级收件箱与档案卡。 [REAL] brandwatch.com/p/social-media-management-platform
- **Mention Engage**：「all your social inboxes combined in one place」，结合监测+互动回复。 [REAL] mention.com/en/

**关键反差——小红书原生生态没有「统一互动收件箱」这个品类：**

- 千瓜、蝉小红（蝉妈妈）属于**数据分析/投放**工具，不提供私信或评论的交互式收件箱，仅做舆情正负向预警、评论内容分析（正面/中性/负面/未知）、词云。 [COMP] wap.qian-gua.com/information/detail/21 ；chanmama.com
- 蒲公英是官方达人合作（brand×creator）平台，抽 10% 服务费，不是 DM/CRM 工具；其线索能力（智域蒲公英 AI+）属第三方「线索挖掘」，非原生互动收件箱。 [INF]
- 小红书侧唯一「统一互动收件箱」是官方**私信通** + 经官方授权的三方 IM（来鼓Pro / 美洽AI / 米多客）。 [COMP]

→ 与 O.2 结论自洽：用户反馈在小红书专业运营中「缺一个独立的一级 Inbox Surface」，正是 Curis 可补位的空白。 [INF]

### O.3.2 评论/私信分类体系（情感 × 意图 × 自动路由）

- **情感分层**：Sprout 将每条入站消息判定为 Positive / Negative / Neutral / Unknown；Hootsuite Advanced Inbox 加语言检测；Brandwatch 加垃圾检测。 [REAL]
- **标签/话题体系**：Sprout Tag Collections（Customer Care：差评/退款/预约；Product Feedback：按产品二次打标），多层叠加、过滤、导出；Hootsuite Topics + tag automations + skill-based routing；均支持 auto-resolve 低优会话。 [REAL]
- **AI 自动路由**：Hootsuite AI classifiers 按意图与上下文自动分类并路由；Sprout Automated Rules 按关键词/网络/情感自动打标与分派；来鼓Pro/美洽AI 用意图识别+情绪分析+自动打标签+「顾客印象」摘要。 [COMP]
- **与我方信号 schema 的对接**：上述「情感/意图标签/自动路由」正是 `intent_class`（是什么）与 `intent_tier`（多热）的落地范例——西方工具把情感与意图/技能路由拆开处理的做法，印证「两层模型分离」设计，避免 tier 污染。 [INF]
- **小红书原生分类**：私信通提供「客资标注」「意向评论识别」（问地址/价格/产品/服务自动抓取）、「进线来源」标注。 [COMP]

### O.3.3 线索提取与 CRM 流转

- **线索提取**：私信通实时抓取笔记下「意向评论」，可一键私信触达，把浅层意向转为深度沟通；「客资标注 + 线索管理工具」沉淀线索。 [REAL] m.xiao-ad.com/jd/3422.html
- **→ 自有 CRM 流转**：私信通提供 API 推送与回传（小红书 → 商家自有 CRM）。 [REAL]
- **三方工具**：来鼓Pro / 美洽AI 支持客资秒级推送至企业微信 / 钉钉 / 飞书 / 内部 CRM，自动发送合规「留资卡/名片卡」。 [COMP]
- **⚠️ 蒲公英澄清（重要，避免误判 Surface 归属）**：蒲公英是官方**达人合作**平台（品牌方 × 创作者投放），抽佣 10%，不承载私信/评论/线索管理；私信通（非蒲公英）才是官方 CRM 桥接件；「智域蒲公英 AI+」属第三方线索挖掘插件。在信号归属上，蒲公英相关信号应归入 **Growth/Collaboration Surface**，而非 Feedback Inbox。 [INF]

### O.3.4 小红书专业号「私信通」能力边界与监管红线（2026 最新）

**私信通能力边界（官方）：**
- 全域咨询统一承接：笔记页 / 主页 / 直播 / 搜索等多入口私信统一进私信通
- 多客服分线：1 个账号可分线至最多 **200 个客服子账号**，主账号可见全部并管理权限
- 多端操作（网页/客户端/APP），强提醒（弹窗/语音/标签）
- 话术库、欢迎语 + 自动回复、笔记来源追踪、私信回复意向评论
- **私信通 AI 小助手**：对「意向评论」自动识别并私信回复，两种模式——默认话术（≤50 字）/ 模型生成；若人工正在处理则不自动回复
- 客资标注、获客工具（商家名片/留资卡/表单/商品/小程序/笔记组件）、线索管理工具、API → 自有 CRM
- 2026 新版：私信通 / 私信服务组件 / 获客工具 / 咨询分 / 线索管理 已集合至专业号平台【咨询服务】模块统一管理。 [REAL]

**监管红线（2026-05 留资新规，三大红线，违规处罚升级：首次限流 7 天，三次违规永久封号，矩阵账号连带追责）：** [COMP] baiyangseo.com/blog/1500.html

1. **合规引流红线**：严禁私信/评论直接发微信号、手机号、谐音暗语（如「薇❤」）、站外链接；仅支持通过官方留资卡/名片卡导流；诱导用户跳转第三方平台交易直接封号。
2. **避免重复私信红线**：AI 算法严查「非人感」回复；高频重复话术、短时间批量私信、回复间隔 < 5 秒均判垃圾信息触发限流；**单日主动私信超 50 人即进入频率监控名单**。
4. **多账号同质化红线**：KOS 矩阵号严禁发布重复内容、共用话术模板、同一 IP 批量操作；多账号协同导流、内容高度相似判为营销矩阵，全账号降权或封禁。

**私信频次限制（硬规则）：** [COMP] cloud.tencent.com/developer/article/2729477

- 对方关注/回复你之前，24 小时内最多给同一陌生用户发 **1 条**私信
- 普通账号每天最多主动私信 **5 位**陌生用户（未回复则不可继续）
- 企业蓝 V 每天上限 **20 位**；双向关注不限条数，但官方口径仍「不得引导至站外平台」

**私信服务组件（欢迎语/自动回复）边界：** [COMP]

- 专业号私信规则（2025-01 起）：后台自动回复及欢迎语中禁止出现联系微信及联系电话
- 私信服务组件限额：欢迎语 + 自动回复 ≤ **3 组 Q&A**，问题 ≤ 5 字 / 答案 ≤ 100 字
- 《小红书社区规范》（2026 版）：笔记/评论/个人资料/私信中留或暗示加微信/QQ/二维码均属违规导流，限制账号功能

→ **对 Curis 的硬约束（设计必读）**：任何「评论→私信追粉」「自动留资」类能力，**必须**走官方授权接口 + 官方留资组件，且须内置防封（真人级语气、频次/间隔控制、敏感词拦截）。非官方脚本/插件违规率高达 68%。 [CAND] 这直接定义了 Feedback Inbox 的「自动化上限」——自动回复/线索卡只能在合规骨架内运行。

## O.4 反馈管理工具矩阵 [REF: ai-comment-specialist]

> 列定义：统一管理=是否聚合多渠道私信+评论+提及于单一收件箱；分类=是否具备情感/意图/标签分类；线索=是否支持线索提取与 CRM 流转；自动回复=是否支持欢迎语/自动回复/AI 接待；XHS 支持=是否原生支持小红书。
> ✓=完整支持 △=部分/间接支持 ✗=不支持/不适用

| # | 工具 | 统一管理 | 分类 | 线索 | 自动回复 | XHS 支持 | 证据 |
|---|---|---|---|---|---|---|---|
| 1 | **Sprout Social Smart Inbox** | ✓（DM/评论/提及/评价统一，会话线程化） | ✓（情感 P/N/Neu/Unk；Tag Collections；Saved Views） | △（联系档案+CRM 集成） | ✓（Saved Replies、Chatbots、AI 建议回复、Automated Rules） | ✗ | [COMP] support.sproutsocial.com/.../20104813531533 |
| 2 | **Hootsuite Inbox** | ✓（FB/IG/WhatsApp/LinkedIn/X/TikTok/Threads/YouTube） | ✓（AI classifiers 意图路由；Topics；skill-based routing；情感/语言检测） | △（Salesforce 双向同步） | ✓（生成式 AI chatbot、Saved Replies、auto-resolve） | ✗ | [COMP] hootsuite.com/platform/social-media-inbox |
| 3 | **Mention Engage** | ✓（all social inboxes combined） | △（监测情感；互动侧分类弱于 Sprout） | △（互动回复为主，线索能力有限） | ✓（发布+回复，自动化较弱） | ✗ | [COMP] mention.com/en/ |
| 4 | **Brandwatch Engage** | ✓（各大网络互动汇入单一收件箱） | ✓（按互动量/情感/垃圾标记；优先级收件箱） | △（Helpdesk 集成） | △（Engage 回复） | ✗ | [COMP] brandwatch.com/p/social-media-management-platform |
| 5 | **千瓜** | ✗（纯数据分析，无交互式收件箱） | △（舆情正负向预警；评论内容分析；词云） | ✗（舆情监测可定位用户但非线索管理） | ✗ | ✓（小红书数据分析） | [COMP] wap.qian-gua.com/information/detail/21 |
| 6 | **蝉小红（蝉妈妈）** | ✗（数据分析：找博主/爆款笔记/品牌投放监控） | △（舆情/热搜词/笔记分析） | ✗ | ✗ | ✓（小红书数据分析） | [COMP] chanmama.com |
| 7 | **蒲公英** | ✗（官方达人合作平台，非 DM/CRM） | ✗ | △（智域蒲公英 AI+ 为第三方线索挖掘，非原生） | ✗ | ✓（官方 creator 合作） | [INF] pgy.xiaohongshu.com |
| 8 | **小红书私信通（官方）** | ✓（全域咨询统一承接；多客服分线≤200 子账号；多端） | ✓（客资标注；意向评论识别；进线来源标注） | ✓（线索管理工具；API→自有 CRM） | ✓（欢迎语+自动回复≤3 Q&A；AI 小助手意向评论回复） | ✓✓（原生官方） | [REAL] m.xiao-ad.com/jd/3422.html |
| 9 | **来鼓Pro** | ✓（小红书/抖音/视频号/快手/微信等聚合；评论+私信统一） | ✓（意图识别；情绪分析；自动打标签；「顾客印象」摘要） | ✓（客资秒级推送企微/钉钉/飞书/CRM；留资卡） | ✓（AI 托管/工作流/人工三模式；评论追粉；智能发卡；7×24 人感接待） | ✓（小红书首家官方授权三方 IM，厂商自述） | [COMP] laigu.com |
| 10 | **美洽AI** | ✓（小红书矩阵账号统一接入；私信+公开评论单工作台） | ✓（关键词/情绪触发转人工；AI 顾客印象摘要；智能分配） | ✓（留资卡/名片卡合规收集；秒级同步企微/飞书/钉钉/CRM） | ✓（大模型获客机器人；评论自动回复/私信秒回/自动追粉） | ✓（首批官方授权/第一家合作三方 IM，厂商自述） | [COMP] meiqia.com |
| 11 | **米多客** | ✓（50+ 账号聚合；自研大模型；意图识别 96.8%，厂商自述） | ✓（NLP 意图识别） | ✓（全链路私域获客/留资） | ✓（真人级 AI 对话；内置防封策略） | ✓（官方认证，厂商自述） | [COMP] — |

**矩阵读法（对 Curis 的衔接提示）：**

1. **西方四强 ≠ XHS 可用**：Sprout/Hootsuite/Mention/Brandwatch 均无小红书原生接入，其「统一 Inbox + 分类 + 路由 + CRM」是**模式证据**，证明 Feedback Inbox 应作为独立 Surface，而非依附 Insight/Growth/Content。 [INF]
2. **XHS 原生分析工具不碰互动**：千瓜/蝉小红只做数据与舆情，缺交互式收件箱；蒲公英是投放合作，非反馈管理。→ 印证 O.2「独立 Feedback Inbox」的空白机会。 [INF]
3. **XHS 唯一合规闭环 = 私信通 + 官方授权三方 IM**：私信通是官方底座（统一管理+分类+线索+API→CRM），来鼓Pro/美洽AI/米多客是官方授权之上的 AI 增强层。Curis 若进入此层，必须走**官方接口授权 + 官方留资组件 + 防封**，否则触发 O.3.4 三大红线。 [CAND]
4. **证据可信度提示**：来鼓Pro/美洽AI/米多客的「官方授权」为**厂商自述**（未独立核验官方授权清单）；其 AI 能力数值（如意图识别 96.8%、留资率 +38%）属厂商营销口径，引用时建议降权为「厂商声称」。 [INF]

---

# P. Commercialization

> 不要忽略商业化。

## P.1 成熟账号经营中的商业化对象 [REAL][COMP]

- **品牌合作 / 商单**：蒲公英平台任务（定制/招募/共创/新芽）[COMP·XHS 2026]
- **商务线索 / Commercial Lead**：私信/表单咨询（专业号「私信通/咨询分」）[COMP]
- **报价 / 合作状态 / 内容交付 / 回款 / 收入**：蒲公英数据看板 + 财务
- **商业价值**：通过聚光/千帆/薯条放大自然流量 [COMP]

## P.2 判断：什么阶段需要独立 Surface？[INF][CAND]

- **小账号（Bootstrap/Growth）**：隐藏商业化 Surface，避免干扰内容建设。
- **成熟账号（Commercialization 阶段）**：启用 Commercialization 作为可选模块（Optional Module），含 Brand Deal / Commercial Lead 对象。
- **是否属于 Capability Package 可选模块？** 是——按经营阶段启用，不默认全开。 [CAND]

## P.3 与 Curis 边界 [CURIS]

- 财务/结算属 Reserved（Curis v1 暂不建设完整财务）；商业化 Surface 聚焦「合作机会/商单管理/交付状态」，回款接入外部（蒲公英/财务系统）。

---

# Q. Team Projection

> Workspace 内 Team Surface 真正需要显示什么？复用 Curis Employee/Responsibility，不重造。

## Q.1 原则 [CURIS]

- **复用 Curis 组织层**：Employee、Responsibility、Handoff、Needs CEO 是 Company OS 能力，XHS 不重造员工系统。
- **XHS Team View = Workspace-scoped projection**：显示「哪些责任正在被谁执行、卡在哪、谁 needs_ceo」。

## Q.2 需要的专业信息（投影）[INF][CAND]

- 当前各责任节点（研究/选题/生产/审核/发布/数据）的 Current Executor 与状态
- 待 Handoff / Needs CEO 列表
- 阶段吞吐（哪些环节是瓶颈）
- **不显示**：员工列表常驻侧栏、员工顶部 tab（已 Frozen 禁止）[CURIS]

---

# R. Knowledge / Materials

> Workspace scoped 资料 vs Curis Global Knowledge / Artifact。

## R.1 区分 [CURIS][INF]

- **Curis Global Knowledge / Artifact System**：跨 Workspace 的通用知识库、素材库、方法论。
- **XHS scoped professional view**：仅「本账号相关的」品牌资料、规范、研究报告、素材的**投影/过滤视图**。
- **不重造 XHS Knowledge Base**：XHS 的资料视图是 Curis Global 的过滤，不是独立库。

## R.2 Workspace 资料可能包含 [REAL]

品牌资料、账号资料、内容规范、素材（→Artifact）、历史内容（→Note 归档）、研究报告（→Knowledge）、竞品资料（→Research）、模板、Evidence、运营方法（→可复用 Strategy/Experiment）。

---

# S. External Provider Boundary

> 真实接管小红书账号后，Workspace 需要的平台连接能力边界（Product Capability Boundary，不实现）。证据来自 interaction-automator 专项报告（[COMP]/[REAL]，检索日 2026-08-21）。

## S.1 连接能力清单与平台真实边界

| # | 能力 | 依赖外部 Provider | 平台事实状态 |
|---|---|---|---|
| 1 | 账号状态/身份（专业号/蓝V/实名） | 是（小红书账号体系） | `VERIFIED`：专业号=商业入场券（蓝V/店铺/直播/KOS） |
| 2 | 授权 OAuth | 是（开放平台 OAuth2 授权码） | `VERIFIED`（企业应用）：仅 authorization code；access_token 2h；个人开发者受限 |
| 3 | 内容发布 API | 是（开放平台/专业号） | `CONDITIONAL`（核心）：端点存在但仅企业白名单/特定场景，审核严、需合规协议 |
| 4 | 笔记数据获取（详情/互动/评论） | 是（开放平台/蒲公英） | `VERIFIED`（企业）：读取类接口对企业开放 |
| 5 | 阅读/曝光数 | 是（蒲公英/第三方聚合） | `CONDITIONAL`：阅读/曝光属蒲公英数据面，非消费者 API |
| 6 | 评论/私信 | 是（原生+专业号私信通） | `VERIFIED`：专业号提供私信入口+线索管理；自动回复受限、监管严 |
| 7 | 商业平台（蒲公英/聚光/千帆） | 是（独立平台） | `VERIFIED`：蒲公英(合作)/聚光(投放)/千帆(电商) 独立后台，非统一 API |
| 8 | 小程序/店铺接入 | 是（小程序开放能力） | `VERIFIED`：微盟/有赞经小程序方案开店、同步商品/订单 |

## S.2 Curis 内可完成 vs 必须依赖外部 Provider [INF][CAND]

- **Curis 内可完成（不碰平台黑盒）**：草稿/素材库、协作评审、审批门禁、日历排期、跨账号视图、内容风格转换(AI)、风控护栏规则、基于已授权数据的可视化。
- **必须依赖外部 Provider**：真实发布动作（开放平台 API 企业资质 / 原生定时 / RPA 第三方）、深度数据（蒲公英/聚合）、商业合作/投放/电商（蒲公英/聚光/千帆）、小程序开店（小程序开放能力）。

## S.3 小红书平台能力边界（VERIFIED / CONDITIONAL / UNKNOWN）[COMP]

- `VERIFIED`：开放平台存在(企业资质)、OAuth2 授权码、读取类接口对企业开放；专业号体系；蒲公英/聚光/千帆/灵犀/直播中控台真实存在；APP 原生定时(≤7天)。
- `CONDITIONAL`：笔记发布 API（端点存在但高度受限、非公开自助）；阅读/曝光仅蒲公英/聚合可得；自动互动受强监管、无安全自助 API。
- `UNKNOWN`：发布 API 具体准入门槛（不同来源表述不一，最稳妥=对企业应用存在但高度受限）；RPA 矩阵工具「小红书自动发布」稳定性（依赖平台风控演进）。

## S.4 重要纠偏（避免误把第三方误传当事实）[INF]

- 「西方工具能发小红书」是**误传**——Later/Hootsuite/Buffer/Sprout 官方支持列表不含小红书。
- 「候斯特是小红书自动发布工具」需修正——候斯特是**微信公众号生态工具**，其小红书相关能力是「多平台内容风格转换(输出小红书腔调文案)」，非账号接管/自动发布。
- 真正的小红书发布自动化竞品：① 原生 APP/创作服务平台定时发布；② 易媒助手等 RPA/账号绑定工具；③ 开放平台企业级笔记发布 API；④ 微盟/有赞小程序店铺同步(电商向)。

## S.5 对 Curis 启示 [CAND]

1. 日历=一级 Surface + 多维过滤器（参考 Later/Sprout）。
2. 审批门禁内建（草稿→待审→已排→已发，支持多层+外部干系人）。
3. 发布能力分层对接：优先开放平台企业 API；兜底原生定时(半自动)；不承诺 RPA 无 API 自动发布(风控高危、稳定性 UNKNOWN)，若做须内置独立环境/IP/养号/错峰护栏+显著风险提示。
4. 数据分层获取：互动走开放平台，阅读/曝光走蒲公英/聚合。
5. 自动化规则=调度+审批+数据+风控护栏(频率上限/错峰/去重/养号/转人工)，非无监督生成/互动。
6. AI 代理守门：默认 Human-in-the-loop，仅企业资质+合规预审+养号达标时开放受控自动发布(审计+可回滚)。

## S.6 证据 URL 清单（节选·完整见 specialist 报告）

- 竞品审批/日历：sproutsocial.com/insights/publishing-calendar/ ；blog.hootsuite.com/social-media-approval-workflow/ ；planable.io
- 小红书开放能力：cndev.cn/platform/xiaohongshu-open ；m.php.cn/faq/2511984.html(发布端点) ；ask.csdn.net/questions/9637727(无公开发布 API)
- 商业工具：guangzhou0543572.11467.com/product/47082954.asp(白皮书) ；justoneapi.com/en/blog/xiaohongshu-vs-pugongying(数据边界)
- 真实实践：yimeizhushou.com(易媒助手) ；developer.aliyun.com/article/1712916(OpenClaw 自动发布) ；weixinhost.com/blog/one-post-multi-platform-ai-adapter/(候斯特=风格转换)
- 不可靠(已纠偏)：jiangyoupai.com(称西方工具支持小红书→误传)

---

# T. Competitor Matrix

> 真实竞品格局（由 signal-miner 专项研究补充完整矩阵与 URL）。此处给出研究团队已确认的归纳框架与初步结论。

## T.1 类别覆盖（brief §19 A–G）[COMP]

- **A. Social Media Management**：Hootsuite / Sprout Social / Buffer / Later / Planable / CoSchedule
- **B. Content Planning / Publishing**：Later / Tailwind / Planable / 小红书创作服务平台
- **C. Social Analytics**：Iconosquare / Keyhole / Brandwatch / Talkwalker / 千瓜 / 灰豚 / 新红
- **D. Creator / Influencer**：蒲公英 / 千瓜 / 蝉妈妈 / Upfluence / GRIN / Aspire
- **E. AI Social Agents**：OwlyWriter / Sprout AI / Later AI / Jasper / Predis.ai / Lately / Ocoya / ChatGPT-Claude 代理
- **F. 中国/小红书导向**：候斯特 / 微盟 / 有赞 / 千瓜 / 蝉妈妈 / 小红书专业号·千帆·蒲公英
- **G. Marketing / Growth platforms**：HubSpot / Salesforce MC / Adobe / 聚光 / 乘风

## T.2 行业已解决的（复用而非重造）[COMP][INF]

- 日历+拖拽排期（Later Visual Calendar）→ Curis Content Operating/Calendar
- 收件箱统一管理多平台互动（Sprout Inbox）→ Curis Feedback Inbox
- 可配置 Analytics 模板（千瓜/Iconosquare）→ Curis Performance & Growth
- 选题灵感/爆款拆解（新红/千瓜）→ Curis Topic & Signal Library
- 审核+Handoff（小红书违禁词+蒲公英规范）→ Curis Review Gate + Needs CEO

## T.3 行业缺口（Curis 应填补）[COMP][CAND]

- **国际工具普遍不支持小红书**（中国平台封闭）→ Curis 以 XHS Instance 专门承载。
- **研究/策略/实验是弱项**：多数工具把研究降级为「搜索框/监听」，无「洞察→策略→实验」链路 → Curis 升格 Research & Insight + Experiment。
- **自治运营缺失**：工具止于人类判断（策略方向、合规、报价、归因）→ Curis 的 Autonomous Operating + Decision Gate 是差异化。

> 以下 T.4 / T.5 / T.6 由 signal-miner 专项报告回填（检索日 2026-08-16）。

## T.4 竞品能力矩阵总表（19 个代表性竞品 × 11 列）

| # | 竞品（类目） | 导航/IA | 核心对象 | 日常工作流 | 分析能力 | 内容能力 | 团队/协作 | 知识沉淀 | 商业化 | 自动化 | 对小红书支持 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Hootsuite**（A） | 流(Streams)列式 Dashboard + 多账号切换 | 多平台账号/帖子/消息/流 | 排程发布 → 收件箱互动 → 流监控 | 内建 Analytics + 自定义报告 | 内容库、批量排程、OwlyWriter AI | 多席位、审批、角色权限 | 内容库模板、最佳时间 | $99/mo 起 | 自动排程、AI 文案 | ❌ 不支持 | [COMP] |
| 2 | **Sprout Social**（A） | Smart Inbox 统一收件箱 + 日历视图 | 对话/任务/标签/报告 | 收件箱处理 → 排程 → 审批 | 强 Listening + 标签化报告 | 内容日历、草稿、Sprout AI 智能回复 | 协作任务、审批流、CRM 集成 | 标签体系、Saved replies | $249/mo 起 | ViralPost 最佳时间、智能自动回复 | ❌ 不支持 | [COMP] |
| 3 | **Buffer**（A） | 频道侧栏 + Publish/Engage/Analyze | 频道/帖子/互动 | 排程 + Community 互动收件箱 | Analyze 基础指标 | 草稿、Ideas、AI Assistant | 简易协作、审批 | 内容 ideas 板 | Free / $6·频道/mo | 排程、AI 改写 | ❌ 不支持 | [COMP] |
| 4 | **Later**（A/B） | 视觉化日历(Visual Planner) + Linkin.bio | 媒体库/帖子/链接页 | 拖拽排程 + 媒体库管理 | 基础分析 | 视觉排程、Media Notes、Later AI | 多席位、审批 | 媒体库、最佳时间 | $25/mo 起 | 自动排程、AI 文案/标签 | ❌ 不支持(IG/TikTok/Pinterest 为主) | [COMP] |
| 5 | **Tailwind**（B） | 平台分栈(Pinterest/IG/FB) + SmartSchedule | Pin/Post/Tribes 社群 | 排程 + 社群互推 | 基础分析、Profile 评分 | Tailwind Create、Ghostwriter AI | 多席位 | Tribes 内容库 | Free / $14.99–49.99/mo | SmartSchedule、AI 生成 | ❌ 不支持(Pinterest 官方伙伴) | [COMP] |
| 6 | **小红书创作服务平台**（B/F） | 数据中心/笔记灵感/内容管理/粉丝中心/创作学院 分模块 | 笔记/粉丝/数据 | 创作 → 发布 → 看数据 → 优化 | 笔记数据、粉丝画像、搜索词流量 | 笔记灵感、创作工具、话题 | 个人为主(专业号团队功能弱) | 创作学院、灵感库 | 免费(官方) | 弱(官方无第三方自动化) | ✅ 原生(仅 XHS) | [COMP] |
| 7 | **Iconosquare**（C） | 仪表盘 + 标签/Conversations 收件箱 | 帖子/受众/标签 | 监控 + 报告 + 互动 | 强(IG/FB/LinkedIn/TikTok/Threads) | 排程、标签 | 多席位、Conversations 收件箱 | 标签、基准 | 订阅制 | 报告自动生成、排程 | ❌ 不支持 | [COMP] |
| 8 | **Keyhole**（C） | 监测项目 + 实时仪表盘 | 话题标签/关键词/账号 | 监听 + 报告 + 竞品对标 | 强监听(X/IG/TikTok/FB/YT/新闻博客论坛) | 弱(非发布工具) | 多席位、白标报告 | 历史数据、基准 | $59/$199/$999 三级 | 自动报告、预警 | ❌ 不支持(监听列表无 XHS) | [COMP] |
| 9 | **Brandwatch / Talkwalker**（C） | 查询 + 仪表盘 + 警报 | 提及/主题/情绪 | 全域监听 + 危机预警 | 顶级(全网+多语种+AI 情绪) | 几乎无(纯聆听) | 企业级席位 | 主题模型、趋势库 | 企业报价 | 警报、AI 洞察 | ⚠️ 部分([INF]可监听 XHS 公开提及，非原生发布/互动) | [COMP]/[INF] |
| 10 | **千瓜**（C/D/F） | 数据大盘 + 选题/达人/笔记 三大模块 | 关键词/达人/笔记/品牌 | 选词 → 找达人 → 监测笔记 → 复盘 | 强(XHS 种草数据、品牌声量、转化) | 选题库、爆文拆解 | 企业席位、报告 | 行业库、达人库 | ¥1299/mo 标准版(78% 企业) | 监测、报告 | ✅ 原生 XHS 专精 | [COMP] |
| 11 | **灰豚**（C/F） | 直播/达人/笔记 监测台 | 达人/直播/笔记 | 找达人 + 爆文复用 | 中(爆文、达人榜) | 爆文复用、脚本 | 小团队席位 | 爆文库 | ¥99–199/mo 入门 | 榜单、监测 | ✅ 原生 XHS(抖音+小红书) | [COMP] |
| 12 | **新红**（C/F，新榜旗下） | 红人/笔记/词 监测 | 红人/笔记/关键词 | 监测 + 分钟级预警 | 强(分钟级监测、性价比) | 选题、红人 | 企业席位 | 红人库、词库 | ¥199–999/mo | 分钟级监测、预警 | ✅ 原生 XHS 专精 | [COMP] |
| 13 | **蒲公英**（D/F） | 广场/订单/数据 三大模块 | 报备笔记/达人/订单 | 选达人 → 下单 → 托管笔记 → 数据 | 达人画像、笔记数据 | 报备笔记托管 | 品牌+机构+M_CN | 达人库、行业 | 官方抽佣(XHS 唯一合规种草) | 订单流、数据回传 | ✅ 原生 XHS 官方 | [COMP] |
| 14 | **Upfluence / GRIN / Aspire**（D） | 达人发现 + CRM + 流程 | 达人/活动/内容 | 发现 → 招募 → 管理 → 度量 | 达人 ROI、内容表现 | 内容审核、UGC | 品牌营销团队 | 达人库、活动模版 | 企业报价 | 招募、付款、度量 | ⚠️ 部分([INF]可管理 XHS 达人活动，依赖手动/有限 API，非发布) | [COMP]/[INF] |
| 15 | **AI 社媒代理群**（E：OwlyWriter/Sprout AI/Later AI/Jasper/Predis.ai/Lately/Ocoya） | 集成于母平台或独立生成器 | 文案/创意/视频 | 输入主题 → AI 生成 → 编辑 → 发布 | Predis/Lately 带表现分析；其余弱 | 强(多模态文案/图/视频) | 多席位(企业版) | 提示库、品牌语气 | 订阅(Jasper $39+；Predis/Ocoya 低阶) | 批量生成、部分自动发布(Predis 自动发) | ❌ 无原生(Predis 自动发 IG/TikTok/Pinterest/FB/LinkedIn；无 XHS) | [COMP] |
| 16 | **候斯特 / 微盟 / 有赞**（F） | SCRM 模块化(客户/社群/商城) | 私域客户/社群/商品 | 引流 → 私域运营 → 转化 | 私域数据、转化漏斗 | 群发、素材 | 销售/运营团队 | 客户标签、SOP | SaaS + 抽佣 | SOP、群发、打标 | ⚠️ 间接([INF]微信生态为主；小红书仅引流，无原生经营 API) | [COMP]/[INF] |
| 17 | **小红书专业号·千帆**（F） | 专业号后台 + 千帆 商家中心 | 店铺/商品/粉丝/笔记 | 开店 → 上品 → 笔记/直播 → 交易 | 店铺数据、流量、转化 | 图文/视频笔记、直播 | 商家多角色 | 经营学院 | 官方(保证金+佣金) | 官方有限工具 | ✅ 原生 XHS 官方经营 | [COMP] |
| 18 | **HubSpot / Salesforce MC / Adobe**（G） | 营销中枢 + Social Inbox / Social Studio | 联系人/活动/帖子 | 发布 + 互动 + 归因 | 强(归因、ROI) | 排程、Inbox(FB/IG 等) | 营销/销售全团队 | CRM、流程库 | 订阅+按量 | 工作流、打分 | ❌ 不支持(SF Social Studio 监听发布 X/FB/LinkedIn/YT/Pinterest 等，无 XHS；Adobe AEM Social 同) | [COMP] |
| 19 | **聚光 / 乘风**（G） | 聚光 投放台 + 乘风 电商投放 | 广告计划/关键词/商品 | 建计划 → 投放 → 优化 → 复盘 | 投放数据、搜索词、ROI | 创意、落地页 | 投放团队 | 行业定向包 | 官方广告消耗 | 智能托管、出价 | ✅ 原生 XHS 广告闭环 | [COMP] |

> Planable / CoSchedule 作为「画布式协作」与「单一营销日历」代表，能力已被 #1–#4 行（Hootsuite/Sprout/Buffer/Later）覆盖，未单列以免冗余。

## T.5 按类目的关键结论（对应 §T.2 行业已解决 / §T.3 行业缺口）

- **A 社媒管理（国际）**：已解决多平台统一收件箱(Inbox/Streams)、排程、审批、基础报告。缺口：无一支持小红书；XHS 用户被排除在「统一收件箱」范式之外。
- **B 内容规划/发布**：已解决视觉化日历、最佳时间、AI 文案。缺口：XHS 原生创作服务平台仅做「创作→发布→看数」单点，无跨账号协作日历、无第三方自动化接口。
- **C 社媒分析**：已解决监听、情绪、基准、竞品对标。缺口：千瓜/灰豚/新红 填补了 XHS 种草数据，但「监听→线索→互动」闭环仍断开；国际监听工具(Brandwatch/Talkwalker)仅能「看」XHS 提及，不能「动」。
- **D 创作者/达人**：已解决达人发现、CRM、ROI 度量。缺口：蒲公英是 XHS 唯一合规种草通道，但创作者侧的「反馈/评论/DM 信号」未被结构化沉淀为经营线索。
- **E AI 社媒代理**：已解决多模态内容批量生成、部分自动发布。缺口：所有 AI 代理均不覆盖 XHS 原生发布与互动；XHS 经营侧的「代理式洞察→自动行动」完全空白 —— **Curis 的最高优先级机会点 [CAND]**。
- **F 中国/小红书导向**：已解决私域 SCRM、XHS 官方经营/种草/数据工具链。缺口：工具高度「烟囱化」（创作/数据/种草/交易分属不同官方或三方产品），缺乏统一 Workspace 把「反馈信号→内容→种草→转化」串成一条经营流。
- **G 营销/增长**：已解决归因、ROI、广告闭环（聚光/乘风为 XHS 原生）。缺口：国际 MarTech 巨头完全缺席 XHS；XHS 原生广告与「社媒互动/反馈经营」尚未在统一工作台内打通。

## T.6 核心缺口 thesis（Curis 差异化锚点）

1. **XHS 被国际工具集体排除**：Hootsuite、Sprout、Buffer、Later、Iconosquare、Keyhole、HubSpot、Salesforce、Adobe、全部 AI 代理 —— 均不支持小红书（官方文档核验；Sprinklr 同样仅 WeChat/Sina Weibo/Tencent Weibo，无 Xiaohongshu）。
2. **XHS 原生工具「强数据、弱经营流」**：千瓜/灰豚/新红/蒲公英/千帆/聚光/乘风各自解决单点，但无人把「评论/DM/搜索词/品牌提及」信号统一聚合、分级、并驱动内容/种草/投放动作。
3. **信号→行动闭环是空白**：这正是 Curis 的差异化锚点 —— 以统一 Signal Schema 为中枢，打通「信号挖掘→线索化→内容/互动/投放响应」。

---

# U. AI Agent Matrix

> 成熟 AI Social/Marketing Agent 如何处理 Goal→Research→Strategy→Content→Scheduling→Publishing→Analytics→Learning→Human approval（由 brand-monitor 专项研究补充完整矩阵与 URL）。

## U.1 初步归纳 [COMP][INF]

- **Content generation**：成熟（Jasper/Copy.ai/Predis/Lately 生成文案/图文），但多为「建议+人工定稿」。
- **Scheduling/Publishing**：半自动（Later/Hootsuite 定时+审批），仍需人类确认发布。
- **Analytics**：自动报表，但**因果判断/策略建议仍人类做**。
- **Research/Strategy**：弱——多为搜索摘要，无「业务适配加权」的策略推导。
- **Learning**：浅——基于模板复用，非真正的实验闭环。

## U.2 Human-Judgment Gap（Curis 要超越的点）[COMP][CAND]

当前 AI 代理**仍要求人类判断**的环节：
1. **策略方向**（定位/ Mix / 阶段切换）
2. **品牌调性与合规风险**（敏感表达、限流边界）
3. **商业化报价与合作决策**
4. **跨平台/跨域归因**（搜索→转化链路）
5. **因果判断**（相关≠因果，避免过拟合）

> Curis 的应对：AI 员工在**规则内自主推进**（含实验假设、微调、临时加源），只在 **Decision Gate（Needs CEO）** 出现；结构性变化（新 Mix、新平台、 repositioning）走 CEO。这与 Content Growth 研究的 AI/CEO 边界一致。

> 以下 U.3 矩阵与 U.4 模式归纳由 brand-monitor 专项报告回填（检索日 2026-08-16）。

## U.3 AI Social/Marketing Agent × 九环运营链矩阵（11 个代表性产品）

| # | 产品 / Agent | 产品定位 | Goal 处理 | Research 能力 | Strategy 能力 | Content 生成 | Scheduling | Publishing | Analytics | Learning | Human-approval 环节 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Hootsuite / OwlyWriter AI** | 企业级社媒管理平台内嵌 AI 写作 | 用户设定目标/话题，AI 围绕目标生成文案与日历 | 行业趋势话题建议（基于 Talkwalker 监听） | 内容日历从提示/URL 一键生成 | OwlyWriter 多平台文案 / 图片(beta) / repurpose 旧帖 | AutoSchedule AI 按历史互动排最优时段 | 内嵌发布 + Team 计划审批流 | 表现分析 + 监听份额 | OwlyGPT 学历史帖语气/受众风格 | Team/Business 计划审批流，发布前需确认 | [REAL] blog.hootsuite.com/ai-copywriting ; blog.hootsuite.com/ai-powered-content-creation |
| 2 | **Sprout Social / Trellis** | 社媒情报平台 + 代理式 AI Trellis | 自然语言提问，Trellis 转战略情报与行动方向 | 实时监听 / 竞品情报 / 叙事趋势检测 | 跨平台战略建议 + Trellis Studio 定制 AI 工作流 | 基于实时信号创作/发布（建议层，非批量生成） | 融入发布工作流（信号驱动排期） | 发布模块集成；Trellis 主做情报而非自动发 | 高管级执行摘要 / 情感 / 跨网对比 | 持续从社媒原生数据学习 | 情报→人类决策；风险预警人工介入 | [REAL] sproutsocial.com/ai-agent/ ; investors.sproutsocial.com/.../Trellis-Is-Helping-Reshape-How-Social-Teams-Prove-Their-Value |
| 3 | **Later AI** | 视觉优先社媒排期 + AI | 用户设内容支柱/目标，AI 辅助 | Future Trends 趋势预测（有限，非竞品深研） | Ideas tab 内容构思 | Caption Writer / 多平台改写 / Hashtag | Best Time to Post（分 Reels/Feed/Stories） | 直发 TikTok / IG Reels / YouTube Shorts | 自定义分析仪表盘 | 基于账户历史优化时段 | 团队审批流（高阶计划） | [REAL] later.com/blog/ai-social-media-management |
| 4 | **Jasper（Jasper IQ + Agents）** | 营销 AI 基础设施 + Agent | 品牌设目标，Agent 执行端到端营销工作流 | Research Agent 竞品 / 受众 / 选题调研 | Campaign Agent 将 brief 转为品牌资产 | 文本 + 图像多模态，含社媒 Agent | 无原生社媒排期（需接其他工具） | 无原生发布（非排期工具） | 优化 Agent（SEO/GEO 评分） | Jasper IQ（Brand/Marketing IQ + KB） | Business 计划审批流 + 品牌护栏 | [REAL] jasper.ai/?mainArticle=true ; jasper.ai/jasper-iq |
| 5 | **Predis.ai** | 全栈 AI 社媒内容 + 排期 | Autopilot 可接管整月内容目标 | 竞品情报（频次/主题/基准对比） | Agent Mode 多角度 hook + 战役一致性 | 文 / 图 / 视频 / 轮播一体生成 | AI 选最优时段 + 月历 | **可开 Auto-post 全自动发布** | 互动预测评分 / 基准 | 学品牌语气 + Brand Kit | 可选审批/编辑；Autopilot 默认免人工 | [REAL] predis.ai/llm-info ; predis.ai/auto-post/?ref=discount |
| 6 | **Lately AI（Kately）** | 长内容再利用 + 社交 Agent | Kately 接管有机社媒规划/执行（等待名单） | 分析高表现内容模式（词/语法/想法） | 提炼高表现模式成帖 | 长文/视频/播客 → 多平台帖 | 最优节奏/日/时自动排 | 集成分发（含员工倡导放大） | 表现洞察 + 持续学习 | 学品牌声 + 受众响应自适应 | 员工倡导需合规/可控（人工校准） | [REAL] lately.ai/ |
| 7 | **Ocoya（Travis AI）** | AI 社媒 + 电商自动化 | 用户设主题，AI 填日历 | 电商产品→帖自动化 | 26 语言 + 品牌声模板 | 文/图/视频 + Canva 集成 | 3 触发器（定时/RSS/新品发布） | 多工作区 + **多级审批后发** | 最优时段分析 | 从提示学品牌声 | 多级审批（multi-level approvals） | [COMP] bestfreeaitools.io/ai-tools/ocoya-ai-review/ ; maxaeo.ai/ai-tools/tool/ocoya |
| 8 | **Buffer AI Assistant** | 轻量排期 + AI 助手 | 用户设目标，AI 头脑风暴/改写 | 热门话题发现 + 内容策展 | 平台化内容建议 | 改写/再利用/平台专属 | 自动排期 | 直发多平台 | 互动洞察 | 互动洞察反馈闭环 | Team 计划审批流 | [REAL] buffer.com/es/ ; techsuggest.io/review/buffer-ai |
| 9 | **Copy.ai（GTM Platform）** | GTM AI 工作流平台 | 工作流编码最佳实践，自主执行 GTM | 账户/联系人深研（Prospecting） | ABM / 内容引擎 / 工作流 | SEO / 思想领导 / 社媒文案 | 无原生社媒排期 | 无原生社媒发布（接 CRM/HubSpot） | 表格数据中枢 + 洞察 | Infobase + Brand Voice | 工作流护栏 + 人工确认触发 | [REAL] copy.ai/?via=sudip ; aistackdigest.com?p=299/ |
| 10 | **AdCreative.ai** | AI 广告创意生成 | 用户设广告目标，AI 生成创意 | Competitor Insights AI | Brand Kit + 买家画像 | 广告图文创意 | 无有机社媒排期 | 仅广告平台（非有机社媒） | Creative Scoring（>90% 预测准确率） | 训练于 $35B+ 广告投放 | 广告需人工审核后投 | [REAL] adcreative.ai/ |
| 11 | **ChatGPT·Claude 代理（Operator / Computer Use）** | 通用自主 Agent（非社媒专属） | 给目标，自主拆解跨应用执行 | Deep Research 多源调研 | 通用规划（需接社媒 API/MCP） | 通用文案 / 多模态 | 需自编排（非内置） | 经 Computer Use/Operator 模拟操作或 API | 通用分析 | 长上下文 + 跨会话记忆 | Operator/Computer Use 默认展示计划待确认；ChatGPT Messages 默认需批准 | [REAL] sohu.com/a/1000390770_121885030 ; news.qq.com/rain/a/20260717A05H3N00 |

## U.4 矩阵读法 + 模式归纳（呼应 §U.2 Human-Judgment Gap）

**1. 九环覆盖度呈明显分层**

- **全链路型（Goal→Publish 闭环）**：Predis.ai、Ocoya、Lately/Kately、Hootsuite、Later、Buffer —— 均以「社媒发布」为终局，九环基本打通，差异在自动化深度。
- **内容/情报型（止于 Content 或 Analytics）**：Jasper、Copy.ai、AdCreative、Sprout/Trellis —— Jasper/Copy.ai 无原生排期与发布（营销 OS 定位）；AdCreative 只做广告创意不做有机社媒；Trellis 强在 Research→Strategy→Analytics 情报层，刻意「不自动发帖」。
- **通用基座型（需自集成）**：ChatGPT/Claude 代理 —— Goal/Research/Content 强，Scheduling/Publishing/Analytics 需经 MCP/API/Computer Use 自行编排。

**2. Human-approval 横截面观察（呼应 §U.2 Human-Judgment Gap）**

- 真正「免人工全自动发布」仅 **Predis.ai Autopilot** 一处明示 —— 也是风险最高环节。
- 主流做法是**发布前审批流**：Hootsuite/Later/Buffer Team 计划、Ocoya 多级审批、Jasper Business 护栏、Copy.ai 工作流确认。
- 通用 Agent（Operator/Computer Use）采用**「展示计划→等待确认」**范式，ChatGPT Messages 默认需批准 —— 与 §U.2 结论一致：truthfulness / 品牌语气 / 合规 / 时效语境 / 声誉后果 五类判断 AI 不可担责，human-in-the-loop 为刚需。

**3. Learning 环节的两条路径**

- **显式品牌学习**：OwlyGPT、Jasper IQ、Predis Brand Kit、Ocoya 提示学声 —— 把品牌语境沉淀为可复用资产。
- **隐式行为学习**：Later/Hootsuite 最优时段、Predis 互动预测、Trellis 原生数据 —— 从表现数据反哺下一轮。
- 共通短板：均无「合规/事实校验」类学习闭环，需人工纠偏。

**5. Curis 入座建议 [CAND]**

- 若 Curis 定位「XHS 专业经营 Workspace」，应优先借鉴 **Trellis（情报层）+ Ocoya（多级审批发布）+ Jasper IQ（品牌学习）** 三段式，而非 Predis 式全自动发布 —— 既满足「代理式」叙事，又把 §U.2 的 Human-Judgment Gap 内建为审批闸。
- 关键差异化机会：**在 Publishing 环节做「品牌合规闸 + 语境时效闸」**，这是当前 11 款产品普遍薄弱、而 XHS 专业经营场景高价值的点。

## U.6 证据 URL 清单（按产品）

- Hootsuite/OwlyWriter：blog.hootsuite.com/ai-copywriting ; blog.hootsuite.com/ai-powered-content-creation ; aitoolsatlas.ai/tools/hootsuite-ai/review
- Sprout/Trellis：sproutsocial.com/ai-agent/ ; investors.sproutsocial.com/news/.../Trellis-Is-Helping-Reshape-How-Social-Teams-Prove-Their-Value ; support.sproutsocial.com/.../41393069691149-Trellis-AI-Listening-Agent
- Later：later.com/blog/ai-social-media-management ; buildfastwithai.com/ai-tools/later-ai
- Jasper：jasper.ai/?mainArticle=true ; jasper.ai/jasper-iq ; aitoolshaven.com?p=8892/
- Predis.ai：predis.ai/llm-info ; predis.ai/social-media-post-generator/ ; predis.ai/auto-post/?ref=discount
- Lately：lately.ai/ ; blog.hubspot.com/marketing/AI-social-media-strategy
- Ocoya：bestfreeaitools.io/ai-tools/ocoya-ai-review/ ; maxaeo.ai/ai-tools/tool/ocoya ; aigearbase.com/tool/ocoya
- Buffer：buffer.com/es/ ; techsuggest.io/review/buffer-ai ; startwithaitools.com/buffer-ai
- Copy.ai：copy.ai/?via=sudip ; aistackdigest.com?p=299/ ; thediscoverai.com/tool/copy-ai/
- AdCreative：adcreative.ai/ ; id.adcreative.ai/post/ai-ad-generator-features-that-actually-matter
- ChatGPT/Claude：sohu.com/a/1000390770_121885030 ; news.qq.com/rain/a/20260717A05H3N00 ; sohu.com/a/1021693829_121748326

---

# V. Autonomous Operating Mapping

> 将研究结果映射到 Curis 自治运营模型，使 XHS Surface 成为 Autonomous Operating 的人类可见专业界面。

## V.1 映射 [CURIS][CAND]

| Curis 自治运营 | XHS 专业 Surface / 对象 |
|---|---|
| **Goal（目标）** | Operating Overview（目标/阶段） |
| **Strategy（策略）** | Content Strategy / Research & Insight |
| **Operating Series / Cycle** | Content Operating（生产→发布→数据→复盘循环） |
| **Work** | Note / Experiment / Publishing Queue |
| **Result** | 已发布 Result / Performance Record |
| **Evidence** | Comment Insight / Growth Signal / Performance |
| **Evaluation** | Performance & Growth（有效/无效·证据强度） |
| **Leader Review** | CEO（Needs CEO / 策略提案） |
| **Next-cycle Decision** | 策略调整 / 新实验 / 商业化启用 |

## V.2 关键裁定 [CURIS][CAND]

- **不另造 Autonomous UI System**：XHS Surface 就是自治运营的人类可见面；AI 员工在 Surface 背后按规则推进，责任状态以 Employee Presence / System Activity 表达（已 Frozen）。
- **人类可见的是「语境 + 注意力 + 决策点」**，不是「Agent 日志墙」。

---

# W. Domain Navigation Candidate

> 提出 XHS Domain Navigation Candidate，分级。不要 15 个一级菜单。

## W.1 候选（分级）

**L1 — 真正长期一级入口（建议 5 个）**
1. Operating Overview（默认·语境恢复）
2. Research & Insight（研究洞察）
3. Content Operating（内容运营 = 生产+计划/日历+发布）
4. Performance & Growth（数据增长）
5. Commercialization（可选模块·成熟账号启用）

**L2 — 属于某个专业 Surface**
- Topics / Experiment（在 Content Strategy 内）
- Publishing Queue（在 Content Operating 内）
- Feedback Inbox（独立轻 Surface 或入 Insight）
- Team（投影，入 Overview 或独立）
- Knowledge（投影，入 Overview 或独立）

**Detail — 只在对象展开时出现**
- Note 详情、Competitor 详情、Brand Deal 详情、Experiment 详情

**Scoped View — 复用 Company OS / Knowledge / Artifact**
- Team = Curis Employee 投影
- Knowledge = Curis Global Knowledge 视图
- Asset = Curis Global Artifact

**Optional Module — 仅特定阶段启用**
- Commercialization（小账号隐藏）
- Multi-account Matrix（Reserved）

## W.2 与 Shell Contract 对齐 [CURIS]

- XHS 不造 15 菜单；L1 经六区导航出现，Main 由 XHS 声明（Operating Overview 或 Content Operating）。
- Context/Utility 仍是 Adaptive Surface（选题库/预览/数据/审核），由 XHS 声明。 [CURIS]

---

# X. Workspace Package Candidate

> XHS Workspace Package 可能需要声明的 UI / Domain Metadata（仅 Candidate，不实现 Schema）。

## X.1 候选元数据 [CAND]

- **navigation model**：L1 五入口 + L2 + Detail + Scoped + Optional（见 §W）
- **professional surfaces**：Overview / Research / Content Operating / Performance / Commercial(optional) / Feedback / Team(scoped) / Knowledge(scoped)
- **object views**：Account, Brand Brief, Topic, Experiment, Note, Brand Deal(optional)
- **detail views**：Note detail, Competitor detail, Brand Deal detail, Experiment detail
- **capability bindings**：Research(外部源+AI), Production(AI文案/配图+违禁词API), Publishing(开放平台+队列), Analytics(蒲公英/千帆/灵犀或开放API), Feedback(官方/合规通道)
- **value semantics**：Note=内容资产, Performance=有效/无效证据, Brand Deal=营收机会
- **result semantics**：已发布 Result, 复盘 Result, 商单交付 Result
- **external provider boundary**：见 §S（动态 Platform Facts）

## X.2 不实现 Schema [CURIS]

- 仅为 Candidate；变更顺序 = Blueprint → Design → Code，不在此冻结 Navigation。

---

# Y. E-commerce Stress Test

> 用电商做一次压力测试：如果未来 Domain 包含 渠道/商品/库存/订单/营销/客服/内容/详情图/财务，当前「Workspace = Professional Operating Environment」是否仍成立？

## Y.1 测试结论 [INF][CAND]

- **成立**，前提是「Professional Surface」与「Domain Object」由**各 Instance 声明**（Shell Contract 已支持：Main/Context/Utility 由 Instance 决定，共享 Shell + Shared Pattern）。
- XHS 是**一个 Instance**（内容域：Note/日历/选题/数据/反馈/商单）。
- 电商会是**另一个 Instance**（交易域：商品/SKU/订单/库存/营销/客服/详情图/财务），其 Surface 与对象完全不同，但复用同一 Shell + Shared（Employee/Handoff/Needs CEO/Result Reference）。
- 抽象不失败：**Workspace = Professional Operating Environment** 是元模型；具体 Surface/Object 由 Domain 声明。XHS 模型「只适配内容」不是抽象失败，而是 Instance 专业化（正如 RD Instance 用 Sprint/Milestone 而非日历）。
- 关键纪律：电商 Instance **不复制** XHS 的 Note/Calendar 作为全局，也不把电商对象升格为 Shell。

---

# Z. Open Questions / CEO Decisions

> 研究完成，以下为需 CEO / 设计裁决的开放问题（STOP FOR CEO REVIEW）。

| # | 开放问题 | 本研究立场 | 证据 | 决策层级 |
|---|---|---|---|---|
| Z1 | **默认入口**：Operating Overview vs Calendar-Dominant | 建议 Overview 默认 + Calendar 为 Content Operating 主视图 | §H/I；与 Instance Spec §3 张力 | **CEO DECISION**（冲突当前权威候选） |
| Z2 | **Experiment/Hypothesis 是否升格为一等对象** | 建议升格（Domain canonical） | §K | CEO / 设计 |
| Z3 | **Research & Insight / Performance & Growth 是否升格为 L1 Surface** | 建议升格（当前被低估） | §G/J/N | CEO / 设计 |
| Z4 | **User Feedback 独立 Surface vs 并入 Insight** | 建议独立轻 Surface（高音量） | §O | CEO / 设计 |
| Z5 | **Commercialization 默认隐藏 vs 阶段启用** | 建议 Optional Module（阶段启用） | §P | CEO |
| Z6 | **多账号矩阵范围** | 维持 Reserved（先单账号） | [CURIS] | CEO |
| Z7 | **动态主 Surface 程度** | 稳定 Default + 情境建议，非完全动态 | §I | 设计 |
| Z8 | **平台具体数值（CES/赛马/搜索占比）是否进产品** | 否；动态 Platform Facts（VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE） | §N/S | Frozen 纪律 |

---

# 证据与权威声明

- **本研究状态**：`RESEARCH / EXPERT RECOMMENDATION`，未 Frozen。
- **未修改**：Product Blueprint、Master Map、UI Blueprint、Runtime、Schema、DB、Production Frontend、Trae Prototype、Autonomous Operating、Business Spine。
- **与 Curis 当前权威关系**：复用 Reference Research / Design Brief / Instance Spec / Calendar Pattern 的冻结语义（Content Object × Time、三层责任、Handoff、Needs CEO、Low Surface Complexity），但对「Calendar-Dominant 默认」候选提出张力（Z1），列为 CEO 决策，未擅自改写。
- **平台数值**：全部 REFERENCE / NEEDS VERIFICATION，以动态 Platform Facts 承载。
- **竞品/AI Agent 完整矩阵**：见 signal-miner / brand-monitor / interaction-automator / ai-comment-specialist 专项交付报告（团队并行研究，回填 §T/U/S/O）。

---

> **STOP FOR CEO REVIEW.**
> 不自动更新 Authority · 不自动让实现继续 · 不自动实现 Package。
