# WORKSPACE-OPERATING-CYCLE-CLOSURE-001

Status: Completed  
Decision: `PASS_WORKSPACE_OPERATING_CYCLE_CLOSURE_WITH_EXTERNAL_EXECUTION_AND_ACTIVITY_DB_BASELINES`  
Date: 2026-08-10

## Outcome

让已批准且处于 `OPERATING` 的研发 Workspace 使用当前 Operating Version 和已激活 AI 团队，
完成第一条真实 `Cycle → Responsibility Handoff → ExecutionRef → Evidence → CEO Acceptance →
Review Decision → Closed` 运行链。旧 Workflow 只继续作为显式 `workflow_run:<id>` 内部执行基座；
不得改变 Runtime 业务状态或自动形成验收。

## Authority

- `docs/00_Context/CURRENT_STATE.md`
- `docs/01_Product/Curis_Product_Context.md`（Frozen）
- `docs/01_Product/Curis_Product_Blueprint.html`（Single Current Blueprint, Review）
- `docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md` §1.7 / §1.11 / §5.7
- `docs/reviews/20260810_desktop_runtime_execution_001_review.md`
- `docs/reviews/20260810_workspace_staffing_approval_activation_001_review.md`

## Allowed Files

- `backend/app/runtime/workspace.py`
- `backend/app/runtime/execution_adapter.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_operating_cycle.py`
- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/20260810_workspace_operating_cycle_closure_001.md`
- `docs/reviews/20260810_workspace_operating_cycle_closure_001_review.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

## Required Runtime Contract

1. 只接受当前 Tenant / Company 的 CEO 命令和 RD `CYCLE`；Workspace 必须为 `OPERATING`，
   当前 Blueprint Version 必须是 approved current Operating Version，组织版本、Role、Employee、
   Binding 和责任关系必须完整且处于可接手状态。
2. 启动在同一事务形成可反查的责任 Handoff，并按既有状态机进入：Cycle
   `PLANNED → READY → RUNNING`、Role Slot `ASSIGNED → OPERATING`、AI Employee
   `AVAILABLE → OPERATING / RUNNING`。客户端不能选择或伪造员工、岗位、组织版本或授权。
3. 执行只复用现有显式 `workflow_run:<id>` 适配器。成功结果必须保存为
   `fixture=false / UNVERIFIED` Evidence、待 CEO 的输出 Handoff 和 `PENDING` Acceptance，
   Cycle 进入 `WAITING_CEO`；失败不得产生成功 Evidence，并原子进入 `PAUSED`，保留失败与恢复入口。
4. CEO `ACCEPT` 必须选择当前 Cycle 的真实 Evidence，形成 Acceptance 并验证 Evidence；
   `REJECT` 保留原 Evidence、拒绝 Handoff 和原因，Cycle 进入 `REJECTED`。任一决定均释放本周期
   Employee 到 `AVAILABLE`，但不撤销持续运行的 Role Slot 或 Capability Binding。
5. 已接受 Cycle 只有在 CEO 明确提交 `CONTINUE / ADJUST / PAUSE` 复盘决定后，才形成并应用
   DecisionPacket、关闭 Acceptance，并进入 `ACCEPTED → REVIEWING → CLOSED`；决定只写入当前
   Cycle 的下一动作，不静默修改 Workspace Blueprint、组织或外部系统。
6. 命令必须幂等、并发 fail-closed、重启可恢复；所有对象可由
   `companyId / workspaceId / cycleId / executionRef` 反查，API 不投影凭据、原始执行 payload 或
   hidden metadata。
7. 研发办公室把 Operating Cycle 与 Simulation 分开呈现，提供“启动运行、AI 员工执行、
   CEO 接受 / 拒绝、复盘关闭”真实动作；共享 Assistant 保持根布局浮层。

## Explicitly Out Of Scope

- Schema / Migration、Runtime Registry / 状态枚举修改
- 新执行器、旧 Workflow 表或状态写路径修改
- 小红书 / 抖音外部发布、平台授权、回执、互动与 Outcome
- Blueprint Revision、组织变更、Capability Catalog 写路径、活动 `data/curis.sqlite`
- Desktop 打包、签名、公证、Platform / Admin、一级导航
- stage、commit、push

## Acceptance Evidence

- Backend：正常启动 / 执行 / 接受 / 关闭、拒绝、执行失败暂停、幂等、强制中途失败整体回滚、
  重启恢复、跨 Tenant / 非 Operating / 版本或组织漂移 fail-closed、安全投影。
- Frontend：Operating 与 Simulation 分离、动作门禁、接受 / 拒绝 / 三种复盘决定、失败恢复文案、
  共享 Assistant 无第三栏断言。
- Browser：临时 SQLite 的已批准 RD Workspace 完成接受关闭链与拒绝链；刷新和 Backend 重启后
  恢复同一 Handoff / Evidence / Acceptance / Decision / Cycle 状态。
- SQLite `integrity_check=ok`；活动库不作为写目标；Review、CURRENT_STATE、CHANGE_LOG 同步。

## Delivery Evidence

- Backend Operating Cycle 与既有执行适配器、Runtime Entity / Link / Transition Log 复用完成；未新增
  Schema、Registry、状态枚举或执行器。
- Backend 聚焦联合回归 `19 passed`；Frontend Runtime tests `18 passed`；Python compile、scoped
  ESLint、Next production build `44/44` 均通过。
- Codex In-app Browser 在临时 SQLite 完成一条 `CLOSED / CONTINUE` 接受链和一条
  `REJECTED` 保留证据链；Backend 重启后恢复同一 Cycle、Handoff、Evidence、Acceptance 与
  DecisionPacket。
- 临时 SQLite `integrity_check=ok`、`foreign_key_check` 无结果；接受链 Evidence=`VERIFIED`、
  Acceptance=`CLOSED`、DecisionPacket=`APPLIED`，拒绝链 Evidence=`UNVERIFIED`、
  Acceptance / Cycle=`REJECTED`。
- 浏览器使用的受控执行器只验证 Runtime 闭环，不冒充生产旧 Workflow 的真实子执行；生产
  `workflow_run` 结果与新鲜打包 Desktop 仍保留为外部基线。
- 活动 `data/curis.sqlite` 未作为服务、测试或浏览器写目标；未 stage、commit 或 push。
