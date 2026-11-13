# 模型网关 领域研究

> 范围：Curis Admin Platform 后续模型网关治理方向研究。基于 Phase-2 MVP（New API 网关管理 + 审计轨迹 + usage_event 多维查询）和 Phase-3.5 契约评审结论，研究后续模型网关 Adapter 选型、官方与租户私有网关边界、credential_ref 安全前提等议题。本文为纯研究文档，不写代码、不改现有文件。

---

## 现状分析

### Curis 当前模型网关架构

Curis Admin Platform 在 Phase-2（issue 065 / ADR-0028）已完成 New API 网关管理的 MVP，核心架构如下：

**数据层**（`backend/app/database.py`）：

- `model_gateways` 表（GatewayConfig）：`gateway_id`(PK) / `name` / `type`(CHECK `newapi`) / `base_url` / `status`(active|inactive) / `credential_ref`(TEXT, 可空) / `default_model` / `created_at`。**零密钥值列**——`credential_ref` 仅存 `scheme:reference` 不透明引用串。
- `official_models` 表：`model_key`(PK) / `provider_id` / `display_name` / `supported_models`(JSON) / `auth_type`(none|oauth|apikey 形状) / `source`(default `official`) / `gateway_ref`(逻辑引用 `model_gateways.gateway_id`) / `status` / `default_model` / `type`(model|tool|connector) / `name`。
- 种子：默认网关 `gateway_id='newapi'`（env `CURIS_MODEL_GATEWAY_ID`），`base_url` 取 env `CURIS_MODEL_GATEWAY_BASE_URL`，`credential_ref` 留 NULL。

**服务层**（`backend/app/model_catalog.py`）：

- `GatewayCatalog`：网关 CRUD + 启用/停用 + `capability.gateway_created` / `capability.gateway_status_changed` 审计事件。
- `ModelCatalog`：官方模型 CRUD + `gateway_ref` 存在性校验 + `capability.model_created` / `capability.model_status_changed` 审计事件。

**API 层**（`backend/app/main.py`）：

- `/api/platform/gateways`（GET/POST/PUT）：Admin-only 写通道，复用 `_require_platform_admin`。
- `/api/platform/models`（GET/POST/PUT）：Admin-only 写通道。
- `/api/catalog/gateways`（GET）：Workspace 只读投影，**显式排除 `credential_ref` 与 `default_model`**，仅返回 `gateway_id/name/type/base_url/status`。
- `/api/catalog/models`（GET）：Workspace 只读，`source='official' AND status='active' AND type='model'`。
- `/api/platform/usage`（GET）：Admin-only 只读计量，复用 `evolution_event_log.list_usage_events`，支持 7 维查询（tenant_id/capability_type/capability_source/model_gateway_id/model_name/status/since/until）。

**执行层**（`backend/app/model_gateway.py`）：

- `ModelGatewayAdapter`：Workspace 执行层，`urllib` POST `{base_url}/v1/chat/completions`，带 Bearer key。**Admin 绝不 import 此模块**（约束 6/7 硬边界）。

### 已有决策（ADR-0028）

1. **G2 决策(b) 低成本路径**：本期不持久化任何真实凭证；`credential_ref` 仅作外部密钥托管引用标识占位；绝不向 New API 发起任何出站调用。
2. **Admin 边界铁律**：Admin 只定义网关/模型元数据 + 只读计量；绝不 import Workspace 执行层、绝不实现模型调用/网关代理/请求转发。
3. **`credential_ref` 引用格式**：`scheme:reference`，`scheme ∈ {env, kms, vault}`，正则 `^(env|kms|vault):.+$`（`catalog_constants.py`）。空串允许。
4. **`gateway_type` 枚举**：首批仅 `newapi`（`GATEWAY_TYPE=['newapi']`）；预留未来值须经独立评估（R-10）。
5. **catalog 读 ≠ platform 写**：`/api/catalog/*` 对 Workspace 仅只读（网关投影不含 `credential_ref`）；`/api/platform/*` 仅 Admin 写。
6. **fail-closed 规则**：usage 查询 `tenant_id` 缺失 → 拒绝（422），不返回跨租户聚合；创建官方模型时 `gateway_ref` 不存在 → 拒绝（422），不写入悬空引用。

### 当前痛点与未决项

1. **`credential_ref` 仍是占位**：DB 存 `scheme:reference` 串但无真实密钥托管实现，Workspace 执行层 `ModelGatewayAdapter` 目前通过 env 注入密钥（`CURIS_MODEL_GATEWAY_API_KEY`），而非从 `credential_ref` 解析。G2 gate 未解锁。
2. **`gateway_type` 仅 `newapi`**：无法接入 LiteLLM、One API、直连 OpenAI/Anthropic 等其他网关类型。R-10 预留但未评估。
3. **官方网关与租户私有网关边界未显式定义**：当前 `model_gateways` 表无 `source` / `tenant_id` 列，无法区分官方网关与租户私有网关。租户私有模型走 `tenant_private_capabilities` 表（`metadata_json` 内嵌 `credential_ref`），与官方网关治理分离。
4. **网关健康检查缺失**：Admin 不出站，无法主动探测网关可达性；依赖 Workspace 执行时被动发现故障。
5. **网关轮询/负载均衡缺失**：同一 `gateway_ref` 仅指向一个网关，无多网关 failover 能力。

---

## 研究发现

### 行业竞品对比：New API / One API / LiteLLM

基于 2026 年行业调研（awesome-ai-gateway 对比、ai-insight 研报、CSDN/知乎实战文章），三者定位与功能矩阵如下：

#### 定位差异

| 维度 | One API | New API | LiteLLM |
| --- | --- | --- | --- |
| **定位** | 元祖级中转/分发系统 | One API 的活跃继任者 | 功能最全的自托管 AI Gateway |
| **语言** | Go | Go | Python |
| **协议** | MIT | AGPL-3.0 | MIT（核心） |
| **Star（2026）** | ~35k | ~40k（已反超 One API） | ~51k |
| **维护活跃度** | 已放缓 | 最活跃（国内） | 高（周更） |
| **基因** | 协议转换插头 | 运营管理后台 | 开发者 SDK + Proxy |

#### 功能矩阵

| 功能 | One API | New API | LiteLLM |
| --- | --- | --- | --- |
| **OpenAI 兼容接口** | ✅ | ✅ | ✅ |
| **国产模型支持** | ✅ 豆包/DeepSeek/通义 | ✅ + Rerank/Realtime | ✅（走 OpenAI 格式） |
| **多 Provider 路由** | ✅ 渠道 | ✅ 渠道（更完善） | ✅ 100+ 厂商 |
| **虚拟 Key/预算** | ✅ | ✅ | ✅ 更完善（per-key budget） |
| **计费/分发** | ✅ | ✅ 更完善 | ✅ |
| **团队/用户管理** | ✅ | ✅ | ✅ |
| **租户隔离** | ⚠️ 用户级 | ⚠️ 用户级 | ✅ virtual key 级 |
| **日志审计** | ✅ | ✅ | ✅ + 可观测性（OpenTelemetry） |
| **负载均衡** | ✅ 渠道权重 | ✅ 渠道权重 | ✅ 更完善（策略丰富） |
| **Fallback/重试** | ⚠️ 基础 | ✅ | ✅ 策略丰富 |
| **护栏/Guardrails** | ❌ | ❌ | ✅ 内置 |
| **成本跟踪** | ✅ | ✅ | ✅ per-key/per-user |
| **模型别名** | ✅ | ✅ | ✅ |
| **Rerank/Realtime** | ❌ | ✅ | ✅ |
| **协议转换** | OpenAI 格式 | OpenAI 格式 | 多格式（OpenAI/Anthropic/Cohere） |
| **部署方式** | Docker/二进制 | Docker/二进制 | Docker/Python pip |
| **CVE 历史（2026）** | 同源风险 | IDOR/SSRF/SQLi/DoS（已修） | 预鉴权 SQLi + RCE（v1.83.7 已修） |

#### 安全警示

- **New API**（AGPL-3.0）：2026 年有 IDOR 越权（CVE-2026-30886）、SSRF、SQLi/DoS 系列 CVE。商用嵌入须看清 AGPL 协议义务；务必隔离部署、限制出站、别把后台暴露公网。
- **One API**：同源风险，维护放缓，上生产前须自行审计。
- **LiteLLM**：两个严重 CVE（预鉴权 SQLi + CISA 在野利用清单 RCE）均已在 v1.83.7 修复，须锁定最新 stable。
- **转售中转风险**：2026 年研究测出转售"免费 API"中转里 45.8% 指纹测试模型身份不符、输出偏差最高 47%（arXiv 2603.01919）。自建、用自己的 key 才安全。

### Curis Model Gateway Adapter 选型分析

Curis 当前 `ModelGatewayAdapter` 采用 New API 作为唯一网关类型，通过 OpenAI 兼容接口（`/v1/chat/completions`）调用。此选型的合理性分析：

#### New API 作为主网关的优势

1. **OpenAI 兼容**：Curis `ModelGatewayAdapter` 已实现 `urllib` POST `{base_url}/v1/chat/completions`，与 New API 接口天然兼容，零适配成本。
2. **国内生态成熟**：New API 是国内最活跃的中转系统，支持豆包/DeepSeek/通义等国产模型，符合 Curis 数据零出境需求。
3. **运营管理后台**：New API 内置用户/渠道/计费管理，Curis Admin 可复用其后台能力而非自建。
4. **协议转换**：New API 已支持 Rerank/Realtime，为 Curis 未来能力扩展预留空间。

#### New API 作为主网关的风险

1. **AGPL-3.0 协议**：商用嵌入须评估协议义务（网络服务也须开源）。Curis 当前仅通过 HTTP 调用 New API（非代码嵌入），协议风险较低，但须法务确认。
2. **CVE 历史**：须隔离部署、限制出站、及时打补丁。Curis Admin 不出站铁律天然隔离了 Admin 侧风险，但 Workspace 执行层须注意。
3. **单点依赖**：若 New API 故障，Curis 无备选网关。R-10 预留但未评估。

#### LiteLLM 作为备选的必要性

| 场景 | New API 是否够用 | LiteLLM 备选价值 |
| --- | --- | --- |
| 国产模型中转 | ✅ 够用 | 低 |
| 100+ 厂商统一接口 | ⚠️ 走 OpenAI 格式 | ✅ 原生支持 |
| per-key 预算/护栏 | ⚠️ 基础 | ✅ 更完善 |
| 多格式协议转换（Anthropic/Cohere 原生） | ❌ | ✅ |
| 可观测性（OpenTelemetry） | ❌ | ✅ |
| Python 生态集成 | ❌ Go | ✅ Python |

**结论**：当前以 New API 为主网关合理（OpenAI 兼容 + 国内生态 + 运营后台）。建议在 R-10 评估时将 LiteLLM 作为备选网关类型纳入 `GATEWAY_TYPE` 枚举（如 `['newapi', 'litellm']`），用于需要多格式协议转换或高级可观测性的场景。但本期不解锁，保持 `['newapi']` 单值。

### 官方网关与租户私有网关的边界

Curis 当前架构中，官方网关与租户私有模型走两套独立路径：

| 维度 | 官方网关 | 租户私有模型 |
| --- | --- | --- |
| **载体表** | `model_gateways` + `official_models` | `tenant_private_capabilities`（`capability_type='model'`） |
| **管理方** | Admin（`/api/platform/gateways`） | CEO（`/api/workspace/private-models`） |
| **`source`** | `official` | `tenant_private` |
| **`credential_ref`** | 存于 `model_gateways.credential_ref`（占位） | 存于 `tenant_private_capabilities.metadata_json.credential_ref` |
| **Workspace 可见性** | `/api/catalog/gateways` 只读（不含 credential_ref） | `/api/workspace/private-models` 租户内可见 |
| **Admin 可见性** | 全量（含 credential_ref 占位串） | 仅见 usage_event（按 tenant_id 过滤），不见配置内容 |
| **网关类型** | `newapi`（CHECK 约束） | 无网关类型约束（metadata 内嵌 `provider_type`/`base_url`） |

**边界一致性分析**：

- 官方网关由 Admin 统一管理，所有租户共享，`credential_ref` 占位待 G2 gate 解锁。
- 租户私有模型由 CEO 自管，`credential_ref` 同样走 `scheme:reference` 格式校验（`_validate_reference`），密钥值同样不落库。
- 两者均遵循"DB 零密钥值列"铁律，差异仅在管理方与可见性。

**潜在改进点**：当前 `model_gateways` 表无 `source` / `tenant_id` 列，无法支持"租户私有网关"（即租户自管网关配置而非模型条目）。若未来需要租户私有网关，须 additive 加 `source` / `tenant_id` 列，与 `tenant_private_capabilities` 形成两套模型治理路径。但本期不建议引入此复杂度。

### credential_ref 真实密钥托管的安全前提（G2 gate）

当前 `credential_ref` 仅存 `scheme:reference` 不透明串，无真实密钥托管实现。要解锁 G2 gate，须满足以下安全前提：

#### 1. 密钥托管后端选型

`credential_ref` 的 `scheme` 已预留三种：

| scheme | 含义 | 实现前提 | 适用场景 |
| --- | --- | --- | --- |
| `env` | 环境变量名 | 进程启动时注入，`os.getenv(reference)` | 开发/单机部署 |
| `kms` | KMS ARN | 云厂商 SDK 解析，IAM 权限控制 | 生产/云部署 |
| `vault` | Vault 路径 | HashiCorp Vault 客户端解析，动态密钥 | 生产/多租户 |

#### 2. 解析边界（铁律）

- **Admin 绝不解析 `credential_ref`**：Admin 仅存储不透明串，不 import 任何密钥解析库（`boto3` / `hvac` 等），不发起任何出站调用。
- **解析权归 Workspace 执行层**：`ModelGatewayAdapter` 在执行时解析 `credential_ref`，获取真实密钥，发起出站调用。解析逻辑须在 Workspace 侧封装，Admin 不可见。
- **密钥不落库**：解析后的密钥值仅存在于 Workspace 进程内存，绝不写回 DB、绝不写日志、绝不回传 Admin。

#### 3. 访问控制

- **KMS/Vault 策略**：须配置 IAM 策略，仅允许 Workspace 执行角色解密特定 `credential_ref`，Admin 角色无解密权限。
- **租户隔离**：租户 A 的 Workspace 不可解析租户 B 的 `credential_ref`（须在 KMS/Vault 策略中按 tenant_id 隔离）。
- **审计**：KMS/Vault 的解密操作须有独立审计日志（云厂商原生或 Vault audit backend）。

#### 4. 密钥轮转

- `credential_ref` 须支持密钥轮转（KMS 动态密钥 / Vault 动态 secret），DB 中的引用串不变，实际密钥定期轮转。
- 轮转须无 downtime：Workspace 执行层每次调用都重新解析（或带 TTL 缓存）。

#### 5. gate 解锁条件

G2 gate 须 **总控决策席 + 安全边界席** 双签，确认：
1. 密钥托管后端选型（env/kms/vault 之一或组合）。
2. 解析边界（Admin 不解析，Workspace 解析）。
3. 访问控制策略（IAM/Vault 策略）。
4. 审计方案（KMS/Vault 原生审计 + Curis evolution_events）。
5. 轮转方案。

### 当前继续 scheme:reference 占位的原因

1. **G2 gate 未解锁**：真实密钥托管须总控决策席 + 安全边界席双签，本期未进入此 gate。
2. **低成本路径**：ADR-0028 G2 决策(b) 明确"本期不持久化任何真实凭证"，`credential_ref` 仅作形状占位，避免引入密钥托管复杂度。
3. **Workspace 执行层现状**：`ModelGatewayAdapter` 当前通过 env `CURIS_MODEL_GATEWAY_API_KEY` 注入密钥，不依赖 `credential_ref` 解析。占位串不影响执行。
4. **契约先行**：`credential_ref` 格式（`scheme:reference`）已定义并校验，待 G2 gate 解锁后只需补解析逻辑，DB schema 不变。
5. **安全边界席约束**：在密钥托管方案未定前，强行实现真实密钥存储会触碰"DB 零密钥值列"铁律，风险高于收益。

### Admin 绝不出站、绝不解析凭证的铁律

此铁律在 ADR-0028 §1.3 / §8（约束 6/7）中明确，落地方式：

| 铁律 | 落地方式 | 验证 |
| --- | --- | --- |
| Admin 绝不出站 | `model_catalog.py` / `gateway_catalog.py` 不 import `urllib` / `requests` / `httpx`；不发起任何 HTTP 调用 | 禁止区扫描（`test_d5_*` 零命中 `urllib`/`requests`/`httpx`） |
| Admin 绝不解析凭证 | `catalog_constants.py` 仅校验 `credential_ref` 格式（正则），不解析 `scheme:reference`；不 import `boto3` / `hvac` / `os.getenv`（对 credential_ref） | 禁止区扫描零命中 `boto3`/`hvac` |
| Admin 绝不持久化密钥值 | `model_gateways` / `official_models` 表零 `api_key` / `token` 列；`credential_ref` 是 TEXT 引用串 | DDL 审查 + 禁止区扫描 |
| Admin 绝不向 Workspace 回传密钥 | `/api/catalog/gateways` 显式排除 `credential_ref`；`list_catalog_gateways()` 仅选非密钥列 | 测试 `test_d5_*` 断言 catalog 响应无 `credential_ref` 字段 |

---

## 设计建议

### 数据模型建议

#### 1. `model_gateways` 表扩展（additive，待 R-10 / G2 gate）

当前表结构已满足 MVP，未来扩展建议（均 additive `_ensure_column`）：

| 新增列 | 类型 | 说明 | 前置 gate |
| --- | --- | --- | --- |
| `source` | text default 'official' | 官方网关 vs 租户私有网关区分；CHECK `('official','tenant_private','marketplace')` | R-10 |
| `tenant_id` | text default 'platform' | 租户私有网关的归属租户；official='platform' | R-10 |
| `description` | text default '' | 网关描述（运营备注） | 无 |
| `updated_at` | text default current_timestamp | 与 `official_models` 对齐 | 无 |
| `health_status` | text default 'unknown' | 网关健康状态（unknown/healthy/degraded/down）；由 Workspace 被动上报，Admin 只读 | R-10 |

**不建议扩展的列**：
- `api_key` / `token` / `secret`：违反"DB 零密钥值列"铁律。
- `health_checked_at`：Admin 不出站，不主动探测；若由 Workspace 上报，则落 `health_status` 即可。

#### 2. `gateway_type` 枚举扩展（R-10）

当前 `GATEWAY_TYPE = ['newapi']`。R-10 评估时建议扩展为：

```python
GATEWAY_TYPE = ['newapi', 'litellm', 'openai_direct', 'anthropic_direct']
```

- `newapi`：OpenAI 兼容，国内多模型中转（当前）。
- `litellm`：100+ 厂商统一接口，多格式协议转换。
- `openai_direct`：直连 OpenAI（无中转）。
- `anthropic_direct`：直连 Anthropic。

**Adapter 策略**：`ModelGatewayAdapter` 按 `gateway_type` 分派不同执行逻辑。Admin 仍只定义元数据，不 import 任何 Adapter。

#### 3. `credential_ref` 格式扩展（G2 gate）

当前 `scheme ∈ {env, kms, vault}`。G2 gate 解锁后建议扩展：

| scheme | 用途 | 解析方 |
| --- | --- | --- |
| `env` | 环境变量 | Workspace |
| `kms` | KMS ARN | Workspace（须 IAM 权限） |
| `vault` | Vault 路径 | Workspace（须 Vault token） |
| `k8s_secret` | Kubernetes Secret 名 | Workspace（须 RBAC 权限） |

Admin 仍仅校验格式，不解析。

### API 设计建议

#### 1. 网关管理 API（已有，保持稳定）

- `GET /api/platform/gateways`：Admin 列表（含 credential_ref 占位串）。
- `POST /api/platform/gateways`：Admin 新增。
- `PUT /api/platform/gateways/{gateway_id}`：Admin 启停。
- `GET /api/catalog/gateways`：Workspace 只读（不含 credential_ref）。

**建议新增**（R-10）：

- `PATCH /api/platform/gateways/{gateway_id}`：Admin 编辑网关元数据（name/base_url/default_model/description）。当前无编辑路径，只能新建+停用。
- `GET /api/platform/gateways/{gateway_id}/health`：Admin 只读网关健康状态（由 Workspace 被动上报，Admin 不主动探测）。

#### 2. 网关健康上报 API（R-10，Workspace 侧）

- `POST /api/workspace/gateways/{gateway_id}/health`：Workspace 执行后被动上报健康状态（`healthy`/`degraded`/`down` + 延迟/错误率）。Admin 只读此状态，不出站。

#### 3. catalog 投影白名单（强化）

`/api/catalog/gateways` 须持续保证白名单列：

```python
# 允许返回的列（白名单）
CATALOG_GATEWAY_COLUMNS = {"gateway_id", "name", "type", "base_url", "status"}
# 显式排除：credential_ref, default_model, source, tenant_id, health_status
```

建议在 `list_catalog_gateways()` 中用显式列名 SELECT（已实现），并在测试中断言响应不含敏感字段。

### 边界规则

#### 1. Admin 边界（铁律，不可突破）

| 规则 | 实现 | 违反后果 |
| --- | --- | --- |
| Admin 不 import `model_gateway` | `model_catalog.py` / `gateway_catalog.py` 无 `from .model_gateway import` | 禁止区扫描失败 |
| Admin 不发起任何 HTTP 调用 | 不 import `urllib`/`requests`/`httpx` | 禁止区扫描失败 |
| Admin 不解析 `credential_ref` | 仅正则校验格式，不 `os.getenv`/`boto3`/`hvac` | 禁止区扫描失败 |
| Admin 不持久化密钥值 | DB 零密钥列 | DDL 审查失败 |
| Admin 不向 Workspace 回传密钥 | catalog 投影白名单 | 测试断言失败 |

#### 2. 官方网关 vs 租户私有模型边界

| 维度 | 官方网关 | 租户私有模型 |
| --- | --- | --- |
| 管理方 | Admin | CEO（Workspace） |
| 载体 | `model_gateways` + `official_models` | `tenant_private_capabilities` |
| credential_ref 存储 | `model_gateways.credential_ref` | `metadata_json.credential_ref` |
| Admin 可见 | 全量（含占位串） | 仅 usage_event（按 tenant_id） |
| Workspace 可见 | `/api/catalog/gateways`（不含 credential_ref） | `/api/workspace/private-models`（租户内） |
| 网关类型 | `newapi`（CHECK） | 无约束（metadata 内嵌） |

#### 3. credential_ref 解析边界

| 层 | 权限 |
| --- | --- |
| Admin | 仅存储 + 格式校验，不解析 |
| Workspace 执行层 | 解析 + 出站调用（须 IAM/Vault 权限） |
| DB | 零密钥值列 |
| 日志 | 不记录解析后的密钥值 |

#### 4. 网关类型扩展边界（R-10）

- 新增 `gateway_type` 须经独立 ADR + 总控决策席 gate。
- 每种类型须有对应的 Adapter 实现（Workspace 侧），Admin 仍只存元数据。
- `GATEWAY_TYPE` 枚举扩展须 additive，不破坏既有 `newapi` 行。

---

## 前置条件

### G2 gate（credential_ref 真实密钥托管）

- **解锁条件**：总控决策席 + 安全边界席双签。
- **须确认**：密钥托管后端选型（env/kms/vault）、解析边界（Admin 不解析）、访问控制（IAM/Vault 策略）、审计方案、轮转方案。
- **解锁后**：Workspace 执行层补 `credential_ref` 解析逻辑，DB schema 不变（`credential_ref` 列已存在）。

### R-10 gate（gateway_type 扩展）

- **解锁条件**：独立 ADR 评估多网关类型需求。
- **须确认**：是否需要 LiteLLM/直连等备选网关；每种类型的 Adapter 实现方案；多网关 failover 策略。
- **解锁后**：`GATEWAY_TYPE` 枚举扩展，`model_gateways.type` CHECK 约束更新（additive）。

### 网关健康检查 gate（R-10 子项）

- **解锁条件**：Workspace 侧确定健康上报机制（被动上报 vs 主动探测）。
- **须确认**：Admin 不出站铁律下，健康状态只能由 Workspace 上报；上报频率、状态机、告警阈值。
- **解锁后**：`model_gateways` additive 加 `health_status` 列，新增 Workspace 上报 API。

---

## 结论

1. **New API 作为主网关合理**：OpenAI 兼容 + 国内生态成熟 + 运营后台能力，与 Curis `ModelGatewayAdapter` 零适配成本。当前 `GATEWAY_TYPE=['newapi']` 单值保持不变。

2. **LiteLLM 作为备选值得预留**：R-10 评估时建议将 `litellm` 纳入 `GATEWAY_TYPE` 枚举，用于多格式协议转换或高级可观测性场景。但本期不解锁，保持单值。

3. **官方网关与租户私有模型边界已清晰**：官方走 `model_gateways` + `official_models`，租户私有走 `tenant_private_capabilities`，两者均遵循"DB 零密钥值列"铁律，差异在管理方与可见性。不建议本期引入"租户私有网关"（`model_gateways` 加 `source`/`tenant_id`），避免复杂度。

4. **credential_ref 占位正确**：`scheme:reference` 格式已定义并校验，G2 gate 未解锁前继续占位是低成本路径的正确选择。Workspace 执行层当前通过 env 注入密钥，不依赖 `credential_ref` 解析，占位不影响执行。

5. **G2 gate 解锁须满足 5 项安全前提**：密钥托管后端选型、解析边界（Admin 不解析）、访问控制（IAM/Vault 策略）、审计方案、轮转方案。解锁后只需 Workspace 侧补解析逻辑，DB schema 不变。

6. **Admin 绝不出站、绝不解析凭证铁律须持续守护**：通过禁止区扫描（`urllib`/`requests`/`httpx`/`boto3`/`hvac` 零命中）+ DDL 审查（零密钥列）+ catalog 投影白名单（`credential_ref` 不外泄）三重保障。任何新功能不得突破此铁律。

7. **网关健康检查与多网关 failover 留待 R-10**：当前单网关 + env 注入密钥已满足 MVP；健康检查须 Workspace 被动上报（Admin 不出站），failover 须多网关类型支持，均留待 R-10 评估。
