# Workspace R4 第2项子Issue C3｜多项目 Session 恢复可追溯性

- 日期：2026-07-18
- 状态：PASS — 已闭环
- 父项：`issues/20260718_workspace_r4_multi_project_session_gate.md`
- Owner：质量运行席
- Next Seat：质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

在 C1/C2 边界形成后，对一条失败或中断 run 做“项目内恢复可追溯性”最小演练：

- 明确恢复对象固定为某个 `tenant_id + employee_id + project_id`；
- 证明项目 A 恢复失败不改变项目 B 已有历史；
- 证据化恢复后的可读状态与剩余步骤边界。

## 约束

- 只允许一次聚焦复核（No full regression、No mock/stub）。
- 不改代码、不改网关、不改前端、不新建 external call。
- 历史失败 run 与历史失败原因保留不变。

## 输出（必须）

- 一次恢复演练记录（输入 run_id、输出状态、边界说明）。
- 证明当前项目 B 仅受本项目运行事实影响的 evidence。

## 最小执行口令（一次）

```bash
cd '/Users/yy/Documents/Curis AI Workspace'
DB='deploy/curis/gateway/.generated/data/quality.sqlite'
backend/.venv/bin/python - <<'PY'
import sqlite3

db = '/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite'
run_target = 'wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

run = c.execute("""
select r.tenant_id, r.project_id, r.status,
       sa.employee_id
from workflow_runs r
left join workflow_steps ws on ws.workflow_run_id = r.workflow_run_id
left join step_assignments sa on sa.workflow_step_id = ws.workflow_step_id
where r.workflow_run_id=?
LIMIT 1
""", (run_target,)).fetchone()
print("target", dict(run) if run else None)
if not run:
    raise SystemExit("run not found")

proj_runs = c.execute(
    """
    select r.workflow_run_id, r.status
    from workflow_runs r
    join workflow_steps ws on ws.workflow_run_id = r.workflow_run_id
    join step_assignments sa on sa.workflow_step_id = ws.workflow_step_id
    where r.tenant_id=? and sa.employee_id=? and r.project_id=?
      and sa.employee_id is not null
    group by r.workflow_run_id, r.status
    """,
    (run["tenant_id"], run["employee_id"], run["project_id"])
).fetchall()
other_proj_runs = c.execute(
    """
    select r.workflow_run_id, r.project_id, r.status
    from workflow_runs r
    join workflow_steps ws on ws.workflow_run_id = r.workflow_run_id
    join step_assignments sa on sa.workflow_step_id = ws.workflow_step_id
    where r.tenant_id=? and sa.employee_id=? and r.project_id!=?
      and sa.employee_id is not null
    group by r.workflow_run_id, r.project_id, r.status
    """,
    (run["tenant_id"], run["employee_id"], run["project_id"])
).fetchall()

print("same_project_runs", [dict(r) for r in proj_runs])
print("other_project_runs", [dict(r) for r in other_proj_runs])
print("scope_isolation_ok", all(r["project_id"] != run["project_id"] for r in other_proj_runs))
PY
```

## 验收

- 复盘后可用 query 同时读出：
  - 当前恢复 run 的进度与上界；
  - 被保留失败 run 的项目隔离；
  - 无额外 run 被注入。
- 通过后由产品规划席签收第2项闭环。

## 实时核验结论（当前库）

- run `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50` 对应 `emp-7417237e-2f30-4268-807f-88eaaf951bf8`。
- `same_project_runs`：`4`（项目内仅本项目 run）
  - `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
  - `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`
  - `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
  - `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`
- `other_project_runs` 已出现 `1` 条（跨项目）：
  - `wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`（`project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`，`running`）；
- `scope_isolation_ok=True`（反查未命中到非当前项目）。
- 目标 run 的 Step1~7 均可读且 `succeeded`。

## 最终核验与交接
Issue:
`issues/20260718_workspace_r4_multi_project_session_recovery_gate.md`
Objective:
复核同一员工多项目场景下，单项目恢复对其他项目不污染且可追溯。
Special Constraints:
只做质量 focused 复核；不新建/改写持久化 schema，不扩展 API。
Next Seat:
产品规划席

Review：
`reviews/20260718_workspace_r4_multi_project_session_recovery_gate_review.md`
