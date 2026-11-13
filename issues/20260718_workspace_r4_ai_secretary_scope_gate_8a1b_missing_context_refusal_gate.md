# Workspace R4 第8项｜8a.1b｜来源缺失与空上下文拒绝 Gate

- 日期：2026-07-18
- 状态：PASS（来源缺失场景定义完成；待质量复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

定义来源参数缺失、空上下文、空字符串上下文下的统一阻断，防止默认回退到历史数据。

## 约束

- 不起新调用。
- 不启用 fallback。
- 不改前端。

## 任务

1. 明确缺 tenant/project/run/result/task 时的统一行为。
2. 禁止默认查询“最近一次”或“全局最近”策略。
3. 复用已批准的统一响应体与唯一失败码。

## 产物

- 缺失类型清单（missing tenant/missing run/missing id）。
- 统一失败码映射（401/400/404 之一）。

## 固定规则

- `tenant_id` 缺失或空字符串：`401`（缺少身份域上下文）。
- 任意来源 `*_id` 缺失、类型不合法、空白字符串：`400`。
- source_id 不在已允许对象类型内：`400`，不做回退。
- 同时缺 `tenant_id` 与对象参数：仍按缺 `tenant` 优先返回 `401`。
- 禁止默认回退：“最近一次/全局最近”策略一律不可执行，统一返回 `400`。

## 统一响应（固定）

- 关键参数缺失、空白上下文、非法来源类型均复用 `8a.1a.3a` 的 `400` 固定体：`{"error_code":"secretary_request_invalid","message":"Request is invalid."}`。
- 只允许 `error_code`、`message`；不得返回 `error`、`code`、来源类型、实体 ID、状态或对象存在性提示。
- 固定体不得因缺失字段、空白字段或来源类型改变。

## 结果（本批次）

- 状态：PASS（来源缺失场景定义完成；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate.md`
Objective:
定义来源缺失与空上下文 fail-closed 行为。
Special Constraints:
只读定义；不新增路由。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
