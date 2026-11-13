# Workspace R4 第1项子Issue B2｜恢复演练与不可逆边界

- 日期：2026-07-18
- 状态：PASS — 质量复核完成
- 前置：`issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md`
- 父项：`issues/20260718_workspace_r4_project_memory_recovery_path_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席
- 分支：`feat/roadmap-r1r2`

## 目标

给出一条可复现的从失败/中断到可继续推进边界判断的最小恢复演练：明确输入、判定、终态与不可逆字段。

## Must Do

1. 定义演练输入（历史失败 run 标识与可见事实集）。
2. 定义恢复动作（读取→判定→继续边界）与终态判据。
3. 明确不可逆字段、跨 Tenant/Project 回退规则。
4. 给出复盘记录模板（输入/操作/输出/边界）。

## 演练前提

- 复用 B1 v1 scope 规范。
- 本演练为只读记录，不发起任何出网与模型调用。
- 演练数据源：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 示例历史失败 run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`（tenant-a/project-e84e06d4-f014-4326-abcd-e6d9aea6ff95）。

## 演练输入

- `tenant_id = tenant-a`
- `project_id = project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`
- `workflow_run_id = wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- `task_id = 285e3bb5-3fd5-4bd9-9eff-4cbd53e11d7b`

## 演练步骤（只读）

1. 读取 run 事实
   - 通过 API：`GET /api/workspace/workflows/{workflow_run_id}`（`X-Tenant-Id: tenant-a`）
   - 记录 `status`, `steps`, `step_results`, `usage`。
2. 校验 scope 一致性
   - `tenant_id` 与 `project_id` 必须与 scope 一致。
   - `workflow_run_id` 对应行必须唯一。
3. 推断恢复决策
   - 若 `run.status != pending/running`，判定为不可直接续推。
   - 若 `run.status in {pending,running}` 且 `steps` 中存在 `pending`：可定义继续边界为“next pending step”。
4. 若不可续推，输出恢复建议
   - 该场景应形成**新建 Run**建议，而非回写旧 run。
5. 记录不可逆字段
   - 对 failed run：不得改写 `workflow_runs.status`、`workflow_steps/error`、`step_results`、`evolution_events`。
   - `project.status` 及历史 `final_report` 仅可读、不得变更。

## 预期结果（当前示例）

- 输入 run：
  - `status = failed`
  - step1~5 `succeeded`，step6 `failed`，step7 `pending`
  - usage 仅出现 5 条（step1~5）
  - 无 final report 写入（`final_report=''`）
- 恢复决策：**不可直接续推**（终止于历史失败状态）。
- 可继续动作：在同 tenant/project 下创建新 run 执行新链路；并保留失败 run 作为历史边界。

## 不可逆边界

- `run.status=failed` 一旦形成，不得通过 Memory 读取“逆向修复”为 succeeded。
- 任何 `usage`/`step_error` 字段在失败链路中只能做审计读取，不得在恢复演练中变更。
- 跨 project/跨 tenant 的恢复匹配按 `tenant_id + project_id` 严格 fail-closed。

## 复盘记录模板（示例）

- 输入：`tenant_id/run_id/task_id`
- Scope：`scope_version=workspace.project_memory.scope.v1`
- 读取摘要：run status、steps、results count、usage count、project_id match
- 判定：`recoverable=true/false`
- 行为：不可续推则 `create-new-run`，否则 `resume-next-step`
- 输出：恢复结果/边界清单（跨租户失败、不可逆字段、历史保持）

## 兼容声明

- 本演练不要求补齐历史字段，不改历史失败前提；只做最小恢复判定定义。
- 与 R3 历史证据兼容：失败 run 与成功 run 共存，历史不变。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`
Objective:
形成 1 条最小恢复演练与不可逆边界闭环。
Special Constraints:
本 Issue 仅定义与复核演练，不发起模型调用，不改 API，不改历史数据库。
Next Seat:
质量运行席（B3）
