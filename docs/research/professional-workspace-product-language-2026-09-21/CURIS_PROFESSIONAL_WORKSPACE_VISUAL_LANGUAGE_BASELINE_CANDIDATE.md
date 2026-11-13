# Curis Professional Workspace Visual Language — Baseline Candidate

Authority Class: RESEARCH
Status: Review
Date: 2026-09-21
Disposition: VISUAL LANGUAGE CANDIDATE — READY FOR CEO REVIEW
Owner: CEO / Design
来源：本轮CEO指令确认上一轮Product Language已通过Review；仅作为本候选输入接受，不代表原研究已自动升为Current Authority。
Next Gate: CEO Review；涉及Current差异须另行明确批准，不自动修改Authority或启动UI。

## 1. 定位与继承

共享的是视觉职责、关系和状态表达，**不是页面模板**。继续继承Direction D、Neutral Foundation、Iris稀缺使用、中文可读性、键盘焦点与可访问性、短且可中断的动效。字体与状态色等未验证项不在此冻结。

Professional Workspace不以“大量留白＋Card Dashboard”为统一方向。高级感来自秩序：关系相邻、重点明确、信息不重复、主要动作可找到、专业对象可读。原型成功只证明相应Mock交互，不能作为真实执行或视觉全量验收。

## 2. 三条空间原则：Calm Density

| 原则 | 可执行规则 | 反例 |
|---|---|---|
| Space for Judgment | 当前需要判断时，给依据、差异、后果和选择足够阅读空间；无待决不保留空白判断区 | 每页固定大Header或CEO横幅 |
| Density for Relationships | 对象—当前工作—责任人—状态—产物—下一步靠近，按相关性分组；重复计数只留一个有口径的来源 | 到多张卡寻找同一工作的关系；塞满所有字段 |
| Room for Artifact | 给正文、Diff、音频比较、视频/参考足够审视空间；元数据与高级操作退后 | 为统一密度压缩正文，或只给产物一行链接 |

密度先通过删重复、减容器、渐进披露、对齐与分组获得，不靠缩小字体/点击目标。长文本保持阅读节奏，队列保持可比较列，数字标单位与时间口径。Card仅用于确有独立边界的对象/选择/浮层，不按Section批量套卡。动作按当前问题出现，低频动作进详情/更多；核心入口仍须可发现且可键盘操作。

## 3. 两个中心，不是两个固定区域

**Artifact = Visual Center**：真实专业对象不能被聊天、日志或状态卡代替。在阅读、修改、比较与验收产物时，产物是主要视觉焦点。它不意味着每个首页都展示巨大产物，也不意味着尚无产物时制造预览占位。

**Employee = Agency Center**：用户能理解谁承担责任、正在判断/做什么、已返回什么、可以找谁交流。员工嵌在实际工作、产物来源和交接中，有持续身份；不能只剩Owner列，也不能以头像/员工卡墙取代专业工作。

默认呈现当前相关负责人和动作关系，按需展开团队。区分Work Owner与实际步骤/产物责任人；指定员工交流不串台。Provider是执行来源，不是员工或发言身份。一个员工多个Work、多员工同业务并行，按实际工作范围表达，不为每个执行会话复制员工。

## 4. 两种Surface Grammar

| Grammar | 首先组织什么 | 主要关系 | 不推导的布局 |
|---|---|---|---|
| Operating / Flow-centric | 当前目标与偏差、团队已做/正做/等决定、供应与交接、下一检查 | 经营判断→相关工作→结果/反馈→下一步 | Flow不等于DAG；不要求固定Workflow、看板或顶部判断＋底部执行 |
| Project / Artifact-centric | 长期对象的正式状态、当前变化/候选、相关工作与待选 | 对象/版本→变化→依据→决定→接受状态 | 不要求相同编辑器、同一导航或最大区域永远给产物 |

Content Growth是Operating主要证据，RD/Writing是Project主要证据。Music从Business Operating进入Song Project-like Surface，保同一身份与来源返回。**Hybrid是组合，不是第三套模板。**同一业务可以因工作目的切换组织方式，不按业务标签锁死页面。

## 5. Four-Pane与当前主位

Navigation负责公司级位置；Context负责专业导航、集合与当前局部范围；Main负责selected Professional Surface＋相关Shared Work Area；Utility负责按需检查/详情/专业工具。不是固定四栏，不为空栏留空间。默认Nav＋Main能独立理解和完成主要工作；Context/Utility遵守既有收起、调整、最大化和Pane-local Header合同。

Conversation是持续工作关系。Main可因当前工作由交流、专业产物、经营面或决定内容占视觉主位；不据此删除相关业务身份与来源。进入具体员工仍遵守Main.Shared Work Area的Conversation-first合同，不能把完整员工对话搬到Utility。

证据审阅可获得主要阅读空间；**当前合法路径优先是Utility最大化**。视觉主位≠Main宿主变更；将完整Evidence直接迁入Main的扩展记入Delta C1，未批准前不执行。相同边界适用于Result：汇报、专业产物与证据不可因同样能打开而混称。

## 6. 统一视觉职责，不统一组件或专业页面

| 概念 | 用户必须辨认 | 默认表达 / 展开边界 |
|---|---|---|
| Employee | 谁负责、与当前工作的关系、找谁说 | 关联实际工作与返回；团队/权限详情按需 |
| Work | 目标、当前状态、负责人、可介入动作 | 专业内容优先；执行参数/日志非默认主体 |
| Conversation | 正在和谁、谈哪个对象/版本 | 轻量引用与可返回产物；不复制整份正式产物为聊天真源 |
| Artifact | 内容本身、当前版本及归属 | 专业阅读/比较空间；不同媒介不同工具 |
| Candidate | 尚未接受、针对哪一版、可选择什么 | 与正式版明确区分；选择不假装已写入 |
| Result | 做了什么、意义、未解决项、下一步 | 引用产物/Evidence，必要时成为焦点，不造结果卡墙 |
| Evidence | 来源、对象/版本、时点/口径、证明边界 | 摘要关联判断；完整内容按当前Utility合同检查 |
| Decision | 要决定什么、谁有权、后果与范围 | 按目的表达，见§7；普通进度不是Decision |
| Context | 当前范围和影响判断的依据 | 用账号/章节/文件等自然对象表达，不强制“Context”产品区 |
| Utility | 为哪个问题打开、当前对象、如何返回 | 保原筛选、选区、版本与位置；不只会返回Conversation |
| State | 真实发生、等待什么、下一合法动作 | 文案/标识与颜色共同表达，不靠颜色单独传递 |
| Version | 正式、候选、当前执行输入及历史关系 | 当前判断必要版本可见；全历史/依赖按需，不满屏技术标签 |

## 7. Decision表达

- **Choice**：正文/方案/音频等正常选择。中性展示可比较内容、理由与采纳范围，可拒绝全部；不因等待作者就显示红色异常。
- **Gate**：实际权限、风险、外部副作用或必需审核。显示目标、版本、影响和等待点；批准≠执行成功，参数实质改变需重新判断。
- **Operating Decision**：目标、策略、节奏或资源调整。呈现当前与建议、依据、影响范围和下一步，不制造第二经营配置系统。

三者是可重叠的交互目的，不新增Runtime对象，不按业务固定配色或默认CEO审批。权限与既有P7仍有效；超出当前P7的快速采纳规则不能由视觉候选自行批准。

## 8. 状态诚实

| 必须区分 | 视觉/文案规则 |
|---|---|
| Waiting ≠ Failed | 写明等人/等数据/等依赖及下一检查；没有失败不使用失败语气 |
| Unknown ≠ 0 | 标未知/未采集/不可得并说明来源缺口；不能用零填补 |
| Provider Running ≠ Work Working | Provider仅表示一次执行活动；Work可同时等待审查/被阻塞，不由执行动画推导业务进展 |
| Accepted ≠ Applied ≠ External Effect | 分别表达决定已接受、实际已应用、外部已核验；失败保留已完成事实 |
| Human Choice ≠ Exception | 正常创作选择中性可达；真实风险另示 |
| Version Updated ≠ Downstream Updated | 标明受影响/待重验；保留旧产物与在途版本，不假装全链同步 |

无可靠分母不画进度百分比；供应数量、断档风险不是进度条。动画、计时和估计不代替状态证据。失败和效果未知给不同动作，未知外部效果不能默认“一键重试”。状态颜色继续按Current语义，未新增token。

## 9. 长期连续性与资产归属

用户回来能找回：当前对象与范围、谁在工作、最近Result、待决事项、正式版本和下一步。相关信息可按任务分层，不要求常驻六张卡。切换/关闭检查面不丢对象位置；空状态说明缺什么和可做什么，不制造假运行数据。

Business Working Space只以所属业务/项目/作品、来源与持久引用轻量表达。目录不是专业导航，Provider临时文件不是唯一归宿；不做Finder，不设计真实文件系统。重开后持续状态不等于后台进程一定仍运行。

## 10. Professional Override与四次反证

| 业务反证 | 若套统一模板会怎样 | 保留的专业自由 / 降级的规则 |
|---|---|---|
| Content Growth：比较参考后介入制作 | 巨大Artifact固定占首页会遮住账号判断和交接 | Reference、生产Flow、队列/比较按当前任务展开；删除“所有首页Artifact最大” |
| RD：讨论需求后审阅Diff | 永久Conversation最大看不清变化；永久Diff最大又妨碍澄清 | 对话与Diff/Code按任务成为焦点；不恢复IDE或统一DAG |
| Writing：连续读正文并部分采纳 | 紧凑多列把故事切碎，固定技术侧栏挤正文 | 正文阅读空间与作者选择优先；Story State可独立Main；密度规则只约束关系不压缩文字 |
| Music：经营组合进入候选试听 | 套文字稿编辑器或卡式Dashboard无法比较版本 | 专门试听/版本空间，回同一Song/经营范围；Hybrid不新增第三模板 |

反证后保留Grammar，删除固定位置/尺寸/媒介/步骤/员工数。共享规则若迫使四者同页，按此原则降为局部建议或撤除。

## 11. 明确禁止与后续检查

禁止万能页面模板、固定四栏、Card Wall、Employee Card Wall、Universal Workflow Canvas、Universal Task Board、IDE/ERP/Jira/ChatGPT Clone；禁止所有业务统一导航或统一Artifact Viewer。禁止通过换色掩盖同一模板，禁止以“减法”删掉来源、权限、失败与返回。

后续设计检查只问：当前工作是否一眼可辨？责任人与产物是否连贯？判断是否有依据？复杂信息是否能找到且能返回？普通选择是否中性？正式/候选/已应用/外部状态是否分清？专业媒介是否获得合适空间？四业务是否仍各自成立？可访问性与真实状态需在后续实现验证，本轮不宣称通过。

来源与Current对账见[Visual Language Delta](CURIS_VISUAL_LANGUAGE_DELTA_FROM_CURRENT.md)。本轮只生成两文档，不修改输入、Authority、HTML、Runtime或UI。

CURIS PROFESSIONAL WORKSPACE VISUAL LANGUAGE BASELINE CANDIDATE — READY FOR CEO REVIEW

STOP FOR CEO REVIEW。
