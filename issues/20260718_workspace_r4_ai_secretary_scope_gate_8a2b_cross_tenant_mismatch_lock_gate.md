# Workspace R4 第8项｜8a.2b｜跨租户与错配封锁 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2a_status_code_singleton_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

定义 tenant/project/run/result/task 维度的错配封锁口径，跨租户一律拒绝，不能降级读取。

## 约束

- 不重试、不中间补偿、不可降级继续。
- 不改前端。
- 不改现有出网逻辑。

## 任务

1. 定义跨租户 mismatch 的统一拒绝规则。
2. 定义 run/result/task 三元关联 mismatch 的统一拒绝规则。
3. 约束“匹配未通过即整体拒绝”，不返回部分对象。

## 统一规则（fail-closed）

- 首先校验请求 tenant 与目标对象 tenant 一致，不一致直接 `401`（无上下文）或 `403`（已验证但非授权），不继续查询。
- Project 必须属于同一 tenant，并与 run/workflow/workspace 作用域一致，不一致直接 `403`。
- `run_id`、`task_id`、`step_result_id` 的已有可核验关联链必须闭合：必经对象或中间行未命中为 `404`；对象均存在但 tenant/关联值不一致为 `403`。不返回 partial。
- `publish_package_id`、`content_workflow_run_id` 仅核验已存在的本源字段与 tenant；没有可核验 project/run/task 关系时必须拒绝（`403`），不得推断或拼接关联。
- 对象可见性不足时返回 `404`，与存在性区别统一隐藏。
- 统一禁止默认回退：即便 tenant/project 不匹配，也不得返回其他 tenant 的空列表或提示。

## 匹配矩阵（最小）

- `tenant_id` mismatch：`403`（或 401，若身份上下文缺失）。
- `project_id` mismatch：`403`。
- `workflow/task/run` mismatch：`403`。
- `step_result` 无效关联 run：`403`。
- `publish_package/content_workflow` 的本源关联不可证：`403`。

## 结果（本批次）

- 状态：PASS（跨租户与错配封锁规则定义完成；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate.md`
Objective:
统一定义跨租户与来源错配封锁。
Special Constraints:
只读定义；不触发重算。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
