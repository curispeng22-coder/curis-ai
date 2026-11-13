# Workspace R4 第8项｜8a.3b｜敏感字段过滤 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（分来源 allowlist 与安全拒绝契约已固化；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3_output_projection_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

定义输出脱敏规则，禁止泄露原始 prompt、tool payload、token 文本与凭据信息。

## 约束

- 不改前端。
- 不改历史数据结构。
- 不触发新模型调用。

## 任务

1. 明确不允许返回字段清单（prompt、raw tool payload、模型 token 文本、凭据标识、敏感 headers）。
2. 定义可返回字段级别的最小化策略。
3. 给出反例样本（包含敏感字段）拒绝输出示例。

## 禁止字段（Denylist）

- `prompt`
- `raw_prompt`
- `tool_payload`
- `model_input_text`
- `token_text`
- `token_payload`
- `api_key`
- `authorization`
- `cookie`
- `set-cookie`

## 分来源可返回最小字段（Allowlist，exact）

### `workflow_runs`

- 允许：`tenant_id`、`workflow_run_id`、`company_id`、`project_id`、`workflow_instance_id`、`workflow_template_id`、`department_id`、`task_id`、`created_at`、`status`。
- 所有字段必须来自同一 `(tenant_id, workflow_run_id)` 行。

### `step_results`

- 允许直出：`tenant_id`、`step_result_id`、`workflow_step_id`、`employee_id`、`created_at`、`status`。
- 允许关联：`workflow_run_id`，但仅能通过 `step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)` 核验后返回。

### `content_publish_packages`（API 投影名 `publish_packages`）

- 允许：`tenant_id`、`package_id`、`created_at`、`status`。
- `source_workflow` 是本源文本而非可证外键，不进入本最小输出 allowlist。

### `content_workflow_runs`

- 允许：`tenant_id`、`run_id`、`workflow_content_id`、`department_id`、`created_at`、`status`。
- 该 `run_id` 只代表内容状态机，不得改名或推断为 RD `workflow_run_id`。

### Allowlist 固定边界

- 不允许通用 `source_run_id`、`source_step_id`、`source_result_hash`；不得为不同来源补齐同形字段。
- `result`、`final_report`、`summary`、`artifacts`、`source_workflow`、`next_step_hint` 均不在本最小 allowlist；不得以现场哈希、摘要、默认值或裸文本替代来源引用。
- 不得使用同名 ID、名称匹配、字符串拼接、前后缀替换或“最近一次”推断跨状态机关系。
- 请求字段不在对应来源 allowlist、必需 ID 缺失或关系不可证时 fail-closed，不返回部分投影。

### 安全裁定（PASS，exact）

- 响应投影的任意字段、嵌套字段或敏感文本伪装命中 denylist 时，整体拒绝，唯一 HTTP 状态为 `403`。
- 固定响应体：`{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}`。
- 响应体只允许 `error_code`、`message`；不得包含 `fail_code`、命中字段名、来源 ID、状态、scope、实体存在性或调试字段。
- `SENSITIVE_PROJECTION_REJECTED` 仅作为内部固定日志 `fail_code`，不得进入对外响应；不得剔除后继续，不得返回 partial、空对象、`summary` 或 `next_step_hint`。
- 日志只允许 `timestamp`、`tenant_id`、`project_id`、`run_id`、`task_id`、`fail_code`、`step` 七个字段；不得记录 principal 原值或派生字段、denylist 命中值、prompt、payload、token、credential、Cookie、JWT、Authorization、`summary` 或 `next_step_hint` 原文。
- `summary`、`next_step_hint` 不是来源字段，只能在未命中 denylist、来源通过 exact allowlist 且内容来自预定义非敏感状态模板时作为模板投影返回；不得拼接或回显任何原始文本。
- 无法证明模板来源或安全性时省略该字段；若省略后整体投影不满足契约，则使用上述固定 `403` 整体拒绝。
- 该裁定来自 `reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_security_review.md`；不允许输出上下文敏感 headers，不记录未脱敏原始字符串。

## 结果（本批次）

- 状态：IMPLEMENTED（分来源真实字段 allowlist 与 denylist 唯一 403 行为已完成；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3_output_projection_gate.md`。
- `8a.3c` 在本修复 Gate 获得质量 PASS 前继续冻结。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md`
Objective:
定义 Secretary 输出敏感字段过滤规则。
Special Constraints:
只读输出约束；不新增网关。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
