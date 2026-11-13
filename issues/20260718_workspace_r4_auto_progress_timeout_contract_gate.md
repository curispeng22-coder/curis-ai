# Workspace R4 第4项｜第4b｜超时与阻断边界 Gate

- 日期：2026-07-18
- 状态：PASS — CLOSED（超时/阻断边界已确认）
- 前置：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- 父项：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

定义超时与阻断边界：单次调用、等待窗、恢复窗口如何判定，不触发无限等待，不做新服务。

## 约束

1. 不改现有出网实现。
2. 不发起真实调用。
3. 不新增凭据路径、环境变量、scheduler。
4. 单轮只给出参数与判定，不实现新执行器。

## Must Do（结论）

- 固定 `run-next-step` 单次可用超时上限：`single_request_grace`（仅用于判定，不新建定时器）。
- 固定恢复观察窗：`recover_window_sec=900`（15 分钟）；
  超过观察窗仅允许人工/主线程决策，不自动恢复。
- 失败后阻断规则：超时/网络异常按“失败 + 停止自动推进 + 记录可见原因”处理。
- 明确可观测字段（至少）：`run_id`、`step_id`、`step_order`、`status`、`error_code`、`error_detail`。

### 边界定义（仅定义）

- `single_request_grace_sec = 60`（来自 `ModelGatewayAdapter.timeout`，未改实现）
- `max_input_tokens = 8192`（上限）  
- `max_output_tokens = 2048`（上限）  
- `max_total_tokens = 10240`（上限）  
- `max_call_cost_usd = 0.10`（预算上限）
- 失败分支立即 `failed`，无重试/无退避；异常只保留一次失败记录。

### 复核结果（只读）

- 静态证据：`backend/app/model_gateway.py`（`ModelGatewayAdapter.__init__` 与 `validate_runtime_config`、`execute`）
- 无出网样本：`backend/tests/test_model_gateway_adapter.py`
  - `test_r3_contract_uses_fixed_path_limits_and_approved_price`
  - `test_r3_workflow_failure_stops_without_retry`
  - `test_r3_contract_classifies_429_without_retry_or_secret_leak`
- 超时/阻断策略：单次调用失败后转为阻断，不做无限等待。

## 参考复核样本（只读）

- `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`（历史失败 run）。
- `wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（完整成功 run）。

## 交付

- 输出：第4项统一超时/阻断参数与判定表。
- 输出形式必须可被 `Quality` 在第4d 作为 focused 脚本复核依据。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_auto_progress_timeout_contract_gate.md`
Objective:
给出单次调用与恢复窗口的超时/阻断上界与可复核判定。
Special Constraints:
只定义，不实现；不改 `run-time`；不改前端；不改历史。
Next Seat:
产品规划席
