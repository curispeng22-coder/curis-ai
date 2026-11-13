# MVP Phase 2 / S3 — AI Employee

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase2_s3_ai_employee_review.md`

## Objective

按 Curis v1.0 既定 AI Employee 模型完成：

- T006：从真实部门与员工模板创建员工，配置名称、角色和职责。
- T007：通过现有 Capability Selector 为员工保存人工配置的 Capability Profile。
- T008：在组织中心与员工详情展示真实员工状态。

## Product Boundary

- 固定关系为 `Company -> Department -> Employee -> Capability Profile`。
- Employee 是责任主体，Capability 是员工装备；员工不是 Agent 或 Model。
- 角色由用户选择的员工模板确定，职责保存到现有 `instructions_override`。
- Capability Profile 在 MVP 中复用现有员工能力绑定集合，不新增 Marketplace 或第二套能力系统。
- 项目关系、Memory、自动招聘、智能推荐和自动能力切换不在本 Sprint 实现。
- 不使用示例员工、本地草稿或未提交的 affiliation 实验能力冒充产品功能。

## Implementation

- 员工列表改用共享 API 层读取真实员工、部门、模板和能力绑定。
- 新建员工时选择真实部门、兼容该部门类型的员工模板、填写职责，并可配置能力组合。
- 员工详情读取真实员工与能力绑定；编辑名称、职责、状态和能力组合均写回现有 API。
- 状态按真实值展示：`idle / assigned / completed / error / disabled`；不生成模拟运行状态。
- 删除使用现有员工软删除接口。

## Allowed Files

- `issues/20260729_mvp_phase2_s3_ai_employee.md`
- `reviews/20260729_mvp_phase2_s3_ai_employee_review.md`
- `backend/tests/test_mvp_phase2_s3_ai_employee.py`
- `frontend/app/layout.js`
- `frontend/lib/api.js`
- `frontend/components/terra/TerraPrimitives.js`
- `frontend/app/ceo-office/organization/employees/page.js`
- `frontend/app/ceo-office/organization/employees/EmployeeFormDrawer.js`
- `frontend/app/ceo-office/organization/employees/[id]/page.js`
- `frontend/app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可选择真实部门与兼容模板，创建包含名称、角色和职责的真实员工。
2. 用户可在创建或编辑时保存 Capability Profile；详情展示真实能力名称与类型。
3. 员工列表和详情展示真实状态，支持空闲、工作中、已完成、异常和暂停文案。
4. 用户可真实编辑员工名称、职责、状态和能力组合，并软删除非管理者员工。
5. 组织中心可看到新员工；员工详情不再展示示例快照或本地草稿。
6. 请求保持租户隔离；不新增依赖、数据库表、Workspace/Admin 或 Marketplace。
7. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
