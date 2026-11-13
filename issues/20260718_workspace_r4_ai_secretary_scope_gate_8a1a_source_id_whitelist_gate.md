# Workspace R4 第8项｜8a.1a｜来源对象白名单 Gate

- 日期：2026-07-18
- 状态：IN_PROGRESS — 8a.1a.1/8a.1a.2/8a.1a.3 PASS（待质量复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

固定 Secretary 可承接来源对象白名单与唯一字段映射，确保只读链路仅基于可核验实体。

## 约束

- 不起新 run。
- 不改历史记录。
- 不改前端。

## 任务

1. 固定可接收对象：`workflow_runs.id`、`step_results.id`、`publish_packages.id`、`content_workflow_runs.id`。
2. 记录 `tenant_id / project_id / company_id / department_id / employee_id / workflow_id / task_id / run_id` 必要映射。
3. 明确仅允许归档/完成态引用的判定标准（或等价现有历史完成态）。

## 子任务（本轮）

### 8a.1a.1｜来源对象字段映射白名单

- 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_object_field_map_gate.md`
- 产出：对象-字段白名单（exact 字段名、必选/可选、类型、空值策略）。

### 8a.1a.2｜可承接来源状态过滤

- 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_visibility_state_filter_gate.md`
- 产出：workflow_runs、step_results、publish_packages、content_workflow_runs 的可接收状态集合。

### 8a.1a.3｜缺失/失配拒绝码映射

- 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_refusal_status_gate.md`
- 产出：缺失、非可接收状态、来源错配、跨域错配统一返回码与行为。

执行顺序：8a.1a.1 → 8a.1a.2 → 8a.1a.3

## 产物

- 来源对象白名单表。
- 映射字段对照表。
- 失配/缺失统一拒绝策略（401/400/403/404）。

## 结果（本批次）

- 状态：IN_PROGRESS — 8a.1a.1/8a.1a.2/8a.1a.3 PASS，等待 8a.1a 全链复核后推进 8a.1b。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
Objective:
定义 Secretary 可承接来源对象白名单与字段映射。
Special Constraints:
只读边界定义，不起新接口。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
