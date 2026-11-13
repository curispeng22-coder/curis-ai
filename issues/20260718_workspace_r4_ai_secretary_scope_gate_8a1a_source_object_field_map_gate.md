# Workspace R4 第8项｜8a.1a.1｜来源对象字段映射白名单 Gate

- 日期：2026-07-18
- 状态：PASS（字段白名单已定义；待质量复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

定义 Secretary 可承接的来源对象字段白名单，固定字段最小集合，禁止其它路径注入。

## 任务

1. 固定并枚举对象：`workflow_runs.id`、`step_results.id`、`publish_packages.id`、`content_workflow_runs.id`。
2. 固定每对象可接受字段集合（tenant/company/project/department/employee/workflow/task/run/result 相关）。
3. 定义字段空值/异常形态在当前 Issue 内统一拒绝策略。

## 白名单（exact）

- workflow_runs（来源对象：历史 RD 运行）  
  - 必要：`tenant_id`、`workflow_run_id`、`company_id`、`project_id`、`workflow_template_id`、`workflow_instance_id`、`department_id`、`status`、`task_id`  
  - 可选：`created_at`、`updated_at`、`started_at`、`completed_at`、`failed_at`、`final_report`
- step_results（来源对象：已落地步骤结果）  
  - 必要：`tenant_id`、`step_result_id`、`workflow_step_id`、`employee_id`、`status`、`result`  
  - 可选：`created_at`
- publish_packages（来源对象：成果包）  
  - 必要：`tenant_id`、`package_id`、`source_workflow`、`status`、`platforms_targeted`、`published_platforms`、`artifacts`
  - 可选：`version`、`language`、`brand_voice_ref`、`created_at`、`updated_at`
- content_workflow_runs（来源对象：内容运行）  
  - 必要：`tenant_id`、`run_id`、`workflow_content_id`、`department_id`、`status`、`steps_total`、`steps_done`  
  - 可选：`summary`、`created_at`、`updated_at`

## 联动映射（最小）

- `step_results.workflow_step_id` → `workflow_steps.workflow_step_id` → `workflow_runs.workflow_run_id`
- `workflow_runs.workflow_run_id` → `task_id`（由调用侧用于上下文对齐）
- `content_workflow_runs.run_id`、`publish_packages.package_id` 为独立成果索引源（不共享状态机）
- `publish_packages` 与 `content_workflow_runs` 均为 `tenant_id` 级可见源，默认不扩展到外租户或历史外域

## 产物

- white_list 字段清单（exact 字段名）。
- 字段可见性与必需性（required/optional）。
- 异常字段/越界字段拒绝映射。

## 直接失败规则（先验）

- 缺必要字段：fail-closed（统一映射到 8a.1a.3/8a.1b 规则）
- 参数为空字符串/`null`：若字段为必要字段，立即拒绝；可选字段允许空但不进行类型推断

## 结果（本批次）

- 状态：PASS（字段白名单已定义；可推进 8a.1a.2）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`。

## 当前闸门

- 现在阻塞点：等待质量运行席对本 Issue 复核回流（以 PASS/CLOSED 证据为准）后，才可进入 `..._8a1a_source_visibility_state_filter_gate.md`。
- 当前文件已完成定义交付，**未见回流 review 文件**，不得并行推进 8a.1a.2 或后续 8a 子项。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_object_field_map_gate.md`
Objective:
冻结 Secretary 可承接来源对象字段白名单。
Special Constraints:
只读边界定义，不起新接口。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
