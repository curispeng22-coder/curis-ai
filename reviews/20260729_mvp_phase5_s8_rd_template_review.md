# MVP Phase 5 / S8 — 研发项目模板 Review

结论：`PASS`

日期：2026-07-29

Issue：`issues/20260729_mvp_phase5_s8_rd_template.md`

## 交付事实

- 现有 Project 可选择已绑定模型的真实 Task，提交受控目标文件、测试文件和最多三轮修复。
- `wt_rd_pipeline` 复用 Model Gateway、RealRDExecutor、LocalRDToolset 与既有 Task/WorkflowRun，真实写入代码、运行测试并记录 Git diff。
- 执行闸门、显式 Workspace Root、研发部门、Project/Task 归属或模型绑定任一无效时 fail-closed。
- WorkflowRun 详情展示六个真实步骤、变更路径、测试退出码、Diff SHA-256、执行模型、Token、成本与轮次。
- 未新增依赖、数据库表、Workspace/Admin、任意 Shell、远程提交、分支或 PR。

## 验证证据

- 聚焦后端：`15 passed`。
- Frontend lint：`PASS`。
- Frontend build：`PASS`，26 个页面生成。
- 隔离干净提交候选全量后端回归：`1128 passed, 3 skipped, 0 failed`。
- 当前共享工作树回归另命中一项越界未提交部门删除文案冲突；该改动不属于本 Issue，未纳入 S8 提交。隔离候选证明 S8 提交内容无回归。
- 真实 Desktop 浏览器：Project → Task → 研发工作流 → `wfr-245da3f6-3773-4095-b0e9-197ba3d9ba1b` 完成；`target_a.py` 产生真实 diff，测试退出码 `0`，Token `120`，成本 `$0.006000 USD`。
- Mobile `390×844`：六步运行、用量与 Git diff 单列可读，导航切换为移动入口。
- `git diff --check`：`PASS`。

## 变更说明

- 收敛研发运行请求为 Project/Task 入口并强化执行前校验与失败回写。
- 修正共享研发运行时的 RealRD 执行顺序、Project 关联和真实结果传播。
- 新增 Project 内研发启动抽屉与真实 WorkflowRun 详情，移除示例运行数据。

Handoff: sent to 产品规划席
