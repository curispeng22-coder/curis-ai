# R4 Secretary 8b.2 完整性契约安全 Review

Issue：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_gate.md`  
结论：`PASS`

## 来源完整性

只接受 8a.3a 已证明的分源真实关联：StepResult 必须通过 tenant + `workflow_steps` 关联 RD Run；内容来源只按其本源字段和 tenant 核验。文本快照、同名 ID、字符串拼接、默认推断、历史版本或 fallback 均不是来源证明。

已存在但 tenant/归属/关联错配，或 schema 关系无法证明：对外 `403 secretary_source_forbidden`；对象或必经中间行缺失、不可见：对外 `404 secretary_source_unavailable`。`CONFLICT`、`STALE_CONTEXT` 只能是内部 fail_code，并统一对外映射 `404 secretary_source_unavailable`，不得出现 `409`、`423`。

## summary / next_step_hint

仅允许来自 8a.3b 已批准的预定义非敏感模板，且模板输入必须来自已验证真实字段。不能证明来源、模板或完整性时，优先省略；若省略后无法满足整体投影契约，则整体拒绝，禁止剔除后继续返回不完整结果。

两字段不得携带 prompt、tool payload、token、credential、Cookie、JWT、Authorization、模型原文、裸文本快照或用户原文；不得用文本替代来源引用。不存在历史替代或自动 fallback。

## 对外响应与验收

对外继续只允许 8a/8b.1 的四种固定体：401/400/403/404，字段仅 `error_code`、`message`。完整性失败不得泄露来源、对象、状态或实体差异。

Focused 验收须覆盖跨分源关联、缺失中间行、错配、篡改文本、未验证模板、fallback/历史替代尝试；确认 Adapter 不调用、不出网，日志不含敏感原文。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
