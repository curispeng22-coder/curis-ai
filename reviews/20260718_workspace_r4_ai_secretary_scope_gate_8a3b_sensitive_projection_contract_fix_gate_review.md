# Workspace R4 第8项｜8a.3b 敏感投影契约修复 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`c737a54aca9bb0a21241a681d32d73ed278f0b83`
- 质量结论：`PASS`
- 安全结论：`PASS`

## 结论

父契约与 focused 测试已统一复用全局 `403` exact body；`SENSITIVE_PROJECTION_REJECTED` 仅保留为内部日志 `fail_code`，不会进入公开响应。原质量阻塞已关闭。

唯一缺口：无。本修复 Gate 通过；需重派父项 8a.3b 复核，完成前 `8a.3c` 继续冻结。

## 独立核对

- denylist 任一字段、嵌套字段或敏感文本伪装命中时整体 `403`。
- 对外固定体：`{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}`。
- 响应仅含 `error_code`、`message`；不得包含内部 fail_code、命中字段、来源 ID、状态或调试信息。
- `SENSITIVE_PROJECTION_REJECTED` 仅为七字段日志中的内部 `fail_code`。
- 分来源真实 allowlist、递归 denylist、禁止 partial/空对象/`summary`/`next_step_hint`、现场哈希和裸文本规则未改变。

## 新鲜证据

提交仅修改父契约与 focused 测试两文件，未修改运行时、API、schema 或安全边界。

```text
.venv/bin/python -m pytest -q \
  backend/tests/test_ai_secretary_sensitive_projection_contract.py \
  backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`10 passed in 0.08s`。敏感投影测试现直接断言全局 `403` body，并断言内部 fail_code 不得进入公开响应。

`git diff --check c737a54a^ c737a54a`：通过。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Review 不替代父项 8a.3b 的重新复核。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
