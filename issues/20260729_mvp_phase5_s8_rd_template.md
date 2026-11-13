# MVP Phase 5 / S8 — 研发项目模板真实执行闭环

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase5_s8_rd_template_review.md`

## Objective

按 Curis v1.0 既定研发项目模板完成“开发任务 → 代码变更 → 自动测试 → Git 差异 → 运行结果”真实闭环。

## Product Boundary

- Task 仍是内部执行载体，研发入口属于现有 Project；不新增 Workspace、Admin、研发项目类型或第二套 Workflow。
- 复用既有 `wt_rd_pipeline`、`RdWorkflowRuntime`、`RealRDExecutor`、`LocalRDToolset`、Model Gateway、Task/Execution 与 WorkflowRun。
- 代码执行必须受现有 `CURIS_D1_EXECUTE_ENABLED`、`CURIS_D1_FROZEN` 和显式 Workspace Root 约束；未就绪明确失败，不回退 mock/scaffold。
- 开发模型沿用 Task 已人工绑定的 Model Capability；无已配置模型时明确失败。
- 只允许受控文件读写、已登记测试命令和只读 Git 差异；不提供任意 Shell、远程 Git 写入、自动提交、分支或 PR。
- 运行结果展示真实变更文件、测试退出码、Git diff、Token/成本；缺失事实显示 `未记录`。

## Implementation

- 收敛既有研发 Workflow 入口：固定使用 `wt_rd_pipeline`，校验真实 Project Task、所属 Project、研发部门与执行闸门。
- 修正共享研发运行时的真实执行顺序、Project/Task 关联、失败传播与安全结果回写。
- Project 研发入口可选择现有 Task、提交受控目标文件与测试文件，并进入真实 WorkflowRun。
- WorkflowRun 详情读取真实 API，展示步骤、代码差异、测试与模型用量事实。

## Allowed Files

- `issues/20260729_mvp_phase5_s8_rd_template.md`
- `reviews/20260729_mvp_phase5_s8_rd_template_review.md`
- `backend/app/main.py`
- `backend/app/rd_workflow_runtime.py`
- `backend/tests/test_mvp_phase5_s8_rd_template.py`
- `backend/tests/test_rd_workflow_real_rd.py`
- `frontend/lib/development.js`
- `frontend/app/ceo-office/projects/[id]/page.js`
- `frontend/app/ceo-office/projects/[id]/DevelopmentRunDrawer.js`
- `frontend/app/ceo-office/execution/runs/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户从现有 Project 选择真实 Task，提交受控目标文件和已登记测试文件。
2. 后端仅在执行闸门、显式 Workspace Root、真实 Project/Task、研发部门、已配置 Model Capability 全部有效时启动。
3. `wt_rd_pipeline` 的代码步骤经 Model Gateway 与 LocalRDToolset 产生真实代码变更；测试与 Git diff 同次回写。
4. Model、Connector、RealRD 或测试失败时 WorkflowRun 与 Task 明确失败，不把 scaffold、摘要文案或 API 存在当作成功。
5. WorkflowRun 关联原 Project 与 Task，详情展示真实步骤状态、变更文件、测试退出码、Git diff、Token 与成本。
6. 不新增依赖、数据库表、Workspace/Admin、任意 Shell、远程 Git 写入或第二套研发运行时。
7. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
