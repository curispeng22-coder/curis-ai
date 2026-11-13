# Workspace R4 第9项｜团队迁移任务队列

- 日期：2026-07-18
- 状态：OPEN — 任务执行队列（进行中）
- 所属：`issues/20260718_workspace_r4_codex_workbuddy_team_migration_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（拆分）→ 质量运行席（聚焦复核）→ 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

将第9项按最小闭环粒度拆分后，提供明确顺序推进口径。

## 顺序与依赖

1. `issues/20260718_workspace_r4_team_migration_scope_gate.md`
   - `issues/20260718_workspace_r4_team_migration_scope_gate_9a1_owner_boundary_gate.md`
   - `issues/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate.md`
   - `issues/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_gate.md`
2. `issues/20260718_workspace_r4_team_migration_scope_gate_9a_rollup_gate.md`
3. `issues/20260718_workspace_r4_team_migration_transfer_gate.md`
   - `issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate.md`
   - `issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate.md`
   - `issues/20260718_workspace_r4_team_migration_transfer_gate_9b3_sensitive_artifact_gate.md`
4. `issues/20260718_workspace_r4_team_migration_transfer_gate_9b_rollup_gate.md`
5. `issues/20260718_workspace_r4_team_migration_closeout_gate.md`

1→2→3→4→5，任一未 PASS 阻塞其后。

## 复核入口

- 先完成 9a 单项与 9a.4 汇总、再完成 9b 单项与 9b.4 汇总后，执行 `issues/20260718_workspace_r4_team_migration_closeout_gate.md` 收口。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_rollout_queue.md`
Objective:
规范化第9项任务拆分与顺序。
Special Constraints:
只做队列与拆分状态，不改实现。
Next Seat:
产品规划席（确认后续分配）

Handoff: sent to 产品规划席
