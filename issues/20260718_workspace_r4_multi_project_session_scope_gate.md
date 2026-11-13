# Workspace R4 第2项子Issue C1｜同一员工多项目 Session Scope 与 Key 规范

- 日期：2026-07-18
- 状态：PASS — 已闭环
- 父项：`issues/20260718_workspace_r4_multi_project_session_gate.md`
- Owner：系统交付席
- Next Seat：质量运行席（C2联动）
- 分支：`feat/roadmap-r1r2`

## 目标

定义 `employee + tenant + project` 场景下 Session scope 与 key 的最小事实边界，保证：

- 同一员工不同项目之间 key 不冲突；
- Session 快照可按 project 定位；
- key 冲突、缺失 project scope、非法 scope 统一 fail-closed。

## 约束

- 只写入边界配置/映射文档与只读核验 SQL。
- 不改模型调用、不改 workflow execution 行为。
- 不新增 API 路径，仅复用现有读取/查询路径进行最小验证。

## 输出（必须）

- Scope 字典（最小）：`tenant_id`、`employee_id`、`project_id`、`scope`（与第1项 memory 的 `owner` 兼容）。
- Key 规范（推荐）：`session_scope:{tenant_id}:{employee_id}:{project_id}:{scope}`，并补充 `scope` 取值白名单。
- fail-closed 规则：不带 project 维度时必须拒绝或报错，不可回退到默认工程。

## 实时核验结论（当前库）

- 已执行 `SELECT`：`multi-project candidates: 2`，已发现样本 `emp-7417237e-2f30-4268-807f-88eaaf951bf8` 覆盖 2 个项目；同一 employee 的
- `session_scope:{tenant_id}:{employee_id}:{project_id}:{scope}` 在 owner/execution/context 下无 key 冲突，`workflow_runs.project_id IS NULL` 命中 0。
- 复核文档：`reviews/20260718_workspace_r4_multi_project_session_scope_gate_review.md`

## 最小执行口令（一次）

```bash
cd '/Users/yy/Documents/Curis AI Workspace'
DB='deploy/curis/gateway/.generated/data/quality.sqlite'
backend/.venv/bin/python - <<'PY'
import sqlite3
conn = sqlite3.connect("/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite")
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1) 找到有多项目的同一员工（以 step_assignments→workflow_runs 追踪）
rows = c.execute("""
select sa.tenant_id, sa.employee_id, count(distinct wr.project_id) as c
from step_assignments sa
join workflow_steps ws on ws.workflow_step_id = sa.workflow_step_id
join workflow_runs wr on wr.workflow_run_id = ws.workflow_run_id
where sa.tenant_id='tenant-a'
  and sa.employee_id is not null
group by sa.tenant_id, sa.employee_id
having c>=2
order by c desc, sa.employee_id
limit 1
""").fetchall()
print("multi-project candidates:", len(rows))
for r in rows:
    print(dict(r))

if not rows:
    raise SystemExit("no multi-project sample in fixture; 需先由系统交付席补充跨项目样本")
tenant_id = rows[0]["tenant_id"]; employee_id = rows[0]["employee_id"]

# 2) 按项目列出 run，验证 key 生成不冲突
project_rows = c.execute("""
select distinct wr.tenant_id, wr.project_id
from step_assignments sa
join workflow_steps ws on ws.workflow_step_id = sa.workflow_step_id
join workflow_runs wr on wr.workflow_run_id = ws.workflow_run_id
where sa.tenant_id=? and sa.employee_id=?
""", (tenant_id, employee_id)).fetchall()

def mk(tenant_id, employee_id, project_id, scope):
    return f"session_scope:{tenant_id}:{employee_id}:{project_id}:{scope}"

keys = []
for prj in project_rows:
    keys.append(mk(tenant_id, employee_id, prj["project_id"], "owner"))
    keys.append(mk(tenant_id, employee_id, prj["project_id"], "execution"))
print("projects", len(project_rows), [dict(r) for r in project_rows])
print("keys", keys)
print("unique", len(set(keys)) == len(keys))
PY
```

## 验收

- 基于已有失败/成功样例数据可复现地给出 3 类检查：
  - key 冲突检出；
  - project 缺失拒绝；
  - 同一 employee 跨项目读取隔离通过。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_multi_project_session_scope_gate.md`
Objective:
固化 C1 scope/key 最小规范与冲突拒绝规则。
Special Constraints:
仅第四轮第2项 C1；不得改 `projects` 写入链路，不扩展 API，不发起模型/工具调用。
Next Seat:
质量运行席（C2联动）
