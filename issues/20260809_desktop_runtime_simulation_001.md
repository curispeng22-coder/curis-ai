# DESKTOP-RUNTIME-SIMULATION-001

Status: Completed (local browser gate; packaged Desktop revalidation open)  
Decision: `PASS_LOCAL_DESKTOP_SIMULATION_GATE_WITH_PACKAGED_APP_BLOCKER`

## 1. 目的

让三业务 Workspace 能从真实运行对象进入可恢复的 Simulation 状态，而不是永远显示“尚无
SimulationRun”。Simulation 只负责验证蓝图和运行路径，不允许前端伪造 PASS、外部回执或 CEO 验收。

## 2. 允许范围

- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_foundation_api.py`
- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应 Review、Current State 与 Change Log

不得修改 Runtime 状态机、活动数据库、旧 Project / Task 链、真实平台 API、商业化 Admin 或新增一级导航。

## 3. 契约

- CEO 可以为当前 Workspace 的当前 Blueprint 和真实 Cycle / ContentItem 创建对应 SimulationRun。
- Desktop 通过受控 API 将 SimulationRun 从 `DRAFT` 启动为 `RUNNING`，所有转换写入审计。
- 非当前租户、非当前 Company / Workspace、错误业务场景和非 CEO 操作者必须 fail-closed。
- 缺少真实证据时不得进入 `PASSED`；界面必须显示“验证中 / 待证据”，不能显示成功。

## 4. 验收条件

1. Backend API 聚焦测试覆盖创建、启动、跨租户隔离、非法状态与脱敏投影。
2. RD / XHS / TTK 运行现场均显示对应 SimulationRun 状态和“开始验证”入口。
3. 创建 / 启动后刷新仍能恢复同一 SimulationRun；不会重复创建隐形运行记录。
4. 前端测试、Next build、scoped ESLint、fresh Desktop 真实窗口和临时 SQLite integrity 通过。
