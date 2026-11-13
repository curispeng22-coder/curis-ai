# R4 Secretary 8b.1 响应契约安全 Review

Issue：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b1_response_contract_alignment_decision.md`  
结论：`PASS`（安全边界意见，待总控裁决）

## 总控裁决后的唯一规则

本轮不新增 `429`、`409`、`423` 或 `5xx` 的 Secretary 对外差异化响应体。8a 的 exact 两字段响应契约继续作为唯一外部规则：

- 缺身份/上下文：既定 `401 secretary_access_required`；
- 参数非法：既定 `400 secretary_request_invalid`；
- 越权、跨租户或作用域错配：既定 `403 secretary_source_forbidden`；
- 对象不可用、状态不可读、来源快照/状态冲突或非终态不可安全读取：既定 `404 secretary_source_unavailable`。

响应只含 `error_code`、`message`，不返回 `ok`、细分类 `fail_code`、配额、锁定状态、重试提示、Provider 状态或对象存在性细节。

## 内部失败分类

`409`、`423` 以及 `STALE_CONTEXT`、`CONFLICT` 等细分类只能作为内部 `fail_code`，写入既定最小七字段日志，并对外映射既定 404。`429`、`5xx` 及配额/速率/外部依赖处理不属于本轮只读范围，删除其对外与实现路径；不得借此新增限流或外部依赖处理。

失败立即终止，不返回 partial、不跨租户重算、不自动重试、不切换路由。日志不得含 prompt、payload、raw output、token、credential、Cookie、JWT、Authorization、principal 或其派生字段。

## 裁决状态

总控已 `APPROVE_INTERNAL_ONLY_MAPPING`：否决 8b.1 草案的 `ok/fail_code/error` 对外体；8b.1 已与 8a exact 响应契约对齐，可解除质量复核冻结。8c 与第9项仍按总控调度。

Next Seat：总控决策席 + 产品规划席。  
Handoff：sent to 总控决策席 and 产品规划席。
