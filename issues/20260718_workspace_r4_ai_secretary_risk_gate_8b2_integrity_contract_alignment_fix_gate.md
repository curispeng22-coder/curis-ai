# Workspace R4 第8项｜8b.2｜来源完整性真实字段与响应契约修复 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md`
- Owner：系统交付席（真实关联定义）+ 安全边界席（完整性边界）→ 质量运行席（复核）

## 目标

使 8b.2 只使用 8a.3a 已通过的分源真实关联，并复用 8a/8b.1 的唯一对外响应契约。

## 必须对齐

- 不得要求所有来源都有 `source_run_id`、`source_step_id`、`source_result_id`；StepResult 只允许经 tenant + `workflow_steps` 关联 RD Run，内容来源只按本源字段核验。
- `CONFLICT`、`STALE_CONTEXT` 仅可作为内部 `fail_code`，对外统一映射既定 `404` 固定体；不得对外 `409`、`423`。
- 已存在对象但归属/关联值错配为 `403`；schema 无法证明所需关系也为 `403`。必经对象/中间行缺失或不可见为 `404`。
- `summary`、`next_step_hint` 仅可来自 8a.3b 已批准的预定义非敏感模板；不能证明时省略或整体拒绝，不得将文本快照当作可验证来源。

## 禁止

- 不新增哈希、schema、接口、模型调用、前端或历史数据回填。
- 不允许 fallback、历史版本替代、同名 ID/拼接/默认推断或裸文本映射。

## 验收

- 系统交付席固化分源真实关联与 fail-closed 映射；安全边界席复核文本与篡改边界。
- 质量复核 PASS 后才重派 8b.2；8b.3 继续冻结。

## 实施证据

- 已在 `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md` 用四类真实来源替换通用 `source_*` 链，并对齐 8b.1 的 403/404 固定体。
- 安全裁定：`reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_security_review.md`（`PASS`）；已存在错配 `403`，缺行/不可证 `404`，篡改/fallback/历史替代禁止。
- focused：`backend/tests/test_ai_secretary_integrity_contract.py`。
- 命令：`.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_integrity_contract.py`。
- 结果：`6 passed`。
- 未修改 schema、API、运行时、前端或历史数据；未新增哈希/fallback/推断关系；`8b.3` 保持冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_gate.md`
Objective:
对齐8b.2来源完整性与既有真实字段、全局响应契约。
Special Constraints:
仅契约；不新增字段/API/运行时。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
