# Professional Workspace Product Grammar Comparison

Authority Class: RESEARCH
Status: Review
Date: 2026-09-21
Disposition: CROSS-BUSINESS CANDIDATE — CEO REVIEW REQUIRED
Owner: CEO / Product
Next Gate: CEO确认产品语言范围后，单独启动Visual Language Baseline Candidate。

来源简称见[研究索引](CURIS_PRODUCT_LANGUAGE_RECONCILIATION_INDEX.md)。本文件在三业务独立推导之后比较，不是生成三业务的通用页面模板。Content Growth依据已有原型Review，不把Mock E2E当真实平台/Runtime验收。[V4]

## 1. 分类成立，但不是互斥的Business类型

| 业务 | 长期中心 | 用户主要循环 | 主导分类 | 不能由分类推导什么 |
|---|---|---|---|---|
| Content Growth | 账号目标、内容组合、策略及真实表现 | 授权范围内连续发现→制作→发布→观察→调整 | Operating | 不是每天必须按固定Workflow导航；某条内容仍有复杂长期制作 |
| RD | Software Project的接受状态、代码及证据 | 提出变化→执行→验证→接纳→维护 | Project | 不等于缺经营、不需要发布反馈，也不是IDE |
| Writing | Book Project、正式正文与Story State | 构思→候选→作者判断→正式写入→检查与继续 | Project / Creative | 不意味着无限自动开下一章；暂停创作可以正常 |
| Music | 业务方向与歌曲组合；单曲长期版本 | 经营层持续循环，Song内反复试听选版与交付 | Hybrid | Song不是新增组织Workspace；不必全局增加Project类型 |

分类是两条观察轴：**持续经营的范围**与**长期专业对象的工作深度**。RD/Writing也有经营，Content Growth也有项目式制作；Music两层都必须显式承载。四者不需要四套Company OS。

## 2. Shared Grammar：比较生命周期，不只比较词语

| 语义 | Content Growth | RD | Writing | Music | 可共享的合同 / 不共享的部分 |
|---|---|---|---|---|---|
| Employee | 长期研究/制作等责任人 | 项目责任人，不是Coding Agent | 编辑，不是小说人物或每个审校Pass | 制作/发行责任人，不是Suno | 身份长期，人员更替保历史；人数不由导航决定 |
| Responsibility | 内容供应、制作、发布等 | 需求、实现、验证等 | 编辑、连续性、写入核验等 | 研究、制作、发行、分析等 | 长期责任可分配；专业定义不强行共用 |
| Assignment | 员工在业务范围承担责任 | 同人多项目须逐范围授权 | 同人多书不自动共享私稿 | 一区多人/一人多责 | Employee×Role×Scope；不是Provider会话 |
| Work | 一次研究/交付/观察 | 一次改变或验证Project | 一次写作/修改/检查 | 一次生成/选版准备/发布核验 | 目标、责任、输入、结果与完成标准；不统一专业步骤 |
| Conversation | 围绕账号/内容/步骤 | 围绕项目/变化/文件 | 围绕作品/章节/候选 | 围绕Song/版本/片段 | 同一身份与合法范围，保来源返回；不是所有工作都必须发聊天 |
| Artifact | 脚本、视频、封面 | 代码、文档、测试等 | 正文、计划、设定等 | 歌词、音频、封面等 | 有所属对象、版本、来源；编辑器与审阅方式不同 |
| Candidate | 选题、内容稿、策略建议 | 待接纳工程变化 | 未采纳正文/Canon建议 | 待选音频/方向 | 提议→明确决定→成功应用；不是四业务共用新数据库对象 |
| Result | 工作汇报引用交付与观察 | 变更/验证/未决说明 | 候选、检查或写入报告 | 制作/选版/发行汇报 | 报告不复制产物，不等于自动接受或外部成功 |
| Evidence | Publication、数据源、观察窗 | revision、测试环境、实际输出 | 正文段落、Canon版本、检查依据 | 音频版本、回执、平台观察 | 对象/版本/来源/时间可追溯；判断标准不能统一 |
| Decision | 内容接受、发布边界、策略 | 方案取舍、接纳、生产授权 | 作者采纳、Canon变更、出版 | 试听选择、权利/发布、经营 | 明确决定者、范围、输入版本、结果及失效条件；正常选择不是异常 |
| Context | 账号/策略/参考/交付 | Project/Work/Execution/Conversation | 章节/正式事实/计划/候选 | 方向/歌词/版本/来源 | 有权且相关，实际使用可查；不是固定一个Context栏 |
| Utility | 临时资料、证据、详情 | Source/Diff/Preview及相关证据 | Ledger、证据、版本检查 | 发布回执、参数、权利材料 | 是辅助当前任务的承载职责，不保证同一对象永远在侧栏 |
| Learning | 观察→洞察候选→策略接受 | 缺陷/交付反馈→方法改进 | 审校经验/偏好；Canon不是Learning | 创作经验与市场学习分开 | 有来源、范围、采用状态；不自动重写事实或策略 |

这些是产品解释与既有对象的对账，不新增Candidate Runtime、Decision子系统或统一知识存储。已确认的Shared关系继续消费A1–A4；领域对象和候选增强仍待CEO Review。

## 3. 三类Decision是交互目的，不是三个新对象

| 模式 | Trigger | Risk | Frequency | UI Behavior（职责，不定布局） | Authority | Result |
|---|---|---|---|---|---|---|
| Choice | 多方案/改稿/试听/方案取舍 | 选择错误或基线过期 | Writing/Music高频；RD/Content也存在 | 展示可比较产物、理由、范围；允许拒绝全部/部分接受，不默认红色故障 | 作者、指定审阅者或已授权Leader | 选择记录；按范围应用/形成后续Work，未必发布 |
| Gate | 外发、权限、不可逆变化、超预算或必需审核 | 外部副作用、隐私、资产损失 | 按动作风险触发，不按业务类别固定频率 | 说明将发生什么、对象版本、影响、等待点；变更快照需重判 | 对该动作有权者；CEO并非所有Gate唯一人选 | 批准/拒绝/补充要求；成功还要执行核验 |
| Operating Decision | 目标、策略、资源、节奏变化 | 持续经营范围改变 | 周期性或事件触发 | 比较当前与建议、影响和依据 | Envelope内Leader；超范围CEO | 生效范围/版本/下一步；旧Work快照保留 |

三分类可用但不互斥：接受一个高成本Music候选可同时含Choice与预算Gate；修改软件架构可含Choice与Operating Decision。不能只存一个标签推导全部权限。登录/MFA接管是等待用户操作，不自动等于CEO业务Decision。

## 4. 长期资产与执行连续性

| 业务 | 长期归属 | 执行中的临时产物 | 接受后如何连续 |
|---|---|---|---|
| RD | Business下Software Project代码/文档/测试/架构 | 隔离变更、Provider输出 | 核对基线与验证后接纳；发布另外核验 |
| Writing | Business下Book正文/Canon/人物/大纲/研究 | 未采纳候选与审校报告 | 作者明确采纳，写入读回与知识同步状态分别可见 |
| Music | Business下Song参考/歌词/版本/Master/封面/发行证据 | 生成中请求、待选音频 | Master身份稳定，多平台发布记录引用指定版本 |
| Content Growth | Business下账号/内容/交付的专业资产 | 制作候选、步骤产物 | 确认交付版本，Publication与Observation保来源 |

B1的Business Working Space是逻辑资产归属候选，不替换Company组织Workspace，也不等于一次Execution目录。不强制所有资产Git化，不按Employee保存唯一资产。物理路径、Adopt/Copy、备份机制仍属后续Gate，本轮未创建实际业务资产根。

结果必须区分：**已产生→已验证→已接受→已应用→已外部生效**。不同Work终点不同，不是每件工作都强制走五步。恢复先查已发生事实；外部效果未知不能直接重发。暂停一个候选或一首歌不暂停全部独立工作。

## 5. 明确不能统一

1. 不统一导航数量：Content Growth七区、Music五区；RD最小两类工作面；Writing三类工作面。Surface不等于必须新增Tab。
2. 不统一首屏：经营看当前判断和动作，研发看项目变化，写作看作品与正文，音乐Song看可听版本。
3. 不统一工作流：图文、软件变更、章节写入、音频发行没有一条共用步骤链。
4. 不统一完成标准：测试绿、作者采纳、Master确认、平台上线不是同一个Done。
5. 不统一人参与节奏：Writing正常反复选择；运营可授权连续推进；RD/Music依具体动作与边界。
6. 不统一Artifact编辑器：Diff、正文差异、音频试听、视频预览分别成立；不造万能工作编辑器。
7. 不统一Knowledge与事实：Canon、工程基线、市场Learning、审美偏好不同；不能互相自动覆写。
8. 不统一资产存储技术、Provider、人数、固定四栏宽度、固定Conversation比例与固定Decision警报条。

## 6. 两轮视觉探索需要修正的结论

| 来源 / 原结论倾向 | 保留什么 | 本轮修正 |
|---|---|---|
| V1 Project长期产物与当前工作 | 长期对象连续，工作不等于项目 | RD/Writing相似不代表同一页面；写作Story State不能缩成一般文件列表 |
| V1 Writing来源不足 | 原图保为表达样例 | W1–W3补齐；此前样例不能证明写作功能合同完整 |
| V1 Artifact永远主导 / R2 Conversation固定主导 | 都是重要工作面 | 按当前任务：讨论、审阅、写作、试听切主位；不冻结百分比分栏 |
| V1 RD异常Gate、Writing常规Choice | 人参与有不同节奏 | 四业务均可能有三类Decision；普通作者选择不画系统事故 |
| V1 Writing三员工样例 | 身份、当前工作可见 | 默认一编辑+Skills仍成立，三人不成为产品配置 |
| V2 Employee是流程属性的表达 | 人可嵌入工作，无卡墙 | Employee有独立长期组织身份，不能退化为Workflow字段 |
| V2 推荐C Hybrid | 经营判断与可操作工作并列的思路 | 视觉密度Hybrid不是Music业务Hybrid，也不是跨业务通用版式结论 |
| V1/V2固定顶部待决、默认关闭Utility等 | 渐进披露与保留返回 | 只是探索选择；当前A3/A4宿主合同优先，不因本轮另造Shell |
| V3一区一员工、评分选版 | 五工作区、版本试听和发行接续 | 0..N Assignment；评分Mock没有审美/商业证据，不能取代试听 |
| V4完整链条验证 | 复用同一对象/版本/责任/交接思路 | 属Mock产品表达E2E；不可声称真实平台可发布、跨业务已验收 |

原HTML、截图、视觉Findings全部保留，不做覆盖或回填伪证。旧Research与Current差异按来源级别纠偏，本轮未确认需要自行裁决的Current对Current冲突。

## 7. 反证检查

| 压力场景 | 合同回答 | 边界 |
|---|---|---|
| 同Employee同时服务两软件项目 | 多Work、逐项目合法Context与隔离输入 | 不从同一身份推导文件共享 |
| 作者拒绝所有候选 | 正式正文不变，保留理由，可继续或暂停 | 不触发“自动修到接受” |
| 作者采纳后同步失败 | 正文保存与知识待同步分别表达 | 不标全成功，不重复追加 |
| Music选版与预算冲突 | 保留审美选择，费用/执行单独待决 | Choice不暗含额外付费授权 |
| 生成Provider更换 | Employee/Song/Work identity不变，执行来源另记 | 旧版本来源不能改写 |
| 无后台运行能力用户关机 | 恢复长期状态，再核实Execution | 不宣传离线仍持续经营 |
| 平台没有Completion字段 | 不可得，不填0，不推算为事实 | 其它可得数据仍能形成有边界分析 |
| RD只研究方案 | 接受研究Result即可结束该Work | 不强制Diff/PR/Release |
| Writing人物在角色对话中说谎 | 非Canon演练，需作者判断才转正式 | 不把聊天内容直接当故事事实 |
| Music平台A已上线、B未知 | 保两平台独立回执，核验B | 不重发A，不删除Song |

## 8. Visual Baseline Candidate的输入边界

可以作为下一轮候选输入：稳定身份与责任、目标对象/版本、当前工作、产物与证据、正常Choice和风险Gate的区别、来源返回、等待/未知/失败的诚实表达。

不批准：新模板库、统一导航、通用DAG、固定员工区、所有业务Artifact主导、实际Provider可用性、最终Shell改版。后续视觉研究需分别验证研发变更审阅、写作部分采纳、音乐试听选择、内容制作介入；一张漂亮截图不能替代四类不同操作。

**Verdict：三业务产品语言候选与跨业务比较已形成，可供CEO Review。CEO接受后可进入有证据边界的Visual Language Baseline Candidate；不是本轮已Frozen或自动启动视觉设计。**
