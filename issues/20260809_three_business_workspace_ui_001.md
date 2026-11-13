# THREE-BUSINESS-WORKSPACE-UI-001：三业务 Workspace Runtime UI

Status: Completed  
Decision: `PASS_THREE_BUSINESS_WORKSPACE_RUNTIME_UI`  
Input: `RUNTIME-WORKSPACE-FOUNDATION-001`  
Owner: Curis 产品 / Runtime / UI 评审  
Date: 2026-08-09

## 1. 背景

Backend Workspace Runtime Foundation 已定义 RD、XHS、TTK 三条业务轨道的 Workspace、Blueprint、
Cycle、ContentItem、Version、Simulation、Receipt 与 Interaction 运行事实，但当前 Draft 不代表其
Review 已通过，也不授权前端实现。

本 Issue 只定义三业务 Workspace Runtime 的 UI 迁移边界。页面必须消费真实 Runtime API 投影，
不得从旧 Project / Task、mock、fixture 或静态原型反推业务状态。

## 2. 前置条件

以下条件必须全部满足，才能把本 Issue 改为 Authorized：

1. `RUNTIME-WORKSPACE-FOUNDATION-001` 独立 Review 必须为 `PASS`；允许保留已明确归属、不会影响
   本 UI 切片的 baseline blocker，但不得保留 Workspace Runtime 契约、隔离、活动库 provenance
   或数据完整性阻塞；
2. 产品负责人明确批准三业务 Workspace UI 进入实施，并冻结封闭文件清单；
3. 实施时使用通过 Review 的 Runtime API / 对象 / 状态契约，不读取未批准草稿或旧链补齐事实；
4. 质量席已登记真实浏览器验证、空 / 失败 / 越权和三业务 Simulation Review 责任。

前置条件未满足时，只允许文档评审，不得修改 frontend、prototype、Desktop、Backend 或活动库。

前置条件现已满足：Runtime Workspace Review Decision=
`PASS_RUNTIME_WORKSPACE_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`，产品负责人已授权以下封闭清单。

## 2A. 允许文件

允许修改：

- `frontend/lib/runtimeApi.js`；
- `frontend/lib/assistantState.mjs`；
- `frontend/app/ceo-office/workspace/page.js`；
- `frontend/app/ceo-office/workspace/software/page.js`；
- `frontend/app/ceo-office/workspace/xhs/page.js`；
- `frontend/app/ceo-office/workspace/shortvideo/page.js`；
- `issues/20260809_three_business_workspace_ui_001.md`；
- `docs/00_Context/CURRENT_STATE.md`；
- `docs/08_Change_Log/CHANGE_LOG.md`。

允许新增：

- `frontend/components/runtime/WorkspaceRuntimeView.js`；
- `frontend/tests/runtimeWorkspaceUi.test.mjs`；
- `reviews/20260809_three_business_workspace_ui_001_review.md`。

禁止修改 Backend、Desktop、prototype、活动数据库、旧 Project / Task / content workflow、
真实平台 API 或清单外文件。保留所有 pre-existing dirty diff。

## 3. 目标

在同一个 Company OS shell 内提供三个具有独立业务语义和空间感的 Workspace：

```text
Company OS
→ Workspace Portal
   ├─ 研发 Workspace：Cycle / 8 Stage / Evidence / CEO 决策
   ├─ 小红书 Workspace：Content / Version / Receipt / Interaction
   └─ 抖音・TikTok Workspace：Content / Version / Receipt / Interaction
```

Company OS shell 保持固定的全局经营语义、导航、主题、身份和 Assistant Host；Workspace 内部允许
根据业务对象、阶段、证据和反馈形成不同视图。不得把三个 Workspace 做成同一张换标题的 Project
看板，也不得复制三套 Company OS。

## 4. UI 范围

### 4.1 Workspace Portal 与办公室视图

- Workspace Portal 只展示真实 Runtime Workspace collection / snapshot；
- 每个 Workspace 卡片至少投影名称、业务类型、运行版本、生命周期、异常、当前对象、下一检查点和
  Simulation 状态；缺失数据明确显示空态，不生成演示数字；
- 进入 Workspace 后保留 Company OS shell，同时让标题、主对象、阶段语言、证据区与反馈区体现
  RD、XHS、TTK 的 Workspace-specific 空间感；
- 旧 Project / Task / Execution 路由只作为兼容或内部执行入口，不得成为 Workspace Portal 的事实源。

### 4.2 RD Cycle Runtime

- 展示真实 Cycle 列表与当前 Cycle，首个工作项语义为“完善 Curis”；
- 展示 `INTAKE → DESIGN → IMPLEMENT → VERIFY → ACCEPT → REVIEW → IMPROVE → ARCHIVE`
  八阶段及当前阶段；
- 展示 outcome、intent、owner、lifecycle / exception、evidence、executionRef、nextCheckAt 和
  Blueprint 版本；
- Project / Task / Workflow 只作为执行引用，不覆盖 Cycle 或 Stage 状态；
- WAITING_CEO、拒绝、失败、版本失效和无证据状态必须如实显示，不允许 UI 自动批准或伪装完成。

### 4.3 XHS / TTK Content Runtime

- XHS 与 TTK 使用各自独立的 ContentItem，不合并为固定内容流水线；
- 展示 ContentItem 生命周期、当前 / 批准 / 发布版本、平台、Owner、异常、验证状态、证据条件和
  nextCheckAt；
- ContentVersion 以不可覆盖的版本历史展示，CEO 拒绝后保留原版本与审计；
- XHS 与 TTK 可共享 UI 原语，但平台语义、回执字段、内容阶段和互动反馈必须来自各自 Runtime 投影；
- 不提供真实平台发布实现，不把前端点击、手动文字或 fixture 标记为平台 VERIFIED。

### 4.4 Simulation / Receipt / Interaction 反馈

- Workspace 详情展示当前 SimulationRun、输入版本、状态、失败原因、CEO 决策、证据引用和失效原因；
- Blueprint 或运行版本变化后，旧 Simulation 必须明确显示失效，不沿用历史 PASS；
- PublicationReceipt 区分平台 API 回执与 CEO 手动反馈，显示来源和验证等级；
- InteractionItem 展示最小互动事实、风险、ReplyPolicy、responseVersion 和处理状态，不创建 CRM；
- 手动反馈只作为未验证事实，不得让需要平台回执的 Simulation 通过；
- 所有写操作只能调用已授权的受控 Runtime API，禁止前端直接写 status、verified、published 或
  approved 字段。

### 4.5 CEO Assistant 浮层

- 继续复用根布局级 Global Assistant Provider / Host，不新增第三栏或 Workspace 专属 Assistant；
- CEO Office 可展示完整 Assistant 面板，Workspace 页面只提供共享浮层入口；
- 页面只向 Assistant 提供安全上下文，例如：

```json
{
  "page": "workspace",
  "company_id": "...",
  "workspace_id": "...",
  "business_type": "RD | XHS | TTK",
  "cycle_id": "...",
  "content_id": "..."
}
```

- Assistant 查询、摘要、通知与命令只读取真实 Runtime 投影；执行命令仍必须进入现有受控 Runtime /
  Task 执行链，不得绕过状态机直接改业务对象；
- 不展示隐藏思维链、密钥、Prompt、原始凭据或跨 Tenant 数据。

## 5. API 与状态边界

- UI 只消费 Tenant / Company / Workspace scoped 的安全 API 投影；
- 必须覆盖 Workspace collection / snapshot、Cycle、ContentItem / Version、Simulation、Receipt 和
  Interaction 的真实读取契约；
- 当前 Backend 未授权的写能力不得由 UI 假按钮、local state 或 mock 补齐；
- 401 进入 Local Owner 登录并返回原页面；403 / 404 / 409 / 422 显示结构化失败或越权状态，
  不显示假成功和泛化 `Failed to fetch`；
- 刷新和服务重启后，页面状态必须从 Runtime API 恢复，不以浏览器内存作为事实源；
- Tenant、Company、Workspace、Cycle、ContentItem 和 Assistant Context 必须 fail-closed，禁止跨作用域拼接。

## 6. 视觉与交互边界

- 固定复用当前 Company OS shell、220px 导航、52px 顶部栏和系统 / 浅色 / 深色三主题；
- Workspace 可以有不同主对象和布局节奏，但不得建立平行导航、独立 Admin 壳或新的产品体系；
- 保持 Desktop First Calm Executive Workspace，不实现 SaaS 后台、BI 仪表盘、ERP 或通用聊天工作台；
- 所有页面提供 loading、真实空态、失败、无权限、版本失效和无可操作权限状态；
- CEO Office 默认只汇总异常、阻塞、成本和结果；底层 Workspace 承载阶段、证据和反馈详情。

## 7. 必须证明

1. Workspace Portal 仅使用真实 Runtime Workspace API，旧 Project / Task 与 mock 扫描为 0；
2. RD、XHS、TTK 三个办公室在同一 Company OS shell 内可辨识且不复制三套产品；
3. RD Cycle 八阶段、证据、失败、CEO 等待 / 拒绝、版本失效和重启恢复正确；
4. XHS / TTK ContentItem、版本、手动 / 平台 Receipt 与 Interaction 各自独立；
5. Simulation PASS、失败、失效和手动反馈不能替代平台验证的边界正确；
6. Assistant 浮层跨三个 Workspace 复用同一 Host，并携带安全页面上下文；
7. fresh 空 Workspace、空对象、API 失败、401、越权、跨 Tenant / Company / Workspace 均有真实浏览器证据；
8. Desktop 1440、紧凑 Desktop 1024 和三主题验证通过，无第三栏 Assistant；
9. scoped tests、ESLint、Next production build 和 Runtime 联合回归通过，既有 baseline blocker 不新增；
10. 测试使用临时数据库和受控 API，不写活动 `data/curis.sqlite`。

## 8. 禁止范围

- 不修改 Backend Runtime、数据库模型、状态机或真实平台 API；
- 不新增 Company、Workspace、Project、Task、Employee、Capability、Assistant 或 Admin 体系；
- 不开发真实小红书、抖音 / TikTok 发布、抓取、账号授权或自动互动；
- 不重做 Company OS shell、产品导航、Global Assistant Runtime 或 Desktop Packaging；
- 不删除旧兼容路由，不迁移或伪造历史数据；
- 不使用 fixture、mock、静态原型或旧 Project / Task 聚合作为产品完成证据；
- 未获得 Authorized 状态和封闭文件清单前不得实施。

## 9. 关闭条件

实施授权后必须生成独立 UI Review，记录：实际改动文件、Runtime 对象与页面映射、三业务差异、
Assistant Context、空 / 失败 / 越权 / 失效状态、真实 API 请求、浏览器截图绝对路径、scoped tests、
ESLint、production build、Runtime 联合回归、pre-existing diff 分离和活动库 SHA。

Review 必须为 `PASS` 后才能把三业务 Workspace UI 描述为完成；完成后暂停，等待 Desktop Packaging
或后续正式授权。

## 10. 完成结论

三业务 Workspace UI 已在封闭文件清单内完成，并由
`reviews/20260809_three_business_workspace_ui_001_review.md` 记录验证证据。页面只读取 Runtime
Company snapshot、Workspace detail 与 Simulation 投影；未修改 Backend、Desktop、prototype、旧链或
活动数据库，未接真实平台 API，也未使用 mock / fixture 伪造状态。
