# CURIS — FULL PRODUCT EXPRESSION V1

Authority Class: REVIEW / UI-READY PRODUCT SPECIFICATION CANDIDATE  
Status: Review  
Disposition: COMPLETE SPECIFICATION CANDIDATE — CEO REVIEW REQUIRED；NOT CURRENT AUTHORITY  
Owner: CEO / Product Review；编制：Codex  
Date: 2026-09-14 · Asia/Shanghai  
Target Authority: 唯一 Product Blueprint，经CEO接受后另行Reconciliation  
Next Gate: CEO REVIEW → CURIS PRODUCT BLUEPRINT RECONCILIATION → 既有Design Gate → UI  
Scope: 全产品共享表达 + Content Growth完整实例；不替未知专业Domain发明内部业务页面  
Boundary: 本轮仅此规格与来源校验；不改旧稿/Blueprint/Frozen Authority，不画UI、不改代码/Runtime/Schema、不commit/push。

本稿规定“画什么、在哪里、点后怎样、失败后怎样回来”，不规定像素和视觉风格。**PF-A**表示既有Authority固定关系；**PF-C**表示本稿选定、待CEO接受的表达合同，不能被设计师自行替换，也不能冒称已Frozen；**DO**只表示视觉开放。所有页面与按钮都是目标产品合同，是否已实现须独立验收。

## 1. Background / Why Old UI Failed

旧稿失败原因在本任务中作为CEO给定的问题定义：抽象意图没有转译为字段、动作和状态，导致设计阶段继续决定产品。这里不重新做旧图优劣审计，不以旧Prototype截图或DOM布局为答案。

承接已明确的业务方向：普通CEO让真实Curis员工持续经营多项业务；员工身份稳定、责任按范围变化；Provider提供能力，Curis保留责任与工作结果。S10的“所有其他Agent只能一次性工作”等竞争判断不采纳；S11已纠正。S12的经营链是产品逻辑，不是实际发布/Analytics闭环验收。

最重要的分离：Business负责持续业务方向，Workspace提供真实经营环境；Account是外部经营对象；Employee不是模型；查看不是接受；AI建议不是决定；用户报告完成不是平台成功。部门可以由公司事实预填，不允许缺canonical父关系仍创建成功。

## 2. Product Expression Method

先走六条链，再归纳页面。链A“意图→提案→建业务/首空间→责任/能力→首轮→结果/复盘”，决定创建Main与可继续的缺口；链B“工作台→异常→Leader→依据→决定→返回”，决定来源返回和P7；链C“员工→多责任→工作/对话/结果”，决定身份详情与工作分离；链D“绑定能力→连接/授权→保存”，决定能力Drawer与连接Settings；链E“同员工跨业务”，决定浏览范围、消息范围和执行范围分离；链F“真人动作→回执核对→继续”，决定Human Handoff。逐步模拟在附录A，不是事后演示。

每一步按以下30项闭合：Surface/Context/Object由§36及各面定义；字段/优先级/默认/展开见§9及各面；组件/理由/点击/承载/编辑/保存见§3–6及§37；Context变化/Work或Result等副产物见§37；成功/空/Loading/Unknown/Failed/Blocked/User Required/Provider Waiting/权限见§8和各面覆盖；返回/规模/检索见§7和各面；外部与手机见§26/33；PF/DO见§40。继承条款有实际行为，不能用“按需”“提供入口”代替决定。

字段为空不等于字段不存在。Required指必须保留语义位置，可显示明确未知/未设置；创建必填另写。对象ID仅内部定位，默认不展示。这里只定义产品语义字段，**不创建Schema字段、状态枚举或新的执行系统**。

## 3. Global Interaction Language

### 3.1 基本动作

- 行标题打开对象主工作面；头像/姓名打开同员工Utility详情；显式[和…讨论]打开Main同源对话。禁止整行点哪都聊天。
- 每个局部动作组最多一个主要CTA。存在待真人动作时[继续处理]优先，正常时用该对象的下一步；不能全页把[查看]都画成主按钮。
- 只读详情无[保存]。编辑未修改时[保存]禁用；成功后原摘要更新并显示“已保存”；失败保留输入、字段旁解释、[重试保存]。目标/权限等不是普通保存，见§37。
- Dropdown选择马上更新本地视图；需要持久化的设置明确[保存]。默认不把筛选变化写成业务策略。危险动作不放Hover唯一入口。
- 悬停可显示次要动作，但键盘Focus与[更多]必须能访问同一动作；已选行有持续选中反馈。状态颜色必须同时有文本。

### 3.2 Desktop / Keyboard（PF-C，非已交付快捷键）

| 操作 | 推荐键位/范围 | 反馈与冲突处理 |
|---|---|---|
| 全局对象搜索 | Cmd+K / Ctrl+K | 打开S-G2；文本编辑器已有此键用于链接时保留编辑器行为，Nav搜索始终可达；不变成Command Palette |
| 返回 / 前进 | Cmd+[ / Cmd+]；其他平台Alt+Left/Right | 原导航历史；编辑器明确占用时不劫持 |
| 关闭临时层 | Esc | 顺序：Popover→Modal/Drawer→maximized Utility→Search；脏编辑先退出确认；不停止工作 |
| Send / 换行 | Enter / Shift+Enter，输入法组字期间不发送 | 成功接收后清空文字，发送失败保留；多行和粘贴不自动发送 |
| 列表选择/打开 | ↑↓与Enter，仅列表获得焦点时 | 只改变选中与打开，不自动执行CTA；Tab遍历行内按钮 |
| 保存编辑 | Cmd/Ctrl+S，仅当前编辑器 | 等价可见保存；目标提案不会越过Decision直接生效 |
| 搜索结果 | ↑↓、Enter、Esc | 选中项包含类型与完整范围；无结果不打开空对象 |
| 停止 / 批准 / 拒绝 | 首版仅显式可见按钮 | 不使用裸空格/Esc/Enter作为全局危险动作快捷键 |
| 新对话 / 聚焦Composer / 切范围 | 可见[新话题]、点击输入框、范围选择 | 首版不再添加全局组合键；后续快捷键扩展不阻断本稿 |

键盘焦点可见、Modal/Drawer捕获焦点、关闭回触发控件；Utility为非模态，不圈住Main；屏幕阅读器读出状态变化与操作结果，不逐token播报。冷启动首次进入CEO工作台；从后台唤回仍保留当前工作面。应用重启后工作台提供[回到上次工作]，恢复已存对象/草稿，不自动重发请求。Window关闭、最小化、Pane收起不代表停止。没有后台执行证据时不得写“关闭电脑后继续”。重启恢复已存对象与草稿不重发请求；无法接回执行时显示“连接已中断，核对进度”。

### 3.3 Tabs / Segmented / Dropdown的全局规则

| 控件 | 固定用途 | 本稿实例 | 切换和保存 |
|---|---|---|---|
| Tabs | 同一对象/集合稳定且长期存在的信息面；标签不能随Hover才出现 | Employee详情资料/责任/能力/记录；Meeting讨论/决定与跟进；员工雇佣状态 | 本地信息面切换保留对象与草稿；选中态可恢复，不代表Work状态修改 |
| Segmented Control | 2–3个同层即时视角，结果应能直接比较 | 业务空间部门/业务/工作空间 | 立即切集合视角；不新增对象，不让用户点保存 |
| Dropdown / Select | 选择单个Option、范围、版本或排序；非隐藏主要导航 | 账号范围、模型用途默认、Result版本、列表排序 | 视图选择立即生效；配置字段选值后明确保存；消息scope选择遵守N2 |
| More Menu | 不常用维护动作，不替代首要任务 | 复制/归档/断开/改名 | 选项有动词和对象，危险动作进入影响确认；不可用项有原因 |
| Popover | 短选择、搜索定位、少量上下文提示 | 切换范围/选择已绑定能力 | 关闭回触发点；多步骤转Drawer/Main，不无限扩成长配置面 |

不采用三层Tab嵌套；有两层长期分类时Left Context承担一级，Main Tab最多再一层。当前对象核心动作不藏Dropdown；Platform是筛选/事实，不把平台选择当整个App一级导航。Tabs不自动改变Conversation下一消息scope，范围选择也不重写历史。

## 4. Surface Type Rules

| 类型 | 职责与默认使用 | 不采用 |
|---|---|---|
| Operating Main | CEO Desk、Business、Workspace经营摘要；同页理解方向/责任/结果/下一步 | 统一BI大屏或永久员工工位墙 |
| Working Main | Conversation、Work、Meeting、内容编辑、复杂创建 | 右侧窄栏承担完整工作 |
| Reading Main | 资料长读、分析报告 | 为每个来源再造正文副本 |
| Utility / maximize | Result、Evidence、员工身份、只读策略；可与Main对照 | 常驻空结果栏；把最大化当新业务Context |
| Guided Main | Business创建、Workspace复制、长配置/验证提案 | 8步小Modal、先选模板才能表意 |
| Bounded Drawer | 修改身份/Assignment/连接配置/目标提案的精确字段 | 完整对话、长内容生产、整套团队流程编辑 |
| Temporary overlay | 搜索、引用选择、短确认 | 第八导航、新的持久对象层级 |

Generic Workspace必须可完成共享工作链；Professional在此基础上呈现域对象，不能用“通用任务表”替换已形成的专业语义。其他领域的未定义专业页面明确不在首版表达承诺中，其共享工作入口已经可画。

## 5. Component Type Rules

| 组件 | 何时用 | 本稿默认对象 | 禁止/切换条件 |
|---|---|---|---|
| List / Row | 快速扫描、同一对象导航、列不需严格比较 | Business、Employee、Work、Account、Meeting、Result列表 | 不在每行嵌套完整对话/长报告 |
| Card | 单个待决定/人工动作，需解释与下一步 | P7、Handoff、提案摘要 | 不将所有数据变Card Wall；同类大量事项用行列表 |
| Table | 多对象同口径字段比较 | Analytics比较、Variant逐账号执行状态、能力清单 | 必须提供列名/单位/未知；不把普通员工列表变复杂数据表 |
| Tree | 真实Company→Department→Business→Workspace层级 | 组织公司版图 | Account、Employee服务关系用引用，不嵌成第二父树 |
| Timeline | 有序发生记录/来源 | Work活动、发布回执、决定记录 | 无真实事件不填演示进度 |
| Kanban | 仅专业领域有稳定状态移动且业务允许改变状态 | 本稿无默认Kanban | Publication/Work不能拖到“成功”；未来域提案单独审 |
| Calendar | 时间安排是当前任务中心 | 内容计划的可选排期视图 | 非Business/CEO默认；不代表平台已接受排程 |

六类对象默认：Business摘要行；Employee身份行；Work活动行；Account经营行；Meeting讨论行；Result引用行。不是让设计师在Card/Table之间再选。内容Variant用比较表是例外，原因是逐账号差异及部分成功必须同时可辨。列表分页/加载更多不改变现有排序；所有集合显示总量未知时仅“已加载N项”。

## 6. Modal / Drawer / Utility / Main Rules

### 6.1 八种表达方案比较与选型

| 重要动作 | Inline | Popover | Dropdown | Drawer | Modal | Right Utility | Main | Conversation | 选定与理由 |
|---|---|---|---|---|---|---|---|---|---|
| 改姓名/标题 | 适合单字段 | 不承载编辑 | 只动作入口 | 多字段时可用 | 过重 | 员工详情内可启动 | 无须离开 | 不要求AI | Inline；员工多字段用Drawer，身份不变 |
| 调整Goal/Strategy | 长文/影响不宜 | 太窄 | 只入口 | 精确修订合适 | 仅最终危险确认 | 先读原值合适 | 大范围方案适合 | 主要形成方式 | 讨论→Main；[修改提案]→Drawer；P7接受后更新，保留对照 |
| 创建Business | 不够 | 不够 | 只入口 | 多步骤太挤 | 不采用小窗 | 仅来源 | 最适合长期编制 | 可发起/补全 | Guided Main，能比较方案、暂存、恢复 |
| 看员工是谁 | 不够 | 只短身份提示 | 只入口 | 不必阻塞 | 不用 | 最适合对照 | 工作用Main | 身份不靠询问 | Utility详情；[进入工作]才Main |
| 绑定一项能力 | 不够 | 只选已绑定默认 | 选类型 | 最适合中等配置 | 升权确认 | 只读影响 | 连接维护可跳设置 | 可提出建议 | Drawer绑定，Settings负责连接，授权单独确认 |
| 看Evidence/Result | 摘要引用 | 不够 | 版本选择 | 无须编辑 | 不用 | 最适合核对 | maximize阅读 | 追问回Main | Utility→maximize；不丢来源与原Work |
| 做复杂Decision | 仅Banner | 不够 | 不隐藏选项 | 内容长不采用 | 仅不可逆最终确认 | 证据 | 原Work的P7详细工作面 | 可询问 | P7在Main；简单低歧义可Banner按建议 |
| Human Handoff | 原Work提示 | 不够 | 官方目标多个时选择 | 不新增 | 支付前确认可能必要 | 补充证据 | 原Work动作包 | 可以解释 | 原Work Main，手机/浏览器完成，回原Work核验 |
| 改团队默认流程 | 单项标题可 | 不够 | 选择成员 | 单责任编辑可 | 最终重大影响 | 对照旧版 | 最适合整体顺序 | 可提修改 | Main顺序责任表；没有自由DAG |
| 多平台内容编辑 | 适合短字段 | 附加选项 | 选账号/版本 | 长文不够 | 不用 | 规格/对照 | 最适合 | 与生产员工讨论 | Main编辑当前Variant，逐账号预览 |
| 断开/停止/归档 | 不直接 | 不直接 | More入口 | 影响复杂转Main | 短影响确认适合 | 查看受影响对象 | 转移/合并方案 | 可解释 | 不可逆需明确对象与后果；取消不触发请求 |

### 6.2 层与保存合同

同一时刻只开一个Drawer，不在Drawer内叠第二Drawer；需连接时暂存绑定草稿→Settings→返回原Drawer。Utility有自己的T3 Toggle，不加第二个✕；Drawer是临时编辑层，有[取消]/[保存或提交]，不是改名Utility。Utility最大化可✕/Esc退出，恢复原Pane布局与滚动。Evidence链用Utility内部返回，不无限叠Pane。

离开有修改但未保存的编辑：Modal“保留草稿后离开 / 放弃修改 / 继续编辑”；正式内容未保存不得被后台刷新覆盖。只读视图直接返回。保存发生并发变化：保留本地草稿，显示“原内容已更新”，[对照更新]后重新提交，不自动覆盖。成功提示只在确实持久化后出现；请求超时显示“保存结果待确认”，先读取对象最新版本，不盲目创建副本。

## 7. Navigation Rules

统一返回合同 **R**：记录From对象、范围、筛选、排序、选中ID、滚动锚点、当前对话/话题、Composer草稿、Pane开合与Utility引用。Back恢复这些值，正文/状态加载最新事实，不恢复过期可执行按钮；对象已删除/失权则保留来源页并解释，不能泄露旧内容。不是新增History真源，而是导航恢复合同。

**N0**局部读详情/Utility：不改执行Context；**N1**Main对象跳转：改浏览Context，既有Work不改；**N2**Conversation下一条消息范围切换：显式确认/显示目标，旧消息保持原scope；**N3**启动/修改工作：明确Assignment/对象/权限，产生真实请求与回执。用户当前看B不会把A运行中的工作改成B。

多范围标题显示最短不歧义链：Business / Workspace / 对象；重名补Department，公司切换不默认开放，首版只当前Company。长标题可截断视觉但Hover/Focus有全文；返回按钮永远保留来源目标文字。新窗口深链无From时回所属一级区，不制造虚构历史。

全局导航切换可恢复该区上次子面；首次默认见各面。账户筛选、资料类型不进入全局Nav。Search结果直达对象不强制沿Company树下钻。外部浏览器/手机离开不标任务完成；原Work保留[核对结果]/[我已完成]见§26。用户返回Curis时恢复原页或在Attention显示原动作，不强行抢焦点。

## 8. State Language

### 8.1 统一缺口与反馈（G，所有Surface继承）

| 状态 | 用户文字 | CTA / 后果 |
|---|---|---|
| No Data | 还没有可显示的记录 | 该面实际创建入口；筛选无结果则[清除筛选]；不放“刷新”假解法 |
| Unknown | 暂时无法确认 | [查看原因]→Utility来源；确有查询能力才[核对状态] |
| Not Connected | 尚未连接〈服务〉 | [连接服务]→对应Settings，返回原对象；不是连接成功 |
| Not Supported | 当前方式不支持〈动作〉 | [查看可用方式]→可用连接/官方操作；没有替代显示说明不假CTA |
| Not Configured | 还需要设置〈必要项〉 | [完成设置]→精准字段，不丢原草稿 |
| No Result Yet | 尚未产生结果 | 有运行则[查看工作]；未启动则真实发起入口，不造空报告 |
| Waiting User | 需要你〈具体动作〉 | [继续处理]→原P7/Handoff；不一律标失败 |
| Waiting Provider | 已提交，等待〈服务〉回应 | 有查询能力[核对进度]；否则显示最后确认时间与等待说明，不再次提交 |
| Failed | 〈动作〉未完成：〈可理解原因〉 | 确认未发生副作用才[重试]；不确定用[核对结果] |
| Blocked | 暂不能继续：缺〈责任/授权/输入〉 | [补充资料]/[安排负责人]/[完成授权]之一，定位缺口 |
| Loading | 正在读取〈对象〉 | 骨架/小进度并保留已读内容标过期；局部失败不抹全页 |
| Permission denied | 你当前无法访问或执行此项 | [返回]；确有授权入口[检查权限]，不把401一律说服务坏了 |
| Success | 按动作：“已保存/已提交/已确认发布” | 展示真实对象与下一步；“已提交”绝不写“已完成” |
| Interrupted | 连接已中断，正在核对原工作 | [核对进度]，仅支持续接时[继续工作]；禁止重发原始指令冒充Resume |

G适用于读取/编辑/执行操作，不能给本无Provider步骤的“员工目录”虚构Provider Waiting。各面状态覆盖写明哪个对象触发；不存在的状态为N/A。Blocked是可解释阻碍，不是统一错误码。

### 8.2 分对象状态映射（产品显示标签，非新增Runtime enum）

| 对象 | 保留的用户词 | 特别区分 |
|---|---|---|
| Work | 已计划、工作中、等待你处理、等待外部回应、待审核、已完成、未完成、已暂停 | 有真实接受结果才完成；计划不代表执行中；Unknown单列原因；审核归Result/P7 |
| Employee | 空闲、工作中·摘要、阻塞·原因 | 雇佣状态“在岗/未在岗/离职”另字段；不显示员工“已完成/等待/离线”冒充presence |
| Business/Workspace | 准备中、经营中、已暂停、存在待处理事项、已归档 | 经营中需实际责任/运行支撑；有单项失败不把全业务判失败 |
| Publication | 待定稿、待确认、待执行、已提交、待平台确认、已发布、发布未完成、结果待确认 | 分账号记录；平台回执和核验决定已发布，非按钮点击 |
| Decision | 待你决定、已接受、已拒绝、已暂缓、已失效 | 被替代方案失效不能旧按钮再次批准；按建议处理保留actor/依据 |
| Meeting | 准备中、讨论中、等待补充/决定、已结束 | 离开页面不结束；结束讨论不取消会后工作；状态来自真实会议记录 |
| Connection | 未连接、检查中、可用、需要重新授权、检查失败、状态未知 | 可用仅验证过的能力，不代表所有动作支持 |
| Result / Learning | 已交付、已查看、待接受、已接受/需修改；经验建议/已采用 | 阅读不改变接受状态；Learning生效是可追溯规则/知识变化 |

聚合状态显示“2项待处理/1个空间暂停”，不生成无依据的健康分数、全员忙碌率或统一百分比。后台tool call、router、heartbeat、幂等键在诊断详情按需，不成为主状态词。

## 9. Field Language

优先级：**P0**识别与需要动作，**P1**判断所必需，**P2**按需来源/维护。下表每行字段按默认显示顺序排列；“必备”可有合法未知。O为可选。禁止字段即便底层存在也不得默认暴露。摘要超过两行显示[展开]，正文不以Badge表达。

| 合同 | 组件 / 必备字段（顺序） | O / 按需 | 禁止默认显示 |
|---|---|---|---|
| F01 Business Row | 名称P0；状态/真实Attention数P0；Goal一句P1；真实Leader或未安排P1；最新业务Result标题P1 | 当前业务重点、Workspace数、最近变化时间；没有统一Cycle则不显示Business cycle | 所有Workspace任务、模型/Token、虚构营收、统一Team Flow |
| F02 Employee Row | 头像/姓名P0；雇佣状态P1；当前工作状态P0；当前范围责任P1；当前Work标题P1 | 多责任数量、组织归属；能力摘要在Detail | 在线绿点、完成状态、裸模型名代替岗位、同员工多条身份副本 |
| F03 Work Row/Card | 工作标题P0；范围P1；当前责任员工P1；状态+具体阻塞P0；下一动作P0；最后活动时间P1 | 关联Goal/Result、真实截止时间、执行进度证据 | 无证据完成率、内部Job ID/日志墙 |
| F04 Result Reference | 标题P0；作者/责任P1；所属Work/范围P1；交付与接受状态P0；一句结论P1；来源/Evidence数量P1 | 版本、交付时间、输出文件类型 | 无来源好评、把读取当接受、把Business关联当唯一scope |
| F05 Conversation Header | 员工/会议身份P0；话题P1；下一消息当前范围P0；关联Work与状态P1 | 上级业务链、参与者、过去范围可在历史查看 | 自动将浏览筛选写成消息scope、全量上下文常驻 |
| F06 Decision Card | 发生了什么/需决定什么P0；为何需CEO P1；员工推荐P1；主要风险/代价/未知P1；动作P0 | 全部选项对比、依据、选择后如何继续；详情覆盖P7八要素 | 一句话批准高风险、无来源成本/期限 |
| F07 Handoff Card | 需你做什么P0；为什么P1；对象/账号/平台P0；已准备材料P1；下一步恢复条件P1；CTA P0 | 有依据的到期时间、最近核对时间、操作来源、备选方式 | 密码/Token/支付信息、自动推断已付款 |
| F08 Meeting Row | 标题P0；范围P1；状态P0；参与员工摘要P1；未决事项数P0；最近讨论时间P1 | 主持责任、相关结果、真实计划时间 | 强制日历时间、CEO离开=结束 |
| F09 Knowledge Item | 标题P0；类型P1；来源P1；适用范围P0；新鲜度/版本P1 | 作者、引用次数/Used By、更新时间、接受状态 | 文件路径树替代产品分类、向量/chunk/embed配置 |
| F10 Workspace Row | 名称P0；真实LeaderP1；经营状态/本轮重点P0；需注意事项P0 | 形态/验证状态、成员数量；细节进入Workspace | 完整Goal/规则/所有Workstation嵌套Business |
| F11 Account Row/Header | 账号名+平台P0；可辨身份（handle/头像）P1；连接状态P0；Goal一句P1；需处理事项P0 | 当前负责者、本轮重点、最新有效表现及周期/来源 | 粉丝等级推断资格、裸Provider品牌主标题、Account=Workspace |
| F12 Variant Row | 目标账号/平台P0；内容形式P1；版本标题/修订号P1；生产/审核/发布状态分别P0；阻塞/下一动作P0 | 内容规格差异、作者、预览、更新时间 | 一份总“已发布”、自动继承别账号审核 |
| F13 Metric | 名称/值+单位P0；范围/周期P1；数据可用状态P0；来源/时效P1 | 可比上期变化、采集方式、样本量 | 缺失填0；不同平台指标直接相加；不完整成本算利润 |
| F14 Capability Row | 能做什么/名称P0；类型P1；连接/可用状态P0；当前用途/默认选择P1 | 来源/版本/权限/许可/依赖、使用该能力的员工 | 自动把市场候选当已安装、Endpoint/Key常驻 |
| F15 Assignment Row | 责任名P0；Scope/对象P0；当前Holder或空缺P0；职责一句P1 | 汇报关系、能力要求、有效时间、变更历史 | 把Role当授权、Employee姓名自由文本冒充绑定 |
| F16 Goal / Strategy | Goal全文摘要P0；成功标准P1；目标范围P0；策略一句P1；当前生效/待确认状态P0 | 约束、预算口径、周期/检查点、来源、旧版本 | 默认展示JSON、把业务目标当全部账号覆盖值 |
| F17 Proposal | 建议做什么P0；目标/成功标准P1；Business/首Workspace身份P0；Leader/责任覆盖P1；能力缺口P0；预算/授权边界P1；下一步P1 | 可复用方案与证据、Department归属、专业形态及验证级别、输入资料 | 创建即全自动经营、隐藏未落实团队 |
| F18 Connection | 服务/连接名称P0；关联外部身份P1；状态P0；授予范围P1；最近成功检查时间P1 | 来源/版本、影响员工/业务、维护说明、安全凭证存在状态 | 显示Secret、用保存配置当测试成功 |

全局日期：相对时间用于行扫描，Hover/Focus给含时区的绝对时间；排期/截止/外部到期必须显示日期时区。金额必须货币和口径，估算写“估算”。姓名/标题不作为ID，重名追加范围。系统状态及来源事实只读；注释、草稿与正式改动分开。失权后缓存字段不得继续显示。

## 10. Global Navigation

**Surface ID: U10** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 任何位置知道所在公司、所在一级区并进入对象；全局辅助功能不变第八区 |
| Entry | 应用主窗口；每个Surface共用 |
| Context / Product Object | 当前Company；导航选中区域与工作执行scope分离 |
| Layout responsibility | Navigation：七区当前区；Left Context：由当前Surface声明；Global层不放永久员工树；Main：Nav Header原生窗口控制/搜索/T1 → 七区固定顺序 → bounded最近对话 → 底部通知与CEO头像；Main由目标区接管；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 七区标签、选中态；当前Company名称；Quick Access话题/员工/最后活动；Avatar可访问名称 |
| Optional fields | 最近对话展开到最多10条，更多进搜索；有真实事项才显示Attention数 |
| Component form / 默认顺序 | Nav Header原生窗口控制/搜索/T1 → 七区固定顺序 → bounded最近对话 → 底部通知与CEO头像；Main由目标区接管 |
| Primary actions | [搜索]打开对象搜索；七区任一项打开目标面 |
| Secondary / More actions | [新话题]先选员工/明确范围；最近对话More [从最近列表移除]；头像菜单[设置][公司资料][帮助][关于] |
| Interaction / 编辑保存 | Nav不编辑业务。菜单选项进Settings Main；关闭菜单不变页面。T1折叠后移Main Header，T2/T3保持Shell合同 |
| State variants | 无最近对话显示“这里会保留最近的对话”；Company加载失败只显示恢复页；通知读取失败“待处理状态暂不可用”，不写0 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 区间切换恢复各区最后浏览；同对话重新打开恢复同identity；继承R |
| Scale / Search / Filter / Sort | 七区不随业务数增加；最近10条不是全部历史，搜索支持更早记录 |
| Product Fixed | PF-A七区/Quick Access/浮层Assistant/Pane Header；PF-C最多10条与菜单分组 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

**U10-S Global Object Search**：Nav放轻量搜索图标，Cmd+K打开独立overlay。顶部输入框placeholder“搜索业务、员工、资料、工作…”，下方空查询为最近对象；输入后按对象类型分组，每行图标、标题、类型、最短合法范围。键盘选中/Enter打开Main对象，Result打开来源Main+Utility；底部范围声明“当前公司内你可访问的内容”。无结果：“没有找到‘…’”，[清空搜索]；部分检索失败显式提示未覆盖类型，[重试搜索]；不显示无权对象数量。Esc/遮罩关闭回原焦点；返回Search恢复查询/选中。首版不新增Command Palette、自然语言问答或高级语法（S07明确Reserved）。

**U10-N Notification / Attention**：底部[通知]开临时Drawer，Tabs“待处理 / 更新”；待处理行显示事项、范围、原因、下一动作、时间，按真实紧急/截止再更新时间排序；更新按时间倒序。[继续处理]到原Work/P7，[查看结果]到原Work+Utility。[标为已读]仅更新阅读回执，不接受结果、不完成Handoff。无事项：“目前没有需要你处理的事项”。系统通知仅在获OS权限后发送，正文默认不带敏感业务全文；点击复用相同深链。通知偏好在U28。

## 11. CEO Desk

**Surface ID: U11** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | CEO打开后知道公司发生了什么、必须处理什么、接下来去哪 |
| Entry | 首次打开/点击CEO工作台/处理完成返回 |
| Context / Product Object | Company；Attention、Decision、Result的合法聚合投影 |
| Layout responsibility | Navigation：CEO工作台；Left Context：默认收起；展开是“今天/上次离开后”的阅读区间及已处理记录入口，不放业务树；Main：公司Header → Return Summary一句概况 → 需要你处理的事项行 → 值得注意的Business行 → 重要Result引用行；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 公司名称；简报截止/覆盖时间；F06/F07事项；F01业务异常；F04结果；数据缺口说明 |
| Optional fields | 完整变化清单[查看全部变化]；没有真实变化则隐藏Return Summary正文；Company目标摘要按需 |
| Component form / 默认顺序 | 公司Header → Return Summary一句概况 → 需要你处理的事项行 → 值得注意的Business行 → 重要Result引用行 |
| Primary actions | 首个事项的[继续处理]/[查看方案]；无业务时[开始一项业务] |
| Secondary / More actions | [进入业务空间][查看经营分析]；Result[查看结果]；无全局[全部批准] |
| Interaction / 编辑保存 | 事项在原Work/P7 Main展开；Result到U27；公司目标点击[查看公司目标]→Utility，[讨论方向]→同Assistant/合法责任Main，不在主页编辑数字 |
| State variants | Business=0仍显示原装组织准备状态和开业务入口；模型未设置写“员工已在，开始执行前需配置模型”；无简报不虚构“经营良好”；离线显示上次更新 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 处理后[返回CEO工作台]恢复事项位置，并显示真实已处理状态；失败留在原事项；继承R |
| Scale / Search / Filter / Sort | 默认最多5条需处理、5个注意业务、3条重要结果，超出显示计数与[查看全部]；待处理可按业务筛选，不永久8块Dashboard |
| Product Fixed | PF-A CEO Desk≠Assistant≠Insights；PF-C默认顺序/数量只是信息上限，不截断事项事实 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Return Summary基于实际离开/阅读记录，字段“自〈时间〉以来 / 变化摘要 / 未处理N / 新结果N / 最后更新”。缺离开时间就写“最近变化”，不假装一周后台运行。点击[查看全部变化]在Main同面展开时间列表，[收起]回同位置；已看不代表接受。Attention只重复展示引用，不新建事项；原事项失效时立即同步并显示“已由原工作处理”。

## 12. Business Space

**Surface ID: U12** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 直接进入经营责任层或工作现场，开始新业务 |
| Entry | 全局业务空间/CEO Desk业务入口 |
| Context / Product Object | Company内Directory；不是新执行scope |
| Layout responsibility | Navigation：业务空间；Left Context：默认收起；展开提供部门过滤及最近使用对象；Main：Header“业务空间”+[开始一项业务] → Segmented“部门 / 业务 / 工作空间”（首次业务） → 搜索/状态筛选 → 对应摘要行；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 业务F01；工作空间F10；部门名称/负责人/职责一句/真实事项数 |
| Optional fields | 归档对象在筛选中；成员数非默认；目录总数已知才显示 |
| Component form / 默认顺序 | Header“业务空间”+[开始一项业务] → Segmented“部门 / 业务 / 工作空间”（首次业务） → 搜索/状态筛选 → 对应摘要行 |
| Primary actions | [开始一项业务]→U12-C Guided Main |
| Secondary / More actions | [进入]行标题；More [复制业务]/[复制工作空间]依对象类型；不把两种复制混名 |
| Interaction / 编辑保存 | 输入搜索即过滤当前集合；默认最近使用排序可切名称；切Segment只换目录视角不变任何Work |
| State variants | 0业务说明“公司已有建设团队，可以从一个想法开始”；0工作空间不能显示虚构实例；列表失败[重新读取]；已有对象创建中不重复建 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从目录进入对象后Back恢复Segment、筛选和行；创建取消回目录原状态；继承R |
| Scale / Search / Filter / Sort | 1/5/20业务均摘要行；按名称搜索、部门/状态筛选；不按规模自动变Card Wall |
| Product Fixed | PF-A三个直接目录视角与canonical层级；PF-C默认业务视角和行列表 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

**U12-C 创建业务 / Operating Proposal**：Main Guided Surface，Left Context只有步骤“意图→经营提案→准备与启用”，不是新层级；当前步骤Main可长留、草稿持久。第一步必填“你想经营什么”，可附参考；已有合法业务候选先给[使用现有业务]与[仍创建新业务]，不静默复用。可[请空间工程团队准备方案]形成有范围的建设Work；[我来填写]走同一Proposal字段，不绕过关系校验。

提案Main默认顺序：F17身份与目标→经营方式→首Workspace→团队/责任覆盖→能力与授权缺口→预计下一步。Business Name必填，Goal/成功标准必填；Department使用合法已有归属建议显示在[组织归属]展开项，不能空父关系成功；新Department需要明确名称/职责并入提案确认。首Workspace Name必填；Leader/责任可未落实但必须显示缺口。策略内容有[讨论打法]到同来源Conversation、[修改提案]Drawer精确编辑；目标/授权/资源等高影响变化用P7语义明确接受。用户已完整明确授权的创建指令不再要求无意义第二次同意。

提交按钮[创建业务与首个工作空间]仅物化确认的结构，非[开始赚钱]。处理中保留提案、按钮禁用；超时先[核对创建结果]，不盲目再次创建。成功同一确认页列实际Business/Workspace/责任缺口，主要[进入工作空间]；未具备能力时次要[完成准备]，无自动实发/支出。原子失败保持草稿并指出哪个关系未通过；只创建一半不得称成功。离开走R与草稿确认。

**U12-D Copy Preview**：Main展示“复用/重新确认/不复制”三段。新名称必填，Goal/定位/账号/员工安排/权限/排期逐项确认；禁止复制身份、秘密、对话、历史Result/Evidence或当前运行。Employee复用是新Assignment不是克隆员工。[确认复制]成功进入新对象，原对象不改；失败核对原请求。

## 13. Business Operating

**Surface ID: U13** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 管理持续业务方向与跨Workspace事项，进入真实工作现场 |
| Entry | U12业务行/CEO异常/组织版图Business/搜索 |
| Context / Product Object | Business，显示所属Department；下游Workspace仍独立 |
| Layout responsibility | Navigation：业务空间；Left Context：默认收起；展开是本Business空间目录，不显示全部员工；Main：四段连续：Business Definition紧凑Header/目标/Leader入口 → Operating Status业务重点/事项/重要结果 → Workspace Directory摘要行 → Business Team轻量责任行；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 名称/简介/业务Goal与规则摘要；真实Business Leader；Current Focus/下一判断；F10；F15团队投影 |
| Optional fields | 策略/约束全文Utility；详细指标到Insights；成员列表默认5项[全部参与员工] |
| Component form / 默认顺序 | 四段连续：Business Definition紧凑Header/目标/Leader入口 → Operating Status业务重点/事项/重要结果 → Workspace Directory摘要行 → Business Team轻量责任行 |
| Primary actions | [和业务负责人讨论]→U24 Business范围；有阻塞P7就以[查看方案]为该事项主动作 |
| Secondary / More actions | [调整目标][查看规则][查看经营分析][新增工作空间]；More [复制业务][暂停经营][归档业务] |
| Interaction / 编辑保存 | 目标查看Utility→修改提案Drawer；CEO接受后更新摘要及版本；新Workspace用U12-C缩减到当前Business；不将Business规则编辑应用到全部Workspace具体目标 |
| State variants | Leader缺失显示[安排负责人]；无统一业务Cycle则不显示Current Cycle；暂停写明还未取消的外部事项；Workspace读取失败不隐藏Business方向 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 进入Workspace/Conversation/Insights均保留业务From；返回恢复四段滚动位置；继承R |
| Scale / Search / Filter / Sort | 空间目录超过5项显示[查看全部工作空间]在同Main目录区过滤；团队可查人/职责；不展开全部Work进展 |
| Product Fixed | PF-A保留Business四段IA与Team不统一运行；PF-CDefinition压成短段，不用旧四大Card |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Header名称可Inline改名；[调整目标]不直接改成功标准，进入I03提案。Business[暂停经营]表示该范围的经营暂停请求，确认Modal列受影响Workspace/未完承诺/平台已提交动作，并说明“外部已提交动作不会因此撤回”；实际状态逐范围回执投影。若需复杂资源转移/关闭/合并，More[调整业务安排]进入Main影响提案，不能一个Modal伪装全部处理。当前工作详细记录在Workspace；Business只显示业务级真实Work及下游问题引用，不复制任务系统。

## 14. Workspace

**Surface ID: U14** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 在同一真实责任边界进行专业工作、团队协作与结果复盘 |
| Entry | U12工作空间/U13目录/深链 |
| Context / Product Object | Workspace归属Business；selected Surface只是观察面 |
| Layout responsibility | Navigation：业务空间；Left Context：本Workspace身份 + Domain Navigation；Generic固定“经营 / 工作 / 结果 / 团队”；Professional使用批准的域导航；Main：Header身份/Leader → 当前选中专业面 → 相关Shared Work Area；Generic经营默认Goal简述/本轮重点/最新判断/下一步→实际Work行→最新Result；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F10身份、F16目标；真实Operating状态/周期范围；F03/F04；工作面要求的责任Holder |
| Optional fields | 规则、授权、知识引用、方法与验证级别详情；需关注仅真实Need时出现 |
| Component form / 默认顺序 | Header身份/Leader → 当前选中专业面 → 相关Shared Work Area；Generic经营默认Goal简述/本轮重点/最新判断/下一步→实际Work行→最新Result |
| Primary actions | [和工作空间负责人讨论]；当前专业面自己的主要业务动作 |
| Secondary / More actions | [查看团队运转][查看结果][调整目标]；More [暂停经营][复制工作空间][调整工作空间] |
| Interaction / 编辑保存 | 专业面切换N0/N1不换Workspace identity；团队运转Main顺序表可编辑责任/输入/输出/默认下一责任，保存形成新版本，运行中Work继续旧版本 |
| State variants | 无团队不写准备就绪；没模型可编制计划不可假运行；未知领域用Generic真实Work+能力缺口；Package候选不显示已验证 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | Domain切换记住各面选中对象/滚动；进员工/结果后回原面，收Pane不停止Work；继承R |
| Scale / Search / Filter / Sort | 1或多个专业面均来自当前域；长列表搜索/状态筛选；团队人数增长用责任行，不无限并排工位 |
| Product Fixed | PF-A单Workspace一责任边界、Shared Work Area在Main；PF-CGeneric四项导航/团队编辑形式 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

[查看团队运转]打开同Workspace Main工作面：顺序责任行字段“责任/目的/当前员工/输入/输出/默认下一步/Review-Return”。[修改]先复制为编辑草稿，不是执行流程图。拖动顺序须有[上移/下移]键盘替代；保存前显示变化、受影响的未来工作，重大权限/策略变化转P7。缺Holder→组织Assignment Drawer，不在此创建第二员工。Professional升级/回退只在具备真实验证方案时给操作，否则[交给空间工程团队评估]形成Work，不让设计师画可用升级按钮。

### 本轮计划 / Cycle / Review的具体表达

[查看本轮计划]在Workspace Main展开工作面，不放小Drawer。Header显示“本轮目标 / 对应Goal版本 / 范围 / 负责人 / 周期起止或检查点 / 当前状态”；正文顺序为计划Work行（标题、责任、所需输入、预期输出、Review要求、真实期限或未设置）、当前证据/结果、Review结论、下一步。日期未知就“尚未确定检查时间”，不自动凑一周。没有计划时[和负责人制定首轮计划]到当前Leader Main Conversation，带Goal/能力缺口引用。

[调整本轮计划]主要进入同Leader Conversation；精确修订用Main可编辑顺序列表，字段为工作目标/输入引用/预期输出/Review标准/优先级/期限。[保存计划修订]显示“尚未执行的安排会更新”，在途Work固定原定义；调整执行目标或受保护预算/策略需P7，不能拖行自动撤销运行。空输入或输出标准在字段旁报错；并发计划更新按§6对照，保存未知先核对原版本。

[查看本轮复盘]打开Result Utility：目标结果对照、事实/未知、未完责任、建议及依据。下一步读既有经营决定：“继续 / 调整后继续 / 等待条件 / 请你决定”；显示决定者/理由/检查点/关联下一轮。继续和调整才创建或安排一次下一轮，已存在下一轮则按钮[查看下一轮]，不再给[再启动一次]。暂停保留恢复入口，结束责任须明确终止后果；普通Cycle Close不显示整个Business“已完成”。返回恢复原Workspace专业面及本轮选择。

## 15. Organization Center

**Surface ID: U15** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 查看与调整公司组织事实，清楚谁对哪个范围负责 |
| Entry | 全局组织中心/缺岗入口/Company结构链接 |
| Context / Product Object | Company Organization；不因看版图拥有执行权限 |
| Layout responsibility | Navigation：组织中心；Left Context：“公司版图 / 员工目录”两稳定子面；首次公司版图；Main：Header公司/组织摘要 → 公司版图或员工目录；默认展示原装部门和真实用户Business，业务可0；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 真实部门名称/职责/Leader；人员数量/空缺只有事实；F15责任 |
| Optional fields | 变更历史、组织说明；不显示演示用户业务 |
| Component form / 默认顺序 | Header公司/组织摘要 → 公司版图或员工目录；默认展示原装部门和真实用户Business，业务可0 |
| Primary actions | [安排责任]从真实缺口进入Assignment编辑 |
| Secondary / More actions | [创建员工][开始一项业务]；More [调整部门]；新增真人邀请不在首版 |
| Interaction / 编辑保存 | 组织字段Drawer编辑；归属变更必须列未完成Work和接收责任，复杂变更Main提案；保存不重写旧Work身份 |
| State variants | Business0不等于空组织；无模型员工依然存在；读取失败不给全公司0员工；权限拒绝保留原链接返回 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从缺岗返回原Work时刷新Holder，执行是否继续依真实恢复状态；继承R |
| Scale / Search / Filter / Sort | 多部门可折叠、搜索组织对象；按缺岗过滤不创造“异常部门”新树 |
| Product Fixed | PF-A Organization是唯一组织投影；PF-C子面及编辑形式 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

“安排责任”先定位责任，再选符合要求的既有员工；当前无责任时[新增责任]要求名称、职责、合法scope，不能直接输入员工姓名表示已绑定。[创建员工]调用U17-C；[找合适人才]跳U19并保留缺岗目标，招聘后回Assignment，不自动获得执行权限。

## 16. Business Map / 公司版图

**Surface ID: U16** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 看真实层级和责任关系，既可进入经营也可调整组织 |
| Entry | U15公司版图/Company资料入口 |
| Context / Product Object | Company→Department→Business→Workspace；Employee为服务引用 |
| Layout responsibility | Navigation：组织中心；Left Context：沿用U15子面；可收起；Main：公司Header → 层级Tree；默认展开Department与Business，Workspace与责任按行展开；选中对象仅打开只读摘要Utility；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 对象名称/类型/Leader/真实状态/下级数量；责任展开F15 |
| Optional fields | 风险、最新Result引用、员工服务引用边；全图网络线默认无 |
| Component form / 默认顺序 | 公司Header → 层级Tree；默认展开Department与Business，Workspace与责任按行展开；选中对象仅打开只读摘要Utility |
| Primary actions | 节点[进入经营]→对应U13/U14/部门Leader Main |
| Secondary / More actions | [查看责任][安排负责人]；More [重命名][调整归属] |
| Interaction / 编辑保存 | 展开箭头只展孩子，节点正文选中→Utility；显式[进入经营]才Main；组织拖拽首版不开放，避免误迁移 |
| State variants | 空子级显示“尚无业务”与创建入口；空Holder显示缺岗；加载失败局部节点[重试读取]，不删除节点 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 进经营返回恢复展开路径和选中；重命名跨区同身份更新；继承R |
| Scale / Search / Filter / Sort | 搜索定位结果高亮路径；20业务按Department折叠；员工多业务以Assignment链接不复制到树中作多身份 |
| Product Fixed | PF-A真实层级与唯一员工；PF-C树默认展开深度与明确进入经营按钮 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Department节点[进入经营]复用共享Management Main：职责/Leader→跨Business当前事项→Business目录→资源/责任摘要；[和部门负责人讨论]进入Department范围Conversation，不制造假Business。结构编辑仍在组织中心；部门经营面不提供专业团队默认流程。

## 17. Employee Directory

**Surface ID: U17** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 找已有公司员工，判断其身份与当前责任，进入工作或调整安排 |
| Entry | U15员工目录；U19[查看公司已有员工]是跳转不是第二目录 |
| Context / Product Object | Company员工集合；可筛Business服务关系 |
| Layout responsibility | Navigation：组织中心；Left Context：U15公司版图/员工目录；Main：Header“员工”+[创建员工] → Tabs“全部/在岗/未在岗/离职” → 搜索/服务业务筛选 → F02行；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F02；多责任默认显示当前筛选范围的责任；未筛选显示主要责任+“另N项” |
| Optional fields | 能力摘要在Utility，最近结果不整段放行；默认姓名排序，可切最近工作 |
| Component form / 默认顺序 | Header“员工”+[创建员工] → Tabs“全部/在岗/未在岗/离职” → 搜索/服务业务筛选 → F02行 |
| Primary actions | [创建员工]→U17-C；行[进入工作]→U18 Main |
| Secondary / More actions | 头像/姓名→U18 Utility；[找新人才]→U19；行More [编辑资料][复制员工][调整责任] |
| Interaction / 编辑保存 | 姓名与进入工作分离；跨业务筛选只是投影；编辑同identity，复制明确新identity但无历史/授权 |
| State variants | 原装员工不能当待招聘；无模型显示能力缺口与空闲/阻塞真实状态；离职不抹历史；无匹配[清除筛选] |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从Utility关闭留原行；从Main Back恢复员工筛选/滚动；创建完成选中新员工；继承R |
| Scale / Search / Filter / Sort | 1/20/100员工同身份行，可搜索姓名/职责并筛范围；同员工跨两业务仍一行 |
| Product Fixed | PF-A目录Owner在组织中心，Employment与Work状态分离；PF-C默认排序/创建表单 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

**U17-C 创建员工**用有标题的Drawer，不强迫先建部门。必填姓名、职责简介；可选头像/已有岗位能力包/组织归属/推荐模型；权限与执行范围默认未授予。底部[创建员工]只创建身份，[取消]不留假员工；可保留未完成草稿。成功“员工已创建”，显示[安排责任]/[配置能力]/[进入工作]，无模型不自动工作。

**复制员工**同Drawer预填新姓名（明确“副本”可改）、职责和可复用能力引用；“将复制：可编辑职业配置；不复制：身份、对话、Result、经验私有范围、Secret、Assignment、权限”。连接引用只有原本合法可使用者才可选，需重新确认授权。保存产生新员工并回目录。离职/暂停参与必须预览未完成责任和Holder缺口，不能静默转给复制品。

## 18. Employee Detail / Workstation

**Surface ID: U18** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 清楚这位员工是谁、负责哪些业务，并在正确范围和他工作 |
| Entry | 全产品头像/姓名→Utility；目录[进入工作]→Main；Assignment[讨论]→指定范围Main |
| Context / Product Object | 同Employee identity；选定Assignment与下一消息scope显式 |
| Layout responsibility | Navigation：来源区；独立进入时组织中心；Left Context：Main打开时列此员工最近话题，按最后活动；不是所有工作空间知识树；Main：Main Header F05 → 当前工作/责任摘要 → Conversation → Composer；Utility详情Tabs“资料 / 责任 / 能力 / 记录”，默认资料；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 资料：姓名/头像/来源/加入时间/组织/职责；责任F15；能力F14；记录最近Work/Result；Main F05/F03 |
| Optional fields | 长期专长、成长建议、成本/运行诊断按需；内部ID不默认展示 |
| Component form / 默认顺序 | Main Header F05 → 当前工作/责任摘要 → Conversation → Composer；Utility详情Tabs“资料 / 责任 / 能力 / 记录”，默认资料 |
| Primary actions | Main [发送]；Utility [进入工作]或具体责任[讨论] |
| Secondary / More actions | Utility [编辑资料][添加能力][调整责任]；记录[查看结果]；Main [新话题] |
| Interaction / 编辑保存 | 编辑资料Drawer含姓名/头像/职责简介，岗位/权限不混成文字改名；保存回同详情Tab。能力[添加]开U20；复杂责任变更回组织入口 |
| State variants | 未安排责任可Identity Conversation讨论能力，不伪造业务；模型未配置[配置能力]；多责任无明确目标先选范围再派Work；历史失权引用不可加载 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从头像打开不离开原Work；进入Main保留来源；切Tab不换scope；换责任仅控制下一消息；继承R |
| Scale / Search / Filter / Sort | 责任Tab按业务分组且搜索，显示同一身份；话题可搜索；全部工作不堆在身份卡 |
| Product Fixed | PF-A头像姓名Utility/工作Main/same Employee；PF-C四详情Tab与字段顺序 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

资料Tab默认身份→组织→职责；责任Tab每行“Business/Workspace / 责任 / 汇报对象 / 当前Holder状态 / [讨论]”；能力Tab每行“用途 / 当前能力 / 连接状态 / 默认或可选 / [配置]”；记录Tab为“工作/结果/已采用经验”筛选行。点结果打开U27，不把结果全文嵌员工侧栏。跨业务示例：林墨在Content Growth显示“内容审核”，在Novel Writing显示“章节编辑”，员工名称/头像不变。Identity Conversation标题“与林墨讨论员工安排”，不自动携带两业务私有文本。

## 19. Talent & Capability

**Surface ID: U19** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 发现外部专家与可引入能力，随后成为公司资源/员工 |
| Entry | 全局人才与能力/缺岗[找人才]/能力缺口 |
| Context / Product Object | 外部候选目录；返回目标Employee/Responsibility可选 |
| Layout responsibility | Navigation：人才与能力；Left Context：发现分类“专家 / 技能 / 连接器 / 职业模板”；首次专家；Main：Header+[搜索] → 类型/领域筛选 → 简洁候选行（价值一句/来源/适用职责/依赖状态） → 选中详情Utility；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 名称/能做什么/来源/许可可否使用/依赖/是否公司已有；详情版本与授权要求 |
| Optional fields | 示例结果/来源链接；未经验证的效果不写成评分 |
| Component form / 默认顺序 | Header+[搜索] → 类型/领域筛选 → 简洁候选行（价值一句/来源/适用职责/依赖状态） → 选中详情Utility |
| Primary actions | 专家[招募]；Skill[纳入公司资源]；Connector[连接服务]；模板[预览组队方案] |
| Secondary / More actions | [查看公司已有员工]→U17；[查看来源]；[返回原责任] |
| Interaction / 编辑保存 | 招募Drawer确认姓名/职责/依赖/权限→创建同canonical Employee；Connector跳U28；能力添加不是执行，成功后[绑定给员工] |
| State variants | 目录离线保留已缓存并标更新时间；无可靠供应项显示“暂无可用来源”而非假专家；已引入显示[查看公司资源]；许可未知不自动安装 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 保留来源缺岗/员工目标；招募成功回目标确认Assignment，不能自动覆盖Holder；继承R |
| Scale / Search / Filter / Sort | 搜索名称/岗位，筛类型/来源；大量结果列表分页，不制造第二员工目录 |
| Product Fixed | PF-A人才是外部生态，连接维护Settings；PF-C候选行与招募流程 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

模型/External Agent/MCP若供应发现入口存在，作为能力类型而非额外一级导航；浏览说明与安装能力严格分离。具体Codex可用性由适配器/本机连接事实判定，本文不声称已接通某版本，也不规定不存在的认证方式。可以从员工能力缺口跳到此页找候选，选中后返回U20完成正式绑定。

## 20. Capability Binding

**Surface ID: U20** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 给同一员工增加可验证能力，明确权限与默认用途 |
| Entry | U18能力Tab[添加能力]/U19引入后[绑定给员工]/Work缺口 |
| Context / Product Object | Employee + 能力用途；执行授权仍按原Work范围 |
| Layout responsibility | Navigation：保持原区；Left Context：不新增Context；背景保持员工/原Work；Main：单Drawer：类型→选择能力→连接与检查→权限/范围→默认或可选→影响摘要→保存；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | Employee姓名/用途；类型；能力名称/版本来源；连接状态；必要权限；可用范围；默认或可选 |
| Optional fields | 高级endpoint/启动参数仅该适配器确需时在Settings；费用说明/许可/依赖详情折叠 |
| Component form / 默认顺序 | 单Drawer：类型→选择能力→连接与检查→权限/范围→默认或可选→影响摘要→保存 |
| Primary actions | [保存能力]；连接未满足时主要[连接并检查]，可明确[保存为待配置]但不可显示可用 |
| Secondary / More actions | [取消][查看权限][查看连接]；已有绑定More [设为此用途默认][移除绑定] |
| Interaction / 编辑保存 | 配置Drawer不嵌秘密；[连接]暂存→U28对应连接→检查返回。授权扩大需具体确认，选可选不改默认；保存刷新能力Tab与缺口，原Work不自动重发 |
| State variants | 无连接=待配置；认证失败=需重新授权；连接可用但当前动作不支持独立显示；当前运行使用原版本/授权，变更只作用后续合法工作 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 保存/取消回原员工能力Tab或Work缺口；Settings返回恢复绑定草稿；升级许可被拒不丢原配置；继承R |
| Scale / Search / Filter / Sort | 同类型多能力按用途明确一个默认，其余可选；搜索本公司可用资源；不按员工复制Provider连接 |
| Product Fixed | PF-A唯一Employee能力真源、scope授权不等于组织权力；PF-CDrawer步骤/默认选择 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Codex链具体按钮：员工能力→[添加能力]→类型[外部Agent]→搜索“Codex”→候选详情显示适配器事实。已可用连接选择后[检查连接]；未安装或未授权显示适配器给出的[安装说明]/[前往授权]，正常系统授权窗不由Curis伪造。无法检测就“尚未验证”，可保存待配置但不能[设为可执行默认]。授权确认显示“读取哪些文件/允许哪些动作/作用目录/何时需你确认”，不使用“完全访问”作为默认。完成后返回Drawer，选择“默认用于代码工作”或“需要时选择”，[保存能力]。页面文字“已绑定，尚未用于工作”区别于“已执行成功”。移除绑定不卸载程序或断开其他员工共用连接。

## 21. Operating Intelligence

**Surface ID: U21** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 把已有事实变成可解释的经营判断，并追问形成真实分析工作 |
| Entry | 全局经营洞察/业务[查看经营分析]/Result追问 |
| Context / Product Object | Company/Business/Workspace/Employee等分析范围+周期；非新执行父级 |
| Layout responsibility | Navigation：经营洞察；Left Context：公司经营 / 业务分析 / 组织与员工 / 模型与能力 / 分析报告 / 专项研究；Main：范围与周期Header → 数据完整性提示 → 目标相关指标行/语义图表 → 分析报告列表；选报告Reading Main；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F13；报告标题/范围/周期/作者/责任/时间/复核；正文事实→解释→未知→建议→依据 |
| Optional fields | 模型/Agent来源在报告来源详情；方法/样本量/可比性展开；不默认几十图表 |
| Component form / 默认顺序 | 范围与周期Header → 数据完整性提示 → 目标相关指标行/语义图表 → 分析报告列表；选报告Reading Main |
| Primary actions | [请分析师分析]→带范围和数据引用的U24 |
| Secondary / More actions | [比较业务][查看依据][补充数据][追问报告][请求复核]；有事实才[切换图表] |
| Interaction / 编辑保存 | 比较Main选择相同指标口径/周期/对象；不可比标明原因，不强制排名。补充数据Drawer必填值/单位/期间/来源/记录人，只追加人工事实，不覆盖原值 |
| State variants | Business0解释暂无经营数据但有真实Analyst；未连接/不支持/过期分开；报告生成中链接真实Work；分析师失配[安排分析责任]；查询失败不填0 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从业务进入保留From/期间；报告→Conversation→新报告可回旧版本；Evidence关闭回同报告段；继承R |
| Scale / Search / Filter / Sort | 业务比较默认选择2–5项，更多仍Table明确口径；报告搜索/范围/期间筛选，默认最新 |
| Product Fixed | PF-A不建第二数据/分析真源，Analyst正式责任；PF-C顺序及比较交互 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

[追问报告]打开同报告来源的分析Conversation Main，引用报告版本和当前选中数据；用户先看到预填问题与范围，[发送]才成为新消息/必要Analysis Work。追问不会改旧报告正文。Trend默认Line；Comparison默认Sorted Bar并附表格；Composition可Stacked；缺可比数据直接Table+未知说明，不强造图。[请求复核]选具有相关能力且满足独立性条件的员工；没有候选显示缺口，不把同一执行换名字当独立验证。

## 22. Knowledge Library / 资料库

**Surface ID: U22** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 读取、引用与沉淀资料，知道来源、版本、谁在使用 |
| Entry | 全局资料库/Composer添加引用/结果知识候选 |
| Context / Product Object | Company Reference Space；显示适用范围，不复制Work对象 |
| Layout responsibility | Navigation：资料库；Left Context：概览 / 浏览；浏览下类型过滤“来源/参考/成果文件/模板/知识/规则”，是分类非独立系统；Main：概览最近使用/需核对来源→浏览F09列表；点击正文进入Reading Main：标题/来源/适用范围/版本→正文→Used By；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F09；阅读页正文/许可或访问限制/引用与版本；Used By原Work/Result链接 |
| Optional fields | 作者、更新历史、导入记录、来源同步时间、标签；不默认本地路径技术树 |
| Component form / 默认顺序 | 概览最近使用/需核对来源→浏览F09列表；点击正文进入Reading Main：标题/来源/适用范围/版本→正文→Used By |
| Primary actions | [添加资料]→选择本地文件/链接/文本的短选择overlay |
| Secondary / More actions | [引用到当前工作][查看来源][查看使用关系]；More [更新资料][调整使用范围][归档] |
| Interaction / 编辑保存 | 添加后Drawer标题/类型/来源/适用范围必填确认，解析完成才可引用；长文编辑Main。正式Knowledge/Policy修改形成有来源新版本和必要接受，不把普通备注升Authority |
| State variants | 空库[添加资料]；解析中不可引用未完成文本；来源不可达保留合法已读版本标过期；无权限Reference显示不可访问；导入失败可重试原条目 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从Work选择引用完成后回原Composer草稿；阅读→Used By→原Work；返回保留资料筛选/阅读位置；继承R |
| Scale / Search / Filter / Sort | 搜索标题与合法正文、类型/适用范围/新鲜度筛选，默认最近使用；模板不触发自动新Business |
| Product Fixed | PF-A Reference/Evidence/Result边界；PF-C列表/阅读布局与引入动作 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

**引用选择器**是Main工作上的overlay：搜索框、范围声明、结果行、已选引用列表，[添加引用]。选中即显示版本/适用范围；未保存的上传附件有“正在准备”，不能发送为已读取。只显示当前Work有权使用的内容，跨范围引用若不合法需回源授权，不能一个确认框绕过。Artifact是输出文件引用，打开编辑若支持则新修订，不修改原Result；Template点击[预览复用]回U12-D/对应创建，不复制历史。Policy正文由合法Owner确认后生效，普通Library导入只能参考材料。

## 23. Meetings

**Surface ID: U23** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 持续多人讨论、明确分歧、形成正式决定和可追踪后续工作 |
| Entry | 全局会议/Business或Work[发起讨论会议]/Assistant建议 |
| Context / Product Object | Meeting有Company或真实来源scope，参与Employee权限独立 |
| Layout responsibility | Navigation：会议；Left Context：会议集合：进行中 / 已结束；当前会议可切“讨论/决定与跟进”两个Main Tab；Main：列表F08；会议Main Header议题/范围/参与者/状态 → 当前议题与未决摘要 → 参与员工自然Conversation → Composer；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F08/F05；消息发言人/内容/引用；提案/P7；后续Work标题/Owner/状态/检查点 |
| Optional fields | 议题背景、参与者职责、历史来源、结构化观点/分歧在Utility；计划时间可选 |
| Component form / 默认顺序 | 列表F08；会议Main Header议题/范围/参与者/状态 → 当前议题与未决摘要 → 参与员工自然Conversation → Composer |
| Primary actions | 列表[发起会议]；会议[发送]；需要CEO时P7 [查看方案] |
| Secondary / More actions | [查看参与者][添加资料][查看决定与跟进]；More [编辑议题][结束讨论][重新讨论] |
| Interaction / 编辑保存 | 创建Drawer必填标题/讨论目标/范围/至少真实参与员工，背景资料可选；[创建并进入]只创建会议，发起AI讨论须真实可用执行；参与者修改检查权限 |
| State variants | 无会议可创建；无模型保留准备中；等待CEO与等待资料分开；讨论中断核对原轮次；会后Work失败不把会议决定删掉 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 离开不结束会议；Back恢复话题位置；Follow-up Work→Result→返回原会议跟进Tab；继承R |
| Scale / Search / Filter / Sort | 列表可搜议题/筛范围/按最近讨论；多人头像最多3+人数，详细参与者Utility；长讨论折叠已读部分但不丢历史 |
| Product Fixed | PF-A自然Conversation/Decision/Work闭环；PF-C两个Main Tab、创建形式 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

AI整理的Fact/Opinion/Proposal放可打开的引用块，CEO不需要手工分类每句话。会议[形成决定]进入既有P7，不把会议结束当全部建议被批准。接受后按原Decision生成明确Owner/范围/期限的后续Work，跟进Tab每行可[查看工作]；尚未产生Work时写“等待安排”，不造任务。[结束讨论]短Modal说明“后续工作继续，讨论可重新打开”，不取消执行。签字/付款相关事项进入U26，不在会议里放真实支付表单。

## 24. Conversation / Work

**Surface ID: U24** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 与员工在清楚的责任范围持续工作，看进展、控制请求和取得结果 |
| Entry | Leader [讨论]/员工[进入工作]/Work行/Quick Access |
| Context / Product Object | Conversation identity + 每条message scope + Work/Assignment；不强制一话题一新业务 |
| Layout responsibility | Navigation：保留来源七区；不是第八区；Left Context：当前员工/工作的近期话题与有限引用导航；可收起；Main：F05 Header → 当前Work摘要/真实待处理Banner → 消息流 → Shared Composer；进展在对应工作消息内，不另建后台面板；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 员工名/话题/下一消息范围；消息身份/引用/发送状态；工作标题/责任/状态/下一动作；Composer文字/附件/上下文/Send或Stop |
| Optional fields | 时间按消息组与Hover显示、工具过程折叠、来源Utility、消息范围变化事件；无虚构thinking全文 |
| Component form / 默认顺序 | F05 Header → 当前Work摘要/真实待处理Banner → 消息流 → Shared Composer；进展在对应工作消息内，不另建后台面板 |
| Primary actions | [发送]；运行中[停止当前执行]（有停止能力才提供） |
| Secondary / More actions | [添加引用][添加附件][新话题][查看工作][查看结果]；More [查看工作记录]；对失败消息[重试发送] |
| Interaction / 编辑保存 | 未接收消息保留草稿；已经接收但断流先核对，不能把[重试发送]用于重做任务。编辑未发送文字直接；已发送内容[引用并补充]产生新消息，首版不改写历史/自动branch |
| State variants | 无消息写“在〈范围〉与〈员工〉开始讨论”；无模型发送区域说明并给[配置能力]，草稿可写；运行/等待/失败按G；停止请求中“正在请求停止”，停止回执后才暂停 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 主对话离开保存草稿/滚动锚点；切范围不清历史；结果关闭回对应消息；工作历史重开同identity；继承R |
| Scale / Search / Filter / Sort | 长内容块bounded阅读+[展开阅读]Utility；消息不自动跳底，底部出现[有新消息]；多任务用Work标题选择，不混Stop对象 |
| Product Fixed | PF-A Conversation Main/Shared Composer/历史scope；PF-C消息行为、按钮、滚动与错误策略 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

**Composer合同**：由上到下是可移除的Reference/Attachment预览行、输入区、操作行。输入placeholder“和〈员工〉讨论〈当前范围〉…”；操作行左[添加]菜单“引用/文件”，中为简短可点Context（打开只读范围与必要引用Utility），右[发送]或[停止当前执行]。模型/Agent选择仅宿主确有合法可选能力时在[工作方式]菜单；普通业务面不强制展示型号。多行向上扩展至约8行后输入区自身滚动；精确高度由视觉阶段定。附件每项显示准备中/可引用/失败与[移除]；不支持类型明确拒绝，不丢文字；拖入文件与选择文件走同一校验，拖入对象只加引用，不移动原对象。

**Steering**：运行时允许输入补充并点击[发送补充]，产品需真实区分“已送达当前工作/排队等待/当前执行不支持中途补充”；后者保留草稿并给[停止后继续讨论]，不假装已改变当前运行。Stop只指Header明确的当前执行，不停止整个业务。Work计划展示真实步骤与状态，工具细节折叠[查看过程]；没有可量化进度只写正在处理的动作，不估百分比。只有实际可恢复的工作才给[继续工作]，否则说明需要以已保存结果重新安排，产生新Work并链接旧Work。

**消息切范围**：[切换范围]打开搜索选择Popover，先选Business/Workspace/具体责任；发送前Header及输入区显示目标。旧消息保留原scope，引用重新校验；有不兼容附件列出并要求移除或选回原范围。身份聊天可合法无Business；不能为一次简单工作造Workspace。

## 25. Decision

**Surface ID: U25** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | CEO看清必须自己决定的取舍，并留下可执行的选择 |
| Entry | CEO Desk/原Work/Meeting的P7 Banner |
| Context / Product Object | 原Decision及其原责任scope；AI责任未转移 |
| Layout responsibility | Navigation：保留来源区；Left Context：继承原Work/Meeting Context；Main：原Working Main的P7 Detail：问题与为何需CEO→推荐与理由→可选方案/代价/风险→选择后继续方式→动作；Utility证据；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F06并完整覆盖P7八语义；方案版本/当前有效状态；来源FACT/POLICY/EVIDENCE/EST/UNK |
| Optional fields | 长技术依据仅Utility；没有事实的时间/成本写未知 |
| Component form / 默认顺序 | 原Working Main的P7 Detail：问题与为何需CEO→推荐与理由→可选方案/代价/风险→选择后继续方式→动作；Utility证据 |
| Primary actions | 简单Banner [按建议处理]；复杂Banner [查看方案]；Detail [选择〈明确方案名〉] |
| Secondary / More actions | [其他方案][暂缓][要求修改][查看依据]；拒绝明确[不接受此方案] |
| Interaction / 编辑保存 | 可逆低歧义直接按已见方案；高风险/不可逆先Detail再明确影响确认，不能Banner一键批准。修改方案形成新版本，旧按钮失效 |
| State variants | 提交中禁重复，成功显示选择/时间/后续状态；已被处理显示真实结果；授权失效不能批准；网络超时核对Decision而非重复提交 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 完成返回原Work继续状态或CEO来源；无需另建对话/Handoff；Evidence回同方案选项；继承R |
| Scale / Search / Filter / Sort | 选项默认完整呈现，不藏Dropdown；多Decision以问题行列表导航，禁止批量批准不同高风险事项 |
| Product Fixed | PF-A P7/Viewed≠Accepted/决策≠Handoff；PF-C布局与明确按钮语言 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

[暂缓]不等于拒绝或同意，保留原责任；可选“何时再看”仅在用户填写时记录检查点，不默认自动催促。接受后的“已决定，等待工作恢复”与“工作已继续”分开；若执行恢复失败，Decision仍已接受，CTA是[查看恢复问题]，不能要求重复批准同一方案。

## 26. Human Handoff

**Surface ID: U26** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 让人完成AI无法完成的必要动作，并可靠接回原工作 |
| Entry | 原Work提示/CEO Desk/通知[继续处理] |
| Context / Product Object | 原Work外部动作与账号/目标；不是将整个业务交给真人 |
| Layout responsibility | Navigation：保留来源区；Left Context：原Work Context；不新建人工操作中心；Main：原Work Main内F07动作包 → 已准备内容/必要说明 → 外部入口 → 完成报告/核对结果 → 继续条件；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F07；外部目标可辨识身份；原责任Employee；完成判据；真实时效如有 |
| Optional fields | 备用操作方式、合法帮助链接、提交凭证引用；无有效链接不生成假二维码 |
| Component form / 默认顺序 | 原Work Main内F07动作包 → 已准备内容/必要说明 → 外部入口 → 完成报告/核对结果 → 继续条件 |
| Primary actions | [前往〈平台/授权页〉]；回来[我已完成]→核验；可查询时[核对结果] |
| Secondary / More actions | [查看准备内容][暂时不处理][遇到问题]；后者回原Conversation而非新工单 |
| Interaction / 编辑保存 | 浏览器/系统授权/手机完成真实动作；用户报告后显示“已记录，正在核对”，核验成功才恢复。无法核验则“你已报告完成，尚无平台确认”，保留证据要求 |
| State variants | 外链到期[获取新入口]前先核对旧动作结果；手机未回收=等待你；平台未确认=等待平台；权限不足定位授权，不记录秘密；未知结果不重复付款/发布 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 外部回来原Work，不强制跳CEO首页；从通知进入仍能返回原通知清单；恢复自动按已有授权继续；继承R |
| Scale / Search / Filter / Sort | 多动作按原Work行排列，按账号/截止筛选；一个包一个明确目标，无全局[全部完成] |
| Product Fixed | PF-A Work continuity/权限/Decision分离；PF-C动作包与核验文案 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

登录、手机确认、签字、付款的入口形式共用动作包，完成判据不同：登录需连接检查；手机发布需平台回执或明确人工证据；签字需签署回执；付款需真实支付状态。人工截图或用户报告必须保留“人工来源/尚无平台回执”；可据其作有边界的经营判断，但不能伪造Connector Receipt或把人工说明写成平台已确认状态。付款/不可逆签字若尚未得到授权，先P7决定再外部执行，不能把[前往平台]当支付授权。专业Handoff可能只是User Required步骤，并不自动构成员工间accountability transfer；只有明确接收责任才记既有责任Handoff。两个概念共用可理解语言，不混写Runtime truth。

## 27. Result / Evidence / Learning

**Surface ID: U27** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 读取成果、追溯依据、确认接受或形成后续改进 |
| Entry | Work/CEO Desk/员工/Meeting/Library结果引用 |
| Context / Product Object | 原Result/版本/原Work scope；Business/Account仅关联视角 |
| Layout responsibility | Navigation：保留来源区；Left Context：保持原来源，不另建结果中心；Main：Utility：F04 Header/版本与接受状态→一句结论→输出预览→证据列表→后续动作；长读[maximize]；Evidence替换同Utility并有内部Back；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F04；原Work链接、作者、版本、交付时间、Evidence source/freshness/访问权限；接受方/状态 |
| Optional fields | 工具日志/附件元数据、旧版差异、使用记录；下载只对真实文件可用 |
| Component form / 默认顺序 | Utility：F04 Header/版本与接受状态→一句结论→输出预览→证据列表→后续动作；长读[maximize]；Evidence替换同Utility并有内部Back |
| Primary actions | [展开阅读]；待接受且当前有资格[接受结果]，否则只读 |
| Secondary / More actions | [查看依据][要求修改][继续讨论][下载]；Learning [应用建议]/[保存为知识候选] |
| Interaction / 编辑保存 | 查看只产生Viewed；接受明确当前版本与用途；要求修改→原Work补充/后续Work，不涂改原交付。Learning应用显示目标规则/适用范围/变更前后，普通战术在授权内，重大目标转P7 |
| State variants | 尚无Result保留Work入口；附件读取失败不丢结果摘要；证据缺失显示缺口不禁阅读，但接受需按原评审规则；下载失败重试文件读取不重跑Agent |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 最大化退出恢复原Utility大小与Main滚动；Evidence内部返回保留Result版本；继续讨论回Main并引用当前版本；继承R |
| Scale / Search / Filter / Sort | 多版本Dropdown按时间/修订列，默认入口指向的版本；不可默换最新；证据列表搜索标题/类型 |
| Product Fixed | PF-A Result/Evidence同源/Viewed≠Accepted；PF-C阅读结构、版本与Learning动作 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Result若来自报告，点击[在报告中查看]进入U21 Reading Main；Artifact若可编辑，[编辑副本/新修订]在专业Main，保留旧Result引用。Learning默认只是“这次发现/适用条件/证据/下一步建议”，不新建成长中心。[应用建议]先显示作用对象与未来范围，成功后链接真实规则/知识变更；未保存则仍“建议”。不把盈利相关性写成确定因果。

## 28. Settings / Connections

**Surface ID: U28** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 维护全局偏好、连接和权限，并回到需要它的工作 |
| Entry | CEO头像[设置]/Work[连接服务]/U20连接步骤 |
| Context / Product Object | 当前Company资源与个人应用偏好；具体连接唯一 |
| Layout responsibility | Navigation：来源区保留高亮；从头像打开；Left Context：个人与外观 / 公司设置 / 模型与AI / 权限与安全 / 应用与数据 / 账户与帮助；Main：Settings Main类别Header→设置行/连接列表；连接Detail同Main：F18→可用能力与范围→使用者→维护动作；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 当前选中类别；连接F18；默认模型对应用途；权限对象/授权状态；主题/语言/时区/通知实际值 |
| Optional fields | 端点/自定义命令/诊断展开；只显示凭证已保存/未保存，不展示值 |
| Component form / 默认顺序 | Settings Main类别Header→设置行/连接列表；连接Detail同Main：F18→可用能力与范围→使用者→维护动作 |
| Primary actions | 未连接[添加连接]/[连接并检查]；偏好[保存]（主题即时预览并保存） |
| Secondary / More actions | [测试连接][发现模型][重新授权]；More [撤销连接][清理缓存][导出数据]按权限与影响 |
| Interaction / 编辑保存 | 连接编辑Drawer采用适配器声明字段，秘密只安全输入；保存配置不等可用，检查单独回执；返回原绑定继续确认，不自动授权所有Employee |
| State variants | 模型不可发现允许明确手动配置但标未验证；认证失败/不支持分开；访问OS设置用户完成再检查；导出失败不显示完成；无权限不能透出Secret |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | [返回〈员工/Work〉]恢复草稿；无From回原一级区；换主题不重置业务Context；继承R |
| Scale / Search / Filter / Sort | 连接按类型/状态搜索；Account为连接外部身份列表，不新增业务Account第二真源；更多服务分页 |
| Product Fixed | PF-A设置六类/权限可撤销/来源返回；PF-C设置行和连接编辑 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

模型与AI：Tabs“模型 / 外部Agent / 连接器”用于稳定资源类型；MCP显示在连接器类型标签，Skill资源维护可从人才或员工跳入既有公司资源，不另增一级区。Company Model Default只影响后续未明确选择的工作；不能偷偷覆盖员工显式配置。Computer Access在权限与安全：分别显示屏幕读取/辅助功能/文件目录/浏览器操作真实状态，[打开系统设置]后[重新检查]，角色高不等于系统许可。

通知：应用内更新/待处理提醒/系统通知开关，静默不终止业务；Data/Privacy：数据位置只读、[导出]先范围/目标确认、[清理缓存]说明不会删除Work/结果；[删除数据]必须显示确切集合、不可逆与备份出口，不混在清缓存。Company资料名称/时区可编辑，改时区展示对排期解释的影响；现有排期不能静默重排。Theme只视觉，未冻结新颜色。Provider账户与CEO应用账户分开，不加入多真人邀请/付费购买流程承诺。

## 29. Global CEO Assistant

**Surface ID: U29** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | CEO随时表达经营意图、收取简报和追踪专业责任 |
| Entry | 全局浮动入口/已有Assistant展开状态 |
| Context / Product Object | 同canonical Assistant与durable Conversation；使用可见且合法的范围提示 |
| Layout responsibility | Navigation：跨七区全局浮层；Left Context：无专属Pane；Main：收起形态身份/真实待处理提示；展开浮层Header身份/收起→简短对话→Context提示→Shared Composer；复杂工作跳原Main；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | Assistant身份；当前引用范围；消息/动作状态；明确[在工作面继续]目标 |
| Optional fields | 窗口位置/尺寸视觉开放，跨七区保持；无真实通知不造红点 |
| Component form / 默认顺序 | 收起形态身份/真实待处理提示；展开浮层Header身份/收起→简短对话→Context提示→Shared Composer；复杂工作跳原Main |
| Primary actions | [发送]；提案/Work明确[打开〈工作面〉] |
| Secondary / More actions | [收起][查看当前引用][打开相关工作]；可拖动Handle带可访问名称，收起不停止 |
| Interaction / 编辑保存 | “开始新业务”生成/进入U12-C同源提案；不在浮层完成复杂配置/审批。拖动不选中文字，键盘可用[重置位置]；不创建第二Assistant记录 |
| State variants | 无模型可写草稿，提示设置入口；连接中断保留对话；跨页面不换身份；引用失权移除并解释，不能携带旧scope全文 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 收起恢复原Main焦点；打开专业面后浮层仍同identity但可收起；返回不重发委托；继承R |
| Scale / Search / Filter / Sort | 只呈现当前简短交互，长结果[查看结果]Utility；不塞全公司未读会话树 |
| Product Fixed | PF-A独立global floating/同identity/不替专业Owner；PF-C复杂内容转Main与明确Context提示 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Assistant随浏览可提示“当前查看：内容增长”，但已有对话指令作用范围不能自动改变。[引用当前页面]才添加具体对象引用，执行前显示目标。Assistant代为找到Leader不是把Leader人格装进浮层；[和负责人讨论]进入同Leader Main。简单P7仅在真正符合八语义与授权条件时可按既有Banner处理，复杂/资金决定一律[查看方案]进入原Main。

## 30. Content Growth Domain

**Surface ID: U30** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 在共享公司责任上组织内容经营现场，保持专业对象连续 |
| Entry | 已启用Content Growth业务→具体Workspace；不是默认新公司业务 |
| Context / Product Object | Content Growth Workspace；Account pool为合法绑定投影 |
| Layout responsibility | Navigation：业务空间；Left Context：经营 / 账号 / 内容 / 发布；数据入口到scoped经营洞察；团队入口复用U14；Main：默认经营面：当前目标/本轮重点/最新判断/下一步 → 真实待处理 → 值得注意账号行 → 当前内容Work行 → 最新结果引用；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | Workspace身份/Leader；F11/F03/F04；目标/数据缺口 |
| Optional fields | 机会输入/收益证据只有当前目标相关才展示；规则/平台能力Utility |
| Component form / 默认顺序 | 默认经营面：当前目标/本轮重点/最新判断/下一步 → 真实待处理 → 值得注意账号行 → 当前内容Work行 → 最新结果引用 |
| Primary actions | 初始[接入经营账号]；正常[和负责人讨论]；具体事项[继续处理] |
| Secondary / More actions | [查看全部账号][查看内容][查看发布][查看经营分析][带入一个机会] |
| Interaction / 编辑保存 | 账号接入U31绑定合法Company Account；外部机会[带入]Drawer链接/描述/来源/适用账号→参考输入，必要时形成研究Work不自动接单 |
| State variants | 无账号可准备经营方案不可发布；Provider未连接不伪造统计；不支持的域动作显示边界而非假按钮 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | Account/内容/发布面切换恢复对象选择，Workspace不变；数据分析后回原账号/内容；继承R |
| Scale / Search / Filter / Sort | 1/5/20账号保持同Workspace可行，按真实经营边界拆空间，不因平台不同自动拆 |
| Product Fixed | PF-A Domain Candidate/Account≠Workspace；PF-C域导航/默认顺序，承接S12 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

发布员工和分析员工始终解析为Curis责任Holder；Provider品牌在连接详情与错误恢复出现，不替换员工身份。内容增长Business仍用U13四段，域经营面位于Workspace；业务级摘要可直接引用账号异常，但点击进入其实际Workspace/账号。共享127项能力的Owner沿用S12附录B，本稿没有因为四个域入口再建四套Work/Result/Analytics。

## 31. Content Growth Account Operating

**Surface ID: U31** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 一个账号长期由团队经营，CEO看重点、当前内容和真实反馈 |
| Entry | U30账号行/U13引用异常/Search |
| Context / Product Object | 具体Channel Account + 所属经营Workspace + Business；连接身份单独 |
| Layout responsibility | Navigation：业务空间；Left Context：本Workspace Domain导航；账号集合可展开并搜索/平台筛选，不强迫经过平台页；Main：Header F11/Goal一句 → 当前经营（Strategy一句/本轮重点/下一步） → 需你处理（有才出现） → 当前内容与Work行 → 最近表现与Result摘要；无八Tab；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 账号名/平台/handle/连接状态/Goal；真实负责责任员工；F03/F12/F13的当前相关记录 |
| Optional fields | Goal全文[展开]；Strategy全文Utility；团队/历史/收益证据按需；不默认粉丝等级/资格地图 |
| Component form / 默认顺序 | Header F11/Goal一句 → 当前经营（Strategy一句/本轮重点/下一步） → 需你处理（有才出现） → 当前内容与Work行 → 最近表现与Result摘要；无八Tab |
| Primary actions | [和账号负责人讨论]；当前人工动作[继续处理]为事项主按钮 |
| Secondary / More actions | [调整目标][查看打法][查看全部内容][查看经营分析][查看负责团队]；More [管理账号连接][暂停此账号相关安排] |
| Interaction / 编辑保存 | Goal点击[调整目标]先Utility对照→Drawer“目标修订提案”（目标/成功标准/检查点/影响范围）→P7接受生效；Strategy[讨论打法]Main，同一对象不改Workspace |
| State variants | 账号未绑定[接入经营账号]；连接失效显示[重新连接]不称账号被封；无数据用六类G细分；Provider失败留准备成果；无Holder显示[安排责任] |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 从20账号选中A后打开内容/报告返回仍A、原筛选与滚动；改连接不丢账号长期历史；继承R |
| Scale / Search / Filter / Sort | 当前Work最多5条、最近结果3条，[查看全部]到同范围集合；账号名/平台/需处理筛选，默认需处理优先再名称 |
| Product Fixed | PF-A账号不是scope/Workspace；PF-C无八Tabs、字段顺序、按需Strategy |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

**账号绑定Drawer**：选择Company已有外部账号或[连接新账号]；显示平台/可辨身份/连接环境、当前Workspace、目标与策略摘要、责任安排、当前能力覆盖。保存绑定只建立合法关联，不默认发布。多Workspace可服务同账号时显示已有关系，要求明确本次经营范围，不自动迁移历史。新连接返回后再确认绑定；无法验证账号身份时保存草稿，不编造handle。

Header Goal默认一句最多两视觉行，[展开]看全文，不能用“增长中”Badge代替具体目标。[查看打法]Utility字段“定位/受众/内容策略/节奏/边界/生效状态”；只读不会新建Work。账号本轮策略与Business整体方向不能简单default/override；有冲突提示交给Leader处理。暂停账号安排是对关联Work/排期的范围化请求，影响列表逐项说明，不能发明Account Runtime总开关。

## 32. Content / Variant

**Surface ID: U32** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 把共同内容意图生产为各账号适配的定稿并审核 |
| Entry | U30内容/U31内容行/生产Work Result |
| Context / Product Object | Content Intent→per-account Variant→原Work；同账号修订保留版本 |
| Layout responsibility | Navigation：业务空间；Left Context：内容集合/当前Intent；保留Workspace导航，可收起；Main：Intent Header标题/目的/目标账号 → per-account Variant比较表 → 选中Variant Main Editor；规格与引用Utility；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | Intent目的/目标账号；F12；Editor内容形式/标题/正文或脚本/媒体/封面（依规格）/审核状态 |
| Optional fields | 平台标签/分类/版权/链接等仅适用时显示；差异说明/来源引用按需；不默认全部平台表单 |
| Component form / 默认顺序 | Intent Header标题/目的/目标账号 → per-account Variant比较表 → 选中Variant Main Editor；规格与引用Utility |
| Primary actions | [交给员工生产]；已产出选中版[提交审核]；审核通过[准备发布] |
| Secondary / More actions | [添加目标账号][预览此版本][编辑内容][查看规格][和生产员工讨论]；More [移除此目标]仅未执行计划 |
| Interaction / 编辑保存 | 长内容Main编辑，[保存此账号版本]保存草稿修订不发布；改已审核内容需重新审核，旧已发布版本不改；FULL_DIVERGENCE仍属于原Intent下Variant |
| State variants | 无内容[创建内容意图]；生成中显示真实Work；规格未知不能承诺适配；媒体上传失败保留文本；某账号版本失败不阻塞阅读其他版 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 编辑/预览/Conversation回同Variant修订与滚动；换账号前脏草稿处理，不将A正文带到B；继承R |
| Scale / Search / Filter / Sort | 1目标仍显示具体账号；多目标表格可按平台/状态筛；目标过多可分页但保存始终标具体账号 |
| Product Fixed | PF-A Shared Intent/per-account Variant/隔离；PF-C表格+Main编辑、字段显隐 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

Intent创建Drawer必填标题/要表达什么/预期目的/目标账号；内容参考可选，[保存意图]不创建假生产Result，[交给员工生产]才按已授权责任形成Work。平台形式在生产前参与Brief，账号定位/语气/受众在同一Brief限定，不等到发布时才改字数。

Variant编辑按形式：图文为标题/正文/图片顺序/封面；视频为标题/描述/脚本或真实视频/封面；不适用项隐藏且不强制空值。平台规格来自可追溯能力事实，未知标明。共用修改只有显式[将这项修改应用到其他目标…]选择目标并预览差异才执行，默认只当前版，不复制账号私有Context。审核是逐版本明确状态，不因一个通用文案被接受就所有账号自动通过。

## 33. Publishing

**Surface ID: U33** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 按账号准确提交、确认与恢复发布，清楚部分成功 |
| Entry | U32 [准备发布]/U30发布/账号状态 |
| Context / Product Object | 每个Publication关联目标Account/Variant修订/原Work/执行方式 |
| Layout responsibility | Navigation：业务空间；Left Context：本Workspace发布集合，当前Intent或账号筛选；Main：Header范围/计划摘要 → 目标执行表（账号/修订/审核/能力/计划时间/状态/下一动作） → 选中记录详情/真实回执Timeline；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | F12+执行方式可用性、明确账号、定稿修订、授权、每个Publication状态/最近核对 |
| Optional fields | 排程/分发政策/平台选项按需；Provider技术详情Utility；原生平台回执链接 |
| Component form / 默认顺序 | Header范围/计划摘要 → 目标执行表（账号/修订/审核/能力/计划时间/状态/下一动作） → 选中记录详情/真实回执Timeline |
| Primary actions | [确认发布计划]后在已授权可用目标[执行发布]；需要人则[继续处理] |
| Secondary / More actions | [预览定稿][查看回执][核对结果]；确认未提交才[重试发布]；More [取消未执行计划] |
| Interaction / 编辑保存 | 确认Main计划列目标/内容/时间/权限/不可逆影响；必要P7先批准。按钮禁重入，已提交立即显示真实状态；返回未知先查结果，不能整体重试成功账号 |
| State variants | 未定稿/未审核=Blocked；等待手机=User Required；已提交=Provider Waiting；未知=结果待确认；失败仅确认未完成；停止不撤平台内容 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 手机/浏览器返回原Publication/Work；查询成功同步账号/Variant/Work投影；已发布记录不可因页面返回重发；继承R |
| Scale / Search / Filter / Sort | 1/5/20目标均每账号一行，可平台/状态筛选；汇总“已确认2/待确认1”只是聚合，非总publication truth |
| Product Fixed | PF-A per-account Publication/Distribution Policy/回执事实；PF-C发布计划Main、表格及恢复按钮 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

发布能力用四种说明：“员工可执行 / 需要你确认 / 需要浏览器连接 / 当前无法代办”，未知另写“尚未验证”。同Provider对不同账号能力不同。失效账号仍留在目标表，状态Blocked并给恢复入口，不静默从Target移除以美化成功比例。时间选择区默认[准备好后发布]，有真实能力才[指定时间]；指定时间必须日期/时区，注明“Curis计划”或“平台已接受排期”，不能混同。BEST_EFFORT/ALL_REQUIRED用人话解释其他目标失败后未执行项怎样处理，消费已有Distribution Policy，不新增总状态；已成功发布不回滚。

[取消未执行计划]只取消尚未提交的安排；对已提交平台动作显示原生取消能力是否可用，无能力则给官方入口与核验。撤回已发布内容是独立危险动作，不混在Stop。[重试发布]先重新校验修订/账号/权限，已有未知执行先核对；无查询通道时保持未知并人工核实，不通过新发一次“解决”未知。

## 34. Analytics / Content Growth

**Surface ID: U34** · PF-A关系 + PF-C表达（下述具体字段、形式与动作）。

| 合同项 | 选定表达 |
|---|---|
| Purpose | 看账号真实表现及分析员工判断，形成下一轮有依据调整 |
| Entry | U31/U30 [查看经营分析]/发布回执的表现入口 |
| Context / Product Object | 原Account/Publication/Workspace + 周期作为分析对象，执行scope仍canonical |
| Layout responsibility | Navigation：经营洞察（从账号带范围进入）；Left Context：U21业务分析，原账号范围保留；Main：范围/周期Header → 数据覆盖说明 → F13指标/趋势 → 相关Publication表 → 分析解释/未知/Learning → 原Work与证据；Right Utility：对象详情/Evidence，默认收起；Assistant：同一全局浮层，不占位 |
| Required fields | 值/单位/期间/来源/采集时间；六类数据状态；分析作者/责任/依据；下一步建议 |
| Optional fields | 收益仅有明确来源/币种/确认状态才加入；成本不全不显示确定利润；归因范围说明 |
| Component form / 默认顺序 | 范围/周期Header → 数据覆盖说明 → F13指标/趋势 → 相关Publication表 → 分析解释/未知/Learning → 原Work与证据 |
| Primary actions | [请分析员工解读]→原范围Conversation |
| Secondary / More actions | [补充数据][查看原始依据][比较内容][返回账号]；有真实通道[重新获取数据] |
| Interaction / 编辑保存 | 人工数据Drawer必填账号/指标/值单位/期间/来源，标人工并附证据；Learning回U27规则提案；拉取失败不写0 |
| State variants | 真实0显示0且来源；未采集/不支持/连接失败/过期/无法确认的0各自文案；旧值保留但标时效，不算新周期 |
| Empty / Unknown / Failure / 权限 | 继承G；以下专项状态优先。空集合与筛选无结果分开；局部失败保留其他区；无权不显示私有内容 |
| Navigation target | 以行标题与明确CTA区分目标，详见本节补充及§37 |
| Return behavior | 报告/证据/讨论后回原账号、期间与筛选；数据修正追加记录不改平台原始事实；继承R |
| Scale / Search / Filter / Sort | 多账号只比较同语义数据，不跨平台盲加；1/5/20账号支持表格筛选/分别报告，空数据列有原因 |
| Product Fixed | PF-A分析Employee≠Provider、同源Insights；PF-C覆盖说明先于图表 |
| Design Open | 颜色、字体、间距、分隔线、圆角、图标、动效；可调密度但不删除Required、改变顺序/组件类型/行为或改变Context |

首次无数据的默认页面就是“尚未取得这个账号的表现数据 / 最后检查时间 / 原因 / 可做的下一步”。不要求设计师补一套美化演示数。累计值只有区间端点同口径、无重置且时间可比时可派生增量；否则展示累计及限制。建议下一轮必须带“基于哪些内容/有效期/尚未知道什么”，不因一个数据点自动改Goal。

## 35. Multi-account / Multi-business Context

同一Employee林墨服务内容增长和小说：组织版图只一身份、两条Assignment；目录只一行“内容审核，另1项”；详情责任Tab分两业务；从内容账号进入显示“林墨 · 内容审核 · 内容增长/空间A/账号A”，从小说进入显示“林墨 · 章节编辑 · 小说/空间B”。这里只举既有共享关系，不承诺Novel专业页面已经定义。

Conversation列表可以同员工多话题，也可保持同Conversation跨Assignment。每条消息保留发生时范围；新消息前选目标并重新校验引用，不能把当前筛选当访问许可。切Business时停留当前执行任务并显示其原范围，不能更换运行身份/历史。

| 规模/场景 | 已选定的表达 | 禁止 |
|---|---|---|
| 1 Business / 1 Workspace | Business仍保留四段，可从目录直接[进入工作空间]；返回目标明确 | 消除Business identity |
| 5 Business | Business行可比较目标/真实事项/最近结果；CEO Desk只选真实需关注 | 五个全量Dashboard拼在首页 |
| 20 Business | 搜索、部门/状态筛选、最近使用排序；跨业务比较进Insights | 20常驻Nav节点或全部员工气泡 |
| 1 Account | 单账号经营面，目标仍标账号，内容仍明确Variant | 将账号变Workspace或全局scope |
| 5 Account | 同一专业集合、每账号负责与状态；当前账号Header明确 | 五套分析/连接/资料系统 |
| 20 Account | 搜索/平台/需处理筛选、表格比较发布；当前Work先5条再展开 | 全部账号的历史同时进入员工上下文 |
| 同账号多个经营关系 | 先选本次真实Workspace和责任；查询聚合可见但执行目标单义 | 静默搬迁历史或同一次任务多处重复发布 |
| 无权范围 | 保留可见标题策略遵守权限，敏感字段不加载；[返回原范围] | 以同员工服务过为由读取所有内容 |

所有切换继承R。筛选条件是个人视图，不是策略、授权或新的Account Owner。跨范围拖拽首版只支持合法Reference添加，不拖动对象来迁移归属；真正归属变更在组织/绑定编辑明确确认。

## 36. Full Surface Map

这是同一规格的索引，不是第二Page Map Authority。U编号只用于本稿交叉引用，不是Route或Schema。首次进入采用下表默认；从既有工作返回采用R。选中对象的组件行为以对应正文为准。

| ID | Surface / 类型 | 首次Main | 对象入口 / 返回原则 |
|---|---|---|---|
| U10 | Global Navigation | Nav Header原生窗口控制/搜索/T1 → 七区固定顺序 → bounded最近对话 → 底部通知与CEO头像；Main由目标区接管 | 应用主窗口；每个Surface共用；区间切换恢复各区最后浏览；同对话重新打开恢复同identity |
| U11 | CEO Desk | 公司Header → Return Summary一句概况 → 需要你处理的事项行 → 值得注意的Business行 → 重要Result引用行 | 首次打开/点击CEO工作台/处理完成返回；处理后[返回CEO工作台]恢复事项位置，并显示真实已处理状态；失败留在原事项 |
| U12 | Business Space | Header“业务空间”+[开始一项业务] → Segmented“部门 / 业务 / 工作空间”（首次业务） → 搜索/状态筛选 → 对应摘要行 | 全局业务空间/CEO Desk业务入口；从目录进入对象后Back恢复Segment、筛选和行；创建取消回目录原状态 |
| U13 | Business Operating | 四段连续：Business Definition紧凑Header/目标/Leader入口 → Operating Status业务重点/事项/重要结果 → Workspace Directory摘要行 → Business Team轻量责任行 | U12业务行/CEO异常/组织版图Business/搜索；进入Workspace/Conversation/Insights均保留业务From；返回恢复四段滚动位置 |
| U14 | Workspace | Header身份/Leader → 当前选中专业面 → 相关Shared Work Area；Generic经营默认Goal简述/本轮重点/最新判断/下一步→实际Work行→最新Result | U12工作空间/U13目录/深链；Domain切换记住各面选中对象/滚动；进员工/结果后回原面，收Pane不停止Work |
| U15 | Organization Center | Header公司/组织摘要 → 公司版图或员工目录；默认展示原装部门和真实用户Business，业务可0 | 全局组织中心/缺岗入口/Company结构链接；从缺岗返回原Work时刷新Holder，执行是否继续依真实恢复状态 |
| U16 | Business Map / 公司版图 | 公司Header → 层级Tree；默认展开Department与Business，Workspace与责任按行展开；选中对象仅打开只读摘要Utility | U15公司版图/Company资料入口；进经营返回恢复展开路径和选中；重命名跨区同身份更新 |
| U17 | Employee Directory | Header“员工”+[创建员工] → Tabs“全部/在岗/未在岗/离职” → 搜索/服务业务筛选 → F02行 | U15员工目录；U19[查看公司已有员工]是跳转不是第二目录；从Utility关闭留原行；从Main Back恢复员工筛选/滚动；创建完成选中新员工 |
| U18 | Employee Detail / Workstation | Main Header F05 → 当前工作/责任摘要 → Conversation → Composer；Utility详情Tabs“资料 / 责任 / 能力 / 记录”，默认资料 | 全产品头像/姓名→Utility；目录[进入工作]→Main；Assignment[讨论]→指定范围Main；从头像打开不离开原Work；进入Main保留来源；切Tab不换scope；换责任仅控制下一消息 |
| U19 | Talent & Capability | Header+[搜索] → 类型/领域筛选 → 简洁候选行（价值一句/来源/适用职责/依赖状态） → 选中详情Utility | 全局人才与能力/缺岗[找人才]/能力缺口；保留来源缺岗/员工目标；招募成功回目标确认Assignment，不能自动覆盖Holder |
| U20 | Capability Binding | 单Drawer：类型→选择能力→连接与检查→权限/范围→默认或可选→影响摘要→保存 | U18能力Tab[添加能力]/U19引入后[绑定给员工]/Work缺口；保存/取消回原员工能力Tab或Work缺口；Settings返回恢复绑定草稿；升级许可被拒不丢原配置 |
| U21 | Operating Intelligence | 范围与周期Header → 数据完整性提示 → 目标相关指标行/语义图表 → 分析报告列表；选报告Reading Main | 全局经营洞察/业务[查看经营分析]/Result追问；从业务进入保留From/期间；报告→Conversation→新报告可回旧版本；Evidence关闭回同报告段 |
| U22 | Knowledge Library / 资料库 | 概览最近使用/需核对来源→浏览F09列表；点击正文进入Reading Main：标题/来源/适用范围/版本→正文→Used By | 全局资料库/Composer添加引用/结果知识候选；从Work选择引用完成后回原Composer草稿；阅读→Used By→原Work；返回保留资料筛选/阅读位置 |
| U23 | Meetings | 列表F08；会议Main Header议题/范围/参与者/状态 → 当前议题与未决摘要 → 参与员工自然Conversation → Composer | 全局会议/Business或Work[发起讨论会议]/Assistant建议；离开不结束会议；Back恢复话题位置；Follow-up Work→Result→返回原会议跟进Tab |
| U24 | Conversation / Work | F05 Header → 当前Work摘要/真实待处理Banner → 消息流 → Shared Composer；进展在对应工作消息内，不另建后台面板 | Leader [讨论]/员工[进入工作]/Work行/Quick Access；主对话离开保存草稿/滚动锚点；切范围不清历史；结果关闭回对应消息；工作历史重开同identity |
| U25 | Decision | 原Working Main的P7 Detail：问题与为何需CEO→推荐与理由→可选方案/代价/风险→选择后继续方式→动作；Utility证据 | CEO Desk/原Work/Meeting的P7 Banner；完成返回原Work继续状态或CEO来源；无需另建对话/Handoff；Evidence回同方案选项 |
| U26 | Human Handoff | 原Work Main内F07动作包 → 已准备内容/必要说明 → 外部入口 → 完成报告/核对结果 → 继续条件 | 原Work提示/CEO Desk/通知[继续处理]；外部回来原Work，不强制跳CEO首页；从通知进入仍能返回原通知清单；恢复自动按已有授权继续 |
| U27 | Result / Evidence / Learning | Utility：F04 Header/版本与接受状态→一句结论→输出预览→证据列表→后续动作；长读[maximize]；Evidence替换同Utility并有内部Back | Work/CEO Desk/员工/Meeting/Library结果引用；最大化退出恢复原Utility大小与Main滚动；Evidence内部返回保留Result版本；继续讨论回Main并引用当前版本 |
| U28 | Settings / Connections | Settings Main类别Header→设置行/连接列表；连接Detail同Main：F18→可用能力与范围→使用者→维护动作 | CEO头像[设置]/Work[连接服务]/U20连接步骤；[返回〈员工/Work〉]恢复草稿；无From回原一级区；换主题不重置业务Context |
| U29 | Global CEO Assistant | 收起形态身份/真实待处理提示；展开浮层Header身份/收起→简短对话→Context提示→Shared Composer；复杂工作跳原Main | 全局浮动入口/已有Assistant展开状态；收起恢复原Main焦点；打开专业面后浮层仍同identity但可收起；返回不重发委托 |
| U30 | Content Growth Domain | 默认经营面：当前目标/本轮重点/最新判断/下一步 → 真实待处理 → 值得注意账号行 → 当前内容Work行 → 最新结果引用 | 已启用Content Growth业务→具体Workspace；不是默认新公司业务；Account/内容/发布面切换恢复对象选择，Workspace不变；数据分析后回原账号/内容 |
| U31 | Content Growth Account Operating | Header F11/Goal一句 → 当前经营（Strategy一句/本轮重点/下一步） → 需你处理（有才出现） → 当前内容与Work行 → 最近表现与Result摘要；无八Tab | U30账号行/U13引用异常/Search；从20账号选中A后打开内容/报告返回仍A、原筛选与滚动；改连接不丢账号长期历史 |
| U32 | Content / Variant | Intent Header标题/目的/目标账号 → per-account Variant比较表 → 选中Variant Main Editor；规格与引用Utility | U30内容/U31内容行/生产Work Result；编辑/预览/Conversation回同Variant修订与滚动；换账号前脏草稿处理，不将A正文带到B |
| U33 | Publishing | Header范围/计划摘要 → 目标执行表（账号/修订/审核/能力/计划时间/状态/下一动作） → 选中记录详情/真实回执Timeline | U32 [准备发布]/U30发布/账号状态；手机/浏览器返回原Publication/Work；查询成功同步账号/Variant/Work投影；已发布记录不可因页面返回重发 |
| U34 | Analytics / Content Growth | 范围/周期Header → 数据覆盖说明 → F13指标/趋势 → 相关Publication表 → 分析解释/未知/Learning → 原Work与证据 | U31/U30 [查看经营分析]/发布回执的表现入口；报告/证据/讨论后回原账号、期间与筛选；数据修正追加记录不改平台原始事实 |
| U10-S | Global Search / overlay | 查询→分组结果→范围与键盘提示 | Nav搜索；关闭回触发点；选结果保留Search query |
| U10-N | Notification / Drawer | 待处理/更新Tab→事项行 | 底部通知；继续处理去原Work；读回执不接受结果 |
| U12-C | Business Creation / Guided Main | 意图→经营提案→准备与启用 | Assistant/业务空间；取消回From，保留草稿；创建成功进首空间 |
| U12-D | Business/Workspace Copy / Guided Main | 复用/重新确认/不复制→确认 | 原对象More；返回源对象；新对象独立identity |
| U17-C | Employee Create/Copy / Drawer | 身份→职责→可复用能力→确认 | 目录/人才；成功回目录新行，无历史复制 |
| U14-T | Team Operating / Main | 顺序责任表→改动影响→保存新版本 | Workspace[查看团队运转]；回原专业面 |
| U16-D | Department Operating / Main | 职责/Leader→跨业务事项→Business目录→责任摘要 | 公司版图/业务空间部门视角；回原树或目录 |

不额外增加“平台管理中心、人工执行中心、员工能力第二目录、独立学习中心”。Policy、Template、Artifact、Source是资料类型和来源关系；Publication/Account是Domain对象；全局Settings与搜索不是第八区。

## 37. Interaction Matrix

以下矩阵决定重要交互的具体实现形式，字段采用F合同。N0/N1/N2/N3与R见§7；G见§8。所有保存失败保留草稿，所有改变业务事实的成功要有真实持久化/回执；本稿不把它们宣称已实现。

| ID / From → Action | 形式 / To | 编辑或显示字段 | 提交后状态 / 对象副产物 | Context / Back |
|---|---|---|---|---|
| I01 U11/U12/Assistant→开始一项业务 | Guided Main U12-C | 意图/参考→F17 | 可保存提案；委托准备才形成建设Work；创建为真实Business+首空间，未就绪明确 | N1→N3；取消回From |
| I02 U13/U14→改名 | Inline | 名称必填 | [保存]同identity新显示名；无新Work/员工 | N0；Esc还原当前编辑 |
| I03 Goal→调整目标 | Utility读原值→Drawer提案→P7 | 目标/成功标准/检查点/范围/影响 | [提交目标修订]形成待确认提案；CEO明确接受才生效；不把草稿当新目标 | N0→N3；回对象摘要/原版本 |
| I04 Strategy→讨论打法 | Conversation Main U24 | 原策略版本/范围/问题 | [发送]消息；需要产出则原责任Work；普通战术在授权内，受保护策略P7 | N2/N3；回原Strategy位置 |
| I05 U13→精确修改规则 | Drawer | Title/Content/作用范围/变化原因 | 保存为修订提案；按权限接受后生效，不变各Workspace独立策略 | N0/N3；回规则Utility |
| I06 业务/空间→暂停经营 | Modal，复杂影响Main | 目标范围/未完责任/已提交外部动作/可恢复方式 | [确认暂停经营]请求暂停，回执前“正在请求暂停”；不取消已发布 | N3；回原面保留部分失败 |
| I07 已暂停→恢复经营 | Main轻量影响摘要 | 当前目标/责任/连接变化/未完事项 | [恢复经营]校验授权后恢复原系列；终止系列需新决定，不伪Resume | N3；回原经营摘要 |
| I08 原对象More→归档 | Modal或复杂转移Main | 对象/影响/未完承诺/保留历史 | [确认归档]可追溯；未交接责任时Blocked；不删除数据 | N3；回来源集合保留筛选 |
| I09 U12/U13→复制 | Guided Main U12-D | 新名称/目标/重新绑定/复用与禁止项 | [确认复制]新identity；失败查原请求；无秘密/历史复制 | N1/N3；回源或进入新对象 |
| I10 全局头像姓名→员工详情 | Utility U18 | 资料/责任/能力/记录四Tab | 阅读无Work，编辑Drawer同identity | N0；T3恢复原Main |
| I11 Employee→进入工作/责任讨论 | Main U24 | F05 + 目标Assignment | 打开同Conversation或新话题；读取不自动派工作 | N1/N2；回原员工行/责任 |
| I12 U17→创建/复制员工 | Drawer U17-C | 姓名/职责/可选能力/来源 | [创建员工]新identity；无Key可存在；不自动执行 | N3；回目录新行 |
| I13 责任→安排/换Holder | Drawer，复杂转移Main | F15、候选资格/当前Work/新安排影响 | [保存责任安排]更新Assignment；在途工作固定原身份，必要acknowledged交接 | N3；回缺岗原对象 |
| I14 Employee→添加能力 | Drawer U20 | 类型/用途/资源/连接/权限/默认 | [保存能力]绑定；待配置与可用分开；无新员工/执行 | N0/N3；回能力Tab |
| I15 能力→连接服务 | Settings Main+连接Drawer | F18/适配器必要安全输入/授权范围 | [连接并检查]有事实才可用；未授权Blocked；不抄秘密进聊天 | N1/N3；回原绑定草稿 |
| I16 连接→撤销连接 | Modal | 受影响员工/业务/进行工作/权限撤销 | [撤销连接]确认后断开；未知结果核对；保留历史 | N3；回连接详情及原缺口 |
| I17 U24→发送/补充 | Main Composer | 文字/合法Reference/附件/目标范围 | 发送成功保留message；可形成Work，已接收超时先核对；补充有送达反馈 | N2/N3；留原对话 |
| I18 U24→停止当前执行 | 原Work内确认（有外部动作先影响Modal） | 明确当前执行/在途动作/不能撤回项 | [确认停止]仅请求，回执前不标Stopped；不关Business | N3；留原Work，草稿保留 |
| I19 U24失败→继续/重试 | 原Main | 已保存结果/失败点/可恢复范围 | 支持原执行恢复则恢复；新执行明确“重新安排”并链接旧Work | N3；留原Work或显式新Work |
| I20 P7→选择方案 | Main Detail；必要最终Modal | P7八语义/方案版本/风险来源 | 同Decision记录接受/拒绝/暂缓，原责任自动继续；无新Conversation/Handoff | N3；回原Work/CEO Desk |
| I21 Handoff→前往平台 | 外部浏览器/手机/系统授权 | 账号/动作/准备内容/完成判据 | 外跳不算完成；授权与支付仍独立边界 | N0；保留Curis原Work |
| I22 Handoff→我已完成 | 原Work动作包 | 用户报告及必要证据 | 已报告→核对→确认或未知；确认后原Work继续，不假自动结果 | N3；留原Work或回CEO事项 |
| I23 Result→查看依据 | Utility/内部Back/maximize | 当前版本/来源/时效/正文 | Viewed单独记录，未接受；读取失败保留引用 | N0；回同Result/消息 |
| I24 Result→接受/要求修改 | 当前Result动作+必要确认 | 版本/范围/接受后果/修改说明 | 接受真实版本；需修改形成后续责任，不改旧Result | N3；回原Work |
| I25 Learning→应用建议 | Drawer差异→必要P7 | 适用对象/证据/原规则/拟变更 | 已采用须真实变更链接；未落地仍建议；不建Learning真源 | N3；回报告/Review |
| I26 Insights→追问 | Main Conversation | 报告版本/范围/周期/问题 | message/Analysis Work/新报告，不改旧事实 | N1/N2/N3；回原报告 |
| I27 Library→添加/引用 | 添加Drawer；引用overlay | 类型/来源/适用范围；选择版本 | 导入真实Reference；[添加引用]只改草稿Context，Send才提交 | N0/N3；回原阅读或Composer |
| I28 Meeting→创建/跟进 | Drawer→Working Main | 标题/议题/参与者/范围/资料 | 建Meeting；决定后生成合法Work引用；离开不结束 | N1/N3；回原来源 |
| I29 U31→接入账号 | Drawer→必要Settings | 平台/真实账号/连接/Workspace/目标/责任 | 保存绑定不发布不创建Workspace；身份待核验不能假成功 | N3；回账号集合 |
| I30 Intent→生产Variant | Drawer意图→Main Work/Editor | 意图/目标账号/规格/账号Context | 保存意图与派Work分开；产生每账号Variant | N3；回原Intent |
| I31 Variant→编辑/审核 | Main Editor→审核Work/P7 | 具体修订/内容/媒体/规格/审核范围 | [保存此账号版本]新修订；审核状态重新核对；不改发布版 | N3；回同Variant |
| I32 定稿→准备/执行发布 | Publishing Main U33 | 目标表/时间时区/版本/权限/分发政策 | 每账号Publication回执；成功/等待/失败独立；无总假成功 | N3；回账号或Intent |
| I33 发布未知→核对结果 | 原Publication Main | 原提交/账号/平台回执 | 查询/人工证据更新状态；未确认绝不重复发布 | N3查询；留原记录 |
| I34 Analytics→补充数据 | Drawer | 账号/指标/单位/期间/值/来源 | 追加manual记录，空不是0；新报告消费，不改原始平台数据 | N3；回同期间 |
| I35 内容/资料→拖入Composer | Reference预览行 | 对象/版本/可用scope | 只加合法引用；无迁移/复制对象；不支持文件给原因 | N0；留草稿 |
| I36 长文编辑→离开 | Modal | 草稿对象/未保存状态 | [保留草稿后离开]/[放弃修改]/[继续编辑]；不静默丢失 | R恢复草稿，不自动提交 |

### 危险动作词义必须分开

- **Archive / 归档**：从活跃集合移出，历史可查；不默认终止承诺。可恢复时提供[恢复到活跃]，无能力不能承诺。
- **Delete / 删除**：确切对象与不可逆范围明确，影响引用列出；不可逆以[永久删除〈对象〉]确认，必要输入对象名称，不要求所有小动作都输入确认。没有产品授权不展示删除Company/原装组织的可用按钮。
- **Disconnect / 撤销连接**：撤授权及未来可用能力，不删Employee/历史；共用连接需显示全部影响者。
- **Stop / 停止当前执行**：请求结束指定执行，不取消平台已经产生的副作用，也不等于归档Business。
- **Cancel / 取消编辑/计划**：取消编辑不写入；取消未执行计划不影响已执行结果；取消平台已接收操作是另一动作，依真实能力。
- **Pause / 暂停经营**：保存持续责任并等待显式恢复；**结束本次经营责任**为另一个需明确终止影响的决定，不能用Stop icon模糊替代。

## 38. Component / Pattern Map

| Pattern | 字段 / 表达合同 | 使用Surface | Interaction | State / 不可变边界 |
|---|---|---|---|---|
| Pane Header | 当前对象/Breadcrumb、T1–T3条件位置、More | 全Shell | N0开合；R返回；Utility maximize | 无重复✕，开合不停止执行 |
| Scoped Object Header | 名称/类型/最短范围/当前状态 | Business/Workspace/Account/Work | 标题不编辑scope；改名I02 | unknown有文字 |
| Summary Row | F01/F02/F03/F08/F10/F11 | U11–18/23/30–31 | 标题Main，头像Utility | 不整行一键执行 |
| Goal Summary | F16，一句+展开 | U13/14/31 | I03/I04 | 草稿/待确认/已生效分开 |
| Current Operating | 本轮重点/最新判断/下一步；真实Need | U14/30/31 | Work/Result/Decision链接 | 无虚构进度/健康分 |
| Attention Item | F06/F07问题/范围/下一动作 | U10-N/U11/原Work | I20–22 | 阅读不完成 |
| Employee Presence | 头像/名/当前责任，另显[工作过程] | 业务对象/Work | 头像I10，过程I11 | 身份与Executor不混 |
| Assignment Row | F15范围/责任/Holder | U15–18/14-T | I13 | 缺岗是事实，不创建假员工 |
| Shared Composer | Context/Reference/附件/输入/动作行 | U23/24/29 | I17/I35 | IME/禁重发/中断/失败保草稿 |
| Message Block | 身份/内容/范围来源/引用/状态 | U23/24/29 | 展开阅读/引用补充 | 历史不可改写 |
| Work Progress | F03/真实活动/当前阻碍 | U24/专业Work | I18/I19 | tool详情折叠，无猜测百分比 |
| P7 Package | F06八语义/分层来源 | U25 | I20 | 高风险不Banner一键批准 |
| Human Action Package | F07动作/准备/回收判据 | U26 | I21/I22 | 报告完成≠核验成功 |
| Result Reference / Reader | F04/版本/输出/依据 | U27 | I23–25 | 原scope，Viewed≠Accepted |
| Source / Used By | F09/来源/使用范围/引用 | U22/27 | I27 | 不复制Source与Result真源 |
| Capability Binding Editor | F14/权限/用途/连接 | U20 | I14–16 | 配置≠可用≠执行 |
| Metrics / Report | F13/事实解释未知建议 | U21/34 | I26/I34 | 数据缺失不填0 |
| Variant Comparison | F12/账号/修订/各状态 | U32/33 | I30–33 | 不静默跨账号修改 |
| Guided Proposal | F17/可复用/缺口/后果 | U12-C/D | I01/I09 | 创建不等启用成功 |
| Search Result | 标题/类型/合法范围 | U10-S/局部选择器 | 选中→打开→R | 同源对象，不是答案引擎 |

组件复用指语义和行为，不要求所有专业页面视觉相同。Material编辑器、图表、Timeline不能只换标题便当另一Domain；未明确的新专业组件由独立域规格补齐，本稿共享能力不为其伪装。

## 39. Four-Pane Mapping

继承S07：Pane-local Header、T1/T2/T3原位置、默认Nav+Main、Utility maximize Overlay。表中Left/Right内容都是“可用时”，不是常驻列数；默认除局部导航必需且用户打开外均收起。Assistant一列仅说明可达，不预留宽度。

| Surface | Navigation | Left Context | Main | Right Utility | Assistant |
|---|---|---|---|---|---|
| U10 Global Navigation | 七区当前区 | 由当前Surface声明；Global层不放永久员工树 | Nav Header原生窗口控制/搜索/T1 → 七区固定顺序 → bounded最近对话 → 底部通知与CEO头像；Main由目标区接管 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U11 CEO Desk | CEO工作台 | 默认收起；展开是“今天/上次离开后”的阅读区间及已处理记录入口，不放业务树 | 公司Header → Return Summary一句概况 → 需要你处理的事项行 → 值得注意的Business行 → 重要Result引用行 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U12 Business Space | 业务空间 | 默认收起；展开提供部门过滤及最近使用对象 | Header“业务空间”+[开始一项业务] → Segmented“部门 / 业务 / 工作空间”（首次业务） → 搜索/状态筛选 → 对应摘要行 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U13 Business Operating | 业务空间 | 默认收起；展开是本Business空间目录，不显示全部员工 | 四段连续：Business Definition紧凑Header/目标/Leader入口 → Operating Status业务重点/事项/重要结果 → Workspace Directory摘要行 → Business Team轻量责任行 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U14 Workspace | 业务空间 | 本Workspace身份 + Domain Navigation；Generic固定“经营 / 工作 / 结果 / 团队”；Professional使用批准的域导航 | Header身份/Leader → 当前选中专业面 → 相关Shared Work Area；Generic经营默认Goal简述/本轮重点/最新判断/下一步→实际Work行→最新Result | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U15 Organization Center | 组织中心 | “公司版图 / 员工目录”两稳定子面；首次公司版图 | Header公司/组织摘要 → 公司版图或员工目录；默认展示原装部门和真实用户Business，业务可0 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U16 Business Map / 公司版图 | 组织中心 | 沿用U15子面；可收起 | 公司Header → 层级Tree；默认展开Department与Business，Workspace与责任按行展开；选中对象仅打开只读摘要Utility | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U17 Employee Directory | 组织中心 | U15公司版图/员工目录 | Header“员工”+[创建员工] → Tabs“全部/在岗/未在岗/离职” → 搜索/服务业务筛选 → F02行 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U18 Employee Detail / Workstation | 来源区；独立进入时组织中心 | Main打开时列此员工最近话题，按最后活动；不是所有工作空间知识树 | Main Header F05 → 当前工作/责任摘要 → Conversation → Composer；Utility详情Tabs“资料 / 责任 / 能力 / 记录”，默认资料 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U19 Talent & Capability | 人才与能力 | 发现分类“专家 / 技能 / 连接器 / 职业模板”；首次专家 | Header+[搜索] → 类型/领域筛选 → 简洁候选行（价值一句/来源/适用职责/依赖状态） → 选中详情Utility | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U20 Capability Binding | 保持原区 | 不新增Context；背景保持员工/原Work | 单Drawer：类型→选择能力→连接与检查→权限/范围→默认或可选→影响摘要→保存 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U21 Operating Intelligence | 经营洞察 | 公司经营 / 业务分析 / 组织与员工 / 模型与能力 / 分析报告 / 专项研究 | 范围与周期Header → 数据完整性提示 → 目标相关指标行/语义图表 → 分析报告列表；选报告Reading Main | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U22 Knowledge Library / 资料库 | 资料库 | 概览 / 浏览；浏览下类型过滤“来源/参考/成果文件/模板/知识/规则”，是分类非独立系统 | 概览最近使用/需核对来源→浏览F09列表；点击正文进入Reading Main：标题/来源/适用范围/版本→正文→Used By | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U23 Meetings | 会议 | 会议集合：进行中 / 已结束；当前会议可切“讨论/决定与跟进”两个Main Tab | 列表F08；会议Main Header议题/范围/参与者/状态 → 当前议题与未决摘要 → 参与员工自然Conversation → Composer | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U24 Conversation / Work | 保留来源七区；不是第八区 | 当前员工/工作的近期话题与有限引用导航；可收起 | F05 Header → 当前Work摘要/真实待处理Banner → 消息流 → Shared Composer；进展在对应工作消息内，不另建后台面板 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U25 Decision | 保留来源区 | 继承原Work/Meeting Context | 原Working Main的P7 Detail：问题与为何需CEO→推荐与理由→可选方案/代价/风险→选择后继续方式→动作；Utility证据 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U26 Human Handoff | 保留来源区 | 原Work Context；不新建人工操作中心 | 原Work Main内F07动作包 → 已准备内容/必要说明 → 外部入口 → 完成报告/核对结果 → 继续条件 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U27 Result / Evidence / Learning | 保留来源区 | 保持原来源，不另建结果中心 | Utility：F04 Header/版本与接受状态→一句结论→输出预览→证据列表→后续动作；长读[maximize]；Evidence替换同Utility并有内部Back | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U28 Settings / Connections | 来源区保留高亮；从头像打开 | 个人与外观 / 公司设置 / 模型与AI / 权限与安全 / 应用与数据 / 账户与帮助 | Settings Main类别Header→设置行/连接列表；连接Detail同Main：F18→可用能力与范围→使用者→维护动作 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U29 Global CEO Assistant | 跨七区全局浮层 | 无专属Pane | 收起形态身份/真实待处理提示；展开浮层Header身份/收起→简短对话→Context提示→Shared Composer；复杂工作跳原Main | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U30 Content Growth Domain | 业务空间 | 经营 / 账号 / 内容 / 发布；数据入口到scoped经营洞察；团队入口复用U14 | 默认经营面：当前目标/本轮重点/最新判断/下一步 → 真实待处理 → 值得注意账号行 → 当前内容Work行 → 最新结果引用 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U31 Content Growth Account Operating | 业务空间 | 本Workspace Domain导航；账号集合可展开并搜索/平台筛选，不强迫经过平台页 | Header F11/Goal一句 → 当前经营（Strategy一句/本轮重点/下一步） → 需你处理（有才出现） → 当前内容与Work行 → 最近表现与Result摘要；无八Tab | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U32 Content / Variant | 业务空间 | 内容集合/当前Intent；保留Workspace导航，可收起 | Intent Header标题/目的/目标账号 → per-account Variant比较表 → 选中Variant Main Editor；规格与引用Utility | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U33 Publishing | 业务空间 | 本Workspace发布集合，当前Intent或账号筛选 | Header范围/计划摘要 → 目标执行表（账号/修订/审核/能力/计划时间/状态/下一动作） → 选中记录详情/真实回执Timeline | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U34 Analytics / Content Growth | 经营洞察（从账号带范围进入） | U21业务分析，原账号范围保留 | 范围/周期Header → 数据覆盖说明 → F13指标/趋势 → 相关Publication表 → 分析解释/未知/Learning → 原Work与证据 | 对象详情/Evidence，默认收起 | 同一全局浮层，可收起，不占Pane |
| U12-C/D 创建/复制 | 业务空间 | 当前提案步骤 | 长提案/影响预览/准备状态 | 来源与方案依据 | 同一浮层 |
| U14-T 团队运转 | 业务空间 | 当前Workspace导航 | 顺序责任表/变更预览 | 责任说明/旧版 | 同一浮层 |
| U16-D 部门经营 | 业务空间 | 本部门Business目录 | 职责/跨业务事项/目录/摘要 | 员工身份/证据 | 同一浮层 |

宽度不足时先收Utility，再收Context，保Main可工作；已有Utility内容保留可再次打开。Main与Utility各有自己的阅读滚动；嵌套长消息只在bounded内容块内滚动，普通Section不各开小滚动框。Drawer/modal覆盖时锁背景交互并保滚动，退出恢复焦点。具体断点/尺寸留DO，但不能以窄屏为由把Conversation搬到Utility。没有可用Context时T2仍按Shell位置保留，禁用并用Hover/Focus说明“当前没有辅助导航”；不展开空栏。Utility无对象时T3按条件显示规则处理，不保留空占位面。

## 40. Product Fixed vs Design Open

| Surface组 | PF-A：已存在关系必须守住 | PF-C：本稿选定，接受后交设计固定 | DO：真正开放 |
|---|---|---|---|
| Global / U10–11 | 七区、Quick Access、CEO Desk非Assistant | 最近10、主页信息顺序、Search/Attention行为、快捷键冲突规则 | Nav密度/图标/提示动效 |
| Business / U12–14 | canonical层级、Business四段、独立Workspace、Team责任 | 创建Guided Main、提案字段/提交后果、列表默认、Generic导航 | Section外观/行高/空间呼吸 |
| Organization / U15–18 | 单Employee、Assignment、目录Owner、头像Utility/工作Main | 公司版图Tree、详情四Tab、创建复制/换责任编辑 | 头像形式/树连线细节/间距 |
| Capability / U19–20/28 | 发现≠公司员工、绑定真源、权限可撤 | Drawer绑定/Settings连接/类型/默认规则 | 设置分隔、表单宽度、状态视觉 |
| Insights / U21/34 | 原事实来源/Analyst责任/不建第二Truth | 数据覆盖先于图表、报告结构/比较/补录/追问 | 图表配色/网格/表格密度 |
| Library / U22 | 来源/Reference/Knowledge/Result边界 | 列表→Reading、选择引用/Used By/新版本 | 阅读字号/目录样式/行距 |
| Meeting / U23 | Main讨论/正式Decision/后续Work | 两Tab、会议创建字段/结束语义 | 参与者摘要样式/消息节奏 |
| Conversation / U24/29 | same identity、消息scope、Shared Composer；Assistant不占Pane | Enter/ShiftEnter、草稿恢复、Steering反馈、Stop明确对象 | 气泡或非气泡/字体/Composer几何；不得变更字段层次与动作 |
| Decision/Handoff / U25–26 | P7八语义、Decision非责任转移、核验后恢复 | 原Main动作包、具体按钮/失败分支/返回 | 卡片造型/强调级别/过渡 |
| Result / U27 | 可追证据/Viewed≠Accepted/原scope | Utility→maximize/内部Back、版本固定、接受与Learning | 阅读布局微调/文件预览视觉 |
| Content / U30–33 | Account≠Workspace、每账号Variant/Publication、Provider不替员工 | 域导航、Account Section顺序、Main Editor、逐目标表格 | 预览比例/媒体表现/状态样式 |

兼容性检查结果：本稿沿当前七区、四层scope、Shell/P7与Employee模型可安放，**不需要改变Frozen产品关系**。S12若被读成Business用独立的域Dashboard取代四段，按U13修正；人才页若被理解为第二员工目录，按U17/U19修正；全局搜索不偷偷扩大成Reserved Command Palette。无新增PRODUCT AUTHORITY CHALLENGE。

视觉稿可以废弃，但Frozen Header/Toggle行为不能因旧稿同时出现过而一并废弃。圆角/色值/字体等最终仍须消费届时正式Visual Authority；本稿的DO不是授权覆盖既有视觉规则。未采用任何旧Prototype布局、像素或截图作为本稿答案。

## 41. UI-readiness Review

**审查标准是“设计师还需不需要补产品决策”，不是运行产品验收。** 每个主Surface均有Purpose/Entry/Context/Layout/字段/组件/主次动作/编辑/状态/返回/规模/PF/DO，重要动作八种表达形式已比较并选定；§37给具体按钮与副产物，附录A走12条完整链。

| 检查 | 本稿闭合证据 | 判定 |
|---|---|---|
| 七区首次进入可画 | U10–23及地图，每区默认Main/Left/CTA/对象去向 | PASS（规格） |
| 全局辅助能力 | 搜索/Quick Access/通知/Avatar/Settings/Assistant | PASS（规格） |
| 业务从意图到经营 | U12-C、U13–14、I01及模拟1/3 | PASS（规格） |
| 字段与组件无需设计师发明 | F01–18、各面Required/Optional、组件图 | PASS（规格） |
| 编辑/保存/取消/失败 | §6、G、I01–36；具体对象状态覆盖 | PASS（规格） |
| 跨范围/跨员工/返回 | N0–N3、R、U18/24/35、模拟5 | PASS（规格） |
| 人工/平台失败/数据未知 | U26/33/34、模拟7/11/12 | PASS（规格） |
| Result→Evidence→Learning | U27、I23–26、模拟8 | PASS（规格） |
| Content Growth完整表达 | U30–34及模拟9/10；复用S12能力Owner | PASS（规格） |
| 无静默Authority修改 | §40及来源hash校验 | PASS（文档边界） |
| 真实用户交互与可发现性 | 未制作/运行新UI；设计阶段验证 | NOT TESTED，不冒充通过 |
| Provider/Runtime真实能力 | 本轮不实现/不实发，按既有缺口设计诚实状态 | NOT RE-ACCEPTED |

**FULL PRODUCT EXPRESSION READY FOR UI — SPECIFICATION CANDIDATE ONLY。** 表达已给确定答案，可以交CEO作整体接受/修订；这不等于获准开始画图。本轮可画的范围是全产品共享链与Content Growth实例，未知Domain的专业内部仍不虚构。CEO确认后必须先CURIS PRODUCT BLUEPRINT RECONCILIATION，唯一Blueprint正式更新再消费Blueprint+本规格进入设计，并遵守已有Design Gate。不能跳过此顺序。

## 42. Remaining Product Expression Gaps

本次指定共享范围与Content Growth主链，没有留下“选Drawer还是Main、字段放哪里、按钮叫什么”给设计师决定。剩余事项区分如下，不能混成一个笼统Ready：

1. **CEO接受与正式对账（下一Gate，不是DO）**：确认PF-C默认交互/字段；唯一Blueprint吸收已确认新定义、Global/Business/Content Growth/Product Expression。用户要求这一轮结束后再做，因此本轮不代写、不自动批准。
2. **实现证据缺口**：Codex适配器可用性、Provider实际执行/查询、原工作恢复、OS通知、权限与引用细粒度、数据时效等必须用真实实现验收。其不可用UI已经定义，不能把图里有按钮当已实现。
3. **专业领域扩展**：小说、电商等只以真实Generic与共享责任链承载。本稿不宣称它们专业内容编辑/订单/支付链已可画；想启用其专业产品需独立领域表达，不复用Content Growth强塞。
4. **视觉与可用性验证（DO）**：字体、颜色、间距、响应断点、动效与密度；用1/5/20对象、长中文、Keyboard、失败与返回验证。不得借视觉验证重定义Owner或隐去Unknown。
5. **明确排除首版**：Command Palette/高级查询、多真人协作、统一钱包/商业订单后台、任意流程图、跨Company管理、新学习中心。不拿这些Future填充当前导航。

Owner: CEO / Product Review。Disposition: 提交本规格整体Review；原V1/V2与Frozen来源保留。Next Action: CEO接受或指出需修订PF-C；Next Gate: **CURIS PRODUCT BLUEPRINT RECONCILIATION**。之后再确认UI Design Gate。本轮没有授权或执行Blueprint更新。

# 附录A. 十二条完整模拟

以下是**产品合同走查**，不是用虚构业务数据冒充实际产品测试。每步给当前所见、按钮、组件、目标、范围变化和返回。正常链中的“可用/成功”均以真实能力与回执为条件；否则转G/对应失败分支。按钮不因示例而自动触发真实外部行为。

## 模拟 1. CEO创建新Business

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U11：公司身份、真实原装团队、暂无业务 | [开始一项业务] / Button | U12-C Guided Main，不弹小Modal | Company浏览→提案；取消回工作台 |
| 2 | U12-C：想经营什么/参考输入 | 输入目标，[继续] / 多行输入 | 读取Company已有业务建议 | 不创建Business；Back保留输入 |
| 3 | 提案准备：已有相近业务或新建建议 | [使用现有业务]或[仍创建新业务] / 选项 | 明确复用或新建；需研究[请空间工程团队准备方案] | 委托为真实Company/Department建设Work，无假Workspace |
| 4 | U12-C：F17提案、Goal、成功标准、首空间、团队、能力缺口 | [讨论打法] / Main Conversation入口 | 同来源建设员工Conversation；[发送]补充方案 | 消息有建设范围；返回同提案版本 |
| 5 | 提案：Name/目标/Department/空间/Leader推荐 | [修改提案] / Drawer | 精确字段编辑，[保存提案]仅更新候选 | 不改变已存在业务；关Drawer回提案 |
| 6 | 提案：明确受保护目标/预算/权限及未知 | [查看方案] / P7 Main | 需要时CEO接受高影响边界；已有明确授权不重复 | Decision原scope，不新建Handoff |
| 7 | 最终提案：真实父关系、首空间名、缺口 | [创建业务与首个工作空间] / Primary | 校验并提交结构创建，按钮处理中禁重入 | 成功新Business+首Workspace；失败留草稿 |
| 8 | 创建结果：两个真实对象链接、团队/模型待准备 | [进入工作空间] / Button | U14 Generic或真实专业候选；不写已全自动 | Workspace浏览scope；返回新业务目录 |
| 9 | U14：Goal/Leader/缺岗/连接状态 | [安排负责人] / Drawer；[完成设置] / Settings | 合法Assignment和能力配置，保存返回；暂无模型可停准备 | 不假绑定；不重建空间 |
| 10 | U14：本轮建议/范围/输出/边界 | [和工作空间负责人讨论] / Main | Leader形成有限First Plan；已授权范围可执行 | Work属于真实Workspace；返回原经营面 |
| 11 | U24：计划/当前员工/动作/等待 | [查看工作] / Work Main | 展示执行与实际结果；失败转原责任恢复 | 不离开就不应阻断；Back原面 |
| 12 | U27：交付版本/证据/待接受 | [查看依据]、[接受结果] / Utility与动作 | Review记录，Leader判断Continue/Adjust或Wait | Result原scope；回本轮 |
| 13 | U14：本轮结束/判断/下一步 | [查看下一轮] / 链接 | 只有有授权且Continue/Adjust才创建一次下一Cycle | Cycle结束不终止Business；回CEO工作台可见真摘要 |

走查判据：拒绝方案/创建失败/没有模型都有明确停留点。创建、启用、执行成功三层不混；首Workspace存在不保证专业能力。

## 模拟 2. CEO每天经营公司

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U11：自上次离开以来摘要/覆盖时间/真实事项 | [查看全部变化] / Inline展开 | 同Main变化行，不新建Dashboard | Company范围不变；[收起]回摘要 |
| 2 | 业务异常行：名称、问题、最近确认时间 | 点击业务标题 / Row | U13对应Business | N1；Back原事项行 |
| 3 | U13：业务目标、整体问题、Leader、相关空间 | [和业务负责人讨论] / Button | U24有Business责任与异常引用 | N2明确Business；回U13 |
| 4 | U24：范围Header/当前问题/建议 | [查看依据] / Result Reference | U27 Utility证据 | N0，聊天不离开 |
| 5 | 证据：来源/时间/未知与现象 | [返回结果] / Utility内部Back | 原建议及版本 | 不换消息scope |
| 6 | U24：P7选项/影响/推荐 | [查看方案]→[选择明确方案] / Main P7 | 接受或暂缓；不要求手工创建每项任务 | 原责任合法继续 |
| 7 | 原Work：Decision已接受、实际恢复状态 | [返回CEO工作台] / 来源返回 | U11原筛选/行，事项按真实状态更新 | 只Viewed的Result仍待接受 |

走查判据：CEO可从证据返回原讨论；做决定只处理该事项；主页不依赖假健康值。

## 模拟 3. CEO进入一个Business

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U12：业务Segment、F01摘要行 | 业务标题 / Row | U13四段Main | 目录状态保留 |
| 2 | U13：紧凑Definition、Goal、Leader；第二段Status | [查看规则] / Text button | Utility只读Title/Content/范围/版本 | N0，仍Business |
| 3 | Utility规则：当前值与来源 | [讨论打法] / Button | U24 Business Leader范围 | 回U13规则位置 |
| 4 | U13：Workspace Directory名称/Leader/事项 | [进入工作空间] / Row | U14对应Domain Main | Business→真实Workspace |
| 5 | U14：专业对象/Current Work | [查看团队运转] / Button | U14-T Main责任顺序表 | 同Workspace，不进组织树 |
| 6 | U14-T：责任/输入/输出/Holder | 责任员工姓名 / Link | U18 Utility身份 | N0；回团队表 |
| 7 | U14：当前专业面 | [返回业务] / Breadcrumb | U13原选中Workspace行 | 恢复原滚动，不显示全部空间任务 |

走查判据：Business四段与专业Workspace并存；团队运转只归Workspace，不在Business生成统一流程。

## 模拟 4. CEO和Leader讨论

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U13或U14：有真实Leader Assignment | [和负责人讨论] / Button | U24同Employee、对应责任scope | Business Leader与Workspace Leader范围不同 |
| 2 | U24 Header：员工/责任/范围/话题 | 输入问题与[添加引用] / Composer | 选择合法当前版本资料 | 旧历史不全量注入 |
| 3 | 引用overlay：搜索/版本/适用范围 | [添加引用]→[发送] | 消息携带引用；必要时责任Work | 发送前草稿可撤销，提交后保历史 |
| 4 | Agent工作消息：当前动作/已确认进展 | [发送补充] / Composer | 显示已送达/排队/不支持中途补充 | 不谎称实时改变当前执行 |
| 5 | 建议Result与来源 | [查看结果] / Reference | Utility可maximize阅读 | 不自动接受 |
| 6 | 策略建议：战术调整或受保护目标 | [应用建议] / 差异Drawer，必要P7 | 有授权范围内改下一轮；重要目标须CEO | 回同Conversation，有真实变更链接 |
| 7 | U24：消息/新结果/后续工作 | [返回工作空间/业务] / 来源返回 | 原Main最新摘要 | 草稿与话题可再开 |

走查判据：讨论是主要形成方式；精确表单用于修订，不让设置表单取代经营判断。

## 模拟 5. 同Employee跨Business工作

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U16：Content Growth与Novel两个Business | 展开责任 / Tree disclosure | 两个Assignment引用同林墨身份 | 只改变浏览 |
| 2 | U17：林墨一行，责任摘要与另1项 | 姓名 / Link | U18 Utility责任Tab | 无第二员工 |
| 3 | 责任Tab：内容审核/Content Growth/空间A | [讨论] / Row action | U24下一消息scope=A | 不加载小说私有资料 |
| 4 | U24：A工作正在进行 | 导航进入Novel / N1 | 浏览B，AWork保持A执行与状态 | Back回AConversation |
| 5 | U18责任Tab：章节编辑/Novel/空间B | [讨论] / Row action | B范围话题或同Conversation范围切换 | 新消息B，旧消息A不重写 |
| 6 | 同Conversation切范围草稿有A引用 | [切换范围] / Popover | 列出不适用引用，移除或取消切换 | 未满足权限不能发送B |
| 7 | 返回Content Growth账号A | [查看工作] / Button | A原Work/Result/话题 | 范围、选中、滚动恢复 |

走查判据：身份唯一、服务关系可多，scope不是权限。Novel仅共享关系示例，不假称其专业产品已完成。

## 模拟 6. 给Employee绑定Codex

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U19人才与能力或U17员工目录 | [查看公司已有员工] / 导航链接 | U17，选择研发员工[进入工作] | 保存来源，人才页不是第二目录 |
| 2 | U18 Utility能力Tab：用途/能力/状态 | [添加能力] / Button | U20单Drawer | 同Employee，不建新Agent员工 |
| 3 | Drawer：类型与用途 | 选择[外部Agent]、搜索Codex / Select+Search | 候选名称/适配器来源/依赖 | 没有候选时未支持，不假装可绑定 |
| 4 | Codex候选：连接状态 | [连接并检查] / Button | 暂存绑定→U28真实适配器连接 | Return目标是同Drawer |
| 5 | Settings：必要安装/授权缺口 | [前往授权]或[打开系统设置] / External | 合法系统流程，Curis不读取显示Secret | 失败/拒绝留待配置，不继续执行 |
| 6 | Settings：实际权限/目录/检查结果 | [检查连接] / Button | 真实检查可用或错误；不以安装代替可用 | 状态Unknown则不得写可执行 |
| 7 | 返回U20：连接可用、所需权限/范围 | 选[默认用于代码工作]或[需要时选择] / Radio | 说明后续影响及正在运行的工作不变 | 必要升权明确确认 |
| 8 | Drawer：能力/用途/权限摘要 | [保存能力] / Primary | U18能力行更新“已绑定，尚未用于工作” | 原Employee identity/历史不变 |
| 9 | 原Work若因能力Blocked | [返回原工作]→按支持[继续工作] | 重新校验原scope与授权后请求恢复 | 不能自动重发原指令，失败仍原Work |

走查判据：没有假定Codex已安装/可用，也没有规定未经验证的OAuth或CLI协议；不可用终点的画法确定。

## 模拟 7. Human Handoff：登录、支付、手机确认或签字

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U24：工作中出现真人必要动作 | 原Work显示F07 / Action Package | 原因/目标账号/材料/回收判据 | 工作等待，不判失败 |
| 2 | U11或通知：同一待处理引用 | [继续处理] / Row | U26原Work Main | 不是另建人工任务库 |
| 3 | 若付款/不可逆签字尚未获授权 | [查看方案] / P7 | 金额/对象/影响/来源/可选项，CEO明确选择 | Decision≠实际付款 |
| 4 | 动作包：明确已准备好什么 | [查看准备内容] / Utility | 真实材料/版本预览 | 退出回动作包 |
| 5 | 动作包：官方入口与到期信息 | [前往平台] / External | 浏览器/手机/系统界面 | Curis原Work持久，外跳不完成 |
| 6 | 用户实际完成后返回 | [我已完成] / Button | 记录用户报告→核对状态 | 无回执时显示尚未确认 |
| 7 | 结果核对：确认/未知/失败 | [核对结果]或[补充凭证] | 确认才自动继续；未知不再付/发一次 | 范围仍原Work |
| 8 | 原Work显示恢复结果 | [返回CEO工作台] / Back | 事项按真实回执更新；暂缓仍待处理 | 同通知不重复生成 |

走查判据：外部动作来源和回收判据都有；链接过期先核对旧结果，避免重复支付或发布。

## 模拟 8. Result → Evidence → Learning

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U24：F04结果引用/当前修订 | [查看结果] / Reference | U27 Utility | 只Viewed，不Accepted |
| 2 | Utility：结论/作者/原Work/证据 | [展开阅读] / Maximize | 同Result最大化，不换业务scope | Esc回原Utility |
| 3 | Result：某项判断的证据引用 | [查看依据] / Link | 同Utility Evidence，来源/时间/正文 | 内部Back回原Result段 |
| 4 | 结果存在错误或可接受 | [要求修改]或[接受结果] / Action | 写明确版本接受状态/修改责任 | 不覆盖原交付 |
| 5 | Review：事实/适用条件/下一步建议 | [应用建议] / Drawer | 目标对象、原策略/规则、差异、依据 | 不是新Learning中心 |
| 6 | 建议为重大Goal改变 | [提交修订] / P7 | CEO接受后新规则/目标版本 | 未接受仍建议，不自动写Truth |
| 7 | 建议为合法知识候选 | [保存为知识候选] / Library入口 | 带来源/范围的新候选，正式接受规则不变 | 不把聊天当公司Policy |
| 8 | 原Review：已采用/仍候选状态 | [返回原工作] / Back | 变更引用与下一Cycle判断 | 失败留应用建议未完成，不骗下一轮已改 |

走查判据：结果读取、接受、知识候选、策略生效四件事有不同动作与证据。

## 模拟 9. Content Growth一个账号完整经营

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U30：实际Content Growth Workspace，无账号 | [接入经营账号] / Drawer | 选择真实Company Account或连接新账号 | 保持真实Workspace，不创建平台Workspace |
| 2 | 账号绑定：平台/handle/连接/本空间 | [保存绑定] / Button | U31账号经营面；无连接则待配置 | 新绑定不代表开始发布 |
| 3 | U31 Header：账号身份/Goal缺口 | [和账号负责人讨论] / Main | “这个账号交给Curis经营”的责任Conversation | 下一消息scope=实际空间+账号引用 |
| 4 | 目标/策略提案：成功标准、范围、约束 | [查看方案] / P7 | CEO确认必要Goal/边界 | 目标正式生效后摘要更新 |
| 5 | U31：本轮重点/当前负责人 | [查看工作] / Row | Research Work：输入/任务/结果证据 | 账号关系保留 |
| 6 | 研究Result与计划提案 | [查看结果] / Utility；[继续讨论] | Planning/Topic按真实责任下一步，不机械固定所有角色人数 | 原Workspace Cycle连续 |
| 7 | U32：内容意图标题/目的/目标账号 | [交给员工生产] / Primary | 包含平台规格和账号Context的生产Work | 明确目标Variant，不简单复制common text |
| 8 | U24：生产过程与输出 | [查看此账号版本] / Link | U32 Main Editor，标题/正文或脚本/媒体 | 回原生产Work可追来源 |
| 9 | U32：当前修订与适用规格 | [保存此账号版本] / Button | 新草稿修订，其他账号不变 | 保存后留同Variant |
| 10 | 定稿：内容/素材/版权/规格/修订 | [提交审核] / Button | 真实Review责任Work/P7 | 待审核不是审核通过 |
| 11 | 审核通过当前修订 | [准备发布] / Primary | U33目标/账号/版本/时间/能力表 | 保持原Intent/Account |
| 12 | 发布计划及授权范围 | [确认发布计划]→[执行发布] | Curis发布员工调用合法Provider | 每账号Publication产生真实回执 |
| 13 | 若平台需手机确认 | [继续处理] / Handoff Main | U26材料/账号/官方入口 | 原发布Work等待用户 |
| 14 | 用户外部完成返回 | [我已完成]→[核对结果] | 确认平台发布或保留未知 | 不因用户点击就标已发布 |
| 15 | 发布记录：真实回执/链接 | [查看回执] / Utility | 可检查真实平台结果 | 不更改原内容版本 |
| 16 | U31：表现数据可用/缺口 | [查看经营分析] / Button | U34原账号/周期/F13 | 进入既有Insights，回原账号 |
| 17 | U34：数据来源/时效/值或Unknown | [请分析员工解读] / Main Conversation | Curis分析Employee形成报告/解释/限制 | Provider只是数据来源 |
| 18 | 报告：Learning与调整建议 | [应用建议] / 差异/P7按边界 | 合法下一轮改变；目标大改CEO | 与原Result/Evidence连通 |
| 19 | U31：本轮结束/最新判断/下一步 | [查看下一轮] / Link | Continue/Adjust才进入一次下一Cycle；Wait保留检查点 | CEO返回U11看真实变化，不假收益 |

走查判据：接管→Goal→策略→研究→计划→生产→审核→发布→人工→回执→数据→分析→学习→下一轮全部有对象与返回；不保证平台实际可用。

## 模拟 10. Content Growth同一内容多平台发布

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U32：共同Intent，已有一个账号目标 | [添加目标账号] / 选择overlay | 选抖音A/小红书B/YouTube C等真实已绑定账号 | Account仅目标，Workspace不自动拆 |
| 2 | Variant比较表：每账号形式/修订/状态 | [交给员工生产] / Button | 各目标规格×账号Context生产独立版本 | 每份私有Context隔离 |
| 3 | 选择B行：图文标题/正文/图片 | [编辑内容] / Main Editor | 只改B；A/C版本留原样 | 换行前处理脏草稿 |
| 4 | 全部目标审核状态分别显示 | 逐个[提交审核] / Row action | 审核对应具体修订，未通过目标保持Blocked | 不批量假通过 |
| 5 | U33：每目标时间/能力/授权/政策 | [确认发布计划] / Main | 看到自动/需确认/未连接差异 | BEST_EFFORT/ALL_REQUIRED决定未执行项 |
| 6 | 发布执行后：A需手机、B已确认、C未知 | A[继续处理]；C[核对结果] | A走外部动作；B保成功；C先查 | 不得整体[再发一次] |
| 7 | 表格各目标最新回执 | [查看回执] / Utility | 逐账号可追溯来源 | 回同表筛选 |
| 8 | 汇总：已确认N/待处理N | [返回内容意图] / Back | 同Intent保持各版本和发布历史 | 不存在总Publication成功真源 |

走查判据：多平台差异在生产前进入Brief；发布部分成功与Unknown都有独立恢复路径。

## 模拟 11. Provider失败与未知外部结果

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U33：发布请求中断/超时 | 状态“结果待确认” / Row | 显示最后确认时间/已提交信息 | 保留原Publication |
| 2 | 未知结果条目 | [核对结果] / Button | 查询原请求对应账号/回执 | 不新建发布请求 |
| 3 | 查询证实已成功 | [查看回执] / Utility | 同条更新已发布，链接实际对象 | 原Work继续，不再发布 |
| 4 | 查询证实未完成且可重试 | [重试发布] / Action | 重验账号/定稿/授权，只重试失败目标 | 与原尝试关联，保留旧记录 |
| 5 | 查询也失败/不支持 | [前往平台核实] / External | Human Handoff收集实际证据 | 保持Unknown，不能归类确认失败 |
| 6 | 连接需要授权 | [重新连接] / Settings | 修复唯一连接后[返回原发布记录] | 不把重连当已发成功 |
| 7 | 回到原记录仍待确认 | [核对结果] / Action | 只有证据更新状态；需用户等待则待处理 | 返回账号/CEO清单保持事实 |

走查判据：禁止把“超时”当“没发生”；Shared恢复不因新连接或新页面创建第二次副作用。

## 模拟 12. 数据未知、过期与无法确认的0

| 步骤 | 当前Surface / 所见字段 | 点击 / 组件 | 打开什么 / 产生什么 | Context变化 / 返回 |
|---|---|---|---|---|
| 1 | U31表现摘要：没有可信值 | [查看经营分析] / Button | U34当前账号/周期数据覆盖说明 | From是原账号 |
| 2 | U34：指标名/单位/期间/来源/状态 | [查看原因] / Utility | 区分未采集/不支持/连接失败/过期/可疑0 | 不显示绿色0增长 |
| 3 | 状态未采集且有真实通道 | [重新获取数据] / Button | 局部读取中，旧值保留标时效 | 成功回原期间，失败留原因 |
| 4 | 状态不支持或缺证据 | [补充数据] / Drawer | 值/单位/期间/来源/凭证必填 | 用户可取消，不强迫填0 |
| 5 | 人工记录保存成功 | [查看依据] / Utility | manual来源、作者、时间；不覆平台事实 | 回报告/同指标 |
| 6 | 确有来源的真实零值 | [请分析员工解读] / Main | 允许分析0，但标样本/归因限制 | 新的分析Work，不修改平台数据 |
| 7 | 仍有未知指标 | 报告显示事实/未知/可做下一步 | 允许有边界分析或等待，不伪装全量趋势 | 策略大改仍P7 |
| 8 | 完成阅读或分析 | [返回账号] / Back | U31原账号和滚动；更新可信摘要 | 来源范围和缺口保留 |

走查判据：真实0与无法确认的0有不同结果；未知不会阻止全部阅读，也不会被UI填成假成功。

# 附录B. 来源与适用范围

所有引用均为本地文档输入；本轮未重新开展平台研究或声称新竞品事实。S10/S11/S12/S13保留原Research/Review等级，不能覆盖S01路由的Current Truth。S03/S06中旧记录按S08明确supersession解释；没有自行在互相矛盾的Current Authority间选第三种方案。

| Source | 文件 | Class / 采用边界 |
|---|---|---|
| S01 | [PRODUCT_DOCUMENT_POINTER.md](</Users/yy/Documents/Curis AI Workspace/docs/00_Context/PRODUCT_DOCUMENT_POINTER.md>) | FROZEN Truth Router；Current Required Input |
| S02 | [Curis_Product_Blueprint.html](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Blueprint.html>) | CURRENT/Frozen唯一Product Blueprint；产品关系/字段/九空间七导航 |
| S03 | [Curis_Product_Master_Map.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Master_Map.md>) | CURRENT/Frozen展开；字段与对象动作 |
| S04 | [Curis_Product_UI_Blueprint.html](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_UI_Blueprint.html>) | CURRENT/Frozen空间投影；未读取旧视觉作为答案 |
| S05 | [CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md>) | CURRENT PRODUCT STRUCTURE/Frozen；七区/层级/组织/共享壳 |
| S06 | [Curis_Company_OS_Shared_Authority.md](</Users/yy/Documents/Curis AI Workspace/docs/03_Design/Curis_Company_OS_Shared_Authority.md>) | CURRENT/Frozen Shared；责任/权限/持续经营 |
| S07 | [Curis_Workspace_Shell_Contract_And_Shared_Patterns.md](</Users/yy/Documents/Curis AI Workspace/docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md>) | CURRENT/Frozen Shell；头像Utility、P7、T1–T3、Search Reserved |
| S08 | [CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md](</Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md>) | CURRENT ACCEPTED CEO DECISION/Frozen；明确修订适用范围 |
| S09 | [Curis_Content_Growth_Domain_Authority.md](</Users/yy/Documents/Curis AI Workspace/docs/03_Design/Curis_Content_Growth_Domain_Authority.md>) | DOMAIN/Frozen；Intent/Variant/Publication与账号 |
| S10 | [CURIS_PRODUCT_DEFINITION_REBUILD.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_PRODUCT_DEFINITION_REBUILD.md>) | REVIEW/Draft；新定义的用户价值，非整篇自动接受 |
| S11 | [CURIS_2026_09_14_FULL_PRODUCT_RETHINK_REVIEW.md](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/CURIS_2026_09_14_FULL_PRODUCT_RETHINK_REVIEW.md>) | REVIEW/Review；真假证据/范围/竞争判断纠偏 |
| S12 | [CURIS_CONTENT_GROWTH_PRODUCT_LANGUAGE_V2.md](</Users/yy/Documents/Curis AI Workspace/docs/research/content-growth-product-language-2026-09-14/CURIS_CONTENT_GROWTH_PRODUCT_LANGUAGE_V2.md>) | RESEARCH/Review；Content Growth V2候选与127项Owner |
| S13 | [CURIS_AITO_EARN_SOCIAL_PLATFORM_EXECUTION_PROVIDER_REVIEW.md](</Users/yy/Documents/Curis AI Workspace/docs/research/aitoearn-execution-provider-2026-09-14/CURIS_AITO_EARN_SOCIAL_PLATFORM_EXECUTION_PROVIDER_REVIEW.md>) | REVIEW/Review；Provider能力与数据/恢复缺口，非真实端到端验收 |
| S14 | [Curis_Product_Context.md](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Context.md>) | CURRENT / Frozen；普通CEO定位、同一Company与专业环境边界；身份措辞按S08四层具体关系限定，不另创排他身份定义 |

本稿没有修改Current Pointer、Master Map、UI Blueprint、Change Log；原因是本轮只有候选表达，没有Current Truth晋升。文件位置：docs/research/full-product-expression-2026-09-14；输入版本由同目录input-manifest.json记录。CEO接受后唯一Blueprint Reconciliation再决定正式下游链接，不能因为文件名含“Specification”就成为第二Authority。

# 附录C. 交付核对

检查范围：42个指定章节；25个主Surface合同及7个子面；18份字段合同；36条Interaction；12个完整模拟共108步；输入Hash及本地引用可达。结构计数用于检查遗漏，不作为产品能力验收。实际脚本检查结果保存在同目录verification.json。

**VERDICT: FULL PRODUCT EXPRESSION READY FOR UI — SPECIFICATION CANDIDATE。**  
**AUTHORITY: UNCHANGED。**  
**UI EXECUTION: NOT STARTED / NOT AUTHORIZED BY THIS VERDICT。**  
**NEXT: CEO REVIEW → CURIS PRODUCT BLUEPRINT RECONCILIATION。**  
**STOP FOR CEO REVIEW。**
