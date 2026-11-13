# Curis · AiToEarn 架构复盘

> **状态**：CONTENT × CHANNEL ARCHITECTURE REVIEW REQUIRED
> **类型**：Reference Only · 参考实现复盘（F 节，非接入决策）
> **源**：https://github.com/yikart/AiToEarn （MIT License，2,616 commits，最新 2026-07-30 `hide Douyin channel integration`）
> **配套**：`Curis_Content_Production_Channel_Operations_Model.md`、`Curis_Multi_Channel_Architecture_Review.md`

> **本轮不是决定直接接入 AiToEarn。** 仅研究其架构思想，为本轮「Content × Channel 分离」提供外部参照。

---

## 1. AiToEarn 概览

- **定位**：`OPC（一人公司）的 AI 内容营销智能体`；口号 `Monetize · Publish · Engage · Create —— 一站式平台`。
- **支持渠道（14+）**：抖音、小红书、快手、B站、视频号、TikTok、YouTube、Facebook、Instagram、Threads、X、Pinterest、LinkedIn、微信公众号。
- **四大 Agent 能力**：
  - 💰 **Monetize**（商家推广任务，CPS/CPE/CPM 结算）
  - 📢 **Publish**（一键分发 10+ 平台 + 日历排期）
  - 💬 **Engage**（浏览器插件自动点赞/收藏/关注、AI 回复、评论挖掘、品牌监测）
  - 🎨 **Create**（视频/图文自动生成，批量铺量）
- **使用方式**：网站 / OpenClaw 插件 / MCP 接入（Claude/Cursor）/ Docker / 源码。

---

## 2. 逐能力拆解（对应本轮关注点）

| 关注点 | AiToEarn 实现 | 备注 |
|---|---|---|
| **多平台账号模型** | OAuth 登录各社媒账号；Relay 中转借用 aitoearn.ai 凭据，用户免自申开发者账号 | Relay 抽象是亮点，但 Curis 不应做凭据代理 |
| **OAuth / Account Binding** | `Server → Relay 中转` 统一 OAuth；中国版 `aitoearn.cn` / 国际版 `aitoearn.ai` Key（不匹配 401） | 渠道配置化、可隐藏（`hide Douyin channel`） |
| **Content / Post 对象** | README 未披露 Schema；仅从功能推断（草稿含参考图/视频、目标平台限制、文案提示词） | **缺数据契约**——Curis 必须自有明确对象模型（见数据模型文档） |
| **Platform Adapter** | 服务端适配层 + Relay 配置；非代码级公开接口 | 配置驱动，渠道可增删 |
| **一键多平台发布** | Publish Agent 选平台 / 日历排期 → 调各平台 OAuth → 一键分发 | 与 Curis「1 Content → N Variant → N Publication」同向 |
| **Platform-specific metadata** | 草稿支持「目标平台限制」「文案提示词」 | 弱：未见到逐字段映射（ratio/duration/copyright…） |
| **Publish status / receipt** | 未描述 pending/success/fail、receipt ID、webhook | **缺发布回执模型**——Curis 必须自有 Publication.receipt |
| **Scheduling** | 日历排期统一规划各平台发布时间 | 隐含任务状态，但未展开实现 |
| **Engagement** | 浏览器插件自动点赞/收藏/关注 + AI 回复 + 评论挖掘 + 品牌监测 | ⚠️ 浏览器插件自动化互动，**触碰平台「AI托管/自动化互动」封禁风险** |
| **Analytics** | 未提及看板/导出；CPS/CPE/CPM 结算隐含效果统计 | **缺 Analytics 架构** |
| **Connector abstraction** | MCP 统一端点 + OpenClaw 插件 CLI；Relay 抽象分离 `Server Relay`(发布/OAuth) 与 `AI Relay`(模型) | ✅ 连接器抽象思想可借鉴 |

---

## 3. 技术栈 / 许可证

- **Monorepo**：Nx；`apps/aitoearn-ai` + `apps/aitoearn-server`；配置 `config.yaml` / `local.config.yaml`。
- **前端**：`aitoearn-web`（pnpm）；桌面 `AttAiToEarn`（Electron + better-sqlite3）。
- **数据/缓存**：MongoDB、Redis（Docker 或自指向）。
- **运行**：Node.JS 20.18.x；Docker / `docker-compose.yml`。
- **许可证**：**MIT**（代码可复用，若许可允许 —— 但本轮不决定接入，仅参考）。

---

## 4. 复用评估

### ✅ 值得复用的架构思想
1. **四 Agent 能力域分离**（Monetize / Publish / Engage / Create）对应 Curis 的能力分层 —— 尤其 Publish（分发）与 Create（生产）的分离，与本轮「Content × Channel」拆分**同构**。
2. **Relay OAuth 抽象**：用户免自申开发者账号即可授权多平台 —— 解决「每平台自申开发者门槛高」的痛点（Douyin Research C 节打通条件痛点）。
3. **统一 MCP 端点 + 日历排期跨平台**：连接器抽象与跨平台排期的 UX 参考。
4. **渠道配置化可隐藏**：`hide Douyin channel` 证明渠道是插件式，可增删。

### 📦 可直接复用代码/协议（MIT 允许，需法律/安全复核）
- MIT 许可证下，Nx monorepo 结构、MCP 端点协议、Relay 抽象、配置驱动渠道可作为**参考实现基线**。
- **本轮不决定接入**，仅记录「若未来需要，MIT 允许参考其连接器/MCP 抽象」。

### ❌ 不应继承的产品模型
1. **Content 与 Channel 混淆**：AiToEarn 是「创作+分发」单一工具，未做 Canonical Content → Channel Variant → Publication 的干净分离。Curis 必须自有该分离。
2. **Create Agent 批量铺量视频/图文自动化**：生产侧「批量铺量」与 Curis「全自动任务流 + 质量门禁」取向不同，且易触发平台反垃圾。
3. **浏览器插件自动点赞/关注/收藏的互动自动化**：属于「自动化互动」，直接触碰抖音「AI托管类账号」封禁与平台反滥用政策（见 Douyin Research，本轮已降级为待验证，但风险信号明确）。
4. **Relay 凭据代理模型**：让用户社媒凭据经第三方 Relay 中转 —— 与 Curis「用户自用凭据、密钥不落盘、不代管」的安全/责任模型冲突（`working_memory` §13）。

### 🏗️ Curis 应自有的部分
- 干净的 **Canonical Content → Channel Variant → Publication** 分离（数据模型文档）。
- **Professional Workspace + Employee Responsibility + Capability Provider** 架构。
- **AI 披露 / 政策合规层**（各平台 disclosure 字典由政策层维护）。
- **Human-in-loop 审核门禁**（Frozen P7 CEO Decision Package）—— 不依赖浏览器插件绕过平台审核。
- **Target Channels 前置 → Production Requirements** 契约（连接 Production 与 Channel Ops）。

---

## 5. 定位判断（核心问题）

> **AiToEarn 在 Curis 中最合适的定位是什么？**

| 候选定位 | 判定 |
|---|---|
| Channel Operations Capability Provider（直接接入） | ❌ 否 —— content+channel 混淆、浏览器插件互动自动化风险、Relay 凭据代理不合安全模型 |
| Multi-platform Distribution Provider（分发能力参考） | ⚠️ 次选 —— 其「一键多平台 + 日历排期」UX 可作 Douyin/XHS/... Channel Ops WS 的设计灵感 |
| **Reference Implementation（参考实现）** | ✅ **主选** —— MIT 许可下，其多平台分发 UX、Relay OAuth 模式、MCP 连接器抽象、配置化渠道，均可作为 Curis 自研架构的外部基线对照 |
| 其他 | 可作为「市场竞品 / 参考实现」基线，用以凸显 Curis「Content×Channel 干净分离 + 合规门禁」的架构优势 |

**结论**：AiToEarn 是**优秀的参考实现与分发 UX 灵感来源**，但因其产品模型混淆与自动化互动风险，**不应作为直接接入的 Channel Operations Capability Provider**。Curis 应基于自有干净分离架构自研，仅在 MIT 许可范围内参考其连接器/MCP/Relay 抽象。

---

## 6. 与本轮架构的对接

- AiToEarn 的 **Publish/Create 分离** ⇔ 本轮 **Channel Operations / Video Production 分离**（同向印证）。
- AiToEarn 的 **缺失**（Content Schema、Publish receipt、Analytics 架构）⇔ 本轮**必须自建**的部分（数据模型文档 §6–§9）。
- AiToEarn 的 **Relay OAuth** ⇔ 可参考用于降低 Douyin Research C 节「开发者账号/OAuth 打通门槛」，但须重写为「用户自有凭据 + Curis 不自代理」的安全形态。

---
*参考实现复盘，非接入决策。MIT 许可下可参考其架构，但 Curis 应基于自有 Content×Channel 分离模型自研。*
