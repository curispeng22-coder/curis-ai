# AiToEarn 功能 → Curis 模块 精确资产映射表

> **研究日期**：2026-07-12（深化自 `docs/research/aiearn-content-marketing-reuse-plan.md`）
> **目的**：逐功能比对 AiToEarn 四大 Agent + 辅助模块，定位对应 Curis 模块、判定复用/需修正。
> **数据来源**：`official-skill-catalog-contract.md`（33 条 `skl_ai_content_*`）、`tool-catalog-official-plan.md`（10+ 条 `tl_ai_content_*`）、`workflow-official-content-plan.md`（12 条 `wl_ai_content_*`）。
> **性质**：纯研究/映射（零代码、零提交、不 patch）。
> **符号约定**：✅ 直接复用 ｜ ⚠️ 概念复用但执行层需修正 ｜ 🔧 经 AiToEarn MCP 统一吸收（推荐）｜ ❌ 缺失需新建/走 Gate

---

## 0. 我们 `ai_content` 资产现状清点

| 层 | 前缀 | 数量 | 说明 |
|---|---|---|---|
| Skill（能力 what） | `skl_ai_content_*` | 33 | 内容策划/脚本/视频/分发/运营/SEO/品牌/审核/投放等 |
| Tool（执行 how） | `tl_ai_content_*` | 10+ | web_search / browser_scraper / image_generator / video_generator / text_to_speech / speech_to_text / translation_api / spreadsheet_read / markdown_renderer / youtube_transcript |
| Workflow（编排 order/who） | `wl_ai_content_*` | 12 | content_production / topic_research / script_writing / video_production / seo / editorial_calendar / multichannel_distribution / content_audit / livestream / ugc_campaign / viral_analysis / brand_voice |
| 部门/公司包 | `dt_content_ops` / `ccp_ai_content_company` | design-only 占位 | 尚未填充真实容器 |

> **结构性结论**：我们 catalog 主体是**能力描述层 + 编排层**（Skill/Workflow 饱满），**执行层（Tool）偏抽象**——只有"生成/搜索/爬取"类，缺"真实平台操作"类。这正好与 AiToEarn 形成**能力层↔执行层互补**。

---

## 1. 🎨 Create（内容创作）映射

| AiToEarn 功能 | 对应 Curis 模块 | 判定 | 修正说明 |
|---|---|---|---|
| 视频生成（Grok/Veo/Seedance/HappyHorse 文生/图生视频） | `tl_ai_content_video_generator`（media_generation） | ⚠️ | 我们仅有抽象 `video_generator`，**未绑定具体模型供应商**。修正：映射到具体供应商，或经 AiToEarn AI Relay 统一调用。 |
| 图片生成（Nano Banana / Pro） | `tl_ai_content_image_generator`（media_generation） | ⚠️ | 同上，未绑定 Nano Banana 等具体模型。 |
| 视频翻译 | `tl_ai_content_translation_api`（api_integration） | ✅ | 直接复用。 |
| 视频剪辑 / 拼接 | —— | ❌ | **缺视频剪辑 Tool**。我们有"生成"无"剪辑"。需新增 `tl_ai_content_video_editor`（或经 AiToEarn 吸收）。 |
| 批量生成 + 参考素材 + 目标平台限制 | `wl_ai_content_video_production_sop` / `wl_ai_content_content_production_sop` | ⚠️ | Workflow 描述了批量/多模型意图，但 Tool 层是单一 generator，**缺 batch orchestration 执行**。 |
| 文案/标题/描述自动生成 | `skl_ai_content_copywriting` / `hook_writing` / `title_optimization` | ✅ | 直接复用。 |
| 缩写/扩写/标签生成 | `skl_ai_content_content_repurposing` / `editing_guidance` | ✅ | 直接复用。 |

**Create 小结**：文案类 100% 复用；生成类"能力在、执行抽象"→ 经 MCP 吸收（🔧）或更换具体模型绑定（⚠️）；剪辑类纯缺口（❌）。

---

## 2. 📢 Publish（内容发布）映射

| AiToEarn 功能 | 对应 Curis 模块 | 判定 | 修正说明 |
|---|---|---|---|
| 一键分发 14+ 平台（抖音/快手/B站/小红书/视频号/公众号/TikTok/YouTube/FB/INS/Threads/X/Pinterest/LinkedIn） | `wl_ai_content_multichannel_distribution_sop` + `skl_ai_content_multi_platform_distribution` | ⚠️🔧 | **重大缺口**：Workflow/Skill 是"能力描述"，但**缺真实平台发布连接器**。我们只有 `tl_ai_content_browser_scraper`（读，非发）。修正：新建平台发布 Connector，或🔧 经 AiToEarn MCP 统一委托（推荐，避免自建 14+ 平台适配）。 |
| 日历排期（calendar scheduler） | `skl_ai_content_content_calendar` / `wl_ai_content_editorial_calendar_sop` | ⚠️ | 我们有"日历规划"能力，但**缺真实发布调度执行引擎**（定时器触发实际发布）。需补 scheduling execution step。 |
| Smart Import（历史内容再编辑再分发，如小红书→YouTube） | `skl_ai_content_content_repurposing` | ✅ | 直接复用（内容再利用）。 |
| 各平台格式/规则自动适配 | `skl_ai_content_platform_algorithm_research` | ⚠️ | 我们有算法研究 skill，但**缺"格式自动适配"执行 Tool**。 |

**Publish 小结**：规划/再利用✅；真实分发与排期执行❌⚠️ → 最佳路径是🔧 一个 `tl_ai_content_aiearn_mcp` connector 统一吸收全部平台发布+排期，我们 catalog 几乎零修正。

---

## 3. 💬 Engage（内容互动）映射

| AiToEarn 功能 | 对应 Curis 模块 | 判定 | 修正说明 |
|---|---|---|---|
| 自动点赞/收藏/关注（浏览器插件） | —— | ❌ | **缺互动执行连接器**。我们 `browser_scraper` 是读取，无"操作"能力。需新增 `tl_ai_content_engagement_bot`（或🔧 经 AiToEarn 吸收）。 |
| AI 智能回复评论（调大模型针对性回复） | `skl_ai_content_community_management` / `ugc_campaign` | ⚠️ | 有社区管理/ugc skill，但**缺"自动评论回复"执行 Tool**（需平台 API + LLM）。 |
| 评论挖掘（识别"求链接/怎么买"高转化信号） | —— | ❌ | **缺评论挖掘 Skill/Tool**。需新增 `skl_ai_content_comment_mining`。 |
| 品牌声量监测 | `skl_ai_content_competitor_content_watch` | ⚠️ | competitor watch 偏竞品，**品牌声量监测需补** `skl_ai_content_brand_monitoring`（或扩展现有）。 |
| 热点话题追踪参与 | `skl_ai_content_trend_research` | ✅ | 直接复用。 |

**Engage 小结**：热点追踪✅；互动执行与评论挖掘❌；品牌监测⚠️ → 互动执行建议🔧 经 MCP 吸收，评论挖掘 skill 需新建。

---

## 4. 💰 Monetize（内容变现）映射

| AiToEarn 功能 | 对应 Curis 模块 | 判定 | 修正说明 |
|---|---|---|---|
| 内容交易市场 / 淘金广场任务池 | —— | ❌ | **需 Marketplace 资产**（运营协定 L2 #4 冻结项）。 |
| CPS / CPE / CPM 结果导向结算 | `cmcf_*`（Commercial Configuration，冻结） | ❌ | 需 L2 #2 解冻收费规则。 |
| 线下商户推广（餐厅/零售/民宿→线上传播任务） | —— | ❌ | 新场景，无对应资产。 |

**Monetize 小结**：整体缺失，且触 **L2 ①②④（商业模式/收费/Marketplace）**，须升级流程，不可在阶段1落地。

---

## 5. 辅助模块映射

| AiToEarn 模块 | 对应 Curis 模块 | 判定 |
|---|---|---|
| 案例库（1万+赞怎么写） | `skl_ai_content_viral_analysis` / `content_series_planning` | ✅ |
| 趋势雷达（trend radar） | `skl_ai_content_trend_research` | ✅ |
| 跨平台数据对比 | `skl_ai_content_content_performance_dashboard` / `platform_algorithm_research` | ✅ |
| 端到端涨粉监控 | `skl_ai_content_data_retrospective` / `content_performance_dashboard` | ✅ |

---

## 6. 缺口汇总（按层归类）

| 缺口 | 层 | 类型 | 修正路径 |
|---|---|---|---|
| 14+ 平台发布连接器 | Tool | ❌ 缺失 | 🔧 建 `tl_ai_content_aiearn_mcp` 统一吸收（推荐）或逐平台自建 |
| 发布调度执行引擎 | Workflow/Tool | ⚠️ 执行缺 | 补 scheduling step（可寄于 MCP connector） |
| 视频剪辑 Tool | Tool | ❌ 缺失 | 🔧 经 AiToEarn / 或新增 `tl_ai_content_video_editor` |
| 互动自动化连接器（点赞/关注/回复） | Tool | ❌ 缺失 | 🔧 经 AiToEarn MCP 吸收 |
| 评论挖掘 Skill | Skill | ❌ 缺失 | 新增 `skl_ai_content_comment_mining` |
| 品牌声量监测 Skill | Skill | ⚠️ 不足 | 新增/扩展 `skl_ai_content_brand_monitoring` |
| 生成 Tool 绑定具体模型 | Tool | ⚠️ 抽象 | 绑定 Grok/Veo/Seedance/Nano Banana 或经 AI Relay |
| Monetize 变现 + 结算 + Marketplace | 新资产 | ❌ + L2 | 走 L2 Gate ①②④ |

---

## 7. 修正策略：两种补法

### 策略 A：🔧 MCP 统一吸收（推荐）
只新增 **1 个 Tool** `tl_ai_content_aiearn_mcp`（Connector 类型），把所有"执行缺口"——平台发布、排期、互动、剪辑、评论挖掘——统一委托给 AiToEarn 的 MCP 端点。
- **优点**：我们 catalog 几乎零修正（不逐一建 14+ 平台发布器/互动器）；随上游更新；MIT 合规。
- **前提**：L2 #5 审批把 AiToEarn `x-api-key` 纳入 Credential Vault（安全边界席评估）。
- **结果**：Create/Publish/Engage 三类能力在我们的 `wl_ai_content_*` / `skl_ai_content_*` 编排下，由 AiToEarn 执行——**一站式复用达成，修正量最小**。

### 策略 B：逐能力自建 Tool
为每个缺口单独建 `tl_ai_content_platform_publisher` / `video_editor` / `engagement_bot` 等，并自建平台 OAuth 适配。
- **优点**：完全自主、不依赖外部服务。
- **代价**：工作量大、需维护 14+ 平台 API 变动、Relay 合规风险自担。
- **结论**：仅当数据主权/可用性要求极高时采用。

> **建议**：阶段1 走策略 A，把缺口打包成 1 个 MCP connector；阶段3（若做 Monetize）再评估是否部分自建。

---

## 8. 复用率结论

- **可直接复用（✅）**：文案/标题/钩子、翻译、内容再利用、趋势研究、案例库/病毒分析、社区管理、内容性能看板、竞品监测 → 约占 AiToEarn 功能的 **40%**（集中在 Skill/Workflow 能力层）。
- **概念复用 + MCP 吸收（⚠️🔧）**：视频/图片生成、14+ 平台发布、排期、互动、剪辑、评论挖掘 → 约占 **45%**，经 1 个 MCP connector 吸收，catalog 基本不修正。
- **缺失需新建/走 Gate（❌）**：Monetize 变现市场 + 结算 + Marketplace → 约占 **15%**，触 L2 ①②④，须升级。

**一句话**：AiToEarn 的"能力层"我们已基本具备（Skill/Workflow 饱满），它主要补我们的"执行层"缺口；用 MCP 接入可把 85% 的功能以最小修正实现一站式复用，仅 Monetize 必须走 L2 Gate。

---

*—— 精确资产映射表（零代码、零提交、不 patch 契约）。DevOps Automator · 2026-07-12。*
