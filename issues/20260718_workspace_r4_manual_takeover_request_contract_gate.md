# Workspace R4 第5项｜5b｜人工接管入口与动作边界 Gate

- 日期：2026-07-18
- 状态：PASS — CLOSED（人工接管边界定义收口）
- 前置：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- 父项：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 结论

5b 为“人工接管只读决策口径”闭环：系统不会提供 cancel/reopen 接口，也不允许回改历史 run。人工接管的唯一合法动作是“确认后创建新 run 并重跑新链路”，旧 run 仅保留证据。

## 人工接管入口

仅当满足下列全部条件时，可启动接管前置核验：

1. `workflow_runs.status = failed` 且存在 `workflow_steps.status = failed` 的失败步；
2. 接管目标对象明确到 `workflow_run_id`；
3. 读取到失败步 `step_order`、`error`、`failed_at`、`updated_at`，并计算 `recover_age_sec`；
4. `recover_age_sec` 在决策窗口内（建议参考 4c 的 `recover_window_sec=900`）；
5. `run` 与 `step` 的 tenant/company/project/binding 前提无变化（防止错目标）；
6. 决策流程由负责人签字确认。

不满足上述条件则不可进入 5b 接管预检，需按 5c 升级（Escalate）或直接 Hold。

## 接管动作边界

- 允许动作（唯一动作）：创建新 run，继承既有约束：
  - tenant、project、workflow、department、scope 继承；
  - 受控模型/网关/Token 上限保持不变；
  - 不改历史失败 run。
- 禁止动作：
  - 回写 `workflow_runs`/`workflow_steps`/`step_results`/`usage_events`/`evolution_events` 的历史状态；
  - 不改 `final_report`、`status`、`completed_at`、`failed_at`；
  - 不做 step 跳过、状态补齐、历史重放。

## 不可逆字段保护（只读锁）

- 运行级锁：`workflow_runs.status/final_report/failed_at/completed_at/updated_at`
- 步骤级锁：`workflow_steps.error/status/started_at/completed_at`
- 结果级锁：`step_results.step_result_id/result/status`
- 用量与账务级锁：`usage_events`、`result_cost`、`result_token_count`
- 事件级锁：`evolution_events` 的失败/停机事件

## 决策模板（执行记录外部保存）

- `Stop`：终态已停/不可变更；
- `Hold`：需要人工确认、非自动恢复；
- `Escalate`：转 5c 风险上报；
- `Create-New-Run`：确认且通过门限后新增 run。

每次人工接管决策必须具备 `tenant/run_id/step_order/decision/approver/timestamp`，不允许空白确认。

## one-shot 复核 SQL（只读）

```sql
-- 5b预检：取目标 run 的接管前置和决策起点
SELECT wr.workflow_run_id, wr.tenant_id, wr.project_id, wr.department_id,
       wr.workflow_template_id, wr.task_id, wr.status, wr.failed_at, wr.completed_at,
       ws.workflow_step_id, ws.step_order, ws.employee_role, ws.error, ws.updated_at AS step_updated_at,
       (julianday('now') - julianday(wr.failed_at)) * 86400 AS recover_age_sec
FROM workflow_runs wr
LEFT JOIN workflow_steps ws
       ON ws.workflow_run_id = wr.workflow_run_id
      AND ws.status = 'failed'
WHERE wr.workflow_run_id = :workflow_run_id
  AND wr.tenant_id = :tenant_id;
```

```sql
-- 5b决策一致性：确认不得回改历史
SELECT 'workflow_runs' AS entity, count(*) AS locked_rows
FROM workflow_runs
WHERE workflow_run_id = :workflow_run_id
UNION ALL
SELECT 'workflow_steps', count(*)
FROM workflow_steps
WHERE workflow_run_id = :workflow_run_id
UNION ALL
SELECT 'step_results', count(*)
FROM step_results sr
JOIN workflow_steps ws ON ws.workflow_step_id = sr.workflow_step_id
WHERE ws.workflow_run_id = :workflow_run_id
UNION ALL
SELECT 'usage_events', count(*)
FROM usage_events ue
JOIN workflow_steps ws ON ws.workflow_step_id = ue.workflow_step_id
WHERE ws.workflow_run_id = :workflow_run_id;
```

## 复核证据（静态）

- `backend/app/main.py` 仅暴露：
  - `POST /api/workspace/workflows/{workflow_run_id}/run-next-step`
  - `GET  /api/workspace/workflows/{workflow_run_id}`
  - `POST /api/workspace/workflows`（用于新 run）
  - 未提供原 run reset/cancel/reopen 接口。
- `backend/app/workflow_runtime.py` 运行器：失败后改写为终态失败、不可回转继续；无历史重写分支。

## 下一步

- 5b 交接 5c，确认风险升级口径后，返回主项统一模板闭环。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_manual_takeover_request_contract_gate.md`
Objective:
定义 5b 人工接管入口、确认条件与新 run 动作边界。
Special Constraints:
只定义边界与复核模板；不实现，不改历史，不发起实际重跑。
Next Seat:
产品规划席
