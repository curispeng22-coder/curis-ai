# Workspace R4 第5项｜5a｜停止边界（Stop）

- 日期：2026-07-18
- 状态：PASS — CLOSED（停止边界定义收口）
- 前置：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- 父项：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

定义明确且可复核的停止/阻断边界：什么时候只能 stop/halt，不允许任何 step 继续推进。

## 约束

1. 不改现有执行器逻辑。
2. 不改历史。
3. 不新增前端/服务/字段。
4. 不发起 run。

## Must Do

- 停止条件（只读判定）：
  - `workflow_runs.status` 已是 `succeeded` / `failed` / `cancelled` 时，后续 `run-next-step` 不得执行；
  - 当同 run 任一 `workflow_steps.status='failed'` 时，`run-next-step` 执行 `_fail_run`，其后不再推进下一步；
  - `run-next-step` 每次只处理同 run 的**一个**首个 `pending` 步骤。
- 人工禁止项：
  - 未命中上述条件前提的任何新运行行为都不允许（不允许“补写状态”或“隐式跳步”）。
- 产出最小可见事实：
  - `workflow_runs`：`status / failed_at / final_report / completed_at / updated_at`
  - `workflow_steps`：`step_order / employee_role / status / error / completed_at`
  - `step_results`：每个成功 step 的 `step_result_id / result / status`
  - `evolution_events`：`workflow.step.failed`、`workflow.run.failed`、`workflow.run.completed` 及 `reason`  
    （`run` 与 `step` 事件同链路，支持失败可追溯）
- 与 4a/4b 一致性复核：
  - 对齐 `issues/20260718_workspace_r4_auto_progress_advance_contract_gate.md` 与 `issues/20260718_workspace_r4_auto_progress_timeout_contract_gate.md` 的终态判定。
- 已落地脚本（只读）：
  - 下节 `执行证据` 中给出一组可复核 SQL。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_manual_stop_boundary_contract_gate.md`
Objective:
定义第5项中 stop/halt 的统一触发与可复核输出边界，并产出 one-shot 复核脚本。
Special Constraints:
只定义边界与复核模板，不实现，不改历史。
Next Seat:
产品规划席

## 结论（第5a）

已闭环。停止边界不涉及任何实现变更，仅通过 `WorkflowRuntime.run_next_step` 与现有事件链路固定可复核：

- `run.status in (succeeded|failed|cancelled)`：直接返回当前 run，不会执行 step；
- `exists failed step`：返回前直接 `workflow_runs.status='failed'`，并落 `workflow.run.failed`；
- 失败发生后 `step N` 标记 `failed`，其后 step 仅能停留 `pending`；
- `evolution_events` 具备 `step.failed` + `run.failed`/`run.completed`，具备 reason 与 action 追踪闭环；
- 当前数据库中没有 `cancelled` 样本，因此只确认 `succeeded/failed/running/pending` 的可复核边界；
- 继续调用 `run-next-step` 前提应仅用于状态读取，不应作为“恢复失败 run”的更新手段，恢复由 5b 接口层定义。

### 复核证据（只读）

1) 代码静态

- `backend/app/workflow_runtime.py:336-760`  
  - `run-next-step` 返回前置终态判定：`if run.status in {"succeeded","failed","cancelled"}: return run`
  - 失败后停止判定：`if any(step.status == "failed" for step in run["steps"]): _fail_run(...)`
  - 失败后无条件重返失败状态与失败事件；不会进入下一 step
  - 成功路径：所有 step 成功后 `_complete_run(...)`
- `backend/app/main.py:1919-1925`  
  - 对外路由只有 `POST /api/workspace/workflows/{workflow_run_id}/run-next-step` 与 `GET /api/workspace/workflows/{workflow_run_id}`
  - 未提供 cancel/reset/rollback API

2) 复核 SQL（`deploy/curis/gateway/.generated/data/quality.sqlite`）

```sql
-- stop 可复核：终态 run 与失败样本最小视图
SELECT wr.workflow_run_id, wr.status, wr.failed_at, wr.completed_at,
       SUM(CASE WHEN ws.status='failed' THEN 1 ELSE 0 END) AS failed_steps,
       MIN(CASE WHEN ws.status='pending' THEN ws.step_order END) AS min_pending_step,
       MAX(CASE WHEN json_extract(ee.payload, '$.event_type')='workflow.run.failed' THEN ee.event_type END) AS last_run_failed_evt
FROM workflow_runs wr
LEFT JOIN workflow_steps ws ON ws.workflow_run_id = wr.workflow_run_id
LEFT JOIN evolution_events ee
  ON json_extract(ee.payload, '$.workflow_run_id') = wr.workflow_run_id
GROUP BY wr.workflow_run_id
ORDER BY wr.workflow_run_id;
```

```sql
-- run 停止/拒绝闭环（失败 run）
SELECT ws.workflow_run_id, ws.step_order, ws.status AS step_status, ws.error,
       ee.event_type, json_extract(ee.payload,'$.reason') AS reason,
       ee.created_at
FROM workflow_steps ws
LEFT JOIN evolution_events ee
  ON ee.event_type IN ('workflow.step.failed','workflow.run.failed')
 AND json_extract(ee.payload, '$.workflow_run_id') = ws.workflow_run_id
 AND json_extract(ee.payload, '$.workflow_step_id') = ws.workflow_step_id
WHERE ws.workflow_run_id IN ('wfr-69926fdb-21a2-4166-b6c6-37059309d7ff',
                            'wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6',
                            'wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc')
ORDER BY ws.workflow_run_id, ws.step_order, ee.event_id;
```

3) 历史数据样本

- `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`：step6 failed 后 step7 pending；`workflow.step.failed` + `workflow.run.failed` 落 reason；
- `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`：step1 failed 后后续步骤 pending；`workflow.step.failed` + `workflow.run.failed` 落 reason；
- `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`：step1 failed 后后续 pending；`workflow.step.failed` + `workflow.run.failed` 落 reason。

### 聚焦验证

- 执行用例：`backend/tests/test_phase6_workflow_mvp.py::Phase6WorkflowMvpTests::test_failed_step_marks_workflow_failed`
- 结果：`1 passed`、`2 deselected`
- 结论：失败 step 后 run 状态保持失败且无越步执行。
