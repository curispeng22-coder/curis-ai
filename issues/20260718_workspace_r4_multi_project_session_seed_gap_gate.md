# Workspace R4 第2项子Issue C0｜跨项目样本前置（最低成本）

- 日期：2026-07-18
- 状态：PASS — 已登记
- 父项：`issues/20260718_workspace_r4_multi_project_session_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

补齐“同一 employee 在同一 tenant 下同时存在至少两个 project 的真实样本”，用于 C1/C2 的跨项目 Session 隔离核验。

## 约束

- 不改代码，不改 Gateway，不扩 API 行为；仅补齐可复核样本。
- 不更改已通过历史失败 run 的失败原因，不重跑全量。
- 保持第四轮范围，不并行推进第3~9项。

## 前置条件

- 当前样本链路可复用 `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（employee `emp-7417237e-2f30-4268-807f-88eaaf951bf8`，project `project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`）作为基准。
- 目标是新建/复用同一 employee 的**第二个项目**，不是替换现有 run。

## 最小执行口令（一次）

```bash
cd '/Users/yy/Documents/Curis AI Workspace'

echo "在当前服务可用时，执行以下最小动作："
echo "1) 用既有会话创建一个新项目（同一 tenant-company，project_name 可唯一）"
echo "2) 向该项目创建一个 task"
echo "3) 发起一次工作流实例（use 与已有 run 相同的 template/official 模板可复用）"
echo "4) 运行/暂停后不必完成最终成功；只要 step_assignments 下该 employee 落到第二个 project"
echo "5) 以 C1 脚本核验多项目样本恢复"
```

若服务不可用，可使用质量库只读复核路径临时验证（样本是否存在）：

```bash
backend/.venv/bin/python - <<'PY'
import sqlite3
conn = sqlite3.connect('/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

rows = c.execute("""
select sa.tenant_id, sa.employee_id, count(distinct wr.project_id) as project_count
from step_assignments sa
join workflow_steps ws on ws.workflow_step_id = sa.workflow_step_id
join workflow_runs wr on wr.workflow_run_id = ws.workflow_run_id
where sa.tenant_id='tenant-a'
group by sa.tenant_id, sa.employee_id
having project_count >= 2
order by project_count desc
limit 5
""").fetchall()
print("multi-project candidates:", [dict(r) for r in rows])
PY
```

## 验收

- C1/C2 继续脚本复用后，出现至少一条 `project_count>=2` 的员工样本。
- 样本生成过程不改既有 scope 写入语义与运行契约。

### 当前结果（本 Issue 当前批次）

- multi-project candidates：`2`
- 见证样本：
  - `emp-7417237e-2f30-4268-807f-88eaaf951bf8`
  - `emp-75f8934f-cfb9-4c9f-a759-bdfe942f15db`
- 新项目/新run：`project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd` / `wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`
- `step_assignments` 已出现，C1/C2 前置已满足。
- Review：`reviews/20260718_workspace_r4_multi_project_session_seed_gap_gate_review.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_multi_project_session_seed_gap_gate.md`
Objective:
补齐同一 employee 的跨项目样本，解除 C1/C2 的前置阻塞。
Special Constraints:
不改 C2/C3验收边界定义与验证命令；只做样本前置。
Next Seat:
系统交付席 → 继续 C1/C2
