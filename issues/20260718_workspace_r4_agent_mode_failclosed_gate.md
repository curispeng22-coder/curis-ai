# Workspace R4 第3项｜Agent Mode 失效/拒绝边界 Gate（M1b）

- 日期：2026-07-18
- 状态：OPEN — PARTIAL（核心拒绝闭环已出；待补失配/绑定缺失反例样本）
- 父项：`issues/20260718_workspace_r4_agent_mode_profile_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

在现有事实模型不改动前提下，给出 Agent Mode 下的 fail-closed 规则与禁止行为清单，确保当条件不足时不进入隐式降级，而是明确失败。

## 必须定义

1. 作用域失配失败（tenant/project/employee 不一致）
2. 角色/绑定缺失失败（缺 `binding`、缺 `capability`/`model` 绑定）
3. 会话离散失败（session 跨项目复用、run 复用旧上下文）
4. 运行态失败（token 过期、X-Ceo-Id/subject 缺失、授权链断裂）

## 最小复核（只读）

- 只查 `workflow_runs`、`workflow_steps`、`evolution_events` 的既有事实链，确认失败场景返回为明确拒绝而非变成可执行退化

## 执行口令（系统交付席）

- 只读抽样 3 类失败场景（tenant/project/employee、binding 缺失、session/step 越权），给出：
  - 触发条件命中项；
  - 是否出现 run 继续推进的痕迹；
  - 失败字段是否可还原为“显式拒绝”；
  - 若命中非拒绝，明确不通过原因（不得通过）。
- 要求：同 run/同 employee 不得存在“模式判断失败但 step 继续推进”记录。

执行 SQL（只读）示例（`workspace.db`）：

```sql
-- A. 作用域失配/越权样本（先挑有失败历史的 run）
select wr.workflow_run_id, wr.tenant_id, wr.company_id, wr.project_id,
       ws.workflow_step_id, ws.step_order, ws.status as step_status,
       sa.employee_id, sa.capability_binding_id
from workflow_runs wr
join workflow_steps ws on ws.workflow_run_id = wr.workflow_run_id and ws.tenant_id = wr.tenant_id
left join step_assignments sa on sa.workflow_step_id = ws.workflow_step_id and sa.tenant_id = ws.tenant_id
where wr.tenant_id='tenant-a'
  and (wr.project_id is null or ws.status in ('failed','running'))
order by wr.updated_at desc
limit 80;

-- B. 运行态失败后是否阻断（含 token/subject 相关失败可见性：靠 evolution_events reason）
select e.event_id, e.event_type, e.payload
from evolution_events e
where e.tenant_id='tenant-a'
  and e.event_type in ('workflow.step.failed', 'workflow.run.failed')
order by e.event_id desc
limit 120;

-- C. 绑定缺失与越步：step 无 assignment 或 status 跳步传播
select prev.workflow_run_id, prev.step_order as prev_order, prev.status as prev_status,
       nxt.step_order as next_order, nxt.status as next_status
from workflow_steps prev
join workflow_steps nxt
  on nxt.workflow_run_id = prev.workflow_run_id
 and nxt.tenant_id = prev.tenant_id
 and nxt.step_order = prev.step_order + 1
left join step_assignments sa_prev on sa_prev.workflow_step_id = prev.workflow_step_id and sa_prev.tenant_id = prev.tenant_id
where prev.tenant_id='tenant-a'
  and (sa_prev.step_assignment_id is null or prev.status = 'failed')
  and nxt.status in ('running', 'succeeded');
```

有一项命中时，`evolution_events` 必须能给出显式拒绝字段/原因；若缺失则判失败。

## 当前复核状态（2026-07-18）

- Review：`reviews/20260718_workspace_r4_agent_mode_failclosed_gate_review.md`
- 结论：`PARTIAL`。已完成 3 条失败原因、失败后禁止续跑样本；尚未覆盖 tenant/project/employee 失配与 binding 缺失直接失败反例。

## 约束

- 不改数据库、不改执行器、不改网关、不改 API
- 不改现网 front-end，不发起模型调用，不新增 mock/stub
- 仅定义项，不实现

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_agent_mode_failclosed_gate.md`
Objective:
固化 Agent Mode 的失败拒绝边界与 fail-closed 规则。
Special Constraints:
仅做边界定义与可复核口径；不改实现，不改现网数据结构，不调用模型。
Next Seat:
产品规划席（确认定义）→ 系统交付席（确认落地）→ 质量运行席（focused 复核）
