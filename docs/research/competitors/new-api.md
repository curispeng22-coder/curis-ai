# New API 竞品档案

> 研究时间：2026-07-09
> 研究员：research-gateway
> 研究目的：为 Curis Admin Platform 模型网关（`model_gateways` 表）的设计提供竞品参考

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **项目名** | New API（新一代大模型网关与 AI 资产管理系统） |
| **GitHub URL** | https://github.com/QuantumNous/new-api （原 `Calcium-Ion/new-api`） |
| **官方文档** | https://docs.newapi.pro/zh/docs |
| **开源协议** | GNU Affero General Public License v3.0（AGPLv3），附加 Section 7 条款；同时提供商业授权 |
| **Star 数** | 已上 Trendshift 榜单（#20180），被 HelloGitHub、Product Hunt 收录（精确数字需实时查询，预估 20k+） |
| **主语言** | Go（后端）+ JavaScript/React（前端） |
| **Commit 数** | 6,083 |
| **贡献者** | 274 人 |
| **最新活跃** | 2026-07-08（高度活跃，几乎每日提交） |
| **Docker 镜像** | `calciumion/new-api:latest` |
| **维护组织** | QuantumNous（提供商业授权联系：support@quantumnous.com） |

### 项目定位声明（来自 README）

> "本项目仅面向**合法授权的 AI API 网关、组织内部鉴权、多模型管理、用量统计、成本核算和私有化部署**场景。使用者必须合法取得上游 API Key、账号、模型服务或接口权限，并遵守上游服务条款及适用法律法规。"

这一定位与 Curis Admin Platform "Admin 只定义元数据 + 只读计量，不执行调用" 的边界存在**职责重叠**，需要重点分析借鉴边界。

---

## 核心功能

### 1. 渠道（Channel）管理 —— 对应 Curis `model_gateways`

New API 的"渠道"等价于 Curis 的"模型网关"概念，是上游 AI 供应商的抽象。

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **渠道增删改查** | 完整的渠道生命周期管理 | ⭐⭐⭐ 直接参考表结构 |
| **批量创建渠道** | 支持批量导入渠道 | ⭐⭐ |
| **渠道分组** | 为不同分组设置不同倍率 | ⭐⭐⭐ Curis 的分组计量可参考 |
| **模型列表设置** | 渠道可声明支持的模型列表 | ⭐⭐⭐ Curis `supported_models` 字段可参考 |
| **渠道加权随机** | ⚖️ 按权重做负载均衡 | ⭐ New API 执行调用才需要，Curis 不执行调用则不需要 |
| **失败自动重试** | 🔄 可配置重试次数 | ⭐ 同上，Curis 不执行调用 |
| **自动禁用渠道** | 根据请求成功率自动禁用 | ⭐ 同上 |
| **渠道可用性检查** | `CHANNEL_TEST_FREQUENCY` 定期测试 | ⭐⭐ Curis 可做只读健康检查 |
| **渠道余额更新** | `CHANNEL_UPDATE_FREQUENCY` 定期更新余额 | ⭐⭐⭐ Curis 只读计量可参考 |
| **高级自定义渠道** | 支持自定义上游端点配置（PR #5590） | ⭐⭐ Curis `credential_ref` 占位设计可参考 |
| **指定渠道调用** | 管理员令牌可通过 `ONE_API_KEY-CHANNEL_ID` 指定 | ⭐ Curis 不执行调用 |
| **Cloudflare AI Gateway** | 渠道代理可填 CF 地址 | ⭐ |
| **列宽持久化** | UI 列宽拖拽调整并持久化（PR #5948） | ⭐ 体验细节 |

**关键结论**：New API 渠道管理的"元数据定义"部分（分组、模型列表、倍率、健康检查、余额查询）高度适合 Curis 借鉴；而"执行调用"部分（加权随机、重试、禁用）Curis 不应照搬，因为 Admin 不执行调用。

### 2. 模型目录（Model Catalog）

| 能力 | 说明 |
|------|------|
| **多格式接口** | Chat / Responses / Image / Audio / Video / Embeddings / Rerank / Realtime / Claude Messages / Gemini Chat |
| **格式互转** | OpenAI ⇄ Claude Messages、OpenAI → Gemini、Gemini → OpenAI、Responses ⇄ Chat（开发中） |
| **Reasoning Effort** | 支持 `o3-mini-high/medium/low`、`gpt-5-high/medium/low`、`claude-3-7-sonnet-thinking`、`gemini-2.5-*-thinking/nothinking` 等后缀控制 |
| **模型映射** | 重定向用户请求的模型名称 |
| **Token 比率配置** | 为各模型配置 token 比率（如 GPT-5.6） |
| **缓存计费支持** | OpenAI、Azure、DeepSeek、Claude、Qwen 的 cache billing 统计 |

### 3. 支持的模型供应商

| 类别 | 供应商 |
|------|--------|
| **海外头部** | OpenAI（含 Responses/Realtime）、Anthropic Claude、Google Gemini、Azure OpenAI、Mistral、Cohere、xAI |
| **国内头部** | DeepSeek、通义千问 Qwen、文心一言、讯飞星火、智谱 ChatGLM、腾讯混元、360 智脑、Moonshot、百川、MINIMAX、阶步星辰、零一万物、字节豆包 |
| **多模态** | Midjourney（通过 Midjourney-Proxy）、Suno（音乐）、Dify（ChatFlow） |
| **Rerank** | Cohere、Jina |
| **聚合平台** | OpenRouter、Groq、together.ai、novita.ai、硅基流动 SiliconCloud、Coze |
| **本地/自托管** | Ollama |
| **自定义上游** | 支持配置合法授权的自定义端点 |

### 4. 用量统计与成本核算

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **数据仪表盘** | 可视化控制台与统计分析 | ⭐⭐⭐ |
| **按次计费** | 组织级按请求计费 | ⭐⭐⭐ |
| **按量计费** | 按 token 用量计费 | ⭐⭐⭐ |
| **缓存命中成本核算** | cache billing 单独统计 | ⭐⭐⭐ Curis 计量可参考 |
| **Token 比率** | 可配置各模型 token 比率 | ⭐⭐⭐ |
| **分组倍率** | 用户分组 × 渠道分组 × 模型倍率 | ⭐⭐⭐ Curis 多维计量可参考 |
| **饱和保护** | int32 饱和钳制，防止畸形计费输入 | ⭐⭐ 健壮性设计 |
| **参数验证** | 验证 quantity 参数，加固额度计算路径 | ⭐⭐ |
| **审计能力** | 配额饱和事件记录在 `admin_info` 供审计 | ⭐⭐⭐ Curis 审计日志可参考 |
| **音频时长钳制** | 负音频时长钳制后再转 token | ⭐ |

### 5. 令牌（Token）与额度控制

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **Token 分组** | 令牌分组管理 | ⭐⭐ |
| **模型限制** | 令牌级模型访问控制 | ⭐⭐⭐ Curis RBAC 可参考 |
| **过期时间** | 令牌过期设置 | ⭐⭐⭐ |
| **额度限制** | 令牌级额度（与账户额度分离） | ⭐⭐⭐ Curis 预算控制可参考 |
| **IP 范围限制** | 令牌级 IP 白名单 | ⭐⭐ |
| **用户级限速** | 🚦 用户级别模型速率限制 | ⭐⭐ |
| **配额查询工具** | [new-api-key-tool](https://github.com/Calcium-Ion/new-api-key-tool) | ⭐⭐ |
| **账户安全** | 邮箱规范化（trim+lowercase）、唯一性校验、并发写入序列化 | ⭐⭐⭐ |
| **会话安全** | `SESSION_COOKIE_SECURE` / `SESSION_COOKIE_TRUSTED_URL` | ⭐⭐ |

### 6. 支付/订阅能力

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **易支付（EPay）** | 兼容易支付协议的内部充值 | ⭐ Curis Admin 若不做支付则不参考 |
| **Stripe** | 国际支付渠道 | ⭐ 同上 |
| **兑换码** | 批量生成/导出兑换码充值 | ⭐⭐ |
| **充值链接** | 可配置外部充值链接 | ⭐ |
| **新用户初始额度** | 注册即赠额度 | ⭐ |
| **美元额度显示** | 支持美元单位 | ⭐⭐ |
| **灵活计费策略** | 面向内部管理或企业客户 | ⭐⭐ |

**关键结论**：New API 把"支付/订阅"与"模型网关"耦合在一起。Curis Admin Platform 若定位为"只读计量 + 不执行调用"，应**避免**把支付能力塞进 Admin，而应由独立的计费系统承担。

### 7. 日志能力

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **请求日志** | 记录每次调用 | ⭐⭐⭐ Curis 计量日志可参考 |
| **额度明细** | 额度使用明细查看 | ⭐⭐⭐ |
| **错误日志** | `ERROR_LOG_ENABLED` 开关 | ⭐⭐⭐ |
| **独立日志库** | `LOG_SQL_DSN` 为 logs 表使用独立数据库 | ⭐⭐⭐ Curis 日志分离可参考 |
| **Pyroscope** | 连续性能分析 | ⭐ |
| **流式超时** | `STREAMING_TIMEOUT=300` | ⭐ |

### 8. 授权与登录

| 方式 | 说明 |
|------|------|
| **邮箱** | 基础注册 |
| **飞书** | OAuth |
| **GitHub** | OAuth |
| **微信公众号** | OAuth |
| **Discord** | OAuth |
| **LinuxDO** | OAuth |
| **Telegram** | OAuth |
| **OIDC** | 统一认证 |
| **Cloudflare Turnstile** | 人机校验 |

---

## 架构特点

### 技术栈

| 层级 | 技术 |
|------|------|
| **后端语言** | Go |
| **前端框架** | React（含 Electron 桌面端支持） |
| **容器化** | Docker / Docker Compose（含 cosign 签名） |
| **性能分析** | Pyroscope |
| **国际化** | i18n（中/繁/英/法/日） |
| **会话管理** | 可选 Secure session cookies |

### 数据存储

| 存储类型 | 说明 | Curis 借鉴价值 |
|----------|------|----------------|
| **SQLite** | 默认数据库（Docker 挂载 `/data`） | ⭐⭐ 轻量部署 |
| **MySQL** | ≥ 5.7.8 | ⭐⭐⭐ |
| **PostgreSQL** | ≥ 9.6 | ⭐⭐⭐ Curis 主选 |
| **Redis** | 缓存（推荐），多机部署需 `CRYPTO_SECRET` | ⭐⭐⭐ |
| **内存缓存** | `MEMORY_CACHE_ENABLED` | ⭐⭐ |
| **批量更新** | `BATCH_UPDATE_ENABLED` / `BATCH_UPDATE_INTERVAL` | ⭐⭐⭐ 高并发写入优化 |

### 部署模式

| 方式 | 说明 |
|------|------|
| **Docker Compose（推荐）** | `docker-compose up -d` 一键启动 |
| **Docker 命令** | 支持 SQLite 或 MySQL |
| **宝塔面板** | ≥ 9.2.0，应用商店一键安装 |
| **多机部署** | 需 `SESSION_SECRET` + 共享 Redis + `CRYPTO_SECRET` |

### 系统架构要求

- 64 位系统（amd64 / arm64），不支持 32 位
- 容器引擎：Docker / Docker Compose

### 关键环境变量（计费与运维相关）

```env
STREAMING_TIMEOUT=300                    # 流式超时（秒）
MAX_REQUEST_BODY_MB=32                   # 最大请求体（MB，解压后计）
STREAM_SCANNER_MAX_BUFFER_MB=64          # 流扫描器最大行缓冲（MB）
AZURE_DEFAULT_API_VERSION=2025-04-01-preview
ERROR_LOG_ENABLED=false                  # 错误日志开关
PYROSCOPE_URL=                           # 性能分析服务
SESSION_SECRET=                          # 多机部署必须
CRYPTO_SECRET=                           # Redis 加密必须
SQL_DSN=                                 # 数据库连接
REDIS_CONN_STRING=                       # Redis 连接
MEMORY_CACHE_ENABLED=                    # 内存缓存
```

### 中继架构（执行调用）

New API 的核心是**中继转发**架构：

```
用户请求 → New API（鉴权 + 计费 + 路由）→ 上游模型供应商
                                      ↓
                                   返回结果（流式/非流式）
```

这一架构与 Curis Admin Platform "不执行调用"的定位**本质不同**。Curis Admin 是"元数据管理 + 只读计量"，而 New API 是"执行调用 + 在线计费"。

---

## 与 Curis Admin Platform 的关系

### Curis Admin 当前网关管理设计回顾

根据任务背景：
- `model_gateways` 表存储网关元数据
- `credential_ref` 为 `scheme:reference` 占位（不存储明文凭证）
- Admin 只定义元数据 + 只读计量
- Admin **不执行调用**

### 可借鉴的设计

#### 1. 渠道元数据模型（⭐⭐⭐ 强烈推荐）

New API 的渠道表结构可作为 Curis `model_gateways` 表的设计参考：
- 渠道名称、类型、BaseURL
- 支持的模型列表（`supported_models`）
- 分组归属
- 倍率配置
- 健康检查频率
- 余额查询频率
- 权重（Curis 可保留字段但不在 Admin 层使用）

#### 2. 多维计量体系（⭐⭐⭐ 强烈推荐）

New API 的"用户分组 × 渠道分组 × 模型倍率 × 缓存命中"四维计量模型，非常适合 Curis 的只读计量场景：
- 用户分组倍率（组织/团队维度）
- 渠道分组倍率（网关维度）
- 模型倍率（模型维度）
- 缓存命中单独计费（成本精细化）

#### 3. 日志分离设计（⭐⭐⭐ 强烈推荐）

`LOG_SQL_DSN` 为 logs 表使用独立数据库的设计，适合 Curis 的高频计量日志场景，避免主库被日志拖慢。

#### 4. 健康检查与余额查询（⭐⭐⭐ 推荐）

`CHANNEL_TEST_FREQUENCY`（可用性检查）和 `CHANNEL_UPDATE_FREQUENCY`（余额更新）两个定时任务设计，适合 Curis 的只读监控：
- 定期检查网关可达性（不执行业务调用）
- 定期查询网关余额（只读计量）

#### 5. 安全加固细节（⭐⭐⭐ 推荐）

- 邮箱规范化（trim + lowercase）+ 唯一性校验
- 并发写入序列化防重复账户
- 配额饱和钳制（int32 防溢出）
- quantity 参数验证
- 负音频时长钳制

#### 6. 批量更新优化（⭐⭐⭐ 推荐）

`BATCH_UPDATE_ENABLED` + `BATCH_UPDATE_INTERVAL` 的批量聚合写入设计，适合 Curis 高频计量数据的写入优化。

#### 7. 凭证占位设计（⭐⭐ 参考）

New API 的"高级自定义渠道"与 Curis 的 `credential_ref: scheme:reference` 占位设计理念相通——都不在主表中存储明文凭证。

### 不应借鉴的设计

#### 1. 执行调用能力（❌ 强烈不借鉴）

New API 的核心是"中继转发执行调用"，包括：
- 加权随机负载均衡
- 失败自动重试
- 自动禁用渠道
- 流式转发
- 格式互转（OpenAI ⇄ Claude ⇄ Gemini）

**Curis Admin 不应执行调用**，这些能力应交给下游的 Model Gateway Adapter（如 New API 本身、One API、LiteLLM）承担。Admin 只做元数据 + 计量。

#### 2. 支付/订阅能力（❌ 不借鉴）

New API 把易支付、Stripe、兑换码、充值链接等支付能力与网关管理耦合。Curis Admin 若定位为"只读计量 + 不执行调用"，应避免把支付塞进 Admin，由独立的计费/财务系统承担。

#### 3. 用户额度账户体系（⚠️ 谨慎借鉴）

New API 维护用户级的"账户额度 + 令牌额度"双层体系，并直接扣减。Curis Admin 若只做"只读计量"，则不应维护可写的额度账户，而应只记录"计量数据"供下游计费系统消费。

#### 4. 在线注册与多渠道 OAuth（❌ 不借鉴）

New API 内置邮箱注册、飞书/GitHub/微信/Discord/LinuxDO/Telegram/OIDC 等多种登录。Curis Admin 作为内部管理平台，应走企业 SSO，不需要面向公众注册。

#### 5. 绘图/音乐/视频等多模态接口（❌ 不借鉴）

New API 支持 Midjourney、Suno、Dify 等。Curis Admin 的网关元数据应聚焦于"模型"维度，多模态接口的执行能力由下游 Adapter 承担。

#### 6. 前端可视化仪表盘的过度集成（⚠️ 谨慎借鉴）

New API 把数据看板内置在前端。Curis Admin 可考虑用独立 BI 工具（如 Grafana/Metabase）消费计量数据，而非自建看板。

### 不应把哪些 Curis 业务逻辑塞进 New API

基于 AGPLv3 协议风险和职责边界，以下 Curis 业务逻辑**不应**塞进 New API：

1. **Curis 的租户/组织/团队/项目层级模型** —— New API 的用户/分组模型较扁平，强行塞入会导致 AGPL 衍生品风险
2. **Curis 的 RBAC 权限体系** —— New API 有自己的令牌/用户权限模型，耦合会增加合规复杂度
3. **Curis 的财务/账单/发票系统** —— 应保持独立，通过计量数据接口对接
4. **Curis 的审计合规逻辑** —— 应在 Admin 层实现，不依赖 New API 的 `admin_info`
5. **Curis 的 SSO/身份提供商集成** —— 应在 Admin 层实现，New API 只作为下游 Adapter
6. **Curis 的业务模型映射**（如病例、患者、研究项目的模型使用配额）—— 属于业务域，不应下沉到网关层

正确做法：**Curis Admin 通过 API 调用 New API 的管理接口**（渠道管理、令牌管理、日志查询），把 New API 视为"模型网关 Adapter"之一，而非把 Curis 业务逻辑 fork 进 New API 代码库。

### 协议风险（AGPLv3）

#### AGPLv3 核心义务

1. **开源义务**：任何基于 New API 修改并**通过网络提供服务**的衍生作品，必须开源全部代码（包括服务端）
2. **传染性**：与 New API 代码紧密耦合的代码也会被"传染"为 AGPLv3
3. **Section 7 附加条款**：QuantumNous 附加了额外条款（需查阅 LICENSE 原文）

#### 对 Curis 的具体风险

| 风险场景 | 风险等级 | 说明 |
|----------|----------|------|
| **Fork New API 并二次开发** | 🔴 高 | 衍生作品必须开源，Curis 业务逻辑泄露 |
| **修改 New API 源码并部署为内部服务** | 🟡 中 | AGPLv3 对"内部使用"也有开源义务（网络服务条款） |
| **仅部署未修改的 New API 作为 Adapter** | 🟢 低 | 未修改则无衍生作品，但需保留署名 |
| **通过 API 调用 New API 管理接口** | 🟢 低 | API 调用不构成衍生作品 |
| **闭源商业产品集成 New API** | 🔴 高 | 必须购买商业授权或开源全部代码 |

#### 缓解方案

1. **首选**：Curis Admin **不修改 New API 源码**，仅通过 API 调用 New API 作为下游 Adapter
2. **次选**：如需定制，购买 QuantumNous 商业授权（support@quantumnous.com）
3. **备选**：改用 MIT 协议的 One API（见 one-api.md）

---

## 结论

### 适合 Curis 的定位：**下游模型网关 Adapter（主用）+ 元数据设计参考**

New API 在 Curis 架构中的角色应为：

```
Curis Admin Platform（元数据 + 只读计量）
        ↓ API 调用（渠道管理、日志查询）
New API（执行调用 + 在线计费）← 作为 Adapter 之一
        ↓
上游模型供应商（OpenAI / Claude / Gemini / ...）
```

#### 推荐策略

1. **借鉴元数据设计**：渠道表结构、多维计量、日志分离、健康检查等设计模式
2. **不借鉴执行逻辑**：负载均衡、重试、格式转换等由 New API 自己处理
3. **不 Fork 源码**：通过 API 集成，规避 AGPLv3 风险
4. **保留可替换性**：New API 是 Adapter 之一，Curis Admin 应支持切换到 One API 或 LiteLLM
5. **凭证隔离**：Curis 的 `credential_ref: scheme:reference` 占位设计与 New API 的凭证管理保持解耦

#### 不适合作为 Curis Admin 本体

New API 的"执行调用 + 在线计费 + 支付 + 用户注册"全栈设计与 Curis Admin "只读计量 + 不执行调用"的定位冲突。若把 Curis 业务逻辑塞进 New API，会同时面临 AGPLv3 合规风险和架构耦合问题。

#### 建议的集成边界

| Curis Admin 职责 | New API 职责 |
|------------------|--------------|
| 网关元数据定义 | 执行调用 |
| 只读计量数据汇总 | 在线计费扣减 |
| 组织/团队/项目层级 | 令牌/用户管理 |
| RBAC 权限 | 渠道路由 |
| 审计合规 | 请求日志 |
| 财务账单 | 充值/兑换码 |
| SSO 身份管理 | OAuth 登录 |

两端通过 **API + 计量数据回流**对接，不共享数据库，不共享代码库。
