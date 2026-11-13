# CURIS BUSINESS TO PRODUCT TRANSLATION LEDGER

> Status: Draft（业务→产品翻译台账 · Content Growth 样板）
> Authority Class: REVIEW — 未来 Product Structure 与 UI 的直接上游；每条必须能追溯到业务场景。
> Updated: 2026-09-14 · T-CG-001 ~ T-CG-026 · 来源：CURIS_CONTENT_GROWTH_BUSINESS_TO_PRODUCT_TRANSLATION.md。
> Existing Status 图例：✅ 已支持 / 🟡 部分支持 / ❌ 缺失 / ⚠️ 现有模型表达错误或不完整。
> Interaction 只描述操作类型（click/select/type/toggle/popover/modal/navigate/utility/inline/composer），不谈视觉。

| ID | Business | Business Scenario | User Need | Product Capability | Existing Status | Product Placement | Interaction | Required Information | Failure / Recovery |
|---|---|---|---|---|---|---|---|---|---|
| T-CG-001 | Content Growth | "三个月把业务做起来"落成标准 | 目标可判断、可对照 | 定义目标与成功定义（方向/时间/成功/偏离/约束/预算/停止条件） | 🟡 Business Goal 有；三层分离与停止条件缺 | Business（Persistent Truth） | 对话提案→逐条 inline 确认；设置内可再编辑 | 目标句；检查点；成功标准；约束；预算上限；停止条件 | 标准含糊→继续澄清，不阻塞开业 |
| T-CG-002 | Content Growth | 决定怎么赢：主题/平台/形态/不做什么 | 打法可确认、可调整、可复盘 | 制定/确认/圈内调整打法；版本历史 | 🟡 business_directions+Envelope 权威有；产品表达与溯源缺（G-22） | Business | 打法提案→确认；圈内调整直接生效留痕；出圈转 CEO；历史版本查看 | 当前打法含负空间；版本依据；与成功定义对照 | 越圈→自动转 CEO 决策带建议 |
| T-CG-003 | Content Growth | 持续知道外面发生什么 | 信号可信、时效明确、不漏 | 配置信息源；收到信号；转机会/忽略 | ❌（CG 内需要）→G-25 | Business 研究面；连接类源在 Settings | 添加源（type+select 频率）；信号列表 click 展开；转选题/忽略；自动收集 toggle | 信号（来源/时间/摘要/时效/可信度）；源健康；上次收集 | 源失效→换源/重配；拿不到→浏览器或人工（标注来源） |
| T-CG-004 | Content Growth | 观察竞品账号怎么做 | 添加/停止观察；看变化；引用；深研 | 管理观察对象（Observed External Entity）；派深研 Work | ❌ →G-26 | Business 研究面 | 添加竞品（select 平台+type 链接）；列表 click 最新变化；单条「引用到选题」；「深研」派员工 | 竞品列表与详情；数据新鲜度；我们的分析 | 数据拿不到→浏览器（授权档位）/人工导入标注 |
| T-CG-005 | Content Growth | 信号+洞察→下周做什么 | 选题有依据、有目标关联 | 记录选题；信号转选题；批量选题会 | ❌（Authority 概念有）→G-27 | 内容工作面 | 信号行「转为选题」inline 保存；选题会批量提案勾选；依据引用回看 | 选题列表（标题/依据/目标关联/状态）；时效 | 误转可删（未排期）；过时淘汰留痕 |
| T-CG-006 | Content Growth | 告诉执行者这条内容要什么 | 要求准确、可交接 | 写 Brief；从选题生成草稿（挂引用） | ❌ →G-27 | 内容工作面（Work 输入） | 「开始创作」生成 Work+Brief；inline 编辑；「+引用」挂竞品/品牌资料 | 受众/要点/口径/引用/时效 | 执行中发现缺信息→对话追问 Leader 补充留痕 |
| T-CG-007 | Content Growth | 委托写作并多轮调整；重要内容想用更强模型 | 发要求、调整、本次换执行、拿产出 | Composer 发任务；对话调整；**本次执行切换（模型/Agent）**；产出查看 | 🟡 对话+模型选择器已实现【事实】；显性执行选择/Stop/Steering 缺 | Conversation→Composer；产出 Result→Utility | Composer 输入发送；执行选择器 select（本次生效）；引用行 click→Utility；失败「换执行重试」；运行中「停止」 | 本次执行者；Brief 摘要；产出状态；预估成本 | Provider 不可用→员工仍在→换执行者（CAP-008） |
| T-CG-008 | Content Growth | 封面/配图交给视觉员工 | 拿到可用图并定稿 | 派活（带 Brief+品牌规范）；预览；定稿进内容包 | ❌（图像 Provider 未接入）→G-31 | 视觉员工对话线；Utility 预览 | Composer 派活（引用 Brief/规范）→图集引用行→Utility 预览→「定稿」 | 版本图集；所用模型工具；规范引用；定稿状态 | 风格跑偏→查规范引用；工具不可用→换 Provider |
| T-CG-009 | Content Growth | 专业团队还是全能员工；分工与交接 | 按人手选择组织；分工清楚；交接不丢 | 派任；一人多责任；Leader 分工；CEO 改派；Handoff | 🟡 任职/路由/Handoff 权威有；团队视图表达不完整 | Business 团队视图+对话 | 团队矩阵视图；对话分工→任职调整提案→确认；成员「调整责任」；交接自动事件行 | 成员×责任矩阵；在途；空岗；交接记录 | 员工离任→责任交接提案→确认；历史不改写 |
| T-CG-010 | Content Growth | 普通内容自动发、商业内容要我确认 | 按风险决定谁审；CEO 不做机器人 | 设置发布政策（类型×账号→三档） | ❌（C-12 未落地）→G-27 | Business 设置；执行在现场 | 政策表（行=类型，列=档位，select） | 政策矩阵；适用说明 | 政策冲突→升级 |
| T-CG-011 | Content Growth | 待审内容批/驳/改 | 审得快、驳得清 | 执行审核；待审队列 | 🟡 旧 XHS 实例有审核决策；通用缺 | 内容现场；CEO 档走通知/工作台 | 待审项 click→预览→「批准」/「驳回」（type 理由→退回作者对话） | 内容预览；档位原因；审核人；时效 | 驳回→作者改→重提 |
| T-CG-012 | Content Growth | 一条内容发到形态不同的账号 | 按账号适配、校验规则 | 为账号生成适配版；逐账号微调；规则校验 | ❌ →G-27 | 内容工作面/发布准备 | 发布准备选账号→适配建议→逐账号 tab inline 微调；不符高亮点击看规则来源 | 每账号预览；平台规则要点+来源+更新时间 | 不符→按提示修改；规则存疑→看来源 |
| T-CG-013 | Content Growth | 我在小红书/抖音上的经营身份 | 添加账号；经营定位/受众/策略；看发布史与数据 | 添加账号；账号经营面；账号策略；暂停经营 | ❌（Authority 有 Channel/Account）→G-27 | Business（经营面）；身份在公司层 | 「添加账号」select 平台+填身份；列表 click→经营面 inline 编辑 | 账号列表（平台/名/连接状态/最近发布/表现）；经营字段；主要经营责任标注 | 未连接→「去连接」直达 Settings；被封→显式状态+影响 |
| T-CG-014 | Content Growth | 让 Curis 能代表我操作账号 | 连接/重连/断开/换方式 | 连接账号（OAuth/API/浏览器/人工）；重新授权 | ❌（模型连接已实现；平台 Connector 无授权入口【事实】） | Settings/Connections；业务失败提示直达 | 连接表单 select 方式→跳转/贴 Key→「测试」→保存；失效行「重新授权」 | 授权方式/状态/最近同步/权限范围 | 过期→重跳/重登；断开→确认（历史保留） |
| T-CG-015 | Content Growth | 内容就绪，立即或定时发到多账号 | 发出去并逐账号确认 | 发布到账号；排期；逐账号状态与回执 | ❌（S5 已推）→G-27 | 业务现场（发布队列/日历） | 「发布」多选账号（checkbox）→Variant 预览→政策判定→select 立即/datetime→队列逐账号状态行 | 队列（内容×账号×状态×回执×时间）；失败原因；政策档位 | 失败→重试/换连接；被拒→按原因修改 |
| T-CG-016 | Content Growth | 3 个账号成 1 个败 | 失败的单独处理，不全部重来 | 逐账号重试；部分成功状态 | ❌ →G-27 | 发布队列 | 失败行「重试」；部分成功逐行显示 | 逐账号状态；失败原因 | 授权过期→重连后重试 |
| T-CG-017 | Content Growth | 删掉已发的一条内容 | 删除是新的对外动作，要确认与回执 | 平台删除已发内容（新对外动作） | ❌ →G-16/G-27 | 发布队列/内容包 | 已发行「…」→「平台删除」→确认弹窗（说明对外属性）→删除回执 | 删除状态；平台结果 | 删除失败→重试；无法删→如实显示 |
| T-CG-018 | Content Growth | 这条内容/账号表现如何 | 数据可信、缺口诚实 | 查看内容/账号表现（原生指标+统一维度切换） | 🟡 洞察已实现【事实】；平台数据接入缺 | 业务现场；Operating Intelligence（深度） | 内容行点开 per 平台 tab；洞察切范围 | 原生指标+平台名；采集时间/来源；Unknown 原因 | 未连接→连接后补采 |
| T-CG-019 | Content Growth | 平台没回数据但我知道数值 | 手动补数并保留来源 | 手动录入数据（带来源标注） | ❌ →G-27 | 业务现场数据缺口行 | 「手动录入」表单（数值+来源说明） | 数值；来源；录入人/时间 | 误录→更正留痕 |
| T-CG-020 | Content Growth | 观众评论/私信要回，还能变选题 | 不漏互动、回复得体、转化为机会 | 查看互动；拟回复（政策）；发送（对外动作）；转选题；升级敏感 | ❌（Authority 社区闭环有）→G-28 | 业务现场互动流 | 列表 click→「拟回复」→政策判定→发送；「转为选题」 | 互动内容/账号/情感/已回状态/关联内容 | 敏感→升级 CEO；发送失败→重试或人工标注 |
| T-CG-021 | Content Growth | 什么内容/形式有效 | 把数据变成调整依据 | 查看本业务分析报告；追问分析师 | ✅ Operating Intelligence IMPLEMENTED【事实】 | 经营洞察（scoped 进入回原上下文） | 业务内「查看分析」→报告→「追问」→分析师对话 | 范围/周期/事实/解读/未知/建议 | 数据不完整→报告内显式 Unknown |
| T-CG-022 | Content Growth | 本轮学到"案例类互动率高" | 学到的东西改变下一轮 | 记录复盘结论；落地到打法/账号/员工（勾选确认） | 🟡 Learning 语义有；落地表达缺 →G-29 | 复盘（业务）→写入 Truth | 结论卡→「应用到」勾选→确认写入（策略新版本等） | 本轮事实/结论/应用去向 | 应用失败→留痕重试 |
| T-CG-023 | Content Growth | 这个打法别的业务也可能有用 | 升级为公司知识（有确认） | 升级公司知识（Leader 提出+CEO 确认，标注来源） | ❌（C-18 规则已定）→G-29 | 复盘→Knowledge | 「升级为公司知识」→两级确认→入库 | 升级状态；确认人；来源业务 | 被拒→留业务层可再提案 |
| T-CG-024 | Content Growth | "每月 AI 费用不超过 100 美元" | 花费可控可见可预期 | 设置月度预算与超限政策；费用构成；高成本前确认 | ❌（Usage Ledger 有）→G-30 | Business 设置；提醒在通知；确认在发起处 | 预算（type 金额+select 政策：硬停/降级/仅提醒）→进度显示；高成本 Work→预估+确认 | 已用/构成/剩余；订阅类标"预估"；阈值 | 超限→按政策降级/暂停并通知；CEO 可临时扩额留痕 |
| T-CG-025 | Content Growth | 没有研究/浏览器/发布 API 时的执行 | 让员工"使用"订阅的外部执行者 | 连接外部 Agent（Settings）→授权员工→Composer 使用→Work 归因 | ❌（S4 模型已推）→G-04 | Settings/员工/Composer/Work | 同 CAP-004/008 链路 | 执行者身份；健康；本次谁执行 | Provider 不可用→换执行者；配额尽→排队/请示 |
| T-CG-026 | Content Growth | 同一账号在经营/连接/授权三个时刻 | 各看所需一面，永不同步错 | 跨上下文查看（经营面/连接面/授权面互达） | 🟡（原则已定，PRODUCT BEHAVIOR） | Business/Settings/员工授权三投影 | 各上下文入口互跳；失败提示直达重连 | 各上下文字段（经营/连接/授权） | 一处更新三处一致（单真相） |

## FULL PRODUCT CAPABILITY DERIVATION 增补（2026-09-14 · 本轮只更新 Capability/Need/Owner/Context/Priority/Confidence，不定 Surface/Layout）

### T-CG-001~026 状态矩阵（Owner / Context / Priority / Confidence）

| ID | Owner | Context 入口 | Priority | Confidence |
|---|---|---|---|---|
| T-CG-001 | Business | 业务设置/对话 | CORE | VERIFIED |
| T-CG-002 | Business | 业务/对话 | CORE | VERIFIED |
| T-CG-003 | Business 研究面 | 现场 | OPERATING | STRONG |
| T-CG-004 | Business 研究面 | 现场 | OPERATING | STRONG |
| T-CG-005 | 内容工作面 | 现场/对话 | CORE | VERIFIED |
| T-CG-006 | 内容工作面 | 选题行 | CORE | VERIFIED |
| T-CG-007 | Conversation/Composer | 工位 | CORE | VERIFIED |
| T-CG-008 | 员工对话线 | 对话/Utility | CORE | STRONG |
| T-CG-009 | Business Team | 团队视图/对话 | CORE | VERIFIED |
| T-CG-010 | Business 设置 | 设置 | CORE | VERIFIED |
| T-CG-011 | 内容现场/通知 | 待审项 | CORE | VERIFIED |
| T-CG-012 | 发布准备 | 发布流 | CORE | VERIFIED |
| T-CG-013 | Business | 账号列表 | CORE | VERIFIED |
| T-CG-014 | Settings/Connections | 失败提示直达 | CORE | VERIFIED |
| T-CG-015 | 发布队列 | 内容包/日历 | CORE | VERIFIED |
| T-CG-016 | 发布队列 | 队列行 | CORE | VERIFIED |
| T-CG-017 | 发布队列/内容包 | 已发行 | OPERATING | VERIFIED |
| T-CG-018 | 业务表现/洞察 | 表现页 | OPERATING | STRONG |
| T-CG-019 | 业务表现 | 缺口行 | CORE（无 API 主通道） | VERIFIED |
| T-CG-020 | 业务互动流 | 互动 | OPERATING | STRONG |
| T-CG-021 | Operating Intelligence | scoped 入口 | CORE | VERIFIED（已实现） |
| T-CG-022 | 复盘/Knowledge | 复盘 | OPERATING | VERIFIED |
| T-CG-023 | 复盘→Knowledge | 复盘 | OPERATING | STRONG |
| T-CG-024 | Business 设置 | 预算/通知/发起处 | OPERATING | STRONG |
| T-CG-025 | Settings/员工/Composer/Work | 四段入口 | OPERATING（连接层 CORE） | STRONG |
| T-CG-026 | 三投影（PRODUCT BEHAVIOR） | 三上下文互跳 | CORE | STRONG |

### 新增能力行（本轮推导新产出）

| ID | Product Capability | Need | Owner | Context | Priority | Confidence |
|---|---|---|---|---|---|---|
| T-CG-027 | 平台自动化能力范围显示 | 知道该平台哪些环节能自动/需人工 | Platform Facts | 连接页/适配/发布 | OPERATING | STRONG |
| T-CG-028 | 平台官方后台入口（Deep Link+最后访问） | 身份/资金/申诉类操作跳官方 | Platform Facts | 账号面/业务 | OPERATING | STRONG |
| T-CG-029 | 平台规则变化感知与影响评估 | 规则变了知道影响哪些账号/内容/计划 | Platform Facts+Leader | 通知/业务 | OPERATING | STRONG（自动监测 CANDIDATE） |
| T-CG-030 | 规则变化后未发内容重新校验 | 未发内容不按旧规则发出 | 发布准备 | 队列 | OPERATING | STRONG |
| T-CG-031 | 账号健康一览 | 一眼看懂账号是否健康 | Account | 账号列表/事实面 | CORE | STRONG |
| T-CG-032 | 账号异常处理（限流/违规/封禁） | 异常有应对而非黑箱 | Account | 账号面/通知 | OPERATING | STRONG |
| T-CG-033 | 账号时间线与最近变化 | 快速找到该账号最近内容/数据/互动/Learning | Account | 账号面 | OPERATING | STRONG |
| T-CG-034 | 账号生命周期与历史查看 | 为什么当初这么经营 | Account | 账号面 | OPERATING | STRONG |
| T-CG-035 | 账号经营责任归属与调整 | 账号不能没人负责，但不强制单人 | Business Team | 账号面/团队视图 | CORE | STRONG |
| T-CG-036 | 账号暂停/恢复/转移/共享 | 经营关系可变，历史保留 | Account/Company | 账号面/Settings | OPERATING | VERIFIED |
| T-CG-037 | 重复添加检测 | 防同一账号重复建 | Business | 添加流 | OPERATING | STRONG |
| T-CG-038 | 排期受阻处理（改期/换账号/改派） | 授权过期/封号时排期不悬空 | 发布队列/Leader | 队列受阻行 | OPERATING | STRONG |
| T-CG-039 | 人工代发与回执回填 | 无 API 时唯一发布通道 | 发布流 | 队列/Variant | CORE | VERIFIED |
| T-CG-040 | 数据快照与时间序列（累计→周期差分） | 数据按快照累积而非覆盖 | 数据层 | 表现/分析 | CORE | VERIFIED |
| T-CG-041 | 手工数据录入（平台原生指标周期快照） | 无 API 时数据主通道 | 业务表现 | 缺口行 | CORE | VERIFIED |
| T-CG-042 | 数据修正与修改历史 | 填错可改且留痕 | 数据层 | 表现 | OPERATING | VERIFIED |
| T-CG-043 | 数据来源区分（API/Browser/人工/导入） | 数据可信度判断的前提 | 数据层 | 全部数据面 | CORE | VERIFIED |
| T-CG-044 | Freshness/Stale 政策 | 多久没更新算过期，可配 | 数据层/业务 | 表现/分析 | CORE | STRONG |
| T-CG-045 | Unknown 四因表达（未到时间/未连接/未录入/源失效） | 缺数据≠0 | 数据层 | 全部数据面 | CORE | VERIFIED |
| T-CG-046 | 数据失效提醒 | 源断了知道并重试 | 通知/事实面 | 事实面 | OPERATING | STRONG |
| T-CG-047 | 分析引用数据可信度呈现 | 分析知道数据可不可信 | 洞察 | 报告 | OPERATING | VERIFIED |
| T-CG-048 | 增长实验记录（假设→设计→结果→结论） | 试错有记录、结论进 Learning | 复盘/业务 | 数据/复盘 | OPERATING | STRONG |
| T-CG-049 | 对话中 Account Context 标识 | 知道本次对话服务哪个账号 | Conversation | 对话头/Composer | OPERATING | STRONG |
| T-CG-050 | 素材库/模板库/版权红线检查 | 资产可复用、风格一致、版权安全 | 内容工作面/发布 | 生产引用/发布前 | OPERATING | STRONG |
| T-CG-051 | Account Goal（价值创造目标） | 账号最终靠什么创造价值（带货/商单/激励/付费/私域…） | Account | 账号经营面/对话 | CORE | VERIFIED |
| T-CG-052 | 账号变现资格与门槛跟踪 | "还差 400 粉可开橱窗" | Account | 账号面 | OPERATING | STRONG |
| T-CG-053 | 成长阶段×机会联动 | 阶段决定可用机会/重点/动作 | Account | 账号面 | OPERATING | STRONG |
| T-CG-054 | 机会发现与查看 | 知道平台有哪些活动/任务/激励/商品/商单 | Business/Account | 机会列表 | OPERATING | STRONG |
| T-CG-055 | 机会筛选/收藏/比较 | 判断哪个机会适合当前账号 | Business/Account | 机会列表 | OPERATING | STRONG |
| T-CG-056 | 手动创建机会（链接+条件+证据） | 平台没 API 也能经营机会 | Account | 机会列表 | OPERATING | STRONG |
| T-CG-057 | 机会→内容→发布→追踪 | 小账号赚钱主循环 | Business/Account | 机会→选题→内容包 | CORE | VERIFIED |
| T-CG-058 | 收益追踪（佣金/订单/转化/线索/商单/激励） | 变现结果可见、可复盘 | Account/数据层 | 账号面/表现 | CORE | STRONG |
| T-CG-059 | 机会有效期与失效提示 | 过期机会不误导 | Account | 机会列表 | EDGE | STRONG |
| T-CG-060 | 机会复盘 | 哪个机会值得继续 | Account/复盘 | 复盘 | OPERATING | STRONG |
| T-CG-061 | 平台经营维度档案扩展（变现/机会/门槛/限制/变化史） | 平台不只发布规则 | Platform Facts | 适配/发布/账号 | CORE | STRONG |
| T-CG-062 | 平台商业能力矩阵 | 每个账号当前能赚哪几种钱、差什么资格 | Platform Facts/Account | 账号面 | OPERATING | STRONG |
| T-CG-063 | 能力覆盖视图（能自动什么/需手工什么/哪些跳官方） | 用户知道 Curis 能替他做什么 | Platform Facts/Account | 连接页/账号面 | CORE | STRONG |
| T-CG-064 | 自动化成熟度四档标注（MANUAL/ASSISTED/AUTOMATED/AUTONOMOUS） | 对每项能力有正确预期 | Platform Facts | 全部能力面 | CORE | STRONG |
| T-CG-065 | 规则检测分层（Manual/Cheap/Browser/AI 只解释变化） | AI 不烧 Token 巡检无变化页面 | Platform Facts | 通知/业务 | OPERATING | STRONG |
| T-CG-066 | 收益数据类型与三层归属（Platform 原生/Account 经营/Business 结果） | 变现数据进数据逻辑且不混层 | 数据层 | 表现/账号/洞察 | CORE | STRONG |
| T-CG-067 | 三层绩效区分表达（内容≠账号≠业务） | 三个层级回答三种判断 | 表达原则 | 表现/账号/洞察 | CORE | STRONG |
| T-CG-068 | Platform Definition（可扩展平台定义） | 新平台不写死进产品 | Platform Facts | 档案 | CORE | STRONG |
| T-CG-069 | 新平台进入方案（内置/自定义/Connector/Package） | 新平台能进入 Curis | Platform Facts | 档案/设置 | OPERATING | STRONG |
| T-CG-070 | 意图关联官方入口+便利动作集 | 被封→申诉；想带货→选品中心；一键打开原文/后台/返回原上下文 | Platform Facts/各上下文 | 账号面/队列/互动 | OPERATING | STRONG |

---

## T-CG-071 ~ T-CG-080（PART III 抖音变现深挖新增，2026-09-13，Draft 待判定）

来源：CURIS_DOUYIN_REAL_PLATFORM_OPERATING_DEEP_DIVE.md PART III。每行 Scenario=真实赚钱场景。

| ID | Product Capability | Scenario（业务逻辑） | Owner | Context | Priority | Confidence |
|---|---|---|---|---|---|---|
| T-CG-071 | Monetization Qualification Map（九字段资格地图） | "这个账号离下一种赚钱方式还差什么"必须随时可答 | Account | 账号面/变现 | CORE | STRONG |
| T-CG-072 | Opportunity Intake 多通道（分享/截图/快填/深链） | 机会在 App 里也要进经营闭环 | Account | 机会库 | CORE | STRONG |
| T-CG-073 | Revenue Settlement State Machine（五态+扣减） | 钱有结算周期与售后扣回，单一数字=说谎 | Account/数据层 | 收益面 | CORE | STRONG |
| T-CG-074 | Cost & Profit 分层视图 | 收入最大≠赚钱；保证金/DOU+/制作是真实成本 | Account/数据层 | 收益/复盘 | OPERATING | STRONG |
| T-CG-075 | 选品决策对照卡（六维，非评分） | 选品是账号适配×经济性×内容可行性结构化判断 | Account | 选品/机会 | OPERATING | STRONG |
| T-CG-076 | 任务 Brief 结构化（截图识别→生产衔接） | 变现任务卡=命题 Brief，直接驱动内容生产 | Account/生产 | 机会→内容包 | OPERATING | STRONG |
| T-CG-077 | Mobile-Only 执行包（导航+步骤+回执） | App 执行动作要有清单与回执，不能静默丢失 | Account | 发布/执行 | OPERATING | STRONG |
| T-CG-078 | 直播 ASSISTED 包（播前/播后；不含实时场控） | 直播是人工执行+数据回流的另一种经营形态 | Employee/Account | 直播 | EDGE | CANDIDATE |
| T-CG-079 | 平台激励计划跟踪（Rule Version 化） | 激励计划会停发（中视频先例），过时资格=错误决策 | Account | 变现/机会 | EDGE | CANDIDATE |
| T-CG-080 | 瓜分制/有效播放/核销结算语义建模 | 平台结算语义必须原样进入数据层，不得简化为"收入" | 数据层 | 收益/机会 | EDGE | STRONG |
