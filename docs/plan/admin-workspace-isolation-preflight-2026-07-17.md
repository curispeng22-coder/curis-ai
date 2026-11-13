# Admin / Workspace 隔离实施前置核验

日期：2026-07-17
负责人：产品负责人（本席）
状态：前置核验完成；实施暂不启动

## 已锁定的部署参数

| 产品 | 前端 | 后端 | 数据库 |
|---|---:|---:|---|
| Admin | 3100 | 8001 | `data/admin.sqlite` |
| Workspace | 3000 | 8002 | `data/workspace.sqlite` |

两个后端进程分别设置 `CURIS_PRODUCT`、`CURIS_DB` 和 `CURIS_ALLOWED_ORIGINS`。不采用单进程动态切换数据库。

## 当前核验事实

- 当前仍是单体 Next.js：`frontend/`。
- 当前仍是单体 FastAPI：`backend/`。
- 当前活动数据库为 `data/curis.sqlite`。
- 已生成 `data/admin.sqlite` 与 `data/workspace.sqlite`，并完成首轮表级数据隔离；原 `data/curis.sqlite` 保留为回滚基线。
- 两个后端实例已在 8001/8002 启动验证；产品域路由已互相拒绝。
- `frontend/app/employees/page.js` 仍有未提交改动，必须在前端拆分前交接。
- 数据库包含平台资产、Workspace 运行态、租户、安全、执行、工作流和商业化相关表，不能按表名直接拆分。

## Issue 状态裁决

- Issue 090：参数约定已具备，可进入实施前设计；尚未授权修改部署。
- Issue 088：被 `employees/page.js` 未提交改动阻塞。
- Issue 089：双进程启动已验证；被数据库表归属和迁移规则阻塞。

## 数据边界原则

- Admin 私有资产：仅在 Admin 数据库保留。
- Workspace 运行数据：仅在 Workspace 数据库保留。
- 租户、Company、Department、Project、Employee、Task、Workflow、Credential、Usage、Audit 等跨域或安全敏感数据：先建立明确的数据契约，不得直接迁移。
- 根目录 `curis.sqlite` 保留为种子基线；当前活动库在拆分前不得删除或覆盖。

## 下一步

1. 先完成 `employees/page.js` 的 Workspace 交接提交。
2. 为 Issue 089 建立逐表归属和迁移策略评审。
3. 评审通过后，才允许创建双库和双后端进程。
4. Issue 088 与 Issue 089 均通过实施前评审后，再进行前端目录迁移。

## 当前逐表归属草案

### Admin 私有或优先归 Admin

`billing_events`、`capability_packages`、`company_packages`、`company_templates`、`dashboard_templates`、`dashboard_widget_catalog`、`model_gateways`、`official_models`、`platform_policies`、`pricing_rules`、`quota_rules`、`skill_templates`、`tool_templates`。

### Workspace 运行数据

`companies`、`company_department_state`、`department_instances`、`department_observations`、`departments`、`employee_instances`、`employee_capability_bindings`、`employee_context_manifests`、`employee_role_guard_audits`、`employee_role_guard_claims`、`employee_session_audit_events`、`employee_session_step_bindings`、`employee_session_step_claim_bindings`、`employee_sessions`、`employee_skill_bindings`、`employee_working_memory_audits`、`employee_working_memory_checkpoints`、`projects`、`tasks`、`workflows`、`workflow_runs`、`workflow_steps`、`workflow_instances`、`workflow_traces`、`workflow_metrics`、`step_assignments`、`step_results`、`workspace_goals`、`credential_metadata`。

### 共享基线，暂不拆分

`tools`、`tool_performance`、`tool_traces`、`executions`、`auto_workflows`、`execution_patterns`、`execution_scores`、`failure_logs`、`development_strategies`、`meta_development_reports`、`evolution_*`、`rollback_records`、`workflow_templates`、`workflow_contents`、`department_types`、`department_templates`、`employee_templates`、`persona_templates`、`plans`、`tenants`、`tenant_*`、`secretary_*`、`decision_*`、`content_*`、`project_*`、`goal_*`。

该草案不是迁移授权。非空共享表、租户表、凭证表和执行关联表必须在 Issue 089 实施评审中逐项确认。

本文件不授权代码迁移、数据库变更、部署变更或依赖安装。
