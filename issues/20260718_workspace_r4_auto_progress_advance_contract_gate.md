# Workspace R4 第4项｜第4a｜自动推进合规模型 Gate

- 日期：2026-07-18
- 状态：PASS — CLOSED（自动推进闭环定义已确认）
- 前置：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- 父项：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

给出“何时自动继续、何时停机、何时转人工恢复”的最小推进契约，先从现有 run-next-step 事实链推导，不改执行器、不改数据库。

## 约束

1. 不改 `ModelGatewayAdapter`、网关、Provider/Model、凭据边界。
2. 不改数据库 Schema。
3. 不发起新建 Run，不改历史失败。
4. 不新增外部服务，不改前端。

## Must Do（结论）

- 定义自动推进触发条件：
  - 当前 `run.status` 非 `succeeded/failed/cancelled`；同时不存在任意 `workflow_steps.status='failed'`。
  - 只选同 run 的首个 `pending` 步骤（按 `step_order` 最小优先）。
  - 当前步骤角色、员工、能力绑定检查通过后才继续执行。
- 定义停机条件：
  - 任何 `run.status in (succeeded/failed/cancelled)` 不再继续推进。
  - 发现任一 `failed` 步骤时，立即 `workflow_runs.status=failed`，不再进入下一步。
- 定义安全禁止条件：
  - 同 run 同一时刻只允许推进一个 `pending` 步骤，未完成状态不会形成重复运行。
  - 步骤跨租户/跨 project 不可续推。
- 给出最小可复核脚本（只读）：
  - 顺序推进：取同 run 首个 `pending` + `step_order`，其前序全部 `succeeded` 才运行。
  - 阻断边界：`run.status in (succeeded/failed/cancelled)` 或 `exists failed_step` 直接返回。
  - 幂等验证：同一 run 重复触发时，仅第一条 `run-next-step` 可产生状态变更。

### 复核结果

- 静态证据：`backend/app/workflow_runtime.py:336-397`（`run_next_step` 行为）
- 顺序样本：`backend/tests/test_phase6_workflow_mvp.py::test_workflow_run_executes_sequential_employee_steps_and_records_redacted_events`
- 失败阻断样本：`backend/tests/test_phase6_workflow_mvp.py::test_failed_step_marks_workflow_failed`

## 参考复核样本（只读，来自已有历史）

- `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`：step1 failed。
- `wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`：running；可复核中间步骤未越界。

## 交付

- 输出：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md` 用于主项收口的推进-停机-失败条件定义稿（已闭环）。
- 产出不可含“无限重试/后台调度器/新状态机”。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_auto_progress_advance_contract_gate.md`
Objective:
定义 run-next-step 的自动推进触发、停机与非法并发边界。
Special Constraints:
不改 runtime 行为，不改 DB，不发新 Run，不改前端。
Next Seat:
产品规划席
