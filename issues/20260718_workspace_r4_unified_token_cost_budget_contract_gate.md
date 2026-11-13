# Workspace R4 第7项｜7a｜统一项目级 Token 成本契约 Gate

- 日期：2026-07-18
- 状态：PASS
- 前置：`issues/20260718_workspace_r4_unified_token_cost_budget_backend_gate.md`
- 父项：`issues/20260718_workspace_r4_unified_token_cost_budget_backend_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

1. 固化项目级预算事实源：
   - `token_usage`：基于 `usage_events` 累计；
   - `estimated_cost`：基于执行时定价与计费模型；
   - 统一缺失值处理（缺 price 时不得默认为 0）。
2. 明确记录字段在 artifact/project_status 的最小可见字段。
3. 保持项目内历史 run 不回改；仅读时回放。

## 约束

- 不新增外部定价服务；
- 不新增运行时调用；
- 不改前端。

## 复核清单（先写先看）

- `step_results` / `usage_events` 可被只读回放；
- `workflow_runs` 真实 `estimated_cost/actual_model` 与使用序列可追溯；
- `estimated_cost` 缺失或不可信时显示 `unknown` 并阻断预算判断。

## 约束复核输入

- 现有第6项与R3收口证据复用：
  - `reviews/20260718_workspace_r4_unified_artifact_output_backend_gate_review.md`
  - `reviews/20260718_workspace_r4_unified_artifact_output_contract_gate_review.md`
  - `reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md`
  - `reviews/20260717_workspace_r3_artifact_project_status_closure_review.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_token_cost_budget_contract_gate.md`
Objective:
定义第7项 Token/成本记录契约，禁止默认 0 成本掩盖缺失。
Special Constraints:
只读边界定义，不做运行时改造。
Next Seat:
系统交付席（已完成）→ 质量运行席（PASS）→ 产品规划席
