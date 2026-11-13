# UI-RUNTIME-MIGRATION-001：Company OS 首批 UI 迁移

Status: Completed  
Decision: `PASS_UI_RUNTIME_WITH_BASELINE_BLOCKERS`  
Input: `PASS_TO_UI_RUNTIME_IMPLEMENTATION`  
Owner: Curis 产品 / UI Runtime 评审  
Date: 2026-08-09

按 `docs/reviews/ui-runtime-migration-review-2026-08-09/README.md`，将首次进入、CEO Desk、业务版图、Workspace Portal 和 Global Assistant 接到 Runtime API。三业务 Workspace 细节、真实平台和 Desktop 不在本 Issue。

## 1. 允许文件

### 1.1 允许修改

- `frontend/app/layout.js`
- `frontend/app/globals.css`
- `frontend/lib/api.js`
- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/components/terra/TerraShell.js`
- `frontend/components/terra/TerraSidebar.js`
- `frontend/components/terra/TerraNavData.js`
- `frontend/app/onboarding/page.js`
- `frontend/app/ceo-office/page.js`
- `frontend/app/ceo-office/workspace/page.js`

### 1.2 允许新增

- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/RuntimeProvider.js`
- `frontend/components/runtime/RuntimeStates.js`
- `frontend/app/ceo-office/business/page.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeProvider.test.mjs`
- `reviews/20260809_ui_runtime_migration_001_review.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

## 2. 必须实现

1. Runtime API 客户端统一处理 `X-Tenant-Id`、错误、空状态、加载状态和中文安全错误；
2. Founding Guide 使用 FoundingRun API，不再把 LocalStorage / 页面内存当 Company 事实；
3. CEO Desk 首屏显示 Company Snapshot、AI Organization、Workspace / Simulation 安全投影，并保留 Operating Day 信息层级；
4. Business Map 以业务目标结果和 Workspace 状态为主体，不显示 Project 列表；
5. Workspace Portal 由 Runtime Workspace 生成办公室入口，不按 `project_type` 固定映射；
6. Global Assistant 保留共享浮层，不增加侧栏 / 第三列；上下文来自当前 Runtime 对象；
7. 所有状态动作只调用 Runtime API，禁止前端直接写状态、伪造回执或填充 mock 事实；
8. 统一实现深 / 浅 / 跟随系统三主题、中文文案、220px / 52px Shell 和失败 / 未授权状态；
9. 旧 Project / Task / Execution 路由不删除，只从一级导航移入兼容区；
10. 运行测试覆盖 Runtime API 客户端、空 / 错误状态、Assistant 打开 / 关闭、Workspace 入口和导航结构。

## 3. 禁止范围

- `backend/`、`desktop/`、`curis-ui-prototype/`、活动数据库；
- 真实小红书 / 抖音 / TikTok API、账号授权和外部消息；
- 完整 RD / XHS / TTK Workspace 运行细节（下一 Issue）；
- 删除旧路由、旧表、旧组件或历史文档；
- 新增一级导航、第二套 Assistant 或第二套 Task 系统；
- 清单外任何文件；不得 reset、checkout 或删除 dirty diff。

## 4. 必须证明

- 浏览器：空公司首次进入、FoundingRun 恢复、已有公司 CEO Desk、业务版图、Workspace Portal、Assistant 浮层、API 失败 / 越权；
- Runtime：Company / Assistant / Workspace 来自 API，跨 Tenant / Company 不泄漏；
- 视觉：三主题、中文、主按钮、Shell 尺寸、无第三栏和一致侧栏；
- 兼容：旧 Project / Task 数据不被删除，旧兼容入口仍可达但不再是一级入口；
- 回归：后端既有 API / Foundation / Simulation 聚焦测试不下降，前端测试与构建通过。

## 5. 关闭条件

完成后生成 `reviews/20260809_ui_runtime_migration_001_review.md`，明确浏览器截图路径、页面与 Runtime 对象映射、空 / 失败 / 越权证据、测试结果、未完成的三业务 Workspace 细节。完成后暂停，不进入 Desktop。

## 6. 独立验收

2026-08-09 主线程复核通过：Runtime API 客户端、FoundingRun 恢复、CEO 工作台、业务版图、Workspace Portal、Global Assistant、导航迁移、三主题和安全状态均有代码、测试、构建及浏览器证据。已独立重跑 scoped Node tests（9 passed）与 Next build（44 routes，成功）。

保留阻塞：Runtime API 尚未提供 `CEO_CONFIRMED → COMPANY_CREATED` 的 SYSTEM 物化命令；全仓仍有清单外既有 ESLint 5 errors / 1 warning；三业务 Workspace 细节与 Desktop 不在本 Issue。上述阻塞不否定本 Issue 的 Company OS UI 迁移，但必须在后续 Backend Runtime Issue 与三业务 UI Issue 中闭环。
