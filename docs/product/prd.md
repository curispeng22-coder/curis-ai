# Curis Workspace PRD

## 1. 产品定位

Curis Workspace 的最终产品目标是面向个人创业者的 AI 公司系统。

用户在产品中扮演 CEO。系统帮助用户把业务目标拆成任务、工作流、工具调用、模型调用、执行结果、学习记录和持久化数据。长期形态会支持公司、部门、AI 员工、知识、工具、模型、成本和业务包。

当前上线范围不是完整 AI 公司系统，而是 AI Task Executor MVP。现阶段开发必须搭好未来 AI 公司系统的框架，但只实现已经过 gate 批准的执行器能力。

全局分层架构：

```text
L6 经济层: ROI / 成本 / 优化
L5 公司层: 组织 / 部门 / 职责
L4 工作流层: 任务拆解 / 编排 / 状态流转
L3 工具层: 工具注册 / 路由 / 执行 / fallback
L2 员工层: AI执行角色 / 员工能力 / 角色偏好
L1 执行层: Task / Run / Status / History / Result
L0 产品层: 用户界面 / 操作台 / 可视化
```

当前 AI Task Executor MVP 只覆盖已批准的 L0-L4 能力，以及执行所必需的最小 L2 coordinator。L5 公司层和 L6 经济层保留为未来阶段。

## 2. 当前实现门槛

当前版本：Curis Workspace Tool System v1.8。

当前唯一允许闭环：

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

本阶段不实现完整 AI 公司系统，只验证：

- 用户提交任务。
- 系统生成工作流。
- AI Employee 协调工具选择与执行。
- Tool Router 选择工具并支持 fallback。
- Tool Executor 执行单工具、链式工具和异步工具。
- Orchestrator 记录状态、工作流、trace、失败和学习结果。
- Meta Development System 分析开发缺口、生成内部实现计划、生成验证计划，并输出事实源校准建议。
- Evolution Governor 按稳定性优先原则评估是否允许系统演进。
- Architecture Locking 保护核心模块，避免未授权改动。
- Controlled Self-Rewrite Engine 只生成受控 proposal，不绕过审批直接改代码。
- Simulation / Risk Analysis / Rollback Record 保障每次演进可评估、可拒绝、可回退。
- Result Store 使用 SQLite 持久化任务、工具、执行、trace、workflow、learning 数据。
- 前端只提供最小任务输入、执行动作、结果展示和任务历史。

### AI 员工工作流低 Token 原则

产品内 AI Employee 工作流也必须遵守低 Token、职责自持、事件式流转原则。

- Orchestrator 只向 AI Employee 传递当前步骤必要上下文，不重复完整任务背景、全局规则或历史长文。
- AI Employee 默认知道自己的执行位置：接收 step、选择或调用工具、返回结构化结果、交给下一执行节点。
- Auto Workflow Generator 生成的 step 应包含 `action`、`purpose`、`required tool`、`expected output` 和必要约束，不生成长篇角色说明。
- 每个 step 完成后记录结果、状态、trace、next step 和 blocker；最终由 Orchestrator 汇总给用户。
- 只有当任务越权、触发安全边界、需要用户决策或需要系统演进评估时，才追加额外上下文。
- 禁止把 AI Employee workflow 演变成 multi-agent system、Employee CRUD 或复杂员工管理。

## 3. 禁止范围

当前阶段禁止：

- ROI 系统。
- Employee CRUD 或员工扩展。
- Multi-agent system。
- 业务模块。
- 复杂 UI。
- Mock data 或 simulation mode。
- 任何绕过最小闭环的业务自动化。
- 未受控架构变更。
- 绕过评估层的自动自改代码。

## 4. 长期愿景拆分

### Sprint 0: AI 公司执行内核

目标：验证任务执行闭环和学习闭环。

需求：

- Task API。
- Run API。
- Status API。
- History API。
- Execution trace API。
- Workflow API。
- Tool Registry。
- Tool Router。
- Tool Executor。
- Tool chaining。
- Async tool execution。
- Tool fallback。
- Auto Workflow Generator。
- Execution Learning Core。
- Autonomous Development Loop。
- Stateful workflow execution。
- Codex Executor。
- Prompt Builder。
- Result Store。
- SQLite persistence。
- Minimal frontend。

验收：

- 一个任务可以从创建到执行完成。
- 状态流完整记录。
- 工作流、工具 trace、执行结果和学习数据可查询。
- 无 forbidden scope。

### Sprint 1A: Tool System v1.6 - Meta Development System

目标：让系统不只执行任务，还能管理自己的开发过程，为后续公司运行可视化和长期 AI 公司方向提供可控的开发闭环。

需求：

- Meta Development Analyzer：分析目标能力、当前实现、缺口和约束冲突。
- Internal Issue Planner：把缺口转成内部开发 issue 草案。
- Verification Planner：为每个开发 issue 生成测试、lint、build、API evidence 和 scope drift 检查计划。
- Source-of-Truth Advisor：识别需要同步的 `knowledge/`、`issues/`、`reviews/`、`PROJECT_STATUS.md`、`TASKS.md`。
- Meta Development Records：持久化 meta 分析、issue 草案、验证计划和事实源建议。

验收：

- 一个任务执行完成后，可以生成 meta development report。
- 报告包含 gap analysis、planned issues、verification plan、source-of-truth suggestions。
- 数据进入 SQLite 持久化。
- API 可以查询 meta development report。
- 不新增 ROI、Employee CRUD、多 Agent、业务模块、复杂 UI、mock data 或 simulation mode。

### Sprint 1B: Tool System v1.8 - Controlled Self-Evolution Kernel

目标：把系统从自我复盘升级为受控自进化 AI 操作系统内核。系统可以提出演进，但必须优先稳定性，并能决定不演进。

系统定义：

- AI Operating System Kernel with Controlled Self-Evolution。
- 不是 agent system。
- 不是单纯 tool system。
- 不是单纯 workflow system。

需求：

- Evolution Control Governor：基于 failure rate、latency、workflow inefficiency 等阈值判断是否触发演进评估。
- Stability-first Policy：强制 `STABILITY > OPTIMIZATION > EVOLUTION`。
- Architecture Locking：锁定 core orchestrator、execution engine、tool router base layer。
- Controlled Self-Rewrite Proposal：生成代码级和架构级 proposal，但不直接应用。
- Simulation Environment：模拟 task execution flow、tool routing behavior、workflow graph、performance impact。
- Risk Analysis：分析稳定性、安全性、回归风险和锁定模块影响。
- Meta Decision Layer：输出 evolve、do_not_evolve、postpone_evolution、rollback_previous_evolution。
- Rollback System：记录 previous architecture、stable version、performance comparison 和 rollback plan。

验收：

- 系统可以可靠执行任务。
- 系统可以在阈值触发时生成 evolution decision。
- 系统可以明确决定 do_not_evolve。
- 锁定模块不会被自动修改。
- 每次 proposal 都包含 simulation、risk analysis、approval decision 和 rollback record。
- 不新增 UI、ROI、业务模块、多 Agent、agent abstraction layer、mock data 或 uncontrolled architecture changes。

### Sprint 1: 公司运行可视化

Status: PRD slice drafted; pending 总控决策席 gate approval.

目标：在 v1.8 闭环稳定后，把执行内核变成可观察的公司运行面板。

P0 需求：

- Task execution dashboard。
- Workflow step visualization。
- Tool selection and fallback visualization。
- Result, trace, failure, and learning display。
- Meta-development report visibility。
- Evolution decision visibility。
- Compact AI Employee runtime step visibility。

P1 需求：

- Minimal company operating status labels derived from existing execution state。

进入条件：

- v1.8 测试通过。
- 当前 source of truth 明确批准。
- 总控决策席打开对应 Sprint gate。

事实源：

- `docs/sprints/sprint-1-company-visualization.md`
- `issues/004_sprint_1_company_visualization_gate.md`

非目标：

- Company CRUD。
- Employee CRUD。
- 复杂部门/员工管理。
- 业务模块。
- ROI。
- Multi-agent system。
- Agent abstraction layer。
- Complex UI。

### Sprint 2: 统一任务操作台

目标：把任务入口、历史、运行控制和执行复盘合成一个日常工作台。

状态：第一实现片已由 系统交付席 实现，质量运行席 验证，并由 产品规划席 接受。

事实源：

- `docs/sprints/sprint-2-unified-task-console.md`
- `issues/008_sprint_2_unified_task_console_gate.md`
- `issues/009_sprint_2_unified_task_console_first_slice.md`

P0 需求：

- Unified task composer。
- Compact task history and minimal status grouping。
- Run and inspect flow using existing APIs。
- Review and decision signals derived from existing execution state。
- Accepted Sprint 1 selected task detail inside the console。

P1 需求：

- Basic local presentation preferences。

进入条件：

- Sprint 1 可观察性可用。
- 用户能看懂一个任务的完整执行链路。

非目标：

- ROI。
- Business modules。
- Employee CRUD。
- Multi-agent system。
- Agent abstraction layer。
- Complex UI。
- 新执行行为。
- Automatic evolution behavior。

### Sprint 2 Follow-up: Project Memory Foundation

目标：建立项目事实记忆层，让 AI Task Executor MVP 可以记住项目目标、架构边界、Sprint 历史、Issue 结果和 Review 证据，减少后续角色读取上下文的 Token 消耗。

状态：PRD slice 已由 产品规划席 起草，等待 总控决策席 gate approval。

事实源：

- `docs/sprints/sprint-2-project-memory-foundation.md`
- `issues/010_sprint_2_project_memory_foundation_gate.md`

P0 需求：

- 定义 Project Memory 与 Execution Memory 的边界。
- 定义 Project Memory 的事实来源：`knowledge/`、`PROJECT_STATUS.md`、`TASKS.md`、ADR、issues、reviews、已有 execution summary memory。
- 定义最小 read model，服务低 Token 上下文读取。
- 定义 issue/sprint 完成后的刷新规则。

非目标：

- Agent memory。
- Employee memory。
- Multi-agent coordination。
- Vector database / embeddings。
- External memory service。
- ROI。
- Business modules。
- Company organization。
- 新执行行为。

### Sprint 3: 轻量角色与职责系统

目标：引入轻量 CEO / Employee / responsibility labels，让任务、工具和结果有角色归属，但不做复杂员工 CRUD 或 multi-agent。

候选需求：

- Executor role labels。
- Responsibility labels。
- Owner type and assigned employee label。
- Role-aware task display。
- Role-aware acceptance language。

进入条件：

- Sprint 2 操作台稳定。
- 角色字段不会破坏执行内核。

### Sprint 4: 多入口与高级 UI

目标：在核心链路稳定后增加多个入口和更高级的 UI 体验。

候选需求：

- Sidebar / command palette。
- Quick task entry。
- Responsive layouts。
- Advanced trace inspection。
- More polished visual hierarchy。

进入条件：

- Sprint 3 角色展示稳定。
- 高级 UI 不改变执行内核边界。

## 5. 当前用户故事

作为用户，我希望输入一个任务，让 Curis Workspace 自动生成工作流、选择工具、执行任务、记录结果和学习执行表现，这样我可以验证系统是否具备未来承载一人公司工作流的基础。

## 6. 角色与职责

当前采用五个合并工作席位。旧的单独角色不再作为日常派发对象。

- 总控决策席：控制 gate、范围冲突、Sprint 推进和长期愿景边界。
- 产品规划席：维护 PRD、需求优先级、验收标准、PMO 状态和唯一事实源。
- 系统交付席：维护系统边界、接口、技术方案、后端/前端实现、Review 和 Commit。
- 质量运行席：维护验收证据、测试策略、环境可靠性和回归风险。
- 安全边界席：维护数据、密钥、外部服务、隐私和安全边界。

## 7. 当前验收标准

- 根目录 `AGENTS.md`、`README.md`、`docs/product/prd.md`、`docs/pmo/current-status.md` 的当前门槛一致。
- 禁止范围在所有 active source of truth 中一致。
- 后端和前端只服务 v1.8 controlled self-evolution gate。
- 文档不再把 ROI、Employee CRUD、Company Dashboard 或业务模块写成当前允许实现。
- 测试命令和无法验证的原因必须记录。
