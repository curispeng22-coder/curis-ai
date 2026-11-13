# Workspace R4 第8项｜8a.3b 敏感字段过滤 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`c737a54aca9bb0a21241a681d32d73ed278f0b83`
- 质量结论：`PASS`
- 安全结论：`PASS`

## 结论

四类来源使用真实分源 allowlist；递归 denylist 任一命中即整体 `403`，对外逐字复用全局固定体。内部 fail_code、七字段日志和无 partial/空对象/敏感模板补偿边界一致。

唯一缺口：无。可推进 `8a.3c`。

## 独立核对

- `workflow_runs`、`step_results`、`content_publish_packages`、`content_workflow_runs` 均使用各自真实字段，不补通用 `source_*` 伪字段。
- 只有 StepResult 可经 tenant + `workflow_steps` 真实路径增加 `workflow_run_id`。
- 禁止 `result/final_report/summary/artifacts/source_workflow/next_step_hint` 作为来源最小投影或裸文本引用。
- 任意字段、嵌套字段或敏感文本伪装命中 denylist 时整体拒绝，唯一 HTTP 为 `403`。
- 对外 exact body：`{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}`。
- `SENSITIVE_PROJECTION_REJECTED` 仅作为内部日志 `fail_code`，不得进入响应。
- 日志仅允许 `timestamp/tenant_id/project_id/run_id/task_id/fail_code/step` 七字段。
- 不得剔除后继续，不返回 partial、空对象、`summary` 或 `next_step_hint`；安全模板不可证时省略，整体不满足契约则固定 `403`。

## 新鲜证据

固定修订：`feat/roadmap-r1r2 @ c737a54a`。

```text
.venv/bin/python -m pytest -q \
  backend/tests/test_ai_secretary_sensitive_projection_contract.py \
  backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`10 passed in 0.08s`。覆盖 fresh schema allowlist、真实 StepResult 关联、递归 denylist、全局 `403` 固定体、内部 fail_code、七字段日志与无 partial 行为。

安全 Review：`reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_security_review.md`，结论 `PASS`。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Gate 为契约复核，不声称 Secretary API 已实现。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
