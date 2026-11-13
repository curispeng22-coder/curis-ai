# Workspace R4 第8项｜8a.1b 来源缺失与空上下文拒绝 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1b_missing_context_refusal_gate.md`
- 分支：`feat/roadmap-r1r2`
- 复核基线：`ff050e1fc251ebeeae57a30685a78c63c0ae1ad5`
- 结论：`PASS`

## 结论

来源缺失、空上下文和非法来源类型的 fail-closed 边界完整；tenant 缺失优先 `401`，其余来源参数错误统一 `400`，且禁止“最近一次/全局最近”回退。`400` 完整复用 8a.1a.3a 固定体，不因缺失字段或来源类型泄露差异。

唯一缺口：无。可推进 `8a.1c`。

## 独立核对

| 场景 | 唯一结果 |
| --- | --- |
| `tenant_id` 缺失或空字符串 | `401`；优先于其它参数错误 |
| 任意来源 `*_id` 缺失、空白或类型非法 | `400` |
| 来源类型不在四类批准白名单 | `400` |
| 同时缺 tenant 和来源参数 | `401` |
| 请求“最近一次/全局最近”或未给明确来源 | `400`，不得回退查询历史数据 |

`400` exact body：

```json
{"error_code":"secretary_request_invalid","message":"Request is invalid."}
```

- 仅允许 `error_code`、`message`。
- 不得返回缺失字段名、来源类型、实体 ID、状态、存在性或部分对象。
- 缺失、空白、类型非法和禁止回退场景不得改变该响应体。

## 新鲜证据

```text
.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`4 passed in 0.01s`。确认 `400` 固定体、两字段白名单、同 HTTP 响应不随来源差异变化，以及 `401 > 400 > 403 > 404` 优先级契约。

静态复核当前 Issue 确认 tenant 优先、来源参数统一 `400` 与禁止最近一次回退均有明确单值规则。

## 范围声明

- 本 Gate 是只读契约复核，不声称 Secretary API 或运行时已经实现。
- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
