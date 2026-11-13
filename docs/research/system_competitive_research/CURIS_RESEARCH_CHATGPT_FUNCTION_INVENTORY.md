# Curis 竞品研究：ChatGPT 桌面端与当前应用功能清单

- Authority Class: RESEARCH
- Status: Draft
- 研究日期：2026-09-12（信息截至当日，均标注来源 URL）
- 研究对象：ChatGPT Desktop app（macOS / Windows，含新版 "ChatGPT" 应用与旧版 "ChatGPT Classic"）、chatgpt.com 当前应用功能
- 研究方法：官方 Help Center（help.openai.com）、OpenAI 产品页（chatgpt.com / openai.com）、可获得的社区与第三方资料；视觉描述均为近似（APPROXIMATE），未逐屏截图核验
- 用途：为 Curis（AI Company OS：AI Employees / Teams / Workspaces / Knowledge / Meetings / CEO Assistant）提供竞品功能边界参照。本文档只是 Research Evidence，不能覆盖 Curis 的 Current Authority。

> 重要背景：截至 2026 年，ChatGPT 的产品结构已从"单一 Chat + 工具"演进为 **Chat / Work / Codex 三分结构**。ChatGPT agent（agent mode）官方文档已标注被新的 **ChatGPT Work** 替代（社区与第三方来源；官方 help 文章仍保留 agent 说明）。桌面应用也已重构为"新版 ChatGPT 应用（含 Chat、Work、Codex）+ ChatGPT Classic（旧桌面应用）并存"。本清单按当前状态记录，并注明历史形态。

---

## 1. 产品总览（Overview）

- 定位：通用 AI 助手 + 个人/团队工作代理。三大体验面：
  - **Chat**：快速问答、搜索、日常对话（帮助文档："Ask questions, search, and have conversations"）。
  - **Work**：面向更长时程、多步骤工作的 agent，产出"finished deliverables"（文档、电子表格、演示文稿、报告、Sites）。网页/移动端在云端运行；桌面端可经授权使用本地文件与桌面应用。
  - **Codex**：软件开发专用（本地文件、repo、终端、开发者工具），仅桌面可选，web/移动不可选（移动端 Remote tab 可访问 desktop Codex chats）。
- 交付形态：Web（chatgpt.com）、macOS app、Windows app（Microsoft Store / winget）、iOS / Android。
- 计划线（来源 chatgpt.com/pricing 导航）：Free、Go、Plus、Pro（注：页面横幅显示 Pro $200 新注册/升级暂停）、Business、Enterprise、Edu、K–12 Teachers；另有 Healthcare 工作区变体。
- 模型（帮助文档可见）：GPT-6 Pro（powered by GPT-6 Astra，Pro $100/$200、Business、Enterprise 可用；Plus 在 Work/Codex 中含 Astra）、GPT-5.6 Sol 等。旧模型 GPT-4o/4.1/o4-mini/GPT-5 已于 2026-02-13 退役。
- 来源：
  - https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
  - https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app
  - https://help.openai.com/en/articles/8554397-creating-and-editing-gpts
  - https://chatgpt.com/work/

---

## 2. 应用壳（App Shell）与桌面特有行为

### 2.1 新版桌面应用（ChatGPT，含 Chat/Work/Codex）

- 顶部结构：左上角菜单切换 **ChatGPT / Codex**；进入 ChatGPT 后顶部 toggle 切换 **Chat / Work**。
- 侧栏（Sidebar，APPROXIMATE，综合帮助文档与产品描述）：
  - **Recents**：Chat 与 Work chats 混合显示，可 sort / filter（全部 / 仅 Chat / 仅 Work）/ pin。
  - **Projects**：现有 ChatGPT Projects 显示在 Projects 区；从 project 内选择 Chat 或 Work 开新 chat，Work chat 会使用 project 上下文。
  - **GPTs 区**：Explore GPTs 入口（chatgpt.com/gpts），My GPTs 管理（帮助文档对应 web，桌面近似）。
  - **Library**：云端 Work 产出的文件可保存到 Library；web 上有 Library → New → View templates → Create template 路径。
  - **Scheduled**：任务页（在桌面 app 是否可见取决于 app 版本与账户；event-triggered tasks 桌面只能查看，不能创建/编辑 trigger）。
  - Codex 为独立 view，历史与 ChatGPT 历史分离。
- **ChatGPT Voice（新）**：桌面 Work/Codex 的实时语音界面，可自然打断、口述协调任务；需要麦克风权限，Computer context 需要 Screen & Audio Recording 与 Accessibility 权限；同时只能有一个 Voice 会话；Voice 计量在 flexible pricing 下单独计量。
- **内置浏览器体验**：桌面 app 新增 built-in browser，支持多 tab、跨工具/文件/账号的 agentic workflow。
- Cloud Work chats 跨 web/mobile/desktop 同步；本地 desktop Work chats 的"messages and task context may be stored in the cloud"。
- 来源：
  - https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app
  - https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
  - https://chatgpt.com/work/

### 2.2 ChatGPT Classic（旧 macOS/Windows 桌面应用）

- 仍可用，继续获得模型更新、bug 修复、安全补丁；新 agent features 只在新 app。
- macOS：**Option + Space** 全局快捷键打开 companion 窗口（Chat Bar，置顶小窗）；OpenAI 官方公告确认。
- Windows：**Alt + Space** 打开 Companion Window（需 app 已打开）；窗口记住上次位置，重置后回到底部居中；快捷键冲突时需在 **Settings > App > Companion window hotkey** 修改。
- Companion 窗口能力：提问、上传文件、生成图片、New chat 清空；关闭后可用快捷键重开或从主窗口侧栏历史继续。
- 旧 macOS app 截图/文件行为：可上传文件、拍照（帮助文章 "ChatGPT macOS app - File Uploads and Photos"）。
- 企业分发：Microsoft Store + MDM/MAM（Intune）、winget 安装；Enterprise/Edu 保留策略默认不用于训练。
- 来源：
  - https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app
  - https://help.openai.com/en/articles/10003026-windows-app-release-notes
  - https://x.com/OpenAI/status/1820914089612439622
  - https://help.openai.com/en/articles/9295234-chatgpt-macos-app-file-uploads-and-photos

---

## 3. Projects（项目工作区）

> 与 Curis Workspace 的直接对标物。

### 3.1 定位

- "smart workspaces"：把 chats + 参考文件 + custom instructions 聚合于长期工作；带项目级 memory；支持跨设备续做、重复性工作流。
- 可用性：所有 free/付费用户全球可用；Business/Enterprise/Edu 可共享项目（2025-10-22 起个人计划 Free/Plus/Pro/Go 也支持 sharing）。

### 3.2 字段级清单（field-level）

| 字段/能力 | 说明 |
|---|---|
| 名称 Name | 建项目时设置 |
| 图标 Icon + 颜色 Color | 建项目时选择；共享后默认图标会变为"共享"样式（自定义图标则不变） |
| Project instructions（项目指令） | 项目 > 三点菜单 > Project settings；只在本项目生效，**覆盖全局 custom instructions** |
| Files（项目文件） | 上传 PDF/表格/文档/图片/粘贴文本；预览/下载/删除；重名文件选 Upload anyway / Skip；单次最多同时上传 10 个 |
| Links from apps（App 链接源） | 支持粘贴 Google Drive（文件/文件夹）与 Slack（频道）链接作为 project sources；需连接并授权 |
| Save to project（保存回复） | 把某条 chat 回复保存为 project source 复用 |
| Chats | 项目内新建、拖拽/菜单 Move to project 移入已有 chat（GPT 生成的 chat 不可移入；Temporary chat 不可加入）；移入后继承项目指令与文件上下文 |
| Branching（分支） | 从已有 chat 分支新对话（标题 'Branch'），保留原线程；可见发起人 profile icon |
| Memory 设置 | Default memory / Project-only memory（建项目时选，Project settings 里可改；改动需数小时生效） |
| Members（共享） | Edit 权限（改指令、传/删文件、邀请他人，不能移除成员）/ Chat 权限（可见可用，不能邀请）；Owner 可改名、删项目、移除成员、设权限 |
| 邀请方式 | Only those（个人邮箱/群组）或 Anyone with a link；Business/Enterprise/Edu 可用 workspace link（默认 chat 权限）；SCIM 组可见性由 admin 控制 |
| 协作上限 | Pro：40 文件 / 100 协作者；Plus 与 Go：25 文件 / 10 协作者；Free：5 文件 / 5 协作者；Business/Enterprise/Edu：40 文件，workspace 项目 100 人 |
| 删除 | Delete project 永久删除全部文件/chats/指令（含共享项目） |
| Leave project | 成员可退出，退出前可复制自己的 chats（Copy 前缀新项目） |
| Admin 控件 | Workspace settings 里 Projects 开关；Shared projects toggle（RBAC）；Compliance API（isolate project、列出共享用户）；继承 workspace 工具/保留/驻留设置 |

### 3.3 Memory in Projects（关键机制）

- Default memory：引用 saved memories；项目内 chat 可互引；Enterprise/Edu 下项目 chat 与项目外完全隔离；非 Enterprise（含 Business）下项目内外可互引（除非另一项目为 project-only）。
- Project-only memory：不引用项目外记忆/chat；共享项目强制 project-only 且不可改；**ChatGPT Work 在 project-only memory 项目中不可用**。
- 项目 memory 没有可查看的记忆列表（与个人 memory 不同）。
- 来源：
  - https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt （本节全部字段出处）

---

## 4. Custom GPTs 与 GPT Store

> 与 Curis "AI 人才与能力" 的对标物（角色 = 配置化 GPT）。

### 4.1 GPT 定义与组成（field-level）

GPT = 配置化的 ChatGPT，可包含：

| 配置字段 | 说明 |
|---|---|
| Name | 在搜索结果、GPT Store、分享链接、聊天顶部显示 |
| Description | 用途摘要，出现在预览与 GPT Store 列表 |
| Conversation starters | 打开 GPT 时显示的示例 prompts |
| Instructions | 行为定义（做什么、如何回应、避免什么），作用于每次对话；官方写法建议：显式步骤结构（"When X → do Y"）、正向指令、含正反例、用标题与列表 |
| Knowledge | 上传文件作参考素材；上限 **20 个文件，每个 512 MB**；部分文件类型需开启 Code Interpreter & Data Analysis |
| Recommended model | 建议用户新对话使用的模型；不可用时自动选相似模型 |
| Capabilities | 内置能力开关：Web search / Image generation / Canvas / Code Interpreter & Data Analysis / Apps |
| Apps（连接外部服务） | GPT 可用用户已连接的 app；**GPT 只能在 Apps 与 Actions 二选一** |
| Actions | 自定义外部 API 连接（OpenAPI schema 定义；见 Configuring actions in GPTs） |
| Version history | ••• 菜单中可查看/恢复旧版本（恢复含 actions 的版本可能需重配认证） |
| Sharing | 指定人 / workspace / 链接 / GPT Store 发布（视 plan 与 workspace 权限；发布要求见 Sharing and publishing GPTs） |

- 构建方式：**Conversational builder**（对话生成配置）或 **Configuration view**（直接编辑字段）；Preview 内测试。
- 关键现状（2026-02 起）：**个人账号（Free/Go/Plus/Pro）不能新建/发布 GPT**；已有 GPT 可继续使用、符合权限可编辑；Business/Enterprise/Edu 按工作区权限可建/编/发布。GPT creation 仅在 web（移动只能使用）。
- GPT 不使用 saved memory / custom instructions / 历史 chat（每次对话全新开始）。
- GPT builders 无法查看用户与其 GPT 的具体对话。
- @ 提及：web 上在对话中输入 @ 可把某 GPT 引入当前对话且保留上下文（移动端不支持）。
- GPT Store listing 字段（名称、描述、分类、Builder Profile 等）：官方 Sharing and publishing GPTs 文章覆盖，本文件未逐字段核验 = UNKNOWN（公开 GPT Store 于 2025-2026 年逐步被 workspace 化/插件目录调整，个人新发布已停）。
- 来源：
  - https://help.openai.com/en/articles/8554407-gpts-in-chatgpt
  - https://help.openai.com/en/articles/8554397-creating-and-editing-gpts

---

## 5. ChatGPT Work（当前 agent 交付面）

> agent mode 的后继产品；与 Curis Work/Result/CEO Assistant 对标。

- 入口：桌面顶部 toggle 选 Work；web/mobile 选 Work；project 内也可开 Work chat。
- 描述式委派：给出目标/文件/约束/审阅标准；Work 收集上下文 → 制定计划（**Plan mode：先问问题、给 step-by-step plan，可改或批准后开工**）→ 执行 → 产出 deliverable；同一 chat 内继续修改。
- 计划与调度：Work 可一次性运行、按 schedule 重复、由触发器（trigger）启动、或监控变化（monitor），均可通过 **Scheduled** 管理。
- Event-triggered（webhook）tasks：Gmail 新邮件 / Slack 新频道消息（需把 @ChatGPT 拉入频道）/ GitHub PR 活动；展示 **Trigger / Condition / Prompt** 三个字段；限 Plus/Pro/Business/Enterprise/Edu/Healthcare；Free/Go/FedRAMP 不可；Enterprise/Edu/Healthcare admin 需开启 "Allow event-triggered scheduled tasks"。
- 产出物：文档/电子表格/演示文稿/报告/**Sites**（可分享的交互网站/web app，随信息更新保持新鲜）；支持 native Google Docs/Sheets/Slides（需启用相应 Google Workspace app）；桌面支持 ChatGPT for Excel add-in 直接操作 Excel；PowerPoint 桌面 flow 未含（有独立 ChatGPT for PowerPoint app）。
- 模板（Template）体系：@Template-Creator 由参考文件+复用指令生成模板；@Documents / @Spreadsheets / @Presentations 打开 Templates gallery；web Library 管理；模板跨 web/Codex 不同步；workspace 分发需打包为 plugin。
- 文件保存：云端 Work 产出存 **Library**；本地桌面产出留在本地 project/folder。
- 权限模型：Work Cloud / Work Local / Codex Local 三类 workspace 权限（Permissions & roles 分开控制）；浏览器与网络访问单独控制；Workspace settings > Models 可设 Work & Codex 起始模型/推理级别/Fast Mode。
- 用量：Work 遵循 Codex 同款用量结构（included usage + credits）；Astra 用量消耗快于 GPT-5.6 Sol。
- 来源：
  - https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
  - https://help.openai.com/en/articles/20001278-creating-and-editing-documents-spreadsheets-and-presentations-with-chatgpt-work
  - https://chatgpt.com/work/

---

## 6. Agent mode（ChatGPT agent；历史形态，文档仍可考）

- 启动：tools 菜单选 agent mode 或输入 `/agent`；描述任务 → 执行；会暂停请求澄清/确认；可中途引导或打断。
- 虚拟计算机：虚拟浏览器 + 终端；通过截图"看"网页并操作；**takeover mode**（••• → Take over browser）用于登录等敏感输入（接管期间不截图）；cookies 跨会话保留，可在 Data controls 清除。
- Connectors：可用 apps 作为数据源（composer connectors 菜单：Web search、Box、Gmail、Google Calendar 等）；agent 不能访问带 sync 的 app 数据（如 Google Drive sync）。
- 安全：高影响操作需用户确认、prompt injection 监控、"watch mode"（部分站点需人监督）、网站黑名单；输出含来源链接或截图。
- 调度：任务完成后点 **Clock icon** 可设 daily/weekly/monthly 重复；chatgpt.com/schedules 管理（••• → Edit schedule）。
- 用量限额：Plus 40 msg/月；Pro 400 msg/月；Business & Enterprise 40 msg/月（flexible pricing 30 credits/msg）；仅用户主动发起计费；agent 调用计入 scheduled tasks 用量。
- 企业控制：workspace 默认 OFF 的 toggle、RBAC、app 控件、Compliance API（只记会话级，不记具体 agent 动作）、域名屏蔽（精确/整域）、数据驻留。
- 设备：Web、iOS/Android、桌面均可。
- 现状：官方 agent help 文章仍在，但多个社区/第三方来源指出 agent mode 已被 ChatGPT Work 取代（"ChatGPT agent is no longer available. Use ChatGPT Work"）；Operator 功能已并入。
- 来源：
  - https://help.openai.com/en/articles/11752874-chatgpt-agent
  - https://openai.com/index/introducing-chatgpt-agent/
  - https://www.usecarly.com/blog/chatgpt-agent-mode/
  - https://community.openai.com/t/solved-cant-get-agent-mode-to-run-in-any-project/1373479

---

## 7. Deep Research

- 用途：多源调研、比较证据、产出带引用的结构化报告；可在 **Chat / Work / Codex** 使用。
- 启动：`@Deepresearch` 直接在聊天输入；Chat 中也可 tools 菜单（+）选择。
- 流程：描述目标（含报告结构）→ Chat 中生成可编辑的 research plan（可修改；可指定网站）；Work/Codex 中先问 clarifying questions → 运行中可实时看进度、随时打断调整焦点/来源 → 结构化报告。
- 来源控制：Chat 默认用 public web + 上传文件 + 可用 connected apps（只读 read actions，不用 write actions）；**Sites > Manage sites** 可限定站点或"优先这些站点但允许全网搜索"。
- 结果视图（Chat，APPROXIMATE）：全屏报告视图，含 **table of contents**、**sources used** 区、**activity history**（研究过程回放）；可导出 Markdown / Word / PDF。
- 用量：Chat 侧独立 plan 配额（30 天滚动重置）；Work/Codex 侧消耗 Work/Codex allowance 或 credits。
- 企业：RBAC 控制（Deep research permission；web search 必须开启）；遵守 workspace app 启用与角色权限。
- 来源：
  - https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt
  - https://openai.com/index/introducing-deep-research/

---

## 8. Scheduled tasks（定时/监控任务）

> 与 Curis 任务化/例行自动化最直接的对标。

- 入口：**Scheduled** 页（chatgpt.com/tasks / 侧栏入口）；Settings > Notifications > Manage tasks 也可打开；对话内 ••• → See scheduled tasks。
- 类型：
  1. **One-time / recurring（定时）**：一次性或重复任务；
  2. **Monitoring（监控）**：检查变化、相关更新时通知，可用前次运行结果，满足结束条件后停止；
  3. **Event-triggered（webhook）**：Gmail / Slack / GitHub 事件驱动，字段为 **Trigger / Condition / Prompt**，在 Work 内运行。
- 创建方式：自然语言（如 "Let me know when my package is delivered"）→ ChatGPT 显示任务确认卡（任务名 + 时间，如 "Mom's birthday – March 13, 9 AM"）；项目内创建的任务不能访问项目内上传文件。
- 任务面板字段：标题、instructions、schedule、时区；操作 Edit / Pause / Delete / Manage tasks（任务 ••• 菜单）。
- 通知：Settings > Notifications 选 **Push / Email / both**；浏览器通知权限被禁时提示 Allow；移动端需在 app 内创建任务并授权推送。
- 频率与限额（field-level）：
  - 活跃任务数：Free/Go 3；Plus 5；Business/Edu 10；Pro/Enterprise 15。
  - 频率：Free 只能一次性或每天最多一次（灵活时段：morning/afternoon/night）；付费可每小时、可精确时间；event-triggered 全账户合计 30 次/小时、720 次/天（多事件可合并）。
  - 不支持：Voice chats、GPTs。
  - 需审批的动作会让任务暂停，直到人审批。
- 分享：可分享 eligible 任务链接（快照：标题/instructions/schedule/原时区，可保留 mode/model）；不含创建者身份、聊天历史、既往结果、记忆、自定义指令、附件、连接凭证；收件人 "Log in to schedule" 后在 **Shared with you** 中调整并 Schedule task 生成独立副本；链接可删除（不影响已生成副本）；已完成任务与新任务分享受限。
- 数据：Compliance API 覆盖 scheduled tasks（但 shared task links 快照未覆盖）；数据导出不包含 tasks/shared links。
- 与 Codex automations 区分：Scheduled 在 ChatGPT；Codex automations 在 Codex（developers.openai.com/codex/app/automations）。
- 案例：连接 ChatGPT Finances 会自动创建 "Weekly finances update" 任务（可 Pause/Delete）。
- 来源：
  - https://help.openai.com/en/articles/10291617-tasks-in-chatgpt
  - https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex

---

## 9. Memory 与个性化

- 位置：**Settings > Personalization > Memory**；可随时开关。
- **Memory summary（新记忆系统）**：
  - 自动从 chats/files/connected apps 综合记忆；summary 顶部显示 "last updated X ago"；可点 "Refresh"（••• 菜单）。
  - 编辑：底部文本框直接输入修改；或高亮具体文本做更正。
  - 删除：Delete and turn off memory（••• 菜单）删除 summary 且关闭 memory（不删历史 chats；重开后可能从旧 chat 生成新记忆）。
  - **Memories in sources**：每条回复下方 book 图标显示本次个性化用了哪些来源（custom instructions / past chats / files / memories）；点某条 memory 可看"为什么被使用"，可 ••• 更正；分享链接不含 sources。
  - 可回退 legacy "saved memories"（逐条记忆）：Settings > Memory > "saved memories" 链接切换；saved memories 与聊天历史分开存储（删 chat 不删 memory）；保留已删 memory 日志最多 30 天。
- **Custom Instructions**：Settings > Personalization（移动端 Customize ChatGPT）；Enable customization toggle + 指令文本框；字数上限 Free/Go 1,500 字符，Plus/Pro/Enterprise/Business/Education 5,000 字符；立即对所有 chat 生效；随账号删除 30 天内清除；可导出。
- Temporary Chats：不使用也不产生记忆；不可加入 Projects。
- Enterprise/Regulated workspace：improved memory 默认关闭，owner 可按角色开放（不覆盖 BAA 限制）；Business 有单独 Memory FAQ。
- 来源：
  - https://help.openai.com/en/articles/8590148-memory-faq
  - https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt

---

## 10. Canvas 与文档编辑（历史 + 现状）

- Canvas（2024-10 引入）：写作/编码的独立编辑界面——内联编辑、选中局部要求修改、Google Docs 式评论、全屏模式、代码运行、导出/下载；曾为 GPT capability 之一。
- 现状（2026）：文档/表格/演示编辑主要由 **ChatGPT Work** 承接（第 5 节）；帮助文档中 Canvas 仍作为 GPT capability 与项目内工具列出（"Canvas to draft docs, code, or layouts"），但独立 Canvas 帮助文章已指向 Work 文档编辑（第三方报道"quietly killed it"）。状态介于两者之间，精确 UI 归属 = UNKNOWN。
- 来源：
  - https://openai.com/index/introducing-canvas/
  - https://help.openai.com/en/articles/20001278-creating-and-editing-documents-spreadsheets-and-presentations-with-chatgpt-work
  - https://medium.com/@mubashirburfat4/i-used-chatgpts-canvas-feature-for-six-months-then-openai-quietly-killed-it-88c542f1a63f

---

## 11. Voice

- 形态：
  - **Standard Voice**（当前主推）：自由语音对话，长按麦克风开始；支持 web/mobile/desktop。
  - **Advanced Voice**：上一代实时语音，保留用于需要 video/屏幕共享等移动能力的场景。
  - **Voice with Video**：移动端视频语音（chatgpt.com/features/voice-with-video）。
  - **ChatGPT Voice（桌面 Work/Codex）**：见 2.1；语音协调任务，桌面专属，单一并发。
- 限制：Voice mode 不支持 apps；Scheduled tasks 不支持 voice chats。
- 来源：
  - https://help.openai.com/en/articles/8400625-voice-mode-faq
  - https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex

---

## 12. Connectors / Apps / Plugins / MCP

- 体系（2026-07-09 起）：**Apps**（连接外部服务：Google Drive、Slack 等）+ **Plugins**（打包 apps/skills/app templates 成工作流，Plugins Directory 为主要发现入口，1,400+ plugins）+ **MCP**（用 Model Context Protocol 构建自定义 app；Apps SDK 打包发布；Developer mode 管理 custom MCP apps）。
- App 能力分级：Interactive apps（卡片/地图/歌单）、Search、Deep research、Sync（预索引加速）、Write actions。
- 权限（field-level）：
  - 个人默认：Settings > Apps > App Preferences > **Ask permission**；档位 Always ask / Allow read actions / Allow low-risk actions / Allow all actions（后者不给标准选择器）。
  - **Important actions** 默认档：读自动、有意义外部影响的写操作先询问（发邮件、删内容、购买、上传/移动文件、改共享权限、分享敏感信息等）。
  - 审批卡：Deny / Allow（once）/ Allow low-risk actions / Always allow。
  - 单 app 覆盖：Plugins Directory > app > Preferences > Ask permission；Reset to default。
- 工作区管理：Workspace settings > Apps（Directory / Enabled / Drafts tabs；Business 默认启用、Enterprise/Edu 默认禁用）；按 app 配置 RBAC、Action control（含 Custom + 参数约束 Parameter Constraints：regex/range）、Manage domains、Enable sync（Deploy to your team / Self-service setup）；Workspace settings > Plugins 管理 plugin Available/Installed。
- 数据：app 可获得对话上下文与相关 memory；可见 IP、设备类型、语言区域、近似位置；Business/Enterprise/Edu 默认不用于训练。
- 来源：
  - https://help.openai.com/en/articles/11487775-connectors-in-chatgpt
  - https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt

---

## 13. Model picker（模型选择）

- Chat：composer 旁模型选择器；GPT 有 Recommended model；用户可切换可用模型。
- Work & Codex：workspace 管理员可在 Workspace settings > Models 设起始模型、推理级别、速度、Fast Mode、新 chat 行为；Chat 起始默认独立。
- GPT-6 Pro（Astra）：Pro $100/$200、Business、Enterprise（按 workspace 模型权限）；Plus 在 Work/Codex 内含 Astra。
- 旧模型退役后 GPT 自动切到相似模型。
- 来源：
  - https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
  - https://help.openai.com/en/articles/8554397-creating-and-editing-gpts

---

## 14. Settings 分区（field-level 枚举；APPROXIMATE — 桌面与 web 的分区命名随版本变动）

依据帮助文档中的明确路径 + 当前通用布局；未逐项截图核验的项标 UNKNOWN。

| 分区 | 已证实的字段/开关 | 来源锚点 |
|---|---|---|
| **General / App** | Windows: Companion window hotkey；语言、主题（APPROXIMATE） | 9982051 |
| **Notifications** | Push / Email / both；Manage tasks（进入 Scheduled）；桌面浏览器通知授权 | 10291617 |
| **Personalization** | Enable customization + Custom Instructions 文本框（1,500/5,000 字符）；Memory 开关；Memory Summary（Manage → Refresh/编辑/删除）；saved memories 切换链接 | 8096356, 8590148 |
| **Speech** | Voice 设置（模式选择、快捷键；桌面 Voice 权限引导）= 部分UNKNOWN | 8400625, 20001275 |
| **Data controls** | "Improve the model for everyone" 开关；Temporary chats；Archive/删除 chats；agent cookies 清除；导出（custom instructions 在导出内；tasks/共享链接不在） | 11752874, 8590148, 10291617 |
| **Security** | 登录与设备、双向验证 = UNKNOWN（未取官方字段清单） | — |
| **Connected apps / Apps** | App Preferences > Ask permission 档位；已连接 app 列表与断连 | 11487775 |
| **Apps & SDK（开发者）** | Developer mode（custom MCP apps）在 Settings 内开启（帮助文档指认存在；具体字段 UNKNOWN） | 12584461 |
| **Features / Beta** | 新功能开关（历史存在；当前具体项 UNKNOWN） | — |
| **About** | 版本、更新（桌面 Menu > Check for Updates） | 20001275 |

工作区级 Settings（admin）：chatgpt.com/admin/settings — Settings & permissions（Projects toggle、Shared projects toggle、RBAC、Work Cloud/Work Local/Codex Local、Plugins、Models 起始默认、event-triggered tasks 开关、SCIM、Compliance API）。
来源：10169521, 20001275, 10291617。

---

## 15. 状态与流（States & Streams；APPROXIMATE）

- Chat：流式输出；工具激活时显示 **Searching the web / Reading…** 一类状态行（APPROXIMATE）；回复下方显示工具/来源 chips（含 memory sources book 图标）。
- Deep Research：研究计划确认 → 进度实时滚动（"You can follow progress as it runs and interrupt at any time"）→ 全屏报告（TOC + sources + activity history）。
- Agent/Work：长任务呈现"计划 → 执行步骤 → 截图/浏览器窗口"流；需要授权时暂停（approval card）；Plan mode 先出 step-by-step plan 供批准；完成产出 deliverable 文件。
- Scheduled tasks：任务确认卡；到期后以通知（Push/Email）+ 新对话消息形式交付结果；监控类任务"检测到有意义更新"才通知。
- 澄清点：Work/agent 会主动 pause for clarification（agent 文档："pause for clarification or confirmation when needed"）。

---

## 16. OBSERVATION → PATTERN → CURIS GAP

### 16.1 Tasks / Scheduled automation

- OBSERVATION：Scheduled 是独立的任务对象（标题/instructions/schedule/时区/trigger/condition），支持一次性、周期（最小粒度付费为每小时）、监控、事件触发三类；有 plan 级数量限额与通知渠道（Push/Email）；任务可被分享为模板式链接；任务暂停条件明确（需审批、chat 删除、不活跃）。
- PATTERN：把"自动化"做成可枚举、可管理、可分享、有明确触发模型（时间/事件/变化）的一等对象，而不是聊天里的隐式约定；且把"等待人工审批"内建为任务状态。
- CURIS GAP：Curis 若只把任务作为对话附庸，将缺少 (a) 事件触发（Gmail/Slack/GitHub 类 webhook），(b) 监控型任务（变化才通知），(c) 任务级审批暂停语义，(d) 任务模板分享。CEO Assistant 派活的落地层需要等价的 Scheduled 对象与限额/通知模型。

### 16.2 Projects vs Curis Workspace

- OBSERVATION：Project = 指令 + 文件 + 链接源（Drive/Slack）+ chats + 项目级 memory（可隔离）+ 共享权限（edit/chat 两级、链接邀请、100 人/40 文件上限）+ 分支对话 + 保存回复为 source；admin 可在 workspace 层禁用与隔离。
- PATTERN：项目是"上下文容器"而非流程容器：没有阶段、没有看板、没有角色分工；多用户协作靠 branching 与共享 memory，不同步共编同一 chat。
- CURIS GAP：Curis Workspace 若具备阶段/职责/可交付物结构，则强于 Project；但 ChatGPT 的"save a response to project sources"（把产出物沉淀回上下文）与"project instructions override global"的上下文优先级规则值得对齐；Curis 需明确 Workspace 与 Knowledge 的写入路径（谁、何时、什么被沉淀）。

### 16.3 GPT marketplace vs Curis 人才与能力

- OBSERVATION：GPT = 名称/描述/指令/知识/能力/推荐模型/apps-or-actions 二选一/版本历史/权限化分享；2026 年起个人不能新建，GPT 已向 workspace 化与 Plugins 目录迁移。
- PATTERN：把"能力"定义为配置包（指令+知识+工具权限）并可版本化、可审计、可按角色发布；OpenAI 用权限与目录控制能力的组织化分发。
- CURIS GAP：Curis 的 AI Employee 若要对比 GPT，需要补齐：版本历史与回滚、知识文件上限管理（20 文件/512MB 是用户可理解的心智模型）、"能力二选一"式的明确边界（GPT 的 apps XOR actions 避免了权限叠加混乱）、以及组织内目录（谁可发布、谁可安装）。GPT 无记忆/无历史对话（每次全新）是刻意设计——Curis 需要决定 Employee 是否保留组织记忆。

### 16.4 Agent-mode / Work 的工作面 vs Curis Work/Result

- OBSERVATION：Work 的展示单元是"chat + deliverable"：计划先批（Plan mode）、执行可打断、结果落为文件（Library）或 Sites；agent 的展示单元是"虚拟计算机截图流 + approval"。执行证据（activity history、sources、screenshots）保留在对话内。
- PATTERN：把长任务的信任链拆为三层——计划批准、执行可见、产物可验收（文件打开、来源核对）；证据（sources/activity history）与结果一体交付。
- CURIS GAP：Curis Work/Result 应明确三层证据链：Approve（计划/审批动作）、Trace（执行回放）、Deliverable（结果物及其引用）。ChatGPT 缺少的是"组织级结果归档"——结果散在 chat 中，Library 只是文件库；Curis 的 Result 若绑定 Employee/Workspace 结构化归档，将是明确差异化。

### 16.5 其他可借鉴点

- 权限分级语言成熟：Important actions / low-risk / read-only + 审批卡（Deny/Allow once/Always allow）可直接映射 Curis 的 AI Employee 操作权限模型。
- Memory 的可解释性（memories in sources + 为什么被使用）是 Curis Knowledge/记忆设计的对标线。
- 项目共享的"edit/chat 两级 + 链接邀请 + 退出时复制自己的 chats"是轻量协作的完整闭环。

---

## 17. 未决项（UNKNOWN 汇总）

- GPT Store listing 的当前逐字段规范（分类、Builder Profile 字段）— 官方 Sharing and publishing GPTs 文章未抓取全文。
- Settings 各分区的最新完整字段（Speech/Security/Features/Beta）— 需桌面实测。
- Canvas 当前确切 UI 归属（独立入口是否仍在）。
- ChatGPT Work 与 Codex 用量计费的具体 credit 数字（见 rate card 12642688 / 11481834，未抓取）。
- 移动端 Settings 结构。

---

## Sources

- https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt （Projects in ChatGPT）
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex （ChatGPT Work and Codex）
- https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app （新桌面应用迁移）
- https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app （Windows app / Companion Window）
- https://help.openai.com/en/articles/10003026-windows-app-release-notes （Windows App Release Notes）
- https://help.openai.com/en/articles/10291617-tasks-in-chatgpt （Scheduled tasks）
- https://help.openai.com/en/articles/11752874-chatgpt-agent （ChatGPT agent）
- https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt （Deep research）
- https://help.openai.com/en/articles/8590148-memory-faq （Memory FAQ）
- https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt （Custom Instructions）
- https://help.openai.com/en/articles/8554407-gpts-in-chatgpt （GPTs in ChatGPT）
- https://help.openai.com/en/articles/8554397-creating-and-editing-gpts （Creating and editing GPTs）
- https://help.openai.com/en/articles/11487775-connectors-in-chatgpt （Apps in ChatGPT / plugins / MCP）
- https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt （Developer mode and MCP apps）
- https://help.openai.com/en/articles/20001278-creating-and-editing-documents-spreadsheets-and-presentations-with-chatgpt-work （Work 文档/表格/演示）
- https://help.openai.com/en/articles/8400625-voice-mode-faq （ChatGPT Voice）
- https://help.openai.com/en/articles/9295234-chatgpt-macos-app-file-uploads-and-photos （macOS 文件上传/拍照）
- https://chatgpt.com/work/ （ChatGPT Work 产品页）
- https://openai.com/index/introducing-chatgpt-agent/ （agent 发布公告）
- https://openai.com/index/introducing-deep-research/ （Deep research 公告）
- https://openai.com/index/introducing-canvas/ （Canvas 公告）
- https://x.com/OpenAI/status/1820914089612439622 （macOS Option+Space 公告）
- https://www.usecarly.com/blog/chatgpt-agent-mode/ （agent mode 被 Work 取代的第三方报道）
- https://community.openai.com/t/solved-cant-get-agent-mode-to-run-in-any-project/1373479 （社区：agent mode 退役）
- https://medium.com/@mubashirburfat4/i-used-chatgpts-canvas-feature-for-six-months-then-openai-quietly-killed-it-88c542f1a63f （Canvas 现状第三方报道）
