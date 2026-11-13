# CURIS PRODUCT STRUCTURE BASELINE — PRE-DESIGN RESEARCH

> **Authority Class:** CURRENT / PRODUCT STRUCTURE AUTHORITY
> **Status:** Frozen
> **Disposition:** RECORDED / CURRENT — INCLUDED IN CONTROLLED BASELINE PROMOTION
> **Effective:** 2026-09-15（原2026-09-10结构保持；Consolidation增量同步）
> **Scope:** Product structure only; this is not a visual specification, Runtime contract, schema, or implementation acceptance.

## 1. Purpose and authority boundary

这是进入独立 Desktop AI / Agent UX 竞品研究前的唯一产品结构基线。它汇总已由 CEO、Frozen Authority、Phase A 与 Phase B 确认的结构，供 Product Design Research、Final UI Master 与 Frontend Reconciliation 共同消费。

本基线不创建第二套 Product Truth，不替代唯一 Product Blueprint、Master Map、UI Blueprint 或适用 Frozen Authority；它把这些 Current Truth 在设计研究前集中指针化。视觉组合、像素、动效和最终页面形态仍未批准。

### 1.1 2026-09-15 accepted capability consolidation

结构仍唯一消费[Product Blueprint](Curis_Product_Blueprint.html#consolidation-20260915)、[Master Map](Curis_Product_Master_Map.md)、[UI Blueprint](Curis_Product_UI_Blueprint.html#consolidation-20260915)；跨业务目标合同见[Company OS Shared §10–18](../03_Design/Curis_Company_OS_Shared_Authority.md)，账号经营见[Content Growth §5.4](../03_Design/Curis_Content_Growth_Domain_Authority.md)。Research不默认必读，Final UI Restart仍须本轮CEO最终Review。

Human Handoff在原Work完成必要人工动作，≠P7/≠自动P5责任转移。F2 Option A为opt-in Local Background目标：关闭UI后合法Work可继续，睡眠/登出不保证、关机不运行，可停止全部并退出、重开接同一历史。Browser/Model/恢复/专业工具/Backup合同已接受，G1-V～G6-V仍NOT RUN，不升级实现事实。

同Employee多Business服务由Assignment/Context隔离、目录身份唯一；Account/Platform不等Workspace或第五Scope。Main承载完整Conversation、复杂Browser/Model/编辑/专业工作；Utility辅助、Left Context局部、Assistant独立；新能力不新增一级区。其他既有结构与视觉语言保持。

## 2. Seven primary product areas

七个一级产品空间固定为：

1. CEO 工作台：公司级注意力、异常、简报、结果、待处理与下一决定。
2. 业务空间：Business 下的实际经营与 Workspace 入口。
3. 组织中心：公司版图与员工目录。
4. 人才与能力：专家发现、招聘、Employee、Skill、Capability 与 Provider binding。
5. 经营洞察：Company Analyst 驱动的趋势、比较、归因、报告与 Decision support。
6. 资料库：Company Reference Space，供读取、引用、来源追踪和沉淀。
7. 会议：持续的多人经营讨论空间。

Conversation Quick Access、CEO Assistant、搜索、最近工作、通知/待处理、模型与设置是全局能力或 utility，不占用第八个一级产品区。后续视觉研究不得自行增删一级区。

## 3. Company OS structure

### 3.1 Canonical relations

```text
Company
└─ Department
   └─ Business
      └─ Workspace
```

Employee、Role、Responsibility、Assignment、Work、Execution、Result / Evidence、Decision 与 Conversation 形成同一 Company OS 运行关系。Business 是持续经营身份；Workspace 是实际工作空间；二者不得混淆。Business 必须归属 Department；长期 Business 至少拥有一个 Workspace。用户可以先拥有 Company 而 Business = 0。

### 3.2 Curis 原装公司经营组织

新 Company 不是空组织，出厂包含 Company、CEO、同一 canonical CEO Assistant、空间工程部、数据分析部及真实原装 AI Employees。原装组织不是 Demo，也不是用户招聘目录；它是每个 Company 的 canonical 实例，可后续调整，不是永久人数限制。

空间工程部的六名初始 canonical Employee / Role 为：空间工程负责人、行业研究专家、经营方法专家、空间设计专家、搭建实施专家、质量验证专家。各自拥有已定义的 Responsibility、Handoff 与 Leader 关系；姓名和 Holder 可按合法规则调整，六名初始实例不等于永远只能六人。

数据分析部至少包含一名 Company Analyst / 公司经营分析师，当前默认 display name 为“司衡”（可编辑）。其工作位是经营洞察，承担 Company / cross-Business analysis、Data Trust、Report、Evidence 与 Decision support。

## 4. Employee and leadership model

Official Employee Definition → Company Employee Instance → Current Responsibility Holder。原装、招聘和用户自建 Employee 都消费同一 canonical Employee System，禁止 Built-in Employee 第二真源。

Employee 是真实公司员工身份，不是 Agent 配置记录。其产品身份至少包括 Identity、Department、Role、Responsibility、Capability、Skill、Model availability、Work Surface、Current Work、Result 与 Conversation；最终视觉尚未冻结。头像属于共享身份展示模式，不改变责任、能力或执行身份。

团队关系为 CEO → Team Leader → Employees。Leader 负责目标理解、策略边界内调整、分工、协作、异常、整合、结果和 CEO 沟通；Task routing only-on-exception 只约束异常路由，不削弱 Leader 的业务领导力。CEO 负责 Goal、Strategy、重大判断与 Decision Gate，不负责 DAG、Router、Workflow graph、Agent topology 或逐任务审批。

## 5. Business activation and workspace forms

标准责任转译为：

```text
CEO intent
→ Company
→ reuse / propose Business
→ necessary Decision Gate
→ canonical Department
→ canonical Business
→ first Workspace
→ Team / Responsibility
→ Operating
```

CEO 可直接创建，也可把建设意图交给空间工程团队。Generic Workspace 是合法真实工作环境；Professional Workspace 是业务具有稳定专业方法、工具和语义时的目标形态。Professional 不是所有 Workspace 的强制前置，Generic 不能吞并已形成的 Professional 形态。Content Growth、RD 等是用户启用的 Business / professional portfolio 示例，不是 Curis 固定业务类型、原装部门或 Core domain enum；Channel ≠ Workspace，具体 Channel Account 也不等于 Workspace；Project ≠ Business。

## 6. Workspace Engineering and Package First

Curis Core + Declarative Workspace Package 采用 Package First。Core 持有 identity、truth、execution、security 与 references；Package 负责 bounded professional composition，不回到 monolithic frontend。Workspace Engineering 以经营意图和 Current Company Truth 为输入，优先复用已有 Department、Business 与 Workspace，再按需调整或创建结构；它不拥有第二套 Organization Truth。

## 7. Canonical execution and truth boundaries

Company / Department / Business / Workspace 是统一 canonical execution scope，Assignment、Conversation、Work、Execution、Context、Result、Evidence、Usage 与 Authorization 共同消费。四层 scope infrastructure 的存在不等于四层 Autonomous Operating 产品已全部验收；实现状态必须回到 CURRENT_STATE、Issue、Review 与 Accepted Evidence。

Autonomous/Team Runtime 仍负责确定性、边界、版本、持久化、幂等、权限、Context isolation、restart 与 recovery。Work → Execution → Result / Evidence → Decision / next Work 是 canonical continuity；Viewed ≠ Accepted，Decision 继续使用既有 P7 truth。

## 8. Four-Pane and shared spatial responsibilities

App 空间基础由四种职责组成：Navigation、Context、Main、Utility。默认 Navigation + Main；Context / Utility 按需出现，不是四列常驻。Reading、Working、Operating 是同一 Shell 内的三种空间职责，不是三套 Shell：

- **Reading**：理解资料、结果与证据。
- **Working**：与 Employee、Work、Meeting 持续工作。
- **Operating**：方向、责任、状态、结果、问题与下一判断。

Navigation 承载七区、Conversation Quick Access、Company object navigation/search 与 CEO/settings utility。具体视觉 chrome、密度和布局留给竞品研究。

## 9. Conversation, CEO Assistant and Composer

### 9.1 Conversation Sidebar

Conversation Sidebar 是 **GLOBAL CONVERSATION QUICK ACCESS**：canonical persisted conversations、recent activity、Employee-backed / Work-backed 对话、同一 Employee 的多个 topic、搜索、reopen；dismiss ≠ delete。它不是 CEO Assistant。

### 9.2 CEO Assistant

CEO Assistant 是 **GLOBAL FLOATING CEO ASSISTANT**：全局可达、可拖动、可收起/展开，跨七区和页面切换不销毁，保持同一 canonical identity 与 durable Conversation，并消费合法 current context。它不占 Four-Pane，不等于 Conversation Sidebar，也不等于 CEO Desk。尺寸、位置、handle、snap、快捷键、动效和视觉呈现全部开放给后续 Design Research。

在 Bootstrap 中，Assistant 理解经营意图、协调 Situation / Capability Discovery / Research、组织 Operating Proposal、把专业责任交给合法 Leader / Department / Employee，并跟进结果；它不替代 Team Leader、Domain Expert、专业员工或 Executor。

### 9.3 Shared Composer

基础功能合同为 Text、Context、Reference、Attachment（按真实支持）、Send，以及 execution / waiting / failure state。不同宿主可以扩展，完整语义槽位继续消费Frozen Shell §3.5：Input / + / 访问权限 / 工作模式 / 已选资源 / Model·Agent / Voice / Send（按真实支持）。此简表不能成为第二套缩减Composer；消息节奏、气泡、输入框和具体视觉均未冻结。

## 10. Meeting, Knowledge and Operating Intelligence

- **Meeting**：持续的多人经营讨论空间，支持 participants、conversation、evidence、proposal、decision、responsibility、work、result 与 continued discussion。CEO 离开不结束 Meeting；它不是 Calendar、Slack archive 或审批后台。
- **资料库 / Knowledge**：Company Reference Space，核心是 Reading、Reference、Source、Scope、Freshness、Used By 及 Work ↔ Result continuity；不是 File Manager 或 RAG Console。
- **经营洞察 / Operating Intelligence**：产品工作面。数据分析部与 Company Analyst 承担组织责任，关系为 Organization responsibility → Analyst → Analysis → Report / Evidence → Decision support；不创建第二套 Metric / Result / Analytics Truth。
- **人才与能力**：Talent 用于招聘、创建 Employee、扩展 Skill / Capability 和 Provider binding；原装员工已经是 Company Employees，不是待招聘 Expert。

## 11. “交给 Curis”与开放业务

“交给 Curis”是普通用户心智，不要求理解 Business Responsibility Handoff、Operating Lifecycle、Playbook、Runtime 或 Provider。内部责任转译为：Intent → Situation / Capability Discovery → Research / Proposal → 必要 CEO Gate → Reuse / Compose / Acquire / Build → Leader Responsibility → Result / Evidence / Review → Next-cycle Decision。该箭头固定责任、Truth、Evidence、Gate 与 Recovery 语义，不固定所有行业的工作箭头。

未知业务必须诚实走：

`USE EXISTING → COMPOSE EXISTING → RESEARCH / ADAPT → BUILD / ACQUIRE → ESCALATE → REFUSE / CANNOT OPERATE YET`。

Curis 不得把未知业务伪装成已验证行业能力。XHS、抖音、RD、宠物寄养等只用于 Validation / Pressure-test，不进入 Core 成为固定流程或默认模板。

## 12. Runtime capability record (preserved, not re-accepted here)

历史与当前证据中已记录的能力继续保留：built-in organization、6+1 Employee、Business=0、Business activation、canonical execution scope、Employee edit persistence、Conversation persistence、Usage、Attention、Result、Knowledge、Meeting core、General lifecycle、Four-Pane behavior、Floating Assistant behavior、restart / no replay。此清单是保留的 Implementation Truth 指针，不在本文件重新宣称 Runtime 全量验收；真实边界以 CURRENT_STATE 与 Accepted Reviews 为准。

## 13. Intentional visual boundary

当前 19 张 Figma / Batch 1 资产只作为 **STRUCTURAL / IA REFERENCE**。它们不是 FINAL VISUAL AUTHORITY。

**FINAL UI MASTER: PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED**。已确定的是产品结构与空间责任，不是 Typography、spacing、border、radius、shadow、button、Composer/message appearance、Employee treatment、Workspace density、Result reading、Assistant appearance 或 Pane chrome。

竞品研究可以借鉴 interaction pattern、visual hierarchy、desktop behavior、composer pattern、message rhythm、pane behavior、artifact reading 与 agent progress，但不得推翻 Company OS、七区、原装组织、Employee model、Business / Workspace、Four-Pane responsibilities、CEO Assistant identity 或 canonical scope。

## 14. DESIGN RESEARCH — OPEN QUESTIONS

- App Shell 最终视觉与 Desktop density
- Navigation visual、Pane chrome 与 Context / Utility 的适配行为
- Conversation message rhythm、identity、references 与 Composer appearance
- Agent progress、Employee identity presentation 与 Workstation 表达
- Workspace working surface、Result / Artifact reading
- Floating CEO Assistant 的 visual、位置、收起/展开和 motion
- Modal / overlay、status / feedback 与 interaction feedback

这些是研究问题，不是未授权的新产品区或新 Runtime primitive。

## 15. Downstream consumption and stop rule

后续 Product Design Research、Final UI Master、Frontend Reconciliation 必须先读本基线，再读 Pointer 指向的 Current Product Truth 与适用 Frozen Authority。若研究、实现或旧资产与本基线冲突，按 AGENTS.md 执行 `STOP / REPORT AUTHORITY CONFLICT`，不得静默改写。

### VERDICT

**PRODUCT STRUCTURE: RECORDED / CURRENT**
**CORE RUNTIME: PRESERVED**
**FINAL UI MASTER: PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED**
**VISUAL AUTHORITY: NOT APPROVED**
**NEXT: CURIS PRODUCT DESIGN RESEARCH — DESKTOP AI / AGENT UX**
**STOP FOR CEO / CHATGPT PRODUCT STRUCTURE REVIEW**
