# CURIS AUTONOMOUS OPERATION
## PRODUCT SURFACE MAPPING
## 将经营真相映射到 CEO / Department / Business / Workspace / Leader Conversation

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CEO ACCEPTED / APPROVED SURFACE MAPPING  
**Date:** 2026-08-20  
**Scope:** 只定义既有产品表面的信息责任、入口、下钻与语言映射；不创建 Operating Console，不修改 Product Blueprint、Master Map、UI Blueprint、Frozen Shell、Runtime、Schema、数据库、Frontend、Prototype 或高保真。

## 0. 结论

本文件消费已接受的 `CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md`，把经营连续性映射到当前五个产品表面：

1. CEO 工作台（CEO Desk）
2. Department Work Surface
3. Business Work Surface
4. Workspace
5. Leader Conversation

它不增加“Operating Center / Strategy Center / Learning Center / Review Center / Cycle Console”，也不把 Runtime 状态机直接呈现给用户。用户看到的是公司正在发生的经营状态、结果、判断和下一步；经营引擎仍是内部实现。

**核心原则：**

> 让 CEO 感觉公司正在自己经营，而不是让 CEO 学会操作一套经营引擎。

本轮只是页面责任映射候选。需要 CEO 接受后，才能由 UI Blueprint / Design 继续消费；仍不等于实现授权。

## 1. 当前产品层级与不变的页面骨架

### 1.1 层级

```text
Company
└── Department
    └── Business
        └── Workspace
```

Department Leader 管跨 Business 的经营与协调；Business Leader 管多个 Workspace 的 Business Strategy 与整体结果；Workspace Leader 持有 V1 Operating Cycle。三层不是同一页面的重复版本。

### 1.2 Workspace 页面骨架

```text
Parent Path
→ H1
→ 负责人 / 目标 / 规则与配置
→ [Conditional CEO Decision]
→ Current Operating
→ Domain / Generic Primary Surface
→ Team Operating
→ Employee Work Area
```

自主经营只增强这些区块的信息表达，不替换 Domain Primary Surface。XHS 仍以内容经营为主，RD 仍以研发工作对象为主，Generic 仍以“当前工作”为主。

### 1.3 层级职责总表

| Surface | 用户要回答的问题 | 经营范围 | 默认密度 | 不承担 |
|---|---|---|---|---|
| CEO Desk | 今天什么值得我关注、决定、跟进？ | Company / 跨 Business | 低表面复杂度、高注意力密度 | 全量任务台、BI Dashboard、完整运行控制 |
| Department | 这个部门下的 Business 整体怎样？ | Department → 多 Business | 管理摘要 | Workspace 周期、员工逐条工作 |
| Business | 这项业务为什么这样经营、整体结果怎样？ | Business → 多 Workspace | 经营组合摘要 | 细粒度执行现场、重复 Workstation |
| Workspace | 现在正在做什么、为什么、结果如何、下一步是什么？ | 单一 Workspace | 专业工作现场 | Runtime 图、抽象控制台 |
| Leader Conversation | 为什么这样做、下一步为何如此、需要我什么？ | 当前 Leader Scope | 解释与协作 | 第二套任务/事实系统 |

## 2. 经营真相的展示层级

### 2.1 Progressive Disclosure

| Level | 普通 CEO 看到的内容 | 典型承载 |
|---|---|---|
| Level 1 | 一句话经营状态 | CEO Desk、Department、Business、Workspace Current Operating |
| Level 2 | 当前策略 / 重要结果 / 下一步 / 需要关注 | Desk Matter、Business Summary、Workspace Current Operating |
| Level 3 | Review / Evidence / Signal / Learning / Evaluation Contract | Detail、抽屉、Context Pane、Leader Conversation |
| Level 4 | 版本号、引用、Runtime / audit ref、原始状态 | 仅按需审计或技术追溯，不进入默认产品语言 |

普通 CEO 默认停在 Level 1–2。下钻必须保留来源上下文和返回路径。

### 2.2 信息不重复原则

- CEO Desk 只呈现 material change、需要 CEO 注意的 Matter 和重要 Result。
- Department 只呈现跨 Business 的聚合趋势、协调和 Leader 注意事项。
- Business 呈现整体经营摘要和 Workspace Directory，不复制每个 Workspace 的工作细节。
- Workspace 呈现本空间当前策略、专业工作对象和团队执行，不复制公司总览。
- Leader Conversation 负责解释“为什么”，但引用既有事实，不生成第二套 Truth。
- Detail / Drawer 承担完整证据、来源和审计，不把全部字段永久铺在页面上。

## 3. Truth Inventory 分类

| Truth | CEO Desk | Department | Business | Workspace | Leader Conversation | Detail Surface | Hidden / Internal |
|---|---|---|---|---|---|---|---|
| Intent | 重大经营意图变化 | 部门方向摘要 | Business 意图 | 当前空间目的 | 解释意图与取舍 | 完整意图来源 | 原始引用 / 版本 ref |
| Goal | Company / Business 重要目标 | 跨 Business 目标摘要 | Business Goal | Workspace Goal | 讨论目标是否仍成立 | Goal / Success Contract | ID、版本 |
| Strategy | 重大改变或需决定时 | 部门策略摘要 | 一句话当前策略 | 本轮重点 / 当前假设 | 解释为什么选它 | hypothesis、边界、评估合同 | Strategy version |
| Approved Strategy Envelope | 仅越界提醒 | 风险/资源摘要 | 边界说明 | 本轮可自主调整范围 | 解释能否自行调整 | 完整边界与授权 | policy ref |
| Current Operating Cycle | 结果或异常摘要 | 不展示 Cycle 细节 | “本周复盘”等语义 | 当前经营 / 本轮重点 | 解释本轮在哪一步 | Cycle Detail | cycle_id / phase enum |
| Current Plan | 下一步摘要 | 跨 Business 计划冲突 | Business 计划摘要 | 当前工作对象与安排 | 解释计划为何改变 | Plan Detail | plan_version |
| Result | material Result、重要变化 | 跨 Business Result | 业务整体 Result | 最新结果 / 判断 | 解释结果意义 | Result / Artifact | execution internals |
| Evidence | 重要证据或缺证提醒 | 可信度摘要 | 结果依据 | 本轮证据与缺口 | 解释证据是否充分 | Evidence Detail | raw trace |
| Signal | 只显示会改变注意力的 Signal | 聚合趋势 | 业务趋势 | 当前验证信号 | 解释 signal / confounder | Signal Detail | sensor / event raw |
| Review | 需要 CEO 的 Review | 部门复盘摘要 | 最近判断 | 最新判断 / 最近学习 | 复盘对话 | Review Detail | review state enum |
| Learning | accepted Learning 的 material 变化 | 跨 Business 学习 | 业务经验 | 已验证经验 | 解释如何影响下一轮 | Learning Detail | generated drafts |
| Next-cycle Decision | 需要 CEO 的 CONTINUE/ADJUST/WAIT 等 | 依赖协调时 | 业务下一步 | 下一步标签 | 解释选择与代价 | Decision Detail | enum / packet ref |
| Need | 需要 CEO / 部门资源 | 跨 Business 资源缺口 | 业务缺口 | 缺能力 / 人 / 资料 | 询问与路由 | Need Detail | resolver internals |
| Risk | 高影响风险 / 异常 | 部门风险 | Business 风险 | 当前阻塞 / 关注 | 解释风险和缓解 | Risk Detail | detector raw |
| CEO Decision | 待 CEO 处理事项 | 部门升级事项 | Business gate | 条件性 Decision Slot | 讨论后确认 | Decision Package | approval audit |
| PAUSE / STOP | 状态变化与需确认事项 | 组合影响 | 业务影响 | 当前空间暂停/结束 | 解释责任连续性 | Lifecycle Detail | terminal policy |
| Operating status | 用户语言的公司状态 | 聚合状态 | 业务状态 | 本空间状态 | 解释来源 | Status Detail | Runtime phase |
| nextCheckAt | 重要复盘/检查提醒 | 协调窗口 | 业务复盘时间 | 下次复盘 | 对话中解释 | Schedule Detail | scheduler ref |
| autonomy policy | 仅越界或审批提示 | 例外摘要 | 边界摘要 | 当前可自主范围 | 解释责任边界 | Policy Detail | policy engine |

## 4. CEO Desk 映射

### 4.1 Page responsibility

CEO Desk 不是 Dashboard，而是 CEO 的注意力入口。首屏回答：

1. 公司当前是否在经营；
2. 哪些变化是真正重要的；
3. 哪些事项需要 CEO 现在介入；
4. 未完成责任、决定和风险如何承接到下一经营日。

### 4.2 信息分组

| 信息责任 | 默认展示 | 下钻 |
|---|---|---|
| Brief | 今日简报 + 自上次查看以来的 material change | Brief detail / 来源对象 |
| Needs You | CEO Gate、风险、高影响决定、受保护 PAUSE/STOP、未解决升级 | Decision Package / Business / Workspace |
| Company Operating | 经营中、增长验证、稳定经营、等待数据、暂停等用户语言 | Business / Workspace |
| Important Changes / Results | 重要 Result、accepted Learning、Strategy change、风险变化、Goal progress | Result / Review / Insights |
| Continuity | 未完成 Responsibility、Decision、Risk、Follow-up | 原 Matter / Leader Conversation |

不要展示每一条 Task、Handoff、Employee execution，也不创建 Daily Close 按钮。Closeout 由系统 / Assistant 根据真实事实持续形成。

### 4.3 主动打扰

Assistant 只在以下条件主动打扰：

- CEO Gate 或高影响不可逆外部动作；
- 责任冲突、无法继续、等待 CEO 的关键条件；
- 高风险异常、证据不足但需要决定；
- PAUSE / STOP 提案或 Strategy Envelope 越界；
- 重要外部结果改变 Business 判断。

普通运行、单个员工完成、普通交接不构成 Desk Matter。

## 5. Department Surface 映射

Department 是管理与协调面，不是每日执行现场。

默认展示：

- Department 当前责任与 Leader；
- 下属 Business 的经营状态分布；
- 跨 Business 的重要 Result / Risk / Need；
- 资源、能力或目标冲突；
- Department Leader 需要处理的协调与升级。

不默认展示：Workspace Cycle、员工逐条对话、完整 Work list、Runtime 阶段图、每个员工状态墙。

Department 的核心句式是：“这个部门整体如何支持和协调这些业务？”而不是“今天每个员工做了什么？”

## 6. Business Surface 映射

Business Surface = Business Work Surface / Operating Work Directory 的业务级管理面。

### 6.1 Business Definition

保留：Business Name、Business Goal、Positioning、所属 Department、Responsible Leader、Workspace 数量与入口。Strategy 默认只用一句普通语言表达，复杂内容通过 Detail 或 Leader Conversation 展开。

### 6.2 Operating Summary

展示：

- 当前经营状态；
- 当前 Strategy summary；
- material Result；
- accepted Learning；
- Risk / Need；
- 下一重要节点或复盘时间。

禁止默认显示 `TRIGGER_CLAIMED / SENSED / PLANNED / REVIEWING / DECIDING` 等 Runtime phase。

### 6.3 Workspace Directory

每个 Workspace 轻量显示：Name、Leader、用户语言的经营状态、当前 Focus / Strategy hypothesis、最新 material Result、Need / Risk、下次复盘。不要把 Cycle 数字和执行内部状态做成首要信息。

Business Leader 查看多个 Workspace 的经营组合；Business 不复制 Workspace 的 Workstation，也不把所有 Workspace 展开成 Dashboard wall。

### 6.4 Business Team

只呈现 Business-level Responsibility Assignment、Leader、关键能力和组队摘要。Workspace Team Operating / Employee Work Area 进入对应 Workspace 后再看。

## 7. Workspace Surface 映射

Workspace 是 autonomous operation 的主要证明面，但它必须仍是专业工作场所，不是通用 Operating Console。

### 7.1 Current Operating 的最小合同

| 项目 | 用户语言 | 例：小红书 |
|---|---|---|
| 经营状态 | 增长验证中 | 增长验证中 |
| 本轮重点 | 一句话策略 / 假设 | 验证 AI 工具实测对转化的影响 |
| 进展 | 优先由 Domain Primary Surface 表达；只有主面无法表达时才补充 | 由内容排期 / 发布主面表达；必要时补充简短结果 |
| 最新结果 / 判断 | 事实 + 当前判断 | 工具测试有领先信号，但证据不足 |
| 下一步 | 继续 / 调整 / 等待 / 升级 | 继续观察，本周五复盘 |
| 需要关注 | 仅存在真实 Need / Risk / CEO Gate 时显示 | 需要补充外部数据来源时才显示 |

这些信息是轻量摘要，优先放在 Current Operating，不替换 Domain Primary Surface。

### 7.2 Domain Primary Surface

- XHS：内容经营 / 内容排期 / 发布与反馈对象；
- RD：真实研发工作对象、Version、Build、Test、Review、Blocker；
- Generic：当前工作；
- 其他 Domain：由其专业工作方式决定。

Autonomous Lifecycle 只补充 `Why / Current Operating / Result / Next`。Employee Work Area 是 Shared Work Area，不得占据整个 Workspace 的最大视觉主体。

### 7.3 Strategy 与工作对象

在专业主面上方用一句话显示“本轮重点：验证 AI 工具实测”。点击后进入 Strategy Detail：hypothesis、原因、expected outcome、Evaluation Contract 摘要、Strategy version、Approved Envelope、evidence refs。默认不显示 `cycle_id / strategy_ref / plan_version`。

### 7.4 Review / Learning

不新增 Review Center / Learning Center。Workspace 默认只显示“最新判断 / 最近学习”；点击进入 Detail，查看 Result、Evidence、Signal、不确定性、accepted Learning、Next-cycle Decision。

## 8. Leader Conversation 映射

Leader Conversation 是解释经营的首要人机表面，不是聊天入口包装，也不是第二个任务系统。

它必须能回答：

- 现在怎么样？
- 为什么在做这些工作？
- 上一轮结果说明了什么？
- 为什么没有调整？
- 下一步是什么？
- 为什么需要我决定？

回答必须引用当前 Scope 内的 Goal、Strategy、Plan、Result、Evidence、Review、Learning、Next-cycle Decision。不能只列“3 个任务进行中”。

### 8.1 Scope

- 从 Workspace Leader 入口进入：整个 Workspace Responsibility Scope；
- 从 Role Assignment 进入：具体责任范围；
- 从 CEO Desk / Business / Department 进入：带对应 Company / Business / Workspace scope；
- 保持 Assignment-scoped isolation，不混用其他 Employee identity。

### 8.2 CEO 可以做什么

CEO 可以询问、建议、改变方向、创建新 Goal、挑战 Strategy、请求 PAUSE。改变 Goal、Success Contract、Positioning、Target Audience、Business / Monetization Model、protected Strategy Boundary、material Budget 或高影响不可逆承诺时，必须进入 CEO Decision Slot。

不得增加 Strategy Editor、Lifecycle Editor、Cycle Editor 作为独立产品入口。

## 9. 产品语言映射

| 内部/研究概念 | 产品默认语言 | 备注 |
|---|---|---|
| Intent | 经营意图 | 可在 Brief / Conversation 解释 |
| Strategy | 当前策略 / 本轮重点 | 不显示版本枚举 |
| Cycle | 本轮经营 / 本周复盘 | 默认不暴露 Cycle 名称 |
| Result | 结果 / 重要结果 | 必须有来源或标记未知 |
| Evidence | 依据 / 证据 | 说明是否充分 |
| Review | 最近判断 / 复盘 | 不自动生成大报告 |
| Learning | 已验证经验 / 最近学习 | 只显示 material learning |
| CONTINUE | 继续当前策略 | 仅 detail 可见内部 enum |
| ADJUST | 已调整下一轮计划 / 策略 | 说明调整原因 |
| WAIT | 等待数据 / 外部条件 | 说明等待什么 |
| ESCALATE | 需要你决定 | 进入 CEO Decision |
| PAUSE | 已暂停 | 保留责任与历史，需显式恢复 |
| STOP | 已结束当前经营目标 | 不是普通 Cycle terminal |
| TRIGGER_CLAIMED 等 phase | 不作为默认产品词 | 仅审计 / 技术追溯 |

建议状态候选：筹备中、经营中、增长验证、稳定经营、策略调整中、等待数据、等待你的决定、暂停、已结束。它们是产品投影，不是 Runtime Enum。

## 10. CEO Decision mapping

### 10.1 进入 CEO Decision Slot 的条件

只在以下情形出现：

- CEO Gate；
- Strategy Envelope 越界；
- 高影响 / 不可逆外部承诺；
- 责任冲突或跨层无法自动解决；
- 受保护 PAUSE / STOP；
- 证据不足但继续经营会产生重大风险。

普通 Review 不自动成为 CEO Decision。

### 10.2 决定后续

Decision Slot 必须明确：当前事实、缺少什么、可选动作、影响范围、建议、来源、返回入口。处理完成后回到原 Business / Workspace / Matter，不统一回 CEO Desk 根页。

## 11. Bootstrap 体验映射

自主经营开始前，产品入口只定义为：

```text
CEO Intent
→ Research / Assistant 理解
→ Strategy Proposal
→ CEO Gate
→ Company Truth 中的 Department / Business / Workspace / Team
```

### 11.1 入口建议

| 场景 | 入口候选 | 责任 |
|---|---|---|
| CEO 还没有对应 Business | CEO Desk Assistant / New Business entry | 捕获意图并提出范围建议 |
| 已有 Business，想新增空间 | Business → 创建 Workspace / Leader Conversation | 读取现有 Company Truth，优先复用 |
| 复杂建设意图 | Assistant / 空间工程入口 | 提出 Department / Business / Workspace / Role / Capability 方案 |
| 已有责任但想改方向 | Workspace Leader Conversation / CEO Decision | 不新建第二套经营对象 |

Strategy Proposal 在 CEO Gate 前作为候选表达；确认后写回同一 Company Truth。具体创建 Wizard、字段、交互不在本轮定义。

### 11.1 不完整意图是正常入口

Bootstrap 默认接受模糊或不完整的经营意图。CEO 不需要先填写 Positioning、Strategy、Team、Workflow、Workspace Structure 或 Operating Plan；这些不是 Bootstrap 的固定表单前置。

缺少信息时，Curis 先执行：

```text
CEO Intent
→ Curis Research
→ Situation Understanding
→ Strategy Proposal
→ 必要的 CEO Gate
```

CEO Gate 只处理系统不能合理代理的 Goal、Strategy Boundary、Risk、Constraint 与 High-impact Decision。未来实现不得把 Bootstrap 退化成复杂的“新建业务配置表单”。

## 12. Bootstrap 与日常经营的边界

- Bootstrap 负责把经营意图落到已有 Company / Department / Business / Workspace 结构；
- 日常经营从 Workspace Leader 的责任与 Goal 开始；
- Company / Department / Business 只消费并聚合 Workspace 产生的经营真相；
- Assistant 可帮助理解、准备和路由，但不建立第二套 Business / Strategy / Task Truth。

## 13. Visual Baseline 对账

以下只列最小 Delta，不修改高保真或 HTML。

| Baseline | 最小变化类型 | 要求 |
|---|---|---|
| Business Visual Baseline | TEXT / DATA DELTA | Business 卡片增加用户语言经营状态、重要 Result、Risk / Need；不变成 Dashboard wall |
| XHS Workspace | TEXT / DATA DELTA；必要时 NEW INTERACTION | 在内容主面上方补本轮重点 / 当前经营 / 最新判断 / 下一步；详情通过 drawer / context pane，不拆成多个同权重主 Tab |
| RD Workspace | TEXT / DATA DELTA；必要时 NEW INTERACTION | 在研发主面旁补当前策略、Blocker、Review 判断、下一步；不把 Employee Work Area 变成主视觉 |
| Generic Workspace | TEXT / DATA DELTA | “当前工作”主面必须仍能显示当前策略、经营阶段、最近结果、下一步 |

### 13.1 视觉原则

- Domain Primary Surface 占最大视觉面积；
- Current Operating 是轻量上下文，不是大型控制台；
- Goal / Rules / Current Operating / Team Operating / Workstations 采用渐进披露；
- Matter、Decision、Exception、Handoff 优先作为对象或下钻，不重复成首页大卡片；
- 无 Global Topbar 假设，遵守 Frozen Pane-local Header；
- Runtime State 不控制 UI Expand / Collapse；
- 经营状态使用产品语言，不使用内部 Enum。

## 14. 显式 Non-Surfaces

本轮明确不创建或不把以下内容作为一级产品表面：

- Operating Lifecycle Dashboard；
- Cycle Console / 状态机可视化；
- Strategy Center；
- Learning Center；
- Review Center；
- Runtime Graph；
- 独立的每日 Closeout 页面或按钮；
- 第二套 Task / Notification / Decision 系统；
- 因自主经营新增的一级导航；
- 把 Assistant 做成固定秘书栏；
- 把 Domain Primary Surface 推翻为统一经营控制台。

## 15. 反向入口与返回合同

所有下钻必须携带：

```text
companyRef
sourceSurface
sourceObjectRef (optional)
scopeRef (optional)
matterRef (optional)
period (optional)
returnContext (optional)
```

典型动线：

```text
CEO Desk → Business → Workspace → Leader Conversation → Result / Evidence → 原 Workspace
Department → Business → Workspace → 原 Department
Business → Workspace / Employee / Insights / Meeting → 原 Business
Workspace → Strategy / Review / Result / Evidence / Leader → 原 Workspace 主面
Assistant → 任一 scoped Surface → 处理后回原问题上下文
```

`returnContext` 只恢复来源与焦点，不成为新的导航或事实存储。

## 16. Surface Mapping Matrix

| Truth | CEO Desk | Department | Business | Workspace | Leader Conversation | Detail | Hidden / Internal |
|---|---|---|---|---|---|---|---|
| Strategy | material change | summary | current summary | current hypothesis | full explanation | version / envelope | ref |
| Goal / Outcome | important progress | portfolio summary | business outcome | workspace outcome | challenge / clarify | success contract | IDs |
| Current Operating | company status | aggregate | business status | current operating | explain why | semantic-to-runtime mapping | phase enum |
| Result / Evidence | important result | cross-business result | business result | latest result | interpret sufficiency | source / freshness | raw trace |
| Review / Learning | accepted material change | summary | recent judgment | latest judgment | reasoning | full evidence | draft summaries |
| Need / Risk | Needs You | coordination | business risk | blocker / need | resolve / escalate | owner / return-stage | detector internals |
| Decision | CEO matter | escalation | business gate | conditional slot | prepare / explain | package / audit | policy refs |
| PAUSE / STOP | company attention | portfolio impact | business impact | workspace state | explain / resume | lifecycle detail | terminal rules |

## 17. 领域领导层的差异

| Leader | 主要问题 | 可见范围 | 不应越权 |
|---|---|---|---|
| Department Leader | 这些 Business 如何协同、哪里有冲突？ | Department 与 Business 聚合 | 不直接替代 Workspace 执行 |
| Business Leader | 这些 Workspace 是否共同服务 Business Strategy？ | Business 与 Workspace 组合 | 不把每个 Workstation 当 Business 总览 |
| Workspace Leader | 本轮为何这样做、结果如何、下一步是什么？ | 当前 Workspace Responsibility | 不修改 CEO Gate 之外的 Goal / Contract |

## 18. Generic Workspace 证明要求

Generic Workspace 不得因为没有行业专用 UI 就退化成项目列表。它的 Current Operating 至少能表达：

1. 当前经营阶段；
2. 当前策略 / 假设；
3. 最近真实结果；
4. 下一步和复盘时间；
5. 需要 CEO 的问题或缺口。

Generic 的“当前工作”是主面；自主经营信息以轻量上下文融入，不另建 Generic Operating Console。

## 19. 实现与产品边界

本映射不代表以下能力已经实现：

- Primary Autonomous E2E 连续两轮；
- Cross-domain Contract Proof；
- External live provider quality / cost；
- Business-scope Provider Execution；
- 全量 RD / XHS Domain migration；
- 跨层自动 Leader escalation；
- 完整的 Result / Evidence / External Business Feedback 生产链。

这些仍由 `CURRENT_STATE → active Issue → Accepted Evidence` 判断，不能用本 Review 的页面合同冒充交付。

## 20. Visual Delta 分类汇总

| 类型 | 本轮结论 |
|---|---|
| NO CHANGE | 页面层级、五个既有表面、Domain Primary Surface、Frozen Pane-local Header、无 Global Topbar |
| TEXT / DATA DELTA | 经营状态、当前重点、最新判断、已验证经验、Need / Risk、下一步 |
| STRUCTURE DELTA | 暂无授权；若 Design 发现承载不足，优先现有 Detail / Drawer / Context Pane |
| NEW INTERACTION | 条件性：点击策略、结果、判断进入 Detail；Decision / Conversation 需恢复原上下文；不新增一级 Surface |

## 21. CEO Review Questions

1. CEO 打开 Curis 第一眼能否通过 Brief / Company Operating 感知公司正在经营，而不是看到控制台？
2. 主动打扰阈值是否只覆盖 CEO Gate、高风险、责任冲突、外部结果变化和受保护 PAUSE / STOP？
3. Business 页面是否能轻量比较多个 Workspace，而不变成 Dashboard wall？
4. Workspace 是否能在不压过 Domain Primary Surface 的情况下说明“为什么做这些工作”？
5. Strategy 是否以当前重点进入 Current Operating，并通过 Detail / Conversation 展开，而不是新建 Strategy Center？
6. Review / Learning 是否只显示 material 判断，完整证据是否可按需进入？
7. Leader Conversation 是否能基于 Goal → Strategy → Result → Evidence → Learning → Next-cycle Decision 回答“为什么”？
8. Cycle 是否以“本轮经营 / 本周复盘”存在，且不暴露 Runtime phase？
9. PAUSE / STOP 是否能表达责任、历史保留和恢复/终止差异，而不让一次 Cycle Close 看起来像公司停止？
10. Generic Workspace 是否具备与 Domain Workspace 相同的经营连续性摘要？
11. Business、XHS、RD、Generic Visual Baseline 是否只需要本文件列出的最小 TEXT / DATA Delta？
12. 在不新增一级导航的前提下，现有五个表面和 Detail / Conversation 是否足以承载这些真相？

## 22. Final disposition for this review

**CEO 已接受本映射为 Approved Surface Mapping。** 本文件仍是 Review 级产品映射输入，不是新的 Product Authority，不代表 UI 或 Runtime 已实现。

接受后的下一步是：

1. UI Blueprint / Design 消费本映射中的 Visual Delta；
2. 为 Domain Primary Surface 做独立 UX Exploration；
3. 将需要实现的产品 → 实现缺口登记到正式 Issue；
4. 以真实 Runtime / Browser / Desktop / 外部结果证据逐项验收。

后续 UI Blueprint / Design 可以消费本映射中的 Visual Delta；仍不得据此直接进入代码实现，必须另有 Approved Design 与正式 Issue。

---

**CURIS AUTONOMOUS OPERATION PRODUCT SURFACE MAPPING**  
**OPERATING TRUTH MAPPED**  
**CEO DESK / DEPARTMENT / BUSINESS / WORKSPACE / LEADER CONVERSATION MAPPED**  
**PROGRESSIVE DISCLOSURE DEFINED**  
**NO OPERATING CONSOLE**  
**VISUAL DELTA REQUIREMENTS READY**  
**NO IMPLEMENTATION**  
**STOP FOR CEO REVIEW**
