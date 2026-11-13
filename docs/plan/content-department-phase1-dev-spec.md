# 内容部门 Phase 1 开发规格 · 执行层（AiToEarn 地基 + social-auto-upload 发布）

> **文档性质**：开发团队可直接执行的 Phase 1 技术规格（非战略文档）。
> **战略依据**：`docs/research/aiearn-content-marketing-final-decision.md`（§7 方向①「以 MIT 代码为底座自建」+ §11「social-auto-upload 选型」）、`docs/product/federated-agent-os.md`、`docs/product/ai-content-publish-package.md`、`docs/research/platform-api-qualification-tracker.md`。
> **授权**：总控 2026-07-13 拍板——「第一阶段工作流产出复用 AiToEarn 地基，发布走 social-auto-upload」。
> **边界**：零代码改动既有的 L2 冻结项（Monetize / 市场 / 计费 / 外部 Agent 生态）；本规格仅描述 Phase 1 执行层自建，不触 Relay ToS。

---

## 0. 范围一句话

**Phase 1 把内容部门的「生产」与「发布」两端都做成自动化，且全部基于 MIT 代码自托管：**

- **生产端（生成 / 策划 / 脚本 / 分析）** = 自托管 **AiToEarn 的 MIT 代码** 作为地基（改造为 Curis 内部服务，界面换 Curis 品牌，AI 走我们自己的 key）。
- **发布端（真实发到平台）** = 自托管 **social-auto-upload（MIT，patchright）**，租户经它连自己的平台账号。
- **两端都绝不碰 AiToEarn 的 Relay / 在线服务** —— 零 aitoearn 服务费、零双付费、无 ToS 违约。

> 注：此前研究阶段把 Phase 1 框为「方向③ 仅产出、租户手动发」。本规格在总控拍板下把**自动发布（social-auto-upload）并进 Phase 1**；发布包 schema 的手动导出（Markdown / 逐平台 Clipboard）仍保留为兜底能力。

---

## 1. 范围边界

### 1.1 做（Phase 1）
- 自托管 AiToEarn MIT 代码，作为内容生成 / 策划的生产地基（内部服务）。
- 自托管 social-auto-upload，作为发布执行端。
- Curis 工作流编排：调生产地基产出内容 → 套用发布包 schema → 调 social-auto-upload 发布。
- 发布包 schema（已定义）作为两段之间的契约。
- 租户平台账号以 cookie（Phase 1）/ 未来自有 OAuth（后续阶段）接入。

### 1.2 不做（Phase 1 明确排除）
- ❌ AiToEarn **Relay** / 任何 aitoearn 在线服务（ToS §5.1 禁转授权，白标违法）。
- ❌ **Monetize**（变现 / 结算）—— 触 L2 ①②④，另行 gate。
- ❌ 白标第三方 Relay 给租户。
- ❌ 各平台原生 OAuth App 注册（Phase 1 走 social-auto-upload cookie；原生 API 替换见追踪表，归后续阶段）。
- ❌ 市场 / 计费 / 外部 Agent 生态。

---

## 2. 架构总览

```
┌──────────────────────────────────────────────────────┐
│ Curis OS（编排中枢）                                    │
│  - 内容部门 Workflow（wl_ai_content_*）                  │
│  - 发布包 schema（契约，已定义）                         │
│  - Credential Vault（租户 cookie / 我们自有 AI key）     │
└───────────┬───────────────────────────────┬────────────┘
            │ ① 生成 / 策划请求             │ ③ 发布请求（发布包）
            ▼                               ▼
┌────────────────────────┐      ┌─────────────────────────────┐
│ AiToEarn MIT（自托管）    │      │ social-auto-upload MIT        │
│ 生产地基（内部服务）      │      │ 发布执行端（内部服务）         │
│ - Create 生成             │      │ - patchright 浏览器自动化      │
│ - Publish 规划 / 排期     │      │ - cookie 登录各平台            │
│ - Engage 分析             │      │ - 覆盖 抖音/小红书/视频号/…    │
│ AI key = 我们自有         │      └─────────────┬───────────────┘
└────────────────────────┘                    │ ④ 真实发布
                                             ▼
                                   平台（抖音/小红书/视频号/B站/…）
```

- 两段都是**独立自托管服务**，Curis 经内网 API 调用，不依赖任何第三方 SaaS。
- 账号绑定步：租户在 social-auto-upload 侧连自己平台 cookie（法律要求的最小感知，不可避免）。

---

## 3. 组件 A：AiToEarn MIT 自托管（生产地基）

- **来源**：`https://github.com/yikart/AiToEarn`（MIT，2026-05 v2.4，~18.8k★）。
- **部署**：`docker compose up -d`（Nginx + Web + Server + AI + Mongo + Redis + RustFS）。
- **改造点（地基 → Curis 内部服务）**：
  1. 前端界面换 Curis 品牌（去除 aitoearn 标识）。
  2. **AI 模型 key 填我们自己的**（Docker 文档确认 `AI → 模型服务商` 可配 OpenAI / Gemini / Anthropic）。
  3. **禁用 Relay**：部署时不配置 Relay，发布 / 互动 / 数据不走 aitoearn.ai。
  4. 仅向 Curis 编排层暴露内部生成 / 策划 API；不向租户暴露其 Web。
- **Curis 调用方式（推荐）**：把 AiToEarn 当作内部微服务，Curis 工作流在「生成」步调用其 Create / Publish-planning 内部端点，拿回结构化结果 → 套发布包 schema。
  - 备选（成本更高，Phase 1 不采）：从 AiToEarn 抽取生成模块直接嵌入 Curis 运行时。
- **复用边界**：只用其 **Create（生成）/ Publish（规划排期，非真实发）/ Engage（分析）** 能力；**真实发布交给组件 B**。

---

## 4. 组件 B：social-auto-upload 自托管（发布执行端）

- **来源**：`https://github.com/dreammis/social-auto-upload`（MIT，Python + patchright 反检测分支）。
- **部署**：headless 服务模式（服务端 / agent 友好），Docker 支持。
- **集成**：
  1. Curis 在「发布」步把 **发布包（publish-package）** 传给 social-auto-upload connector。
  2. connector 调 `sau <platform> login --account <name>`（cookie 来自 Vault）完成账号绑定。
  3. 调各平台发布命令，把发布包内容发到对应平台。
- **平台覆盖**：抖音 / 小红书 / 微信视频号 / Bilibili / 快手 / 百家号 / TikTok / YouTube。
- **Phase 1 角色**：它是 Phase 1 的**唯一发布通道**（替代被否决的 Relay），覆盖含无 API 平台（小红书 / 视频号）在内的全部目标平台。

---

## 5. 发布包 Schema（集成契约）

- 完整定义见 `docs/product/ai-content-publish-package.md`。
- **它是两段之间的唯一契约**：AiToEarn 生产地基产出 → 规范为 publish-package → social-auto-upload connector 消费。
- 开发必须让两段都对齐该 schema，保证未来切换执行端（如某平台获批原生 API 后换分支 A）**只改 connector、不动工作流**。

---

## 6. 凭据与 Vault（L2 #5）

- **租户平台 cookie**：存 Credential Vault，加密、按租户隔离；social-auto-upload 发布时按需取用。
- **AI 模型 key**：我们自有，存 Vault（非租户凭证）。
- **Gate 提示**：当未来注册 Curis 自有平台 OAuth App、把 `client_secret` 存 Vault 时，触发 **L2 #5（安全边界席）**——届时已无 Relay 灰区，属合法自有资产。

---

## 7. 分阶段任务分解（开发团队可执行）

### 7.1 团队归属原则
本规格跨 **Admin（资产工厂）** 与 **Workspace（运行时）** 两条线，遵循产品原则「Admin 提供资产、Workspace 运行」。

**资产 vs 运行时（写给两个团队看的边界）**：内容增长部门包（`ccp_ai_content_company` / `dt_content_ops`）是一个**完整的 Admin 资产** —— 既覆盖内容生成工作流，也覆盖全平台发布动作。租户未来商业化时订阅的正是这个完整包。但「整包是 Admin 资产」要拆成两层看：
- **Admin 拥有包的「定义（蓝图）」**：工作流模板（**含生成节点与发布步骤节点**）、技能目录、工具/连接器**规格**（WHAT + 接口 + 发布包 schema）、部门模板、品牌声音、看板。发布动作是包里的一环，不是 Workspace 另起的产品。
- **Workspace 拥有包的「运行实例（执行）」**：真跑起来的 AiToEarn 服务、social-auto-upload 服务、连接器**实现代码**、租户 cookie 进 Vault、监控告警。这些是运行态、有状态的。

> 口诀：**整包定义归 Admin、整包运行归 Workspace**。不是「生成=Admin、发布=Workspace」。租户订阅 Admin 的包，Workspace 把订阅的包实例化并执行。包 = 资产；跑包 = 运行时。
> ⚠️ 红线：Admin 拥有包定义 **≠** Admin 运行包（会撞「Admin 不管理用户实例」）。Admin 打包、Workspace 跑。

- **Admin 团队** 交付：内容部门资产**定义** —— `wl_ai_content_*` 工作流模板（含发布步骤节点）、`skl_ai_content_*` 技能目录、`tl_ai_content_*` 工具/连接器规格（含 social-auto-upload connector 规格）、发布包 schema 契约、部门模板（属 Workflow Template / Skill Catalog / Tool Catalog / Department Template / Template 资产）。
- **Workspace 团队** 交付：包的**运行时执行** —— 自托管服务、connector 实现、Credential Vault 集成、工作流编排串联、监控告警。
- **接口契约**：发布包 schema（`docs/product/ai-content-publish-package.md`）是两队唯一对接面。Admin 定义结构，Workspace 消费并序列化；切换执行端（如未来某平台获批原生 API 走分支 A）仅 Workspace 改 connector，Admin 资产与工作流不动。
- **Git 基线纪律**：Admin 改动只进 `admin-platform/` 与 Admin 范围；Workspace 改动只进 `workspace/`、`backend/app/`、`frontend/app/`；跨线变更先开 shared contract，禁直接改对方执行链。

### 7.2 任务分解（标注归属团队）

| # | 任务 | 产出 | 归属团队 | 依赖 |
|---|------|------|----------|------|
| **T0** | **Admin 交付含发布步骤的完整部门包**：工作流模板(`wl_ai_content_*`，含生成节点+发布节点) + 技能目录(`skl_ai_content_*`) + 工具/连接器规格(`tl_ai_content_*`，含 social-auto-upload connector 规格) + 发布包 schema 契约 + 部门模板(`dt_content_ops`) | 完整包资产就绪（Workspace 前置契约） | **Admin** | — |
| T1 | 自托管 AiToEarn MIT：`docker compose` 部署 + 去品牌 + 配自有 AI key + 禁 Relay | 内部生成服务可用 | Workspace | — |
| T2 | 暴露 AiToEarn 内部生成 API 给 Curis 编排层（或抽模块） | 生成端点 | Workspace | T1 |
| T3 | 自托管 social-auto-upload：headless 服务 + Docker | 发布服务可用 | Workspace | — |
| T4 | 发布包 schema 校验 + 序列化（Curis 侧） | schema 落地 | **Admin 定义 / Workspace 实现** | T0 |
| T5 | social-auto-upload connector：发布包 → `sau` 调用 + cookie 取自 Vault | 发布打通 | Workspace | T3, T4 |
| T6 | 内容工作流串联：生成(AiToEarn) → 发布包 → 发布(social-auto-upload) | 端到端跑通 | **Admin 资产 / Workspace 运行时** | T2, T5, T0 |
| T7 | 租户 cookie 接入 UI + Vault 加密隔离 | 多租户账号绑定 | Workspace | T5 |
| T8 | 监控 / 告警：服务存活、发布成功率、封号预警 | 可观测 | Workspace（DevOps） | T1, T3, T6 |

### 7.3 前置顺序（关键）
1. **Admin 先交付 T0**（资产前置）：落地**含发布步骤的完整部门包**（工作流模板含发布节点 + 技能目录 + 连接器规格 + 发布包 schema + 部门模板），作为 Workspace 的契约输入。
2. **Workspace 再执行** T1–T8 运行时实现；T4、T6 在 T0 资产到位后才可联调。
3. 执行落地（自托管 social-auto-upload、Vault 存租户 cookie）触发 **L2 #5 安全边界席**，届时确认边界干净。

---

## 8. 关键风险与对策

| 风险 | 对策 |
|------|------|
| AiToEarn 全栈较重，自托管运维成本 | Phase 1 仅用其生成 / 规划能力，可后续抽模块瘦身 |
| social-auto-upload 反爬 / 封号 | 账号隔离、限流、UI 变更监控、cookie 加密；无 API 平台本就长期走此路径 |
| 平台 UI 变更致脚本脆弱 | 监控 + 快速修；有 API 平台后续替换分支 A 收敛风险 |
| 租户 cookie 安全 | Vault 加密 + 隔离 + 轮换 |

---

## 9. 关联文档

- 战略决策：`docs/research/aiearn-content-marketing-final-decision.md`
- 架构原则（编排中枢 + 可插拔执行端）：`docs/product/federated-agent-os.md`
- 发布包 schema：`docs/product/ai-content-publish-package.md`
- 平台资质追踪：`docs/research/platform-api-qualification-tracker.md`
- 工作流规划：`docs/plan/workflow-official-content-plan.md`

---

*—— 内容部门 Phase 1 开发规格（执行层自建，MIT 自托管，零 Relay）。DevOps Automator · 2026-07-13。*
