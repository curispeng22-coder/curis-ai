# Curis Music Business — 完整产品结构候选

Authority Class: RESEARCH
Status: Review
Disposition: CEO ACCEPTED PRODUCT CANDIDATE / HTML EXPLORATION ACCEPTED；非Frozen、非Runtime验收
Baseline: 工作区 HEAD 78cacbd0857cc36c9f3fe0e4b11346489993b728（含既有未提交资料，不代表干净基线）
Updated: 2026-09-23
Module: Music Business
Owner: CEO / Product
Supersedes: None；本轮仅提出相对旧研究的修订，不替换 Current Authority。
Target Authority: 本轮不写入；CEO接受后明确唯一 Product Blueprint 及其展开文件的窄幅吸收范围。
Next Action: 保留本Candidate；按Closure分流Final UI与专项能力验证，不继续HTML探索。
Next Gate: Final UI Master或真实Capability/Platform/Runtime专项验证；Authority吸收另需CEO明确Gate。

## 1. 结论、范围与阅读入口

Music 是持续经营原创音乐的业务：确定值得做什么→创作→选定成品→发布→回收真实表现→分析→把经验用于下一首与下一周期。采用 **Business Operating + Song Project-like Professional Surface**。Song 是长期专业对象，一首歌有多个 Work；它不是新组织层级、第二个 Workspace 或一次生成请求。

本轮选择 **六个长期专业区：经营、市场与方向、歌曲制作、发行与发布、听众与收益、创作经验**。全部是 Music Workspace 内部专业导航，不新增公司七区。§3提供逐页面清单，§4是构思之前的定位合同，§5–10定义全链关系与决定，§11回答验收问题。

配套：[关系图与交接](CURIS_MUSIC_BUSINESS_RELATIONSHIP_MAP.md)、[断点审计与下一证据 Gate](CURIS_MUSIC_BUSINESS_GAP_AUDIT.md)。三文件互为本轮研究索引，不是第二 Product Pointer。

本轮产物是CEO已接受的**产品结构候选**，HTML产品表达也已接受；这不冻结唯一Product Authority，也不证明外部执行。HTML的实际交互、截图及Console边界见[探索Closure](CURIS_MUSIC_HTML_EXPLORATION_CLOSURE.md)。未调用生成Provider、未登录音乐人后台、未真实发布或收取收益、未验证Runtime。事实、提案与推断分开：**已确认（公开文档）≠账号实测；未确认=UNVERIFIED；推断=HYPOTHESIS；产品建议=CANDIDATE**。

## 2. 从业务责任推导六区

| 长期区 | 长期问题与资产 | 保持独立的理由 |
|---|---|---|
| 经营 | 目标、歌曲组合、预算、责任、待决、下一周期 | 跨歌曲取舍和资源决策，不能用单歌制作进度代替 |
| 市场与方向 | 来源关注、市场快照、Reference、Pattern、创作定位与方向候选 | 没有新歌时也持续研究；一个方向可支持多首歌，研究不可被某首歌吞没 |
| 歌曲制作 | Song、歌词、结构计划、音频候选、反馈、Master | 需要长期试听、改词、版本取舍与成品资产维护 |
| 发行与发布 | 发行包、目标账号、提交、回执、上线及驳回历史 | Master批准后仍有独立外部责任；无在途发行时仍维护发布历史和后续接续 |
| 听众与收益 | 真实观测、评论、收益、歌曲归因和观察计划 | 发布后跨时间与平台取证；尚未产生经验也可完成描述性复盘 |
| 创作经验 | 有适用范围的经验、反例、采用历史和验证结果 | 跨歌曲长期查用、修订、停用与应用回访，生命周期超过单次归因报告 |

相对旧五区：研究与方向细化为市场与方向；数据与复盘拆成“听众与收益”与“创作经验”。理由是观察事实、解释假设和被采用的方法不同，不能以“已写分析报告”冒充后续创作实际采用。不是为了模仿 Writing 六区，也不按六区招聘六员工。

不增设独立 Provider、Prompt、歌词、试听、版权、评论、版本、团队一级专业区；这些各有对象归属与上下文入口。创作经验空白时诚实展示暂无经验，可先记录有来源的作者偏好，不能灌入虚构市场规律。

## 3. 导航 → 页面 → 完整操作清单

“页面”指产品工作面或对象详情，不冻结 Tab、卡片、列数或高保真布局。E-L=经营责任，E-R=研究责任，E-P=制作责任，E-D=发行责任，E-A=分析责任；均通过现有 Assignment 找实际 Employee，可兼任，缺位明确。完整 Conversation 使用 Shared Work Area，打开和返回保留 Song/Version/Work/筛选范围。

### 3.1 经营

| 导航 | 页面 | 页面功能 | 能做什么 | 经营帮助 | 主要交互 | Employee | 关键对象 | 输入 | 输出 | 下一去向 |
|---|---|---|---|---|---|---|---|---|---|---|
| 经营 | O1 经营总览 | 歌曲组合、真实进展、待决、数据新鲜度、下一检查 | 判断当前业务卡在哪里、下一首为何开始 | 把创作进展和市场结果连起来 | 按状态筛选、打开Song/Result、处理待决、恢复工作 | E-L | Business、Song、Work、Decision | 各区真实状态与来源 | 决定或有目标的后续Work | 原Song/发行/分析；返回同组合 |
| 经营 | O2 目标与经营方向 | 市场定位、作品组合、发行节奏、预算与试验额度 | 设置目标、继续投入/观察/调整/停止投入 | 避免只追生成数量和单首偶然爆款 | 比较策略前后、接受建议、设下一复核条件 | E-L＋有权用户 | Goal、Strategy版本、Decision | 目标、收益/成本、Learning | 有范围策略和允许的下一周期 | R3定位、O1；旧Work快照不变 |
| 经营 | O3 责任与接续 | 当前Holder、在途Work、能力/权限缺口 | 分配已有员工、交接未完事项、定位等待原因 | 次日仍知道谁接着做 | 查看责任、合法分配、带证据交接、修复连接后回原Work | E-L及各Holder | Responsibility、Assignment、Work | 工作范围、可用人员与能力 | 接续记录或明确待补条件 | 原专业页；不复制组织目录/设置 |

### 3.2 市场与方向

| 导航 | 页面 | 页面功能 | 能做什么 | 经营帮助 | 主要交互 | Employee | 关键对象 | 输入 | 输出 | 下一去向 |
|---|---|---|---|---|---|---|---|---|---|---|
| 市场与方向 | R1 市场观察与关注 | 平台/市场/榜种/风格/时间快照、来源关注和采集缺口 | 查看热门样本，比较同口径变化，安排下一观察 | 找有证据的机会，避免把单次排名当趋势 | 添加合法链接/截图、筛选、比较快照、关注/停止关注 | E-R | Source、Market Snapshot | 公开资料或授权数据、研究范围 | 带采集时间的信号Result | R2拆解/R3定位；回原来源 |
| 市场与方向 | R2 Reference与歌曲拆解 | 结构、Hook、歌词主题、人声、编曲及表现证据 | 标记片段、比较参考、提取Pattern并注明反例 | 从“收藏一首歌”变成可用创作依据 | 播放合法音源/打开来源、标注、改分析、接受Pattern候选 | E-R＋E-P | Reference、片段引用、Pattern | 合法可听材料、元数据、市场信号 | 拆解Artifact、方向证据及未知 | R3/R4；来源可回查 |
| 市场与方向 | R3 创作定位（构思前） | 风格/标签、人群、语种、市场、平台、场景、目标、禁区 | 搜索多选、自由描述、选“不确定/请建议”，界定探索范围 | 在花费生成预算前明确做给谁、为什么做 | 编辑定位、比较建议、讨论冲突、确认/暂存、从旧定位派生 | E-R＋有权创作者 | 创作定位版本（Direction前置部分） | 用户意图、经营范围、研究/经验 | 已确认或明确待探索的定位 | R4构思；已有歌词可入P1再补 |
| 市场与方向 | R4 构思与Song Direction | 原创主题、记忆点、歌词叙事、结构声音、参考差异和目标 | 形成/比较/拒绝方向，确定一首歌值得做什么 | 将市场证据和用户审美变成可执行制作意图 | 提方向、逐项修订、确认、创建Song或关联已有Song | E-R＋E-P；用户作Choice | Direction版本、Decision | R3定位、Pattern、Learning、灵感 | Direction及采纳理由、制作输入 | P1；保留来源与原方向返回 |

### 3.3 歌曲制作（P2–P5是同一Song内部工作面）

| 导航 | 页面 | 页面功能 | 能做什么 | 经营帮助 | 主要交互 | Employee | 关键对象 | 输入 | 输出 | 下一去向 |
|---|---|---|---|---|---|---|---|---|---|---|
| 歌曲制作 | P1 歌曲库与Song概览 | 稳定Song身份、负责人、方向、当前版、历史、下一步 | 新建、导入自有歌曲、改名、暂停、继续；找回旧歌 | 一首歌跨多次Work长期经营 | 从方向创建/直接新建/导入预览、打开当前或历史工作 | E-P | Song、Direction、Work、资产引用 | 定位/方向、自有歌词或音频 | Song及待补信息、下一Work | P2/P3/P5；导入音频仍待审 |
| 歌曲制作 | P2 歌词与结构 | 歌词正文/候选、段落、Hook、叙事与情绪推进、结构计划 | 手写/导入/局部改词/比较/采纳；选择纯音乐或无词人声 | 用户能控制表达，减少盲目重生成 | 保存、选段讨论、押韵/可唱性建议、逐项采纳、回旧版查看 | E-P | Lyrics版本、Structure Plan、Candidate | Direction、自有材料与反馈 | 选定歌词/结构及修改记录 | P3；改词不改旧音频事实 |
| 歌曲制作 | P3 制作与生成 | 本次制作概要、来源、支持/不支持的要求、预算和请求状态 | 发起限定数量版本、导入外部制作、查询结果、提出局部改版 | 把Provider变成制作手段且可追溯成本 | 核对本次依据、提交、取消等待/查远端、取回音频 | E-P | Work、Execution、Provider、Audio Candidate | Direction/歌词快照、授权Reference、本次要求 | 实际音频Artifact、来源/成本、Result或失败证据 | P4；缺音频不可进入试听完成 |
| 歌曲制作 | P4 试听、比较与修改 | 单版试听、A/B切换、版本差异、片段反馈和拒绝理由 | 选择、拒绝全部、保留候选、请求改词/换声/调整结构 | 用真实听感取舍而非“商业潜力分” | 播放/暂停/定位/可选循环试听、标记时间段、讨论、改版 | E-P＋有权审阅人 | Audio Version、Feedback、Choice | 可播放候选和本次制作依据 | 选择记录、改版Work或Master提案 | P2/P3/P5；不跨版本误贴时间点 |
| 歌曲制作 | P5 成品、素材与版本历史 | Master批准记录、歌词/封面/音频一致性、完整旧版与权利材料 | 确认成品、查看/取回旧版为新候选、导出自有成品 | 确保发行的是实际选定版本 | 核对试听对象、批准Master、打开完整历史、查资产缺失 | E-P；有权人确认 | Approved Master、Artifact、Decision | 已审候选、质量结果、版本说明 | 不变的Master版本引用及未解事项 | D1发行包；批准不等于允许发布 |

### 3.4 发行与发布

| 导航 | 页面 | 页面功能 | 能做什么 | 经营帮助 | 主要交互 | Employee | 关键对象 | 输入 | 输出 | 下一去向 |
|---|---|---|---|---|---|---|---|---|---|---|
| 发行与发布 | D1 发行包与平台预检 | 指定Master、音频/封面/歌词/署名、平台要求、授权材料 | 准备/修改发行包、预览导出、指出缺项 | 防止成品到上传之间断链 | 选平台/账号、核对字段、检查文件和声明、提交发布决定 | E-D＋E-P | Release Package版本、Gate | Master、素材、目标平台现行要求 | 发行包与逐平台预检结果 | D2；未知规则保持待核 |
| 发行与发布 | D2 提交与回执 | 按平台账号的提交尝试、等待/拒绝/未知、人工接续 | API或获准Computer Use提交；导出后人工发布并登记 | 无API仍可持续经营且不假称上线 | 在授权内执行、人工接管、登记证据、查询远端、处理拒绝 | E-D＋有权用户 | Submission、Receipt、Work | 指定发行包与发布授权 | 提交事实/审核状态/失败/Unknown | D3或D1返修；始终回同提交 |
| 发行与发布 | D3 发布历史与观察安排 | Song×Master×平台×账号的Publication、上线/下架事实 | 核对上线版本、安排数据观察、处理再发布或撤回请求 | 多平台状态独立，留存长期发行历史 | 打开平台证据、核对映射、设检查期、发起变更请求 | E-D＋E-A | Publication、Observation Plan | 回执与远端核验 | 发布映射、下一检查、变更Work | A1/A2或D1；撤回须另授权与核验 |

### 3.5 听众与收益

| 导航 | 页面 | 页面功能 | 能做什么 | 经营帮助 | 主要交互 | Employee | 关键对象 | 输入 | 输出 | 下一去向 |
|---|---|---|---|---|---|---|---|---|---|---|
| 听众与收益 | A1 表现总览与对比 | 同口径指标、发布时间龄、平台/歌曲筛选、数据覆盖 | 比较已发布作品，识别变化和缺口 | 区分播放增长与经营成功 | 切窗口/指标、打开异常、查来源、比较相同观察年龄 | E-A | Performance Observation | 已核对Publication与真实数据 | 描述性观察、分析/补数据Work | A2/A4；保留原筛选 |
| 听众与收益 | A2 数据回收与订正 | 四模式回流、对象映射、字段原义、重复/冲突预览 | 导入报表/截图、人工录数、核对和订正 | 真实可得字段才成为经营依据 | 预览、映射确认、去重、校正、查看原证据 | E-A＋用户 | Observation、Evidence | API/界面/导出/手录实际来源 | 正式观测或待核记录、采集Result | A1/A3/A5；不明版本不强挂 |
| 听众与收益 | A3 评论洞察 | 歌词/旋律/副歌/人声/情绪/编曲/记忆点/传播点/反感/期待 | 看主题簇、代表原文、矛盾反馈，关联歌曲版本/片段 | 将“喜欢/难听”转成可讨论的制作问题 | 改分类、去重、查看反例、确认片段推断、交给制作 | E-A＋E-P | Comment、Feedback Cluster | 合法评论、截图/摘录与采样说明 | 有证据的反馈主题及修改问题 | A4/P4/L1；不自动回复评论 |
| 听众与收益 | A4 歌曲表现归因 | 观察、证据、内容特征、替代解释、反证、建议 | 解释可能原因，建立下一次验证 | 不停留在“播放量上涨”，不伪造因果 | 对照已发布音频/歌词、检查因素、讨论、选择观察/改版 | E-A＋E-P | Analysis、Hypothesis、Result | 表现/评论、发布版、市场环境 | Learning候选、经营建议、验证计划 | L1/O2/P3；回原观测 |
| 听众与收益 | A5 收益与投入观察 | 按歌曲/平台实际可得粒度呈现收益、账号粉丝及可核成本 | 看平台收益与来源口径，判断继续投入是否值得 | 不把热度或账号粉丝冒充歌曲收入 | 查原账单、核对币种账期、标明缺失 | E-A及有权经营责任 | Revenue Observation、既有Usage引用 | 平台可得收益证据与实际成本 | 有限范围收益判断或未知 | O2；不承担结算/到账交易流程 |

### 3.6 创作经验

| 导航 | 页面 | 页面功能 | 能做什么 | 经营帮助 | 主要交互 | Employee | 关键对象 | 输入 | 输出 | 下一去向 |
|---|---|---|---|---|---|---|---|---|---|---|
| 创作经验 | L1 经验库与适用检查 | 创作偏好/生产经验/市场学习分开，来源、边界、反例、验证次数 | 接受、质疑、停用经验，查适用于何种风格和受众 | 防止一首成功机械复制到所有歌 | 筛选、查看证据、确认范围、用于方向/本次制作 | E-A＋E-R＋E-P | 既有Learning/Knowledge的领域内容 | 归因Result、试听经验、反例 | 已接受经验或待验证候选 | R3/R4/P3/O2；保引用版本 |
| 创作经验 | L2 经验详情与应用回访 | 用过哪些Song/Direction/Work、采用方式、后续表现 | 检查经验是否真被用到、是否有效、是否失效 | 关闭“报告写完但下一首没改变”的断点 | 对照应用前后、追加反证、修订、暂停适用 | 原责任人或当前Holder | Learning版本、应用记录、Observation Plan | 采用记录及后续证据 | 修订经验、验证Result、下一行动 | L1/A4/下一方向；旧采用记录保留 |

## 4. 构思前：先划定创作方向，而不是先写Prompt

### 4.1 从Writing吸收的方法

Writing参考研究 W1–W3 表明，定位选择需要作用范围、可检查的创作依据、候选确认和历史保护。照搬小说标签或固定流程没有必要。Music采用：

**Business经营方向 → 创作定位（先界定探索范围）→ 构思候选 → Song Direction（这首具体做什么）→ 制作概要与本次要求 → Provider执行输入**。

创作定位是Direction的前置内容，不新建Company OS primitive。HTML探索确认：**一句自然语言、少量引导标签、与负责Employee持续讨论**可以并行起步；标签帮助表达，不自动拼接成Provider Prompt。允许先有歌词、Reference、自有音频、明确专业要求、纯音乐，或完全不知道方向而请Employee结合市场提出建议。常用选择直接可见，细分类按需展开；未选维度标“待探索”，不是AI偷偷补成确定事实。用户可保存多个Direction Candidate稍后讨论，也可带着其中一条回到同一会话继续修订；每条候选独立保留听众、语言、市场、表达边界及理由。**Human Choice之后才有Accepted Direction**，并成为Song制作的正式、带版本的上下文。市场未知不阻止私人草稿；有外部副作用的动作仍需具体目标与授权。

### 4.2 用户可选择、AI可建议的维度

| 维度 | 用户选择/自由输入 | AI辅助与未知边界 | 实际影响下游 |
|---|---|---|---|
| 创作目的 | 自我表达、建立艺人定位、积累听众、检验方向、商业发行、场景配乐 | 明确优先顺序；不承诺收入或爆款 | 方向判断、预算、完成标准、观察指标 |
| 目标人群 | 语言社群、兴趣/音乐偏好、生活处境、可选年龄段及已有听众 | 推荐带理由和证据；不能凭风格猜真实人口画像 | 用词、情绪与理解门槛、发布研究范围 |
| 市场与地域 | 国内/特定地区/海外/待探索；可多选主次 | 地域与语种分开；真实需求待研究 | 来源选择、发布时间解释、平台与权利范围预检 |
| 语种与表达 | 普通话、方言、英语、多语、纯音乐、无词人声 | 小语种发音/方言支持按Provider核验；没有歌词不强填押韵 | 歌词、发音审阅、Provider适配及发布元数据 |
| 风格与标签 | 主风格、辅助风格；标签可搜索、多选、自由补充 | AI解释标签在这首歌里的含义；不把营销标签视作科学分类 | 节奏、配器、人声、制作提示及对照依据 |
| 聆听/使用场景 | 通勤、独处、运动、睡前、现场、短视频配乐等 | 场景不等平台；AI提出可能设计，标推断 | 能量变化、时长、歌词密度和片段目标 |
| 情绪与能量 | 温暖/克制/激烈/松弛等，自由描述起伏 | 区分全曲气质与某段效果 | 结构、声音、试听评议 |
| 主题与表达边界 | 想说什么、不想说什么、叙述视角、敏感/禁用表达 | 构思前可只定宽主题；后续形成具体原创表达 | Lyrics、Hook、取舍与审稿依据 |
| 作品形态 | 歌曲、纯音乐、无词人声；完整作品/短篇；暂定长度 | 不强制Verse/Chorus；数字可稍后定 | 结构方案、Provider选择、试听和发行适配 |
| 声音与人声 | 独唱/合唱意向、声线质感、演唱方式、主要乐器 | 受众性别≠歌手性别；不默认真人声音克隆授权 | 声音方向、实际能力检查与成品核验 |
| 节奏和结构偏好 | 快慢/律动、可选BPM范围、Hook和高潮意向 | 用户不懂BPM可用描述；AI建议并标待验证 | 结构计划、节拍/段落比较；不是精确控制保证 |
| 参考与差异 | 合法链接、自有音频、喜欢/不喜欢的特征 | 先拆特征、说明不照搬什么；上传权限另核 | Pattern/Direction Evidence；仅可用材料进入Provider |
| 目标平台与路径 | 汽水为主要样本，可选其它平台或待定 | 用户选择≠账号可发布、AI内容已获准 | 平台预检、发布包、数据计划 |
| 投入与约束 | 预算、候选数量、完成期限、本人参与度 | AI建议最小试验；未知价格不能生成虚假精确估算 | Work边界、重生成限度、超范围决定 |

这些不是全必填大表单。启动一次探索至少知道：作品形态、当次目的、用户已定的硬约束，以及哪些维度允许AI探索。真正提交付费生成还需输入、能力、有效权限、费用范围和完成标准。正式Direction需补足做给谁、哪里发布或暂不发布、主题与声音方向、参考差异及目标；不确定项逐项可见。

### 4.3 确认、继承与变更

1. 业务策略给默认范围；用户本首歌已确认的定位优先于AI建议。本次改版允许明确覆盖偏好，但不能越过权限/预算/素材权利边界。
2. 冲突例：“睡前低刺激”与“副歌强爆发”：AI解释取舍，用户选择全曲低刺激、局部爆发或保留探索；不能自动删除一个标签。
3. 每次生成可查看实际采用的定位/Direction/歌词版本、本次要求、采用的Learning、排除内容及原因。超出Provider输入长度或能力的要求必须说明，不能静默截断后声称全量执行。
4. 选择进入执行输入不等于输出遵守；试听/歌词核对检查实际结果。Provider只支持整曲重生成时，明确无法保证局部修改及其它部分不变。
5. 改定位/Direction产生新版本：未开始Work先重核输入；在途Work保持已固定输入，需明确继续、取消或另起Work（外部效果未知先核验），不得热切。旧Candidate保留原Direction/歌词/制作要求快照，对当前Direction标“需重新比较”，不能无声转为新基线；手写歌词草稿和已保存歌词版本不自动覆盖。旧Master批准与旧Release Package/Publication保持历史事实，新版要成为成品或另行发布需重新Choice和目标包预检。具体失效提示、冲突交互与恢复证据移交Final UI/Runtime验证。
6. 方向暂存、作者手改与AI候选分开。旧候选基于旧定位/歌词时先重对比，不能覆盖用户后改内容。保完整历史和恢复为新候选的操作。

示例（虚构产品走查，不是市场结论）：用户选“普通话、都市独处人群、温暖克制、轻电子、通勤、先探索汽水发行、不用失恋叙事”。研究可建议把“下班路上重新找回自己”作为方向，给出原创Hook意图、结构和声音方案；用户确认后进入Song。若市场报告偏向伤感情歌，只能提出不同建议，不能悄悄覆盖用户禁区。

## 5. 市场研究与Reference真正进入制作

观察单位=来源×平台/地域×榜种或样本选择规则×时间窗。保存来源、抓取/观察日期、排名或平台原指标、是否广告/推荐信息可得、未知项。只有多次可比观察才称趋势；单一热门样本不能说明市场普遍偏好。关注保存下一检查目的和日期，实际访问受能力与授权约束，不承诺实时全网采集。

HTML探索确认R1–R4应作为**持续市场观察工作面**表达：Research Scope（观察什么、从哪里、窗口/频率/关注对象及来源可用性）→同一范围版本的Snapshot History→新进入/升降/持续或稳定等Change→具体Reference Candidate→合法可听材料的拆解与Pattern→Employee在证据之后给出解释→Direction Candidate→Human Choice。可新增、修改、暂停、恢复、删除/归档范围及手动检查；改比较口径开启新范围版本，旧快照不混算。删除后历史快照和已用Reference应可检索且不继续扫描；这一归档入口是Final UI待完成项。检查频率是计划，未接入后台时不得称自动观察。没有真实来源时，榜单、频率和趋势明确标Mock；不发明通用市场指数，也不从排名推定场景需求。

Reference拆解包含：Intro/Verse/Chorus/Bridge/Outro或实际存在的段落，起止位置，Hook、高潮/副歌进入点，BPM/节奏，情绪曲线，歌词主题/押韵/重复，声线与唱法，编曲/配器，长度，声音特征，封面与定位。每项注明**人工听辨、Provider分析、源文件元数据或推断**；不可听/不可解析则未知，不能只凭曲名填分析。

结构标注和评论锚点均绑定具体音频版本；BPM半拍/倍拍等不确定性可并列保留。无需DAW时间轴，时间段标注、播放器与表格即可表达。参考的市场表现另列来源，听感好不等于市场有效。

Pattern记录：参考范围、共同特征、证据片段、观察到的表现、可能有效理由、差异/反例、适用范围与原创转译建议。Direction逐项说明采用了哪个Pattern、如何变化、哪些不采用。没有合法音源也可保元数据研究，但不宣称完成音频拆解。

公开Reference链接不等于上传许可。研究保合法引用；制作只发送有权使用且Provider允许的内容。不得把艺人名/歌名机械送入Provider：例如ElevenLabs现行Music Terms明确限制此类输入，见E4。不会由“学习风格”推导声音克隆或复制歌词旋律的权限。

## 6. Song创作内核、Candidate与Master

Song持有方向、参考、歌词、结构计划、候选音频、封面/元数据、Master历史、发行记录、表现与Learning引用。Composition/Recording是作品和录音的专业区分；Curis Work是一次有边界的工作。可先建立尚未命名、尚未注册、尚无收入的Song，不强制有ISRC等外部编号才开始创作。

歌词允许自写、导入自有稿、AI候选、逐段比较/采纳/拒绝。可按需要讨论可唱性、音节密度、重复、押韵、叙事和Hook；不承诺押韵检查等于好歌词。纯音乐的歌词字段为不适用，无词人声单独说明。生成唱词与输入歌词可能不一致，发布歌词需核对实际成品，不能只引用旧输入。

一轮Work可以有多次Provider请求，一次请求可以有多个独立可试听Candidate；**每个可听输出都具有独立版本引用**，不因同一次请求而藏成无法单独选择的附件。保存父版本、方向/歌词/本次要求快照、Provider/模型/请求与输出标识、来源、实际费用或未知、产物引用与获取状态。音轨/Stem仅按需作为附件，不建DAW对象系统。

A/B是审美比较，支持独立音量/播放定位及说明时长差异；两个版本片段位置不能按秒数自动认为语义相同。反馈可挂全曲、段落或时间段，保留“更喜欢B人声”这类偏好与可验证技术问题的区别。拒绝所有版本可结束该Work或请求下一轮；重生成没有无限自动循环。

HTML探索确认Song是长期创作工作对象：负责制作的Employee与持续Conversation在工作主位，Direction/Reference/Lyrics/Structure/Current Work/Candidate/Audio/Feedback/History/Master围绕**同一Song**组织，定位与来源作为可随时查看的上下文。直接“创作一首”可建立方向待确认的Song草稿，在Song内以自然语言、引导选择和员工提议明确方向；从市场已接受Direction出发则继承该版本，两个入口不能强迫经过同一个空白引导页。HTML可操作的试听、版本比较、位置反馈与Human Choice只验证交互关系，不验证真实生成或音质。

Approved Master成立条件：指定音频确实可访问并完成必要质量检查；有权者针对该确切版本作创作接受；关联歌词/标题等版本一致或明确未完成项；保存决定者、时间、理由、范围及来源。未获发行许可可以是已批准创作成品，但发行Gate必须保持未通过。Master不是工程母带处理认证，也不是版权保证。

Master改变=新批准版本；旧Master仍供旧Publication追溯。旧发行包不随“当前Master”指针漂移；选版成功、素材持久保存、发行授权、外部上线分别确认。临时音频URL失效且没有合法保存副本时显示资产不可用，不能播放假进度。

## 7. Provider、Employee、Work与Result

Employee承担研究/制作/发行/分析责任，Provider提供专业能力。一个员工可兼多责，一项责任可由多人分工，每个Work明确一个负责交付的Owner及协作者。Song负责人协调长期接续，不能自动获得全部发布或预算权限。

**Employee → Work → Provider执行 → Artifact/Candidate → Result → 原Song/接收责任人 → Decision或下一Work**。Result报告输入版本、交付、证据、失败/未决与下一去向，不复制音频、不替用户选择、不等于外部成功。交接带目标Song/版本、完成标准、接收人、来源及返回位置；无人接收则明确等待。

Provider连接与费用消费既有共享能力/Usage；不建Music模型商店或第二成本账。Mureka可作为优先技术验证对象，ElevenLabs为另一个文档化候选，Suno暂保合法外部导入路径；这是验证顺序，不是已选定商业接入合同。详见§12证据。

任何切换都检查输入/外发权限、支持能力、费用与版本差异。生成超时先查原请求效果，再决定重试；缺请求查询能力保持未知，不能无条件“重试两次再换供应商”。用户停止本地等待不代表远端取消或退款。

## 8. Master → 发布：汽水样本、平台中立关系

Release Package引用确切Master、音频、封面、实际歌词（适用时）、艺人/署名、必要声明/权利依据、平台元数据与要求版本。共同概念存在，不代表所有字段通用必填。ISRC/UPC、封面尺寸、音频规格、AI声明方式以目标平台实际要求核验；不沿用旧稿“全部必填”“审核1–3天”“千次播放单价”。

| 通道 | 使用前提 | 回流与边界 |
|---|---|---|
| API | 官方合法接口、具体账号资格/权限和能力已核实 | 请求标识、回执、远端核验；文档存在不等于Curis接通 |
| Computer Use | 实际可用且获准的界面、指定账号/文件/提交授权、有效控制能力 | 登录失效/CAPTCHA/MFA/风控/权限失败→立即STOP→WAITING_FOR_USER；用户接管期间AI不抢控制 |
| 导出后人工发布 | 用户可合法进入平台并上传 | 导出包完成≠提交；用户回填平台、账号、版本、时间及回执；无可核证据记“用户报告待核验” |
| 人工登记已有发布 | 已有作品和可确认映射 | 先核对Song/Master/外部作品，不盲目重建或再发 |

产品语义：Ready→Submitting→有证据的Submitted/Waiting（审核）→Published；也可Rejected/Failed/Unknown。WAITING_FOR_USER属于原Work接续；EFFECT_UNKNOWN表示副作用未明。平台原状态保留，不强行映射成一个百分比进度。

点击上传、平台收件、审核通过、实际上线是不同事实。查询/用户回执只证明对应事件。无直接公开链接时可保存合法后台上线证据；没有任何上线证据不能标Published。恢复时核对账号、发行包版本和远端事实；先查是否已提交，再决定下一动作，防止重复上传。

每平台/账号拥有独立Submission和Publication。同一Song可关联多个Master与发布记录，但跨平台授权逐项检查。改音频、重发、下架另走有权决定和远端核验；不假设平台支持原位替换。停止Curis计划不等于撤销外部已排期提交。

**Publication是独立记录，不是Song上的单一发布状态**：固定Song、被发布Master、目标平台与账号、采用的Release Package/提交尝试、可核上线证据及后续状态。同一Master跨平台、同一Song换Master或同平台再次发行都保留各自记录；Song层“已发布/待发布”仅为可筛选汇总，不能替代明细。Observation先归可核对的Publication；只能确认平台作品或账号时保存该粒度和映射未知，不自动归给“当前Master”。HTML验证了多平台状态与发布包的表达，未验证真实提交、回执或多次发行的外部映射。

## 9. 数据、评论、收益与Music Attribution

### 9.1 已知能力与字段上限

2026-09-22公开核查：汽水合作平台官方搜索索引说明提供歌曲发布、推广、数据分析与分账结算；正文直开超时，未登录后台。因此只能确认公开功能类别，不能确认具体指标、API、导出、AI作品资格、账号权限或Computer Use执行成功。E1。

| 待核实指标类别 | 汽水当前证据 | 使用规则 |
|---|---|---|
| 播放、听众 | 逐字段定义/粒度未确认 | 保原字段名；次数≠人数，公开热度≠播放量 |
| 收藏、点赞、分享、粉丝 | 后台字段与作品/账号层级未确认 | 累计/新增/净增区分，账号粉丝不能分摊到歌曲 |
| 完播、重复播放 | 未确认提供及分母 | 没有不填0，不从播放量反推；无行为锚点不造片段留存 |
| 评论 | 完整获取、接口、版本锚点未确认 | 合法实际摘录可分析；样本不冒充全量 |
| 榜单/推荐位置 | 可访问榜源、规则、更新频率待选源验证 | 保存榜种和时间；排名不是收入或因果证据 |
| 收益 | 官方公开说明分账结算类别；精确账单未确认 | 原类别、币种、账期与粒度；不承诺收益单价/日更 |

四种输入模式 API_SYNC / COMPUTER_USE / IMPORT / MANUAL_ENTRY 是产品可选路径，不是各字段均支持四种通道。手工录入也不能创造平台没有的数据。未知市场数据不妨碍记录创作偏好，但无法声称已经证明市场有效。

每条观测保存：Business、Song、可确认Master/Publication、平台/账号、原指标名/定义/单位、数值或缺口原因、累计/区间、时间窗/时区、采集时间、来源/原始证据、粒度、订正历史。无法确认版本则挂已知平台作品并标映射未知，不能归给最新本地版。导入先预览映射和重复，截图提取需核对；订正保原读数。

固定日期趋势与“上线后第几天”比较分开。跨平台不兼容指标不相加；没有去重依据不算全网独立听众。收益面展示平台可得的收益及其来源、币种、账期、粒度与缺口；不把“已结算/实际到账”做成Music业务首页指标或资金交易流程。若源账单含预估、调整或结算口径，作为证据属性保留，不能重复累计。生成费、发行费、推广费仅在真实可得且同币种/期间/确认基础可比较时用于有限投入判断；不做虚假歌曲利润。账号粉丝数属于账号观测，不能摊成某首歌收益。

### 9.2 评论 Intelligence

评论记录实际平台/作品、时间、原文证据、可得版本、来源与采样范围，尽量少取个人信息。去重保证据；点赞不等于独立投票。主题包含歌词、旋律、副歌、人声、情绪、编曲、审美、记忆点、传播点、反感点、期待，可多标签及“不明确/混合”。每簇展示样本数、代表意见、相反意见和来源。

“副歌太晚”可建议关联某一段；没有平台时间锚点时明确为AI推断、待确认。旧版评论保旧版锚点；无法分清版本不贴到新版。评论不是全部听众画像，也不直接成为改歌命令。由制作责任人和用户判断是否改；形成问题Work回到原Song/片段，未经授权不回复评论。

音乐语义锚点应区分**Song整体、确切音频版本、结构段落、音频时间点/区间、歌词行及人声片段**，并注明依据是实际对齐、人工标记、推断或未知。它们不是天然互相映射：器乐的时间标记不能自动证明某句歌词或唱法的位置；无可验证锚点的评论只挂可证实的Song/Publication粒度。HTML的时间点反馈验证了交互与版本引用，未验证真实词曲/人声对齐。

### 9.3 归因必须分五层

| 层 | 必须包含 |
|---|---|
| Observation | 发生什么变化；指标、窗口、样本、Song/版本/平台；数据新鲜度和缺口 |
| Evidence | 平台读数/回执、实际发布音频/歌词、评论原文、市场快照、对照对象；不存在的证据明确缺失 |
| Hypothesis / Analysis | Hook、副歌时间、结构、情绪、BPM、人声、编曲、长度、歌词与反馈的可能关联；发布时间、曝光/推广、平台环境、趋势等替代解释与反证 |
| Learning候选 | 结论适用平台/人群/风格/时期、已有正反例、验证次数与未排除因素 |
| Recommendation | 继续推广/观察/改版/换策略/增同类/停投入/下一首方向；决定者、预算、下一验证条件 |

示例（虚构）：某首前7日播放高于既有可比作品，评论样本称“副歌容易记”。可以提出Hook可能有帮助；也可能是推荐曝光、推广、艺人听众基础或发布时间变化。若没有曝光数据，必须标无法排除；不能说“提前副歌使播放增长30%”。下一首在适用范围试验并记录其他差异，非随机试验不能声称因果已证实。

无段落留存数据时，音频时间点只用于解释/创作反馈，不声称某一秒导致流失。纯音乐仍可分析主题动机、高潮、节奏、音色；歌词维度不适用。新版本未发布时，其试听好评不能解释旧发布版的市场表现。

## 10. Learning、经营决定、资产与次日恢复

Learning保存来源、Song/Version/Publication、平台/市场、时间、Evidence、结论和性质、适用范围、反例、验证次数、采用状态、负责人及后续验证。作者偏好、制作经验和市场学习分开；一条经验多次被复制不增加验证次数。次数指独立可追溯的验证记录，不是浏览/调用次数。

HTML支持“创作经验”作为独立长期专业区的**产品表达候选**：可按市场方向、受众、发行时机、曲风、技巧、乐器等维度拆分复用，既能进入新Direction，也能进入尚未完成的Song修改Work；不能整首套用。其长期真实使用频率尚无证据，保持Candidate，不升为Frozen独立性结论。

应用到下一首时保存Learning版本、目标Direction/Work、采用或不采用的理由、具体改变和观察计划。新证据可修订/停用，不抹旧使用历史。重大经营调整由有权用户/Leader决定；在已授权范围内的研究/数据整理/候选准备无需每次CEO批准。Leader身份不自动授予审美终审、版权确认或外发权限。

**采用记录与验证结果分开**：只有目标Direction/Song/Work确实采用了可指认的改变，且后续取得对应Observation/Result并检查适用条件、替代解释和反例，才可增加验证记录或修订有效性；调用、复制、生成候选、发布本身均不等于验证。Song内持续Conversation的上下文关系已通过HTML表达；跨Song或Business Operating会话如何准确引用目标、版本与行动责任仍是Candidate/Final UI验证项，不能把泛讨论自动写入某首歌的Work。

| 决定 | 谁决定 | 结果与失效条件 |
|---|---|---|
| 定位/方向、歌词、试听选版与Master | 有权创作者/指定审阅人 | 绑定版本的Choice；新基线需重对比，不自动批准发布 |
| 发布、权利材料、额外费用/权限 | 对具体动作有权的人 | 目标账号/包/范围的Gate；对象或条件实质变化需重查 |
| 继续推/观察/调整版本/改策略/换方向/增同类/停投入 | 授权内Leader，超范围CEO | 有理由的Operating Decision、下一Work或明确不行动、复核条件 |

资产逻辑归属 Business→Song；跨歌市场资料/经验归Business，Song引用。员工离岗、换Provider不能带走唯一资产。音频/歌词/封面/发行包需真实可访问、来源明确、版本稳定，受控保存与备份遵循Shared合同；本轮不选择存储技术、不建目录Runtime、不声称已经持久化。

次日恢复最少看到：当前Song及定位/歌词/候选/Master版本、未保存编辑状态、待确认Choice、Work负责人/输入/最后证据、Provider请求状态、已发发行包与外部效果、未完成账号接续、观测窗口/最后采集/下一检查、待采用经验和下一动作。恢复先读已发生事实；不会重发生成、重扣款或重复发布。

用户退出、断网、电脑睡眠时不保证本地继续。后台只有已启用且实际可运行才推进；下次打开补核状态。暂停一首不冻结其它独立Song；停止投入不删除已发布历史或自动撤歌。

## 11. 十二项验收问题定位

| 问题 | 可直接检查的答案 |
|---|---|
| 几个长期导航？ | 六区，§2；公司七区保持 |
| 每区有哪些页面？ | §3的22个工作面/详情，非22个独立Tab承诺 |
| 每页能干什么？ | §3功能、动作、输入输出列 |
| 对经营有什么价值？ | §2长期理由、§3经营帮助列 |
| Employee在哪里工作？ | §3责任列＋§7现有Assignment/Shared Work Area，非Provider人格化 |
| 从市场走到Master？ | §4定位→构思，§5Reference→Direction，§6歌词/音频/Choice→Master |
| Provider怎样进入？ | §7有边界Work调用，独立输出版本与Result返回 |
| 怎么发布？ | §8四条真实能力条件路径，回执不等上线 |
| 怎么拿真实数据？ | §9四模式、映射和口径，未知不补零 |
| 怎么理解好/差？ | §9.2–9.3评论与五层归因，相关不冒充因果 |
| 怎么带到下一首？ | §10经验接受→明确采用→后续回访，§4执行依据可检查 |
| 还有断点吗？ | 配套Gap Audit：合同补齐与真实验证缺口分开，尚不能宣称执行Ready |

## 12. 来源、定向补证与旧稿处置

### 12.1 Current只读约束

按[Pointer](../../00_Context/PRODUCT_DOCUMENT_POINTER.md)的Current Required Input读取[唯一Blueprint](../../01_Product/Curis_Product_Blueprint.html)、[Master Map](../../01_Product/Curis_Product_Master_Map.md)、[UI Blueprint](../../01_Product/Curis_Product_UI_Blueprint.html)的当前层级/身份/专业工作面合同，并读取[Shared Authority](../../03_Design/Curis_Company_OS_Shared_Authority.md)的Assignment、§11–16人工接续/能力/恢复。Authority Class为CURRENT/FROZEN及其展开，Status Frozen；仅消费适用边界，不把Research升权。未发现需自行裁决的当前产品Authority冲突。

[Document Status Rules](../../00_Context/DOCUMENT_STATUS_RULES.md)只用于本轮元数据与Review处置；其历史通用排序不用于让Implementation覆盖Product，Truth路线按AGENTS与Current Pointer。

### 12.2 已有研究来源（全部非Current，原文件保留）

| 编号 | 来源与读入范围 | Authority Class / Status或Disposition | 本轮用途与限制 |
|---|---|---|---|
| M1 | [Music Business Truth](</Users/yy/Documents/Curis Business Research/business-research/music/MUSIC_BUSINESS_TRUTH_REPORT.md>)、[Operating Model](</Users/yy/Documents/Curis Business Research/business-research/music/BUSINESS_OPERATING_MODEL.md>)、[Open Questions](</Users/yy/Documents/Curis Business Research/business-research/music/OPEN_QUESTIONS.md>)：对象、循环、角色、验证缺口 | 外部RESEARCH，旧稿未统一标准Status，非Current | 保长期Song/版本与人判断；不采用“已有编号/收入才有Song”或无条件remix标识公式 |
| M2 | [Translation](</Users/yy/Documents/Curis Business Research/product-translation/music/MUSIC_PRODUCT_TRANSLATION.md>)§1–5、[Structure](</Users/yy/Documents/Curis Business Research/product-translation/music/MUSIC_PROFESSIONAL_WORKSPACE_STRUCTURE_CANDIDATE.md>)§1–3、[Employee/Provider](</Users/yy/Documents/Curis Business Research/product-translation/music/MUSIC_EMPLOYEE_AND_PROVIDER_EXECUTION_MODEL.md>)§1–4 | RESEARCH / CANDIDATE旧状态；2026-09-18 | 保边界；本轮修正固定五员工、Song Work混用、请求与Candidate混用 |
| M3 | [Reconciliation rulings](</Users/yy/Documents/Curis Business Research/product-translation/shared/RECONCILIATION_RULINGS_2026-09-18.md>)Music条目、[Continuous Model](</Users/yy/Documents/Curis Business Research/product-translation/music/MUSIC_CONTINUOUS_OPERATING_MODEL.md>)§1–4、[Qishui Model](</Users/yy/Documents/Curis Business Research/product-translation/music/MUSIC_QISHUI_PUBLISH_AND_RESULT_INTAKE_MODEL.md>)§1–6 | RESEARCH / CANDIDATE，非Authority | 保四模式与Auth Stop；B2B不作主路径；纠正无市场反馈也叫经营闭环 |
| M4 | [Provider Deep Dive](</Users/yy/Documents/Curis Business Research/business-execution/music/MUSIC_PROVIDER_FEASIBILITY_DEEP_DIVE.md>)、[Pricing](</Users/yy/Documents/Curis Business Research/business-execution/music/PROVIDER_PRICING_AND_ACCESS.md>)生成段、[ElevenLabs摘录](</Users/yy/Documents/Curis Business Research/business-execution/music/evidence/elevenlabs_music_excerpt.md>) | 历史RESEARCH / 旧称终稿；不是接入验收 | 发现来源/价格/许可缺口；不继承READY和当前价格 |
| M5 | [最新Music Language](../professional-workspace-product-language-2026-09-21/MUSIC/CURIS_MUSIC_PRODUCT_LANGUAGE_CANDIDATE.md)、[Grammar Comparison](../professional-workspace-product-language-2026-09-21/CURIS_PROFESSIONAL_WORKSPACE_PRODUCT_GRAMMAR_COMPARISON.md) | RESEARCH / Review；CEO待审 | 保Song≠Work、Provider≠Employee、Choice/Gate/Operating及资产连续 |
| V1 | [旧Music HTML README](../../../MUSIC_WORKSPACE_HTML_EXPLORATION/README.md)§5–6 | 旧视觉探索/Mock证据，非Current；2026-09-22原研究轮次未复测 | 模拟试听、固定员工、虚构指标和无持久化不能当能力；本次Codex HTML验收另见Closure |
| W1 | [Writing结构候选](../writing-business-product-structure-2026-09-21/CURIS_WRITING_BUSINESS_PRODUCT_STRUCTURE_CANDIDATE.md)§3–10、13 | RESEARCH / Review；后续局部探索授权非Authority | 逐页价值/动作/输出/返回，定位和经营不替代创作深度 |
| W2 | [Writing能力采用审计](../writing-business-product-structure-2026-09-21/reference-capability-reconciliation/CURIS_WRITING_REFERENCE_CAPABILITY_ADOPTION_AUDIT.md) | REVIEW / Review；补齐候选 | 标签进入依据、候选保护、完整版本与应用回访 |
| W3 | [妍语会员工作流研究](../writing-business-product-structure-2026-09-21/reference-capability-reconciliation/CURIS_YANYUWRITE_MEMBER_WORKFLOW_DEEP_DIVE.md)§2–5、10–12 | RESEARCH / Review；观察样本有未完成边界 | 吸收方向选择与分层意图控制；不宣称每个标签已可靠控制模型 |

### 12.3 本轮外部定向补证（2026-09-22）

仅为修补影响产品路径的证据不足，没有泛搜行业、抓登录态或做Provider调用。

| 编号 | 直接来源 | 已确认 | 未确认与产品处置 |
|---|---|---|---|
| E1 | [汽水音乐合作平台](https://music.douyin.com/) | 官方搜索索引列歌曲发布/推广、数据分析/分账结算，并说明为原抖音音乐开放平台 | 正文直开超时，后台未观察；精确字段/接口/审核周期/AI政策皆未确认，按§9保守处理 |
| E2 | [Mureka Quickstart](https://platform.mureka.ai/docs/en/quickstart.html)、[API目录](https://platform.mureka.ai/docs/) | 官方API入口、API Key、生成任务形态；目录列歌曲/器乐等能力 | 当前账号、计费、商用用途、各能力真实质量未验证；不是Curis已集成 |
| E3 | [ElevenLabs Music Quickstart](https://elevenlabs.io/docs/eleven-api/guides/cookbooks/music) | 官方Music API教程，声明付费用户访问 | 无实际调用；不从教程推断所有付费用途均可发行 |
| E4 | [Music Terms](https://elevenlabs.io/music-terms)、[API Terms](https://elevenlabs.io/music-api-terms) | 前者存在输入限制及模型专属条款；后者另有客户集成类别要求 | Curis商业分类及具体模型/计划用途未裁定；需选定后定向核验，不给笼统商用保证 |
| E5 | [Suno Terms](https://suno.com/terms-of-service) | 付费输出有附条件权利安排，remix另有条件 | 不据此推出公开API存在或不存在；自动化通道和账号使用资格未确认。旧sunnoai.com来源不能证明官方身份 |

上述外部事实仅到公开说明；产品合同是本轮推导。未核当前价格，因此文档不推荐套餐、不写固定单价；计划生成前显示真实可核费用范围。知识产权归属、Provider使用许可、平台接受与商业收益四者不能相互代替。

### 12.4 变更登记

2026-09-22原研究轮次只新增本目录三份RESEARCH / Review文件；互链承担研究Index。2026-09-23按已接受HTML探索作窄幅Candidate对账，另增[Closure](CURIS_MUSIC_HTML_EXPLORATION_CLOSURE.md)；未修改Pointer、全局Index、CURRENT_STATE、Change Log或Current Truth，未将候选提升Authority。未改HTML、Figma、Runtime、Frontend、Backend、数据库；未stage/commit/push。

Verdict: CEO接受Music产品结构Candidate与HTML表达；PF-01/02/04/05及Market/Direction接续已补为产品约束，PF-03/06与真实能力仍保持验证边界。真实Provider、发行、数据、保存恢复仍待专项证据。

CURIS MUSIC BUSINESS PRODUCT CANDIDATE — HTML EXPLORATION RECONCILED / NOT FROZEN

STOP。
