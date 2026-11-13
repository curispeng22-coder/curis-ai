# 2026-07-18 Workspace R4 Memory 恢复演练 Gate 复核（B2）

- Issue: `issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`

## 复核范围（只读）

- 对示例失败 run `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` 做一次读取演练。
- 检验恢复判定、不可逆字段、是否可直接续推、历史回溯边界。

## 复核命令（只读）

```bash
BACKUP_DB='/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite'
RUN_ID='wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc'
backend/.venv/bin/python - <<'PY'
import sqlite3

db='/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite'
run_id='wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc'

def status(vals):
    vals=sorted(set(vals))
    if not vals: return 'none'
    return ','.join(vals) if len(vals)>1 else vals[0]

with sqlite3.connect(db) as c:
    c.row_factory=sqlite3.Row
    run=c.execute(\"select workflow_run_id,tenant_id,project_id,task_id,status,final_report from workflow_runs where workflow_run_id=?\", (run_id,)).fetchone()
    steps=c.execute(\"select workflow_step_id,step_order,status from workflow_steps where tenant_id=? and workflow_run_id=? order by step_order\", (run['tenant_id'],run_id)).fetchall()
    step_results=c.execute(\"select workflow_step_id,status from step_results where tenant_id=? and workflow_step_id in (select workflow_step_id from workflow_steps where tenant_id=? and workflow_run_id=?)\", (run['tenant_id'],run['tenant_id'],run_id)).fetchall()
    usages=c.execute(\"select event_id,payload from evolution_events where tenant_id=? and event_type='usage.model_call' and correlation_id=(select task_id from workflow_runs where workflow_run_id=?)\", (run['tenant_id'],run_id)).fetchall()
    latest_success=c.execute(\"select workflow_run_id from workflow_runs where tenant_id=? and project_id=? and status='succeeded' order by updated_at desc limit 1\", (run['tenant_id'],run['project_id'])).fetchone()

print('run_id', run['workflow_run_id'])
print('status', run['status'])
print('tenant', run['tenant_id'], 'project', run['project_id'], 'task', run['task_id'])
print('final_report_len', len(run['final_report'] or ''))
print('steps', len(steps), 'statuses', status([s['status'] for s in steps]))
print('results', len(step_results), 'result_statuses', status([s['status'] for s in step_results]))
print('usages', len(usages))
print('pending_steps', [s['workflow_step_id'] for s in steps if s['status']=='pending'])
print('recoverable', run['status'] in ('pending','running') and any(s['status']=='pending' for s in steps))
print('latest_success_run', latest_success['workflow_run_id'] if latest_success else None)
PY
```

## 结果（单次聚焦）

- run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`（tenant-a/project-e84...）
  - `status=failed`
  - `steps=7`, `results=5`, `usages=5`
  - `steps status`: `succeeded`+`failed`+`pending` 混合
  - `pending_steps` 存在，但 `status != pending/running`，因此**不可直接续推**
  - `final_report=''`
  - 同 project 下有成功 run `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`

## 结论

- 该示例演练在现有事实下判定为不可续推（`recoverable=false`），建议新建 Run 重跑而非回写旧 run。
- 未读取/改写历史 `workflow_runs`、`workflow_steps`、`step_results`、`evolution_events`，满足只读演练边界。
- B2 结论闭环通过，可转 B3 兼容性验收。

Compact Handoff:
Issue: `issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`
Special Constraints: 不发起模型调用、不改 API、不改历史数据库。  
Next Seat: 质量运行席（B3 兼容性验收）
Handoff: sent to 质量运行席
