# 2026-07-18 Workspace R4 第5项｜人工接管入口与动作边界 Gate Review

- Issue：`issues/20260718_workspace_r4_manual_takeover_request_contract_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 审核结论：`PASS`

## 复核对象

- `issues/20260718_workspace_r4_manual_takeover_request_contract_gate.md`
- `backend/app/main.py`（接口列表）
- `backend/app/workflow_runtime.py`（失败与顺序推进逻辑）

## 结论

5b 已闭环为**只读人工接管口径**：

- 不提供 cancel/reset/reopen 接口，仅允许读取查询 + 新建新 run；
- 人工接管入场为 failed + failed step 存在 + 负责人确认，且不得改写历史；
- 接管动作唯一化为「创建新 run」；
- 明确了 Stop/Hold/Escalate/Create-New-Run 决策模板与不可逆字段锁。

## 关键证据

- 路由限制：`backend/app/main.py` 仅暴露 `run-next-step`、`GET /api/workspace/workflows/{workflow_run_id}`、`POST /api/workspace/workflows`；未提供 reset/cancel/reopen。
- 失败停止：`backend/app/workflow_runtime.py` 在发现失败 step 后终止后续推进，`run.status` 标记失败并写入 `workflow.step.failed` / `workflow.run.failed`。
- one-shot 复核 SQL（issue 内定义）可复现 failed step、不可逆计数、决策链。
- 现有库中 failed 失败样本可见且无历史回改痕迹。

Next Seat: 产品规划席
