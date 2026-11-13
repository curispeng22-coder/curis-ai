# WORKSPACE-STAFFING-SIMULATION-001 Review

Status: Completed (isolated staffing simulation; activation gate open)  
Decision: `PASS_WORKSPACE_STAFFING_SIMULATION_WITH_ACTIVATION_GATE`  
Date: 2026-08-10

## 1. 结论

Workspace Studio 候选组织已具备隔离 `ORG-001` Simulation。Runtime 从当前 Workspace、
Blueprint 和 orgVersion 推导参与对象，验证岗位责任、候选覆盖、能力需求、汇报关系、人工失败
出口与未授权边界；成功后形成非 fixture VERIFIED Evidence、CEO Handoff 和持久化 Review。

本 Review 只证明候选组织草案通过隔离结构验证。Simulation PASS 后 Workspace 仍为 `DRAFT`，
岗位仍为 `DRAFT`、员工仍为 `PROPOSED`、能力需求仍未授权；批准和激活必须进入独立 Issue。

## 2. 实际改动

- Workspace Simulation API 复用现有 `ORG-001`、状态机、Evidence、Handoff 与 CEO Review，
  不新增 Schema、Registry 或平行运行对象。
- `ORG-001` 不接受客户端 subject、participants 或 input refs；Runtime 从当前 Proposal 推导并
  对相同 Blueprint / orgVersion 幂等返回同一未失效运行。
- 隔离执行验证 Blueprint / orgVersion、Role Slot / AI Employee / Capability Binding 覆盖、
  `PROPOSED_FOR`、`REPORTS_TO`、`REQUIRES_CAPABILITY`、人工备用路径和未授权状态。
- 正常路径进入 `WAITING_CEO`；CEO 明确 PASS 后仅 Simulation 进入 `PASSED / PASS`。
- 缺失关系时持久化 `BLOCKED`、责任人与恢复路径；未解决失败不能 PASS，Proposal 不发生部分激活。
- CEO Desk 增加“开始隔离验证 → 等待 CEO 审查 → 已验证 · 未激活”真实 Runtime 动作与状态。
- 通用 Simulation Review 收紧为先验证 PASS 证据，再从 `WAITING_CEO` 恢复，避免非法 PASS
  留下中间状态。

## 3. 证据

- Backend 聚焦回归：`14 passed`；Python compile：通过。
- Frontend Runtime 聚焦回归：`15 passed`；scoped ESLint：通过。
- Next production build：`44/44` 路由生成通过。
- 临时 SQLite 浏览器运行 `simulation-c1bc91c2-2ddb-4f4d-bd2e-8ff615e973b2`：
  `DRAFT → RUNNING → WAITING_CEO → RUNNING → REVIEWED → PASSED`，最终
  `pass_status=PASS / final_state=STAFFING_PROPOSAL_VALIDATED`。
- 运行形成 1 份 `fixture=false / VERIFIED` Evidence、1 个 CEO Handoff、1 个 CEO Decision，
  无 Failure；新页面重新进入后恢复同一 `PASSED` 状态。
- 浏览器先显示“3 位候选 · 证据已形成，等待 CEO 审查”，CEO 点击“确认验证通过”后显示
  “隔离验证已通过，等待独立批准激活 / 已验证 · 未激活”。视觉证据位于
  `/tmp/curis-workspace-staffing-simulation-evidence/`。
- PASS 后 Workspace 保持 `DRAFT / simulation_passed=0`；3 个 Role Slot 保持 `DRAFT`，
  3 位 AI Employee 保持 `PROPOSED`，4 个 Capability Binding 保持
  `PROPOSED / PROPOSED_NOT_AUTHORIZED`。
- 失败测试删除一条能力关系后得到 `WAITING_CEO / BLOCKED` 和未解决 Failure；PASS 被拒绝，
  CEO FAIL 后 Proposal 状态仍不变。
- 临时库 `PRAGMA integrity_check = ok`；活动 `data/curis.sqlite` 未作为服务或测试目标，
  复核 SHA-256 为 `884b2adeba5a61fb3bce68ddcf6d81b1453a730fb5df8740678537fe363d7662`。
- `git diff --check`：通过。

## 4. 边界

- 未修改数据库 Schema、Runtime 状态机 / Registry、活动数据库、旧 Project / Task 链、
  真实平台 API、商业化 Admin、Desktop Packaging、Blueprint 或一级导航。
- VERIFIED Evidence 只证明当前候选组织结构契约，不证明模型、连接器、权限或外部执行能力。
- 未提供员工接受提案、Role Slot 分配、Capability Authorization / Activation 或 Workspace
  Operating 命令；没有自动批准。
- 本轮浏览器写入只指向临时 SQLite；无 stage、commit 或 push。

## 5. 未关闭事项

1. 为 `requirement:*` 选择真实 Company Capability / Connector / Model 供给并完成权限、风险、
   成本和数据流审查；缺失供给必须 fail-closed。
2. 独立 Issue 建立 CEO Approval / Reject / Modify 与原子激活 / 回滚命令；只有当前未失效
   `ORG-001 PASS` 和真实能力供给齐备时才能激活。
3. 激活后验证 Role Slot 分配、AI Employee 可用、Capability Binding 授权、Workspace
   Operating Version 及组织变更失效传播。
4. 当前源码尚未重打包进新鲜 Curis.app；Desktop 分发门保持开放。
