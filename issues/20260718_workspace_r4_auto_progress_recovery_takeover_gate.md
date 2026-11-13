# Workspace R4 第4项｜第4c｜恢复与人工接管边界 Gate

- 日期：2026-07-18
- 状态：PASS — CLOSED（无新字段下恢复口径闭环）
- 前置：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- 父项：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

给出“失败后是否可恢复/人工接管”最小边界：只允许在无跨租户污染、且历史不可逆字段不改前提下定义恢复决策。

## 约束

1. 不改历史数据。
2. 不改历史失败 run 状态。
3. 不改 DB Schema。
4. 不改前端，不改凭据，不改出网。

## Must Do（结论）

- 恢复决策分类：
  - `recoverable=true`：仅用于失败 run 的可读判定，不进行续推。
  - `recoverable=false`：明确建议新建 run。
- 人工接管定义：
  - 仅可在 owner/负责人确认下，读取 `run` 事实后决定创建新 run。
  - 不允许自动覆盖、补状态字段。
- 不可逆字段保护：`workflow_runs.status`、`workflow_steps.error`、`step_results`、`usage`、`evolution_events` 不得在恢复演练中改写。
- 与 B2/B3 保持一致：不可直接续推 failed run；保留历史。
- 给出不出网恢复演练脚本与输出模板（输入/决策/输出/边界）：

```sql
-- 运行级恢复判定（只读）
WITH failed_step AS (
  SELECT ws.workflow_run_id,
         ws.workflow_step_id,
         ws.step_order,
         ws.status AS step_status,
         COALESCE(NULLIF(ws.error, ''), 'NO_ERROR_TEXT') AS step_error
  FROM workflow_steps ws
  JOIN workflow_runs wr ON wr.workflow_run_id = ws.workflow_run_id
  WHERE wr.workflow_run_id = :run_id
    AND wr.tenant_id = :tenant_id
    AND ws.status = 'failed'
  ORDER BY ws.step_order
  LIMIT 1
),
target AS (
  SELECT wr.workflow_run_id, wr.status, wr.failed_at,
         (julianday('now') - julianday(wr.failed_at)) * 86400 AS failed_since_sec,
         fs.step_order, fs.step_error
  FROM workflow_runs wr
  LEFT JOIN failed_step fs ON fs.workflow_run_id = wr.workflow_run_id
  WHERE wr.workflow_run_id = :run_id AND wr.tenant_id = :tenant_id
)
SELECT
  workflow_run_id,
  status,
  failed_at,
  failed_since_sec,
  step_order,
  step_error,
  CASE
    WHEN status='failed'
         AND failed_at IS NOT NULL
         AND failed_since_sec <= 900
         AND (step_error LIKE '%rate limited%'
              OR step_error LIKE '%network%'
              OR step_error LIKE '%gateway%' )
         AND NOT (step_error LIKE '%project%' OR step_error LIKE '%tenant%' OR step_error LIKE '%binding%' OR step_error LIKE '%scope%')
    THEN 1
    ELSE 0
  END AS recoverable
FROM target;
```

### 结论模板（只读返回）
- `recoverable=1`：仅进入人工复核清单（owner 二次确认）；
- `recoverable=0`：直接建议新建 run；历史失败不可变更、不得重放。
- 任何时刻不得改写历史字段、不得在恢复流程里发起历史重跑或回灌。

## 参考复核样本（只读）

- `tenant-a / project-e84e06d4-f014-4326-abcd-e6d9aea6ff95 / wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- `task_id = 285e3bb5-3fd5-4bd9-9eff-4cbd53e11d7b`

## 交付

- 输出：恢复/人工接管最小判定表，覆盖失败 run 的 stop / no-auto / create-new-run。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_auto_progress_recovery_takeover_gate.md`
Objective:
定义失败 run 的恢复可行性、人工接管入口和不可逆字段保护。
Special Constraints:
不改实现；不改历史；不发起真实模型调用。
Next Seat:
产品规划席
