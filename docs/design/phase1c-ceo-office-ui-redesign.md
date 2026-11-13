# Phase-1C CEO Office UI Redesign

状态：Superseded，首页产品结构已由 `docs/design/phase1c-ceo-office-ui-v3.md` 替代

日期：2026-07-10

归属：Workspace 产品规划席

## 1. 产品结论

Curis 的首页不是 Dashboard 首页，也不是任务入口，而是 CEO 进入 AI 公司总部后的经营空间。

打开页面时，用户首先感知到的是：

- 我拥有一家公司；
- 公司有组织、有目标、有正在推进的项目；
- AI 员工正在协作、等待决策或提交汇报；
- 我可以进入 Project War Room 做经营决策；
- Token、模型、成本、价值和知识是经营信号，不是页面主体。

Task 继续存在于 Workflow 与 Project 内部，但不进入一级导航、不占据首页首屏，也不作为 CEO 的默认创建入口。

## 2. 视觉方案选择

### 方案 A：未来企业总部空间（采用）

以公司、部门运行状态和核心项目为视觉主体。首屏像进入总部大厅：公司身份和战略目标位于上方，部门运行概览位于空间中心，核心项目作战室从下方露出。完整组织关系进入独立 Organization 页面，经营信号位于更低层级。

优点：最符合 AI Company OS；CEO 能先看到组织是否正常运行；公司扩展到大量部门和员工后，首页密度仍然稳定。

风险：需要严格控制信息密度，否则空间感会退化为卡片网格。

### 方案 B：硬核控制中心（部分采用）

以实时状态、运行信号、成本和风险为主要视觉元素。

优点：未来科技感强，适合 Workflow、Usage 和风险监控。

风险：容易再次成为 BI Dashboard，因此只吸收状态表达、时间线和信号带，不作为整体布局。

### 方案 C：虚拟办公世界（不采用）

通过 3D 办公室、虚拟楼层或人物场景表达 AI 公司。

优点：第一印象强。

风险：研发成本高、信息效率低、容易游戏化，且不适合 CEO 高频经营操作。

## 3. 设计理念

### 3.1 总部感来自关系，不来自装饰

空间感由 Company、Department、Employee、Project 之间的层级、连线、远近和信息优先级产生。不使用渐变背景、装饰光球、无意义发光或营销式 Hero。

### 3.2 经营对象优先于指标

首页视觉顺序固定为：

```text
公司身份与战略目标
  -> 部门运行概览
    -> 核心项目作战室
      -> CEO 待决事项与员工汇报
        -> 成本、价值、能力与知识信号
```

### 3.3 每个状态必须可解释

Working、Blocked、Waiting Decision、Risk 等状态不能只靠颜色。必须同时显示状态文字、来源对象和下一步动作。

### 3.4 配置模式与经营模式分离

默认是经营模式，页面保持克制。只有点击“调整总部”后才进入 Widget 布局编辑，显示移动、隐藏、添加模块等操作。

## 4. 总体信息架构

```text
CEO Office
├── Headquarters（总部首页）
├── Organization（AI 组织）
│   ├── Department
│   └── Employee Profile
├── Projects
│   └── Project War Room
├── Workflows（Project 内部入口为主）
├── Knowledge
└── Company Settings
```

一级导航不包含 Task。Workflow 保留查询入口，但创建和启动必须从 Project War Room 发起。

## 5. CEO Office 首页结构

### 5.1 Global Command Rail

页面左侧使用窄型总部导航轨，默认宽度 `88px`，展开后 `224px`。

包含：

- Curis 标识；
- 当前 Company 切换；
- CEO Office、Organization、Projects、Knowledge；
- 通知与 Company Settings；
- 不展示 Admin、Billing 或 Marketplace 入口。

按钮优先使用 Lucide 图标并提供 Tooltip。当前入口通过结构位置、文字和边界同时表达，不依赖单色高亮。

### 5.2 CEO Briefing Stage

首屏顶部不是指标卡，而是一块无卡片边界的总部状态区。

展示：

- 公司名称：`星云研发公司`；
- Company 状态：`运营正常`；
- 当前战略目标：`完成 AI Assistant App 第一版交付`；
- 今日公司摘要：`6 位员工在线 · 2 个项目推进中 · 1 项等待你决策`；
- 主操作：`查看待决事项`；
- 次操作：`进入核心项目`。

Company 名称是首屏最大的信息信号，战略目标是第二层。Token、成本等数字不出现在这一区域。

### 5.3 Organization Operations Overview（首屏核心）

首页不承载完整组织架构。它只回答 CEO 的三个问题：哪些部门在运转、哪个部门需要关注、当前核心项目由谁负责。

```text
CEO / 公司身份
  ├─ 研发部：负责人 · 18 位员工 · 3 个项目 · 正常
  ├─ 内容部：负责人 · 12 位员工 · 2 个项目 · 等待决策
  ├─ 市场部：负责人 · 8 位员工 · 1 个项目 · 存在风险
  └─ 查看全部 8 个部门

当前核心项目团队
  Tech Lead · Product Manager · Architect · Frontend · Backend · +12 位员工
```

部门概览单元只展示：

- Department 名称和负责人；
- 员工总数与当前在线/工作人数；
- 活跃 Project 数量；
- 阻塞、等待决策或汇报中的异常数量；
- 进入 Department 页面或完整 Organization 页面的操作。

首页展开规则：

- 默认展示最多 `4` 个核心或异常 Department，超过后合并为“查看全部部门”；
- 每个 Department 不直接展开全体员工；
- 仅在“当前核心项目团队”中展示最多 `5–7` 位关键员工，其余显示为 `+N 位员工`；
- Blocked、Waiting Decision、Reporting 员工可作为例外信号浮出，但不改变组织结构；
- 用户点击 Department 或“查看完整组织”后，进入独立 Organization 页面查看完整层级。

独立 Organization 页面负责：

- CEO → Department Lead → Employee 的完整组织树；
- 缩放、折叠、搜索、按 Department/状态/Project 筛选；
- 大规模员工节点的分区加载或虚拟化渲染；
- Employee Profile 入口和最近汇报摘要；
- 禁止把组织节点变成绩效排行榜或 Agent 管理列表。

首屏在常规桌面高度下必须露出 Project War Room 的主体入口，而不只是边缘，让用户理解部门和员工围绕项目运转。

### 5.4 CEO Decision Strip

部门概览与 Project War Room 之间是一条横向经营信号带，不使用四张等宽 KPI 卡。

只展示需要 CEO 采取行动的事项：

- `AI Assistant App 等待确认交付范围`；
- `Backend Engineer 因能力缺失被阻塞`；
- `Product Manager 提交阶段汇报`。

每条事项包含来源、影响、建议动作和进入上下文的链接。

## 6. Project War Room

Project 是 Curis 的核心经营单位。War Room 是项目的主页面，不是任务详情。

### 6.1 页面结构

```text
Project Identity + Goal
  -> Stage Rail
  -> Team Room
  -> Workflow Timeline
  -> Risks / Decisions
  -> Deliverables / Final Report
```

### 6.2 Project Identity

展示 Project 名称、经营目标、负责人、所属 Department、模板来源和当前阶段。目标文字优先于状态数字。

### 6.3 Stage Rail

固定阶段：Planning → Development → Testing → Completed；Risk 是叠加状态，不是单独流程步骤。

每个阶段显示开始时间、负责人和关键产物。阶段变化来自 Project / Workflow 事实，不能由前端伪造。

### 6.4 Team Room

使用团队关系布局展示参与员工，不使用表格。突出负责人、当前执行员工和等待接力员工。

### 6.5 Workflow Timeline

顺序展示：

```text
Tech Lead 拆解
  -> Product Manager 补充需求
    -> Architect 技术方案
      -> Frontend / Backend 交付
        -> QA 验收
          -> Tech Lead 汇总
```

每一步显示负责人、状态、Step Result 摘要和 Capability 来源。内部 Task 仅出现在步骤展开详情中。

### 6.6 Risk And Decision

风险必须包含：事实、影响、责任员工、需要 CEO 做出的选择。禁止只展示红色数字或无法解释的评分。

## 7. Employee Profile

Employee Profile 是员工工作身份页，不是 Agent 配置表单。

页面结构：

- Identity：姓名、职位、Company、Department、生命周期状态；
- Current Work：当前 Project、当前 WorkflowStep、等待事项；
- Skills：Skill 名称、来源、受限说明；
- Capabilities：Tool / Model / Connector Binding、来源和可用状态；
- Persona：仅展示已批准的非敏感工作风格与沟通偏好；
- Reports：最近阶段汇报和完成产物；
- Activity：脱敏的执行和审计摘要。

禁止展示真实密钥、Provider 原始配置、绩效排行榜、商业席位价格或未批准的员工记忆。

## 8. Dashboard Widget 系统

Widget 是 CEO Office 的经营信号层，不是页面主体。

### 8.1 默认 Widget

| Widget | 默认位置 | 表达方式 |
| --- | --- | --- |
| Company Health | Briefing Stage 辅助区 | 事实摘要，不做黑箱评分 |
| Project Progress | War Room 入口区 | 阶段与 Workflow 事实 |
| Employee Status | Organization 辅助区 | 组织节点状态汇总 |
| Token Usage | Executive Signals | 趋势与归因 |
| Model Usage | Executive Signals | 模型分布，不显示密钥 |
| AI Cost | Executive Signals | `estimated_cost`，固定标注“估算消耗” |
| Value Event | Executive Signals | 价值记录，不是 ROI |
| Knowledge Growth | Executive Signals | 来源、数量和更新时间，不评价质量 |

### 8.2 编辑模式

点击“调整总部”进入编辑模式：

- 12 列布局网格出现；
- Widget 显示移动、调整尺寸、隐藏操作；
- 右侧 Catalog Drawer 用于添加 Widget；
- 保存仅写 DashboardInstance 的布局偏好；
- 取消恢复进入编辑模式前的布局；
- 不允许创建任意查询、公式、数据源或商业规则。

## 9. 视觉系统

### 9.1 色彩

| Token | 值 | 用途 |
| --- | --- | --- |
| `hq.canvas` | `#090A0C` | 总部空间背景 |
| `hq.surface` | `#111318` | 结构表面 |
| `hq.surface.raised` | `#1B1E24` | 浮层与节点 |
| `hq.border` | `#2A2E36` | 克制边界 |
| `hq.text.primary` | `#F4F6F8` | 主信息 |
| `hq.text.secondary` | `#89919C` | 辅助信息 |
| `hq.ai` | `#4CC9F0` | Workflow、AI 活动 |
| `hq.healthy` | `#4ADE80` | 正常运行 |
| `hq.decision` | `#F5B642` | 等待决策 |
| `hq.risk` | `#FF6B6B` | 阻塞和风险 |
| `hq.human` | `#E8C27A` | CEO 与人工决策信号 |

禁止使用大面积紫蓝渐变、装饰光球和单一蓝色体系。功能状态必须采用多信号表达。

### 9.2 字体

字体栈：`-apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Segoe UI", sans-serif`。

| 层级 | 大小 / 行高 | 用途 |
| --- | --- | --- |
| Company Display | `36 / 44` | 公司名称 |
| Strategic Goal | `24 / 34` | 战略目标 |
| Section | `18 / 26` | 页面区块 |
| Card / Node Title | `14 / 20` | 组织节点和项目标题 |
| Body | `13 / 20` | 经营信息 |
| Label | `11 / 16` | 状态与来源 |

字体不随 viewport 缩放，字距固定为 `0`。

### 9.3 布局与材质

- 8px 基础网格；
- 页面最大工作宽度 `1600px`；
- 结构区域间距 `32–48px`；
- 可操作卡片圆角最大 `8px`；
- 不用嵌套卡片；
- 部门概览与 War Room 使用完整页面区域，不放进装饰容器；
- 阴影只用于浮层、Drawer 和被选中节点。

### 9.4 动效

- 页面切换：`180ms`，透明度与轻微位移；
- 部门详情展开：`220ms`；
- Workflow 状态更新：`160ms`；
- 编辑模式进入：布局网格淡入，不缩放整个页面；
- `prefers-reduced-motion` 下关闭位移动效。

## 10. 组件规划

### Shell

- `CommandRail`
- `CompanySwitcher`
- `HeadquartersHeader`
- `ContextBreadcrumb`
- `NotificationCenter`

### Headquarters

- `CompanyIdentity`
- `StrategicGoal`
- `OrganizationOperationsOverview`
- `DepartmentPulse`
- `ActiveProjectTeam`
- `EmployeeExceptionSignal`
- `DecisionStrip`
- `ExecutiveSignalBand`

### Organization

- `OrganizationCanvas`
- `DepartmentNode`
- `EmployeeNode`
- `OrganizationSearch`
- `OrganizationFilter`
- `OrganizationViewport`

### Project

- `ProjectIdentity`
- `ProjectStageRail`
- `ProjectTeamRoom`
- `WorkflowTimeline`
- `WorkflowStep`
- `RiskDecisionPanel`
- `DeliverableList`
- `FinalReport`

### Employee

- `EmployeeIdentity`
- `EmployeeState`
- `CurrentWork`
- `SkillCluster`
- `CapabilityBindingList`
- `PersonaSummary`
- `EmployeeReportFeed`

### Widget

- `WidgetShell`
- `WidgetCatalogDrawer`
- `WidgetEditToolbar`
- `CompanyHealthWidget`
- `TokenUsageWidget`
- `ModelUsageWidget`
- `AICostWidget`
- `ValueEventWidget`
- `KnowledgeGrowthWidget`

图标统一使用 Lucide。按钮只在明确命令中使用文字；常见工具操作使用图标并提供 Tooltip。

## 11. 数据映射与边界

| UI 区域 | 现有数据源 | 不可假设的数据 |
| --- | --- | --- |
| Company Identity | Company Runtime | 自动健康评分 |
| Organization Overview | Department / Employee / Project Runtime | 自动部门健康评分、绩效 |
| Full Organization | Department / Employee Runtime | 未落库的复杂汇报线、绩效 |
| Project War Room | Project / Workflow / StepResult | 复杂 DAG、预测进度 |
| Employee Profile | Employee / Skill / Capability Binding | 明文密钥、完整 Persona Runtime |
| AI Cost | Usage Event `estimated_cost` | Billing、Invoice、真实价格 |
| Value Event | Value Event Contract / future records | 自动 ROI |
| Knowledge Growth | Project Memory / Knowledge source | 知识质量评分 |

当数据未准备时，必须展示“尚未接入”或受控空状态，不使用 Mock、随机数据或伪造经营结论。

## 12. 响应式规则

### Desktop `>= 1280px`

总部首页显示部门概览、当前核心项目团队和 War Room；完整组织树只在 Organization 页面展开。

### Tablet `768–1279px`

Command Rail 收起；部门概览改为两列；核心项目团队折叠为关键成员与人数摘要；War Room 分区纵向排列。

### Mobile `< 768px`

首屏保留 Company、战略目标、部门异常摘要和待决事项；Department 使用单列摘要，不在首页加载员工树；Widget 单列排列；复杂布局编辑只允许排序和显示/隐藏。

## 13. 前端实现建议

本阶段不开发代码。设计确认后建议拆为以下实现顺序：

1. `CEO Office Shell`：Command Rail、Company Identity、Strategic Goal；
2. `Organization Overview`：Department 聚合状态、核心项目团队和异常员工信号；
3. `Project War Room`：Stage Rail、Team Room、Workflow Timeline；
4. `Full Organization`：独立页面的组织树、搜索、筛选与大规模渲染；
5. `Employee Profile`：Skill / Capability / Reports；
6. `Widget Runtime`：默认布局、编辑模式和 DashboardInstance 偏好；
7. `Executive Signals`：Usage / Value / Knowledge 的就绪数据。

建议在 `frontend/app/ceo-office/` 下按领域拆分组件，保留现有 API 语义。不得为了 UI 便利修改后端模型、Workspace/Admin 边界、Credential Vault 或 Workflow Runtime。

实现前必须建立独立 Issue，写清：允许文件、已有 API、真实数据字段、空状态、响应式验收和浏览器截图验证。

## 14. 验收标准

产品负责人确认设计时应满足：

- 首屏最大视觉信号是 Company 名称与战略目标，不是 KPI 数字；
- 首页 Organization Overview 是部门运行聚合，不是完整员工树或员工列表；
- 完整 Organization 页面保留组织关系，并可在大量部门和员工规模下搜索、折叠和分区加载；
- Project War Room 是项目经营空间，不是 Task Board；
- Employee Profile 是工作身份和能力页，不是 Agent 参数表；
- Token、模型、成本、价值和知识处于经营信号层；
- Dashboard 支持配置，但默认经营页面不是自由拼装 BI；
- 页面没有 Admin、Billing、Marketplace 或密钥治理入口；
- 用户可以明确感知“我正在经营一家 AI 公司”。

## 15. 禁止范围

- React / CSS 实现；
- 后端与数据模型修改；
- Admin Platform 修改；
- Billing、Payment、Invoice、Marketplace；
- 复杂 Workflow Engine、DAG 或调度器；
- 自动 ROI、绩效评分或知识质量评分；
- 用 Task List、表格或指标卡网格重新占据首页主体。
