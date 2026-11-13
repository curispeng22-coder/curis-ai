# Curis AI 能力接入现状审计

Status: Review  
Updated: 2026-08-15  
Source: Product Blueprint 5.1、ADR-0046、Master Map v2.0、Page Map v1.0、Talent Market Integration Contract、AI 能力接入专项指令、当前主目录代码与本机实测。

## 1. 审计结论

Curis 已有模型目录、New API/多网关、OpenAI-compatible 调用、Skill/Expert 生产线、MCP/Connector adapter、私有能力、Credential Vault、员工绑定、Task/Workspace Runtime、Usage/Cost 与 Artifact 回收。缺口不是“没有模型系统”，而是四类生态没有形成统一 Registry、产品状态与真实门禁；Agent 仍多为历史适配器或发现契约，缺少统一 session/result contract。

因此本专项复用现有链，不建立第二套 Provider、Employee 或 Runtime：

```text
Provider Definition / Agent Adapter
→ existing tenant_private_capabilities / official_models / model_gateways
→ existing employee_capability_bindings
→ existing execute_model_gateway / Task Runtime
→ existing executions / usage / artifacts
```

本结论不改变 Blueprint 5.1 的公开产品定义。Local Agent Computer Access 的批准边界已由 ADR-0046 单独冻结，不授权 UI 或 Runtime。

## 2. 当前实现清单

| 对象 | 当前实现 | 可复用结论 | 当前缺口 |
| --- | --- | --- | --- |
| Model | `official_models`、`tenant_private_capabilities(type=model)`、`ModelCatalog` | 继续作为官方/租户模型能力存储 | 历史官方目录与租户私有投影字段不完全一致 |
| Provider/Gateway | `model_gateways`、`GatewayCatalog`、`ModelGatewayAdapter` | New API 和 OpenAI-compatible 调用直接复用 | 原先普通用户需手工填技术参数；无统一厂商定义/发现接口 |
| New API | Admin Gateway/Model API、gateway resolver、usage 与受控验证 | 保留为高级聚合网关及未来 PLATFORM Gateway | 当前不应成为 Local Desktop 普通用户默认入口 |
| Agent | `dev_agent.py`、`agent_conversion/*`、Coze/OpenClaw discovery、`CodexCliAdapter` | 人才发现契约、Coze opaque ref、公开来源审计与现有 Adapter 可复用 | Codex requested/effective 混淆、resume 权限未重新验证；其他 Agent 无真实 mapping |
| Executor | `ModelGatewayAdapter`、generic CLI/HTTP/MCP adapters、ToolExecutor | 复用现有 Task 工具执行与审计链 | Agent session/progress/artifact 字段原先未透传 |
| Capability | `CapabilityCatalog`、`capability_registry.py`、tenant private capability | 继续作为 Employee/Workspace 消费面 | 能力证据不足时曾存在 `unknown` 与 `available` 混淆风险 |
| Credential | `CredentialVaultService`、opaque `credential_ref`、metadata+digest | 禁止普通表保存明文的边界可复用 | Local backend 只在进程内存，重启后 secret 不可恢复；Vault/KMS 未配置 |
| Binding | `employee_capability_bindings` | 当前 Task/Workspace 的权威绑定链 | 另有 `employee_capabilities` 被 CapabilityResolver 使用，形成重复绑定实现 |
| Runtime | Task/Orchestrator/ToolExecutor、RuntimeCapabilityContext、usage、Artifact | 继续作为模型与 Agent 的业务执行链 | Runtime 仍含大量历史 Project/Task-first 结构；不得称 Blueprint 目标已交付 |

## 3. New API 专项审计与定位

### 已有能力

- `GatewayCatalog` 管理 gateway metadata、状态和 credential reference。
- `ModelCatalog` 管理官方模型到 gateway 的引用。
- `ModelGatewayAdapter.with_model_metadata()` 能按 gateway 切换 Base URL 和 credential reference。
- `execute_model_gateway()` 负责 Employee/Project/Task/Binding 归因、usage/cost ledger、trace 与失败审计。
- Admin 面有 `/api/platform/gateways`、`/api/platform/models`、usage meter 和受控网关验证。
- New API/OpenAI-compatible 供应链已经存在，不能再造一套。

### 当前定位

| 阶段 | Credential | Supply | 用户路径 |
| --- | --- | --- | --- |
| Local Desktop 当前 | USER | 官方 Provider BYOK | 选择 Provider → 输入自己的 Key → 测试 → 发现模型 |
| Local Desktop 高级 | USER | New API / OpenAI-compatible / enterprise gateway | 高级配置 Base URL + Key → 发现模型 |
| Local Desktop 本地 | USER/none | Ollama / LM Studio / local compatible | 扫描本地服务 → 发现模型 |
| 未来 Curis Cloud | PLATFORM | Admin → New API / managed gateway | 普通用户只选模型，不接触 Key/Base URL |

上层 Employee、Workspace、Capability 与 Binding 不因 supply source 改变。本轮只在 metadata 中保留 `credential_source=USER` 和未来 `PLATFORM` 枚举，不实现云端商业化计费或托管凭据。

## 4. 当前真实调用链

### Employee 如何绑定

`PUT /api/workspace/employees/{employee_id}/capabilities` 写入 `employee_capability_bindings`。绑定包含 source、type、capability_id、priority、enabled。Task 创建时校验绑定并将选择写入 requested capability 字段。

### Workspace 如何调用

Task/Workspace → Orchestrator → ToolExecutor → `execute_model_gateway()`。它读取 `RuntimeCapabilityContext`，验证 tenant/company/project/department/employee/binding 归因，再创建具体 Model/Agent adapter。成功后写 usage、runtime trace、execution；Task 完成时 `ResultStore.transition()` 自动把 output 写为 Artifact。

### Credential 如何保存

- 普通数据库只保存 credential metadata、opaque ref 与 digest。
- Local 开发 secret 当前只保存在 `LocalDevCredentialBackend` 进程内存。
- `vault://` / `kms://` 形状已预留但 backend 未配置。
- `env:VAR` 是历史兼容路径。
- 当前符合“不把明文写入普通数据库/日志/Prompt/Artifact”，但不满足 Desktop 重启后的安全持久化；这是 P0 安全缺口。

## 5. 重复与旧架构

1. `employee_capability_bindings` 是当前 Task/Workspace 使用的绑定；`employee_capabilities` 是 CapabilityResolver 的另一套表。后者不应扩展，应后续迁移到权威绑定链。
2. `dev_agent.py` 的 `OpenAICodexAdapter` 是 Chat Completions 模型调用，不是 Codex Agent；`ClaudeCodeAdapter` 是 Anthropic Messages 模型调用，不是 Claude Code CLI。
3. 旧 `CodexAgentAdapter` 使用交互 PTY、硬编码本机路径/模型并允许直接修改工作树；本专项不复用该执行方式。
4. `CanonicalAgentSpec`、Coze Adapter、OpenClaw Skill discovery 属于人才发现/安全清单，不是外部 Agent session Runtime。
5. generic CLI/HTTP/MCP adapters 是单次能力调用，不满足 Agent 的 session/resume/progress/artifact contract。

## 6. 本轮新增但不新造系统

- `/api/workspace/ai-capabilities/providers`：设置中心可消费的 Provider Definition + configured 状态。
- `/api/workspace/ai-capabilities/providers/{id}/connect`：使用 `credential_ref` 测试、发现并写入既有 tenant-private model capability。
- `/api/workspace/ai-capabilities/local`、`/bootstrap`：本地 Agent/Model 扫描与首次引导数据。
- 本地 Agent 扫描改为内部 Registry 驱动，只返回当前设备实际 detected 的条目；GUI-only 检测明确返回 programmatic import unsupported。
- 既有 `ModelGatewayAdapter` 增加 Anthropic Messages、Gemini generateContent 和厂商 chat path；默认仍是原 OpenAI-compatible 路径。
- Codex 使用官方 `codex exec --json` 与 `codex exec resume`，结果进入既有 Task/Artifact 链。

## 7. 当前状态

- OpenAI Compatible：PASS（既有链 + 回归）。
- New API：PASS（作为现有高级/Admin gateway 保留；本轮未重复实现）。
- 本地模型发现：PASS（本机 Ollama 发现 2 个模型）。
- Employee → Ollama → Runtime → Artifact：PASS（隔离数据库真实执行）。
- Codex detected/authorized/healthy：PASS（本机 `codex-cli 0.144.6`）。
- Codex new session/resume：PASS（真实 CLI JSONL）。
- Employee → Codex → Runtime → Artifact：PASS（read-only 临时项目真实执行）。
- Codex Computer Access evidence：PARTIAL（新 session 只有 requested sandbox；结果为 Adapter 回显；resume 未重新声明/验证；Full 禁止）。
- 云 Provider BYOK：`NOT_CONNECTED / UNVERIFIED`（协议与发现已实现/测试；本机无云 Key，不能声明真实授权或调用）。
- 其他本地 Agent：兼容性已研究；未在当前设备 detected 的产品不进入普通用户列表，也不产生 Runtime capability。
- 远程 Agent：使用通用 Import/Connection 入口；无真实 published object 与授权时不生成可用卡片。
- Skill/Expert：55 个 active SkillTemplate 与现有专家模板链可复用；外部 27 条扫描资源新增 Curis-ready 为 0。
- MCP/Connector：stdio 最小 adapter、5 个 manifest 与 2 个现有 Connector 可复用；本轮无真实 MCP 垂直 Evidence。
- Desktop credential persistence：BLOCKED（当前 local secret backend 仅内存）。

## 8. 产品状态契约收口

本轮不继续扩 Agent 或大规模 Runtime，而是把现有事实投影为前端可消费的统一产品状态：

`AVAILABLE`、`NOT_CONNECTED`、`NOT_INSTALLED`、`AUTH_REQUIRED`、
`CONFIG_REQUIRED`、`HEALTH_UNKNOWN`、`UNAVAILABLE`、`COMING_LATER`、
`BLOCKED`、`UNKNOWN`。

映射仍以 Detected / Configured / Authorized / Healthy / Available 五个事实轴为依据；
`Detected`、Provider Definition、Candidate、Adapter Contract 或协议测试都不能单独升级为
`AVAILABLE`。完整字段、动作权限、Provider/Agent 当前投影与渐进式暴露规则见
`docs/01_Product/AI_Capability_UI_Contract.md`。

当前产品收口不改变运行证据：Ollama 与 Codex 保持已有真实证据；Cloud BYOK 保持
`NOT_CONNECTED / UNVERIFIED`；Skill/Expert、MCP/Connector 与 Agent 的目录/研究证据分别使用
`LIVE / READY / DISCOVERABLE / RESEARCHED / BLOCKED / UNKNOWN`，不得折叠成 Available。Secure Desktop Credential Persistence 继续作为独立 P0，但不阻塞 Ecosystem Contract Review。

## 9. Computer Access Authority

- 用户侧冻结“请求批准 / 自动处理（推荐默认）/ 完全访问”。
- 内部复用现有 Execution Binding、Agent Adapter、Session/Result/Audit 链，不新增权限系统。
- `Detected != Configurable != Granted != Available`；`Requested != Configured != Effective`。
- 权威定义见 ADR-0046、`Agent_Adapter_Contract.md` §3 与 `AI_Capability_UI_Contract.md` §5.6。
- Runtime 只规划：`docs/04_Development/AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md`。
- Full 继续禁止，直到真实 Adapter 同时具有 apply + verify。

## 10. 官方协议来源

- [OpenAI Models API](https://platform.openai.com/docs/api-reference/models/list)
- [Anthropic List Models](https://platform.claude.com/docs/en/api/models/list)
- [Gemini Models API](https://ai.google.dev/api/models)
- [DeepSeek List Models](https://api-docs.deepseek.com/api/list-models)
- [MiniMax List Models](https://platform.minimaxi.com/docs/api-reference/models/openai/list-models)
- [Alibaba Model Studio](https://help.aliyun.com/en/model-studio/what-is-model-studio)
- [Volcengine Ark model list](https://www.volcengine.com/docs/82379/1874970)
- [Zhipu Chat Completions](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)
- [Ollama List Models](https://docs.ollama.com/api/tags)
- [LM Studio REST API](https://lmstudio.ai/docs/developer/rest)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Codex App Server](https://learn.chatgpt.com/docs/app-server)
