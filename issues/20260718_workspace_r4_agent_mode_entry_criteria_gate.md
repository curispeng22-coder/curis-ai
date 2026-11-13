# Workspace R4 第3项｜Agent Mode 触发与准入边界 Gate（M1a）

- 日期：2026-07-18
- 状态：OPEN — PARTIAL PASS（基础准入/顺序样本可复核；未命中失败样本）
- 父项：`issues/20260718_workspace_r4_agent_mode_profile_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席（确认边界定义）→ 系统交付席（补齐失败样本策略）→ 质量运行席（若需）
- 分支：`feat/roadmap-r1r2`

## 目标

定义 Agent Mode 的触发前提与准入键，仅基于现有 `tenant_id / project_id / employee_id / workflow_run_id / step_order` 推断，不改现网数据结构。

## Must Do

1. 定义 Agent Mode 进入条件（最小口径）：
   - run 属于有效 `tenant + project + employee`
   - 当前 step 在有效范围内且角色匹配
   - 绑定能力满足（可复核）
2. 明确未满足条件时的 fail-closed 行为（拒绝执行并记录原因）。
3. 给出 1 条最小核验命令（只读），验证同一 run/employee 的 step 与项目归属可读一致。

## 执行口令（系统交付席）

- 只读核验：选一条可复核 run（例如当前成功 run 与其前后一个 run）输出：
  - run 的 `tenant_id/project_id/employee_id` 与 session 归属一致性；
  - `step_order` 序列是否不越界；
  - 该 run 的每一步 `employee_id` 与该 run 主体一致；
  - 是否可从现有字段定位其绑定能力（`capability binding`）；
  - 任一不满足项必须归类为 `拒绝原因`（非静默放行）。
- 交付物：执行口径 + 抽样结论，写入该 Issue 的 Review 片段。

执行 SQL（只读）示例（`workspace.sqlite`）：

```sql
-- 1) 挑 2 条 run（成功+边界）
select workflow_run_id, tenant_id, company_id, project_id, department_id, task_id, status
from workflow_runs
where tenant_id='tenant-a'
order by updated_at desc
limit 3;

-- 2) 对齐 step 顺序、员工归属、能力绑定
select ws.workflow_run_id, ws.workflow_step_id, ws.step_order, ws.employee_role, ws.status as step_status,
       sa.employee_id, sa.capability_binding_id, sa.status as assignment_status,
       sr.step_result_id, sr.status as result_status
from workflow_steps ws
left join step_assignments sa
  on sa.workflow_step_id = ws.workflow_step_id and sa.tenant_id = ws.tenant_id
left join step_results sr
  on sr.workflow_step_id = ws.workflow_step_id and sr.tenant_id = ws.tenant_id
where ws.workflow_run_id = '待检 run_id'
order by ws.step_order;

-- 2b) Step Order 约束（1..7 且无重复）
select workflow_run_id,
       min(step_order) as min_step_order,
       max(step_order) as max_step_order,
       count(*) as row_count,
       count(distinct step_order) as distinct_step_count
from workflow_steps
where workflow_run_id = '待检 run_id'
having min_step_order < 1 or max_step_order > 7 or row_count != distinct_step_count;

-- 3) 失败场景拒绝原因是否落库
select event_id, event_type, payload
from evolution_events
where tenant_id = 'tenant-a'
  and event_type like 'workflow.%'
  and correlation_id = '待检 task_id'
order by event_id desc;
```

只要发现任一 run/step 未满足 `tenant/project/employee/step_order/绑定`，不得出现“成功继续推进”证据；必须归类为显式拒绝场景，并给出定位字段。当前 run 无失败样本，需在后续 run 中补齐。

## 约束

- 不新增字段，不新增接口，不改执行器。
- 不新增 mock/stub。

## Compact Handoff:
Issue:
`issues/20260718_workspace_r4_agent_mode_entry_criteria_gate.md`
Objective:
固定 Agent Mode 的最小触发条件与失败拒绝边界。
Special Constraints:
仅边界定义；不得改运行逻辑、模型网关、前端或 schema。
Next Seat:
系统交付席 → 产品规划席
