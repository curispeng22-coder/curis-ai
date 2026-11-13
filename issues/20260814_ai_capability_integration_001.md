# AI-CAPABILITY-INTEGRATION-001：统一模型供应与 Agent 执行接入

Status: Review  
日期：2026-08-14  
授权：用户 2026-08-14「AI 能力接入专项」及 New API 定位补充。

## 目标

复用现有 `ModelGatewayAdapter`、New API Gateway Catalog、
`tenant_private_capabilities`、Credential Vault、Employee Capability Binding、
Task/Workspace Runtime 与 Artifact 回收链，补齐：

```text
Provider Definition / Local Discovery
→ USER credential_ref / future PLATFORM credential_ref
→ Model Capability
→ Employee Binding
→ existing Curis model router / Agent Adapter
→ existing Task Result / Artifact
```

New API 保持高级聚合网关；Local Desktop 普通用户默认采用官方 Provider BYOK。
本 Issue 不实现未来商业化计费或平台托管凭据。

本轮继续收口为 Model、Skill/Expert、MCP/Connector、External Agent Import 四类生态；只新增统一 Registry、真实状态与最小 discovery guard，不按品牌创建第二套实现。

## 允许修改

- `backend/app/ai_capability_registry.py`
- `backend/app/agent_adapter.py`
- `backend/app/model_gateway.py`：只扩展既有网关适配器的协议/路径，不创建第二个模型 Runtime。
- `backend/app/main.py`：只装配统一设置数据接口，并让既有 tenant-private 分支调用新增协议/Agent Adapter。
- `backend/app/tool_executor.py`、`backend/app/orchestrator.py`、`backend/app/result_store.py`：只透传并记录 Agent session/artifact/permission 结果。
- `backend/tests/test_ai_capability_registry.py`
- `backend/tests/test_agent_adapter.py`
- `backend/tests/test_model_gateway_provider_protocols.py`
- `docs/01_Product/AI_Capability_Current_State_Audit.md`
- `docs/01_Product/Model_Provider_Registry.md`
- `docs/01_Product/Skill_Expert_Registry.md`
- `docs/01_Product/MCP_Connector_Registry.md`
- `docs/01_Product/Agent_Adapter_Compatibility_Registry.md`
- `docs/01_Product/Agent_Adapter_Contract.md`
- `docs/01_Product/AI_Capability_Integration_Report.md`
- `docs/01_Product/AI_Capability_UI_Contract.md`：只定义前端可消费的数据、状态、动作与产品占位，不设计最终 UI。
- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`：仅登记本专项文档与经验证的当前事实。
- `docs/reviews/20260814_ai_capability_integration_001_review.md`

## 禁止修改

- 不修改 Product Blueprint、Master Map、Page Map、UI Blueprint 或一级导航。
- 不新增 Provider/Model 数据库系统、Employee、Runtime 或 Credential 明文字段。
- 不把 New API 作为普通用户默认入口，不删除其 Admin/高级聚合能力。
- 不把动态发现等同于授权、健康、可执行或能力已验证。
- 不把未提供真实凭据的云 Provider 标记为通过。
- 不复制 Codex、Claude Code、Coze、OpenClaw 的私有能力或绕过授权。

## 验收

- Registry 同时表达官方 BYOK、高级 New API/OpenAI-compatible、本地模型和未来 PLATFORM 来源，不写死业务模型 ID。
- 至少一个现有 OpenAI-compatible Provider 真实完成发现、调用、员工绑定和 Artifact 回收。
- 本机 Agent 扫描区分 Detected/Configured/Authorized/Healthy/Available/Unavailable。
- Codex Adapter 真实完成新会话、输出、usage、session id 与 resume；默认 read-only。
- 凭据只通过 `credential_ref` 解析，错误与响应不返回 secret。
- 所有未完成项按 PASS/PARTIAL/BLOCKED 记录。

## Capability Ecosystem 收口（2026-08-14）

本 Issue 后续不按 Provider/Agent 品牌逐个扩实现。本轮只复用已有证据，建立四个核心 Registry、统一 Capability Product State/Ecosystem Readiness、Employee Execution Binding 与动作权限，供前端设计消费。

未接通能力必须保持 `NOT_CONNECTED`、`NOT_INSTALLED`、`AUTH_REQUIRED`、
`CONFIG_REQUIRED`、`COMING_LATER`、`BLOCKED` 或 `UNKNOWN` 等真实状态；不得为页面完整度
伪造授权、健康、模型列表、session 或执行 PASS。本地 Agent 前台只返回实际 detected 条目；GUI-only 不使用 UI automation。完成标志是
`CAPABILITY ECOSYSTEM REVIEW REQUIRED`，不是 AI Capability Integration Phase 1 PASS。
