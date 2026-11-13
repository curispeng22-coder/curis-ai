# Workspace R3 真实模型执行安全 Review

Issue：`issues/20260717_workspace_r3_real_model_execution_gate.md`
结论：`PASS`
审批：总负责人已批准，2026-07-17

## 批准范围

仅允许以下单一路径：

- Provider：OpenAI API
- Model：`gpt-5.4-mini-2026-03-17`
- Gateway：现有 `ModelGatewayAdapter`，`gateway_id=newapi`
- 出口：`https://api.openai.com:443/v1/chat/completions`
- 凭据：部署密钥设施注入 `CURIS_MODEL_GATEWAY_API_KEY`

客户端不得覆盖 Provider、Model、Gateway、出口或凭据引用。仅批准一个测试 tenant、project、`official.workflow.software_rnd_sop` 和一个 active capability binding。

## 安全限制

- 凭据缺失、价格缺失、配置不完整、绑定不一致或审计字段缺失：调用前拒绝。
- 不写入仓库、Issue、Review、日志、数据库或消息；不得读取或回传密钥值。
- 租户、成员、Company、Project、Workflow、Capability scope 全部服务端校验；禁止默认租户和跨租户执行记录复用。
- 输入上限 8,192、输出上限 2,048、总 Token 上限 10,240；单 Workflow/R3 各最多一次调用。
- R3 成本硬上限 USD 0.10；价格采用已批准的 2026-07-17 官方价格，计算异常即拒绝。
- 超时 60 秒、重试 0 次、429 不重试、无 Fallback。

## 日志、审计与撤销

仅保留脱敏审计元数据：request、主体关联摘要、tenant、company、project、workflow、capability、gateway、精确 model、Token、价格版本、成本、状态、HTTP 状态和延迟。禁止保存 prompt、原始响应、Authorization、API key、Cookie 或敏感 claims。

撤销 binding、Model、Gateway 或凭据后立即拒绝后续调用。回滚只能回到仍满足上述约束的版本，不得恢复 mock、默认模型、Header-only 授权或无约束出站。

## 安全验收

必须验证：批准路径真实成功；无身份/无凭据/无成员/非批准 tenant、project、workflow、model 均拒绝；跨租户资源返回 404；超 Token/成本在出网前拒绝；429 不重试；日志无秘密；撤销后拒绝；真实 Token、模型和成本审计可追溯。

## 交接

本 Review 仅完成安全契约固化，不代表实现或真实模型执行已通过。

Next Seat：系统交付席。
Handoff：sent to 系统交付席；并回产品规划席。
