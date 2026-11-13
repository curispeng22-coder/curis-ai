# Workspace R4 第1项子Issue A3｜focused 复核（事实源/边界闭环）

- 日期：2026-07-18
- 状态：PASS — 质量复核完成
- 父项：`issues/20260718_workspace_r4_project_state_fact_source_gate.md`
- Owner：质量运行席
- Next Seat：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

对 `issues/20260718_workspace_r4_project_state_fact_source_a1_mapping_gate.md`
与 `issues/20260718_workspace_r4_project_state_fact_source_a2_tenant_scope_gate.md` 的输出进行一次 focused 复核（1次），确认可复核闭环。

## Must Do

1. 产出 1 条复核命令（不改模型、不起新服务、不重跑 full）。
2. 验证项：
   - project-level status 与 `workflow_runs` terminal 一致；
   - step/execution/usage 与 final artifact 一致；
   - 跨租户/跨项目访问 fail-closed。
3. 输出固定验证结果样例（预期成功样例 + 1-2 条拒绝样例）。

## 复核结果

执行时间：`2026-07-18`  
固定分支：`feat/roadmap-r1r2`  
数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`（只读）  
Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`

### 复核命令（聚焦且一次）

```bash
CURIS_PRODUCT=workspace \
CURIS_DB=/Users/yy/Documents/Curis\ Workspace/deploy/curis/gateway/.generated/data/quality.sqlite \
CURIS_IDENTITY_MODE=test \
CURIS_ENV=local \
backend/.venv/bin/python - <<'PY'
import os, sqlite3
from fastapi.testclient import TestClient
from backend.app.main import create_app

os.environ["CURIS_PRODUCT"] = "workspace"
os.environ["CURIS_DB"] = "/Users/yy/Documents/Curis Workspace/deploy/curis/gateway/.generated/data/quality.sqlite"
os.environ["CURIS_IDENTITY_MODE"] = "test"
os.environ["CURIS_ENV"] = "local"

app = create_app()
client = TestClient(app)
run_id = "wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50"
project_id = "project-e84e06d4-f014-4326-abcd-e6d9aea6ff95"

def get(path, tenant):
    headers = {"X-Tenant-Id": tenant} if tenant is not None else {}
    return client.get(path, headers=headers)

r_ok = get(f"/api/workspace/workflows/{run_id}", "tenant-a")
r_b = get(f"/api/workspace/workflows/{run_id}", "tenant-b")
r_none = get(f"/api/workspace/workflows/{run_id}", "")

obj = r_ok.json() if r_ok.status_code == 200 else {}
steps = obj.get("steps", [])
step_results = obj.get("step_results", [])
artifact = obj.get("artifact") or {}

with sqlite3.connect(os.environ["CURIS_DB"]) as conn:
    conn.row_factory = sqlite3.Row
    scope_hit = conn.execute(
      "select count(*) c from workflow_runs where workflow_run_id=? and tenant_id='tenant-a' and project_id=?",
      (run_id, project_id),
    ).fetchone()["c"] == 1
    usage_count = conn.execute(
      "select count(*) c from evolution_events where tenant_id='tenant-a' "
      "and correlation_id=(select task_id from workflow_runs where workflow_run_id=?) "
      "and event_type='usage.model_call'",
      (run_id,),
    ).fetchone()["c"]

print("A1_status_ok", r_ok.status_code == 200)
print("A1_exec_completed", obj.get("project_status", {}).get("execution_status") == "completed")
print("A1_steps_7", len(steps) == 7)
print("A1_results_7", len(step_results) == 7)
print("A1_all_steps_succeeded", all(s.get("status") == "succeeded" for s in steps))
print("A1_all_results_succeeded", all(sr.get("status") == "succeeded" for sr in step_results))
print("A1_artifact_source", artifact.get("source"))
print("A2_project_scope_ok", scope_hit)
print("A2_cross_tenant_404", r_b.status_code == 404)
print("A2_missing_tenant_404", r_none.status_code == 404)
print("A1_usage_count_7", usage_count == 7)
PY
```

### 结果样例

- 成功样例：
  - `GET /api/workspace/workflows/wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（`X-Tenant-Id: tenant-a`）  
    - `200`
    - `project_status.execution_status = completed`
    - `artifact.source = workflow_runs.final_report`
    - `steps=7`, `step_results=7`, 且全为 `succeeded`
- 复核样例：
  - `X-Tenant-Id: tenant-b` 同 run → `404`
  - 无 `X-Tenant-Id` 同 run → `404`
- DB 校验样例：
  - `workflow_runs` 以 `tenant-a/project-e84e06d4-f014-4326-abcd-e6d9aea6ff95/run` 命中 `1` 条
  - `usage.model_call` 计数 `7`

### 结论

- 结论：`PASS`
- A1/A2 事实源映射与可见域边界复核通过。
- 未新增服务、不改代码、不改模型，不重跑 full，不发起任何出网调用。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate.md`
Objective:
完成事实源映射与可见域边界的最小 focused 复核并输出可追溯结果。
Special Constraints:
仅本次 focused，不做 full regression，不改前端/Session/Mode/AI Secretary/Workflow 语义。
Next Seat:
产品规划席
Handoff: sent to 产品规划席

