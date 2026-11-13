# Workspace R4 第8项｜8a.1a.2｜可承接来源状态过滤 Gate

- 日期：2026-07-18
- 状态：PASS（状态白名单已定义；待质量复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_object_field_map_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

在 8a.1a 中定义 Secretary 来源对象的“可接收状态”边界，确保只读入口只消费已归档/完成链路。

## 任务

1. 固定 `workflow_runs` 状态判定（完成/归档可接收，其余拒绝）。
2. 固定 `step_results` 状态判定（成功终态可接收，非终态拒绝）。
3. 固定 `publish_packages`、`content_workflow_runs` 可见状态（仅已审计、已完成可接收）。

## 状态白名单

- `workflow_runs.status`：仅 `succeeded` 可读入。其余（`pending`、`running`、`failed`）一律拒绝。
- `step_results.status`：仅 `succeeded` 可读入。`result` 可为空但不得缺失必要元数据。
- `publish_packages.status`：仅 `published` 可进入 Secretary 建议输入；`generated`/`failed` 继续保留源数据但不作为承接对象。
- `content_workflow_runs.status`：仅 `completed` 可承接；`running`/`failed` 不可承接。

## 规则（最小）

- 接受态需要与任务入口参数完成一致（尤其 tenant/project/workflow）。
- 非接受态对象不允许继续透传其子对象；例如 workflow_run 非成功态则关联的 step_results 不可作为 8a.1a 合法入口。

## 产物

- 状态表（对象 → 接受状态集合）。
- 非可接收状态统一处理规则（拒绝原因码/行为）。

## 结果（本批次）

- 状态：PASS（状态白名单已定义；可推进 8a.1a.3）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_visibility_state_filter_gate.md`
Objective:
冻结来源对象可接收状态边界。
Special Constraints:
只读边界定义，不起新接口。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
