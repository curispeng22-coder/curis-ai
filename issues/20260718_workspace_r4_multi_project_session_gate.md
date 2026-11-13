# Workspace R4 第2项｜同一员工多项目独立 Session（启动项）

- 日期：2026-07-18
- 状态：PASS — 第2项闭环
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席（确认闭环，准备第3项）
- 分支：`feat/roadmap-r1r2`

## 目标

在不改前端、不改现有 Session/Mode/UserFlow 形态的前提下，定义并验证“同一员工在多个项目下可独立持有执行上下文”的最小边界：

- 员工与项目的 `Session` 事实边界明确（`tenant_id + employee_id + project_id + scope`）。
- 上下文切换按项目隔离，不跨项目复用步骤状态/上下文缓存/待处理队列。
- 恢复与回放以项目为单元，不污染其他项目的运行事实。

## 允许范围

- 只改边界与映射定义文件、最小只读查询/聚焦验证命令，不扩展新 API 语义。
- 允许复用第四轮第1项的项目长期状态读链（`project_status`、`artifact`、`usage`）作前置事实映射。
- 允许新增聚焦脚本用于 `employee/project/run` 三者交叉验证（无外网调用、无新依赖）。

## 禁止范围

- 不改动 R3 已冻结运行契约与第三方 Gateway。
- 不实现 AI Secretary、人工接管界面、Agent Mode、Workflow Mode、Hybrid Mode。
- 不改 Admin 正式资产、数据库跨库迁移、前端页面与路由。

## 失败前提（L2 触发条件）

- 员工身份与项目归属边界不再按 `tenant` 强绑定；
- 发生 Project 跨租户/跨项目状态污染；
- 以单次内存快照代替可查询历史上下文。

## 工单拆分（顺序）

- C0｜前置样本恢复（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_multi_project_session_seed_gap_gate.md`
  - 目标：补齐跨项目样本，解除 C1/C2 前置阻塞。
- C1｜同一员工多项目 Session Scope 与 Key 规范（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_multi_project_session_scope_gate.md`
  - 目标：固化 scope/key + 冲突拒绝。
- C2｜项目内外 Session 隔离与切换验收（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_multi_project_session_context_switch_gate.md`
  - 目标：project 切换不泄露步骤状态/上下文引用。
- C3｜恢复可追溯性闭环（质量运行）
  - 跳转 Issue：`issues/20260718_workspace_r4_multi_project_session_recovery_gate.md`
  - 目标：失败 run 的项目级恢复不影响其他项目。

## 关键验收

- `employee_id` 同时关联多个 `project_id` 时，`scope key` 不冲突；
- `project_id` 切换下，读取/恢复与历史状态只返回当前 project 范围；
- 失败与历史 run 保持隔离，不因新项目 session 被覆盖；
- 无 mock/stub 验证、无新依赖外呼。

## 当前进展

- 第2项闭环，三链均 PASS：
  - C0：`issues/20260718_workspace_r4_multi_project_session_seed_gap_gate.md`（PASS）
  - C1：`issues/20260718_workspace_r4_multi_project_session_scope_gate.md`（PASS）
  - C2：`issues/20260718_workspace_r4_multi_project_session_context_switch_gate.md`（PASS）
  - C3：`issues/20260718_workspace_r4_multi_project_session_recovery_gate.md`（PASS）
- 第3项已拆分：`issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`（待边界产出并复核）

## 证据

- 复核 Review：
  - `reviews/20260718_workspace_r4_multi_project_session_scope_gate_review.md`
  - `reviews/20260718_workspace_r4_multi_project_session_context_switch_gate_review.md`
  - `reviews/20260718_workspace_r4_multi_project_session_seed_gap_gate_review.md`
  - `reviews/20260718_workspace_r4_multi_project_session_recovery_gate_review.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_multi_project_session_gate.md`
Objective:
定义同一员工多项目独立 Session 的 Scope/Key、隔离与恢复闭环，确保多项目运行不互相污染，且具备可复核边界。
Special Constraints:
仅围绕第四轮第2项；第3项已拆分为边界定义；不改前端、R3 运行核算、外部网关与凭据。
Next Seat:
产品规划席（确认第2项闭环，拆解第3项）
