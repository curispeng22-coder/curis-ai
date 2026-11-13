# 数字员工执行控制闭环 v1

Status: CLOSED — LOCAL CONTROL PASS / BLOCKED_L2_LIVE_VALIDATION

Owner seat: 系统交付席

Approval date: 2026-07-30

Expected review: `reviews/20260730_digital_employee_execution_control_loop_v1_review.md`

## Objective

在现有 Employee、Capability、Task、Task Job、Workflow、Project、Business
Department、Event、Artifact 与 AI Usage Record 上，交付可追踪、可暂停、可接管、
可恢复的数字员工执行闭环。

## Architecture Decision

- 继续使用现有 `task_id` 作为 S5 已公开的持久化 `job_id`，同时作为本期
  `task_run_id`；不新增并行 Task Run / Agent / Session 系统。
- 继续使用追加式 `evolution_events` 保存结构化执行事件；不新增第二套事件表。
- 只给 `tasks` 增加恢复所需的最小持久化字段。
- `usage.model_call` 是已存在的模型调用审计事件；时间线将其规范化为
  `model_called`，且只引用 `usage_record_id`。Token 与成本仍只读
  `ai_usage_records`。
- 用户操作放入现有 Task 详情，不创建聊天工作台。

## Scope

### Structured Events

- `execution_started`
- `capability_selected`
- `knowledge_retrieved`
- `model_called`
- `tool_called`
- `awaiting_input`
- `human_handoff_requested`
- `human_handoff_accepted`
- `execution_resumed`
- `execution_completed`
- `execution_failed`
- `execution_cancelled`

事件关联 tenant、Employee、Capability、Task、Task Run、Project、Business
Department、AI Usage Record 与 UTC timestamp。事件载荷不得包含 Prompt、模型回答、
隐藏思维链、密钥、Credential 或原始供应商响应。

### Persistent Control State

支持：

- `running`
- `awaiting_input`
- `human_handoff`
- `resumed`
- `completed`
- `failed`
- `cancelled`

暂停和接管状态持久化当前步骤、待解决问题、安全上下文摘要、接管人/责任人、
恢复参数和状态变更时间。恢复继续原 `task_id`，跳过已完成 Workflow 步骤。

### Workspace Actions

Task 详情支持：

- 查看结构化时间线
- 标记缺失信息并暂停
- 补充信息
- 请求/接受人工接管
- 转派接管人
- 恢复 AI 执行
- 取消执行

CEO Office 首页不展示底层时间线或调试日志。

## Capability Runtime Signal

既有 Tool/Capability 可通过结构化返回触发暂停：

```json
{
  "status": "awaiting_input",
  "question": "需要补充什么",
  "context_summary": "安全摘要",
  "resume_parameters": {}
}
```

`human_handoff` 使用同一最小契约。不得通过解析模型自由文本猜测暂停状态。

## Migration

对 `tasks` 执行幂等 additive migration：

- `current_execution_step`
- `pending_question`
- `execution_context_summary`
- `handoff_assignee_id`
- `resume_parameters_json`
- `execution_state_changed_at`

不回填伪造历史事件；旧 Task 的时间线从本期后新执行开始产生。

## Allowed Files

- `issues/20260730_digital_employee_execution_control_loop_v1.md`
- `reviews/20260730_digital_employee_execution_control_loop_v1_review.md`
- `backend/app/database.py`
- `backend/app/main.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`
- `backend/app/task_jobs.py`
- `backend/app/tool_executor.py`
- `backend/app/task_execution_control.py`
- `backend/tests/test_digital_employee_execution_control_loop.py`
- `frontend/lib/api.js`
- `frontend/app/ceo-office/execution/page.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Forbidden Scope

- StaffDeck 源码或 AGPL-3.0 代码复制。
- Capability 分支、升级、回滚、差异或自动改进。
- 新 Agent、Skill、Session、SOP、Knowledge、Workspace 或 Admin 体系。
- 外部微信、企微、飞书、钉钉渠道。
- 重复 Token/成本字段或新的 Usage 事实源。
- 隐藏思维链、Prompt、模型回答、密钥、Credential、原始供应商响应展示。

## Acceptance

1. 真实 Task 执行显示完整结构化时间线。
2. 每次模型调用只通过唯一 `usage_record_id` 追溯 `ai_usage_records`。
3. Capability 返回缺失信息信号时 Task 进入 `awaiting_input`，不进入失败。
4. 用户补充信息后原 Task Run 从已保存步骤恢复。
5. 人工接管后不再启动后续 AI/Tool 步骤。
6. 恢复继续原 Task，不创建重复 Task。
7. 刷新或服务重启后暂停、接管和恢复参数仍存在。
8. 所有读写 tenant fail-closed，不泄露思维链、Prompt、回答、密钥或凭证。
9. 系统交付席提交聚焦测试、迁移说明和变更说明。
10. 质量运行席执行一次全量回归、真实浏览器流程并写 Review。

## Verification Ownership

- 系统交付席：聚焦后端测试、聚焦前端测试与 `git diff --check`。
- 质量运行席：一次后端全量回归、Frontend tests/lint/build、正式启动链、真实浏览器
  暂停/补充/接管/恢复/取消流程，并写 Review。
- 产品规划席：根据 Review 接受或退回。

## Final Outcome

- 本地执行控制闭环由产品规划席 `ACCEPT`。
- Backend 全量回归：`1175 passed, 2 skipped`。
- Frontend：`49 passed`；lint/build PASS。
- 官方启动链、数据库完整性、Desktop/Mobile 浏览器暂停、补充、接管、转派、
  接受、同 Task 恢复、刷新/重启持久化和取消均 PASS。
- 安全边界席：`PASS`。
- 真实供应商成功调用到 `AIUsageRecord` / `model_called` 的浏览器正向证据因本机
  无安全批准的模型配置保持 `BLOCKED_L2_LIVE_VALIDATION`，不阻塞本地控制闭环交付。
- Review：`reviews/20260730_digital_employee_execution_control_loop_v1_review.md`。
