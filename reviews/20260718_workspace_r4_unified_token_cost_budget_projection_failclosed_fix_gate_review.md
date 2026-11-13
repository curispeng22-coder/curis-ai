# Workspace R4 第7项｜成本投影 fail-closed 修复 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_unified_token_cost_budget_projection_failclosed_fix_gate.md`
- 分支：`feat/roadmap-r1r2`
- 固定 SHA：`fb827c37f4b7e7202326dc94e5648de6a4c8200c`
- 结论：`PASS`
- 8a 冻结：`可解除`

## 结论

前次审计发现的真实零成本 fail-open 已关闭。合法七步投影仍返回 `artifact` 且 `execution_status=completed`；任一 usage 的成本或价格版本不可信时，投影保持 `artifact=null` 并把 `execution_status` 降为 `incomplete`。

唯一缺口：无。

## 变更范围核对

提交只修改：

- `backend/app/workflow_runtime.py`：在 `_add_read_projection` 增加成本与 `price_version` 可信性判断。
- `backend/tests/test_model_gateway_adapter.py`：增加一个合法基线加反例集合的 focused 测试。

未修改 schema、API、模型调用、网关、预算上限、历史数据或前端。

## 独立代码核对

投影现在要求：

- `estimated_cost` 必须是非 bool 的有限数字且 `> 0`；
- 每条 usage 的 `price_version` 必须是非空字符串；
- 7 条 usage 的 `price_version` 必须完全一致。

任一条件不成立时，`artifact` 保持初始化值 `None`，`project_status.execution_status` 设为 `incomplete`，并在金额求和前返回。

## Focused 复核

执行：

```text
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q \
  backend/tests/test_model_gateway_adapter.py \
  -k 'r3_workflow_allows_seven_ordered_steps_once or r4_projection_rejects_untrusted_cost_and_price_metadata'
```

结果：`2 passed, 19 deselected`。

覆盖结果：

| 场景 | Artifact | execution_status |
| --- | --- | --- |
| 合法 7-step、正成本、同一非空 price_version | 非空 | `completed` |
| 成本缺失 | `null` | `incomplete` |
| 成本非数字 | `null` | `incomplete` |
| 成本为 0 | `null` | `incomplete` |
| 成本小于 0 | `null` | `incomplete` |
| price_version 缺失 | `null` | `incomplete` |
| price_version 非字符串 | `null` | `incomplete` |
| price_version 不一致 | `null` | `incomplete` |

静态核对还确认 bool、NaN、Infinity 成本同样被拒绝。`git diff --check` 通过。

## 范围声明

- 未修改实现。
- 未启动服务、未注入凭据、未出网。
- 未运行全量回归。
- 未改 schema/API/历史数据。

## 最终状态

该修复 Gate 为 `PASS`。第1～7项审计中的唯一阻塞已关闭，可以解除 8a 冻结并恢复 `8a.1a.2`。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
