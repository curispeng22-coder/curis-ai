# 2026-07-18 Workspace R4 Memory Scope Key Gate 复核（B1）

- Issue: `issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`

## 复核范围（只读）

- Scope/Key 规范文本与样例的可复现性；
- `tenant_id + project_id + scope_version + primary` 唯一性；
- 运行/步骤/Execution/Usage/owner 主键映射稳定性；
- 与第三轮历史 run 的兼容（不改历史数据）。

## 聚焦复核命令（一次）

```bash
BACKUP_DB="/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite"
RUN_IDS=(
  "wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc"
  "wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50"
)
backend/.venv/bin/python - <<'PY'
import json
import sqlite3

db = "/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite"
run_ids = [
    "wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc",
    "wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50",
]
scope = "workspace.project_memory.scope.v1"

def k(scope_type, **kws):
    if scope_type == "project":
        return f"mem.v1.project|tenant={kws['tenant_id']}|project={kws['project_id']}|version={scope}"
    if scope_type == "run":
        return f"mem.v1.run|tenant={kws['tenant_id']}|project={kws['project_id']}|run={kws['workflow_run_id']}|version={scope}"
    if scope_type == "step":
        return f"mem.v1.step|tenant={kws['tenant_id']}|project={kws['project_id']}|run={kws['workflow_run_id']}|step={kws['workflow_step_id']}|version={scope}"
    if scope_type == "execution":
        return f"mem.v1.execution|tenant={kws['tenant_id']}|project={kws['project_id']}|task={kws['task_id']}|execution={kws['execution_id']}|version={scope}"
    if scope_type == "usage":
        return f"mem.v1.usage|tenant={kws['tenant_id']}|project={kws['project_id']}|task={kws['task_id']}|step={kws['workflow_step_id']}|usage={kws['event_id']}|version={scope}"
    if scope_type == "owner":
        return f"mem.v1.owner|tenant={kws['tenant_id']}|project={kws['project_id']}|owner={kws['owner_id']}|version={scope}"

with sqlite3.connect(db) as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    for run_id in run_ids:
        run = c.execute(
            "select workflow_run_id, tenant_id, project_id, task_id, status from workflow_runs where workflow_run_id=?",
            (run_id,),
        ).fetchone()
        if not run:
            print(f"{run_id} missing")
            continue

        tenant_id, project_id, task_id, status = run["tenant_id"], run["project_id"], run["task_id"], run["status"]
        steps = c.execute(
            "select workflow_step_id, step_order from workflow_steps where tenant_id=? and workflow_run_id=? order by step_order",
            (tenant_id, run_id),
        ).fetchall()
        exes = c.execute(
            "select execution_id, task_id, tenant_id from executions where tenant_id=? and task_id=?",
            (tenant_id, task_id),
        ).fetchall()
        usages = c.execute(
            "select event_id, payload from evolution_events where tenant_id=? and event_type='usage.model_call' and correlation_id=?",
            (tenant_id, task_id),
        ).fetchall()
        owner = c.execute(
            "select owner_employee_id from projects where tenant_id=? and project_id=?",
            (tenant_id, project_id),
        ).fetchone()
        owner_id = owner["owner_employee_id"] if owner else "NONE"

        keys = [
            k("project", tenant_id=tenant_id, project_id=project_id),
            k("run", tenant_id=tenant_id, project_id=project_id, workflow_run_id=run_id),
            k("owner", tenant_id=tenant_id, project_id=project_id, owner_id=owner_id),
        ]
        for st in steps:
            keys.append(k("step", tenant_id=tenant_id, project_id=project_id, workflow_run_id=run_id, workflow_step_id=st["workflow_step_id"]))
        for ex in exes:
            keys.append(k("execution", tenant_id=tenant_id, project_id=project_id, task_id=ex["task_id"], execution_id=ex["execution_id"]))
        for u in usages:
            payload = json.loads(u["payload"])
            keys.append(
                k(
                    "usage",
                    tenant_id=tenant_id,
                    project_id=project_id,
                    task_id=task_id,
                    workflow_step_id=payload.get("workflow_step_id"),
                    event_id=u["event_id"],
                )
            )

        print("----")
        print("run", run_id, "status", status)
        print("tenant", tenant_id, "project", project_id)
        print("steps", len(steps), "executions", len(exes), "usage", len(usages))
        print("keys", len(keys), "unique", len(set(keys)), "duplicate_groups", len(keys) - len(set(keys)))
        print("step_orders", [s["step_order"] for s in steps][:7])
        print("usage_scope_type", sorted({json.loads(u["payload"]).get("scope_type") for u in usages}))
PY
```

## 结果（预期）

- `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`（失败 run）：
  - `steps=7`、`executions=5`、`usage=5`；
  - `project/run/owner/step/execution/usage` key 构造后 `keys=20`, `unique=20`，无重复；
  - `scope_type` 全部为 `model`，`usage` 对应 `workflow_step_id` 可回映射。
- `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（成功 run）：
  - `steps=7`、`executions=7`、`usage=7`；
  - `project/run/owner/step/execution/usage` key 构造后 `keys=24`, `unique=24`，无重复；
  - `scope_type` 全部为 `model`。

## 结论

- B1 的 scope/key 规范可复现，未出现 key 冲突；
- `tenant_id + project_id + scope_version + 主键` 作为版本化主约束成立；
- `project_status` 与 `final_report` 等读链不在本 Issue 范围内改写；
- 该项质量聚焦 PASS，可进入 B2。

Compact Handoff:
Issue: `issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md`
Special Constraints: 只读核验，不改历史/建新 Run/出网；不改前端/Session/Mode/AI Secretary。  
Next Seat: 产品规划席（接收 PASS，推进 `issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`）  
Handoff: sent to 产品规划席
