# UI-RUNTIME-MIGRATION-001 Final Review

Status: Review

Decision: `READY_FOR_INDEPENDENT_UI_REVIEW_WITH_BASELINE_BLOCKERS`

Date: 2026-08-09

Issue: `issues/20260809_ui_runtime_migration_001.md`

Input: Runtime API `PASS_RUNTIME_API_WITH_BASELINE_BLOCKERS`

## Scope

本轮只完成 Company OS 首批前端 Runtime 迁移：Founding Guide、CEO 工作台、业务版图、Workspace Portal 和共享 Global Assistant。未修改 Backend、Desktop、`curis-ui-prototype/`、活动数据库、真实平台 API 或清单外业务文件；旧 Project / Task / Execution 路由保留，只移入兼容入口。

## Actual Changed Files

- `frontend/app/layout.js`
- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/RuntimeProvider.js`
- `frontend/components/runtime/RuntimeStates.js`
- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/components/terra/TerraShell.js`
- `frontend/components/terra/TerraSidebar.js`
- `frontend/components/terra/TerraNavData.js`
- `frontend/app/onboarding/page.js`
- `frontend/app/ceo-office/page.js`
- `frontend/app/ceo-office/business/page.js`
- `frontend/app/ceo-office/workspace/page.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeProvider.test.mjs`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`
- `reviews/20260809_ui_runtime_migration_001_review.md`

授权但未修改：

- `frontend/app/globals.css`：现有 system / light / dark token 已满足要求，SHA-256 保持 `399d08d6b02fe4544135ef95c6db25f0399789d78857538f5543023e1d3fb845`；
- `frontend/lib/api.js`：继续只复用既有 `workspaceFetch` 与 Assistant Identity；SHA-256 保持输入快照的 `306c0101cb396578f634258982f823e9f0efe6f879aec0613bb5dc93f1feb56e`。

## Runtime Object Mapping

| UI | Runtime source | Projection / action boundary |
| --- | --- | --- |
| Founding Guide | `FoundingRun` | `POST /founding-runs`、`GET /founding-runs/{id}`、`POST /entities/{id}/transition`；URL 保存 `founding_run_id`，刷新后恢复，不以 LocalStorage / 页面内存作为 Company 事实 |
| CEO 工作台 | Company Snapshot | `company`、`assistant`、`organization.employees / role_slots / capability_bindings`、`workspaces`、各 Workspace `SimulationRun`；不读取 Home Summary、Project 或 Task |
| 业务版图 | Workspace + SimulationRun | Workspace 是业务运行单元；展示状态、Simulation 数量、失败 / 失效；API 未提供业务目标 / 结果时明确显示“尚未记录”，不从 Project 反推 |
| Workspace Portal | Workspace + SimulationRun | 根据 `workspace_id` 动态生成 `/ceo-office/workspace?workspace_id=...`；不使用 `project_type` 固定映射；详情展示 blueprint / operating version / simulation gate |
| Global Assistant | Company Snapshot + AI Organization + SimulationRun | Identity 继续使用既有可自定义身份 API；简报、待处理、风险只读 Runtime 投影；共享 fixed overlay，不增加第三栏；执行意图当前 fail-closed，不创建旧 Task 冒充 Runtime 动作 |
| Navigation | Company OS + compatibility | 一级使用 CEO 工作台 / 经营 / 业务版图 / 工作空间；旧项目、旧执行、旧任务流水线保留在“兼容入口” |

`/api/workspace/companies` 仅用于发现当前 Company ID，因为 Runtime API 暂无 tenant company collection；Company、Organization、Workspace 和 Simulation 事实仍全部读取 Runtime Foundation API。

## Browser Evidence

验证环境：`http://127.0.0.1:3011`，1440×900；Backend 使用 `/tmp/curis-ui-runtime-browser.sqlite`，Frontend 使用既有 `/gateway` 同源路径与临时本地转发，不触碰活动数据库。

1. 空公司首次进入：`/tmp/curis-ui-runtime-browser-evidence/01-empty-company-onboarding.png`
2. FoundingRun 创建：`/tmp/curis-ui-runtime-browser-evidence/02-founding-run-created.png`
3. FoundingRun 刷新恢复：`/tmp/curis-ui-runtime-browser-evidence/03-founding-run-recovered.png`
   - URL：`/onboarding?founding_run_id=founding_run-6cc2b336-bc8d-4c3c-b0d9-47a75ed3574b`
   - 刷新后仍为 `INTENT_CAPTURED`。
4. 已有公司 CEO 工作台 + Global Assistant 浮层：`/tmp/curis-ui-runtime-browser-evidence/04-ceo-desk-with-assistant.png`
   - Company=`Curis Runtime Company`；3 Workspace；1 AI Employee；1 WAITING_CEO；1 FAILED；Assistant 浮层打开；最终浏览器 error log=0。
5. 业务版图：`/tmp/curis-ui-runtime-browser-evidence/05-business-map.png`
6. Workspace Portal：`/tmp/curis-ui-runtime-browser-evidence/06-workspace-portal.png`
7. 动态 Workspace Runtime 详情：`/tmp/curis-ui-runtime-browser-evidence/07-workspace-runtime-detail.png`
   - `workspace-rd`、`business-rd`、`blueprint-v1`、`operating-v1`、`RD-001 / WAITING_CEO` 可见。
8. 深色主题：`/tmp/curis-ui-runtime-browser-evidence/08-dark-theme.png`
   - DOM 实测 `data-theme` 依次为 `dark`、`light`、`system`。
9. API 不可用：`/tmp/curis-ui-runtime-browser-evidence/09-api-failure.png`
   - 安全文案“运行状态读取失败 / 运行状态暂时无法读取，请稍后重试”；无底层异常；最终浏览器 error log=0。
10. 跨 Tenant API：`/tmp/curis-ui-runtime-browser-evidence/10-cross-tenant-response.json`
    - 以 `ui-runtime-other` 请求 `company-ui-runtime` 返回 HTTP 404：`{"detail":"运行对象不存在或无权访问"}`。
11. 未授权 UI 投影：`/tmp/curis-ui-runtime-browser-evidence/11-unauthorized-state.png`
    - 安全文案“无权访问 / 无权访问该运行对象，或对象已不存在”；最终浏览器 error log=0。

首次浏览器验证直接跨端口调用 Backend，预检 `OPTIONS /api/workspace/companies` 返回 400。该阻塞属于验证启动方式偏离官方同源 Gateway，不是 Runtime UI 逻辑。复验改用项目既有 `/gateway` 路径和临时本地转发后通过，未修改 Backend 或 `next.config.js`。过程中发现即时失败响应会先于子树 hydration 替换 Loading；已在授权的 `RuntimeProvider` 中延后首次读取 250ms，最终 success / failure / forbidden 新页签均无 hydration error。

## Temporary SQLite Evidence

```text
database=/tmp/curis-ui-runtime-browser.sqlite
integrity_check=ok
companies=1
workspaces=3
runtime_entities=5
simulations=3
transitions=10
founding=('COMPANY_CREATED', 'company-ui-runtime')
simulation_states=[
  ('RD-001', 'WAITING_CEO', 'IN_PROGRESS', 'CEO_SCOPE_REQUIRED'),
  ('TTK-001', 'DRAFT', 'NOT_RUN', None),
  ('XHS-001', 'FAILED', 'FAIL', 'PLATFORM_RECEIPT_MISSING')
]
entity_types=[AI_EMPLOYEE, CAPABILITY_BINDING, CEO_ASSISTANT, FOUNDING_RUN, ROLE_SLOT]
```

这些记录只用于浏览器投影验证，不是活动数据、真实平台回执或产品业务成果。空公司场景先在同一临时数据库建立并刷新恢复 FoundingRun，随后才由可信 Backend 测试脚本推进和物化 Company，以验证已有公司页面。

## Tests

```text
node --test frontend/tests/*.test.mjs
16 passed, 0 failed

npx eslint <本 Issue 14 个前端实现/测试文件>
0 errors, 0 warnings

npm run build
compiled successfully; 44 routes generated

backend/.venv/bin/python -m pytest -q \
  backend/tests/test_runtime_foundation_api.py \
  backend/tests/test_three_business_runtime_simulations.py \
  backend/tests/test_runtime_foundation_state_contracts.py \
  backend/tests/test_runtime_foundation_persistence.py \
  backend/tests/test_runtime_foundation_isolation.py \
  backend/tests/test_runtime_foundation_simulation.py \
  backend/tests/test_runtime_foundation_legacy_adapter.py \
  backend/tests/test_state_machine.py \
  backend/tests/test_integration_baseline_fixes.py::SchemaGovernanceTests::test_fresh_and_upgraded_schema_match_and_record_version
35 passed
```

全仓 `npm run lint` 仍为既有 `5 errors, 1 warning`，全部位于封闭清单外：

- `frontend/app/ceo-office/execution/page.js`
- `frontend/app/ceo-office/knowledge/page.js`
- `frontend/app/ceo-office/organization/page.js`
- `frontend/components/terra/FirstRunGate.js`
- `frontend/components/terra/TaskLauncher.js`

本 Issue 未越权修复或掩盖这些基线问题。

## Pre-existing Diff Separation

- 输入前已 dirty 且本 Issue 内授权改写：
  - `frontend/app/ceo-office/page.js`：输入 SHA-256 `36656937...`，当前 `9d40784d...`；
  - `frontend/app/onboarding/page.js`：输入 `c116b415...`，当前 `48158a2f...`；
  - `frontend/components/terra/TerraNavData.js`：输入 `ce722d38...`，当前 `4add9179...`；
  - `frontend/app/ceo-office/workspace/page.js`：输入为未跟踪文件 `b796eb64...`，当前 `6a4f85e6...`。
- 输入前已 dirty 但本 Issue 未写：`frontend/lib/api.js`，SHA-256 始终为 `306c0101...`。
- 输入前 clean 且本 Issue 修改：layout、GlobalAssistant、TerraShell、TerraSidebar；globals 保持 clean / 原哈希。
- 未执行 reset、checkout、删除清理或活动数据库写入；仓库中其他大量既有 dirty / untracked 文件原样保留。

## Known Limitations / Blockers

1. Runtime API 没有对前端开放 `CEO_CONFIRMED → COMPANY_CREATED` 的 SYSTEM 物化命令。Founding Guide 如实停在“等待 Runtime 系统动作”，不调用旧 `createCompany()` 伪装成功。该缺口需独立 Backend Issue 与授权。
2. Runtime API 尚未投影 Business objective / outcome，因此业务版图明确显示“尚未记录”；没有从 Project 反推。
3. 当前 Assistant 执行意图 fail-closed，只开放 Runtime 查询；没有把旧 Task Command 伪装成目标 Runtime 指令执行。
4. RD / XHS / TTK Workspace 运行细节、平台账号、真实回执和外部消息未开发；静态旧路由只作为兼容入口保留。
5. 全仓 ESLint 的 5 个既有错误和 1 个 warning 未获本 Issue 授权修复。
6. 未进入 Tauri / `.app`，不得宣称目标 Desktop 产品完成。

## Final Decision

实现席结论：`READY_FOR_INDEPENDENT_UI_REVIEW_WITH_BASELINE_BLOCKERS`。

## Independent Review

主线程于 2026-08-09 完成独立复核：

- scoped Runtime UI tests：`9 passed`；
- Next build：成功，生成 `44 routes`；
- 浏览器证据、临时 SQLite 隔离、成功 / 失败 / 越权状态与错误日志均符合 Issue；
- 未发现清单外前端实现变更，也未进入 Backend、Desktop、原型或活动数据库。

独立决定：`PASS_UI_RUNTIME_WITH_BASELINE_BLOCKERS`。

Company 物化命令缺口、全仓清单外 ESLint 基线问题、三业务 Workspace 细节和 Desktop 均保留为后续明确边界，不在本 Issue 内伪装完成。Issue 已关闭；下一步应先单独评审 Company 物化 Runtime API，再并行进入 RD / XHS / TTK Workspace UI 设计与实现，最后才进入 Desktop 壳接入。
