# 2026-07-18 Workspace R4 第5项｜5a｜停止边界复核记录

- Issue：`issues/20260718_workspace_r4_manual_stop_boundary_contract_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 证据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`

## 结论

5a 收口成功，停止边界收敛为只读复核口径：  
`run.status in (succeeded|failed|cancelled)` 或 `run 内存在 failed step` 时，`run-next-step` 不再推进；失败 step 之后只保留后续 `pending`，并落 `workflow.step.failed` + `workflow.run.failed` 审计事件与原因。

## 复核证据

1. 代码静态证据

- `backend/app/workflow_runtime.py`  
  - `run_next_step` 中终态直接返回（336-339）  
  - `run_next_step` 中失败 step 阻断（344-345）  
  - `_fail_step` 与 `_fail_run` 均在失败场景落失败状态与事件（734-784）  
  - `_complete_run` 仅在全部成功时触发（760-766）
- `backend/app/main.py`  
  - 运行口径仅暴露 `POST /api/workspace/workflows/{workflow_run_id}/run-next-step` 与 `GET /api/workspace/workflows/{workflow_run_id}`（1914-1925）  
  - 无 cancel/reopen/reset 接口。

2. 运行样本证据（只读）

```sql
SELECT workflow_run_id,status,tenant_id,project_id,failed_at,completed_at
FROM workflow_runs
WHERE workflow_run_id IN (
  'wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc',
  'wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6',
  'wfr-69926fdb-21a2-4166-b6c6-37059309d7ff',
  'wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50',
  'wfr-16c20143-0119-4ae8-923a-8746fc01ad2e'
);
```

- 结果对应：3 条 failed、1 条 succeeded、1 条 running；失败 run 的失败步后续均 pending。

```sql
SELECT ws.workflow_run_id, ws.step_order, ws.status, ws.error
FROM workflow_steps ws
WHERE ws.workflow_run_id = 'wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc'
ORDER BY ws.step_order;
```

- 结果：step6 failed，step7 pending；同 run 无越步成功/运行。

3. 审计链路（reason）  

```sql
SELECT event_type, json_extract(payload,'$.workflow_run_id') AS run_id,
       json_extract(payload,'$.workflow_step_id') AS step_id,
       json_extract(payload,'$.reason') AS reason,
       json_extract(payload,'$.status') AS status
FROM evolution_events
WHERE json_extract(payload,'$.workflow_run_id') IN
  ('wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc',
   'wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6',
   'wfr-69926fdb-21a2-4166-b6c6-37059309d7ff')
ORDER BY event_id;
```

- 三条失败 run 均有 `workflow.step.failed` 与 `workflow.run.failed` 成对事件，且都带 `reason`。

4. 单点 focused 验证（只读）

- 测试：`PYTHONPATH=backend ./backend/.venv/bin/python -m pytest -q backend/tests/test_phase6_workflow_mvp.py -k "test_failed_step_marks_workflow_failed"`
- 结果：`1 passed, 2 deselected`
- 覆盖：失败 step 会让 run 走失败链路。

## 输出

5a（停止边界）可收口。下一步进入 5b（人工接管）定义其入场与执行边界。

Handoff: sent to 产品规划席
