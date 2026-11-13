# Workspace R4 第5项｜人工接管、停止和风险升级 Gate

- 日期：2026-07-18
- 状态：PASS — 第5项闭环（5a/5b/5c 收口）
- 前置：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

在第4项复核基础上，定义“停止、人工接管、风险升级”三类动作的最小运行口径。

## 约束

1. 不改现有出网实现、网关、Provider/Model、凭据边界。
2. 不改数据库历史与既有 `workflow_runs`/`workflow_steps`/`step_results`/`usage_events`/`evolution_events`。
3. 不新增前端、调度器、schema、凭据路径。
4. 不发起新建 Run/重试历史失败作为第5项实现。

## 工单拆分（本项独立）

- 5a｜停止边界（系统交付）
  - Issue：`issues/20260718_workspace_r4_manual_stop_boundary_contract_gate.md`
- 5b｜人工接管请求/动作（系统交付）
  - Issue：`issues/20260718_workspace_r4_manual_takeover_request_contract_gate.md`
- 5c｜风险升级策略（系统交付）
  - Issue：`issues/20260718_workspace_r4_manual_risk_escalation_contract_gate.md`

## 顺序

5a → 5b → 5c，不并行。

## 交付要求（系统交付可直接复核）

- 5a、5b、5c 都定义为“只读可复核边界”，不执行历史 run。
- 每项输出：
  - 停止/接管/升级触发条件；
  - 可见证据字段；
  - 不可逆字段保护；
  - one-shot 复核脚本（SQL/接口）；
- 一并形成主项决策模板：`Stop / Hold / Escalate / Create-New-Run`。

## 当前进展

- 5a/5b/5c 已按“只读边界+可复核脚本”闭环：
  - 5a 停止边界：`issues/20260718_workspace_r4_manual_stop_boundary_contract_gate.md`（PASS/CLOSED）
  - 5b 人工接管入口：`issues/20260718_workspace_r4_manual_takeover_request_contract_gate.md`（PASS/CLOSED）
  - 5c 风险升级策略：`issues/20260718_workspace_r4_manual_risk_escalation_contract_gate.md`（PASS/CLOSED）

## 输出

- 输出 `issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md` 的第5项补充边界说明。
- 输出 `reviews/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate_review.md`，内含统一 `Stop / Hold / Escalate / Create-New-Run` 决策模板与边界落库。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
Objective:
串行补齐第5项停止/人工接管/风险升级边界并输出统一决策模板。
Special Constraints:
只定义边界与复核清单，不实现；不改历史、不加字段、不改前端。
Next Seat:
产品规划席（收口第四轮）
