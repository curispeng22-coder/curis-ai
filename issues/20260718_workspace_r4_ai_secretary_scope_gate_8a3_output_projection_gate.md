# Workspace R4 第8项｜8a.3｜AI Secretary 输出域与建议来源 Gate

- 日期：2026-07-18
- 状态：IN_PROGRESS — 8a.3a/8a.3b/8a.3c PASS（待质量复核），等待父项汇总
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（先完成）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

明确建议文本与建议来源的唯一构成：只来自已归档 run/result，不拼接裸文本，不发新模型调用。

## 约束

- 只读复核与边界定义。
- 不改前端、不改前置模型调用。

## 任务

1. 定义“建议来源”字段白名单（run/result id、时间、状态、摘要）。
2. 定义输出字段脱敏与不得暴露明文 prompt 的规则。
3. 定义输出为不可写、不触发新 run 的契约。

## 子任务（本轮）

- 8a.3a｜来源可追溯字段白名单（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`
  - `source_run_id`、`source_step_id`、`source_result_hash`、`tenant_id`、`created_at` 必含且一致。
  - `summary`、`next_step_hint` 仅映射已归档文本，不允许空引用。
  - 产物：字段白名单清单。

- 8a.3b｜敏感字段过滤（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md`
  - 严格禁止输出输入 prompt、tool raw payload、模型 token 文本、凭据相关字段。
  - 产物：过滤规则与输出示例。

- 8a.3c｜不可触发执行约束（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3c_no_execute_side_effect_gate.md`
  - 对读取链路返回结果设置只读标记，不提供触发动作接口与新 run 参数。
  - 产物：约束说明与失败样本（“试图触发写操作”必须拒绝）。

## 最低验收

- 输出建议必须可回溯来源对象。
- 不接受未入库、未归档或未授权对象。
- 不新增外部网关，不新增模型执行。

## 结果（本批次）

- 状态：进行中。8a.3a/8a.3b/8a.3c 全部定义完成（待质量复核），可汇总到父项 8a。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`。

## 执行顺序

8a.3a → 8a.3b → 8a.3c

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3_output_projection_gate.md`
Objective:
定义 AI Secretary 输出域与建议来源规则。
Special Constraints:
只读定义；不新增模型与前端。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
