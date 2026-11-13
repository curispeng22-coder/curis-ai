# CURIS PIXEL-LEVEL COMPETITIVE REFERENCE MATRIX

> Authority Class: RESEARCH / EVIDENCE — Final UI Master 的设计 Reference Map（不构成 Product Authority，不修改任何 Frozen 文档）
> Status: COMPLETE — STOP FOR CEO / CHATGPT REVIEW（本报告完成后不自行开始 Final UI Master）
> Date: 2026-09-12
> 消费：20 份既有研究交付物（Gap/Settings/九矩阵/UI Audit/Problem Register/Direction/各 FUNCTION_INVENTORY），不重复功能研究；本报告只回答：**具体抄谁、抄哪一部分、抄到什么程度。**
> 核心验收标准：明天开始重画 Curis Final UI Master 时，每一个页面、每一个重要组件，都能打开指定的竞品截图作为 Reference。

---

## 0. 真实视觉证据（本机实拍，非文档转述）

本机已装 WorkBuddy / ChatGPT(Codex) / Claude / Cursor / Linear / 扣子 / ZCode，以下截图为窗口级实拍（Retina 2x，文中尺寸均为逻辑 px，全部标 APPROXIMATE）：

| # | 证据 | 路径（`evidence/pixel-reference/`） | 覆盖 Surface |
|---|---|---|---|
| E1 | WorkBuddy 任务会话主窗 | `workbuddy/01-main-window.png` | Composer 全槽位 / 消息操作行 / 附件卡 2 列网格 / 成本内联（"共消耗 ◇8.2"）/ 右侧 Utility 文件阅读面板（tabs+全屏+收起） |
| E2 | WorkBuddy 专家中心 | `workbuddy/02-expert-center.png` | 三 tab 分段（专家/技能/连接器）/ 精选场景卡轮播 / 专家·专家团切换 / 综合·最热·最新排序 / 分类 chips 行 / 4 列专家卡网格（含"特邀专家"徽标、"OPC·一人公司"分类） |
| E3 | WorkBuddy 技能市场 | `workbuddy/03-skill-market.png` | 精选技能 / 推荐·SkillHub·套件 / 技能卡（icon+名+内联 + 安装）/ "我安装的 59" 计数 / 添加技能主按钮 / 换一换 |
| E4 | Claude Cowork 空态 | `claude/01-main-composer.png` | 空态（"You're here!" + Ideas 建议行）/ Composer 卡片（+、模型选择、发送）/ "Project or folder" 行 / 错误横幅（标题+解释+Details+两按钮） |
| E5 | ChatGPT(Codex) 主窗 | `chatgpt/01-main-window.png` | 右侧 Agent 工作栏（环境信息：变更 +363,408/-19,138、分支、子智能体"3 完成"头像组、来源列表）/ 用量耗尽卡（就地 + Add Credits）/ Composer（+、⚠完全访问、模型、语音）/ 侧栏（定时任务/插件/项目分组） |
| E6 | Cursor Agents 窗 | `cursor/01-agents-window.png` | 三 pane（导航/会话/结果面板 Browser·Changes·RESULT.md）/ Preview·Source 切换 / Follow-up Composer / "This Mac" 机器选择器 |
| E7 | 扣子 订阅/积分页 | `coze/01-main-window.png` | 总积分/订阅积分/增购积分/活动积分拆分、套餐卡（积分倍率徽标）、侧栏"积分剩余 100%"环 |
| E8 | 扣子 项目工作面 | `coze/02-agent-workspace.png` | 会话内交付卡（视频卡/音频卡/步骤✓行"交付最终工程文件"）/ 右侧 Utility=完整媒体编辑器（项目文件树+搜索+筛选 chips+播放器+工具栏+时间线双轨） |
| E9 | Linear 全局搜索 | `linear/01-search-cmdk.png` | 搜索浮层（输入+类型 chips All/Issues/Projects/Documents+分组结果+右侧预览 Property 行）/ 侧栏分组导航 / 自定义标题栏 tab |

---

## 1. Replication Level 定义

| 级别 | 含义 | 边界 |
|---|---|---|
| **L0 CURIS ORIGINAL** | Curis 独有核心，不能复制竞品 | Company OS / Responsibility / Leader / CEO Decision / 组织经营关系等 |
| **L1 PATTERN ONLY** | 只学模式，不复制视觉 | — |
| **L2 STRUCTURE REPLICATION** | 可复刻信息结构/布局逻辑/字段组织/交互顺序；视觉 Curis 化 | — |
| **L3 INTERACTION REPLICATION** | 可高度复刻交互/状态/操作位置/展开方式/菜单行为/键盘 | — |
| **L4 PIXEL-LEVEL REPLICATION** | 通用成熟组件可接近像素级复刻（geometry/spacing/density/radius/alignment/states/anatomy） | 禁止复制对方 Logo/商标/品牌插画/专有 icon/版权素材；最终套 Curis Token/Typography/Accent/Icon |

## 2. 实测设计 token 摘要（来自 E1–E9，APPROXIMATE）

**WorkBuddy（深色）**：画布 `#111214`，卡片面 `#1B1D21`，边框 `#2A2D33`，主文字 `#E5E7EB`，次文字 `#9CA3AF`；卡片 radius 12 / chips h28 r14 / 分段 active `#2A2D33` r8 / 专家卡 ~370×190 padding16 / 头像 40 / Composer r16 minH76 / 发送键 28 圆 / 消息操作 icon16 gap12 / 危险·授权 chip 琥珀 `#D9A045`。
**Claude（暖浅色）**：画布 `#F5F4EE`，面 `#FFFFFF`，边框 `#E3E2DC`，主文字 `#1A1A17`，次 `#57564F`，占位 `#B0AEA5`；侧栏 ~215 / Composer 卡 ~532 宽 r16 shadow `0 1 3 rgba(0,0,0,.05)` / 占位 20px / 发送键 32 圆 `#EDECE6` / 错误横幅 bg `#F2DCA4` r8 / Ideas 行 h36 icon20。
**ChatGPT（冷浅色）**：侧栏 ~200 `#F9F9F9`，行 h32 字 14；右 Agent 栏 ~370 卡 r12 边框 `#E6E6E6`；变更数 mono 13 红 `#E02E2A` 绿成功色；用量卡全宽 r12 + 黑色 pill 按钮 h32；Composer r16 占位 16。
**Cursor（浅灰）**：三 pane 左 ~230 `#F8F8F8`；行 h28 字 13；Preview/Source 药丸分段；Composer r12；机器选择器 footer 字 13。
**扣子（浅色）**：积分大数 32/600，拆分列 24；套餐卡 ~300 r12 边框 `#ECECEC`；价 28/700；侧栏积分环 + 套餐徽标；会话交付卡 r12 bg `#F6F4EC`；右侧编辑器全高，时间线轨道 label 13。
**Linear（浅灰）**：侧栏 ~215，组标签 11 大写 `#8C8C8C`，行 h28 字 13；搜索浮层宽 ~640 输入 h48 字16，类型 chips h28（active 深底白字），结果行 h36（类型列 w80 字12 灰）；右预览 ~380，Property 行字 13 彩色 icon。

---

## 3. 主矩阵：Curis Surface → Best Reference

> 列：Surface | 当前状态 | 当前问题 | Best Reference | Secondary | 参考具体 Surface | 为什么最好 | 级别 | Curis Adaptation
> "1.5代"现状说明：Curis 当前状态引用 UI Audit（A/B/C/D 代）与 Gap Matrix。

### 3.1 GLOBAL / DESKTOP

| Surface | 当前状态 | 当前问题 | Best Ref | Secondary | 参考具体 Surface | 为什么最好 | 级别 | Curis Adaptation |
|---|---|---|---|---|---|---|---|---|
| App Shell 导航轨 | D 代六区合规；C 代仅 4 项 | 四套 IA 并存 | **Linear** | Cursor Agents 窗 | E9 侧栏：组标签 11 大写灰、行 h28、子项缩进、团队分组 | 桌面密度与分组的行业标杆；七区可直接映射 | L2+L3 | 七区分组（工作区/组织与运营）+ 设置入口；token 化 |
| Sidebar 分组计数/折叠 | 无 | 无折叠 | Linear | WorkBuddy（任务(7)/空间(4) 计数） | E1 侧栏计数徽标 | 计数即注意力 | L3 | 用于待处理/运行中计数 |
| Context Pane（四Pane左） | D 代骨架 | 标签堆叠 | **ChatGPT Codex 右栏结构反向用**（E5）+ Cursor 文件树（E6） | D 代 01 页 | E5"环境信息"卡：分节（变更/分支/子智能体/来源）+ 每节 + 号 | 分节+可展开是 Context 面的正确 anatomy | L2 | 节=最近工作/业务列表/待处理筛选（D 代已定义） |
| Main Pane | B/D 代合规 | 密度节奏缺失 | Linear 行密度 | — | E9 列表行 h36±4 | 安静高密度标杆 | L1 | Domain Surface 结构 L0 不动 |
| Utility Pane | 薄壳 | 无元数据/无编辑 | **扣子右栏编辑器**（E8） | WorkBuddy 文件面板（E1） | E8：Utility=全高编辑器（文件树+预览+工具栏+时间线）；E1：tabs+全屏+收起+TOC | "点开对象→Utility 变成工作台"的活证据，正合 Curis Frozen Result→Utility | L3 | Result/资料/对象详情均按此深度 |
| Floating Assistant | Phase B 可拖浮层 | 面内是报表不是对话 | ChatGPT Classic overlay（库存清单） | Claude Quick Entry | ChatGPT 清单 §desktop：Option-Space 全局浮层 | 系统级唤起+任意上下文 | L2 | 浮层内容=对话+Composer（见 3.7），禁统计卡 |
| Global Search | NOT IMPLEMENTED（D 代骨架） | 无 | **Linear 搜索浮层**（E9） | WorkBuddy ⌘F 会话内搜索 | E9：输入+类型 chips+分组结果+右侧预览 | 类型过滤+预览的搜索是对象型产品最佳实践 | **L4** | 类型=员工/业务/工作空间/结果/资料/会议；预览用 Curis Property 行 |
| Command Palette | 无 | 无 | Linear ⌘K（同 E9 家族） | Cursor 命令面板 | E9 同型 | 与搜索同壳，降低学习成本 | L3 | 动作区：新建工作/派工作/开会 |
| Notification | 仅 CEO Desk 投影 | 无中心 | ChatGPT（任务通知） | Devin Slack | 库存清单字段 | 全员标配形态接近 | L2 | 分四类：结果就绪/需决定/阻塞/会议 |
| Account Menu | 左下身份 chip | 无菜单 | Claude 左下账户行（E4） | WorkBuddy curis 行（E1） | E4："yy · Gateway ⌃"行+弹出 | 底部账户行已是最优位置（Curis 已同位） | L3 | 弹出：个人设置/公司设置/模型/退出 |
| Window/Desktop Chrome | 原生壳 | 无桌面感 | Linear 自定义标题栏（E9 tab 化搜索） | — | E9 标题栏内嵌搜索 tab | 轻量桌面感 | L2 | 暂用原生；标题栏放全局搜索入口 |
| Empty State | 零值仪表盘 | 后台感 | **Claude 空态**（E4） | — | E4：品牌问候+一句 placeholder+Ideas 3 行 | 空态=主行动+叙事的教科书 | **L4** | 禁统计卡；Ideas→Curis 建议行动 |
| Error State | 全屏裸错误+英文 | 无解释无路径 | **Claude 错误横幅**（E4） | — | E4：标题+解释+Details+Copy report/Check again | 解释/自助/上报三路径齐全 | **L4** | 中文文案+重试/返回/求助 |
| Loading/Working | 无规范 | — | WorkBuddy 任务 6 状态（库存） | Coze 步骤✓（E8） | E8 步骤行 ○→✓ | 轻量过程反馈 | L3 | 状态词典见 3.9 |

### 3.2 CEO DESK

| Surface | 当前状态 | 当前问题 | Best Ref | Secondary | 参考具体 Surface | 为什么最好 | 级别 | Curis Adaptation |
|---|---|---|---|---|---|---|---|---|
| Brief / Attention | 空态六卡重复 | 无优先级 | **L0 ORIGINAL**；行密度学 Linear（E9） | Claude Ideas 行式（E4） | — | 注意力模型是 Curis 核心 | L0 + L1 | 简报行=事实+影响+来源员工+动作 |
| Decision | 有 P7 包概念 | 无卡形态 | Claude 错误横幅 anatomy（E4）反用为 Decision Banner | Linear property 行 | E4 分层：标题/解释/动作组 | 需要决策的信息 anatomy 通用 | L2 | P7 包：背景/选项/建议/Evidence 引用 |
| Running Work | 无投影 | 最大缺口 | **ChatGPT Codex 右栏**（E5）+ Cursor 状态摘要 | WorkBuddy 任务行（E1） | E5：子智能体头像+"3 完成"；变更数即工作量 | 运行中工作"一眼可读"的形态 | L2 | 行=员工+Work+当前动作+进度（见 3.9） |
| Latest Result | 无 | — | WorkBuddy 附件卡网格（E1） | Coze 交付卡（E8） | E1 查看所有产物(7) 入口+卡片 | 结果以产物卡出现 | L3 | Result 行→点开 Utility |
| Employee Activity | 无 | — | ChatGPT 子智能体头像组（E5） | — | E5 | 头像组=多人活动的最密表达 | L2 | 员工头像+状态点 |

### 3.3 BUSINESS / WORKSPACE

| Surface | 当前状态 | 当前问题 | Best Ref | Secondary | 参考具体 Surface | 为什么最好 | 级别 | Curis Adaptation |
|---|---|---|---|---|---|---|---|---|
| Business List/Card | 后台目录+0 卡 | 空态错 | Linear Projects 行（E9 右预览的 Project 卡） | — | E9：Project 类型行+预览卡（icon/名/描述/Property 行） | 项目卡字段节奏可平移 | L2 | 业务卡=名+状态+本周一句话+Workspace 数 |
| Workspace 列表/入口 | B 代对 | — | L0+B 代 | Linear 侧栏 team 子项（E9） | — | 空间进入感 | L0/L1 | — |
| Workspace Header/导航 | 面包屑挤压换行 | 断裂 | Linear 顶栏（E9）+ WorkBuddy 面包屑（E1 "Curis/经营/会议工作台"） | — | E1 面包屑 h44 不换行 | 面包屑+Surface tabs 共存样本 | L3 | Surface tabs（总览/研究/内容…）保持 B 代 |
| Working Surface | D 代合规 | 密度 | L0（Four-Pane Frozen） | — | — | 结构不动 | L0 | — |
| Workspace Result | 无消费面 | — | **扣子右栏编辑器**（E8） | Cursor Preview/Source（E6） | E8 全高编辑；E6 文档 Preview⇄Source | 产物消费两档：轻预览/重编辑 | L3 | 文档类走 E6 型；媒体/富产物走 E8 型 |

### 3.4 ORGANIZATION

| Surface | 当前状态 | 当前问题 | Best Ref | Secondary | 参考具体 Surface | 为什么最好 | 级别 | Curis Adaptation |
|---|---|---|---|---|---|---|---|---|
| 公司版图/部门/团队 | 已验收两 Tab | — | L0 | — | — | 组织结构独有 | L0 | — |
| Employee List / Row | D 代两行结构合规 | 无实例页证据 | Linear 行节奏（E9） | WorkBuddy 场景卡专家行（E2） | E2 场景卡内 avatar24+名13 行 | 两行结构+行节奏 | L3（视觉） | 字段=Frozen（头像/姓名+岗位/当前职责/状态） |
| Employee Card（目录卡） | 无 | 无脸面 | **WorkBuddy 专家卡**（E2） | — | E2：avatar40+名15+发布者12+两行简介13+3 tags | 普通用户可读性最强的成员卡 | **L4** | tag→当前责任关键词；发布者→部门·Role |
| Employee Detail / 工作站 | 无（Current P1） | 最大缺口 | Claude Projects 页结构（库存） | WorkBuddy 专家详情+D 代骨架 | 库存：header/instructions/knowledge/chats 分区 | 单对象"身份+配置+活动"分区结构 | L2 | 分区=身份/责任/能力/当前工作/最近结果/对话/设置（Direction §2.5） |
| Employee Status | 状态 chip 漂移 | 词典乱 | **WorkBuddy/Coze 状态点+文字**（E8 步骤行） | — | E8：○/✓ 圈+灰字 | 小面积状态信号规范 | L3 | 三态：空闲/工作中·<desc>/阻塞·<cause>（Frozen） |
| Current Work（员工卡内） | 无 | — | ChatGPT 右栏（E5）压缩为行 | — | E5 | 当前动作+进度的行化 | L2 | 一行：Work 名+当前动作+进度 |
| Responsibility / Handoff | Runtime 有 | 无面 | **L0 ORIGINAL** | Devin Playbook 五段（库存）为字段参考 | — | 责任语义独有 | L0（字段 L2 参考） | Playbook 五段=Procedure/Specifications/Advice/Forbidden/Required 用户化 |

### 3.5 TALENT & CAPABILITY（专题）

> 结论：**人才与能力区的骨架直接 L2 复刻 WorkBuddy 专家中心（E2/E3），卡片 L4 复刻 WorkBuddy，详情与绑定消费 Coze/Cursor 模式；Curis 原装组织叙事（L0）作为内容填入，不改骨架。**

| Surface | Best Ref | Secondary | 参考具体 Surface | 为什么最好 | 级别 | Curis Adaptation |
|---|---|---|---|---|---|---|
| Talent Home | **WorkBuddy 专家·技能·连接器**（E2） | Coze 商店 | E2 顶部三 tab 分段+精选场景轮播+分类 chips+卡网格+右上搜索+我的xx | 三目录（专家/技能/连接器）与 Curis 完全同构；场景导购降低理解成本 | **L2** | 三 tab=专家(员工)/技能/连接器；精选场景→"从一件事开始"（示例业务牵引） |
| Employee/Expert Card | **WorkBuddy 专家卡**（E2 实测） | — | avatar40+名15/600+发布者12+两行简介+3 chips；特邀徽标；hover 召唤按钮 | 极简字段+成果叙事，普通用户友好 | **L4** | "召唤"→"招聘"/"对话"；发布者→部门·Role；徽标→"原装员工" |
| Expert Detail | Coze Agent 配置页（库存字段） | D 代详情骨架 | 库存：身份/人设 prompt/模型/技能挂载/开场白 | 字段最全的 agent 详情 | L2 | +Curis 独有：责任/Scope/当前工作/最近结果 |
| Skill Marketplace | **WorkBuddy SkillHub**（E3） | Cursor/Claude skills | E3：精选技能 4 列（内联 + 安装）+ 推荐/SkillHub/套件 + 分类 chips + 我安装的 59 + 添加技能 | 安装内联化+已装计数+来源分区最成熟 | **L2** | 套件→"岗位包"（对应原装组织叙事候选，需产品裁决） |
| Skill Card | **WorkBuddy 技能卡**（E3 实测） | — | icon32+名14+右侧 + 24 圆+两行描述12 | 一屏可见可装 | **L4** | + 来源徽标（官方/社区/自建） |
| Skill Detail | Coze 插件详情（库存） | Claude SKILL.md | 库存：描述/参数/权限/示例 | 字段齐全 | L2 | + 触发方式用户语言（"什么时候会用它"） |
| Plugin / Connector | WorkBuddy 连接器 tab（库存+E2 结构） | Coze 渠道 | 库存：每项独立授权绿点+开关 | 授权状态可视 | L2 | 状态=未连接/需授权/已连接（Curis 既有真值语言） |
| Install / Installed / Update | WorkBuddy 内联 + 与计数（E3） | Cursor 扩展 | E3 "+"/"我安装的 59" | 就地安装反馈 | L3 | 安装后→"绑定到哪个员工"引导（Curis 特有步骤） |
| Search / Filter / Category | WorkBuddy chips 行（E2/E3 实测） | Linear 筛选（E9） | chips h28 r14 横滚+右箭头 | 单行分类+排序（综合/最热/最新） | **L4** | token 化 |
| Model Binding | Coze 节点级模型设置（库存） | WorkBuddy 模型配置 | 库存：节点级独立模型+参数 | 绑定显式化样板 | L2 | 员工详情"能力卡"第二层暴露 |
| Capability Binding | Curis 已实现（Frozen） | Zcode skill 触发语义 | — | 绑定对象 Curis 已有 | L0 语义 / L2 面 | 用户语言："会做什么"卡（M-06/P-D2） |
| 成果反查导购 | WorkBuddy 灵感做同款（库存） | — | 库存：成果→自动带配置 | Curis 有 Result→Employee 链，天然可做 | L1 | "从这个结果看是谁做的/招同款" |

### 3.6 CONVERSATION（组件级 Reference Map）

| 组件 | Best Ref | 证据/出处 | 级别 | Curis Adaptation |
|---|---|---|---|---|
| Conversation Layout（任务型） | **WorkBuddy 任务视图**（E1） | 标题式用户输入+纵向内容+产物区 | L2 | Employee Work 会话=任务叙事（Curis 事件模型不变） |
| User Message | ChatGPT 气泡（库存/标准） | 右对齐浅底气泡 | L4 | 对话型场景用；任务型用 E1 标题式 |
| Employee/AI Message | Claude/ChatGPT 文本流+结构卡 | — | L3 | 员工消息带身份行（头像+名+状态点） |
| Message Width / Alignment | ChatGPT 中心限宽（~48rem 级） | 标准 | L4 | 对话列 max 720 逻辑 px |
| File Reference | **WorkBuddy 附件卡**（E1 实测） | 2 列网格卡：icon36+名+大小+分享 | **L4** | + Result 卡同构 |
| Knowledge / Citation | ChatGPT 来源栏（E5） | 行内引用 chip+汇总来源列表 | L2 | 引用=资料库条目（Used By 反向已有） |
| Mention | WorkBuddy "@引用对话文件，/调用技能"提示（E1 placeholder） | 语法提示入占位符 | L3 | @员工/资料/结果 |
| Tool Activity | **Cursor 工具折叠卡**（E6/库存） | 默认折叠摘要行 | L3 | "做了什么"一行，点开看工具流（P-B3⭐） |
| Thinking | Claude thinking 开关+折叠（库存） | — | L2 | 员工"思考"默认折叠 |
| Plan | Cursor Plan mode / Devin plan 可编辑（库存） | — | L2 | Work 计划段（见 3.9） |
| Progress（会话内） | **扣子步骤行**（E8） | ○→✓ 圈+灰字步骤 | L3 | 关键节点：已接受/交付中/已交付 |
| Result Reference | **WorkBuddy/扣子 会话内产物卡→右栏**（E1/E8） | 卡片+点击开 Utility | L3 | 正合 Frozen Result Reference→Utility |
| Artifact | 扣子视频/音频卡（E8） | 富产物卡（时长/波形/播放） | L3 | 按产物类型分卡 anatomy |
| Error / Retry | Claude 错误横幅（E4）+ WorkBuddy 重新生成按钮（E1 AX） | — | L4/L3 | 中文+三路径；重试=重新生成 |
| Branch | Claude edit→branch（库存） | — | L2 | 决定类消息分支（候选） |
| Copy / Actions 行 | **WorkBuddy 消息操作行**（E1 实测 AX） | 复制/点赞/点踩/朗读/重新生成/分享/更多 icon16 gap12 | **L4** | + "转给其他员工/升级给我" |
| Timestamp | Cursor "2d ago"（E6） | 相对时间灰字 | L3 | 简报内绝对时间，会话内相对 |
| 成本内联 | **WorkBuddy "共消耗 ◇8.2 ●模型"**（E1 实测） | 操作行尾部 | **L4** | Usage Ledger 投影：本条消耗+模型（P-E6⭐） |

### 3.7 COMPOSER（组件级 Reference Map——不选"最佳整体"，逐组件选）

| 组件 | Best Ref | 证据 | 级别 | Curis Adaptation |
|---|---|---|---|---|
| Composer Container | **Claude**（E4） | 居中浮卡 r16 白底细边框浅影；会话内 dock 同卡 | **L4** | 槽位按 Frozen X10 |
| Text Area / Placeholder | **Claude**（E4） | 20px 浅灰占位"今天帮你做些什么？"句式 | **L4** | 占位句式含语法提示（@/） |
| Attachment | **Claude + 按钮**（E4 左下） | 20px + 图标 | **L4** | — |
| File Chip | WorkBuddy 附件卡缩略（E1）/ ChatGPT chips（库存） | — | L3 | 上传中/已引用两态 |
| Context / Reference（@语法） | **WorkBuddy**（E1） | placeholder 内 @/提示 | L2 | @员工/业务/资料/结果 |
| Model Selector | **Claude "Claude Opus 4.5 ⌄"**（E4）右下内联文字下拉 | 16px 文字+chevron，无重边框 | **L4** | 模型选择保持会话内 |
| Agent/Employee Selector | Curis Frozen"执行·<Agent>"槽位；UI 型=WorkBuddy 专家选择 | D 代已实现语义槽位 | L3 | 执行者下拉同 Model Selector 形 |
| Mode Selector | WorkBuddy"有用操作"chip（E1） | — | L3 | 工作模式（X10 槽位） |
| Permission Selector | **WorkBuddy "⚠允许完全访问"琥珀 chip**（E1）/ ChatGPT 红字完全访问（E5） | 授权态就地可见 | **L3** | 访问权限槽位；默认最窄，放宽显警告 |
| Send | **Claude 32 圆 + WorkBuddy 28 圆**（E4/E1） | up-arrow 圆钮；禁用态灰 | **L4** | accent 由 token 决定 |
| Stop / Running | WorkBuddy 内联 spinner（E1 发送键位左侧） | — | L3 | 发送⇄停止同位切换 |
| Queue / Steering | Cursor queue/steer（库存） | — | L2 | 运行中补指令（P-B8⭐） |
| Disabled | WorkBuddy 发送 disabled（E1 AX 证实） | — | L3 | 空输入禁用 |
| Multi-line / Keyboard | ChatGPT/Cursor 标准 | Enter 发送 Shift+Enter 换行 | L3 | — |
| Drag & Drop | ChatGPT/Claude 标准 | — | L3 | 落点高亮 Composer |

### 3.8 AGENT WORK（专题）

> 结论：**Agent Work 的呈现以 ChatGPT Codex 右栏（E5）为骨架 L2，Cursor 的过程组件为交互 L3，Manus/Devin 的 plan/todo 为结构 L2；Curis Work/Task/Evidence 语义全部 L0。**

| 组件 | Best Ref | 证据/出处 | 级别 | Curis Adaptation |
|---|---|---|---|---|
| Start | L0（Work 由责任/会议/对话发起） | — | L0 | — |
| Plan | **Cursor Plan mode + Devin plan 可编辑**（库存） | 计划先行+中途改 | L2 | Work 卡"计划段"：步骤 checklist |
| Todo | **Manus todo 第一公民**（库存） | 任务列表常驻 | L2 | Work 步骤清单 |
| Current Step / Activity | **ChatGPT 右栏 + Cursor 状态摘要**（E5/E6） | 当前动作+已完成计数 | L3 | 员工行"正在：<动作>" |
| Tool Call | **Cursor 工具折叠+Review**（库存） | 默认折叠 | L3 | 折叠摘要（证据进 Evidence） |
| Subtask / Multi-Agent | **ChatGPT 子智能体头像组"3 完成"**（E5） | 头像+计数最密表达 | L3 | 并行员工头像组（并行能力待 Runtime） |
| Delegation | L0（Leader 分工） | 语义独有 | L0 | 分工画面=谁/做什么/为什么/状态 |
| Steering | Cursor queue/steer（库存） | 非破坏介入 | L2 | 运行中 Work 补充指令 |
| Permission | WorkBuddy 四级审批（库存）+ Cursor Run Modes（库存） | 梯度+档位 | L2 | 对齐 Curis 请示/批准事件（P-A11⭐） |
| Pause / Stop / Retry / Failure / Recovery | WorkBuddy 任务 6 状态机（库存） | 待执行/执行中/完成/暂停/失败 | L2 | Work 状态词典（P-B6⭐） |
| Completion | Cursor "Worked for 14m"摘要（库存） | 人话时长摘要 | L3 | "用时 14 分钟 · 消耗 ◇8.2 · 交付 1 个结果" |
| Resume | WorkBuddy 自动化执行记忆（本地证据） | 可恢复运行 | L1 | Work 重启恢复（Runtime 已有 resume 能力） |
| **Agent 工作右栏（骨架）** | **ChatGPT Codex"环境信息"栏**（E5 实测） | 分节：变更(±mono 数)/分支/子智能体/来源+每节+号 | **L2** | Curis 化：变更=Work 产物、子智能体=协作员工、来源=引用资料、+Evidence 节 |

### 3.9 RESULT / ARTIFACT

| 组件 | Best Ref | 证据 | 级别 | Curis Adaptation |
|---|---|---|---|---|
| Result Card（会话内） | **WorkBuddy 附件卡 / 扣子交付卡**（E1/E8） | icon+名+meta+打开 | **L4** | + Evidence 数徽标 |
| Result Row（列表） | Linear 结果行（E9） | h36 行 | L3 | 成果库列表 |
| Preview | **Cursor Preview⇄Source**（E6） | 文档双态 | **L4** | 文档/Markdown/代码 |
| Artifact Panel（富产物） | **扣子右栏编辑器**（E8） | 全高编辑器+时间线 | L2 | 表格/演示/媒体 |
| Evidence / Citation | **L0 ORIGINAL**（呈现学 ChatGPT 来源栏 E5） | — | L0/L2 | Evidence 行=来源+时间+员工 |
| Version | Claude Artifacts 版本（库存） | — | L2 | Result 版本历史 |
| Download / Export | WorkBuddy 分享/打开所在文件夹（E1 AX） | — | L3 | 导出+所在路径 |
| Continue Working / Ask Employee | Cursor follow-up composer（E6） | 结果面直接续指令 | L3 | "继续这个工作/问员工" |
| Open Utility | Curis Frozen 模式；实现参照 E1/E8 | — | L3 | Result Reference→Utility |

### 3.10 KNOWLEDGE（资料库）

| 组件 | Best Ref | 证据/出处 | 级别 | Curis Adaptation |
|---|---|---|---|---|
| Knowledge Home | Claude Projects knowledge（库存）+D 代 | 分区+搜索 | L2 | 消费已验收 Figma 187 基线 |
| File Row | Linear Document 行（E9） | h36 图标+名+meta | L4 | — |
| Reading Surface | **WorkBuddy 右栏 markdown 阅读器**（E1 实测） | tabs+正文 padding24+右侧 TOC 点 | **L3** | 引用来源/版本常驻头部 |
| Reference / Used By | L0（反向引用独有） | — | L0 | Used By Work/Result 列表 |
| Search / Filter | Linear 搜索浮层（E9） | 同 3.1 | L3 | 限定资料类型 |
| Detail 元数据 | WorkBuddy 面板头部（E1） | 上传云端/分享/所在文件夹 | L3 | 来源/适用范围/版本/被引用 |

### 3.11 MEETING

| 组件 | Best Ref | 说明 | 级别 |
|---|---|---|---|
| Meeting 全部（列表/房间/议程/决议） | **L0 ORIGINAL** | 消费已验收 Figma 214 基线；制度独有 | L0 |
| 参会者头像/说话人 | 会议软件通用（L1） | — | L1 |
| 纪要/转写 | Manus Meeting Minutes（库存） | 未来输入能力候选 | L1 |
| Proposal→Decision 卡 | 3.2 Decision 行（E4 anatomy） | — | L2 |

### 3.12 OPERATING INTELLIGENCE

| 组件 | Best Ref | 说明 | 级别 |
|---|---|---|---|
| 洞察语义（Analyst/归因/Decision support） | **L0 ORIGINAL** | 消费已验收 Figma 172 基线 | L0 |
| Metric/Chart 视觉 | Linear/Notion 图表语言（L1） | 安静、无装饰 | L1 |
| Cost/Usage 视图 | **扣子积分页（E7 实测）**：总积分+三分拆+套餐倍率 | 用量拆分最清晰 | L3 |
| Report 阅读 | WorkBuddy 右栏阅读器（E1） | 同 3.10 | L3 |

### 3.13 SETTINGS（专题）

> 结论：**Settings Shell L3 复刻 Cursor（Cmd+Shift+J 左类右容），分区分 five-way（Claude P11）；各节逐个选最佳。**

| 节 | Best Ref | Secondary | 参考具体 Surface | 级别 | Curis Adaptation |
|---|---|---|---|---|---|
| Settings Shell / Navigation | **Cursor Settings**（库存：General/Agents/Tab/Rules&Memories/Models/MCP/Privacy/Account/Shortcuts/Updates 左栏） | Claude 分区（Appearance/Memory/Capabilities/Instructions/Connectors/Extensions/Cowork/Usage/General/Account/Org） | 左类右容、搜索设置项 | **L3** | 五类：个人偏好/公司设置/AI 与能力/权限与数据/运行与成本+通知/快捷键/关于（Direction §2.7） |
| Account / Appearance | Claude Appearance（库存） | Linear settings | 主题三态（Light/Dark/Auto） | L3 | — |
| Model 列表 / Model Row | **Cursor Models 设置**（库存：双池+逐模型开关+计价） | WorkBuddy 14 内置模型 | 行=名/ID/能力徽标/启用/默认/成本 | **L3** | + Vision/Reasoning/Context 徽标 |
| Provider / 凭据 | WorkBuddy 自定义模型本地 Key（库存） | Cursor BYOK | Endpoint/Key/健康/默认 | L2 | 凭据状态=已连接/需授权/未连接 |
| Skill | Cursor Customize（库存） | Zcode skills 启用 | 已装/启用/绑定员工 | L3 | + 人才市场入口 |
| MCP | **Cursor MCP 配置**（库存：URL/command/OAuth/插值逐字段） | Claude 连接器 | — | **L3** | server 列表+工具清单+健康 |
| Permission | **Cursor Agents→Approvals & Execution**（库存：三档+permissions.json 自然语言规则+sandbox） | WorkBuddy 安全中心 12 分组 | 档位+白名单+高危阈值 | **L3** | + 四层 scope 隔离展示（Curis 独有） |
| Memory | **Claude Memory**（库存：逐条查看/编辑/删除/Pause/Reset/导入导出） | ChatGPT sources 可解释 | 逐条+来源 | **L3** | 公司记忆条目+Evidence 来源（P-C8⭐） |
| Notification | ChatGPT Notifications（库存） | — | 分类型开关 | L2 | 四类事件 |
| Usage / Cost | **扣子积分页（E7 实测）** + Claude usage ring（库存） | Cursor usage dashboard | 总量+拆分+就地环 | **L3** | 按员工/模型/业务拆分（Usage Ledger 投影） |
| Shortcut | Cursor Shortcuts（库存） | — | — | L2 | ⌘K/全局唤起 |
| Developer / About | Cursor（hooks/Updates） | — | — | L2 | — |

### 3.14 DESKTOP SHELL（专题）

| 组件 | Best Ref | 证据 | 级别 | Curis Adaptation |
|---|---|---|---|---|
| Navigation | **Linear**（E9） | 组标签+行节奏+团队分组 | **L4**（视觉节奏） | 七区映射 |
| Sidebar | Linear（E9）+ WorkBuddy 计数（E1） | — | L4/L3 | — |
| Pane 结构 | **Cursor Agents 三 pane**（E6）+ 扣子会话/编辑器（E8） | 230/弹性/380 | L2 | 四 Pane Frozen 不变，宽度节奏参照 |
| Inspector/Utility | 扣子（E8） | 全高工作台 | L3 | — |
| Search | **Linear 浮层**（E9） | 实测 anatomy | **L4** | — |
| Command Palette | Linear ⌘K | 同壳 | L3 | — |
| Floating Surface / Quick Entry | ChatGPT Classic Option-Space（库存） | 系统级唤起 | L2 | 全局助理快捷键 |
| Notification | Devin Slack 三按钮深链（库存） | 通知→深链动作 | L1 | — |
| Window Chrome | Linear 自定义标题栏（E9） | 标题栏内嵌搜索 tab | L2 | 二期 |

---

## 4. DO NOT REINVENT REGISTER（不值得自己设计的通用件——直接采用）

| 通用件 | 直接采用谁 | 级别 |
|---|---|---|
| Model Selector（内联文字下拉） | Claude（E4） | L4 |
| File Attachment 卡/chip | WorkBuddy（E1） | L4 |
| 全局搜索浮层（类型 chips+分组结果+预览） | Linear（E9） | L4 |
| 消息操作 icon 行 | WorkBuddy（E1） | L4 |
| 空态（问候+主行动+Ideas 行） | Claude（E4） | L4 |
| 错误横幅（解释+Details+双按钮） | Claude（E4） | L4 |
| Marketplace 分类 chips+排序 | WorkBuddy（E2/E3） | L4 |
| Skill/Expert 卡 anatomy | WorkBuddy（E2/E3） | L4 |
| Settings 左类右容壳 | Cursor（库存） | L3 |
| MCP 配置字段 | Cursor（库存） | L3 |
| Agent 活动折叠卡 | Cursor（库存） | L3 |
| Result 预览 Preview⇄Source | Cursor（E6） | L4 |
| Usage 就地显示（消耗+模型） | WorkBuddy（E1）+ Claude ring | L4/L3 |
| 侧栏分组行节奏 | Linear（E9） | L4 |
| 权限授权 chip（就地可见） | WorkBuddy"允许完全访问"（E1） | L3 |
| Segmented 顶部分段（三目录切换） | WorkBuddy（E2） | L4 |
| 步骤完成行（○→✓） | 扣子（E8） | L3 |
| 子智能体头像组+完成计数 | ChatGPT（E5） | L3 |
| Follow-up composer（结果面续指令） | Cursor（E6） | L3 |
| 相对时间戳 | Cursor（E6） | L3 |

## 5. CURIS ORIGINAL DESIGN REGISTER（绝不能因竞品好看而被同化）

以下语义/对象为 L0，任何复刻不得把 Curis 核心改画成 Agent Manager / Workflow Builder / Project Manager / Marketplace：

1. CEO Desk 注意力-决定模型（Today Brief / Matters / P7 Decision Gate）。
2. Company → Department → Business → Workspace 责任链与四层执行 Scope。
3. Leader = Employee × Role × Scope Assignment；only-on-exception 路由。
4. Employee = 公司成员身份（Definition → Instance → Holder），非 agent 配置记录。
5. Meeting 制度（Proposal → 决议 → Work → Result → Evidence → Leader 再评估）。
6. Result → Evidence 溯源（"事实先于观点"）。
7. Company Analyst / 经营洞察 / 六维公司脉搏。
8. 原装公司经营组织（fresh Company 自带部门与员工）。
9. 唯一 Usage Ledger 四层归属（呈现可抄，语义不可改）。
10. Package First 的 Workspace Engineering。

内部通用件（Row/Card/Panel/Composer/Search/Menu/Progress）不受此限，按 §3/§4 复刻。

## 6. 统一化规则（多来源拼装如何不散）

1. **所有 L3/L4 复刻件一律过 Curis token**（V1 中性阶+单一 accent+状态三色小面积）——geometry 抄，颜色/字体/圆角档取 Curis。
2. **一个页面最多两个"视觉口音"来源**：结构骨架（L2）+ 组件（L4）分别注明，禁止三个竞品的卡片样式混贴。
3. **状态词典唯一**（§3.9 Work 状态机），所有借来的组件里的状态文字替换为 Curis 词典。
4. **图标全套 Curis icon system**（借 anatomy 不借 icon path）。
5. 拼装冲突时：交互流程听 Best Reference，信息层级听 Curis Object Model，视觉密度听 Linear。

---

## 7. 与既有研究关系与边界

- 消费：Gap Matrix / Settings Matrix / 九矩阵 / UI Audit / Problem Register / Direction / 9 份 FUNCTION_INVENTORY（引用处标"库存"）。
- 新增实测证据：E1–E9（`evidence/pixel-reference/`，Retina 2x 实拍；所有尺寸为逻辑 px APPROXIMATE）。
- 遵守边界：未读取任何密码/Cookie/Token/Keychain；未进入 MFA/CAPTCHA/支付路径；未修改 Figma/Frontend/Runtime/Product Authority；未 commit/push。
- **本报告为研究终点：STOP FOR CEO / CHATGPT REVIEW，不自行开始 Final UI Master。**
