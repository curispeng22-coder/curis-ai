# Issue: AI Call Usage Ledger Foundation

## Objective

建立 Curis 原生、追加式 AI 调用事实账本。每次真实模型供应商调用尝试独立记录，
并以该账本作为 Token 与 AI 成本统计的唯一事实源。

## Authorized Scope

- `backend/app/database.py`
- `backend/app/ai_usage.py`
- `backend/app/model_gateway.py`
- `backend/app/main.py`
- `backend/app/orchestrator.py`
- `backend/app/workflow_runtime.py`
- `backend/app/result_store.py`
- `backend/app/evolution_event_log.py`
- `backend/app/usage_meter.py`
- `backend/app/billing_store.py`
- `backend/app/model_gateway_workspace.py`
- `backend/app/task_jobs.py`
- `backend/app/real_rd_executor.py`
- `backend/app/d1_single_model_toolchain.py`
- `backend/app/local_rd_toolset.py`
- `backend/tests/test_ai_usage_ledger.py`
- 受本契约变更影响的既有后端测试
- `reviews/20260729_ai_call_usage_ledger_foundation_review.md`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Contract

- 新增追加式 `ai_usage_records`；数据库禁止普通更新和物理删除。
- Token 未知、成本未知必须保存 `NULL`，不得伪造为零。
- 固定精度 `Decimal` 负责成本校验和累计。
- `tenant_id`、Business Department、Project、Task、Employee、Capability 必须同租户且
  业务归属一致；`department_id` 是调用发生时的快照。
- 同一 `idempotency_key` 只生成一条记录。
- Retry/Fallback 的每次真实出站尝试独立记录，共享 `logical_call_id`，使用不同
  `attempt_no`。
- `usage.*` 仅作为审计事件并引用 `usage_record_id`；不得再次携带或汇总 Token/成本。
- 只读接口：
  - `GET /api/ai-usage/records`
  - `GET /api/ai-usage/summary`
- 不采集或返回 Prompt、回答、API Key、Credential 或原始供应商响应。

## Acceptance

聚焦测试必须覆盖正常记录、完整业务关联、幂等、聚合、跨租户、Retry/Fallback、
未知计量和敏感字段隔离。系统交付席只运行聚焦测试；质量运行席执行一次全量回归并
写 Review。

## Forbidden

不开发 UI、数据洞察中心、CEO Office 成本页面、预算、支付、账单、外部插件、
tokscale、日志导入、历史回填、独立微服务或第二套组织模型。
