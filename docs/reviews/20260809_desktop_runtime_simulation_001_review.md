# DESKTOP-RUNTIME-SIMULATION-001 Review

Status: Completed (local browser gate; packaged Desktop revalidation open)  
Decision: `PASS_LOCAL_DESKTOP_SIMULATION_GATE_WITH_PACKAGED_APP_BLOCKER`  
Date: 2026-08-10

## 1. 结论

三业务 Workspace 已能从真实 Cycle / ContentItem 创建并启动各自的
`SimulationRun`，刷新后恢复同一运行记录。缺少证据与交接时状态保持
`RUNNING / IN_PROGRESS`，界面继续显示“Simulation 未通过”，没有自动 PASS、平台回执或
CEO 验收。

本轮完成的是本地浏览器与临时 SQLite 门禁。当前源码尚未重打包进新的 Curis.app，因此
不把本轮证据描述为新鲜安装包验收；该项保留为 Desktop Packaging 后续门禁。

## 2. 验收证据

- Backend 聚焦回归：`13 passed`（Runtime Foundation API、Execution Adapter、Workspace Foundation）。
- Frontend 聚焦回归：`14 passed`（Runtime API 与 Workspace UI）。
- Scoped ESLint：`frontend/lib/runtimeApi.js`、
  `frontend/components/runtime/WorkspaceRuntimeView.js` 通过。
- Next production build：`44/44` 路由生成通过。
- 1440×900 本地浏览器从 First Arrival 建立 `Curis Simulation Review`，经 Studio 创建三间
  Workspace，并分别建立首个真实 Cycle / ContentItem。
- RD：`RD-001`，Simulation
  `simulation-f53a2428-0985-4ec9-8946-a84e36cb34c1`。
- XHS：`XHS-001`，Simulation
  `simulation-54400803-6d99-402d-af08-c91a19873ea1`。
- TTK：`TTK-001`，Simulation
  `simulation-173368c9-0aad-44f1-b0ee-51021d217444`。
- 三个运行现场刷新后均恢复原 Simulation；Portal 恢复三间 Workspace，没有重复创建。
- 临时库 `/tmp/curis-desktop-simulation.RgnC6f/curis.sqlite`：3 Workspace、3 Simulation、
  8 条 transition audit，`PRAGMA integrity_check = ok`。
- 三条 Simulation 均为 `RUNNING / IN_PROGRESS`，Evidence `0`、Handoff `0`、
  `final_state` 空；未执行无 `workflow_run` 绑定的 AI 员工命令。
- 视觉证据：`/tmp/curis-desktop-simulation-browser-evidence/`。
- `git diff --check`：通过。

## 3. 边界

- 未修改 Runtime 状态机、活动 `data/curis.sqlite`、旧 Project / Task 链、真实平台 API、
  商业化 Admin 或一级导航。
- 浏览器写入仅指向临时 Simulation SQLite；测试结束后已恢复原 `:8000` UI 验证服务。
- 原 UI 验证临时库未写入本轮 Simulation；其服务重启 / SQLite checkpoint 后文件级 SHA 由
  `4c85e433…` 变为当前 `a4ab4455…`，当前 `integrity_check = ok`，且 Simulation 记录为 `0`。
  该临时文件不属于活动库，本 Review 不把字节级 SHA 保护宣称为通过。
- 不把 `IN_PROGRESS`、页面显示、API 成功或本地浏览器证据描述为业务完成。

## 4. 未关闭事项

- 将当前源码重打包后，在隔离 HOME 的新鲜 Curis.app 中重复三业务创建、启动与刷新恢复。
- 三业务真实执行、外部平台回执、失败恢复和 CEO 验收仍由后续独立 Issue / 既有执行桥门禁控制。
- Workspace Studio 深度装配仍需独立 Issue，不在本 Simulation Issue 内扩展。
