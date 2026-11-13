# Curis Music Business — 断点审计

Authority Class: REVIEW
Status: Review
Disposition: CEO ACCEPTED PRODUCT CANDIDATE + HTML EXPRESSION；EXECUTION GAPS OPEN / NOT FROZEN
Baseline: 工作区 HEAD 78cacbd0857cc36c9f3fe0e4b11346489993b728（含既有未提交资料）
Updated: 2026-09-23
Module: Music Business
Owner: CEO / Product；后续专项证据由对应责任Holder承担
Supersedes: None
Target Authority: 本轮不修改Authority；CEO已接受Candidate，正式吸收范围仍需独立Gate。
Next Action: 保留已接受的产品表达；按Closure分流Final UI与专项能力证据，本轮不派发开发。
Next Gate: Final UI Master或真实Capability/Platform/Runtime专项验证；Authority吸收另需CEO Gate。

审计输入、文件级Authority Class/Status和外部核查边界见[结构候选§12](CURIS_MUSIC_BUSINESS_PRODUCT_STRUCTURE_CANDIDATE.md#12-来源定向补证与旧稿处置)。配套[关系图](CURIS_MUSIC_BUSINESS_RELATIONSHIP_MAP.md)。本轮是研究/合同对账，不是源码、Browser或Desktop能力验收。

## 1. 总体判定

旧Music Language已覆盖核心对象与五区，不能称“完全缺少经营闭环”；但前置创作选择、评论归因、经验应用证据和逐页动作不够完整。更早材料还有已被最新候选纠正的过度承诺，不能重新带入。

原研究轮次将上述断点补成可检查合同，并选择六区/22个工作面或详情。随后CEO已接受Music HTML Exploration的产品表达；这只提高**产品关系的探索证据等级**，不提高外部执行能力等级。**合同与HTML链条可检查，不等于功能已实现，更不等于真实音乐业务已验收。** 发布与数据字段、许可和账号可用性仍存在外部证据缺口。

下表原“合同补齐”指2026-09-22文档级覆盖；2026-09-23的HTML产品表达验收另见§2.1与[Closure](CURIS_MUSIC_HTML_EXPLORATION_CLOSURE.md)。没有真实Provider调用、平台上传或真实经营数据采集；当前真实执行状态仍为 **NOT VERIFIED**，不是“全部可用”。

## 2. 逐断点对账

| ID | 断点 / 既有证据 | 本轮补齐方案及落点 | 关闭所需证据 | 当前Disposition / Owner / Next Gate |
|---|---|---|---|---|
| G01 | 市场研究不真正进入Direction：M5已有关系，具体采用/排除记录不足 | R1→R2→R3→R4；每个方向携Pattern/来源、采用特征和原创差异；结构§4–5 | 一方向可反查市场证据并在制作输入见到对应要求 | 合同补齐候选；Product→CEO Review，之后研究/制作Holder专项验证 |
| G02 | 用户构思前缺少可选定位：M5有Direction字段，尚未明确前置选择、继承/冲突 | R3定位→R4构思，风格/标签/人群/语种/市场等14维；可不确定，非全必填 | 用户选择、暂存、改选、下游实际输入与冲突处理闭环 | 合同补齐候选；Product→CEO Review；制作验证输出是否遵守 |
| G03 | Reference只是链接或一张画像：旧原型V1有样例但非音频分析 | R2逐项拆结构/Hook/BPM/歌词/声音/封面，证据类型与版本锚点 | 合法可听样本→标注→Pattern→原创方向，缺音频诚实未知 | 产品补齐；研究Holder→合法来源及音频分析验证 |
| G04 | Provider结果缺版本关系：M2把一次请求与一个版本混用 | Work→多请求→多独立Candidate；记录每个输出和父版本 | 同请求两音频可独立试听/选Master，切Provider不断链 | 合同补齐候选；制作/后续开发→正式Issue后的真实调用验证 |
| G05 | 歌词只作Prompt输入，用户改词无回路 | P2手写/候选/局部采纳/版本保护，输入歌词与实际唱词核对 | 自写/导入→候选→后改→拒绝过期覆盖→成品歌词一致 | 合同补齐候选；制作Holder→创作动作验证 |
| G06 | Candidate成为Master的责任模糊 | P4/P5有权Choice绑定确切音频、理由与质量证据；Master非版权/发布批准 | 有权者批准指定版，换版保旧记录、检查包过期 | 合同补齐候选；Product/制作→CEO Review及后续版本验收 |
| G07 | Master未可靠进入发行 | D1包引用不可漂移的Master快照；平台字段按证据预检 | 改当前Master不偷偷改旧包；纯音乐不强填歌词 | 合同补齐；发行Holder→选定平台预检证据 |
| G08 | 发布无真实回执或提交当上线：V1本地Mock自动推进 | D2/D3分别记录动作、收件、审核、上线/失败/Unknown | 合法实际提交和上线证据，人工报告与核验来源分明 | 外部执行未验证；发行Holder→平台样本验证 |
| G09 | 发布后数据回收假设过强：M3四模式对指标打勾但无字段证据 | A2四模式逐字段核可得性；无API有条件人工/导入，不补造指标 | 指定账号可见字段、导出/读取权限、真实样本及映射 | OPEN / 平台证据；分析Holder→账号后台定向核查 |
| G10 | 数据不能准确关联Song/Version/Platform：旧M3主张外部编号作主键 | 内部Song+Master+Publication，外部ID为映射；待映射不强入比较 | 同名歌、旧版新版本、多平台样本关联无误 | 合同补齐；分析/发行Holder→映射验收 |
| G11 | 评论只能列举，不能回制作 | A3主题簇+原文+反例+采样范围；时间点无证据标推断 | 一评论簇→原文→发布版/片段→修改Work→回原Song | 合同补齐；分析/制作Holder→合法评论样本验证 |
| G12 | “播放上涨”代替归因，内容锚点和反证不足 | A4五层分析，同时看Hook/歌词/人声等与曝光/时间/平台环境 | 同窗口内容及证据、替代解释、不可得项、可验证建议 | 合同补齐；分析Holder→真实数据后有限归因Review |
| G13 | 分析直接冒充Learning | Analysis→候选→接受范围，创作偏好/生产经验/市场学习分开 | 结论来源与性质、正反例、验证次数可回查 | 合同补齐；分析/有权用户→经验接受Review |
| G14 | Learning不进入下一首 | L1选用→Direction/制作输入→应用记录→L2验证；具体改变可读 | 至少一次采用及下一首实际输入，后续结果（含失败）回写 | 合同补齐；研究/制作/分析Holder→跨歌曲应用验收 |
| G15 | Result不知道回哪里 | 关系图§4逐交接列接收对象、负责人、证据和失败返回 | 生成/发行/分析各Result可打开原Song/版本及下一动作 | 合同补齐；各Work Owner→后续接续验收 |
| G16 | Human Decision位置不清，默认Leader包办所有审美/版权 | Choice/Gate/Operating分目的；能力和权限按实际授权 | 常规选版、发布授权、超预算策略三个场景边界清楚 | 合同补齐；Product→CEO Review，不能靠角色名猜权限 |
| G17 | Provider错误当Employee/一区一人：M2旧稿、V1明确缺口 | 沿M5开放Assignment；责任可兼岗，Provider是来源 | 同Employee多责任、多Employee协作及换Provider不改身份 | 合同已纠偏，旧稿不回写；后续实现证据NOT RUN |
| G18 | 长期资产归属不清/临时音频URL失效 | Business/Song持有资产；合法保存、完整历史、恢复为新候选 | 音频真实可取回、失效诚实、员工更换和恢复无丢失 | 合同补齐；资产/开发责任→正式Issue后持久化验收 |
| G19 | 次日无法恢复经营状态：V1明确零持久化 | 结构§10规定未决、请求、包、回执、观测/学习及下一检查 | 关闭重开/断线/未知效果/用户后改冲突，恢复不重复外写 | OPEN / 实现证据；后续正式Issue，当前未开发 |
| G20 | API文档/历史READY冒充接入和许可 | E2/E3仅DOCUMENTED；具体账号/费用/权限/用途逐项验证 | 授权账号真实调用、音频回收、费用/失败恢复及适用许可 | OPEN / Provider；能力验证Owner→选定来源专项证据 |
| G21 | 汽水具体字段、固定审核时长、收益单价、AI要求被写死 | 撤出本候选承诺；E1仅官方公开类别，字段均按实际核验 | 当前目标账号/作品形态的要求与账单；不是CEO批准即可证明 | OPEN / 平台；发行/分析→定向核查 |
| G22 | 收益/成本口径不一致造成假利润 | A5展示可得收益、来源/币种/账期/粒度与缺口；资金结算/到账不作Music业务面；实际Usage引用、未知成本可见 | 一份真实平台收益记录与实际成本对应，口径不重复累计 | 产品表达已通过HTML；真实收益/成本证据仍OPEN，分析Holder专项核对 |
| G23 | 原型已有成功链被当作产品Ready | V1与本次HTML均明确模拟市场、生成、发布、数据；HTML仅验产品关系和本地交互 | Provider→实音频→实际发布→真实数据→学习应用的分段真实证据 | EXECUTION NOT VERIFIED；CEO接受HTML不替代执行验收 |

“撤出本候选承诺”指新文件不采用，未修改或删除任何旧研究。研究与旧稿差异不是Current Authority冲突，不能以本候选自行覆盖Frozen。

### 2.1 HTML产品反证与执行缺口分账（2026-09-23）

| 层次 | 对应Gap | 本次Disposition | 下一证据 |
|---|---|---|---|
| 产品表达已由HTML探索接受 | G01–G07、G10–G17、G22的交互/对象关系 | 六区与Business/Song、Market证据先行、方向候选与Human Choice、Song内Employee/试听、Master≠Published、归因回音乐、分维经验复用成立为**Candidate表达**；原文档级断点不再记为“没有产品答案” | Final UI Master验证信息架构与复杂状态；不等于真实Provider/平台/数据完成 |
| 仍需产品细化或长期验证 | PF-01–PF-07（下表） | 版本、独立Publication、验证与锚点规则吸收进Candidate；经验独立区使用频率、跨Song/Business会话及删除范围后的历史入口仍待验证/完成 | Final UI复杂场景与真实长期使用；必要时CEO再开产品架构Gate |
| 外部执行与持续性仍OPEN | G04–G05、G07–G12、G14、G18–G23的真实执行部分；尤其G08/G09/G19–G21/G23 | HTML的点击、模拟回执、Mock指标和本地刷新不能关闭这些Gap | 选定账号/Provider的合法真实调用、映射、资产恢复、次日重开与平台实际数据；按正式Issue与能力Gate验收 |

| Product Finding | 对账决定 | 未关闭的Gate |
|---|---|---|
| PF-01 Direction Version | **吸收产品规则**：旧Work/Candidate/Lyrics/Master及包固定原输入，新Direction显式重核在途与未启动Work；不能静默热切或覆盖历史 | Final UI展示冲突/过期与恢复；Runtime验证输入快照和外部未知效果 |
| PF-02 Multiple Publication | **吸收产品规则**：Publication按Song、Master、平台、账号和可核发行事实独立；Song发布状态只是投影，Observation按可确认粒度归属 | 多包/多次尝试的Final UI；真实平台映射和回执仍OPEN |
| PF-03 Learning Independence | **保留Candidate**：HTML支持多维复用与独立区价值，真实跨作品使用频率未知 | 长期多作品实际使用后再决定是否冻结独立性 |
| PF-04 Learning Validation | **吸收产品规则**：采用/调用不计验证；目标作品后续Observation/Result与反例才可支持验证记录 | 真实下一作品/发布版的后续观测与有限效果判断仍OPEN |
| PF-05 Music Semantic Anchoring | **吸收产品规则**：Song/版本/结构/音频时间/歌词/人声锚点分型，并标真实对齐、人工、推断或未知 | 真实音频、中文演唱与评论粒度下的锚点验证仍OPEN |
| PF-06 Business Conversation | **保留Candidate**：Song内持续会话成立，跨Song/Business的引用、目标Work与责任尚未形成验收 | Final UI/Shared Work Area场景验证；不得由普通聊天自动触发单歌动作 |
| PF-07 Market Scope Archive | **吸收待表达规则**：删/停范围后历史快照与已用Reference应可检索且不再扫描 | 当前HTML无归档检索入口；Final UI需补足，不重新打开HTML探索 |

上述Disposition关闭的是“产品合同没有答案”的部分，不关闭原G行要求的真实能力证据。

## 3. 外部证据审计：确认了什么，还差什么

| 问题 | 本轮证据结论 | 最小下一证据与产品影响 |
|---|---|---|
| 汽水是否有音乐人发布/经营入口 | 已确认官方搜索索引的功能类别；直开超时，非后台实测（E1） | 用户授权的具体账号样本；在此之前不冻结字段、资格、评论采集或自动化承诺 |
| Mureka是否存在官方生成API路径 | 已确认官方Quickstart（E2），不含本机成功 | 选定账号/模型/用途后核计费/权利、生成一次、查询、取回；不要继承历史价格 |
| ElevenLabs是否可程序化生成 | 已确认Music API公开教程（E3） | 具体模型用途条款和API客户类别仍需核验（E4）；不因“付费”自动过发行Gate |
| Suno是否官方无API、能否自动化 | 本轮未确认，历史sunnoai.com不能证明官方身份 | 保合法人工导入；未来如要自动化，必须官方通道及授权证据；不编绝对结论 |
| Provider产物是否有完整版权/平台必接受 | 没有此保证；服务条款不替代权利或平台判断 | 具体来源/计划/生成时间/用途与平台要求逐项处理，未知则该发布等待 |
| 是否可以拿完播、重播或逐秒数据 | 本轮没有汽水字段证据 | 只启用实得字段；结构锚点可分析，但不能制造行为曲线 |
| 如何收费、是否现在必须选套餐 | 现有价格冲突/时效不足，本轮未买服务、不锁套餐 | 产品需要每次预计成本范围、实际费用和额度来源；选Provider实施时再定向核价 |

未把无公开证据写成“不存在”。对可能变化的Provider访问/条款做了定向官方核查；未继续泛搜替代厂商。未实际打开登录后台，因此不报告真实汽水截图或字段。

**仍OPEN的最小执行清单**：汽水音乐真实后台字段；合法真实榜单/搜索/数据来源及可比口径；API与Browser/Computer Use实际能力、登录/MFA/CAPTCHA接续；Provider真实生成、价格/商用边界与中文演唱质量；目标平台发布规格、真实提交/回执/上线映射；评论与收益的实际粒度；音频等资产持久化和次日恢复；Market Watch自动触发/频率执行。HTML的Mock快照、模拟Provider、模拟发布及本地localStorage均不能关闭这些项；它们不阻塞当前产品结构Candidate收口。

## 4. 从Writing吸收的能力对账

| 方法 | Music落点 | 明确不照搬 |
|---|---|---|
| 构思前定位选择 | R3风格、标签、人群、语种、市场、场景、目标等→R4 | 小说人称/男频/世界观表单不是音乐通用分类 |
| 作品偏好＋本次要求 | Business默认→Song定位/Direction→当前Work要求，作用范围可检查 | 不做一个隐藏Prompt覆盖所有用户选择 |
| 候选与正式内容分开 | 歌词/音频候选→有权Choice→Master，完整历史 | 生成返回不自动定稿；歌词正式版不冒充对应音频 |
| 作者后改保护 | 旧歌词/定位基线的候选先重对比，未保存编辑保护 | 不能因为简化产品而省掉丢稿/覆盖保护 |
| 创作深度必须可操作 | 改词、结构讨论、试听、时间段反馈、版本比较、完整导出 | 不用总览卡片和通用聊天取代创作动作，也不自研DAW |
| 反馈→内容归因→经验 | A3/A4/L1/L2回到已发布音频与下一Direction | 不把评论推断当精确片段留存或因果证据 |
| 能力采用审计 | G01–G23检查动作、产物、返回、证据 | 有对象名/按钮不等于完整吸收；Mock通过不是专业质量验收 |

## 5. 场景压力检查

以下是2026-09-22原文档轮次的推演记录；2026-09-23 HTML对其中部分产品交互已给出探索证据，外部真实执行仍NOT RUN。没有伪造真实Song、账单、回执或平台数据。

| 场景 | 应能走通的路径 | 失败不能怎样掩盖 |
|---|---|---|
| 首次用户只说想做轻松中文歌 | R3允许暂定人群/市场→R4几个构思可比较→确认本次探索→P2/P3 | 不逼填全表，不擅自认为用户愿意商用/付费 |
| 用户从自己的歌词或音频开始 | P1导入预览→保来源与当前草稿→补必要定位→制作/试听 | 不强迫重新研究市场、不直接把导入文件标Master |
| 已选纯音乐，AI建议歌词 | Lyrics不适用；结构/音色/动机仍可完整制作 | 不把无歌词当缺项、不能未经确认改成歌曲 |
| 用户方向禁区与热门趋势相反 | 保用户明确约束，报告证据差异、给兼容或另案 | 不用市场理由静默覆盖作者选择 |
| 同请求两版，用户先改歌词再选旧音频 | 两独立Candidate；识别歌词不同步，明确实际唱词 | 不把最新文本配到所有音频上 |
| Master确定后换封面/改音频 | 封面变更只影响相关包预检；改音频新Master及包 | 不覆写旧Publication版本 |
| 汽水要求用户验证，另平台已上线 | 原Work WAITING_FOR_USER；另平台数据仍可观察 | 不绕验证、不冻结全业务、不重发成功平台 |
| 提交超时后第二天恢复 | 查远端、维持Unknown直到有证据 | 不以“重试成功”掩盖可能重复发行 |
| 后台只给歌曲总播放和账户收益 | 各按可得粒度保存；评论可做有限分析 | 不生成完播率、段落归因或歌曲收入分摊 |
| 评论对不同版本褒贬不一 | 保版本/不明版本标签、采样偏差及反例 | 不合并为“全体听众喜欢新副歌” |
| 有经验但下一首失败 | 留采用记录、差异和反例，收窄/停用 | 不删除失败、不把调用次数算验证成功次数 |
| 停止投入某首但继续整个业务 | 保Song/Publication/历史、停止新投入计划，继续其它Song | 停投入不等撤歌或删除资产 |

## 6. 自检、范围与接受边界

文档检查：六区及页面ID在三文件一致；22工作面都包含导航、页面、功能、动作、经营价值、交互、Employee、对象、输入、输出、下一去向；关系图标明Employee/Work/Provider/Artifact/Result/Decision；G01–G23与PF-01–PF-07分开记产品表达与执行证据。状态使用Review，未生成第二Current Blueprint。

2026-09-22原文档校验：三文件元数据/结束标记、Markdown代码围栏配对、本地引用存在性、22个唯一页面ID及每行11列均PASS。2026-09-23 HTML产品路径、截图与Console结果见[Closure](CURIS_MUSIC_HTML_EXPLORATION_CLOSURE.md)；Mermaid及外部运行/平台测试不因此获得验收。

原研究轮次新增三份文件，本次只窄幅修订并新增Closure：

- [产品结构候选](CURIS_MUSIC_BUSINESS_PRODUCT_STRUCTURE_CANDIDATE.md)：RESEARCH / Review。
- [关系图](CURIS_MUSIC_BUSINESS_RELATIONSHIP_MAP.md)：RESEARCH / Review。
- 本审计：REVIEW / Review。
- [HTML探索Closure](CURIS_MUSIC_HTML_EXPLORATION_CLOSURE.md)：REVIEW / Review；记录CEO接受和下一Gate。

来源：原研究证据、CEO接受的HTML探索、[CEO Review](../../../MUSIC_BUSINESS_CODEX_HTML_EXPLORATION/CEO_REVIEW.md)及两份定向修订记录。Pointer / 全局Index / CURRENT_STATE / Change Log **未更新**；未改Current Truth。原有脏工作区保留；本次未改HTML/UI/Figma/业务代码/数据库，未commit/push。

CEO已接受Music产品结构Candidate与HTML产品表达；接受不消除外部证据缺口。

最终处置：

- **Verdict:** HTML产品关系已与原Candidate对账；产品表达通过，真实执行未验证。
- **Disposition:** CEO ACCEPTED PRODUCT CANDIDATE + HTML EXPLORATION；非Frozen、非IMPLEMENTED、非执行验收。
- **Owner:** CEO / Product；专项Provider/发行/数据/持久化证据由相应责任Holder负责。
- **Next Action:** HTML探索关闭；按Closure移交Final UI与专项能力验证。
- **Target Authority:** 唯一Product Blueprint及其既有展开文件；本轮无写入。
- **Next Gate:** Final UI Master或真实Capability/Platform/Runtime专项验证；Authority吸收另需独立CEO Gate及正式Issue。

CURIS MUSIC BUSINESS GAP AUDIT — PRODUCT EXPRESSION RECONCILED / EXECUTION OPEN

STOP。
