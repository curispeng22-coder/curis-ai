# WORKSPACE-STAFFING-PROPOSAL-RUNTIME-001

Status: Completed  
Decision: `PASS_WORKSPACE_STAFFING_PROPOSAL_RUNTIME_WITH_ACTIVATION_GATES`

## 1. 目的

把 Workspace Studio 已持久化的 Role Slot、AI Employee 与 Capability Requirement 从 Blueprint
字段推进为真实、可查询、可审计的 Runtime Proposal。创建 Workspace Blueprint Draft 时，在同一
SQLite 事务内建立候选组织对象和关系；所有对象保持未批准状态，不能被计为已在岗员工、已授权
能力或可运行 Workspace。

## 2. 允许范围

- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `backend/tests/test_runtime_foundation_api.py`
- `frontend/app/ceo-office/workspace/studio/page.js`
- `frontend/app/ceo-office/page.js`
- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应 Review、Current State 与 Change Log

不得修改数据库 Schema、Runtime 状态机 / Registry、活动数据库、旧 Project / Task 链、
真实平台 API、商业化 Admin、Desktop Packaging、Blueprint 或一级导航。

## 3. 契约

- 只对 `lifecycleMode=STUDIO_DRAFT` 且显式声明 Role Slot / Capability Requirement 的 Blueprint
  物化 Proposal；旧 Blueprint 保持兼容，不自动补假组织。
- 同一事务建立 `ROLE_SLOT=DRAFT`、`AI_EMPLOYEE=PROPOSED`、
  `CAPABILITY_BINDING=PROPOSED` 与 Runtime Links；任何一步失败时 Workspace 和 Proposal 一起回滚。
- AIEmployee、RoleSlot 与 CapabilityBinding 使用同一 `orgVersion`、当前 Workspace / Company /
  Blueprint scope；跨租户、缺失 CEO Assistant、错误 capability ref 或不完整岗位契约 fail-closed。
- `AI_EMPLOYEE=PROPOSED` 只显示为候选方案，不计入 AI 员工数量；CapabilityBinding 不显示为已授权。
- API 只投影安全的岗位 / 能力摘要，禁止返回 prompt、credential、secret 或原始 payload。
- 本 Issue 不授权 Capability、员工或 Workspace 激活；Simulation 与 CEO Approve 仍为后续门禁。

## 4. 验收条件

1. Studio 三业务 Blueprint 使用稳定 requirement ref，并能创建完整候选岗位与能力供给关系。
2. Workspace 创建响应和 Company Runtime Snapshot 可恢复 Proposal；重启后数量、关系和 orgVersion 一致。
3. CEO Desk 将候选方案与已在岗员工分开，AI 员工统计不包含 `PROPOSED`。
4. Backend 测试覆盖事务回滚、Tenant / Company scope、安全投影与旧 Blueprint 兼容。
5. Frontend 聚焦测试、scoped ESLint、Next build、临时 SQLite integrity 与浏览器验证通过。
