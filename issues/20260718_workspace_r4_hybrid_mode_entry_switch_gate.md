# Workspace R4 第3项｜Hybrid Mode 入口与切换 Gate（M3a）

- 日期：2026-07-18
- 状态：OPEN — PARTIAL（无显式 Hybrid 入口/回退事件字段；仅有顺序降级行为样本）
- 父项：`issues/20260718_workspace_r4_hybrid_mode_profile_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

定义 Hybrid Mode 的入口条件与切换条件：什么情况下允许“人机共担”，什么时候自动回退到 Workflow/Agent 的保守模式。

## 必须定义

1. 准入条件：已签发成员身份 + 同项目 session + 角色/能力可校验
2. 切换条件：上下文缺失或冲突时自动退回到 Workflow Mode
3. 角色优先与并发互斥条件（同一 run 同时只允许一个主动上下文模式）
4. 回退触发后对步骤状态的影响（禁止自动推进、明确失败原因）

## 最小复核（只读）

- 通过现有 `workflow_runs`/`usage_events`（如有）历史核验切换、回退是否有清晰拒绝痕迹

## 执行口令（系统交付席）

- 只读抽样以下场景并记录：
  - 同一 run 内出现“可转 Hybrid 的前置条件”是否满足；
  - 一旦冲突/缺失触发回退时是否立即停止自动推进；
  - 回退原因是否可归档为明确拒绝或回退原因。
- 产物：抽样清单（run_id、触发条件、最终决策）。

## 约束

- 不新增切换 API，不改前端，不改运行器行为
- 不发起真实模型调用，不新增数据库字段
- 仅定义+复核口径

## 当前复核

- 复核输出：`reviews/20260718_workspace_r4_hybrid_mode_entry_switch_gate_review.md`（PARTIAL，未命中显式 `mode/handoff` 日志字段）

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md`
Objective:
清晰限定 Hybrid Mode 的入口、切换与回退边界。
Special Constraints:
不改现网执行器/网关/凭据，不改 schema，不发起模型调用。
Next Seat:
产品规划席（确认定义）→ 系统交付席（确认落地）→ 质量运行席（focused 复核）
