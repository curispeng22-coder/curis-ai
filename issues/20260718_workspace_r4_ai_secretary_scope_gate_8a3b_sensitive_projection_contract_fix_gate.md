# Workspace R4 第8项｜8a.3b｜敏感输出真实字段与拒绝契约修复 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（系统 allowlist + 安全拒绝契约已固化；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`
- Owner：系统交付席（字段契约）+ 安全边界席（敏感输出裁定）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

让 8a.3b 的输出 allowlist 与已通过的 8a.3a 分源真实字段一致，并明确命中敏感字段时的唯一 fail-closed 行为。

## 必须对齐

- 不得允许 `source_run_id`、`source_step_id`、`source_result_hash` 等未在四类来源通用存在的字段。
- 只允许四类来源各自已经验证的 ID、`tenant_id`、`created_at` 及明确允许的最小投影字段。
- 禁止现场哈希结果、报告、摘要或成果文本，禁止用裸文本替代来源引用。

## 安全裁定点

- 命中 denylist 时是整体拒绝还是仅剔除字段，必须给出唯一行为、固定 fail_code 和日志边界；不得保留“剔除后继续返回”的模糊路径。
- `summary`、`next_step_hint` 的允许条件必须可验证且不包含原始 prompt、工具 payload、令牌或凭据内容。
- 命中 denylist 的对外响应必须复用既定 `403` 固定体：`{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}`；`SENSITIVE_PROJECTION_REJECTED` 仅可作为既定白名单中的内部 `fail_code`，不得新增对外错误码或字段。

## 禁止

- 不新增 schema、接口、模型调用、运行时或前端。
- 不扩大可返回字段，不推断跨状态机关系。

## 验收

- 系统交付席给出分源 exact allowlist；安全边界席给出唯一敏感命中处理与日志规则。
- 质量同时复核真实字段与 denylist 反例；均 PASS 后才重派 8a.3b。

## 系统交付证据

- 已在 `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_field_filter_gate.md` 用分来源真实字段替换通用 `source_*` 假设。
- 安全裁定：`reviews/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_security_review.md`（`PASS`）；denylist 任一命中固定整体 `403`，仅两字段响应，日志仅既定七字段。
- focused：`backend/tests/test_ai_secretary_sensitive_projection_contract.py`。
- 命令：`.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_sensitive_projection_contract.py`。
- 结果：`6 passed`。
- 未修改 schema、API、运行时、前端或历史数据；未现场哈希或输出裸文本；`8a.3c` 保持冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_gate.md`
Objective:
将敏感输出过滤收敛为真实字段和唯一拒绝行为。
Special Constraints:
仅契约；不新增字段/接口/运行时。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
