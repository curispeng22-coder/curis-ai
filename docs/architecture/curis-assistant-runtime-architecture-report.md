# Assistant Runtime Architecture Report

Date: 2026-07-30

Issue: `issues/20260730_global_assistant_runtime_v1.md`

## 结论

Curis AI 秘书已从 `TerraShell` 页面占位 Drawer 收敛为 Workspace 级
`Global Assistant Runtime v1`。

本次实现没有新建 Agent、Session、Chat、Memory、Task、Capability、Event 或
AI Usage 体系。Assistant 是现有业务服务之上的 tenant-scoped 聚合与交互入口：

```text
Workspace 页面
→ Global Assistant Host / Provider
→ Assistant Runtime Service
├→ Company / Business Department / Project / Employee
├→ Task / Task Run / Capability / Artifact / Memory
├→ AI Usage Record
└→ tenant-scoped Event 投影
```

执行类指令只能创建现有 Task，并由现有 Orchestrator 进入 Task Run / Capability
执行链；Assistant 不直接修改业务对象，也不直接调用工具。

## 1. Assistant Identity

Identity 是用户数据，不是代码常量。每个 Tenant 可独立保存：

- `name`
- `avatar`
- `role`
- `tone`
- `personality`

所有字段默认均为空。界面中的“未命名 Assistant”与通用图标只是未配置状态提示，
不会写入 Identity。v1 的 `avatar` 只接受短文本、Emoji 或本地显示标记，不抓取远程
头像。

持久化使用最小表 `assistant_identities`，只保存展示 Identity；不保存业务事实、对话、
Prompt、模型回答或凭证。

接口：

```text
GET /api/workspace/assistant/identity
PUT /api/workspace/assistant/identity
```

## 2. Assistant Context

页面只向 Runtime 提供字段白名单化的结构化上下文：

```json
{
  "page": "project",
  "project_id": "project-id"
}
```

允许的实体引用为 Company、Business Department、Project、Task 和 Employee。
Backend 会用现有 tenant-scoped 服务重新读取并校验引用及其组织归属，客户端传入的
ID 不能作为可信业务事实。

已接入：

- CEO Office：`page=ceo-office`
- Project Runtime / 项目工作台：`page=project, project_id`
- Task 详情：`page=task, task_id`
- 其他 Workspace 页面：安全的 `page=workspace` 默认上下文

## 3. Assistant State 与 UI Host

根布局只挂载一个 `GlobalAssistantProvider` 和一个 `GlobalAssistantHost`。
React Context + `useReducer` 管理：

- open / minimized
- 当前页面上下文
- 未提交输入
- 查询 / 执行意图
- Identity
- Snapshot / Notifications
- 未读数量
- 最近一次处理结果

没有新增前端状态库。页面切换不会重建 Provider，因此打开状态、输入和未读状态可在
Workspace 页面之间保留。

展示方式：

- CEO Office 首次进入默认展开完整 Panel；
- 其他 Workspace 页面默认显示隐藏式圆形入口；
- 展开后复用同一个浮层；
- 登录、Onboarding、Platform 与 Credential 页面不显示 Assistant；
- Desktop Floating Assistant 保留为未来宿主，不在本 Issue 实现。

## 4. Assistant Service

### 4.1 Snapshot

```text
GET /api/workspace/assistant/snapshot
```

只聚合现有 tenant-scoped 服务，返回：

- 今日简报：公司、部门、项目、Task、员工、Capability、Artifact、Memory 数量；
- 待处理：`AWAITING_INPUT`、`HUMAN_HANDOFF` Task；
- 风险提示：blocked Project、failed Task、失败或未计量 AI 调用；
- 最近成果和 AI Usage 权威聚合。

Token 与成本继续只来自 `ai_usage_records`，没有复制进 Assistant 数据。

### 4.2 Notifications

```text
GET /api/workspace/assistant/notifications
```

通知复用 `evolution_events`，但新增了 tenant 必填、事件类型白名单和字段白名单投影。
响应只包含标题、级别、时间及必要实体引用，不返回原始 Event payload。

### 4.3 Commands

```text
POST /api/workspace/assistant/commands
```

支持：

- `query`：根据 Project、Business Department 或 Workspace 上下文读取真实状态；
- `execute`：创建并排队现有 Task；
- `auto`：v1 用最小本地意图规则区分查询和执行。

查询返回结构化事实与来源引用。执行缺少唯一 Project 上下文时返回
`awaiting_context`，不猜测写入目标。

## 5. 指令执行链

```text
用户指令
→ Assistant Context / tenant 归属校验
→ 创建现有 Task
→ INIT → PENDING
→ 现有 Orchestrator
→ Task Run
→ Capability / Model Gateway / Tool
→ Artifact / Event
→ AIUsageRecord（如发生真实模型调用）
```

Assistant Event 只记录 Task、Project、Employee 和页面引用，不记录完整指令内容。
Task 的实际执行结果、失败、暂停、接管和恢复继续由现有执行控制闭环负责。

## 6. 安全边界

- 所有接口沿用现有 Local Owner / Workspace 认证和 `TenantContext`；
- tenant 缺失时 fail-closed；
- Page Context 只接受固定字段，实体引用在 Backend 重新校验；
- 通知查询必须带 tenant 条件，禁止直接复用无 tenant 条件的 `get_all()`；
- 不向前端返回 Prompt、完整模型回答、隐藏思维链、API Key、Credential 或原始供应商
  响应；
- Identity 更新审计只保存字段名，不保存字段内容；
- Assistant 不提供直接业务写入或直接 Tool 调用 API；
- 登录、Onboarding 与 Secret Vault 不挂载 Assistant Host。

## 7. 验证

系统交付席聚焦证据：

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_global_assistant_runtime.py \
  backend/tests/test_digital_employee_execution_control_loop.py \
  backend/tests/test_ai_usage_ledger.py
→ 15 passed

node --test app/assistantState.test.mjs
→ 3 passed

npm run lint
→ passed

npm run build
→ passed，28 个 App Router 页面完成生成
```

聚焦测试覆盖 Identity 空默认与持久化、tenant 隔离、真实 Snapshot、Project /
Department 查询、Task 指令链、缺少 Project、通知白名单和跨租户拒绝。

质量运行席的全量回归、官方启动链、Desktop/Mobile 真实浏览器证据记录在：

- `reviews/20260730_global_assistant_runtime_v1_review.md`

最终独立验收：

```text
Backend 全量：1180 passed, 2 skipped
Frontend 全量：52 passed, 0 failed
Frontend lint/build：PASS
Database integrity / foreign_key_check：PASS
官方启动链：PASS
Desktop / Mobile Browser：PASS
安全边界席：PASS
产品规划席：ACCEPT
```

浏览器验证覆盖 Identity 保存与 reload、Project 上下文查询、指令创建既有 Task 并打开
结构化时间线、跨页保留打开状态与未提交输入、其他页面隐藏入口及安全通知投影。

## 8. 已知限制

- v1 查询回答是对现有结构化事实的确定性摘要，不额外发起模型调用；
- `auto` 意图识别使用最小关键词规则；只有在独立批准真实 Assistant 模型路由后，
  才应复用 Model Gateway 替换；
- `tone` 与 `personality` 已持久化并可配置，但确定性摘要阶段不做模型人格化改写；
- 未提交输入、open/minimized 和未读位置是 Local Desktop 前端状态，不提供多设备同步；
- 不保存聊天历史，不实现远程头像、文件上传或 Desktop 浮窗。

## 9. 真实模型链验证

2026-07-30 使用固定非敏感指令验证了现有完整执行链：

```text
Assistant command
→ Task 1d634bb3-c154-4d16-98b6-b35b45eb4e8e
→ official.openai.gpt-5.4-mini-2026-03-17
→ Model Gateway
→ AIUsageRecord usage-4ece6cc0-061b-4b96-90c9-adefcebc0686
→ model_called
→ Artifact
→ COMPLETED
```

供应商实报 211 Input、17 Output、228 Total Tokens；成本按
`price_version=2026-07-17` 估算为 USD `0.00023475`。同一 Task 恰有一个
`model_called`，只引用该 usage ID；Task 详情在真实浏览器展示结果、结构化时间线、
Token 和成本，Console 为 0 error。

真实 Key 仅由 Owner 当前终端临时注入，未进入聊天、Git、SQLite、日志或浏览器。
调用完成后含 Key 容器已停止；无 Key 重启保持 fail-closed。

验证结果：

```text
Focused backend: 42 passed
Runtime snapshot backend: 1179 passed, 3 skipped
Frontend: 59 passed
Frontend lint/build: PASS
Security: PASS
Quality: PASS
Product: ACCEPT
```
