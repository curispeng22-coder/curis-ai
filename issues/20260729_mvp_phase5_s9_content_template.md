# MVP Phase 5 / S9 — 内容项目模板真实产出闭环

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase5_s9_content_template_review.md`

## Objective

按 Curis v1.0 既定内容模板完成“热点依据 → 选题 → 平台文案/脚本 → 图片资产 → 复盘计划”真实闭环。

## Product Boundary

- 入口属于现有 Project，Task 仍是内部执行载体；不新增 Workspace、Admin、项目类型或第二套内容运行时。
- 复用 `ContentWorkflowRuntime`、`ContentPublishPackage`、Model Gateway、Task/Execution 与既有内容运行表。
- 热点必须由用户提供可追溯来源与摘要；未接入实时检索前不把模型知识冒充实时热点。
- 仅使用 Task 已人工绑定的 Model Capability；模型未配置、结果非结构化或事实不完整时明确失败。
- S9 产出小红书、抖音、头条的文案/脚本与原生 SVG 图片资产；不模拟图片生成服务。
- 自动发布不属于本 Issue；不调用外部平台、不读取 Cookie、不把预览冒充发布成功。
- 缺失事实显示 `未记录`。

## Implementation

- 新增 Workspace 内容运行入口，校验真实 Project/Task、内容部门、执行员工和 Model Capability。
- 直接复用 Wave-1 `ccp_ai_content_company` 已实例化的内容部门与员工，不增加全局模板种子。
- 扩展既有内容运行时：使用已选模型生成严格结构化内容包，持久化平台文案、SVG 图片与复盘计划。
- Project 任务页提供内容工作流抽屉；完成后进入现有 Task 详情查看真实内容成果与模型用量。

## Allowed Files

- `issues/20260729_mvp_phase5_s9_content_template.md`
- `reviews/20260729_mvp_phase5_s9_content_template_review.md`
- `backend/app/main.py`
- `backend/app/content_workflow_runtime.py`
- `backend/tests/test_mvp_phase5_s9_content_template.py`
- `frontend/lib/content.js`
- `frontend/app/ceo-office/projects/page.js`
- `frontend/app/ceo-office/projects/ProjectFormDrawer.js`
- `frontend/app/ceo-office/projects/[id]/page.js`
- `frontend/app/ceo-office/projects/[id]/ContentRunDrawer.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户从现有内容 Project 选择已绑定模型的真实 Task，填写热点来源、热点摘要和目标平台。
2. 后端仅在 Project/Task、内容部门、执行员工与 Model Capability 全部有效时启动。
3. 同次运行产出可追溯选题、小红书/抖音/头条文案或脚本、每平台 SVG 图片资产和复盘指标。
4. ContentPublishPackage、ContentWorkflowRun、Task、Execution 与模型 Token/成本真实持久化并关联。
5. 模型失败或返回非法结构时 ContentWorkflowRun 与 Task 明确失败，不回退 mock。
6. Task 详情在 Desktop/Mobile 展示热点来源、选题、平台内容、图片、复盘和用量事实。
7. 不新增依赖、数据库表、Workspace/Admin、实时热点伪造或外部发布。
8. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
