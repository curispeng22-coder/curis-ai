# Workspace R4 第8项｜8a｜AI Secretary 范围与授权 Gate

- 日期：2026-07-18
- 状态：PASS — 8a 全部子项已完成质量复核并由产品规划席收口
- 前置：`issues/20260718_workspace_r4_unified_token_cost_budget_backend_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_backend_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）→ 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

- 明确 AI Secretary 的输入/输出边界：仅承接已授权执行链和已审计成果。
- 约束无边界时拒绝处理（fail-closed）。

## 约束

- 不新增模型/网关；
- 不改历史执行记录；
- 不改前端。

## 当前核查事实（本轮）

- 目前未发现独立 `GET/POST /api/secretary*` 路由；
- 当前可复用范围仅在已有结果读取链路，如 `/api/results/summary`、`/api/results/publish-packages`、`/api/results/content-workflow-runs`；
- 先完成只读边界定义，不起新接口与新模型调用。

## 任务拆分（本项 8a）

- 8a.1｜可承接来源定义（系统交付）
  - 仅允许以下三类输入进入 Secretary：
    - 已授权的 Workspace 运行结果（`workflow_runs` + `step_results`）引用；
    - 已审计成果索引（`publish_packages`/`content_workflow_runs`）；
    - 仅 `tenant_id` 内部可见的 `company/project/department/employee/workflow/task` 上下文。
- 先导子项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`、`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate.md`、`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md`
- 8a.2｜交付边界与越权拒绝（系统交付）
  - 无权访问时返回 `403/404` 及空列表（不泄露实体是否存在）；
  - 缺 tenant 时返回 `401`；
  - 超出单会话授权时返回 `423` 或 `409`（明确阻断，不降级继续）。
- 对应子项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2a_status_code_singleton_gate.md`、`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate.md`、`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_gate.md`
- 8a.3｜输出域约束（系统交付）
  - Secretary 建议与建议来源只来自已归档 run/result，不接受裸文本输入拼接；
  - 不新增模型调用，仅做复用已存在真实成果的只读投影。
- 对应子项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`、`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md`、`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3c_no_execute_side_effect_gate.md`
- 派发队列：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a_rollout_queue.md`

## 当前执行计划（本轮）

- 先完成 8a.1（来源边界与字段映射）；
- 再完成 8a.2（越权与失败边界）；
- 最后完成 8a.3（输出域与建议来源约束）；
- 三段均需经质量运行席复核后回到产品规划席。

## 8a 收口结果

- 8a.1 来源对象、字段、状态、拒绝码、缺上下文与错配隔离：PASS。
- 8a.2 授权返回码、跨租户封锁、日志与响应一致性：PASS；日志敏感边界经安全边界席复核。
- 8a.3 追溯字段、敏感输出过滤、只读无执行副作用：PASS；敏感输出边界经安全边界席复核。
- 本项仅完成只读边界与验收契约，不构成 AI Secretary API、前端、模型调用或执行入口授权。
- 下一链路：进入 8b 风控边界；8c 仍须等待 8a 与 8b 均完成。

## 本项验收（先读后验）

- fail-closed：无授权、越权、错 tenant、缺上下文，全部 fail；
- 单点范围收敛：`secretary` 行为不接入新前端/API 外流，不发起新 run；
- 以历史 run 记录作为唯一读源（只读）；
- 审计可追溯字段（tenant/来源对象 ID/时间/状态）可读但不存高敏明文。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`
Objective:
定义AI Secretary 范围与授权边界。
Special Constraints:
只读边界定义，不起新 run。
Next Seat:
质量运行席（复核一次）
Handoff: sent to 质量运行席
