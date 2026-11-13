# Workspace R4 第5项｜5c｜风险升级与人工确认标准 Gate

- 日期：2026-07-18
- 状态：PASS — CLOSED（风险升级口径收口）
- 前置：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- 父项：`issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 结论

5c 以“错误语义 + 复用历史证据 + 决策可追溯”定义风险升级。只要命中不可恢复类/跨域类失败，即使有重试意愿也不允许自动化续推，必须先 escalate 并由负责人确认。

## Stop / Escalate 分层

- `Stop`：状态已终态（succeeded/failed/cancelled）且已出现 `workflow.run.failed`/`workflow.step.failed` 证据，等待人工复核，不再发起步骤。
- `Hold`：可观察窗口内的瞬时外部异常（如网络抖动）进入短时等待，不触发新 run。
- `Escalate`：命中下列任意一类即转人工风控：
  - 安全与鉴权：`X-Ceo-Id` 缺失、绑定链路失败、凭据/权限异常、tenant/project/department/company 关键字段不一致。
  - 范围/角色失配：`employee_role`/binding 与 run scope 不一致、scope 外步进、重复绑定、历史快照冲突。
  - 配置性系统性失败：`input exceeds the approved limit`、`approved token/price/cost cap` 等重复出现的失败类。
  - 重复失败：同 tenant+project+run 方案在短窗口内多次失败（含同一失败原因）。
- `Create-New-Run`：`Escalate` 处理完毕并确认修复后由人工在原规则下重新创建新 run；不得自动回改旧 run。

## 风险归档字段（最小审计）

建议复核时保留：
`tenant_id`、`workflow_run_id`、`step_order`、`workflow_step_id`、`reason`、`event_type`、`created_at`、`approver`、`action_taken`。

## one-shot 复核 SQL（只读）

```sql
-- 5c 失败原因分类与等级
WITH failed_steps AS (
  SELECT wr.workflow_run_id, wr.tenant_id, wr.project_id, wr.department_id,
         ws.workflow_step_id, ws.step_order, ws.employee_role, ws.error,
         ws.updated_at AS step_updated_at,
         ee.event_type AS evt_type,
         COALESCE(json_extract(ee.payload,'$.reason'), ws.error) AS reason
  FROM workflow_runs wr
  JOIN workflow_steps ws ON ws.workflow_run_id = wr.workflow_run_id
  LEFT JOIN evolution_events ee
         ON ee.event_type IN ('workflow.step.failed','workflow.run.failed')
        AND json_extract(ee.payload,'$.workflow_run_id') = wr.workflow_run_id
  WHERE wr.status = 'failed'
    AND ws.status = 'failed'
    AND wr.tenant_id = :tenant_id
)
SELECT workflow_run_id, tenant_id, project_id, department_id, step_order, employee_role,
       reason,
       CASE
         WHEN lower(reason) LIKE '%x-ceo-id%' OR lower(reason) LIKE '%binding%' OR lower(reason) LIKE '%tenant%' OR lower(reason) LIKE '%project%' OR lower(reason) LIKE '%company%' OR lower(reason) LIKE '%scope%' THEN 'ESCALATE'
         WHEN lower(reason) LIKE '%input exceeds the approved limit%' OR lower(reason) LIKE '%approved limit%' THEN 'ESCALATE'
         WHEN lower(reason) LIKE '%temporary failure in name resolution%' OR lower(reason) LIKE '%time%' OR lower(reason) LIKE '%timeout%' THEN 'HOLD'
         ELSE 'ESCALATE'
       END AS action_hint
FROM failed_steps
ORDER BY workflow_run_id;
```

```sql
-- 5c 重复失败检测（同 run 级 + 同 step 级）
SELECT :tenant_id AS tenant_id,
       json_extract(payload, '$.workflow_run_id') AS workflow_run_id,
       json_extract(payload, '$.workflow_step_id') AS workflow_step_id,
       json_extract(payload, '$.reason') AS reason,
       count(*) AS repeat_count
FROM evolution_events
WHERE event_type = 'workflow.step.failed'
  AND json_extract(payload,'$.tenant_id') = :tenant_id
GROUP BY workflow_run_id, workflow_step_id, reason
HAVING repeat_count >= 2
ORDER BY repeat_count DESC;
```

## 复核结论（本 Issue）

基于当前历史失败样本，已命中 5c Escalate 的代表场景：  
- 绑定/鉴权链路缺失（`X-Ceo-Id is required to write UsageEvent`）  
- 输入边界类失败（`Model gateway input exceeds the approved limit`）  
- 出网 DNS 临时异常（`Model gateway request failed: <urlopen error ...>`）先按 Hold 处理

以上口径用于 5a/5b 的决策联动：若当前失败 run 直接命中 Escalate，禁止创建/重跑；先人工确认后再进入新 run 流程。

## 下一步

- 将 5b/5a/5c 统一汇总到 `issues/20260718_workspace_r4_manual_takeover_stop_risk_escalation_gate.md`。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_manual_risk_escalation_contract_gate.md`
Objective:
定义 5c 风险升级触发标准与只读复核证据。
Special Constraints:
仅定义边界与复核模板，不实现，不改历史，不发起自动处理。
Next Seat:
产品规划席
