# Curis Research — Anthropic Claude 桌面产品家族 Function Inventory

- **Status**: Draft
- **Authority Class**: RESEARCH（仅为竞品研究证据，不构成 Curis 任何 Authority，不得用于改写 Product Blueprint / Master Map）
- **Date**: 2026-09-12
- **Scope**: Anthropic Claude 桌面产品家族 — Claude Desktop app（macOS / Windows / Linux beta）、Claude Cowork、Claude Code（Desktop / Web / CLI）、claude.ai Web、Claude in Chrome、Projects、Artifacts、Connectors/MCP、Skills、Memory、Settings、权限模型
- **Method**: 官方文档（support.claude.com、code.claude.com、claude.com blog、anthropic.com news）为主，第三方评测为辅。逐节标注来源 URL。无法从来源确认的字段标 `UNKNOWN`；凭截图/间接证据推断的字段标 `APPROXIMATE`。
- **Note**: 本文只做 OBSERVATION → PATTERN → CURIS GAP 记录，**不决定** Curis 架构。

---

## 1. Product Family Overview（产品家族概览）

### 1.1 产品清单

| 产品 | 形态 | 平台 | 备注 |
|---|---|---|---|
| Claude Desktop app | 桌面客户端 | macOS（Universal Intel + Apple Silicon）、Windows x64、Windows ARM64、Linux（beta，Ubuntu 22.04+/Debian 12，x64/arm64） | claude.ai/download；Linux 走 apt repo 或 .deb，不自更新 |
| Claude Cowork | Desktop 内的一个 Tab/模式（也是 Web/Mobile/Chrome 面板形态） | Desktop（macOS/Windows/Linux beta）、claude.ai Web、iOS/Android、Chrome side panel | "Claude Code for general computing"，云端 session + 本地资源桥接 |
| Claude Code | 三位一体：Desktop UI（Chat/Cowork/Code 三 Tab 之一）+ Web（claude.ai/code）+ CLI | 同上 + 终端 | Desktop 需 Git；Web 跑在 Anthropic 云 VM |
| claude.ai Web | 浏览器 | 全平台浏览器 | 基线产品，Chat/Projects/Artifacts |
| Claude in Chrome | Chrome 扩展（side panel） | Chrome only（不含其他 Chromium、不含移动端） | 经典版 + Cowork 版两种 side panel |
| Claude Design（Anthropic Labs） | Web（claude.com/product/design） | Web | 设计/原型/幻灯片，与 Code 衔接 handoff bundle，Pro/Max/Team/Enterprise research preview |
| Mobile App | iOS/Android | — | 可远程监控 Code 云端 session 与 Cowork |

Desktop 的核心信息架构（来自 code.claude.com/docs/en/desktop）：**Claude Desktop 内有三个 Tab —— Chat（对话）、Cowork（长任务 agentic 工作，含 Dispatch）、Code（软件开发）**。这是本次研究最重要的结构性事实：Anthropic 把"日常对话 / 自主干活 / 写代码"三种模式做成了同一个桌面壳内的三个入口。

### 1.2 计划与定价（官方口径）

| Plan | 价格 | 说明 |
|---|---|---|
| Free | $0 | 有限用量；Projects 上限 5 个；custom connector 上限 1 个 |
| Pro | $20/月 或 $200/年 | 5 小时滚动 session 窗口 + 用量上限 |
| Max 5x | $100/月 | 约每 session 5x Pro 容量 |
| Max 20x | $200/月 | 约每 session 20x Pro 容量 |
| Team | 约 $25–30/seat/月（Standard）、约 $100–125/seat/月（Premium，含 Claude Code）【APPROXIMATE，来自搜索摘要】 | 上限 150 成员 |
| Enterprise | 定制，年付；有 usage-based 计费模式【APPROXIMATE】 | admin 控制面、Compliance API、managed settings |

来源：[Choose a Claude plan](https://support.claude.com/en/articles/11049762-choose-a-claude-plan)、[What is the Max plan](https://support.claude.com/en/articles/11049741-what-is-the-max-plan)、claude.com/pricing。

### 1.3 关键计划门控（feature gating）

| 功能 | Free | Pro | Max | Team | Enterprise |
|---|---|---|---|---|---|
| Chat | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Code | ✅（Desktop Code Tab） | ✅ | ✅ | ✅ | ✅（seat 类） |
| Cowork | ❌ | ✅ | ✅ | ✅ | ✅（admin 可控） |
| Projects | ✅（≤5 个） | ✅（RAG knowledge） | ✅ | ✅ + 共享协作 | ✅ |
| Artifacts | ✅ | ✅（含 MCP/persistent storage） | ✅ | ✅（+ Claude Code artifacts） | ✅ |
| Skills | ✅ | ✅ | ✅ | ✅（共享/org 推送） | ✅ |
| Chat Search & Memory | 默认开 | 默认开 | 默认开 | 默认关（owner 开） | 同左 |
| Claude in Chrome | ❌ | ✅ | ✅ | ✅ | ✅ |
| Computer Use（Code） | ❌ | ✅ | ✅ | UNKNOWN | UNKNOWN |

来源：[Install Claude Desktop](https://support.claude.com/en/articles/10065433-install-claude-desktop)（功能表）、[memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)、[skills](https://support.claude.com/en/articles/12512180-using-skills-on-claude)。

---

## 2. App Shell（应用外壳 / 导航）

### 2.1 Desktop 顶层结构

- **三 Tab 模型**：Chat / Cowork / Code（Desktop v1.2581.0+ 起的 Code 重设计；官方文档明确"Three tabs in Claude Desktop"）。【来源：code.claude.com/docs/en/desktop】
- **Sidebar（通用）**：
  - Code Tab sidebar：session 列表；按 status / project / environment 过滤；按 project 分组；hover 显示 archive 图标；"+ New session" 按钮。
  - Cowork / Chat：有 "Scheduled"（定时任务）侧栏入口；Artifacts 有独立 sidebar 分区；"Customize" 菜单（管理 Skills / Connectors / Plugins）。
  - 用户头像/姓名首字母在左下角 → Settings 入口。
  - sidebar 不能完全禁用，只能折叠（右上角切换按钮）。【来源：appearance article】
- **Chat composer 附近**：模型选择器（发送按钮旁）；"+" 菜单（Connectors / Tools / 截图等）；model picker 旁有 usage ring（Code Tab）。
- **命令面板**：Desktop 无通用"command palette"命名功能；等价物为：
  - Quick Entry 全局浮层（见 §11）
  - Code Tab 的快捷键体系（Cmd+/ 列出全部快捷键；1–9 选择菜单项）
  - Skills/slash commands（`/` 触发）
  - 【APPROXIMATE】claude.ai Web 有 Search chats（含聊天搜索）；Desktop 覆盖情况 UNKNOWN。
- **键盘快捷键（Code Tab，Win 用 Ctrl 换 Cmd）**：Cmd+/ 快捷键列表；Cmd+N 新 session；Cmd+W 关闭；Ctrl+Tab / Ctrl+Shift+Tab 循环 session；Esc 停止；Cmd+Shift+D diff 面板；Cmd+Shift+B 浏览器；Cmd+Shift+S 选取页面元素；Ctrl+` 终端；Cmd+\ 关闭 pane；Cmd+; side chat；Ctrl+O 视图模式循环；Cmd+Shift+M 权限菜单；Cmd+Shift+I 模型菜单；Cmd+Shift+E effort 菜单。【来源：desktop docs】
- **Prompt 区（Code session 首条消息前）**：Environment、Project folder、Model、Permission mode 四个配置项——除 folder 外都可 session 中途改。

### 2.2 Cowork 入口

- Chat 与 Cowork 共用同一个 composer：在消息框切换 "Cowork" / "Chat"。
- Chrome side panel 打开即 Cowork session（Max/Team）。
- Dispatch：Cowork 会话可 spawn Code session（带 Dispatch badge），推送到手机。

### 2.3 桌面级入口

- Quick Entry 全局浮层（macOS）：双击 Option（默认）/ Option+Space / 自定义；Caps Lock 语音（默认关）。
- 通过 URL 协议打开 Claude Desktop（官方有专门文章）。
- macOS MDM domain `com.anthropic.claudefordesktop`；Windows 注册表 `SOFTWARE\Policies\Claude`。

来源：[desktop docs](https://code.claude.com/docs/en/desktop)、[Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)、[Quick Entry](https://support.claude.com/en/articles/12626668-use-quick-entry-with-claude-desktop-on-mac)。

---

## 3. Conversation & Composer（对话与输入区）

### 3.1 Composer 字段

| 字段/控件 | 细节 | 来源状态 |
|---|---|---|
| 文本输入 | 主输入框；Enter 发送 | 官方 |
| 模型选择器 | 发送按钮旁；点击模型名改模型；"More models" 展开更多；会话中途可改，下一回复生效 | 官方 |
| Effort 选择器 | 模型菜单内 "Effort" 子菜单：Low / Medium / High / Extra high (xhigh) / Max | 官方 |
| Thinking 开关 | 模型菜单内 "Thinking"/"Extended" toggle，与 effort 相互独立；Fable 5.1 永远开启不可关 | 官方 |
| 附件 | 图片（JPEG/PNG/GIF/WebP）、文档（PDF ≤1000 页；101–1000 页仅文本处理）、代码、文本；Chat 上传 500MB/文件（另有 30MB/文件、20 文件/会话的口径出现在"create and edit files"语境，两口径并存【APPROXIMATE】）；Projects knowledge 另有 RAG 容量 | 官方 |
| 截图/窗口分享 | Quick Entry overlay 支持拖拽截图、点击 app 窗口附带内容 | 官方 |
| 工具开关（"+" 菜单） | Connectors（逐会话开关，Chrome connector 默认每会话关闭需手动开）、Research、web search 等 | 官方 |
| Chat/Cowork 模式切换 | 消息框内直接切 "Cowork"/"Chat" | 官方 |
| 隐身对话 | 右上角 ghost 图标；不进历史、不进 memory、不被 chat search 检索 | 官方 |

来源：[model/effort/thinking](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)、[upload files](https://support.claude.com/en/articles/8241126-upload-files-to-claude)、[MCP connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)、[memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)。

### 3.2 消息行为

- **流式输出**：Desktop Code "streams responses as they generate"；Chat 同为流式【官方（Code blog）；Chat 细节 APPROXIMATE】。
- **消息操作**：编辑较早消息会生成对话新 branch（带独立 artifact 版本集）→ 天然支持 branching；retry 具体按钮形态官方文档未逐字描述【APPROXIMATE：主流 UI 有 retry/edit，官方证据只确认 edit→branch 行为】。
- **多轮**：完整多轮；接近 context 上限时自动摘要续接（"organizing its thoughts" 信号），完整历史仍可引用（Automatic context management，需 code execution 开启）。
- **Thinking 展示**：回复上方出现带计时器的 "Thinking" 指示器 + 可展开的思考摘要区。
- **错误修复**：artifact 报错旁 "Try fixing with Claude" 按钮 → 错误详情复制进新消息。
- **Markdown 原位编辑**：选中文字 → "Edit with Claude" → 输入修改请求，改动落在标记处；多文件草稿可批量排队编辑。

---

## 4. Projects（项目）

### 4.1 项目字段

| 字段 | 说明 |
|---|---|
| Name | 项目名 |
| Custom instructions（项目指令） | 项目内所有 chat 生效：语气、角色视角、工作流规则 |
| Knowledge（知识库） | 上传文档/文本/代码；作为背景 context；付费计划 RAG 自动扩容至约 10x |
| Chats | 项目内独立 chat 历史；chat search 在项目内只检索本项目 |
| Artifacts | 属于项目内会话产生；官方 Projects 文章未将 artifacts 列为独立项目字段【UNKNOWN：项目级 artifact 聚合视图细节】 |
| Memory | 每个项目有独立 memory 空间 + project summary（新 memory 体系） |
| 共享（Team/Enterprise） | 权限两级：Can view / Can edit；按邮箱单人/批量/全组织共享；"Shared with me" Tab；邮件通知 |

### 4.2 上下文机制

- Knowledge 接近 context 限制时无缝切 RAG 模式（付费），只加载相关内容，比塞满 context 更省 usage。
- 项目指令 + 知识 + （新）项目 memory 三层叠加构成项目 context。
- 大项目指令与未用文件会额外消耗 usage——官方把"精简项目内容"列为省用量建议。

来源：[What are projects](https://support.claude.com/en/articles/9517075-what-are-projects)、[RAG for projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)（引用）、[memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)。

---

## 5. Artifacts（产出物）

### 5.1 类型

- Markdown / 纯文本文档、代码片段、单页 HTML 网站、SVG 图片、Mermaid 图/流程图（官方 artifacts 文章列 "diagrams and flowcharts"；Mermaid 具名【APPROXIMATE】）、交互式 React 组件。
- 触发标准：内容 >15 行、可独立成立、需迭代/复用。
- Cowork 专业输出：带可用公式的 Excel、PowerPoint、格式化文档（经 code execution 生成真实文件）。
- Claude Code artifacts（Team/Enterprise）：session 输出发布为 live 页面（私有 URL，随 session 持续更新），如 PR walkthrough、数据 dashboard；仅限组织内共享，不能公开。

### 5.2 交互能力

| 能力 | 细节 |
|---|---|
| Preview | 专用窗口位于 chat 旁；右下角可查看源码、复制、下载 |
| 编辑 | 对话修改；Markdown 原位 "Edit with Claude"；版本选择器切换版本；用户编辑不改 Claude 对原版的记忆 |
| 多 artifact | 一场会话多个 artifact；右上 slider 图标切换；可指定 Claude 更新哪个 |
| 发布/分享 | "Publish" → 进 sidebar Artifacts 分区 → 可公开链接 + 嵌入网站 |
| Remix | 他人通过复制代码在其上构建 |
| AI-Powered Artifacts | 应用嵌入 Claude 智能，跑在 Anthropic 基础设施，使用者用自己的订阅额度，创建者零成本 |
| MCP 连接 | artifact 内可连 Asana/Google Calendar/Slack 等；首次交互弹授权；每人独立认证 |
| Persistent Storage | 有状态应用；20MB/artifact；文本 only；Personal（每人私有）/Shared（共用）两种模式；unpublish 永久删除存储 |
| 前置开关 | Settings > Capabilities > "Code execution and file creation"（个人）；Organization settings（组织） |

来源：[Artifacts](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them)。

---

## 6. Files & Connectors（文件与连接器）

### 6.1 文件上传

- 聊天上传：图片 JPEG/PNG/GIF/WebP；PDF ≤1000 页（101–1000 页仅文本）；上限 500MB/文件（官方"chat uploads"口径）；另有 30MB/文件、20 文件/会话口径【APPROXIMATE，出自文件创建场景】。
- Projects knowledge：文档/文本/代码，RAG 扩容。
- Desktop 本地文件：Cowork 可直接读写本地文件（无需上传下载）；Code 直接操作项目 folder；文件访问仅限用户连接的文件夹。
- 创建/编辑文件：Claude 生成 xlsx/docx/pptx 等（code execution + file creation 能力）。

### 6.2 目录连接器（官方目录）

- Connectors Directory：Google Drive、Gmail、Google Calendar、Slack、GitHub、Linear、Notion、Asana 等（部分在 Code 文档明确点名图形化配置）。Team/Enterprise 由 Owner 在 Organization settings > Connectors 添加，成员各自认证。
- Chrome connector：Settings > Connectors > Claude in Chrome > Configure > toggle on，然后装扩展；逐会话默认关闭。

### 6.3 Custom Connector（Remote MCP）配置字段

| 字段 | 必填 | 说明 |
|---|---|---|
| Server URL | ✅ | remote MCP server URL |
| OAuth Client ID | 可选 | Advanced settings 内 |
| OAuth Client Secret | 可选 | Advanced settings 内 |
| 名称/品牌 | — | 无用户命名字段；域名命中目录则显示服务品牌，否则 "Custom" 标签 |
| 编辑 | — | 不支持原位编辑，需删除重加 |

- 计划：全计划可用（Free 上限 1 个 custom connector）。
- 网络：连接从 Anthropic 云端发起（非本机），私有/防火墙服务器需 allowlist Anthropic IP 段。
- 逐会话开关：chat 内 "+" > "Connectors"。

### 6.4 本地 MCP（Desktop 专属）

- 配置文件 `claude_desktop_config.json`；走本机网络；claude.ai Web 与 Cowork 不可用；Code Desktop 会把该文件的 MCP servers 载入本地 Code session（与 `~/.claude.json`/`.mcp.json` 冲突时 desktop config 胜出）。
- CLI 可 `claude mcp add-from-claude-desktop` 导入。

### 6.5 Desktop Extensions（MCP 打包分发）

- 可安装的本地 MCP 扩展包（文件系统、日历、邮件、iMessage 等）；应用内有 curated/verified 目录。
- 安全：代码签名、API key 加密存储、企业 allowlist；Settings > Extensions 管理。

来源：[MCP connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)、[Install Desktop](https://support.claude.com/en/articles/10065433-install-claude-desktop)、[desktop docs](https://code.claude.com/docs/en/desktop)。

---

## 7. Skills & Agents（技能与智能体）

### 7.1 Skills

- 概念：`SKILL.md`（官方写作 skill.md）+ 资源文件打包为 ZIP 上传；文件夹名须与 skill 名一致；description 字段决定 Claude 何时自动调用。
- 位置：Customize > Skills；"+" > "+ Create skill" > Upload a skill (ZIP)；列表内 toggle 开/关；"..." 菜单删除。
- 运行面：Claude app chat（经 code execution）、Microsoft 365 add-ins（"/" 选择 skill）、Claude Code（beta，`~/.claude/skills/` 个人目录）、API code execution tool。
- 内置 skills：Excel、Word、PowerPoint、PDF 创建/处理（Anthropic 官方）。
- Directory（市场）：Browse and install skills / connectors / plugins（Cowork：Customize > "+" > Skills tab）。
- 共享：Team/Enterprise 可按人/组/全组织共享；只读、灰色显示直至启用、自动获得更新；Owner 可全组织推送；个人列表分 Personal / Shared with you / Organization 三区。
- 前置：Settings > Capabilities（个人）或 Organization settings > Skills（组织）开启 code execution 与 Skills。
- 安全：prompt injection / 数据外泄风险；企业 skill scanning（第三方 skill 扫描约 1–2 分钟）。

### 7.2 Cowork 能力（agentic 工作面）

- 任务流程：分析请求 → 建 plan → 拆 subtasks → 隔离环境跑代码/shell → 并行 sub-agent 协调 → 输出到 session 预览/下载。
- 本地桥接：本地文件 / 内置浏览器 / computer use 通过本机 Claude Desktop app 桥接；app 关闭或电脑睡眠则本地依赖型任务中断，云端部分继续。
- 云端 session：跑在 Anthropic 服务器隔离环境；多设备接力（桌面/网页/手机）；合盖继续跑；无会话超时。
- Projects（Cowork 版）：把任务归组为持久 workspace，带自己的 files、links、instructions、memory。
- Plugins：bundle skills + connectors + sub-agents，按角色/团队/公司定制。
- 定时任务：`/schedule` 或 sidebar "Scheduled"；云端跑，无需设备开机。
- Edit in place：Markdown 选中文本 "Edit with Claude"。
- Settings > Cowork：Global instructions（全局 standing instructions）；Folder instructions（连接本地文件夹时的项目上下文，Claude 可自行更新）；Preferred browser（Chrome vs 内置 Cowork 浏览器）。

### 7.3 Subagents（Code）

- Code Desktop 有 subagent pane；Cowork 拆分并行 workstream 可视化。
- Cross-session：Claude 可列出/读取/重命名/归档/发消息给其他 Code session（本地/SSH/WSL，最多最近 20 个）；incoming 消息为带归属的卡片，等当前任务完成才接收；out-of-scope 发现变成可点击 task chip 开新 session（自带 worktree）。
- Dispatch：Cowork 会话 spawn Code session；Pro/Max only。
- Agent SDK：Anthropic 提供 Agent SDK（官方文档存在于 docs；本文未逐字段核对其 UI 呈现）【UNKNOWN：Agent SDK 在桌面 UI 的暴露面】。
- Agent Teams：CLI only，Desktop 明确不支持。

来源：[Skills](https://support.claude.com/en/articles/12512180-using-skills-on-claude)、[Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)、[desktop docs](https://code.claude.com/docs/en/desktop)。

---

## 8. Memory（记忆）

- **新体系（topic-based）**：对话中按"主题"逐条保存（非事后摘要）；Claude 自动存或用户说 "remember this"。
- **层级**：账户级 memory + 每项目独立 memory 空间与 project summary。
- **共享**：chat 与云端 Cowork 共用 memory；本地 Cowork session 不用 memory。
- **会记住**：角色、项目、职业背景、人际关系、沟通/工作风格、技术偏好、项目细节。
- **敏感主题**（健康/种族/宗教/政治等）默认排除，可 opt-in "Include sensitive topics in memory"；保存时弹通知。
- **永不保存**：政府证件号、犯罪记录、金融账号、移民身份。
- **开关**：Settings > Memory > "Generate memory from chats"；Pause（保旧不增）；Reset（全删，不可逆）。Team/Enterprise 默认关，owner 开 org 级。
- **编辑/删除**：Settings > Memory > Topics 列表逐条查看/编辑/删除；或在对话中说"忘掉…"。
- **Chat Search（姊妹功能）**：Settings > Memory > "Search and reference chats"；RAG 检索过往会话，结果以 tool call 形式呈现 + 引用链接到原对话；隐身对话永不检索。
- **导入/导出**：legacy memory 可导出（Settings > Memory）；实验性跨工具迁移（从其他 AI 助手导入 memory / 导出）。
- **不可用**：HIPAA、公共部门、自定义数据保留协议、客户托管加密密钥的组织。

来源：[chat search & memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)。

---

## 9. Model Management（模型管理）

- **选择器**：composer 发送按钮旁；显示当前模型 + effort；"More models" 展开全列表。
- **模型线（2026-09 官方文档口径）**：Fable 5.1、Fable 5、Opus 5、Opus 4.8、Opus 4.7、Opus 4.6、Sonnet 5、Sonnet 4.6。（模型命名为 Anthropic 虚构示例线，按文档照录。）
- **Effort 等级**：Low / Medium（日常，省用量）/ High（默认推荐平衡）/ Extra high xhigh（Opus 4.7+，长 agentic 任务）/ Max（最深推理）。
- **Thinking**：独立 toggle；Fable 5.1 强制开启；API 上 Opus 5 在 xhigh/max 无法关闭 thinking。
- **中途切换**：任意回复边界生效，无需新会话。
- **Usage 展示**：
  - 共享用量池：claude.ai、Claude Code、Claude Desktop 三面共享同一池。
  - Code Tab：model picker 旁 **usage ring**——同时显示 per-session context 占用与共享 plan 用量。
  - Settings > Usage（Cowork 文档明确提及"monitor in Settings > Usage"）。
  - 5 小时滚动 session 窗口 + 每周上限（Pro/Max/Team）【官方口径分散，具体 UI 显示位置部分 UNKNOWN】。
- **消耗因子**：extended thinking、高 effort、工具/connector（web search、Research、MCP 被官方标注 token-intensive）、大项目指令与未用文件。
- **Credits**：付费计划可购买 usage credits（"Manage usage credits"）；Enterprise usage-based 按消耗计费。

来源：[model/effort/thinking](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)、[usage & length limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)、[desktop docs](https://code.claude.com/docs/en/desktop)。

---

## 10. Settings（设置全量清单）

Settings 入口：左下角姓名首字母 > Settings。已从官方文档确证的分区如下；未能证实存在的分区标 UNKNOWN。

| 分区 | 字段级内容 | 证据状态 |
|---|---|---|
| **Appearance** | Color mode：Light / Match System / Dark；Chat font：Default / Match System / Dyslexic Friendly；（sidebar 只能折叠不能禁用） | 官方 |
| **Memory** | "Generate memory from chats" toggle；"Search and reference chats" toggle；"Include sensitive topics in memory"；Topics 列表（查看/编辑/删除）；Pause / Reset；legacy 迁移导出 | 官方 |
| **Capabilities** | "Code execution and file creation" toggle（artifacts/skills 前置）；legacy memory 位置 | 官方 |
| **Instructions for Claude**（个人全局指令） | 账户级 custom instructions 文本区（Settings 内 "Instructions for Claude" 区块） | 官方 |
| **Connectors** | 目录连接器列表 + 连接/断开；Custom connector 添加（URL + Advanced: OAuth ID/Secret）；Claude in Chrome configure；per-connector 移除 | 官方 |
| **Extensions**（Desktop） | desktop extensions（MCP 扩展包）目录与管理 | 官方 |
| **Cowork** | Global instructions（Edit）；Preferred browser（Chrome / 内置浏览器）；（Auto 模式相关设置） | 官方 |
| **Claude Code**（Settings 内子区） | worktree 位置 + branch prefix 配置 | 官方（desktop docs: "Settings → Claude Code"） |
| **General（Desktop app 区）** | Quick access shortcut（双击 Option / Option+Space / 自定义 / 关）；Voice shortcut（Caps Lock / 自定义 / 关） | 官方 |
| **General（Computer Use 区，Code）** | Computer use 开关（默认关）；Denied apps 列表；"Unhide apps when Claude finishes" | 官方（desktop docs: "Settings → General"） |
| **Usage** | 用量监控（Cowork 文档点名 Settings > Usage） | 官方（一句话级细节） |
| **Account/Billing** | Manage usage credits、订阅管理【字段 UNKNOWN：官方文章存在但本文未逐字段核对】 | 部分 |
| **Privacy / Data controls** | 数据导出（含 memory 导出）、chat retention、隐身模式说明【字段 UNKNOWN：未逐项核对】 | 部分 |
| **Notifications** | OS 通知（session 完成、任务需批准）在文档中被引用；Settings 通知分区字段 UNKNOWN | UNKNOWN |
| **Language** | "How to use Claude in your preferred language" 为官方文章标题，证实有语言设置【字段 UNKNOWN】 | 部分 |
| **Voice** | 语音 dictation 设置在 Quick Entry（General）内；独立 Voice mode 分区 UNKNOWN | 部分 |
| **Shortcuts** | 专用设置分区 UNKNOWN；快捷键列表经 Cmd+/ 查看（Code Tab） | 部分 |
| **Developer mode** | UNKNOWN（未见官方分区名） | UNKNOWN |
| **Updates / About** | Linux 不自更新（apt 升级）；应用内更新 UI UNKNOWN | 部分 |
| **Organization settings**（Owner 专属） | Capabilities、Connectors、Skills、Members、"Claude in Chrome"、"Cowork in the cloud"、web search 禁用、公共项目开关、Compliance API、egress、managed settings（disableAutoMode、bypass 禁用、SSH allowlist、disableDesktopLocalSessions 等） | 官方 |

---

## 11. Desktop-specific（桌面专有）

### 11.1 Quick Entry（macOS）

- 全局浮层：双击 Option → 光标附近出现输入框；可打字即发、新建 chat（显示最近 5 个会话）、拖拽截图、点击 app 窗口附带、Caps Lock 实时语音转写。
- 权限需求：Screen Recording（截图/窗口）、Accessibility（核心）、Speech Recognition（dictation）。
- Settings > General > Desktop app 管理；macOS 12+，dictation 需 14+。

### 11.2 Code Desktop 多 pane 工作区

- Pane 类型：chat、diff、browser、terminal、file、plan、tasks、subagent、iOS Simulator（macOS）。
- 拖拽 header 重排、拖边 resize；Cmd+\ 关闭焦点 pane；Views 菜单开 pane。
- Split view：Cmd+点 sidebar session 开第二 pane。
- 三种 view mode（Ctrl+O 循环）：Normal（折叠 tool calls）/ Verbose（全部）/ Summary（仅最终回复+改动）。
- 内置终端（Ctrl+`）：session 工作目录、共享环境、多 tab。
- 文件编辑 pane：点击 chat/diff 中文件路径打开；spot edits + Save；磁盘变更警告（override/discard）。
- 浏览器 pane：自动起 dev server、自我验证（截图/DOM/点击/填表）；`.claude/launch.json` 配置（name、runtimeExecutable、runtimeArgs、port、cwd、env、autoPort、program、args、url、autoVerify）；外部浏览走干净 profile，逐站 Allow once/Always allow/Deny；永不购物/注册账号/绕 CAPTCHA。
- PR 监控：gh CLI；CI 状态条 + Auto-fix（迭代修失败 CI）+ Auto-merge（squash only）开关。
- Git 隔离：worktrees 在 `<project-root>/.claude/worktrees/`；`.worktreeinclude` 含 gitignored 文件；PR merge/close 自动归档 toggle。

### 11.3 Computer Use（Code 内，research preview）

- macOS + Windows；Pro/Max；默认关；macOS 需 Accessibility + Screen Recording。
- App 控制分层：View only（浏览器/交易平台）/ Click only（终端/IDE）/ Full control（其余）；审批按 session 或 30 分钟；终端/Finder/System Settings 等高影响 app 额外警告；Claude 工作时隐藏其他窗口。
- 工具优先级：connector → Bash → Chrome extension → iOS Simulator → computer use。

### 11.4 Desktop Extensions 与环境

- Extensions：签名 MCP 包 + 应用内目录 + 企业 allowlist。
- Environments：Local（部分 shell profile 继承、加密环境变量编辑器）/ Cloud（关 app 继续、多 repo、网络分级）/ SSH（Name、SSH Host、SSH Port(22)、Identity File 四字段对话框）/ WSL。
- Cowork 云 VM（Linux beta 桌面端本地跑）：KVM/QEMU、约 25GB 磁盘、8GB RAM（workspace 占 4GB）。

---

## 12. Permission Model（权限模型）

### 12.1 Cowork 三模式（模式选择器，随时可切）

| 模式 | 只读工具 | 写/删工具 | Claude 自主决定 |
|---|---|---|---|
| Manual（Ask before acting） | 放行 | 逐次请求批准 | 拒绝 |
| Auto（Automatically approve） | 放行 | Claude 决定（每步安全检查；不安全动作被拦并找替代/回头问；反复被拦退回逐步批准；耗 usage 更多） | Claude 决定 |
| Skip（Act without asking） | 放行 | 放行 | 拒绝（原注：无自主决定、也无安全检查） |

- Connector 权限三档：Always allow / Needs approval / Blocked（per connector）。
- 删除保护：永久删除文件必须经显式 "Allow" 批准。
- Team/Enterprise：admin 可移除 Auto 模式、强制写类 connector 工具逐任务批准。

### 12.2 Claude Code 权限模式

| 模式 | key | 行为 |
|---|---|---|
| Manual | `default` | 编辑/命令逐次问；diff 接受/拒绝 |
| Accept edits | `acceptEdits` | 自动接受文件编辑 + mkdir/touch/mv；其他命令仍问 |
| Plan | `plan` | 只探索+出 plan，不改源码（仅当前 session） |
| Auto | `auto` | 全放行 + 后台安全分类器；需特定模型；admin 可 disableAutoMode |
| Bypass permissions | `bypassPermissions` | = `--dangerously-skip-permissions`；仅沙箱容器/VM；Pro/Max 开关、org policy 控制 |

- 默认值经 `permissions.defaultMode`；选择按 folder 记忆（Plan 除外）。
- 云 session 只允许 Accept edits / Plan / Auto。

### 12.3 其他工具批准

- MCP tool approval：逐次审；"Allow always" 仅限可信工具；"Search and tools" 菜单可禁用单工具。
- Chrome 扩展：逐站 allow/deny（Team/Enterprise 由 admin allowlist/blocklist）；高危站点主动干预（webNavigation）。
- 1Password 集成：Claude 不见密码，用户生物识别逐次批准。
- Artifact MCP：首次交互授权弹窗，per-artifact 记忆。

---

## 13. States（状态处理）

| 状态 | 官方证据的处理方式 |
|---|---|
| Streaming | 响应流式生成（Code 明确 streaming；Chat 同【APPROXIMATE】） |
| Thinking | 带计时器的 "Thinking" 指示器 + 可展开思考摘要；可能被安全系统截断（提示改写 prompt） |
| Working/长任务 | Cowork：每步 progress indicator、展示 reasoning/approach、可见并行 sub-agents、中途 course-correct；Code：后台 session 完成发 OS 通知 |
| Tool use | Code：tool calls 默认折叠（Normal 模式），Verbose 全显；批准请求以提示卡呈现（批准/拒绝/always allow） |
| Context 满 | "organizing its thoughts" 信号 + 自动摘要续接 |
| Usage 到顶 | 等待重置 / 升级 / 买 credits；Cowork 提示"限制用得快"→建议拆给普通 chat |
| 错误（artifact） | "Try fixing with Claude" 按钮一键带错误上下文修复 |
| 会话中断（本地依赖） | "Setting up Claude's workspace"=正常更新提示；本地任务停止=app 关闭/睡眠；云端继续 |
| 权限拒绝 | Cowork Auto 模式：拦下不安全动作→找更安全替代或回头问 |
| 加载失败 | Code troubleshooting：403/签名、空白屏、session 加载失败等分场景诊断 |

---

## 14. Visual / Interaction Observations（官方截图级观察，APPROXIMATE）

以下仅来自官方文档文字描述与博客文字，未直接核验截图，全部标 APPROXIMATE：

- Desktop 整体为「左侧栏 + 主区」布局；三 Tab（Chat/Cowork/Code）在壳层顶部。
- Code Desktop 重设计后是**可自由拖拽的多 pane 网格工作区**（terminal / preview / diff / chat 任意组合），类似 IDE，而非纯聊天窗。
- Session 卡片式 sidebar 条目，带 status 指示（可过滤、按项目分组、hover 归档）。
- usage ring（圆环）贴在 model picker 旁，一眼看 context 与 plan 用量。
- Quick Entry 是光标附近的**轻量浮层**（非全窗），截图区提示 "Drag to take a screenshot"。
- Cowork 任务运行时展示并行 sub-agent 的可视化工作流。
- Artifacts 是 chat 旁的**并列专用窗口**，右下角操作区（源码/复制/下载），右上 slider 切换多 artifact。
- 字体/颜色 token 未在官方文档中描述【UNKNOWN】。

---

## 15. OBSERVATION → PATTERN → CURIS GAP（观察 → 模式 → Curis 候选缺口）

> 仅记录模式与候选缺口，**不决定** Curis 架构；供 CEO Assistant、Employee Conversation、Work/Result/Evidence、Knowledge、Meeting、Settings、Desktop shell 各面参考。

### P1. 三入口合一壳：Chat / Work(agentic) / Code
- OBSERVATION：Desktop = Chat + Cowork + Code 三 Tab；composer 内 Chat↔Cowork 一键切换；Cowork 可 spawn Code session（Dispatch）。
- PATTERN：日常对话与长任务不是两个产品，而是同一 composer 的模式切换 + 同一 sidebar 生态；轻→重的迁移成本接近零。
- CURIS GAP（候选）：Curis 的 CEO Assistant（对话）与 AI Employee 执行（Work）若分属割裂入口/视图，可考虑同壳模式切换与跨模式任务移交的对应物。

### P2. 计划先行 + 过程可视 + 中途纠偏
- OBSERVATION：Cowork 先建 plan、拆 subtasks、并行 sub-agent 可视化、随时 course-correct、多设备接力。
- PATTERN：长任务的信任感来自「计划可见 + 步骤进度 + 可打断改向」，而非黑盒等结果。
- CURIS GAP（候选）：Employee Conversation / Work 面是否暴露 plan、步骤级 progress、并行 stream、中途纠偏输入。

### P3. 权限分级是产品级一等公民
- OBSERVATION：Cowork 三模式（Manual/Auto/Skip）+ connector 三档（Always/Needs approval/Blocked）+ 删除显式批准 + Code 五模式 + 逐站/逐 app 允许清单 + Auto 模式带安全检查。
- PATTERN：权限不是一个弹窗，而是「模式选择器 + 粒度 allowlist + 高危动作特殊保护 + admin 覆盖」四层体系，且每层都能随时改。
- CURIS GAP（候选）：Curis Employee 执行动作（尤其写类、删除类）的权限模型粒度与可配置性。

### P4. 结果是"真文件 + 可预览"，不是聊天文本
- OBSERVATION：Cowork 输出带公式的 Excel、PPT、格式化文档；Artifacts 有 preview/版本/发布/嵌入；Code 有 diff viewer + review。
- PATTERN：Work/Result 面以产物为中心（可下载、可预览、可版本化、可发布分享），聊天只是驱动器。
- CURIS GAP（候选）：Curis Work/Result/Evidence 面是否以"可交付物 + 证据链"呈现，并支持版本与分享。

### P5. 上下文三层：全局指令 / 项目（指令+知识+memory）/ 会话
- OBSERVATION：Instructions for Claude（账户级）→ Project instructions + knowledge + 项目独立 memory → 单次会话；skill 按需叠加。
- PATTERN：上下文注入分层明确、每层可单独编辑，且项目层有 RAG 扩容与"只加载相关内容"的省用量策略。
- CURIS GAP（候选）：Curis Knowledge library 与 Workspace/Team 上下文的分层与检索策略。

### P6. Memory 是"可审阅的对象列表"
- OBSERVATION：memory 按 topic 逐条存，Settings > Memory 可逐条查看/编辑/删除；敏感主题 opt-in + 保存通知；Pause/Reset；chat search 可引用旧对话并给出处链接。
- PATTERN：记忆透明化（用户能看到 AI 记了什么并改它），甚至可跨工具导入导出。
- CURIS GAP（候选）：Curis CEO Assistant/Employee 的长期记忆是否可审阅、可编辑、有来源引用。

### P7. Usage 可见性贴近操作点
- OBSERVATION：usage ring 在 model picker 旁（session context + plan 用量双显）；Settings > Usage 汇总；官方持续教育"哪些操作耗 usage"（thinking/effort/tools/大知识库）。
- PATTERN：用量不是月底账单，而是实时环 + 操作级归因。
- CURIS GAP（候选）：Curis 桌面壳的用量/成本显示位置与粒度。

### P8. 隐身与敏感边界显式化
- OBSERVATION：incognito chat（ghost 图标）不进历史/记忆/检索；敏感主题 memory 需 opt-in 且每次保存弹通知；永不保存清单明示。
- PATTERN：隐私边界用显式 UI 状态（图标、通知、清单）表达，而非埋在条款里。
- CURIS GAP（候选）：Curis 处理公司敏感数据（会议、财务、人事）时的隐身/不入库会话形态。

### P9. 桌面壳的"随时唤起"层
- OBSERVATION：Quick Entry 全局浮层（输入/截图/窗口附带/语音）+ Chrome side panel + 手机接力；Desktop app 是本地资源（文件/浏览器/computer use）的桥接节点。
- PATTERN：桌面壳不只是"窗口里的产品"，还是系统级入口 + 本地资源代理；云跑任务、本地桥接、多设备一个账户态。
- CURIS GAP（候选）：Curis Desktop 是否有系统级唤起、本机上下文附带（截图/窗口/文件）与离机继续能力。

### P10. 组织管理面与个人设置分离
- OBSERVATION：Organization settings（Owner）管 Capabilities/Connectors/Skills/权限模式上界/compliance；个人 Settings 管 toggle/个性化；org 关闭某能力会直接改变个人可用集。
- PATTERN：企业产品化的能力开关是双层嵌套（org 上界内个人自选）。
- CURIS GAP（候选）：Curis 若面向公司（Company OS），CEO/管理员 vs 员工的设置分层。

### P11. Settings 分区清单本身是产品信息架构
- OBSERVATION：官方分区 = Appearance / Memory / Capabilities / Instructions / Connectors / Extensions / Cowork / Usage / General（快捷键+computer use）/ Account / Org settings。
- PATTERN：能力开关（Capabilities）与个性化（Appearance/Memory）与接入（Connectors/Extensions）三类分开，不做大一统"偏好"页。
- CURIS GAP（候选）：Curis Settings 信息架构是否区分「能力开关 / 个性化 / 接入 / 用量 / 组织管理」。

---

## 16. Sources

官方文档（support.claude.com / code.claude.com）：
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork （Cowork 总览）
- https://support.claude.com/en/articles/10065433-install-claude-desktop （Desktop 安装/平台/extensions）
- https://code.claude.com/docs/en/desktop （Claude Code Desktop：Tab/pane/权限/computer use/环境）
- https://code.claude.com/docs/en/claude-code-on-the-web （Claude Code Web：云 session/GitHub/sandbox）
- https://claude.com/blog/claude-code-desktop-redesign （Code Desktop 重设计博客）
- https://support.claude.com/en/articles/9517075-what-are-projects （Projects）
- https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them （Artifacts）
- https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp （Custom connectors / MCP）
- https://support.claude.com/en/articles/12512180-using-skills-on-claude （Skills）
- https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context （Memory & Chat Search）
- https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features （个性化：指令/项目指令/skills）
- https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings （模型/effort/thinking）
- https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work （用量与 context 限制）
- https://support.claude.com/en/articles/8887527-customizing-your-appearance-settings （Appearance）
- https://support.claude.com/en/articles/8241126-upload-files-to-claude （文件上传）
- https://support.claude.com/en/articles/12626668-use-quick-entry-with-claude-desktop-on-mac （Quick Entry）
- https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome （Claude in Chrome）
- https://support.claude.com/en/articles/11049762-choose-a-claude-plan （计划定价）
- https://support.claude.com/en/articles/11049741-what-is-the-max-plan （Max 计划）
- https://www.anthropic.com/news/claude-design-anthropic-labs （Claude Design）

第三方（辅助，标 APPROXIMATE 处使用）：
- https://arstechnica.com/ai/2026/01/anthropic-launches-cowork-a-claude-code-like-for-general-computing/ （Cowork 评测）
- https://www.wired.com/story/shut-those-laptops-anthropic-puts-its-claude-cowork-agent-on-your-phone/ （Cowork 手机接力）
- https://www.macrumors.com/2026/04/15/anthropic-rebuilds-claude-code-desktop-app/ （Code Desktop 重设计报道）
- https://www.superblocks.com/blog/claude-code-pricing （Team/Enterprise 定价口径，APPROXIMATE）
- https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn （Chrome 扩展商店页）

（完）
