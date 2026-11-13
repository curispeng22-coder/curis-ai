---
title: XHS Current Prototype → Research-derived Professional Workspace · Gap Matrix
status: RESEARCH / EXPERT RECOMMENDATION
date: 2026-08-21
purpose: 对比「Current Trae XHS Prototype」（依据 Curis_XHS_Workspace_Instance_Spec_v1 / Design Brief / Calendar Pattern Spec）与本研究推导的专业 Workspace。逐项 KEEP/REPOSITION/EXPAND/MERGE/REMOVE/MISSING/FUTURE。特别回答 Calendar 的位置。
current_prototype_basis:
  - docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md（Calendar-Dominant 默认 / Note Split / Context=选题库 / Utility=预览·数据·素材·审核 / Review Gate / Handoff / Needs CEO / Publishing Queue / Analytics / Content Reuse Loop）
  - docs/03_Design/Curis_XHS_Workspace_Calendar_Pattern_Spec.md
research_basis: CURIS_XHS_PROFESSIONAL_WORKSPACE_DOMAIN_RESEARCH.md
---

# XHS Prototype Gap Matrix

判定图例：**KEEP**（保留）· **REPOSITION**（重新定位）· **EXPAND**（扩展/升格）· **MERGE**（合并入既有系统）· **REMOVE**（移除/纠正）· **MISSING**（缺失·需新增）· **FUTURE**（未来轮次）。

## 1. 逐项矩阵

| # | 当前原型元素 | 判定 | 研究推导处理 |
|---|---|---|---|
| 1 | Note / Content Object（笔记） | **KEEP** | 核心业务对象，保留；双主轴语义冻结不破 |
| 2 | Calendar 作为全局默认主导面（状态 A） | **REPOSITION** | 降级为「Content Operating 阶段主视图」；默认入口让位 Operating Overview（见 §3） |
| 3 | Note Split Working（状态 B） | **KEEP** | 保留为 Content Operating 内的工作方式 |
| 4 | Context = 选题库 / 信号（侧栏） | **EXPAND** | 升格为 **Research & Insight L1 Surface**；研究价值被严重低估，不能仅侧栏 |
| 5 | Utility = 图文预览 | **KEEP** | 保留为 Note detail / Utility |
| 6 | Utility = 数据看板 / Analytics | **REPOSITION→EXPAND** | 从 Utility 升格为 **Performance & Growth L1 Surface** |
| 7 | Utility = 素材 | **MERGE** | 素材归入 Curis Global Artifact，不在 XHS 重建 |
| 8 | Utility = 审核详情 | **KEEP** | Review Gate 保留 |
| 9 | Review Gate / Needs CEO | **KEEP** | Frozen 共享能力，保留 |
| 10 | Handoff / Result Reference | **KEEP** | 保留（责任转移事件 / 历史结果） |
| 11 | Publishing Queue（定时+赛马） | **KEEP** | 保留在 Content Operating 内 |
| 12 | Content Reuse Loop（复盘反哺选题） | **KEEP** | 保留（数据驱动闭环） |
| 13 | Employee Presence / System Activity | **KEEP** | Frozen 共享，保留（不伪装、不常驻侧栏） |
| 14 | 多账号矩阵 | **FUTURE** | 维持 Reserved（先单账号） |
| 15 | 商业合作 / 蒲公英任务流 | **MISSING→Optional** | 研究建议按经营阶段启用 **Commercialization 可选模块**（非永久隐藏） |
| 16 | 财务管理 / 结算 | **FUTURE** | Reserved（Curis v1 暂不建设完整财务） |
| 17 | AI 文案自动生成引擎 | **FUTURE** | LATER（先人工+AI 辅助润色） |
| 18 | 社媒监听 / 竞品实时追踪 | **EXPAND→Research & Insight** | 当前仅侧栏信号，升格为 Research Surface 的外部采集能力 |
| 19 | 团队审批流（多角色会签） | **MISSING→Scoped** | 用 **Curis Employee 投影**（Team Scoped View），不重造员工系统 |
| 20 | 外部 API 集成面板 | **MISSING→Boundary** | 以 **External Provider Boundary / 动态 Platform Facts** 承载，不硬编码 |
| 21 | **Operating Overview（默认语境恢复）** | **MISSING** | 研究核心新增：默认入口，回答 7 问，非 Dashboard |
| 22 | **Research & Insight Surface（L1）** | **MISSING** | 新增（阶段 0–3 专业面） |
| 23 | **Experiment / Hypothesis 对象** | **MISSING** | 新增 Domain canonical（建议升格） |
| 24 | **Performance & Growth Surface（L1）** | **MISSING** | 新增（由 Utility 升格） |
| 25 | **Feedback Inbox（用户反馈）** | **MISSING** | 新增轻 Surface（高音量，回流 Insight/Content） |
| 26 | **Team（Scoped 投影）** | **MISSING** | 新增 Scoped 视图（Curis Employee 投影） |
| 27 | **Knowledge（Scoped 视图）** | **MISSING** | 新增 Scoped 视图（Curis Global Knowledge 过滤） |
| 28 | Dashboard 作为默认主面 | **REMOVE** | 不采用；Overview ≠ Dashboard，不堆指标、不暴露架构 |
| 29 | 「Workspace = 一个 Calendar」框架 | **REMOVE** | 纠正：Workspace = Professional Operating Environment，Calendar 只是其中一段 |

## 2. 汇总

- **KEEP（13 项）**：Note、Note Split、预览、审核、Review Gate、Needs CEO、Handoff、Result、Publishing Queue、Content Reuse Loop、Employee/System 状态、素材合并前提、双主轴语义。
- **REPOSITION（3 项）**：Calendar 默认 → 阶段主视图；Analytics Utility → L1 Surface；Context 侧栏 → Research L1。
- **EXPAND（2 项）**：选题库/信号、社媒监听 → Research & Insight。
- **MERGE（1 项）**：素材 → Curis Global Artifact。
- **MISSING（10 项）**：Operating Overview、Research & Insight、Experiment、Performance & Growth、Feedback Inbox、Team(Scoped)、Knowledge(Scoped)、Commercialization(Optional)、External Boundary、多账号(FUTURE)。
- **REMOVE（2 项）**：Dashboard 默认、Workspace=Calendar 框架。
- **FUTURE（4 项）**：多账号矩阵、财务、AI 文案引擎、深度归因。

## 3. Calendar 应该放在哪里？（核心回答）

> **Calendar = Content Operating Surface 内部的一等视图，不是 Workspace 的默认入口。**

- **承载**：Note × Time 双主轴语义（冻结，不破）。Calendar Pattern Spec 的「同天多篇 / Primary 优先级 / +N 收口」规则全部保留。
- **位置**：位于 **Content Operating（内容运营 = 生产 + 计划/日历 + 发布）** 这一 L1 Surface 内部，作为该阶段的主视图。
- **默认入口**：让位给 **Operating Overview**——进入 Workspace 先恢复语境（阶段/目标/策略/注意力/下一步），一键进 Content Operating 见 Calendar。
- **与当前权威的张力**：Instance Spec §3 规定「默认进入面 = Publishing Calendar（Calendar-Dominant）」。本研究认为这把「排期」误提升为「经营」代表面，建议降级。此为 **OPEN QUESTION / CEO DECISION（Z1）**，本研究不擅自改写权威。

## 4. 对 Design 的启示（不实现）

- 现有原型的所有 Surface 都**有效**，问题在**范围与默认**——不是重画，而是补「经营前半段（研究/策略/实验）」与「经营后半段（增长/商业化）」，并把默认入口从 Calendar 改为 Overview。
- 不新增 Frozen 设计；变更顺序 = Blueprint → Design → Code。
- 平台数值（CES/赛马/搜索占比）不写死，以动态 Platform Facts 承载。

---

*本矩阵为 RESEARCH / EXPERT RECOMMENDATION，未 Frozen，未修改任何 Curis 权威文档。*
