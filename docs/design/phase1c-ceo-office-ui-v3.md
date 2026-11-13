# Phase-1C CEO Office UI V3.1

状态：产品方向已确认，首个有界 UI 切片已批准进入系统交付

日期：2026-07-10

产品确认日期：2026-07-11

归属：Workspace 产品规划席

替代：`docs/design/phase1c-ceo-office-ui-redesign.md` 的首页产品结构

V3.1 更新重点：

- `Organization Overview` 改为 `Organization Health`，首页只表达组织健康，不展示完整组织结构；
- `AI Cost` 改为 `AI Resource Operations`，表达 AI 资源运营，不做账单或 ROI；
- CEO 区域强化 `需要 CEO 决策` 和 `重要汇报`；
- 增加 `Strategic Meeting Room` 作为公司级战略会议入口；
- Project War Room 默认采用 CEO 视图，技术细节进入展开层；
- 视觉从偏军事控制中心调整为柔和玻璃质感、更多留白和更轻的深色空间。

## 0. 产品确认与实施条件

产品规划席确认 V3.1 作为 Phase-1C CEO Office 当前产品与视觉事实源。确认范围是页面定位、信息层级、交互原则、视觉方向和 AI Employee 形象规则，不代表所有 V3.1 模块均可立即实现。

首个实现切片由 `issues/phase1c_ceo_office_ui_first_slice.md` 约束，只允许基于现有 Workspace 真实 API 实现 CEO Office Shell、CEO Briefing、Organization Health、Core Project Command 和进入既有执行工作台的次级入口。

以下模块仍未获得 Runtime Contract，不进入首个实现切片：

- Decision Center；
- Important Reports Inbox；
- Strategic Meeting Room；
- Brainstorm Room；
- Dashboard 自由布局编辑；
- Value / Knowledge 自动聚合结论。

这些模块不得使用 Mock、静态假数据或前端推测伪装为已实现能力。其正式实现必须分别经过 Contract -> Issue -> Verification -> Product Acceptance。

## 1. 产品结论

CEO Office V3 不再以“看数据”为首页主任务，而以“经营公司”为首页主任务。

用户进入 Curis 后，首屏必须直接回答：

1. 公司现在是否正常；
2. 当前最重要的战略目标是什么；
3. 哪些事项必须由 CEO 决策；
4. 哪些项目正在推进、存在什么风险；
5. AI 员工刚刚完成了什么、正在汇报什么。

Token、模型、AI 成本、Value Event 和 Knowledge Growth 继续保留，但降级为经营信号，不定义首页结构。

核心体验语句：

> 我进入自己的 AI 公司总部，接收汇报、做出决策、推动项目，而不是查看一组系统指标。

## 2. 方向选择

### 方案 A：经营事件型总部（采用）

以战略目标、CEO 待决策、重要汇报和核心项目为主线。部门和员工围绕经营事件出现，数据作为辅助证据。

优点：最能形成 CEO 角色感；与 Project-first 产品结构一致；日常使用路径清晰。

风险：需要 Decision、Report、Project 三类信息有明确优先级，不能把所有动态都升级为通知。

### 方案 B：空间化组织总部（局部采用）

以组织关系和部门空间作为首页主体。

优点：AI 公司感强。

风险：部门和员工增多后首屏失控；容易把经营行为退化为浏览组织架构。

采用部分：部门身份、负责人、员工状态和组织入口；完整组织下沉到 Organization Center。

### 方案 C：实时数据控制中心（不作为首页）

以 Token、成本、模型、状态和趋势为主。

优点：监控效率高。

风险：最容易回到 BI Dashboard，不符合 CEO Office 定位。

保留部分：作为页面底部 Executive Signals 和按需展开的分析视图。

## 3. V3 信息架构

```text
CEO Office
├── Headquarters
│   ├── CEO Briefing
│   ├── Decision Center Preview
│   ├── Important Reports
│   ├── Core Project Command
│   ├── Organization Health
│   └── Executive Signals
├── Decision Center
├── Projects
│   └── Project War Room
├── Organization Center
│   ├── Department
│   └── AI Employee Profile
├── Strategic Meeting Room
├── Brainstorm Room
├── Knowledge
└── Company Settings
```

一级导航不包含 Task。Task 继续作为 Project、Workflow 和 Employee 内部的执行记录。

## 4. CEO Office 首页

### 4.1 首屏结构

首页采用不对称经营布局，不使用等宽指标卡网格。

```text
公司身份 / 公司状态 / 战略目标       CEO 身份 / 今日经营摘要

CEO Decision Center（需要 CEO 决策） Important Reports（重要汇报）

Core Project Command（完整横向经营区）

Organization Health

AI Resource Operations / Value / Knowledge（低层级经营信号）
```

默认桌面首屏必须完整出现 CEO Briefing、Decision Center、Important Reports 和核心项目的主要状态。组织健康可以露出入口，但不得挤占决策、汇报和项目空间。

### 4.2 CEO Briefing

顶部是一块无卡片边界的公司简报区。

展示：

- Company 名称与状态；
- 当前战略目标；
- 一句自然语言经营摘要；
- CEO 身份和当前 Company；
- 主操作：`处理需要 CEO 决策`；
- 次操作：`进入战略会议`；
- 轻入口：`发起经营讨论`。

推荐文案：

```text
星云研发公司 · 运营正常
当前战略：完成 AI Assistant App 第一版交付
今天有 2 项需要你决策，3 份重要汇报已提交，核心项目处于开发阶段。
```

禁止在顶部排列 Token、成本、员工数等大号 KPI。

### 4.3 CEO Decision Center Preview

这是首页最重要的经营区域，不是通知列表。

默认展示最多 `3` 项待决策事项，每项包含：

- 决策问题；
- 来源 Project / Department / Employee；
- 对战略目标的影响；
- 建议选项及推荐理由；
- 决策截止时间；
- `查看上下文` 与 `做出决策` 操作。

决策优先级由事实表达：阻塞项目、等待 CEO、影响交付。不得使用无法解释的 AI 黑箱分数。

完整 Decision Center 支持：

- 待处理、已决策、已过期；
- 按 Company、Department、Project 筛选；
- 查看输入证据、AI 建议和历史决策；
- 决策后写入可追踪记录。

V3.1 命名规则：

- 首页标题使用 `需要 CEO 决策`，避免弱化为普通待办；
- 事项示例包括 `API 供应商选择`、`发布范围确认`、`成本预算调整`、`需求优先级取舍`；
- 每项必须说明“不决策会阻塞什么”。

AI 可以给建议，但不能替 CEO 自动做出经营决策。

### 4.4 Important Reports

重要汇报是 CEO 对 AI 员工产生信任的核心入口。

首页只显示最多 `3` 份重要汇报：

- 汇报员工与职位；
- 所属 Project；
- 汇报类型：阶段进展、风险、交付、需要决策；
- 一句摘要；
- 提交时间；
- `阅读汇报`。

普通执行日志和 Tool 调用不得进入 Important Reports。

报告来源优先级：

```text
等待 CEO 决策
  -> Project 风险
    -> 阶段交付
      -> Employee 主动汇报
```

V3.1 展示规则：

- CEO Briefing 必须显示 `需要 CEO 决策` 与 `重要汇报` 两个入口；
- Important Reports 以 AI 员工身份呈现，不以系统日志呈现；
- 汇报卡必须出现 AI Employee 名称、职位、Persona 短语或 Skill 标签中的至少一项，强化“AI 员工在汇报”。

### 4.5 Core Project Command

Project 是首页的经营核心，不展示 Task Board。

主项目区域展示：

- Project 名称和目标；
- 当前阶段；
- Project Owner AI Employee；
- 核心团队与 `+N 位员工`；
- Workflow 当前步骤和总体进度；
- 当前主要风险；
- 最近交付物；
- `进入项目作战室`。

首页默认突出 `1` 个核心项目，最多补充 `2` 个次要项目摘要。项目过多时进入 Projects 页面，不在首页横向堆叠。

### 4.6 Organization Health

首页不显示完整组织树，也不显示员工列表。

默认展示最多 `3` 个核心或异常 Department，并表达组织运行健康，而不是组织架构浏览：

- Department 名称；
- Department Lead；
- AI Employee 数量；
- 活跃 Project 数量；
- 状态：运行正常、等待决策、存在风险；
- 当前健康原因：交付正常、等待 CEO、能力不足、负载过高；
- `进入部门`。

超过三个部门时显示 `进入组织中心`，完整组织在 Organization Center 通过搜索、筛选、折叠和分区加载展示。

只有 Blocked、Waiting Decision、Reporting 的员工可作为异常信号浮出；其他员工只在部门、项目或完整组织上下文中展示。

### 4.7 AI Resource Operations And Executive Signals

AI 经营数据保留为页面底部连续信号带或轻量玻璃区域，不做大面积卡片网格。

包含：

- Token Usage；
- Model Usage；
- AI Resource Operations，包含 Token、模型、能力负载和估算消耗；
- Value Event，固定标注“价值记录，不是 ROI”；
- Knowledge Growth。

每项只显示当前值、变化方向和归因入口。详细趋势进入独立分析层或 Widget 展开态。

禁止标题使用 `AI Cost` 作为独立大模块，避免让 CEO Office 看起来像账单后台。

## 5. Organization Center

Organization Center 是完整 AI 组织的管理与理解空间。

### 5.1 默认视图

先显示 Department，再按需展开 Employee：

```text
CEO
  -> Department Lead
    -> AI Employee Team
```

支持：

- 搜索 Department / Employee；
- 按状态、Project、Skill 筛选；
- Department 折叠与展开；
- 大规模员工的分区加载或虚拟化；
- 进入 Department 和 AI Employee Profile。

不做绩效排行榜，不把 AI Employee 做成 Agent 参数列表。

### 5.2 Department 页面

展示：

- 部门使命和当前目标；
- Department Lead；
- 当前 Projects；
- AI Employee 团队；
- 部门 Workflow；
- 风险与待决事项；
- 最近汇报。

## 6. AI Employee Profile

AI Employee 是有身份、职责和能力边界的公司员工，不是模型配置项。

### 6.1 核心信息

- 名称；
- 职位和所属 Department；
- 生命周期状态；
- Persona 摘要；
- Skills；
- Tools / Models / Connectors；
- 当前 Project 和 Workflow Step；
- 最近汇报与交付物。

### 6.2 展示原则

- Persona 用工作方式和沟通风格表达，不展示长 Prompt；
- Skill 用能力领域表达，不展示内部路由参数；
- Capability 显示 official / tenant_private 来源和可用状态；
- AI Employee 默认使用与首页一致的虚拟人物形象，可以带 AI 身份徽章、光效边框或职位标签；
- 参考已确认首页图的 AI 员工风格：轻卡通、半写实、专业虚拟人物，保留一点“数字员工”的非真人距离感；
- 不使用照片级真人、过度拟人化肖像或真人员工摄影风格；
- 不得把 AI Employee 默认画成机器人、机械头像、工具图标或模型图标；
- 机器人/自动化图标只能用于 Tool、Workflow 自动化、系统能力或空状态，不能代表员工身份；
- 不展示明文 credential、Provider 原始配置或商业席位价格；
- 不展示无法解释的绩效分数。

## 7. Project War Room

Project War Room 是 CEO 推动项目的主要工作空间。

页面顺序：

```text
Project Goal
  -> AI Project Owner / Team
    -> CEO View Workflow
      -> Needs CEO Decision
        -> Project Knowledge Chain
          -> Technical Details
            -> Final Report
```

必须展示：

- 项目目标和成功标准；
- Project Owner AI Employee，不使用真人项目负责人概念；
- 项目团队；
- 当前阶段；
- Workflow Timeline 的 CEO 摘要；
- 当前负责 AI 员工和下一位接力 AI 员工；
- 需要 CEO 决策的干预点；
- Project Knowledge Chain；
- StepResult、交付物和最终汇报；
- 可展开的技术详情。

Task 仅在 Workflow Step 详情中出现。

### 7.1 CEO View First

Project War Room 默认进入 CEO 视图，不直接展示工程日志、API 调用、credential resolver、usage_event 或 audit_event 原始细节。

CEO 视图必须先回答：

1. 项目目标是什么；
2. 当前处于哪个阶段；
3. 哪位 AI 员工负责；
4. 哪些步骤已经完成；
5. 哪些事项需要 CEO 决策；
6. 最终报告和项目知识沉淀在哪里。

技术详情通过 `展开技术详情` 打开，包含：

- WorkflowStep 原始状态；
- StepAssignment；
- Capability / Tool / Model 调用归因；
- credential_ref resolver 结果的脱敏状态；
- usage_event / audit_event 脱敏记录；
- 错误码和调试信息。

### 7.2 Project Goal Area

工作流页面顶部必须有项目目标区域，不以进度条作为第一视觉。

推荐结构：

```text
项目目标：完成 AI Assistant App 第一版可演示交付
成功标准：核心问答链路可用、私有模型可执行、QA 通过、本地演示稳定
AI 项目负责人：林序 · Tech Lead AI Employee
当前阶段：研发协作执行中
```

### 7.3 Needs CEO Decision

工作流页的 CEO 干预区命名为 `需要 CEO 决策`。

默认展示示例：

- API 供应商选择：DeepSeek / New API fallback / 官方模型；
- 发布范围确认：本地演示、私测、还是对外演示；
- 成本预算调整：是否允许本轮工作流继续消耗更高模型额度。

每个干预点必须包含：

- 决策问题；
- 影响范围；
- AI 团队建议；
- 截止时间；
- `查看上下文` 与 `确认决策`。

### 7.4 Project Knowledge Chain

底部协作产物统一命名为 `Project Knowledge Chain` / `项目知识链`。

项目知识链表达每一步如何沉淀到 Knowledge Memory：

```text
需求理解
  -> 技术方案
    -> 前端实现记录
      -> 后端实现记录
        -> QA 验收
          -> Tech Lead 最终报告
            -> Knowledge Memory
```

不得使用 `协作产物` 作为主标题，因为最终产品心智是知识记忆沉淀，而不是文件列表。

## 8. Brainstorm Room

Brainstorm Room 是从想法到 Project 的经营入口，不是聊天机器人首页。

Strategic Meeting Room 与 Brainstorm Room 分工：

- Strategic Meeting Room：公司级战略会议，处理目标、优先级、资源、风险和 CEO 决策；
- Brainstorm Room：创意探索入口，把想法转化为 Project Proposal。

两个入口都必须在 Runtime Contract 通过后才能实现正式交互。

### 8.1 目标流程

```text
CEO 提出想法
  -> 选择或接受推荐讨论团队
    -> AI 员工按职责提出观点
      -> 形成目标、范围、风险和资源建议
        -> 生成 Project Proposal
          -> CEO 确认后创建 Project
```

### 8.2 页面结构

- Idea Brief：CEO 输入想法、目标和约束；
- Discussion Team：显示参与员工、职位和讨论职责；
- Discussion Thread：按主题组织观点，不做无序聊天流；
- Synthesis：目标、机会、风险、建议方案；
- Project Proposal：项目名称、目标、Owner、Team、建议 Workflow；
- 主操作：`确认创建项目`；
- 次操作：`继续讨论`。

### 8.3 边界

现有 Runtime 尚未证明具备 Brainstorm Session、Discussion Message、Project Proposal 的正式数据契约。V3 只定义入口和体验；进入实现前必须单独建立 Contract / Issue / Gate，不得用前端假数据伪造讨论过程。

## 9. Dashboard Widget 规则

CEO Office 支持 Widget，但默认首页不是自由拼装的 BI Dashboard。

### 9.1 可配置范围

CEO 可以：

- 调整 Organization Overview、Executive Signals、Important Reports 的顺序；
- 隐藏或添加批准的 Widget；
- 调整支持的尺寸；
- 保存 DashboardInstance 布局。

### 9.2 固定经营骨架

以下结构默认不可移除：

- Company Identity；
- Strategic Goal；
- Decision Center Preview；
- Core Project Command。

这样可以避免自定义后重新退化为数据卡片大屏。

## 10. 视觉语言

### 10.1 总部感

- 使用更轻的深色石墨蓝空间，减少纯黑压迫感；
- Company 名称、战略目标、决策和项目目标是最大视觉信号；
- 通过连续空间、分隔线、信息远近建立总部感；
- 少用封闭卡片，避免卡片嵌套；
- 使用克制的玻璃质感、柔和背景光和充分留白；
- 不使用军事控制中心式重黑、密集边框、高压告警墙；
- 不使用装饰渐变、光球、紫蓝大面积背景或 3D 办公室。

V3.1 视觉修正：

- 首屏最多两个强视觉面，其他内容以轻量分区表达；
- 卡片密度降低，区块之间保留更大的呼吸空间；
- 背景允许有柔和空间光，但不得做离散装饰光球；
- 玻璃面板只用于核心经营区域，避免全屏卡片堆叠；
- 文字层级优先表达 Company、Strategy、Decision、Project Goal。

### 10.2 状态色

- Cyan：AI 运行与 Workflow；
- Green：正常运行；
- Amber：等待 CEO 决策；
- Red：阻塞和风险；
- Gold：CEO 与人工决策。

颜色必须配合文字和图标，不单独承担状态含义。

### 10.3 降低 BI 感的规则

- 首屏不出现四张或更多等宽 KPI 卡；
- 不用环形图表达无法解释的公司健康度；
- 不把部门、项目和员工都压缩成相同卡片；
- 数字必须依附于 Company、Project、Department 或 Employee 上下文；
- 趋势图只在用户主动展开经营信号时出现。

## 11. 关键交互流程

### 11.1 日常经营

```text
进入 CEO Office
  -> 阅读公司简报
    -> 处理 CEO 待决事项
      -> 查看重要汇报
        -> 进入核心 Project War Room
```

### 11.2 从想法到项目

```text
发起经营讨论
  -> Brainstorm Room
    -> AI 团队讨论
      -> Project Proposal
        -> CEO 确认
          -> 创建 Project
```

### 11.3 从异常到责任上下文

```text
发现风险信号
  -> 查看影响 Project
    -> 查看负责 Employee / Workflow Step
      -> 做出决策或进入汇报
```

## 12. 数据就绪与实现 Gate

| V3 区域 | 当前可复用数据 | 实现前缺口 |
| --- | --- | --- |
| CEO Briefing | Company / Project / Department / Employee | 自然语言摘要规则 |
| Organization Health | Department / Employee / Project | 聚合 Read Model 可用性确认 |
| Core Project Command | Project / Workflow / StepResult | 首页核心项目选择规则 |
| AI Resource Operations | Usage / Value / Knowledge | 部分聚合字段仍需核验 |
| Decision Center | 风险与状态事实 | Decision Runtime Contract |
| Important Reports | StepResult / Final Report | Report Inbox Contract |
| Brainstorm Room | Employee / Project Template | Brainstorm Runtime Contract |
| Strategic Meeting Room | Company / Project / Decision | Strategic Meeting Runtime Contract |

设计不得反向修改 Company OS 架构。缺少 Contract 的区域只能进入后续 Gate，不得在第一实现切片中伪造数据。

## 13. 响应式原则

### Desktop `>= 1280px`

Decision Center 与 Important Reports 形成主次区域；核心项目横向完整展示；组织健康最多三个 Department。

### Tablet `768–1279px`

Decision Center 与 Important Reports 纵向排列；核心项目保留目标、AI Owner、Workflow 和风险；Department 两列。

### Mobile `< 768px`

顺序固定为：公司简报 → 需要 CEO 决策 → 核心项目 → 重要汇报 → 组织健康异常 → AI 资源运营。完整组织树、复杂 Widget 编辑和多列 War Room 不在移动首屏展开。

## 14. 后续实现拆分建议

本阶段不开发代码。设计确认后按独立 Issue 推进：

1. V3 Shell + CEO Briefing；
2. Organization Health + Core Project Command；
3. Organization Center + AI Employee Profile；
4. Decision Center + Important Reports，仅在 Contract 通过后；
5. Project War Room CEO View + Technical Details 展开层；
6. Strategic Meeting Room / Brainstorm Room，仅在对应 Runtime Contract / Gate 通过后；
7. AI Resource Operations + Widget Layout。

每个 UI Issue 必须由产品规划席定义页面层级、状态和验收，开发团队不得自行改变产品结构或视觉方向。

## 15. 产品验收标准

- 用户进入首页首先看到公司、战略、待决策和核心项目；
- 首页没有完整组织树、员工列表、Task List 或 KPI 卡片网格；
- 首页使用组织健康，不使用组织结构堆叠；
- Project 明显是经营核心，Task 只在执行上下文出现；
- AI Employee 以职位、Persona、Skill、当前 Project 和汇报建立员工感；
- Decision Center 是 CEO 决策入口，不是通知中心；
- Project War Room 默认展示 CEO 视图，技术详情默认收起；
- Brainstorm Room 的结果是 Project Proposal，不是无目标聊天；
- Token、模型、AI 资源运营、Value Event、Knowledge Growth 保留但处于辅助层；
- 工作流底部沉淀为项目知识链并最终进入 Knowledge Memory；
- 页面不包含 Billing、Payment、Invoice、Marketplace 或真实密钥治理；
- 用户能明确感知“我正在经营一家 AI 公司”。

## 16. 本阶段禁止范围

- React / CSS 实现；
- 后端、API 或数据模型修改；
- Admin Platform 修改；
- Decision、Report 或 Brainstorm Runtime 的无 Contract 实现；
- Billing、Payment、Invoice、Marketplace；
- 复杂 DAG、自动 CEO 决策、自动 ROI；
- 用 Mock 数据伪造经营结论。
