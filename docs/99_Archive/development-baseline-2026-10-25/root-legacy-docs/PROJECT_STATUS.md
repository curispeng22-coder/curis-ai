# Project Status

Authority Class: HISTORY
Disposition: HISTORICAL / NOT A CURRENT ENTRYPOINT
Navigation updated: 2026-10-25

**以下是原阶段历史记录。** 旧“Current / Active / Next / Read this first”只描述当时状态。
当前请从 [AGENTS](<../../../../AGENTS.md>) → [现有入口](<../../../00_Context/CURIS_CURRENT_ENTRYPOINT.md>)查询；进度只看 [既有执行看板](<../../../../artifacts/tasks/CURIS-V1-BUSINESS-CATALOG-TEAM-20261008/DELIVERY_PROGRESS_AND_BATCH_PLAN_20261013.md>)。
[本轮维护决定](<../../../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)保留原文、原 Status 和历史日期；物理归档尚未执行。候选见 [精确归档清单](<../../../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/PLACEMENT_REVIEW.md>)。

Status: Deprecated

Updated: 2026-07-30

## Current Phase

- Sprint 0：`CLOSED — PASS`
- MVP Phase 1 / S1：`CLOSED — PASS`
- MVP Phase 1 / S2：`CLOSED — PASS`
- Regression Stabilization：`CLOSED — PASS`
- MVP Phase 2 / S3：`CLOSED — PASS`
- MVP Phase 3 / S4：`CLOSED — PASS`
- MVP Phase 3 / S5：`CLOSED — PASS`
- MVP Phase 4 / S6：`CLOSED — PASS`
- MVP Phase 4 / S7：`CLOSED — PASS`
- MVP Phase 5 / S8：`CLOSED — PASS`
- MVP Phase 5 / S9：`CLOSED — PASS`
- MVP Phase 5 / S10：`CLOSED — PASS`
- MVP Phase 6 / S11：`CLOSED — PASS`
- MVP Phase 6 / S12：`CLOSED — PASS`
- MVP P0 Authentication & Onboarding Recovery：`SUPERSEDED`
- MVP P0 Local Desktop Owner：`CLOSED — PASS（Issue Scope）`
- Workspace Regression：`CLOSED — PASS`
- Business Department Organization Model：`IMPLEMENTATION ACCEPTED / BLOCKED_L2`
- 数字员工执行控制闭环 v1：`LOCAL CONTROL PASS / BLOCKED_L2_LIVE_VALIDATION`
- Global Assistant Runtime v1：`CLOSED — PASS`
- Global Assistant Live Model Chain Validation：`CLOSED — PASS`
- 当前基线：Curis v1.0
- 当前阶段：Local Desktop 单用户 AI Workspace

## Sprint 0 Outcome

- 单前端：`frontend/`
- 单默认数据库：`data/curis.sqlite`
- 实验能力不进入默认启动链
- 本地唯一启动/停止命令通过
- Frontend lint/build、7 项前端测试、21 项后端测试、网关配置和浏览器验证通过

## Evidence

- `issues/20260729_sprint0_architecture_convergence.md`
- `reviews/20260729_sprint0_architecture_convergence_review.md`
- `issues/20260729_mvp_phase1_s1_app_shell_design_system.md`
- `reviews/20260729_mvp_phase1_s1_app_shell_design_system_review.md`
- `issues/20260729_mvp_phase1_s2_workspace_model.md`
- `reviews/20260729_mvp_phase1_s2_workspace_model_review.md`
- `issues/20260729_regression_stabilization.md`
- `reviews/20260729_regression_stabilization_review.md`
- `issues/20260729_mvp_phase2_s3_ai_employee.md`
- `reviews/20260729_mvp_phase2_s3_ai_employee_review.md`
- `issues/20260729_mvp_phase3_s4_project.md`
- `reviews/20260729_mvp_phase3_s4_project_review.md`
- `issues/20260729_mvp_phase3_s5_task_execution.md`
- `reviews/20260729_mvp_phase3_s5_task_execution_review.md`
- `issues/20260729_mvp_phase4_s6_capability_registry.md`
- `reviews/20260729_mvp_phase4_s6_capability_registry_review.md`
- `issues/20260729_mvp_phase4_s7_model_gateway.md`
- `reviews/20260729_mvp_phase4_s7_model_gateway_review.md`
- `issues/20260729_mvp_phase5_s8_rd_template.md`
- `reviews/20260729_mvp_phase5_s8_rd_template_review.md`
- `issues/20260729_mvp_phase5_s9_content_template.md`
- `reviews/20260729_mvp_phase5_s9_content_template_review.md`
- `issues/20260729_mvp_phase5_s10_knowledge_management.md`
- `reviews/20260729_mvp_phase5_s10_knowledge_management_review.md`
- `issues/20260729_mvp_phase6_s11_basic_memory_context.md`
- `reviews/20260729_mvp_phase6_s11_basic_memory_context_review.md`
- `issues/20260729_mvp_phase6_s12_experience_convergence.md`
- `reviews/20260729_mvp_phase6_s12_experience_convergence_review.md`

## S1 Outcome

- 23/23 个 CEO Office 页面复用唯一 `TerraShell`。
- 全局 AI Assistant Layer 已补齐并明确未连接服务。
- Terra `Input / Table / Modal / Drawer` 与三种业务卡片已补齐。
- 员工管理页采用共享组件；Frontend lint/build 与 Desktop/Mobile browser 验证通过。

## S2 Evidence

- Company / Department / Home 聚焦测试与真实浏览器流程通过。
- Frontend lint/build PASS。
- 干净提交树全量后端回归：1112 passed、3 skipped、0 failed。

## S3 Outcome

- 用户可从真实部门与兼容模板创建员工，保存名称、角色和职责。
- Capability Profile 复用既有员工能力绑定；列表与详情展示真实能力。
- 员工状态、编辑、软删除、组织中心同步与租户隔离通过。
- Frontend lint/build、Desktop/Mobile browser 与干净提交树全量回归通过。
- 全量后端回归：1114 passed、3 skipped、0 failed。

## S4 Outcome

- 用户可从真实部门与负责人创建包含目标和说明的项目。
- 项目中心按真实部门展示；项目工作台提供概览、任务、资料、成果和数据视图。
- 真实 Project Task 可见；未持久化资料、成果和经营指标保持空状态。
- Frontend lint/build、Desktop/Mobile browser 与干净提交树全量回归通过。
- 全量后端回归：1116 passed、3 skipped、0 failed。

## S5 Outcome

- 用户可在真实项目中创建 Task，并指定当前公司已启用 AI Employee。
- 启动接口返回 `202 + job_id`；queued / running / completed / failed 状态可查询。
- 项目工作台、执行工作台和 Task 详情展示真实任务、状态流、结果或失败原因。
- Frontend lint/build、Desktop/Mobile browser 与干净提交树全量回归通过。
- 全量后端回归：1119 passed、2 skipped、0 failed。

## S6 Outcome

- Workspace 用户可真实查看、注册和启停六类 Capability，无需 Platform Admin。
- 五个历史 `skl_skill_*` 幂等迁移，稳定 ID、来源、描述与许可边界可追溯。
- 历史 Skill 保持停用，许可复核前的启用请求明确失败。
- Frontend lint/build、Desktop/Mobile browser 与干净提交树全量回归通过。
- 全量后端回归：1123 passed、2 skipped、0 failed。

## S7 Outcome

- 用户创建 Project Task 时只可人工选择执行员工已绑定、已启用的官方 Model Capability。
- 首选模型失败后仅回退一次到现有默认模型；最终模型、Token、成本与回退事实写入 UsageEvent 并展示。
- Workspace 可查看安全的 Provider、模型、运行配置状态和租户用量摘要，不返回凭证或原始请求/响应。
- Frontend lint/build、Desktop/Mobile browser 与干净提交树全量回归通过。
- 全量后端回归：1125 passed、2 skipped、0 failed。

## S8 Outcome

- 现有 Project Task 可使用已人工绑定的 Model Capability 启动真实 `wt_rd_pipeline`。
- RealRD 同次完成受控代码修改、已登记测试和 Git diff，失败明确回写 Task 与 WorkflowRun。
- 运行详情展示六步状态、变更文件、测试退出码、Diff SHA、模型、Token、成本与轮次。
- Frontend lint/build、Desktop/Mobile browser 与隔离干净提交候选全量回归通过。
- 全量后端回归：1128 passed、3 skipped、0 failed。

## S9 Outcome

- 复用既有内容公司包，真实 Project Task 可生成选题、三平台文案/脚本、SVG 图片与复盘计划。
- ContentWorkflowRun、ContentPublishPackage、Task、Execution 和模型用量真实持久化。
- 项目创建按所选部门解析 Company，内容公司项目可从现有项目中心直接建立。
- 外部发布未执行；Frontend lint/build、Desktop/Mobile browser 与隔离干净提交候选全量回归通过。
- 全量后端回归：1131 passed、3 skipped、0 failed。

## S10 Outcome

- 用户可从安全配置的本地根导入真实 Markdown/Text，或手工创建公司、项目、部门资料。
- KnowledgeEntry 保存正文、来源、相对路径、SHA、标签、归属和时间；同路径重复导入幂等更新。
- 资料中心支持标题/正文/标签检索、范围筛选与真实详情；Knowledge 不冒充 Memory。
- Frontend lint/build、Desktop/Mobile browser 与隔离干净提交候选全量回归通过。
- 全量后端回归：1136 passed、2 skipped、0 failed。

## S11 Outcome

- 用户、项目、员工 Memory 可真实创建、更新、检索并保持租户/身份/对象隔离。
- 终态 Task 可由用户确认沉淀经验；下一 Task 自动检索相关 Memory 与 Knowledge。
- Context Package 持久化并进入现有 Orchestrator Prompt，使用事实、SHA 与 Memory 使用次数可追溯。
- Frontend lint/build、Desktop/Mobile browser 与隔离干净提交候选全量回归通过。
- 全量后端回归：1140 passed、2 skipped、0 failed。

## S12 Outcome

- 唯一 App 的加载、错误恢复、过期请求与可选事实失败处理完成收口。
- 旧库补入 330 条缺失记录，主库优先且幂等；完整性与外键检查通过。
- 五个旧库文件可恢复清理，Admin 旧启动文件退出默认运行链，`data/curis.sqlite` 为唯一活动主库。
- 最终浏览器闭环与 Memory 下一 Task 复用通过；Desktop/Mobile 无横向溢出。
- Frontend lint/build、唯一启动与隔离干净提交候选全量回归通过。
- 全量后端回归：1143 passed、2 skipped、0 failed。

## Guardrails

- 不重写产品或改变 Curis v1.0 架构。
- 不创建第二套 Workspace/Admin。

## Global Assistant Runtime v1

- Identity 默认全空并支持用户自定义名称、头像标记、角色、语气和个性。
- 根布局级 Provider / Host 支持 CEO Office 完整 Panel、其他页面隐藏入口和跨页状态。
- 查询复用现有业务服务；执行只创建并启动现有 Task，不直接修改业务对象。
- Backend：`1180 passed, 2 skipped`；Frontend：`52 passed`、lint/build PASS。
- 数据库、官方启动链、Desktop/Mobile Browser、安全边界和产品验收 PASS。
- Review：`reviews/20260730_global_assistant_runtime_v1_review.md`。

## Global Assistant Live Model Chain Validation

- 固定非敏感 Assistant 指令经现有 Task / Capability / Model Gateway 真实完成。
- Task `1d634bb3-c154-4d16-98b6-b35b45eb4e8e` 为 `COMPLETED`，生成 1 个 Artifact。
- 唯一 AIUsageRecord `usage-4ece6cc0-061b-4b96-90c9-adefcebc0686`：
  228 Tokens、USD `0.00023475` estimated、计量 confirmed。
- `model_called` 只引用同一 usage ID；数据库与日志无 Key 命中，无 Key 重启
  fail-closed。
- Backend 全量 `1179 passed, 3 skipped`；Frontend `59 passed`、lint/build、
  真实 Browser Task 详情与 Console `0 error`。
- 安全边界席 `PASS`；质量运行席 `PASS`；产品规划席 `ACCEPT`。
- Review：`reviews/20260730_global_assistant_live_model_validation_review.md`。

## Business Department Organization Model

- Company 保留为技术聚合与 tenant 隔离根，不再作为 Local Desktop 日常组织树层级。
- 业务部门复用 `department_instances`；员工与项目直接归属业务部门，Task 属于 Project，Artifact 属于 Task。
- 旧项目迁移、API 约束、前端 IA、Desktop/Mobile、官方启动与全量回归 PASS。
- Backend：`1158 passed, 2 skipped`；Frontend：`49 passed`、lint/build PASS。
- `BLOCKED_L2`：本机缺少 Model Gateway 外部运行配置，尚无真实成功 Task 可完成正向成果 Browser 证据。
- Review：`reviews/20260729_business_department_org_model_review.md`。

## MVP P0 Authentication & Onboarding Evidence

- 本地认证、401 原页面跳转、首次 Onboarding、Desktop/Mobile 登录布局与安全边界聚焦检查 PASS。
- Frontend `4 passed`、lint/build PASS；Backend 身份与 OIDC `28 passed`。
- Google 登录链已被 Local Desktop Owner 产品决定替代，不再是 MVP Gate。
- 该阶段当时的共享工作树全量回归为 `1 failed, 1149 passed, 2 skipped`；后续已由 Workspace Regression Issue 修复。

## Digital Employee Execution Control Loop v1

- 复用现有 Task、Workflow、Capability、`evolution_events` 和 AI Usage Record，
  未新增并行 Agent、Session、SOP、Knowledge 或 Task Run 系统。
- Task 详情支持结构化时间线、持久化等待补充、人工接管、转派、接受、同 Task 恢复和取消。
- `model_called` 只引用 `usage_record_id`；Token/成本不重复保存，敏感恢复参数不进入公开投影。
- Backend：`1175 passed, 2 skipped`；Frontend：`49 passed`、lint/build PASS；
  数据库、官方启动链、Desktop/Mobile 浏览器本地控制闭环 PASS。
- Security Boundary：`PASS`；产品规划席：`ACCEPT`。
- `BLOCKED_L2_LIVE_VALIDATION`：待 Owner 提供安全模型配置后补真实供应商成功调用到
  `AIUsageRecord` / `model_called` 的正向浏览器证据。
- Review：`reviews/20260730_digital_employee_execution_control_loop_v1_review.md`。
- Review：`reviews/20260729_mvp_p0_authentication_onboarding_review.md`。

## MVP P0 Local Desktop Owner Evidence

- 默认入口：创建/进入 Local Owner；不依赖 Google OAuth Client ID、Secret 或外网。
- Local Owner → HttpOnly Session → Onboarding → Company → Employee → Project 真实浏览器 PASS。
- Backend 身份聚焦 `33 passed`；Frontend `4 passed`、lint/build PASS；安全边界 PASS。
- Google OAuth/JWT/trusted gateway 保留为未来扩展并继续 fail-closed。
- 该阶段发现的 `backend/app/employee_templates.py` Issue 外失败已由后续 Workspace Regression Issue 修复。
- Review：`reviews/20260729_mvp_p0_local_desktop_owner_review.md`。
- Department Delete 错误契约已恢复；当前 Backend 全量为 `1155 passed, 2 skipped, 0 failed`。
- Regression Review：`reviews/20260729_workspace_regression_employee_templates_review.md`。
- 后续数据变更必须使用独立 Task。
- MVP 功能按 Sprint 建 Issue、测试、Review 和提交。
