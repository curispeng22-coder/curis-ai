# CURIS FINAL COMPETITIVE REFERENCE DECISIONS

Authority Class: RESEARCH / EVIDENCE
Status: Review
Date: 2026-09-13
Disposition: FOR CEO / CHATGPT REVIEW — no Product Authority write

本文件是下一轮 HTML 修复的 **Reference Decision 输入**，不成为新的 Product Authority。修复仍必须先获授权、消费 Current Authority 与 Allowed Files。标 NEED MORE EVIDENCE 的条目不准以 L3/L4 完成口径实现验收；新增产品对象、模式、周期任务或审批策略均不在本轮授权内。

KEEP ZCODE REFERENCE: **53** | REPLACE REFERENCE: **4** | COMBINE: **36** | CURIS ORIGINAL: **18** | NEED MORE EVIDENCE: **22**

## 优先决策

1. 保留 WorkBuddy 人才/技能目录、专家卡、技能卡、文件卡与消息操作方向。
2. 保留 Claude 输入面与模型菜单方向；撤回“20px占位+32px圆发送”的错误像素假设，Shared Composer 槽位优先。
3. Linear 保留导航密度、搜索结果/预览；Search与Command分开，后者不越过 Curis v1 scope。
4. Cursor 保留文档/Source/Preview/最大化/Follow-up 交互；Coze 只负责媒体类型编辑器参考。
5. Employee Detail/Workstation 与 Decision 回到 Curis Original，不用 Claude Projects 或 Error Banner 接管语义。
6. EvoFlow 加入下方10项参考/反例，其中9项正向结构或交互补充，1项结果/恢复边界反例；没有EvoFlow L4。

## 逐行最终登记

| ID | Decision | Reference / Level | 下一轮约束 | Evidence |
|---|---|---|---|---|
| Z001 App Shell 导航轨 | KEEP ZCODE REFERENCE | Linear / L3 | 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | R16–R18 / E9 |
| Z002 Sidebar 分组计数/折叠 | KEEP ZCODE REFERENCE | Linear / L3 | 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | R16–R18 / E9 |
| Z003 Context Pane（四Pane左） | REPLACE REFERENCE | Curis Context 职责 + Linear 集合导航 / L2 | Codex 环境 Inspector 是执行环境与来源，不应反向搬成 Curis 左侧 Context；完整员工档案应在 Utility。 | A2 §§2–3 / R17 / H12 |
| Z004 Main Pane | KEEP ZCODE REFERENCE | Linear 行密度；Employee 行服从 Curis / L2 | 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | R17 / E9 / H34 |
| Z005 Utility Pane | COMBINE | WorkBuddy 阅读 + Cursor 文档/代码 + Coze 媒体编辑器 / L3 | 按对象类型分流：正文阅读、Source/Preview、媒体时间线；不把所有 Utility 做成媒体编辑器。 | E1 / R19–R24 |
| Z006 Floating Assistant | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z007 Global Search | COMBINE | Curis Object Search 浮层合同 + Linear 搜索结果/侧预览 / L3 | E9 实际是完整搜索页面，不是带 chips 的 ⌘K 浮层；保留类型/选中/预览思想，不能宣称整壳 L4。 | R16–R18 / E9 / A2 §2.3.1 |
| Z008 Command Palette | CURIS ORIGINAL | Curis v1 Search；Command Palette 为预留 / L0 | 不能把竞品 Command Palette 的派工/开会动作直接加入 v1；下一轮只修 Object Search 的键盘闭环。 | A2 §2.3.1 / R18 |
| Z009 Notification | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z010 Account Menu | KEEP ZCODE REFERENCE | Claude 底部身份与账户入口 / L3 | 位置方向可保留；模型、公司、个人设置分属 Curis 语义，当前账户 menu 全菜单未逐项验证。 | R06 / E4 |
| Z011 Window/Desktop Chrome | KEEP ZCODE REFERENCE | Linear / L3 | 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | R16–R18 / E9 |
| Z012 Empty State | KEEP ZCODE REFERENCE | Claude 行动型空态 / L3 | 保留一个主行动和建议行，降低 L4；CEO 空态需符合公司已创建/未创建的真实阶段，不能照抄品牌欢迎页。 | R06 / E4 / H29 |
| Z013 Error State | KEEP ZCODE REFERENCE | Claude 分层错误横幅 / L3 | 标题、影响、Details、自助与上报路径可借；本例为 Gateway 连接失败，不是通用 Agent 失败。不得把 Retry 等同于 Regenerate。 | R06 / E4 / H30 |
| Z014 Loading/Working | COMBINE | Cursor 工作摘要 + EvoFlow Running/队列 + Coze 步骤行 / L3 | 只观察到 Coze 演示步骤静态记录；动态运行参考 EvoFlow，语义仍由 Curis Runtime projection 决定。 | R19 / R26–R28 / E8 |
| Z015 Brief / Attention | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z016 Decision | CURIS ORIGINAL | Curis P7 Decision Package / L0 | Error Banner 不是审批模型；高风险 Layer0 只能查看方案/暂缓，具体 Choice 留 Layer1。 | A2 §3.13 / H08 / H31 |
| Z017 Running Work | COMBINE | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector / L2 | E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | R19 / R26–R28 / E5 |
| Z018 Latest Result | KEEP ZCODE REFERENCE | WorkBuddy / Coze 结果引用 → 阅读或编辑面 / L3 | 保留对象连续性；Curis Evidence 与员工来源需要额外字段，不可只做卡片导航。 | E1 / R22 / R24 / H26–H27 |
| Z019 Employee Activity | KEEP ZCODE REFERENCE | Codex 子智能体头像组（仅静态结构） / L2 | 保留头像+计数的紧凑结构，降到 L2；并行生命周期与点击反馈未独立验证，不能作为运行中 L3/L4 验收。 | E5；当前原生访问被工具限制 |
| Z020 Business List/Card | KEEP ZCODE REFERENCE | Linear 行密度；Employee 行服从 Curis / L2 | 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | R17 / E9 / H34 |
| Z021 Workspace 列表/入口 | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z022 Workspace Header/导航 | KEEP ZCODE REFERENCE | Linear / L3 | 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | R16–R18 / E9 |
| Z023 Working Surface | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z024 Workspace Result | COMBINE | WorkBuddy 阅读 + Cursor 文档/代码 + Coze 媒体编辑器 / L3 | 按对象类型分流：正文阅读、Source/Preview、媒体时间线；不把所有 Utility 做成媒体编辑器。 | E1 / R19–R24 |
| Z025 公司版图/部门/团队 | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z026 Employee List / Row | KEEP ZCODE REFERENCE | Linear 行密度；Employee 行服从 Curis / L2 | 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | R17 / E9 / H34 |
| Z027 Employee Card（目录卡） | CURIS ORIGINAL | Curis Employee Row / Conversation-first Workstation / Utility Detail / L0 | 员工目录不是人才市场；Claude Projects 的 instructions/knowledge/chats 配置页不适合作员工默认 Main。 | A2 §§3.1,3.14 / H12,H14,H34 |
| Z028 Employee Detail / 工作站 | CURIS ORIGINAL | Curis Employee Row / Conversation-first Workstation / Utility Detail / L0 | 员工目录不是人才市场；Claude Projects 的 instructions/knowledge/chats 配置页不适合作员工默认 Main。 | A2 §§3.1,3.14 / H12,H14,H34 |
| Z029 Employee Status | COMBINE | Curis 三态 + EvoFlow 员工/工作项/审批分层 / L2 | 员工存在与工作完成分开；不要复制 EvoFlow 在岗/自动上班词典或 Coze 步骤完成状态作为 Employee UI 状态。 | A2 §3.1 / R11 / H34 |
| Z030 Current Work（员工卡内） | COMBINE | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector / L2 | E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | R19 / R26–R28 / E5 |
| Z031 Responsibility / Handoff | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z032 Talent Home | KEEP ZCODE REFERENCE | WorkBuddy 专家/技能/连接器目录 / L2 | 三目录、场景导购、来源与已装计数方向正确；不混淆已雇员工与可招聘模板。 | R01,R02 / E2,E3 |
| Z033 Employee/Expert Card | KEEP ZCODE REFERENCE | WorkBuddy 专家卡 / L4 | 保留头像/标题/发布者/简介/标签层级；招聘动作与 Curis-ready/Candidate 语义单独适配，Hover 尚未验证。 | R02 / E2 / M1 |
| Z034 Expert Detail | REPLACE REFERENCE | WorkBuddy 专家消费详情 + Curis 能力/责任边界 / L2 | 不能把 Coze Agent 配置页的 prompt/model 作为普通用户专家详情主面；高级配置后置。详情交互仍需补测，不提升 L3。 | R02 / E2 / A1 / H17 |
| Z035 Skill Marketplace | KEEP ZCODE REFERENCE | WorkBuddy 专家/技能/连接器目录 / L2 | 三目录、场景导购、来源与已装计数方向正确；不混淆已雇员工与可招聘模板。 | R01,R02 / E2,E3 |
| Z036 Skill Card | KEEP ZCODE REFERENCE | WorkBuddy Skill Card / L4 | 技能卡需更紧凑，首行内联安装；不要复用较高的专家卡。 | R01 / E3 / M2 |
| Z037 Skill Detail | COMBINE | WorkBuddy 技能消费信息 + EvoFlow 能力概览 / L2 | 先说明何时使用/输入输出/来源，再按需看权限与挂载。完整技能详情仍需补证。 | R01 / R13 |
| Z038 Plugin / Connector | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z039 Install / Installed / Update | KEEP ZCODE REFERENCE | WorkBuddy 就地安装状态与计数 / L3 | 静态已装/可装态已验证；未执行新技能安装，安装失败/更新链路仍需补测。 | R01 / E3 |
| Z040 Search / Filter / Category | KEEP ZCODE REFERENCE | WorkBuddy 分类与目录过滤 / L3 | 实际分类为文本/矩形选中面，不支持一律 h28 r14 圆药丸；降低像素复刻声明。 | R01,R02 / E2,E3 |
| Z041 Model Binding | COMBINE | Curis Execution Selector + EvoFlow Agent/Model 分层 / L2 | 员工是公司身份，Model 与 Agent 显性区分；能力绑定不等于某模型绑定。 | A2 §3.5 / R13 |
| Z042 Capability Binding | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z043 成果反查导购 | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z044 Conversation Layout（任务型） | KEEP ZCODE REFERENCE | WorkBuddy 任务型 Conversation / L2 | AI 正文文本流、阶段摘要、结果引用、消息操作相邻；CEO/Meeting 的发言语义不能被任务标题替代。 | R04,R05 / E1 |
| Z045 User Message | KEEP ZCODE REFERENCE | ChatGPT 用户消息气泡 / L4 | 仅双人对话用户消息：右对齐、浅底、宽度受限；不要复制到所有 Employee/Meeting 发言。 | R25 DOM EXACT / M6 |
| Z046 Employee/AI Message | KEEP ZCODE REFERENCE | Claude / ChatGPT AI 正文流 / L3 | AI 回复不套统一气泡；Curis 保留员工身份行和工作事件。 | R25 / R04 / R13 |
| Z047 Message Width / Alignment | COMBINE | ChatGPT 限宽思想 + Curis 宿主宽度规则 / L2 | 一张截图不能推出固定720；Conversation 与 Composer 对齐优先，Context/Utility 打开后宽度需自适应。 | R25 / H14 / A2 §3.5 |
| Z048 File Reference | KEEP ZCODE REFERENCE | WorkBuddy 文件附件卡 / L4 | 两列按可用宽度适配；文件类型/名称截断/meta/打开独立，上传过程与菜单需补测。 | E1 实拍 provenance / M3 |
| Z049 Knowledge / Citation | KEEP ZCODE REFERENCE | Codex 来源列表（静态） / L2 | 只借引用集合的折叠结构；浏览器来源/附件不是 Curis Evidence 的完整可信链。 | E5 |
| Z050 Mention | COMBINE | WorkBuddy 语法提示 + EvoFlow @员工/#文件入口 / L2 | 提示语不是已实现引用；真实选中资源 chip、移除、不可用态需要实现和验收。 | R04 / R13 |
| Z051 Tool Activity | COMBINE | Cursor 折叠摘要 + EvoFlow 工具逐层展开 / L3 | 先摘要，再具体工具，再输出；不把日志全部永久铺开。 | R13 / R19 / E6 |
| Z052 Thinking | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z053 Plan | COMBINE | Curis Work 计划语义 + Cursor 工作摘要 + EvoFlow 工作流分步 / L2 | 不把普通 Work 变成必须编辑 DAG；计划改写/任务复用仍须补测。 | R08,R19 / A2；Manus 本轮不可用 |
| Z054 Progress（会话内） | COMBINE | Cursor 工作摘要 + EvoFlow Running/队列 + Coze 步骤行 / L3 | 只观察到 Coze 演示步骤静态记录；动态运行参考 EvoFlow，语义仍由 Curis Runtime projection 决定。 | R19 / R26–R28 / E8 |
| Z055 Result Reference | KEEP ZCODE REFERENCE | WorkBuddy / Coze 结果引用 → 阅读或编辑面 / L3 | 保留对象连续性；Curis Evidence 与员工来源需要额外字段，不可只做卡片导航。 | E1 / R22 / R24 / H26–H27 |
| Z056 Artifact | KEEP ZCODE REFERENCE | Coze 类型化媒体产物 / 编辑器 / L2 | 媒体场景方向正确；E8 是演示，不支持宣称真实多 Agent 生成能力；不覆盖文档/证据阅读。 | R22–R24 / E8 |
| Z057 Error / Retry | KEEP ZCODE REFERENCE | Claude 分层错误横幅 / L3 | 标题、影响、Details、自助与上报路径可借；本例为 Gateway 连接失败，不是通用 Agent 失败。不得把 Retry 等同于 Regenerate。 | R06 / E4 / H30 |
| Z058 Branch | COMBINE | Cursor Fork + EvoFlow 分叉 / L2 | 分叉保留原对象与来源；本轮未新建分支，不升级完整交互结论。 | R13,R28 / Cursor 历史研究截图 |
| Z059 Copy / Actions 行 | KEEP ZCODE REFERENCE | WorkBuddy 消息操作行 / L4 | 动作贴近当前消息、More 渐进披露；Curis 的交接/升级需要语义 Gate，不是普通分享按钮。 | R04,R05 / E1 / M4 |
| Z060 Timestamp | KEEP ZCODE REFERENCE | Cursor 完成时长/相对时间 / L3 | 保留已完成摘要与时间；工作完成属于 Work/Turn，不属于员工身份状态。 | R19,R21 |
| Z061 成本内联 | KEEP ZCODE REFERENCE | WorkBuddy 成本内联 / L3 | 旧截图有成本，新测试只有模型/时间；按真实 usage 可用性显示，不能把常量成本当完成证据。 | E1 / R04 |
| Z062 Composer Container | KEEP ZCODE REFERENCE | Claude Composer 外形与 Add 入口 / L3 | 参考方向正确，L4 降级：旧20px与圆发送按钮描述不符合实拍，Curis 更完整语义槽位需适配。 | R06,R07 / E4 / M5 |
| Z063 Text Area / Placeholder | KEEP ZCODE REFERENCE | Claude Composer 外形与 Add 入口 / L3 | 参考方向正确，L4 降级：旧20px与圆发送按钮描述不符合实拍，Curis 更完整语义槽位需适配。 | R06,R07 / E4 / M5 |
| Z064 Attachment | KEEP ZCODE REFERENCE | Claude Composer 外形与 Add 入口 / L3 | 参考方向正确，L4 降级：旧20px与圆发送按钮描述不符合实拍，Curis 更完整语义槽位需适配。 | R06,R07 / E4 / M5 |
| Z065 File Chip | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z066 Context / Reference（@语法） | COMBINE | WorkBuddy 语法提示 + EvoFlow @员工/#文件入口 / L2 | 提示语不是已实现引用；真实选中资源 chip、移除、不可用态需要实现和验收。 | R04 / R13 |
| Z067 Model Selector | KEEP ZCODE REFERENCE | Claude 内联模型选择 + 锚定菜单 / L4 | 保留内联标签/chevron/就近菜单/当前选中标记；不复制 Gateway 自定义模型目录。 | R07 / E4 / M5 |
| Z068 Agent/Employee Selector | COMBINE | Curis Execution Selector + EvoFlow Agent/Model 分层 / L2 | 员工是公司身份，Model 与 Agent 显性区分；能力绑定不等于某模型绑定。 | A2 §3.5 / R13 |
| Z069 Mode Selector | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z070 Permission Selector | COMBINE | WorkBuddy 就地权限 + EvoFlow requested/configured/effective 分层 / L3 | 就地可见档位 + 安全中心生效状态；完全访问不等于已启用沙箱，不用颜色替代解释。 | R12,R13 / A2 §3.5 |
| Z071 Send | COMBINE | Claude 圆角方形禁用按钮 + WorkBuddy 圆形按钮 / L3 | 参考不是统一32圆；选 Curis 自己的共享按钮形状，保留空输入禁用与同位 Stop。 | R06 / E4 / R04 |
| Z072 Stop / Running | KEEP ZCODE REFERENCE | WorkBuddy Send/Stop 与空输入禁用 / L3 | 操作方向正确；HTML 发送不追加消息和空输入可发送需先修。 | R04 / 新任务空输入与本轮 Stop 操作 |
| Z073 Queue / Steering | COMBINE | EvoFlow Running 时排队提示 + Cursor 补充指令 / L3 | 观察到可输入与 Enter 排队提示；本轮未真正排队执行，queue 与 steer 不等同，后续验收需分别测试。 | R26 / R19–R21 |
| Z074 Disabled | KEEP ZCODE REFERENCE | WorkBuddy Send/Stop 与空输入禁用 / L3 | 操作方向正确；HTML 发送不追加消息和空输入可发送需先修。 | R04 / 新任务空输入与本轮 Stop 操作 |
| Z075 Multi-line / Keyboard | KEEP ZCODE REFERENCE | ChatGPT / Cursor 多行输入与键盘 / L3 | HTML 换行与发送需要补闭环；不能仅凭 textarea 判多行扩展完成。 | R25 / H14–H15 / Cursor 已有研究 |
| Z076 Drag & Drop | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z077 Start | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z078 Plan | COMBINE | Curis Work 计划语义 + Cursor 工作摘要 + EvoFlow 工作流分步 / L2 | 不把普通 Work 变成必须编辑 DAG；计划改写/任务复用仍须补测。 | R08,R19 / A2；Manus 本轮不可用 |
| Z079 Todo | COMBINE | Curis Work 计划语义 + Cursor 工作摘要 + EvoFlow 工作流分步 / L2 | 不把普通 Work 变成必须编辑 DAG；计划改写/任务复用仍须补测。 | R08,R19 / A2；Manus 本轮不可用 |
| Z080 Current Step / Activity | COMBINE | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector / L2 | E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | R19 / R26–R28 / E5 |
| Z081 Tool Call | COMBINE | Cursor 折叠摘要 + EvoFlow 工具逐层展开 / L3 | 先摘要，再具体工具，再输出；不把日志全部永久铺开。 | R13 / R19 / E6 |
| Z082 Subtask / Multi-Agent | KEEP ZCODE REFERENCE | Codex 子智能体头像组（仅静态结构） / L2 | 保留头像+计数的紧凑结构，降到 L2；并行生命周期与点击反馈未独立验证，不能作为运行中 L3/L4 验收。 | E5；当前原生访问被工具限制 |
| Z083 Delegation | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z084 Steering | COMBINE | EvoFlow Running 时排队提示 + Cursor 补充指令 / L3 | 观察到可输入与 Enter 排队提示；本轮未真正排队执行，queue 与 steer 不等同，后续验收需分别测试。 | R26 / R19–R21 |
| Z085 Permission | COMBINE | WorkBuddy 就地权限 + EvoFlow requested/configured/effective 分层 / L3 | 就地可见档位 + 安全中心生效状态；完全访问不等于已启用沙箱，不用颜色替代解释。 | R12,R13 / A2 §3.5 |
| Z086 Pause / Stop / Retry / Failure / Recovery | REPLACE REFERENCE | Cursor 中断续作 + 明示恢复边界 / L2 | 替换单一 WorkBuddy 自动化记忆引用。EvoFlow 停止后丢弃未完成输出，不可列最佳恢复。原生重启恢复本轮未重测。 | Cursor 20260910 interrupted/resumed-result；R26–R28 为 EvoFlow 反例 |
| Z087 Completion | KEEP ZCODE REFERENCE | Cursor 完成时长/相对时间 / L3 | 保留已完成摘要与时间；工作完成属于 Work/Turn，不属于员工身份状态。 | R19,R21 |
| Z088 Resume | REPLACE REFERENCE | Cursor 中断续作 + 明示恢复边界 / L2 | 替换单一 WorkBuddy 自动化记忆引用。EvoFlow 停止后丢弃未完成输出，不可列最佳恢复。原生重启恢复本轮未重测。 | Cursor 20260910 interrupted/resumed-result；R26–R28 为 EvoFlow 反例 |
| Z089 Agent 工作右栏（骨架） | COMBINE | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector / L2 | E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | R19 / R26–R28 / E5 |
| Z090 Result Card（会话内） | COMBINE | WorkBuddy 文件卡 + Coze 类型化交付卡 / L3 | 按 Result 类型区分，Evidence/UsedBy 属 Curis；不能用一个L4卡覆盖所有文档/代码/音视频。 | E1 / R22 / H26,H27 |
| Z091 Result Row（列表） | KEEP ZCODE REFERENCE | Linear 行密度；Employee 行服从 Curis / L2 | 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | R17 / E9 / H34 |
| Z092 Preview | KEEP ZCODE REFERENCE | Cursor Preview/Source/最大化与 Follow-up / L3 | 交互已复核；Pane 宽度与宿主随用户布局变化，降 L4 为 L3。HTML 标签不切换内容不是复刻。 | R19–R21 / M8 |
| Z093 Artifact Panel（富产物） | KEEP ZCODE REFERENCE | Coze 类型化媒体产物 / 编辑器 / L2 | 媒体场景方向正确；E8 是演示，不支持宣称真实多 Agent 生成能力；不覆盖文档/证据阅读。 | R22–R24 / E8 |
| Z094 Evidence / Citation | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z095 Version | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z096 Download / Export | KEEP ZCODE REFERENCE | WorkBuddy 阅读器与文件动作 / L3 | 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | E1 |
| Z097 Continue Working / Ask Employee | KEEP ZCODE REFERENCE | Cursor Preview/Source/最大化与 Follow-up / L3 | 交互已复核；Pane 宽度与宿主随用户布局变化，降 L4 为 L3。HTML 标签不切换内容不是复刻。 | R19–R21 / M8 |
| Z098 Open Utility | KEEP ZCODE REFERENCE | WorkBuddy / Coze 结果引用 → 阅读或编辑面 / L3 | 保留对象连续性；Curis Evidence 与员工来源需要额外字段，不可只做卡片导航。 | E1 / R22 / R24 / H26–H27 |
| Z099 Knowledge Home | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z100 File Row | KEEP ZCODE REFERENCE | Linear 文件行密度 / L3 | Curis 有来源/范围/引用计数，两行模型合理，但不能宣称复制36px单行 L4。 | R17 / E9 / H33 |
| Z101 Reading Surface | KEEP ZCODE REFERENCE | WorkBuddy 阅读器与文件动作 / L3 | 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | E1 |
| Z102 Reference / Used By | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z103 Search / Filter | COMBINE | Curis Object Search 浮层合同 + Linear 搜索结果/侧预览 / L3 | E9 实际是完整搜索页面，不是带 chips 的 ⌘K 浮层；保留类型/选中/预览思想，不能宣称整壳 L4。 | R16–R18 / E9 / A2 §2.3.1 |
| Z104 Detail 元数据 | KEEP ZCODE REFERENCE | WorkBuddy 阅读器与文件动作 / L3 | 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | E1 |
| Z105 Meeting 全部（列表/房间/议程/决议） | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z106 参会者头像/说话人 | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z107 纪要/转写 | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z108 Proposal→Decision 卡 | CURIS ORIGINAL | Curis P7 Decision Package / L0 | Error Banner 不是审批模型；高风险 Layer0 只能查看方案/暂缓，具体 Choice 留 Layer1。 | A2 §3.13 / H08 / H31 |
| Z109 洞察语义（Analyst/归因/Decision support） | CURIS ORIGINAL | Curis Current Authority / L0 | 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | A1 / A2 / A4 / A5 |
| Z110 Metric/Chart 视觉 | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z111 Cost/Usage 视图 | KEEP ZCODE REFERENCE | Coze 用量拆分（仅结构） / L2 | 只借总量与来源拆分；充值套餐/倍率不等于 Curis 员工/业务成本归因。 | E7 / R24免费版 |
| Z112 Report 阅读 | KEEP ZCODE REFERENCE | WorkBuddy 阅读器与文件动作 / L3 | 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | E1 |
| Z113 Settings Shell / Navigation | COMBINE | Cursor 设置壳 + EvoFlow 生效状态分层 / L3 | 左类右容、设置搜索与分组；Cursor 当前 MCP/Skills 已迁到 Customize，不能照库存旧 IA 全搬。 | R29 / R12 / H22 |
| Z114 Account / Appearance | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z115 Model 列表 / Model Row | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z116 Provider / 凭据 | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z117 Skill | COMBINE | Cursor Customize + EvoFlow 能力概览 / L2 | 参考安装/启用/绑定/运行健康的区别；完整MCP配置界面本轮未验，禁止标完整L3。 | R29迁移提示 / R13的Skills/Tools/Knowledge/MCP |
| Z118 MCP | COMBINE | Cursor Customize + EvoFlow 能力概览 / L2 | 参考安装/启用/绑定/运行健康的区别；完整MCP配置界面本轮未验，禁止标完整L3。 | R29迁移提示 / R13的Skills/Tools/Knowledge/MCP |
| Z119 Permission | COMBINE | WorkBuddy 就地权限 + EvoFlow requested/configured/effective 分层 / L3 | 就地可见档位 + 安全中心生效状态；完全访问不等于已启用沙箱，不用颜色替代解释。 | R12,R13 / A2 §3.5 |
| Z120 Memory | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z121 Notification | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z122 Usage / Cost | KEEP ZCODE REFERENCE | Coze 用量拆分（仅结构） / L2 | 只借总量与来源拆分；充值套餐/倍率不等于 Curis 员工/业务成本归因。 | E7 / R24免费版 |
| Z123 Shortcut | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z124 Developer / About | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z125 Navigation | KEEP ZCODE REFERENCE | Linear 分组导航节奏 / L4 | 仅视觉节奏参考；冻结七区与 T1 控制优先。截图估测，不认可 Zcode 原逻辑像素值。 | R16–R18 / E9 / M7 |
| Z126 Sidebar | KEEP ZCODE REFERENCE | Linear 分组导航节奏 / L4 | 仅视觉节奏参考；冻结七区与 T1 控制优先。截图估测，不认可 Zcode 原逻辑像素值。 | R16–R18 / E9 / M7 |
| Z127 Pane 结构 | COMBINE | Cursor 自适应 Pane + Coze 类型化编辑器 / L2 | 保留分栏/最大化思想，Curis T1–T3/resize/记忆范围优先；不固定230/380或四列常驻。 | R19–R24 / A2 |
| Z128 Inspector/Utility | COMBINE | WorkBuddy 阅读 + Cursor 文档/代码 + Coze 媒体编辑器 / L3 | 按对象类型分流：正文阅读、Source/Preview、媒体时间线；不把所有 Utility 做成媒体编辑器。 | E1 / R19–R24 |
| Z129 Search | COMBINE | Curis Object Search 浮层合同 + Linear 搜索结果/侧预览 / L3 | E9 实际是完整搜索页面，不是带 chips 的 ⌘K 浮层；保留类型/选中/预览思想，不能宣称整壳 L4。 | R16–R18 / E9 / A2 §2.3.1 |
| Z130 Command Palette | CURIS ORIGINAL | Curis v1 Search；Command Palette 为预留 / L0 | 不能把竞品 Command Palette 的派工/开会动作直接加入 v1；下一轮只修 Object Search 的键盘闭环。 | A2 §2.3.1 / R18 |
| Z131 Floating Surface / Quick Entry | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z132 Notification | NEED MORE EVIDENCE | 暂不指定唯一 Best / 待定 | 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | Zcode 库存描述；本轮无对应完整交互证据 |
| Z133 Window Chrome | KEEP ZCODE REFERENCE | Linear / L3 | 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | R16–R18 / E9 |

## EvoFlow 新增 Reference 登记（不计入原133行）

| ID / Surface | Decision | Level | Evidence | 采用边界 |
|---|---|---|---|---|
| EV01 Employee / Agent / 工作项分层 | COMBINE | L2 | R11,R13 | 成员身份、能力配置、运行工作不要合并；Curis 三态与责任链优先。 |
| EV02 Task Center：协作任务与我的事项分账 | COMBINE | L2 | R09及事项菜单AX | 工作记录与个人备忘不同；是否新增事项对象须另行产品裁决。 |
| EV03 Approval 队列与空态解释 | COMBINE | L2 | R11 | 单独呈现待CEO事项与为空的原因；本轮无真实待审批项，不采用其直接运行默认策略。 |
| EV04 Permission posture 与实际安全生效状态 | COMBINE | L3 | R12,R13 | 会话请求档位、设置默认档位、实际沙箱生效要区分；不能只显示完全访问。 |
| EV05 Agent Capability / Context Inspector | COMBINE | L2 | R13 | Skills/Tools/Knowledge/MCP、上下文占用、运行统计渐进展开；完整配置留设置。 |
| EV06 运行状态+时长+输入队列提示 | COMBINE | L3 | R26–R28 | 工作状态在标题/历史/输出尾部反馈；Stop就近，排队执行本轮未验证。 |
| EV07 工作空间作为会话文件范围 | COMBINE | L2 | R13及工作空间菜单AX | 显示当前文件夹、切换与解绑入口；只借范围可见性，不能把Curis Workspace降成文件夹。 |
| EV08 Workflow 属性从谁做/做什么开始 | COMBINE | L2 | R08 | 高级指令、模型、失败设置折叠；不把工作流画布搬入普通CEO工作面。 |
| EV09 Automation 调度定义与运行记录分开 | COMBINE | L2 | R15 | 可借两类记录与启用/暂停计数；本轮未启动调度器或创建周期任务。 |
| EV10 结果/产物空态与恢复反例 | COMBINE | L1 | R14,R26–R28 | 文件写入记录不自动成为产物；停止丢弃未完成输出是应避免行为，不能直接列最佳恢复。 |

## 保留 L4 的边界

仅保留7个通用视觉单元：WorkBuddy Expert Card、Skill Card、File Reference Card、Message Actions；Claude 内联 Model Selector；ChatGPT User Bubble；Linear Navigation Rhythm。对应 Z033/Z036/Z048/Z059/Z067/Z045/Z125–126。每项都有真实截图与 M 测量表，但截图估测不是 Pixel Exact；未观察 hover 等状态明确列出。L4 是下一轮目标，不是当前HTML验收结果。Curis Iris/字体/图标与对象语义覆盖竞品品牌；尺寸适配不得假称逐像素相同。

没有因功能名字相似而把 EvoFlow 作为新增全局导航；没有引入 Workflow Builder/Agent Manager 产品模型。暂停的条目包括真实并行运行、真实审批成功/拒绝、Claude Memory 全流程、拖放、通知深链与版本恢复，需后续补证或降级。

## Evidence / Current inputs

- A1 [Structure Baseline](../../01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md) — FROZEN；七区/对象/全局Assistant。
- A2 [Frozen Shell](../../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md) — Frozen；§2.3 T1–T3/Search、§3.1 Employee、§3.5 Composer、§3.13 P7、§3.14 Detail。
- A3 [Visual Standard](../../03_Design/CURIS_VISUAL_STANDARD_V1.md) — Frozen；Iris #806BE5。
- A4 [Content Growth Domain Authority](../../03_Design/Curis_Content_Growth_Domain_Authority.md) 与 [CEO Reconciliation](../../reviews/CONTENT_GROWTH_CEO_AUTHORITY_DECISION_RECONCILIATION.md) — Current/Frozen 业务语义；Candidate ≠ Verified。
- A5 [RD Instance](../../03_Design/Curis_RD_Workspace_Instance_Spec_v1.md) 顶部 Current Shared Rule Supersession 与 §1a，以及 [RD Closeout](../../03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md)。
- 入口：[AGENTS](../../../AGENTS.md) → [Product Pointer](../../00_Context/PRODUCT_DOCUMENT_POINTER.md)；按其 Current Required Input 消费 Blueprint、Master Map、UI Blueprint、Context 和 [CURRENT_STATE](../../00_Context/CURRENT_STATE.md)。不以 Research/Prototype 反推 Truth。
- 假设：[Zcode Matrix](../system_competitive_research/CURIS_PIXEL_LEVEL_COMPETITIVE_REFERENCE_MATRIX.md)、[Page Reference](../system_competitive_research/CURIS_PAGE_REFERENCE_BLUEPRINT.md)、[Direction](../system_competitive_research/CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md)、[Prototype Review](../../prototypes/full-product-html/CURIS_FULL_PRODUCT_HTML_PROTOTYPE_REVIEW.md)。旧文件保持原样。
- E1–E9：[原始截图目录](../system_competitive_research/evidence/pixel-reference/)。本轮确认 E5 是 **Codex**，不是 ChatGPT 消费端；E8 是**演示视频项目**；E9 是**完整搜索页**，不是 ⌘K 命令浮层。
- H/R 文件名与尺寸、排除理由：[截图索引](evidence/EVIDENCE_INDEX.md)。HTML DOM 数据 JSON 同目录，均为真实读取。
- 受控基线：a9bd736e9affdcf8f5c6b5ad24d5c8dd34dd7809 / 15e081a26ab1e77a3251cc952f06d5b898b9c5cc / 2fabe556993c9d2abc7ee41fe085fce89e4b0128 / 78cacbd0857cc36c9f3fe0e4b11346489993b728。按用户给定 Baseline 消费；未重新冻结。
