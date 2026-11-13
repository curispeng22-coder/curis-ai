# Curis Global Assistant Runtime v1 — Quality Review

Review date: 2026-07-30

Review seat: 质量运行席

Issue: `issues/20260730_global_assistant_runtime_v1.md`
Conclusion: **PASS**

## 结论

Global Assistant Runtime v1 通过独立质量验收：

- CEO Office 默认展示完整 Assistant Panel；其他 Workspace 页面展示隐藏入口。
- Identity 默认无固定名称、头像、角色、语气或人格，并可由用户保存、自定义、重载持久化。
- Project 页面上下文查询返回真实项目状态、Task 数量和风险。
- 执行指令创建并启动既有 Task，通过既有执行链产生结构化时间线；没有绕过 Task 修改业务对象。
- Provider 在真实 Next 页面导航后保留打开状态和未提交输入。
- Desktop 与 `390 × 844` Mobile 均可访问 Assistant。
- Snapshot、Notifications 和 UI 投影未展示 Prompt、回答、API Key、Credential 或原始 Event payload。
- Backend 全量回归、Frontend tests/lint/build、数据库完整性和官方启动链全部通过。

质量验收中发现的两个真实回归已由系统交付席修复并复核通过：

1. Identity PUT 曾携带只读 `updated_at`，被 Backend `extra=forbid` 以 `422` 拒绝；现由统一 API
   出站边界只发送五个可写 Identity 字段，编辑态同时展示错误。
2. `TerraBackLink` / `ProjectCard` 曾使用原生 `<a>` 导致 Provider 随整页 reload 重建；现改用
   Next `Link`，真实跨页面导航保留 `open` 和未提交输入。

## Provenance

- Worktree: `/Users/yy/Documents/Curis AI Workspace`
- Branch: `feat/roadmap-r1r2`
- Verification base HEAD: `dca7089695ce974f4be5607bc77f911b351110b6`
- Source state: 上述 HEAD 之上的未提交 Issue 工作树
- Database: `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite`
- Frontend: `127.0.0.1:3001`
- Gateway: `127.0.0.1:8080`
- Workspace API: container internal port `8002`
- Gateway health: `GET /health = 200`
- Frontend health: `GET /ceo-office = 200`

官方启动链执行前：

```text
Frontend PID: 93130 / 93138
Workspace image:
sha256:c51dbe0d18b619aa1fabb19a5f454ed45243f0bc770ffbba697f4063d43c23a2
Workspace started_at: 2026-07-30T06:34:06.730922539Z
```

该实例是本 Issue 编译前的旧 Workspace 镜像；Frontend HMR 已出现新 Panel，但 Assistant API
返回 `404 Not Found`。经主线程明确授权后，质量运行席只停止当前 Curis 官方实例并按官方命令
重建；未停止其他进程、未清空或重置数据库。

官方启动链执行后：

```text
Frontend PID: 9660
Gateway container:
749f05343cfb8c32d55bf985f1d633f011c09988e66dda35d986b37808c64e1a
Workspace container:
fc81a13301437d82090f632030c8c9a76d9bb7db5183177f9c67800138ecd29d
Workspace image:
sha256:8a969ce7b27682d838114b19f4d99cebc4c76cd337bd4f78feb098756ec2b357
Workspace started_at: 2026-07-30T09:13:12.853689275Z
```

工作树在验收前已存在大量与本 Issue 无关的未提交改动。质量运行席未修改实现、未暂存、未提交、
未推送，只新增本 Review；浏览器仅创建一条明确标识的 QA Task，并在 Identity 验收后恢复原空值。

## Full Regression

### Backend

Command:

```text
backend/.venv/bin/python -m pytest -q backend/tests
```

Result:

```text
1180 passed, 2 skipped, 123028 warnings in 150.53s
```

现有 warnings 主要为 FastAPI `on_event` / coroutine deprecation；没有测试失败。

### Frontend tests

最终修复后的 Command:

```text
cd frontend
node --test app/*.test.mjs app/platform/commercial/*.test.mjs \
  app/projects/'[project_id]'/*.test.mjs tests/*.test.mjs
```

Result:

```text
52 passed, 0 failed
```

### Frontend lint

Command:

```text
cd frontend && pnpm lint
```

Result: `PASS`

### Frontend build

最终修复后的 Command:

```text
cd frontend && pnpm build
```

Result: `PASS`

Next.js `16.2.10` 完成生产构建，生成 28 个页面/路由。

### Database

Command:

```text
sqlite3 data/curis.sqlite 'PRAGMA integrity_check; PRAGMA foreign_key_check;'
```

Result:

```text
ok
```

`foreign_key_check` 无返回行。

## Official Startup Chain

Command:

```text
./deploy/curis/stop-local.sh
CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh
```

Result: `PASS`

启动后：

```text
GET http://127.0.0.1:8080/health = 200
GET http://127.0.0.1:3001/ceo-office = 200
```

## Browser Acceptance Evidence

### Local Owner / CEO Office / Snapshot

真实浏览器路径：

```text
打开 Curis -> 登录 Curis -> 进入 Curis -> CEO Office
```

CEO Office 默认出现 `Global Assistant` dialog。空 Identity 显示通用占位：

```text
未命名 Assistant
尚未设置角色
```

没有写入固定名称、头像、角色、语气或人格。

Panel 从当前 Workspace 返回真实聚合：

```text
1 个业务部门
2 个项目
2 个既有 Task（执行验收前）
0 个待处理
1 个风险
12 条结构化通知
```

### Identity customization and persistence

在真实浏览器中保存：

```text
name: 质量验收 Assistant
avatar: QA
role: 本地 Workspace 验收助手
tone: 专业简洁
personality: 只基于真实业务数据回答
```

保存后表单关闭，名称与角色即时显示；完整 reload 后仍显示相同值，数据库记录存在。

最初保存复现过：

```text
PUT /api/workspace/assistant/identity = 422
```

修复后同一路径通过。验收结束前已再次通过 UI 将五个字段恢复为空；数据库最终未遗留固定或 QA
Identity。

### Project context query

真实 Project 页面：

```text
/ceo-office/projects/project-030c562c-fa20-4ad8-bdf8-e418e0859b30
```

在该页面打开隐藏 Assistant，选择“查询”，输入：

```text
当前项目怎么样？
```

返回：

```text
质量验收项目 20260729当前状态为planned；
共有 3 个 Task，其中 0 个执行中、0 个待处理、2 个失败；
已有 0 项成果。
```

回答使用页面 `project_id` 上下文和真实业务数据，不需要用户在指令中重复项目名称。

### Command -> Task -> Task Run

在 CEO Office 选择“执行”，输入：

```text
在质量验收项目 20260729中生成 Assistant Runtime 质量验收摘要 20260730
```

Assistant 创建并启动既有 Task：

```text
task_id: fa93d0f1-23c3-4542-ba5b-04283c849a49
project_id: project-030c562c-fa20-4ad8-bdf8-e418e0859b30
status: FAILED
created_at: 2026-07-30 09:15:08
```

Assistant 返回“指令已创建 Task 并进入执行链”和“查看 Task”。Task 详情可打开并展示：

```text
开始执行
已选择能力
已检索上下文
执行失败
```

当前本地模型调用归属不完整，执行链返回真实失败：

```text
business model call attribution is incomplete
```

系统没有伪装成功，也没有生成虚假 Token、成本或成果。该结果不阻塞本 Issue 的“创建并启动既有
Task”验收；真实外部模型成功结果需在 Owner 配置可用 Model Gateway 后另行验证。

### Cross-page state and hidden entry

真实复现路径：

```text
Task 详情
-> 打开 Assistant
-> 输入“跨页面未提交输入复核 20260730”
-> 点击“返回执行工作台”
-> /ceo-office/execution
```

最终修复后：

- `Global Assistant` 仍保持打开。
- 未提交输入原样保留。
- 最小化后 dialog 关闭，页面保留统一隐藏入口。
- 其他页面没有固定第三列 Assistant。

### Mobile

在 `390 × 844` 视口验证：

- 其他 Workspace 页面显示隐藏 Assistant 入口。
- 点击后浮层边界为 `left=12`、`right=378`、`top=12`、`bottom=832`。
- Panel 宽 `366`、高 `820`，完整位于 Mobile 视口内。
- Identity、Snapshot、通知和指令输入均可访问。

### Sensitive projection

真实 Browser dialog 与 Notifications 未出现：

```text
api_key
prompt
credential
原始 Event payload
模型隐藏思维链
```

通知只显示安全标题、事件类型和允许的业务引用。

## Acceptance Matrix

| # | Acceptance | Result | Evidence |
|---|---|---|---|
| 1 | Identity 可保存、重启保留、tenant fail-closed | PASS | 浏览器保存与 reload 持久化；Backend 全量覆盖 tenant 隔离 |
| 2 | Identity 默认不固定 | PASS | 初始及最终均为空值，只显示通用未命名占位 |
| 3 | Snapshot 聚合真实业务数据 | PASS | 浏览器显示真实部门、项目、Task、成果与风险；聚焦/全量测试覆盖其余数据源 |
| 4 | Pending / Risk 覆盖规定状态 | PASS | Browser 显示真实风险；Backend 全量覆盖 awaiting_input、handoff、failed、unmetered |
| 5 | Notifications tenant-scoped 且白名单化 | PASS | Browser 无敏感字段；Backend 全量覆盖跨租户和字段投影 |
| 6 | Project / Department 上下文查询 | PASS | Project 页面“当前项目怎么样”返回真实状态与 Task 数量；Backend 覆盖 Department |
| 7 | 指令创建并启动既有 Task | PASS | `fa93d0f1-...` 进入既有 Task Run 并显示结构化时间线 |
| 8 | 缺少 Project 返回 awaiting_context | PASS | Backend 全量覆盖，无猜测写入 |
| 9 | Provider 跨页保留状态 | PASS | 真实 Next 导航后 open 与未提交输入保留 |
| 10 | CEO 完整 Panel，其他页面隐藏入口 | PASS | Desktop 与 Mobile 浏览器通过 |
| 11 | Desktop / Mobile Identity、查询、指令链 | PASS | 本 Review 记录完整真实流程 |
| 12 | 全量回归、构建、启动链 | PASS | Backend 1180/2；Frontend 52/0；lint/build/官方启动全绿 |

## Security Boundary

- Assistant 只聚合既有 tenant-scoped 服务，不拥有 Company、Project、Task、Employee、
  Capability、Artifact、Memory 或 AI Usage 事实。
- 指令执行只创建并启动既有 Task；没有直接调用工具或修改业务对象。
- Identity PUT 仅发送五个可写字段，Backend 继续拒绝未知字段。
- Notifications 使用事件类型和字段白名单，不返回原始 payload。
- Token 与成本没有在 Assistant 中重复保存，继续以 `ai_usage_records` 为唯一事实源。
- 浏览器与日志没有出现 Prompt、回答、API Key、Credential 或隐藏思维链。
- 安全边界席最终结论：`PASS`。

## Known Limitations

- 当前本地环境缺少可成功完成该 QA Task 的业务模型调用归属，Task 真实失败；未把失败表述为
  Capability 或模型成功。
- v1 Identity avatar 仅支持 Emoji / 短文本标记，不支持远程头像、上传或 Desktop Floating
  Assistant；均符合本 Issue 禁止范围。
- v1 不持久化聊天历史或未提交输入的多设备状态；没有新建 Assistant Session、Chat 或
  Notification 表。

## Review

Global Assistant Runtime v1 准予进入产品规划席验收。

Next Seat: 产品规划席
Handoff: sent to main thread for 产品规划席 routing
