# AiToEarn 复用 · 最终决策文档（内容营销部门一站式集成）

> **整合自**：`aiearn-content-marketing-reuse-plan.md`（总览规划）+ `aiearn-asset-mapping.md`（精确映射）+ 三轮问答（用户流程 / 部署决策 / 多租户矛盾）+ 用户授权截图实测（API Keys 页 + 开放平台页）。
> **研究日期**：2026-07-12 ｜ **研究人**：DevOps Automator（一键达）
> **性质**：纯研究 / 决策文档（零代码、零提交、不 patch 任何契约）
> **对象**：https://github.com/yikart/AiToEarn（MIT，约 18.8k★，2026-05 v2.4）

---

## 0. 结论摘要（三段式 · 战略终版 2026-07-12 21:43）

> **修订记录**：
> - 20:41 总控裁定放弃 wrap 路径，改走方向③（只产出 MVP）；AiToEarn 降级为能力参照。
> - 21:01 查定价：按量积分制，社交动作极便宜，COGS 内化模型成立（但成本是「可变积分池」非固定买断）。
> - 21:43 查 LICENSE + ToS：MIT 代码可白标（含"出售"权），但 Relay/在线服务受 ToS §5.1 约束（non-sublicensable）→ **Relay 白标转售违法**。终局=用 MIT 代码、不用其服务。

**结论（终版）**：AiToEarn 的 **GitHub 代码为 MIT（LICENSE 含"商业使用/分发/修改/出售"权）→ 可自托管、改 Curis 界面、当自有功能白标售卖，完全合法**；但其 **在线服务（Relay/API）受 ToS §5.1 约束：`solely for your` + `non-sublicensable` → 禁止转授权给第三方 / 白标转售**。因此**不能把 Relay 借给租户当静默后端**（原 COGS 内化模型法律上不通）。合规且最优解 = **自托管 MIT 代码为执行引擎底座 + AI 用我们自有 key + 发布/互动/数据不接 Relay、改为注册 Curis 自有平台开发者账号(OAuth App) + 租户经 Curis 的 app 授权连自己社交号**。结果：**白标 100% 干净、零 aitoearn 服务费（双付费彻底消失）、无供应依赖、仅受 MIT 约束（从不点接受 ToS 即不绑）**。

**原因**：ToS 管"在线服务"、MIT 管"GitHub 代码"——**两层分离**。Relay 白标被否，但反而逼出比 COGS 内化更优的路径：完全不依赖 aitoearn 的服务，只用其开源代码作起点，执行层资产 100% 归我。唯一真难题（各平台开发者账号注册+过审，国内审核严）合法且归我方掌控，正是 Relay 曾想绕过的坎现在自己迈。

**建议（终版）**：① 阶段1 仍先做方向③验证产出/编排价值（零风险、零依赖）；② 执行层终态锁定「**自建（以 AiToEarn MIT 代码为底座改造）**」——自托管 Docker、界面换 Curis 品牌、AI 接自有 key、注册 Curis 自有平台 OAuth App、租户连自己社交号；③ Monetize 仍走 L2 Gate（①②④）；平台账号注册是合法合规工作、不触 Relay 灰区、不触发原 Relay ToS 风险。

---

## 1. 研究对象

- **定位**：Monetize · Publish · Engage · Create 一站式 AI 内容营销平台，帮 OPC/创作者/品牌在全球平台构建→分发→变现。
- **四大 Agent**：Create(多模态生成) / Publish(14+ 平台一键分发+排期) / Engage(互动+评论挖掘+品牌监测) / Monetize(CPS/CPE/CPM 结算市场)。
- **技术**：Nx monorepo + MongoDB + Redis + Docker Compose；Electron 桌面端。
- **集成点（复用关键）**：
  - **MCP 协议**：`https://aitoearn.ai/api/unified/mcp`（国际）/ `aitoearn.cn/api/unified/mcp`（国内），Header `x-api-key` → 可作外部 Connector/Skill 接入，**无需 fork**。
  - **OpenClaw 插件**：`npx -y @aitoearn/openclaw-plugin-cli`。
  - **Docker 私有部署**：`docker compose up -d`。
- **License**：MIT（可商用、可私有化）。

---

## 2. 资产映射（功能 → 模块 → 复用判定）

### 2.1 我们 `ai_content` 资产现状清点
| 层 | 前缀 | 数量 | 说明 |
|---|---|---|---|
| Skill | `skl_ai_content_*` | 33 | 策划/脚本/视频/分发/运营/SEO/品牌/审核/投放等 |
| Tool | `tl_ai_content_*` | 10+ | web_search / browser_scraper / image_generator / video_generator / tts / stt / translation_api / spreadsheet / markdown / youtube_transcript |
| Workflow | `wl_ai_content_*` | 12 | content_production / video_production / multichannel_distribution / editorial_calendar / ugc_campaign / viral_analysis / brand_voice 等 |
| 部门/公司包 | `dt_content_ops` / `ccp_ai_content_company` | design-only 占位 | 尚未填充真实容器 |

**结构性结论**：能力层饱满、执行层抽象（只有生成/搜索/爬取，缺真实平台操作）→ 与 AiToEarn 形成**能力↔执行互补**。

### 2.2 逐 Agent 映射（✅复用 / ⚠️需修正 / 🔧MCP吸收 / ❌缺失）
| Agent | AiToEarn 功能 | 对应 Curis 模块 | 判定 |
|---|---|---|---|
| Create | 文案/标题/钩子/翻译/再利用 | `skl_ai_content_copywriting` 等 | ✅ |
| Create | 视频/图片生成(Grok/Veo/Seedance/NanoBanana) | `tl_ai_content_video/image_generator` | ⚠️ 未绑具体模型 |
| Create | 视频剪辑/拼接 | —— | ❌ 缺失 |
| Publish | 规划/再利用 | `wl_*` / `skl_ai_content_content_repurposing` | ✅ |
| Publish | 14+ 平台真实发布 | `wl_ai_content_multichannel_distribution_sop` | ❌⚠️ 只有 browser_scraper（读非发） |
| Publish | 日历排期执行 | `skl_ai_content_content_calendar` | ⚠️ 缺调度引擎 |
| Engage | 热点追踪 | `skl_ai_content_trend_research` | ✅ |
| Engage | 互动执行(点赞/关注/回复) | —— | ❌ 缺失 |
| Engage | 评论挖掘 | —— | ❌ 缺 skill |
| Engage | 品牌声量监测 | `skl_ai_content_competitor_content_watch` | ⚠️ 偏竞品，不足 |
| Monetize | 变现市场/结算 | `cmcf_*`(冻结) | ❌ + L2 ①②④ |
| 辅助 | 案例库/趋势雷达/跨平台分析/涨粉监控 | `skl_ai_content_viral_analysis` 等 | ✅ |

### 2.3 缺口与修正策略
- **执行层缺口**：14+ 平台发布、排期、互动、剪辑、评论挖掘。
- **修正策略 A（MCP 统一吸收，推荐）**：只新增 **1 个 Tool `tl_ai_content_aiearn_mcp`**，把上述执行缺口统一委托 AiToEarn MCP，catalog 近乎零修正；前提 L2 #5 把 `x-api-key` 进 Credential Vault。
- **修正策略 B（逐能力自建）**：代价大，仅数据主权要求极高时采用。

**复用率**：✅约40%(能力层) + ⚠️🔧约45%(经1个MCP吸收) + ❌约15%(Monetize走L2) = **85% 最小修正一站式复用**。

---

## 3. 用户使用流程（早期 wrap 模型 · **已被 §0 终版推翻**）

> ⚠️ 本节为 20:41 前的 wrap 设想（MCP + Relay 静默后端），**已被 §0 终版推翻**：Relay 白标违法，终版改用「自托管 MIT 代码 + Curis 自有平台 OAuth App」。以下仅作历史对照保留。

1. Curis Workspace → AI 公司 → 内容营销部
2. 用户给 AI 内容员工自然语言指令（如"发抖音/小红书+明早10点+回评论"）
3. Curis 运行时加载 `wl_ai_content_*` Workflow
4. 在发布/互动 step 调 `tl_ai_content_aiearn_mcp` Connector
5. Connector 从 Credential Vault 取 `x-api-key`，调 AiToEarn MCP 端点
6. AiToEarn 经 Relay/OAuth 执行真实平台操作
7. 结果回写 Curis Task/WorkflowRun + 看板

**关键**：用户全程只见 Curis；AiToEarn 是静默后端，无需登录/部署/装插件。

---

## 4. 部署决策（终版 · 2026-07-12 21:43）

| 项 | 判定 | 说明 |
|---|---|---|
| 是否部署 AiToEarn **代码** | **是（自托管 MIT 代码）** | `docker compose up -d`（Nginx+Web+Server+AI+Mongo+Redis+RustFS），界面改 Curis 品牌，作为执行引擎底座 |
| 是否用其**在线服务**(Relay/API) | **否** | ToS §5.1 禁转授权，白标转售违法 |
| AI 模型 | **用我们自有 key** | Docker 文档确认 `AI→模型服务商` 可填 OpenAI/Gemini/Anthropic |
| 社交发布/互动/数据 | **不接 Relay，注册 Curis 自有平台 OAuth App** | 租户经 Curis 的 app 授权连自己社交号 |
| aitoearn 服务费 | **零** | 完全不碰其服务 → 双付费彻底消失 |

**不再部署 `tl_ai_content_aiearn_mcp` Connector**（那是 Relay 路径的遗存）；执行层改为自托管 MIT 代码 + 自有平台 App。

---

## 5. 多租户矛盾（关键产品-架构冲突）

**问题**：若要求租户自建 AiToEarn 账号拿 key → ① 用户导流到 AiToEarn（成其注册用户，我们变导流壳）；② 流程复杂，与"纯个人创业小白"画像冲突。两问题同源 → **"每租户 key"路径整体性否决**。

**兼容"小白多租户"的三路径（租户永不见 AiToEarn）**：
| 路径 | 租户碰 AiToEarn? | 各发各号? | 代价 |
|---|---|---|---|
| A 共用 1 账号（我们持） | 否 | ❌ 共用身份 | 轻（试点/代运营） |
| B 自建 + 多租户垫片 | 否 | ✅ | 重（部署+可能 fork） |
| C 组织号后台代开子账号 | 否 | ✅（若有 admin API） | 中（依赖其 API） |

---

## 6. 截图实测验证（用户授权，20:08 / 20:16）

### 6.1 API Keys 管理页（`aitoearn.cn/zh-CN/developer/api-keys`）
- 创建弹窗："**创建量只允许在同一关联下**" → Key 限制单一 account，非组织级。
- 左侧导航：纯个人结构（概览广场/内容管理/AI助手/发布库/**开放平台**/**API Keys**/**对接指南**），**无组织/团队/子账号入口**。
- Key 列表：仅名称+时间+状态，**无作用域/权限粒度/团队归属**。

### 6.2 开放平台 / 对接指南页
- 文案："用一套 API 接入 AI 内容生成、多平台发布和结果追踪"。
- 教程卡片：发布流程/资源上传/**获取 API KEY**/视频生成/图像生成/大语言模型 → **纯个人开发者视角**。
- "获取 API KEY"：创建接口调用凭证并完成鉴权 → 单用户凭证，无 app/client_id/OAuth 授权流程。
- 可用模型：LLM(Gemini/Claude/DeepSeek/GPT) / 视频(Seedance,Grok) / 图像(GPT-image-2)。

### 6.3 判定
**路径 C（组织号代开子账号）❌ 正式排除**——无组织/子账号 admin API、账号中心化、Key 限制单一关联、对接指南无第三方应用授权。

---

## 7. 最终路径判定（终版 · 2026-07-12 21:43）

原"wrap AiToEarn"三路径（A 共用账号 / B 自建 / C 组织号）已**整体推翻**；"转售分润"方向②也因 Relay 白标违法 + ①已零成本而**放弃**。替换为以下：

| 方向 | 描述 | 判定（终版） |
|---|---|---|
| **① 自建执行层（MIT 代码底座）** | 自托管 AiToEarn **MIT 代码**为引擎 + 自有平台 OAuth App + 自有 AI key；租户连自己社交号 | ✅ **终版锁定**（原"只参照"升级为"以开源代码为底座改造"，省去从零写执行引擎） |
| **② 转售分润** | 与 AiToEarn 谈接入分账 | ❌ **放弃**（Relay 白标违法，且①已零成本没必要） |
| **③ 只产出（MVP）** | 工作流只做产出，用户自发改发 | ✅ **阶段1 先跑**（验证产出价值，零风险），非终态 |

**终版战略**：阶段1 用③快速验证；执行层终态 = **①（以 MIT 代码为底座自建，彻底摆脱对 AiToEarn 服务的依赖与任何双付费）**。

**AiToEarn 终版定位**：**MIT 开源代码 = 执行引擎底座（合法白标改造）**；其在线服务(Relay/API) = 不使用。

---

## 8. L2 Gate 红线（微调 · 2026-07-12 21:43）

| Gate | 触发点 | 处理（终版） |
|---|---|---|
| **①②④** | Monetize 变现（商业模式/收费/Marketplace） | 仍须 L2 Gate，飞书升级 + 总控决策 |
| **#5** | Curis 自有平台 OAuth App 的 client_secret 等凭据进 Credential Vault | 安全边界席评估（已是合法自有资产，非 Relay 灰区） |
| 原 Relay ToS 风险 | **已消除**——终版方案不接 Relay，注册 Curis 自有平台 App，无冒充/转授权问题 | 不触发 |

> Create/Publish/Engage 三类（不含外部凭据接入执行细节）可在 `ai_content` 红线内做 design-only 规划；**Monetize + 外部平台凭据接入 = 必须走 L2 Gate**。本决策文档仅研究，未触发任何 gate 写入/提交。

---

## 9. 下一步行动（终版 · 2026-07-12 21:43）

**阶段1 · 方向③（立即，零风险验证）**
1. 落地 `ai_content` 产出侧资产：`skl_ai_content_*` / `wl_ai_content_*` / `dt_content_ops` / `ccp_ai_content_company` 做成**可导出内容工件**（文案/脚本/视频分镜/排期表/多平台发布草稿），用户拷贝去各平台发。
2. **不建**发布/互动 Connector、**不接** AiToEarn 服务、**不触** Monetize。
3. 真实 tenant 场景跑通"指令 → 工作流 → 产出工件"，验证产出质量与编排体验。

**阶段2 · 执行层自建（以 MIT 代码为底座，合法合规）**
4. 自托管 AiToEarn **MIT 代码**（Docker），界面换 Curis 品牌，AI 接我们自有 key。
5. 注册 **Curis 自有平台开发者账号**（抖音/小红书/视频号/TikTok 等 OAuth App），租户经 Curis 的 app 授权连自己社交号 → 实现一键发布/互动/数据。
  - **无 API 平台（小红书 / 视频号）过渡**：资质获批前，先以 `social-auto-upload`（MIT，patchright）自托管打通（见 §11），获批后 drop-in 替换为原生 OAuth。
6. 发布/互动/数据执行层资产 100% 归 Curis，**零 aitoearn 服务费**。

**未来 · L2 Gate**
7. Monetize 切入时触发 L2（①②④）+ 安全边界席裁定。

---

## 10. 文件索引
- 总览规划：`docs/research/aiearn-content-marketing-reuse-plan.md`
- 精确映射：`docs/research/aiearn-asset-mapping.md`
- 本决策文档：`docs/research/aiearn-content-marketing-final-decision.md`
- 产品架构定调（编排中枢 + 可插拔执行端）：`docs/product/federated-agent-os.md`

---

## 11. 无 API 平台执行端选型（social-auto-upload · design-only 补充）

> 承接 §7 方向①。针对"小红书 / 视频号无开放 API"这一硬约束，给出具体执行端底座与渐进替换路线。零代码 / 零提交 / 不 patch 契约。

- **项目**：`dreammis/social-auto-upload`（MIT，Python，基于 **patchright** —— Playwright 反检测分支做浏览器自动化；cookie 登录 `sau <platform> login --account <name>`；headless 适合服务端 / agent；`skills/` 供 agent 调用；Docker 支持）。
- **平台覆盖**：抖音 / 小红书 / 微信视频号 / Bilibili / 快手 / 百家号 / TikTok / YouTube —— **正好覆盖我们确认无开放 API 的小红书 / 视频号**，与 AiToEarn 自托管覆盖互补。
- **为什么用它**：MIT 合法自托管 / 改造 / 向租户白标（零第三方 ToS 绑定）；比自托管 AiToEarn 全栈更轻，专攻"无 API 平台发布"这一窄场景；直接替代 §7 曾设想的 Relay 灰区。
- **渐进替换路线（总控 2026-07-12 23:40 拍板）**：
  1. **先打通**：以 social-auto-upload 自托管把整套发布链路跑通（含无 API 平台），快速拿结果、验证执行端模式；
  2. **同步申请**：并行提交各平台开发者资质（抖音 / B站企业号、小红书专业号、视频号等 OAuth App）；
  3. **逐步替换**：资质获批后，将该平台执行端从"浏览器自动化（分支 B）"drop-in 替换为"原生 OAuth API（分支 A）"；工作流与发布包 schema 不变，仅 Connector 层切换；
  4. 随替换推进，脆弱的浏览器自动化面递减；**有 API 平台**终态收敛到原生 API，但**无 API 平台（小红书 / 视频号）无官方发布 API 可换，分支 B 为长期手段**，须持续投入反爬 / 封号对抗与监控。
- **落地风险（须技术治理）**：① 平台反爬检测（patchright 缓解但平台持续进化）；② 封号风险（逐租户 cookie / 账号）；③ 平台 UI 变更致脚本脆弱；④ 逐租户 cookie 托管安全（加密进 Credential Vault + 账号隔离 + 限流 + UI 监控）。
- **与 §7 一致性**：本选型属"自托管 MIT 代码"干净路径，不触 Relay ToS 风险；平台开发者账号注册（Curis 自有 OAuth App）仍归 L2 #5（安全边界席）。

---

*—— 最终决策文档（零代码、零提交、不 patch 契约）。DevOps Automator · 2026-07-12。*
