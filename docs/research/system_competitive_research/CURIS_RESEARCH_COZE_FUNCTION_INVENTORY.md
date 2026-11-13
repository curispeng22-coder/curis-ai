# CURIS RESEARCH — Coze / 扣子 Function Inventory（Multi-Agent 深研）

- Authority Class: RESEARCH
- Status: Draft
- Date: 2026-09-12
- Subject: Coze（国际版 coze.com）/ 扣子（中国版 coze.cn），ByteDance 出品的 AI Agent / AI 团队协作平台
- Purpose: 为 Curis（桌面 AI Company OS：AI Employees / Teams / Leaders / Responsibility / Meetings / Work-Result Chain）提供竞争产品功能清单与组织模型对照证据。本文只记录事实与模式，不做 Curis 架构决策。
- Evidence note: 扣子官方文档站 docs.coze.cn 提供 markdown 源（`https://docs.coze.cn/<page>.md` 与 `llms.txt` 索引），本文大量引用该源。2026 年起扣子（中国版）已从"Bot 开发平台"转型为"面向 Agent 时代的新一代 AI 团队协作平台 / AI 办公空间（扣子空间）"，与 Curis 定位直接重叠，属于重点竞争产品。
- UNKNOWN 标记：官方文档未提供字段级证据的地方一律标 `UNKNOWN`，不做推测。

---

## 1. Product overview：Coze vs 扣子、平台、定价、版本

### 1.1 两条产品线
- **扣子（coze.cn，中国版）**：已重组为两大产品面。
  - **扣子编程（低代码开发平台）**：面向开发者的低代码智能体 / 应用 / 工作流搭建平台（原"扣子专业版"延续），含知识库、插件、工作流、多 Agent 编排、发布渠道。
  - **扣子空间（AI 办公空间）**："你的 AI 办公空间"。用户拥有一个默认的"扣子 Agent"，可创建多个 AI Agent（理解为"组建一支 AI 团队"），通过项目（Project）持续跟进任务，Agent 具备持久化长期记忆、日程、云盘、会议旁听等办公能力。官方标语："扣子用AI重塑生产力与工作效率"。
- **Coze（coze.com，国际版）**：面向海外开发者的 AI Bot / Agent 构建平台，核心能力与扣子编程同构（Agent 编排、Workflow、Knowledge、Plugin、Database、发布渠道、API/SDK），定价采用订阅 + 额度（credits）。国际版具体功能差异证据：`UNKNOWN`（官方 docs 站为 JS 渲染，本次未能抓取正文）。

### 1.2 定价 / 积分
- 扣子空间按"积分"计费："使用扣子时，会产生一定的费用，通过积分方式抵扣。你每日[可获得一定额度]……"（docs.coze.cn/cozespace_coze_billing_overview.md）。每日免费积分上限、各套餐价格、按模型/技能的积分消耗表：`UNKNOWN`（本次未抓取全表）。
- 扣子编程存在订阅套餐体系（文档含"订阅套餐"、"存储空间"、"订阅管理"、"企业工作空间购买席位"等页）：套餐档位价格字段级证据 `UNKNOWN`。
- 付费功能示例（有明确证据）："付费功能、批量管理技能"页面说明可批量启用/停用技能为付费功能；加入企业后 "空间页会展示开发空间与编程空间…开通 Pro、Premium 套餐的企业…开通企业版后"——即存在 **Pro / Premium / 企业版** 多档位（docs.coze.cn/guides_edition.md 摘要）。
- 免费版多 Agent 限制（来自官方文档）："免费版每个多 Agent 智能体最多添加 10 个 Agent 节点；如需添加更多，需升级到付费套餐"。

### 1.3 平台 / 客户端
- Web（coze.cn / coze.com）；扣子空间有桌面端与移动端同步（"提供多种使用方式，支持多端同步"——docs.coze.cn/what_is_coze.md，桌面端具体形态 `UNKNOWN`）。
- 发布触达端：微信、飞书、抖音小程序、微信小程序、掘金、多维表格、Web/Chat SDK、API、扣子商店等（详见第 10 节）。

### 1.4 定位证据（对 Curis 重要）
- 文档首页定位句："扣子是面向 Agent 时代的新一代 AI 团队协作平台，支持多人多 Agent 协作、多项目独立管理。能承载项目、沉淀资产，可用于办公、编程、视频创作等。提供多种使用方式，支持多端同步，让人和 Agent 共同协作推进任务。"（docs.coze.cn/llms.txt / what_is_coze.md）

Sources: docs.coze.cn/llms.txt；docs.coze.cn/what_is_coze.md；docs.coze.cn/cozespace_coze_billing_overview.md；docs.coze.cn/guides_edition.md；docs.coze.cn/guides_multiagent.md

---

## 2. Agent 创建流程与身份字段

### 2.1 扣子空间（AI 办公）侧的 Agent 创建
- 默认 Agent：打开扣子后自动拥有一个默认"扣子 Agent"，直接对话即可处理日常任务（写文案、分析等）。
- 创建新 Agent：入口在左下角"新建 Agent / 新建项目"或个人中心"创建 Agent"；需填写 Agent 名称与使用场景描述；可上传头像或从系统库选择；选择访问权限（个人 / 团队共享范围）。创建后进入对话页直接下达任务。
- Agent 身份字段（扣子空间）：名称、头像、使用场景/职责描述、访问权限、发布状态。开场白、语音、标签等字段：`UNKNOWN`（扣子空间文档未见对应字段证据）。
- Agent 管理页（cozespace_agent_management.md）："你可以在 Agent 设置页面管理 Agent 的身份信息、发布状态…（其余配置项本次未抓取正文，字段清单 UNKNOWN）"。
- 模板创建：官方提供模板库，选择模板后自动创建项目与 Agent（cozespace_coze_agent.md 摘要："选择合适的模板自动创建项目"）。

### 2.2 扣子编程（低代码开发）侧的 Agent 创建
- 创建路径：登录 → 选择工作空间 → 新建项目 / 新建低代码智能体 → 进入编排页（guides_agent_workflow.md 摘要）。
- 默认单 Agent 模式；编排页可切换到多 Agent 模式（见第 8 节）。
- 单 Agent 编排配置项（多 Agent 模式 FAQ 中反向枚举，属官方确认的全局配置字段）：**人设与回复逻辑（Persona & Prompt）、触发器、变量、数据库、开场白、快捷指令、背景图片、语音**。另有模型设置、插件、工作流、知识库、长期记忆、文件盒、对话体验设置（证据见第 3–7、11 节文档索引）。
- 身份展示类字段（名称/头像/描述）在低代码侧同样存在，字段级表单证据：`UNKNOWN`（未抓取创建表单正文）。

Sources: docs.coze.cn/cozespace_agent_overview.md；docs.coze.cn/cozespace_agent_management.md；docs.coze.cn/cozespace_coze_agent.md；docs.coze.cn/cozespace_create_projects.md；docs.coze.cn/guides_multiagent.md；docs.coze.cn/guides_agent_workflow.md

---

## 3. 每智能体模型配置

### 3.1 模型选择与参数（扣子编程，guides_llm.md）
- "扣子编程已接入多款大模型，支持对各种大模型进行精细化的参数设置，例如生成多样性、输入及输出设置等。"具体模型列表与各参数取值范围：`UNKNOWN`（正文未抓全）。
- 文档索引中模型参数字段（章节标题级证据）：生成多样性（对应 temperature/top_p 类参数）、回复上限（max tokens）、上下文轮数（携带对话历史轮数）、带曝光的历史轮数、输出格式、工具调用、温度/回复随机性等。字段级取值与默认值：`UNKNOWN`。
- 模型试运行：支持"试运行/调试模型"能力（模型设置页含试运行入口，章节标题级证据）。

### 3.2 多 Agent 节点内的模型设置
- 多 Agent 模式下每个 Agent 节点有独立 **"模型设置"** 字段——"pick the LLM and its configuration"（guides_multiagent.md），即不同子 Agent 可用不同模型与参数。
- 多模型并存（同一节点挂多个模型自动切换）：`UNKNOWN`。

### 3.3 扣子空间侧
- 扣子空间用户不直接配模型参数，由平台按任务自动路由（文档未暴露 per-Agent 模型选择 UI；`UNKNOWN` 是否在 Agent 设置中提供）。

Sources: docs.coze.cn/guides_llm.md；docs.coze.cn/guides_multiagent.md；docs.coze.cn/llms.txt

---

## 4. Knowledge（知识库）

### 4.1 扣子编程（guides_knowledge.md）
- "扣子编程支持使用扣子编程官方知识库和火山知识库，两者均支持上传和存储外部知识内容，并[在智能体中以检索方式使用]。"即双知识底座：**扣子知识库 + 火山引擎知识库**。
- 知识库类型（文档索引标题级证据）：文本知识库、表格知识库、图片知识库；支持"自定义"（自定义类型/分块方式）；支持"上传表格"、"数据表"、"Rocket";分块与切片设置（"分块"、"切割文本"、"分段标识"、"按行读取"、"文本预处理（OCR/PDF）"等章节标题）；检索设置（"召回设置"、"召回测试"、"最大召回数量"、"最小匹配度"、"向量检索/混合检索"类配置）。
- 知识库分类/标签管理、共享（"共享知识库"章节）：存在。
- 知识库在对话中的回调（"知识库回调"）：存在。
- 字段级数值（chunk 长度默认值、召回数量上限等）：`UNKNOWN`。

### 4.2 扣子空间侧
- Agent 可使用知识库（cozespace_skill_overview 系列提及知识库作为技能之一）；管理界面字段：`UNKNOWN`。
- 火山知识库："配置火山知识库后，用户的所有对话内容将保存到火山知识库中，火山知识库会对对话内容进行切片、索引和存储，并返回匹配的片段…"（guides_knowledge.md 摘要）。

Sources: docs.coze.cn/guides_knowledge.md；docs.coze.cn/llms.txt

---

## 5. Skill / Plugin（插件与技能）

### 5.1 插件市场与插件字段（扣子编程）
- 官方插件商店（商店/插件市场）+ 自建插件。插件结构字段（文档索引标题级证据）：插件 → 工具（tool）→ 输入参数 / 输出参数（元数据、类型、必填、描述）、插件描述（供 LLM 选择）、OAuth 授权、出参示例、请求头配置。
- 自定义插件：基于 **OpenAPI(Swagger) schema** 导入创建（"通过 URL 或本地文件导入 OpenAPI 规范"）；支持鉴权配置；插件创建后可调试、发布。
- 插件在 Agent 中的挂载：单 Agent 的技能区 + 多 Agent 每个节点"技能"字段（插件/工作流/知识库三类可挂）。
- 触发器（Trigger）：作为智能体的一种能力存在（"触发器"是单 Agent 全局配置之一）；发布渠道差异表中触发器仅飞书渠道支持（见第 10 节）。

### 5.2 扣子空间"技能商店"
- 技能是 Agent 能力来源："为 Agent 配置技能"，技能分为：**知识库（如飞书知识库）、内容技能（小红书、知乎、抖音、B站、掘金、36氪等自媒体来源）、云盘（个人云盘、GitHub、本地文件、Google Drive、Notion、飞书文档等）、工作流（简历初筛、竞品分析、每日热点监控、电商选品、社媒运营等模板）、子 Agent**。加入方式包括"推荐、朋友在用、浏览全部技能商店"（cozespace_skill_overview.md 摘要）。
- "付费功能、批量管理技能"页：可批量启用/停用技能，属付费功能。
- 组织内技能共享："技能的共享功能允许企业将自定义的技能共享给整个企业内的所有成员使用"（guides_organization_share_capabilities.md 摘要）。
- 内置技能示例：搜索（网页搜索、Link Reader 等）、图片理解、代码执行/代码编辑器、文生图/图像生成、图像处理、速读、网页读取、数据分析师、视频生成/数字人、内容撰写（营销文案/公文/各行业文案）、Office（文档/PDF/表格/PPT）、翻译、撰写推文、对话历史管理（清空上下文）等（llms.txt 技能索引）。
- MCP：低代码侧有 MCP 章节；扣子空间侧 "MCP" 页面存在（cozespace_mcp.md），字段级 `UNKNOWN`。

Sources: docs.coze.cn/llms.txt；docs.coze.cn/cozespace_skill_overview.md；docs.coze.cn/guides_plugin.md（索引）；docs.coze.cn/guides_organization_share_capabilities.md

---

## 6. Workflow（工作流）

### 6.1 工作流定位
- 低代码方式组装插件/模型/代码的编排工具："通过可视化方式组合插件、大语言模型、代码块等节点"（guides_workflow.md 摘要）；工作流可被智能体以"技能"方式挂载。
- 官方节点清单（llms.txt 工作流节点索引，逐条列举）：
  - 开始（Start）、结束（End）、Answer（答复/输出）、LLM、意图识别（Intent）、知识库检索、知识库写入、文本处理、文本转语音、语音转文本、文件处理、条件器、循环器、批处理、代码执行、变量、数据库（增/查/更新/删除单条/多条）、消息（发送消息）、问答、输入、会话历史、插件、子工作流、HTTP 请求、MCP、图像生成、图像理解、图像处理、视频生成、视频合成、视频拼接、文生视频、视频生成试运行、画布（布局）、虚拟节点、批处理嵌套、任务状态、终止、标签、长连接、飞书多维表格/飞书文档/飞书电子表格、钉钉、企业微信、微信公众号/企微智能机器人、Cameo（数字人视频生成）、小说/口播/跟拍/片头/口播数字人类视频生成、AI 生成卡片、混合检索（Rephrase/知识库检索/知识库检索 Dify 语义重排）、文本抽取、格式转换、文件转换、变量节点、多分支、知识检索蒸馏等（以 docs.coze.cn/llms.txt 实际条目为准，条目极多，此处为主要聚类）。
- 对话流（Chatflow）：与 Workflow 并行的面向对话的编排形态（guides_chatflow_mode.md；对话流节点含问答/输入/消息等，发布渠道差异表中有"对话流搭建的应用"提法）。

### 6.2 多 Agent 编排与 Workflow 的关系（官方原文）
- "工作流是低代码构建插件的一种方式；多 Agent 模式则是把不同人设分配给不同 Agent、并在满足跳转条件时移交对话。多 Agent 模式更适合处理复杂的任务。"（guides_multiagent.md）——即 Coze 把"多 Agent 编排"与"Workflow"区分为两种机制。
- 多 Agent 节点：在扣子空间/低代码应用侧存在"多 Agent 节点"类组件（llms.txt 应用节点索引含 multi_agent 相关条目），字段级证据：`UNKNOWN`。

Sources: docs.coze.cn/llms.txt；docs.coze.cn/guides_workflow.md；docs.coze.cn/guides_multiagent.md；docs.coze.cn/guides_chatflow_mode.md

---

## 7. Memory（记忆）

### 7.1 扣子编程侧
- **变量（Variable）**：用户级/会话级键值，系统变量 + 自定义变量（guides_variable.md）；在工作流中可读写（变量节点）。
- **数据库（Database）**：智能体可创建单张/多张内存表用于持久化结构化记忆；工作流数据库节点支持单条/多条 CRUD（guides_database.md）。
- **长期记忆（Long-term Memory）**：智能体自动从对话中提取记忆变量/记忆片段并在后续对话引用；开关式配置 + 记忆内容查看/编辑（guides_long_memory.md 摘要级证据，字段 `UNKNOWN`）。
- **文件盒（File Box）**：对话中上传的文件持久存放，供智能体跨轮引用（文档索引存在"文件盒"条目；字段 `UNKNOWN`）。

### 7.2 扣子空间侧（重点证据）
- "扣子是真正具备持久化长期记忆的 Agent"（cozespace_memory.md）。
- 记忆功能组件（cozespace_memory.md / cozespace_memory_edit.md）：
  - Agent 在对话中沉淀记忆；用户可在**记忆列表页**查看所有 Agent 的记忆，并**手动新增、编辑、删除记忆**；
  - 可设置记忆的生效范围（记忆归属某 Agent 或全局；编辑记忆条目）；
  - 记忆用于个性化：Agent 记住用户偏好（如称呼、写作风格、常用联系人）。
- 云盘（cozespace_cloud_drive.md）：上传本地文件到云端，供任务和对话引用，构成文件型记忆；具体容量/字段 `UNKNOWN`。

Sources: docs.coze.cn/cozespace_memory.md；docs.coze.cn/cozespace_memory_edit.md；docs.coze.cn/guides_variable.md；docs.coze.cn/guides_database.md；docs.coze.cn/guides_long_memory.md；docs.coze.cn/llms.txt

---

## 8. Multi-Agent（深研重点）

### 8.1 组织模式总览
三种并存的"多 Agent"形态（跨扣子编程与扣子空间）：
1. **多 Agent 模式（Multi-agent mode）**：低代码智能体编排画布上布置多个 Agent 节点，由"开始节点 + 适用场景描述"做 LLM 任务分发。
2. **智能体节点（嵌套已发布 Bot）**：多 Agent 画布中嵌入已发布的单 Agent。
3. **扣子空间 AI 团队 + 子 Agent 技能**：一个项目内主 Agent 与成员 Agent 协作（组织级多 Agent，非画布式）；Agent 可把子 Agent 当作技能配置使用。

### 8.2 多 Agent 模式（guides_multiagent.md，官方原文逐字段）
- **动机**：单 Agent 处理复杂任务需冗长 prompt 与大量插件/工作流，任何细节改动都可能影响整体；多 Agent 模式把复杂任务拆为子任务，每个 Agent 独立配置提示词、插件、工作流，调试只改出错的那个 Agent。
- **切换**：创建智能体默认单 Agent 模式；编排页点击"单 Agent 模式"→ 选择"多 Agents 模式"。
- **任务分发机制（LLM routing，非图编排）**：由**开始节点**结合各节点的 **"适用场景"** 描述，由 LLM 判断用户消息应交给哪个 Agent 节点。两种分发策略（配置在开始节点）：
  - **"上一次回复用户的节点"**：新消息回到上一轮回复的节点（适合多轮任务，如积分游戏）；清空历史后回到开始节点；
  - **"开始节点"**：所有消息经开始节点重新分发（适合独立功能集合，如售后群）。
- **节点类型与字段**：
  - **开始节点**：设置分发策略；
  - **Agent 节点**：重命名（"重命名"，清晰的名称帮助 LLM 分配任务）、创建副本、"模型设置"（独立 LLM 配置）、"适用场景"（告诉上游节点何时切换到本节点）、"Agent 提示词"（运行逻辑与解题步骤）、"技能"（+ 按钮：插件 / 工作流 / 知识库）、"用户问题建议"（默认开启，生成 3 个追问建议；可选"用户自定义 Prompt"复选框；可关闭）；
  - **智能体节点**：创建副本、"智能体详情"（查看/编辑源 Bot）、"适用场景"、"用户问题建议"（默认"跟随原始智能体状态"）。
- **全局跳转条件**：作用于所有 Agent 的优先路由条件；"全局跳转条件的优先级高于节点适用场景"；"一个智能体中最多可以添加 5 个条件节点"（免费版上限 10 个 Agent 节点，付费可加）。
- **画布 UI（4 面板）**：面板 1（顶）Agent 信息 + 发布历史；面板 2（左）全局提示词 / 变量等配置（可折叠）；面板 3（中）画布，"添加节点"，默认开始节点连着一个以 Bot 名命名的默认 Agent；面板 4（右）"预览与调试"。
- **Handoff（移交）语义**：对话控制权按"满足跳转条件时移交"在节点间转移；被移交节点直接对用户输出。官方文档未描述显式的"结果聚合节点"（多 Agent 结果聚合：`UNKNOWN`——当前机制下由当前接管节点直接答复）。
- **任务拆分**：靠"适用场景"描述引导 LLM 拆分选择；无显式 planner/分解节点（`UNKNOWN` 是否有新增 planner 节点）。
- **模式切换的数据语义（FAQ）**：
  - 单 → 多：保留全局配置（人设与回复逻辑、触发器、变量、数据库、开场白、快捷指令、背景图片、语音）；快捷指令默认"自动分配节点"；已有插件/工作流/知识库移入第一个默认 Agent；
  - 多 → 单：保留同类全局配置，但快捷指令与各 Agent 节点挂的插件/工作流/知识库会**丢失**；
  - 发布限制：包含智能体节点的多 Agent 智能体"无法选择公开配置"（发布到商店时）。
- **对话内多 Agent 协同**（对话中把消息"指定给某节点"）：调试时可在"预览与调试"通过节点右上角对话图标**直接与指定节点会话**；点击 Agent 运行图标可单节点试运行。

### 8.3 扣子空间侧多 Agent（组织级协作，官方摘要）
- "你可以把它理解为**组建一支 AI 团队**"（cozespace_agent_overview.md）——多 Agent 按团队方式组织而非画布。
- 项目（Project）作为协作载体："当一件事不是一次对话就能完成，而是需要持续跟进、或需要多个 Agent 协作时，可以创建一个项目"（cozespace_collaboration.md）。项目成员可包括多个 Agent 与多个人；项目内共享会话、云盘文件、任务、长期记忆。
- 主 Agent 与成员 Agent 的指派/交接过程细节（是否有 Leader 概念、任务单、回执）：`UNKNOWN`（未抓取正文，官方摘要未见显式 Leader/Handoff 字段）。
- 多 Agent 会话模式（一次输入多 Agent 同时/顺序应答）：`UNKNOWN`。

### 8.4 多 Agent 调试与可观测
- 编排期：右侧"预览与调试"面板实时对话试运行；**单节点直连会话**（对话图标）、单节点试运行（运行图标）；发布历史面板。
- 运行期（扣子编程 guides_data.md）："借助分析看板，你能够全面跟踪和分析已发布的低代码智能体、应用和工作流的运行状况，包括 Token…（消耗、调用次数、用户数等指标；字段清单 UNKNOWN）"；另有"日志查询"（日志页可查看智能体/工作流调用明细与错误）、"运行历史"。
- Trace 级（每个节点输入输出逐跳展示）：低代码工作流试运行可见逐节点 I/O；多 Agent 会话中查看"运行详情"（guides_preview_debug.md）。

Sources: docs.coze.cn/guides_multiagent.md（正文）；docs.coze.cn/cozespace_agent_overview.md；docs.coze.cn/cozespace_collaboration.md；docs.coze.cn/guides_preview_debug.md；docs.coze.cn/guides_data.md；docs.coze.cn/llms.txt

---

## 9. Team / Space（工作空间、团队、角色权限）

### 9.1 空间体系
- 个人空间 + 团队/企业空间；企业购买席位（"企业工作空间购买席位"）；付费套餐开通后进入企业（guides_edition.md）。
- 开发空间与编程空间并列展示："加入企业后，空间页会展示开发空间与编程空间…开通 Pro、Premium 套餐的企业…"（guides_team_config.md 摘要）。
- 扣子空间（AI 办公空间）：以"项目"为单位隔离资产（会话/文件/任务/记忆），个人与团队项目并存。

### 9.2 角色与权限
- 企业角色（guides_team_config.md）："超级管理员可以修改企业的设置，包括修改名称和头像，查看套餐信息并续费。"其余角色（管理员/成员/访客）及权限矩阵：`UNKNOWN`。
- 扣子空间协作权限：创建项目时选择访问权限；邀请协作方式：链接、邮箱邀请、二维码、邀请码、电话号码、名片（cozespace_invite_members.md）；"你可以邀请同事加入项目（消息、云盘、任务与记忆默认共享）"；"了解项目管理权限"（cozespace_collaborate_on_projects.md，权限矩阵字段 `UNKNOWN`）。
- 资源共享：知识库共享（guides_knowledge_base_share.md："将知识库共享给团队成员"）、技能企业级共享（guides_organization_share_capabilities.md）、项目模板/商店（市场）、数据表复制。

### 9.3 人机协作特征（对 Curis 重要）
- 多人 + 多 Agent 同项目协作：成员可在项目内直接与所有共享 Agent 对话、查看会话历史（会话历史默认项目内共享）。
- 人与 Agent 共同推进任务的官方表述："让人和 Agent 共同协作推进任务"（what_is_coze.md）。
- 组织内是否出现"Leader/主管 Agent"角色或审批链：`UNKNOWN`（未见证据）。

Sources: docs.coze.cn/guides_team_config.md；docs.coze.cn/guides_edition.md；docs.coze.cn/cozespace_invite_members.md；docs.coze.cn/cozespace_collaborate_on_projects.md；docs.coze.cn/cozespace_collaboration.md；docs.coze.cn/guides_knowledge_base_share.md；docs.coze.cn/guides_organization_share_capabilities.md

---

## 10. Publishing / Channels（发布与渠道）

### 10.1 发布渠道（扣子编程 guides_channels_differences.md，官方渠道差异表）
- 渠道清单：**Chat SDK、Web SDK、API、微信公众号、微信服务号、微信客服、微信小程序、抖音小程序、飞书、多维表格、掘金、扣子商店**。
- 关键功能差异矩阵（官方原文摘录）：
  - 全渠道支持：上传图片、快捷指令、清除上下文；
  - **飞书是唯一支持"触发器"的渠道**；飞书仅缺 TTS 与语音通话；
  - 微信限制多：不支持上传文件、TTS、语音通话、用户问题建议、流式输出；微信客服还不支持语音输入与开场白；微信服务号/客服/订阅号"不支持工作流输出节点提前输出消息内容，仅支持汇总后统一输出"；
  - 多维表格、掘金：不支持语音输入、TTS、语音通话、开场白、用户问题建议、流式输出；
  - Chat SDK / API / 扣子商店功能最全（仅触发器不支持）；
  - 问答节点、输入节点、消息节点、会话历史节点在不同渠道有支持差异（官方表逐节点标注）。
- 发布形态：Agent（Bot）、Application（应用）、工作流可独立发布为 API；发布历史/版本管理（"发布历史"面板）。

### 10.2 扣子空间侧发布
- Agent 发布状态管理（Agent 设置页："管理 Agent 的身份信息、发布状态…"）；发布给团队/组织的方式与字段：`UNKNOWN`。

Sources: docs.coze.cn/guides_channels_differences.md（正文）；docs.coze.cn/guides_publish_overview.md；docs.coze.cn/cozespace_agent_management.md

---

## 11. Conversation surface & composer（对话界面与输入区）

### 11.1 扣子空间对话（cozespace_session.md）
- "在扣子，解决复杂问题就像聊天一样简单。通过自然语言下达你的指令，Agent 会主动[思考、拆解、执行并汇报]"（摘要）。
- Composer 能力（摘要级）：文本输入、语音输入、上传文件（图片/文档/表格）、@某个 Agent（项目内多 Agent 时选择对话对象）、消息快捷指令；流式输出。
- 消息动作：重试/复制/点赞点踩（`UNKNOWN` 字段级）；卡片消息：任务卡片、日程卡片等（扣子空间各功能页以卡片形式呈现执行结果，`UNKNOWN` 细节）。
- 多端同步：Web/桌面/移动（what_is_coze.md）。

### 11.2 低代码侧对话体验字段
- 单 Agent 全局配置中影响对话面的字段：开场白、用户问题建议（3 条）、快捷指令、背景图片、语音（TTS 音色）、背景图片、清除上下文（各发布渠道支持差异见第 10 节）。

Sources: docs.coze.cn/cozespace_session.md；docs.coze.cn/guides_multiagent.md；docs.coze.cn/guides_channels_differences.md

---

## 12. Debug / Monitoring（调试、评测、数据分析）

- **预览与调试（编排期）**：右侧面板对话试运行；单 Agent 节点直连调试与试运行；"运行详情"查看每次对话的路由与节点执行（guides_preview_debug.md / guides_multiagent.md）。
- **日志**：工作流日志、智能体调用日志（日志查询页，按时间/状态筛选；字段 `UNKNOWN`）。
- **数据分析看板（guides_data.md）**："借助分析看板，你能够全面跟踪和分析已发布的低代码智能体、应用和工作流的运行状况，包括 Token[消耗]、调用[次数]、用户[数]等指标"（更多维度 `UNKNOWN`）。
- **评测**：模型试运行；是否提供独立 Evaluation 集/自动化评测：`UNKNOWN`（llms.txt 索引未见独立评测章节）。
- **扣子空间侧监控**：任务执行历史（成功/失败/暂停）、执行过程可视（执行器进度、生成物预览、积分消耗）；数据分析页：`UNKNOWN`。

Sources: docs.coze.cn/guides_preview_debug.md；docs.coze.cn/guides_data.md；docs.coze.cn/cozespace_task.md（索引）；docs.coze.cn/cozespace_job.md

---

## 13. Settings（设置分区与字段）

- **个人设置**：个人资料（头像/昵称）、账号、语言、通知、积分/账单入口（guides_setting_up_your_profile.md；字段级 `UNKNOWN`）。
- **企业设置（仅超级管理员）**："修改企业的设置，包括修改名称和头像，查看套餐信息并续费"（guides_team_config.md 原文）；成员管理、席位购买。
- **Agent 设置（扣子空间）**：身份信息、发布状态、（其余分区 `UNKNOWN`）。
- **低代码 Agent 全局设置分区**：模型设置、人设与回复逻辑、技能（插件/工作流/知识库/触发器/变量/数据库/长期记忆/文件盒）、对话体验（开场白/用户问题建议/快捷指令/背景图片/语音）、快捷指令绑定节点（多 Agent 模式）、发布配置（公开配置/渠道勾选）。
- **API Key**：低代码发布 API 需生成访问令牌（PAT）；字段级 `UNKNOWN`。
- **权限默认值**：项目访问权限（个人/团队）、知识库共享范围、技能共享范围（企业级）。

Sources: docs.coze.cn/guides_team_config.md；docs.coze.cn/guides_setting_up_your_profile.md（索引）；docs.coze.cn/cozespace_agent_management.md；docs.coze.cn/guides_multiagent.md；docs.coze.cn/llms.txt

---

## 14. Automation / Trigger / Schedule（自动化）

- **触发器（Trigger）**：智能体级定时/事件触发；"配置时间触发器，让智能体定时唤醒执行任务或主动发送消息"；渠道支持矩阵中**仅飞书渠道支持触发器**（guides_channels_differences.md）。触发器配置字段：`UNKNOWN`。
- **工作流定时执行**：工作流可独立发布并通过 API/定时调度运行（索引级证据）。
- **扣子空间日程（cozespace_job.md）**："在日历视图里，所有任务一目了然，不同颜色代表不同状态（待执行、执行中、已完成、已暂停、执行[失败]）"——任务以日历形式管理，支持设置执行周期（"你可以随时调整任务的执行周期"）；任务完成后 Agent 主动汇报结果。每日任务/周期任务/暂停/调整字段级 `UNKNOWN`。
- **AI 定时任务示例**：模板含"每日热点监控""电商选品"等定时类工作流模板。

Sources: docs.coze.cn/cozespace_job.md；docs.coze.cn/guides_channels_differences.md；docs.coze.cn/llms.txt

---

## 15. Visual / interaction observations（官方文档截图观察，APPROXIMATE）

- 多 Agent 编排画布（APPROXIMATE，来自官方文档配图描述）：中央画布横向流式布局，开始节点在最左，Agent 节点以卡片呈现、卡片上有节点名、适用场景与技能数量；节点间以连线表示跳转；右上角节点图标提供"直接对话/试运行"；右侧抽屉式预览调试窗。
- 扣子空间界面（APPROXIMATE）：左侧导航（空间/项目/日历/云盘/技能商店等）；项目页为会话流 + 右侧成员（人 + Agent）与文件/任务面板；任务卡片带状态色标。
- 会议旁听（APPROXIMATE）：Agent 可被拉入飞书会议旁听并生成纪要/待办（官方宣传与 quickstart 提及"会议旁听"能力；交互细节 `UNKNOWN`）。
- 对话界面（APPROXIMATE）：单输入框 composer，支持 @Agent、附件、语音；Agent 回复为卡片 + 过程步骤展开（执行计划/生成物预览）。

Sources: docs.coze.cn/guides_multiagent.md（配图说明）；docs.coze.cn/cozespace_quickstart.md；docs.coze.cn/cozespace_meeting_observation.md（索引，正文未抓取）

---

## 16. OBSERVATION → PATTERN → CURIS GAP（组织模型对照）

> 仅记录模式与候选差距，不做 Curis 架构决策。本节基于本文第 1–15 节证据。

### 16.1 OBSERVATION（Coze 事实）
1. Coze 的"多 Agent"核心机制是**对话路由**：开始节点 + 每个 Agent 的"适用场景"描述 + LLM 分发 + 全局跳转条件（最多 5 个，优先级高于场景描述）；会话控制权在 Agent 间**移交**，无显式聚合节点。
2. 每个 Agent 节点有**独立身份四件套**：独立提示词、独立模型设置、独立技能（插件/工作流/知识库）、独立名称（名称本身参与路由决策——"清晰的名称帮助 LLM 分配任务"）。
3. 组织级多 Agent 不靠画布，而靠**项目（Project）作为协作容器**：人 + 多 Agent 同项目，会话/文件/任务/记忆默认共享。
4. 记忆是**一等公民**：跨 Agent 可见的记忆列表，用户可增删改记忆条目，记忆有归属范围；长期记忆自动沉淀。
5. 自动化落在**日历/任务**上：任务有状态机（待执行/执行中/已完成/已暂停/执行失败）、可调周期、Agent 主动汇报。
6. 调试多 Agent 靠**画布单节点直连会话 + 预览调试面板 + 发布历史**；运行期靠日志与数据分析看板。
7. 组织治理：企业级角色（超级管理员）、席位、技能企业共享、知识库共享——但**未出现 Leader/主管 Agent、审批链、责任(RA)模型、会议制度**等组织概念。

### 16.2 PATTERN（可迁移的竞争模式）
- **P1 场景路由**：用"适用场景/职责描述 + 名称"让 LLM 做意图分发，而不是硬编码工作流——组织即路由。
- **P2 节点级身份**：每个子 Agent 独立模型 + 技能 + 提示词，故障域隔离（只调试出错的节点）。
- **P3 全局跳转条件**：少量高优先级硬规则覆盖 LLM 路由（安全阀模式）。
- **P4 项目 = 共享工作区**：多 Agent 协作的容器不是"团队对象"，而是带权限的项目及其共享资产（会话/文件/任务/记忆）。
- **P5 记忆治理 UI**：让人类直接读写 Agent 记忆（新增/编辑/删除/范围）。
- **P6 任务状态机 + 主动汇报**：自动化任务以日历承载，完成后 Agent 主动回播。
- **P7 单点调试通道**：画布上对任意子 Agent 直接开小会（旁路调试，不经过路由）。

### 16.3 CURIS GAP（候选差距；只记录，不决策）

**Curis 组织概念领先于 Coze 的部分（Coze 产品面未见的对应物）：**
- **Leader / 主管角色**：Coze 多 Agent 只有"开始节点分发 + 适用场景"，无持久 Leader Agent、无对下属 Agent 的绩效/职责界定。
- **Responsibility / Assignment 模型**：Coze 的分发是每条消息的实时路由，不是"分配责任—跟踪—回执"的持续指派关系；无 Assignment 对象。
- **Meeting 制度**：Coze 有会议旁听（飞书会议纪要），但无"AI 团队内部会议 / 议程 / 决议"机制。
- **Work ↔ Result 链**：Coze 的任务历史偏日志/会话，未提出 Work 与 Result 的显式对象链路。
- **Handoff 作为契约**：Coze 的 handoff 是隐式路由跳转（无交接说明、无上下文打包动作）。

**Coze 已上船、Curis 产品面需对照的 OPERATIONS（事实差距候选）：**
- O1 多 Agent 编排画布 + 单节点直连调试 + 分发策略可配置（"上次回复节点 vs 开始节点"）。
- O2 每个子 Agent 独立模型/提示词/技能绑定（技能=插件+工作流+知识库三类挂载）。
- O3 项目容器内人机混合成员与共享资产（会话/文件/任务/记忆）。
- O4 记忆管理 UI（列出、编辑、删除、设定范围）与跨 Agent 长期记忆。
- O5 日历化自动化任务（状态机 + 周期 + 主动汇报）。
- O6 发布矩阵（12+ 渠道 + 差异化功能矩阵 + 发布历史）与渠道能力降级表。
- O7 组织级共享（技能/知识库企业共享、席位、企业设置）。
- O8 数据分析看板（Token、调用、用户指标）+ 调用日志查询。
- O9 技能商店 + 工作流模板市场（组织化复用）。
- O10 全局跳转条件式安全阀（规则优先于 LLM 路由）。

### 16.4 风险提示
- 扣子（CN）已直接定位为"AI 团队协作平台 / AI 办公空间"，其"组建一支 AI 团队""项目协作""长期记忆""日程"叙事与 Curis 的 Company OS 定位正面重叠；本清单 O 系列各项为 Curis 产品面对照的最低基线证据。
- 国际版 Coze（coze.com）功能快照本次证据不足（`UNKNOWN` 项较多），后续可补充抓取。

---

## Sources

官方文档（docs.coze.cn，markdown 源）：
- https://docs.coze.cn/llms.txt（全量文档索引）
- https://docs.coze.cn/what_is_coze.md
- https://docs.coze.cn/guides_multiagent.md（多 Agent 模式，正文）
- https://docs.coze.cn/guides_channels_differences.md（发布渠道差异，正文）
- https://docs.coze.cn/guides_team_config.md（团队配置）
- https://docs.coze.cn/guides_edition.md
- https://docs.coze.cn/guides_llm.md
- https://docs.coze.cn/guides_knowledge.md
- https://docs.coze.cn/guides_workflow.md
- https://docs.coze.cn/guides_chatflow_mode.md
- https://docs.coze.cn/guides_preview_debug.md
- https://docs.coze.cn/guides_data.md
- https://docs.coze.cn/guides_publish_overview.md
- https://docs.coze.cn/guides_agent_workflow.md
- https://docs.coze.cn/guides_organization_share_capabilities.md
- https://docs.coze.cn/cozespace_agent_overview.md
- https://docs.coze.cn/cozespace_agent_management.md
- https://docs.coze.cn/cozespace_coze_agent.md
- https://docs.coze.cn/cozespace_collaboration.md
- https://docs.coze.cn/cozespace_collaborate_on_projects.md
- https://docs.coze.cn/cozespace_invite_members.md
- https://docs.coze.cn/cozespace_create_projects.md
- https://docs.coze.cn/cozespace_memory.md / cozespace_memory_edit.md
- https://docs.coze.cn/cozespace_session.md
- https://docs.coze.cn/cozespace_job.md
- https://docs.coze.cn/cozespace_skill_overview.md
- https://docs.coze.cn/cozespace_coze_billing_overview.md
- https://docs.coze.cn/cozespace_quickstart.md

二手来源（参考）：
- https://cozehq.medium.com/building-an-all-in-one-personal-assistant-with-cozes-multi-agent-mode-e0f695137edf（国际版 Multi-Agent Mode 实操）
- https://www.youtube.com/watch?v=l00ZB2ZaVO0（Coze Multi-agent mode 视频教程）
- 知乎《COZE多agent企业应用实践落地》；CSDN《字节Coze多Agent模式》；飞书文档《Coze进阶：多Agent模式下定制工作流》
