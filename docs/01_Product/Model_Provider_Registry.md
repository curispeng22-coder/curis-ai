# Curis Model Provider Registry

Status: Review  
Updated: 2026-08-14  
Source: AI 能力接入专项、New API 定位补充、当前 Gateway/Model/Credential/Usage 代码、各厂商官方 API 文档。

## 1. Registry 边界

Provider Registry 是“供应定义与发现规则”，不是第二个模型数据库或第二个 Runtime。

```text
Provider Definition
→ discovery/health
→ existing tenant_private_capabilities or official_models
→ existing employee_capability_bindings
→ existing execute_model_gateway
```

Registry 不永久内置业务模型 ID。动态 API 可用时从厂商发现；官方没有稳定模型列表 API 时，由用户选择/输入并以 Curis 推荐目录作为 Review 数据维护，不把文档枚举写死进业务路由。

## 2. 三类当前入口与一类未来来源

| Channel | 当前入口 | Credential source | 定位 |
| --- | --- | --- | --- |
| `official_byok` | OpenAI、Anthropic、Gemini、DeepSeek、通义、豆包、智谱、MiniMax、Kimi、Mistral、xAI、Groq、硅基流动 | USER | Local Desktop 普通用户默认 |
| `advanced_gateway` | New API、OpenAI Compatible、OpenRouter、企业网关 | USER | 高级/聚合网关 |
| `local_model` | Ollama、LM Studio、本地 compatible endpoint | USER/none | 本地模型 |
| future platform | Curis Admin → New API/managed gateway | PLATFORM | 未来云商业化；本轮不实现 |

Employee/Workspace 只消费 Model Capability，不读取 channel 或 credential owner 做业务判断。

## 3. Provider Definition

| Provider | Base URL | Auth | Discovery | Invoke protocol | 当前验证 |
| --- | --- | --- | --- | --- | --- |
| OpenAI | `https://api.openai.com` | Bearer | dynamic `/v1/models` | OpenAI Chat | 协议测试；无真实 Key |
| Anthropic | `https://api.anthropic.com` | `x-api-key` | dynamic `/v1/models` | Messages | 适配器回归；无真实 Key |
| Gemini | `https://generativelanguage.googleapis.com` | `x-goog-api-key` | dynamic `/v1beta/models` | generateContent | 适配器回归；无真实 Key |
| DeepSeek | `https://api.deepseek.com` | Bearer | dynamic `/models` | OpenAI Chat | 既有 compatible 能力；无本轮真实 Key |
| Alibaba/Qwen | `https://dashscope.aliyuncs.com/compatible-mode` | Bearer | curated/manual | OpenAI Chat | 未提供 Key，BLOCKED |
| Volcengine/Doubao | `https://ark.cn-beijing.volces.com/api/v3` | Bearer | curated/manual | OpenAI Chat custom path | 未提供 Key，BLOCKED |
| Zhipu | `https://open.bigmodel.cn/api/paas/v4` | Bearer | curated/manual | OpenAI Chat custom path | 未提供 Key，BLOCKED |
| MiniMax | `https://api.minimaxi.com` | Bearer | dynamic `/v1/models` | OpenAI Chat | 协议已定义；无真实 Key |
| Moonshot/Kimi | `https://api.moonshot.cn` | Bearer | dynamic `/v1/models` | OpenAI Chat | 协议已定义；官方端点需下一轮凭据验证 |
| Mistral AI | `https://api.mistral.ai` | Bearer | dynamic `/v1/models` | OpenAI Chat | 官方协议已定义；无真实 Key |
| xAI | `https://api.x.ai` | Bearer | dynamic `/v1/models` | OpenAI Chat | 官方协议已定义；无真实 Key |
| GroqCloud | `https://api.groq.com/openai` | Bearer | dynamic `/v1/models` | OpenAI Chat | 官方协议已定义；无真实 Key |
| SiliconFlow/硅基流动 | `https://api.siliconflow.cn` | Bearer | dynamic `/v1/models` | OpenAI Chat | 官方协议已定义；无真实 Key |
| OpenRouter | `https://openrouter.ai/api` | Bearer | dynamic `/v1/models` | OpenAI Chat | 高级聚合入口；无真实 Key |
| New API | user base URL | Bearer | dynamic `/v1/models` | OpenAI Chat | 复用既有 Gateway Catalog/Router |
| OpenAI Compatible | user base URL | Bearer | dynamic `/v1/models` | OpenAI Chat | 既有 Runtime 回归通过 |
| Ollama | `http://127.0.0.1:11434` | none | dynamic `/api/tags` | OpenAI Chat compatible | 真实发现与调用 PASS |
| LM Studio | `http://127.0.0.1:1234` | optional Bearer | dynamic `/api/v1/models` | OpenAI Chat compatible | 本机未安装/运行 |

以上 18 个 Runtime Definition 只复用现有三类协议和 Gateway，不为品牌创建业务分支。[Mistral](https://docs.mistral.ai/api/endpoint/models)、[xAI](https://docs.x.ai/developers/rest-api-reference/inference/models)、[Groq](https://console.groq.com/docs/models)、[SiliconFlow](https://docs.siliconflow.cn/en/api-reference/models/get-model-list) 与 [OpenRouter](https://openrouter.ai/docs/guides/overview/models) 的官方模型发现接口已核对；真实授权、健康、调用仍须用户凭据。

### 已研究、暂不进入 Runtime Definition

| Provider | Connection shape | 状态 | 不直接加入原因 | 下一动作 |
| --- | --- | --- | --- | --- |
| [百度千帆](https://cloud.baidu.com/doc/qianfan-api/s/Dmba8k71y) | 平台 endpoint/credential，模型目录 | RESEARCHED | 平台鉴权与当前产品入口需版本化确认 | 有用户需求与凭据时按官方 API 验证 |
| [腾讯混元/TokenHub](https://cloud.tencent.com/document/product/1729) | 平台 endpoint/credential，OpenAI-compatible 迁移路径 | RESEARCHED | 产品/平台迁移中，不应写死旧端点 | 锁定用户实际平台版本后接入 |
| [AWS Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListFoundationModels.html) | AWS IAM + region + model access/deployment | RESEARCHED | 不是简单 API Key Provider；需云账号、IAM 和区域契约 | 企业场景独立 Issue |
| [Microsoft Foundry/Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview) | Azure identity/key + resource/deployment | RESEARCHED | 需要 resource/deployment/identity，不应塞进普通 BYOK 表单 | 企业场景独立 Issue |

这些企业平台未来仍输出统一 Model Capability；不会让 Employee/Workspace 读取 AWS、Azure、百度或腾讯品牌分支。

## 4. 设置中心数据契约

本节记录当前 Runtime API；面向产品/前端的稳定卡片、状态与动作契约统一以
`docs/01_Product/AI_Capability_UI_Contract.md` 为准。两者不是第二套 Registry：UI Contract
只把当前 Registry、连接、Credential、Health 与模型发现事实投影成用户状态。

### Provider List

`GET /api/workspace/ai-capabilities/providers`

返回 provider_id、name、channel、base_url、auth、discovery_mode/path、protocol、documentation、是否允许 custom base URL、configured、credential source 枚举。

### Connect / Discover / Save

`POST /api/workspace/ai-capabilities/providers/{provider_id}/connect`

输入：

- `credential_ref`：只接受现有 Credential Vault 的 opaque ref。
- `base_url`：只对 New API/OpenAI-compatible/local provider 开放。
- `model_ids`：仅 curated provider 由用户/推荐目录提交。
- `save`：为 true 时写入现有 `tenant_private_capabilities(type=model)`。

输出：health、availability、discovery_mode、model list、Capability Profile、save 状态。任何 secret 都不返回。

### First Arrival

`GET /api/workspace/ai-capabilities/bootstrap`

Onboarding 只消费统一扫描结果与 recommended provider id；不包含 Provider 配置逻辑。

## 5. Model Capability Profile

```json
{
  "features": {
    "chat": "supported",
    "reasoning": "unknown",
    "coding": "unknown",
    "vision": "unknown",
    "image": "unknown",
    "audio": "unknown",
    "embedding": "unknown",
    "tool_calling": "unknown",
    "structured_output": "unknown",
    "context": null,
    "location": "cloud"
  },
  "evidence": "provider_api | conservative_curis_default",
  "cost": {"status": "unknown", "source": "official-doc-url"},
  "availability": "available"
}
```

规则：

- 只有厂商 API 返回的字段才能升级为 `supported`。
- 模型列表 API 未返回的能力保持 `unknown`，不按品牌名猜测。
- Cost 不写死在业务代码；未接入版本化价格源时保持 `unknown`。
- “发现到模型”只证明 catalog visibility，不证明授权、health、binding 或一次真实结果。

## 6. Credential 与供应来源

当前 private model metadata 保存 `credential_ref` 和 `credential_source=USER`。未来 PLATFORM credential 进入 Gateway/Admin 层后仍生成同样的 Model Capability；Employee binding 不迁移、不改 schema。

当前 Local backend 只在内存保存 secret，因此 UI 上必须显示“本次进程可用/重启需重新授权”，不能展示为持久化 Authorized。原生 Keychain 或配置好的 Vault/KMS 是进入 Desktop 正式可用前的必要门禁。

## 7. URL 与安全边界

- 官方 Provider 使用固定 HTTPS Base URL，不允许普通连接请求覆盖。
- custom Base URL 只对高级/本地定义开放。
- URL 禁止内嵌 username/password。
- 明文 HTTP 当前只允许 loopback；企业内部 HTTP gateway 留给未来受控 Admin policy。
- Gemini Key 使用 header，不进入 URL/query/log。
- provider HTTP 错误只返回状态，不回显 response body、request headers 或 secret。

## 8. 产品占位与当前状态

- 当前 18 个 Runtime Provider Definition 继续复用，不为页面完整度新增第二套执行实现。
- 产品层另外保留 `enterprise_gateway`、`local_compatible` 与
  `curis_platform_managed` 位置；前两者复用现有 OpenAI-compatible contract，后者为
  `COMING_LATER`，都不能伪装成当前已连接 Provider。
- 13 个官方 BYOK 在无真实 Key 时统一保持 `NOT_CONNECTED`，Authorized/Healthy/ModelList
  不得由定义或模拟协议回归推断。
- New API / OpenAI Compatible 是高级聚合入口，不是 Local Desktop 普通用户默认路径。
- Ollama 当前为 `AVAILABLE`（本机真实发现 2 个模型并完成垂直调用）；LM Studio 当前为
  `NOT_INSTALLED`。这些是 2026-08-14 证据快照，前端运行时必须重新扫描。
- USER credential 在安全持久化完成前标记 `SESSION_ONLY`；未来 PLATFORM credential 不进入
  当前 Local Desktop 实现范围。
