# Curis 竞品研究：Devin（Cognition）功能清单

- Authority Class: RESEARCH
- Status: Draft
- 研究日期：2026-09-12（信息截至当日，均标注来源 URL）
- 研究对象：Devin（Cognition 出品的 "AI software engineer"），含 Cloud（web app）、Slack/Teams、CLI（Devin for Terminal）、Devin Desktop（Windsurf 桌面）、DeepWiki、API
- 研究方法：官方文档 docs.devin.ai（Mintlify，提供 .md 端点与 llms.txt 索引）、admin/billing 文档；视觉描述均为近似（APPROXIMATE）
- 用途：为 Curis（AI Company OS：AI Employees / Teams / Workspaces / Knowledge / Meetings / CEO Assistant）提供竞品功能边界参照。本文档只是 Research Evidence，不能覆盖 Curis 的 Current Authority。

---

## 1. 产品总览（Overview）

- 定位："an autonomous AI software engineer that can write, run and test code"；经验法则："if you can do it in three hours, Devin can most likely do it"。
- 强项（官方列举）：
  1. 并行处理大量任务（Linear/Jira tickets、从零实现 feature、bug 修复、app testing）；
  2. 迁移/重构/现代化（JS→TS、Angular 16→18、monorepo 拆分、删 feature flag、抽公共库）；
  3. 重复性工程任务（PR Review、Codebase Q&A、repro & fix bugs、写单测、维护文档）；
  4. 客户工程支持（集成陌生 API、定制 demo、原型、内部工具）。
- 形态：Web（app.devin.ai）、Slack / Microsoft Teams、Devin CLI（`curl -fsSL https://cli.devin.ai/install.sh | bash`，可 `/handoff` 给云端 Devin）、Devin Desktop（windsurf.com，配额与 sessions/CLI 共享）、API/SDK、Outposts（自托管基础设施）。
- 核心理念："Devin is most effective when it's part of your team and your existing workflow"——AI 作为团队成员进入现有工程流程。
- 来源：
  - https://docs.devin.ai/get-started/devin-intro.md
  - https://docs.devin.ai/llms.txt

---

## 2. Devin Session（会话）

### 2.1 会话结构

- 会话页两种模式：**Ask** 与 **Agent**。
  - **Ask Mode（Ask Devin）**：轻量模式——代码库问答（高级代码搜索、带引用答案）+ **任务规划**（scoping & planning，为 Agent 会话生成 context-rich prompts）；官方推荐：除非任务已完全明确，先 Ask 构造 plan 再转 Agent 执行。
  - **Agent Mode**：自主执行直至 PR。
- 会话内 Devin 会先出计划（plan）再执行；用户可中断、给反馈、改变方向（session tools 文档："If you see Devin going in the wrong direction, stop and redirect early"）。
- 来源：https://docs.devin.ai/get-started/first-run.md ；https://docs.devin.ai/work-with-devin/ask-devin.md

### 2.2 工作面板（Session Tools，field-level）

| 面板 | 能力 |
|---|---|
| **Shell** | 监看 Devin 执行的命令与输出；**Command history**：全量命令列表 + 输出预览 + 复制 + **时间导航**（点击命令跳转会话中的时间点；灰显命令=未来时间点）；与 progress updates 关联；接管后可在 VSCode 开终端直接执行（read-only ↔ writable 切换） |
| **IDE** | 内嵌 VSCode；实时看 Devin 改码；**Take over**（停掉会话接管 IDE）后可用 Cmd/Ctrl+K（自然语言生成终端命令）、Cmd/Ctrl+I（快速编辑/问答）、Tab 补全；接管后恢复会话需告知 Devin 所做修改 |
| **Desktop / Interactive Browser**（原 "Browser" tab 改名） | 直接查看并操作 Devin 的浏览器与桌面环境；用于 CAPTCHA、MFA、OAuth、复杂导航、测试本地应用、视觉验证；会话内 cookie 持久；可让 Devin "save the browser profile" 把浏览器状态打包进 blueprint 供未来会话复用 |
| **Progress Tab** | 统一视图：所有 shell 命令、代码编辑、浏览器活动按步骤汇总（点击会话中任意 progress step 查看） |
| **Side Chats** | 旁路提问不打断主任务：消息 hover 菜单 / add-tab 菜单 / `/btw 问题`；**只读**（能搜代码答问，不能改文件/跑命令）；可中途停止回答 |
| **Computer Use** | 完整桌面环境操作 GUI、测试应用、视觉验证变更（work-with-devin/computer-use） |
| **Voice mode** | 会话内语音通话：mute/unmute、按住 Space 说话、Silence Devin、End voice call；可随时打断 Devin；对话进 session history |

- 并行动作：Devin 可同时看浏览器 + 跑 shell 命令 + 读多个文件。
- 来源：https://docs.devin.ai/work-with-devin/devin-session-tools.md ；https://docs.devin.ai/work-with-devin/voice-mode.md ；https://docs.devin.ai/work-with-devin/computer-use.md

### 2.3 会话内其他行为

- **Testing & Video Recordings**：Devin 端到端测试自己的改动，并录制**视频**作为"proof of testing"交回用户。
- **Stacked PRs**：把大改动拆成有序、可审的 PR 栈。
- 浏览器认证：Interactive Browser 登录一次 → 保存 browser profile → 未来会话自动带认证态。
- 来源：https://docs.devin.ai/work-with-devin/testing-and-recordings.md ；https://docs.devin.ai/work-with-devin/stacked-prs.md ；https://docs.devin.ai/work-with-devin/browser-auth.md

---

## 3. Knowledge（组织知识 / 新员工式 onboarding）

> 与 Curis Knowledge / Employee onboarding 的直接对标。

- 定义（官方）："Knowledge is a collection of instructions and advice that Devin can reference in all sessions. Think of it as onboarding a new employee with the relevant organizational context."
- 创建入口：**Settings → Resources → Knowledge → Create knowledge**。
- 字段（field-level）：
  - **Trigger Description**（必填）：召回触发描述——当 Devin 当前工作与 trigger 相关时检索该条；越具体（哪个文件/repo/任务类型）召回越准。
  - **Content**：几句话的相关信息。
  - **Macro**：可选，`!` 开头的短标识（如 `!deploy-checklist`），在 prompt 中直接键入引用；仅字母/数字/连字符，组织内唯一。
  - **启用/禁用**：每条知识可 per user enable/disable（禁用不禁删，不参与本人会话检索）。
  - **Pin to repos**：三档——不 pin（按 trigger 智能召回）/ pin 到特定 repo（在该 repo 工作时总是使用）/ pin 到 all repos（任何会话任何 repo 都用）。
- **文件夹组织**：嵌套层级、整文件夹 bulk 启用/禁用、拖拽移动、**Auto-organize**（Devin 自动归类）。
- **Knowledge Suggestions**：Devin 根据会话内反馈自动建议新知识或对已有条目的更新；可编辑后保存或重新生成。
- 自动生成来源：
  - 连接 repo 后基于 README、文件结构与内容自动生成 repo knowledge；
  - 自动拉取代码库内特殊文件：`.rules`、`.mdc`、`.cursorrules`、`.windsurf`、`CLAUDE.md`、`AGENTS.md`（不自动拉普通 `.md`）。
- 可见性：会话中显示 **"Accessed Knowledge"**（本次用了哪些知识）。
- 范围分层（Enterprise）：**Organization Knowledge**（org 内共享）/ **Suggestions** / **Enterprise Knowledge**（跨 org 全企业）；组织级条目可在编辑器中 **Promote to Enterprise** 升级为企业级。
- 最佳实践（官方）：一条知识聚焦一个 workflow；拆小（可同时召回多条）；持续增补；trigger 写具体；统一用专门扩展名的文档文件集中维护。
- 来源：
  - https://docs.devin.ai/product-guides/knowledge.md
  - https://docs.devin.ai/onboard-devin/knowledge-onboarding.md

---

## 4. Playbooks（可复用提示词 / 职责脚本）

> 与 Curis "可复用职责/岗位 SOP" 的对标。

- 定义："easily shareable, reusable prompts for repeated tasks"——"like a custom system prompt for a repeated task"。官方建议：最佳实践/风格指南类内容放 Knowledge，重复任务的过程性 prompt 放 Playbook。
- 结构（官方推荐字段，field-level）：
  - 目标 outcome + **Procedure**（每步一行、祈使句、覆盖 setup→任务→delivery、MECE、含动作动词、可用 if/else/loop 思维组织顺序）；
  - **Specifications**：后置条件（做完后什么应为真）；
  - **Advice**：纠正 Devin 先验的提示；
  - **Forbidden Actions**：绝对禁止的动作；
  - **Required from User**：需要用户提供的输入。
- 创建方式：
  1. Web app：**app.devin.ai/settings/playbooks/create**；
  2. 保存 `<filename>.devin.md` 文件，开会话时拖入（成功附加显示蓝色 pill + 可内联编辑组件）；
  3. 从成功会话生成：把 session link 给 Devin，自动产出结构化 playbook（Advanced Capabilities）。
- 使用方式：会话开始时附加；**Macro 引用**（输入 `!macro_name` 即附加）；Slack 中 `![macro_name]`；可挂到 Schedule 上（每次运行都应用同一 playbook）；`.devin.md` 文件即 playbook 载体。
- 迭代：运行后可 live 迭代；Community Gallery（settings/playbooks）分享示例。
- 来源：
  - https://docs.devin.ai/product-guides/creating-playbooks.md
  - https://docs.devin.ai/product-guides/using-playbooks.md

---

## 5. Automations（事件驱动自动化）

> 与 Curis CEO Assistant 派活 / 事件驱动工作流的对标。

- 结构（三段式，field-level）：
  - **Trigger**：事件源（见下表）；
  - **Conditions**：可选过滤（label = bug、指定 repo 等）；
  - **Action**：四类——**Start session**（新会话，事件 payload 自动作上下文）/ **Message session**（向长跑会话发消息喂事件）/ **Triage Devin**（常驻 Devin 监控 Slack 频道，自动分诊并 spawn 子 Devin 调查）/ **Email notification**（每次/仅失败/仅成功时发邮件）。
- 触发源矩阵：
  - **Slack**：新消息、reaction 添加；
  - **GitHub**：issue、issue comment（可配 `starts_with "/devin"`）、PR、PR review、review comment、check run（CI，可 filter conclusion=failure 自动修构建）、push；
  - **GitLab**：MR、MR comment、issue、issue comment、push、pipeline（filter status=failed）；
  - **Linear**：issue created、label added、status changed、priority changed、assigned、moved to team；
  - **Jira**：issue created/updated、label、status、assigned、comment；
  - **Pylon**：工单事件；
  - **Schedule**：recurring（cron/iCalendar RRULE，可 "Every hour/day/week" 或自定义 RRULE 如 `FREQ=WEEKLY;BYDAY=MO;BYHOUR=9`）或 one-time（运行后自动停用）；
  - **Webhook**：唯一 HTTPS endpoint + secret（header/bearer/query 三种传法）+ 可选 payload regex 过滤；接 PagerDuty/Datadog/Sentry 等。
- 多 trigger：一个 automation 可挂多个 trigger（OR 关系）。
- 创建方式：Automations 页表单；**模板库**（Featured automations）；**自然语言**生成配置（"When a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"）；可用 Terraform provider 声明式管理。
- 安全注记：GitHub automations 默认只在 private repo 触发；public repo 触发有 prompt injection 风险，需 admin 显式开启（Settings → Connections → GitHub → Automation scope）。
- 来源：https://docs.devin.ai/product-guides/automations.md ；https://docs.devin.ai/product-guides/auto-triage.md

---

## 6. Scheduled Sessions（定时会话）

- 创建入口：输入框 ⋯ 菜单 → **Schedule Devin**；或 **Settings > Schedules → Create schedule**。
- 字段（field-level）：
  - **Name**；
  - **Schedule type**：Recurring（默认，cron 基）或 One-time（指定未来时间运行一次后自动禁用；schedule 与历史会话保留供审计）；
  - **Agent**：Devin（默认）/ Data Analyst / Advanced（playbook 与会话分析用）；
  - **Playbook**（可选）：每次运行应用同一 playbook；
  - **Repositories**（可选）：指定工作 repo（作为 prompt hint）；
  - **Frequency**：Visual 模式（Hourly / Daily / Weekly）或 Custom cron 表达式（如 `0 9 * * 1-5`）；
  - **Run at**（one-time）：本地时区输入，内部存 UTC；
  - **Email notifications**：Always / On failure only（默认）/ Never；
  - **Slack notifications**：可发到指定 Slack 频道；
  - **Run as**：会话归属（默认归创建者；可改为当前编辑者——schedule 所有权交接）；
  - **Prompt**：每次运行的指令。
- 管理页：Settings > Schedules 列表（name、frequency、last run、status）。
- 来源：https://docs.devin.ai/product-guides/scheduled-sessions.md

---

## 7. Slack 集成（Devin 作为团队成员）

- 安装：Settings > Connections > Slack → 安装 Devin Slack app → 每个用户 link 个人账号 → `@Devin` 触发。
- 用法：任意频道 `@Devin`（可带附件）；Devin 在 thread 内回复；webapp 与 Slack thread **双向同步**（composer 里的 Slack toggle）。
- 关键词/命令（field-level，全表照录要点）：
  - `!ask`：快速代码库问答（不启完整 agent）；`!deep`：深度研究答案；
  - 模式 bang 命令（可叠放、可位于消息任意处、代码块内则视为字面量）：`!fast` / `!ultra` / `!lite` / `!fusion` / `!swe`（SWE-1.7 模型）/ `!normal`；激活会话中发送即切换模式；
  - `mute` / `unmute`（停止/恢复看本 thread）、`(aside)` / `!aside`（Devin 忽略本条，用于人在 thread 里评论）、`sleep`（任意消息唤醒）、`archive`（休眠+归档）、`EXIT`（结束会话）；
  - `!new`（新 thread/专用频道）、`!channel #name`（改回复频道）、`unsync`；
  - **机器指派**：`!windows`（Windows VM，需组织 entitlement）、`!mac`（macOS VM）、`!outpost <name>`（自托管 Outpost，按名称/前缀/ID）；
  - `!dana` / `!data`：Data Analyst 会话（数据库查询/分析/可视化）+ `!discovery`（catalog 已连 MCP 的数据库与 schema）；
  - `![macro_name]`：附加 playbook。
- Slash commands：`/ask-devin`、`/dana`；消息右键 **Ask Devin about this** / **Create a new session**（modal 可选频道、附 playbook、改 prompt）。
- Code channels：可让会话在专属频道运行。
- 来源：https://docs.devin.ai/integrations/slack.md

---

## 8. DeepWiki 与 Ask Devin（代码库知识面）

- **DeepWiki**：为每个 repo 自动生成架构图、文档、源码链接（sidebar 入口 app.devin.ai/wiki）；公共版 **deepwiki.com** 免费索引公开 GitHub repo（React、TensorFlow 等，也可提交自己的 public repo）。
- Effort levels（per org 可配、per repo 可覆盖）：Low（默认，免费）/ Medium（约 5-10 ACUs/wiki）/ High（约 20-40 ACUs/wiki）；无订阅或无 credits 则拒绝生成；Enterprise 恒为 Low。
- **Steering**：repo 根目录 `.devin/wiki.json` 指定生成行为——`repo_notes`（content ≤10,000 chars + author）与 `pages`（title / purpose / parent 层级）两字段必填；配置后按指定页面精确生成。
- **Ask Devin**：结合 DeepWiki + 高级代码搜索的问答/规划（见 2.1）；Ask Devin 与 DeepWiki 也各有 MCP server（DeepWiki MCP、Devin MCP——外部工具可管理 sessions/playbooks/knowledge/repo docs）。
- 来源：https://docs.devin.ai/work-with-devin/deepwiki.md ；https://docs.devin.ai/work-with-devin/deepwiki-mcp.md ；https://docs.devin.ai/work-with-devin/devin-mcp.md

---

## 9. 多 agent 编排（Managed Devins / Dynamic Workflows / Fleet）

- **Managed Devins**（任一会话内可用）：主 Devin 作为 coordinator——把大任务拆包并行派给多个 managed Devin（各自独立 VM）；可 **Spin up child sessions**（指定 prompt、playbook、tags、**ACU limits**）、**Message child sessions**、**监控每个子会话 ACU 消耗**、**sleep/terminate 子会话**、**给自己 schedule 提醒**（定时检查长跑子会话）；启动前 Devin 会提出方案征求批准。
- **Devin Dynamic Workflows**：用确定性 Python 脚本编排多个 Devin 会话——fan-out、阶段间管道传结构化结果、可从断点恢复（"recorded, resumable script"）。
- **Devin Outposts**：自托管基础设施——self-hosted worker + fleet API（spawn 契约、devin-remote CLI）在自己的机器上跑会话；partner integrations（PKCE 授权）。
- 来源：
  - https://docs.devin.ai/work-with-devin/advanced-capabilities.md
  - https://docs.devin.ai/work-with-devin/dynamic-workflows.md
  - https://docs.devin.ai/cloud/outposts/overview.md

---

## 10. Code / PR Review（Devin Review）

- 覆盖：GitHub（含 GHES/GHEC）与 GitLab（含 Self-Managed）。
- 入口：app.devin.ai/review（open PRs 按类组织：assigned to you / authored by you / review requested）；PR 上评论 `/devin review`；URL 快捷（github.com → devinreview.com，public PR 免费、无需账号）；CLI `npx devin-review {pr-url}`；Devin 自建的 PR 在聊天中显示橙色 **Review** 按钮。
- 功能（field-level）：
  - **逻辑分组 diff**（相关编辑聚在一起而非字母序）+ **moved-code 检测**；
  - **Bug catcher**：按置信度标注 bug，severe bug 需立即处理；
  - **安全检测**：漏洞 + hardening 建议，带 **CWE 分类与严重级别**；
  - **评论/Approve/Request changes**（同步回 GitHub）；
  - **Codebase-aware chat**：对 PR 提问，答案带代码库上下文；可在任意 comment/bug/flag 上直接问；
  - **Merge/close/convert to draft/ready/auto-merge** 直接在 Review 页操作；
  - **Chat agent 改码**：让 agent 改，确认后作为 commit 应用到 PR 分支。
- 治理：角色编辑器中 **Devin Review permissions**（默认全员 auto-review，admin 另有 Manage Devin Review）；Enterprise Custom Roles 可降级为 manual-only / on-PR-creation-only / 移除；成本控制（trigger mode：every commit / PR 打开时 / manual only，per repo 或 per user，Settings > Review）。
- 配置：Settings → Review；Autofix settings 控制 Devin 回应哪些 bot 的 PR 评论。
- 配额耗尽时：Automations 停跑、Devin Review 退化为 smart diff viewer（无 AI 分析）。
- 来源：
  - https://docs.devin.ai/work-with-devin/devin-review.md
  - https://docs.devin.ai/product-guides/bot-comment-settings.md

---

## 11. Session Insights 与会话回放（Evidence）

- **Session Insights**（免费，所有已完成会话）：会话结束自动生成轻量分类（category / languages / tools）；L/XL 会话自动全量分析，小会话可手动 Generate Analysis（约 1 分钟）。
  - 四指标：**ACU Usage**、**User Messages**、**Session Size**（XS/S/M/L/XL 阈值表：XS ≤2 ACU 且 ≤2 msgs … XL >20 ACU 或 >20 msgs；L/XL 被标为 unhealthy，提示拆分任务）、**Category**（11 类：Feature Development / Bug Fixing / Code Review / Refactoring & Optimization / Test Generation / Migrations & Upgrades / CI/CD & DevOps / Security / Data & Automation / Documentation & Content / Research & Exploration）。
  - 分析三 tab：**Issue Timeline**（Issues Detected：label + impact 高中低 + 描述；时间线彩色事件图）、其余 tab（建议与统计）细节未全录。
- **回放**：session tools 提供 command history 时间导航（点击命令跳转会话时间点）；session link 可分享给 Devin 做事后分析（"This session used 42 ACUs … give me a revised prompt"）；session 页面即全程记录（progress steps、命令、diffs、浏览器活动）。
- **Session analysis 由 Devin 完成**：给 session link → Devin 检查历史、找出时间去哪了/死胡同/改写 prompt 建议；还能跨会话找模式。
- 来源：
  - https://docs.devin.ai/product-guides/session-insights.md
  - https://docs.devin.ai/work-with-devin/advanced-capabilities.md
  - https://docs.devin.ai/work-with-devin/devin-session-tools.md

---

## 12. Pricing / ACU（计费）

- 自助四档（官方表格）：
  | Plan | 对象 | 价格 | 成员 |
  |---|---|---|---|
  | Free | 尝试 | $0 | 1 |
  | Pro | 个人 | $20/月 | 1 |
  | Max | 高用量个人 | $200/月 | 1 |
  | Teams | 团队 | $80/月 起 | 最多 200 |
- Free：有限用量 + Devin Review + DeepWiki。
- Pro：日/周配额（覆盖 sessions + CLI + Devin Desktop）+ 超额 on-demand credits + Slack/Linear/MCP 集成。
- Max：仅周配额、无日上限。
- Teams：**full seat**（$40/月/席，含 Pro 级配额 + Desktop）与 **flex seat**（免费，纯走团队共享 credits，无 Desktop）；$80 月最低消费（不足部分自动折算为预付 on-demand credits）；credits 团队共享、无个人余额、不过期、可 auto-reload。
- **ACU（Agent Compute Unit）**：用量计量单位（1 ACU ≈ $2.50 历史；现按 credit 计价，"on-demand credits are the same dollar value as the ACUs"）；Session Insights 以 ACU 衡量效率；子会话可设 ACU limits；admin 可设 org 与 per-user ACU 上限（Enterprise）。
- 配额耗尽：Automations 停、Review 退化；补 credits 恢复。
- 管理：Settings > Plans（升级降级、增删席位、买 credits、发票）；Settings > Usage（auto-reload 阈值、默认 session spending limits）。
- 来源：
  - https://docs.devin.ai/admin/billing/self-serve.md
  - https://docs.devin.ai/admin/billing/enterprise.md
  - https://docs.devin.ai/admin/billing/usage.md

---

## 13. 环境与 Onboarding（环境配置面）

- **Index a Repository**：索引 repo 以启用 Ask Devin 与 DeepWiki。
- **Environment setup / Blueprints**：Blueprint 描述 Devin 的环境（repo、工具、依赖、环境变量、secrets、文件附件）；Devin 可从 repo 自动生成 blueprint，人工审阅/编辑后 build 出 snapshot；字段参考（sections、step types、GitHub Actions、env vars、secrets、file attachments）有专门 reference 文档。
- **Devin VPN**：为 Devin workspace 配置非 MFA VPN（blueprints、file attachments、Secrets、connection knowledge）。
- **Secrets & Site Cookies**：org / personal / repo / session 四级 secrets（API keys、site cookies、TOTP codes）。
- **Security Profiles**：可复用安全档——限制 network、MCP、git、GitHub CLI 访问，可绑定到 org / automations / sessions。
- **OIDC**：给 Devin 无密钥短期云访问。
- **Plugins / Customize 页**：安装 Devin plugins（marketplace）+ 自定义 MCP servers（STDIO/SSE/HTTP）；personal / organization / enterprise 三 scope；org 级 plugin 生态治理文档。
- 来源：
  - https://docs.devin.ai/onboard-devin/environment.md
  - https://docs.devin.ai/onboard-devin/environment/blueprint-reference.md
  - https://docs.devin.ai/product-guides/secrets.md
  - https://docs.devin.ai/product-guides/security-profiles.md
  - https://docs.devin.ai/product-guides/plugins.md

---

## 14. Settings 分区（field-level 枚举；APPROXIMATE——从文档中可证实路径归纳，完整分区清单 UNKNOWN）

| 分区（文档可证实路径） | 字段/能力 |
|---|---|
| **Settings > Plans** | 升级降级、full seats 增删、on-demand credits 购买、auto-reload、发票下载 |
| **Settings > Usage** | auto-reload 阈值、默认 session spending limits、org/per-user ACU 上限（Enterprise） |
| **Settings > Members** | 邀请成员（选 full/flex seat）、seat 类型转换；仅 Team/Enterprise |
| **Settings > Resources > Knowledge** | Create knowledge（Trigger Description / Content / Macro / Pin to repos / enable-disable）、文件夹、Suggestions、Organization/Enterprise 分 tab、Promote to Enterprise |
| **Settings > Playbooks**（app.devin.ai/settings/playbooks） | Create playbook、Macro、Community Gallery |
| **Settings > Schedules** | Create schedule、schedule 列表（name/frequency/last run/status）、编辑、审计留存 |
| **Settings > Connections** | Slack（个人账号 link）、GitHub（含 Automation scope：private-only ↔ All installed repos）、GitLab、Linear、Jira 等 |
| **Settings > Review** | trigger mode（every commit / PR opened / manual only）、per repo / per user |
| **Settings > Security**（Security Profiles、Secrets） | network/MCP/git 访问限制、四级 secrets、OIDC |
| **Customize 页** | Plugins（marketplace 安装、索引排障）、MCP servers（STDIO/SSE/HTTP）、scopes |
| **Automations 页**（侧栏） | Create automation、模板库、自然语言生成、Terraform |
| **Role editor** | Devin Review permissions 等角色权限（Enterprise Custom Roles） |
| **Settings > Support** | Slack Connect 反馈（Teams 用户） |

来源：上述各节引用的 docs 页面。

---

## 15. 状态与流（States；APPROXIMATE）

- 会话状态：**planning（Ask/plan 阶段）→ coding（执行）→ verifying（自测 + 视频录制）→ PR 交付（review）**；progress updates 按子任务滚动；用户可 stop/take over/resume。
- 会话结束：Session Insights 按钮 + 分类；可生成分析。
- Slack 会话状态控制：sleep / archive / EXIT / mute。
- ACU 实时计量显示（coordinator 监控子会话 ACU）。

---

## 16. OBSERVATION → PATTERN → CURIS GAP

### 16.1 "AI as teammate with defined role"

- OBSERVATION：Devin 的全部产品语言都是"雇佣"隐喻——Knowledge = "onboarding a new employee"、会话归人（Run as）、Slack 里像同事一样被 @ 与被 mute/sleep、有 seat/成员管理、任务来自 Jira/Linear 的 "assign to Devin"。
- PATTERN：把 agent 嵌入组织既有协作界面（Slack/Linear/Jira/GitHub），入口与同事一致；角色的差异化不在 UI，而在 Knowledge + Playbook + 环境（blueprint/secrets/security profile）的叠加。
- CURIS GAP：Devin 的"员工"只覆盖软件工程场景且没有组织架构（无团队/部门/汇报线/多角色协作）。Curis 的 AI Employee 若显式建模 Responsibility（岗位职责 = Knowledge + Playbook + 权限 + 入口地址的组合体）、并由 CEO Assistant 分派，则是对 Devin 模式在"公司"维度上的泛化；同时应吸收其 per-seat 配额、spending limits、Run as（归属/交接）等治理细节。

### 16.2 Knowledge onboarding

- OBSERVATION：知识条目 = Trigger（何时召回）+ Content（内容）+ Macro（快捷引用）+ Repo pinning（作用域）+ enable/disable（个人级开关）+ 文件夹（批量管理）+ AI 建议生成与更新 + Enterprise/Organization 双层 + "Accessed Knowledge" 透明显示。
- PATTERN：知识是"员工培训"的一等对象：有召回条件（不是全局注入）、有作用域、有生命周期（建议→审核→启用）、有使用可见性。
- CURIS GAP：Curis Knowledge 需要 (a) 触发/召回模型而非全量注入，(b) 作用域（org/workspace/employee），(c) 从会话反馈自动生成知识建议的回流机制，(d) 员工使用知识时的透明展示。Devin 没有"遗忘/过期"管理（只有手动删除）——Curis 可加入知识的时效与审计。

### 16.3 Playbook = reusable responsibility

- OBSERVATION：Playbook 有明确的结构学（Procedure/Specifications/Advice/Forbidden Actions/Required from User），可从成功会话自动沉淀，可挂 schedule、可经 macro 引用、可用 `.devin.md` 文件承载。
- PATTERN：把"某类活怎么干"固化成带后置条件与禁止项的可执行规格，且与自动化（schedule/automation）打通。
- CURIS GAP：Curis 的 Responsibility/SOP 若只停留在描述性文档，不如 Playbook 可执行；建议吸收其五段式结构与"从一次成功 Work 沉淀 Playbook"的闭环。区别于 Knowledge（知道什么）与 Playbook（怎么干）的切分必须保留。

### 16.4 Session replay / insights as evidence

- OBSERVATION：Devin 的会话天然是证据——命令历史可时间导航、progress steps、测试视频、Session Insights（ACU/消息数/规模分级/11 类任务分类/Issue Timeline）、Devin 可事后剖析任何 session 并给出改进 prompt。
- PATTERN：Work 的证据链 = 全程记录 + 结构化复盘（成本、健康度、问题清单）+ 可从复盘反哺（prompt/playbook/知识更新）。
- CURIS GAP：Curis Work/Result 应内建 (a) 全程可回溯（操作级），(b) 会话级复盘（消耗、健康度、问题），(c) 复盘→能力沉淀的出口。Devin 只在工程域做这件事；Curis 把它泛化到所有工作类型即是差异。

### 16.5 Automations / 组织级派活

- OBSERVATION：Automations = Trigger(8 类源) + Conditions + Action(4 类，含常驻 Triage Devin 与子 Devin spawn)；自然语言可生成配置；Terraform 声明式管理。
- PATTERN：事件驱动派活是"AI 员工接活"的完整模型：不只是 cron，还有事件（issue/CI/工单/IM）与常驻分诊岗。
- CURIS GAP：CEO Assistant 若只做手动派活会落后；至少需要 schedule + webhooks + IM 事件三类触发，以及"分诊 → 指派 → 汇报"的闭环。Devin 的 Triage Devin（常驻监控 + spawn 子 agent）几乎就是"AI 值班主管"原型，与 Curis CEO Assistant 的定位直接可比。

### 16.6 计费与治理

- OBSERVATION：per-seat 配额 + 团队共享 credits + spending limits + ACU 级会话计量 + Review/Automations 独立成本开关（trigger mode 控制烧钱速度）。
- PATTERN：AI 员工的成本必须可控、可归属、可预警；功能开关与成本是同一层治理。
- CURIS GAP：Curis 需要在 Employee/Work 层面定义计量单位与限额（会话级、员工级、组织级），并在派活前可预估成本。

---

## 17. 未决项（UNKNOWN 汇总）

- Devin web app 主界面侧栏完整分区（Suspended/Pending 等会话状态命名）— 未逐屏核验。
- ACU 与 credit 的精确换算与最新价格页（devin.ai/pricing 未抓取）。
- Devin Desktop（Windsurf 桌面）功能边界。
- Enterprise 管理控制台的完整字段（Custom Roles 全清单）。
- Plan 编辑在 Agent 会话中的确切 UI 形态（官方描述分散在 Ask/plan 与 session tools）。
- Slack "code channels" 的开启方式细节。

---

## Sources

- https://docs.devin.ai/llms.txt （Devin Docs 索引）
- https://docs.devin.ai/get-started/devin-intro.md （Introducing Devin）
- https://docs.devin.ai/get-started/first-run.md （Your First Session / Ask vs Agent）
- https://docs.devin.ai/work-with-devin/devin-session-tools.md （Session Tools：Shell/IDE/Desktop/Progress/Side Chats）
- https://docs.devin.ai/work-with-devin/voice-mode.md （Voice mode）
- https://docs.devin.ai/work-with-devin/computer-use.md （Computer Use）
- https://docs.devin.ai/work-with-devin/testing-and-recordings.md （Testing & Video Recordings）
- https://docs.devin.ai/work-with-devin/stacked-prs.md （Stacked PRs）
- https://docs.devin.ai/work-with-devin/browser-auth.md （Browser authentication）
- https://docs.devin.ai/product-guides/knowledge.md （Knowledge）
- https://docs.devin.ai/onboard-devin/knowledge-onboarding.md （Knowledge Onboarding）
- https://docs.devin.ai/product-guides/creating-playbooks.md （Creating Playbooks）
- https://docs.devin.ai/product-guides/using-playbooks.md （Using Playbooks）
- https://docs.devin.ai/product-guides/automations.md （Automations）
- https://docs.devin.ai/product-guides/auto-triage.md （Auto-triage，经 automations 页引用）
- https://docs.devin.ai/product-guides/scheduled-sessions.md （Scheduled Sessions）
- https://docs.devin.ai/integrations/slack.md （Slack 集成与关键词全表）
- https://docs.devin.ai/work-with-devin/deepwiki.md （DeepWiki）
- https://docs.devin.ai/work-with-devin/deepwiki-mcp.md （DeepWiki MCP）
- https://docs.devin.ai/work-with-devin/devin-mcp.md （Devin MCP）
- https://docs.devin.ai/work-with-devin/advanced-capabilities.md （Managed Devins / session analysis / playbook 沉淀）
- https://docs.devin.ai/work-with-devin/dynamic-workflows.md （Dynamic Workflows）
- https://docs.devin.ai/cloud/outposts/overview.md （Outposts）
- https://docs.devin.ai/work-with-devin/devin-review.md （Devin Review）
- https://docs.devin.ai/product-guides/session-insights.md （Session Insights）
- https://docs.devin.ai/admin/billing/self-serve.md （Self-serve plans / credits / seats）
- https://docs.devin.ai/admin/billing/enterprise.md （Enterprise billing / ACU limits）
- https://docs.devin.ai/onboard-devin/environment.md （Environment setup）
- https://docs.devin.ai/onboard-devin/environment/blueprint-reference.md （Blueprint reference）
- https://docs.devin.ai/product-guides/secrets.md （Secrets & Site Cookies）
- https://docs.devin.ai/product-guides/security-profiles.md （Security Profiles）
- https://docs.devin.ai/product-guides/plugins.md （Plugins & Customize）
- https://docs.devin.ai/product-guides/bot-comment-settings.md （Autofix settings）
