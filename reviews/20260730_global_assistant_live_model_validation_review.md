# Global Assistant Live Model Chain Validation — Quality Review

Review date: 2026-07-30  
Review seat: 质量运行席  
Issue: `issues/20260730_global_assistant_live_model_validation.md`  
Conclusion: **PASS**

## 结论

Global Assistant 的一次非敏感真实模型链路通过独立质量复核：

```text
Assistant command
→ existing Task
→ Task Run
→ bound official Model Capability
→ approved newapi / OpenAI Gateway
→ AIUsageRecord
→ usage.model_call
→ completed Task
→ Artifact
```

真实 Task `1d634bb3-c154-4d16-98b6-b35b45eb4e8e` 为 `COMPLETED`，只产生一条
AIUsageRecord `usage-4ece6cc0-061b-4b96-90c9-adefcebc0686`。该记录为 HTTP 200、
`success / confirmed`，共 228 Token，权威成本 `USD 0.00023475`；浏览器按四位小数显示
`$0.0002`。同一 Task 存在一条 Artifact，`usage.model_call` 只引用同一
`usage_record_id`，没有复制 Token 或成本。

本 Review 只读取既有执行结果，没有触发第二次模型调用。

## Provenance

- Isolated worktree: `/private/tmp/curis-assistant-live-validation`
- Isolated base HEAD: `3b849cdab82f3061a2ece376d620691bcac953ca`
- Runtime source snapshot: `a57098c6dce4ac25d185863b7012c2daf12ade8d`
- Real database: `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite`
- Task: `1d634bb3-c154-4d16-98b6-b35b45eb4e8e`
- Usage: `usage-4ece6cc0-061b-4b96-90c9-adefcebc0686`

运行容器内源码与 `a57098c6` blob 哈希完全一致：

```text
backend/app/main.py
ebd8d5e699542f110978d08d973278f2d2f59d190e1ca17f2130c00f2f7a22ca

backend/app/assistant_runtime.py
8744953b418c40522eda905390fe1124f4449c6a25125a2e8e9bc16c44c50dc7
```

隔离工作树只承载本 Issue 的审核差异；实际运行快照同时包含主 Workspace 的其他既有改动。
Assistant Runtime 文件与运行快照一致，`main.py` 的差异仅来自这些既有、非本 Issue 改动。

## Test Evidence

### Focused

系统交付席冻结证据：

```text
42 passed
```

质量运行席在隔离工作树独立执行：

```text
/Users/yy/Documents/Curis AI Workspace/backend/.venv/bin/python -m pytest -q \
  backend/tests/test_global_assistant_runtime.py \
  backend/tests/test_workspace_startup_entry.py \
  backend/tests/test_model_gateway_adapter.py \
  backend/tests/test_ai_usage_ledger.py
```

Result:

```text
37 passed in 12.70s
```

测试使用主 Workspace venv 作为解释器和依赖来源，但 pytest 加载路径为隔离工作树。

### Frozen runtime snapshot regression

实际运行源码快照 `a57098c6` 的冻结证据：

```text
Backend: 1179 passed, 3 skipped
Frontend: 59 passed, 0 failed
Frontend lint: PASS
Frontend build: PASS
```

根据项目“不重复 unchanged evidence”的验证规则，本 Review 未再次执行相同全量回归。

### Database

```text
PRAGMA integrity_check = ok
PRAGMA foreign_key_check = no rows
git diff --check = PASS
```

## Real Execution Evidence

### Task and attribution

```text
status: COMPLETED
requested_capability_source: official
requested_capability_type: model
requested_capability_id: official.openai.gpt-5.4-mini-2026-03-17
output length: 35 characters
error: empty
```

Task、Company、Project、Business Department、Employee 均属于同一 Tenant：

```text
tenant_id:
local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4

company_id:
company-0fa5e6f8-7acc-4c31-89ea-63349dce8591

project_id:
project-83f1ed87-5f2d-4cc5-8b60-a9ddc20665fe

department_id:
dept-c14e4e2c-252f-4f90-ab7d-e2864076f5bb

employee_id:
emp-eaadda33-6f3c-4919-933c-a8ed3d183225
```

Company、Project、Department 均为 active；Department 与 Employee 的 Company /
Department 归属和 Task 快照完全一致。

### Bound Capability

```text
binding_id:
bind-656f10f4-068f-4f4c-a203-321d57795369

source/type:
official / model

capability_id:
official.openai.gpt-5.4-mini-2026-03-17

priority: 1
enabled: 1
```

官方模型与 Gateway 登记保持批准契约：

```text
provider: openai
gateway: newapi
base_url: https://api.openai.com
model: gpt-5.4-mini-2026-03-17
status: active
credential_ref: NULL
```

### AIUsageRecord

```text
usage_record_id:
usage-4ece6cc0-061b-4b96-90c9-adefcebc0686

provider / gateway / model:
openai / newapi / gpt-5.4-mini-2026-03-17

input_tokens: 211
output_tokens: 17
total_tokens: 228
cost_amount: USD 0.00023475
cost_source: estimated
price_version: 2026-07-17
execution_status: success
metering_status: confirmed
http_status: 200
latency_ms: 2394
attempt_no: 1
```

Task 对应的 AIUsageRecord 数量为 `1`，无 Retry 或 Fallback 重复记录。

按批准价格独立复算：

```text
211 × USD 0.75 / 1,000,000
+ 17 × USD 4.50 / 1,000,000
= USD 0.00023475
```

数据库成本与复算值差异为 `0.0`，低于 `USD 0.10` 上限。

### Timeline and audit

Task 的结构化事件顺序为：

```text
assistant.command_submitted
execution_started
capability_selected
knowledge_retrieved
usage.model_call
tool_called
usage.tool_call
usage.task_execution
execution_completed
```

另有既有执行治理的 simulation / rollback / decision 审计事件。

`usage.model_call` 数量为 `1`，引用：

```text
usage-4ece6cc0-061b-4b96-90c9-adefcebc0686
```

`usage.model_call`、`usage.tool_call` 和 `usage.task_execution` payload 均没有 Token 或
成本字段；权威统计仍只来自 `ai_usage_records`。

### Artifact

```text
artifact_id:
artifact-226390f8-5a5b-4407-a3c3-b0fcac68c60c

task_id:
1d634bb3-c154-4d16-98b6-b35b45eb4e8e

artifact_type: execution_result
status: generated
source_ref: task.output
content length: 35
content_sha256:
dcbf42940630e37202f4263d02e356ab208f78bb8fd9faf7362d04b5a8a2d2f0
```

同一 Task 的 Artifact 数量为 `1`。

## Browser Evidence

冻结的真实浏览器证据与数据库结果一致：

- 从 Global Assistant 提交固定非敏感指令。
- Assistant 返回同一 Task 链接。
- Task 页面显示 `COMPLETED`。
- 页面显示 228 Token、`$0.0002`、模型调用时间线及同一
  `usage_record_id`。
- Artifact 在 Task 页面可见。
- Browser console errors: `0`。

数据库独立复核确认浏览器所示 Task、Token、成本、usage 引用和 Artifact 均为真实持久化
记录，而非前端 Mock。

## Security Boundary

- 验收期间没有读取、输出或记录 Key 值。
- 真实调用完成后，当前 Workspace 容器已不再保留非空
  `CURIS_MODEL_GATEWAY_API_KEY`。
- Git diff、Workspace logs 和数据库中未发现符合实际 OpenAI Key 长度的明文模式。
- `credential_metadata` 为 `0` 行；`model_gateways.credential_ref` 为 `NULL`。
- 执行事件中敏感键检查为 `0`：无 Prompt、API Key、Credential、Authorization、
  原始响应或隐藏思维链字段。
- Gateway 仍为 `newapi`，Workspace 仍通过既有 egress allowlist；没有扩大公网边界。
- 没有新增 Workspace、Admin、Vault、Billing 或第二套 Usage 系统。

## Acceptance Matrix

| # | Acceptance | Result | Evidence |
|---|---|---|---|
| 1 | 无 Capability Binding 返回 awaiting_capability | PASS | 聚焦测试覆盖，且不创建 Task |
| 2 | Task 保存完整业务与 Capability 归属 | PASS | 真实 Task / Binding / Usage lineage 一致 |
| 3 | 官方启动安全转发；默认无 Key fail-closed | PASS | Compose 聚焦测试；当前容器 Key 已移除 |
| 4 | Key 不进入 Git、DB、API、日志、Review | PASS | 安全扫描与 credential 表检查通过 |
| 5 | 一次真实调用返回真实 HTTP 结果 | PASS | HTTP 200，attempt 1，单条真实 Usage |
| 6 | Task COMPLETED 且存在 Artifact | PASS | Task COMPLETED；Artifact 数量 1 |
| 7 | 唯一 AIUsageRecord，Token / 成本合法 | PASS | 228 Token；USD 0.00023475；price version 合法 |
| 8 | model_called 只引用同一 usage_record_id | PASS | 单条事件引用唯一 Usage，无 Token / cost 复制 |
| 9 | Browser 打开同一 Task 并显示结果 | PASS | Task、Usage、时间线、Artifact 与 DB 一致 |
| 10 | 测试、回归、启动、DB、安全 Review | PASS | 42 focused；QA 37；1179/3；59；DB 与边界检查通过 |

## Known Baseline

- 实际运行源码快照 `a57098c6` 是主 Workspace 的融合快照；隔离工作树用于确保本 Issue
  评审不混入其他开发改动。
- 本轮只验证一次已批准、非敏感、Owner-only 模型调用，不代表新增 SLA、额度、预算、
  Billing 或多租户模型权益。
- 价格为 `estimated`，但有明确 `price_version` 且按批准价格可独立复算；不是供应商实报成本。
- 本 Review 不触发第二次模型调用。

## Review

Global Assistant Live Model Chain Validation 准予通过，原
`BLOCKED_L2_LIVE_VALIDATION` 可按本 Task / Usage / Artifact 证据关闭。

## Product Acceptance

产品规划席结论：`ACCEPT`。本次 Owner-only、非敏感、单次批准模型链已满足产品验收，
`BLOCKED_L2_LIVE_VALIDATION` 可以关闭；该结论不构成 SLA、额度、Billing 或多租户
模型权益承诺。

Next Seat: main thread  
Handoff: sent to `/root`
