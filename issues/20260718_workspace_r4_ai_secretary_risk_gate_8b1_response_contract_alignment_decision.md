# Workspace R4 第8项｜8b.1｜风险失败响应契约对齐裁决

- 日期：2026-07-18
- 状态：PENDING_GATE_DECISION
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`（8a PASS）
- Owner：总控决策席（范围裁决）+ 安全边界席（多租户/外部失败边界意见）

## 冲突

8a 已冻结 `401/400/403/404` 的单码优先级与 exact 两字段对外响应。8b.1 草案新增 `429/409/423/5xx`，并使用 `ok/fail_code/error` 的不同响应体；两套契约不能同时作为同一 Secretary 对外接口规则。

## 需要裁决

1. 8b.1 的 `429/409/423/5xx` 是否属于本轮获准的对外 Secretary 契约，或只可作为内部风险/日志分类。
2. 若允许对外新增状态，是否保留 8a 的 exact 响应体原则并为新增状态给出单一固定体；若不允许，8b.1 必须映射回 8a 已批准的对外状态，细分类仅保留内部 `fail_code`。

## 边界

- 本项只做裁决，不改实现、不启动服务、不新增 API、模型调用、凭据或外部依赖。
- 裁决前不得派发 8b.1 质量复核；8c 与第9项继续冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b1_response_contract_alignment_decision.md`
Objective:
裁决8b风险码与8a全局响应契约的冲突。
Special Constraints:
仅范围/安全裁决；不实施。
Next Seat:
总控决策席 + 安全边界席

Handoff: sent to 总控决策席 and 安全边界席
