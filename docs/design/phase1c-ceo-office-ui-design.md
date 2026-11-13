# Phase-1C CEO Office UI 产品与 Figma 设计

状态：产品设计已完成；Figma 原型部分完成，等待 Figma MCP 配额恢复后补齐全部页面并进行视觉验收。

日期：2026-07-10

产品归属：Workspace 产品规划席

Figma 文件：[Curis CEO Office v1 - Product Design](https://www.figma.com/design/aE7KcRhwGVXYUbwdpyLfzO)

## 1. 产品定位

Curis 不是任务管理工具，而是 AI Company Operating System。

CEO Office 是 CEO 进入自己 AI 公司总部后的第一空间：看公司运转、项目推进、员工协作、能力消耗、价值记录与知识增长；它不以待办任务或后台配置作为第一视觉语言。

```text
CEO Office
  -> Company 经营状态
  -> Project 经营目标
  -> Department 资源与责任
  -> Employee 协作状态
  -> Workflow 研发 SOP
  -> Task 执行底座
```

## 2. UX 主流程

### 已有公司 CEO

```text
进入 Curis
  -> CEO Office
  -> 查看公司经营状态与风险
  -> 打开 Project
  -> 启动或查看研发 SOP Workflow
  -> 查看 Employee Step Result 与最终报告
  -> 返回 Dashboard 复盘用量、价值记录与知识增长
```

### 首次进入 CEO

```text
欢迎成为 CEO
  -> 创建第一家 AI 公司
  -> 选择“软件研发公司 / 内容运营公司 / 电商公司 / 投资研究公司 / 自定义”
  -> 预览 CompanyPackage 的 Department、Employee、Workflow、Skill、Tool
  -> 确认生成 tenant 私有 Instance / Binding
  -> 进入 CEO Office
```

首版真实可用模板仍以 Software R&D 为准；内容、营销、电商、投资只作为未来 CompanyPackage 的产品入口预留，不能在 UI 中伪装为已可实例化能力。

## 3. 信息架构

| 一级入口 | 目的 | 主要内容 |
| --- | --- | --- |
| CEO Office | AI 公司总部大厅 | 公司状态、项目、部门、员工、经营信号 |
| Company | 公司经营配置与概览 | 公司信息、部门、项目组合、默认能力/模板来源 |
| Projects | CEO 的研发目标 | Project 状态、SOP、风险、最终报告 |
| Employees | AI 员工经营 | 员工状态、能力绑定、近期汇报 |
| Workflows | Project 驱动研发 SOP | 步骤、负责人、Step Result、最终汇总 |
| Knowledge | 公司知识沉淀 | Project Memory、执行摘要、知识来源 |

Task 不进入一级导航；它只在 Project / Workflow 的执行详情中作为内部记录出现。

## 4. 视觉方向与 Design System

### 视觉原则

- 空间感来自清晰层级、深色材质、克制阴影和宽松留白，不使用渐变、光球或装饰噪音。
- 高级感来自信息优先级与可解释经营信号，不来自夸张大标题或营销式 Hero。
- CEO Office 是“总部”，不是 ERP、SaaS 后台或 Agent 列表工具。
- 卡片圆角统一为 `16px`，浮层可使用 `20px`；所有状态必须同时依赖文字与颜色表达。
- 动效只用于层级切换、状态反馈与 Workflow 进度，建议 `160–240ms`；不做炫技动画。

### Design Token

| 类别 | Token | 值 | 用途 |
| --- | --- | --- | --- |
| Canvas | `surface/canvas` | `#0E1210` | 主空间背景 |
| Card | `surface/card` | `#171D1A` | 信息卡片 |
| Raised | `surface/card-raised` | `#202724` | 次级容器、状态标签 |
| Border | `border/default` | `#3C4741` | 低对比边界 |
| Text | `text/primary` | `#F3F7F2` | 主信息 |
| Text | `text/muted` | `#A5B3AB` | 辅助信息 |
| Action | `action/primary` | `#14B99F` | 行动、健康状态 |
| Warning | `accent/amber` | `#F59E1E` | 待决、注意 |
| Risk | `accent/coral` | `#F45245` | 风险、阻塞 |
| Flow | `accent/sky` | `#3CA5F1` | 工作流、信息状态 |

字体采用 Inter：Display `34/42`、Section `20/28`、Card `15/22`、Body `14/21`、Secondary `12/18`、Metric Label `11/16`、Metric Large `28/34`。间距使用 `4/8/12/16/20/24/32/40/48/64` 的固定节奏。

## 5. 高保真页面定义

### 5.1 CEO Office 首页

定位：AI 公司总部大厅。

布局：左侧公司级导航；顶部显示 CEO 问候、Company 状态和时间范围；主体依次显示经营指标、核心 Project、Department、Employee 状态、Token/成本、Value Event、Knowledge Growth。

必显信息：

- 公司名称、公司状态、部门数量、AI 员工数量、项目数量、今日产出、风险事项。
- 研发部负责人、员工数量、当前项目、运行状态。
- Project 目标、当前阶段、负责人、团队、Workflow 进度、风险事项。
- Employee Card：姓名、职位、状态、当前项目、最近汇报。
- AI Cost：Token 用量、模型分布、估算消耗与归因链。
- Value Widget：已记录价值事件和估算影响，明确“不是 ROI”。
- Knowledge Widget：项目知识、执行摘要、更新时间与来源。

### 5.2 Company 页面

定位：一家公司经营结构的总览与配置页。

内容：Company 身份、来源模板版本、Department 网格、Project 组合、Employee 总数、默认 Workflow、能力覆盖摘要、公司知识摘要。

关键动作：编辑公司名称/描述、查看模板来源、进入 Department / Project；不在该页直接编辑官方 Template、商业套餐或密钥。

### 5.3 Department 页面

定位：部门是 Project 分派员工与 SOP 的组织范围。

内容：部门使命、负责人、员工编制、活跃 Project、默认研发 SOP、可用 Skill/Tool/Model 覆盖、部门级阻塞事项。

首版真实部门为研发部。未来部门类型在模板选择入口可见，但 UI 必须清楚标识“未来可用”，不能假装已启用。

### 5.4 Project 页面

定位：CEO 经营研发目标的主工作页。

内容：Project 目标、状态、负责人、团队、研发 SOP、Workflow Timeline、当前步骤、Step Result、风险、最终报告、内部 Task 摘要。

关键动作：创建 Project、选择负责人、启动官方 Software R&D SOP、查看最终报告。Workflow 必须由 Project 详情触发，不单独成为 CEO 首页入口。

### 5.5 Employee 页面

定位：AI 员工经营与能力配置页。

内容：员工身份、岗位、Company/Department、生命周期状态、当前 Project、近期报告、Skill Binding、Tool/Model/Connector Binding、模板来源。

关键动作：基于模板创建员工、启用/停用、查看受限能力绑定。Persona 只作为未来安全预留，不展示或录入密钥、路由指令、Provider 配置。

### 5.6 首次创建公司页面

定位：欢迎成为 CEO 的公司启动流程。

内容：空白创建与 CompanyPackage 两条路径、模板预览、将生成的 Department/Employee/Workflow/Skill/Tool 清单、来源版本与确认提示。

前置条件：只有 Shared Contract 定义官方目录与版本读取后，才能将 CompanyPackage 从设计变为可点击的真实实例化流程。

## 6. Widget 与组件库

### 已在 Figma 建立的基础组件

- `Status Chip`：Working / Idle / Blocked / Reporting。
- `Employee Card`：身份、角色、当前 Project、状态、最近汇报。
- `Project Card`：目标、阶段、Workflow 进度、负责人、风险。
- `Department Card`：负责人、员工数、Project 数、运行状态。
- Design Token、文字样式、阴影样式与 Foundations Board。

### CEO Dashboard Widget Catalog

| 分类 | Widget | 状态 | 说明 |
| --- | --- | --- | --- |
| 公司 | Company Health | ready | Company/Project/Department 事实汇总 |
| 公司 | Department Overview | ready | 研发部状态与员工数量 |
| 项目 | Project Progress | ready | Project/Workflow 进度 |
| 项目 | Project Risk | derived | 仅展示 blocked/failed/缺失事实 |
| 员工 | Employee Status | ready | 生命周期事实映射 |
| 员工 | Employee Load | ready | 活跃 Step/Task 数量 |
| 员工 | Employee Growth | reserved | 尚无正式成长指标 |
| 成本 | Token Usage | ready | Usage Event 聚合 |
| 成本 | Model Usage | ready | 模型调用与 Token 分布 |
| 成本 | AI Cost | ready | `estimated_cost` 聚合，非账单 |
| 价值 | Value Event | reserved | 当前仅有 Contract |
| 价值 | Estimated Impact | reserved | 非 ROI、非收费 |
| 能力 | Skill Usage | partial | 缺少独立 Skill 使用归因 |
| 能力 | Tool Usage | ready | capability_type=tool 归因 |
| 知识 | Knowledge Growth | partial | 缺少统一计数数据模型 |

Widget 自定义仅允许：添加/删除 Catalog Widget、显示隐藏、排序、尺寸和受限 Company/Project/Department/时间范围。禁止任意查询、外部数据源、商业公式或跨 tenant 范围。

## 7. 交互与状态语言

| 对象 | 状态词 | UI 表达 |
| --- | --- | --- |
| Employee | Working / Idle / Waiting Decision / Blocked / Reporting | 标签、文字和活动事实 |
| Project | Planning / Development / Testing / Completed / Risk | 状态条、Workflow 进度、风险解释 |
| Workflow | Pending / Running / Succeeded / Failed / Skipped | 顺序时间线与责任人 |
| Company | Operating / Attention / Blocked | Company Health 摘要与明确原因 |

状态不依赖纯色；每个状态必须具有文字、图标/点位和可解释的事实来源。

## 8. Figma 交付状态

已创建 Figma 文件与已写入内容：

- [Curis CEO Office v1 - Product Design](https://www.figma.com/design/aE7KcRhwGVXYUbwdpyLfzO)
- `00 Cover & Product Flow` 页面。
- `01 Foundations & Components` 页面：Token、文字样式、阴影样式、Status Chip、Employee Card、Project Card、Department Card。
- `02 CEO Office Screens` 页面：CEO Office 首页高保真画板。

Figma Starter 的 MCP 调用额度在首页创建后耗尽，导致 Company、Department、Project、Employee、首次创建公司画板及最终截图 QA 尚未写入该文件。它们的完整产品规格已在本文件冻结，不可视为完成的 Figma 页面。

## 9. 后续前端开发拆分

设计确认后，按以下顺序进入独立开发 Issue：

1. CEO Office 信息架构与静态 UI Shell。
2. Company / Department 只读经营页。
3. Project 详情与 Workflow Timeline。
4. Employee 管理与能力绑定呈现。
5. Dashboard Instance / Widget 布局偏好。
6. 数据就绪度允许后的 Usage / Value / Knowledge Widget。

每个 Issue 必须引用：

- `docs/design/ceo-dashboard-product-definition.md`
- `docs/contracts/ceo-dashboard-contract.md`
- `docs/review/dashboard-data-readiness.md`
- 本文件

## 10. 严格禁止

- 未经产品确认直接开发 React UI。
- 以 Task List 取代 CEO Office、Company 或 Project 入口。
- 用 UI 反向修改后端、数据模型、Admin、Credential Vault、Workflow Runtime。
- Billing、Payment、Invoice、Marketplace、购买流程、ROI Dashboard。
- 任何明文凭据、可解析 credential_ref、Provider 原始响应或跨 tenant 数据展示。

## 11. 产品负责人确认项

在进入 `Phase-1C CEO Office UI Implementation` 前，产品负责人需要确认：

1. CEO Office 的深色经营驾驶舱视觉方向。
2. Company / Project-first 信息架构与 Task 降级为内部记录。
3. 第一版 Widget 的展示边界：估算消耗非账单，Value Event 非 ROI。
4. Figma MCP 配额恢复后补齐其余五个高保真画板并完成视觉 QA。
