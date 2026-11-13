# MVP Phase 3 / S4 — Project

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase3_s4_project_review.md`

## Objective

按 Curis v1.0 既定 Project 模型完成：

- T009：创建包含目标、归属部门、项目负责人以及资料/成果容器的真实项目。
- T010：以统一项目骨架提供概览、任务、资料、成果和数据视图。

## Product Boundary

- Project Center 负责创建、查找和进入项目；真实业务执行发生在 Project Workspace。
- Project Workspace 是目标到成果之间的工作空间，不是 Task 列表或 Workflow 管理器。
- 本 Sprint 复用既有 Project CRUD、员工负责人和 Task 查询底座，不新增数据库表或第二套项目服务。
- 当前持久化团队关系只使用既有 `owner_employee_id`；不依赖未提交的 affiliation 实验能力。
- Task 创建/执行、异步 `job_id`、Artifact/Knowledge/Memory 独立对象、Business Template 自动生成和经营指标接入不在本 Sprint 实现。
- 所有缺失数据使用真实空状态或 `未记录/未分配`，不展示示例项目、模拟进度或本地草稿。

## Implementation

- 项目中心改用共享 API 层顺序读取真实 Company、Department、Employee 和 Project。
- 创建项目写入既有 Project API，保存名称、目标、描述、部门、负责人和规划中状态，成功后进入项目工作台。
- 项目卡片展示真实部门、负责人和状态，不生成进度、风险或经营数据。
- 项目工作台读取真实 Project 与项目 Task，提供概览、任务、资料、成果和数据容器。
- 资料、成果与业务数据未有独立持久化对象时展示明确空状态和后续 Sprint 边界。

## Allowed Files

- `issues/20260729_mvp_phase3_s4_project.md`
- `reviews/20260729_mvp_phase3_s4_project_review.md`
- `backend/tests/test_mvp_phase3_s4_project.py`
- `frontend/lib/api.js`
- `frontend/components/terra/TerraPrimitives.js`
- `frontend/app/ceo-office/projects/page.js`
- `frontend/app/ceo-office/projects/ProjectFormDrawer.js`
- `frontend/app/ceo-office/projects/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可选择真实部门及该部门员工负责人，创建包含名称、目标和描述的真实项目。
2. 新项目出现在项目中心和所属部门分组，并可直接进入真实项目工作台。
3. 项目工作台展示真实目标、部门、负责人、状态和项目 Task。
4. 项目工作台包含任务、资料、成果和数据视图；无持久化事实时显示真实空状态。
5. 项目中心和工作台不再展示示例项目、本地草稿、模拟进度或硬编码部门/团队。
6. 请求保持租户隔离；不新增依赖、数据库表、Workspace/Admin 或 affiliation 依赖。
7. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
