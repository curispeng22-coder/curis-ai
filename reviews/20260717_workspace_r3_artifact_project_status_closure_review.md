# 2026-07-17 Workspace R3 Artifact 与 Project Status Closure 质量复核

- Issue：`issues/20260717_workspace_r3_artifact_project_status_closure.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定 SHA：`2da0367b`
- Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- 结论：`PASS`

## 真实可打开验收（无出网）

使用 `TestClient` 读取固定数据库 `deploy/curis/gateway/.generated/data/quality.sqlite`：

- `GET /api/workspace/workflows/wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（`X-Tenant-Id: tenant-a`）返回 200。
- `artifact.artifact_type = document_report`
- `artifact.content_length = 6018`
- `artifact.content_sha256 = 2d14cf90ca1fa850f7e8425763b922cda4c6c9c2132a2f55eac07791a07ba96c`
- `artifact.content == detail.final_report`。
- `artifact.step_references` 长度 = 7，`workflow_step_id` 覆盖 1..7。
- `artifact.usage_event_references` 长度 = 7。
- `project_status.execution_status = completed`
- `project_status.next_step_suggestion = null`
- `project_status.stored_status = active`
- 重复读取同一 Run 的 artifact 字段一致（幂等）。

## 聚合一致性与链路闭环

直接从 `quality.sqlite` 核对：

- Run：`status=succeeded`，`tenant_id=tenant-a`，`company_id=company-a`，`project_id=project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`，`task_id=404942fa-b4a5-4e84-a4a4-7b4427b23129`
- `workflow_steps`=7，`step_order=1..7`，`status=succeeded` 全量。
- `step_results`=7，`status=succeeded` 全量。
- `executions`=7，`tool_name=official.openai.gpt-5.4-mini-2026-03-17` 全量。
- `evolution_events` usage model_call=7，且每条 `outbound_attempted=true`。
- `total_tokens = 9,622`，`estimated_cost = 0.013269`。
- `final_report` SHA256 与 artifact SHA256 一致。

## 边界回归

- 跨租户（`tenant-b`）请求同一 `workflow_run_id`：404。
- 错 Run 请求：404。
- 不重新读取/不修改/不新增 Run。

## 备注

- 未启动模型、未注入 Key、无新出网动作、无 full-run 变更。
- 本复核直接满足 `issues/20260717_workspace_r3_artifact_project_status_closure.md` 的聚焦验收与边界要求，可由产品规划席据此推进父 Issue。

Handoff: sent to 产品规划席
