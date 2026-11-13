# Workspace R4 第6项｜统一 Artifact / Output 后端 Gate

- 日期：2026-07-18  
- 状态：PASS — 第6项闭环（6a/6b/6c）
- 前置：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

按第四轮序列进入第6项，统一说明并闭环 Artifact 与 Output 后端的只读边界，使 `GET /api/workspace/workflows/{workflow_run_id}` 的成果与项目长期状态在第四轮已有基础上形成一致读取口径。

## 允许范围（本项不实施）

- 复用 R3/现有闭环证据（`final_report`、`step_results`、`usage_events`）定义统一可见规则；
- 对外只读投影字段、可见域与 fail-closed 行为做边界复核；
- 输出：本项 Review 的 PASS/阻塞说明；
- 新增/修订 focused 复核脚本（仅无出网验证）。

## 不允许范围

- 新增存储、成果表、外部存储桶或模型调用；
- 改写历史 `final_report`/`step_results`/`usage_events`；
- 改前端、改 Dashboard、改 Admin 或引入新凭据链路；
- 并发开启 AI Secretary、Mode/团队迁移、Marketplace、外部 Connector。

## 最小验收

1. Artifact 仅源于 `workflow_runs.final_report` 的只读投影，不重新生成正文；
2. `artifact.source`、`tenant/company/project/run/task` 与 `steps/results/usage` 可追溯一致；
3. 跨租户与错 Run 必须 404/403 fail-closed；
4. 历史成功和失败 run 不回改；
5. 不展开新的 full regression，执行最小复核并形成 review。

## 特殊约束

- 第3~5项边界不改写；
- 不扩展模型/网关/Token 规则；
- 不发起 run，不注 Key，不出网。

## 证据输入（复用）

- `reviews/20260717_workspace_r3_artifact_project_status_architecture_review.md`
- `reviews/20260717_workspace_r3_artifact_project_status_closure_review.md`
- `reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md`
- `reviews/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate_review.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_artifact_output_backend_gate.md`
Objective:
统一收口 Artifact 与 Output 后端只读边界（不新增功能、不改历史）。
Special Constraints:
固定引用 `final_report` 与现有事实源，不得新增服务、凭据、front-end、出网实现。
Next Seat:
产品规划席（第6项关闭）→ 第7项（统一项目级 Token 与成本预算）
