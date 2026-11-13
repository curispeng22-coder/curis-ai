# CURIS OPERATING INTELLIGENCE — UX CONSOLIDATION

**Authority Class**：RESEARCH  
**Status**：**ACCEPTED — OPERATING INTELLIGENCE UX BASELINE**（2026-08-18 CEO FINAL ACCEPTANCE）  
**Disposition**：**CONSUMED BY CURRENT PRODUCT TRUTH**（Product Blueprint 5.3 / Master Map 3.0 / UI Blueprint）
> 本文件与 `CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html` 一并登记为本 Baseline。整合对象：6 项已 CEO 接受/登记的研究。本文件只记录「整合了什么、如何落地、CEO 已确认决策」，不引入新研究结论。本文件经 FINAL CLEANUP 修正（去无依据判断、复核人规则、空间工程部语义、首页占位移除）。
> 纪律：未改动 Product Blueprint / Master Map / UI Blueprint / Frozen Shell / Runtime / Schema / Database；不写产品代码；所有数据为 DEMO DATA — NOT RUNTIME TRUTH。
> 本 Baseline = **产品 UX 真相输入（Product Truth Delta），不是 Runtime / Schema Authority**。已由 **FINAL PRODUCT ARCHITECTURE DELTA** 消费进入 Blueprint / Master Map / UI Blueprint / Global Navigation 合同。不再继续同范围研究，除非 CEO 明确重新开启。

---

## 1. 已消费的 Accepted Research（全部已登记）
1. Operating Intelligence 产品研究（方向：经营洞察 = 数据洞察 + 经营分析）
2. Analytics UX & Page Exploration（CEO 首屏 / 完整 IA / 三 Variant）
3. Analyst Organization UX Delta（Business Analyst + Company Analyst 责任分层）
4. Data Visualization Research（CEO 问题→图、图表族、Benchmark 纪律、10 原则、P0/P1/P2）
5. Semantic-safe Visualization Switching（Delta A）
6. Default Functional Analytics Organization（Delta B：空间工程部 + 数据分析部 + 默认 Company Analyst）

---

## 2. 最终 IA（内部导航，6 区）
`经营洞察` → 公司经营 / 业务分析 / 组织与员工 / 模型与能力 / 分析报告 / 专项研究（Company Analyst）
- 公司级入口心智：首页 = 「我的 AI 经营分析团队给我准备了什么」（Company Analyst Brief + 经营信号 + 业务报告 + 跨公司分析），非 KPI 卡片墙。
- **CEO 已确认：经营洞察 = Curis 第七一级导航**（UX 表达层确认，未改动 Frozen Navigation 文档，由后续 Global Navigation Final Delta 落实）。
- 首页已移除 Industry Research Vision 占位（未来能力保留，不在首页占位）。

## 3. Analyst Organization（责任分层，真实 AI Employee）
- **Company Analyst（司衡）**：公司级经营分析责任，明确属于**数据分析部**，不替代 Business Analyst。
- **Business Analyst**：默认由数据分析部 Employee 指派（Mode A：小陈→小红书运营、小陆→抖音运营、研析→研发）；成熟 Business 可自有数据分析 Role/Employee（Mode B）。
- 报告责任链：Scope / Period / Responsibility / Author Employee / Department / Business / Trigger / Data Sources / Model-Agent provenance / Created At / Review。
- 报告正文：FACT / INTERPRETATION / UNKNOWN / RECOMMENDATION / EVIDENCE；AI 解释**永不冒充 Fact**。
- CA ↔ BA 协作：CA 发现跨公司异常 → 委派 BA → BA 执行 → 报告 → CA 独立汇总；BA 的 INTERPRETATION **不自动升级为 Company Fact**。
- **No Analyst 状态**：无负责 Employee 时显示「无负责分析师」+ 4 选项（临时任务 / 指派现有 / 建岗位 / 从人才与能力招募），**不出现匿名 AI Analyst**。

## 4. 可视化模式（正式进入 UX，整合 HTML 真实展示）
| # | 场景 | 推荐图 | 整合位置 |
|---|---|---|---|
| 1 | Model / Agent Benchmark | Sorted Horizontal Bar + Small Multiples + Scatter(Cost×Quality) + Table，必须 Sample Size / Comparability / Evidence，**禁止单一名次榜** | 模型与能力 |
| 2 | 小红书经营趋势 | Line + Baseline/Previous Period + 关键经营事件标记 | 业务分析 |
| 3 | 内容表现分析 | Heatmap（发布时段 × 内容类型 × 平均涨粉）或 CTR×涨粉 Scatter | 业务分析 |
| 4 | Organization Capacity | Capacity/Load 可视化（空岗/接近饱和/过载，Capability≠Capacity） | 组织与员工 |
| 5 | Workflow | Funnel（Stage/Failure/Rework/Handoff/Bottleneck） | 组织与员工 |

> **CEO 已确认：当前 5 类核心 Visualization 已足够，不继续为展示而补图**（如 Sankey 替代 Funnel、CTR×涨粉 Scatter 与 Heatmap 并列等不在本轮新增）。

## 5. Semantic-safe Visualization Switching（Delta A）
同一 Dataset，系统给推荐图，用户只在**语义兼容**视图间切换；只改 Presentation，不改 Dataset/Metric 真相。
- Trend：**[Line 推荐] [Bar] [Table]**
- Model Comparison：**[Bar 推荐] [Scatter] [Table]**
- Composition：**[Stacked 推荐] [Donut] [Table]**
- 禁止错误图：时间趋势≠饼图；10–20 模型≠饼图；关系≠无意义折线。

## 6. 默认职能分析组织（Delta B）
`公司 → Company Support Organization { 空间工程部 + 数据分析部 } → 数据分析部 { Company Analyst 司衡, 小红书分析师→小红书运营, 抖音分析师→抖音运营, 研发分析师→研发 }`
- **空间工程部 = Curis 默认职能支撑部门**，与数据分析部同属默认 Company Support Organization（**非 Business / 工程业务示例**）。
- 仅表达已确认 Product Delta，**不授权 Runtime/Schema 改动**。

## 7. Data Trust
Source / Freshness / Verified / Manual / Unknown / Stale / Missing / External。
- External 未连接 → 显示「待连接 / 无数据」，**绝不显示 0 或空冒充**；Manual Entry 标注录入人/时间/可信度。
- 图表只需可追溯到 Scope / Metric / Period / Source / Freshness / Responsible Analyst。

## 8. Report · Conversation · Review · Decision（闭环）
- Report → CEO「问分析师」进入**既有 Conversation Surface**（非第二聊天记录）→ CEO 质疑 → 要求调查 → 真实 Analysis Task（责任仍归原 Employee）→ 新 Report 回写同一对话。
- 可请求 **Second Analyst Review**（Agreement / Disagreement / Evidence / Unknown / Final Rec）。
- **Second Analyst Review 复核人硬规则**：必须同时满足 **Independence（独立于原分析）** 与 **Relevant Analysis Capability（具备该业务的相关分析能力）**；不再以"研发分析师复核小红书增长分析"为例（研发分析师不具相关能力）。
- 决策经 Meeting / Decision 在原产品入口落地，新数据回流 Company OS，下一轮分析反映 Before/After（依赖变更事件标记，无标记不给因果结论）。

## 9. Dependency-Gated（非正式 Roadmap）
P0/P1/P2 仅作**研究/依赖参考**，不是正式 Roadmap，不在整合中按版本切割交付。

## 10. CEO FINAL DECISIONS（已确认，2026-08-18 · FINAL CLEANUP）
1. **全局导航**：经营洞察 = Curis 第七一级导航（UX 表达层确认；Frozen Navigation 由后续 Global Navigation Final Delta 落实，本轮未改）。
2. **可视化范围**：当前 5 类核心 Visualization 已足够，**不继续为展示而补图**（Sankey / CTR×涨粉 Scatter 等不新增）。
3. **默认组织命名**：空间工程部 / 数据分析部 名称确认；空间工程部 = 默认职能支撑部门，与数据分析部同属 Company Support Organization，非 Business。
4. **Composition 口径**：Composition 跟随当前 Metric 口径（本例用发布量），不建立单一全局口径。
5. **首页占位**：移除 Industry Research Vision 占位，但**不删除未来能力**（未来扩展保留）。

### FINAL CLEANUP 修正项（本轮已落地于 HTML）
- 删除无明确规则支撑的判断：Capacity 70% → 仅「负载 70%」；Employee「优」→ 仅保留 Quality / Acceptance 事实；公司级「组织负载 78%」去「接近饱和」包装；空岗去「过载预警」包装。
- Second Analyst Review 复核人改为 **司衡（Company Analyst）**，满足 Independence + Relevant Analysis Capability；废止"研发分析师复核小红书增长分析"示例。
- 空间工程部语义修正：= Curis 默认职能支撑部门，与数据分析部同属 Company Support Organization，非 Business / 工程业务示例。
- 首页移除 Industry Research Vision 占位（未来能力保留）。

---
*整合产物：`CURIS_OPERATING_INTELLIGENCE_UX_EXPLORATION.html`（完整 Consolidated Exploration，经 FINAL CLEANUP）。所有数字/人员/报告均为 DEMO，不代表 Runtime。*
