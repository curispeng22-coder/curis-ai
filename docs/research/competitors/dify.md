# Dify 竞品档案

> 研究对象：Dify（github.com/langgenius/dify）
> 研究目的：为 Curis Admin Platform 能力市场（marketplace）的上架流程、审核机制、安装体验提供参考。
> 研究时间：2026-07-09

---

## 基本信息

| 项 | 内容 |
|----|------|
| 项目名 | Dify |
| 官网 | https://dify.ai |
| 仓库 | https://github.com/langgenius/dify |
| 插件市场 | https://marketplace.dify.ai |
| 官方插件仓库 | https://github.com/langgenius/dify-official-plugins |
| 协议 | Apache 2.0（主仓库），插件仓库同理 |
| GitHub Stars | 100K+（2025-06 突破 10 万 star，是增长最快的 LLM 应用平台之一） |
| 开发团队 | LangGenius（国际化团队，中文社区活跃） |
| 用户规模 | 云端 + 自托管混合，企业版客户覆盖广；marketplace 插件总安装量已达数百万级（如 DeepSeek 模型插件单家即 123 万+ 安装） |
| 起源 | 2023-05-15 开源，2025-02 v1.0 引入 plugin-first 架构 |

### 一句话定位
Dify 是一个开源的 LLM 应用开发平台，定位为"production-ready platform for agentic workflows"，通过直观的可视化界面组合 AI workflow、RAG pipeline、agent capabilities、model management 与 observability。

### 架构演进关键节点
- **v1.0 之前**：模型供应商、工具等内置在主仓库中
- **v1.0（2025-02）起**：转向 **plugin-first 架构**，所有核心模型和工具集成从主仓库迁移到 `dify-official-plugins` 独立仓库，通过 marketplace 分发

---

## 核心功能

Dify 平台核心功能矩阵：

| 模块 | 功能 | 说明 |
|------|------|------|
| **Workflow 编排** | 可视化工作流 | 拖拽式节点编排，支持 LLM、代码、HTTP、工具、条件分支等节点 |
| **Chatflow** | 对话型应用 | 面向对话场景的特殊 workflow |
| **Agent** | 智能体 | 支持 Function Calling、ReAct 等 Agent 推理策略 |
| **Knowledge Base（RAG）** | 知识库 | 文档导入、分块、嵌入、检索；支持多种数据源 |
| **Model Management** | 模型管理 | 统一管理多家模型供应商，配置 API Key，选择模型 |
| **Prompt IDE** | 提示词开发 | 在线调试 prompt、变量、模型组合 |
| **Observability** | 可观测性 | 集成 Opik、Langfuse 等可观测平台 |
| **API 发布** | 应用 API | 每个应用自动暴露 RESTful API |
| **Plugin System** | 插件系统 | v1.0 起的核心扩展机制 |
| **Marketplace** | 插件市场 | 集中分发插件，类似 VS Code Marketplace |

---

## Marketplace / 应用市场机制

Dify 自 v1.0 起将 marketplace 作为核心分发渠道。marketplace.dify.ai 是其官方插件市场。

### 插件类型（6 类）

Marketplace 将插件分为 **6 大类型**，每类对应不同的扩展场景：

| 类型 | 用途 | 典型示例 |
|------|------|----------|
| **Models（模型）** | 接入 LLM、Embedding、Rerank、STT、TTS | OpenAI、DeepSeek、Anthropic、Ollama、通义、火山方舟 |
| **Tools（工具）** | 工作流和 Agent 可调用的功能工具 | Tavily、Google Search、ComfyUI、Firecrawl、JSON Process |
| **Data Sources（数据源）** | 将外部数据导入知识库 | NDJSON dump、Dify Extractor |
| **Triggers（触发器）** | 从外部事件启动 workflow | Webhook、定时任务 |
| **Agent Strategies（Agent 策略）** | 自定义 Agent 推理逻辑 | Function Calling、ReAct、自定义规划算法 |
| **Extensions（扩展）** | 扩展平台核心能力 | Agora Conversational AI |
| **Bundles（捆绑包）** | 多插件集合 | 多个相关插件一起分发（如某供应商完整套件） |

### 插件分类标签

除类型外，还通过标签系统做功能领域分类：
- **SEARCH**（搜索）：Tavily、Google、Brave、Bing、Serper
- **IMAGE**（图像）：Stability、ComfyUI、Stable Diffusion
- **VIDEOS**（视频）：YouTube、FFmpeg、D-ID
- **UTILITIES**（实用工具）：JSON Process、Firecrawl、Regex
- **PRODUCTIVITY**（生产力）：Google、SearchApi、exa
- **BUSINESS / FINANCE**：alipay_plugin、alipay_subscribe
- **MEDICAL**（医疗）：PubMed
- **SOCIAL**：Wikipedia
- **RAG**：Dify Extractor、NDJSON dump

### 市场展示板块

- **Partners**：由 Dify 合作伙伴验证的插件（认证徽章）
- **Top 20 Models**：安装量前 20 的模型插件
- **Search / Image & Video / Data**：按功能领域聚合
- **Featured**：精选插件
- **Latest**：最新发布

### 插件卡片信息结构

每个插件详情卡片包含：
- 类型标识（Tool / Model / Extension / Data Source）
- 插件名 + 作者（如 `by langgenius`、`by sawyer-shi`）
- 安装量（如 `275,672 installs`，公开透明）
- 简短描述
- 标签
- 详情页链接：`https://marketplace.dify.ai/plugin/{author}/{plugin_name}`

### 安装量 Top 数据（参考）

**模型类 Top 5**：
1. DeepSeek：1,236,142
2. Tongyi（通义）：1,176,061
3. Ollama：894,877
4. Volcengine Ark：817,528
5. OpenAI-API-compatible：817,183

**工具类 Top 5**：
1. Tavily：275,672
2. JSON Process：227,347
3. Jina AI：167,564
4. Firecrawl：164,809
5. MinerU：164,662

### 上架流程

Dify 提供 **3 种发布方式**，覆盖从官方市场到私有分发的不同场景：

#### 方式 1：Auto-publish PR（官方市场发布）
1. **准备插件包**：使用 CLI 打包，包含完整 `manifest.yaml`
2. **创建 Pull Request**：提交到 `dify-plugins` 仓库
3. **自动验证检查**（4 层）：
   - Manifest schema 验证
   - 代码安全扫描
   - 隐私合规检查
   - 签名验证（code signing）
4. **人工审核**：市场维护者手动审查
5. **合并与部署**：合并后自动部署到 marketplace

#### 方式 2：GitHub Release（个人仓库分发）
- 在自己的 GitHub 仓库标记 release
- 用户在 Dify 实例中输入仓库 URL 拉取安装
- 适合个人开发者、未通过官方审核的插件

#### 方式 3：File Release（私有分发）
- 将打包好的插件文件直接分发
- 用户在 Dify 中上传文件安装
- 适合企业内部分发、闭源插件

### 审核机制

#### 自动化验证（4 层检查）

| 检查项 | 说明 |
|--------|------|
| Manifest Schema 验证 | 确保描述符格式正确，必填字段齐全 |
| 代码安全扫描 | 检测潜在安全漏洞、恶意代码 |
| 隐私合规检查 | 验证数据处理符合隐私标准（数据透明、用户同意、最小化原则） |
| 签名验证 | 确认作者身份和代码完整性，防篡改 |

#### 人工审核
- 自动验证通过后，由市场维护者手动审查
- 审查维度：行为准则（专业沟通、尊重协作）、隐私保护、文档完整性、示例质量

#### 发布元数据要求
- 插件版本和变更日志（changelog）
- 兼容性要求（最低 Dify 平台版本）
- 依赖项和前提条件
- 安装说明
- 文档和示例

### 分发方式

Dify 的分发模式具有 **多层共存** 特点：

| 分发渠道 | 适用场景 | 特点 |
|----------|----------|------|
| **官方 Marketplace** | 公开插件 | 流量入口最大，自动更新，需通过审核 |
| **GitHub Release URL** | 个人/实验性插件 | 无需审核，用户主动输入 URL 安装 |
| **文件上传** | 私有/企业内 | 完全离线可用，无网络依赖 |
| **合作伙伴认证** | 企业级集成 | "Partners" 板块，有官方认证徽章 |
| **Bundles** | 多插件集合 | 一次安装多个兼容插件 |

### 安装体验

#### 路径一：Marketplace 一键安装
```
市场浏览/搜索 → 选择插件 → 查看详情 → 点击安装 → 自动下载与验证 → 安装到 Dify 实例
```

#### 路径二：GitHub URL 安装
```
获取插件仓库 URL → 在 Dify Plugin Management 中输入 URL → 拉取 release → 验证并安装
```

#### 路径三：文件上传安装
```
获取打包好的插件文件 → 在 Dify 中上传文件 → 验证签名 → 安装
```

#### 安装后配置
- **模型类插件**：需用户填写 API Key 等凭据（通过 `provider_credential_schema` 定义的表单）
- **预定义模型**：配一次凭据即可访问所有预定义模型
- **自定义模型**：每个模型实例需单独配置（如 Xinference 的 `model_uid`）
- **工具类插件**：通常开箱即用，部分需配置 OAuth 或 API Key

### 版本管理

- 遵循 **语义化版本**（MAJOR.MINOR.PATCH）
- manifest 中声明最低 Dify 平台版本
- minor 版本保持向后兼容
- major 版本需提供迁移指南
- 更新流程：递增版本 → 更新 changelog → 测试兼容性 → 发布 → 通知用户

---

## 插件系统架构（与 marketplace 紧密相关）

### 运行时隔离

Dify 插件在**沙盒执行环境**中运行，关键安全机制：

| 机制 | 说明 |
|------|------|
| Plugin Daemon | 运行在 `PLUGIN_DAEMON_PORT=5003`，管理插件生命周期 |
| Sandbox Execution | 受控运行时环境，权限显式授予 |
| Resource Limits | CPU、内存、网络约束 |
| API Rate Limiting | 反向调用限流 |
| Credential Encryption | API 密钥和机密信息安全存储 |

### Manifest 描述符

`manifest.yaml` 是插件的描述符，Dify 用它进行安装和执行：

```yaml
version: "0.0.1"
type: "tool" | "model" | "datasource" | "trigger" | "agent-strategy" | "endpoint"
author: "Plugin Author"
name: "plugin_name"
label:
  en_US: "Plugin Display Name"
  zh_Hans: "插件显示名称"
created_at: "2024-01-01T00:00:00.000000Z"
icon: "icon.svg"
description:
  en_US: "Description"
  zh_Hans: "描述"
resource:
  memory: 524288000
  permission:
    tool:
      enabled: true
    llm:
      enabled: true
    storage:
      enabled: true
```

### 高级特性

| 特性 | 说明 |
|------|------|
| **Plugin Bundles** | 多插件打包分发，确保版本兼容 |
| **反向调用（Reverse Invocation）** | 插件可回调 Dify 平台服务：App Invocation、Model Invocation、Tool Invocation、Node Invocation |
| **持久化存储** | KV 存储，支持 Plugin 级 / User 级 / Session 级三种范围 |
| **远程调试** | 本地开发插件，挂到远程 Dify 实例调试 |

---

## Admin 与 Workspace 边界

Dify 在插件管理上存在清晰的边界划分：

### 平台级（插件开发者 / Admin）
- 插件开发与发布（YAML 配置、Python 实现）
- 插件打包与分发（通过 marketplace 或私有渠道）
- 权限声明（在 manifest 中声明所需权限：Models、LLM、Storage 等）
- 模型定义（决定哪些预定义模型可用、模型 features、参数规则）

### Workspace / 用户级
- 填写供应商凭据表单（API Key 等认证信息）
- 添加和配置自定义模型（如 Xinference 的 model_uid）
- 在参数规则范围内调整模型参数（temperature、max_tokens）
- 选择和使用模型
- 在 workflow / agent 中使用已安装的工具插件

### 边界示意

```
┌─────────────────────────────────────────────────────┐
│  插件开发者 / 平台级                                  │
│  • 供应商和模型的定义与实现                            │
│  • YAML 配置（供应商信息、模型属性、参数规则）          │
│  • Python 代码（API 调用逻辑、凭据验证逻辑）           │
│  • 权限声明和插件打包发布                              │
├─────────────────────────────────────────────────────┤
│  工作区 / 用户级                                      │
│  • 填写凭据表单（API Key 等认证信息）                  │
│  • 添加和配置自定义模型                                │
│  • 在参数规则范围内调整模型参数                        │
│  • 选择和使用模型                                     │
└─────────────────────────────────────────────────────┘
```

### 模型供应商配置的两种方式

Dify 在模型配置上设计了两种模式，体现了平台与用户的分工：

| 配置方式 | 特点 | 用户操作 | 适用场景 |
|----------|------|----------|----------|
| **predefined-model** | 供应商预定义所有模型 | 只需配一次供应商 API Key | OpenAI、Anthropic 等封闭模型 |
| **customizable-model** | 用户可添加自定义模型 | 每个模型单独配置参数 | Xinference、Ollama 等自托管模型 |

两种方式可在单个供应商中**共存**。

---

## 与 Curis Admin Platform 的关系

### 可借鉴的设计

#### 1. Plugin-first 架构（强烈推荐）
- v1.0 起将所有核心能力（模型、工具）从主仓库剥离为插件
- 主平台只保留 runtime 和 marketplace 客户端
- **对 Curis 的启发**：Curis marketplace 应该从第一天就设计为 plugin-first，能力目录与平台核心解耦

#### 2. 多类型插件分类（强烈推荐）
- 6 类插件（Models、Tools、Data Sources、Triggers、Agent Strategies、Extensions）+ Bundles
- 每类有独立的 manifest schema 和权限模型
- **对 Curis 的启发**：Curis 能力目录可参考此分类，至少区分"模型能力"、"工具能力"、"数据源能力"、"集成扩展"几类

#### 3. 多层分发渠道（推荐）
- 官方 marketplace（带审核）
- GitHub Release URL（无审核，开发者自分发）
- 文件上传（私有/离线）
- **对 Curis 的启发**：企业内部能力市场需要支持"官方认证能力"、"团队自建能力"、"私有能力"三档分发

#### 4. 四层自动验证 + 人工审核（推荐）
- Manifest schema → 安全扫描 → 隐私合规 → 签名验证 → 人工审核
- **对 Curis 的启发**：Curis 能力上架应建立类似的流水线，特别强调"签名验证"和"隐私合规"两环

#### 5. Manifest 描述符（推荐）
- 用 YAML 声明插件元数据、权限需求、兼容性
- 平台根据 manifest 自动决定安装和执行策略
- **对 Curis 的启发**：每个 Curis 能力都应有标准化的 manifest，包含版本、权限、依赖、兼容性信息

#### 6. 沙盒执行 + 权限授予（强烈推荐）
- 插件在沙盒中运行，显式申请权限（tool、llm、storage）
- 资源限制（CPU、内存、网络）
- **对 Curis 的启发**：企业场景对安全要求更高，Curis 能力运行时必须沙盒化，权限最小化

#### 7. 安装量透明（参考）
- 每个插件公开展示安装量
- **对 Curis 的启发**：企业内部能力市场可展示"被多少团队使用"，作为能力可信度的信号

#### 8. 反向调用机制（参考）
- 插件可回调平台服务（App Invocation、Model Invocation）
- **对 Curis 的启发**：Curis 能力可能需要调用平台其他能力（如 RAG、模型），应设计安全的反向调用 API

#### 9. 合作伙伴认证体系（参考）
- Partners 板块，官方认证徽章
- **对 Curis 的启发**：企业内部可有"平台团队认证"、"安全团队认证"等质量标签

#### 10. 远程调试模式（参考）
- 开发者本地开发，挂到远程实例调试
- **对 Curis 的启发**：Curis 能力开发者应有类似的本地开发 + 远程调试体验

### 不应借鉴的设计

#### 1. marketplace 仅展示公开安装量，缺乏质量评分
- Dify marketplace 只有安装量，没有评分、评论、issue 反馈机制
- **对 Curis 的启发**：企业内部能力市场需要更丰富的质量信号（评分、问题反馈、SLA 指标）

#### 2. 审核标准文档不透明
- 4 层自动检查的具体规则、人工审核的标准未公开
- 开发者难以预判审核结果
- **对 Curis 的启发**：Curis 应公开能力上架的审核 checklist，让开发者自助预检

#### 3. 模型供应商配置门槛较高
- 需要写 Python 代码实现 `_invoke` 方法、错误映射、token 估算
- 对非开发者的能力上架不友好
- **对 Curis 的启发**：Curis 应提供低代码 / 配置化的能力上架方式，复杂能力才走代码路径

#### 4. Workspace 与 Admin 在"插件可见性控制"上文档不清晰
- 文档未明确说明 Admin 是否能控制哪些插件对特定 Workspace 可见
- 企业场景下，这种可见性控制是刚需
- **对 Curis 的启发**：Curis 应明确设计"能力可见性策略"（哪些部门可用、哪些环境可用）

#### 5. 缺少能力下架 / 弃用流程的清晰说明
- 文档重点在"上架"，对"下架"、"弃用"、"迁移"流程说明不足
- **对 Curis 的启发**：Curis 需要设计完整的能力生命周期：上架 → 迭代 → 弃用 → 下架 → 迁移

#### 6. 离线安装体验差
- 社区有大量"离线安装踩坑"博客，说明默认流程对内网/离线环境不友好
- 依赖 `uv` 而非 `pip`，需额外配置
- **对 Curis 的启发**：企业内网部署是 Curis 的核心场景，离线安装必须是一等公民

---

## 结论

### 对 Curis marketplace 的核心启发点

#### 启发 1：能力市场是平台核心，不是附属功能
Dify v1.0 将 marketplace 提升为核心架构，所有能力通过 marketplace 分发。Curis 应将能力市场作为 Admin Platform 的核心模块，而非后期补充。

#### 启发 2：plugin-first 架构是正确方向
主平台瘦身，能力外置为插件，带来：
- 主平台更易维护和升级
- 能力可独立迭代、独立版本化
- 第三方生态可自然生长

#### 启发 3：多类型分类 + 多渠道分发
- 类型分类：模型 / 工具 / 数据源 / 触发器 / Agent 策略 / 扩展 / 捆绑包
- 渠道分类：官方认证 / 个人发布 / 私有分发
- 两个维度交叉，覆盖从个人实验到企业生产的全场景

#### 启发 4：审核 = 自动验证 + 人工审查
- 自动化：schema、安全、隐私、签名四层
- 人工：行为准则、文档、示例
- 企业场景还可加入"安全合规审查"、"数据分类审查"

#### 启发 5：能力运行时必须沙盒化
- 沙盒执行 + 显式权限 + 资源限制
- 企业场景对安全的要求远高于开源社区
- 凭据加密存储、反向调用限流

#### 启发 6：Admin / Workspace 边界要清晰设计
- 平台级（Admin）：能力定义、发布、权限声明
- 工作区级（Workspace）：凭据配置、参数调整、能力使用
- **企业特有需求**：能力可见性策略（哪些部门/环境可用哪些能力）

#### 启发 7：manifest 是 marketplace 的契约
- 标准化的描述符文件
- 包含版本、权限、依赖、兼容性
- 平台和开发者之间的"接口契约"

#### 启发 8：完整的版本与生命周期管理
- 语义化版本
- 兼容性声明
- 变更日志
- **Curis 需补充**：下架流程、弃用预警、能力迁移指引

### 不适合 Curis 的部分

- **完全开放的第三方发布**：Curis 是企业内部平台，能力发布应受控，不能像 Dify 社区那样任意开发者发布
- **GitHub Release 作为分发渠道**：企业内部不应依赖外部 GitHub，应有内部代码仓库和分发通道
- **社区驱动的审核**：企业应有明确的审核团队和 SLA，而非依赖社区维护者

### 整体评价

Dify 的 marketplace 设计是当前开源 LLM 平台中**最成熟、最系统化**的之一。其 plugin-first 架构、6 类插件分类、四层自动验证、多渠道分发机制，都值得 Curis 深度参考。但其审核标准不透明、Workspace 可见性控制缺失、离线体验差等问题，是 Curis 需要避免的。

**推荐借鉴度：高（8/10）**
