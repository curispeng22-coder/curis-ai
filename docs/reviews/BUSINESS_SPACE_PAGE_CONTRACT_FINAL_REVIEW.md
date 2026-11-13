# CURIS PAGE CONTRACT FINAL REVIEW — 02 BUSINESS SPACE

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** CEO CONSOLIDATED PRODUCT DECISION APPLIED — FINAL REVIEW REQUIRED  
**日期：** 2026-08-18  
**前置：** CEO Desk Page Contract 已为 `ACCEPTED CANDIDATE — READY FOR CROSS-PAGE REVIEW`。  
**范围：** 定义 Business Space 的 Operating Work Directory、Department / Business / Workspace 直接入口、Leader Work Surface、Business / Workspace / Organization 关系、入口、返回、状态和动作；本轮同步 CEO Consolidated Operating Hierarchy，不修改 Frozen Shell、Runtime、Schema、数据库或代码。

## 0. 结论

### BUSINESS SPACE PAGE CONTRACT
**FINAL REVIEW REQUIRED — STOP FOR CEO REVIEW**

本契约按 CEO Consolidated Operating Hierarchy 更新。Business Space = **Operating Work Directory**，提供 Department、Business、Workspace 三种直接入口；它不是 Business 列表、Workspace 列表或后台数据表。进入 Department / Business 后进入对应 Leader Work Surface；进入 Workspace 后进入专业工作现场。

其中 Department Work Surface 与 Business Work Surface 只作为跨 Domain 的 **Shared Management Surface Contract Candidate**，提供共同管理骨架；具体 Domain 必须在此基础上叠加 Domain-specific Operating Surface，并通过内容增长部、研发部、小红书运营与 Curis 产品研发 UX Exploration 验证，不预设同构页面。

本文件是 Page Contract Review Candidate。CEO 接受后，可作为 UI Blueprint 的跨页面输入；仍需 Approved Design 与正式 Issue 才能开发。

## 1. Page Mission

CEO 需要 Business Space，是为了在一个地方回答：

> 公司现在经营哪些 Business？每项 Business 正在做什么、由谁负责、在哪个办公室工作、最近产生了什么真实结果、有什么风险或缺口，以及我下一步应该进入哪个经营对象。

Business Space 的职责是：

- 读取并呈现当前 Company 的 Business Portfolio；
- 让 CEO 比较业务定位、整体目标、Office 数量/状态、负责人、结果和风险；
- 进入某一 Business 的 Business Work Surface，或直接进入其 Office / Workspace；
- 从 Business Work Surface 进入整体管理、员工、组织、人才与能力、经营洞察和会议；
- 创建、复制、调整或退出 Business，创建/复制 Office；
- 让新的 Business 自动回到同一 Company Map / Organization Truth。

它不是：Project Center、Task Center、Workspace 列表页、Department 页、BI Dashboard、Organization Map、File Manager 或第二套运行控制台。

## 2. Entry / Return Contract

### 2.1 进入 Business Space

| 来源 | 进入语义 | 首个焦点 |
|---|---|---|
| 一级导航“业务空间” | 打开当前 Company 的全部当前 Business | Portfolio 中最需要 CEO 注意的 Business 变化；无 Business 时进入创建空态 |
| CEO Desk | 带 Company / Business / Matter / Result scope 进入 | 对应 Business 卡片或 Detail 的来源事项 |
| 公司版图 | Company Map 中点击 Business | 进入该 Business Work Surface；Office 按需展开 |
| 经营洞察 | 从 Business / Workspace / Result 反查 | 保留 Business、周期、分析来源和原 Matter |
| Employee Profile / Workstation | 员工所属 Business 反查 | 进入对应 Business Work Surface，保留 Employee 焦点 |
| Meeting | 会议上下文关联 Business | 进入 Business Work Surface 的相关 Decision / Commitment / Result |
| CEO Assistant | Assistant 识别 Business 或目标 | 打开对应 Business / Detail，不把回答变成第二个业务列表 |

### 2.2 返回

```text
Business Space / 来源页面
  → Business Work Surface
  → Workspace / Employee / Organization / Talent / Insights / Meeting / Result
  → 完成查看或处理
  → 原 Company + Business + Matter/Result/Employee/Workspace + Filter/Focus
```

返回必须恢复来源对象、筛选、滚动位置和焦点；如果 Business 当前事实已变更或失效，先显示当前事实、新鲜度和原因，再返回，不恢复旧快照。

## 3. Operating Work Directory IA

Business Space 的默认首页不是单一 Business Portfolio，而是 Operating Work Directory。三个直接入口是同一 Company Truth 的不同访问视角：

```text
[部门]  → Department Work Surface
[业务]  → Business Work Surface
[工作空间] → Professional Workspace
```

Object hierarchy ≠ Navigation hierarchy。CEO 不必强制 Department → Business → Workspace 逐层进入；CEO Desk、Search、Assistant、Recent、Insights 等也可以直接进入合法 Scope。

首页提供 Search、Recent / Current Work（如 Current Authority 允许）、负责人、当前工作和必要 Attention；本合同不确定 Tab、卡片或最终布局。

## 3.1 Company Truth 与直接访问

三种入口共享同一 Department / Business / Workspace / Employee Truth，不复制对象或建立第二套导航事实。

Business Space 由三类信息职责组成，不要求分别画成固定 Card 或 Dashboard Block：

1. **Business Portfolio**：公司有哪些 Business、它们各自的经营语义和最新变化；
2. **Attention / Transition**：哪些 Business 有 Risk、Blocker、Needs CEO、Staffing Gap、External Data 缺口或生命周期动作；
3. **Next Entry**：CEO 下一步应进入哪个 Business Work Surface、Office / Workspace、Result、Meeting 或相关能力入口。

目标是 **Low Surface Complexity / High Operating Information Density**。Portfolio、Attention、Result 和 Workspace 摘要可以在同一 Business 表面合并呈现；不得为了“完整”复制 CEO Desk、Insights 或 Company Map 的整块内容。

### 3.1 页面主叙事

```text
当前 Company / 业务空间
        ↓
Business Portfolio（每项业务现在怎么样）
        ↓
Attention（哪些业务需要关注或介入）
        ↓
Business Work Surface（经营全貌）
        ↓
Workspace / Employee / Result / Insights / Meeting / 组织与能力入口
```

Business Space 不默认展开全部员工，也不把 Office 直接作为一级列表替代 Business；Office 是 Business 卡片内的高频直接入口。

## 4. Business Card / Portfolio Contract

每个 Business Portfolio 单元必须让 CEO 在不打开后台字段表的情况下知道“要不要进去”。

### 4.1 Portfolio Information Responsibilities

以下是 Business Portfolio 的信息责任集合，不代表每张 Business Card 都必须始终完整可见。默认第一视觉层优先呈现：Business Name、 一句话业务目标/定位、Office 数量与 Office 快速入口、Responsible Leader、Recent Important Result；仅在存在时呈现 Risk / Needs CEO。Department、Staffing、External Object、Freshness 按当前上下文轻量表达或进入 Detail 查看。保持 Low Surface Complexity / High Operating Information Density。

| 信息 | 表达要求 |
|---|---|
| Business Name | 独立经营单元名称，可进入 Detail |
| Goal / Positioning | 目标、定位或受众的简短经营表达 |
| Department | 当前 Business 的组织归属 / 所属 Department；可为空或按需形成 |
| Current Operating State | 只使用已存在的合法生命周期状态；不自行发明健康度 |
| Responsible Leader / Employee | 当前责任主体；无责任人显示 Staffing Gap |
| Office / Workspace | Office 数量、名称/摘要、独立经营状态或“尚未配置办公室” |
| Staffing | Role / Employee Binding / Vacancy 摘要 |
| Recent / Important Result | 真实结果、验收状态或“尚无真实结果” |
| Risk / Blocker / Needs CEO | 有来源的经营事项，不用颜色替代事实 |
| External Object / Account | 当前服务的外部对象摘要，未连接显示“未连接” |
| Last Activity / Freshness | 最近事实更新时间和来源新鲜度 |

### 4.2 不应显示

- 无来源的 Healthy / At Risk / 80 分等综合健康分；
- 伪造的收入、流量、运行次数或员工负载 0；
- 全量 Task、通知和 Execution 日志；
- 全部员工和内部 Runtime 字段墙；
- 直接进入某个 Workspace 的技术路由代替 Business Work Surface。

### 4.3 Business Portfolio 动作

- 打开 Business Work Surface；
- 直接进入选定 Office / Workspace；
- 查看当前 Matter / Result；
- 复制 Business 或复制 Office；
- 打开 scoped Insights；
- 查看 Company Map / Employee / Meeting；
- 通过 Assistant 询问或准备下一步。

## 5. Business Status / Operating Facts

Business Space 不创建“健康度”产品模型。当前状态必须来自合法 Business 生命周期或来源事实，例如 `Operating`、`Paused`、`Closing` 及已确认的其他状态；不能把 UI 推断或统计分数当作 Business State。

如果当前 Runtime 没有统一 Business Operating State 的投影契约，记录为：

> **PRODUCT → IMPLEMENTATION GAP：Business Operating State Projection**

页面仍可显示真实的 Result、Risk、Blocker、Staffing、External Data、Needs CEO 和更新时间，不以综合分数补齐缺口。

## 6. Business Work Surface（合并原整体业务管理职责）

Business Work Surface 回答：

> 这项 Business 属于什么分类、整体如何经营、有哪些独立 Office、产生了什么结果，以及 CEO 可以怎样改变它。

### 6.1 Identity

Business Work Surface 是 Business Leader 的真实管理与经营工作面。Business Space 只保留一个 Business 经营工作面，不创建重复的详情页；低频编辑使用 Focus / Edit / Settings-like configuration surface。

必须可读：

- Business Name；
- Goal；
- Positioning；
- Audience / Market；
- Office / Workspace 列表与 External Object / Account 摘要；
- Company / Department 归属；
- 当前状态、成立/更新时间和来源新鲜度。

### 6.2 Operating Model

Business Work Surface 内以经营语言表达：

- Strategy；
- Workflow Definition；
- Role Structure；
- Responsibility；
- Required Capability；
- Workspace IA / 专业工作环境；
- Automation / 节奏结构（只表达业务作用，不展示 DAG）。

Operating Model 是业务如何创造结果的说明，不是技术 Workflow Editor。普通 CEO 看到的是目标、责任、步骤、能力、团队和预期结果；高级运行细节进入相应 Workspace 或审计层。

**Workflow Definition UI 位置：**当前真源确认 Operating Model 需要包含 Workflow Definition，但没有授权一个统一 Workflow Builder。页面可先提供可读的工作方式摘要、责任和下一步；完整编辑承载属于后续专项，不能在本页擅自创建通用 DAG / Workflow Center。

### 6.3 Organization / Staffing

Business Work Surface 可显示摘要：

```text
Department（可空 / 按需）
  → Role Structure
      → Employee Binding
      → Vacancy / Capacity / Responsibility
```

完整公司版图进入 Organization Center；招聘进入 Talent & Capability；Business 页不复制招聘系统。Department 不是招聘员工的强制前置，空岗可先存在，后续再形成 Department 或招募员工。

### 6.4 Operating Surface

Business Work Surface 显示：

- 当前 Office / Workspace；
- 每个 Office 的独立 Mission、External Object、Team、Current Work、Result 摘要、Needs CEO / Blocker、Last Activity；
- 当前目标、周期、责任、结果、风险和下一步；
- 外部结果和回执状态。

Business 有一个 Office 时可以突出“进入工作空间”；有多个 Office 时按 Office 说明专业职责并允许直接选择；Business Work Surface 不是 Office 的强制中转页。

### 6.5 Management Actions

Business Work Surface 的管理动作承载：编辑、复制、Pause、Reduce、Transfer、Close、Merge、Split。动作前必须展示未完成责任、External Commitment、Handoff、Employee / Capability / Capacity 变化、Workspace 影响以及 Result / Evidence / History 保留方式。

## 7. Business 聚合 Office，Office 独立经营

这是 Business Space 的硬边界：

```text
Business = 同类经营办公室的分类 / 聚合层
Office / Workspace = Business 内的独立经营单元与专业工作环境
```

一个 Business 可以拥有一个或多个独立 Office / Workspace，例如：

```text
内容增长 Business
├─ AI 科技办公室
├─ 旅游办公室
└─ 汽车办公室
```

Business Work Surface 负责整体经营；Office / Workspace 负责具体专业工作。Business Space 可直接进入 Office；Business Work Surface 不是 Office 的强制中转页。

## 8. Workspace Entry Contract

每个 Office / Workspace 摘要至少包含：

- Name 与所属 Business；
- External Account / Operating Object；
- Mission；
- Team / Employees；
- Current Work；
- Result 摘要；
- Needs CEO / Blocker；
- Last Activity / Freshness；
- 当前 Operating / Draft / Paused 等合法状态（若来源提供）。

点击 Office 进入对应专业 Workspace，而不是统一 Runtime / Workflow 页面。每个 Office 保有独立目标、策略、团队、能力、资料、排期与结果；Workspace 内部可使用各自成熟工作方式。

Workspace 不复制 Employee identity；组队只是已有员工进入该 Workspace。Workspace 失败或缺能力时，返回 Business Work Surface 必须保留缺口、Owner、下一步和原来源。

## 9. Results / Evidence

Business Space 和 Business Work Surface 只显示摘要和入口：

- Recent Result；
- Important Result；
- External Result；
- Acceptance 状态；
- Evidence 入口；
- 未记录、未连接或人工回填状态。

完整 Result 历史留在来源 Workspace / 资料库 / Result Surface；深度趋势、比较、归因和报告进入 scoped Operating Intelligence。Business Work Surface 不复制 Insights。

每个摘要至少可追溯到 Business、Workspace、Employee、Evidence、Acceptance 和 External Result；来源缺失时显式未知，不能把“已运行”写成“已产生价值”。

## 10. External Object / Account

页面层允许表达每个 Office 当前服务或经营的外部对象：一个或多个 Account、频道、客户、平台对象或其他 Domain Object。它们不是自动新增的 Business，也不构成全局 Account 层级。

External Account / Operating Object 字段应至少包括：名称/标识、所属 Office / Business、Connector / 连接状态、授权范围摘要、最近回执或数据时间、负责人和未连接原因。无真实连接显示“未连接 / 待授权 / 人工回填”，不显示 0。

一个 Business 可以包含多个独立 Office；对于账号经营 Domain，一个账号通常对应一个 Office，但具体多对象关系由 Domain Operating Model 决定。本 Page Contract 不扩展 Account Scope Switching 或 Account Matrix。Duplicate Office / Business 后，External Account、Connector、Credential 和 Permission 必须重新确认，不能直接复制绑定。

## 11. Staffing 与跨空间关系

Business Space 只显示 Staffing 摘要：Role、Employee Binding、Vacancy、Capacity / Responsibility 的最小信息。需要查看完整关系时：

- Role / Staffing → Organization Center；
- 招募外部专家 → Talent & Capability；
- Employee 详情 / 工作面 → Employee Profile / Workspace；
- 能力缺口 → Talent & Capability / Settings（按缺口类型）。

员工可以进入多个合理 Workspace，但不因组队复制身份。Role 可以属于 Operating Model；Employee 是具有公司身份的专家 / Agent，不能把专家卡片直接当员工。

## 12. Create Business

### 12.1 入口

- Business Space 空态或 `+ 创建业务`；
- Company Map / Department / Business Work Surface 的创建入口；
- CEO Desk / Assistant 的自然语言意图；
- Workspace 工程或会议中明确形成的 Business 创建意图（仍返回 Business 创建路径）。

### 12.2 创建来源

区分两条路径：

```text
Create from scratch
→ Business Name / Goal / Positioning / Audience
→ Operating Model 来源
→ Office 初始策略 / Staffing
→ 预览并确认

Duplicate existing Business
→ Copy Preview
→ 复用 / 重新配置 / 不复制
→ 确认新 Business
→ 新 Business Work Surface
```

### 12.3 当前字段

只使用已确认字段：

- Business Name；
- Goal；
- Positioning；
- Audience；
- Department（可空、后绑定）；
- Office 初始 External Account / Operating Object（不作为 Business 全局层级）；
- Operating Model 来源（从零、已有验证模型或合法模板候选）；
- Staffing 方式（空岗、已有员工绑定、重新 Staffing）；
- Office 初始策略（暂不建、创建一个、选择多个独立专业办公室）。

Business Template 与 Marketplace 的最终产品关系仍未冻结；不把模板当作已确认 Product Truth，也不新增 Template Runtime Primitive。

## 13. Business / Office Duplication

### 13.1 入口与流程

```text
Business Space / Business Work Surface → Duplicate Business
Source Business
  → Copy Preview
  → Reuse
  → Reconfigure
  → Do Not Copy
  → Confirm
  → New Business Identity
  → 同一 Business Space / Company Map
  → 新 Business Work Surface
  → 选择 Office / Staffing
```

同一 Business 内的 Office 复制入口为：`Business Space / Business Work Surface / Office … → Duplicate Office`；完成后仍属于原 Business，不创建新的 Business Identity。

### 13.2 复制边界

**可复用：**已验证 Operating Model、Strategy、Workflow Definition、Role Structure、Responsibility Structure、Required Capabilities、Workspace IA、专业界面、可复用业务方法和合理 Automation structure。

**必须重新确认：**Business Name、Goal、Positioning / Audience、External Account / Connector、Credential / Permission、Brand / Business Knowledge、Employee Staffing、Schedule / publishing cadence 及其他外部副作用。

**禁止直接复制：**Business Identity、Employee identity、Credential / Secret、Conversation history、Task / Execution、Result / Evidence、Business history、Audit history、External receipt 和当前 Runtime state。

Role 可以复制，Employee 只能重新 Binding。Duplicate Office 完成后仍属于原 Business；Duplicate Business 完成后作为独立 Company OS Business Truth 出现在 Business Space、Company Map 与对应 Office，不复制三份组织数据。

## 14. Business Exit

Business Work Surface 的管理动作消费已 Frozen 生命周期：`Pause`、`Reduce`、`Transfer`、`Close`、`Merge`、`Split`。不创建 Exit Center。

执行前必须让 CEO 看见：未完成责任、External Commitment、Handoff、Employee / Capability / Capacity 变化、受影响 Workspace、责任接收人、可恢复性以及 Result / Evidence / History / Learning 保留方式。完成后从当前 Portfolio 视图移出或转入相应状态，但历史仍可反查；Closed / Archived Business 不与当前 Operating Business 混在默认 Portfolio。

具体 Runtime 状态转换、承诺保护和证据保留若未被实现，应记录为 Product → Implementation Gap；本页不新增 Exit Primitive。

## 15. Empty / Loading / Unknown / Error

| 场景 | 页面表达 | 合法下一步 |
|---|---|---|
| No Business | “还没有业务，从第一项业务开始” | 创建业务 / 让 Assistant 帮助定义 |
| Business no Office | Business 存在但尚未配置专业办公室 | 进入 Detail，配置或创建 Office；不伪装 Operating |
| Business no Employee | Staffing Gap / 空岗及责任缺口 | 查看 Role、进入人才与能力或配置已有员工 |
| External Account not connected | 未连接 / 待授权 / 人工回填 | 进入 Connector / Settings / Business 来源页 |
| Business no Result | 尚无真实结果、结果来源或回执 | 进入 Workspace、补输入、等待或回填真实外部结果 |
| Partial failure | 某 Business 的读取失败 | 其他 Business 继续可读；失败项显示原因、重试、来源和恢复入口 |
| Loading | Portfolio、Attention、Result 等职责独立加载 | Skeleton 只表示读取中，不显示示例数值 |
| Unknown / Stale | 来源未知或已过期 | 显示原因、来源、新鲜度和下一步，不用 0 替代 |
| Archived / Closed | 历史 Business 独立查看 | 从历史筛选进入，不混入当前 Operating Portfolio |
| Runtime unavailable | 当前事实读取失败 | 返回来源 / 重新读取 / 查看诊断；不把失败渲染为已运行 |

## 16. Actions

| 动作 | 目标 | 约束 |
|---|---|---|
| Create Business | 业务创建路径 | 只使用已确认字段；创建后回新 Detail |
| Open Business | Business Work Surface | 保留 Company、Matter、筛选和焦点 |
| Enter Office / Workspace | 具体独立专业办公室 | 可从 Business Space 直接进入；不以 Office 列表替代 Business |
| Edit | Identity / Operating Model / 连接等 | 高影响变更先显示影响和返回 |
| Duplicate Business | Copy Preview → 新 Business | 不复制身份、密钥、历史或运行状态 |
| Duplicate Office | Copy Preview → 同一 Business 下的新 Office | 复用专业结构但重新确认外部对象、员工、知识、授权、排期；不复制运行事实 |
| Pause / Reduce / Transfer / Close / Merge / Split | Business Lifecycle | 先展示责任、承诺、交接、容量和保留计划 |
| View Company Map | Organization Center / Company Map | 不复制第二份 Business 列表 |
| View Employee | Employee Profile / Workstation | 由 Organization / Workspace 承载完整关系 |
| Recruit | Talent & Capability | 不在 Business 页造招聘系统 |
| Open Insights | scoped Operating Intelligence | 返回 Business / 原 Matter |
| Open Meeting | Company / Business / Workspace Meeting | 带议题和来源，不把聊天当决定 |
| Ask Assistant | 当前 Business scope | Assistant 解释、准备和路由，不新建平行 Task |

## 17. Drill-down / Reverse Entry

| 来源内容 | 点击目标 | 返回保留 |
|---|---|---|
| Business Card / Portfolio | Business Work Surface | Company、Business、筛选、焦点 |
| Office / Workspace 摘要 | Office / Workspace | Business、Office、Matter、员工焦点 |
| Employee / Staffing | Employee Profile / Workstation 或 Organization Center | Business、Role、Employee、来源事项 |
| Role / Vacancy | Organization Center | Business、Department、Role、Staffing focus |
| Capability Gap | Talent & Capability / Settings | Business、Role、Workspace、Gap、下一步 |
| Trend / Analysis | scoped Operating Intelligence | Business、period、comparison、原 Matter |
| Result | Result / Evidence Source | Business、Workspace、Owner、Evidence |
| Meeting signal | Meeting | Business、议题、参与人、承诺 |
| Assistant answer | 被引用对象 | 原问题、Business scope、Assistant focus |
| Company Map Business | Business Work Surface | Company Map focus、Business |

不能所有内容都打开万能 Drawer；需要完整经营阅读、配置或比较时进入对应产品空间。

## 18. Cross-page Boundary

| 空间 | 负责的问题 | Business Space 只保留 |
|---|---|---|
| CEO Desk | 今天发生什么、什么需要注意和决定 | Business 变化、风险、结果、Needs CEO 摘要 |
| Organization Center | 公司长成什么样、Department / Business / Role / Employee 如何组成 | Department 归属、Role / Staffing / Vacancy 摘要 |
| Talent & Capability | 专家、Skill、Connector 发现、招募、纳入和维护 | 能力缺口与进入入口 |
| Operating Intelligence | 趋势、比较、归因、分析、报告和经营评估 | 需要关注的分析结论入口 |
| Library | 本地/外部资料、索引、引用、来源和沉淀 | 资料来源摘要和证据入口 |
| Meeting | 讨论、Proposal、Decision、Commitment 和跟进 | Business 相关决定、承诺和待跟进 |
| Office / Workspace | 独立专业工作、Employee Workstation、自动协作和结果生成 | Office Mission、External Object、Team、Current Work、Result 摘要和入口 |

Company Map 和 Business Space 都可以展示 Business，但前者是组织结构视图，后者是经营 Portfolio；两者共享同一 Business Truth，不复制列表或对象。

## 19. Product → Implementation Gaps

这些是实现门，不是本文件新增产品模型，也不授权代码：

1. **Business-level Projection Gap**：需要同源投影 Business Goal、Operating State、Owner、Workspace、Staffing、Result、Risk、External Object 和 Freshness；页面不能自行拼接旧列表。
2. **Business ↔ Workspace Gap**：需要稳定引用和反查，Business Work Surface 不能把 Workspace 当 Business，Workspace 失败后要能回原 Business。
3. **Business ↔ Department Gap**：Department 可空、按需形成，Company Map 和 Business Work Surface 的归属投影必须一致。
4. **Business Operating State Gap**：若 Runtime 未提供完整合法状态集合，必须显示未知或现有事实，不由 UI 发明 Healthy / At Risk。
5. **External Account / Object Gap**：多账号、连接、授权、回执和外部结果的 scope / freshness / manual 回填需要既有 Capability / Domain Authority 支撑；本页不扩 Schema。
6. **Duplication Runtime Gap**：Copy Preview、Operating Model 复用、身份/密钥/历史隔离和新 Business Truth 需要真实持久化与恢复证据。
7. **Exit Lifecycle Gap**：Pause / Reduce / Transfer / Close / Merge / Split 的责任保护、交接、容量释放、历史保留和恢复需要真实运行链。
8. **Result Aggregation Gap**：Business 摘要必须追溯到 Workspace、Employee、Evidence、Acceptance 和 External Result，不能用静态计数代替。
9. **Staffing Projection Gap**：Role、Employee Binding、Vacancy、Capacity / Responsibility 的摘要要与 Organization Center 同源，招聘由 Talent & Capability 承载。
10. **Partial Failure Gap**：单一 Business、Workspace 或外部来源失败时，Business Space 必须保留其他业务可读并提供可恢复入口。

实现前为每个 Gap 建立正式 Issue、Allowed Files、Simulation / Browser / Desktop 验收门；本 Review 不授权实现。

## 20. Open Questions

以下是当前仍需后续 Authority / Domain Review 的真实问题，不在本轮自行回答：

1. **Business Operating State vocabulary**：除已确认生命周期状态外，最终允许投影哪些状态，哪些只属于 Runtime / 审计？
2. **Operating Model Workflow UI**：Workflow Definition 的可读摘要与可编辑承载，是否由 Business Work Surface、Workspace Studio 或 Domain Workspace 分担；不得因此创建统一 Workflow Builder。
3. **Multiple External Accounts**：哪些 Domain 可以由一个 Business 服务多个 Account，何时必须 Duplicate Business；需要 Domain Operating Model 规则。
4. **Business Template**：模板与 Duplication 的产品关系、来源、版本和可更新边界仍需单独确认。
5. **Closed / Archived Business**：历史 Business 的筛选、恢复、合并和只读范围需与 Exit Runtime 共同确认。
6. **Business Creation Staffing**：创建时默认空岗、沿用合法 Binding 或重新 Staffing 的推荐策略需由具体 Domain 验证。

这些问题不会阻塞本页面的基本 IA 和入口合同；若决定改变 Business / Workspace / Organization 的对象语义，必须另走 Product Delta。

## 21. Final Recommendation

建议 CEO 接受本文件作为 **Business Space 专项 Page Contract**，并与 CEO Desk Contract 一起进入 Cross-page Review。接受后顺序：

```text
CEO Acceptance
→ 跨页面一致性 Review（CEO Desk / Business Space / Company Map / Workspace）
→ UI Blueprint 消费本合同（不反向改 Product Truth）
→ Business Space Design Brief / Wireframe
→ Approved Design
→ 独立 Issue / Runtime Projection
→ Browser + Desktop + restart + failure/recovery 验收
```

本次已按 CEO Correction 同步三份 Current Product Truth；在 Approved Design 与正式 Issue 之前，仍不修改 Frozen Shell、Runtime、Schema、数据库或代码，不创建第二套 Business 列表、Workspace 列表、Exit Center 或招聘系统。

---

CURIS PAGE CONTRACT FINAL REVIEW  
— 02 BUSINESS SPACE · CEO CORRECTION APPLIED  
— STOP FOR CEO REVIEW
