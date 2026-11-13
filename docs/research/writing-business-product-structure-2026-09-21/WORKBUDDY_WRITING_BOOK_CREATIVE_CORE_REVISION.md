# WorkBuddy「html 探索」— Writing Book创作内核定向修订

Authority Class: RESEARCH
Status: Review
Disposition: CEO已授权执行本地HTML修订；不是Authority变更或最终验收
Owner: WorkBuddy
Next Gate: 完成交CEO / Codex Review，STOP，不自评最终Accepted

继续你已交付的Writing Business HTML，直接执行修订，不只写计划。CEO会明天检查。

工作目录：
`/Users/yy/Documents/Curis AI Workspace/WRITING_BUSINESS_HTML_EXPLORATION/`

保留六区经营链和现有视觉方向。本轮重点补Book创作内核，不重做整个应用，不把工作区变成经营后台加简单写字框。

## 先读输入

研究目录：`/Users/yy/Documents/Curis AI Workspace/docs/research/writing-business-product-structure-2026-09-21/`

- `CURIS_WRITING_BUSINESS_PRODUCT_STRUCTURE_CANDIDATE.md`：**新增§13是本轮核心合同，完整读取**。
- `book-depth-audit/BOOK_CREATIVE_DEPTH_REVIEW.md`：当前问题与实际复现。
- `CURIS_WRITING_BUSINESS_RELATIONSHIP_MAP.md`、`CURIS_WRITING_BUSINESS_GAP_AUDIT.md`：保留经营/发布/反馈关系，旧“闭合”结论不替代本轮创作验收。

同时直接读取创作依据，不能只读摘要：
- `/Users/yy/Documents/Curis AI Workspace/docs/research/professional-workspace-product-language-2026-09-21/WRITING/CURIS_WRITING_PRODUCT_LANGUAGE_CANDIDATE.md`
- `/Users/yy/Documents/大魔王知识库/资料/NovelFlow：本地 AI 长篇写作工作台功能拆解与工作原理.md`（重点§4.1–4.3）
- `/Users/yy/Documents/大魔王知识库/资料/世界档案馆：AI 长篇写作智能体产品结构研究.md`（大纲/细纲、人物、故事状态）
- `/Users/yy/Documents/大魔王知识库/Curis_Workspace_完整知识库/03_技术架构/Curis 写作 Agent 产品框架与功能定义.md`（重点§7.1–7.4、7.12）

这些是研究输入，不要求照搬全部模块；采用范围以新增§13为准。继续消费既有Visual Language Candidate的正文空间、员工责任、渐进披露与诚实状态原则。

## 必须落实

1. **开书与定位**可构思、编辑、确认、后补：题材、读者分区、原创核心、视角/风格等。男频/女频与都市/玄幻/科幻等不是同一个分类维度；不强制一次填完。
2. **背景、人物、主支线、大纲、场景**有真正工作操作：创建/编辑/讨论→具体候选→确认应用→后续写作引用。包括人物动机/弧线/声纹/知情、世界限制、总纲到章/场景、结局方向及伏笔。不要用几张静态表或通用“提出变更”替代。
3. **正文可实际写、改、保存**；从章纲和场景进入写作，能看到相关依据。Mock生成也要形成绑定本书本章的具体可编辑产物，随后部分采纳/拒绝/确认；不是固定“收到”加一条Work记录。
4. **审稿、校对、表达质量**分别可触发、查看带位置/证据的问题、局部修改、作者选择和复查。表达质量覆盖模板化、重复表达、人物声纹趋同等，不做规避AI检测或假“去AI率”。
5. **变更与连续性**：计划不是已发生事实，正式稿不是线上稿。改人物/设定/大纲后列影响，不静默全书覆盖；旧版本与已发事实保留。
6. **明确修掉已复现错误**：新空书Story State不得回退B-01；卷章不得每卷重复展示全书章节。检查所有创作入口的Book范围，不能只修这两处表现。无资料显示真实空状态并给创建入口。

设计自主：自行决定Book内部工作面、合并方式及交互，不能机械做十个Tab/卡墙，不能把能力藏到不可发现。保中文用户语言、正文阅读空间、直接操作与编辑交流。不给所有作者强制同一种先后顺序。

## 验收必须超出原第43章样例

实际浏览器完成并记录：
- 新故事：定位→背景/人物→主支线与结局→大纲/场景→生成/手写→审稿/校对/风格检查→局部采纳→同步→发布队列。
- 先手写后补规划；少量自有测试稿导入、分类、接续。
- 改人物知情或规则→影响检查→修订/复查。
- 两本书＋新空书来回切换，正文/大纲/人物/对话/审校不串，刷新保持本地状态。
- 原市场→作品→发布→反馈归因→Learning→下一章回归。

AI与平台可以Mock，文字、编辑、候选、确认、保存和下游引用要真实改变本地状态。超出Mock能力明确说未支持；不能以假产物冒充理解自由输入。无Console Error不等于产品成立。

## 交付与边界

只改上述HTML探索目录，保原结构和既有数据；必要的本地状态升级应保用户已存编辑，不通过清空localStorage让测试通过。修订前留轻量备份，旧证据不覆盖。共享CSS/JS/data＋单一index.html；index.single.html仅通过现有构建脚本再生成。

在目录内提交简短修订说明、能力→实际入口映射、本轮浏览器截图及索引、路径前后状态、Console Error与仍未覆盖/Mock项。所有验证针对当前构建。不得修改Curis Authority、正式Frontend、Runtime、数据库；不真实发布、登录、付费、绑账号或使用凭据；不commit/push。

完成后输出实际入口、截图、已走通及未走通路径、已修问题与剩余问题。STOP FOR CEO / CODEX REVIEW。不要等待逐项确认再完成这些已授权的普通本地修订；若出现范围外真实阻塞，准确报告，不编造通过。
