# THREE-BUSINESS-WORKSPACE-UI-001 Review

Status: Review  
Decision: `PASS_THREE_BUSINESS_WORKSPACE_RUNTIME_UI`  
Date: 2026-08-09

## 结论

PASS。Workspace Portal、研发办公室、小红书运营办公室、抖音 / TikTok 运营办公室已在同一
Company OS shell 内消费真实 Runtime 投影。未建立新的 Company / Workspace / Assistant 系统，未把
Project / Task、mock、fixture 或浏览器状态作为业务事实。

## 实际改动文件

- `frontend/lib/runtimeApi.js`
- `frontend/lib/assistantState.mjs`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/app/ceo-office/workspace/page.js`
- `frontend/app/ceo-office/workspace/software/page.js`
- `frontend/app/ceo-office/workspace/xhs/page.js`
- `frontend/app/ceo-office/workspace/shortvideo/page.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/20260809_three_business_workspace_ui_001.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`
- `reviews/20260809_three_business_workspace_ui_001_review.md`

## Runtime 对象映射

| 页面 | 唯一事实投影 | UI 结果 |
| --- | --- | --- |
| Workspace Portal | Runtime Company snapshot + 每个 Workspace detail | 三个真实 Workspace、当前对象、下一检查点、蓝图与 Simulation gate |
| 研发办公室 | RD Workspace + Cycle + SimulationRun | `INTAKE → DESIGN → IMPLEMENT → VERIFY → ACCEPT → REVIEW → IMPROVE → ARCHIVE` 八阶段、Owner、Outcome、Intent、Evidence、ExecutionRef |
| 小红书办公室 | XHS Workspace + ContentItem / Version / Receipt / Interaction / SimulationRun | 独立内容对象、不可变版本、手动回执 `UNVERIFIED`、互动与 `REPLY_POLICY` 版本失效 |
| 抖音办公室 | TTK Workspace + 独立 ContentItem / Version / Receipt / Interaction / SimulationRun | 独立短视频对象；无回执和互动时如实为空，不伪装平台成功 |
| Global Assistant | 根布局共享 Provider / Host + 安全 Workspace 上下文 | 浮层复用；上下文只增加 workspace / business / cycle / content 标识，不形成第三栏 |

## 状态与安全边界

- fresh 临时 SQLite 首次进入显示“还没有公司工作空间”，无惰性 Company 或 Workspace 写入。
- 请求不属于当前 Company snapshot 的 `workspace_id` 显示“无权访问”，不发起跨作用域拼接。
- 跨 Tenant 读取 Runtime Company 返回 `404 {"detail":"运行对象不存在或无权访问"}`。
- Backend 停止后页面显示“运行状态读取失败”，不显示 `Failed to fetch`，浏览器 warning/error 日志为 0。
- XHS Blueprint `v1 → v2` 后，旧 `XHS-001` 明确显示“已失效 / REPLY_POLICY”，历史内容仍标记 v1。
- CEO 手动发布回执显示 `UNVERIFIED`；TTK 无回执时明确说明不会把前端操作伪装为平台成功。
- Assistant Identity 未写死；验证现场显示“未命名 Assistant”，继续使用现有共享浮层。

## 临时数据库与重启证据

验证库：`/tmp/curis-three-workspace-ui-browser.82G9VM/curis.sqlite`

独立 fresh 空态库：`/tmp/curis-three-workspace-ui-fresh-20260809.sqlite`

```text
PRAGMA integrity_check = ok
companies = 1
workspaces = 3
cycles = 1
content_items = 2
content_versions = 2
publication_receipts = 1
interactions = 1
runtime_simulation_runs = 3
invalidated_simulations = 1
RD-001  v1 DRAFT NOT_RUN current
TTK-001 v1 DRAFT NOT_RUN current
XHS-001 v1 DRAFT NOT_RUN invalidated
restart browser recovery = true
fresh integrity_check = ok
fresh companies = 0
fresh workspaces = 0
fresh runtime_entities = 0
```

## 自动验证

```text
node --test tests/runtimeApi.test.mjs tests/runtimeProvider.test.mjs \
  tests/runtimeFirstArrival.test.mjs tests/runtimeMaterialization.test.mjs \
  tests/runtimeWorkspaceUi.test.mjs
18 passed, 0 failed

eslint [本 Issue 八个前端源文件与测试]
PASS（无输出）

NEXT_PUBLIC_API_BASE=http://127.0.0.1:3206 npm run build
PASS（Next production build，Generating static pages 44/44；三条 Workspace 路由均在构建清单）

git diff --check [本 Issue 前端范围]
PASS

Project / Task / TaskLauncher / mock / fixture scope scan
0 matches

Runtime Foundation / Simulation / API / Materialization / First Arrival / Workspace 联合回归
28 passed
```

Node 的 `MODULE_TYPELESS_PACKAGE_JSON` 为既有 package metadata warning，不影响测试结果。
Backend 联合回归仅产生既有 FastAPI lifecycle / asyncio deprecation warnings；无失败。输入阶段的
Workspace Foundation `44 passed` 与全量 `1285 passed, 31 failed, 2 skipped` 基线保持原 Review 归属，
本 UI Issue 未重跑全量 Backend，也未修改其 31 项既有失败。

## 真实浏览器证据

全部来自 Codex In-app Browser、同源代理与临时 SQLite；不是静态原型。

- `/tmp/curis-three-workspace-ui-browser-evidence/01-fresh-empty.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/02-workspace-portal.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/03-rd-cycle-eight-stages.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/04-xhs-content-receipt-interaction-invalidated.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/05-ttk-content-runtime.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/06-ttk-global-assistant-overlay.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/07-workspace-forbidden.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/08-runtime-api-failure.png`
- `/tmp/curis-three-workspace-ui-browser-evidence/09-compact-dark.png`

视口与主题：1440×900、1024×768 均完成真实渲染；主题选择器依次验证 `system`、`light`、
`dark` 为选中态，结束时已恢复 `system`。1024 深色证据见 `09-compact-dark.png`，Assistant 仍为
浮层入口，没有形成第三栏。

## Pre-existing diff 与活动库分离

- 本 Issue 未修改 `backend/`、`desktop/`、`curis-ui-prototype/`、旧 Project / Task 链或真实平台 API。
- `backend/app/main.py` 等大量既有 dirty diff 保持原样；本 Issue 没有清理、回退或纳入。
- 活动库 `data/curis.sqlite` SHA-256 前后均为
  `c663222af90129012e41b542780c9dffcd302b540e27074a13fbd62cce65321e`。
- 所有业务验证写入仅发生在上述 `/tmp` SQLite。

遗留库边界说明：UI 开始验证时 `backend/data/curis.sqlite` 为 `2ba1f018…`；一次 Backend 联合
pytest 命令未为模块级 `app.main` 显式设置全局 `CURIS_DB`，其 schema 初始化把该遗留库 SHA 漂移为
`6bc1ff46bdd1bc5262c9f5b2b3bf454f0c4c6b002de5f2a01027d28bc978021b`。只读复核为
`integrity_check=ok`、`companies=2`、`workspaces=0`、`runtime_entities=0`、
`runtime_simulation_runs=0`，没有写入本轮三业务验证对象；唯一活动库未变化。由于缺少原字节副本，
本轮没有做猜测性覆盖或回退。该遗留副本不参与产品运行，但此测试环境副作用必须在交接中显式保留。

## 未进入范围

未进入 Backend Runtime、Desktop Packaging、真实小红书 / 抖音 API、旧链删除、平台账号、自动互动或
活动库迁移。下一阶段需独立授权。
