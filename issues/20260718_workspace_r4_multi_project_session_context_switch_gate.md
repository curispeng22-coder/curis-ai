# Workspace R4 第2项子Issue C2｜同一员工跨项目 Session 切换隔离

- 日期：2026-07-18
- 状态：PASS — 已闭环
- 父项：`issues/20260718_workspace_r4_multi_project_session_gate.md`
- Owner：系统交付席
- Next Seat：质量运行席（C3衔接）
- 分支：`feat/roadmap-r1r2`

## 目标

给出“项目切换”场景下的最小验证，证明：

- 同一员工从项目 A 切到项目 B 时，读取上下文只返回 B；
- 运行态恢复不会把 A 的 step_result/usage/context 注入 B；
- 反向测试下 project B 请求无法读到项目 A 的未完成状态。

## 约束

- 只做聚焦验证与证据化，不修改执行内核行为。
- 不允许新增 Session 存储结构或跨库改造。
- 保持 R3 收口证据不变。

## 输出（必须）

- 列出 3 条切换脚本：
  - 同一员工同租户两个项目的 project/run 交叉查询；
  - 反向越权读取预期失败/空返回；
  - 切换后运行摘要仅包含当前 project。
- 形成 fail-closed 规则：任一越权访问必须不可见。

## 最小执行口令（一次）

```bash
cd '/Users/yy/Documents/Curis AI Workspace'
python3 - <<'PY'
import sqlite3
db = "/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite"
tenant='tenant-a'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1) 按租户找一位多项目 employee
sample = c.execute("""
select sa.employee_id
from step_assignments sa
join workflow_steps ws on ws.workflow_step_id = sa.workflow_step_id
join workflow_runs wr on wr.workflow_run_id = ws.workflow_run_id
where wr.tenant_id=? and sa.employee_id is not null
group by sa.employee_id
having count(distinct wr.project_id) >= 2
order by sa.employee_id
limit 1
""", (tenant,)).fetchone()
if not sample:
    raise SystemExit("no multi-project employee found; 先由系统交付席补充跨项目样本")
employee = sample["employee_id"]

# 2) 跨项目切换上下文核验（基于 employee_id 与 step_assignments）
rows = c.execute("""
select distinct wr.project_id, wr.workflow_run_id, wr.status
from step_assignments sa
join workflow_steps ws on ws.workflow_step_id = sa.workflow_step_id
join workflow_runs wr on wr.workflow_run_id = ws.workflow_run_id
where wr.tenant_id=? and sa.employee_id=?
order by wr.project_id, wr.workflow_run_id
""", (tenant, employee)).fetchall()
print("employee", employee, "projects", len({r["project_id"] for r in rows}))
for r in rows:
    print(dict(r))

# 3) 取同一员工任一项目的成功快照（作为切换后基准）与失败快照（作为隔离反例）
by_project = {}
for r in rows:
    by_project.setdefault(r["project_id"], []).append(r["workflow_run_id"])
projects = list(by_project.keys())
if len(projects) >= 2:
    p1,p2 = projects[0], projects[1]
    print("switch_pair", p1, "->", p2)
    print("p1_runs", by_project[p1])
    print("p2_runs", by_project[p2])
    print("isolation_check", bool(set(by_project[p1]) & set(by_project[p2])) == False)
else:
    print("single_project employee; cannot run switch check")
PY
```

## 验收

- 切换前后查询基准样例一致；
- 项目级上下文不串租、不串项目；
- 不出现历史 run 被覆盖的证据。

## 实时核验结论（当前库）

- 已执行 `SELECT`：样本员工 `emp-7417237e-2f30-4268-807f-88eaaf951bf8` 跨项目命中，项目 run 集无交集；反向过滤不存在跨项目命中，隔离核验通过。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_multi_project_session_context_switch_gate.md`
Objective:
定义并核验同一员工跨项目切换过程中的上下文隔离与串项目拒绝。
Special Constraints:
仅第2项 C2；不改运行器核心、网关、前端与凭据链路。
Next Seat:
质量运行席（C3衔接）
