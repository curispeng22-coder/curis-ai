# Taskade 竞品档案

> 研究对象：Taskade（taskade.com）— AI-first 任务管理 + Agent 自动化平台
> 研究目的：判断任务管理与 AI Agent 的结合模式、工作流模板组织、团队协作与 AI 自动化的边界、对 Curis workflow template 的启发。
> 研究时点：2026-07-09
> 研究者：research-extra
> 关联档案：`crewai-examples.md`（模板组织）、`openclaw-agents.md`（skill 市场）

## 基本信息

| 项目 | 值 |
| --- | --- |
| 项目名 | Taskade |
| 官网 | https://www.taskade.com/ |
| 模板库 | https://www.taskade.com/templates |
| Agent 库 | https://www.taskade.com/agents |
| 自动化库 | https://www.taskade.com/automate |
| AI 应用生成器 | Taskade Genesis（`/generate`） |
| 定位 | AI-first 项目/任务管理 + Agent 自动化平台 |
| 部署 | SaaS（闭源），无开源版本 |
| 模板规模 | 1000+ AI 项目模板，9 大分类 |
| Agent 规模 | 数百 AI Agent，9 大分类 |
| 自动化规模 | 9 大分类，含 Business-in-a-Box 整套包 |
| 集成 | 100+ 应用（Slack/Gmail/Drive/GitHub/Stripe 等） |
| 商业模式 | 按席位订阅 + AI credits 用量计费 |
| 安全合规 | SOC 2 Type II 对齐（认证中） |
| 核心抽象 | Workspace DNA = Memory + Intelligence + Execution |

## 核心定位

Taskade 把自己定位为"**AI Workforce 平台**"——用 AI Agent + 自动化替代传统 SaaS 工具栈。它的核心承诺是：

> Build apps from templates instead of starting from scratch. 1000+ AI-powered project templates for productivity, business automation, and team collaboration. Transform templates into living apps with agents, automations, and memory.

与传统任务管理工具（Asana / Monday / Trello）的差异：Taskade 把 AI Agent 作为**一等公民**嵌入到每个项目模板中，模板不再是"空白结构"，而是"自带 AI 队友 + 自动化流程 + 示例数据"的活系统。

与 Curis 的相关点：Curis Phase-4 的 `WorkflowTemplate` 设计需要回答"模板里应包含什么"。Taskade 给出了一个偏激进的答案（结构 + Agent + 自动化 + 数据全打包），Curis 应借鉴其分层但不照搬其打包粒度。

## 核心架构：Workspace DNA

Taskade 的所有能力围绕 **Workspace DNA** 三层架构组织：

```
┌─────────────────────────────────────────┐
│  Workspace DNA                          │
├─────────────────────────────────────────┤
│  Memory (Projects)      — 结构化数据    │
│     ↕                                   │
│  Intelligence (Agents)  — AI 决策       │
│     ↕                                   │
│  Execution (Automations) — 工作流执行   │
└─────────────────────────────────────────┘
```

| 层 | 职责 | Curis 对应概念 |
| --- | --- | --- |
| Memory（项目） | 文档、数据库、结构化数据 | `KnowledgeEntity` + `Conversation` 状态 |
| Intelligence（Agent） | AI 队友，读 Memory、做决策、触发 Execution | `Employee` + `CapabilityBinding` |
| Execution（自动化） | 触发器 + 动作 + AI 路由 | `Workflow` + `WorkflowStep` |

**反馈循环**：Execution 的结果回流到 Memory，Agent 从 Memory 学习，形成自改进循环。Taskade 称之为"living software"。

## 核心功能矩阵

| 功能 | 描述 | 模板化程度 | 对 Curis 的相关度 |
| --- | --- | --- | --- |
| 项目模板 | 1000+ AI 模板，9 大分类 | 极高 | 高 |
| AI Agent 库 | 数百预置 Agent，9 大分类 | 极高 | 高 |
| 自动化模板 | 9 大分类，含 Business-in-a-Box | 极高 | 高 |
| Taskade Genesis | 从 prompt 生成完整应用 | 中 | 中（Phase-5+） |
| 多视图 | List / Board / Calendar / Mind Map / Doc | 中 | 低 |
| 多 Agent 协作 | Agent 间通过 workspace 共享上下文 | 中 | 高 |
| AI 训练 | 自动从项目/文件/URL/对话学习 | 中 | 中 |
| 集成 | 100+ 应用原生 + webhook | 中 | 中 |
| 团队协作 | 实时协作、共享、权限 | 中 | 中 |
| AI credits 计费 | 按 Agent 动作消耗 credits | 低 | 高（计费模式参考） |
| Community Gallery | 用户发布模板，可被 fork | 高 | 高 |
| 安全隔离 | Workspace 隔离 + 权限控制 + 审计日志 | 中 | 高 |

## 模板组织方式

### 模板三件套

Taskade 的模板不是单一概念，而是三类并行：

| 类型 | URL | 规模 | 本质 |
| --- | --- | --- | --- |
| **Project Templates** | `/templates` | 1000+ | 项目结构（视图、字段、布局） |
| **AI Agents** | `/agents` | 数百 | AI 队友（角色、训练数据、指令） |
| **Automations** | `/automate` | 9 大类 | 工作流（触发器、动作、条件） |

三者可独立使用，也可组合成"活系统"。模板 FAQ 明确：

> Each template comes with:
> - Project structure — Organized views, fields, and layouts
> - Pre-trained agents — AI teammates configured for specific tasks
> - Automation flows — Workflows that trigger on events
> - Sample content — Examples you can customize or replace

### Project Template 分类（9 大类）

| 分类 | 模板数 | 典型模板 | Curis 对应 |
| --- | --- | --- | --- |
| Featured | 30 | Taskade Kits Collection / Digital Bullet Journal / Blog Post | 精选包 |
| ChatGPT Templates | 58 | Task Manager / Novel Writing / Content Marketing | AI-first 模板 |
| Table Templates | 85 | Inventory / E-commerce Order Tracker / Public Speaking | 数据库式 |
| Personal | 65 | Letter of Recommendation / Two Week Notice / CV | 个人场景 |
| Project Management | 43 | AI Project Dashboard / Team Capacity Planner / Task Management Dashboard | 项目治理 |
| Sales | 101 | AI CRM Dashboard / Client Booking / Sales Funnel | 销售域 |
| Flowchart | — | 流程图、决策树 | 流程建模 |
| Task Management | — | 多视图待办 | 任务管理 |
| Engineering | — | Sprint / Release / Bug Tracking | 工程域 |

### AI Agent 分类（9 大类）

| 分类 | Agent 数 | 典型 Agent | Curis 对应角色 |
| --- | --- | --- | --- |
| Featured | 30 | Math Solver / To-Do Manager / Blog Creator | 通用员工 |
| Project Management | 41 | Product Dev Advisor / Training & Onboarding / Knowledge Mgmt | 项目经理类 |
| Productivity | 43 | Stress Reduction / Time Management / Pet Care | 个人生产力 |
| Marketing | 46 | Slogan / Digital Marketing / Website Critic | 营销专员 |
| Translator | 43 | Portuguese / Turkish / Italian | 翻译员 |
| Content | 82 | Multi-Channel Optimization / B2B Strategy / Testimonial Curation | 内容创作者 |
| Workflow | — | 多步骤流程协调 | Workflow 编排者 |
| Research | — | 来源收集、信息分析、知识库更新 | 研究员 |
| Personal | — | 日历、习惯、日常任务 | 个人助理 |

### Automation 分类（9 大类）

| 分类 | 典型自动化 | Curis 对应 Workflow |
| --- | --- | --- |
| Featured | Full Funnel Lead / Customer Support Triage / Revenue Ops | 端到端业务流 |
| Business-in-a-Box | Freelancer / Agency / Consulting | 整套业务包 |
| Investor Ops | Fundraising CRM / Monthly Update / Due Diligence | 投资域 |
| Education | Enrollment / Progress / Assignment | 教育域 |
| Healthcare | Patient Intake / Appointment Reminder / Care Plan | 医疗域 |
| Real Estate | Lead Qualification / Listing Generator / Showing Scheduler | 房产域 |
| Stripe | 支付、订阅、财务 | 金融域 |
| Sales | Pipeline / Lead Scoring / Playbook | 销售域 |
| E-commerce | 订单、库存、客服 | 电商域 |

**Business-in-a-Box** 是 Taskade 最独特的打包方式：一个"模板"= 完整业务系统（含多个 Agent + 多个 Automation + 多个 Project 结构 + Dashboard）。例如 `freelancer-command-center` 包含客户门户、项目跟踪、时间记录、发票、自动跟进。

## AI Agent 与模板的结合模式

### Agent 训练：Workspace DNA 自动学习

Taskade 的 Agent 不需要 ML 专业知识或数据标注。训练通过 Workspace DNA 自动完成：

> Training process:
> 1. Create an agent and describe its role
> 2. Connect it to relevant projects and data sources
> 3. Give it instructions in natural language
> 4. Let it learn from real interactions

**学习来源**：
- Projects（文档、数据库、结构化数据）
- Files（PDF、表格、上传内容）
- URLs（网站、文档、知识库）
- Conversations（历史交互与决策）

### 多 Agent 协作

Taskade 支持多 Agent 团队编排：

> Example team setup:
> - Research Agent — Gathers information from the web
> - Analysis Agent — Processes data and identifies patterns
> - Writer Agent — Drafts content based on findings
> - Review Agent — Checks quality and suggests improvements

Agent 间通过 workspace 共享上下文，一个 Agent 的输出成为另一个的输入。这与 CrewAI 的 Crew 模式一致，但 Taskade 把协作放在 workspace 层而非代码层。

### 模板中的预置 Agent

模板可自带预训练 Agent。例如：

- CRM 模板 → 自带"线索资格审查 + 跟进邮件草拟"Agent
- 内容日历模板 → 自带"选题建议 + 草稿撰写"Agent
- 会议纪要模板 → 自带"讨论总结 + 行动项提取"Agent
- 支持收件箱模板 → 自带"工单分类 + 响应建议"Agent

> These agents inherit the template's context automatically. They understand the structure and can start working immediately after you fork.

## 工作流自动化机制

### 自动化三要素

Taskade 自动化由三部分组成：

| 要素 | 说明 | Curis 对应 |
| --- | --- | --- |
| **Triggers** | 表单提交、定时、webhook | `WorkflowTrigger` |
| **Actions** | 发邮件、更新数据库、调 API | `WorkflowStep.action` |
| **AI Decisions** | Agent 分析上下文并路由 | `WorkflowStep.assigned_employee_id` + 条件分支 |

### 自动化构建方式

三种等价入口：

1. **Prompt 生成** — 用自然语言描述，Genesis AI App Builder 生成
2. **模板 fork** — 从 `/automate` 选预置模板定制
3. **从零构建** — 可视化 builder 连接触发器/条件/动作

### 与 Zapier/Make 的差异

Taskade 明确对标 Zapier/Make：

| 维度 | Zapier/Make | Taskade |
| --- | --- | --- |
| 核心 | 数据搬运 | 数据 + 智能 |
| 决策 | if-then 规则 | 上下文决策 |
| 位置 | 独立于工作 | 嵌入 workspace |
| 计费 | 按任务计费 | 无限自动化 |
| 连接 | 通用集成 | workspace 感知 |

**关键差异**：Zapier 把数据从 A 搬到 B；Taskade 让 Agent 读取数据、理解意图、决定动作，即使遇到未预设场景也能处理。

### 自动化与 Memory 的闭环

> The cycle:
> 1. Memory (Projects) stores your data
> 2. Intelligence (Agents) reads and analyzes it
> 3. Execution (Automations) takes action
> 4. Results flow back into Memory

这是 Taskade "living software" 的核心：自动化结果回流到项目数据库，Agent 从结果学习，下次决策更准。

## 团队协作与 AI 自动化的边界

Taskade 对"人 vs AI"的边界定义：

| 维度 | 人类团队 | AI Agent |
| --- | --- | --- |
| 工作时间 | 工作时段 | 24/7 |
| 上下文记忆 | 跨会话遗忘 | 持久上下文 |
| 协作方式 | 实时协作、评论、@mention | 通过 workspace 共享、自动化触发 |
| 权限 | 席位权限 | workspace 隔离 + 权限控制 + 审计日志 |
| 成本 | 按席位订阅 | 按 AI credits 用量 |

**边界原则**（来自 FAQ）：

> Agents operate within your workspace boundaries. They enhance your work without compromising your privacy.

具体安全措施：
- **Workspace 隔离** — Agent 不能访问 scope 外数据
- **权限控制** — 定义每个 Agent 可读写的内容
- **审计日志** — 追踪 Agent 的每个动作
- **SOC 2 Type II 对齐**（认证中）
- **数据保护** — 数据不用于训练外部 AI 模型

### AI Credits 计费模型

| 行为 | 是否消耗 credits |
| --- | --- |
| 克隆模板 | 否（免费） |
| 非 AI 功能（项目、任务、视图、协作） | 否 |
| 触发 AI 功能（Agent 对话、内容生成、AI 自动化） | 是 |
| 模型相关 | 轻量模型（Gemini Flash / Claude Haiku）最便宜，前沿推理模型最贵 |
| 公开 Agent 链接访客交互 | 否（不消耗 owner credits） |

## 与 Curis Admin Platform 的关系

### 可借鉴的设计

1. **Workspace DNA 三层分离**：Memory / Intelligence / Execution 的分层清晰。Curis 应在 schema 层明确分离：
   - Memory → `KnowledgeEntity` + `ConversationState`
   - Intelligence → `Employee` + `CapabilityBinding` + `Persona`
   - Execution → `Workflow` + `WorkflowStep` + `WorkflowTrigger`
   三层通过引用关联，不交叉实现。

2. **模板三件套分离**：Project Template / Agent / Automation 三类独立，可组合。Curis 不应把所有内容塞进单一 `CompanyPack`，而应分三类：
   - `EmployeeTemplate`（对应 Agent）
   - `WorkflowTemplate`（对应 Automation）
   - `WorkspaceTemplate`（对应 Project 结构 + 视图）
   三者通过 `CompanyPack` 组合，但各自独立可复用。

3. **预置 Agent 与模板绑定**：模板自带"懂该模板上下文"的 Agent。Curis 的 `WorkflowTemplate` 可声明 `recommended_employees`，fork 后 Admin 可一键激活对应 `EmployeeTemplate`。

4. **Business-in-a-Box 整套包**：Taskade 的 `freelancer-command-center` 等是"完整业务系统"。Curis Phase-5+ 可考虑"行业包"（如 `healthcare-clinic-pack` / `real-estate-brokerage-pack`），包含部门、员工、工作流、能力绑定的完整集合。但 Phase-4 应聚焦单维度模板，避免打包过重。

5. **AI Credits 计费模型**：按 Agent 动作计费，非 AI 功能免费。Curis 的计费应类似：
   - 模板克隆免费
   - 非 AI 治理功能（CRUD、权限）免费
   - LLM 调用按 token 计费（通过 `ProviderBinding` 透传）
   - 公开 Workspace 链接的访客交互不消耗租户 credits

6. **Workspace 隔离 + 审计日志**：Agent 不能访问 scope 外数据，所有动作有审计。Curis 的多租户隔离必须满足：跨租户数据零泄露，Agent 动作全审计。

7. **三种自动化构建入口等价**：Prompt 生成 / 模板 fork / 从零构建。Curis Phase-5+ 可提供等价入口，但 Phase-4 仅做"模板 fork + 表单编辑"。

8. **与 Zapier/Make 的差异化定位**：Taskade 强调"数据 + 智能"vs"纯数据搬运"。Curis 在定位 Workflow 时应同样强调"AI 决策"而非"规则路由"，否则与 n8n/Zapier 无差异。

9. **Community Gallery 模式**：用户发布模板，他人 fork。Curis marketplace 可借鉴，但需保留 Admin 强审核（参考 OpenClaw 的 Trust Envelope）。

### 不应借鉴的设计

1. **1000+ 模板规模**：Taskade 的模板数量导致发现性问题，用户难以选择。Curis Phase-4 应控制规模：官方维护 30-50 个高质量模板，远期开放社区贡献但保留强治理。

2. **闭源 SaaS 模式**：Taskade 是闭源 SaaS。Curis 是面向企业的 Admin Platform，必须支持私有化部署与数据自持。

3. **Agent 自动从对话学习**：Taskade 的 Agent 从历史交互自动学习。Curis Phase-4 不应让 Employee 自动学习；学习必须通过 Admin 显式更新 `Persona` 或 `CapabilityBinding`，避免行为漂移。

4. **Genesis AI App Builder**（从 prompt 生成应用）：Phase-4 不做。生成的应用无法治理、无法审计，与 Admin Platform 的强治理目标冲突。

5. **模板含 Sample Content**：Taskade 模板带示例数据。Curis 模板应**不含**示例数据，避免租户间数据混淆；示例数据应作为独立的 `demo_dataset`，由 Admin 显式加载。

6. **AI Decisions 嵌入自动化**：Taskade 在自动化中嵌入 AI 路由。Curis Phase-4 的 Workflow 应是**声明式编排**，AI 决策通过 `WorkflowStep.assigned_employee_id` 显式委派，而非隐式 AI 路由。

7. **公开 Agent 链接**：Taskade 允许公开 Agent 链接，访客交互不消耗 owner credits。Curis 不应在 Phase-4 暴露公开链接；所有 Employee 交互必须在租户认证后进行。

8. **9 大分类过细**：Taskade 模板/Agent/自动化各有 9 大分类，交叉过多。Curis Phase-4 应使用更粗的分类（如 4-5 个 domain：通用 / 工程 / 销售 / 运营 / 客户成功），避免分类爆炸。

9. **"替代 SaaS"的营销话术**：Taskade 称"用一个 Agent 替代 Intercom+Zendesk+Freshdesk"。Curis 不应承诺"替代"现有系统；Curis 是 Admin Platform，定位是"治理 AI 员工"，而非替代业务系统。

### 对 Curis Workflow Template 的具体启发

Curis `WorkflowTemplate` 应包含的字段（综合 Taskade 与 CrewAI Examples）：

```text
WorkflowTemplate:
  id: string
  name: string
  description: string
  domain: enum                          // 通用/工程/销售/运营/客户成功
  complexity: enum                      // 初级/中级/高级
  trigger:
    type: enum                          // manual / scheduled / event / webhook
    config: object                      // 触发器配置
  steps: [WorkflowStep]
  recommended_employees: [EmployeeTemplateRef]   // 借鉴 Taskade 预置 Agent
  required_capabilities: [CapabilityRef]         // 借鉴 CrewAI tools 声明
  expected_output: string               // 借鉴 CrewAI expected_output
  schema_version: string
  source_stamp: enum                    // official / tenant_private / marketplace
```

`WorkflowStep`：

```text
WorkflowStep:
  id: string
  instruction: string                   // 任务指令（借鉴 CrewAI description）
  expected_output: string               // 输出契约（强制）
  assigned_employee_id: EmployeeRef     // 借鉴 Taskade Agent 绑定
  context_refs: [StepRef]               // 借鉴 CrewAI context 依赖
  capability_bindings: [CapabilityRef]  // 该步骤可用能力
  output_schema_ref: SchemaRef          // 结构化输出（可选）
```

### 对 Curis 计费模型的启发

借鉴 Taskade 的 credits 模型，Curis 计费应分三层：

| 层 | 计费对象 | 说明 |
| --- | --- | --- |
| 平台订阅 | 按租户席位 | 治理功能、CRUD、权限 |
| LLM 用量 | 按 token 透传 | 通过 `ProviderBinding` 走客户自己的 LLM 账号 |
| Marketplace | 免费 | Capability 与模板上架/下载免费 |

**关键决策**：Curis 不在 marketplace 层引入交易（与 OpenClaw 一致），不在 LLM 层加价（与 Taskade credits 不同），仅按席位订阅 + token 透传。

## 结论

Taskade 的核心贡献是验证了"**任务管理 + AI Agent + 自动化**"三位一体的产品形态，以及"**模板自带 AI 队友**"的打包方式。它的 Workspace DNA 三层架构（Memory / Intelligence / Execution）是 Curis schema 分层的直接参考。

Curis 应**采纳**：
- Workspace DNA 三层分离
- 模板三件套独立可组合（Employee / Workflow / Workspace）
- Business-in-a-Box 整套包模式（Phase-5+）
- AI Credits 计费分层的思路（但 Curis 用 token 透传）
- Workspace 隔离 + 审计日志

Curis 应**拒绝**：
- 1000+ 模板规模
- 闭源 SaaS 部署
- Agent 自动学习导致行为漂移
- Genesis 式 prompt 生成应用
- 模板含示例数据
- 隐式 AI 路由
- 公开 Agent 链接
- "替代 SaaS"的定位话术

Taskade 的 Business-in-a-Box 是 Curis Phase-5+ "行业包"的参考形态，但 Phase-4 应聚焦单维度模板（EmployeeTemplate / WorkflowTemplate 各自独立），避免打包过重导致治理复杂度上升。

## 是否影响 capability_type 设计

**间接影响**。Taskade 没有显式的 `capability_type` 概念，它的 Agent 能力通过"连接的项目/文件/URL/集成"隐式定义。但其三类模板（Project / Agent / Automation）的分离印证了 Curis 应将 `Capability` 独立于 `Employee` 与 `Workflow`：

- `EmployeeTemplate` 定义"谁是员工"
- `WorkflowTemplate` 定义"如何编排"
- `CapabilityPack` 定义"员工能做什么"（独立于前两者）

Taskade 的"100+ 集成"暗示 Curis `capability_type` 需要 `external_integration` 类型，但其隐式定义方式不可取。Curis 应保持 OpenClaw 档案中建议的 6 值枚举（`builtin` / `declarative` / `external_api` / `local_tool` / `custom_code` / `marketplace_skill`），并将 Taskade 式的"集成"归入 `external_api` 类型，需 `ProviderBinding`。

综合三份档案（CrewAI Examples / OpenClaw / Taskade）的结论：Curis `capability_type` 的 6 值枚举设计是稳健的，应作为 Phase-3.5 治理文档的输入。
