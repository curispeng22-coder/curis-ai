# Workspace R4 第7项｜7b｜统一 Token/成本预算可见域与阻断 Gate

- 日期：2026-07-18
- 状态：PASS
- 前置：`issues/20260718_workspace_r4_unified_token_cost_budget_contract_gate.md`
- 父项：`issues/20260718_workspace_r4_unified_token_cost_budget_backend_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

统一定义项目级预算读取边界：
- 合法 tenant/project/run 可读取累积 budget；
- 跨 tenant/project/wrong run 及缺失授权 fail-closed；
- 超预算或成本未明确时拒绝误导展示并触发阻断信号。

## 约束

- 不扩展 scope，不新增 API；
- 不改模型调用行为；
- 不改前端。

## 最小复核

- 在现有已完成 run 上验证预算字段与实际调用计数一致；
- `tenant-b` 或错误 run 的预算读取不可泄漏；
- 缺失价格字段时不应显示可结算总额。

## 约束复核输入

- 预算源与跨租户边界复用：
  - `reviews/20260718_workspace_r4_unified_artifact_output_backend_gate_review.md`
  - `reviews/20260718_workspace_r4_unified_output_cross_tenant_visibility_gate_review.md`
  - `reviews/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate_review.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_token_cost_budget_visibility_gate.md`
Objective:
定义第7项 budget 可见域与阻断边界，避免越权预算展示与误报。
Special Constraints:
保持只读复核，不起新 run，不出网。
Next Seat:
系统交付席（已完成）→ 质量运行席（PASS）→ 产品规划席
