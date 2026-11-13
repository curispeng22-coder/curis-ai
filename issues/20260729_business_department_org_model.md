# Business Department Organization Model

Status: IMPLEMENTATION ACCEPTED / BLOCKED_L2

Owner seat: 系统交付席

Product approval date: 2026-07-29

Expected review: `reviews/20260729_business_department_org_model_review.md`

## Objective

将 Local Desktop 单用户产品路径统一为：

`CEO（Local Owner）→ 业务部门 → 员工 / 项目 → 任务 → 成果`

其中员工与项目都直接归属于业务部门；任务属于项目；成果属于任务。

## Product Decisions

- `Company` 保留为兼容与数据隔离聚合根，现有 `companies`、`company_id`、默认 Company 与 tenant 校验不删除。
- Local Desktop 日常组织树不再把 Company 显示为 CEO 下一级；现有公司设置能力保留。
- 业务部门复用 `department_instances`，不创建第二套 BusinessDepartment/Workspace/Admin。
- `owner_employee_id` 仅表示项目负责人，不表示 Project 归属于 Employee。
- 新产品 Task 必须经 Project 创建；历史无 Project Task 保留为内部兼容记录。
- `task.output` 是原始执行输出；只有成功执行后登记、且明确关联 `task_id` 的 Artifact 才是成果。
- Local Owner 认证方案保持不变。

## Task A — Database And API

Allowed files:

- `backend/app/database.py`
- `backend/app/company_project_runtime.py`
- `backend/app/result_store.py`
- `backend/app/main.py`
- `backend/app/routers/home.py`
- `backend/tests/test_business_department_org_model.py`
- `backend/tests/test_phase1a_company_project_runtime.py`
- `backend/tests/test_project_runtime_page.py`
- `backend/tests/test_mvp_phase1_s2_workspace.py`
- `backend/tests/test_mvp_phase5_s10_knowledge_management.py`
- `backend/tests/test_mvp_phase6_s11_basic_memory_context.py`

Acceptance:

1. 旧 Project 的空 `department_id` 幂等回填到其 Company 下可见的“待归属业务部”，不丢数据。
2. 新建 Project 必须选择业务部门，更新时不能清空业务部门。
3. Employee 继续强制主归属 Department；Task 继续从 Project 入口创建。
4. 新增独立 Artifact 持久化，Artifact 必须有 `task_id`；成功 Task 的成果可按 Task 和 Project 查询。
5. 所有查询保持 tenant 隔离；跨部门负责人继续被拒绝。
6. 不修改认证文件或 Local Owner 行为。

## Task B — Frontend Information Architecture

Allowed files:

- `frontend/components/terra/TerraNavData.js`
- `frontend/lib/api.js`
- `frontend/app/ceo-office/page.js`
- `frontend/app/ceo-office/organization/**`
- `frontend/app/ceo-office/projects/**`
- `frontend/app/ceo-office/execution/tasks/**`
- `frontend/app/organizationModel.mjs`
- `frontend/app/organizationModel.test.mjs`

Acceptance:

1. 首页与组织中心以“业务部门”作为 CEO 首层价值创造单元。
2. 首次业务路径明确为业务部门 → AI 员工 → 项目。
3. 员工与项目表单都明确、强制选择业务部门。
4. 业务部门详情先展示直属员工，再展示直属项目。
5. Project 工作台按任务展示真实成果；不把未成功输出或无法确认 Task 的旧内容包冒充成果。
6. 页面不新增 Company 层级，不重设计现有 Terra 视觉体系。

## Task C — Migration And Verification

Allowed files:

- `reviews/20260729_business_department_org_model_review.md`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

Verification:

- Backend 聚焦测试。
- Backend 全量测试一次，由质量运行席执行。
- Frontend tests、lint、build。
- 官方启动链健康检查。
- 浏览器 Desktop 与 Mobile 验收：
  `Local Owner → 业务部门 → 员工 → 项目 → Task → 成果`。
- 重启后关系与成果保持。
- 迁移库中旧项目不丢失、均有业务部门、无伪造 Artifact。
- `git diff --check`。

## Forbidden

- Google OAuth、JWT、Local Owner、trusted identity 与认证中间件修改。
- 新 Workspace/Admin/BusinessDepartment 平行体系。
- 删除 Company 或历史 Project/Task/Content Artifact。
- 新增手工成果编辑器。
- 修改任务执行、模型选择、Capability、Workflow 的既有架构。

## Completion

系统交付席完成 Task A/B 聚焦测试后路由质量运行席。质量运行席只执行一次全量回归、启动链和浏览器验收并写 Review；产品规划席依据 Review 验收。
