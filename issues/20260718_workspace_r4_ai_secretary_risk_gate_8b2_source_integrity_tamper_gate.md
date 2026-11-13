# Workspace R4 第8项｜8b.2｜来源完整性与篡改防护 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（真实字段与响应契约已对齐；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_ai_secretary_risk_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

把 AI Secretary 的建议输出限定为 run/result/audit 的可追溯链，防止引用错配、摘要空洞或状态漂移。

## 约束

- 不新增模型调用
- 不新增前端接口
- 不回填历史 run

## 完整性规则（8b.2，按真实来源）

### `workflow_runs`

- 仅以 `(tenant_id, workflow_run_id)` 定位；`company_id`、`project_id`、`workflow_instance_id`、`workflow_template_id`、`department_id`、`task_id` 只与该行本源值核验。
- 已存在对象与请求的 tenant/作用域/关联值错配，或 schema 无法证明请求所需关系为 `403`；对象、必要本源值缺失、不可见或状态不可安全承接为 `404`。

### `step_results`

- 仅以 `(tenant_id, step_result_id)` 定位，且只允许 `step_results.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_step_id) → workflow_steps.(tenant_id, workflow_run_id) → workflow_runs.(tenant_id, workflow_run_id)` 证明 Step→Run 归属。
- 任一必经对象或中间行缺失/不可见为 `404`；对象均存在但 tenant、Step→Run 或 Run 作用域值错配为 `403`。
- 不存在 `step_results.workflow_run_id`，不得补 `source_run_id/source_step_id/source_result_id` 通用别名。

### `content_publish_packages`（API 投影名 `publish_packages`）

- 仅以 `(tenant_id, package_id)` 定位并核验 `tenant_id`、`package_id`、`created_at`、`status`；`source_workflow` 是本源文本，不是 RD Run/Step/Result 外键。
- 对象缺失/不可见/状态不可安全承接为 `404`；已有对象 tenant 错配，或请求 project/company/RD workflow/run/step/result 等本表没有可证路径的关系为 `403`。

### `content_workflow_runs`

- 仅以 `(tenant_id, run_id)` 定位并核验 `tenant_id`、`run_id`、`workflow_content_id`、`department_id`、`created_at`、`status`。
- 该 `run_id` 只属于内容状态机，不等于 RD `workflow_runs.workflow_run_id`；对象缺失/不可见/状态不可安全承接为 `404`，已有对象 tenant/本源关系错配或请求关系没有可证路径为 `403`。

### 内部完整性分类

- `CONFLICT`：同一请求内已核验的本源记录或必经中间行出现非作用域值冲突；仅写内部 `fail_code`，对外映射 `404`。
- `STALE_CONTEXT`：来源已不在批准可读终态或不能安全承接；仅写内部 `fail_code`，对外映射 `404`。
- 两者均不得进入响应字段、文案或状态码，不得对外使用 `409`、`423`。

## 篡改拒绝场景

- 已存在对象的 tenant、作用域或可证关系错配：`403`，固定体 `{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}`。
- 主对象、必经中间行缺失/不可见，或内部 `CONFLICT/STALE_CONTEXT`：`404`，固定体 `{"error_code":"secretary_source_unavailable","message":"Source is unavailable."}`。
- 对外响应只允许 `error_code`、`message`；内部 `fail_code`、来源类型、ID、状态、scope、命中字段和调试信息均不得返回。
- `summary`、`next_step_hint` 仅在来源通过 exact allowlist 且内容来自 8a.3b 安全批准的预定义非敏感状态模板时允许；来源、模板或完整性验证失败时优先省略，省略后不满足契约则按对应失败类别整体拒绝。

## 固化原则

- 不返回“这个 id 是否存在”的可枚举差异。
- 任一不一致都不允许 fallback 到历史版本或替代来源。
- 禁止现场哈希或持久化新哈希，禁止同名 ID、名称匹配、字符串拼接、默认值、“最近一次”或裸文本推断关系。
- 篡改文本、历史版本替代和自动 fallback 均不是来源证明；拒绝后不继续查询关联对象，不返回 partial、空对象或降级成功。
- 所有完整性拒绝必须在 Adapter/模型调用/出网前完成；日志不得包含 prompt、payload、token、credential、Cookie、JWT、Authorization、模型原文、裸文本快照或用户原文。

## 任务成果

- 完成来源完整性判定清单。
- 明确摘要/可追溯字段必须有归档来源。
- 缺失、错配、漂移统一 fail-closed。

## 复核入口

- `issues/20260718_workspace_r4_ai_secretary_risk_gate.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md`
Objective:
定义 source run/result 的完整性与篡改防护边界。
Special Constraints:
只读定义；仅输出可追溯、可核验字段。
Next Seat:
质量运行席


## 结果（待复核）

- 已按 8a.3a 真实字段与 8b.1 全局响应映射修正，等待质量运行席 focused 复核。
- `8b.3` 在本 Gate 质量 PASS 前继续冻结。

Handoff: sent to 质量运行席
