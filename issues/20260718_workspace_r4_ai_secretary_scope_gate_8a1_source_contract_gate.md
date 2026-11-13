# Workspace R4 第8项｜8a.1｜AI Secretary 来源范围边界 Gate

- 日期：2026-07-18
- 状态：IN_PROGRESS — 8a.1a/8a.1b/8a.1c PASS（待质量复核），等待父项汇总复核
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（先写边界）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

明确 Secretary 可消费输入边界：限定只能读历史真实结果与成果索引，不接受任意外部文本。

## 约束

- 只读定义，不改数据库结构，不改现有运行逻辑。
- 不起新 run。
- 不新增模型、外部连接、凭据。

## 任务

1. 明确“可承接来源”三元组：`workflow_runs` + `step_results`、`publish_packages`、`content_workflow_runs`。
2. 明确每条来源的租户/项目/公司/员工作用域字段映射。
3. 明确来源失配后的拒绝码与行为（不漏数，不泄露）。

## 子任务（本轮）

- 8a.1a｜来源对象白名单与字段映射（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
  - 固定 `workflow_runs.id`、`step_results.id`、`publish_packages.id`、`content_workflow_runs.id` 入参映射。
  - 约束 tenant/project/company/department/employee/workflow/task 五元组必须全部可核验。
  - 仅允许归档/完成态引用（可复用现有可见读源）；其余直接拒绝。
  - 产物：字段白名单 + 失败行为映射表。

- 8a.1b｜来源缺失与空上下文拒绝（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate.md`
  - 查询参数/上下文 ID 缺失时直接 fail-closed。
  - 禁止默认回退到最近一次/全局历史。
  - 产物：缺失类型与统一 401/404 映射。

- 8a.1c｜来源错配隔离（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md`
  - `workflow_run_id` 与 `project_id`、`tenant_id` 必须一致；`publish_package` 与 `run` 来源关联必须完整一致。
  - 一条来源错配即拒绝本次查询，不返回部分对象。
  - 产物：错配测试清单。

## 最低验收

- 仅允许来源为已归档真实运行/成果，缺失字段直接 fail-closed。
- 允许字段集固定清单，其他路径拒绝。
- 不允许通过 query 参数注入空白上下文。

## 结果（本批次）

- 状态：进行中。8a.1a/8a.1b/8a.1c 已完成定义（待质量复核），等待 8a.2/8a.3 汇总复核。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`。

## 执行顺序

8a.1a（已完成定义，待质检）→ 8a.1b（已完成定义，待质检） → 8a.1c（已完成定义，待质检） → 8a.2a（PASS）→ 8a.2b（PASS）→ 8a.2c（PASS）→ 8a.3a/3b/3c（PASS）

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`
Objective:
定义 Secretary 可承接来源边界。
Special Constraints:
只读边界定义；不新增接口。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
