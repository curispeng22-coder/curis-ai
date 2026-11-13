# Paperclip 竞品与架构分析报告

**日期**：2026-07-08
**研究任务**：深度研究 — Paperclip 竞品与架构分析
**分析对象**：https://github.com/paperclipai/paperclip (v2026.707.0, 2,978 commits)
**对比基准**：Curis Workspace Tool System v1.8 (AI Task Executor MVP)

---

## 执行摘要

Paperclip 是一个面向 **AI 代理公司的控制平面（Control Plane）**，定位为"自主经济的骨干基础设施"。其核心理念是通过公司（Company）、组织架构（Org Chart）、目标层级（Goal Hierarchy）、任务（Issue）、预算（Budget）和审批（Approval）来管理由 AI 代理组成的虚拟公司。

与 Curis 相比，Paperclip 在 **公司级组织管理、代理编排、成本追踪、审批治理** 方面成熟度远超 Curis，但其 **多租户隔离、任务执行引擎、自演化系统** 方面弱于 Curis。两者在定位上存在显著差异：Paperclip 是"代理公司的操作面板"，Curis 是"AI 任务执行器 + 企业级多租户平台"。

**核心结论：不建议 fork 或复用任何 Paperclip 代码，但应系统性地参考其产品设计。** Paperclip 的技术栈（Node.js/TypeScript/React/pnpm monorepo）与 Curis（Python FastAPI/SQLite/Next.js）完全不兼容，且其架构决策与 Curis 的多租户商业化路线存在结构性冲突。但在产品形态、治理模型、模板系统和成本追踪方面，Paperclip 提供了极具参考价值的设计范式。

---

## 1. Paperclip 数据模型分析

### 1.1 核心实体层级

```text
Company (公司)
  ├── Goal (目标层级: company → team → agent → task)
  ├── Agent (代理/员工, 严格树状 reports_to)
  │     ├── AgentApiKey (代理认证)
  │     ├── HeartbeatRun (心跳运行)
  │     └── AdapterConfig (适配器配置 JSONB)
  ├── Project (项目, 可关联 Goal)
  │     └── Issue (任务, 核心工作单元)
  │           ├── IssueComment (评论)
  │           ├── Document (文档, Markdown, 仅追加修订)
  │           ├── Attachment (附件)
  │           └── WorkProduct (工作产物)
  ├── Approval (审批: hire_agent / approve_ceo_strategy / budget_override)
  ├── CostEvent (成本事件: input_tokens, output_tokens, cost_cents)
  ├── ActivityLog (审计日志)
  ├── CompanySecret (密钥管理, local_encrypted 提供者)
  └── Plugin (插件注册)
```

### 1.2 关键数据表对比

| 维度 | Paperclip | Curis Workspace |
|------|-----------|-----------------|
| **组织单元** | Company（单实例多公司） | Tenant（真实多租户, tenant_id 列过滤） |
| **员工/代理** | Agent（多代理, 树状汇报, 适配器驱动） | 无（单例 AIEmployee 协调器, 无 CRUD） |
| **任务模型** | Issue（层级父子, 原子签出, 单一受托人） | Task（扁平, state_flow JSON, 无签出） |
| **工作流** | 无（代理外部自行编排） | Workflow/AutoWorkflow（步骤级编排） |
| **目标对齐** | Goal（四级层级, company→team→agent→task） | 无（任务无目标溯源） |
| **成本追踪** | CostEvent（token 级, 按 agent/issue/project 聚合） | execution_scores（评分制, 无货币化） |
| **预算控制** | 公司+代理月度预算, 软警报(80%)+硬停止(100%) | 无 |
| **审批治理** | Approval（招聘/策略/预算覆盖） | GovernanceProposal（部门开关, 两级治理） |
| **密钥管理** | CompanySecret + UserSecret, local_encrypted 提供者 | 零凭证（明确禁止） |
| **审计日志** | ActivityLog（actor_type, action, entity_type） | EvolutionEvent（correlation_id, idempotency_key） |
| **插件系统** | Plugin SDK + sandbox-providers（Daytona 等） | 无（capability catalog 作为未来 hook） |
| **数据库** | PostgreSQL（嵌入式或外部, Drizzle ORM） | SQLite（单文件, 无 ORM） |

### 1.3 数据模型评估

Paperclip 的数据模型在 **公司治理完整性** 方面显著领先：
- **目标溯源链**：每个 Issue 通过 parent_id 链最终追溯到 Company Goal，保证了代理行为的一致性对齐
- **原子签出**：`POST /issues/:id/checkout` 使用单条 SQL UPDATE + WHERE 条件实现无锁冲突安全
- **成本事件流**：CostEvent 以独立事件流形式摄入，支持按 agent/issue/project/company 多维度聚合

Curis 的数据模型在 **执行深度** 方面领先：
- **state_flow JSON** 记录了任务从 INIT→PARSED→RUNNING→COMPLETED/FAILED 的完整状态转换
- **execution_patterns** 跨租户学习成功模式，支持自演化
- **architecture_locks** 提供了精细化的模块级安全边界

---

## 2. Paperclip 代理编排机制

### 2.1 心跳模型（Heartbeat-Based）

Paperclip 的核心编排模式是 **心跳驱动** 的拉取模型：

```text
调度器 (Scheduler)
  │
  ├── 检查: 代理是否 paused/terminated/达到预算硬限制?
  ├── 检查: 是否有活跃运行 (maxConcurrentRuns)?
  │
  └── 触发心跳 → Adapter.invoke(agent, context)
                    │
                    ├── Process适配器: 启动子进程, 流式 stdout/stderr
                    ├── HTTP适配器: 出站 HTTP 请求, 可选回调异步完成
                    ├── Local CLI适配器: Claude Code / Codex / Gemini / Cursor
                    ├── OpenClaw网关: 远程代理 webhook 回调
                    └── External Plugin: 动态加载的外部适配器包
```

**与 Curis 的差异**：
- Paperclip：代理**自我驱动**，心跳触发后代理自行决定做什么、调用什么工具、何时完成
- Curis：任务**引擎驱动**，Orchestrator 生成工作流步骤，AIEmployee 逐步执行，工具链由 ToolRouter 选择

### 2.2 上下文交付模式

Paperclip 支持两种上下文策略：
- **Thin 模式**：仅发送 ID 和指针，代理通过 API 拉取上下文
- **Fat 模式**：包含当前分配、目标摘要、预算快照和最近评论

Curis 的上下文管理更简单：每一步执行时，前一步的 output 累积到上下文中传递给下一步。

### 2.3 代理适配器接口

```typescript
interface AgentAdapter {
  invoke(agent: Agent, context: InvocationContext): Promise<InvokeResult>;
  status(run: HeartbeatRun): Promise<RunStatus>;
  cancel(run: HeartbeatRun): Promise<void>;
}
```

Paperclip 适配器是**外部运行时的桥梁**，而 Curis 的 ToolRouter/ToolExecutor 是**内部执行的选择器**。两者设计哲学完全不同。

### 2.4 多代理组织架构

Paperclip 支持严格的**树状汇报结构**（`agents.reports_to`），形成 CEO → CTO → 工程师 等多层级代理组织。代理可以通过审批流程招聘新代理，CEO 可以向董事会提交策略提案。

Curis 当前**完全没有多代理模型**——只有一个单例 AIEmployee。

---

## 3. Paperclip 插件、外部工具与沙箱机制

### 3.1 插件系统架构

Paperclip 的插件系统分为多个层次：

```text
packages/plugins/
├── sdk/                          # 核心 SDK（类型定义、API 接口）
├── create-paperclip-plugin/      # 插件生成器 CLI
├── sandbox-providers/            # 沙箱提供者集合
│   ├── daytona/                  # Daytona 沙箱（完整生命周期管理）
│   └── ...                       # 其他提供者
├── paperclip-plugin-fake-sandbox/ # 虚拟沙箱（测试用）
├── plugin-llm-wiki/              # LLM Wiki 插件
├── plugin-workspace-diff/        # 工作区差异比较
└── examples/                     # 示例代码
```

### 3.2 沙箱提供者能力

沙箱提供者（Sandbox Provider）是插件系统的核心扩展点，支持：
- **工作区生命周期管理**：启动/停止沙箱工作区
- **交互式设置**：在沙箱中运行配置命令
- **模板捕获**：将配置好的沙箱状态保存为可复用的自定义镜像
- **探针检测**：沙箱健康检查和状态探测

### 3.3 适配器插件

Paperclip 支持外部适配器插件通过 `~/.paperclip/adapter-plugins.json` 动态加载：
- 服务端适配器注册表（mutable `registerServerAdapter`/`unregisterServerAdapter`）
- UI 适配器注册表（mutable `registerUIAdapter`/`unregisterUIAdapter`）
- 共享 schema 的 `adapterType` 验证从硬编码 enum 改为开放式字符串

### 3.4 与 Curis 对比

| 维度 | Paperclip | Curis |
|------|-----------|-------|
| 插件 SDK | ✅ 完整 SDK + CLI 生成器 | ❌ 无（capability catalog 仅蓝图） |
| 沙箱 | ✅ Daytona + Fake + 可扩展 | ✅ EvolutionGovernor sandbox（仅内部演进验证用） |
| 适配器扩展 | ✅ 外部适配器插件 + 动态注册 | ❌ 无 |
| 市场/分发 | ❌ 云市场不在 V1 范围 | ❌ 无 |
| 模型网关 | ❌ 适配器直连模型提供商 | ✅ ModelGatewayAdapter（New API 兼容） |

---

## 4. Paperclip 成本追踪与治理机制

### 4.1 成本追踪系统

Paperclip 的成本追踪是 **token 级实时事件流**：

```typescript
// POST /companies/:companyId/cost-events
{
  "agentId": "uuid",
  "issueId": "uuid",        // 可选：归因到具体任务
  "provider": "openai",
  "model": "gpt-5",
  "inputTokens": 1234,
  "outputTokens": 567,
  "costCents": 89,           // 以美分为单位
  "occurredAt": "2026-02-17T20:25:00Z",
  "billingCode": "optional"
}
```

**聚合维度**：
- `GET /companies/:companyId/costs/summary` — 总览
- `GET /companies/:companyId/costs/by-agent` — 按代理
- `GET /companies/:companyId/costs/by-project` — 按项目

### 4.2 预算执行机制

Paperclip 的预算是**双层硬执行**：

```
预算周期: 每月 UTC 日历窗口

软警报（80%）:
  → 发出通知
  → 代理继续运行

硬限制（100%）:
  → 代理状态设为 paused
  → 阻止新的签出和心跳调用
  → 发出高优先级活动事件
  → 仅董事会可覆盖（提高预算或显式恢复代理）
```

### 4.3 审批治理流程

Paperclip 有四种审批类型：
1. **hire_agent** — 招聘新代理
2. **approve_ceo_strategy** — CEO 策略提案
3. **budget_override_required** — 预算覆盖
4. **request_board_approval** — 通用董事会审批

审批流：`pending` → `approved`/`rejected`/`cancelled`（终态）

### 4.4 与 Curis 对比

| 维度 | Paperclip | Curis |
|------|-----------|-------|
| 成本计量 | token 级, cents 精度, 实时事件流 | execution_scores 评分制（speed/correctness/efficiency） |
| 预算控制 | 双层(80%警报+100%硬停), 月度窗口 | 无 |
| 审批治理 | 4 种审批类型, 完整生命周期 | GovernanceProposal（部门开关, CEO 参与） |
| 成本归因 | agent/issue/project/company 多维度 | 无归因模型 |
| 货币化 | 美元计费就绪 | 无货币化设计 |

---

## 5. Paperclip Companies 模板与 Curis Department Template 对比

### 5.1 Paperclip 的公司可移植性包

Paperclip 设计了一套 Markdown 优先的公司模板系统：

```
COMPANY.md                # 根定义（目标、品牌、设置）
├── agents/               # 代理定义（角色、适配器配置）
├── goals/                # 目标层级
├── issues/               # 初始任务（可选）
└── .paperclip.yaml       # Paperclip 特定保真度（元数据、设置）
```

关键特性：
- **导出**：生成供应商中立的 Markdown 包，模板导出仅含结构不含状态
- **导入**：支持创建新公司（rename/skip/replace 冲突策略），支持预览（试运行）
- **规范基础包**：与供应商无关的设计，`.paperclip.yaml` 仅增补 Paperclip 特定属性

### 5.2 Paperclip 的技能目录（Skills Catalog）

```
packages/skills-catalog/
├── catalog/
│   ├── bundled/           # 捆绑技能（推荐默认项）
│   │   └── <category>/<slug>/SKILL.md
│   └── optional/          # 可选技能（角色/领域特定）
│       └── <category>/<slug>/SKILL.md
└── generated/catalog.json # 自动生成的清单
```

技能是 Markdown 格式的操作指令，支持：
- **来源标识**：bundled / optional-catalog / runtime / adapter-provided
- **审批门控**：敏感操作（财务、法律、凭证）需审批
- **安全原则**：故障封闭（fail-closed），外部指令从属于 Paperclip 治理规则
- **安装管理**：CLI `paperclipai skills install` + Board UI + API

### 5.3 Curis 的部门模板系统

Curis 采用 **部门类型目录 + Manifest + 实例化** 三层模型：

```
department_types (type_key)      # 系统级目录（跨租户共享）
  ├── business.general           # 通用业务
  ├── function.hr                # 人事
  ├── function.admin             # 行政（ROI 指标）
  └── function.bi                # 商业智能

DepartmentManifest (7 个契约字段):
  capability_set, tool_classes, quality_lines,
  output_channels, roi_schema, guardrail_refs,
  employee_role_spec

Department Instance               # 租户级实例化
  └── department_observations     # 自可观测快照（D3）
```

**两级治理**（ADR-0025）：
- **类型级**：新增部门类型需要 gate + ADR
- **实例级**：CEO 在现有类型中启用/禁用部门，仅需配置变更 + 审计日志

### 5.4 对比评估

| 维度 | Paperclip Companies Template | Curis Department Template |
|------|------------------------------|---------------------------|
| 格式 | Markdown（COMPANY.md）+ YAML 侧车 | 数据库记录 + Manifest JSON |
| 可移植性 | 文件系统导出/导入，供应商中立 | 数据库内，跨实例不直接移植 |
| 模板复用 | COMPANY.md 作为蓝图创建新公司 | 部门类型作为目录，租户按需激活 |
| 治理 | 无类型级/实例级区分 | 两级治理（类型级 gate，实例级配置） |
| 技能/能力 | Skills Catalog（Markdown 指令） | Manifest（声明式契约，当前占位符） |
| 成熟度 | 已实现导出/导入全流程 | D2-D4 已实现，Manifest 仍为占位符 |

**Paperclip 的 COMPANY.md 模板设计在可移植性方面明显优于 Curis 的纯数据库方案。** 文件系统基础的可移植包天然支持版本控制（Git）、分享（GitHub）和 CI/CD 集成。

---

## 6. Paperclip 与 Curis 多租户架构差异

### 6.1 架构对比

| 维度 | Paperclip | Curis Workspace |
|------|-----------|-----------------|
| **租户模型** | 单租户部署，多公司（单实例内 Company 隔离） | 真实多租户（tenant_id 列过滤，共享 DB） |
| **隔离边界** | Company 级（所有业务实体 company-scoped） | Tenant 级（所有核心表带 tenant_id） |
| **数据库** | PostgreSQL（嵌入式或外部） | SQLite（单文件） |
| **认证** | Board 会话 + Agent API Key（Bearer Token） | X-Tenant-Id 头部 + X-Ceo-Id 头部 |
| **密钥管理** | CompanySecret + UserSecret（加密存储） | 零凭证（明确禁止） |
| **平台管理** | 无独立 Admin Platform 概念 | Admin Platform（`/api/platform/*`）与 Workspace 分离 |
| **能力供应** | 插件通过 adapter-plugins.json 本地安装 | Capability Catalog（official/tenant_private/marketplace 来源） |
| **部署模式** | local_trusted / authenticated，支持 lan/tailnet | 仅本地开发（生产托管明确禁止） |

### 6.2 关键差异分析

**Paperclip 的 Company 隔离 vs Curis 的 Tenant 隔离**：

Paperclip 的 Company 是一个"逻辑公司"：一个 Paperclip 实例可以运行多个 Company，每个 Company 有独立的代理、目标、预算和审批流。但其隔离依赖代码纪律（company-scoped routes），没有数据库级别的强制隔离。

Curis 的 Tenant 是真正的"租户"：通过中间件级 `TenantContext` 自动注入，所有数据层读写由上下文变量限定的 tenant_id 过滤。这在 SaaS 多租户场景中更加安全。

**Curis 的唯一优势在于多租户隔离的安全性和 admin-platform 与 workspace 的分离**，这使之更适合商业化平台路线。Paperclip 更适合单一组织自托管部署。

---

## 7. 复用判断与建议

### 7.1 综合评估矩阵

| 评估维度 | 仅参考产品设计 | 复用部分架构 | Fork 二次开发 | 不参考 |
|----------|:---:|:---:|:---:|:---:|
| 数据模型（Company/Agent/Goal/Cost） | ✅ | ❌ | ❌ | — |
| 代理编排（Heartbeat + Adapter） | ✅ | ❌ | ❌ | — |
| 任务模型（Issue 层级 + 原子签出） | ✅ | ❌ | ❌ | — |
| 成本追踪（token 级事件流 + 预算硬执行） | ✅ | ❌ | ❌ | — |
| 审批治理（4 种审批类型） | ✅ | ❌ | ❌ | — |
| 公司模板（COMPANY.md + 导入/导出） | ✅ | ❌ | ❌ | — |
| 技能目录（Skills Catalog） | ✅ | ❌ | ❌ | — |
| 插件系统（SDK + 沙箱提供者） | ✅ | ❌ | ❌ | — |
| 前端 UI（React/Tailwind/shadcn） | — | ❌ | ❌ | ✅ |
| 后端技术栈（Node.js/Express/Drizzle） | — | ❌ | ❌ | ✅ |
| 数据库（PostgreSQL） | — | ❌ | ❌ | ✅ |

### 7.2 明确建议：**仅参考产品设计，不复用代码/架构**

**技术性理由**：

1. **技术栈完全不兼容**：Paperclip = Node.js/TypeScript/Express/Drizzle/PostgreSQL/React/Tailwind/shadcn/pnpm monorepo。Curis = Python/FastAPI/SQLite/Next.js。fork 或复用代码意味着引入完全异构的技术栈，维护成本和认知负担不可接受。

2. **多租户模型冲突**：Paperclip 的单实例多 Company 模型与 Curis 的 tenant_id 列过滤模型在底层设计上存在结构性差异。强行融合会导致安全边界模糊。

3. **数据库选型冲突**：Paperclip 依赖 PostgreSQL（Drizzle ORM、JSONB、事务性迁移），Curis 使用 SQLite（零依赖、单文件部署）。PostgreSQL 的正确使用（JSONB 查询、并发签出、事务隔离）在 SQLite 中需要完全重写。

4. **执行模型根本不同**：Paperclip 是外部代理自主执行 + 心跳监控（拉取模型），Curis 是内部引擎逐步编排 + 工具链路由（推送模型）。两个模型互斥，无法融合。

**不应该 fork 的强化理由**：

- Paperclip 有 2,978 次提交，代码库庞大且快速演进（日均数十次提交）
- 维护一个 fork 需要持续跟踪上游变更，而 Curis 团队规模有限
- Paperclip 采用 MIT 许可证，fork 无法律障碍，但实际维护成本远超收益

### 7.3 具体参考建议（按优先级排列）

#### P0 — 应立即参考的设计范式

**（1）任务模型升级：引入 Issue 层级 + 原子签出**

Paperclip 的 Issue 模型的核心优势在于：
- **目标溯源链**：每个 Issue 通过 parent_id 最终追溯到 Company Goal
- **原子签出**：`WHERE id = ? AND status IN (?) AND (assignee IS NULL OR assignee = ?)` 无锁并发安全
- **单受托人模型**：明确责任归属

Curis 当前 Task 模型是扁平的，没有父任务、目标对齐或签出机制。建议在 Curis 的未来迭代中参考 Paperclip 的 Issue 模型设计层级任务。

**（2）成本追踪：从评分制演进到 token 事件流**

Paperclip 的 CostEvent 模型提供了三个关键设计：
- 独立事件流（非聚合行锁），适合高频写入
- 多维度归因（agent/issue/project/company）
- 预算双层执行（软警报 + 硬停止）

Curis 当前仅通过 `execution_scores` 做定性评分，没有量化的成本计量。这是未来 L6 经济层的基础。

**（3）组织架构：从单例到代理树**

Paperclip 的 Agent 树状组织 + 心跳编排是 Curis 从"单任务执行器"演进到"多代理公司系统"的唯一成熟参考。关键设计要素：
- `reports_to` 树状结构（无循环保证）
- 适配器配置决定代理行为
- 代理通过审批招聘新代理

#### P1 — 中期规划参考

**（4）公司模板系统：Markdown 优先的可移植包**

Paperclip 的 COMPANY.md + .paperclip.yaml 模式优于 Curis 的纯数据库方案。建议 Curis 的 Department Template / Business Pack 设计参考此模式：
- 根定义文件（DEPARTMENT.md）
- 子文件夹按约定（agents/、goals/、tools/）
- 平台特定侧车文件（.curis.yaml）增补元数据
- 导出/导入支持冲突策略（rename/skip/replace）

**（5）审批治理：细粒度审批类型**

Paperclip 的四种审批类型（hire_agent / approve_ceo_strategy / budget_override / request_board_approval）可作为 Curis GovernanceProposal 的类型扩展参考。

**（6）技能系统：Markdown 指令 + 来源标识**

Paperclip 的 Skills Catalog（bundled/optional/runtime/adapter-provided 四类来源 + 审批门控）可作为 Curis 未来能力目录的"操作指令"层设计参考。

#### P2 — 长期关注

**（7）插件 SDK 设计**

Paperclip 的插件 SDK + 沙箱提供者接口是一个成熟的扩展架构，值得在 Curis 需要外部连接器/第三方能力时参考。

**（8）设计系统**

Paperclip 的 DESIGN.md + Token Layer + Storybook 可视化回归测试是前端工程化的优秀实践。

### 7.4 不应参考的部分

| Paperclip 设计 | 原因 |
|----------------|------|
| 单实例多 Company 隔离 | Curis 已实现更安全的 tenant_id 列级隔离 |
| 嵌入式 PostgreSQL | Curis 的 SQLite 零配置部署更适合 MVP 阶段 |
| 外部代理自主执行模型 | Curis 的引擎驱动编排更可控、更可观测 |
| React/shadcn UI | Curis 使用 Next.js，技术栈差异 |

### 7.5 竞品跟踪建议

Paperclip 是一个活跃项目（日均数十次提交），建议建立定期跟踪机制：

- **跟踪频率**：每月一次
- **关注重点**：
  - Plugin Marketplace 上线（当前 V1 范围外）
  - ClipHub/ClipMart 公共模板市场
  - 多成员董事会治理
  - 知识库插件发布
  - 部署模式演进（托管部署 → 开放公司）
- **跟踪方式**：GitHub Watch releases + 阅读 CHANGELOG/discussions

---

## 附录 A：Paperclip 技术栈速览

| 层面 | 技术 |
|------|------|
| 后端框架 | Express (Node.js/TypeScript) |
| 数据库 | PostgreSQL (Drizzle ORM) |
| 嵌入式 DB | embedded-postgres (零配置开发) |
| 前端框架 | React + Vite |
| UI 组件库 | shadcn + Tailwind CSS v4 |
| 设计系统 | DESIGN.md + Token Layer (CSS custom properties) |
| 测试 | Vitest (单元) + Playwright (E2E) + Storybook (可视化回归) |
| 包管理 | pnpm workspace monorepo |
| 构建工具 | esbuild (CLI), rollup (插件) |
| 代码生成 | Claude Fable 5, GPT-5 Codex (大量 AI 辅助开发) |
| CI/CD | GitHub Actions |
| 许可证 | MIT |

## 附录 B：Paperclip V1 里程碑与 Curis 当前状态对照

| Paperclip 里程碑 | 内容 | Curis 对应状态 |
|------------------|------|----------------|
| M1: 公司核心+认证 | companies 表, Board 会话, Agent API Key | ✅ Tenant 已实现, ❌ Agent API Key |
| M2: 任务+治理 | 原子签出, 审批工作流 | ⚠️ 任务模型扁平, ✅ 部门级治理 |
| M3: 心跳+适配器 | Adapter 接口, Process/HTTP 适配器 | ❌ 无代理心跳, ✅ ToolRouter 工具链 |
| M4: 成本+预算 | CostEvent, 月度预算, 硬停止 | ❌ 无成本追踪, ⚠️ execution_scores 评分制 |
| M5: 董事会 UI | 仪表板, 组织图, 审批页面 | ✅ 统一控制台, ⚠️ 无组织图 |
| M6: 加固发布 | E2E, 种子模板, 发布检查清单 | ⚠️ 155 测试通过, ❌ 无模板系统 |

---

*报告完成。本报告基于 2026-07-08 对 Paperclip 仓库 master 分支的深度分析，涵盖 AGENTS.md、PRODUCT.md、SPEC-implementation.md、GOAL.md、DESIGN.md、DATABASE.md、DEVELOPING.md、adapter-plugin.md、pnpm-workspace.yaml、packages/ 结构、server/src/ 结构及多项相关 PR 和提交记录。*
