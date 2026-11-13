# Project Owner Workbench Product Flow

## Status

`CLOSED — PASS / USER_FLOW_PASS`

## Parent

`issues/20260722_macos_keychain_google_oidc_project_runtime.md`

## Supersedes

`issues/20260722_macos_keychain_google_oidc_project_runtime.md` 只保留 `PRODUCT_MISMATCH / PARTIAL` 与历史登录 / 首轮运行证据。

总控已裁决选择新产品纵向切片口径：`22bdfcf4` 不在旧 Issue 验收，但其 next-run 新实体 `task-169503a4` / `graph-1d3c4201e22d` 可迁移到本 Issue 复核，作为“项目负责人工作台”的继续动作候选证据。该实体保留，不删除、不回填、不改写。

质量已确认：`22bdfcf4` next-run 可作为本 Issue 的候选证据，但当前实现仍缺双入口与共用结构化确认单，因此结论为 `FAIL / STRUCTURED_CONFIRMATION_MISSING`。后续必须先补齐该产品入口，不得仅凭 next-run 证据收口。

最终质量结论：`PASS / USER_FLOW_PASS`。Delivery SHA `b349b436`（已推送，仅三个获授权前端文件）经独立 Chrome 真链完成：聊天式 / 结构化双入口 → 同一三字段确认单 → 确认生成下一次计划 → 启动 → `7 passed` / `exit0` / `round1` → 成果与 Trace → 批准 → “修改目标并继续”。本次新 Task `task-5506d18e` / Graph `graph-6396d4a85b2e` 仅在折叠证据区；员工、成本、风险按真实记录展示，未知成本不伪造 0。旧 Task `task-169503a4` / Graph `graph-1d3c4201e22d` 保留未改写；`22bdfcf4` 不作为旧 Issue 完成证据。未触模型、RealRD、凭据或身份扩展。

## Objective

把当前 Project Runtime Local 的“运行证据页”收敛成最小“项目负责人工作台”：

负责人可以提出、追加或修改项目目标，也可以直接填写结构化任务；两路最终都进入同一份结构化任务确认单。确认后复用既有 Pipeline / Task / Graph / Workflow 路径启动执行，页面展示目标树、计划、进度、员工分工、成果、成本、风险，以及批准 / 返工 / 再运行动作。

## Product Requirement

首屏必须回答四件事：

1. 这个项目现在要完成什么；
2. AI 公司准备怎么做；
3. 哪些员工 / 能力正在负责；
4. 这次结果是否可用，下一步能做什么。

允许两个输入入口：

- 聊天式目标：一个自然语言输入区，用于“我想让这个项目继续做什么”；
- 结构化任务：目标、验收标准、约束 / 风险三个字段。

两路提交前必须显示同一结构化任务确认单，确认单最少包含：

- 目标；
- 验收标准；
- 约束 / 风险；
- 将创建或继续的项目运行；
- 下一步主动作。

## Implementation Scope

复用现有页面与 API，先做最小前端闭环：

- `frontend-workspace/app/projects/[project_id]/page.js`
- `frontend-workspace/app/projects/[project_id]/projectRuntimeViewModel.mjs`
- `frontend-workspace/app/projects/[project_id]/projectRuntimeViewModel.test.mjs`

优先复用现有接口：

- `PATCH /api/workspace/projects/{project_id}`
- `POST /api/pipeline/submit`
- `POST /api/pipeline/{graph_id}/auto-run`
- `POST /api/pipeline/{task_id}/dispatch`
- `POST /api/pipeline/{task_id}/approve|reject|rework`
- `GET /api/pipeline/project/{project_id}`

不得新增模型调用、凭据、身份范围、RealRD 取证、后端执行器、Workflow 语义或外网。

## Acceptance

浏览器真实验收必须通过同一项目页完成：

1. 登录后进入项目负责人工作台，而不是运行证据页；
2. 聊天式目标和结构化任务两种入口至少各有一个可见路径；
3. 任一路径提交后先看到结构化任务确认单；
4. 确认后生成 / 更新同一项目运行计划；
5. 启动后页面显示计划、进度、员工分工、结果解释和可继续动作；
6. 成功时可批准 / 返工 / 创建下一次运行；
7. 失败时必须用白话说明发生了什么，并给出“修改目标继续”或“重新运行”动作；
8. 不得把 Task ID、Graph ID、trace 证据当作主页面叙事；它们只能放在“运行证据”折叠区。

## Non-goals

- 不做 CEO Office、组织管理、模型 / Agent / Skill / Tool / Credential 配置页。
- 不把测试、trace、Task 状态页包装成产品完成。
- 不新增 mock 交互或假成果。
- 不修 RealRD、模型调用、Key 注入、Google 登录、CORS 或容器问题，除非当前页面动线直接回归。

## Route

系统交付席单主线程实施最小前端闭环并 focused 验证 → 质量运行席只做最终浏览器验收 → 产品规划席收口。
