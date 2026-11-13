# 2026-07-18 Workspace R4 项目状态事实源 A3 Focused 复核

- Issue：`issues/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- 结论：`PASS`

## 复核范围（只读）

- 成功链路：`GET /api/workspace/workflows/wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（`X-Tenant-Id: tenant-a`）
- 拒绝链路：
  - `X-Tenant-Id: tenant-b` 同 Run
  - 缺省 tenant 同 Run（`X-Tenant-Id` 空）

## 结果（单次命令聚焦）

- A1 status：`200`，`project_status.execution_status = completed`。
- A1 映射一致性：
  - steps = `7`，`step_results = 7`，两者均全体 `succeeded`；
  - artifact 存在且 `artifact.source = workflow_runs.final_report`；
  - final_report 非空，`final_report` 为 read-model 的直接正文来源之一。
- A2 可见域：
  - SQL 核对 `tenant_id='tenant-a' AND project_id='project-e84e06d4-f014-4326-abcd-e6d9aea6ff95' AND workflow_run_id=<run>` 命中 `1` 条；
  - usage 侧链：`usage.model_call` 命中 `7` 条；
  - 跨租户请求返回 `404`；
  - 缺省 tenant 请求返回 `404`。

## 结论

- 事实源映射与边界规则在一次 focused 中闭环通过，可继续推进父链路。
- 未改模型、不起新服务、不重跑 full、不触发出网。

Handoff: sent to 产品规划席
