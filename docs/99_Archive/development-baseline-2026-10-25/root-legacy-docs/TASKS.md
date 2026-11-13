# Tasks

Authority Class: HISTORY
Disposition: HISTORICAL / NOT A CURRENT ENTRYPOINT
Navigation updated: 2026-10-25

**以下是原阶段历史记录。** 旧“Current / Active / Next / Read this first”只描述当时状态。
当前请从 [AGENTS](<../../../../AGENTS.md>) → [现有入口](<../../../00_Context/CURIS_CURRENT_ENTRYPOINT.md>)查询；进度只看 [既有执行看板](<../../../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)。
[本轮维护决定](<../../../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)保留原文、原 Status 和历史日期；物理归档尚未执行。候选见 [精确归档清单](<../../../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/PLACEMENT_REVIEW.md>)。

Status: Deprecated

Updated: 2026-07-30

## Active

- 无。

## Next

1. 无。

## Done

- Sprint 0 / T-S0-01：唯一前端入口、CI、发布收敛。
- Sprint 0 / T-S0-02：主数据库固定为 `data/curis.sqlite`。
- Sprint 0 / T-S0-03：实验能力默认禁用。
- Sprint 0 / T-S0-04：静态、构建、后端、启动、浏览器验证 PASS。
- Sprint 0 / T-S0-05：Review 与状态文件更新。
- MVP Phase 1 / S1 / T001：复用并收口单一 App Shell，补齐 AI Assistant Layer。
- MVP Phase 1 / S1 / T002：补齐 Terra 原语和业务卡片，并由员工管理页实际采用。
- MVP Phase 1 / S2 / T003：Company 创建、读取与编辑。
- MVP Phase 1 / S2 / T004：Department 生命周期与受保护删除。
- MVP Phase 1 / S2 / T005：Workspace 首页真实聚合。
- Regression Stabilization：全量回归 1112 passed、3 skipped、0 failed。
- MVP Phase 2 / S3 / T006：从真实部门与兼容员工模板创建员工并保存职责。
- MVP Phase 2 / S3 / T007：复用既有能力绑定保存并展示 Capability Profile。
- MVP Phase 2 / S3 / T008：真实员工状态、编辑、软删除、组织中心同步与租户隔离 PASS。
- MVP Phase 3 / S4 / T009：真实项目创建并保存目标、部门、负责人和说明。
- MVP Phase 3 / S4 / T010：统一项目工作台的概览、任务、资料、成果和数据视图 PASS。
- MVP Phase 3 / S5 / T011：真实项目 Task 创建并指派 AI Employee。
- MVP Phase 3 / S5 / T012：`202 + job_id` 异步启动、状态查询与真实执行记录 PASS。
- MVP Phase 4 / S6 / T013：六类 Workspace Capability Registry 真实注册、详情与启停 PASS。
- MVP Phase 4 / S6 / T014：五个历史 Skill 幂等迁移并保持许可阻断 PASS。
- MVP Phase 4 / S7 / T015：现有 Provider Adapter、Capability Registry 与员工 Capability Profile 接通 PASS。
- MVP Phase 4 / S7 / T016：人工模型选择、单次默认模型回退与真实 Token/成本记录 PASS。
- MVP Phase 5 / S8 / T017：真实 Project Task 经 `wt_rd_pipeline` 完成代码修改与测试 PASS。
- MVP Phase 5 / S8 / T018：Git diff、WorkflowRun、模型 Token/成本与失败事实回写 PASS。
- MVP Phase 5 / S9 / T019：真实内容 Project Task 生成选题、三平台文案/脚本与 SVG 图片 PASS。
- MVP Phase 5 / S9 / T020：ContentPublishPackage、复盘、模型用量与外部未发布事实回写 PASS。
- MVP Phase 5 / S10 / T021：受控本地 Markdown/Text Connector 与真实 KnowledgeEntry 入库 PASS。
- MVP Phase 5 / S10 / T022：手工资料、基础检索、范围筛选与来源详情 PASS。
- MVP Phase 6 / S11 / T023：用户、项目、员工 Memory 创建、更新、检索与隔离 PASS。
- MVP Phase 6 / S11 / T024：Context Package 构建、持久化并进入真实 Task Prompt PASS。
- MVP Phase 6 / S11 / T025：终态 Task 沉淀经验与下一 Task 自动复用浏览器闭环 PASS。
- MVP Phase 6 / S12 / T026：统一加载与可恢复错误体验 PASS。
- MVP Phase 6 / S12 / T027：核心页面稳定性与响应式收口 PASS。
- MVP Phase 6 / S12 / T028：旧 SQLite 备份、幂等迁移与完整性检查 PASS。
- MVP Phase 6 / S12 / T029：旧数据库与 Admin 旧运行文件可恢复清理 PASS。
- MVP Phase 6 / S12 / T030：完整回归、唯一启动与最终浏览器验收 PASS。
- MVP P0 / T037-T041：Local Desktop Owner、Session、Onboarding 与 Company → Employee → Project 浏览器链 PASS。
- Workspace Regression：Department Delete 错误契约修复；Backend 全量 `1155 passed, 2 skipped`。
- T-BD-01：业务部门数据/API、旧 Project 迁移与 Artifact→Task 持久化 PASS。
- T-BD-02：CEO → 业务部门 → 员工/项目 → Task → 成果前端 IA PASS。
- T-BD-03：Backend `1158 passed, 2 skipped`；Frontend `49 passed`、lint/build、启动链与 Desktop/Mobile PASS。
- T-EXEC-01：复用 Task/Workflow/Event 交付结构化执行时间线与持久化控制状态 PASS。
- T-EXEC-02：等待补充、接管、转派、接受、同 Task 恢复、刷新/重启持久化和取消浏览器闭环 PASS。
- T-EXEC-03：Backend `1175 passed, 2 skipped`；Frontend `49 passed`、lint/build、
  数据库、启动链、安全边界与产品验收 PASS。
- T-ASSIST-01：用户可配置 Identity、真实 Snapshot/Notifications 与 tenant 安全投影 PASS。
- T-ASSIST-02：Project/Business 查询、Task 指令链、跨页状态与 Desktop/Mobile Host PASS。
- T-ASSIST-03：Backend `1180 passed, 2 skipped`；Frontend `52 passed`、lint/build、
  数据库、官方启动链、安全边界与产品验收 PASS。
- T-ASSIST-LIVE-01：真实 Assistant 指令经现有 Task / Capability / Model Gateway
  完成，唯一 AIUsageRecord、Artifact 与 Browser 时间线闭环 PASS。

## Blocked

- 无。
