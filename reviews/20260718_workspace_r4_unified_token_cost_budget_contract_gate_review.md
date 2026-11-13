# 2026-07-18 Workspace R4 第7项 7a Review

- Issue：`issues/20260718_workspace_r4_unified_token_cost_budget_contract_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 复核 run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- 结论：`PASS`

## 复核范围

1. `reviews/20260718_workspace_r4_unified_artifact_output_backend_gate_review.md`
2. `reviews/20260718_workspace_r4_unified_output_cross_tenant_visibility_gate_review.md`
3. `reviews/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate_review.md`
4. `reviews/20260717_workspace_r3_artifact_project_status_closure_review.md`
5. `backend/app/workflow_runtime.py` 与 `backend/app/evolution_event_log.py` 现有只读映射

## 结果

- 第7a契约目标可回放：该 run 在 `usage.model_call` 下有 **7** 条真实 usage 记录，且均 `outbound_attempted=true`、`status=success`、`estimated_cost>0`、`total_tokens>0`。
- 预算累计一致：
  - `prompt_tokens=8008`
  - `completion_tokens=1614`
  - `total_tokens=9622`
  - `estimated_cost=0.013269`（USD）
- `workflow_runs` 对应 final_report 已回放：`final_report` 非空，长度 `6018`，SHA-256 `2d14cf90ca1fa850f7e8425763b922cda4c6c9c2132a2f55eac07791a07ba96c`，与既有 Artifact read-model 规则一致。
- `workflow_runtime` 的 `project_status`/`artifact` 仍为只读投影链路，现阶段没有新增预算字段持久化，仅通过 usage 事件进行聚合可见（契约上是读链透明）。
- 未出现 `estimated_cost` 缺失/<=0 记录；当前 run 对应 budget 断言可直接成立。

## 结论

7a（项目级 Token/成本基础契约）在既有真实 run 与只读投影链上闭环为 `PASS`，可进入 7b 验证预算可见域与阻断边界。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_token_cost_budget_contract_gate.md`
Objective:
定义项目级 Token/成本 read-contract 的只读边界与缺失值处理。  
Special Constraints:
当前阶段不新增字段/接口/运行；只读核验既有 usage 与 artifact 链路。  
Next Seat:
质量运行席（可收口确认）→ 产品规划席
