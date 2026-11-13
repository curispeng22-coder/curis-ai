# DESKTOP-RUNTIME-FLOW-001 Review

Status: Review  
Decision: `PASS_DESKTOP_RUNTIME_FLOW_WITH_EXTERNAL_RELEASE_BLOCKER`  
Date: 2026-08-09

## 1. 结论

本地 Desktop 的第一条真实经营链已通过：新安装从空公司进入创办引导，建立 Company 后，
CEO 可在 Workspace Portal 进入 Studio，创建研发、小红书、抖音三类真实 Workspace，并进入
各自 Runtime 运行现场。未使用示例数据、旧 Project API 或活动数据库。外部分发仍未通过
Developer ID、公证、staple、Gatekeeper 与 `/Applications` 安装门。

## 2. 实际变更

仅在授权范围内修改：

- `desktop/runtime/gateway.py`：受信任 Desktop Origin 的 OPTIONS 204；非 Desktop Origin
  fail-closed；代理响应只保留一组 CORS 头，过滤上游重复头。
- `frontend/lib/runtimeApi.js`：增加 Runtime Workspace 创建请求。
- `frontend/app/ceo-office/workspace/page.js`：Company 已建立且无 Workspace 时提供 Studio 入口。
- `frontend/app/ceo-office/workspace/studio/page.js`：从旧 Project/Department 表单切换到
  Runtime Workspace 创建，支持 RD / XHS / TTK 的最小 Blueprint 草稿与首阶段目标。
- `frontend/tests/runtimeApi.test.mjs`：验证 Studio 使用 Runtime Workspace API 且不调用旧 Project API。

Backend、活动数据库、真实平台 API、旧链迁移和商业化 Admin 未修改。

## 3. 验收证据

| 检查 | 结果 |
| --- | --- |
| Gateway 受信任 Origin OPTIONS | HTTP 204，单组 CORS 响应头 |
| 前端 / Runtime 联合测试 | `12 passed` |
| Python 语法检查 | `py_compile` 通过 |
| Desktop Rust | `cargo check` 通过 |
| fresh Desktop 空态 | 显示“公司尚未建立”，Company / Workspace 为空 |
| FoundingRun | 真实窗口完成 `CEO_CONFIRMED → COMPANY_CREATED`，刷新可恢复 |
| Workspace Studio | 真实窗口创建研发、小红书、抖音三间 Workspace |
| Runtime 运行现场 | 三个 Workspace 分别进入 RD / XHS / TTK Runtime 页面，显示草拟状态且无伪造结果 |
| 最终 Workspace Portal | 显示 3 个真实 Workspace、0 个等待 CEO、0 个失败或失效 |
| 生产构建 | Next `44/44` 静态页面通过；scoped ESLint 通过 |
| 应用包 | app 主可执行文件 SHA-256 `20a40bf06ade55d177a39113d937eebfc10849fb9a290099a16920f0bf573c7f` |
| 手工 DMG | SHA-256 `b5ff9495749f10d86df1624f5d924f074c4e0d57b3ea2229fcca2a8da1b01d4e` |
| 退出清理 | `8002`、`8080`、`3010` 不可连接，无 Curis sidecar / guardian 孤儿 |
| 活动库保护 | 使用隔离 HOME；活动 `data/curis.sqlite` 未作为测试目标 |

## 4. 边界与未关闭项

本 Issue 只建立 Studio 的最小可用创建入口，不包含拖拽装修、AI 员工装配、Simulation 执行 UI
或真实平台发布回传。当前 app 仍为本地 ad-hoc 签名，未证明 Developer ID、Hardened Runtime、
公证、staple、`spctl`、Gatekeeper 或 `/Applications` 安装，因此不能标记为最终外部分发完成。

## 5. 后续门

下一步应先由产品负责人验收真实 Desktop 链和三间 Workspace 的体验，再另立 Issue 处理
Workspace Studio 的业务空间装修与 AI 团队装配；外部分发另需真实 Apple 签名与安装证据，
不可用本地手工 DMG 替代。
