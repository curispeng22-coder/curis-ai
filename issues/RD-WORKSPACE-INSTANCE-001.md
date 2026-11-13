# RD-WORKSPACE-INSTANCE-001：RD 真实执行纵向切片

**Status:** PHASE 0/1 ACCEPTED · PHASE 2A DESIGN FIDELITY PASS · LONG-RUNNING EXECUTION RELIABILITY IMPLEMENTED · REVIEW REQUIRED  
**Date:** 2026-08-16  
**Owner:** Curis 主开发 / RD Workspace

## Goal

只打通首个真实 RD 执行链：

```text
既有 Project / Cycle → Task → Responsibility → Employee
→ Execution Binding → Codex → 真实文件修改
→ Artifact → Evidence → Result Reference → 重启读取
```

本 Issue 不完成整个 RD Workspace。成功与失败都必须来自真实 Codex / 文件 /
命令事实；不得把对话、fixture 或手工 `workflow_run:<id>` 当执行结果。

## Authority

1. `docs/00_Context/CURRENT_STATE.md`
2. `docs/01_Product/Curis_Product_Blueprint.html`
3. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` P1–P7
4. `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md`
5. `docs/03_Design/Curis_RD_Workspace_UI_Drift_Audit_v1.md`
6. `docs/04_Development/RD_IMPLEMENTATION_GAP_AUDIT.md`
7. `docs/04_Development/RD_IMPLEMENTATION_PLAN_v1.md`
8. `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`
9. `issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md`

## Current gap

- RD Cycle 只能人工填写 `workflow_run:<id>`，不能自然创建真实 Task / Codex 执行。
- Cycle 当前把所有 Workspace 员工都投影为正在执行，无法区分 Holder 与 Executor。
- 执行返回只有文字摘要，缺少真实 changed files、diff、测试结果、Codex session、
  Artifact / Evidence / Result Reference 链。
- 重启后持久化状态可能被误读为外部 Agent 仍在运行。

## Runtime truth model

```text
Object Owner != Responsibility Holder != Current Executor
Task/Execution != Project/Cycle
Artifact != Evidence != Conversation
requested Computer Access != configured != effective
```

- 初始责任分配不是 Handoff。
- `Current Executor` 只在真实 Task 运行时存在；等待、完成、失败和重启后均为 `none`。
- Runtime 只验证声明范围内真实文件差异与无 shell 的测试命令；没有证据即 `UNVERIFIED`。
- Full Computer Access 在 Codex Adapter 不支持时保持 `UNSUPPORTED`，不降级执行。

## Allowed Files

```text
backend/app/runtime/workspace.py
backend/app/runtime/execution_adapter.py        # 仅登记 rd_task 既有 Task 执行引用
backend/app/api/runtime_foundation_router.py
backend/app/main.py
backend/app/result_store.py                 # 仅复用/读取现有 Task、Execution、Artifact
backend/app/agent_adapter.py                # 仅补真实隔离目录 New Session 所需原生参数
backend/tests/test_agent_adapter.py         # 上述 Codex 参数与 Computer Access truth 回归
backend/tests/test_rd_workspace_real_execution.py
frontend/app/ceo-office/workspace/software/page.js
frontend/components/runtime/WorkspaceRuntimeView.js
frontend/components/rd/**
frontend/components/workspace/WorkspacePaneShell.js
frontend/lib/runtimeApi.js
frontend/lib/api.js                         # 仅复用现有 Project / Task / Artifact 读取
frontend/tests/rdWorkspaceExecution.test.mjs
frontend/tests/runtimeWorkspaceUi.test.mjs  # 仅共享 Shell no-regression
issues/RD-WORKSPACE-INSTANCE-001.md
reviews/RD-WORKSPACE-INSTANCE-001_review.md
```

不得修改未列出的生产文件。若既有调用链必须改动其它文件，先把 Issue 置为 BLOCKED，
不得自行扩边界。

## Explicit exclusions

- Product Blueprint、Frozen Shell/P1–P7、Approved RD Spec、tokens。
- `data/curis.sqlite`、任何活动数据库、Secret、Key、Cookie、私有会话内容。
- XHS、TTK 路由/组件/Runtime/测试与全局 TerraShell 重构。
- Multi Employee 协作、Artifact Review Request、Handoff、CEO Decision P7、完整
  System Activity、Organization Router、Queue/Bottleneck。
- Computer Access P1/P2、Full Access、非 Codex Adapter。
- 新 Workflow Engine、DAG、RDProject/RDTask/WorkflowTask 平行模型。
- 模拟 Agent 回复、前端伪造 Running、fixture 执行结果、手工 Execution Result。

## Phase 0 — Migration safety

1. 记录当前 dirty worktree；不清理或覆盖用户改动。
2. 使用 fresh 临时目录与隔离 SQLite；不写 `data/curis.sqlite`。
3. 复用现有 Project / Cycle / Task / Employee / Capability / ResultStore。
4. 首轮 focused baseline 覆盖 RD Runtime、Codex P0 与 XHS accepted path。

## Phase 1 — RD real execution vertical slice

1. Cycle 保存真实 Project、工作标题、bounded instruction、声明文件范围、测试命令和
   requested Computer Access intent；不再要求 `workflow_run:<id>`。
2. 从现有 Workspace staffing 选择一个真实 Responsibility Holder；从既有 Company
   Employee / Capability Binding 选择合法 Codex execution employee/provider。
3. 创建真实 Task 并通过现有 Orchestrator / Codex Adapter 执行。
4. 在 Codex 前后读取声明文件，生成真实 changed-file/diff Artifact；运行声明测试命令，
   记录真实 exit status/output Evidence。
5. Conversation 只保存白话摘要与 Result Reference；详细 diff/test 进入 Artifact/Evidence。
6. 成功、失败均清空 Current Executor；失败保留 Artifact/Evidence 且不得标记 Completed。
7. 同一隔离 DB stop/restart 后读取同一 Cycle/Task/Binding/session/Artifact/Evidence。

## Runtime simulation

- 在 fresh 临时 Git/文件项目中准备一个安全小函数与测试。
- 成功场景：Codex 真实修改声明文件，真实测试通过，Result Reference 可读取。
- 失败场景：Codex 仍产生真实可观察结果，但真实测试非零；执行保持失败，证据保留。
- 重启场景：requested 历史与证据可读取；持久化不把外部 Agent 投影为仍在运行。

## Acceptance scenarios

1. Cycle / Task 可自然启动真实 Execution，不输入 `workflow_run:<id>`。
2. Task、Responsibility、business Employee、execution Employee、Capability Binding、
   Project / Workspace scope 均可追踪。
3. 真实 Codex session 被调用，真实声明文件发生变化。
4. Artifact 含 changed files / diff / command-test facts / timestamps / provider/session refs。
5. Evidence 与 Artifact 分离；无通过证据不得声称完成。
6. Conversation 只含白话结果摘要与可回访 Result Reference。
7. 重启后同一对象链可读，Current Executor 为 none。
8. 真实失败保留 Artifact/Evidence，Cycle/Execution 不显示 Completed。
9. Computer Access 始终保持 requested/configured/effective 事实分离。
10. XHS accepted Runtime/UI focused checks无新增回归。

## Review

正式证据写入 `reviews/RD-WORKSPACE-INSTANCE-001_review.md`，至少记录隔离 DB 与临时项目、
脱敏对象 ID、Codex session/access snapshot、文件差异、测试事实、restart、失败路径、
focused tests、XHS no-regression 和 Remaining RD Phases。

## Phase 2A — Approved professional Workspace migration

### Goal

把 Phase 0/1 已验收的真实 Project / Cycle / Task / Responsibility / Employee /
Execution Binding / Codex Session / Artifact / Evidence / Result Reference 投影到
`Curis_RD_Workspace_Instance_Spec_v1.md` 批准的研发专业工作面。

### Bounded implementation

- 复用 `WorkspacePaneShell` 的四 Pane、T1/T2/T3、Resizable、Search 与 Utility Maximize；
  仅增加 Instance 可传入的 Context/Utility 名称和 Result Reference 打开信号，XHS 默认行为不变。
- RD Main 使用 Employee Workstation 垂直栈，不复制 XHS Calendar/Note。
- Employee Workstation 只读取真实 Responsibility Holder、Current Executor、Task 和
  execution status；waiting 可有 Holder 且 Executor 为 none。
- Conversation 只显示 Runtime 白话摘要和 Result Reference。
- Context 只显示当前 Project/Cycle/Task、声明文件与相关 Evidence。
- Utility 通过既有 Task API 读取真实 code-change Artifact，显示 changed files、diff、
  test evidence、Codex session 与 Computer Access truth。
- execute 请求期间通过重新读取 Runtime 显示真实 `RUNNING`/Current Executor，不以本地
  按钮状态伪造执行事实。

### Explicit Phase 2A exclusions

Artifact Review Request、员工间 Handoff、CEO Decision P7、完整 Multi-Employee、
Queue/Bottleneck、Organization Router、Computer Access P1/P2、Full Access、DAG、
Workflow Engine、XHS/TTK 业务改动。

### Phase 2A acceptance

1. RD Workspace 读取真实 Project/Cycle/Task。
2. Employee Workstation 区分 Holder / Executor / waiting / working / completed / failed。
3. 真实 Codex 执行时通过 Runtime polling 显示 Current Executor；结束后清空。
4. Result Reference 打开 Utility 中同一 Task 的真实 diff/test/metadata。
5. 失败 Cycle 显示 `PAUSED/FAILED` 与持久化失败 Evidence，不显示 Completed。
6. 同一隔离 SQLite stop/restart 后 UI 投影不漂移。
7. XHS Shared Shell/Runtime focused checks无回归。

## Phase 2A — Design fidelity closure

本 Closure 只调整 RD 专业工作面的默认信息层级与用户语言，不改变已验收的
Project → Cycle → Responsibility → Employee → Execution Binding → Codex → Artifact /
Evidence / Result Reference 链。

- Main 默认以 Employee Workstation、当前工作、负责人、执行者、进展和结果入口为中心；
  Runtime 对象卡与内部 ID 退出默认阅读层。
- Context 默认只显示项目背景、当前工作、相关文件和已有结果；Cycle / Task / Evidence ID
  收入折叠技术引用。
- Utility 分为用户可读结果、专业 Diff/Test Evidence、折叠 Execution metadata/ID；
  Computer Access 枚举保留在技术详情，默认翻译为自然语言。
- 新工作主表只收集“要解决的问题”和“期望结果”；当前 Project 尚不能推导的文件范围、
  验证命令与补充执行说明保留在 Advanced，不伪造自动推导。
- Runtime 中的 `Engineering AI` 暂以诚实中性名称“研发员工 · 研发工程师”展示；本 Closure
  不编造尚未存在于 Workspace Employee Runtime 的实名身份。

### Fidelity closure exclusions

不新增 Multi-Employee、Artifact Review Request、Handoff、P7、Queue/Bottleneck、
Organization Router、Computer Access P1/P2 或 Full Access；不修改 XHS/TTK、Frozen
Contract、Product Blueprint 或底层 Runtime 状态语义。

## Phase 2A — Long-running execution reliability closure

### Goal

关闭 packaged Desktop 中同步等待 Codex 最终结果导致的 Gateway timeout / 503 真相漂移：

```text
Submit → Runtime ACCEPTED / RUNNING → 后台真实执行
→ Runtime 状态观察 → COMPLETED / FAILED + Artifact / Evidence
```

提交只确认既有 Cycle、Responsibility、Execution Binding 已由 Runtime 接管，不等待
Codex、测试或 Artifact 才返回。Gateway/客户端传输状态不得覆盖已持久化的执行事实。

### Bounded implementation

- 仅 `rd_task:auto` 改为接管后异步完成；其它既有 Runtime execution 保持兼容。
- `begin_operating_cycle_execution` 的同一事务继续负责 `READY → RUNNING` 与真实
  Current Executor；同一 Cycle 已有 active execution 时返回当前 Runtime，不再创建第二次执行。
- 后台执行复用既有 `RuntimeExecutionAdapter`、Codex Task、ResultStore、Artifact/Evidence
  与成功/失败落库函数，不新增 Queue、Job、Workflow 或 DAG 模型。
- Frontend 只轮询既有 Workspace Runtime；提交按钮不等待最终结果，也不伪造本地 Running。
- Runtime 重启时，遗留 `rd_task:auto / RUNNING` 若无法证明外部 Agent 仍在执行，沿既有失败
  事实收口并清空 Current Executor；持久化不等于外部进程仍有效。

### Acceptance

1. 超过旧 Gateway 等待窗的真实 Codex 执行，提交快速返回 `202` 与 Runtime `RUNNING`。
2. 执行期间 Runtime/UI 可观察真实 Holder、Current Executor 和 `RUNNING`。
3. 完成后读取同一 Cycle 的 Task、Artifact、Evidence、Result Reference 与 `COMPLETED`。
4. 真实失败保持 `FAILED`，失败 Artifact/Evidence 保留，不显示 Completed。
5. 同一 Cycle 在 `RUNNING` 时重复提交不创建第二个 Task/Codex Session。
6. transport timeout 不把已接管执行写成业务失败；重读以 Runtime 为准。
7. stop/restart 后最终事实可恢复；无法验证的遗留 Running 不投影为 Agent 仍活跃。
8. Computer Access requested/configured/effective 语义不变；XHS accepted path 无回归。

### Reliability closure exclusions

不修改 Phase 2A 视觉结构，不进入 Multi-Employee、Artifact Review、Handoff、P7、
Computer Access P1/P2 或 Full Access；不修改 XHS/TTK、Frozen Contract、Product Blueprint；
不新增通用 Queue、Workflow Engine、DAG 或分布式任务系统。

### Reliability closure result

- `rd_task:auto` 提交在 Runtime 原子写入 `RUNNING` 后返回 HTTP `202`；真实 Codex、测试、
  Artifact 与 Evidence 继续由同一 Runtime 在后台完成。
- 同一 Cycle 已有 active execution 时返回同一 Runtime 对象，不创建第二个 Task 或
  Codex Session。
- Workspace 页面观察既有 Runtime `RUNNING / COMPLETED / FAILED`；提交调用不再承担
  Agent 最终结果的等待窗口。
- Runtime 重启时，无法证明外部 Agent 仍存活的历史 `RUNNING` 按失败事实收口并清空
  Current Executor；已完成和已失败事实保持原状。
- 实施与验收证据见 `reviews/RD-WORKSPACE-INSTANCE-001_review.md`；本 Closure 不进入
  Phase 2B。
