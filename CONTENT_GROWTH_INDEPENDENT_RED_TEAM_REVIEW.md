# CURIS CONTENT GROWTH
# INDEPENDENT PRODUCT RED-TEAM REVIEW

Status: **REVIEW / STOP FOR CEO REVIEW**  
Authority Class: **REVIEW**  
Scope: 独立审查 Content Growth Professional Workspace Research；不修改 Product Authority、Frozen Authority、研究原文、IA、UI、Runtime、Schema、DB 或实现。

## 0. 独立结论摘要

现有研究已经覆盖了很多经营环节，也正确保留了 Quick Path、Per-Account Publication Truth、Target ≠ Eligibility、Human-in-the-loop 与 CEO 不维护专业参数等重要方向。但“覆盖了环节”不等于“已经证明产品可以可靠经营”。

本次红队发现：

1. Content Growth 的产品边界与当前 Frozen Product Truth 尚未完成一次无歧义收敛。
2. 从发布到反馈、评估、Learning、下一周期的“闭环”主要是流程叙事，不是已定义的可验证经营结果闭环。
3. AI AUTO 的 Confidence、Value、Cost、Strategy Envelope 和升级规则仍有伪精确风险，且关键阈值被研究明确留为 OPEN，却被描述为“不阻塞”。
4. CEO 看到的 8 类投影、8 态 Operating State、9 个 Publication 状态与多套 Employee/Runtime 状态尚未形成一个最小、可恢复、不会制造通知噪音的注意力模型。
5. 研究把多平台适配的共享比例和统一模型说得过早；视频、语言、地区、平台审核、商业化归因和账号关系仍不足以支撑“同一 Intent 可靠复用”。

**独立裁决：NOT READY FOR IA。**

原因不是缺少页面，而是 IA 之前仍有 5 个产品合同没有被 CEO 接受：Workspace 边界、最小经营闭环、自治安全/成本门、CEO 注意力模型、首批渠道与能力真相范围。

---

## 1. 审查依据与 Authority 边界

本次完整阅读了 `docs/Content_Growth_Professional_Workspace_Research/` 下的 Domain Operating Model、Product Mapping、Product Experience、Functional Interaction、End-to-End Journey、Onboarding/Daily Operating、Content Creation、Channel/Account/Publishing、Multi-Account Publishing、Error Recovery/State、AI Company Operating Experience、Configuration Ownership、AI Employee Decision、Autonomous Operating Case、CEO Operating State、CEO Daily Simulation、Unit Economics、Source/Topic/Research、Operating Matrix、Shared vs Channel、CEO Experience、User Journey、Content Employee Interaction 与 Current UI Reconciliation。

同时核对了：

- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`：Product Blueprint 是唯一 Product Authority；研究不能覆盖 Current Truth。
- `docs/03_Design/Curis_Content_Growth_Domain_Authority.md`：Office/Workspace、Channel/Channel Account、Intent、Target、Variant、Publication 与 Capability Truth 的 Frozen 语义。
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`：User Surface → Employee Operating Layer → System Runtime、Responsibility Routing、Leader/CEO 升级与不创建行业 Workflow Runtime。
- `docs/01_Product/Curis_Product_Blueprint.html`：Business → Workspace、Workspace 是完整专业经营环境、Main 不固定等于 Overview、Surface 不拥有 Work/Result/Cycle/Runtime、长期 Workspace 必须由真实 Operating Team 承载。

研究文档中的 `[CAND]`、`[INF]`、`[COMP]` 与 OPEN QUESTION 在本报告中仍按候选/推断/外部参考处理，不当作已接受事实。

---

# P0 — BLOCKER

## P0-1. Content Growth Workspace 边界仍与 Current Product Truth 存在未关闭的语义分叉

**问题是什么**  
研究把 Content Growth 定义为 Professional Workspace，并把 XHS/Douyin 定义为其下的 Channel；同时把“经营驾驶舱”设为默认 Main、列出 7 个 Surface。但 Frozen Domain Authority 仍保留 `Company → Department → Business → Office / Workspace`、Office 独立经营单元和 Business 内 Office/Workspace 的语义；Current Blueprint 又规定 Main 是当前 selected Professional Surface，且“不固定等于 Overview”。研究自己也把 Workspace 边界和 XHS 重组列为 OPEN QUESTION。

**出现在哪些研究结论**  
`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2–§4、§8；`CONTENT_GROWTH_SHARED_VS_CHANNEL_MATRIX.md` §5；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §1、§4、§8；`CONTENT_GROWTH_CURRENT_UI_RECONCILIATION.md` §1、§4、§6。

**为什么是问题**  
IA 必须知道导航 identity、Main 的默认责任、Office/Workspace 的入口与 Channel 的层级。如果这些语义未锁定，任何 IA 都会在 Context、Main、Channel switch、Business Directory、Employee Work Area 和返回路径上返工。把研究中的“待 CEO 裁决”标成“足以消费 IA”的结论，会把 Product Truth 与 Research 混成第三种真相。

**一个真实用户例子**  
小白 CEO 说“我想做成这个账号这样”，系统到底是在现有 Business 下创建一个长期 Workspace/Office，还是直接进入 Content Growth Workspace？用户回来时左侧看到的是 Business → Workspace，还是 Content Growth → Channel？如果两者都存在，哪个才是当前经营身份？

**是否违反 Curis 原则**  
是。违反“Current Authority 优先”“不创建第二套产品架构”“Workspace identity 不被 Surface/Channel 偷换”的原则。

**建议怎么处理**  
在进入 IA 前只做一次 CEO Authority Reconciliation：明确 Content Growth 的 canonical identity、Business/Workspace/Office 的关系、XHS/Douyin 的层级、Main 是否固定为默认 Surface，以及研究文档中哪些旧表述废弃。不要先画两个版本再让 UI 选择。

**是否需要继续研究**  
不需要继续扩展领域研究；需要 CEO 对现有 Authority 与候选研究做一次收敛裁决。

**是否阻塞 IA**  
**是，直接阻塞。**

## P0-2. “完整闭环”仍是阶段链，不是可证明的经营价值闭环

**问题是什么**  
研究完整列出了 Goal → Information → Signal → Opportunity → Topic → Research → Content → Asset → Channel → Publish → Feedback → Evaluation → Learning → Next Cycle，但发布后的核心业务结果没有被定义为可验证闭环：涨粉、线索、订单、广告机会、品牌资产、内容成本和风险之间如何归因、如何回到下一周期，没有一个统一结果合同。Feedback 文档提到 Lead/CRM，Unit Economics 提到业务价值，Autonomous Case 主要仍用收藏率/完播率作为终点代理。

**出现在哪些研究结论**  
`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2；`CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md` §5；`CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md` §5.9；`CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md` §3–§5；`CONTENT_GROWTH_AUTONOMOUS_OPERATING_CASE.md` 的评估叙事；`CONTENT_GROWTH_CONTENT_EMPLOYEE_INTERACTION_MODEL.md` §4–§5。

**为什么是问题**  
没有“业务结果”的定义，Evaluation 只能把平台指标重新包装成建议；Learning 可能优化收藏率，却偏离“以后接广告”或带货、企业品牌、海外转化等真实目标。这样系统可能高效地产出低价值内容，闭环只是内容生产闭环，不是公司经营闭环。

**一个真实用户例子**  
CEO 的目标是“先涨粉，以后接广告”。一个主题收藏率上涨 12%，但吸引的是无法商业化的受众，或带来投诉、平台限流和高 Token 成本。系统却给出“继续并扩抖音”，用户无法知道这对广告机会是否真的更接近。

**是否违反 Curis 原则**  
是。违反 CEO 消费 Value/Recommendation/Risk、Result 必须有 Evidence，以及 AI Company 应由 Employee 负责经营判断而非只做内容流水线的原则。

**建议怎么处理**  
下一轮只补“最小经营结果合同”：按至少 A 个人 IP、B 带货、C 企业品牌分别定义目标、可观测结果、归因边界、缺失数据时的 UNKNOWN、成本与风险返回方式。明确哪些结果 Content Growth 能真实负责，哪些只能 REFUSE/CANNOT OPERATE YET；不要先增加 Lead、CRM、Campaign 等对象。

**是否需要继续研究**  
**需要，且是业务闭环研究，不是 IA 研究。**

**是否阻塞 IA**  
**是。没有价值结果，IA 只能把流程画完整，无法决定 Main 应显示什么。

## P0-3. AI Employee Decision Model 的 Confidence/Value/Cost 仍然不可执行，存在“伪精确 AUTO”

**问题是什么**  
模型规定 HIGH 是“≥2 个独立 Evidence 一致 + Envelope 内 + 可复核 + 可逆”，MEDIUM 是单源或强推断；但没有定义 Evidence 独立性、样本量、来源相关性、时间衰减、平台数据缺失、反事实基线、预期价值、Token ceiling、预算扣除或失败成本。决策表大量使用“阈值”“Content Value ≥ 阈值”“观察次数 N”，而研究 §9 又明确这些初值仍 OPEN，却称为非阻塞。

**出现在哪些研究结论**  
`CONTENT_GROWTH_AI_EMPLOYEE_DECISION_MODEL.md` §2–§6、§7–§8；`CONTENT_GROWTH_AUTONOMOUS_OPERATING_CASE.md` §2–§5；`CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md` §3–§6。

**为什么是问题**  
“有两个来源”不等于有两个独立证据；同一新闻的转载会制造假一致。Reference 账号、行业常识和用户目标也不能自动把定位升级为 HIGH。没有可执行成本模型时，Progressive Investment 只是口号，AI 仍可能先做 Deep Research、生成多版素材、跨多平台发布，再发现价值不足。

**一个真实用户例子**  
用户贴一个热门账号链接，系统从该账号和它引用的同一新闻得到两条“独立证据”，把“新模型实测”判为 HIGH，自动启动多源 Research、三版草稿、封面生成和两个平台适配；最后只得到几十浏览，成本高于直接生成。

**是否违反 Curis 原则**  
是。违反 UNKNOWN 不得推测填充、Capability Truth 不能伪造、AI Employee 必须可审计和成本受控的原则。

**建议怎么处理**  
在 IA 前冻结最小决策安全合同，而不是继续增加 18 问字段：证据独立性、最小观察量、数据新鲜度、可逆性、单次/周期预算、最大自动步骤数、超时/循环上限、失败后降级和必须升级的条件。没有这些值时只能 WAIT、给建议或 Quick，不允许 AUTO。

**是否需要继续研究**  
**需要，需用小样本真实案例校准，不应靠继续写规则解决。**

**是否阻塞 IA**  
**是。**

## P0-4. CEO 8 态、8 类投影、9 个 Publication 状态与 Runtime 状态尚未收敛为一个可恢复注意力合同

**问题是什么**  
研究同时引入驾驶舱 8 类内容、CEO Operating State 8 态、Publication 9 态，并引用 Work/Employee 的运行状态。研究解释“不同分类维度”，但没有证明它们在重启、跨天、多个同时在途 Work、迟到回执、重复通知和状态降级时如何合并为一个唯一的 CEO 注意力结果。尤其 S2 RESULT 与 S6 READY、S3 WATCH 与 S5 IN_PROGRESS、S7 ACTION_REQUIRED 与 S4 DECISION 在真实案例中容易重叠。

**出现在哪些研究结论**  
`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §1、§4、§9；`CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md` §2–§4；`CONTENT_GROWTH_CEO_DAILY_SIMULATION.md` 全文；`CONTENT_GROWTH_ERROR_RECOVERY_AND_STATE_MODEL.md`；`CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` §5。

**为什么是问题**  
如果每个状态都可能成为卡片、通知、排序条件或返回入口，最终会重新形成 Dashboard。若多个 Work 同时产生状态，CEO 不会关心“状态正确”，只会问“现在我必须做什么”。没有 canonical precedence、去重、acknowledgement、静默、过期和跨日规则，IA 会把内部状态泄漏到前台。

**一个真实用户例子**  
CEO 离开两天后回来：一个 Research 已完成、一个抖音 Publication 在审核、一个账号 OAuth 失效、一个新选题建议待看。系统同时显示 RESULT、READY、IN_PROGRESS、ACTION_REQUIRED、ALERT 和 WATCH；CEO 仍不知道先处理授权、等审核，还是决定下一轮。

**是否违反 Curis 原则**  
是。违反 CEO 一眼知道公司在干什么/需要做什么、Quiet State 自然、Main 不是 Dashboard，以及 Runtime State 与用户侧投影分离的原则。

**建议怎么处理**  
下一轮只做注意力模型验证：对“离开/重启/跨天/多 Work/无变化/迟到回执”建立唯一主状态、最高优先动作、通知频率、acknowledge 与恢复规则。若 8 态不能减少用户判断，合并它们；不要把 8 态直接转成 8 种 UI 卡片。

**是否需要继续研究**  
需要，但范围应是状态语义与恢复证明，不是视觉设计。

**是否阻塞 IA**  
**是。**

## P0-5. 首批 Channel/Account 能力范围不真实，无法支撑研究声称的多平台闭环

**问题是什么**  
研究同时压力测试 XHS、Douyin、TikTok、YouTube、Bilibili、公众号、视频号，以及一个 Channel 多账号；但 Frozen Authority 要求具体 API、OAuth Scope、Scheduling 和能力状态由 Capability Registry/Connector 提供，UNKNOWN 必须保留。研究又把 Unavailable 平台的 RPA/手动替代、平台审核、数据回收、私信/反馈和跨平台归因放进可操作旅程，却没有锁定首批真实能力边界。

**出现在哪些研究结论**  
`CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md`；`CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` §1–§7；`CONTENT_GROWTH_SHARED_VS_CHANNEL_MATRIX.md` §2–§5；`CONTENT_GROWTH_ERROR_RECOVERY_AND_STATE_MODEL.md` 的 E07–E13；`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §8。

**为什么是问题**  
“支持平台”不仅是能不能发，还包括媒体上传、账号授权、审核、定时、删除/修改、评论/私信、Analytics 粒度、地区/语言和真实回执。若 IA 先按统一 Channel 模型铺开，后续每个平台都会产生例外入口和状态，尤其手动/RPA 路径容易被小白理解为 Curis 已经支持自动经营。

**一个真实用户例子**  
用户选择“发到 TikTok 和 YouTube”。TikTok 账号能授权但无法回收同口径数据，YouTube 可发布但视频语言、缩略图、审核和 Shorts/长视频格式不同。系统若仍显示“跨渠道增长结果”，结果可能不可比且无法解释。

**是否违反 Curis 原则**  
是。违反 Capability Truth、UNKNOWN 合法、不把局部 API/静态流程当作完整能力、不得伪造回执与产品可用性的原则。

**建议怎么处理**  
CEO 先锁定首批真实支持的 Channel × Account × Capability 矩阵：授权、发布、定时、审核、回执、Analytics、反馈、手动替代分别标 VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE。其余平台只能作为未来扩展，不进入首轮 IA 的核心路径。

**是否需要继续研究**  
**需要事实核验；不能用领域模型替代 Connector/Capability 证据。**

**是否阻塞 IA**  
**是，至少阻塞首批多渠道 IA。**

## P0-6. “贴一个链接就能从零启动”的 First Run 依赖未验证的 Reference 访问与推断能力

**问题是什么**  
研究把“账号/帖子/视频/网站链接”作为小白最自然的输入，并推断账号历史、受众、表达、增长特点、更新规律和商业化方式，再自动建立定位、Source、关键词和团队。但没有把链接无法访问、登录墙、地区限制、反爬、内容不足、样本偏差、作者商业化不可见、用户并不想模仿其商业模式等情况定义为第一类失败路径。

**出现在哪些研究结论**  
`CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md` §4.1、§8；`CONTENT_GROWTH_AUTONOMOUS_OPERATING_CASE.md` §1–§2；`CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md` §1；`CONTENT_GROWTH_USER_JOURNEY_MODEL.md` Journey A。

**为什么是问题**  
这是最核心的小白入口。如果第一步把不可见内容当事实，系统会把模仿对象误读成战略；如果第一步失败，用户必须突然理解 Source、Audience、Positioning 和 Research，所谓零配置体验就断裂。

**一个真实用户例子**  
用户贴一个海外 TikTok 账号链接，但 Curis 只能看到标题页，无法看到历史视频和受众数据。系统仍生成“科技从业者、周更、靠搜索红利、以后接广告”的定位，CEO 很难发现这些只是猜测。

**是否违反 Curis 原则**  
是。违反“事实、推断、未知分离”“未知能力显式表达”“CEO 不应被迫理解专业参数”的原则。

**建议怎么处理**  
在 IA 前只验证三条入口合同：Reference 可访问时的最小证据、不可访问时的自然降级、样本不足时必须展示 UNKNOWN 并请求最少的用户事实。不能把“解析链接成功”当作“理解账号经营”。

**是否需要继续研究**  
需要真实平台/地区/权限样本验证。

**是否阻塞 IA**  
**是，阻塞 First Run 主路径。**

---

# P1 — IMPORTANT

## P1-1. CEO 与 Employee 的责任反转仍未完全一致

**问题是什么**  
AI Company Experience 宣称 CEO 只提供 Intent/Reference/Constraint，但旅程仍要求 CEO 选择“先调研/就做这个”、选择渠道、确认下一周期、确认定位建议；另一方面 Domain/Shared Authority 又要求 CEO 对 Goal、方向、风险、不可逆外部动作负责。研究没有给出“建议确认”“相关决策”“不可替代点击”的统一判定，因此不同文档会让 CEO 在同一动作上既像客户、又像运营经理。

**出现在哪些研究结论**  
`CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md` §1–§7；`CONTENT_GROWTH_USER_JOURNEY_MODEL.md` Journey B–F；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §2、§7；`CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md` S4/S7。

**为什么是问题**  
小白体验的成本不在字段，而在每次都要判断“这次我要不要替团队做决定”。这会导致确认疲劳，也会让团队责任无法审计。

**一个真实用户例子**  
AI 已推荐 XHS 主号与抖音主号并完成适配，但 CEO 还要先点渠道、再点“就做这个”、再点“按建议继续”。如果这些都是专业判断，为什么不是 Employee；如果都只是授权，为什么显示为 Decision。

**是否违反 Curis 原则**  
部分违反 CEO/Employee ownership、Relevant Decision 与最低责任升级原则。

**建议怎么处理**  
用真实动作清单逐项标注：CEO 必须决定、CEO 只需授权、AI 可执行、AI 只能建议、AI 必须 REFUSE。清除“为了旅程完整而保留”的确认。

**是否需要继续研究**  
需要一次责任审计，不需要新页面研究。

**是否阻塞 IA**  
是，阻塞主要 CTA 和确认流，但不必阻塞全部领域研究。

## P1-2. Quick/Structured/Deep 的自动选型仍可能在用户不知情时升级成本

**问题是什么**  
研究说 AI 自动决定复杂度，并在必要时提示升级；但“多平台、品牌一致、合规敏感、需测量迭代”都可能由一句普通请求触发，且没有说明升级前是否创建 Work、调用多少工具、消耗多少预算、用户拒绝后哪些已发生事实保留。

**出现在哪些研究结论**  
`CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md` §1、§4；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §7；`CONTENT_GROWTH_AI_EMPLOYEE_DECISION_MODEL.md` §4。

**为什么是问题**  
自动选型如果不可预览，就可能把“一篇内容”变成多员工、多工具、多平台工作；如果每次都询问“继续/直接生成/讨论”，Quick Path 又不再 Quick。

**一个真实用户例子**  
用户说“帮我写一篇适合小红书和抖音的 AI 工具介绍”，系统因为“多平台+合规”升级 Structured，先做 Research 和素材生成；用户只想要一个可以马上改的草稿。

**是否违反 Curis 原则**  
违反渐进投资、成本透明和小白复杂度预算原则。

**建议怎么处理**  
定义升级前的可见边界：预计成本/时间、最大步骤、默认停止点、拒绝升级后的 Quick 结果、已发生的 Work/Token 如何记录。否则宁可默认 Quick，再由 CEO 明确要求结构化经营。

**是否需要继续研究**  
需要用真实低量场景测成本与升级率。

**是否阻塞 IA**  
阻塞 Quick 与 Structured 的入口设计。

## P1-3. Unit Economics 公式把不可获得的业务价值当作可计算输入

**问题是什么**  
“预期业务价值 × 复用次数 × 学习收益 > 结构化成本”方向正确，但普通用户通常没有内容的货币价值、增量转化、学习收益或平台机会成本数据；文档中的成本基准也不能代表 Curis 实际模型、连接器成本或失败成本。

**出现在哪些研究结论**  
`CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md` §2–§6；`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §5；`CONTENT_GROWTH_AI_EMPLOYEE_DECISION_MODEL.md` §4。

**为什么是问题**  
系统若输出“值得 Deep”却不能解释价值来源，会制造专业幻觉；若用默认常数，自动器会把不同目标、不同平台和不同账号错误比较。

**一个真实用户例子**  
个人 IP 没有历史转化数据，企业品牌有销售周期，带货账号有佣金数据。三者都说“做一篇内容”，同一个 Worth-Doing 公式不能用同一阈值判断。

**是否违反 Curis 原则**  
违反证据驱动、未知显式化和不能把候选指标冒充真实业务价值的原则。

**建议怎么处理**  
先把 Unit Economics 限定为可观察的代理指标：预计调用成本、时间、复用次数、失败风险、可获得数据；没有业务增量证据就显示“无法估算价值”，不输出伪造的 ROI。

**是否需要继续研究**  
需要，按场景分层校准。

**是否阻塞 IA**  
阻塞成本提示与升级确认，但不是所有专业 Surface 的阻塞项。

## P1-4. Intent → Variant 的统一复用假设不足以覆盖真实跨语言、跨格式与跨地区经营

**问题是什么**  
研究把 Intent 作为共享上游、在账号处分叉为 Variant，并用 HIGH_REUSE/FULL_DIVERGENCE 解决平台差异。这能覆盖简单图文适配，但没有覆盖语言重写、文化语境、字幕/配音、视频时长、素材版权、地区法律、平台搜索字段、账号受众冲突和不同商业 CTA。

**出现在哪些研究结论**  
`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2–§3；`CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md`；`CONTENT_GROWTH_SHARED_VS_CHANNEL_MATRIX.md` §1、§4；`CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` §4。

**为什么是问题**  
“复用”可能只复用了一个错误的核心判断；“完全发散”又可能失去可解释的共同来源。跨平台表现差异不能只由比例或格式决定。

**一个真实用户例子**  
中文 AI 科技内容要扩到海外 YouTube：标题、缩略图、口播、引用来源和事实核验都要重做；若仍显示为同一 Intent 的轻适配，CEO 会误以为只是翻译和裁剪。

**是否违反 Curis 原则**  
目前是产品完整性风险；若把候选复用规则当作能力则违反 Capability Truth 与 NO_CROSS_ACCOUNT_CONTEXT_LEAK 的精神。

**建议怎么处理**  
把首版复用范围限制在事实可验证、格式相近、同语言/同地区的少数 Channel；跨语言/跨地区/视频化先标为高风险 Full Divergence/人工审核，不在 IA 中假设为普通变体。

**是否需要继续研究**  
需要真实跨渠道样本和能力证据。

**是否阻塞 IA**  
阻塞跨语言/跨地区 IA；不阻塞受限首批场景。

## P1-5. 多账号模型保留了复杂性，只是把复杂性藏到了推荐卡后面

**问题是什么**  
研究让 AI 自动分析 8 个账号、推荐命名/定位/角色/默认，并在发布时按账号生成 Variant；但用户仍需要理解“主号、个人 IP、测评号、定位覆盖、覆盖发布、Target、Eligibility、Distribution Policy”。AI 自动推荐没有消除账号组合、冲突和授权生命周期。

**出现在哪些研究结论**  
`CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md` §5.6–§5.8；`CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` §1–§4；`CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md`。

**为什么是问题**  
“不显示账号树”不等于用户不需要理解结果。推荐错误时，CEO 必须能发现为什么发到这个账号、为什么另一个账号被跳过、谁承担风险。

**一个真实用户例子**  
同一 XHS Channel 下有专业测评号和个人 IP 号。系统因历史表现把同一内容推荐给两者，其中一个账号定位不匹配；用户只看到“建议发布到 2 个账号”，无法快速判断风险。

**是否违反 Curis 原则**  
不直接违反 Frozen Invariant，但违反专业深度不能被隐藏到不可解释、以及 CEO 消费风险/相关决策的原则。

**建议怎么处理**  
至少要求每次推荐提供“为什么这个账号、为什么跳过那个账号、缺什么授权、覆盖的风险是什么”，并将多账号首轮限制在少数已验证账号，不把 8 账号矩阵当作默认测试。

**是否需要继续研究**  
需要真实多账号错误案例。

**是否阻塞 IA**  
阻塞多账号默认流，不阻塞单账号 Quick。

## P1-6. 离开、重启、跨天与长期等待的连续性仍停留在逐步剧本

**问题是什么**  
发布文档对 9 个 Publication 状态写得很细，但跨周期的 Research、平台审核、OAuth 修复、数据回收失败、重复重试、已过期 Recommendation、用户暂停/删除 Work、Runtime 重启后的责任恢复和下一 Cycle 幂等没有形成同一条 continuity contract。

**出现在哪些研究结论**  
`CONTENT_GROWTH_ERROR_RECOVERY_AND_STATE_MODEL.md`；`CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` §5；`CONTENT_GROWTH_CEO_DAILY_SIMULATION.md`；`CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md` §3。

**为什么是问题**  
连续剧本能证明理想路径，但不能证明用户在任意时间回来仍能理解“事实是什么、谁负责、下一步是什么”。这是桌面 AI Company OS 的核心可靠性，而不是边缘异常。

**一个真实用户例子**  
周五提交抖音审核，周一 OAuth 失效，周二 Analytics 拉取失败，期间策略已经调整。用户回来看到旧建议仍要求“按建议继续”，但它引用的 Publication、数据和 Strategy 已过期。

**是否违反 Curis 原则**  
违反跨天连续性、事实不伪造、Work/Result/Evidence 持久化与恢复优先原则。

**建议怎么处理**  
下一轮建立四个最小证明：重启恢复、迟到回执、过期建议、暂停后恢复。每条必须明确事实时间、当前责任、是否可继续、旧结果是否失效，以及 CEO 返回时唯一主动作。

**是否需要继续研究**  
需要真实状态转换测试；不能仅靠更多文字旅程。

**是否阻塞 IA**  
阻塞 Current Work、通知、返回入口和 Result Detail 的 IA。

## P1-7. 专业深度与可发现性没有被证明，默认隐藏可能变成能力缺失

**问题是什么**  
研究把 Source 管理、全量 Signal、评分、Research Scope、版本比稿、素材库、Connector 健康、逐账号时间精调全部降为 Expert Only/Utility；同时又要求用户能添加指定 Source、深入 Research、修改内容、查看 Analytics、处理反馈。没有定义一个不依赖运营知识的发现路径，也没有证明 Utility 能承载这些高密度工作。

**出现在哪些研究结论**  
`CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md` §3–§5；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §5、§8；`CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md` §1–§5；`CONTENT_GROWTH_CURRENT_UI_RECONCILIATION.md` §5–§6。

**为什么是问题**  
Simple ≠ invisible. 当 AI 判断错、用户有指定来源、需要查证或要改一个账号时，用户必须能找到控制点，否则只能重新对话，形成不可解释的“黑箱员工”。

**一个真实用户例子**  
用户说“以后必须看这个官方博客，别看那个竞争账号”，系统说自然语言可处理，但用户找不到 Source 是否已生效、何时采集、影响哪些 Research。

**是否违反 Curis 原则**  
违反 Progressive Disclosure、Professional Workspace 既要简单又要可用、以及 Result/Evidence 可追溯原则。

**建议怎么处理**  
定义“CEO 可发现的三条专业入口”：指定 Source、查看证据/未知、修正/重做结果；其他深度能力仍由 Employee Work Area 承担。先证明入口和返回，不增加一级导航。

**是否需要继续研究**  
需要可用性验证。

**是否阻塞 IA**  
阻塞 Utility、Context 与返回路径的 IA。

## P1-8. Domain 对象、Artifact 投影与 Work/Result 真源仍有重复建模风险

**问题是什么**  
Product Mapping 说 Signal/Opportunity/Topic 是 Artifact + Surface Projection，Research 是 Work+Result+Evidence；但其他研究又把 Source、Signal、Opportunity、Topic、Brief、Draft、Asset、Variant、Publication 作为连续专业对象，并为它们分别设计列表、状态、操作和负责人。若没有 canonical truth map，IA 会把 Artifact、Projection、Work、Result 画成多个可编辑实体。

**出现在哪些研究结论**  
`CONTENT_GROWTH_PRODUCT_MAPPING_MODEL.md` §2–§4；`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2–§6；`CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md`；`CONTENT_GROWTH_CONTENT_CREATION_MECHANICS.md`；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §4–§5。

**为什么是问题**  
同一“选题”若同时有 Topic、Topic Work、Brief、Result、Artifact 五个可编辑入口，会出现谁是当前状态、谁能修改、谁产生 Evidence、用户改哪个才生效的问题。Research 说不新造 Runtime primitive，不能阻止 UI 端重复造对象。

**一个真实用户例子**  
CEO 在选题卡上点“就做这个”，随后在内容页修改标题，又在 Research 结果里看到旧标题。系统必须明确哪一个是 Intent，哪一个只是历史 Artifact，哪一个 Result 已被替代。

**是否违反 Curis 原则**  
是。违反复用 Company OS shared objects、禁止第二套 Task/Workflow/Runtime/Truth 的原则。

**建议怎么处理**  
IA 前补一张 canonical object/truth/authority map：每个概念只有一个真源、一个可编辑入口、一个生命周期、一个结果回流路径；其余全部是投影或不可编辑引用。

**是否需要继续研究**  
需要，但属于模型收敛而不是增加对象。

**是否阻塞 IA**  
**是，阻塞对象页、详情页和编辑路径。**

## P1-9. 反馈与商业化路径超出了当前 Content Growth 的已证能力

**问题是什么**  
研究把评论、私信、Mention、投诉、高意向线索归一为反馈，并进一步建议转 Signal、Opportunity、Lead、外部 CRM；但 Content Growth 的主闭环和 Frozen Domain Authority 没有确认 Lead/CRM/商业化归因的责任、权限、数据边界和真实 Connector。研究又把“以后接广告”作为 First Run 目标，却没有可落地的商业化结果。

**出现在哪些研究结论**  
`CONTENT_GROWTH_CONTENT_EMPLOYEE_INTERACTION_MODEL.md` §4；`CONTENT_GROWTH_AI_COMPANY_OPERATING_EXPERIENCE.md` §4；`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2；`CONTENT_GROWTH_CURRENT_UI_RECONCILIATION.md` §1。

**为什么是问题**  
这会让用户以为 Content Growth 已经覆盖 CRM、线索与商业化；也会把外部用户数据、私信和留资带入新的权限/隐私/隔离问题。若不能落地，反馈 Surface 只是“社交收件箱”而不是经营反馈。

**一个真实用户例子**  
带货账号收到高意向私信。AI 识别为 Lead，但没有官方留资能力或 CRM 连接；用户不知道是继续在平台内回复、丢弃，还是手动跟进，系统也不能证明转化。

**是否违反 Curis 原则**  
违反 unknown capability、数据隔离、不要把候选集成冒充产品能力的原则。

**建议怎么处理**  
首轮把反馈限定为“已验证可读取/归一化的反馈事实”，商业化与 CRM 只保留明确 GAP；不要进入 IA 主导航，直到有 Capability/权限/结果证据。

**是否需要继续研究**  
需要能力与数据边界研究。

**是否阻塞 IA**  
阻塞 Feedback/Commercial IA，不阻塞核心内容生产。

---

# P2 — OPTIMIZATION

## P2-1. “16 阶段、7 Surface、8 类结果、8 态”仍然是过度专业化的叙事负担

**问题是什么**  
研究强调不把 16 阶段画成 16 页，但仍把 16 阶段、7 Surface、8 类投影、8 态行为层并列作为 IA 消费输入。即使后台不全展示，团队在实现和文案中仍会围绕这些分类组织系统。

**出现在哪些研究结论**  
`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2–§4；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §1、§4、§9；`CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md` §2。

**为什么是问题**  
它可能把“专业完整”误变成“模型完整”。删除部分中间分类，用户仍能完成“说意图→得到结果→做相关决定”；如果分类不能改变责任、恢复或结果，就不应成为 IA 前置约束。

**一个真实用户例子**  
用户只想每周偶尔发一条内容，却在后台被归入选题、研究、内容、渠道、增长与评估六个专业工作面；她并不需要经营一个持续团队。

**是否违反 Curis 原则**  
部分违反轻量与渐进工作形态原则。

**建议怎么处理**  
IA 只消费最少的 CEO 任务入口、当前结果、相关决定、专业深入口和恢复入口；把 16/7/8/8 留作研究索引，不作为页面数量或导航承诺。

**是否需要继续研究**  
不需要；在 IA 阶段做删除测试即可。

**是否阻塞 IA**  
不阻塞，但必须作为约束携带。

## P2-2. “推荐 3 个选题/3 条变化/1–3 个草稿”有伪精确风险

**问题是什么**  
研究多处使用固定数量压缩复杂度，但没有说明数量是否由信息量、置信度、CEO 注意力和成本决定。固定三条可能制造内容，也可能隐藏唯一高价值机会。

**出现在哪些研究结论**  
`CONTENT_GROWTH_SOURCE_TOPIC_RESEARCH_INTERACTION.md` §2、§4；`CONTENT_GROWTH_USER_JOURNEY_MODEL.md` Journey A/B；`CONTENT_GROWTH_CONTENT_CREATION_MECHANICS.md`；`CONTENT_GROWTH_CEO_OPERATING_STATE_MODEL.md` S2/S3。

**为什么是问题**  
对小白来说，三张卡不一定比一张更简单；对 AI 来说，固定数量会成为“必须填满”的诱因。

**一个真实用户例子**  
本周只有一个有证据的机会，系统仍生成两个低置信推荐，CEO 以为三者等价。

**是否违反 Curis 原则**  
违反 UNKNOWN/证据分级的表达要求，但不构成核心架构冲突。

**建议怎么处理**  
使用“最多 N、可少于 N、允许为空”的投影规则，理由优先于数量。

**是否需要继续研究**  
不需要，后续按真实样本校准。

**是否阻塞 IA**  
不阻塞。

## P2-3. Calendar、Channel Module 与反馈入口仍留有未关闭的 IA 争议

**问题是什么**  
Calendar 是内容内视图还是独立入口、Channel 是否有可见 Module、Feedback 是否独立 Surface，研究都给出了相反意见或 OPEN QUESTION。它们不是 P0，因为核心路径可以先不依赖；但若在 IA 中提前冻结，会造成导航返工。

**出现在哪些研究结论**  
`CONTENT_GROWTH_MULTI_ACCOUNT_PUBLISHING_JOURNEY.md` §7；`CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` §4、§6；`CONTENT_GROWTH_CURRENT_UI_RECONCILIATION.md` §1、§6。

**为什么是问题**  
这些入口服务专业用户，不应被小白默认看到，也不能因“完整”而升级为一级导航。

**一个真实用户例子**  
高频运营人员需要按账号查排期，偶尔发内容的 CEO 完全不需要 Calendar。若两者共用同一默认 IA，都会被另一方打扰。

**是否违反 Curis 原则**  
不直接违反；是 progressive disclosure 与用户角色适配风险。

**建议怎么处理**  
先保留为待验证深入口，不在第一版 IA 承诺一级导航；由真实用户任务决定。

**是否需要继续研究**  
需要轻量可用性验证。

**是否阻塞 IA**  
不阻塞主 IA，但阻塞这些入口的最终层级。

## P2-4. 研究的外部实践与平台事实证据不足以支撑部分强结论

**问题是什么**  
多个关键判断标为 `[COMP]`、`[REAL]` 或 `[INF]`，例如“60–70% 价值共享”“平台规则/定时/反馈边界”“深度与内容保质期绑定”，但没有在研究交付中提供可复核来源、适用时间、地域和失败边界。

**出现在哪些研究结论**  
`CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` §2–§3、§5；`CONTENT_GROWTH_SHARED_VS_CHANNEL_MATRIX.md` §2–§4；`CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md` §2；各平台 Publishing 研究。

**为什么是问题**  
这不会立即破坏用户旅程，但会把推断误带入后续 Authority、Capability 或 IA；平台能力和成本尤其容易漂移。

**一个真实用户例子**  
系统依据旧的平台定时规则给出“明早 9 点发布”，平台实际只允许某类账号或某地区操作，用户以为是 Curis 失败而不是能力条件不满足。

**是否违反 Curis 原则**  
若保持为研究推断，不违反；若进入产品真相，则违反 Truth Governance 与 UNKNOWN 规则。

**建议怎么处理**  
进入 IA 前只消费 `[CURIS-AUTH]` 与已验证 Capability；所有外部事实携带来源、日期、地区、账号类型和状态，不把比例或竞品结论冻结成产品规则。

**是否需要继续研究**  
后续核验即可，不需扩大本轮产品模型。

**是否阻塞 IA**  
不阻塞受限 IA；阻塞具体平台能力文案。

---

## 2. 真实用户压力测试结果

| 场景 | 当前模型能否成立 | 主要断点 |
|---|---|---|
| A. 个人 IP 涨粉 | 部分成立 | 结果仍偏平台互动，未证明个人 IP 的长期价值与身份风险；多账号推荐可能过度经营 |
| B. 带货账号 | 未证明 | 商品/佣金/库存/归因/合规与内容目标没有形成可验证闭环 |
| C. 企业品牌内容 | 部分成立 | 多级审批、品牌规则、法务责任、素材版权和组织责任未落地 |
| D. 海外 TikTok / YouTube | 未证明 | 跨语言、地区、视频格式、数据口径、授权和审核能力未验证 |
| E. 偶尔发内容、不持续经营 | 可以走 Quick，但有过度升级风险 | 自动识别 Deep/Structured 可能把轻量用户拖进长期 Workspace 语义 |
| F. 历史内容多、多个成熟账号 | 未证明 | 迁移、去重、历史指标归因、账号定位冲突、批量授权与数据成本未定义 |

结论：模型不是“所有场景都失败”，但当前证据只足以支持受限的单账号/低量/同语言/低风险内容路径，不能支持研究中声称的通用 Content Growth Company OS。

---

## 3. 独立裁决

### NOT READY FOR IA

进入 IA 前下一轮只需要补以下五件事，不需要继续增加页面、Surface、员工或领域对象：

1. **Authority Reconciliation**：锁定 Content Growth 的 canonical identity、Business/Workspace/Office、Channel/Account 与 Main/Surface 关系。
2. **最小经营结果合同**：至少覆盖个人 IP、带货、企业品牌；明确从发布数据到 Value/Recommendation/Learning 的边界，不能获得的数据显式 UNKNOWN。
3. **自治安全与成本门**：定义 Evidence 独立性、最小观察量、数据新鲜度、Token/时间/外部风险上限、最大自动链长度、循环/重试/超时与升级条件。
4. **CEO 注意力与连续性证明**：用离开、重启、跨天、多 Work、迟到回执、OAuth 失效和无变化场景收敛唯一主状态与下一动作；不要把状态直接变成卡片。
5. **首批真实 Channel Capability Matrix + First Run fallback**：只锁定有证据的 Channel × Account × Capability；验证链接不可访问、样本不足、地区/权限失败时的最小用户路径。

完成以上五项后，仍需保留的 IA 约束是：Quick 不被专业系统污染；长期 Workspace 必须由真实 Operating Team 承载；CEO 不配置员工/Workflow/专业参数；Surface 不拥有 Runtime Truth；Target 与 Eligibility 分离；Publication 按账号独立记录；专业深度通过可发现的按需入口提供；UNKNOWN 不被压缩成肯定答案。

**STOP FOR CEO REVIEW。**
