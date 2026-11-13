# WORKSPACE-OPERATING-CYCLE-CLOSURE-001 Review

Status: Review  
Decision: `PASS_WORKSPACE_OPERATING_CYCLE_CLOSURE_WITH_EXTERNAL_EXECUTION_AND_ACTIVITY_DB_BASELINES`  
Date: 2026-08-10

## 结论

PASS。已批准且处于 `OPERATING` 的研发 Workspace 现在可使用当前 Operating Version 和已激活
AI 团队，完成 `Cycle → Responsibility Handoff → explicit workflow_run executionRef → Evidence →
output Handoff → CEO Acceptance → Review Decision → CLOSED`。Operating Cycle 与 Blueprint
Simulation 分离；客户端不能选择员工、岗位、授权、组织版本或验证结果。

本 Review 只放行源码 Runtime 的研发 Operating Cycle 闭环。浏览器使用受控注入执行器验证状态、
证据、交接、验收和复盘持久化，不代表生产旧 Workflow 已完成一次真实子执行；小红书 / 抖音外部
结果、新鲜打包 Desktop、Blueprint Revision、外部分发和活动数据库均未进入本 Issue。

## 实际改动文件

- `backend/app/runtime/workspace.py`
- `backend/app/runtime/execution_adapter.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_operating_cycle.py`
- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- Issue、本文、`CURRENT_STATE.md`、`CHANGE_LOG.md`

未修改 Schema / Migration、Runtime Registry / 状态枚举、旧 Workflow 写路径、Capability Catalog、
Blueprint、Desktop、导航、平台 API、凭据或活动数据库。

## Runtime 与安全证据

- 启动命令在单一 `BEGIN IMMEDIATE` 事务内复核 Tenant / Company / Workspace、当前 approved
  Operating Version、orgVersion、Role Slot、AI Employee、Capability Binding 与责任关系；形成
  可反查输入 Handoff，进入 Cycle `PLANNED → READY → RUNNING`、Role `OPERATING`、Employee
  `OPERATING / RUNNING`。
- 执行只调用既有显式 `workflow_run:<id>` Adapter。成功原子保存 `fixture=false / UNVERIFIED`
  Evidence、输出 Handoff 与 `PENDING` Acceptance，Cycle 进入 `WAITING_CEO`；失败不产生成功
  Evidence，Cycle 进入 `PAUSED`，员工进入 `DEGRADED / BLOCKED`，CEO 可在修复后恢复并重试。
- `ACCEPT` 只接受当前 Cycle 的完整 Evidence，验证 Evidence、完成 Handoff 并进入 `ACCEPTED`；
  `REJECT` 保留 `UNVERIFIED` Evidence、拒绝 Handoff / Acceptance / Cycle。两条路径均释放员工到
  `AVAILABLE`，持续 Role 与 Binding 不被撤销。
- 只有已接受 Cycle 可由 CEO 显式提交 `CONTINUE / ADJUST / PAUSE`，形成并应用 DecisionPacket，
  关闭 Acceptance，进入 `ACCEPTED → REVIEWING → CLOSED`。决定只写入当前 Cycle 下一动作。
- 重复命令幂等；跨 Tenant、非 Operating、版本 / 组织漂移和强制中途失败均 fail-closed。安全投影
  不包含凭据、原始执行 payload、prompt、token、secret 或 hidden metadata。
- Operating Workspace 不再创建非 `ORG-001` Blueprint Simulation，避免 Simulation 反向覆盖
  Operating Version 的真实运行状态。

## 自动验证

```text
Backend Operating Cycle focused tests: 4 passed
Backend Operating Cycle + Workspace Foundation + Execution Adapter: 19 passed
Python compile: PASS
Frontend Runtime focused tests: 18 passed
Scoped ESLint: PASS
Next production build: PASS, 44/44 static pages
```

Backend 覆盖接受关闭、拒绝保留证据、执行失败暂停 / 恢复 / 重试、幂等、重启恢复、跨 Tenant、
强制中途失败整体回滚和安全投影。Frontend 覆盖显式命令、Operating / Simulation 分离、状态门禁、
接受 / 拒绝 / 三种复盘决定、失败恢复与共享 Assistant 无第三栏边界。

附加运行清单外的五文件 Frontend Runtime 联合套件时为 `26 passed, 1 failed`：未跟踪的
`frontend/tests/runtimeProvider.test.mjs` 仍要求已修改的 `frontend/app/ceo-office/page.js` 包含
“能力引用”。两者均是本 Issue 输入时已有的清单外脏树文件，本 Issue 未修改或扩大修复；该断言
漂移不影响上述 18 个 Operating Cycle 授权范围测试与 44/44 build，但需由其所属 Issue 收口。

## 浏览器与临时 SQLite 验收

Codex In-app Browser，`http://127.0.0.1:3000/ceo-office/workspace/software`：

- 临时数据库：`/tmp/curis-operating-cycle.9Kx7xc/browser.sqlite`
- 当前 RD Workspace=`OPERATING`、Operating Version=`1`、2 个 Role Slot=`OPERATING`、2 位
  AI Employee 与 2 个 active Binding 构成当前执行团队。
- 第一轮依次显示 `PLANNED → RUNNING → WAITING_CEO → ACCEPTED → CLOSED`；执行后 Evidence=1、
  Acceptance=`PENDING`，CEO 接受后 Evidence=`VERIFIED`，复盘选择 `CONTINUE` 后
  Acceptance=`CLOSED`、DecisionPacket=`APPLIED`。
- 第二轮依次显示 `PLANNED → RUNNING → WAITING_CEO → REJECTED`；Evidence=1 继续保留为
  `UNVERIFIED`，没有生成 DecisionPacket。
- Backend 使用同一临时 SQLite 重启后，页面恢复第一轮 `CLOSED / CONTINUE` 和第二轮
  `REJECTED`；团队恢复为 Employee=`AVAILABLE`、Role=`OPERATING`、Binding=`ACTIVE`。
- SQLite `integrity_check=ok`、`foreign_key_check` 无结果；Runtime Transition Log 共 68 条。
- 视觉证据：
  - `/tmp/curis-workspace-operating-cycle-evidence/02-closed-and-rejected-after-restart.png`
  - `/tmp/curis-workspace-operating-cycle-evidence/03-cycle-states.png`

活动 `data/curis.sqlite` 未作为本 Issue 的服务、测试或浏览器写目标；浏览器验收完成时只读快照为
`68199cdb703e8e40097f804c47393fc1c9063add0b643f7343d38fb925dd3dc1`，恢复既有三服务后快照为
`b45d50da702e53fef5f4a6b48db697e6e7dfa364b428603c9f732286537df105`。此前已确认的外部活动库
漂移继续作为产品负责人裁定的基线；本 Issue 未恢复、覆盖、合并、清理或追查旧链数据。

## 仍未完成

1. 用生产注入的旧 Workflow Executor 完成一次真实 `workflow_run` 子执行并核对其外部产物；当前
   浏览器受控执行器只证明 Runtime 闭环。
2. 在新鲜打包 Curis.app 中复核同一 Operating Cycle；Developer ID、公证、安装与外部分发门仍开放。
3. 小红书 / 抖音真实平台授权、发布回执、互动与 Outcome，以及 Blueprint Revision / 重新批准链。
