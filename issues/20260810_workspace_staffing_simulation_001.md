# WORKSPACE-STAFFING-SIMULATION-001

Status: Completed  
Decision: `PASS_WORKSPACE_STAFFING_SIMULATION_WITH_ACTIVATION_GATE`

## 1. 目的

为 Workspace Studio 已物化的候选岗位、候选员工和能力需求建立隔离 `ORG-001`
Simulation。Simulation 只验证当前 Blueprint / orgVersion 的责任覆盖、能力需求覆盖、
汇报关系、失败出口与未授权边界，形成可追溯 Evidence、Handoff 和 CEO Review；不产生
外部副作用，不授权或激活任何运行对象。

## 2. 允许范围

- `backend/app/runtime/simulation.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `frontend/app/ceo-office/page.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应 Review、Current State 与 Change Log

不得修改数据库 Schema、Runtime 状态机 / Registry、活动数据库、旧 Project / Task 链、
真实平台 API、商业化 Admin、Desktop Packaging、Blueprint、一级导航或员工 / 能力激活命令。

## 3. 契约

- `ORG-001` 只接受当前 Tenant / Company / Workspace / Blueprint 的显式 Studio Staffing
  Proposal；subject、participants 与 input refs 由 Runtime 推导，拒绝客户端伪造。
- 开始后执行只读结构验证：Role Slot、AI Employee、Capability Binding 数量与 orgVersion
  一致；岗位责任、能力引用、候选关系、向 CEO Assistant 汇报和人工失败出口完整。
- 隔离验证必须证明所有 AI Employee 仍为 `PROPOSED`、Role Slot 仍为 `DRAFT`、Capability
  Binding 仍为 `PROPOSED_NOT_AUTHORIZED`；Simulation 本身不能越过授权门。
- 通过验证时创建 `fixture=false / VERIFIED` 的结构验证 Evidence、CEO Handoff，并进入
  `WAITING_CEO`；重复执行不产生平行 Evidence 或 Handoff。
- 结构缺失时持久化 `BLOCKED` final state、失败责任与恢复路径；有未解决失败时禁止 PASS。
- CEO 可明确 PASS / FAIL / 请求补证据。`ORG-001 PASS` 只表示候选组织草案通过隔离验证，
  不设置 Workspace `simulation_passed`，不改变岗位、员工或能力状态。

## 4. 验收条件

1. API 能创建、启动、执行、刷新恢复并 Review `ORG-001`；跨 Scope、旧 Blueprint、伪造输入 fail-closed。
2. 正常路径生成一份非 fixture VERIFIED Evidence、一个 Handoff 和 `WAITING_CEO`；CEO PASS 后仅 Simulation 为 `PASSED / PASS`。
3. 缺失关系或 orgVersion 漂移形成可恢复失败，且 Workspace / Proposal 状态保持不变。
4. CEO Desk 从真实 Runtime 显示“开始隔离验证 → 等待 CEO 审查 → 已通过但未激活”，不把 PASS 计为员工或能力授权。
5. Backend / Frontend 聚焦测试、scoped ESLint、Next build、临时 SQLite integrity 与浏览器验证通过。
