# Workspace R4 第7项｜统一项目级 Token 与成本预算 Gate

- 日期：2026-07-18
- 状态：PASS — 第7项已收口
- 前置：`issues/20260718_workspace_r4_unified_artifact_output_backend_gate.md`
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

在第四轮第7项，统一项目级 `Token / 成本 / 预算` 的运行口径，限定为只读与只展示真实记录，不在无授权场景新增调用。

## 允许范围（本项不实施）

- 复用第6项与第3轮收口成果（`workflow_runs.step_results`、`usage_events`）定义预算口径；
- 明确预算上限、缺失值、跨调用可累计成本与单位统一；
- 补齐 fail-closed 与边界解释。

## 不允许范围

- 不新增模型供应商、Provider、出口或凭据链路；
- 不新建测试之外的真实运行；
- 不新增前端展示交互（仅定义边界与复核）。

## 工单拆分（建议）

- 7a｜项目级 Token/成本基础契约（系统交付）
  - Issue：`issues/20260718_workspace_r4_unified_token_cost_budget_contract_gate.md`
- 7b｜预算阻断与可见域边界（系统交付）
  - Issue：`issues/20260718_workspace_r4_unified_token_cost_budget_visibility_gate.md`
- 7c｜第7项收口（产品规划）
  - Issue：`issues/20260718_workspace_r4_unified_token_cost_budget_closeout_gate.md`

## 当前执行

- 7a、7b、7c 已通过，主链路已收口，进入第8项。

## 依赖顺序

1) 7a（契约）
2) 7b（可见域/阻断）
3) 7c（收口）

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_token_cost_budget_backend_gate.md`
Objective:
统一项目级 Token/成本预算边界与可见域，形成 fail-closed 复核。
Special Constraints:
只读边界复核，不改历史、不改前端、不改模型运行链路。
Next Seat:
产品规划席（第8项启动）→ 系统交付席（8a定义）
