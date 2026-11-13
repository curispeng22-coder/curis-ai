# 数字员工执行控制闭环 v1 — Quality Review

Review date: 2026-07-30
Review seat: 质量运行席
Issue: `issues/20260730_digital_employee_execution_control_loop_v1.md`
Conclusion: **LOCAL CONTROL PASS / BLOCKED_L2_LIVE_VALIDATION**

## 结论

本 Issue 的本地执行控制闭环通过质量验收：

- Task 详情可展示结构化执行时间线。
- `awaiting_input`、补充信息、人工接管、转派、接受接管、恢复和取消均在真实浏览器中完成。
- 恢复继续同一 `task_id`，没有创建重复 Task。
- 刷新页面及完整停止/重启官方服务后，暂停状态、恢复信息和时间线未丢失。
- 人工接管期间没有继续自动执行。
- Desktop 与 390 × 844 Mobile 视口均可访问控制操作和结构化时间线。
- Backend 全量回归、Frontend tests/lint/build、数据库检查及官方启动链全部通过。

当前环境没有可用的真实外部模型配置。恢复执行时系统返回真实错误
`business model call attribution is incomplete`，没有伪装成功。因此：

- 本地控制、持久化、租户边界和 UI 流程：**PASS**。
- 真实供应商模型成功调用及其 `usage_record_id` 浏览器正向链：**BLOCKED_L2_LIVE_VALIDATION**。
- `usage_record_id` 唯一追溯和“不复制 Token/成本”的契约由聚焦测试及 Backend 全量回归覆盖，
 但本 Review 不把测试替代为真实外部模型成功证据。

## Provenance

- Worktree: `/Users/yy/Documents/Curis AI Workspace`
- Branch: `feat/roadmap-r1r2`
- HEAD: `ceaf33ebf3e5368cd7b23d721bb7d5f2c843a44f`
- Database: `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite`
- Frontend: `127.0.0.1:3001`
- Gateway: `127.0.0.1:8080`
- Workspace API: container internal port `8002`
- Workspace image:
  `sha256:c51dbe0d18b619aa1fabb19a5f454ed45243f0bc770ffbba697f4063d43c23a2`
- Gateway image:
  `sha256:caa5b411be1633b90023592a34a7e010c933d6e60206c758f631485e53006865`
- Gateway health: `GET /health = 200`
- Frontend health: `GET /ceo-office = 200`

工作树在验收前已存在大量与本 Issue 无关的未提交改动；质量运行席未修改源码、未暂存、
未提交、未推送，只新增本 Review。

## Full Regression

### Backend

Command:

```text
PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python -m pytest -q backend/tests
```

Result:

```text
1175 passed, 2 skipped, 116804 warnings in 114.81s
```

初次全量回归曾发现历史 D1 fixture 的 `tasks` 表没有 `updated_at`，而迁移 SQL 使用
`coalesce(updated_at, created_at)`，导致 3 个失败。系统交付席修复兼容性后冻结源码，
质量运行席重新执行上述完整命令，最终结果为全绿。

### Frontend tests

Command:

```text
cd frontend
node --test app/*.test.mjs app/platform/commercial/*.test.mjs \
  app/projects/'[project_id]'/*.test.mjs tests/*.test.mjs
```

Result:

```text
49 passed, 0 failed
```

### Frontend lint

Command:

```text
cd frontend && pnpm lint
```

Result: `PASS`

### Frontend build

Command:

```text
cd frontend && pnpm build
```

Result: `PASS`

Next.js `16.2.10` 完成生产构建；生成 28 个页面/路由，其中
`/ceo-office/execution` 为静态页面，
`/ceo-office/execution/tasks/[id]` 为动态页面。

### Database

Commands:

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

启动器确认：

```text
Frontend 3001
Workspace internal 8002
Gateway 8080
```

首次镜像构建遇到本机 Docker `no space left on device`。质量运行席仅清理 dangling
Docker images，回收 `1.235GB` 构建缓存；未删除项目数据。随后使用相同官方命令启动成功。

## Browser Acceptance Evidence

### Desktop

认证路径使用现有 Local Owner：

```text
打开 Curis -> 进入 Curis -> CEO Office -> 执行工作台 -> Task 详情
```

在既有 Task `83eebab8-7d33-4462-99fd-5ecee7b992d1` 上完成：

1. 请求人工接管。
2. 保存当前步骤、待解决问题、安全摘要和 `local-owner` 责任人。
3. 刷新页面后 `HUMAN_HANDOFF` 和时间线仍存在。
4. 转派给现有 Owner，时间线新增“已转派接管人”。
5. 接受接管，时间线新增“人工已接管”。
6. 点击恢复后 URL 和 `task_id` 不变；时间线新增“恢复 AI 执行”。
7. 因外部模型配置缺失，执行返回真实失败并新增结构化失败事件，没有伪造成功。

### Awaiting input, restart persistence, resume and cancel

通过 Workspace UI 创建质量验收 Task：

```text
task_id: c75e8944-0b04-4231-83fc-ba9ad8f46625
name: 质量验收：等待补充、恢复与取消闭环 20260730
```

官方运行环境没有外部模型配置，Task 会在可由 UI 触发暂停前真实失败。为只验证控制闭环，
质量运行席对该新建 QA Task 使用一次显式、租户限定、条件更新的本地 fixture，将其从
`INIT` 置为 `PENDING`；该操作没有创建模型成功、用量或成本记录。

随后在真实浏览器完成：

1. 点击“等待补充”，状态变为 `AWAITING_INPUT`。
2. 保存当前步骤“确认验收目标”、问题“请补充验收结果用途”、安全摘要和责任人。
3. 刷新后暂停状态仍存在。
4. 点击“补充信息”，时间线新增“用户已补充信息”。
5. 在暂停状态执行完整 `stop-local.sh` / `start-local.sh`。
6. 重新进入 Local Owner 后，同一 Task 仍为 `AWAITING_INPUT`，暂停与补充事件均存在。
7. 点击“恢复 AI 执行”，继续同一 Task；没有创建重复 Task。
8. 外部模型配置缺失时返回真实失败，然后请求人工接管。
9. 在 390 × 844 Mobile 视口确认操作按钮及时间线可访问。
10. 点击“取消执行”，通过原生确认框确认；同一 Task 变为 `CANCELLED`。
11. 重新打开 Task 详情，页面显示“已取消”，时间线新增：
    `执行取消 2026/7/30 06:42:09 用户在 Task 详情取消执行`。

数据库最终状态：

```text
status = CANCELLED
state_flow = ["INIT","PENDING","AWAITING_INPUT","RESUMED","PARSED",
              "RUNNING","FAILED","HUMAN_HANDOFF","CANCELLED"]
```

追加事件按时间可见：

```text
awaiting_input
input_supplied
execution_resumed
execution_failed
human_handoff_requested
execution_cancelled
```

## Acceptance Matrix

| # | Acceptance | Result | Evidence |
|---|---|---|---|
| 1 | 真实 Task 显示结构化时间线 | PASS | 浏览器显示开始、能力、知识、暂停、恢复、失败、接管、取消等安全事件 |
| 2 | 模型调用唯一追溯 AI Usage Record | BLOCKED_L2 | 聚焦测试/全量回归通过；本机无外部模型配置，未取得真实成功调用 |
| 3 | 缺失信息进入 awaiting_input | PASS | QA Task 进入 `AWAITING_INPUT`，未直接标记为该控制动作失败 |
| 4 | 补充后原 Task 从保存位置恢复 | PASS | 同一 `task_id` 追加 `input_supplied`、`execution_resumed` |
| 5 | 人工接管后 AI 停止 | PASS | 接管状态仅提供接受、转派、恢复、取消；未自动继续 |
| 6 | 恢复不创建重复 Task | PASS | 恢复前后 URL、`task_id` 均一致 |
| 7 | 刷新/重启不丢状态 | PASS | 浏览器刷新及官方服务停止/启动后仍为原暂停状态 |
| 8 | Tenant fail-closed，无敏感泄露 | PASS | 全量回归通过；UI 仅展示结构化事件/安全摘要，未见 Prompt、回答、密钥、凭证或隐藏思维链 |
| 9 | 聚焦测试、迁移、变更说明 | PASS | 系统交付席聚焦测试通过；additive migration 与变更说明已随 Issue 交付 |
| 10 | 全量回归、真实浏览器、Review | PASS | 本 Review 记录最终冻结源码后的独立证据 |

## Security Boundary

- 所有控制记录和事件保留 `tenant_id`，跨租户访问保持 fail-closed。
- 接管人转派限定为当前 Tenant 的 Local Owner。
- 敏感字段检查覆盖嵌套及 camelCase 形式。
- 控制写入使用状态前置条件，避免旧页面覆盖较新的执行状态。
- `model_called` 只引用 `usage_record_id`；Token/成本仍以 `ai_usage_records` 为唯一事实源。
- 浏览器页面未展示 Prompt、模型完整回答、隐藏思维链、密钥、Credential 或原始供应商响应。
- 安全边界席最终回传：`PASS`。

## Known Limitations / Blocker

`BLOCKED_L2_LIVE_VALIDATION`：

- 当前官方本地运行环境未配置真实模型 Gateway/Provider。
- 无法在本轮取得“供应商成功响应 -> AIUsageRecord -> model_called timeline”的真实正向证据。
- 系统已正确 fail-closed，返回真实 attribution error；未知 Token/成本未被伪造为 `0`。
- 解锁需要 Owner 在既有安全凭证边界内提供可用模型配置，再由质量运行席仅补跑真实模型正向链。

## Review

本地执行控制闭环准予进入产品规划席验收；不得把本结论表述为真实外部模型链已完成。

Next Seat: 产品规划席
Handoff: sent to main thread for 产品规划席 routing
