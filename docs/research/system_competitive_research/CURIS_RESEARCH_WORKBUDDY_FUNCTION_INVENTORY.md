# Curis Competitive Research — WorkBuddy 功能清单（Function Inventory）

- **研究对象**: WorkBuddy（腾讯 / CodeBuddy 团队出品的"全场景职场 AI 智能体桌面工作台"，官网 workbuddy.cn / workbuddy.ai）
- **研究方法**: 纯 Web 研究（官方文档站、官网、腾讯云国际站、第三方报道与社区文章）。未拆解本地 App 包、未读取本地代码。
- **Authority Class**: RESEARCH
- **Status**: Draft
- **研究日期**: 2026-09-12
- **标记约定**: `UNKNOWN` = 未找到公开证据；`APPROXIMATE` = 依据截图/营销页/第三方转述推断，非官方字段级确认。
- **关联文件**: `CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE.md`（本地第一方证据：自动化执行记忆、席位/升级治理、飞书 webhook 升级、含 software-engineer / software-qa-engineer 角色的 teams）。本文件不修改该文件。
- **产品快速身份**: WorkBuddy 是腾讯"全场景 AI 办公工作台"，口号"AI Agent 办公新范式 / 你的办公好搭子"；与 CodeBuddy（IDE/插件/CLI）共享账号与积分体系；同一客户端内有 WorkBuddy、WorkBuddy 小程序、WorkBuddy 移动端、WorkBuddy Enterprise 多条产品线。
- **证据可信度总注**: 官方文档站（workbuddy.cn/docs）字段级可信；官网营销页与第三方文章为 APPROXIMATE。部分第三方文章对开发商表述混乱（有"腾讯/字节"两种说法），以官方文档为准。

---

## 1. 产品概览（Product Overview）

**来源**: https://www.workbuddy.cn/docs/workbuddy/Overview ; https://www.workbuddy.cn/docs/workbuddy/Quickstart ; https://www.workbuddy.cn/docs/workbuddy/Pricing ; https://www.tencentcloud.com/act/pro/workbuddy ; https://www.qbitai.com/2026/03/391894.html ; https://cloud.tencent.com/developer/article/2640403

### 1.1 是什么
- 腾讯推出的"全场景职场 AI 智能体桌面工作台"（官方文档用语）；营销口号"WorkBuddy - AI Agent 办公新范式"（中文站）、"AI Agent for Everyday Office Work"（国际站）、"Your Scenario-Ready AI Suite / AI Team Workbench"（腾讯云国际企业页）。
- 核心承诺：一句话自然语言下达任务 → 自主规划拆解 → 执行 → 交付可验收结果（文档/表格/PPT/报告/网页/代码）；支持多任务并行、多 Agent 并行、本地文件操作。
- 与"传统 AI 对话"的官方对比表：传统对话只给建议 vs WorkBuddy 实际执行任务；手动操作文件 vs 自动操作本地文件；单步骤 vs 多步骤复杂任务；文字回复 vs 交付可验收结果。
- 出品方：腾讯，由 CodeBuddy 团队打造；社区昵称"小龙虾/龙虾/虾"（Agent 被称为 Claw）。
- 规模宣称（APPROXIMATE，官方营销口径）：国内 2026 年 3 月上线，"中国 PC 端第一生产力 AI Agent"；国际站宣称 5,000+ 团队、200 万+ 任务、50+ 语言。

### 1.2 产品线（同一文档站顶部导航）
- IDE、插件、CLI、**WorkBuddy**（本产品）、WorkBuddy 小程序、WorkBuddy 移动端、WorkBuddy Enterprise。

### 1.3 目标用户
- 个人职场用户（文档/数据/PPT/研究/邮件/文件批处理）；代码开发者（编码、项目理解、网站/应用开发）；设计创意人员（产品稿、PPT、原型、Logo、海报）；团队/企业（项目协作、Buddy 应用、Enterprise 版）。

### 1.4 平台
- 桌面端：Windows x64（ARM64 兼容）、macOS x64 / ARM64（官网下载区）；Linux 通过国产应用商店覆盖 UOS / 银河麒麟（APPROXIMATE，来自官网下载页转述）。
- 移动/其他端：iOS / Android / 鸿蒙（电脑版 + 手机版）App、微信小程序、Web 在线版（官网按钮：App / 小程序 / 网页版在线体验）。
- 分发：官网下载、腾讯软件中心 pc.qq.com。

### 1.5 定价（国内个人版，2026-07-01 起 4 档）

| 项目 | 体验版 | 标准版 | 高级版 | 旗舰版 |
|---|---|---|---|---|
| 月付 | 免费 | ¥99/月 | ¥199/月 | ¥999/月 |
| 连续包月(7折) | — | ¥70/月 | ¥140/月 | ¥700/月 |
| 年付(7折) | — | ¥840/年 | ¥1,680/年 | ¥8,400/年 |
| 连续包年(再8折) | — | ¥672/年 | ¥1,344/年 | ¥6,720/年 |
| 基础积分/月 | 500 | 2,000 | 4,000 | 20,000 |
| 限时赠送积分/月 | — | 2,000 | 5,000 | 30,000 |
| 限时合计/月 | 500 | 4,000 | 9,000 | 50,000 |
| 代码补全 | 5,000/月(促销无限) | 无限 | 无限 | 无限 |
| 自动化任务数 | 3(促销99) | 15(促销99) | 30(促销99) | 99 |
| 模型调度 | 仅自动(促销全模型) | 全模型 | 全模型 | 全模型 |
| 每人项目数 | 5 | 10 | 15 | 20 |
| 每项目成员 | 3(促销5) | 5 | 8 | 10 |
| 个人助理数 | 3 | 5 | 8 | 10 |
| 资料库存储 | 5GB | 10GB | 20GB | 50GB |

- 加量包：1,000 积分 ¥50，有效期 1 个月，仅标准版及以上可购。
- 国内企业版：企业旗舰版（SaaS）¥198/席位/月，1 席位起，2,000 积分/席位/月团队共享，问答不限量；企业专享版（私有化）¥316/席位/月，100 席位起。企业加量包 6 个月有效期（¥100/2,000 → ¥9,200/200,000）。
- 国际版：Team Plan $40/席位/月，1,000 积分/席位/月（团队共享池）；TokenPlan 自带模型订阅 $7（1,000 积分）～ $103/月（15,900 积分），可选混元/DeepSeek/GLM/Kimi。
- 老用户迁移、积分有效期规则见定价页（积分按月发放不结转；赠送积分到账 1 个月有效）。

---

## 2. App Shell 与导航（App Shell & Navigation）

**来源**: https://www.workbuddy.cn/docs/workbuddy/Quickstart ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Setting ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Library ; https://www.workbuddy.cn/docs/workbuddy/FirstTask ; https://www.workbuddy.cn/（官网，APPROXIMATE）

### 2.1 三栏主结构（官方确认）
- **左侧边栏**：按文件夹分组显示的任务列表，支持搜索和管理；底部为用户头像；列表分「任务」（最近访问/更新）与「空间」（按工作空间归组）两个板块；侧边栏底部有容量条（资料库存储，APPROXIMATE 来自资料库文档"侧边栏底部容量条"）。
- **中间对话区**：核心交互区，含任务标题栏、消息列表、输入框。
- **右侧结果区**："产物、全部文件、变更、预览等视图"（Quickstart 语），即右侧边栏。

### 2.2 左侧边栏导航条目（官方文档逐页印证的完整清单）
- 新建任务
- 任务（列表：任务 / 空间 两板块；空项目自动隐藏）
- 工作空间（任务列表"空间"板块；工作空间级右键菜单：新建任务/打开文件夹/重命名/从列表中移除）
- Claw（= 助理/Assistant 入口；量子位与官网演示中 Agent 称 Claw；设置里"经助理会话创建的任务不绑定助理（Claw）工作空间"——官方文档原文明示 Claw 与助理同指）
- 专家（专家中心 + 我的专家）
- 技能（技能市场 + 已安装）
- 连接器
- 自动化
- 资料库
- 「更多」内：灵感、我的邮箱、我的文件（APPROXIMATE：灵感文档称"左侧边栏「更多」进入"；邮箱文档称"左侧边栏「更多」中，位于「我的文件」下方"）
- Buddy 应用（首页左上角应用入口，展开应用列表；APPROXIMATE 来自 Buddy-App 文档"点击首页左上角的应用入口"）
- 项目（"左侧导航 → 项目 → + 新建项目"）
- 消息中心铃铛（左侧边栏底部；整页平铺展示，点击 × 或再次点击铃铛退出；空态"暂无消息"）
- 用户头像（底部）→ 用户菜单
- 官网演示首页侧栏顺序（APPROXIMATE，营销截图）：新建任务 / Claw / 专家 · 技能 · 连接器 · 自动化（一栏四项）/ 任务 / 工作空间。

### 2.3 全局搜索 / 命令面板
- 全局搜索：文档站页面自身有"搜索（快捷键 K）"（APPROXIMATE：这是文档站快捷键，桌面端全局搜索快捷键 UNKNOWN）。
- 对话内搜索：任务对话顶部"对话内搜索"，关键词查找对话内容。
- 斜杠命令补全：输入 `/` 触发命令补全；项目级命令定义于 `.codebuddy/commands/`，支持嵌套目录（如 `team:review`）、筛选、优先级合并；`/skills` 查看技能列表、`/skills import <git url|本地路径>` 导入技能。
- 独立"命令面板"（如 VS Code 式 Ctrl+K/Ctrl+P）：UNKNOWN。

### 2.4 通知
- 消息中心（铃铛，整页平铺）：消息类型=①任务操作（待确认任务需要操作，点击直达任务）②任务已成功完成（点击查看结果）。未读红点、可一键全部已读（开放平台通知语境）。
- 通知中心（我的邮箱语境，位于左侧栏顶部）：新邮件提醒、开通成功、冻结、封禁、授权吊销；新邮件可"添加邮件到对话"或"前往邮箱"。
- 系统通知：任务完成/需关注时推送到微信（助理集成）、小程序、企业微信 bot。

### 2.5 设置入口
- 左下角头像 → 用户菜单 → 设置。用户菜单项（官方全列）：企业版（进入企业智能体）、查看积分余额（余额与明细）、记忆与进化、外观（浅色/深色主题切换）、帮助与反馈、检查更新、退出登录。

---

## 3. 专家（Expert）系统

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Expert-Center ; https://cloud.tencent.com/developer/article/2640403 ; https://www.qbitai.com/2026/03/391894.html ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Ispiration

### 3.1 定义与三层概念模型（官方对比表原样）
| 维度 | Skill | 专家（Agent 型） | 专家团（Team 型） |
|---|---|---|---|
| 组成关系 | 工具能力：让 AI 能做某件事 | AI 顾问：懂某个领域的 AI 角色 | AI 协作团队：自动拆解、并行执行、完整交付 |
| 怎么选 | 需要 AI 具备工具能力 | 有明确单点问题 | 任务复杂，需多角色配合 |

- 官方总结："Skill 是能力；专家是能力+经验；专家团是多位专家+协作流程。"
- 专家机制 = "人设 + 方法论 + 工具链"的角色切换；专家团机制 = 团长（自动拆解、分配、并行执行、整合交付）+ 多位专家分工。
- 灵感文档的三问表述：Skill="WorkBuddy 能做什么"；专家="WorkBuddy 中的谁能帮我做"；灵感="用这些能力实际做出了什么"。

### 3.2 专家中心 vs 我的专家
- **专家中心**：包含"专家"与"专家团"两类卡片，支持按行业分类浏览，"召唤他们为你服务"。规模：**140+ 位专家，覆盖 12 大行业领域**（官方云+社区文章《一句话召唤 140+ 位行业专家》；7×24 待命）。12 领域具体枚举：公开报道仅举例"市场营销、游戏开发、工程技术"（量子位称"12 大类垂类专家"）；完整行业枚举 UNKNOWN。
- **我的专家**："创建属于你的专家，分享专业知识"。创建表单字段、发布/分享流程、审核流程（开放平台有专家发布审核）在用户侧文档中 UNKNOWN（开放平台 open.workbuddy.cn 有发布审核通过/驳回/强制下架等 6 类通知，见 §12 Buddy 应用）。

### 3.3 专家卡片字段（官方文档明示）
- 专家卡片展示：**能力介绍、擅长领域、任务示例**。
- 专家团卡片展示：**能力介绍、擅长领域、团队成员、任务示例**。
- 第三方观察补充（APPROXIMATE，量子位实测）：专家有拟人化名字与职能，如 Ari（社交媒体策略师）、Kai（内容创作专家）、Fay（小红书运营专家）、Gia（知乎策略师）。
- 以下字段官方文档未提及，UNKNOWN：头像/封面、状态（在线/离线）、角色职称、详细描述、能力标签枚举、挂载 Skill 列表、底层模型、发布者/认证方、评分/评价、使用量/调用次数、价格/积分倍率标签、操作按钮明细（召唤/详情/分享/置顶等）。

### 3.4 专家详情页
- 官方文档未单独描述"专家详情页"结构；卡片即主要信息载体。UNKNOWN：是否有独立详情页、是否有方法论展示、示例对话、用户评价区。

### 3.5 使用流程（官方 4 步）
1. 打开专家中心（左侧边栏"专家"）→ 查找专家/专家团。
2. 召唤（点击召唤按钮 → 进入对话界面）。
3. 置顶与搜索：对话中点击专家入口展开**最近使用列表**；按名称关键字搜索（不可用时提示"搜索暂不可用，请稍后重试"）；常用专家**置顶后持久保存**；专家团会话限制——"当前会话已使用专家团，切换其他专家需要开启新对话"。
4. 描述任务：专家按角色视角方法完成；专家团由团长自动拆解/分配/执行/返回完整结果。

### 3.6 权限与数据边界（官方隐私声明）
- 专家"本身不主动获取系统权限"，仅处理用户主动提供的对话与上传文件；配备 Skill/MCP 时才在授权下间接访问。
- 信息收集表：账户信息（必要：用户 ID、昵称）、对话内容（必要）、上传文件（非必要）、工作区文件（非必要，仅经 Skill 触发间接访问）。不收集：通讯录、精确地理位置、设备唯一标识、生物特征、产品外浏览历史。
- 免责声明：生成内容不构成专业意见；医疗/法律/投资/合规需咨询专业人士。
- 积分：专家团因并行调用多专家，积分消耗"通常为单专家的 3–5 倍"。

### 3.7 普通用户如何理解专家（产品叙事）
- 官方文章叙事："他们就在你的电脑桌面上""不是泛泛而谈的通用 AI，而是真正的领域专家"；举例"懂品牌策略的设计顾问、精通敏捷管理的项目经理、深谙增长黑客的营销老兵"。
- 行业案例：专家直接产交付物（专业文档、数据分析、报告、代码）而非咨询回复。
- 用户教育入口：灵感板块"一键做同款"自动加载专家配置（见 §10.3），Expert-Center 文档的 Skill/专家/专家团选型表。

---

## 4. 专家市场（Expert Marketplace）

**来源**: 同 §3；https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Ispiration ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project

- **浏览**：专家中心按行业分类浏览（12 领域，具体分类枚举 UNKNOWN）；专家与专家团并列展示。
- **搜索**：对话中专家入口的最近使用列表支持按名称搜索；专家中心内是否有独立搜索框 UNKNOWN（APPROXIMATE：官网演示截图显示有）。
- **筛选/排序**：UNKNOWN。
- **推荐位**：UNKNOWN（专家中心是否有"推荐专家"分区未在文档中出现）。
- **"安装"模型**：专家无安装概念，采用"召唤"（summon）即用；常用专家可置顶持久化。个人/项目层可配置"项目可召唤的领域专家"（项目配置字段之一，项目专家在任务内置顶显示）。
- **供给端**：我的专家（用户自建）+ 开放平台 open.workbuddy.cn（第三方提交专家/技能/连接器/Buddy 应用，经审核上架，有驳回/强制下架机制）。
- **普通用户理解成本设计**：卡片三要素（能力介绍/擅长领域/任务示例）+ 行业分类 + 灵感案例反查（看到成品 → 做同款 → 自动带出专家）。这是"成果即导购"的模式：灵感卡片展示作者头像昵称，双栏详情（左产物、右基础信息+所用专家+Prompt）。

---

## 5. SkillHub / 技能市场（Skill Marketplace）

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market ; https://blog.csdn.net/u013176440/article/details/163773511 ; https://www.cls.cn/detail/2310349 ; https://finance.sina.com.cn/tech/digi/2026-03-12/doc-inhqstev8770052.shtml ; https://skillhub.cloud.tencent.com/skills ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Inspiration（灵感页对照）

### 5.1 定义
- 技能（Skill）："封装一组可执行的脚本与工作流，使 AI 在您的授权下完成具体动作"；示例：发送邮件、订外卖、查询股价、读写文件、调用第三方 API。技术形态多为 SKILL.md + 脚本（兼容 OpenClaw/ClawHub 社区技能）。

### 5.2 页面结构（官方文档：技能板块两区域）
| 区域 | 内容 |
|---|---|
| 技能市场 | "推荐技能，可按需一键安装" |
| 已安装 | "已安装的本地技能，可直接在对话中调用" |

- 第三方实测补充（APPROXIMATE）：已安装区在上、推荐技能区在下；技能 Tab 内有关键词搜索框（如"Excel 自动化""会议纪要"）；列表项可参考"评分、下载量、版本信息"（第三方文章提及，官方文档未确认，评分/下载量字段 UNKNOWN）。
- 分类体系：官方文档未列出技能分类枚举；第三方实测提及文档、代码、数据分析、设计、营销等类别（APPROXIMATE）。

### 5.3 规模
- SkillHub（skillhub.cn / skillhub.cloud.tencent.com，腾讯龙虾技能社区）：2026-03-12 上线时整合 ClawHub 生态 **13,000+** 技能，兼容 WorkBuddy、QClaw 等框架；第三方实测文章称当前 **"数万乃至 7 万+"（≈70,000+）技能包**——该数字**非官方文档数字，APPROXIMATE**，未见官方页面确认。
- WorkBuddy 内置技能：官网称"内置 20+ 技能包，兼容 OpenClaw 社区技能导入"；官方文档另有"零成本 Skill 精选 10 个"：Agent Browser、办公文档四件套、Local Whisper、tl_video_downloader、Web Search、Obsidian、Skill Scanner、self-improvement、Find Skills、Frontend Design。

### 5.4 技能的四个来源 / 三种安装方式（"添加技能"入口）
1. **上传技能**：导入本地技能包（.zip / .skill，拖拽或点选），导入后自动配置。
2. **查找技能**：输入任务描述，WorkBuddy 自动查找相关技能（FindSkills）。
3. **创建技能**：输入任务描述，AI 自动创建技能（生成 SKILL.md + 脚本框架，可调试后发布）。
- 对话自然语言安装（第三方）：说"帮我安装 XX 技能"，AI 自动查找/下载/安装并提示填写 API 凭证。
- Git/本地导入（第三方）：`/skills import https://github.com/.../skill-repo` 或 `/skills import /downloads/my-skill/` → 克隆/扫描 SKILL.md → 安装到全局技能目录 → 校验完整性。

### 5.5 启用/关闭/卸载
- 随时关闭/重启用，无需卸载；关闭后保留在已安装列表但不参与自动调用；**开关状态多端同步**（记录在用户全局配置）。
- 不修改技能原文件（不改 SKILL.md）；关闭 ≠ 卸载；卸载彻底删除技能及开关记录，支持**批量卸载**。
- 已安装技能较多时提供搜索定位。

### 5.6 对话中调用
- 模型自动调用（关闭的技能不参与自动调用）；`/` 手动唤起技能列表；建议仅启用当前任务所需技能以降低误调用。
- 技能与专家关系：官方文档未直接描述字段级绑定；专家的"工具链"由 Skill/MCP 构成（专家文档："配备 Skill/MCP 时才在授权下间接访问"）；项目配置中专家与技能是并列的两类资产，任务内可同时选择。灵感做同款会"自动预填 Prompt、加载关联的 Skill 和专家配置"。

### 5.7 技能类型
- 官方分类枚举 UNKNOWN。可观察的类型维度：官方内置 / SkillHub 社区 / 本地上传 / AI 现造；用户级 / 项目级（项目级在 `.codebuddy/skills/`，云端统一管理双端一致）；零成本精选（无需外部 API）vs 需凭证型。
- SkillHub 精选：skillhub.cloud.tencent.com 有"Top 50 高质量 AI Skills"（经安全审核与多维度评估），如 WorkBuddy 配置健康自检工具（7 维度 46 项检测）。

### 5.8 安全
- 官方警示：非官方 Skill 可能存在恶意提示词注入、越权访问、后门；优先官方推荐；安装第三方前核查权限申请、来源与脚本内容。
- SkillHub 侧：技能经安全审核后上架（腾讯云 SkillHub 精选审核机制）。

---

## 6. 连接器市场（Connector Marketplace）

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector ; https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project ; https://www.tencentcloud.com/act/pro/workbuddy

### 6.1 定义与技术形态
- 连接器 = WorkBuddy 与外部服务间的桥梁。技术形态两种：**MCP + CLI**（标准化协议）与 **Skill + CLI**（内置脚本）。"新增连接器将同步更新隐私协议相关条款。"

### 6.2 官方连接器列表
| 连接器 | 能力 |
|---|---|
| QQ 邮箱 | 收发/搜索/整理邮件，自然语言读内容、汇总线程、管理文件夹 |
| 腾讯文档 | 访问与操作腾讯文档 |
| 腾讯乐享 | 搜索/创建/管理知识库文档、导入 Markdown、按标签整理、追踪文档更新 |
| 腾讯会议 | 会议服务对接 |
| TAPD | 项目数据访问 |
| 腾讯网盘 | 云端文件访问 |
| 自定义连接器 | 用户自行安装的 MCP 服务（配置方式参考 CodeBuddy IDE 的 MCP 文档） |

- 国际版连接器（腾讯云国际页）：GitHub、GitLab、Jira、Confluence、Google Drive、Gmail、Notion、Slack；平台接入 GitHub/Notion/Jira。
- 连接器市场是否有"分类/推荐/搜索"货架：官方文档仅描述卡片列表 + 添加按钮；分架 UNKNOWN。

### 6.3 授权模型（官方两例）
- **QQ 邮箱（扫码授权）**：连接器卡片右侧"+"→ 跳转授权页扫码（要求 QQ 邮箱 App 7.1.5+/鸿蒙 0.2.9+）→ 手机端确认权限：账号信息 / 读取邮件（近一个月收件箱）/ 发送邮件（代发）/ 删除邮件（可选，移入已删除）→ 授权可在 QQ 邮箱 App"设置-账号-安全管理-登录设备和授权码-应用授权"管理 → 卡片出现**绿色圆点 + 启用/禁用开关**。浏览器弹窗需点"打开"，取消会中断需重配。
- **腾讯乐享（MCP 授权）**："+"→ 授权确认页（按已有权限访问、搜索查询、创建管理内容）→"立即前往授权"→ 微信/手机号登录 → 确认权限 → 绿点 + 开关。
- **断开**：点击已连接卡片 → 弹窗"解绑"。
- **项目内两类授权**：公共授权（管理员配置一次、全员共用票据，适合团队服务账号）与个人授权（各自授权、票据不共享，仅存本地）；同一连接器可并存；**协作任务中个人授权连接器全部禁用**；公共授权调用日志仅管理员可见（审计）。

### 6.4 数据范围（官方收集表）
| 收集项 | 类型 | 用途 |
|---|---|---|
| 第三方账号标识 | 必要 | 邮箱地址、账号 ID |
| 授权凭据 | 必要 | OAuth Access/Refresh Token 或手动 API 密钥 |
| 第三方业务数据 | 必要 | 仅指令触发时按需读取 |
| 用户写入数据 | 非必要 | 代发邮件、创建/编辑文档、创建会议，需明确指令确认 |

- 权限边界：每连接器独立授权；不主动定时抓取；不超出用户已有权限范围。
- 积分：连接器自身读写不耗积分；对外部数据理解/汇总耗积分。
- 消息通知类场景：发送企业微信/飞书消息（作为场景示例列出）。

---

## 7. 每个 Expert 的 Model / Tool / MCP / Skill 组合与凭据

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Expert-Center ; .../Model ; .../Connector ; .../Project ; .../Permission-Modes

- **专家组合模型**：专家 = 人设 + 方法论 + 工具链（官方原文）；工具链具体由 Skill / MCP / 连接器在授权下挂载，字段级"某专家挂了哪些工具"配置界面 UNKNOWN。
- **专家团**：团长自动拆解分配，多专家并行，积分 3–5 倍。
- **模型体系（官方内置 14 个）**：Hy4 preview、Hy3、GLM-5.3、GLM-5.3-Flash、GLM-5.2、GLM-5.1、GLM-5v-Turbo、MiniMax-M3、MiniMax-m2.7、Kimi-K3、Kimi-K2.7-Code、Kimi-K2.6、Deepseek-V4-Flash、Deepseek-V4-Pro。能力标记：图片输入 / 思考模式 / 推理模型。
- **对话内模型快选（新建任务栏）**：MiniMax（Excel/数据/PPT，快）、智谱 GLM（多步骤长流程）、Kimi（截图分析/图片转文档）、DeepSeek（日常问答/文案，低成本）、腾讯混元（中文写作/会议纪要）。另有三档调度：快速/均衡/极致模式；思考强度档位；上下文窗口默认 200K（可到 1M）；Max 模式（关闭=自动上下文压缩省积分）。
- **自定义模型**：UI 增删改（弹窗），配置与 API Key 仅存本地 `workbuddy/models.json`（兼容 `~/.codebuddy/models.json`）；接入方式：提供商接入（Token Plan：企业版专业/轻享、通用 Token Plan、Hy Token Plan；Coding Plan：腾讯云/智谱/Kimi；自定义 API 预设）、本地 Ollama（默认 11434 端口，OpenAI 协议）、Custom（手填 URL/Key/模型名）；自定义协议高级开关（跳过 /chat/completions 路径校验）；能力标记（工具调用/图片输入）自动写入。
- **凭据管理**：连接器 OAuth Token / API 密钥（授权凭据表）；模型 API Key 本地 models.json；Skill 所需 API 凭证在配置中填写（第三方：不要硬编码进可分享技能包）；敏感保护可将明文"允许并加密保护"为密文流转（见 §11）。
- **每专家是否可指定专属模型**：UNKNOWN（官方文档未描述专家级模型绑定；对话/自动化层可选模型与技能，自动化配置项含"选择模型和技能：指定模型、技能、专家、连接器"）。
- **项目级 Agent/规则资产**：`.codebuddy/rules/`（团队规范）、`.codebuddy/agents/`（项目专属 Agent 定义，自动发现）、`.codebuddy/skills/`、`.codebuddy/commands/`、`.codebuddy/CODEBUDDY.md`（项目记忆）；优先级项目级 > 用户级。

---

## 8. 对话与 Composer（Conversation & Composer）

**来源**: https://www.workbuddy.cn/docs/workbuddy/Conversation ; .../Task-Bar ; .../Create-Task ; .../Function-Description/Worktree-Task

### 8.1 对话区（任务对话）
- 任务=一个对话+一个工作空间；顶部：任务标题 + 四个操作——**对话内搜索、分享任务（自动生成公开链接）、历史提问（历史对话记录，点击跳转）、显示详情面板（打开右侧边栏：产物/全部文件/变更/内置浏览器）**。
- 消息流展示：回复内容、执行中的阶段说明（"正在分析数据""正在生成报告"）、已生成结果摘要、**可展开的中间步骤**；每条回复显示运行时间（响应时实时计时，完成后定格）。
- 追问：新需求/修改意见/继续追问（如"导出成 PDF"），基于先前上下文继续，无需重述背景；执行中可随时中断（输入框区域停止入口），中断后可补充说明/调整重发/继续推进。
- 发送：点击发送按钮或回车。

### 8.2 Composer（新建任务栏，官方字段级）
- **工作模式**（输入框左侧 + 菜单）：默认（Agent，可修改文件）/ 计划（Plan，先规划确认再执行）/ 仅问答（Ask，只回答不执行）。Plan 与 Ask 互斥；非默认模式输入框下方显示标识，点 × 退出。
- **Plan 模式细节**：开启 → 补充信息（模型就时间、预算、偏好等提问，可全跳过，模型自行假设并标注）→ 审阅方案（右侧面板）→"开始执行"或"调整计划"（删减/收窄/新增/调序/重来，可反复迭代）。
- **切换模型**（快选 + 三档调度 + 思考强度/上下文/Max，见 §7）。
- **设置工作空间**（输入框左下角"选择工作空间"）：文件选择器选文件夹；未指定则自动创建独立任务目录。
- **选择技能**：对话框选择已安装技能，执行时自动调用。
- **连接第三方应用**：输入框内快捷管理连接器。
- **权限管理**：输入框底部常驻权限状态按钮（默认显示「默认权限」）→ 弹面板 →「允许完全访问」开关（见 §11）。
- **Worktree 开关**（工作空间含 .git 时显示在输入框下方，默认关闭）：展开后选 Base Branch（默认本地主分支，可搜索/fetch 刷新），在 `~/WorkBuddy/Worktrees` 建隔离目录，任务分支命名 `workbuddy/{基础分支}-{8位随机哈希}`；上限 25 个提示、50 个强弹清理（清理 7/15/30 天前）；Git 分支选择器（未提交改动三选：Commit 默认/Stash/丢弃需二次确认）。
- **附件**：拖拽到页面任意位置自动入附件区；卡片含文件名/图标/上传状态/删除；**最多 50 个文件，单个大小不限**；不合规文件顶部报错；拖出页面或 ESC 取消；支持类型 PDF/Word/TXT/Markdown/RTF/Excel/CSV/TSV/PPT/图片/ZIP/RAR/代码文件。
- **粘贴**：Ctrl/Cmd+V 粘贴截图；**超 3000 字符粘贴自动压缩为 Chip**（悬停预览、点击展开编辑）。
- **微信聊天记录 Chip**：从微信/企微转发到 WorkBuddy → 生成聊天记录 Chip（来源、文件名、大小或消息条数），压缩包投递，解析失败可删除重发，不自动发送。
- **斜杠命令补全**（见 §2.3）。
- **Buddy 应用内**：工作模式为大胶囊（应用方定制）+ 场景胶囊（预置任务，点击自动召唤绑定专家并提供预设指令卡片）。
- **首页最佳实践案例**：新建任务页下方一排 4 张案例卡；选场景胶囊后切换该场景案例；"换一批"刷新。

### 8.3 历史与多任务
- 多任务并行；执行中任务显示在左侧边栏可随时切换；发送后直接进入对话页，**无 loading 过渡页**。
- 助理会话例外：仅一个会话、完整历史不可清空（对比普通任务可清空历史）。

---

## 9. Agent 工作与结果（Task Execution, Artifacts, Automation）

**来源**: https://www.workbuddy.cn/docs/workbuddy/Results ; .../Function-Description/Right-Sidebar ; .../Automation-Guide ; .../Task-Management ; .../Worktree-Task ; .../Conversation

### 9.1 任务执行与进度
- 自主规划执行：自动拆解任务、规划步骤、执行操作；执行中显示阶段说明与可展开中间步骤（§8.1）。
- 任务状态机（官方 6 态）：进行中 / 已完成 / 失败 / 待处理 / 规划中 / 已归档。
- 中断与继续：任何状态（已完成/失败/中断）均可重进并补充消息续跑。

### 9.2 结果区（右侧边栏四面板）
1. **产物（Artifacts）**：当前对话新生成文件（PPT/PDF/文档/表格/报告）；点击查看任务列表及生成内容；右键"打开文件夹"定位到 Finder/资源管理器；预览时右上角**分享图标**；**上传到云端**：我的云端网盘 / 腾讯文档 / ima 知识库 / 乐享知识库（"在其他端的应用内也可以查看"）。
2. **工作空间文件**：树状文件列表 + 右侧内容区 + 顶部已打开文件切换栏（文件浏览器，非编辑器；是否可编辑 UNKNOWN）。
3. **变更（Changes）**：本次任务文件修改列表、每文件改动、diff 对比。
4. **浏览器（内置浏览器）**：地址栏 + 刷新 + 实时预览；**多页签**（+ 新建，独立浏览状态/历史，关闭自动选相邻）；**登录态持久复用**（切会话/新页签不丢登录态）；**账号隔离**（同机不同 WorkBuddy 账号不串登录态）；可清除 Cookie 与缓存；**设备调试工具栏**（手机/平板/桌面视口切换、自定义宽高）。
- 下载/导出：结果页未提"下载/导出"（本地任务文件本就在本地；分享链接 + 云端上传为主）。已分享文件在"数据管理"可复制链接/下载/取消分享。

### 9.3 自动化（Automation）
- 定位：按设定时间执行周期性重复任务（每日简报、周报汇总、定时数据整理），结果保存到指定目录；触发时"以您当前的登录身份自动发起 Agent 任务"；受任务频率、最大执行时长、系统并发控制限制。
- **配置项（官方字段）**：名称 / 提示词 / 工作空间（默认自动分配 "automation-xxxx 工作空间"；经助理会话创建的不绑定 Claw 工作空间，统一落 automation 目录）/ 权限模式（默认权限 | 完全访问权限）/ 选择模型和技能（模型、技能、专家、连接器）/ 定时规则（执行频率与生效日期区间）/ 推送到小程序 / 推送到企业微信。
- **定时规则**：每周多天（周一/三/五 09:00 一条规则）、每月多天（1/15/28 日）；官方要求同一任务多执行日合并一条规则；cron/分钟级粒度 UNKNOWN。
- **模板**：新闻推送、周报生成、体检预约、学习计划等场景模板；第三方报道示例：每 12 小时 AI 资讯推送、每晚九点工作总结。
- **推送通道**：小程序（完成后自动发结果到小程序）；企业微信 bot（二选一来源：助理的企微 bot 复用通道 / 独立自动化通知 bot）；建议助理 bot 用 WebSocket 长连接（URL 回调有时效失效风险 ⚠）；通道解绑显示红点 +"该通道已断开 · 重新绑定"，推送开关不自动关；通知失败不阻塞任务；单向通知不写入助理上下文。
- **执行历史**：自动化页面可查看已安排任务及历史执行记录（详情字段 UNKNOWN）。
- **执行记忆**：官方文档未详述；本地第一方证据（companion 文件 `CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE.md`）观察到自动化带执行记忆。云端/网页端与客户端个人 Skill 库互不相通；自动化为个人级别，仅创建者可见可管理（项目内自动化"仅自己可见"）。
- **信息收集**：账户身份（触发时沿用登录身份调用模型/工具/MCP/连接器）、用户输入（名称/prompt/调度）、行为日志（创建/启停/触发/执行结果与耗时，用于状态展示与审计）、第三方凭证（仅用已授权凭证，不另存）、本地文件读写（仅限指定工作目录）。

### 9.4 并行与隔离
- 多任务并行、文件系统层面完全隔离（worktree）；任务卡片 fork 图标 + 只读分支 Badge（hover 详情、点击复制）。
- 任务卡片字段：任务标题、当前状态、最近更新时间或创建时间；列表级搜索（按标题）+ 筛选（状态/日期）+ 重置。
- 任务操作：置顶 / 打开文件夹 / 重命名 / **保存到工作空间**（可开多 Agent 协作、持久保存、随时用 IDE 打开）/ 分享任务（公开链接）/ 删除 / 归档（归档后在系统设置-数据管理查看）。工作空间级：新建任务/打开文件夹/重命名（默认时间戳名，仅显示名不改路径）/从列表中移除。命名校验：非空、无 `\ / : * ? " < > |`、≤255 字符、同级不重名，非法时按钮置灰并提示原因。
- 任务流转（项目内）：转交自动打包产物 + 自动生成的进度摘要 + 自定义字段（标题、描述、处理人、状态、截止日期，可编辑）+ 附件；接收方可基于完整上下文继续；对话记录/调用记录/中间产物复制到新会话。

---

## 10. 工作空间 / 项目 / 记忆 / 知识

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project ; .../Library ; .../Memory ; .../Knowledge-Base/Tencent-Doc ; .../Knowledge-Base/IMA%20Knowledge%20Base/01-Workbuddy-IMA-Basic-Guide ; .../Knowledge-Base/Lexiang（未逐页展开，字段 UNKNOWN）

### 10.1 工作空间（Workspace）
- 定义：当前任务主要读写文件的文件夹（新建任务选择的目录或自动创建的任务目录）。每任务独立空间；自动化有 automation-xxxx 空间；助理有专属文件夹；Worktree 任务在 `~/WorkBuddy/Worktrees`。
- 任务列表"空间"板块按工作空间归组；工作空间可重命名（仅显示名）。

### 10.2 项目（Project，团队协作）
- 结构：项目 + 任务两层；"让团队成员共享上下文、标准与知识"。
- **项目配置字段**：名称（必填）/ 指令（全局行为规则，所有任务自动继承）/ 连接器（公共/个人授权）/ 专家（项目可召唤专家）/ 技能 Skill。
- **注入机制**：项目指令拼入模型上下文；项目资料库以 reference 形式进入；个人记忆拼入上下文。
- **项目动态三类**：与我有关（被定向分享/转交）/ 成员动态（上传文件、邀请成员、公开任务、增删 Skill/专家/连接器、改指令等）/ 自动化（仅自己可见）。
- **协作**：分享（链接邀请，备注申请 + 管理员在消息中心审批）、转交/流转、多人协作；邀请链接加成员；积分按实际发起 AI 操作的人计。
- **任务内选择范围与排序**：专家=项目+个人+专家中心（项目专家置顶）；Skill=项目+已安装+现场导入（项目 Skill 置顶）；连接器=公共授权+项目个人授权（公共置顶）。
- **资产库**：项目详情页顶部标签栏「资产」；成员手动上传或从任务产物保存；以 RAG 形式注入任务上下文（Agent 也可 read-file）；每项目独立空间默认 5GB（依托腾讯网盘）；支持 md/txt/docx/csv/xlsx/pptx/PDF/图片/视频/音频/网站链接/Markdown/其他；记录更新人/更新时间。
- **.codebuddy/ 目录**（§7）；Web 端与客户端个人 Skill 库互不相通。

### 10.3 记忆（Memory）
- 从会话历史自动抽取，每晚整理当天会话重新生成记忆摘要；类型：事实信息、偏好习惯、人物关系、近期跟进事项、其他。
- 使用：注入系统提示词；支持会话历史检索（"上周做过什么""之前聊过的 XX"）。
- 管理 UI（设置 → 记忆）：查看 / 编辑（对话方式告诉它记住或忘记什么）/ 删除（清空或删单条）/ 关闭（停止提取）/ **导入**（复制示例提示词到其他 AI 对话 → 结果粘贴回来 → "添加到记忆"，即跨 AI 记忆迁移）。
- 费用：不耗积分/token；仅本人可见；关闭/删除后停用但已生成输出不追溯。
- 用户菜单中该入口名为"记忆与进化"。"进化"独立机制官方文档未展开（相关主题为实践八"自我进化—创建自己的 Skills"：AI 自创建技能形成能力进化）。

### 10.4 知识（Knowledge Bases / 资料库）
- **资料库（Library）**："人和 Agent 共同的产物存放地"。三大模块：①内容管理（个人文档与团队资料统一目录树，任务中直接读取与修改）②多人多 Agent 协作（团队空间与权限、MD 审阅与 AI 修订"以待确认状态呈现，接受后才写入正文"、划词评论、按评论修订、多人协同编辑 HTML）③轻量发布（本地 HTML 发布为在线链接 workbuddy.link；HTML+CSV 搭轻应用，HTML 按表格 ID 读 CSV 实时渲染）。
- **AI 三件套**：MD（内容叙事）/ CSV（唯一数据源，在线表格承载）/ HTML（表达呈现，读 CSV 实时渲染）——"改内容改 MD，改数据改 CSV，改样子改 HTML""改一处、处处生效"。
- 分区：我的文档（仅自己）/ 团队空间（成员可见，权限档位决定范围）；配额 5–50GB 按会员档。
- 添加到任务：选择空间或文档 →"点击添加到任务"；Agent 权限与当前用户完全一致不越权。
- **应用集成**：腾讯文档（知识库）、ima 知识库（功能指引/知识复利/OPC 攻略/创作者/学业助手/求职展示六篇攻略）、乐享知识库、人机双写（字段细节本页未展开，UNKNOWN）。

---

## 11. 权限 / 隐私 / 安全面；升级与审批流

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes ; .../Expert-Center ; .../Connector ; .../Assistant ; .../Automation-Guide ; .../Mailbox

### 11.1 权限模式（两种，输入框底部常驻切换）
| 维度 | 默认权限 | 完全访问权限（Full Access） |
|---|---|---|
| 行为 | 沙箱内高效执行；越界/危险动作暂停请求确认 | 关闭二次确认（写/删/脚本/外部程序不再逐步确认） |
| 生效范围 | 当前任务 | 当前客户端内**所有任务**（全局开关，不跨设备） |
| 风险 | 低 | 高 |

- 切换弹窗："确认允许完全访问？"并列出放开的能力（文件操作、终端命令、访问互联网）；可随时关闭恢复。
- 默认权限下需确认的操作：写入受保护/敏感路径；删除受保护文件/重要目录/批量删除；执行脚本/命令/外部程序；网络访问或敏感能力（命中安全中心规则）。取消则不执行，可让 AI 换安全方式。
- 确认弹窗检查要点（官方教用户看）：操作内容 / 影响范围 / 执行理由。

### 11.2 沙箱与安全中心（设置"安全中心"分组，官方完整字段）
| 分组 | 配置项 | 说明 |
|---|---|---|
| 沙箱 | 安全沙箱 | 总开关，隔离运行，配置文件/命令/网络访问策略 |
| 文件安全 | 文件白名单/黑名单 | 沙箱拦截后的路径规则 |
| 命令安全 | 询问/放行名单 | 命令前缀规则 |
| 网络安全 | URL 与域名规则 | 沙箱网络访问控制 |
| 自动备份 | 每轮对话修改前快照 | 默认开启；同轮次同文件仅首次备份；共享备份空间默认上限 3000MB，按时间清理最早 |
| 数据安全 | 安全网关 | 工作空间出入流量统一经网关（默认开启） |
| 数据安全 | 传输加密 | 本地-云端端到端加密通道（默认开启） |
| 敏感保护 | 敏感信息拦截 | 票据/密码泄露拦截，自定义规则（默认开启） |
| 删除保护 | 优先废纸篓/回收站 | 关闭则系统删除 |
| 删除保护 | 批量删除审批 | 一次删除达阈值（默认 50）需审批；需先开删除保护 |
| 内置运行时 | 随包运行时工具开关 | |
| 审计中心 | 拦截/放行日志 | 支持导出与清空 |

- **敏感保护细节**：自动检测规则库（1Password Secret Key、各类 API Key、Client Secret；标注检测方式：关键词/正则/熵值；"支持加密"标签；可加自定义规则）；检测时机=输入侧（打开小文件/读取内容/输入框输入）+ 输出侧（执行命令/联网搜索/抓网页前）；命中选项：输入侧 允许访问/允许加密访问(推荐)/禁止，输出侧 允许/禁止；**敏感数据管理**：明文"允许并加密保护"后存此生成密文，对话以密文流转、输出自动还原；MCP Token 调用的工具在白名单不弹确认。
- 拦截哲学（官方）："比脚本分析更稳"——在实际执行高风险动作时拦截确认，覆盖动态路径/嵌套脚本/参数级影响/外部程序真实行为。

### 11.3 升级（Escalation）/审批流（公开文档可见的形态）
- **对话内确认升级**：越界/高危操作暂停 → 确认弹窗 → 用户批准或拒绝（拒绝后 AI 换安全方案）。这是产品内最主要的 human-in-the-loop 机制。
- **批量删除审批**：达阈值（默认 50）需审批（安全中心规则）。
- **远程助理高风险确认**：涉及文件删除、系统配置修改、批准命令执行需确认后执行；每条远程指令多层来源校验；绑定身份+换绑。
- **项目/企业治理**：公共授权连接器调用日志仅管理员可见；协作任务禁用个人授权连接器；企业版有管理端（国际站 Team：role-based access admin/member/viewer、IP allowlist、access logs、budget caps、productivity dashboard、per-member usage）。
- **IM 侧升级/审批**：微信助理可"批准命令执行、文件修改等需确认的操作"——审批动作可远程在 IM 完成。飞书侧：官方有《飞书接入指南》（接入机器人收发任务）；**飞书 webhook 形式的席位/升级治理**未见公开文档，本地第一方证据（companion 文件）观察到该机制，官方口径 UNKNOWN。
- 专家/技能/连接器上架审核（开放平台）：发布审核通过/驳回、信息审核、强制下架、资料违规通知（3 送达渠道：开放平台通知中心、端内消息中心、开发者邮箱 openworkbuddy@tencent.com；不可退订）。

---

## 12. 设置（Settings）— 分节枚举

**来源**: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Setting ; .../Memory ; .../Model ; .../Data ; .../Permission-Modes ; .../Assistant ; .../Buddy-App

设置面板：左侧导航 + 右侧内容区，修改即时生效无需重启。

### 用户菜单（头像）快捷入口
企业版（进入企业智能体）/ 查看积分余额（余额与明细）/ 记忆与进化 / 外观（浅色/深色）/ 帮助与反馈 / 检查更新 / 退出登录 / 设置。

### 设置 → 分组与条目（官方全列）
**设置分组**
| 条目 | 说明（官方原文概要） |
|---|---|
| 通用 | 语言、字体大小、锁屏运行、开机自启、网络代理等基础选项 |
| 个人主页 | 账号资料与个人中心入口 |
| 快捷键 | 键盘快捷键查看与配置 |
| 功能个性化 | AI 对话个性化：回复风格、加载欢迎语、自定义指令、称呼与身份 |
| 记忆与进化 | 记忆的管理与清除（查看/编辑/删除/关闭/导入，见 §10.3） |
| 智能体 | 智能体（Agent）相关配置（子字段 UNKNOWN） |
| 模型 | 内置模型与自定义模型接入（模型列表/添加编辑删除/接入方式/自定义协议，见 §7） |
| 助理设置 | 各 IM 平台集成接入（微信助理/微信客服号/企微/QQ/飞书/钉钉），集成卡片（配置/绑定二维码/已绑定状态/解绑按钮） |
| Buddy 应用 | 已连接的 Buddy 应用查看、取消授权 |

**数据与安全分组**
| 条目 | 说明 |
|---|---|
| 数据管理 | 我分享的文件（复制链接/下载/取消分享）+ 已归档任务（删除需二次确认 / 取消归档） |
| 安全中心 | §11.2 全部安全策略配置 |

**关于分组**：版本信息、检查更新、用户协议。
- 各子页具体字段：通用/个人主页/快捷键/功能个性化/智能体仅有概述级官方描述，字段级明细 UNKNOWN。
- 代码开发用户级配置兼容：设置外，`~/.codebuddy/`（rules/skills/commands/MCP）自动加载，与项目级按优先级合并。

---

## 13. 桌面端特有能力（Desktop-specific）

**来源**: 官方文档多篇（Task-Bar、Permission-Modes、WeixinBot-Guide、Mailbox、Design-Idea、Worktree-Task、Model、Right-Sidebar）

- 本地文件操作：读取授权文件夹并批量处理；文件默认本地处理，"原始数据不上传云端"，服务端仅处理数据片段用后即弃。
- 沙箱 + 自动备份 + 回收站式删除（本地文件系统层安全，§11.2）。
- 内置浏览器：登录态持久复用、账号隔离、多页签、设备视口调试（§9.2）。
- 终端命令本地执行（本地环境与依赖），远程指令也在电脑端执行。
- 微信扫码远程遥控桌面端（WeixinBot >= 8.0.70，WorkBuddy >= 4.6.4；手机仅发指令/批准/追问，执行全在电脑）；锁屏运行（设置-通用）、防止合盖休眠建议、锁屏远程开关。
- Agent Mail 我的邮箱（xxx.agent@agent.qq.com，Agent 专属工作信箱，邮件到达触发 AI，附件安全扫描，防邮件内容注入 AI）。
- Git worktree 并行开发（§8.2/§9.4）；`~/WorkBuddy/Worktrees`。
- 本地模型（Ollama）与本地 API Key（workbuddy/models.json）。
- 设计创意模式（WorkBuddy × 腾讯 Ardot）：画布实时生成 UI/PPT/海报，智能框选+对话修改，色块占位/AI 生图开关，设计风格模板（TDesign、Apple、Meta、Miro、Notion、Spotify、Discord、Linear、X AI、Ferrari 等），跳转 Ardot 精修（像素级/组件化/导出 PNG/SVG/PDF/PPTX 切图标注），设计稿一键生成应用代码（"用 React 重写""加 dark mode"）。
- 拖拽文件全局投递、剪贴板粘贴 Chip、微信聊天记录导入 Chip。
- 开机自启、网络代理、锁屏运行（通用设置）。

---

## 14. 状态（States：loading / working / streaming / error / success）

**来源**: Task-Management、Conversation、Right-Sidebar、Task-Bar、Expert-Center、Automation-Guide、Mailbox、FirstTask 等官方文档

- **任务状态机（6 态，官方）**：进行中（执行中）/ 已完成 / 失败（执行出现问题未完成）/ 待处理（等待进一步处理或输入）/ 规划中（正在分析需求整理执行思路）/ 已归档。
- **Streaming/working 表现**：发送后直接进入对话页**无 loading 过渡页**；执行中展示阶段说明（"正在分析数据"）+ 可展开中间步骤；每条回复**实时计时，完成后定格**；结果区同步刷新产物/文件/变更。
- **待确认（升级态）**：默认权限下高危操作暂停并弹确认窗（操作内容/影响范围/执行理由）；消息中心"任务操作"消息=待确认任务，点击直达任务；远程在 IM 也可批准。
- **错误态样例（官方原文可见）**：专家搜索不可用提示"搜索暂不可用，请稍后重试"；附件不合规"顶部报错"；命名校验非法时按钮置灰并提示原因（列出非法字符规则）；上传失败 TIP（检查格式/大文件压缩拆分/查网络）；自动化推送通道断开=红点+"该通道已断开 · 重新绑定"；二维码过期/绑定失败="绑定中..."卡住 FAQ + 重试生成新码；邮箱状态=运行中/已停用/已封禁/冻结（封禁冻结显示错误码和原因，跳邮箱管理页）；灵感"发送到任务"失败停留详情页保留原因可重试；worktree 创建失败自动回滚不遗留半成品；Git 分支切换失败完整回滚。
- **成功态**：任务完成消息进消息中心（点击查看结果）；完成推送（小程序/微信/企微 bot）；产物可分享/上传云端。
- **空态**：消息中心"暂无消息"；任务列表空项目自动隐藏。
- 完整错误码表：官方有《错误码说明》页面但内容未能抓取（UNKNOWN）。

---

## 15. 视觉 / 交互观察（官方截图与营销页，APPROXIMATE）

**来源**: https://www.workbuddy.cn/（官网首页）；https://www.workbuddy.ai/；官方文档站配图文字说明。全部标注 APPROXIMATE。

- 官网首屏：产品名 + "AI Agent 办公新范式"主标语；下载入口（Mac x64/ARM64、Windows x64/ARM64 兼容、App/小程序/网页版在线体验）。
- 官网演示截图（首页大图）呈现的桌面端布局：左侧窄栏自上而下"新建任务 / Claw / 专家 · 技能 · 连接器 · 自动化（四项并列）/ 任务 / 工作空间"；中部任务卡片（示例任务："AI 行业趋势深度研究报告""新能源公司官网生成""金融分析师 Skill 自动创建"）；composer 内可见模型 chip（演示含 "Craft"、"Hy3" 字样）与场景胶囊（APPROXIMATE，截图分辨率有限）。
- 配色与风格：腾讯蓝为主、浅色主题，深色主题存在（设置"外观"）；整体为"轻 IM + 工作台"混合风格（APPROXIMATE）。
- 首页新建任务页：场景胶囊 + 下方"最佳实践案例"一排 4 卡（未选胶囊时默认组，选中切换场景组，可"换一批"）。
- 灵感详情：双栏（左产物、右基础信息+专家+Prompt），卡片显示作者头像昵称。
- 专家/专家团卡片：图 + 能力介绍 + 擅长领域 +（团队）成员 + 任务示例（官方文档图注）。
- 设计创意模式：Ardot 画布 + 对话并排；设计风格模板选择器、素材处理开关。
- 国际站（workbuddy.ai）：极简英文落地页"AI Agent for Everyday Office Work"；腾讯云国际页为标准企业营销页（用例卡片 + 定价卡 + FAQ）。
- 市场推广元素：Nova 大使计划、OPC（一人公司）运营生态白皮书、智能硬件接入白皮书、客户 logo 墙（招商银行、招商证券、中国太平、中国联通、小米、荣耀、美的、OPPO、Insta360、微众银行、易方达、圆通、德邦、唯品会、易车等）（APPROXIMATE，营销页转述）。

---

## 16. OBSERVATION → PATTERN → CURIS GAP（面向 Curis「人才与能力」域；仅记录，不做 Curis 架构决策）

**来源**: 本文件全部章节 + companion 文件 `CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE.md`（本地第一方证据）

### O1. 三层能力模型："能力 / 角色 / 团队"分离
- **OBSERVATION**：WorkBuddy 用一张官方对比表固定三概念：Skill=能做什么（工具），专家=谁能帮我做（人设+方法论+工具链），专家团=多专家协作（团长拆解、并行、整合）；灵感="实际做出了什么"（成果反查）。专家团积分明示 3–5 倍。
- **PATTERN**：能力供给按"可复用单元"分级：单能力（Skill）→ 单角色（Expert）→ 编排角色组（Team，含 leader 角色与协作流程）。每一级都有独立的展示卡片、独立的市场/中心、独立的成本口径。
- **CURIS GAP**：Curis 本地证据已有 teams（含 software-engineer / software-qa-engineer 角色），即存在"角色组"形态；需要对照盘点：Curis 是否有等价的"单能力（Skill/工具）→ 单人才（专家）→ 团队编排"三层公开模型与各自的字段、成本、入口表达，以及"成果反查能力"（灵感式导购）是否存在。

### O2. 专家卡片 = 极简三字段 + 召唤制（无安装制）
- **OBSERVATION**：专家卡片官方仅承诺四个字段（能力介绍、擅长领域、任务示例、专家团加团队成员）；专家不是"安装"对象而是"召唤"对象，常用置顶持久化；最近使用列表内搜索；专家团会话不可中途换专家（须开新对话）。评分/模型/发布者/使用量等字段 UNKNOWN——官方反而弱化了字段复杂度。
- **PATTERN**：面向非技术用户的能力选择被压缩到"看三个字段 → 一键召唤 → 直接出活"；理解成本转移到"成果案例"（灵感做同款自动带配置）而非参数化比较。
- **CURIS GAP**：若 Curis 人才卡沿用更重的字段模型（本地证据待比对），需评估普通用户理解成本；以及 Curis 是否有"成果案例 → 反向加载人才+技能+Prompt"的导购闭环。

### O3. 市场供给两端开放 + 平台治理
- **OBSERVATION**：专家 140+/12 行业（官方）、SkillHub 7 万+（第三方口径，上线时 1.3 万）；供给来自官方预制、用户自建（我的专家/创建技能）、开放平台第三方上架（open.workbuddy.cn，含发布审核/驳回/强制下架/通知三渠道）；技能有安全审核与"恶意提示词注入/越权/后门"警示。
- **PATTERN**：能力市场 = 官方精选 + 社区规模 + 第三方生态 + 平台审核治理四层；规模数字本身是营销资产。
- **CURIS GAP**：Curis 若规划连接器/技能市场，需明确官方精选层与治理层（审核、下架、通知送达）是否在范围；规模叙事是否可复制。

### O4. 工具链挂载走"授权边界"而非"配置面板"
- **OBSERVATION**：专家"本身不主动获取系统权限"，仅当配备 Skill/MCP 时"在授权下间接访问"；连接器每项独立授权（OAuth/扫码/MCP 三种），绿点+开关状态；项目层分公共授权/个人授权，协作任务强制禁用个人授权；公共授权调用日志仅管理员可见。
- **PATTERN**：能力的权限不内嵌于专家对象，而是运行时按"调用边界"逐层授权（专家→Skill/MCP→连接器→数据范围），并以组织层（公共票据/审计日志/协作禁用个人票据）收口。
- **CURIS GAP**：对照 Curis 人才与能力的授权模型：是否存在"角色不自带权限、按调用边界授权"的原则；是否存在公共/个人票据双轨与协作场景禁用规则；管理员审计面是否成形。

### O5. 审批/升级（Escalation）有四级形态
- **OBSERVATION**：①对话内确认弹窗（操作内容/影响范围/执行理由三要素教学）②批量删除阈值审批（默认 50，安全中心可配）③自动化/远程任务的高危操作确认（可远程在微信/企微批准）④组织层审计中心（拦截/放行日志导出）。本地第一方证据另有席位/升级治理与飞书 webhook 升级（官方公开文档未描述该形态）。
- **PATTERN**：升级不是单一弹窗而是"任务内 → 阈值规则 → IM 远程批准 → 审计留痕"的梯度体系；通知（任务完成/待确认）统一走消息中心+IM 双通道。
- **CURIS GAP**：比对 Curis 现有升级机制覆盖的层级（本地证据显示已有飞书 webhook 升级）；尤其"IM 远程批准高危操作"是否纳入；阈值类审批规则是否可配置。

### O6. 自动化 = 个人定时任务 + 执行留痕 + 推送出口
- **OBSERVATION**：自动化字段固定七项（名称/提示词/工作空间/权限模式/模型技能专家连接器/定时规则/推送）；触发仅定时（周多天/月多天合并单规则）；执行历史可查（字段 UNKNOWN）；官方文档未详述"执行记忆"，但本地第一方证据观察到自动化带执行记忆；推送出口=小程序/企微 bot（单向、不回写上下文、通道断开红点提示、失败不阻塞任务）。
- **PATTERN**：自动化被刻意做成"个人级、低治理负担"：仅创建者可见、无团队共享自动化；可靠性表达集中在"通知可达性"而非"重试策略"（失败重试策略 UNKNOWN）。
- **CURIS GAP**：对照 Curis 自动化：执行记忆的呈现方式、失败重试、以及是否需要团队级自动化（WorkBuddy 明确不做，可能是差异空间或风险信号）。

### O7. 记忆与进化绑定"人才"心智
- **OBSERVATION**：设置入口名为"记忆与进化"；记忆每晚自动摘要、可编辑/删除/关闭/跨 AI 导入；"进化"的官方落点是"自我进化—创建自己的 Skills"（实践八）——即记忆沉淀为可复用技能，而非人才个性化。
- **PATTERN**：个人记忆（偏好/事实/关系/跟进）与能力资产（Skill）分开演进；"懂你"落在通用层，"更强"落在技能资产层。
- **CURIS GAP**：Curis 若让"人才"拥有持续记忆/成长叙事（本地证据未覆盖），需与 WorkBuddy 的"记忆归用户、技能归资产"切法对比，决定人才记忆的归属层（仅记录差异，不做决策）。

### O8. 组织侧"人才"治理靠项目配置注入
- **OBSERVATION**：项目配置五字段（名称/指令/连接器/专家/技能）在任务创建时自动注入上下文；任务内选择范围=项目+个人+专家中心，项目专家置顶；成员动态（增删 Skill/专家/连接器）会广播到项目动态流；国际站企业版另有 custom agent 创建/版本化/部署、共享 skills/experts/knowledge base（RAG）、Playbooks、ROI 看板。
- **PATTERN**："团队统一的人才/能力配置"通过"项目默认值 + 置顶排序 + 配置变更广播 + 管理员审计"实现，而非强管控；企业版才出现 Agent 版本化与 ROI 度量。
- **CURIS GAP**：Curis 组织级人才管理（若在 Blueprint 范围）可对照：默认值注入、置顶、变更可见性、版本化、ROI/用量看板这五个能力位哪些已有/缺失（仅盘点，不做决策）。

### O9. 模型层与人才层解耦，明示成本档位
- **OBSERVATION**：模型选择独立于专家（对话内快选 5 家 + 三档调度 + 思考强度/上下文/Max）；每档/每专家团都有明确积分倍率叙事（专家团 3–5 倍）；自定义模型本地存 Key；积分规则（按到期顺序、基础优先于赠送）公开成文。
- **PATTERN**：成本透明是人才/能力商业化的一部分：用户在任何选择点都能感知"这个角色/模式多贵"。
- **CURIS GAP**：Curis 人才选择的成本表达（若存在积分/额度体系）是否同样透明、粒度是否到"角色/团队"级。

---

## 附：官方文档站全目录（本研究的地图，路径前缀 https://www.workbuddy.cn/docs/workbuddy/）

- 入门指南：Overview、Quickstart、Changelog、Download-History、Create-Task、Task-Management、Conversation、Results、FirstTask
- 从入门到精通指南：Installation-Win/Mac-Guide；Function-Description：Task-Bar、Design-Idea、Assistant、Project、Buddy-App、Worktree-Task、Expert-Center、Skills-Market、Ispiration、Mailbox、Connector、Library（+Content-Management/Collaboration/Lightweight-Publish）、Knowledge-Base（Tencent-Doc、IMA×6、Lexiang、Cowriting）、Automation-Guide、Right-Sidebar、Setting、Permission-Modes、Memory、Model、Data、Feedback；Practice-Cases 一至十一；Efficient-Tips；Zero-Cost-Skill-Top-10×10；FAQ、Error-Code
- 助理接入指南：WeixinBot、Wechat、Wecom、QQ、Feishu、Dingtalk
- 账号：Pricing、Credits、Plan、Usage、Billing、Invoice
- 支持：Contact
- 产品线：/docs/ide/、/docs/plugin/、/docs/cli/、/docs/workbuddymini/、/docs/workbuddyapp/、/docs/enterprise/

**未抓取/UNKNOWN 汇总**：FAQ、Error-Code、Feedback、Plan/Usage/Billing/Invoice、Knowledge-Base 各子页、Library 三个子页、Practice-Cases、Efficient-Tips、Changelog、企业版文档（cloud.tencent.com/document/product/1831）、专家详情页字段、专家/技能市场的筛选排序与完整分类枚举、各设置子页字段级明细、执行历史字段、失败重试策略、桌面端全局搜索快捷键。

---

## Sources

1. 官网（中文）: https://www.workbuddy.cn/
2. 官网（国际）: https://www.workbuddy.ai/
3. 腾讯云国际 WorkBuddy 活动页: https://www.tencentcloud.com/act/pro/workbuddy
4. 官方文档-简介: https://www.workbuddy.cn/docs/workbuddy/Overview
5. 官方文档-快速开始: https://www.workbuddy.cn/docs/workbuddy/Quickstart
6. 官方文档-开启你的第一个任务: https://www.workbuddy.cn/docs/workbuddy/FirstTask
7. 官方文档-创建任务: https://www.workbuddy.cn/docs/workbuddy/Create-Task
8. 官方文档-任务管理: https://www.workbuddy.cn/docs/workbuddy/Task-Management
9. 官方文档-任务对话: https://www.workbuddy.cn/docs/workbuddy/Conversation
10. 官方文档-结果查看: https://www.workbuddy.cn/docs/workbuddy/Results
11. 官方文档-新建任务栏: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar
12. 官方文档-专家: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Expert-Center
13. 官方文档-技能: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market
14. 官方文档-连接器: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector
15. 官方文档-项目: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project
16. 官方文档-资料库: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Library
17. 官方文档-自动化: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide
18. 官方文档-右侧边栏: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar
19. 官方文档-系统设置: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Setting
20. 官方文档-默认权限与安全沙箱: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes
21. 官方文档-记忆: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory
22. 官方文档-模型配置: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Model
23. 官方文档-数据管理: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Data
24. 官方文档-助理: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Assistant
25. 官方文档-Buddy 应用: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Buddy-App
26. 官方文档-设计创意: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Design-Idea
27. 官方文档-灵感: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Ispiration
28. 官方文档-我的邮箱: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Mailbox
29. 官方文档-Git 集成和并行开发: https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Worktree-Task
30. 官方文档-微信助理接入指南: https://www.workbuddy.cn/docs/workbuddy/WeixinBot-Guide
31. 官方文档-定价详情: https://www.workbuddy.cn/docs/workbuddy/Pricing
32. 官方文档-积分说明: https://www.workbuddy.cn/docs/workbuddy/Credits
33. 腾讯云开发者社区-《WorkBuddy「行业专家」正式上线 一句话召唤140+位专家》: https://cloud.tencent.com/developer/article/2640403
34. 量子位-《WorkBuddy 杀疯了？一群 AI 专家帮我打工》: https://www.qbitai.com/2026/03/391894.html
35. CSDN-《WorkBuddy 技能市场上手指南：三种方式一键安装技能》: https://blog.csdn.net/u013176440/article/details/163773511
36. 财联社-SkillHub 上线: https://www.cls.cn/detail/2310349
37. 新浪财经-腾讯龙虾技能社区 SkillHub 上线（13,000+ 技能）: https://finance.sina.com.cn/tech/digi/2026-03-12/doc-inhqstev8770052.shtml
38. OSCHINA-SkillHub 报道: https://www.oschina.net/news/409758
39. SkillHub 官网: https://skillhub.cn/ ；腾讯云 SkillHub: https://skillhub.cloud.tencent.com/skills
40. 云站-《WorkBuddy 技能市场值得用吗？7万+技能包功能实测》（70,000+ 口径来源，APPROXIMATE）: https://www.yun88.com/news/11277.html
41. 腾讯软件中心 WorkBuddy 页: https://pc.qq.com/detail/11/detail_56131.html
42. 关联本地证据文件: `/Users/yy/Documents/Curis AI Workspace/docs/research/system_competitive_research/CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE.md`（未修改）
