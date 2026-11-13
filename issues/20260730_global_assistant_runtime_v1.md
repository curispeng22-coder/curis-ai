# Curis Global Assistant Runtime v1

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-30

Expected review: `reviews/20260730_global_assistant_runtime_v1_review.md`

## Objective

将当前 `TerraShell` 内的 AI 秘书占位 Drawer 收敛为系统级 Global Assistant
Runtime，同时复用现有 Company、Business Department、Project、Task / Task Run、
Employee、Capability、Artifact、Memory、AI Usage 与 Event。

Assistant Identity 必须由用户配置，不固定名称、头像、角色、语言风格或个性。

## Architecture Decision

- Assistant 是现有 Workspace 的应用层聚合与入口，不拥有业务事实数据。
- Assistant 查询只读取现有 tenant-scoped 服务。
- Assistant 指令必须创建并运行现有 Task，禁止绕过 Task 修改业务对象或直接调用工具。
- Assistant 模型调用继续通过现有 Model Gateway；Token 与成本只写
  `ai_usage_records`。
- 复用 `evolution_events` 作为结构化审计来源，不新建通知事件表。
- 不新建 Agent、Session、聊天记录、Memory、Capability、Task 或 Workspace 体系。
- Local Desktop v1 的未读位置和未提交输入使用前端状态；不新增多设备同步表。

## Scope

### Assistant Identity

每个 Tenant 保存一份可选 Identity：

- `name`
- `avatar`
- `role`
- `tone`
- `personality`

Identity 允许为空，不写入产品固定身份。v1 `avatar` 是短文本、Emoji 或本地显示标记，
不加载远程图片。

接口：

```text
GET /api/workspace/assistant/identity
PUT /api/workspace/assistant/identity
```

### Assistant Service

接口：

```text
GET  /api/workspace/assistant/snapshot
GET  /api/workspace/assistant/notifications
POST /api/workspace/assistant/commands
```

`snapshot` 返回真实今日简报、待处理和风险提示。

`notifications` 只返回 tenant-scoped、字段白名单化的结构化通知，不返回原始 Event
payload、Prompt、回答、隐藏思维链或凭证。

`commands` 支持：

- 查询交流：按当前页面上下文或明确业务对象返回状态、进展与风险。
- 指令执行：创建现有 Task，并通过现有 Task Run / Capability 执行。
- 缺少 Project 上下文时返回 `awaiting_context`，不猜测写入目标。

### Assistant Context / State / Host

全局 Provider 管理：

- open / minimized
- 当前页面上下文
- 未提交输入
- 未读数量
- snapshot / notifications

页面只提供安全的结构化上下文，例如：

```json
{
  "page": "project",
  "project_id": "project-id"
}
```

CEO Office 默认展示完整 Assistant Panel；其他 Workspace 页面保留隐藏入口，点击后
展开同一个浮层。实现不得成为页面 Grid 的固定第三列。

## Allowed Files

- `issues/20260730_global_assistant_runtime_v1.md`
- `reviews/20260730_global_assistant_runtime_v1_review.md`
- `docs/architecture/curis-assistant-architecture-review.md`
- `docs/architecture/curis-assistant-runtime-architecture-report.md`
- `backend/app/database.py`
- `backend/app/main.py`
- `backend/app/assistant_runtime.py`
- `backend/app/evolution_event_log.py`
- `backend/app/task_jobs.py`
- `backend/tests/test_global_assistant_runtime.py`
- `frontend/app/layout.js`
- `frontend/app/globals.css`
- `frontend/app/ceo-office/page.js`
- `frontend/app/ceo-office/projects/[id]/page.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/components/terra/TerraPrimitives.js`
- `frontend/components/terra/TerraShell.js`
- `frontend/lib/api.js`
- `frontend/lib/assistantState.mjs`
- `frontend/app/assistantState.test.mjs`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Forbidden Scope

- 固定 Assistant 名称、头像、角色、语气或人格。
- Assistant 专属 Agent / Session / Chat / Memory / Task / Event 系统。
- 第二套 Token 或成本统计。
- 绕过 Task 直接修改 Company、Project、Employee、Capability 或 Artifact。
- 原始 Prompt、模型完整回答、隐藏思维链、Credential 或 Event payload 展示。
- 远程头像抓取、文件上传、Desktop 浮窗或多设备同步。
- AI 会议室 Runtime；当前阶段只允许明确导航或未接入状态。

## Acceptance

1. Identity 可读取、保存、重启后保留，并保持 tenant fail-closed。
2. Identity 默认不包含固定名称、头像、角色、语气或人格。
3. Snapshot 读取真实 Company、Department、Project、Task、Employee、Artifact 与
   AI Usage 数据。
4. Pending 覆盖 `awaiting_input`、`human_handoff`；Risk 覆盖 blocked Project、
   failed Task、失败或未计量 AI 调用。
5. Notifications 只返回 tenant-scoped 白名单字段，不泄露原始 payload。
6. 查询交流能根据 Project 或 Business Department 上下文返回真实状态、进展与风险。
7. 指令执行创建并启动现有 Task，不直接调用工具或修改业务对象。
8. 缺少 Project 上下文时不猜测目标，返回 `awaiting_context`。
9. Global Provider 在页面切换后保持 open/minimized、输入和未读状态。
10. CEO Office 展示完整 Panel；其他 Workspace 页面使用统一隐藏入口。
11. Desktop/Mobile 浏览器完成 Identity、查询和 Task 指令链验证。
12. Backend 聚焦与全量回归、Frontend tests/lint/build、官方启动链通过。

## Verification Ownership

- 系统交付席：聚焦 Backend/Frontend 测试、lint/build 和变更说明。
- 安全边界席：Identity、Tenant、Event 投影、指令/Task 与敏感字段边界。
- 质量运行席：一次全量回归、官方启动链和真实浏览器流程，写 Review。
- 产品规划席：根据 Review 接受或退回。

## Completion

- 系统交付席：Backend 聚焦 15 passed；Frontend Assistant 3 passed；lint/build PASS。
- 安全边界席：PASS。
- 质量运行席：Backend 全量 `1180 passed, 2 skipped`；Frontend
  `52 passed, 0 failed`；官方启动链、数据库、Desktop/Mobile Browser PASS。
- 产品规划席：ACCEPT。
- Review：`reviews/20260730_global_assistant_runtime_v1_review.md`
- Architecture Report：
  `docs/architecture/curis-assistant-runtime-architecture-report.md`
- Handoff: completed to main thread.
