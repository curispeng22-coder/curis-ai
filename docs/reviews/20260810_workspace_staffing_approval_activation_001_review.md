# WORKSPACE-STAFFING-APPROVAL-ACTIVATION-001 Review

Status: Review  
Decision: `PASS_WORKSPACE_STAFFING_APPROVAL_ACTIVATION_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`  
Date: 2026-08-10

## 结论

PASS。当前 Workspace Blueprint、同一 `orgVersion`、未失效 `ORG-001 PASSED / PASS`
和实时无阻塞 Resource Check 全部成立后，CEO 可以明确选择 `APPROVE / MODIFY / REJECT`。
`APPROVE` 在一个 SQLite 事务内生成唯一 Operating Version，并按既有状态机完成 Role Slot
分配、AI Employee 启用、Capability Binding 授权激活和 Workspace `OPERATING`；14 天内可由
CEO 显式原子回滚。`MODIFY / REJECT` 只保留草案与决定、失效当前 Simulation，不产生生产责任。

本 Review 只放行候选组织的 CEO 决定、激活与回滚。它不代表真实 Cycle / ContentItem 执行、
Evidence、Handoff、Acceptance、外部 Outcome、Blueprint Revision 编辑器、新鲜打包 Desktop 或
外部分发已经完成。

## 实际改动文件

- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `frontend/lib/runtimeApi.js`
- `frontend/app/ceo-office/page.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- Issue、本文、`CURRENT_STATE.md`、`CHANGE_LOG.md`

未修改 Schema / Migration、Runtime Registry / 状态枚举、Capability Catalog 写路径、旧
Project / Task / Workflow 链、活动数据库、Blueprint、导航、Desktop、平台 API 或凭据。

## Runtime 与安全证据

- `APPROVE` 在同一 `BEGIN IMMEDIATE` 事务内重新核对 Tenant / Company / Workspace、当前
  Blueprint、`orgVersion`、完整 Role / Employee / Binding 关系、未失效 `ORG-001 PASS` 与实时
  Resource Check；客户端不能提交运行版本、对象集合或授权结果。
- 成功批准依次留痕并进入：Role Slot `ASSIGNED`、AI Employee `AVAILABLE / AVAILABLE`、
  Capability Binding `ACTIVE / AUTHORIZED_ACTIVE`、Workspace `OPERATING`，且只有当前 Blueprint
  Version 标记为 Operating Version。
- 同一决定与同一回滚幂等；冲突决定、跨 Tenant、版本 / Catalog / Simulation 漂移、中途写入
  失败和超出 14 天回滚窗均 fail-closed。强制触发器失败测试证明无部分状态残留。
- `MODIFY / REJECT` 均保留 `DRAFT / PROPOSED` 候选对象与决定，Workspace 返回
  `BLUEPRINTING`，当前 Simulation 失效。
- 回滚保留原批准、运行版本与审计历史，同时原子进入 Workspace `PAUSED`、Role Slot `READY`、
  AI Employee `SUSPENDED / BLOCKED`、Capability Binding `REVOKED`。
- API 使用可信 CEO 身份和当前 Company 范围；安全投影不包含 credential、token、secret、
  private metadata 或隐藏 Runtime 配置。

## 自动验证

```text
Backend Workspace Runtime focused tests: 12 passed
Backend Workspace + three-business Runtime joint tests: 16 passed
Python compile: PASS
Frontend Runtime focused tests: 17 passed
Scoped ESLint: PASS
Next production build: PASS, 44/44 static pages
```

Backend 覆盖批准、修改、拒绝、幂等、重启恢复、跨 Tenant、强制中途失败整体回滚、安全投影、
显式回滚与超窗拒绝。Frontend 覆盖 API 契约、门禁、三种决定文案、Operating Version、回滚状态
和共享 Assistant 无第三栏边界。

## 浏览器与临时 SQLite 验收

Codex In-app Browser，`http://127.0.0.1:3000/ceo-office`：

- 临时数据库：`/tmp/curis-staffing-approval.3clwFf/browser.sqlite`
- 三个独立 Workspace 分别执行 `APPROVE / MODIFY / REJECT`；初始均为 2 位候选、
  `ORG-001 PASS`、Resource Check 通过且等待 CEO。
- `APPROVE` 后 CEO Desk 显示 2 位专业 AI 员工、`Operating Version 1`、已授权 2；Backend 重启
  后恢复同一决定与运行状态。
- `MODIFY / REJECT` 后两组候选继续保持草案，决定与 Simulation 失效原因在重启后恢复。
- 14 天窗口内显式回滚后，CEO Desk 显示“已安全回滚”、Workspace 已暂停、已授权 0；第二次
  Backend 重启后仍恢复同一回滚、修改和拒绝事实。
- SQLite `integrity_check=ok`、`foreign_key_check` 无结果。最终：批准 Workspace 为
  `PAUSED / ROLLED_BACK`，2 Role Slot=`READY`、2 AI Employee=`SUSPENDED / BLOCKED`、
  2 Binding=`REVOKED`；修改 / 拒绝 Workspace 均为 `BLUEPRINTING`，候选对象未激活。
- 视觉证据：
  - `/tmp/curis-workspace-staffing-approval-evidence/01-ready-for-ceo-approval.jpg`
  - `/tmp/curis-workspace-staffing-approval-evidence/02-approved-operating-version.jpg`
  - `/tmp/curis-workspace-staffing-approval-evidence/04-rollback-complete.jpg`

活动 `data/curis.sqlite` 未作为本 Issue 的服务、测试或浏览器写目标；所有显式写入均指向 pytest
临时目录或上述 `/tmp` 数据库。本轮只读快照从
`9de2fb7e981c2aa2a39435f84c278692e513c38833cbfe0002b4074aced403d6` 持续外部漂移；服务恢复时
快照为 `ae15dfadfb1e73c99bfd3f4df4ce65ca2a7567a5d398d97baee9ea1fe3734951`。该现象归入已由
产品负责人裁定的外部活动库基线；本 Issue 未恢复、覆盖、合并、清理或追查旧链数据。

## 仍未完成

1. 在已激活组织中运行真实 Cycle / ContentItem，形成可验证 Execution、Evidence、Handoff、
   Acceptance、Decision 与外部 Outcome。
2. 为执行失败、证据不足、Acceptance 拒绝和组织回滚补齐完整 Business Runtime Simulation。
3. 独立 Issue 完成 Blueprint Revision 编辑、重新 Simulation / Resource Check / CEO Approval，
   以及新鲜打包 Desktop 的端到端复核。
