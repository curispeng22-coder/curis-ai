# DESKTOP-RUNTIME-EXECUTION-001

Status: Completed (runtime bridge; external execution evidence open)  
Decision: `PASS_RUNTIME_EXECUTION_BRIDGE_WITH_EXTERNAL_RESULT_BLOCKER`

## 1. 目的

把已启动的 Runtime `SimulationRun` 接到真实 AI 执行基座，形成第一条可恢复的
`执行请求 → ExecutionRef → Evidence → CEO Review` 闭环。旧 Project / Task /
Workflow 只能作为内部执行载体；它们不能直接改变 CEO 所见的 Runtime 状态，也不能
生成自动通过的结果。

## 2. 本 Issue 的产品边界

- 当前 Desktop 仍是单 CEO、本机、三业务同步验证。
- AI 执行必须绑定已有的 `executionRef`（首版支持 `workflow_run:<id>`）；没有绑定、
  越权、执行器未配置或执行失败时，必须明确阻断或失败，不能以“运行中”掩盖。
- 执行成功只产生 `UNVERIFIED` 的 Runtime Evidence 和交接记录；不会自动通过、不会
  自动 CEO 验收、不会产生外部平台发布回执。
- CEO 明确提交 Review 时，才允许将指定的真实 Evidence 标记为 `VERIFIED` 并作出
  `PASS / FAIL / REVIEW_REQUIRED`；XHS / TTK 仍要求真实平台回执才能 PASS。
- 外部发布、资金、权限、不可逆动作继续由现有治理闸和 CEO 决策控制。

## 3. 允许范围

- `backend/app/runtime/execution_adapter.py`（新增）
- `backend/app/api/runtime_foundation_router.py`
- `backend/app/main.py`（仅注入 Runtime 执行桥）
- `backend/tests/test_runtime_execution_adapter.py`
- `backend/tests/test_runtime_foundation_api.py`
- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应 Review、Current State 与 Change Log

不得修改 Runtime 状态机、活动数据库、旧执行表结构、外部平台 API、商业化 Admin 或
新增一级导航。

## 4. 验收条件

1. `RUNNING` Simulation 执行时，租户 / Company / Workspace / Subject / Blueprint
   全部重新校验；无 `executionRef` 或不支持的引用 fail-closed。
2. 真实执行结果被保存为 Runtime Evidence（`fixture=false`、初始
   `verification_status=UNVERIFIED`），Simulation 保留 ExecutionRef、交接和审计。
3. AI 执行失败不会生成成功证据；可见状态是失败或待恢复，并保留原因摘要。
4. CEO Review 只接受当前租户和当前 Simulation 的 Evidence；明确 PASS 前不会进入
   `PASSED`，XHS / TTK 无 `PLATFORM_API + VERIFIED + SUCCESS` 回执时 PASS 必须拒绝。
5. Desktop Workspace 显示“执行 / 待证据 / CEO 验收”状态，刷新和重启后仍可恢复；
   页面不得显示伪造成功或外部发布数据。
6. 通过聚焦 Backend / Frontend 测试、Next build、scoped ESLint；全量基线失败不得
   被扩大或掩盖。
