# LiteLLM 竞品档案

> 研究时间：2026-07-09
> 研究员：research-gateway
> 研究目的：评估 LiteLLM 作为 Curis Model Gateway Adapter 备选方案的可行性

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **项目名** | LiteLLM（Python SDK + Proxy Server / AI Gateway） |
| **GitHub URL** | https://github.com/BerriAI/litellm |
| **官方文档** | https://docs.litellm.ai/ |
| **开源协议** | **双协议模式**：核心代码 MIT License；`enterprise/` 目录为 BerriAI Enterprise License（需订阅） |
| **Star 数** | 40,345 commits / 2,374 branches / 1,462 tags（Star 数为 LLM 网关领域最高之一，预估 15k+） |
| **主语言** | Python（核心 SDK 与 Proxy）+ TypeScript/React（UI Dashboard）+ Rust（部分性能组件） |
| **维护组织** | BerriAI（Berrie AI Inc.） |
| **企业版** | `litellm-enterprise` 包（当前 0.1.48+），与开源版并行发布 |
| **最新活跃** | 持续高频更新（几乎每日提交，大量 AI 辅助开发） |
| **Docker 镜像** | 基于 Chainguard Wolfi 基础镜像，多架构 amd64/arm64 |

### 项目定位

> "LiteLLM is an open source AI Gateway that gives you a single, unified interface to call 100+ LLM providers — OpenAI, Anthropic, Gemini, Bedrock, Azure, and more — using the OpenAI format."

LiteLLM 同时提供：
1. **Python SDK** —— 开发者库，统一调用 100+ LLM
2. **Proxy Server（AI Gateway）** —— 独立部署的网关服务
3. **Enterprise 版** —— 企业级控制能力

---

## 核心功能

### 1. 多模型统一接口（Python SDK）

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **统一 OpenAI 格式** | 100+ 供应商通过单一 OpenAI 兼容接口调用 | ⭐⭐⭐ |
| **Chat Completions** | `/v1/chat/completions` 完全兼容 | ⭐⭐⭐ |
| **Responses API** | `/v1/responses` 桥接 | ⭐⭐⭐ |
| **Images API** | `/v1/images/generations`、`/v1/images/edits` | ⭐⭐ |
| **Rerank API** | `/v1/rerank`、`/v1/score`（支持 vLLM/Qwen3-Reranker） | ⭐⭐ |
| **Embeddings** | OpenAI 兼容嵌入端点 | ⭐⭐⭐ |
| **Audio Transcriptions** | `/v1/audio/transcriptions` | ⭐⭐ |
| **流式 SSE** | fallback 错误格式与 OpenAI SSE 兼容 | ⭐⭐⭐ |
| **异常映射** | 所有供应商异常映射到 OpenAI 异常类型 | ⭐⭐⭐ Curis 错误处理可参考 |

### 2. Proxy Server（AI Gateway）模式

这是 Curis 最关注的能力——独立部署的网关服务。

#### 架构层次

| 层级 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **入口验证层** | `run_server` 启动前验证 `DATABASE_URL` 协议（仅接受 `postgresql://`） | ⭐⭐⭐ Curis 可参考严格启动校验 |
| **数据库层** | Prisma ORM，固定 `provider = 'postgresql'`，支持 `DATABASE_URL` 和 `DIRECT_URL` | ⭐⭐⭐ Curis 主选 PostgreSQL |
| **路由层（Router）** | 多种路由策略（含 LAR-1 语义路由），fallback 链式调度 | ⭐⭐ |
| **供应商抽象层** | `ProviderConfigManager` 统一管理供应商配置 | ⭐⭐⭐ Curis 网关抽象可参考 |
| **安全层** | 敏感数据掩码器、Semgrep 规则、护栏（guardrails） | ⭐⭐⭐ |
| **日志层** | Postgres 存储 + 冷存储（`ColdStorageHandler`，支持 GCS 等） | ⭐⭐⭐ |
| **调度器** | APScheduler 后台任务（如 FOCUS 报告导出） | ⭐⭐ |
| **UI Dashboard** | TypeScript/React（Tremor 图表），Usage 页面、密钥管理、团队预算 | ⭐⭐ |

#### 关键约束

- **强制 PostgreSQL**：Proxy 模式仅接受 `postgresql://` 协议的 `DATABASE_URL`，非 Postgres URL 直接退出
- **Prisma ORM**：使用 Prisma 管理数据库 schema 和迁移
- **双 URL 支持**：`DATABASE_URL`（连接池）+ `DIRECT_URL`（直连，用于迁移）

### 3. 成本追踪机制（⭐ Curis 重点关注）

LiteLLM 的成本追踪是三个竞品中最精细的，非常适合 Curis 的"只读计量"定位。

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **模型价格映射表** | `model_prices_and_context_window.json` 维护所有模型定价、上下文窗口、最大输出 token | ⭐⭐⭐ Curis 模型目录可参考 |
| **托管成本映射** | 支持从托管服务动态拉取最新价格（无需升级版本） | ⭐⭐⭐ Curis 价格更新机制可参考 |
| **分层定价** | 支持 `above_<N>_tokens` 阶梯定价（128k/200k/272k/512k 等阈值） | ⭐⭐⭐ Curis 阶梯计量可参考 |
| **图片 token 定价** | 区分文本输出 token 与图片输出 token（如 gpt-image-2: $10/1M 文本 vs $30/1M 图片） | ⭐⭐⭐ |
| **搜索查询计费** | Perplexity 按 `search_context_cost_per_query` 每次请求计费（非除以1000） | ⭐⭐⭐ |
| **Fallback 成本计算** | API 不返回 `usage.cost` 时使用手动计算器 | ⭐⭐⭐ Curis 计量兜底可参考 |
| **每日支出表** | `LiteLLM_DailyUserSpend` 按日汇总 | ⭐⭐⭐ Curis 计量汇总可参考 |
| **FOCUS 格式** | 支持 FOCUS 标准格式 CSV 导出至 GCS | ⭐⭐⭐ Curis 财务对接可参考 |
| **Mavvrik 集成** | 通过 FOCUS 标准将成本数据导出至 Mavvrik 平台 | ⭐⭐ |
| **增量追踪** | `metricsMarker` 增量追踪机制 | ⭐⭐ |

### 4. Fallback / Routing 能力

#### Fallback（故障转移）

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **链式 Fallback** | 多跳（multi-hop）fallback 链，错误信息逐跳累积 | ⭐⭐ |
| **流式 Fallback** | 流式请求触发 fallback 时通过 SSE 事件通知 | ⭐⭐ |
| **SSE 事件** | `litellm-fallback-metadata` 事件 + `x-litellm-attempted-fallbacks` 响应头 | ⭐⭐⭐ Curis 追踪可参考 |
| **可选错误暴露** | `include_fallback_errors: true`（opt-in） | ⭐⭐ |
| **运营开关** | `expose_fallback_errors_to_caller` 控制 | ⭐⭐ |
| **不可变性修复** | fallback 查找不再修改路由器配置（此前会 `pop` 移除列表项） | ⭐⭐ 健壮性设计 |
| **OpenAI 兼容** | 流式 fallback 错误格式与 OpenAI SSE 兼容（Vercel AI SDK 测试通过） | ⭐⭐⭐ |

#### Routing（路由策略）

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **LAR-1 语义路由** | 根据 `metadata.lar1`（confidence/evidence/time）选择部署层 | ⭐⭐ 创新但 Curis 不执行调用 |
| **部署层选择** | cloud-smart / cloud-fast / local / deep | ⭐⭐ |
| **阈值可配置** | 路由阈值可配置 | ⭐⭐ |
| **原子化策略切换** | 验证通过后才修改路由器状态，防止无效阈值残留 | ⭐⭐⭐ 健壮性设计 |
| **模型访问组** | `model_access_groups` 支持团队级模型权限扩展 | ⭐⭐⭐ Curis RBAC 可参考 |
| **负载均衡** | 多部署间分发请求 | ⭐⭐ |

### 5. 虚拟密钥与预算管理

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **虚拟密钥生成** | 密钥生成与预算控制 | ⭐⭐⭐ |
| **团队预算管理** | UI 中展示团队级预算 | ⭐⭐⭐ Curis 组织预算可参考 |
| **密钥概览** | UI 显示团队预算 | ⭐⭐⭐ |
| **预算控制** | 密钥级预算限制 | ⭐⭐⭐ |

### 6. 日志与可观测性

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **Postgres 日志存储** | 请求/响应持久化到 `LiteLLM_DailyUserSpend` 等表 | ⭐⭐⭐ |
| **冷存储（Cold Storage）** | 提示/响应卸载到冷存储（GCS 等） | ⭐⭐⭐ Curis 日志分层可参考 |
| **冷存储回读** | UI 日志详情视图通过 `ColdStorageHandler` 按存储对象键取回 | ⭐⭐⭐ |
| **敏感数据掩码** | `sensitive_data_masker` 对短于阈值的密钥/令牌完全掩码 | ⭐⭐⭐ Curis 凭证安全可参考 |
| **MCP 调试** | `mcp_debug` 对认证令牌掩码，仅保留首尾字符 | ⭐⭐⭐ |
| **Usage 页面** | Token 使用趋势图、请求量趋势图（支持 B/M 级格式化） | ⭐⭐⭐ |
| **日志详情抽屉** | 支持冷存储回读 | ⭐⭐⭐ |
| **第三方集成** | Mavvrik FOCUS（成本 CSV 导出）、Greptile（代码审查） | ⭐⭐ |
| **追踪 ID** | `x-litellm-attempted-fallbacks` 等响应头追踪 fallback 路径 | ⭐⭐⭐ Curis 链路追踪可参考 |

### 7. 护栏（Guardrails）

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **请求/响应安全防护** | 内置护栏机制 | ⭐⭐ |
| **Semgrep 规则** | 代码安全扫描 | ⭐⭐ |
| **缓存防毒** | cache poisoning 防护 | ⭐⭐ |

### 8. 支持的 LLM 供应商（100+）

| 类别 | 供应商 |
|------|--------|
| **云平台** | AWS Bedrock、Azure、Google VertexAI、Sagemaker |
| **模型厂商** | OpenAI、Anthropic、Cohere、Mistral、DeepSeek、Moonshot、Perplexity、SambaNova、NVIDIA NIM、Fireworks AI |
| **托管平台** | HuggingFace、VLLM、GitHub Copilot、OpenRouter |
| **新增供应商** | Darkbloom、zai/glm-5.1、zai/glm-4.7-flash |
| **其他** | hosted_vllm、Azure AI、Gemini 等 |

### 9. GitHub Copilot 特殊处理

通过 `transform_parsed_response_dict` hook 将 Anthropic 原生内容块合成为 OpenAI choices 格式——这种"格式归一化"思路值得 Curis 借鉴。

---

## 架构特点

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **核心 SDK** | Python | `litellm` 包 |
| **Proxy Server** | Python | 基于 FastAPI/Starlette |
| **UI Dashboard** | TypeScript + React + Tremor | 图表展示 |
| **性能组件** | Rust | `.cargo` 目录可见 |
| **ORM** | Prisma | 固定 `provider = 'postgresql'` |
| **包管理** | `uv`（从 Poetry 迁移） | 现代 Python 包管理 |
| **基础镜像** | Chainguard Wolfi | 安全加固，glibc 2.43-r10 |
| **CI/CD** | CircleCI + GitHub Actions | 双流水线 |
| **后台任务** | APScheduler | 如 FOCUS 报告导出 |
| **数据库迁移** | `ci_cd/run_migration.py` | Schema 迁移管理 |

### 数据存储

| 存储 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **PostgreSQL（强制）** | Proxy 模式唯一支持的关系数据库 | ⭐⭐⭐ Curis 主选一致 |
| **Prisma ORM** | Schema 管理和迁移 | ⭐⭐⭐ |
| **冷存储（GCS 等）** | 日志提示/响应离线存储 | ⭐⭐⭐ Curis 日志分层可参考 |
| **双 URL** | `DATABASE_URL`（连接池）+ `DIRECT_URL`（迁移） | ⭐⭐⭐ 高可用部署可参考 |

### 部署模式

| 模式 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **Docker** | Chainguard Wolfi 基础镜像，支持 `Dockerfile.non_root` 非 root 运行 | ⭐⭐⭐ 安全加固可参考 |
| **多架构** | amd64 / arm64 | ⭐⭐⭐ |
| **Kubernetes** | 通过 Terraform 模块部署至 AWS EKS / GCP GKE | ⭐⭐⭐ 企业部署可参考 |
| **Terraform 模块** | 公共注册表：`BerriAI/litellm/aws`、`BerriAI/litellm/google` | ⭐⭐⭐ IaC 可参考 |
| **GCP Cloud Shell** | 一键部署（含 DeployStack 教程） | ⭐⭐ |
| **AWS CloudShell** | 软一键部署（clone + cd + cp tfvars + terraform apply） | ⭐⭐ |
| **Render/Railway** | 一键部署按钮 | ⭐⭐ |
| **DevContainer** | `.devcontainer` 支持 VS Code Remote 开发 | ⭐⭐ |

### 企业级能力

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **Terraform 模块** | AWS/GCP 公共注册表 | ⭐⭐⭐ |
| **Microsoft Graph GCC High** | 支持政府云环境 | ⭐⭐ |
| **企业版包** | `litellm-enterprise`（0.1.48+） | ⭐⭐ |
| **数据库迁移脚本** | `ci_cd/run_migration.py` | ⭐⭐⭐ |
| **Semgrep 安全扫描** | 代码安全 | ⭐⭐⭐ |
| **缓存防毒** | cache poisoning 防护 | ⭐⭐⭐ |
| **Conventional Commits** | 强制提交规范 | ⭐⭐⭐ |
| **非 root 运行** | `Dockerfile.non_root` | ⭐⭐⭐ 安全加固 |

---

## 双协议模式详解

### 协议边界

LiteLLM 采用**双协议模式**，这是三个竞品中最独特的：

```
litellm/
├── litellm/           ← MIT License（开源核心）
├── litellm_core_utils/ ← MIT License
├── enterprise/        ← BerriAI Enterprise License（需订阅）
└── LICENSE            ← MIT License
```

#### MIT 部分（开源核心）

```
MIT License

Copyright (c) 2023 Berri AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

**MIT 部分包含**：
- Python SDK（核心调用逻辑）
- Proxy Server 基础功能（OpenAI 兼容网关、虚拟密钥、成本追踪、预算、fallback、请求/响应日志）
- 100+ 供应商适配

#### Enterprise 部分（需订阅）

```
The BerriAI Enterprise license (the "Enterprise License")
Copyright (c) 2024 - present Berrie AI Inc.

This software and associated documentation files (the "Software") may only be
used in production, if you (and any entity that you represent) have agreed to,
and are in compliance with, the BerriAI Subscription Terms of Service...
and otherwise have a valid BerriAI Enterprise license for the
correct number of user seats.

Subject to the foregoing sentence, you are free to modify this Software and
publish patches to the Software...

Notwithstanding the foregoing, you may copy and modify the Software for
development and testing purposes, without requiring a subscription.

Subject to the foregoing, it is forbidden to copy, merge, publish, distribute,
sublicense, and/or sell the Software.
```

**Enterprise 部分包含**（根据官方文档）：
- SSO / SCIM 集成
- 审计日志增强
- RBAC 细粒度权限
- 团队级预算控制增强
- 合规报表

### Enterprise License 关键条款

| 条款 | 说明 | 对 Curis 的影响 |
|------|------|-----------------|
| **生产使用需订阅** | `enterprise/` 目录代码在生产环境使用需购买订阅 | 若 Curis 需要企业版功能，需付费 |
| **开发测试免费** | 可免费复制和修改用于开发测试 | PoC 阶段可免费试用 |
| **席位授权** | 需为正确数量的用户席位购买授权 | 按 Curis 用户数计费 |
| **修改权** | 可修改并发布补丁 | 可定制 |
| **版权归属** | 修改版权归 BerriAI | 修改无法独占 |
| **禁止分发** | 禁止复制、合并、发布、分发、sublicense、出售 | 不能二次分发 |

### 对 Curis 的协议风险分析

| 使用场景 | 协议 | 风险等级 | 说明 |
|----------|------|----------|------|
| **仅用 MIT 核心功能** | MIT | 🟢 低 | 可闭源商用 |
| **Fork MIT 部分并修改** | MIT | 🟢 低 | 可闭源 |
| **集成进 Curis 闭源产品** | MIT | 🟢 低 | 允许 |
| **使用 enterprise/ 功能（生产）** | Enterprise | 🔴 高 | 需购买订阅 |
| **使用 enterprise/ 功能（开发测试）** | Enterprise | 🟢 低 | 免费试用 |
| **SaaS 部署 MIT 部分** | MIT | 🟢 低 | 无网络服务条款 |
| **修改 enterprise/ 并部署生产** | Enterprise | 🔴 高 | 需订阅 + 版权归属 BerriAI |

### MIT 核心功能是否够用？

根据官方文档：

> "LiteLLM OSS already covers the fundamentals — an OpenAI-compatible gateway, virtual keys, spend tracking, budgets, fallbacks, and request/response logging. Enterprise adds the controls larger organizations need."

**MIT 核心功能包含**：
- ✅ OpenAI 兼容网关
- ✅ 虚拟密钥
- ✅ 成本追踪
- ✅ 预算控制
- ✅ Fallback
- ✅ 请求/响应日志
- ✅ 100+ 供应商适配

**Enterprise 额外功能**：
- SSO / SCIM
- 审计日志增强
- RBAC 细粒度权限
- 团队级预算增强
- 合规报表

**结论**：对 Curis 的"只读计量 + 不执行调用"定位，MIT 核心功能**基本够用**。SSO 和 RBAC 可在 Curis Admin 层实现，无需依赖 LiteLLM Enterprise。

---

## 与 Curis Admin Platform 的关系

### Curis Model Gateway Adapter 备选评估

任务背景提到需评估 LiteLLM 是否适合作为 Curis Model Gateway Adapter 的备选。

#### LiteLLM 作为 Adapter 的优势

| 优势 | 说明 |
|------|------|
| **成本追踪最精细** | 分层定价、图片 token、搜索查询、Fallback 成本计算、每日汇总、FOCUS 格式 |
| **PostgreSQL 原生** | 与 Curis 主选数据库一致，强制 PostgreSQL 保证一致性 |
| **100+ 供应商** | 供应商覆盖最广 |
| **Python 生态** | 适合 AI/ML 场景，与 Curis 的 AI 定位契合 |
| **MIT 核心可闭源** | 不像 New API 的 AGPLv3 那样限制 |
| **企业级部署** | Terraform 模块、K8s、多云一键部署 |
| **冷存储日志** | 日志分层存储，适合大量计量数据 |
| **OpenAI 兼容** | SSE fallback 错误格式兼容 |
| **冷存储回读** | UI 支持冷存储日志回读 |
| **护栏机制** | 安全防护能力 |
| **Prisma ORM** | 现代 Schema 管理 |

#### LiteLLM 作为 Adapter 的劣势

| 劣势 | 说明 |
|------|------|
| **Python 性能** | 相比 New API 的 Go 后端，Python 并发性能较弱 |
| **强制 PostgreSQL** | 若 Curis 想用 MySQL 则不兼容 |
| **Enterprise 功能需付费** | SSO/RBAC/审计增强需订阅 |
| **架构较重** | Proxy + Prisma + 冷存储 + UI，比 One API 的单二进制重 |
| **企业版版权归属** | 修改 enterprise/ 版权归 BerriAI |
| **国内供应商覆盖** | 对国内模型（文心/星火/混元等）支持不如 New API/One API 全面 |

### 可借鉴的设计

#### 1. 成本追踪体系（⭐⭐⭐ 强烈推荐）

LiteLLM 的成本追踪是三个竞品中最精细的，Curis 的只读计量可直接借鉴：
- `model_prices_and_context_window.json` 模型价格映射表
- 托管成本映射（动态拉取最新价格）
- 分层定价（`above_<N>_tokens` 阶梯）
- 图片 token 与文本 token 分别计价
- 搜索查询按次计费
- Fallback 成本手动计算器（兜底）
- 每日支出汇总表（`LiteLLM_DailyUserSpend`）
- FOCUS 标准格式导出

#### 2. 冷存储日志分层（⭐⭐⭐ 强烈推荐）

- 热数据：PostgreSQL（近期日志，支持快速查询）
- 冷数据：GCS 等对象存储（历史日志，按需回读）
- `ColdStorageHandler` 统一接口
- UI 日志详情视图支持冷存储回读

适合 Curis 大量计量数据的长期存储。

#### 3. 凭证安全设计（⭐⭐⭐ 强烈推荐）

- `sensitive_data_masker` 对短于阈值的密钥/令牌完全掩码
- `mcp_debug` 对认证令牌掩码，仅保留首尾字符
- 这与 Curis 的 `credential_ref: scheme:reference` 占位设计理念一致

#### 4. 数据库启动校验（⭐⭐⭐ 推荐）

`run_server` 启动前验证 `DATABASE_URL` 协议（仅接受 `postgresql://`），非合规 URL 直接退出并给出可操作错误信息——这种"快速失败"设计值得 Curis 借鉴。

#### 5. 供应商抽象层（⭐⭐⭐ 推荐）

`ProviderConfigManager` 统一管理不同供应商的配置，适合 Curis 的网关元数据抽象。

#### 6. 链路追踪（⭐⭐⭐ 推荐）

`x-litellm-attempted-fallbacks` 等响应头追踪 fallback 路径，适合 Curis 的请求链路追踪。

#### 7. 模型访问组（⭐⭐⭐ 推荐）

`model_access_groups` 支持团队级模型权限扩展，适合 Curis 的 RBAC 设计。

#### 8. 原子化策略切换（⭐⭐⭐ 推荐）

验证通过后才修改路由器状态，防止无效阈值导致部分状态残留——这种"原子化配置更新"设计值得 Curis 借鉴。

#### 9. Fallback 不可变性修复（⭐⭐ 参考）

fallback 查找不再修改路由器配置（此前会 `pop` 移除列表项导致配置丢失）——这是一个值得 Curis 警惕的"查询副作用"反模式。

#### 10. 双 URL 数据库连接（⭐⭐⭐ 推荐）

`DATABASE_URL`（连接池）+ `DIRECT_URL`（迁移）的设计，适合 Curis 的高可用数据库部署。

### 不应借鉴的设计

#### 1. 执行调用与路由（❌）

同 New API/One API，LiteLLM 的 LAR-1 语义路由、负载均衡、fallback 执行等属于"执行调用"层，Curis Admin 不应执行调用。

#### 2. Enterprise 版功能依赖（❌）

SSO/SCIM、审计增强、RBAC 细粒度权限等应在 Curis Admin 层实现，不依赖 LiteLLM Enterprise（避免订阅成本和版权归属问题）。

#### 3. Python 性能瓶颈（⚠️）

若 Curis 计量数据量极大，Python 的 Proxy 可能成为瓶颈，需评估性能或选择 Go 方案（New API/One API）。

#### 4. UI Dashboard 过度集成（⚠️）

LiteLLM 的 Tremor 图表 UI 内置，Curis 可考虑独立 BI。

#### 5. 强制 PostgreSQL（⚠️ 双刃剑）

虽然是 Curis 主选，但若未来需要切换数据库，LiteLLM 不支持。

### 协议风险

#### MIT 核心部分（极低风险）

| 风险场景 | 风险等级 | 说明 |
|----------|----------|------|
| 使用 MIT 核心 | 🟢 低 | 可闭源商用 |
| Fork MIT 部分修改 | 🟢 低 | 可闭源 |
| 集成进 Curis 闭源产品 | 🟢 低 | 允许 |
| SaaS 部署 MIT 部分 | 🟢 低 | 无网络服务条款 |

#### Enterprise 部分（需订阅）

| 风险场景 | 风险等级 | 说明 |
|----------|----------|------|
| 生产使用 enterprise/ | 🔴 高 | 需购买订阅 |
| 修改 enterprise/ 版权 | 🟡 中 | 归 BerriAI |
| 二次分发 enterprise/ | 🔴 高 | 禁止 |

#### 缓解方案

1. **仅用 MIT 核心**：Curis 只使用 LiteLLM 的开源核心功能
2. **SSO/RBAC 自建**：在 Curis Admin 层实现，不依赖 Enterprise
3. **开发测试可免费**：PoC 阶段可试用 Enterprise 功能
4. **生产需评估**：若必须用 Enterprise 功能，需购买订阅

---

## 三个竞品对比总结

| 维度 | New API | One API | LiteLLM |
|------|---------|---------|---------|
| **协议** | AGPLv3 + 商业授权 | MIT | MIT（核心）+ Enterprise（订阅） |
| **语言** | Go + React | Go + React | Python + React + Rust |
| **数据库** | SQLite/MySQL/PostgreSQL | SQLite/MySQL/PostgreSQL | PostgreSQL（强制） |
| **供应商数** | 20+（含多模态） | 28+ | 100+ |
| **成本追踪** | 组织级 + 缓存计费 | 双层额度 + 多维倍率 | 分层定价 + FOCUS 格式 + 冷存储 |
| **格式互转** | ✅ OpenAI⇄Claude⇄Gemini | ❌ | ✅ OpenAI 兼容 |
| **Reasoning Effort** | ✅ | ❌ | 部分 |
| **Realtime API** | ✅ | ❌ | 部分 |
| **Fallback** | 基础重试 | 基础重试 | 多跳链式 + 流式 SSE |
| **企业部署** | Docker/宝塔 | Docker/宝塔/单二进制 | Terraform/K8s/多云 |
| **日志** | 独立日志库 | 独立日志库 | 冷存储分层 |
| **安全** | 邮箱规范化/会话安全 | 基础 | 敏感数据掩码/护栏 |
| **活跃度** | 高（6083 commits） | 低（1210 commits，放缓） | 高（40345 commits） |
| **国内模型** | 全面 | 全面 | 一般 |
| **闭源商用** | ❌（除非购买授权） | ✅ | ✅（核心） |
| **适合 Curis** | 主用 Adapter（需授权） | 备选 Adapter（合规友好） | 备选 Adapter（成本追踪最强） |

---

## 结论

### 适合 Curis 的定位：**Curis Model Gateway Adapter 备选方案（成本追踪与日志分层参考标杆）**

LiteLLM 在 Curis 架构中的角色：

```
Curis Admin Platform（元数据 + 只读计量）
        ↓ API 调用（渠道管理、日志查询）
        ↓
LiteLLM Proxy（备选 Adapter，MIT 核心，成本追踪最强）  ←  备选方案
        ↓
上游模型供应商（100+）
```

#### 推荐策略

1. **作为 New API/One API 之外的第三选项**：当 Curis 需要最强的成本追踪和日志分层时选择
2. **仅用 MIT 核心**：避免 Enterprise 订阅成本和版权归属问题
3. **借鉴成本追踪设计**：分层定价、FOCUS 格式、冷存储分层、每日汇总等
4. **借鉴安全设计**：敏感数据掩码、启动校验、双 URL 连接
5. **评估性能**：Python 性能可能不如 Go，需压测

#### 不适合作为 Curis Admin 本体

同 New API/One API，LiteLLM 的"执行调用 + 路由 + Fallback"全栈设计与 Curis Admin "只读计量 + 不执行调用"定位冲突。

#### 三选一建议

| Curis 需求优先级 | 推荐 | 理由 |
|------------------|------|------|
| **合规优先**（零 AGPLv3 风险） | One API | MIT 协议最宽松 |
| **功能优先**（最新模型/格式互转） | New API | 功能最全（需购买商业授权） |
| **成本追踪优先**（精细计量） | LiteLLM | 成本追踪最精细 |
| **国内模型覆盖优先** | New API / One API | 国内供应商支持更全面 |
| **企业部署优先**（K8s/多云） | LiteLLM | Terraform 模块最成熟 |
| **性能优先**（高并发） | New API / One API | Go 性能优于 Python |
| **PoC 快速验证** | One API | 单二进制部署最简 |

#### 综合建议

对 Curis Admin Platform，建议采用**多 Adapter 策略**：

1. **主 Adapter**：New API（购买商业授权）—— 功能最全，国内模型覆盖好
2. **合规备选**：One API（MIT）—— 当无法接受 AGPLv3 时切换
3. **计量参考标杆**：LiteLLM（MIT 核心）—— 不一定部署，但其成本追踪和日志分层设计值得 Curis Admin 借鉴

Curis Admin 的 `model_gateways` 表应设计为**Adapter 无关**的元数据模型，支持通过 `credential_ref: scheme:reference` 占位对接任意 Adapter（New API / One API / LiteLLM），保持可替换性。

#### 建议的集成边界

| Curis Admin 职责 | LiteLLM 职责 |
|------------------|--------------|
| 网关元数据定义 | 执行调用 |
| 只读计量数据汇总 | 成本追踪 |
| 组织/团队/项目层级 | 虚拟密钥/团队预算 |
| RBAC 权限 | 模型访问组 |
| 审计合规 | 请求/响应日志 |
| 财务账单 | FOCUS 格式导出 |
| SSO 身份管理 | （Enterprise 版有，但建议 Curis 自建） |

两端通过 **API + 计量数据回流**对接，Curis Admin 可消费 LiteLLM 的 `LiteLLM_DailyUserSpend` 表和 FOCUS 格式 CSV。
