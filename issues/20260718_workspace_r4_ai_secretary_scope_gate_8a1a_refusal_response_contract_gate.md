# Workspace R4 第8项｜8a.1a.3a｜拒绝响应固定体契约 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_refusal_status_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
- Owner：系统交付席（契约固化）→ 质量运行席（复核）→ 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

把 8a.1a 的拒绝响应固定为可比较的最小响应体，避免来源类型、实体存在性或状态通过错误内容泄露。

## Exact 响应体

| HTTP | 响应体（字段与值必须完全一致） |
| --- | --- |
| 401 | `{"error_code":"secretary_access_required","message":"Access context is required."}` |
| 400 | `{"error_code":"secretary_request_invalid","message":"Request is invalid."}` |
| 403 | `{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}` |
| 404 | `{"error_code":"secretary_source_unavailable","message":"Source is unavailable."}` |

## 约束

- 只允许 `error_code`、`message` 两个字段；不得返回 `detail`、来源类型、任意 ID、状态、tenant/company/project/department/task/workflow、命中字段、查询路径、调试信息或部分对象。
- 同一 HTTP 类别下，无论来源对象、ID、实体是否存在、状态不可读或关联失配，响应体必须与上表完全一致。
- 仍沿用 `401 > 400 > 403 > 404`，仅输出一个状态码；拒绝后不得查询关联表。
- 仅固化契约与 focused 复核，不新增 Secretary API、模型调用或运行时。

## 验收

- 对四类来源对象的存在/不存在、状态不可读、作用域失配反例，逐一比对同类响应体仅含上述两个字段且完全一致。
- 质量运行席写 Review；PASS 后才解除 8a.1a.3 阻塞并进入 8a.1b。

## 实施证据

- 契约 focused：`backend/tests/test_ai_secretary_refusal_response_contract.py`。
- 命令：`.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_refusal_response_contract.py`。
- 结果：`4 passed in 0.02s`。
- 范围：仅固化本 Issue 与静态契约复核；未新增 Secretary API、模型调用或运行时。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate.md`
Objective:
固化拒绝响应固定体，消除来源存在性与状态泄露。
Special Constraints:
仅契约/focused复核；不新增接口或运行时。
Next Seat:
系统交付席

Handoff: sent to 系统交付席
