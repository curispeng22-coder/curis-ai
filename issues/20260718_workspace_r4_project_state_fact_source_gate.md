# Workspace R4 项目状态事实源映射 Gate

- 日期：2026-07-18
- 状态：PASS — A1/A2/A3 已闭环
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

定义“项目长期状态”的唯一事实源，形成可直接查询/复用的状态映射：
`workflow_runs` / `workflow_tasks` / `workflow_steps` / `step_results` / `executions` / `usage_events` 的最小读链映射到 `Project` 长期状态字段，明确优先级与缺失回退。

## 背景

第四轮第1项需要先完成“长期状态来源唯一化”，否则恢复、会话衔接与 Memory 无法闭环。此 Issue 只做边界定义与最小验证，不改运行语义，不改模型调用，不改前端。

## Must Do

1. 明确单项事实源：给出每个长期状态字段（如 `status`、`progress`、`last_step`、`last_failure`、`last_cost`、`last_model`）的唯一来源优先级。
2. 明确不可写路径：禁止直接更新 `projects.status` 为强行修复；仅允许基于执行事实计算（只读或已有衍生接口）。
3. 明确跨租户与 run 归属边界：state 只可按 tenant/project/run 读写路径访问。
4. 列出最小聚焦验证（建议1次）命令/查询，覆盖：
   - status 与 run terminal state 一致性；
   - step/execution/usage 与最终报告映射一致性；
   - 跨租户 404/403 fail-closed 不被误读。

## 工单拆分

- A1｜事实源映射定义（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_project_state_fact_source_a1_mapping_gate.md`
  - 输出：字段映射表（字段名 / 来源表 / 优先级 / 缺失回退）。
  - 目标：至少覆盖 `status, progress, last_step, last_event_time, last_failure_code`。

- A2｜跨租户与可见域边界（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_project_state_fact_source_a2_tenant_scope_gate.md`
  - 输出：一页边界规则（tenant_id/project_id/run_id 限定）。
  - 目标：任何未授权查询返回空/403/404，禁止越权读取。

- A3｜focused 复核（质量运行）
  - 跳转 Issue：`issues/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate.md`
  - 输出：一组命令 + 预期样例（1次）；
  - 目标：run 终态、步骤数、usage 计量与最终报告一致可复核。

## 任务链（本 Issue）

- A1 → A2 → A3（完成顺序）

## 当前进展

- A1：PASS；产出字段映射与缺失回退规则，并完成复核对齐。
- A2：PASS；产出 tenant/project/run 可见域与 fail-closed 规则，并完成复核对齐。
- A3：PASS；focused 复核完成，结果已写入 `reviews/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate_review.md`。

## 验收标准

- 文档化出“项目长期状态事实源映射表”（字段+来源+优先级+缺失行为）。
- 不触达新增 API/Schema/Model；不新增前端；不新增数据库。
- 产出一条可复核的验证命令和预期结果。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_project_state_fact_source_gate.md`
Objective:
确定项目长期状态的唯一事实源映射与优先级，并形成最小验证路径。
Special Constraints:
仅定义与读链验证；不改 `projects` 写入链路；不跨越第2项。
Next Seat:
系统交付席
