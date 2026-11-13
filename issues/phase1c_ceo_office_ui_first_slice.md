# Phase-1C CEO Office UI First Slice

Status: Approved for implementation

Owner seat: 系统交付席

Product approval date: 2026-07-11

Expected review: `reviews/phase1c_ceo_office_ui_first_slice_review.md`

## Objective

将 Workspace 默认产品入口从 Task-first 操作台调整为第一版 CEO Office，让 CEO 首先看到 Company、当前核心 Project、Organization Health 和 AI 公司运行事实，同时保留既有执行工作台作为次级入口。

## Minimal Context

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/design/phase1c-ceo-office-ui-v3.md`
- `docs/review/dashboard-data-readiness.md`
- `docs/contracts/company-runtime-contract.md`
- `docs/contracts/project-runtime-contract.md`
- `docs/contracts/department-runtime-contract.md`
- `docs/contracts/employee-lifecycle-contract.md`

## Product Scope

首个切片只实现：

1. CEO Office Shell：默认进入 CEO Office；Task/Workflow 操作台保留为次级“执行工作台”入口，不删除现有能力。
2. CEO Briefing：显示当前 Company 名称、状态和基于真实 Project 数据的经营摘要。
3. Core Project Command：显示一个确定性选择的核心 Project，包括目标、状态、负责人、Department、关联 Workflow 摘要和明确风险事实。
4. Organization Health：显示 Department 数量、AI Employee 数量、负责人和可解释的阻塞/等待事实；不展示完整组织树或黑箱健康评分。
5. AI Employee Identity：核心 Project Owner 使用已确认的轻卡通、半写实专业虚拟人物风格，并显示职位、状态和当前 Project；不得使用机器人头像或照片级真人员工照。
6. 完整 Loading、Empty、Error、Partial Data 状态。

## Real Data Sources

仅允许读取现有 Workspace API：

- `GET /api/workspace/companies`
- `GET /api/workspace/companies/{company_id}`
- `GET /api/workspace/companies/{company_id}/departments`
- `GET /api/workspace/projects`
- `GET /api/workspace/projects/{project_id}`
- `GET /api/workspace/departments`
- `GET /api/workspace/employees`
- `GET /api/workspace/workflows`
- `GET /api/workspace/workflows/{workflow_run_id}`，仅在现有详情交互需要时使用

不得新增、修改或假设不存在的 API。不得调用 `/api/platform/*`。

## Deterministic Presentation Rules

- 当前 Company：优先采用 API 返回的默认 Company；若接口未标记默认项，则采用返回顺序中的第一项，并保留 Company 切换的未来扩展位，不在本切片实现复杂切换器。
- 当前核心 Project：优先选择 `active` 且 `updated_at` 最新的 Project；若不存在，选择 `planned` 且 `updated_at` 最新的 Project；仍不存在则显示创建 Project 的真实空状态。
- 战略文案：当前数据模型没有独立 Company `strategic_goal` 时，必须显示为“当前核心项目目标”，使用 Project `goal`；不得将其伪装为公司战略字段。
- Organization Health：只使用 Company、Department、Employee、Project、Workflow 的事实计数与状态，不生成综合评分、预测、绩效结论或 AI 推测。
- 风险：只显示 `blocked` Project、failed Workflow、缺失 Owner 或已有明确错误事实。
- 成本、Value、Knowledge：首个切片不显示自动聚合数值；不得使用示例数据补位。

## Page And Interaction States

- Loading：保持稳定布局骨架，不显示虚构数字。
- Empty Company：显示创建第一家 AI 公司的真实入口；不得回退到创建 Task。
- Empty Project：显示创建 Project 入口；Task 不作为替代主入口。
- Partial Data：已成功的数据正常展示，失败区域显示局部错误和重试，不阻塞整个 CEO Office。
- Error：说明读取失败并提供重试；错误信息不得包含密钥、Provider 原始响应或内部敏感配置。
- Execution Workspace：既有 Task / Workflow 操作保持可访问，但不再作为默认首屏。

## Non-Goals

- Decision Center、Important Reports Inbox、Strategic Meeting Room、Brainstorm Room 的正式功能。
- Dashboard Widget 编辑器或自由布局。
- 完整 Organization Tree、组织图、员工 CRUD 重构或复杂 Employee Profile。
- 后端、API、数据库、持久化、Task Execution、Workflow Runtime、Employee Runtime 或 Credential Vault 修改。
- Admin Platform、Billing、Payment、Invoice、Marketplace、ROI 或新业务模块。
- Mock 数据、演示假数据或前端生成经营结论。

## Allowed Files

- `frontend/app/page.js`
- `frontend/app/layout.js`
- `frontend/app/globals.css`
- `frontend/app/taskViewModel.mjs`
- `frontend/app/taskViewModel.test.mjs`
- `frontend/app/ceo-office/**`
- `frontend/public/ai-employees/**`，仅用于符合已批准风格的 AI Employee 视觉资产
- `reviews/phase1c_ceo_office_ui_first_slice_review.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

任何其他文件都必须先由产品规划席确认；后端和 `frontend/app/platform/**` 明确禁止进入本 Issue。

## Visual Acceptance

- 首屏第一视觉信号必须是 Company、当前核心项目目标和 AI 公司状态，不是 Task 输入框或 KPI 卡片网格。
- 页面应呈现柔和深色、克制玻璃质感、充分留白和高级企业总部空间；不得使用军事控制中心式纯黑高压视觉。
- 首页最多展示三个 Department 健康摘要，不展开完整员工树。
- Project 信息明显强于 Token、成本或系统指标。
- AI Employee 使用轻卡通、半写实的专业虚拟人物风格；AI 身份通过职位、徽章、Persona/Skill 信息表达。
- 不使用卡片套卡片，不将所有模块做成等宽 Dashboard 卡片。
- Desktop、Tablet、Mobile 均不得出现文字溢出、重叠或主要操作不可达。

## Acceptance Criteria

1. `/` 默认进入 CEO Office，而不是 Task-first 操作台。
2. CEO Office 只使用本 Issue 列出的真实 Workspace API。
3. Company、核心 Project、Organization Health 和 AI Employee Owner 正确展示且遵守 tenant 范围。
4. 核心 Project 选择规则可由单元测试复现。
5. Company 无独立战略字段时，UI 明确使用“当前核心项目目标”。
6. Task / Workflow 操作台仍可通过次级入口访问，现有执行能力不回归。
7. Loading、Empty、Error、Partial Data 状态均可验证。
8. 页面不出现 Decision/Report/Meeting/Brainstorm 假交互或 Mock 经营数据。
9. Workspace 前端无 `/api/platform/*` runtime 调用。
10. 前端单测、lint、build、浏览器桌面/移动验证和 `git diff --check` 通过。

## Verification

- `cd frontend && node --test app/taskViewModel.test.mjs`
- `cd frontend && pnpm lint`
- `cd frontend && pnpm build`
- 浏览器验证 Desktop `1440x900`、Tablet `1024x768`、Mobile `390x844`
- 检查默认首屏、局部错误、空 Company、空 Project 和执行工作台回退路径
- `rg -n '/api/platform/' frontend/app --glob '!platform/**'`
- `git diff --check`
- Commit 范围必须只包含 Allowed Files；既有删除项和未跟踪目录不得混入

验证命令裁决：`frontend/package.json` 当前没有 `test` script，`pnpm test` 不构成测试执行证据。本 Issue 不扩大 Allowed Files，也不修改 `package.json`；前端单测的正式验收命令固定为现有 Node Test Runner 命令。Phase-1C 新增的 view-model 覆盖必须写入 `frontend/app/taskViewModel.test.mjs`。如后续确需调整测试目录或 package script，必须由产品规划席单独修改 Issue 边界。

## Completion Notes

- 系统交付席实现后路由至质量运行席。
- 质量运行席将证据写入 `reviews/phase1c_ceo_office_ui_first_slice_review.md`。
- 产品规划席根据 Review 验收；未经产品验收不得继续 Decision Center、Important Reports、Strategic Meeting Room 或 Brainstorm Room。
