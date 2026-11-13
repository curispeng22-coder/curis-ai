# Workspace R1 统一运行基线

- 日期：2026-07-17
- 状态：CLOSED — PASS
- 固定分支：`feat/roadmap-r1r2`
- Owner：系统交付席
- Review：质量运行席 → 产品规划席
- 前置：`20260717_workspace_tenant_identity_membership_implementation` 已 L2 PASS

## 目标

把 Admin 与 Workspace 固定到同一可复现修订，形成唯一数据库、进程、端口、前端目录、启动命令和测试命令。只修运行基线，不开发新功能。

## 已有事实

- Admin R1/R2 已提交在当前分支；Admin 后端端口基线为 8001。
- Workspace 后端端口基线为 8002；可信 Gateway 本地端口为 8080。
- Admin 默认弱令牌修复已在当前分支提交。
- L2 身份、membership、TenantContext 与 Gateway 已通过安全和质量复核，但仍需形成固定提交。

## 必须完成

1. 把已验证 L2 工作树按批准文件范围形成独立提交；不得夹带无关改动。
2. 记录唯一基线 commit，后续所有启动、测试、Review 均使用该 commit。
3. 明确并验证 Admin 与 Workspace 使用不同数据库文件；不得共享或隐式回落到同一 DB。
4. 明确并验证 Admin、Workspace 两个后端进程、端口和启动命令；端口冲突必须启动前失败。
5. 明确 Admin 与 Workspace 两个真实前端目录、安装、启动和构建命令。
6. 固化仓库已有能力优先的一键本地启动/停止入口；不得新增不必要依赖。
7. 恢复并记录后端测试环境；系统交付席只跑聚焦启动/边界检查，质量运行席负责一次全量回归、两个前端构建和必要 E2E。
8. 复核 Admin 未配置管理员令牌时拒绝请求/严格模式拒绝启动，不存在默认弱口令。
9. 输出唯一运行基线文档和 Review，包含 commit、DB、端口、目录、命令、测试结果和已知失败。

## 允许修改

- 现有启动/停止脚本、部署配置和环境变量示例。
- 与数据库路径、端口冲突、测试环境或 Admin 弱令牌基线直接相关的最少文件。
- `docs/runbooks/` 或仓库现有同类运行文档。
- 本 Issue 对应 Review。

## 禁止范围

- 不开发前端页面、业务 API、资产功能、Workflow Runtime 或计费能力。
- 不进入 R2 资产修复或 R3 纵向 E2E。
- 不切换分支，不覆盖其他席位未提交改动。
- 不把 mock、TestClient 或单进程结果写成双产品真实启动成功。
- 不写入真实密钥、token 或生产凭据。

## 验收标准

- 同一 commit 可启动 Admin 后端、Workspace 后端和需要的 Gateway。
- Admin DB 与 Workspace DB 路径明确且不同；数据互不串读。
- 8001/8002/8080 端口角色明确，重复占用时 fail-fast。
- Admin、Workspace 前端目录真实存在，质量席独立构建通过或给出精确阻塞。
- 一条启动命令和一条停止命令可复现整套本地基线。
- Admin 弱令牌边界验证通过。
- 后端聚焦检查通过；质量席记录全量通过/失败/跳过数并确认无新增基线回归。
- Review 明确结论；未满足任一项不得进入 R2。

## 预期交接

系统交付席回传：提交 SHA、变更文件、启动/停止命令、DB/端口/前端目录、聚焦证据。完成后直接交质量运行席；质量运行席更新 Review 并回产品规划席。

## 产品验收

- 固定提交：`306b9a1182d2a8a510154cdb6883009459e70728`。
- 启停、重复启动 fail-fast、端口、双数据库隔离、Admin 弱令牌边界均通过。
- 聚焦 10 passed；全量 599 passed / 19 failed / 0 skipped，无 R1 新增失败。
- Admin 与 Workspace 两个前端 build 均通过。
- 质量 Review：`reviews/20260717_workspace_r1_unified_runtime_baseline_review.md`，结论 PASS。
- R1 关闭；允许进入 R2，仍禁止进入 R3。
