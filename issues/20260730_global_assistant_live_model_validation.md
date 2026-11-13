# Global Assistant Live Model Chain Validation

Status: CLOSED — PASS

Owner seats: 系统交付席 / 安全边界席 / 质量运行席

Date: 2026-07-30

Expected review: `reviews/20260730_global_assistant_live_model_validation_review.md`

## Objective

在不泄露或落盘真实 Key 的前提下，完成一次非敏感 Global Assistant 真实模型执行：

```text
Assistant command
→ existing Task
→ Task Run
→ bound Model Capability
→ approved Model Gateway
→ AIUsageRecord
→ model_called timeline
→ completed Task / Artifact
```

修复当前 QA Task 在出站前以
`business model call attribution is incomplete` 失败的问题，并证明真实失败不会被伪装
为成功。

## Current Facts

- 当前 Workspace 容器没有注入任何 `CURIS_MODEL_GATEWAY_*` 变量。
- 当前官方启动 Compose 没有把可选 Model Gateway 环境变量传入 Workspace 容器。
- 当前 QA Project Owner Employee 没有 Employee Capability Binding。
- Assistant Task 创建逻辑已复用普通 Task 的 preferred capability 选择；有绑定时会写入
  Task attribution，无绑定时当前仍会创建注定失败的 Task。
- `ai_usage_records` 继续是 Token 与成本唯一事实源。

## Scope

1. 官方启动链支持从当前 Shell 安全转发批准的 R3 Model Gateway 环境变量。
2. 默认没有 Key 时保持未启用，不改变 Local Desktop 启动行为。
3. Assistant 执行前要求目标 Employee 至少有一个启用的 Capability Binding；缺失时返回
   `awaiting_capability`，不创建注定失败的 Task。
4. 复用现有 Employee Capability Binding API，为真实验证员工绑定已登记的官方模型。
5. Owner 只在本机终端以隐藏输入注入 Key；Key 不进入聊天、数据库、Issue、Review、
   Git、日志或截图。
6. 只执行一条固定的非敏感短指令。
7. 验证 Task、Task Run、Capability、AIUsageRecord、model_called、Token、成本、
   Artifact 和浏览器结果之间的关联。

## Approved Runtime Contract

```text
profile: r3_openai
gateway_id: newapi
base_url: https://api.openai.com
model: gpt-5.4-mini-2026-03-17
capability: official.openai.gpt-5.4-mini-2026-03-17
timeout: 60s
retry: 0
fallback: none
max estimated cost: USD 0.10
```

## Security Boundary

- 不要求用户在聊天中发送 Key。
- 不读取、打印、截图或查询 Key 值。
- 只检查变量是否存在。
- Key 只从 Owner 当前终端环境传入 Docker Workspace 容器。
- 不写 `.env`、`quality.env`、SQLite、Credential 表或前端 localStorage。
- 不修改 Gateway 公网边界；Workspace 继续通过现有 egress allowlist。
- Prompt 固定为非敏感测试内容，不含客户数据、源码、凭证或商业机密。
- 日志与 Review 只记录 provider、model、HTTP 状态、延迟、Token、成本、
  usage_record_id 和业务关联 ID。

## Allowed Files

- `issues/20260730_global_assistant_live_model_validation.md`
- `reviews/20260730_global_assistant_live_model_validation_review.md`
- `backend/app/assistant_runtime.py`
- `backend/app/main.py`
- `backend/app/model_gateway.py`
- `backend/tests/test_global_assistant_runtime.py`
- `backend/tests/test_workspace_startup_entry.py`
- `deploy/curis/gateway/docker-compose.yml`
- `docs/architecture/curis-assistant-runtime-architecture-report.md`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Forbidden Scope

- 新 Model Gateway、模型目录、Capability、Workspace、Admin、Billing 或 Vault 体系。
- FreeLLMAPI、tokscale 或外部历史日志导入。
- 将 Key 写入仓库、数据库、Issue、Review、日志、浏览器或聊天。
- 使用 Mock 代替真实供应商调用。
- 使用敏感 Prompt。
- 放宽 Tenant、Employee、Project、Capability 或 AI Usage 归属校验。
- 为通过测试伪造 Token、成本、Artifact 或成功状态。

## Acceptance

1. 没有 Capability Binding 时 Assistant 返回 `awaiting_capability`，不创建 Task。
2. 有绑定后 Task 保存 Employee、Project、Department、Capability 归属。
3. 官方启动链可安全转发 R3 配置；默认无 Key 时仍 fail-closed。
4. Key 不出现在 Git diff、数据库、API、日志、Review 或截图。
5. 一次真实调用返回真实 HTTP 结果；401/403/429/5xx 不伪装成功。
6. 成功时 Task 为 `COMPLETED`，存在 Artifact。
7. 成功时恰有对应 AIUsageRecord，Token 非空，成本与 `price_version` 合法。
8. `model_called` 只引用同一 `usage_record_id`，不复制 Token/成本。
9. Browser 可从 Assistant 打开同一 Task 并查看结果与结构化时间线。
10. 聚焦测试、全量回归、官方启动、数据库检查和安全 Review 通过。

## Actual Evidence

- 固定非敏感指令：`Reply exactly CURIS_ASSISTANT_LIVE_QA_OK_20260730.`
- Task：`1d634bb3-c154-4d16-98b6-b35b45eb4e8e`，最终状态 `COMPLETED`。
- Capability：`official.openai.gpt-5.4-mini-2026-03-17`。
- AIUsageRecord：`usage-4ece6cc0-061b-4b96-90c9-adefcebc0686`。
- Provider / Model：`openai` / `gpt-5.4-mini-2026-03-17`，HTTP `200`，
  延迟 `2394 ms`。
- 用量：Input `211`、Output `17`、Total `228`；成本 USD
  `0.00023475`，`estimated`，`price_version=2026-07-17`。
- Artifact：`artifact-226390f8-5a5b-4407-a3c3-b0fcac68c60c`，内容为固定预期结果。
- 同一 Task 时间线恰有一个 `model_called`，只引用上述 `usage_record_id`。
- 数据库原始记录求和与该记录一致；数据库和运行日志的 Key 模式扫描均为 0 命中。
- 真实调用后立即停止含 Key 的容器；无 Key 重启后模型配置保持 fail-closed。
- 聚焦测试：`42 passed`。
- 实际运行快照 Backend 全量：`1179 passed, 3 skipped, 0 failed`。
- Frontend：`59 passed`；lint/build PASS，28 个 App Router 页面完成生成。
- 真实浏览器 Task 详情、Artifact、结构化时间线、Token/成本展示通过；
  Browser Console `0 error`。
- 安全边界席：`PASS`；质量运行席：`PASS`；产品规划席：`ACCEPT`。
