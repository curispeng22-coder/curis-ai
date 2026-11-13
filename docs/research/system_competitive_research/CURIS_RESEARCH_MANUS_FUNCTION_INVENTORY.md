# Curis 竞品研究：Manus 功能清单

- Authority Class: RESEARCH
- Status: Draft
- 研究日期：2026-09-12（信息截至当日，均标注来源 URL）
- 研究对象：Manus（manus.im / manus.ai，"the general AI agent"），含 Web、Desktop（macOS/Windows）、Mobile、Mail/Slack/Telegram/WhatsApp 触达面
- 研究方法：官方文档（manus.im/docs，Mintlify，提供 .md 端点）、官方 Help Center（help.manus.im）、官方博客与产品页；视觉描述均为近似（APPROXIMATE）
- 用途：为 Curis（AI Company OS：AI Employees / Teams / Workspaces / Knowledge / Meetings / CEO Assistant）提供竞品功能边界参照。本文档只是 Research Evidence，不能覆盖 Curis 的 Current Authority。

---

## 1. 产品总览（Overview）

- 定位（官方 Welcome 文档）："an autonomous general AI agent designed to complete tasks and deliver results"——"virtual colleague with its own computer"，在完整 sandbox 环境（带互联网的虚拟机 + 持久文件系统 + 可安装软件）中自主计划、执行、交付完整工作产物。
- 与 chatbot 的区别：不是逐步引导，而是接收目标后独立运行并交付成果。
- 交付形态：
  - **Web**（manus.im / manus.ai）
  - **Desktop app**（macOS / Windows；核心能力 **My Computer**——本地 CLI 控制）
  - **Mobile**（iOS/Android；可远程给桌面/云端派活）
  - **Mail Manus**（转发邮件触发任务）
  - **Slack**（@manus）、**Telegram**、**WhatsApp Business**、**Zapier**、**API**（open.manus.ai/docs）
- 双模式：**Chat mode**（轻量即时回答，读图/PDF/文本、联网搜索，不耗 credits）与 **Agent mode**（自主计划执行，消耗 credits）。Manus 1.6 起 Agent mode 有 Lite / 1.6 / 1.6 Max 三档（Free 只有 Lite；Pro 可用全部）。可来回切换。
- 来源：
  - https://manus.im/docs/introduction/welcome.md
  - https://help.manus.im/en/articles/11711128-what-are-the-differences-between-chat-mode-and-agent-mode
  - https://manus.im/docs/integrations/integrations.md

---

## 2. 任务会话（Task / Session 结构）

- Manus 的工作单元是 **Task（任务）**：一个任务 = 一次 agent 会话 + 一个虚拟机 sandbox + 一份产出物集合。
- 会话内结构（APPROXIMATE，依据官方截图与文档描述）：
  - 左侧：任务对话流（用户 prompt、Manus 的计划、进度说明、完成消息）。
  - 右侧/全屏面板：**Manus's Computer**（agent 工作面板）——虚拟机内的 Browser、Editor/VS Code、Terminal 视图，实时呈现 agent 正在做什么（"You see everything Manus is doing in real-time"）。
  - 任务清单：agent 在执行多步任务时在面板中维护 **to-do list**（APPROXIMATE：勾选式任务列表随执行逐项打勾，是 Manus 标志性的进度呈现）。
  - 产出物（deliverables）：文档、表格、slides、网页/web app、图表等，任务结束后保存于聊天历史与文件系统。
- 任务列表管理（侧栏）：All tasks / Non-project tasks / Favorites / Scheduled 四种过滤；任务可收藏（favorites）、可恢复删除任务（help 文章 "How can I recover a deleted task"）。
- 模式与模型选择：Chat ↔ Agent mode 切换；Agent mode 内选 Manus 1.6 Lite / 1.6 / 1.6 Max。
- 任务停止/取消：可中断；Mail Manus 任务可回复 "Cancel" 取消。
- 来源：
  - https://manus.im/docs/features/cloud-browser.md
  - https://help.manus.im/en/articles/11711128-what-are-the-differences-between-chat-mode-and-agent-mode
  - https://manus.im/docs/features/projects.md
  - https://help.manus.im/en/articles/11985278-how-can-i-recover-a-deleted-task （存在性）

---

## 3. Agent 工作面（Manus's Computer / 虚拟机 / Cloud Computer）

### 3.1 临时 Sandbox（默认）

- 每个任务运行在临时虚拟机：浏览器 + 终端 + 编辑器 + 文件系统；任务结束后环境关闭，产出物留存于聊天历史。
- **Cloud Browser**：云端浏览器"像真人一样"操作网页——访问、点击、填表、抽取数据、跨页多步工作流；**可登录用户个人/工作账号**执行认证操作（查邮件、更新 CRM、发社交帖）；遇到验证码/短信/MFA 时提示用户 **Take Over** 接管浏览器，完成后交还。
- 安全：会话加密；每用户隔离实例；不存储密码。
- **Take Over**：也可接管 VS Code（help 文章 "How can I take over Manus browser or VS Code"）。
- 来源：https://manus.im/docs/features/cloud-browser.md ；https://help.manus.im/en/articles/11711218-how-can-i-take-over-manus-browser-or-vs-code

### 3.2 Cloud Computer（持久虚拟机，2026 推出）

- 专用持久 VM：**persistent file system + always-on**，7×24 运行 bots、scheduled jobs、爬虫、数据库、Discord/Telegram bot 等；跨任务保留文件、已装工具、运行中的进程。
- 与临时 sandbox 的区别：sandbox 任务结束即关停（输出留存但环境不保留）。
- 与 Desktop "My Computer" 的区别（官方对照）：Cloud Computer 在云端持久（可 24/7 托管），My Computer 在用户本地机器上经授权执行。
- 分配方式：可自动——当任务需要持久性（"build and host a 24/7 Telegram bot"），Manus 自动判断并部署；也可手动设置（"How to Set Up and Access Your Cloud Computer"）。通过 CLI（无 GUI）操作。
- 有独立 plans/billing（"Understanding Cloud Computer Plans and Billing"）。
- 来源：https://help.manus.im/en/articles/15392111-what-is-the-cloud-computer ；https://manus.im/blog/manus-cloud-computer

### 3.3 Desktop app 与 My Computer（本地）

- 桌面 app（macOS/Windows），核心能力 **My Computer**：Manus 通过**命令行（CLI）**与本地机器交互——读写本地文件、启动/控制本地应用、使用本地硬件（如 GPU 训练模型）；任何 CLI 可及工具（Python、Node.js、Swift/Xcode 编译器等）都可用。
- 设置流程：My Computer tab → **Add Folder** 选择授权目录 → OS 授权。
- 安全模型（field-level）：
  - **Explicit Approval**：每条命令需明确批准——**Allow Once / Always Allow**。
  - **Folder-Scoped Access**：只见已授权文件夹，不能触及其他文件系统。
  - 电脑开着时可从手机远程派活（"remote-controlled assistant"）。
- 与 Projects/Scheduled Tasks 组合：本地文件夹可作 project 知识库；本地例行作业可自动化（如每日清理下载文件夹）。
- 来源：https://manus.im/docs/features/desktop.md ；https://help.manus.im/en/articles/14178443-what-is-the-my-computer-feature-capable-of

---

## 4. 进度与任务清单呈现（Progress & Task List）

- OBSERVATION（APPROXIMATE）：agent 执行长任务时的呈现三件套：
  1. **计划（plan）**：开始时列出步骤；
  2. **to-do list**：可勾选任务清单，随执行进度实时更新（Manus 最有辨识度的 UI 元素之一）；
  3. **实时工作面板**：browser/terminal/editor 画面流 + 阶段性文字说明。
- 完成后：产出物卡片 + 总结消息；任务可 **Replay**。
- Scheduled task 失败时：通知用户并记录错误（可查执行历史）。
- 来源：
  - https://manus.im/docs/features/cloud-browser.md
  - https://manus.im/docs/features/scheduled-tasks.md
  - https://www.technologyreview.com/2025/03/11/1113133/manus-ai-review/ （第三方对实时面板的描述）

---

## 5. Replay（回放）与分享

- **Replay**：每个完成的任务可生成回放——官方文档中的示例 share 链接带 `?replay=1` 参数（如 https://manus.im/share/IXdMjxObbFKbIjUUkBk4EH?replay=1 ），可逐步回看 agent 的完整操作过程（浏览器点击、终端命令等）。
- **Share**：任务可生成 public task link 分享给支持团队/家人/朋友；用于排障（contextual issues、bugs、quality reviews）或展示；隐私承诺：仅在排障时查看。
- **Collab**（区别于 share）：见第 10 节。
- 来源：
  - https://manus.im/docs/features/wide-research.md （replay 链接样例）
  - https://help.manus.im/en/articles/11711198-how-can-i-share-a-task

---

## 6. Scheduled Tasks（定时任务）

- 用途：一次性或周期任务自动化（每日报告、每周研究、每月分析、定期抓取、监控）。
- 设置方式（自然语言三要素）：**任务描述 → 时间表 → 输出方式**（email 给我 / 发 Slack 频道 / 存 Google Drive / 更新表格 / 经 connector 发送）。
- Schedule 选项（field-level）：Daily / Weekdays / Weekly / Monthly / Custom（如 "Every Tuesday and Thursday at 2 PM"）/ One-Time；时区用账户时区（Settings 中设定），可在表达式中指定（"9 AM EST"）。
- 管理入口：**Settings → Scheduled Tasks**：
  - 查看全部活跃 schedule；**Pause**（临时停用不删除）；**Edit**（改时间/任务描述/输出方式）；**Delete**；**执行历史**（过往运行、结果、错误）。
- 限额：按 plan 而定（具体数字未公开 = UNKNOWN；"Check Settings → Scheduled Tasks for your limit"）。
- 限制：不适合实时监控（定时运行而非持续）；任何 Manus 能做的任务（含 Wide Research）都可被 schedule。
- 最佳实践建议（官方）：时间具体、输出明确、给检索时间范围、先手动跑一遍再 schedule。
- 来源：https://manus.im/docs/features/scheduled-tasks.md

---

## 7. Knowledge（知识）与 Memory

- **Manus Knowledge**（2025-10 官方发布）：让 agent 从用户偏好中学习并"apply them where it matters"——用户以文本/文件/链接形式教授 Manus 偏好与背景，Manus 在后续任务中自动套用。
- **Knowledge base 限额**：按 plan 分级（Pro / Free 上限不同，具体条数官方未在抓取页面上写明 = UNKNOWN）；官方建议精简条目，过多会影响回答质量；条目可删除；达到上限时官方给"过滤条目"的建议（帮助文章 "What can I do when I reach the knowledge base limit"）。
- **Projects 层知识**：每个 Project 有自己的 **master instruction + knowledge base（文件/文档）**，自动注入该项目内所有新任务；更新规则：指令更新对当前任务的下一消息生效；文件更新只影响更新后新建的任务（旧任务保持创建时快照）。
- 任务记忆：任务内上下文连续；跨任务上下文依赖 Knowledge 与 Projects（ChatGPT 式的全局自动 memory summary 在官方文档中未确认 = UNKNOWN）。
- 来源：
  - https://www.linkedin.com/posts/manus-im_manus-knoweldge-activity-7381352201962708992-MLrR （Knowledge 发布）
  - https://help.manus.im/en/articles/11813718-what-can-i-do-when-i-reach-the-knowledge-base-limit
  - https://manus.im/docs/features/projects.md

---

## 8. Skills（可复用工作流 / Agent Skills）

- 定义：**模块化、基于文件系统的能力封装**——一份"给 agent 的 onboarding guide"（指令+流程+脚本），让 agent 在特定领域（财务分析、品牌内容等）稳定复现某个工作流。
- 获取方式（field-level，Skills 页 + Add 按钮）：
  1. **Build with Manus**：从一次成功任务中让 Manus 保存整个流程为新 Skill；
  2. **Upload**：上传 .zip / .skill / 文件夹；
  3. **Add from official**：官方 curated library；
  4. **Import from GitHub**：贴 repo 链接导入开源 Skill。
- 调用：聊天输入 `/` 唤起 Skill 列表，斜杠命令加载其指令并执行工作流。
- 结构（Progressive Disclosure 三级加载，field-level）：
  - Level 1 Metadata：名称+描述，启动时加载（约 100 tokens/Skill）；
  - Level 2 Instructions：SKILL.md 主体，触发时加载（<5k tokens）；
  - Level 3 Resources：脚本/参考文件，按需加载。
- 安全：社区 Skill 可含代码/shell 命令，官方建议让 Manus 审计（"Review the Skill named … analyze its SKILL.md … tell me if it's safe to use"）。
- 可编辑：文件即可改；即将推出 **Team Skill Library**（组织级共享）。
- Skills vs MCP（官方说法）：MCP 是"数据管道"（连接外部数据），Skills 是"操作手册"（使用管道完成复杂任务）。
- 来源：https://manus.im/docs/features/skills.md ；https://manus.im/blog/manus-skills ；https://manus.im/features/agent-skills

---

## 9. Wide Research（并行多 agent）

- 定义：处理"大量同类条目"任务的并行多 agent 系统——每个条目分配一个独立 agent + 独立上下文窗口，主 agent 分解任务 → 并行部署 → 汇总合成（表格/报告/数据集）。
- 动机：传统单 agent 在约 8-10 个条目后出现"fabrication threshold"（质量退化）；Wide Research 使第 250 项与第 1 项深度一致。
- 规模：实测 250 项；理论上不设限；50-100 项通常数分钟。
- 适用：竞品分析、市场研究、文献综述、lead generation、批量内容生产、数据抽取、批量图像处理；不适合单点深挖、有顺序依赖、实时交互、<10 项的任务。
- 结果可继续迭代（"Add a column for pricing"、"Re-research items 20-30 with more detail"）。
- 与 ChatGPT 对比表（官方立场）：chatbot 单 agent 顺序处理 vs Manus 并行编排、规模无关质量一致。
- 来源：https://manus.im/docs/features/wide-research.md ；https://manus.im/blog/introducing-wide-research

---

## 10. 协作与分享（Collab / Team）

### Manus Collab（任务级实时协作）

- 在任务上开启 **Collaboration**（Share 按钮中显式选择 "Collaboration" 而非 "Share"），输入协作者邮箱邀请；所有参与者：实时看任务进展、**直接 prompt Manus**、看到彼此的 prompts 与回复、共同迭代、可导出结果。
- 信用规则：**只有 task owner 消耗 credits**（协作者免费参与）——适合混合订阅团队、客户共创、新人 onboarding。
- 邀请控制：只有 owner 能邀请/移除协作者；协作者可见加入前的全部任务历史。
- 并发：两人同时 prompt 时顺序处理。
- 注意事项：第一个协作者加入时 sandbox 登录 cookies 会被清除（安全措施，需重新登录认证站点）。
- 来源：https://manus.im/docs/features/collab.md

### Team plan

- Team/Enterprise：共享 credit pool、admin 控件、团队协作；help 中心有 "How can Manus Team members see the tasks I created?"（成员间任务可见性规则 = 细节 UNKNOWN）。
- 来源：https://manus.im/docs/introduction/plans.md ；https://help.manus.im/en/articles/11711785-how-can-manus-team-members-see-the-tasks-i-created

---

## 11. 产出物（Artifacts & Deliverables）

- 类型：报告/文档、电子表格、**Manus Slides**（研究→内容→设计→视觉→speaker notes 的完整 deck）、网页/**web app**（Website Builder：构建、预览、发布、自定义域名、支付、鉴权、通知、分析、SEO、GitHub 同步、Figma 导入）、图像/视频/语音（Multimedia Processing，含 Veo 3 竖屏视频、Nano Banana Pro 图像）、数据可视化、会议纪要衍生物。
- 交付渠道：聊天内文件、email 附件、Slack 频道、Google Drive/Notion（经 connectors）、临时部署链接（会过期）、Google Play（app publishing）。
- 来源：
  - https://manus.im/docs/features/slides.md
  - https://manus.im/docs/website-builder/getting-started.md
  - https://manus.im/docs/features/multi-modal.md
  - https://manus.im/docs/features/data-visualization.md

---

## 12. Meetings（Meeting Minutes）

- 用途：**线下会议/访谈/独白**的现场录音 → 结构化会议纪要 → 直接在同一任务里执行 action items（生成 deck/网站/社交物料）。官方明确：不用于录制线上会议。
- 流程：工作区点 Meeting Recording icon → 实时转写 → Finish → 结构化摘要（key points、attendees、action items 分配）→ 用纪要作为上下文继续产出 → 邀请与会者进任务协作。
- 字段级细节：
  - **Intelligent Speaker Recognition**：识别不同说话人、识别被提到的名字，action item 分配更准。
  - **断网续录**：仅开始与生成纪要需要网络。
  - **不能暂停续录**：关屏会停止，但可从断点继续。
  - 计费：录音免费；分析与纪要生成消耗 credits（余额不足则暂停分析）。
  - 可用性：所有订阅层级。
- 来源：https://manus.im/docs/features/meeting-minutes.md

---

## 13. Connectors / Integrations / MCP

- 五类（field-level）：
  1. **MCP Connectors**（预置，OAuth 2.0）：Gmail、Notion、Stripe、HubSpot、Slack、Google Calendar、Hugging Face、Google Drive、GitHub、Meta Ads Manager、Zoom、LINE 等；读数据 + 受限写动作（更新 ticket 状态、加评论、创建条目）。
  2. **Custom MCP Servers**：自建内部系统/私有 API 集成。
  3. **Zapier**：8,000+ app 无代码自动化。
  4. **Slack**：@manus 在任意 thread 触发；Manus 读完整 thread 上下文；进度与结果在 thread 内公开呈现；支持 DM 与文件投递。
  5. **Manus API**（open.manus.ai/docs）与 **Data Sources**（内置付费三方数据 API，免自管 key）。
- 设置入口：Settings 中选择 connector → OAuth 授权 → prompt 中按名字引用。
- Browser Operator：浏览器扩展，把**用户本地浏览器**（带已登录会话）变为自治 agent——与云端 Cloud Browser 互补。
- 来源：
  - https://manus.im/docs/integrations/integrations.md
  - https://manus.im/docs/integrations/mcp-connectors.md
  - https://manus.im/docs/integrations/slack-integration.md
  - https://manus.im/docs/features/browser-operator.md

---

## 14. Mail Manus（邮件触发）

- 每用户唯一 bot 地址（如 `your-name-abc123@mail.manus.ai`；Settings → Mail Manus 获取）；转发/CC 邮件即触发任务，结果以邮件回送（含附件）。
- **Workflow Emails**：为重复场景创建专用地址（`travel@manus.bot`、`expenses@manus.bot`、`invoices@manus.bot`）+ **Default Prompt** 字段；配合邮箱 filter 自动转发 → 自动处理 → 回送结果。
- 安全：仅 **Approved Senders**（预批准发件人）可触发；复杂任务先发确认邮件可取消。
- 计费：与普通任务一样消耗 credits。
- 来源：https://manus.im/docs/features/mail-manus.md

---

## 15. Pricing / Credits

- 体系：credit-based；消耗取决于任务复杂度。
- 计划（官方文档三档 + 企业）：
  - **Free**：有限月度 credits；核心能力；Agent mode 仅 Manus 1.6 Lite。
  - **Pro**：较多月度 credits；全能力 + priority support；可用 1.6 / 1.6 Max / 1.6 Lite。
  - **Team**：团队共享 credit pool；admin 控件；priority support；联系 sales。
  - Enterprise：另谈。
- 用量面板：Current Balance、Usage History、Spending Insights、低余额 Alerts；任务开始前有用量预估。
- 加购：Add-on credits 不过期；月度 credits 每月重置不滚存。
- 节省建议：用 Chat mode 处理简单问题；合并同类任务；复杂任务先审阅中间产物。
- 具体 credit 数字与价格（如 Pro $/月、单任务 credit 区间）官方 docs 页未列 = UNKNOWN（价格页在 manus.im/pricing，未抓取成功）。
- 来源：https://manus.im/docs/introduction/plans.md ；https://help.manus.im/en/articles/11711128-what-are-the-differences-between-chat-mode-and-agent-mode

---

## 16. Settings 分区（field-level；APPROXIMATE）

官方 docs/help 中可见的 Settings 入口（未逐屏核验，完整清单 UNKNOWN）：

| 分区 | 已证实的字段/入口 |
|---|---|
| Scheduled Tasks | 活跃 schedule 列表、Pause/Edit/Delete、执行历史、数量限额显示 |
| Mail Manus | 个人 bot 地址、Workflow Emails（Name/Address/Default Prompt）、Approved Senders |
| Connectors/Integrations | MCP connector 列表与 OAuth 授权、Custom MCP、Zapier |
| 时区 | 账户时区设定（schedule 依赖） |
| Credits/Plan | 余额、用量历史、警报、升级、加购 |
| Knowledge | 知识条目管理（增删）、限额提示 |
| Skills | Skills 页（搜索、安装、上传、官方库、GitHub 导入） |
| Desktop | My Computer：Add Folder 授权、Allow Once/Always Allow 批准流 |
| Team/Admin | 成员管理、共享 credit pool（细节 UNKNOWN） |

来源：各功能文档（同前）。

---

## 17. 客户端与触达面补充

- Mobile：远程给桌面/云端派任务；接收通知与结果。
- Telegram / WhatsApp Business：agent 入驻聊天软件，credits 消耗有单独说明文章。
- Website Builder：Manus 的"建站/web app"子产品线（独立 docs 树），含部署、域名、支付（Stripe 等）、鉴权、通知、分析、SEO、Figma 导入、GitHub 双向同步、代码完全可下载。
- 来源：https://manus.im/docs/website-builder/getting-started.md ；https://help.manus.im/en/articles/14033949-how-are-credits-consumed-when-using-manus-agents-in-telegram

---

## 18. OBSERVATION → PATTERN → CURIS GAP

### 18.1 长时 agent 工作的呈现

- OBSERVATION：Manus 把 agent 执行拆成"计划 → 可勾选 to-do list → 实时虚拟机画面（browser/terminal/editor）→ 完成总结 + 产出物卡"。用户随时可 Take Over。
- PATTERN：进度不是日志流，而是结构化 checklist + 可视工作面；用户信任来自"看得见的操作"与"可干预"（take over / cancel）。
- CURIS GAP：Curis Work 的进度呈现若只有状态文案，将弱于 Manus；需要 Work 级 to-do list（结构化、可勾选、可追踪）+ 执行画面/操作流（或至少操作摘要）+ Take Over 语义。CEO Assistant 的"任务怎么做到一半"问题必须有答案。

### 18.2 Replay 与 Evidence

- OBSERVATION：任务天然带 replay（`?replay=1`）与 public share link；支持/客户共创都用同一链接。
- PATTERN：回放是一等产物——agent 工作的"录像"即证据，可分享、可审计、可教学。
- CURIS GAP：Curis 的 Work/Result 若能输出"过程回放 + 结果物"二合一 Evidence（而非仅结果文件），与 Manus 对齐且可借组织结构（Employee/Workspace 归属）超越其扁平 share。

### 18.3 定时任务与"7×24 员工"

- OBSERVATION：Scheduled Tasks 有清晰的设置三要素（任务/时间/输出）、管理页（pause/edit/history）、失败通知；Cloud Computer 让 agent 有了"常驻岗位"（24/7 托管 bot/爬虫）；Mail Manus 的 Workflow Email = "按职责分岗的收件箱 agent"（travel@、invoices@ 各有 Default Prompt）。
- PATTERN：把 agent 当作可长期雇佣的"数字员工"：有常驻环境（Cloud Computer）、有例行动作（schedule）、有专属触达地址（workflow email）。
- CURIS GAP：这与 Curis "AI Employee 有岗位与职责"的模型高度同构。Curis 需要在 Employee 层面定义：常驻 vs 按需、例行工作（schedule）、专属入口（邮件/IM 地址）、以及执行历史。Manus 目前没有组织结构（无部门/汇报线）——Curis 的 Teams/组织架构是明确差异点。

### 18.4 Skills vs 知识分层

- OBSERVATION：知识分三层落位——全局 Knowledge（偏好学习）、Project knowledge（master instruction + 文件）、Skills（流程性知识，三级 progressive disclosure）；Skill 可从成功任务一键沉淀（Build with Manus）。
- PATTERN：区分"知道什么"（knowledge）与"怎么做"（skill/workflow），且都文件化、可审计、可分享。
- CURIS GAP：Curis Knowledge 需要同样的分层（组织知识 vs workspace 知识 vs employee 的操作规程），并支持"从一次成功 Work 沉淀为可复用能力"（对标 Build with Manus / ChatGPT 模板）。Curis 的"人才与能力"可吸收 Skills 的三级加载与审计机制。

### 18.5 协作计费

- OBSERVATION：Collab 只收 owner 的 credits；协作者免费。
- PATTERN：把"AI 用量"记在发起者/雇主名下，参与者零成本——促进把 AI 当团队工具而非个人配额。
- CURIS GAP：Curis 的计费/配额模型若面向企业（公司买、员工用），与该模式一致；需注意协作任务的成本归属字段（owner 与 workspace）。

### 18.6 会议到执行

- OBSERVATION：Meeting Minutes 的卖点是"纪要 → 同一任务内直接执行 action items"，且有说话人识别与断网续录等细节。
- CURIS GAP：Curis Meetings 若只产出纪要而不打通到 Work/Employees 的任务分派，将落后于 Manus 的闭环；但 Manus 不做线上会议且无日历/组织上下文，Curis 的组织内会议（与 Workspace/Employee 联动）是差异化空间。

---

## 19. 未决项（UNKNOWN 汇总）

- Knowledge base 具体条数限额（Free/Pro 数字）。
- Scheduled tasks 具体数量限额、最小时间粒度（分钟级？）。
- Pricing 具体价格与 credit 定价表。
- Team plan 成员任务可见性细则。
- Manus 是否有全局 user memory（类似 ChatGPT memory summary）的显式管理 UI。
- 移动端功能差异、桌面 app 设置分区完整清单。
- 多 agent 编排（除 Wide Research 外，普通任务是否内部也用 sub-agents）官方未披露细节。

---

## Sources

- https://manus.im/docs/llms.txt （Manus Documentation index）
- https://manus.im/docs/introduction/welcome.md （Welcome）
- https://manus.im/docs/introduction/plans.md （Plans and Pricing）
- https://manus.im/docs/features/projects.md （Projects）
- https://manus.im/docs/features/skills.md （Manus Skills）
- https://manus.im/docs/features/wide-research.md （Wide Research）
- https://manus.im/docs/features/scheduled-tasks.md （Scheduled Tasks）
- https://manus.im/docs/features/collab.md （Manus Collab）
- https://manus.im/docs/features/desktop.md （Desktop / My Computer）
- https://manus.im/docs/features/meeting-minutes.md （Meeting minutes）
- https://manus.im/docs/features/slides.md （Manus Slides）
- https://manus.im/docs/features/mail-manus.md （Mail Manus）
- https://manus.im/docs/features/cloud-browser.md （Cloud browser）
- https://manus.im/docs/features/browser-operator.md （Browser Operator）
- https://manus.im/docs/integrations/integrations.md （Integrations overview）
- https://manus.im/docs/integrations/mcp-connectors.md （MCP Connectors）
- https://manus.im/docs/integrations/slack-integration.md （Slack Integration）
- https://manus.im/docs/website-builder/getting-started.md （Website Builder）
- https://help.manus.im/en/articles/11711128-what-are-the-differences-between-chat-mode-and-agent-mode （Chat vs Agent mode）
- https://help.manus.im/en/articles/11813718-what-can-i-do-when-i-reach-the-knowledge-base-limit （Knowledge base 限额）
- https://help.manus.im/en/articles/11711198-how-can-i-share-a-task （分享任务）
- https://help.manus.im/en/articles/14178443-what-is-the-my-computer-feature-capable-of （My Computer）
- https://help.manus.im/en/articles/15392111-what-is-the-cloud-computer （Cloud Computer）
- https://help.manus.im/en/articles/11711218-how-can-i-take-over-manus-browser-or-vs-code （Take over）
- https://manus.im/blog/manus-cloud-computer （Cloud Computer 博客）
- https://manus.im/blog/introducing-wide-research （Wide Research 博客）
- https://manus.im/blog/manus-skills （Agent Skills 开放标准）
- https://www.linkedin.com/posts/manus-im_manus-knoweldge-activity-7381352201962708992-MLrR （Manus Knowledge 发布）
- https://www.technologyreview.com/2025/03/11/1113133/manus-ai-review/ （MIT Technology Review 实测）
