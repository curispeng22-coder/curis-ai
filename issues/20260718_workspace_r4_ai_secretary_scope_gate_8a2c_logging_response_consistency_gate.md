# Workspace R4 第8项｜8a.2c｜响应一致性与最小日志 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

统一 `secretary` 失败响应体和日志脱敏字段，消除对象存在性回显，保证返回可预期且不泄漏租户差异。

## 约束

- 不记录 prompt/模型内容明文。
- 不改前端。
- 不改数据库结构。

## 任务

1. 复用既定失败响应体格式。
2. 固定日志字段白名单（tenant_id、run_id/task_id、fail_code、time）。
3. 明确失败场景不返回历史对象明细。

## 响应一致性

- 成功：返回查询成功结构，含必要 ID 与 run/task 状态映射。
- 失败：逐字复用 `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate.md` 对应状态的固定体；仅允许 `error_code`、`message`，不新增堆栈、不返回对象数量/存在性差异。
- 失败场景不参与降级渲染；不同状态不得附加任何动态字段或实体细节。

## 最小日志白名单

- 允许字段：`timestamp`、`tenant_id`、`run_id`、`task_id`、`project_id`、`fail_code`、`step`（如有）。
- 禁止字段：`prompt`、`artifact_content`、`raw_output`、`cookie`、`token`、`JWT` 明文、`member_token`、`Authorization`、实体细节，以及任何 principal 派生字段。
- principal 不入库：禁止 `principal_hash`、`principal_digest`、`principal_count` 及任何变体；不得以 hash、digest、计数或其它派生值绕过白名单。

## 结果（本批次）

- 状态：PASS（响应一致性与最小日志规则定义完成；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_gate.md`
Objective:
统一失败响应与最小日志字段。
Special Constraints:
只读边界定义；不改运行链路。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
