# Workspace R4 第3项｜Workflow Mode 顺序与冲突契约 Gate（M2b）

- 日期：2026-07-18
- 状态：OPEN — PASS（样本顺序/冲突可复核，失败链路由 M2a 覆盖）
- 父项：`issues/20260718_workspace_r4_workflow_mode_profile_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（补齐 M2a 后进入下一链路）
- 分支：`feat/roadmap-r1r2`

## 目标

给出 Workflow Mode 与既有 `run-next-step` 的顺序契约：固定顺序如何判定、冲突如何拒绝、失败如何中止。

## 必须定义

1. Step 顺序契约（固定顺序、不得跳步）
2. 模式互斥契约（Agent/Hybrid 无法同时占用同一 step）
3. 出错即停契约（失败后不得继续执行后续 step）
4. 指标映射：run/step/result/execution 之间拒绝场景的可追踪对应关系

## 最小复核（只读）

- 抽样核验历史 `workflow_runs` 与 `workflow_steps` 中 StepResult 与执行顺序对齐

## 执行口令（系统交付席）

- 抽取一条跨模式边界 run：
  - mode 定义与 `step_order` 是否可一一映射；
  - 失败 step 后后续 step 是否被明确阻断（无成功 continuation）；
  - run/step/result 之间是否可追溯到单一顺序契约结论。
- 产物：顺序表 + 冲突表（若存在）+ 结论。

执行 SQL（只读）示例（`workspace.db`）：

```sql
-- 1) 取 run-level 事实（状态、tenant/project/department）
select wr.workflow_run_id, wr.tenant_id, wr.company_id, wr.project_id, wr.department_id, wr.status
from workflow_runs wr
where wr.workflow_run_id = '待检 run_id';

-- 2) 顺序 + assignment + result 三链是否齐全且同序
select ws.workflow_run_id, ws.workflow_step_id, ws.step_order, ws.employee_role, ws.status as step_status,
       sa.employee_id, sa.capability_binding_id,
       sr.status as result_status, sr.step_result_id
from workflow_steps ws
left join step_assignments sa
  on sa.workflow_step_id = ws.workflow_step_id and sa.tenant_id = ws.tenant_id
left join step_results sr
  on sr.workflow_step_id = ws.workflow_step_id and sr.tenant_id = ws.tenant_id
where ws.workflow_run_id = '待检 run_id'
order by ws.step_order;

-- 2b) 验证顺序是否有跳步（step_order 应为前一个 + 1）
select step_order, prev_step_order
from (
  select ws.step_order,
         lag(ws.step_order) over (order by ws.step_order) as prev_step_order
  from workflow_steps ws
  where ws.workflow_run_id = '待检 run_id'
)
where prev_step_order is not null and step_order != prev_step_order + 1;

-- 3) 验证失败后不得继续推进
select prev.step_order as failed_step_order,
       nxt.step_order as violated_step_order,
       prev.status as failed_status,
       nxt.status as violated_status
from workflow_steps prev
join workflow_steps nxt
  on nxt.workflow_run_id = prev.workflow_run_id
 and nxt.tenant_id = prev.tenant_id
 and nxt.step_order > prev.step_order
where prev.workflow_run_id = '待检 run_id'
  and prev.status = 'failed'
  and nxt.status in ('running', 'succeeded', 'completed')
order by prev.step_order, nxt.step_order;

-- 4) 验证冲突：同一 step 是否出现重复结果/重复分配/多角色归属（Agent 与 Hybrid 冲突）
select ws.workflow_step_id,
       count(sa.step_assignment_id) as assignment_count,
       count(sr.step_result_id) as result_count,
       count(distinct sa.employee_role) as role_count
from workflow_steps ws
left join step_assignments sa on sa.workflow_step_id = ws.workflow_step_id and sa.tenant_id = ws.tenant_id
left join step_results sr on sr.workflow_step_id = ws.workflow_step_id and sr.tenant_id = ws.tenant_id
where ws.workflow_run_id = '待检 run_id'
group by ws.workflow_step_id
having assignment_count > 1 or result_count > 1 or role_count > 1;
```

如有重复分配/重复结果，必须归为 mode/顺序冲突并给出停摆证据。

## 约束

- 不改数据库 schema，不改运行器代码，不发起真实模型调用
- 不改前端、不新增服务、不保存 mock/stub
- 仅定义与可复核核验，不实施

## 当前抽样状态

- 已复核样本更新为 `wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`（运行）与失败链路 `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` / `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`；
- 样本链条支持顺序与冲突基础约束，且失败步后未出现跳步继续；
- 失败场景与显式拒绝链路来自 `reviews/20260718_workspace_r4_workflow_mode_entry_guard_gate_review.md` 复核补齐。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_workflow_mode_sequence_contract_gate.md`
Objective:
确认 Workflow Mode 的顺序与冲突不变式为 fail-closed 可复核契约。
Special Constraints:
仅边界定义；不得改动当前实现，不得新增调用链，不得跨出本项范围。
Next Seat:
产品规划席（确认定义）→ 系统交付席（确认口径）→ 质量运行席（focused 复核）
