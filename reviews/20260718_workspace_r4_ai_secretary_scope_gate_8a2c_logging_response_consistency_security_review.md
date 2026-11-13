# R4 Secretary 8a.2c 安全 Review

Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_gate.md`  
结论：`PASS`

## 最小可留存日志

允许保留：`timestamp`、`tenant_id`、`project_id`、`run_id`、`task_id`、`fail_code`、`step`。这些字段只用于定位拒绝事件，不得扩展为对象内容或存在性证明。

最小方案明确为：删除任何 principal 派生落库。日志、UsageEvent 和普通审计记录均不得保存 `principal_hash`、`principal_digest`、`principal_count` 或其他由 principal 派生的字段；不记录 principal 原值，也不记录 JWT、member token、Authorization 或 Cookie。白名单不保留 hash/digest/count 例外。

禁止保留：`prompt`、`artifact_content`、`raw_output`、模型原文、完整 principal/subject、Cookie、token、JWT 明文、member token、堆栈、查询路径、命中字段及任意敏感 claims。

## 固定失败响应

失败响应必须逐字复用 8a.1a 契约，仅含 `error_code`、`message`；不得返回 `detail`、tenant/company/project/run/task/workflow ID、对象数量、状态、来源类型或实体存在性差异。认证、请求、权限、来源不可用分别使用既定 401/400/403/404 固定体，并保持优先级 `401 > 400 > 403 > 404`。

拒绝后不得继续读取关联对象，不返回 partial、空列表或降级结果。成功响应也不得把未授权来源的实体细节带入错误路径。

## 唯一缺口

无。该 Review 仅通过日志与响应安全边界；实现和质量运行证据仍由对应席位独立确认，8a.3a 前需两者均 PASS。质量复核提出的 hash/digest/count 歧义已用“完全不落库”收口。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
