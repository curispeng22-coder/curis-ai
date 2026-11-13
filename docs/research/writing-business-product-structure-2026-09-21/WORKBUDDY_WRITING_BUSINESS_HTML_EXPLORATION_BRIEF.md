# WorkBuddy — Writing Business HTML Exploration Brief

Authority Class: RESEARCH
Status: Review
Disposition: CEO已接受三份Writing候选作为本轮探索输入；本合同不升级Current Authority。
Owner: WorkBuddy（设计与实现）；CEO（Review）；Codex（交付后的产品对账与验收）
Next Gate: WorkBuddy交付 → CEO / Codex Product Reconciliation；不自动进入正式开发。

## 当前修订入口

首版已交付。本轮执行[定向修订指令](WORKBUDDY_WRITING_BOOK_CREATIVE_CORE_REVISION.md)，重点消费主合同§13；原20项不得作为创作完整性的上限。原Brief作为业务背景保留。CEO已授权直接开展本地HTML修订，完成后交Review，不修改Authority。

## 任务

设计并实现一套统一、可交互的 **Writing Business Professional Workspace HTML Application**。它帮助作者持续研究市场、创作作品、连载变现、理解读者、沉淀经验并改善下一次创作，不是一个AI聊天写作工具。

从六个长期专业区开始：**经营、市场与方向、作品、连载发布、读者与收益、写作经验**。覆盖主文档20项页面合同的能力与交接，但不要机械生成20个页面；可以合并Detail、Surface或Mode。探索中发现结构问题，记录建议与证据，不静默删去业务链。

## 必读输入

路径均位于本机，先完整读取：

1. `/Users/yy/Documents/Curis AI Workspace/docs/research/writing-business-product-structure-2026-09-21/CURIS_WRITING_BUSINESS_PRODUCT_STRUCTURE_CANDIDATE.md`
2. `/Users/yy/Documents/Curis AI Workspace/docs/research/writing-business-product-structure-2026-09-21/CURIS_WRITING_BUSINESS_RELATIONSHIP_MAP.md`
3. `/Users/yy/Documents/Curis AI Workspace/docs/research/writing-business-product-structure-2026-09-21/CURIS_WRITING_BUSINESS_GAP_AUDIT.md`
4. `/Users/yy/Documents/Curis AI Workspace/docs/research/professional-workspace-product-language-2026-09-21/CURIS_PROFESSIONAL_WORKSPACE_VISUAL_LANGUAGE_BASELINE_CANDIDATE.md`

视觉质量参考（只读，不复制页面结构）：

- `/Users/yy/Documents/Curis AI Workspace/CURIS_COLOR_DIRECTION_EXPLORATION/06_curis_hybrid.html`
- `/Users/yy/Documents/Curis AI Workspace/CONTENT_GROWTH_FULL_VISUAL_EXPLORATION/index.html` 的Production Overview。

参考其简洁、干净、紧凑但不拥挤、关系清楚、易扫读的质量。06 Hybrid是本轮允许参考的探索方向，不将其配色升级为正式token或修改Visual Standard。旧视觉候选若存在不同色彩方向，按此范围记录差异，不混成新的Authority。

## 设计自由与产品底线

你负责页面组织、交互与视觉设计；本合同不规定组件、列数、表格、Card、固定四Pane或按钮位置。市场、经营、数据和正文可以采用不同表达方式。共享Grammar，不共享万能布局，不能做Content Growth换皮。

Book内部围绕 **Manuscript / Story State / Employee / Candidate / Author Decision**：正文有足够阅读和编辑空间；员工是长期编辑，责任与当前工作、产物相连，不是聊天插件或员工卡墙。保留自然的直接操作与讨论；对话必须有正确对象、接收人与版本范围。

守住以下事实：

- Book身份贯穿创作、发布和反馈；市场Reference/Pattern可以进入定位和章目标，但不是本书Canon。共享Work、Result、Evidence、Learning只作同一事实的引用。
- Candidate不能静默覆盖正式稿；作者可讨论、修改、拒绝、部分采纳，正式应用后保旧版本。普通作者选择不表现为故障。
- Accepted ≠ Applied ≠ Published。发布队列、人工提交、回执、外部效果未知必须区分；未知不默认重发。
- 数据关联实际发布版本与时间窗；不同平台指标不硬合并，Unknown不填0，不编造章节/段落收益。归因分Observation、Evidence、Hypothesis、Learning、Recommendation，不把相关性说成因果。
- Learning有适用范围、反例与使用回访，能回到下一章/下一作品；不自动停书、不绕平台AI规则、不暗示真实后台持续运行。

## 必须可走通的探索路径

用少量相互关联、明确标注的虚构作品和数据完成路径，不做互不相关的展示页。

| 路径 | 用户必须能实际做什么 |
|---|---|
| 市场进入创作 | 观察来源→打开/讨论参考拆解→形成并修改方向→确认→创建或进入Book；参考随目标进入创作 |
| 长期创作 | 进入Outline/Story State与当前章→找负责编辑交流→返回Candidate→部分采纳/拒绝→确认正式稿→查看版本及故事状态影响 |
| 连载与反馈 | 从正式章加入发布队列→选择目标及节奏→走人工/Mock提交与回执→进入同一本书的数据、评论、收益；保留等待/未知路径 |
| 归因与学习 | 从趋势或评论定位已发布章节→阅读正文与分析依据→形成限定范围的经验→用于下一章、方向或经营决定，并可返回原证据 |
| 日常维护与恢复 | 管理关注来源、平台作品映射、数据补录/订正；切换Book不串稿/对话，返回保范围；刷新/重开行为明确且可验证 |

关注频率、Provider执行、平台回执可以Mock，但增改暂停等本地交互要真实更新原型状态，不能只弹“成功”。使用本地保存模拟长期连续性即可，不搭后端；说明存储范围并提供明确的演示重置方式。外部发布、真实登录、支付、真实账号绑定均不执行。未知平台字段沿用输入文档的缺口，不为让图表好看自行补造。

## 实现与交付

只在独立目录工作：

`/Users/yy/Documents/Curis AI Workspace/WRITING_BUSINESS_HTML_EXPLORATION/`

交付一个入口 `index.html`，配共享CSS、JS、data及必要Mock资产；各区、Book和详情在同一应用内切换，不采用每页一个HTML。已有同名目录时先检查，保留已有成果，不覆盖无关文件。中文用户字段；不接真实服务，不修改Curis Authority、Runtime、正式Frontend或其它探索，不commit/push。

README简要提供：入口及本地运行方法、主要交互、20项合同如何映射到实际Surface、Mock与持久化范围。另交CEO Review截图及简短索引，包含六区主要状态和Candidate部分采纳、正式版本、发布等待/回执、内容归因、Learning回流等关键路径；截图来自真实浏览器操作。

## 完成前自查与报告

在Chrome/Chromium实际运行并点击主链；不得只靠源码扫描或截图宣称可用。检查六区是否够用、入口/返回是否闭合、正文空间是否适合长期写作、员工是否持续承担责任、作者决定与版本是否清楚、发布是否接到反馈、经验是否回到创作。保留设计自主性，同时记录不能顺畅表达的产品关系。

交付时只需清楚报告：

- HTML入口、截图位置与运行方法；
- 已实际走通的路径，以及无法走通的路径；
- 实际发现的产品断点、实现限制及建议，区分两者；
- Console Error数量与具体问题；
- 哪些交互真实更新本地状态，哪些是Mock或尚未实现。

成功标准是完整业务可以被真实体验和评审，不是按钮数量或截图数量。不得把Mock发布/分析称为真实平台适配完成。

完成后STOP FOR CEO / CODEX REVIEW。后续由Codex做Product Structure Reconciliation、Interaction Review、Gap Review及Accept / Targeted Revision；本轮不自行宣告最终产品验收或修改Authority。
