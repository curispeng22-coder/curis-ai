# R4 Secretary 8a.3b 敏感投影安全 Review

Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3b_sensitive_projection_contract_fix_gate.md`  
结论：`PASS`

## 唯一 fail-closed 行为

响应投影或其嵌套值命中 denylist 时，整体拒绝本次投影。不得剔除敏感字段后继续返回，也不得返回 partial、空对象、summary 或 next_step_hint。

固定失败：HTTP `403`，复用既定响应体 `{"error_code":"secretary_source_forbidden","message":"Source access is not allowed."}`。响应体只含 `error_code`、`message`，不含命中字段名、来源 ID、对象状态或实体存在性。`SENSITIVE_PROJECTION_REJECTED` 仅作为内部 `fail_code`，不得出现在对外响应体。

## 日志边界

仅允许既定最小字段：`timestamp`、`tenant_id`、`project_id`、`run_id`、`task_id`、`fail_code`、`step`。固定 `fail_code=SENSITIVE_PROJECTION_REJECTED`。不得记录 principal 原值或任何 principal 派生字段，也不得记录 denylist 命中值、prompt、payload、token、credential、Cookie、JWT、Authorization、summary 或 next_step_hint 原文。

## summary / next_step_hint

两者不是敏感命中时的补偿字段。仅在未命中 denylist、来源字段已通过 exact allowlist、且内容来自预定义非敏感状态模板时允许返回；不得拼接或回显 prompt、tool payload、token、credential、headers、模型原文或任意用户原文。无法证明模板来源或安全性时，字段省略；若整体投影因此不满足契约，则按上述固定 403 拒绝。

## 验收边界

Focused 验收必须证明：任一 denylist 字段、嵌套 denylist、敏感文本伪装命中均整体 403；失败体完全固定且无实体差异；日志只含白名单字段；成功路径的 summary/next_step_hint 不含敏感内容；不得产生模型调用或出网。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
