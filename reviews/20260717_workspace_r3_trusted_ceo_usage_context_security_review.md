# Workspace R3 可信 CEO UsageContext 安全 Review

Issue：`issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md`  
结论：`BLOCKED_L2`

## 唯一阻塞

现有可信链已能提供 `subject_id`、tenant、company、role 和 membership 状态，但没有已确认的服务端 `ceo_id` 事实源或 `subject/membership → CEO` 映射。当前 `CeoContext.parse_ceo_from_request()` 仍直接读取客户端 `X-Ceo-Id`，不能作为 UsageEvent 的可信身份。

因此不能安全地把 Provider 已成功的结果写入带 CEO 审计字段的 UsageEvent，也不能允许新的模型出网。

## 必须固化的唯一契约

`ceo_id` 只能由服务端依据已验证 Gateway subject、活动 membership、tenant/company 和当前 project 的既有 CEO 归属记录推导；若既有 CEO 记录缺失、撤销、过期、角色不匹配或与 tenant/company/project 不一致，模型出网前拒绝，UsageEvent 不得写入不完整审计。

Gateway 必须剥离客户端 `X-Ceo-Id`，不得由客户端、Admin token、默认 CEO、固定字符串或仅凭 `X-Tenant-Id` 推导。UsageEvent 必须绑定当前 TenantContext、company、project、workflow/run、active membership 和服务端派生 `ceo_id`。

## 验收与回滚

Focused 验收必须覆盖：合法映射成功；缺失/撤销/过期/角色不匹配拒绝；跨租户和跨 project 拒绝；伪造 `X-Ceo-Id` 无效；日志不含 token、Authorization、Cookie、完整 subject、API key 或模型原文；UsageEvent 字段完整且脱敏。不得调用真实模型验证实现阶段。

回滚不得恢复客户端 CEO Header、默认 CEO 或跳过 UsageEvent；缺少映射时保持 `BLOCKED_L2`。

Next Seat：产品规划席。  
Handoff：sent to 产品规划席。
