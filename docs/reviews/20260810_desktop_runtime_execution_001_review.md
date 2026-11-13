# DESKTOP-RUNTIME-EXECUTION-001 Review

Status: Completed (runtime bridge; external execution evidence open)  
Decision: `PASS_RUNTIME_EXECUTION_BRIDGE_WITH_EXTERNAL_RESULT_BLOCKER`  
Date: 2026-08-10

## 1. 结论

本 Issue 已把已启动的 Runtime `SimulationRun` 接到现有 Workflow 执行基座，形成
“执行请求 → `ExecutionRef` → 非伪造 Evidence → CEO Review”的第一条可恢复路径。
旧 Workflow 仍只是内部执行载体；Runtime 状态、证据和验收由 Runtime API 控制。

这不是三业务真实外部结果的完成证明：首版只接受显式
`workflow_run:<id>` 绑定，真实工作流必须先存在；小红书 / 抖音仍需要平台授权和
`PLATFORM_API + VERIFIED + SUCCESS` 回执才能 PASS。

## 2. 实际改动

- `backend/app/runtime/execution_adapter.py`：租户 / Company / Workspace / Subject /
  Blueprint 复核、执行幂等、失败收口、`UNVERIFIED` Evidence、Handoff 和审计。
- `backend/app/api/runtime_foundation_router.py`：新增 Simulation execute / CEO review
  命令与安全投影；不返回原始 payload。
- `backend/app/main.py`：仅注入 `workflow_run:<id>` 执行桥，循环现有执行基座至终态。
- `backend/app/runtime/workspace.py`：保存工作项显式 `execution_ref`。
- `frontend/lib/runtimeApi.js`、`frontend/components/runtime/WorkspaceRuntimeView.js`：
  显示“执行 / 待证据 / CEO 验收”并提供显式操作。
- 对应 Backend / Frontend 测试、Issue、Review、Current State、Change Log。

未修改 Runtime 状态机、活动数据库、旧执行表结构、外部平台 API、商业化 Admin 或一级导航。
Blueprint 未另开版本；本实现落实已有 Runtime v1.6 的 ExecutionRef / Evidence / Acceptance 契约。

## 3. 证据

- Backend 聚焦回归：`13 passed`（执行适配器、Runtime API、Workspace Foundation）。
- Frontend 聚焦回归：`13 passed`（Runtime API 与 Workspace UI）。
- `npx eslint lib/runtimeApi.js components/runtime/WorkspaceRuntimeView.js`：通过。
- `npm run build`：Next production build，`44/44` 路由生成通过。
- Runtime 变更后已重建 `.app` 与手工 DMG；DMG SHA-256：
  `bc078a05f323e1f65986f04ea77cdce39dc4ea52b65f0dd237249ec26e320cee`。
- `git diff --check`：通过。
- 执行适配器覆盖：成功生成 `fixture=false / UNVERIFIED` Evidence、重复执行幂等、无绑定阻断、
  执行失败不生成成功证据；API 覆盖 CEO / Tenant / Company / Workspace 作用域和错误映射。

## 4. 未关闭事项

- 尚未在新鲜 Desktop 包内绑定一个真实 `workflow_run` 并完成一次端到端 CEO Review；因此
  “真实 AI 员工已完成业务”仍未宣称。
- 没有真实小红书 / 抖音平台发布、授权、回执、互动或价值反馈；外部结果门保持阻断。
- 当前 UI 只提供 CEO PASS 主路径；失败后的 CEO FAIL / 重试恢复路径留给下一 Issue。
- Desktop 已在本轮前端变更后重打包；仍未在新鲜安装中完成端到端执行 / 浏览器证据，签名、公证、
  staple、Gatekeeper 和 `/Applications` 安装仍属外部分发门。
- 全量 Backend 既有基线失败未在本 Issue 扩大或修复。

## 5. 下一步

1. 重打包 Desktop，在隔离 HOME 中绑定一个真实 `workflow_run`，验证执行、刷新恢复和 CEO Review。
2. 为失败恢复补最小 CEO FAIL / REVIEW_REQUIRED 交互，不扩大成新的任务中心。
3. 再分别接入小红书 / 抖音授权与外部回执，保持平台结果不能由本地 UI 伪造。
