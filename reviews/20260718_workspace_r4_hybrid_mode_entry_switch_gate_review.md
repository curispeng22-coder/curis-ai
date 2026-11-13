# 2026-07-18 Workspace R4 Hybrid Mode 入口与切换复核

- Issue：`issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 证据数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PARTIAL`

## 复核范围

- 只读读取 `evolution_events` 与 `workflow_runs / workflow_steps / step_assignments / step_results`，仅核验是否存在可复核的 Hybrid 入口/回退信号。

## 结果

- 事件类型汇总（样本）：
  - `usage.model_call`、`usage.task_execution`、`usage.tool_call`
  - `workflow.run.created / started / failed / completed`
  - `workflow.step.assigned / started / completed / failed`
- Hybrid 或模式切换相关字段检索：
  - `event.payload` 中未检出 `mode` / `handoff` / `intervention` 字段；
  - 未检出 `workflow.mode*`、`hybrid` 类事件类型。
- `workflow.*` 事件中仅有：
  - `workflow_run_id / workflow_step_id / task_id / actor_id / employee_id / employee_role / action / status / reason / timestamp`；
  - `actor_type`（在 `usage.*` 中）固定为 `ceo`。
- 成功 run `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50` 与失败 run 组（如 `wfr-e96...`）均满足：
  - step 以 `step_order` 顺序推进；
  - 失败后未见继续推进成功行为；
  - 未见显式“Hybrid enter / exit / handoff”日志。

## 结论

- 现有运行时事实可复核到“缺省下以 Workflow/Agent 方式推进”的行为。
- 当前未命中或未记录任何 Hybrid 入口与回退事件；缺少可复核证据样本，因此本项仅能到 `PARTIAL`。

Handoff: sent to 产品规划席（待确认定义边界与后续补样本）
