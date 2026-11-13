# Workspace R4 第3项｜Workflow Mode 入口守卫 Gate（M2a）

- 日期：2026-07-18
- 状态：OPEN — PASS（顺序守卫与失败阻断可复核；越权/越步反例未命中）
- 父项：`issues/20260718_workspace_r4_workflow_mode_profile_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

给出 Workflow Mode 的最小入口守卫定义：何时判定 run 已进入 Workflow Mode，何时必须拒绝。

## 必须定义

1. 入口判定：run/step 是否处于既定顺序执行链内
2. tenant-project-employee 三元守卫
3. 与 Agent / Hybrid 的优先级冲突规则（只命中一个主模式）
4. 非标准入口（越权、越步、越期）直接拒绝，无隐式重写

## 最小复核（只读）

- 仅通过既有 run/step 历史，抽样核验 `run-next-step` 阶段顺序是否有“越步被拒”可复核证据

## 执行口令（系统交付席）

- 只读核验同 tenant 内 2 条 run：
  - Step 1/2/… 的 `step_order` 是否仅按既定序列前进；
  - 是否存在越权 step（跨 tenant/project/employee 或非预期 step）；
  - 任何拒绝场景是否形成“明细错误码/原因”，而非静默放行。
- 产物：抽样 run 表与 step 表对账结论（附 run_id、step_id）。

执行 SQL（只读）示例（`workspace.db`）：

```sql
-- 1) 选两条 run：一条成功/进行中 + 一条失败
select workflow_run_id, tenant_id, project_id, department_id, status
from workflow_runs
where tenant_id='tenant-a'
order by updated_at desc
limit 3;

-- 2) 检查 run 内 step 顺序与越步
select ws.workflow_run_id, ws.workflow_step_id, ws.step_order, ws.employee_role, ws.status
from workflow_steps ws
where ws.workflow_run_id = '待检 run_id'
order by ws.step_order;

-- 3) 若出现失败步，确认后继是否被阻断
select prev.step_order as fail_step, prev.status as fail_status,
       nxt.step_order as next_step, nxt.status as next_status
from workflow_steps prev
join workflow_steps nxt
  on nxt.workflow_run_id = prev.workflow_run_id
 and nxt.tenant_id = prev.tenant_id
 and nxt.step_order = prev.step_order + 1
where prev.tenant_id='tenant-a' and prev.status='failed'
order by prev.workflow_step_id;

-- 4) 关键拒绝/错误记录
select event_type, payload
from evolution_events
where tenant_id='tenant-a'
  and event_type like 'workflow.%'
  and correlation_id in (select task_id from workflow_runs where workflow_run_id='待检 run_id')
order by event_id desc
limit 50;
```

## 约束

- 不改执行器循环，不加 API，不加字段
- 不改现网 front-end，不做真实模型调用，不新增任何外部依赖
- 仅定义与复核口径，不实现

## 最新复核结果

- Review：`reviews/20260718_workspace_r4_workflow_mode_entry_guard_gate_review.md`
- 结论（当前）：`PASS`。已抽样运行 run 与失败 run 复核顺序守卫及失败后停摆；未见越权越步反例。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_workflow_mode_entry_guard_gate.md`
Objective:
固化 Workflow Mode 的入口判断与入口失败处理边界。
Special Constraints:
只做边界定义与复核，不改行为/数据库/网关/凭据。
Next Seat:
产品规划席（确认定义）→ 系统交付席（对齐口径）→ 质量运行席（focused 复核）
