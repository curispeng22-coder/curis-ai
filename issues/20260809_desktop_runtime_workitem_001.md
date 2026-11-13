# DESKTOP-RUNTIME-WORKITEM-001

Status: Completed (local runtime object creation; execution gates open)  
Decision: `PASS_DESKTOP_FIRST_WORKITEM_WITH_SIMULATION_GATE`

## 1. 目的

让刚创建的真实 Workspace 不停在空壳运行现场。CEO 进入研发、小红书或抖音办公室后，
可以创建第一条真实运行对象，并在刷新后继续看到它。

## 2. 允许范围

只允许修改：

- `frontend/lib/runtimeApi.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应的 Review、Current State 与 Change Log 记录

复用已通过 Review 的 Runtime API：

- RD：`POST /workspaces/{workspace_id}/cycles`
- XHS / TTK：`POST /workspaces/{workspace_id}/content-items`

不得修改 Backend 契约、数据库、旧 Project / Task 链、真实平台 API、外部分发签名或新增一级导航。

## 3. 产品边界

- 研发创建对象为首个 Cycle“完善 Curis”，初始状态保持 `PLANNED`。
- 小红书 / 抖音创建对象为 ContentItem，初始状态保持 `IDEA`，内容版本保持 `READY` / `UNVERIFIED`。
- 创建对象不自动通过 Simulation、不生成外部平台回执、不伪造结果、不自动发布。
- 所有用户输入必须持久化到 Runtime；刷新、重新打开和错误重试都只读取 Runtime 事实。

## 4. 验收条件

1. 三个 Workspace 的空态均提供真实创建入口。
2. RD 创建后显示 Cycle、八阶段、负责人、目标和 `PLANNED` 状态。
3. XHS / TTK 创建后显示 ContentItem、版本和平台类型，不能出现平台成功或互动数据。
4. 创建请求使用 tenant-scoped Runtime API，不调用 Project / Task API。
5. 前端测试、Next build、scoped ESLint 和隔离 Desktop 真实窗口验证通过。

## 5. 交付结果

- 三个 Workspace 空态均提供真实创建入口。
- RD 真实窗口创建“完善 Curis” Cycle，状态保持 `PLANNED`，八阶段和 CEO Assistant 责任可见。
- XHS / TTK 真实窗口分别创建 ContentItem，状态保持 `IDEA`，版本为 `READY / UNVERIFIED`，无平台回执和互动数据。
- Runtime 前端测试 `13 passed`、Next `44/44`、scoped ESLint 通过；隔离 Desktop 真实窗口链通过，活动库 SHA 未变化。
- 证据记录于 `docs/reviews/20260809_desktop_runtime_workitem_001_review.md`。
