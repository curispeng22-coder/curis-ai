# CURIS COMPETITIVE REFERENCE VERIFICATION

Authority Class: RESEARCH / EVIDENCE
Status: Review
Date: 2026-09-13
Disposition: FOR CEO / CHATGPT REVIEW — no Product Authority write

本报告只复核 Zcode 的 Reference 假设，不重新做 Product Authority 审计，也不是旧竞品研究任务的完成声明。Best 表示“在已验证样本中适合此 Curis Surface”，不表示全球唯一最优。

计数口径：Zcode 主矩阵 §3.1–§3.14 共 **133 行**，逐行编号 Z001–Z133。重复专题行保留以便回查，不把 §4 重复清单再加进分母。KEEP 只表示产品/模式选择方向成立；不表示原像素数值、所有交互与 HTML 完成。L0 与 NEED MORE 分开，不能合计成“正确率”。

Replication Level：L0 Original / L1 Pattern / L2 Structure / L3 Interaction / L4 Pixel-level。本报告不用 L1–L6 表示来源等级，以免混淆。来源写 OBSERVED（本轮操作）、PROVENANCE SCREENSHOT（既有原始截图）、SOURCE（本地 HTML）、CURRENT AUTHORITY、INFERRED。

证据索引见末尾；M1–M8 为 Fidelity Audit 测量表。Hxx 是本轮 HTML 截图，Rxx 是本轮竞品截图，E1–E9 是 Zcode 原始实拍（本轮已逐张检查）。

KEEP ZCODE REFERENCE: **53** | REPLACE REFERENCE: **4** | COMBINE: **36** | CURIS ORIGINAL: **18** | NEED MORE EVIDENCE: **22**

| ID / Curis Surface | Zcode Best Ref | Codex Independent Ref | Same? | Evidence | Final Recommendation | Level |
|---|---|---|---|---|---|---|
| Z001 · App Shell 导航轨 (§3.1, line 59) | Linear | Linear | YES（方向） | R16–R18 / E9 | KEEP ZCODE REFERENCE — 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | L3 |
| Z002 · Sidebar 分组计数/折叠 (§3.1, line 60) | Linear | Linear | YES（方向） | R16–R18 / E9 | KEEP ZCODE REFERENCE — 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | L3 |
| Z003 · Context Pane（四Pane左） (§3.1, line 61) | ChatGPT Codex 右栏结构反向用（E5）+ Cursor 文件树（E6） | Curis Context 职责 + Linear 集合导航 | NO | A2 §§2–3 / R17 / H12 | REPLACE REFERENCE — Codex 环境 Inspector 是执行环境与来源，不应反向搬成 Curis 左侧 Context；完整员工档案应在 Utility。 | L2 |
| Z004 · Main Pane (§3.1, line 62) | Linear 行密度 | Linear 行密度；Employee 行服从 Curis | YES（方向） | R17 / E9 / H34 | KEEP ZCODE REFERENCE — 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | L2 |
| Z005 · Utility Pane (§3.1, line 63) | 扣子右栏编辑器（E8） | WorkBuddy 阅读 + Cursor 文档/代码 + Coze 媒体编辑器 | PARTIAL | E1 / R19–R24 | COMBINE — 按对象类型分流：正文阅读、Source/Preview、媒体时间线；不把所有 Utility 做成媒体编辑器。 | L3 |
| Z006 · Floating Assistant (§3.1, line 64) | ChatGPT Classic overlay（库存清单） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z007 · Global Search (§3.1, line 65) | Linear 搜索浮层（E9） | Curis Object Search 浮层合同 + Linear 搜索结果/侧预览 | PARTIAL | R16–R18 / E9 / A2 §2.3.1 | COMBINE — E9 实际是完整搜索页面，不是带 chips 的 ⌘K 浮层；保留类型/选中/预览思想，不能宣称整壳 L4。 | L3 |
| Z008 · Command Palette (§3.1, line 66) | Linear ⌘K（同 E9 家族） | Curis v1 Search；Command Palette 为预留 | L0保留 | A2 §2.3.1 / R18 | CURIS ORIGINAL — 不能把竞品 Command Palette 的派工/开会动作直接加入 v1；下一轮只修 Object Search 的键盘闭环。 | L0 |
| Z009 · Notification (§3.1, line 67) | ChatGPT（任务通知） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z010 · Account Menu (§3.1, line 68) | Claude 左下账户行（E4） | Claude 底部身份与账户入口 | YES（方向） | R06 / E4 | KEEP ZCODE REFERENCE — 位置方向可保留；模型、公司、个人设置分属 Curis 语义，当前账户 menu 全菜单未逐项验证。 | L3 |
| Z011 · Window/Desktop Chrome (§3.1, line 69) | Linear 自定义标题栏（E9 tab 化搜索） | Linear | YES（方向） | R16–R18 / E9 | KEEP ZCODE REFERENCE — 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | L3 |
| Z012 · Empty State (§3.1, line 70) | Claude 空态（E4） | Claude 行动型空态 | YES（方向） | R06 / E4 / H29 | KEEP ZCODE REFERENCE — 保留一个主行动和建议行，降低 L4；CEO 空态需符合公司已创建/未创建的真实阶段，不能照抄品牌欢迎页。 | L3 |
| Z013 · Error State (§3.1, line 71) | Claude 错误横幅（E4） | Claude 分层错误横幅 | YES（方向） | R06 / E4 / H30 | KEEP ZCODE REFERENCE — 标题、影响、Details、自助与上报路径可借；本例为 Gateway 连接失败，不是通用 Agent 失败。不得把 Retry 等同于 Regenerate。 | L3 |
| Z014 · Loading/Working (§3.1, line 72) | WorkBuddy 任务 6 状态（库存） | Cursor 工作摘要 + EvoFlow Running/队列 + Coze 步骤行 | PARTIAL | R19 / R26–R28 / E8 | COMBINE — 只观察到 Coze 演示步骤静态记录；动态运行参考 EvoFlow，语义仍由 Curis Runtime projection 决定。 | L3 |
| Z015 · Brief / Attention (§3.2, line 78) | L0 ORIGINAL；行密度学 Linear（E9） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z016 · Decision (§3.2, line 79) | Claude 错误横幅 anatomy（E4）反用为 Decision Banner | Curis P7 Decision Package | L0保留 | A2 §3.13 / H08 / H31 | CURIS ORIGINAL — Error Banner 不是审批模型；高风险 Layer0 只能查看方案/暂缓，具体 Choice 留 Layer1。 | L0 |
| Z017 · Running Work (§3.2, line 80) | ChatGPT Codex 右栏（E5）+ Cursor 状态摘要 | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector | PARTIAL | R19 / R26–R28 / E5 | COMBINE — E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | L2 |
| Z018 · Latest Result (§3.2, line 81) | WorkBuddy 附件卡网格（E1） | WorkBuddy / Coze 结果引用 → 阅读或编辑面 | YES（方向） | E1 / R22 / R24 / H26–H27 | KEEP ZCODE REFERENCE — 保留对象连续性；Curis Evidence 与员工来源需要额外字段，不可只做卡片导航。 | L3 |
| Z019 · Employee Activity (§3.2, line 82) | ChatGPT 子智能体头像组（E5） | Codex 子智能体头像组（仅静态结构） | YES（方向） | E5；当前原生访问被工具限制 | KEEP ZCODE REFERENCE — 保留头像+计数的紧凑结构，降到 L2；并行生命周期与点击反馈未独立验证，不能作为运行中 L3/L4 验收。 | L2 |
| Z020 · Business List/Card (§3.3, line 88) | Linear Projects 行（E9 右预览的 Project 卡） | Linear 行密度；Employee 行服从 Curis | YES（方向） | R17 / E9 / H34 | KEEP ZCODE REFERENCE — 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | L2 |
| Z021 · Workspace 列表/入口 (§3.3, line 89) | L0+B 代 | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z022 · Workspace Header/导航 (§3.3, line 90) | Linear 顶栏（E9）+ WorkBuddy 面包屑（E1 "Curis/经营/会议工作台"） | Linear | YES（方向） | R16–R18 / E9 | KEEP ZCODE REFERENCE — 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | L3 |
| Z023 · Working Surface (§3.3, line 91) | L0（Four-Pane Frozen） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z024 · Workspace Result (§3.3, line 92) | 扣子右栏编辑器（E8） | WorkBuddy 阅读 + Cursor 文档/代码 + Coze 媒体编辑器 | PARTIAL | E1 / R19–R24 | COMBINE — 按对象类型分流：正文阅读、Source/Preview、媒体时间线；不把所有 Utility 做成媒体编辑器。 | L3 |
| Z025 · 公司版图/部门/团队 (§3.4, line 98) | L0 | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z026 · Employee List / Row (§3.4, line 99) | Linear 行节奏（E9） | Linear 行密度；Employee 行服从 Curis | YES（方向） | R17 / E9 / H34 | KEEP ZCODE REFERENCE — 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | L2 |
| Z027 · Employee Card（目录卡） (§3.4, line 100) | WorkBuddy 专家卡（E2） | Curis Employee Row / Conversation-first Workstation / Utility Detail | L0保留 | A2 §§3.1,3.14 / H12,H14,H34 | CURIS ORIGINAL — 员工目录不是人才市场；Claude Projects 的 instructions/knowledge/chats 配置页不适合作员工默认 Main。 | L0 |
| Z028 · Employee Detail / 工作站 (§3.4, line 101) | Claude Projects 页结构（库存） | Curis Employee Row / Conversation-first Workstation / Utility Detail | L0保留 | A2 §§3.1,3.14 / H12,H14,H34 | CURIS ORIGINAL — 员工目录不是人才市场；Claude Projects 的 instructions/knowledge/chats 配置页不适合作员工默认 Main。 | L0 |
| Z029 · Employee Status (§3.4, line 102) | WorkBuddy/Coze 状态点+文字（E8 步骤行） | Curis 三态 + EvoFlow 员工/工作项/审批分层 | PARTIAL | A2 §3.1 / R11 / H34 | COMBINE — 员工存在与工作完成分开；不要复制 EvoFlow 在岗/自动上班词典或 Coze 步骤完成状态作为 Employee UI 状态。 | L2 |
| Z030 · Current Work（员工卡内） (§3.4, line 103) | ChatGPT 右栏（E5）压缩为行 | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector | PARTIAL | R19 / R26–R28 / E5 | COMBINE — E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | L2 |
| Z031 · Responsibility / Handoff (§3.4, line 104) | L0 ORIGINAL | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z032 · Talent Home (§3.5, line 112) | WorkBuddy 专家·技能·连接器（E2） | WorkBuddy 专家/技能/连接器目录 | YES（方向） | R01,R02 / E2,E3 | KEEP ZCODE REFERENCE — 三目录、场景导购、来源与已装计数方向正确；不混淆已雇员工与可招聘模板。 | L2 |
| Z033 · Employee/Expert Card (§3.5, line 113) | WorkBuddy 专家卡（E2 实测） | WorkBuddy 专家卡 | YES（方向） | R02 / E2 / M1 | KEEP ZCODE REFERENCE — 保留头像/标题/发布者/简介/标签层级；招聘动作与 Curis-ready/Candidate 语义单独适配，Hover 尚未验证。 | L4 |
| Z034 · Expert Detail (§3.5, line 114) | Coze Agent 配置页（库存字段） | WorkBuddy 专家消费详情 + Curis 能力/责任边界 | NO | R02 / E2 / A1 / H17 | REPLACE REFERENCE — 不能把 Coze Agent 配置页的 prompt/model 作为普通用户专家详情主面；高级配置后置。详情交互仍需补测，不提升 L3。 | L2 |
| Z035 · Skill Marketplace (§3.5, line 115) | WorkBuddy SkillHub（E3） | WorkBuddy 专家/技能/连接器目录 | YES（方向） | R01,R02 / E2,E3 | KEEP ZCODE REFERENCE — 三目录、场景导购、来源与已装计数方向正确；不混淆已雇员工与可招聘模板。 | L2 |
| Z036 · Skill Card (§3.5, line 116) | WorkBuddy 技能卡（E3 实测） | WorkBuddy Skill Card | YES（方向） | R01 / E3 / M2 | KEEP ZCODE REFERENCE — 技能卡需更紧凑，首行内联安装；不要复用较高的专家卡。 | L4 |
| Z037 · Skill Detail (§3.5, line 117) | Coze 插件详情（库存） | WorkBuddy 技能消费信息 + EvoFlow 能力概览 | PARTIAL | R01 / R13 | COMBINE — 先说明何时使用/输入输出/来源，再按需看权限与挂载。完整技能详情仍需补证。 | L2 |
| Z038 · Plugin / Connector (§3.5, line 118) | WorkBuddy 连接器 tab（库存+E2 结构） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z039 · Install / Installed / Update (§3.5, line 119) | WorkBuddy 内联 + 与计数（E3） | WorkBuddy 就地安装状态与计数 | YES（方向） | R01 / E3 | KEEP ZCODE REFERENCE — 静态已装/可装态已验证；未执行新技能安装，安装失败/更新链路仍需补测。 | L3 |
| Z040 · Search / Filter / Category (§3.5, line 120) | WorkBuddy chips 行（E2/E3 实测） | WorkBuddy 分类与目录过滤 | YES（方向） | R01,R02 / E2,E3 | KEEP ZCODE REFERENCE — 实际分类为文本/矩形选中面，不支持一律 h28 r14 圆药丸；降低像素复刻声明。 | L3 |
| Z041 · Model Binding (§3.5, line 121) | Coze 节点级模型设置（库存） | Curis Execution Selector + EvoFlow Agent/Model 分层 | PARTIAL | A2 §3.5 / R13 | COMBINE — 员工是公司身份，Model 与 Agent 显性区分；能力绑定不等于某模型绑定。 | L2 |
| Z042 · Capability Binding (§3.5, line 122) | Curis 已实现（Frozen） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z043 · 成果反查导购 (§3.5, line 123) | WorkBuddy 灵感做同款（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z044 · Conversation Layout（任务型） (§3.6, line 129) | WorkBuddy 任务视图（E1） | WorkBuddy 任务型 Conversation | YES（方向） | R04,R05 / E1 | KEEP ZCODE REFERENCE — AI 正文文本流、阶段摘要、结果引用、消息操作相邻；CEO/Meeting 的发言语义不能被任务标题替代。 | L2 |
| Z045 · User Message (§3.6, line 130) | ChatGPT 气泡（库存/标准） | ChatGPT 用户消息气泡 | YES（方向） | R25 DOM EXACT / M6 | KEEP ZCODE REFERENCE — 仅双人对话用户消息：右对齐、浅底、宽度受限；不要复制到所有 Employee/Meeting 发言。 | L4 |
| Z046 · Employee/AI Message (§3.6, line 131) | Claude/ChatGPT 文本流+结构卡 | Claude / ChatGPT AI 正文流 | YES（方向） | R25 / R04 / R13 | KEEP ZCODE REFERENCE — AI 回复不套统一气泡；Curis 保留员工身份行和工作事件。 | L3 |
| Z047 · Message Width / Alignment (§3.6, line 132) | ChatGPT 中心限宽（~48rem 级） | ChatGPT 限宽思想 + Curis 宿主宽度规则 | PARTIAL | R25 / H14 / A2 §3.5 | COMBINE — 一张截图不能推出固定720；Conversation 与 Composer 对齐优先，Context/Utility 打开后宽度需自适应。 | L2 |
| Z048 · File Reference (§3.6, line 133) | WorkBuddy 附件卡（E1 实测） | WorkBuddy 文件附件卡 | YES（方向） | E1 实拍 provenance / M3 | KEEP ZCODE REFERENCE — 两列按可用宽度适配；文件类型/名称截断/meta/打开独立，上传过程与菜单需补测。 | L4 |
| Z049 · Knowledge / Citation (§3.6, line 134) | ChatGPT 来源栏（E5） | Codex 来源列表（静态） | YES（方向） | E5 | KEEP ZCODE REFERENCE — 只借引用集合的折叠结构；浏览器来源/附件不是 Curis Evidence 的完整可信链。 | L2 |
| Z050 · Mention (§3.6, line 135) | WorkBuddy "@引用对话文件，/调用技能"提示（E1 placeholder） | WorkBuddy 语法提示 + EvoFlow @员工/#文件入口 | PARTIAL | R04 / R13 | COMBINE — 提示语不是已实现引用；真实选中资源 chip、移除、不可用态需要实现和验收。 | L2 |
| Z051 · Tool Activity (§3.6, line 136) | Cursor 工具折叠卡（E6/库存） | Cursor 折叠摘要 + EvoFlow 工具逐层展开 | PARTIAL | R13 / R19 / E6 | COMBINE — 先摘要，再具体工具，再输出；不把日志全部永久铺开。 | L3 |
| Z052 · Thinking (§3.6, line 137) | Claude thinking 开关+折叠（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z053 · Plan (§3.6, line 138) | Cursor Plan mode / Devin plan 可编辑（库存） | Curis Work 计划语义 + Cursor 工作摘要 + EvoFlow 工作流分步 | PARTIAL | R08,R19 / A2；Manus 本轮不可用 | COMBINE — 不把普通 Work 变成必须编辑 DAG；计划改写/任务复用仍须补测。 | L2 |
| Z054 · Progress（会话内） (§3.6, line 139) | 扣子步骤行（E8） | Cursor 工作摘要 + EvoFlow Running/队列 + Coze 步骤行 | PARTIAL | R19 / R26–R28 / E8 | COMBINE — 只观察到 Coze 演示步骤静态记录；动态运行参考 EvoFlow，语义仍由 Curis Runtime projection 决定。 | L3 |
| Z055 · Result Reference (§3.6, line 140) | WorkBuddy/扣子 会话内产物卡→右栏（E1/E8） | WorkBuddy / Coze 结果引用 → 阅读或编辑面 | YES（方向） | E1 / R22 / R24 / H26–H27 | KEEP ZCODE REFERENCE — 保留对象连续性；Curis Evidence 与员工来源需要额外字段，不可只做卡片导航。 | L3 |
| Z056 · Artifact (§3.6, line 141) | 扣子视频/音频卡（E8） | Coze 类型化媒体产物 / 编辑器 | YES（方向） | R22–R24 / E8 | KEEP ZCODE REFERENCE — 媒体场景方向正确；E8 是演示，不支持宣称真实多 Agent 生成能力；不覆盖文档/证据阅读。 | L2 |
| Z057 · Error / Retry (§3.6, line 142) | Claude 错误横幅（E4）+ WorkBuddy 重新生成按钮（E1 AX） | Claude 分层错误横幅 | YES（方向） | R06 / E4 / H30 | KEEP ZCODE REFERENCE — 标题、影响、Details、自助与上报路径可借；本例为 Gateway 连接失败，不是通用 Agent 失败。不得把 Retry 等同于 Regenerate。 | L3 |
| Z058 · Branch (§3.6, line 143) | Claude edit→branch（库存） | Cursor Fork + EvoFlow 分叉 | PARTIAL | R13,R28 / Cursor 历史研究截图 | COMBINE — 分叉保留原对象与来源；本轮未新建分支，不升级完整交互结论。 | L2 |
| Z059 · Copy / Actions 行 (§3.6, line 144) | WorkBuddy 消息操作行（E1 实测 AX） | WorkBuddy 消息操作行 | YES（方向） | R04,R05 / E1 / M4 | KEEP ZCODE REFERENCE — 动作贴近当前消息、More 渐进披露；Curis 的交接/升级需要语义 Gate，不是普通分享按钮。 | L4 |
| Z060 · Timestamp (§3.6, line 145) | Cursor "2d ago"（E6） | Cursor 完成时长/相对时间 | YES（方向） | R19,R21 | KEEP ZCODE REFERENCE — 保留已完成摘要与时间；工作完成属于 Work/Turn，不属于员工身份状态。 | L3 |
| Z061 · 成本内联 (§3.6, line 146) | WorkBuddy "共消耗 ◇8.2 ●模型"（E1 实测） | WorkBuddy 成本内联 | YES（方向） | E1 / R04 | KEEP ZCODE REFERENCE — 旧截图有成本，新测试只有模型/时间；按真实 usage 可用性显示，不能把常量成本当完成证据。 | L3 |
| Z062 · Composer Container (§3.7, line 152) | Claude（E4） | Claude Composer 外形与 Add 入口 | YES（方向） | R06,R07 / E4 / M5 | KEEP ZCODE REFERENCE — 参考方向正确，L4 降级：旧20px与圆发送按钮描述不符合实拍，Curis 更完整语义槽位需适配。 | L3 |
| Z063 · Text Area / Placeholder (§3.7, line 153) | Claude（E4） | Claude Composer 外形与 Add 入口 | YES（方向） | R06,R07 / E4 / M5 | KEEP ZCODE REFERENCE — 参考方向正确，L4 降级：旧20px与圆发送按钮描述不符合实拍，Curis 更完整语义槽位需适配。 | L3 |
| Z064 · Attachment (§3.7, line 154) | Claude + 按钮（E4 左下） | Claude Composer 外形与 Add 入口 | YES（方向） | R06,R07 / E4 / M5 | KEEP ZCODE REFERENCE — 参考方向正确，L4 降级：旧20px与圆发送按钮描述不符合实拍，Curis 更完整语义槽位需适配。 | L3 |
| Z065 · File Chip (§3.7, line 155) | WorkBuddy 附件卡缩略（E1）/ ChatGPT chips（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z066 · Context / Reference（@语法） (§3.7, line 156) | WorkBuddy（E1） | WorkBuddy 语法提示 + EvoFlow @员工/#文件入口 | PARTIAL | R04 / R13 | COMBINE — 提示语不是已实现引用；真实选中资源 chip、移除、不可用态需要实现和验收。 | L2 |
| Z067 · Model Selector (§3.7, line 157) | Claude "Claude Opus 4.5 ⌄"（E4）右下内联文字下拉 | Claude 内联模型选择 + 锚定菜单 | YES（方向） | R07 / E4 / M5 | KEEP ZCODE REFERENCE — 保留内联标签/chevron/就近菜单/当前选中标记；不复制 Gateway 自定义模型目录。 | L4 |
| Z068 · Agent/Employee Selector (§3.7, line 158) | Curis Frozen"执行·<Agent>"槽位；UI 型=WorkBuddy 专家选择 | Curis Execution Selector + EvoFlow Agent/Model 分层 | PARTIAL | A2 §3.5 / R13 | COMBINE — 员工是公司身份，Model 与 Agent 显性区分；能力绑定不等于某模型绑定。 | L2 |
| Z069 · Mode Selector (§3.7, line 159) | WorkBuddy"有用操作"chip（E1） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z070 · Permission Selector (§3.7, line 160) | WorkBuddy "⚠允许完全访问"琥珀 chip（E1）/ ChatGPT 红字完全访问（E5） | WorkBuddy 就地权限 + EvoFlow requested/configured/effective 分层 | PARTIAL | R12,R13 / A2 §3.5 | COMBINE — 就地可见档位 + 安全中心生效状态；完全访问不等于已启用沙箱，不用颜色替代解释。 | L3 |
| Z071 · Send (§3.7, line 161) | Claude 32 圆 + WorkBuddy 28 圆（E4/E1） | Claude 圆角方形禁用按钮 + WorkBuddy 圆形按钮 | PARTIAL | R06 / E4 / R04 | COMBINE — 参考不是统一32圆；选 Curis 自己的共享按钮形状，保留空输入禁用与同位 Stop。 | L3 |
| Z072 · Stop / Running (§3.7, line 162) | WorkBuddy 内联 spinner（E1 发送键位左侧） | WorkBuddy Send/Stop 与空输入禁用 | YES（方向） | R04 / 新任务空输入与本轮 Stop 操作 | KEEP ZCODE REFERENCE — 操作方向正确；HTML 发送不追加消息和空输入可发送需先修。 | L3 |
| Z073 · Queue / Steering (§3.7, line 163) | Cursor queue/steer（库存） | EvoFlow Running 时排队提示 + Cursor 补充指令 | PARTIAL | R26 / R19–R21 | COMBINE — 观察到可输入与 Enter 排队提示；本轮未真正排队执行，queue 与 steer 不等同，后续验收需分别测试。 | L3 |
| Z074 · Disabled (§3.7, line 164) | WorkBuddy 发送 disabled（E1 AX 证实） | WorkBuddy Send/Stop 与空输入禁用 | YES（方向） | R04 / 新任务空输入与本轮 Stop 操作 | KEEP ZCODE REFERENCE — 操作方向正确；HTML 发送不追加消息和空输入可发送需先修。 | L3 |
| Z075 · Multi-line / Keyboard (§3.7, line 165) | ChatGPT/Cursor 标准 | ChatGPT / Cursor 多行输入与键盘 | YES（方向） | R25 / H14–H15 / Cursor 已有研究 | KEEP ZCODE REFERENCE — HTML 换行与发送需要补闭环；不能仅凭 textarea 判多行扩展完成。 | L3 |
| Z076 · Drag & Drop (§3.7, line 166) | ChatGPT/Claude 标准 | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z077 · Start (§3.8, line 174) | L0（Work 由责任/会议/对话发起） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z078 · Plan (§3.8, line 175) | Cursor Plan mode + Devin plan 可编辑（库存） | Curis Work 计划语义 + Cursor 工作摘要 + EvoFlow 工作流分步 | PARTIAL | R08,R19 / A2；Manus 本轮不可用 | COMBINE — 不把普通 Work 变成必须编辑 DAG；计划改写/任务复用仍须补测。 | L2 |
| Z079 · Todo (§3.8, line 176) | Manus todo 第一公民（库存） | Curis Work 计划语义 + Cursor 工作摘要 + EvoFlow 工作流分步 | PARTIAL | R08,R19 / A2；Manus 本轮不可用 | COMBINE — 不把普通 Work 变成必须编辑 DAG；计划改写/任务复用仍须补测。 | L2 |
| Z080 · Current Step / Activity (§3.8, line 177) | ChatGPT 右栏 + Cursor 状态摘要（E5/E6） | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector | PARTIAL | R19 / R26–R28 / E5 | COMBINE — E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | L2 |
| Z081 · Tool Call (§3.8, line 178) | Cursor 工具折叠+Review（库存） | Cursor 折叠摘要 + EvoFlow 工具逐层展开 | PARTIAL | R13 / R19 / E6 | COMBINE — 先摘要，再具体工具，再输出；不把日志全部永久铺开。 | L3 |
| Z082 · Subtask / Multi-Agent (§3.8, line 179) | ChatGPT 子智能体头像组"3 完成"（E5） | Codex 子智能体头像组（仅静态结构） | YES（方向） | E5；当前原生访问被工具限制 | KEEP ZCODE REFERENCE — 保留头像+计数的紧凑结构，降到 L2；并行生命周期与点击反馈未独立验证，不能作为运行中 L3/L4 验收。 | L2 |
| Z083 · Delegation (§3.8, line 180) | L0（Leader 分工） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z084 · Steering (§3.8, line 181) | Cursor queue/steer（库存） | EvoFlow Running 时排队提示 + Cursor 补充指令 | PARTIAL | R26 / R19–R21 | COMBINE — 观察到可输入与 Enter 排队提示；本轮未真正排队执行，queue 与 steer 不等同，后续验收需分别测试。 | L3 |
| Z085 · Permission (§3.8, line 182) | WorkBuddy 四级审批（库存）+ Cursor Run Modes（库存） | WorkBuddy 就地权限 + EvoFlow requested/configured/effective 分层 | PARTIAL | R12,R13 / A2 §3.5 | COMBINE — 就地可见档位 + 安全中心生效状态；完全访问不等于已启用沙箱，不用颜色替代解释。 | L3 |
| Z086 · Pause / Stop / Retry / Failure / Recovery (§3.8, line 183) | WorkBuddy 任务 6 状态机（库存） | Cursor 中断续作 + 明示恢复边界 | NO | Cursor 20260910 interrupted/resumed-result；R26–R28 为 EvoFlow 反例 | REPLACE REFERENCE — 替换单一 WorkBuddy 自动化记忆引用。EvoFlow 停止后丢弃未完成输出，不可列最佳恢复。原生重启恢复本轮未重测。 | L2 |
| Z087 · Completion (§3.8, line 184) | Cursor "Worked for 14m"摘要（库存） | Cursor 完成时长/相对时间 | YES（方向） | R19,R21 | KEEP ZCODE REFERENCE — 保留已完成摘要与时间；工作完成属于 Work/Turn，不属于员工身份状态。 | L3 |
| Z088 · Resume (§3.8, line 185) | WorkBuddy 自动化执行记忆（本地证据） | Cursor 中断续作 + 明示恢复边界 | NO | Cursor 20260910 interrupted/resumed-result；R26–R28 为 EvoFlow 反例 | REPLACE REFERENCE — 替换单一 WorkBuddy 自动化记忆引用。EvoFlow 停止后丢弃未完成输出，不可列最佳恢复。原生重启恢复本轮未重测。 | L2 |
| Z089 · Agent 工作右栏（骨架） (§3.8, line 186) | ChatGPT Codex"环境信息"栏（E5 实测） | Cursor 当前工作摘要 + EvoFlow 会话状态；Codex 环境信息仅辅助 Inspector | PARTIAL | R19 / R26–R28 / E5 | COMBINE — E5 的 Git ± 行数不是工作进度，3完成不是当前运行证据；将目标/当前动作/等待/结果放首层，环境与来源放次层。 | L2 |
| Z090 · Result Card（会话内） (§3.9, line 192) | WorkBuddy 附件卡 / 扣子交付卡（E1/E8） | WorkBuddy 文件卡 + Coze 类型化交付卡 | PARTIAL | E1 / R22 / H26,H27 | COMBINE — 按 Result 类型区分，Evidence/UsedBy 属 Curis；不能用一个L4卡覆盖所有文档/代码/音视频。 | L3 |
| Z091 · Result Row（列表） (§3.9, line 193) | Linear 结果行（E9） | Linear 行密度；Employee 行服从 Curis | YES（方向） | R17 / E9 / H34 | KEEP ZCODE REFERENCE — 采用可扫描行与选中反馈；Curis 两行责任语义不能强压为单行 Issue。 | L2 |
| Z092 · Preview (§3.9, line 194) | Cursor Preview⇄Source（E6） | Cursor Preview/Source/最大化与 Follow-up | YES（方向） | R19–R21 / M8 | KEEP ZCODE REFERENCE — 交互已复核；Pane 宽度与宿主随用户布局变化，降 L4 为 L3。HTML 标签不切换内容不是复刻。 | L3 |
| Z093 · Artifact Panel（富产物） (§3.9, line 195) | 扣子右栏编辑器（E8） | Coze 类型化媒体产物 / 编辑器 | YES（方向） | R22–R24 / E8 | KEEP ZCODE REFERENCE — 媒体场景方向正确；E8 是演示，不支持宣称真实多 Agent 生成能力；不覆盖文档/证据阅读。 | L2 |
| Z094 · Evidence / Citation (§3.9, line 196) | L0 ORIGINAL（呈现学 ChatGPT 来源栏 E5） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z095 · Version (§3.9, line 197) | Claude Artifacts 版本（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z096 · Download / Export (§3.9, line 198) | WorkBuddy 分享/打开所在文件夹（E1 AX） | WorkBuddy 阅读器与文件动作 | YES（方向） | E1 | KEEP ZCODE REFERENCE — 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | L3 |
| Z097 · Continue Working / Ask Employee (§3.9, line 199) | Cursor follow-up composer（E6） | Cursor Preview/Source/最大化与 Follow-up | YES（方向） | R19–R21 / M8 | KEEP ZCODE REFERENCE — 交互已复核；Pane 宽度与宿主随用户布局变化，降 L4 为 L3。HTML 标签不切换内容不是复刻。 | L3 |
| Z098 · Open Utility (§3.9, line 200) | Curis Frozen 模式；实现参照 E1/E8 | WorkBuddy / Coze 结果引用 → 阅读或编辑面 | YES（方向） | E1 / R22 / R24 / H26–H27 | KEEP ZCODE REFERENCE — 保留对象连续性；Curis Evidence 与员工来源需要额外字段，不可只做卡片导航。 | L3 |
| Z099 · Knowledge Home (§3.10, line 206) | Claude Projects knowledge（库存）+D 代 | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z100 · File Row (§3.10, line 207) | Linear Document 行（E9） | Linear 文件行密度 | YES（方向） | R17 / E9 / H33 | KEEP ZCODE REFERENCE — Curis 有来源/范围/引用计数，两行模型合理，但不能宣称复制36px单行 L4。 | L3 |
| Z101 · Reading Surface (§3.10, line 208) | WorkBuddy 右栏 markdown 阅读器（E1 实测） | WorkBuddy 阅读器与文件动作 | YES（方向） | E1 | KEEP ZCODE REFERENCE — 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | L3 |
| Z102 · Reference / Used By (§3.10, line 209) | L0（反向引用独有） | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z103 · Search / Filter (§3.10, line 210) | Linear 搜索浮层（E9） | Curis Object Search 浮层合同 + Linear 搜索结果/侧预览 | PARTIAL | R16–R18 / E9 / A2 §2.3.1 | COMBINE — E9 实际是完整搜索页面，不是带 chips 的 ⌘K 浮层；保留类型/选中/预览思想，不能宣称整壳 L4。 | L3 |
| Z104 · Detail 元数据 (§3.10, line 211) | WorkBuddy 面板头部（E1） | WorkBuddy 阅读器与文件动作 | YES（方向） | E1 | KEEP ZCODE REFERENCE — 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | L3 |
| Z105 · Meeting 全部（列表/房间/议程/决议） (§3.11, line 217) | L0 ORIGINAL | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z106 · 参会者头像/说话人 (§3.11, line 218) | 会议软件通用（L1） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z107 · 纪要/转写 (§3.11, line 219) | Manus Meeting Minutes（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z108 · Proposal→Decision 卡 (§3.11, line 220) | 3.2 Decision 行（E4 anatomy） | Curis P7 Decision Package | L0保留 | A2 §3.13 / H08 / H31 | CURIS ORIGINAL — Error Banner 不是审批模型；高风险 Layer0 只能查看方案/暂缓，具体 Choice 留 Layer1。 | L0 |
| Z109 · 洞察语义（Analyst/归因/Decision support） (§3.12, line 226) | L0 ORIGINAL | Curis Current Authority | L0保留 | A1 / A2 / A4 / A5 | CURIS ORIGINAL — 保持 Company OS、责任、组织、工作与证据语义；竞品只提供通用控件，不能接管对象模型。 | L0 |
| Z110 · Metric/Chart 视觉 (§3.12, line 227) | Linear/Notion 图表语言（L1） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z111 · Cost/Usage 视图 (§3.12, line 228) | 扣子积分页（E7 实测）：总积分+三分拆+套餐倍率 | Coze 用量拆分（仅结构） | YES（方向） | E7 / R24免费版 | KEEP ZCODE REFERENCE — 只借总量与来源拆分；充值套餐/倍率不等于 Curis 员工/业务成本归因。 | L2 |
| Z112 · Report 阅读 (§3.12, line 229) | WorkBuddy 右栏阅读器（E1） | WorkBuddy 阅读器与文件动作 | YES（方向） | E1 | KEEP ZCODE REFERENCE — 保留阅读正文、顶部文件动作和打开关系；导出/下载本轮未执行，不作为功能成功证据。 | L3 |
| Z113 · Settings Shell / Navigation (§3.13, line 237) | Cursor Settings（库存：General/Agents/Tab/Rules&Memories/Models/MCP/Privacy/Account/Shortcuts/Updates 左栏） | Cursor 设置壳 + EvoFlow 生效状态分层 | PARTIAL | R29 / R12 / H22 | COMBINE — 左类右容、设置搜索与分组；Cursor 当前 MCP/Skills 已迁到 Customize，不能照库存旧 IA 全搬。 | L3 |
| Z114 · Account / Appearance (§3.13, line 238) | Claude Appearance（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z115 · Model 列表 / Model Row (§3.13, line 239) | Cursor Models 设置（库存：双池+逐模型开关+计价） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z116 · Provider / 凭据 (§3.13, line 240) | WorkBuddy 自定义模型本地 Key（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z117 · Skill (§3.13, line 241) | Cursor Customize（库存） | Cursor Customize + EvoFlow 能力概览 | PARTIAL | R29迁移提示 / R13的Skills/Tools/Knowledge/MCP | COMBINE — 参考安装/启用/绑定/运行健康的区别；完整MCP配置界面本轮未验，禁止标完整L3。 | L2 |
| Z118 · MCP (§3.13, line 242) | Cursor MCP 配置（库存：URL/command/OAuth/插值逐字段） | Cursor Customize + EvoFlow 能力概览 | PARTIAL | R29迁移提示 / R13的Skills/Tools/Knowledge/MCP | COMBINE — 参考安装/启用/绑定/运行健康的区别；完整MCP配置界面本轮未验，禁止标完整L3。 | L2 |
| Z119 · Permission (§3.13, line 243) | Cursor Agents→Approvals & Execution（库存：三档+permissions.json 自然语言规则+sandbox） | WorkBuddy 就地权限 + EvoFlow requested/configured/effective 分层 | PARTIAL | R12,R13 / A2 §3.5 | COMBINE — 就地可见档位 + 安全中心生效状态；完全访问不等于已启用沙箱，不用颜色替代解释。 | L3 |
| Z120 · Memory (§3.13, line 244) | Claude Memory（库存：逐条查看/编辑/删除/Pause/Reset/导入导出） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z121 · Notification (§3.13, line 245) | ChatGPT Notifications（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z122 · Usage / Cost (§3.13, line 246) | 扣子积分页（E7 实测） + Claude usage ring（库存） | Coze 用量拆分（仅结构） | YES（方向） | E7 / R24免费版 | KEEP ZCODE REFERENCE — 只借总量与来源拆分；充值套餐/倍率不等于 Curis 员工/业务成本归因。 | L2 |
| Z123 · Shortcut (§3.13, line 247) | Cursor Shortcuts（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z124 · Developer / About (§3.13, line 248) | Cursor（hooks/Updates） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z125 · Navigation (§3.14, line 254) | Linear（E9） | Linear 分组导航节奏 | YES（方向） | R16–R18 / E9 / M7 | KEEP ZCODE REFERENCE — 仅视觉节奏参考；冻结七区与 T1 控制优先。截图估测，不认可 Zcode 原逻辑像素值。 | L4 |
| Z126 · Sidebar (§3.14, line 255) | Linear（E9）+ WorkBuddy 计数（E1） | Linear 分组导航节奏 | YES（方向） | R16–R18 / E9 / M7 | KEEP ZCODE REFERENCE — 仅视觉节奏参考；冻结七区与 T1 控制优先。截图估测，不认可 Zcode 原逻辑像素值。 | L4 |
| Z127 · Pane 结构 (§3.14, line 256) | Cursor Agents 三 pane（E6）+ 扣子会话/编辑器（E8） | Cursor 自适应 Pane + Coze 类型化编辑器 | PARTIAL | R19–R24 / A2 | COMBINE — 保留分栏/最大化思想，Curis T1–T3/resize/记忆范围优先；不固定230/380或四列常驻。 | L2 |
| Z128 · Inspector/Utility (§3.14, line 257) | 扣子（E8） | WorkBuddy 阅读 + Cursor 文档/代码 + Coze 媒体编辑器 | PARTIAL | E1 / R19–R24 | COMBINE — 按对象类型分流：正文阅读、Source/Preview、媒体时间线；不把所有 Utility 做成媒体编辑器。 | L3 |
| Z129 · Search (§3.14, line 258) | Linear 浮层（E9） | Curis Object Search 浮层合同 + Linear 搜索结果/侧预览 | PARTIAL | R16–R18 / E9 / A2 §2.3.1 | COMBINE — E9 实际是完整搜索页面，不是带 chips 的 ⌘K 浮层；保留类型/选中/预览思想，不能宣称整壳 L4。 | L3 |
| Z130 · Command Palette (§3.14, line 259) | Linear ⌘K | Curis v1 Search；Command Palette 为预留 | L0保留 | A2 §2.3.1 / R18 | CURIS ORIGINAL — 不能把竞品 Command Palette 的派工/开会动作直接加入 v1；下一轮只修 Object Search 的键盘闭环。 | L0 |
| Z131 · Floating Surface / Quick Entry (§3.14, line 260) | ChatGPT Classic Option-Space（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z132 · Notification (§3.14, line 261) | Devin Slack 三按钮深链（库存） | 暂不指定唯一 Best | UNVERIFIED | Zcode 库存描述；本轮无对应完整交互证据 | NEED MORE EVIDENCE — 保留假设，不进入可执行复刻输入；须补目标 Surface 与关键状态实拍。 | 待定 |
| Z133 · Window Chrome (§3.14, line 262) | Linear 自定义标题栏（E9） | Linear | YES（方向） | R16–R18 / E9 | KEEP ZCODE REFERENCE — 保留分组、缩进、历史与 Pane-local 导航；不复制团队/Issue IA，宽度服从 Frozen Shell。 | L3 |

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
