# Curis 抖音 / TikTok Workspace — Reference Research（外部证据研究）

**阶段**：TTK PRODUCT MODEL RESEARCH ONLY  
**状态**：RESEARCH ONLY · 不修改任何权威文档（Blueprint / Frozen Shell / P1–P7 / XHS / RD / Runtime / 代码）  
**目的**：回答「Curis 的抖音专业办公室究竟应该是什么」，为产品模型提案（Proposal）提供真实业务证据与外部竞品参照。  
**专家角色**：UiDesigner（产品模型研究，非高保真 / 非 Prototype / 非开发）

> 来源标注约定：
> - `OFFICIAL` = 官方产品文档 / 官方说明（作为事实）
> - `OBS` = 竞品观察（第三方对产品的描述 / 功能罗列，可能含作者主观）
> - `INF` = 研究推断（基于多源归纳的推断，**非事实**）
> - `CURIS` = 对 Curis 的建议（产品结论，待 Review）
> 推断与建议明确区分，不把推断写成事实。

---

## 0. 来源登记（Source Registry）

| ID | 来源 | 类型 | 用于 |
|----|------|------|------|
| S1 | 抖音运营SOP全流程（ProcessOn） | OBS / 行业SOP | 中文短视频标准工作流、辅助工具链 |
| S2 | 抖音短视频运营全攻略（yunyingbu） | OBS | 选题/脚本/拍摄/发布/数据全流程 |
| S3 | 2026短视频学习完整路线图（QQ新闻） | OBS | 从0到变现全流程、核心指标 |
| S4 | 抖音运营SOP·90天路线图（zhco） | OBS | 团队分工、每周执行清单、批量拍摄 |
| S5 | How to Get More Views on TikTok 2026（On Digitals） | OBS（接近官方方法论） | TikTok 增长七步、脚本四段、实验日志 |
| S6 | 10 Essential TikTok Creator Tools 2026（LunaBloom） | OBS | TikTok Studio / CapCut 在栈中的定位 |
| S7 | Grow TikTok Without Face 2026（Kineclip） | OBS | 批量生产、完播率优先、周反馈环 |
| S8 | Short-Form Video Workflow 2026（OutfitVideo） | OBS | 5 阶段工作流、批量、二次利用 |
| S9 | How to Use CapCut AI Video Editing 2026（digen） | OBS | CapCut AI 功能（文生视频/字幕/语音） |
| S10 | What Is CapCut AI（Pexo） | OBS | CapCut 是「草稿生成器」非自主 Agent |
| S11 | CapCut Review 2026（max-productive） | OBS | CapCut 能力边界、15分钟限制 |
| S12 | 蝉妈妈官网（chanmama.com） | OFFICIAL | 数据分析平台能力事实 |
| S13 | 为什么数据分析都推荐蝉妈妈（蝉妈妈运营圈） | OBS | 工具对比（巨量算数/爬虫缺陷） |
| S14 | 抖音数据分析工具（zhangfensi） | OBS | 工具全景（官免/综合/内容/特色） |
| S15 | 短视频运营助手怎么选（今日头条） | OBS | 工具组合（Coze/巨量算数/飞瓜/剪映/Canva/即梦/易媒） |
| S16 | video skill（skillsmp/gitscape） | OBS | Agent-native 视频管线 |
| S17 | video-produce skill（claudepluginhub） | OBS | 工作流 + 工具映射 + 常见错误 |
| S18 | AI Video Production Explained（leenkup） | OBS | 品牌工作流、披露义务、成本、权利 |
| S19 | Best AI Video Tools 2026（whataidoineed） | OBS | 4 类工作流、避免过度自动化 |
| S20 | AI Short-Form Video Tools 2026（findaiverse） | OBS | Opus Clip 需人工复核 |

---

## 1. 真实短视频运营工作链（多源收敛）

以下链条在 S1/S2/S4/S5/S8 中高度一致，作为 `INF`（行业共识，非单一官方事实）：

```
选题 / 热点  →  脚本  →  素材准备  →  拍摄 或 AI 生成  →  剪辑  →  审核  →  排期  →  发布  →  数据观察  →  复盘  →  二次利用
```

**各环节证据要点**

| 环节 | 真实实践（来源） | 推断 / 标注 |
|------|----------------|------------|
| 选题/热点 | 巨量算数查热词TOP50、创作灵感、直播间弹幕痛点（S1）；爆款复制/热点借力/用户痛点三法（S2）；趋势词交 Coze 转选题（S15） | `OBS`→`INF`：选题研究是独立前置环节，依赖外部趋势源 |
| 脚本 | 黄金3秒钩子+每15-20秒信息点（S3）；口播/Vlog/剧情三模板（S2）；问题-方案/故事-启发/对比-选择三结构（S4） | `OBS`→`INF`：脚本是重环节，有多种结构化模板，且**紧密绑定单条视频** |
| 素材准备 | 手机+补光+领夹麦（S2）；BGM/资产准备（S4）；即梦AI生成分镜参考（S15） | `OBS` |
| 拍摄/AI生成 | 一个场景3角度（S3）；AI生成B-roll（S9/S17）；HeyGen数字人（S18） | `OBS` |
| 剪辑 | 剪映：导入→分割→字幕→BGM→比例→导出（S2）；批量剪辑（S4） | `OBS` |
| 审核 | 合规/品牌/版权人工审核（S18 法律确认；S19 敏感内容保留真人） | `OBS`→`INF`：审核是判断型责任，非纯技术 |
| 排期 | 工作日/周末黄金时段（S1/S2）；TikTok 内置可排期10天（S7） | `OBS` |
| 发布 | 标签组合 1主+2扩展、@账号、POI（S1）；多平台分发用易媒（S15） | `OBS` |
| 数据观察 | 完播率/两秒跳出/互动率/涨粉（S2/S3）；**完播率优先于播放量**（S7） | `OBS`→`INF`：完播率是北极星，发布后24h/1h/6h节点观察 |
| 复盘 | 周复盘爆款结构、月调策略（S1/S4）；用数据指导下一批（S8） | `OBS`→`INF`：复盘驱动下一批选题，形成闭环 |
| 二次利用 | 矩阵号、一条多平台改钩子（S8）；长转短（S20） | `OBS` |

**关键模式：批量生产（Batch Creation）**
- 「集中拍摄+分散发布」是最效率方式：周二拍完全周，周三至周五每天发1-2条（S4）。
- 不出镜账号：每周一次批量生成7-14条，每天发1条（S7）。
- **含义（INF）**：运营者同时管理「多条处于不同阶段的视频」，而非「一个日历上的发布时间点」。这直接支持「生产管线」而非「发布日历」作为核心工作面（见 Proposal §C）。

---

## 2. 竞品 / 工具证据（对应任务 H）

每个产品只答三件事：借什么 / 不借什么 / 对 Curis 哪个设计问题有帮助。来源类型已标注。

### 2.1 抖音创作者中心 / 抖音创作服务平台
- **借（OFFICIAL 事实）**：官方免费、数据最权威；提供粉丝画像、播放来源、完播率、互动数据，用于日常复盘（S14）。北极星指标口径（完播率/两秒跳出）可由平台回执提供。
- **不借（INF）**：它只是一个数据后台 + 基础发布入口，**没有责任链/协作/多员工概念**，不适合作为 Curis 办公室的产品形态。
- **帮助的设计问题**：验证「发布后数据观察 = System Activity（Current Executor=none）」而非员工岗位；验证 Analytics 闭环的字段来源（平台回执）。

### 2.2 TikTok Studio
- **借（OBS）**：定位是「发布与复核的控制室，不是创意工作区」——调度、发布管理、基础表现回顾、变现追踪集中一处（S6）。原生发布减少失败/元数据错配。
- **不借（OBS）**：编辑能力弱、跨渠道版本测试/团队工作流不足；团队壮大后不够（S6）。
- **帮助的设计问题**：确认 **TTK 的 Utility/发布面**应承载「发布状态/回执/表现」，而**制作核心在别处**；Studio 式的「发布后检查点」可映射为 Curis 的 Publish Result + Result Reference。

### 2.3 剪映 / CapCut
- **借（OBS）**：文生视频/自动字幕/AI配音/模板/比例转换，是成熟的**生产执行工具**（S9/S11）；CapCut 理解短视频语法（S6）。
- **不借 / 警惕（OBS）**：Script-to-Video 产出的是**草稿**，仍需人工清理（S10：「不是自主视频 Agent」）；15分钟限制、非自主（S11）。
- **帮助的设计问题**：明确 **CapCut/剪映动作 = Tool Capability（执行）**，不是 Employee Responsibility；「制作员工」调用剪映是工具执行，员工责任是「制作方向/审美/成片判断」。

### 2.4 YouTube Studio
- **借（OBS）**：账号级 + 视频级 Analytics（概览/内容/观众/互动），以及 Search performance（S5）。分层数据视图。
- **不借**：YouTube 生态与抖音差异大（横屏为主、搜索权重高）。
- **帮助的设计问题**：Analytics 应同时有「账号层」与「单 Video 层」两级，单 Video 的 Analytics 挂在 Video 对象下（Proposal §B 对象层级）。

### 2.5 Descript / Opus Clip / Captions.ai
- **借（OBS）**：Descript 转录编辑、Opus Clip 自动提取高光、Captions.ai 眼神校正/字幕（S16/S17/S20）。长转短、自动字幕是高频 Tool Capability。
- **不借（OBS）**：Opus Clip 自动发布有风险，AI 常选错上下文/夸大主张，需人工快审（S20）。
- **帮助的设计问题**：「自动提取/自动字幕」可以是 **System Activity / Tool Capability**；但「选哪条、是否发布」需员工或 CEO 判断 → 对应 Artifact Review / Needs CEO 边界。

### 2.6 Canva Video / Adobe Express
- **借（OBS）**：封面、账号视觉模板、运营物料（S15）；品牌一致性。
- **不借**：非生产核心，只是物料/封面工具。
- **帮助的设计问题**：封面/视觉模板 = Asset / Utility 预览内容，非独立 Workplace。

### 2.7 Premiere / 专业剪辑
- **借（OBS）**：精细调色/多轨/音频（S11 边界说明）。
- **不借**：门槛高，非一人公司首版核心。
- **帮助的设计问题**：确认专业剪辑属「高级能力 RESERVED」，首版不前置。

### 2.8 Buffer / Later / Hootsuite
- **借（OBS）**：跨平台排期队列、内容日历追踪发过什么/互动率（S8）；Later/Buffer 做跨平台排期（S7）。
- **不借（INF）**：它们的「日历」是**发布调度日历**，假设内容已生产完；不覆盖生产管线（S15 易媒也只是分发）。
- **帮助的设计问题**：验证「发布日历」只是**生产完成后的最后一环视图**，不能作为 TTK 默认工作面（默认应为生产管线，Proposal §C）。日历可作为 Pipeline 之上的可选「排期视图」。

### 2.9 AI 视频 Agent（HeyGen / Runway / Kling / Veo / Synthesia）
- **借（OBS）**：Agent 写脚本→HeyGen/Runway 生成→Agent 组装成片（S16/S17）；HeyGen 有 MCP 供 Agent 直调（S17）。数字人/生成 B-roll/文生视频是成熟能力。
- **不借 / 警惕（OBS）**：
  - 生成片段 20–40% 需丢弃（一致性/伪影）（S18）。
  - AI 无法可靠渲染可读文字，需程序化叠加（S17）。
  - **过度自动化敏感内容有风险**：道歉/敏感HR/创始人亲笔信应真人出镜（S19）。
  - 披露义务收紧：EU AI Act、TikTok 要求对写实 AI 媒体披露（S18）。
  - 成本：专业栈 $60–250/月 + 人工 $50–500/成品分钟（S18）。
- **帮助的设计问题**：
  - 验证「AI 生成视频」是 **Tool Capability / 高级能力**，风险高、需披露 → 可能触发 **Needs CEO（版权/合规/成本）**。
  - 「Agent-native pipeline」印证责任可拆分为 策划→脚本→生成→组装→发布，但**编辑判断/品牌声音/敏感内容仍留人**（S19）→ 支持真实 Employee Responsibility 而非全自动。

### 2.10 中国成熟运营工具（巨量算数 / 蝉妈妈 / 飞瓜 / 抖查查 / 易媒 / 即梦 / Coze）
- **借（OFFICIAL/OBS）**：
  - 巨量算数（官）：热词/趋势/人群兴趣，用于选题前期（S14/S15）。
  - 蝉妈妈/飞瓜（OBS）：爆款拆解、竞品、矩阵监控、ROI（S12/S13/S14）。
  - 抖查查（OBS）：内容结构分析（S14）。
  - 易媒（OBS）：多平台/矩阵发布管理（S15）。
  - 即梦AI（OBS）：创意素材/分镜/视觉（S15）。
  - Coze（OBS）：运营中枢，沉淀选题逻辑/模板/复盘（S15）。
- **不借（INF）**：这些是**外部专业能力**，各自只覆盖链路一段；Curis 不应「内置一个蝉妈妈」，而应把「趋势/竞品/数据」作为 **Context 来源** 与 **System Activity 数据观察** 的可连接能力。
- **帮助的设计问题**：
  - 工具清晰拆分为 选题研究 / 脚本 / 制作 / 数据复盘 / 多平台分发 → 印证业务对象与责任分层（Proposal §B/E）。
  - 「Coze 作运营中枢沉淀方法论」可映射为 Curis 的 **Knowledge / 选题库 Context**。

---

## 3. 证据充分度自评（供 Proposal 引用）

| 设计问题 | 证据强度 | 说明 |
|----------|---------|------|
| 真实工作链 11 环节 | 强（多源一致） | S1/S2/S4/S5/S8 收敛 |
| 批量生产是核心模式 | 强 | S4/S7/S8 |
| 完播率为北极星 | 强 | S2/S3/S7 |
| 发布日历≠默认面 | 强（反向证据） | S6/S7/S8/S15 |
| Script 是 Video 的子对象 | 中（推断） | 脚本紧密绑定单视频，但可复用为模板（INF） |
| Campaign 是否首版需要 | 弱（待验证） | 矩阵/主题分组多为中大型团队（S1/S4），一人公司首版可后置 |
| 真实平台 API 字段/口径 | 弱（需连接验证） | 完播率/两秒跳出等需真实回执验证（UNK） |
| AI 生成视频执行边界 | 弱（需验证） | 成本/披露/一致性丢弃率（S18）需 Curis 侧实测 |
| 责任链在多 Video 下的性能 | 弱（需验证） | 批量下 Main 栈的 Workstation 密度未实测 |

---

**结论**：外部证据强烈支持「生产管线驱动、Video 为核心追踪对象、批量生产、Analytics 为 System Activity、CapCut 等为 Tool Capability、发布日历仅为末端视图」。这些结论在 Proposal 中转为产品模型推荐，并明确标注哪些是 `INF`/待验证。

**UI Designer** · 2026-08-15 · RESEARCH ONLY
