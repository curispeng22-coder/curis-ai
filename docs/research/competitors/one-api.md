# One API 竞品档案

> 研究时间：2026-07-09
> 研究员：research-gateway
> 研究目的：为 Curis Admin Platform 模型网关设计提供轻量级备选方案参考

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **项目名** | One API（LLM API 管理 & 分发系统） |
| **GitHub URL** | https://github.com/songquanpeng/one-api |
| **作者** | songquanpeng |
| **开源协议** | MIT License（需在页面底部保留署名及指向本项目的链接） |
| **Star 数** | 约 20k+ 级别（具体需实时查询，是 LLM 网关领域 Star 数最高的项目之一） |
| **主语言** | Go（后端）+ JavaScript/React（前端） |
| **Commit 数** | 1,210 |
| **最新更新** | 2025-02-21（活跃度低于 fork 版 New API） |
| **Docker 镜像** | `justsong/one-api:latest` |
| **定位** | OpenAI 接口管理 & 分发系统，单可执行文件，开箱即用 |

### 与 New API 的关系

> **One API 是 New API 的上游原始项目，New API 是 One API 的 fork。**

| 维度 | One API | New API |
|------|---------|---------|
| **协议** | MIT（宽松） | AGPLv3（严格）+ 商业授权 |
| **活跃度** | 1,210 commits，2025-02 后更新放缓 | 6,083 commits，2026-07 仍高频更新 |
| **功能丰富度** | 基础完整 | 在 One API 基础上大幅增强 |
| **数据兼容** | 原始版本 | 完全兼容 One API 数据库 |
| **UI** | 经典界面 | 全新现代化 UI |
| **格式互转** | 不支持 | OpenAI ⇄ Claude ⇄ Gemini 互转 |
| **Reasoning Effort** | 不支持 | 支持 o3-mini/gpt-5 thinking 后缀 |
| **Realtime API** | 不支持 | 支持（含 Azure） |
| **Responses API** | 不支持 | 支持 |
| **支付系统** | 兑换码 + 充值链接 | 易支付 + Stripe + 兑换码 |
| **多语言** | 后端 i18n | 前端多语言（中/繁/英/法/日） |
| **性能分析** | 无 | Pyroscope 集成 |

---

## 核心功能

### 1. 统一 API 适配与中转（核心能力）

One API 的核心价值是**统一接口中继转发**：

```
用户 → 使用 One API 分发的 key 进行请求 → One API
  One API → 中继请求 → OpenAI
  One API → 中继请求 → Azure
  One API → 中继请求 → 其他 OpenAI API 格式下游渠道
  One API → 中继并修改请求体和返回体 → 非 OpenAI API 格式下游渠道
```

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **统一 OpenAI 格式入口** | 所有请求通过标准 OpenAI API 格式访问 | ⭐⭐⭐ Curis 网关元数据可统一格式 |
| **API Base 设置** | 用户将 API Base 设为 One API 部署地址 | ⭐⭐ |
| **模型映射** | 重定向用户请求的模型名称 | ⭐⭐⭐ Curis 模型别名可参考 |
| **stream 流式模式** | 支持流式传输打字机效果 | ⭐ |
| **绘图接口** | 支持绘图 API 中转 | ⭐ |
| **gzip 解码** | 支持 gzip decode | ⭐ |
| **中继超时** | `RELAY_TIMEOUT`（秒） | ⭐⭐ |
| **中继代理** | `RELAY_PROXY` 设置上游代理 | ⭐⭐ |
| **强制返回 usage** | `ENFORCE_INCLUDE_USAGE` 流式强制返回 | ⭐⭐⭐ Curis 计量可参考 |
| **用户内容下载代理** | `USER_CONTENT_REQUEST_TIMEOUT/PROXY` | ⭐ |

### 2. 渠道（Channel）管理

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **批量创建渠道** | 支持批量创建 | ⭐⭐ |
| **渠道分组** | 为不同分组设置不同倍率 | ⭐⭐⭐ |
| **模型列表设置** | 渠道可声明支持的模型列表 | ⭐⭐⭐ |
| **渠道余额定期更新** | `CHANNEL_UPDATE_FREQUENCY`（分钟） | ⭐⭐⭐ Curis 只读余额查询可参考 |
| **渠道可用性检查** | `CHANNEL_TEST_FREQUENCY`（分钟） | ⭐⭐⭐ Curis 健康检查可参考 |
| **负载均衡** | 多渠道负载均衡访问 | ⭐ Curis 不执行调用 |
| **失败自动重试** | 渠道请求失败自动重试 | ⭐ 同上 |
| **指定渠道** | 管理员令牌 `ONE_API_KEY-CHANNEL_ID` | ⭐ |
| **渠道代理设置** | 支持镜像和第三方代理 | ⭐⭐ |
| **自动禁用渠道** | `ENABLE_METRIC` 根据成功率自动禁用 | ⭐ |
| **Cloudflare AI Gateway** | 填写对应地址即可使用 | ⭐ |

### 3. 令牌（Token）管理

| 能力 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **过期时间** | 令牌过期设置 | ⭐⭐⭐ |
| **额度限制** | 令牌级额度（与账户额度分离） | ⭐⭐⭐ |
| **IP 范围限制** | 令牌级 IP 白名单 | ⭐⭐ |
| **模型访问控制** | 令牌级模型权限 | ⭐⭐⭐ Curis RBAC 可参考 |
| **指定渠道** | 管理员令牌追加渠道 ID | ⭐ |
| **初始 Root 令牌** | `INITIAL_ROOT_TOKEN` 自动创建 | ⭐⭐ |
| **系统管理令牌** | `INITIAL_ROOT_ACCESS_TOKEN` 自动创建 | ⭐⭐ |

### 4. 用户分组与额度体系

#### 额度计算公式

```
额度 = 分组倍率 × 模型倍率 × (提示 token 数 + 补全 token 数 × 补全倍率)
```

| 维度 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **用户分组** | 不同用户分组不同倍率 | ⭐⭐⭐ Curis 组织维度计量可参考 |
| **渠道分组** | 不同渠道分组不同倍率 | ⭐⭐⭐ Curis 网关维度计量可参考 |
| **模型倍率** | 按模型计费倍率 | ⭐⭐⭐ |
| **补全倍率** | 与 OpenAI 官方一致（如 GPT-3.5: 1.33，GPT-4: 2） | ⭐⭐⭐ |
| **双层额度** | 账户额度 + 令牌额度分离 | ⭐⭐⭐ |
| **美元额度显示** | 支持美元单位 | ⭐⭐ |
| **额度明细** | 支持查看额度使用明细 | ⭐⭐⭐ |
| **兑换码充值** | 批量生成/导出兑换码 | ⭐⭐ |
| **新用户初始额度** | 注册即赠 | ⭐ |
| **用户邀请奖励** | 邀请返额度 | ⭐ |

### 5. 支持的模型供应商（28+）

| 序号 | 供应商 | 备注 |
|------|--------|------|
| 1 | OpenAI ChatGPT | 支持 Azure OpenAI |
| 2 | Anthropic Claude | 支持 AWS Claude |
| 3 | Google PaLM2/Gemini | 支持 Gemini OpenAI 兼容 API |
| 4 | Mistral | |
| 5 | 字节跳动豆包 | 火山引擎 |
| 6 | 百度文心一言 | 支持 Baidu V2 |
| 7 | 阿里通义千问 | |
| 8 | 讯飞星火 | |
| 9 | 智谱 ChatGLM | |
| 10 | 360 智脑 | |
| 11 | 腾讯混元 | |
| 12 | Moonshot AI | |
| 13 | 百川大模型 | |
| 14 | MINIMAX | |
| 15 | Groq | |
| 16 | Ollama | 本地模型 |
| 17 | 零一万物 | |
| 18 | 阶步星辰 | |
| 19 | Coze | |
| 20 | Cohere | |
| 21 | DeepSeek | |
| 22 | Cloudflare Workers AI | |
| 23 | DeepL | 翻译服务 |
| 24 | together.ai | |
| 25 | novita.ai | |
| 26 | 硅基流动 SiliconCloud | |
| 27 | xAI | |
| 28 | OpenRouter | 支持余额更新 |

### 6. 其他功能

| 功能 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **多机部署** | 主从节点架构，共享数据库 | ⭐⭐⭐ |
| **管理 API** | 系统访问令牌调用管理 API | ⭐⭐⭐ Curis 集成可参考 |
| **Cloudflare Turnstile** | 人机校验 | ⭐ |
| **多种登录** | 邮箱/飞书/GitHub/微信公众号 | ⭐ |
| **主题切换** | `THEME` 环境变量 | ⭐ |
| **报警推送** | 配合 Message Pusher | ⭐⭐ |
| **后端 i18n** | 国际化支持 | ⭐⭐ |
| **自定义设置** | 系统名称/logo/页脚/首页/关于页 | ⭐ |
| **公告/充值链接** | 运营配置 | ⭐ |

---

## 架构特点

### 技术栈

| 层面 | 技术 |
|------|------|
| **后端语言** | Go |
| **前端** | React（JavaScript），支持多主题 |
| **数据库** | SQLite（默认）/ MySQL / PostgreSQL（适配中） |
| **缓存** | Redis（可选） |
| **容器化** | Docker / Docker Compose |
| **构建工具** | npm（前端），go build（后端） |

### 数据存储

| 数据库 | 说明 | Curis 借鉴价值 |
|--------|------|----------------|
| **SQLite** | 默认，无额外配置，适合小型部署 | ⭐⭐ |
| **MySQL** | `SQL_DSN` 配置，适合高并发 | ⭐⭐⭐ |
| **PostgreSQL** | "适配中，欢迎反馈"（未完全稳定） | ⭐⭐ |
| **独立日志库** | `LOG_SQL_DSN` 为 logs 表使用独立数据库 | ⭐⭐⭐ 日志分离设计 |
| **Redis** | `REDIS_CONN_STRING`，支持哨兵和集群 | ⭐⭐⭐ |
| **内存缓存** | `MEMORY_CACHE_ENABLED` | ⭐⭐ |

### 关键存储配置

```env
SQL_DSN=                          # 数据库连接
LOG_SQL_DSN=                      # 独立日志库
SQL_MAX_IDLE_CONNS=100            # 最大空闲连接
SQL_MAX_OPEN_CONNS=1000           # 最大打开连接
SQL_CONN_MAX_LIFETIME=60          # 连接生命周期（分钟）
SQLITE_BUSY_TIMEOUT=3000          # SQLite 锁等待（毫秒）
MEMORY_CACHE_ENABLED=             # 内存缓存
BATCH_UPDATE_ENABLED=             # 批量更新
BATCH_UPDATE_INTERVAL=5           # 批量更新间隔（秒）
REDIS_CONN_STRING=                # Redis 连接
SYNC_FREQUENCY=600                # 同步频率（秒）
```

### 部署模式

| 方式 | 说明 | Curis 借鉴价值 |
|------|------|----------------|
| **Docker 部署** | 单行命令，SQLite 或 MySQL | ⭐⭐⭐ |
| **Docker Compose** | 支持 MySQL 启动 | ⭐⭐⭐ |
| **宝塔面板** | 9.2.0+ 应用商店一键安装 | ⭐⭐ |
| **手动部署** | GitHub Releases 或源码编译 | ⭐⭐ |
| **多机部署** | 主从节点，共享数据库 | ⭐⭐⭐ |
| **第三方平台** | Sealos / Zeabur / Render | ⭐⭐ |
| **Nginx 反代** | 提供 Let's Encrypt HTTPS 参考 | ⭐⭐ |

### 多机部署要点

- 所有服务器 `SESSION_SECRET` 设置相同值
- 必须设置 `SQL_DSN`，使用 MySQL 数据库
- 从服务器设置 `NODE_TYPE=slave`
- 推荐设置 `SYNC_FREQUENCY` 并启用 Redis

### 单可执行文件优势

One API 的一个显著优势是**单可执行文件部署**：
- 后端 Go 编译为单一二进制
- 前端静态资源嵌入二进制
- 无外部依赖（SQLite 默认）
- 适合资源受限的轻量场景

---

## MIT 协议优势

### MIT 协议核心条款

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### 对 Curis 的具体优势

| 优势维度 | 说明 |
|----------|------|
| **可闭源商用** | Curis 可修改 One API 源码并闭源部署，无需开源衍生作品 |
| **无网络服务条款** | 不像 AGPLv3 那样要求"通过网络提供服务也必须开源" |
| **可集成进 Curis 产品** | 可作为 Curis 产品的子模块闭源分发 |
| **可修改不署名衍生**（除底部链接） | 仅需保留版权声明和底部链接 |
| **无商业授权费用** | 无需像 New API 那样购买商业授权 |
| **二次开发自由度高** | 可自由 fork 并定制为 Curis 专用 Adapter |

### 唯一义务

> 需在页面底部保留署名及指向 One API 项目的链接。

这一义务对 Curis 的影响极小，可在管理后台底部添加一个链接即可。

### 与 New API AGPLv3 的对比

| 维度 | One API (MIT) | New API (AGPLv3) |
|------|---------------|------------------|
| **闭源商用** | ✅ 允许 | ❌ 禁止（除非购买商业授权） |
| **修改后部署** | ✅ 无义务 | ❌ 必须开源 |
| **网络服务条款** | ✅ 无 | ❌ 有（AGPLv3 第 13 条） |
| **衍生作品传染** | ✅ 无 | ❌ 有 |
| **商业授权** | 不需要 | 需购买（support@quantumnous.com） |
| **集成进闭源产品** | ✅ 允许 | ❌ 禁止 |
| **Fork 定制** | ✅ 自由 | ❌ 受限 |

---

## 功能缺口（相对 New API）

One API 作为原始项目，功能较 New API 有以下缺口：

### 1. 格式互转能力缺失

| 能力 | One API | New API |
|------|---------|---------|
| OpenAI ⇄ Claude Messages | ❌ | ✅ |
| OpenAI → Gemini | ❌ | ✅ |
| Gemini → OpenAI | ❌ | ✅（仅文本，不支持函数调用） |
| Responses ⇄ Chat | ❌ | 🚧 开发中 |
| 思考转内容 | ❌ | ✅ |

**影响**：若 Curis 下游同时使用 OpenAI、Claude、Gemini 原生格式，One API 无法统一适配，需客户端自行转换。

### 2. 新型 API 缺失

| 能力 | One API | New API |
|------|---------|---------|
| OpenAI Responses API | ❌ | ✅ |
| OpenAI Realtime API | ❌ | ✅（含 Azure） |
| Reasoning Effort 后缀 | ❌ | ✅（o3-mini-high/medium/low 等） |
| Claude thinking 模式 | ❌ | ✅ |
| Gemini thinking 模式 | ❌ | ✅ |

**影响**：若 Curis 需要支持最新的推理模型能力，One API 无法提供。

### 3. 支付系统较弱

| 能力 | One API | New API |
|------|---------|---------|
| 易支付（EPay） | ❌ | ✅ |
| Stripe | ❌ | ✅ |
| 兑换码 | ✅ | ✅ |
| 充值链接 | ✅ | ✅ |

**影响**：若 Curis 需要在线支付能力，One API 不足（但 Curis Admin 定位为不执行调用，此缺口影响不大）。

### 4. 企业级能力缺失

| 能力 | One API | New API |
|------|---------|---------|
| OIDC 统一认证 | ❌ | ✅ |
| Discord/LinuxDO/Telegram 登录 | ❌ | ✅ |
| Pyroscope 性能分析 | ❌ | ✅ |
| 前端多语言 | ❌（仅后端 i18n） | ✅（中/繁/英/法/日） |
| 数据仪表盘 | 基础 | 可视化增强 |
| 配额饱和保护 | ❌ | ✅（int32 钳制） |
| 会话 Cookie 安全 | ❌ | ✅ |

### 5. 维护活跃度

| 指标 | One API | New API |
|------|---------|---------|
| Commit 数 | 1,210 | 6,083 |
| 最新更新 | 2025-02-21 | 2026-07-08 |
| 贡献者 | 较少 | 274 人 |
| 维护状态 | 放缓 | 高频活跃 |

**影响**：One API 维护放缓，新模型/新特性跟进可能滞后；New API 持续跟进最新模型。

---

## 适合作为轻量模型网关备选的原因

### 1. MIT 协议零合规风险

Curis 可以：
- 自由 Fork One API 源码
- 闭源修改为 Curis 专用 Adapter
- 集成进 Curis 闭源产品
- 无需购买商业授权
- 无需开源 Curis 业务代码

这是 One API 相对 New API 的**最大优势**。

### 2. 单可执行文件，部署极简

- Go 单二进制 + 嵌入前端
- SQLite 默认无外部依赖
- 适合资源受限的轻量场景
- Curis 可快速部署多个 One API 实例做隔离

### 3. 数据库兼容 New API

> One API 数据库可无缝迁移到 New API。

这意味着 Curis 可以：
- 先用 One API（MIT 协议）起步
- 业务增长后迁移到 New API（需处理 AGPLv3 合规）
- 数据无损迁移

### 4. 功能"刚好够用"

One API 虽然功能不如 New API 丰富，但核心能力（渠道管理、令牌管理、额度计费、负载均衡、失败重试）完整：
- 28+ 模型供应商
- 完整的渠道/令牌/用户分组体系
- 多机部署支持
- 管理 API 可供 Curis Admin 集成

### 5. 适合 Curis 的"只读计量 + 不执行调用"边界

One API 的功能集恰好覆盖"执行调用 + 在线计费"的下游 Adapter 职责，而不会与 Curis Admin 的"元数据 + 只读计量"职责过度重叠。

### 6. 可作为 New API 的降级方案

| 场景 | 推荐方案 |
|------|----------|
| 合规要求严格（不能接受 AGPLv3） | One API |
| 需要最新模型/格式互转 | New API（购买商业授权） |
| 资源受限轻量部署 | One API |
| 企业级生产 + 多支付渠道 | New API（购买商业授权） |
| 快速 PoC / 原型验证 | One API |

---

## 与 Curis Admin Platform 的关系

### 可借鉴的设计

#### 1. 渠道元数据模型（⭐⭐⭐）

与 New API 一致（New API 继承自 One API），One API 的渠道表结构是 Curis `model_gateways` 的设计原型：
- 渠道名称、类型、BaseURL
- 支持的模型列表
- 分组归属
- 倍率配置
- 健康检查频率（`CHANNEL_TEST_FREQUENCY`）
- 余额查询频率（`CHANNEL_UPDATE_FREQUENCY`）

#### 2. 双层额度体系（⭐⭐⭐）

"账户额度 + 令牌额度"分离的设计适合 Curis 的预算控制：
- 组织/团队级总预算
- 项目/应用级令牌预算
- 二者独立管理

#### 3. 多维倍率计量（⭐⭐⭐）

```
额度 = 分组倍率 × 模型倍率 × (提示 token + 补全 token × 补全倍率)
```

这一公式可直接用于 Curis 的只读计量计算。

#### 4. 独立日志库（⭐⭐⭐）

`LOG_SQL_DSN` 为 logs 表使用独立数据库，适合 Curis 高频计量日志的隔离。

#### 5. 批量更新优化（⭐⭐⭐）

`BATCH_UPDATE_ENABLED` + `BATCH_UPDATE_INTERVAL` 的批量聚合写入设计。

#### 6. 管理 API 设计（⭐⭐⭐）

One API 提供系统访问令牌调用管理 API，Curis Admin 可通过此 API 集成 One API：
- 渠道管理 API
- 令牌管理 API
- 日志查询 API
- 额度查询 API

#### 7. 多机部署架构（⭐⭐⭐）

主从节点 + 共享数据库 + Redis 缓存的架构适合 Curis 的高可用部署。

### 不应借鉴的设计

#### 1. 执行调用能力（❌）

同 New API，One API 的核心是中继转发执行调用，Curis Admin 不应执行调用。

#### 2. 在线注册与支付（❌）

One API 内置用户注册、兑换码、充值链接等，Curis Admin 应走企业 SSO + 独立计费。

#### 3. 前端可视化过度集成（⚠️）

One API 把管理界面内置，Curis Admin 可考虑前后端分离 + 独立 BI。

#### 4. PostgreSQL 适配不成熟（⚠️）

One API 的 PostgreSQL 支持标注"适配中，欢迎反馈"，若 Curis 主选 PostgreSQL，需充分测试或选择 MySQL。

### 协议风险

#### MIT 协议风险（极低）

| 风险场景 | 风险等级 | 说明 |
|----------|----------|------|
| Fork 并闭源修改 | 🟢 低 | MIT 允许 |
| 集成进 Curis 闭源产品 | 🟢 低 | MIT 允许 |
| 修改后部署为 SaaS | 🟢 低 | MIT 无网络服务条款 |
| 分发 Curis 产品含 One API | 🟢 低 | 仅需保留版权声明 |
| 移除底部链接 | 🟡 中 | 协议要求保留，但可协商 |

**结论**：One API 的 MIT 协议对 Curis 几乎零风险。

---

## 结论

### 适合 Curis 的定位：**轻量级模型网关 Adapter 备选方案**

One API 在 Curis 架构中的角色：

```
Curis Admin Platform（元数据 + 只读计量）
        ↓ API 调用（渠道管理、日志查询）
        ↓
One API（轻量 Adapter，MIT 协议，可闭源定制）  ←  备选方案
        ↓
上游模型供应商
```

#### 推荐策略

1. **作为 New API 的合规降级方案**：当 Curis 无法接受 AGPLv3 时，One API 是首选
2. **可自由 Fork 定制**：MIT 协议允许 Curis 闭源修改 One API 为专用 Adapter
3. **适合 PoC 与轻量场景**：单可执行文件，部署极简
4. **数据库可迁移**：业务增长后可无缝迁移到 New API（需处理合规）
5. **功能缺口需评估**：若 Curis 需要最新模型/格式互转，One API 不足

#### 不适合作为 Curis Admin 本体

同 New API，One API 的"执行调用 + 在线计费 + 用户注册"全栈设计与 Curis Admin "只读计量 + 不执行调用"定位冲突。

#### 与 New API 的协同建议

| 场景 | 选择 | 理由 |
|------|------|------|
| Curis Admin 主网关 Adapter | New API（购买商业授权） | 功能完整，活跃维护 |
| 合规敏感场景 | One API | MIT 协议零风险 |
| PoC / 开发测试 | One API | 部署极简 |
| 需要闭源定制 | One API | MIT 允许闭源 fork |
| 需要最新推理模型 | New API | One API 不支持 Reasoning Effort |

#### 建议的集成边界

与 New API 一致：

| Curis Admin 职责 | One API 职责 |
|------------------|--------------|
| 网关元数据定义 | 执行调用 |
| 只读计量数据汇总 | 在线计费扣减 |
| 组织/团队/项目层级 | 令牌/用户管理 |
| RBAC 权限 | 渠道路由 |
| 审计合规 | 请求日志 |
| 财务账单 | 兑换码/充值 |
| SSO 身份管理 | OAuth 登录 |

#### 总体评价

One API 是 Curis 模型网关 Adapter 的**合规友好型备选方案**。其 MIT 协议、单可执行文件、数据库兼容 New API 三大优势，使其在合规敏感、轻量部署、快速验证场景下优于 New API。但功能缺口（格式互转、Reasoning Effort、Realtime API）和维护放缓是主要短板，需根据 Curis 实际需求权衡。
