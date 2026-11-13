# Curis 三大业务 × 可用 Skill 对应关系（2026-10-29）

Status: Review
Authority Class: RESEARCH
Disposition: REVIEW_REQUIRED
Owner: Capability Intelligence Owner
Scope: 只做「业务环节 → Skill」对应分析，不修改代码 / Runtime / Schema / 人才库 Authority，不执行安装。

> 本文是 Research Evidence，不构成新的能力真源。候选的登记真源仍是
> `docs/01_Product/Curis_Talent_Candidate_Package_2026-08-18.md`；
> 晋级 `CURIS_READY` 仍须真实任务 + Evidence。

---

## 0. 直接结论

**有可用 Skill，但覆盖极不均匀。**

- **强覆盖**：内容制作 / 素材采集 / 封面与配图 / 发布物料 / 市场研究 / 竞品分析 / 数据分析 / 写作润色（中文）。`JimLiu/baoyu-skills`（MIT，21 个技能）与 `ever-just/agentskills`（MIT，168 个技能）几乎可以填掉 CG 与 Writing 的大部分「人工+AI 辅助」环节。
- **结构性空缺（真 GAP，不是没找到）**：
  1. **音乐音频生成 / 编曲 / 混音母带** —— 候选池 0 个可用 Skill。`JimLiu/baocut` 只做转写/字幕/配音/剪切，且 License 未确认（NOASSERTION）。
  2. **平台发布连接器**（小红书 / 抖音 / 视频号 / 公众号）—— 这是 Connector 能力，不是 Skill；`baoyu-post-to-*` 只是脚本级发布，需账号授权，属外发授权门。
  3. **写作·人物一致性检查** —— 无专门 Skill，只能用协同写作 + 规划类变通。
- **前置事实**：三大业务当前实现是「本地人工依据链 + 强制 UNVERIFIED」，多数环节是**人工记录**而非 AI 自动执行。Skill 的价值是辅助「研究/写作/出图/整理数据/出物料」，不能替代业务状态机与人工确认。

---

## 1. 三大业务的真实工作流（取自代码，非推测）

### 1.1 Content Growth（内容增长 / CG）— 九环节

来源：`frontend/components/content-growth/ContentGrowthWorkspace.js` 的 `navigation` 数组。

| # | 环节 key | 中文名 | 数据对象 |
|---|---|---|---|
| 1 | `operating` | 经营 | Context |
| 2 | `market` | 市场与方向 | Scope / Snapshot / Reference / Direction |
| 3 | `production` | 内容制作 | Context |
| 4 | `materials` | 素材与灵感 | Reference |
| 5 | `accounts` | 平台与账号 | Scope |
| 6 | `verify` | 发布准备 | Report / Artifact |
| 7 | `observe` | 表现与归因 | Snapshot / Report |
| 8 | `analysis` | 经营分析 | Report |
| 9 | `learning` | 内容经验 | Report |

数据模型来源：`backend/app/content_growth_operating_service.py` — `SCHEMA = "cg.operating-context/v1"`，`FIELDS` 含 `Scope / Snapshot / Reference / Direction / Report / Context`。

### 1.2 Music（音乐）— 经营九视面 + 歌曲创作五阶段

经营视面来源：`frontend/lib/musicState.mjs` 的 `OPERATING_VIEWS`。

| # | 视面 key | 中文名 |
|---|---|---|
| 1 | `operating` | 经营 |
| 2 | `songs` | 歌曲创作 |
| 3 | `market` | 市场依据 |
| 4 | `reference` | 参考分析 |
| 5 | `direction` | 创作方向 |
| 6 | `release` | 发行与发布 |
| 7 | `performance` | 作品表现 |
| 8 | `report` | 分析报告 |
| 9 | `learning` | 经验与下一首 |

歌曲创作阶段来源：`frontend/components/music/MusicMain.js` 的 `aria-label="歌曲创作阶段"` 标签页。

| # | key | 中文名 |
|---|---|---|
| 1 | `lyrics` | 歌词与结构 |
| 2 | `candidates` | 制作与候选 |
| 3 | `history` | 版本历史 |
| 4 | `release` | 发行依据 |
| 5 | `analysis` | 结果与下一首 |

数据模型来源：`backend/app/music_service.py` — Song 子对象含 `LyricsVersion / ProductionVersion / Candidate / AudioAssetVersion / Choice / MasterRevision / ReleasePackage`；经营对象含 `OperatingScope / MarketSnapshot / ReferenceAnalysis / Direction / Observation / Report / Learning`（见 `OPERATING_KIND_VIEWS`）。

### 1.3 Writing（写作）— 五视面 + 作品库 / 章节 / 发布

视面来源：`frontend/components/writing/WritingWorkspace.js:27-33` 的 `WRITING_SURFACES`。

| # | 视面 key | 中文名 | 官方描述 |
|---|---|---|---|
| 1 | `overview` | 经营 | 查看当前作品、依据与待确认方向 |
| 2 | `market` | 市场与方向 | 记录人工来源与观察，保留未核验市场依据 |
| 3 | `directions` | 作品方向 | 选择适用范围与引用依据，确认后应用到章节 |
| 4 | `performance` | 读者与收益 | 人工反馈记录；平台数据尚未连接 |
| 5 | `learning` | 写作经验 | 保存用途、原依据与限制，应用到新章节 |

另有：作品库（`books`）、章节（结构 / 人物 / 正文 / 作者检查）、发布（`WritingPublishingMain`）。

数据模型来源：`backend/app/writing_operating_service.py` — `WritingDirection / WritingLearning / WritingMarketSnapshot / WritingObservation`，`SCHEMA_VERSION = "writing.operating/v1"`。

---

## 2. Content Growth 环节 × Skill 对应

| 环节 | Skill 名称 | 地址 | 功能 | 在 Curis 的作用 | 可用性 |
|---|---|---|---|---|---|
| 经营 | `business-model-canvas` | github.com/ever-just/agentskills/tree/main/skills/business-model-canvas | 用画布拆商业模式（客户/价值/收入/成本） | 建号前梳理账号定位与变现路径，产出写到 CG `Context` | MIT ✅ |
| 市场与方向 | `deep-research` | github.com/ever-just/agentskills/tree/main/skills/deep-research | 多轮检索 + 来源核验的深度调研 | 生成 `market` 环节的 `Snapshot/Reference` 草案（仍待人工确认） | MIT ✅ |
| 市场与方向 | `competitor-identification` | github.com/ever-just/agentskills/tree/main/skills/competitor-identification | 识别并结构化竞品清单 | 填 `Reference`（对标账号/内容） | MIT ✅ |
| 市场与方向 | `ad-transparency-audit` | github.com/ever-just/agentskills/tree/main/skills/ad-transparency-audit | 查投放透明度/广告库 | 判断竞品投放策略，支撑 `analysis` | MIT ✅ |
| 市场与方向 | Agentic-SEO-Skill | github.com/Bhanunamikaze/Agentic-SEO-Skill | SEO/GEO 分析（关键词、E-E-A-T、结构化数据） | 平台搜索流量优化，产出选题依据 | MIT ✅ |
| 内容制作 | `baoyu-format-markdown` | github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-format-markdown | Markdown 规范化排版 | 把草稿整理成可发布结构 | MIT ✅ |
| 内容制作 | `baoyu-translate` | .../skills/baoyu-translate | 高质量翻译 | 多语内容/海外平台改写 | MIT ✅ |
| 内容制作 | `internal-comms`（anthropics） | github.com/anthropics/skills/tree/main/skills/internal-comms | 写状态报告、newsletter、FAQ | 内容体例参照、公告类文案 | Apache-2.0 ✅ |
| 素材与灵感 | `baoyu-url-to-markdown` | .../skills/baoyu-url-to-markdown | 网页抓取转 Markdown | 采集竞品/资料进 `Reference` | MIT ✅ |
| 素材与灵感 | `baoyu-youtube-transcript` | .../skills/baoyu-youtube-transcript | 拉取视频字幕稿 | 视频类素材转文字 | MIT ✅ |
| 素材与灵感 | `contact-sheet-image-analysis` | .../agentskills/skills/contact-sheet-image-analysis | 批量图片缩略表 + 筛选分析 | 从大量图里挑可用素材 | MIT ✅ |
| 素材与灵感 | `baoyu-compress-image` | .../skills/baoyu-compress-image | 图片压缩 | 素材落库前减重（本地存储友好） | MIT ✅ |
| 平台与账号 | `baoyu-post-to-wechat` | .../skills/baoyu-post-to-wechat | 发布到微信公众号 | **需账号授权**，属外发授权门 | MIT ✅（Security Review） |
| 平台与账号 | `baoyu-post-to-weibo` / `baoyu-post-to-x` | .../skills/baoyu-post-to-weibo、baoyu-post-to-x | 发布到微博 / X | 同上 | MIT ✅（Security Review） |
| 发布准备 | `baoyu-xhs-images` | .../skills/baoyu-xhs-images | 生成小红书风格配图 | 图文笔记的成组配图 | MIT ✅ |
| 发布准备 | `baoyu-cover-image` | .../skills/baoyu-cover-image | 封面图生成 | 每篇内容封面 | MIT ✅ |
| 发布准备 | `baoyu-infographic` | .../skills/baoyu-infographic | 信息图 | 长图/知识型内容 | MIT ✅ |
| 发布准备 | `baoyu-slide-deck` | .../skills/baoyu-slide-deck | 幻灯片组 | 图文轮播/资料卡 | MIT ✅ |
| 发布准备 | `pptx` / `pdf` / `docx`（anthropics） | github.com/anthropics/skills | Office/PDF 生成与编辑 | 发布物料、复盘报告 | Apache-2.0 ✅ |
| 表现与归因 | `xlsx`（anthropics） | github.com/anthropics/skills/tree/main/skills/xlsx | 表格读写与公式 | 手工导入的平台数据做归因表 | Apache-2.0 ✅ |
| 表现与归因 | `d3-visualization` | .../agentskills/skills/d3-visualization | 生成交互式数据图 | 归因结果可视化 | MIT ✅ |
| 经营分析 | `data-analysis` / scientific skills | github.com/K-Dense-AI/claude-scientific-skills | 统计分析与科研级图表 | 内容表现统计、显著性判断 | MIT ✅ |
| 内容经验 | `planning-with-files` | github.com/OthmanAdi/planning-with-files | 文件化持久规划，跨会话恢复 | 沉淀「爆款/失败」经验到 `learning` | MIT ✅ |
| 内容经验 | `conversation-review` | .../agentskills/skills/conversation-review | 复盘对话与决策过程 | 单篇内容事后复盘 | MIT ✅ |
| （商业侧）| `meshcode-ai/skills-biz`、`skills-copy`、`skills-seo`、`skills-marketing`、`skills-research`、`skills-docs` | github.com/meshcode-ai/skills | 73 个商业技能（SEO/营销/文案/运营/规划/研究/文档） | 覆盖面与 baoyu 互补 | ⚠️ License REVIEW（NOASSERTION） |

**CG 真 GAP**：小红书 / 抖音 / 视频号发布**连接器**（非 Skill）；粉丝与流量数据自动回填（平台 OpenAPI 未接）。

---

## 3. Music 环节 × Skill 对应

| 环节 | Skill 名称 | 地址 | 功能 | 在 Curis 的作用 | 可用性 |
|---|---|---|---|---|---|
| 歌词与结构 | `baoyu-format-markdown` | github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-format-markdown | 结构化排版 | 把 `[主歌]/[副歌]` 段落整理成规范 `LyricsVersion` 文本 | MIT ✅ |
| 歌词与结构 | `baoyu-translate` | .../skills/baoyu-translate | 翻译/双语 | 歌词多语版本（海外发行） | MIT ✅ |
| 市场依据 | `deep-research` | github.com/ever-just/agentskills/tree/main/skills/deep-research | 深度调研 | 曲风/题材热度依据 → `MarketSnapshot` | MIT ✅ |
| 市场依据 | `competitor-identification` | .../skills/competitor-identification | 竞品识别 | 对标歌曲/作者 → `ReferenceAnalysis` | MIT ✅ |
| 参考分析 | `deep-research` | 同上 | 同上 | 拆解参考曲的歌词结构/主题 | MIT ✅ |
| 创作方向 | `planning-with-files` | github.com/OthmanAdi/planning-with-files | 持久规划 | 确定 `Direction` 并跨会话保留 | MIT ✅ |
| 制作与候选 | —— | —— | —— | **无可用 Skill** | ❌ **GAP** |
| 制作与候选（旁证） | `baocut`（skills/baocut） | github.com/JimLiu/baocut/tree/main/skills/baocut | 转写/字幕/翻译/配音/剪切/动画 | 仅音频**后处理**，不生成音乐 | ⚠️ License NOASSERTION |
| 版本历史 | —— | —— | —— | Curis 自身状态机已覆盖，无需 Skill | — |
| 发行与发布 | `baoyu-cover-image`、`baoyu-post-to-wechat`、`baoyu-post-to-x` | github.com/JimLiu/baoyu-skills | 封面/宣发 | 发行包宣传物料 | MIT ✅（外发授权门） |
| 发行与发布 | `pdf` / `pptx`（anthropics） | github.com/anthropics/skills | 文档/演示生成 | 发行资料、一页纸 | Apache-2.0 ✅ |
| 作品表现 | `xlsx`（anthropics） | github.com/anthropics/skills/tree/main/skills/xlsx | 表格 | 手工导入播放/收藏数据 → `Observation` | Apache-2.0 ✅ |
| 分析报告 | `pptx` / `meshcode-ai/skills-docs` | github.com/anthropics/skills、github.com/meshcode-ai/skills | 生成报告 | `Report` 成稿 | Apache-2.0 ✅ / ⚠️ |
| 经验与下一首 | `planning-with-files` | github.com/OthmanAdi/planning-with-files | 持久经验 | `Learning` 沉淀 | MIT ✅ |

**Music 真 GAP（最严重）**：音频生成、编曲、混音/母带、演唱匹配 —— 候选池无任何可用 Skill。当前 Curis 的 `Candidate`/`AudioAssetVersion` 只能靠**用户本地导入音频**，这与代码注释一致（"用户提供音频仅限本地使用，商业权利与演唱匹配未核验"）。这是**能力供应缺口**，不是配置问题。

---

## 4. Writing 环节 × Skill 对应

| 环节 | Skill 名称 | 地址 | 功能 | 在 Curis 的作用 | 可用性 |
|---|---|---|---|---|---|
| 经营 | `business-model-canvas` | github.com/ever-just/agentskills/tree/main/skills/business-model-canvas | 商业画布 | 作品变现路径 | MIT ✅ |
| 市场与方向 | `deep-research` | .../skills/deep-research | 深度调研 | 题材/榜单依据 → `WritingMarketSnapshot` | MIT ✅ |
| 市场与方向 | `competitor-identification` | .../skills/competitor-identification | 竞品识别 | 同类作品对标 | MIT ✅ |
| 市场与方向 | Agentic-SEO-Skill | github.com/Bhanunamikaze/Agentic-SEO-Skill | 搜索优化分析 | 书名/章节标题的搜索友好度 | MIT ✅ |
| 作品方向 | `doc-coauthoring`（anthropics） | github.com/anthropics/skills/tree/main/skills/doc-coauthoring | 协同写作与方向讨论 | 产 `WritingDirection` 草案，确认后应用 | Apache-2.0 ✅ |
| 章节·结构 | `planning-with-files` | github.com/OthmanAdi/planning-with-files | 文件化大纲/防丢失 | 长篇分卷分章大纲 | MIT ✅ |
| 章节·结构 | `baoyu-format-markdown` | github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-format-markdown | 结构规范化 | 章节格式统一 | MIT ✅ |
| 章节·人物 | —— | —— | —— | **无专门 Skill** | ❌ **GAP** |
| 章节·正文 | `baoyu-skills`（中文写作/润色族） | github.com/JimLiu/baoyu-skills | 中文写作、改写、排版 | 正文起草与润色 | MIT ✅ |
| 章节·作者检查 | `conversation-review` / `agent-quality-grading` | .../agentskills/skills/conversation-review、agent-quality-grading | 清单式复核与评分 | 自查「结构/人物/正文」一致性 | MIT ✅ |
| 章节·作者检查 | `docx`（anthropics） | github.com/anthropics/skills/tree/main/skills/docx | Word 生成与校对 | 正式稿导出与格式检查 | Apache-2.0 ✅ |
| 读者与收益 | `xlsx`（anthropics） | github.com/anthropics/skills/tree/main/skills/xlsx | 表格 | 手工导入的订阅/收益记录 → `WritingObservation` | Apache-2.0 ✅ |
| 写作经验 | `planning-with-files` | github.com/OthmanAdi/planning-with-files | 持久经验 | `WritingLearning` 沉淀 | MIT ✅ |
| 发布 | `baoyu-post-to-wechat`、`baoyu-slide-deck`、`baoyu-cover-image` | github.com/JimLiu/baoyu-skills | 发布/幻灯片/封面 | 上架与宣传 | MIT ✅（外发授权门） |
| 发布 | `pptx` / `pdf`（anthropics） | github.com/anthropics/skills | 文档生成 | 投稿/样章 PDF | Apache-2.0 ✅ |

**Writing 真 GAP**：人物设定一致性检查、中文长篇连贯性审查、平台阅读数据连接器（视面已注明"平台读者与收益数据尚未连接"）。

---

## 5. 覆盖度评分（按环节，非按数量）

| 业务 | 环节数 | 有 Skill 支撑 | 部分支撑 | 空缺 | 覆盖率 |
|---|---|---|---|---|---|
| Content Growth | 9 | 8 | 0 | 1（平台发布连接器） | ~89% |
| Music | 9 视面 + 5 创作阶段 | 8 | 1（发布靠脚本级） | 1（音频生成/制作） | ~67%（但缺的是最核心环节） |
| Writing | 5 视面 + 3 子域 | 7 | 1（作者检查靠清单变通） | 1（人物一致性） | ~80% |

> 注意：覆盖率算的是「环节有对应 Skill」，**不等于** Curis 已具备该能力。全部仍需真实任务验证 + Evidence。

---

## 6. 推荐优先安装（按业务价值，非星标）

### 第一批（CG + Writing 立即可用，MIT，零授权风险）

1. `JimLiu/baoyu-skills` —— **最高优先**。21 个技能覆盖中文写作、配图、封面、信息图、发布物料、网页/视频转素材。对 CG 九环节与 Writing 章节创作直接命中，且中文原生。
2. `ever-just/agentskills` —— 168 个技能，取子集即可：`deep-research`、`competitor-identification`、`ad-transparency-audit`、`business-model-canvas`、`d3-visualization`、`contact-sheet-image-analysis`、`conversation-review`。
3. `anthropics/skills` —— `docx`/`pptx`/`xlsx`/`pdf`/`doc-coauthoring`/`internal-comms`，是三大业务「成稿/报告/数据」的通用底座。
4. `OthmanAdi/planning-with-files` —— 三业务共用的「经验沉淀 + 长任务不丢」。
5. `Bhanunamikaze/Agentic-SEO-Skill` —— CG 与 Writing 的搜索流量优化。

### 第二批（需 Security Review：涉及账号外发）

6. `baoyu-post-to-wechat` / `baoyu-post-to-weibo` / `baoyu-post-to-x` —— 属外发授权门，须用户显式授权且记录授权范围。

### 暂不入库

- `JimLiu/baocut`（NOASSERTION，且不解决音乐生成）
- `meshcode-ai/skills`（NOASSERTION，与 baoyu 高度重叠）

### 需外部补源（不是 Skill 能解决）

- 音乐音频生成/编曲/母带：建议登记为 **GAP**，通过 Connector（如音频生成 Provider）而非 Skill 解决。
- 小红书/抖音/视频号发布与数据回填：Connector 能力。

---

## 7. 边界声明

- 本文只做对应分析，**未安装任何 Skill、未写入 `sources/`、未改生产线**。
- 所有候选仍为 `CANDIDATE`，`CURIS_READY` 为 0；晋级须真实任务 + Evidence。
- 三大业务当前为「本地人工依据链 + 强制 UNVERIFIED」，Skill 只能辅助，不能替代业务状态机与人工确认。
- 外发类技能（`baoyu-post-to-*`）默认不启用，须用户显式授权。

---

CURIS CAPABILITY INTELLIGENCE
— BUSINESS SKILL MAPPING COMPLETE
— AWAITING CONFIRMATION BEFORE INSTALL
