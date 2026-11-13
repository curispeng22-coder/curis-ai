# MVP Phase 3 / S5 — Task 与异步执行记录

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase3_s5_task_execution_review.md`

## Objective

按 Curis v1.0 既定 Task 模型完成：

- T011：用户在真实 Project Workspace 创建 Task，并指定该公司可用 AI Employee。
- T012：用户触发非阻塞执行，通过 `job_id` 查询持久化状态、结果或失败原因。

## Product Boundary

- Task 必须属于 Project；创建与执行入口位于 Project Workspace，执行工作台仅聚合真实 Task。
- 复用既有 `tasks`、`executions`、`ResultStore`、`Orchestrator` 和原生 BackgroundTasks，不新增数据库表、服务或依赖。
- `job_id` 复用租户隔离且持久化的 `task_id`，状态由既有 Task 状态机映射。
- 本 Sprint 不实现暂停/恢复、自动拆解、定时任务、自适应执行、Artifact/Knowledge 或外部凭证注入。
- 无执行事实时保持 `未记录`；失败必须展示真实错误，不用样例或模拟成功替代。

## Implementation

- 新增项目 Task 异步启动与查询路由，立即返回 `202`，后台复用既有 Orchestrator。
- 后台执行显式恢复请求租户上下文，查询继续由 ResultStore 做租户隔离。
- 项目工作台新增 Task 创建、执行与状态轮询；执行工作台和 Task 详情改读真实 API。

## Allowed Files

- `issues/20260729_mvp_phase3_s5_task_execution.md`
- `reviews/20260729_mvp_phase3_s5_task_execution_review.md`
- `backend/app/main.py`
- `backend/app/task_jobs.py`
- `backend/tests/test_mvp_phase3_s5_task_execution.py`
- `frontend/lib/api.js`
- `frontend/app/ceo-office/projects/[id]/page.js`
- `frontend/app/ceo-office/projects/[id]/TaskFormDrawer.js`
- `frontend/app/ceo-office/execution/page.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可在真实项目内创建 Task，内容、项目、公司和执行员工持久化且租户隔离。
2. 启动执行立即返回 `202` 和稳定 `job_id`，不等待执行完成。
3. 用户可查询 queued/running/completed/failed，并查看既有状态流、结果或真实错误。
4. 项目工作台、执行工作台和 Task 详情不再展示样例任务或模拟运行。
5. 未产生执行记录时成本和结果显示 `未记录`，未分配事实显示 `未分配`。
6. 不新增依赖、数据库表、Workspace/Admin、暂停/恢复、自动化或外部服务能力。
7. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
