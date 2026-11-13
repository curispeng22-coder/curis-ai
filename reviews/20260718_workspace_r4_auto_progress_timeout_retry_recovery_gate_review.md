# 2026-07-18 Workspace R4 第4项｜自动推进/超时/恢复 Focused 复核 Gate Review

- Issue：`issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 审核结论：`PASS`

## 审核摘要（本次可复核部分）

- 4a（推进口径）：
  - PASS（静态+可复测）
  - 依据：`backend/app/workflow_runtime.py:336-347,350-397`  
    - run 已成功/失败/取消时不再推进；
    - 仅按 `step_order` 选择首个 `pending`，且存在 `failed` 则立即 `run.failed`；
    - 顺序推进样本覆盖可通过 `backend/tests/test_phase6_workflow_mvp.py::test_workflow_run_executes_sequential_employee_steps_and_records_redacted_events`（7 步序列）验证。
- 4b（超时与阻断）：
  - PASS（有上限边界；不提供恢复窗口字段）
  - 依据：`backend/app/model_gateway.py` 默认 `timeout=60`（r3 profile 通过同参数发起）；无出网重试逻辑，错误会按单次调用失败抛出。
  - 可复核样本：`backend/tests/test_model_gateway_adapter.py::test_r3_contract_uses_fixed_path_limits_and_approved_price`、`...::test_r3_workflow_failure_stops_without_retry`、`...::test_r3_contract_classifies_429_without_retry_or_secret_leak`。
- 4c（恢复与人工接管）：
  - PASS（只读派生版本收口）  
    - 4c 已给出仅读式恢复判定：`recoverable` 不落库，不新增字段，仅靠 `workflow_runs.status/failed_at` + `workflow_steps(step_status,step_order,error)` + 失败时长窗口计算输出；
    - 超过 `recover_window_sec=900`（15 分钟）需人工主线程确认，不做自动续推；
    - 人工接管动作固定为「不改历史、只读核验、确认后新建 run」，不可自动回改 `workflow_runs/status` 或 `step_results/usage_events`。

## 结论

`4a/4b/4c` 均按不改实现、不改历史的边界定义闭环。  
  - 4a：`workflow_runtime.run_next_step` 现状满足顺序/停机/失败阻断边界。  
  - 4b：`ModelGatewayAdapter` 提供单次调用上限与无重试阻断行为；未见扩展出站重试。  
  - 4c：新增恢复脚本为只读派生，强调跨租户隔离与人工决策，不变更历史。  

不进入新 Run 新建/重跑；不改历史。

## 建议动作

1. 由系统交付固定 4a/4b/4c 文字边界定义（已完成）；  
2. 质量运行席沿本样本完成 focused 读证核验（已完成）；  
3. 本 Issue 已更新为 PASS，可转第5项。

Handoff: sent to 产品规划席
