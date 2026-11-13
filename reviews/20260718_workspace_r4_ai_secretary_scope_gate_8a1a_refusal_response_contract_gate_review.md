# Workspace R4 第8项｜8a.1a.3a 拒绝响应固定体 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`ff050e1fc251ebeeae57a30685a78c63c0ae1ad5`
- 结论：`PASS`

## 结论

8a.1a 拒绝响应已固定为可直接比较的 exact body；此前“响应体未定义、无法验证不泄露实体差异”的唯一阻塞已关闭。可解除 8a.1a.3 阻塞并进入 `8a.1b`。

唯一缺口：无。

## 独立核对

| HTTP | Exact body |
| --- | --- |
| `401` | `{"error_code":"secretary_access_required","message":"Access context is required."}` |
| `400` | `{"error_code":"secretary_request_invalid","message":"Request is invalid."}` |
| `403` | `{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}` |
| `404` | `{"error_code":"secretary_source_unavailable","message":"Source is unavailable."}` |

- 响应仅允许 `error_code`、`message` 两个字段；`detail`、来源类型、实体 ID、状态、作用域字段、查询路径、调试信息和部分对象均被明确禁止。
- 同一 HTTP 类别不因来源对象、ID、存在性、状态不可读或关联失配而改变响应体。
- 优先级保持 `401 > 400 > 403 > 404`，每次只返回一个状态码；命中拒绝后不得继续查询关联表。

## 新鲜证据

固定分支与修订核对：`feat/roadmap-r1r2 @ ff050e1f`。提交仅新增本 Issue 与一个 focused 契约测试，未修改 Secretary API 或运行时。

```text
.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`4 passed in 0.01s`。覆盖 exact 四响应体、两字段白名单、同 HTTP 固定体、拒绝优先级和关联查询短路契约。

`git diff --check ff050e1f^ ff050e1f`：通过。

## 范围声明

- 本 Review 仅确认静态响应契约闭合，不声称 Secretary API 或运行时已经实现。
- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
