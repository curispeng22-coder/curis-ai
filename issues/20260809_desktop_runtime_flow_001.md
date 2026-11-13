# DESKTOP-RUNTIME-FLOW-001

Status: Completed (local flow; external release gates open)  
Decision: `PASS_DESKTOP_RUNTIME_FLOW_WITH_EXTERNAL_RELEASE_BLOCKER`

## 1. 目的

补齐真实 Desktop 的第一条可用经营链：CEO 建立 Company 后，可以从工作空间门户进入 Workspace Studio，创建第一间真实 Business Workspace，并进入对应运行现场。修复 Desktop WebView 通过本地 Gateway 读取 Runtime 时的跨源预检失败。

## 2. 已知事实与根因

- Runtime Foundation API 已提供 tenant-scoped Workspace 创建契约；当前 Workspace Studio 仍调用旧 Project API。
- Workspace Portal 在 Company 已建立但没有 Workspace 时只有空态，没有进入 Studio 的动作，CEO 无法继续经营。
- Desktop 前端位于 `127.0.0.1:3010`，Runtime Gateway 位于 `127.0.0.1:8080`；带租户头的 fetch 会触发 OPTIONS 预检。
- Gateway 之前把 OPTIONS 转发给 Runtime，后端返回 400；并且上游 CORS 头与 Gateway 头可能重复，WebView 会拒绝响应。

## 3. 允许范围

只允许修改：

- `desktop/runtime/gateway.py`
- `frontend/lib/runtimeApi.js`
- `frontend/app/ceo-office/workspace/page.js`
- `frontend/app/ceo-office/workspace/studio/page.js`
- 本 Issue 对应的 Review、Current State 与 Change Log 记录

不得修改：Backend Runtime 契约、活动数据库、旧 Project / Task 迁移、真实平台 API、商业化 Admin、导航模型之外的新增一级栏目。

## 4. 验收条件

1. Gateway 对受信任 Desktop Origin 的 OPTIONS 返回 204，并在代理响应中只保留一组 CORS 头；非 Desktop Origin fail-closed。
2. fresh Desktop 首次进入显示“公司尚未建立”，不生成示例 Company / Workspace。
3. 通过 Founding Guide 建立 Company 后，Workspace Portal 空态提供进入 Workspace Studio 的动作。
4. Studio 使用 Runtime Workspace API 创建 RD / XHS / TTK 之一，保存真实 Blueprint 版本；不得调用旧 Project API。
5. 创建成功后进入对应 Workspace Runtime 页面；刷新后从 Runtime 恢复，Company / Workspace / Blueprint 隔离仍成立。
6. 本地 Desktop 重新打包，fresh HOME、单实例、退出清理、Runtime API、真实窗口可访问均有证据。

## 5. 不在本 Issue 内

- Workspace Studio 的拖拽装修、AI 员工装配、Simulation 执行 UI 的完整建设；本 Issue 只建立最小可用创建入口。
- Developer ID、Hardened Runtime、公证、staple、Gatekeeper 与最终分发 DMG；这些仍属于外部发布门。

## 6. 交付结果

- Gateway 受信任 Desktop Origin 的 OPTIONS 返回 204，代理响应只保留一组 CORS 头；非 Desktop Origin fail-closed。
- fresh 隔离 HOME 的真实窗口完成“空公司 → Founding Guide → Company → Workspace Portal → Studio”。
- Studio 通过 Runtime Workspace API 创建研发、小红书、抖音三类 Workspace，分别进入对应 Runtime 页面；未调用旧 Project API。
- 前端 Runtime 测试 `12 passed`、Python `py_compile`、Rust `cargo check`、Next `44/44` build、scoped ESLint 通过。
- app 与手工 DMG 已重新生成；退出后 `8002/8080/3010` 不可连接且无 Curis sidecar / guardian 孤儿。
- 完整证据记录于 `docs/reviews/20260809_desktop_runtime_flow_001_review.md`；Developer ID、公证、staple、Gatekeeper、`/Applications` 安装仍未关闭。
