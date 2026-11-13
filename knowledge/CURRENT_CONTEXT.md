# Current Context

Status: Deprecated

Updated: 2026-07-30

## Closed

- Sprint 0 架构收敛 `PASS`。
- MVP Phase 1 / S1 App Shell 与 Terra Design System `PASS`。
- MVP Phase 1 / S2 Workspace 基础模型 `PASS`。
- Regression Stabilization `PASS`；干净提交树全量后端回归 1112 passed、3 skipped。
- MVP Phase 2 / S3 AI Employee `PASS`；员工创建、职责、能力配置档案、状态与租户隔离均为真实持久化。
- S3 干净提交树全量后端回归 1114 passed、3 skipped。
- MVP Phase 3 / S4 Project `PASS`；真实项目创建、部门分组、负责人团队与统一工作台五视图可用。
- S4 干净提交树全量后端回归 1116 passed、3 skipped。
- MVP Phase 3 / S5 Task 与异步执行记录 `PASS`；真实创建、员工指派、非阻塞启动、状态查询和失败事实展示可用。
- S5 干净提交树全量后端回归 1119 passed、2 skipped。
- MVP Phase 4 / S6 Capability Registry `PASS`；六类能力真实注册、详情和启停可用，五个历史 Skill 幂等迁移并保持许可阻断。
- S6 干净提交树全量后端回归 1123 passed、2 skipped。
- MVP Phase 4 / S7 Model Gateway `PASS`；人工模型选择、单次默认模型回退与最终模型 Token/成本事实可用。
- S7 干净提交树全量后端回归 1125 passed、2 skipped。
- MVP Phase 5 / S8 研发模板 `PASS`；真实 Project Task 可完成代码修改、测试、Git diff 与模型用量回写。
- S8 隔离干净提交候选全量后端回归 1128 passed、3 skipped。
- MVP Phase 5 / S9 内容创作模板 `PASS`；真实内容 Project Task 可完成热点依据、三平台文案/SVG、复盘与模型用量回写。
- S9 隔离干净提交候选全量后端回归 1131 passed、3 skipped。
- MVP Phase 5 / S10 知识管理 `PASS`；受控本地文件与手工资料可真实入库、检索、筛选并查看来源详情。
- S10 隔离干净提交候选全量后端回归 1136 passed、2 skipped。
- MVP Phase 6 / S11 基础 Memory 与 Context Package `PASS`；用户确认沉淀的 Memory 可被下一 Task 检索并进入真实 Prompt。
- S11 隔离干净提交候选全量后端回归 1140 passed、2 skipped。
- MVP Phase 6 / S12 体验优化与最终收敛 `PASS`；最终浏览器闭环、旧库迁移清理与唯一启动链均通过。
- S12 隔离干净提交候选全量后端回归 1143 passed、2 skipped。
- `frontend/` 为唯一前端；旧双前端源码已清理。
- `data/curis.sqlite` 为唯一活动主库；旧库已迁移并可恢复清理。
- 默认启动链排除 Admin 与 FreeLLMAPI；本地 self-use 保持受控，D1 fail-closed。
- 23/23 个 CEO Office 页面复用唯一 Shell；共享原语已在员工管理真实页面采用。
- Business Department Organization Model 实现已接受：Company 保留为技术聚合根，Local Desktop IA 为 `CEO → 业务部门 → 员工 / 项目 → Task → 成果`。
- 旧 Project 已幂等归属业务部门；Artifact 独立关联 Task，失败 Task 不生成伪成果。
- AI Call Usage Ledger Foundation `PASS（Issue Scope）`；`ai_usage_records` 是 Token 与 AI 成本唯一事实源，追加式、tenant fail-closed，未知值保持 `NULL`。
- Model Gateway、RealRD、D1 的真实出站调用统一记账；Retry/Fallback 分尝试记录，`usage.*` 仅保留审计引用。
- 数字员工执行控制闭环 v1 `LOCAL CONTROL PASS`；复用现有 Task/Workflow/Event，
  支持结构化时间线、持久化暂停、补充、接管、转派、同 Task 恢复与取消。
- 执行控制 Backend 全量 `1175 passed, 2 skipped`；Frontend `49 passed`、
  lint/build、官方启动链和 Desktop/Mobile 浏览器本地控制闭环 PASS；安全边界与产品验收通过。
- Global Assistant Runtime v1 `PASS`；Identity 用户可配置，根布局级 Host 保持跨页状态，
  查询聚合现有业务服务，执行指令只进入现有 Task / Task Run / Capability 链。
- Assistant Backend 全量 `1180 passed, 2 skipped`；Frontend `52 passed`、
  lint/build、数据库、官方启动链、Desktop/Mobile Browser、安全与产品验收均 PASS。
- Global Assistant Live Model Chain Validation `PASS`；固定非敏感指令经现有
  Task / Capability / Model Gateway 完成，唯一 AIUsageRecord、Artifact 和真实
  Browser 时间线一致，`BLOCKED_L2_LIVE_VALIDATION` 已解除。

## Evidence

- Issue：`issues/20260729_sprint0_architecture_convergence.md`
- Review：`reviews/20260729_sprint0_architecture_convergence_review.md`
- Issue：`issues/20260729_mvp_phase1_s1_app_shell_design_system.md`
- Review：`reviews/20260729_mvp_phase1_s1_app_shell_design_system_review.md`
- Issue：`issues/20260729_mvp_phase1_s2_workspace_model.md`
- Review：`reviews/20260729_mvp_phase1_s2_workspace_model_review.md`
- Issue：`issues/20260729_regression_stabilization.md`
- Review：`reviews/20260729_regression_stabilization_review.md`
- Issue：`issues/20260729_mvp_phase2_s3_ai_employee.md`
- Review：`reviews/20260729_mvp_phase2_s3_ai_employee_review.md`
- Issue：`issues/20260729_mvp_phase3_s4_project.md`
- Review：`reviews/20260729_mvp_phase3_s4_project_review.md`
- Issue：`issues/20260729_mvp_phase3_s5_task_execution.md`
- Review：`reviews/20260729_mvp_phase3_s5_task_execution_review.md`
- Issue：`issues/20260729_mvp_phase4_s6_capability_registry.md`
- Review：`reviews/20260729_mvp_phase4_s6_capability_registry_review.md`
- Issue：`issues/20260729_mvp_phase4_s7_model_gateway.md`
- Review：`reviews/20260729_mvp_phase4_s7_model_gateway_review.md`
- Issue：`issues/20260729_mvp_phase5_s8_rd_template.md`
- Review：`reviews/20260729_mvp_phase5_s8_rd_template_review.md`
- Issue：`issues/20260729_mvp_phase5_s9_content_template.md`
- Review：`reviews/20260729_mvp_phase5_s9_content_template_review.md`
- Issue：`issues/20260729_mvp_phase5_s10_knowledge_management.md`
- Review：`reviews/20260729_mvp_phase5_s10_knowledge_management_review.md`
- Issue：`issues/20260729_mvp_phase6_s11_basic_memory_context.md`
- Review：`reviews/20260729_mvp_phase6_s11_basic_memory_context_review.md`
- Issue：`issues/20260729_mvp_phase6_s12_experience_convergence.md`
- Review：`reviews/20260729_mvp_phase6_s12_experience_convergence_review.md`
- Issue：`issues/20260729_mvp_p0_authentication_onboarding.md`
- Review：`reviews/20260729_mvp_p0_authentication_onboarding_review.md`（`BLOCKED_L2`）
- Issue：`issues/20260729_mvp_p0_local_desktop_owner.md`
- Review：`reviews/20260729_mvp_p0_local_desktop_owner_review.md`（Issue Scope PASS）
- Issue：`issues/20260729_workspace_regression_employee_templates.md`
- Review：`reviews/20260729_workspace_regression_employee_templates_review.md`（PASS）
- Issue：`issues/20260729_business_department_org_model.md`
- Review：`reviews/20260729_business_department_org_model_review.md`（实现/迁移/回归 PASS；真实成果 Browser `BLOCKED_L2`）
- Issue：`issues/20260729_ai_call_usage_ledger_foundation.md`
- Review：`reviews/20260729_ai_call_usage_ledger_foundation_review.md`（Issue Scope PASS；Security PASS；产品 ACCEPT）
- Issue：`issues/20260730_digital_employee_execution_control_loop_v1.md`
- Review：`reviews/20260730_digital_employee_execution_control_loop_v1_review.md`
  （LOCAL CONTROL PASS；Security PASS；产品 ACCEPT；真实模型正向 `BLOCKED_L2_LIVE_VALIDATION`）
- Issue：`issues/20260730_global_assistant_runtime_v1.md`
- Review：`reviews/20260730_global_assistant_runtime_v1_review.md`
  （PASS；Security PASS；产品 ACCEPT）
- Issue：`issues/20260730_global_assistant_live_model_validation.md`
- Review：`reviews/20260730_global_assistant_live_model_validation_review.md`
  （PASS；Security PASS；产品 ACCEPT）

## Next Boundary

Global Assistant Runtime v1 与真实供应商正向浏览器链均已关闭。后续真实模型使用
继续由 Owner 通过既有环境变量或 Vault 边界提供凭证；无 Key 时保持 fail-closed。
Capability 分支/反馈改进和外部消息渠道必须另立 Issue。
