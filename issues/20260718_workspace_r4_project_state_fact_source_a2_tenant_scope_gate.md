# Workspace R4 第1项子Issue A2｜跨租户与可见域边界

- 日期：2026-07-18
- 状态：PASS — 已复核闭环并对齐 A3
- 父项：`issues/20260718_workspace_r4_project_state_fact_source_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席（A3联合）
- 分支：`feat/roadmap-r1r2`

## 目标

把项目状态事实查询的可见域边界固化成最小可验规则：
`tenant_id + project_id + run_id` 三要素约束。

## 可见域规则（当前实现）

### 1）请求入口与上下文

- 所有 Workspace API 请求先经过 Tenant Scope Middleware：
  - 读取 `X-Tenant-Id`（缺失时走默认租户）；
  - 入 `TenantContext` 后执行后续处理。
- 所有已知 Workspace 读库 SQL 使用 `tenant_id` 作为第一过滤条件。

### 2）run/task/step/result/usage 能力边界

- `GET /api/workspace/workflows/{run_id}` 读取链：
  1. 路由先由 `resource_scope_policy.path_is_owned(".../workflows/{run_id}")` 判定该 `run_id` 属于当前 tenant；
  2. 进入 `workflow_runtime.get_run(run_id)` 后再次按 `tenant_id + workflow_run_id` 查询。
- `workflow_steps`：按 `tenant_id + workflow_run_id` 查询。
- `step_results`：按 `tenant_id + workflow_step_id in (...)` 查询（`workflow_step_id` 来自同 run）。
- `executions`：按 `tenant_id + task_id` 查询。
- `usage`：按 `tenant_id + correlation_id == task_id + event_type='usage.model_call'` 查询。
- `project_row`：按 `tenant_id + project_id` 查询。

### 3）最小约束读取建议（项目长期状态场景）

- 读取任一项目长期状态时，建议同时带：
  - `tenant_id`（`X-Tenant-Id`）
  - `project_id`
  - `workflow_run_id`
- 首先校验 `workflow_runs`，再校验 `run.project_id == project_id`。

### 4）越权返回策略

- 越权 run（run 不在该 tenant）或 run_id 不存在：统一返回 `404`（`resource not found`）。
- 跨项目/project_id 校验失败：返回 `404`（读链不成立，避免枚举）。
- 未通过路径归属检查：返回 `404`（而不是 403），实现 fail-closed。

## Fail-closed 用例（至少两条）

1. **跨租户越权**
   - 请求：`GET /api/workspace/workflows/wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
   - 首部：`X-Tenant-Id: tenant-b`
   - 预期：`404 resource not found`
2. **项目不一致越权（建议项目级聚合）**
   - 在同 tenant 下读取时，如果附带 `project_id` 与 run 的 `project_id` 不一致（仅针对 A2 约定的项目状态查询流程）
   - 预期：视为无权/非法上下文，`404`（不返回 partial 项目信息）

## 最小查询示例（只读）

- API（当前已实现）
  - `GET /api/workspace/workflows/{workflow_run_id}`（仅支持同一 tenant）
- SQL（最小闭环）
```sql
-- 1) 在 tenant+project 上限约束下拿到 run
select workflow_run_id, tenant_id, project_id, status, task_id, updated_at
from workflow_runs
where tenant_id = :tenant_id
  and project_id = :project_id
  and workflow_run_id = :workflow_run_id;

-- 2) 取 step/result/usage
select * from workflow_steps where tenant_id=:tenant_id and workflow_run_id=:workflow_run_id order by step_order;
select * from step_results where tenant_id=:tenant_id and workflow_step_id in (
  select workflow_step_id from workflow_steps where tenant_id=:tenant_id and workflow_run_id=:workflow_run_id
);
select event_id, payload from evolution_events
 where tenant_id=:tenant_id
   and correlation_id=:task_id
   and event_type='usage.model_call'
 order by event_id;
```
- 审计读取（静态）
  - `project_id`、`tenant_id` 与 `workflow_run_id` 必须在日志上下文中三元组出现；失败上下文不回写历史记录。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_project_state_fact_source_a2_tenant_scope_gate.md`
Objective:
定义项目状态读链的 tenant/project/run 可见域边界与 fail-closed 行为。
Special Constraints:
只定义可见域规则，不改 auth/RBAC，不新增 API，不改模型调用。
Next Seat:
系统交付席

## 复核结果（A3 同步）

- 已与 A3 对齐：`tenant-a + project_id + run_id` 三元组可定位到单条 run，跨租户请求与缺省 tenant 请求均为 `404` fail-closed。
