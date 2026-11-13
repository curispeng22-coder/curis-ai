# WORKSPACE-STAFFING-APPROVAL-ACTIVATION-001

Status: Completed  
Decision: `PASS_WORKSPACE_STAFFING_APPROVAL_ACTIVATION_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`  
Date: 2026-08-10

## Outcome

在当前 Workspace Blueprint、同一 `orgVersion`、未失效 `ORG-001 PASS` 与当前
Capability Supply Resource Check 全部有效时，让真实 CEO 明确批准候选组织，并在一个
SQLite 事务内生成唯一 Operating Version、分配 Role Slot、启用 AI Employee、授权并激活
Capability Binding。任何校验或写入失败必须整体回滚；批准后的 14 天内允许 CEO 显式安全回滚。

CEO 也必须能选择 `MODIFY` 或 `REJECT`：两者保留草案与历史决定、失效当前 Simulation、
返回 Studio 装修态，不创建任何生产责任。

## Authority

- `docs/00_Context/CURRENT_STATE.md`
- `docs/01_Product/Curis_Product_Context.md`（Frozen）
- `docs/01_Product/Curis_Product_Blueprint.html`（Single Current Blueprint, Review）
- `docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md` §1.11 / §5.4
- `docs/reviews/20260810_workspace_staffing_simulation_001_review.md`
- `docs/reviews/20260810_workspace_capability_supply_review_001_review.md`

## Allowed Files

- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `frontend/lib/runtimeApi.js`
- `frontend/app/ceo-office/page.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/20260810_workspace_staffing_approval_activation_001.md`
- `docs/reviews/20260810_workspace_staffing_approval_activation_001_review.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

## Required Runtime Contract

1. CEO `APPROVE` 前在同一事务内重新核对 Tenant / Company / Workspace、当前 Blueprint、
   `orgVersion`、完整 Role / Employee / Binding 关系、未失效 `ORG-001 PASS` 与实时无阻塞
   Resource Check；客户端不能提交状态、版本、参与对象或授权结果。
2. 批准按现有状态机留痕并原子进入：Role Slot=`ASSIGNED`、AI Employee=`AVAILABLE`
   且 `presenceState=AVAILABLE`、Capability Binding=`ACTIVE / AUTHORIZED_ACTIVE`、
   Workspace=`OPERATING`，当前 Blueprint Version 成为唯一 Operating Version。
3. `MODIFY` / `REJECT` 保留草案与决定，失效当前 Simulation，返回 `BLUEPRINTING`；不得删除、
   激活或部分改变候选对象。
4. 14 天内显式 rollback 原子进入：Workspace=`PAUSED` 且无当前 Operating Version、Role Slot
   回到 `READY`、AI Employee=`SUSPENDED / BLOCKED`、Capability Binding=`REVOKED`；原批准、
   运行版本、状态转换和回滚原因必须保留历史。
5. 所有命令幂等、Tenant-scoped、CEO-only、并发 fail-closed；响应不得包含凭证、private
   metadata、token、secret 或隐藏 Runtime 配置。
6. CEO Desk 只在真实 Runtime 门禁成立时开放“批准并激活”；同时提供“要求修改”“拒绝并保留
   草案”；激活后显示 Operating Version 与回滚期限。Assistant 继续使用共享浮层，不新增第三栏。

## Explicitly Out Of Scope

- 数据库 Schema / Migration、Runtime Registry / 状态枚举修改
- Capability Catalog 写路径、凭据注入、真实模型或外部平台调用
- 旧 Project / Task / Workflow 链、活动 `data/curis.sqlite`
- Blueprint、一级导航、Desktop Packaging、Platform / Admin
- 蓝图 Revision 编辑器、真实 Cycle 执行、外部 Outcome、Acceptance 或发布
- stage、commit、push

## Acceptance Evidence

- Backend：批准、修改、拒绝、幂等、重启恢复、目录 / 版本 / Simulation 漂移、跨 Tenant、
  并发或中途失败整体回滚、14 天内回滚与超窗拒绝。
- Frontend：API 契约、按钮门禁、安全文案、激活 / 回滚恢复和无第三栏断言。
- Browser：临时 SQLite 完成 `Proposal → Resource Check → APPROVE → OPERATING → rollback`
  与 `MODIFY / REJECT` 非激活路径，刷新和 Backend 重启后保持同一事实。
- SQLite `integrity_check=ok`；活动数据库 SHA 不变；Review、CURRENT_STATE、CHANGE_LOG 同步。
