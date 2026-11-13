# Curis 人才与能力 · 中文产品化（首批 Batch1）

Status: Product-facing Presentation（非 Source Truth）  
规程：`Curis_Capability_Intelligence_SOP.md` §2  
说明：以下为面向中文用户的「人才市场 / 技能商店」商品卡。每条同时保留 **Source Truth**（原始名称/描述/URL/版本/Digest/License/元数据），翻译与改写不改变原能力边界、不写入不存在的能力。当前全部为 **Candidate**，未经真实任务验证不得标 `CURIS_READY`。

---

## 1. Web 设计指南（Vercel）

- **中文名称**：网页设计指南助手
- **一句话简介**：按 100+ 条可访问性、性能与体验规则，帮员工把网页做得更专业、更好用。
- **详细介绍**：一个网页设计与审查助手，内置 Vercel 总结的 100 多条设计规则，覆盖可访问性、加载性能、信息层级与交互体验。员工在写前端页面或审查 UI 时，它会指出不合规之处并给出可落地的改法。
- **能力分类**：设计 / 前端
- **擅长什么**：网页可用性审查、性能与可访问性体检、设计规则落地
- **适合做什么**：前端页面自查、UI 走查、设计规范的代码侧落地
- **典型使用场景**：员工做完一个落地页，让助手按规则体检并给出修改清单。
- **需要的工具 / 连接**：Claude 类模型；本地前端项目（审阅当前代码）
- **来源**：Vercel（开源集合）
- **安全 / 权限提示**：仅读取本地代码做静态审查，不联网、不上传业务数据；建议在可信项目内使用。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: web-design-guidelines (vercel-labs/agent-skills)
- Original Description: 100+ accessibility/performance/UX rules for auditing web UI.
- Source URL: https://github.com/vercel-labs/agent-skills
- Version/Digest: snapshot 2026-08-18（建议固定 commit digest）
- License: MIT
- Original Metadata: type=Skill; category=design/frontend; deps=Claude; source=vercel-labs/agent-skills

</details>

---

## 2. Figma 设计稿转代码（OpenAI）

- **中文名称**：设计稿转代码助手
- **一句话简介**：把 Figma 设计稿直接变成可运行的界面代码，省去手动对照。
- **详细介绍**：连接 Figma 的设计文件，读取图层、颜色、间距与组件结构，自动生成对应的前端代码（如 React）。员工拿到设计师稿子后，可以快速得到第一版实现，再在此基础上调整。
- **能力分类**：设计 / 前端
- **擅长什么**：设计稿解析、组件化代码生成、设计还原
- **适合做什么**：把视觉稿转为前端代码、还原设计规范
- **典型使用场景**：设计师交付 Figma 文件，员工让助手生成首版页面骨架。
- **需要的工具 / 连接**：需 Figma API 令牌（用户自有）；Claude/Codex 类模型
- **来源**：OpenAI（开源技能集合）
- **安全 / 权限提示**：需用户提供 Figma 访问令牌；令牌仅用于读取指定文件，建议用最小权限令牌并妥善保管，不写入代码库。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: figma* (openai/skills .curated)
- Original Description: Convert Figma designs to code / generate from design files.
- Source URL: https://github.com/openai/skills
- Version/Digest: snapshot 2026-08-18
- License: per-skill LICENSE.txt（REVIEW，需逐文件复核）
- Original Metadata: type=Skill; category=design; deps=Figma API, Codex/Claude

</details>

---

## 3. 产品经理方法库（phuryn/pm-skills）

- **中文名称**：产品经理方法库
- **一句话简介**：把成熟的产品管理方法（PRD、路线图、用户访谈等）变成员工顺手可用的能力。
- **详细介绍**：一套面向产品经理的技能集合，覆盖 68 个常用方法论，包括撰写需求文档（PRD）、制定产品路线图、用户访谈提纲、竞品分析与上线复盘等。员工做产品决策或写材料时，可以直接套用结构化模板。
- **能力分类**：产品
- **擅长什么**：需求文档、路线图、用户研究、竞品分析
- **适合做什么**：产品规划、需求梳理、评审材料准备
- **典型使用场景**：员工要写一版新功能 PRD，让助手按结构化模板产出初稿。
- **需要的工具 / 连接**：Claude/Cursor 类模型；无外部连接
- **来源**：phuryn（开源）
- **安全 / 权限提示**：本地模型调用，不联网；内容仅供内部参考，关键决策仍需人审。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: pm-skills (phuryn)
- Original Description: 68 product-management methodology skills (PRD/roadmap/interview).
- Source URL: https://github.com/phuryn/pm-skills
- Version/Digest: snapshot 2026-08-18
- License: MIT
- Original Metadata: type=Skill/Expert; category=product; count=68; deps=LLM

</details>

---

## 4. 数据分析报告生成器（Evidence）

- **中文名称**：数据分析报告生成器
- **一句话简介**：连上数据库，用 SQL 把数据变成可读的分析报告网页。
- **详细介绍**：一个基于 SQL 与模板的报告工具，员工写查询、连上数据仓库后，它能自动生成带图表、可分享的分析报告页面。适合把经营数据、业务指标定期沉淀成可阅读的报表。
- **能力分类**：数据 / BI
- **擅长什么**：SQL 取数、指标报告、可视化网页生成
- **适合做什么**：经营报表、指标看板、数据汇报
- **典型使用场景**：员工连上公司数仓，按周自动产出经营指标报告页。
- **需要的工具 / 连接**：需数据库连接（用户自有，如 Postgres/Snowflake）；Node 运行环境
- **来源**：evidence-dev（开源）
- **安全 / 权限提示**：直接读取用户数据库，请用只读账号并限制库表范围；避免在公网暴露报告页。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: Evidence (evidence-dev/evidence)
- Original Description: Generate data reports from SQL databases using templates.
- Source URL: https://github.com/evidence-dev/evidence
- Version/Digest: snapshot 2026-08-18
- License: MIT
- Original Metadata: type=Tool/Skill; category=data/BI; deps=SQL DB, Node

</details>

---

## 5. 深度研究助手（gpt-researcher）

- **中文名称**：深度研究助手
- **一句话简介**：自动上网查资料、交叉核对，产出带引用的研究报告。
- **详细介绍**：一个自主研究助手，会先制定研究计划，再并行检索多个来源、整理要点并生成带引用出处的研究报告。员工需要快速搞清一个陌生领域或竞品时，可以交给它做第一手调研。
- **能力分类**：研究
- **擅长什么**：资料检索、交叉验证、研究综述撰写
- **适合做什么**：行业研究、竞品分析、技术调研
- **典型使用场景**：员工要在一小时内摸清某个新市场的玩家与格局，让助手产出带来源的报告。
- **需要的工具 / 连接**：需检索类 API（如 Tavily 等，用户自有）；任意 LLM
- **来源**：assafelovic（开源）
- **安全 / 权限提示**：会调用外部检索并可能抓取网页；注意来源可信度，关键结论建议人工复核引用。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: gpt-researcher
- Original Description: Autonomous deep research agent (planner + parallel crawler + publisher with citations).
- Source URL: https://github.com/assafelovic/gpt-researcher
- Version/Digest: snapshot 2026-08-18
- License: Apache-2.0
- Original Metadata: type=Expert/Tool; category=research; deps=LLM + Tavily etc.

</details>

---

## 6. 金融投研团队（FinRobot）

- **中文名称**：金融投研团队
- **一句话简介**：一组金融分析智能体，覆盖投研、估值、风险等常见金融任务。
- **详细介绍**：一个面向金融的 multi-agent 框架，内置多个专业金融智能体，可完成投资研究、公司估值、风险分析等工作。员工做金融相关决策时，可以调用相应角色做初步分析。
- **能力分类**：金融
- **擅长什么**：投研、估值建模、风险分析
- **适合做什么**：金融研究、标的分析、风险初评
- **典型使用场景**：员工要评估一家上市公司，让投研智能体给出基本面初判。
- **需要的工具 / 连接**：需金融数据 API（如 FMP，用户自有）；OpenAI 类模型
- **来源**：AI4Finance Foundation（开源）
- **安全 / 权限提示**：金融分析仅供参考，不构成投资建议；需自备数据 API 密钥，注意合规与授权范围。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: finrobot (ai4finance-foundation/finrobot)
- Original Description: Multi-agent framework with 8 financial agents (research/valuation/risk).
- Source URL: https://github.com/ai4finance-foundation/finrobot
- Version/Digest: snapshot 2026-08-18
- License: Apache-2.0
- Original Metadata: type=Expert-Team; category=finance; deps=OpenAI + FMP API

</details>

---

## 7. 合同审查助手（legal-contract-agent）

- **中文名称**：合同审查助手
- **一句话简介**：读合同、提风险、给审查意见，帮员工更快看清条款坑点。
- **详细介绍**：一个合同审查助手，能抽取主服务协议（MSA）等关键条款、做风险评分，并基于检索增强生成红线提示与审查意见。员工收到合同草稿时，可以先让它标出高风险点。
- **能力分类**：法律
- **擅长什么**：合同条款抽取、风险评分、审查意见
- **适合做什么**：合同初筛、风险标注、审查清单
- **典型使用场景**：员工收到一份供应商合同，先让助手标出责任与违约相关的高风险条款。
- **需要的工具 / 连接**：需向量数据库（如 pgvector）；OpenAI 类模型
- **来源**：argahv（开源）
- **安全 / 权限提示**：处理合同等敏感文本，建议在隔离环境运行、避免外发；**输出不构成法律意见，重要合同须由执业律师确认**（License 待逐文件复核，当前 REVIEW）。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: legal-contract-agent (argahv)
- Original Description: Contract review (MSA extraction / risk scoring / RAG redlines).
- Source URL: https://github.com/argahv/legal-contract-agent
- Version/Digest: snapshot 2026-08-18
- License: REVIEW（未明示，需逐文件复核；当前标记 REVIEW，未晋级）
- Original Metadata: type=Expert/Tool; category=legal; deps=OpenAI + pgvector

</details>

---

## 8. 代码审查助手（Code Reviewer）

- **中文名称**：代码审查助手
- **一句话简介**：自动看代码改动，发现潜在问题并给出修改建议。
- **详细介绍**：一个代码审查助手，会阅读改动内容、对照项目上下文，指出可能的 bug、安全隐患和可维护性问題，并给出具体的修改建议。员工提交代码前可以先用它做一遍自检。
- **能力分类**：研发 / 质量
- **擅长什么**：变更审查、问题发现、改进建议
- **适合做什么**：提交前自检、Code Review 辅助、质量门禁
- **典型使用场景**：员工完成一个功能分支，让助手在提 PR 前先审查一轮。
- **需要的工具 / 连接**：需代码仓库访问（如 GitHub）；Claude/OpenClaw 类模型
- **来源**：OpenClaw（ClawHub，开源集合）
- **安全 / 权限提示**：需读取仓库代码；仅用于内部项目，注意令牌最小权限。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: code-reviewer (OpenClaw ClawHub)
- Original Description: Automated code review with issue detection and suggestions.
- Source URL: https://github.com/openclaw/clawhub
- Version/Digest: snapshot 2026-08-18
- License: per-skill REVIEW（需逐文件复核）
- Original Metadata: type=Skill; category=engineering/QA; deps=OpenClaw, repo access

</details>

---

## 9. 增长营销技能库（marketingskills）

- **中文名称**：增长营销技能库
- **一句话简介**：把常见的增长与营销打法（文案、SEO、付费投放等）变成员工可用的能力。
- **详细介绍**：一套增长营销技能集合，覆盖转化优化（CRO）、文案写作、搜索引擎优化（SEO）、付费投放等 50+ 技能。员工做拉新、转化或内容运营时，可以按需调用对应方法。
- **能力分类**：增长 / 营销
- **擅长什么**：文案、SEO、付费投放、转化优化
- **适合做什么**：营销内容生产、增长实验设计
- **典型使用场景**：员工要写一版落地页文案并做 SEO 自检，调用对应技能辅助。
- **需要的工具 / 连接**：Claude 类模型；无强制外部连接
- **来源**：coreyhaines31（开源）
- **安全 / 权限提示**：本地模型调用；营销文案需符合平台规则与广告法，人工把关。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: marketingskills (coreyhaines31)
- Original Description: 50+ marketing skills (CRO/copy/SEO/paid).
- Source URL: https://github.com/coreyhaines31/marketingskills
- Version/Digest: snapshot 2026-08-18
- License: REVIEW（需逐文件复核）
- Original Metadata: type=Expert/Skill; category=growth; count=50+

</details>

---

## 10. 个性化辅导老师（DeepTutor）

- **中文名称**：个性化辅导老师
- **一句话简介**：像一对一老师那样，根据学生情况出题、讲解、跟踪进度。
- **详细介绍**：一个个性化教育助手，具备三层记忆，能根据学习者的水平出题、讲解难点，并做研究性引导。员工或家庭成员做知识学习时，可以把它当随身的辅导老师。
- **能力分类**：教育
- **擅长什么**：个性化讲解、出题、学习跟踪
- **适合做什么**：知识点辅导、练习出题、学习规划
- **典型使用场景**：员工想系统学某个新知识，让助手按节奏出题并讲解。
- **需要的工具 / 连接**：多 LLM / GraphRAG；无强制外部连接
- **来源**：HKUDS（开源）
- **安全 / 权限提示**：涉及学习内容，建议在校验过的知识范围内使用；不替代正规教学评估。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: DeepTutor (HKUDS/DeepTutor)
- Original Description: Personalized tutoring with 3-tier memory (solve/quiz/research).
- Source URL: https://github.com/HKUDS/DeepTutor
- Version/Digest: snapshot 2026-08-18
- License: Apache-2.0
- Original Metadata: type=Expert-Team; category=education; deps=multi-LLM/GraphRAG

</details>

---

## 11. 中文长文档处理（doc-pro）

- **中文名称**：长文档处理助手
- **一句话简介**：读得懂长文档，帮你摘要、抽取和整理中文资料。
- **详细介绍**：一个面向中文场景的长文档处理助手，能解析长篇文档、提取关键信息、做摘要与结构化整理。员工面对合同、报告、资料汇编时，可以用它快速抓住重点。
- **能力分类**：办公 / 中文处理
- **擅长什么**：长文解析、摘要、信息抽取
- **适合做什么**：文档摘要、资料整理、要点提取
- **典型使用场景**：员工收到一份几十页的行业报告，让助手先输出要点摘要。
- **需要的工具 / 连接**：OpenClaw 运行环境；无强制外部连接
- **来源**：OpenClaw（ClawHub，开源集合）
- **安全 / 权限提示**：处理含敏感信息的文档时，在隔离环境运行，避免外发。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: doc-pro (OpenClaw ClawHub)
- Original Description: Long-document parsing, summarization, information extraction.
- Source URL: https://github.com/openclaw/clawhub
- Version/Digest: snapshot 2026-08-18
- License: per-skill REVIEW
- Original Metadata: type=Skill; category=office/Chinese; deps=OpenClaw

</details>

---

## 12. 飞书多维表格助手（feishu-bitable）

- **中文名称**：飞书多维表格助手
- **一句话简介**：帮你读写飞书多维表格，把表格当数据库来用。
- **详细介绍**：一个连接飞书多维表格的助手，能按指令查询、写入、更新表格数据，把多维表格当作轻量数据库来驱动工作流。员工做运营台账、项目管理时可以用它自动化表格操作。
- **能力分类**：中文协作 / 办公自动化
- **擅长什么**：表格读写、数据同步、轻量自动化
- **适合做什么**：台账管理、数据汇总、表格驱动流程
- **典型使用场景**：员工把每日运营数据自动写入飞书多维表格并生成汇总。
- **需要的工具 / 连接**：需飞书 API 凭据（用户自有）
- **来源**：OpenClaw（ClawHub，开源集合）
- **安全 / 权限提示**：需飞书访问凭据；请用最小权限应用，凭据不入库、不进代码；注意表格数据权限范围。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: feishu-bitable (OpenClaw ClawHub)
- Original Description: Feishu Base (Bitable) read/write automation.
- Source URL: https://github.com/openclaw/clawhub
- Version/Digest: snapshot 2026-08-18
- License: per-skill REVIEW
- Original Metadata: type=Skill; category=collaboration/Chinese; deps=Feishu API

</details>

---

## 13. 公司经营分析师（组合角色 · 待组合 / Gap）

- **中文名称**：公司经营分析师（Curis 内置，非外部市场 Expert）
- **一句话简介**：定期看公司经营数据，告诉 CEO 业务健康度与异常。
- **详细介绍**：数据分析部的默认角色，负责把分散在各业务空间的数据汇总成经营视图，发现趋势与异常，向 CEO 给出可读的分析结论。**当前候选池无现成外部 Expert**；建议由 Codex 从「取数（SQL/数仓 MCP）+ 分析（数据 Skill）+ 研究（gpt-researcher）+ 报告（Evidence / docx Skill）」组合验证，或由 Curis 定义内置 Employee。
- **能力分类**：数据 / 经营分析
- **擅长什么**：经营指标汇总、异常识别、经营报告
- **适合做什么**：周/月经营复盘、指标看板、异常预警
- **典型使用场景**：每周期让该角色拉取各业务空间指标，生成经营健康度报告。
- **需要的工具 / 连接**：数仓/SQL MCP、数据 Skill、报告 Skill（组合）
- **来源**：Curis 内置（组件来自候选池，见验证文档 §2）
- **安全 / 权限提示**：读取公司经营数据，须最小权限、隔离运行；结论供决策参考。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: Company Analyst / 公司经营分析师（Curis default functional role）
- Original Description: Curis-builtin default role for 数据分析部; no external market candidate.
- Source URL: 内部（非外部源）
- Version/Digest: curis-builtin
- License: curis-builtin（非外部）
- Original Metadata: verdict=Gap(待组合); components=gpt-researcher+Evidence+SQL/MetaBase MCP+数据 Skill

</details>

---

## 14. 空间工程核心 Employee（Curis 内置 · Gap）

- **中文名称**：空间工程核心员工（Curis 内置，非外部市场 Expert）
- **一句话简介**：负责创建和运维 Curis 的业务空间，让新业务能快速起步。
- **详细介绍**：空间工程部的默认核心角色，负责业务空间（Workspace）的搭建、配置与运维。这是 Curis 平台内部职能，**候选池无对应外部候选**，必须由 Curis 自行定义内置 Employee，不得标为外部市场 Expert。
- **能力分类**：平台 / 空间工程
- **擅长什么**：业务空间创建、配置、运维
- **适合做什么**：新业务空间初始化、空间模板维护
- **典型使用场景**：CEO 要开一个新产品业务空间，由该角色完成初始化。
- **需要的工具 / 连接**：Curis Runtime（内部）
- **来源**：Curis 内置（非外部）
- **安全 / 权限提示**：高权限平台职能，仅限内部受控运行。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: 默认空间工程核心 Employee（Curis default functional role）
- Original Description: Curis-builtin platform role; workspace build/configure/maintain.
- Source URL: 内部（非外部源）
- Version/Digest: curis-builtin
- License: curis-builtin（非外部）
- Original Metadata: verdict=Gap（无外部候选）；must be curis-builtin, not external Expert

</details>

---

## 15. 本批汇总

| # | 中文名 | 类型 | 外部候选 | License | 中文产品化 |
|---|---|---|---|---|---|
| 1 | 网页设计指南助手 | Skill | 是 | MIT | ✅ |
| 2 | 设计稿转代码助手 | Skill | 是 | REVIEW | ✅ |
| 3 | 产品经理方法库 | Skill/Expert | 是 | MIT | ✅ |
| 4 | 数据分析报告生成器 | Tool/Skill | 是 | MIT | ✅ |
| 5 | 深度研究助手 | Expert/Tool | 是 | Apache-2.0 | ✅ |
| 6 | 金融投研团队 | Expert-Team | 是 | Apache-2.0 | ✅ |
| 7 | 合同审查助手 | Expert/Tool | 是 | REVIEW | ✅ |
| 8 | 代码审查助手 | Skill | 是 | REVIEW | ✅ |
| 9 | 增长营销技能库 | Skill | 是 | REVIEW | ✅ |
| 10 | 个性化辅导老师 | Expert-Team | 是 | Apache-2.0 | ✅ |
| 11 | 长文档处理助手 | Skill | 是 | REVIEW | ✅ |
| 12 | 飞书多维表格助手 | Skill | 是 | REVIEW | ✅ |
| 13 | 公司经营分析师 | 组合/内置 | **Gap** | curis-builtin | ✅（占位） |
| 14 | 空间工程核心员工 | 内置 | **Gap** | curis-builtin | ✅（占位） |

> 全部仍为 **Candidate**。License=REVIEW 的条目在逐文件复核确认前保持 BLOCKED，不晋级 `CURIS_READY`。

---

## 16. 本轮增量（2026-08-19 周常自动化 · 情报专项）

> 来源：alirezarezvani/claude-skills 个体技能深度枚举（MIT 清晰）。以下 11 条均为 High 优先级 + License 清晰，按 SOP §2 补中文商品卡。全部仍为 **Candidate**，未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。

---

## 16.1 网页无障碍审计助手（a11y-audit）

- **中文名称**：网页无障碍审计助手
- **一句话简介**：按 WCAG 2.2 标准自动检查网页的无障碍问题，并给出修复建议。
- **详细介绍**：一个网页无障碍审计助手，能扫描 React、Next.js、Vue、Angular、Svelte 和原生 HTML 页面，识别 20 多类无障碍违规（如对比度不足、缺失替代文本、键盘不可达），并附对比度检查器与框架级修复范式。
- **能力分类**：设计 / 前端 / 质量
- **擅长什么**：无障碍合规体检、对比度检查、可访问性修复建议
- **适合做什么**：前端页面无障碍自查、上线前可访问性门禁
- **典型使用场景**：员工做完一个页面，让助手按 WCAG 2.2 体检并列出待修项。
- **需要的工具 / 连接**：Claude 类模型；本地前端项目（静态扫描）
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：仅读取本地代码做静态审查，不联网、不上传业务数据；建议在可信项目内使用。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: a11y-audit (alirezarezvani/claude-skills)
- Original Description: WCAG 2.2 accessibility audit and fix for React/Next/Vue/Angular/Svelte/HTML; static scanner, 20+ violation types, contrast checker, framework-specific fix patterns.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19（建议固定 commit digest）
- License: MIT
- Original Metadata: type=Skill; category=design/frontend/qa; deps=Claude; source=alirezarezvani/claude-skills

</details>

---

## 16.2 多智能体协作中枢（AgentHub）

- **中文名称**：多智能体协作中枢
- **一句话简介**：让多个 AI 分身并行干活、互相竞争优化，再由评审挑出最好结果。- **详细介绍**：一个多智能体编排助手，能同时生成多个并行子代理去竞争完成同一任务（代码优化、文案草稿、研究思路等），内置 DAG 任务编排、LLM 评审模式和消息板协调，把“一个人想”变成“一队人比”。
- **能力分类**：研发 / 编排
- **擅长什么**：并行多代理、竞争式优化、任务编排
- **适合做什么**：需要多种解法对比的任务、复杂任务拆解并行
- **典型使用场景**：员工面临一个难题，让中枢派出多个代理各给一版方案再择优。
- **需要的工具 / 连接**：Claude 类模型；无强制外部连接
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：本地模型调用；并行代理可能多次调用外部工具，注意成本与权限边界。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: agenthub (alirezarezvani/claude-skills)
- Original Description: Multi-agent collaboration — spawn N parallel subagents that compete on code optimization/content drafts/research; DAG orchestration, LLM judge mode, message board.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill; category=orchestration; deps=Claude

</details>

---

## 16.3 AWS 云架构师（aws-architect）

- **中文名称**：AWS 云架构师
- **一句话简介**：帮你设计 AWS Serverless 架构，给出可落地的模板与成本优化建议。
- **详细介绍**：一个 AWS 架构助手，能设计 Serverless 架构、生成 IaC（基础设施即代码）模板、做成本优化并配套 CI/CD 流水线方案，适合把想法快速落到云上。
- **能力分类**：云 / 架构
- **擅长什么**：Serverless 设计、IaC 模板、成本优化
- **适合做什么**：云架构方案设计、上云脚手架
- **典型使用场景**：员工要做一个新服务，让助手给出 AWS 架构与部署模板。
- **需要的工具 / 连接**：需 AWS 凭证（用户自有）；Claude 类模型
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：涉及云资源与凭证，请用最小权限角色、避免写死密钥；架构建议需结合账号实际配额。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: aws-architect (alirezarezvani/claude-skills)
- Original Description: AWS serverless architecture design with IaC templates, cost optimization, CI/CD pipelines.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill; category=cloud/architecture; deps=AWS credentials, Claude

</details>

---

## 16.4 业务增长技能包（business-growth-skills）

- **中文名称**：业务增长技能包
- **一句话简介**：一组增长业务角色（客户成功/销售工程/营收运营/合同提案），补齐商业侧执行力。
- **详细介绍**：一个面向业务增长的角色集合，内置客户成功经理、销售工程师、营收运营、合同与提案撰写四个角色，覆盖从线索到签约的增长闭环动作，员工做商业化推进时可直接调用对应角色。
- **能力分类**：增长 / 商业
- **擅长什么**：客户成功、销售工程、营收运营、合同提案
- **适合做什么**：商业化推进、销售支撑、合同起草
- **典型使用场景**：员工要写一份客户提案，让合同与提案角色给出结构初稿。
- **需要的工具 / 连接**：Claude 类模型；无强制外部连接
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：涉及客户与合同内容，建议在隔离环境、避免外发敏感商业数据。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: business-growth-skills (alirezarezvani/claude-skills)
- Original Description: 4 business & growth skills: customer success manager, sales engineer, revenue operations, contract & proposal writer.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Expert-Team; category=growth/business; count=4 roles; deps=Claude

</details>

---

## 16.5 高管智囊团（虚拟董事会 · c-level-skills）

- **中文名称**：高管智囊团（虚拟董事会）
- **一句话简介**：一组 C 级高管人格（CEO/CTO/CFO/CMO…），像董事会那样帮你压测决策。
- **详细介绍**：一个虚拟董事会助手，内置 28 个 C 级高管人格（CEO、CTO、COO、CPO、CMO、CFO、CRO、CISO、CHRO 等），加上高管教练、创始人教练、董事会纪要、竞争情报与 M&A 打法。员工做重大经营决策前，可以让“董事会”从多视角给出意见。
- **能力分类**：高管顾问 / 战略
- **擅长什么**：多视角决策压测、董事会纪要、竞争情报、M&A 推演
- **适合做什么**：战略决策辅助、经营复盘、硬决策预演
- **典型使用场景**：CEO 面临一个扩张决策，让虚拟董事会从各职能视角给出风险与机会清单。
- **需要的工具 / 连接**：Claude 类模型；无强制外部连接
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：输出为决策参考，不替代真实董事会/执业判断；涉及敏感经营数据请在隔离环境。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: c-level-skills (alirezarezvani/claude-skills)
- Original Description: 28 C-level advisory skills: virtual board (CEO/CTO/COO/CPO/CMO/CFO/CRO/CISO/CHRO...), executive mentor, founder coach, board deck builder, competitive intel, M&A playbook.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Expert-Team; category=c-level/advisory; count=28 personas; deps=Claude

</details>

---

## 16.6 代码转产品需求助手（code-to-prd）

- **中文名称**：代码转产品需求助手
- **一句话简介**：读已有代码库，反向生成一份完整的产品需求文档（PRD）。
- **详细介绍**：一个代码逆向工程助手，能分析前端（React/Vue/Angular/Next）、后端（NestJS/Django/Express/FastAPI）或全栈代码库，自动生成结构化 PRD，配套两个 Python 脚本与 `/code-to-prd` 命令。
- **能力分类**：产品 / 研发
- **擅长什么**：代码理解、PRD 生成、架构梳理
- **适合做什么**：接手老项目写文档、需求梳理
- **典型使用场景**：员工接手一个没有文档的代码库，让助手先产出 PRD 初稿。
- **需要的工具 / 连接**：Claude 类模型；本地代码库访问
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：读取代码库；仅用于内部项目，注意仓库权限范围。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: code-to-prd (alirezarezvani/claude-skills)
- Original Description: Reverse-engineer any codebase into a complete PRD (frontend/backend/fullstack); 2 Python scripts, /code-to-prd slash command.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill; category=product/engineering; deps=Claude, repo access

</details>

---

## 16.7 数据质量审计助手（data-quality-auditor）

- **中文名称**：数据质量审计助手
- **一句话简介**：给数据集做体检，查出缺失、异常和不一致，并打质量分。
- **详细介绍**：一个数据质量审计助手，能从完整性、一致性、准确性、有效性四个维度检查数据集，给出 DQS 质量评分、缺失值分析（MCAR/MAR/MNAR 分类）与多种异常检测方法，全部用标准库 Python 工具实现、零额外依赖。
- **能力分类**：数据 / BI / 质量
- **擅长什么**：数据质量评分、缺失值/异常值检测、数据画像
- **适合做什么**：数仓入仓前质检、报表数据校验
- **典型使用场景**：员工要出经营报表前，让助手先对底表做一轮质量体检。
- **需要的工具 / 连接**：需数据集访问（用户自有）；Claude 类模型
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：读取业务数据，请用只读账号并限制库表范围。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: data-quality-auditor (alirezarezvani/claude-skills)
- Original Description: Audit datasets for completeness/consistency/accuracy/validity; DQS scoring, missing-value analyzer, outlier detector (stdlib-only Python).
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill; category=data/BI/qa; deps=Python, dataset access

</details>

---

## 16.8 创始人陪练（executive-mentor）

- **中文名称**：创始人陪练（高管教练）
- **一句话简介**：像严苛的搭档一样，帮你压测计划、准备董事会、做艰难决策与复盘。
- **详细介绍**：一个面向创始人与高管的对抗式思考伙伴，会主动挑战你的计划、帮你准备董事会材料、陪你做硬决策推演，并在事后做复盘，内置多个子技能与命令。
- **能力分类**：高管顾问 / 教练
- **擅长什么**：计划压测、董事会准备、硬决策、复盘
- **适合做什么**：战略讨论、决策预演、高管陪练
- **典型使用场景**：CEO 要做一次重要汇报前，让陪练先挑刺并补齐论证。
- **需要的工具 / 连接**：Claude 类模型；无强制外部连接
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：涉及经营敏感话题，建议在隔离环境；输出为参考，不替代真实顾问。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: executive-mentor (alirezarezvani/claude-skills)
- Original Description: Adversarial thinking partner for founders/executives; stress-tests plans, board prep, hard calls, postmortems.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Expert; category=c-level/advisory; deps=Claude

</details>

---

## 16.9 全栈工程师（fullstack-engineer）

- **中文名称**：全栈工程师
- **一句话简介**：从前端到后端到部署，帮你把全栈功能一次做出来。
- **详细介绍**：一个全栈工程助手，覆盖 React、Node、数据库与部署的完整链路，能按需求搭建前端界面、写后端接口、接数据库并给出部署方式，适合快速把产品想法落成可运行的服务。
- **能力分类**：研发
- **擅长什么**：前端开发、后端接口、数据库对接、部署
- **适合做什么**：全栈功能实现、原型搭建
- **典型使用场景**：员工要做一个内部小工具，让助手从前端到部署一气呵成。
- **需要的工具 / 连接**：Claude 类模型；Node 运行环境
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：会写入代码与依赖；建议在受控项目内、走代码审查后再合并。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: fullstack-engineer (alirezarezvani/claude-skills)
- Original Description: Full-stack engineering with React, Node, databases, and deployment.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill; category=engineering; deps=Claude, Node

</details>

---

## 16.10 Google 办公套件自动化（google-workspace-cli）

- **中文名称**：Google 办公套件自动化
- **一句话简介**：用一条命令自动处理 Gmail、网盘、表格、日历等 Google 办公套件。
- **详细介绍**：一个 Google Workspace 自动化助手，通过 gws CLI 管理 Gmail、Drive、Sheets、Calendar、Docs、Chat、Tasks，内置 43 个常用配方与多种角色组合，把日常办公操作变成可重复的自动化。
- **能力分类**：办公自动化
- **擅长什么**：邮件/文档/表格/日历自动化、跨套件联动
- **适合做什么**：办公流程自动化、日报周报、信息同步
- **典型使用场景**：员工要把每周数据自动写入 Google Sheets 并生成日历提醒。
- **需要的工具 / 连接**：需 Google 凭据（用户自有，OAuth）
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：需 Google 授权；请用最小权限、凭据不入库；注意所操作数据的范围。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: google-workspace-cli (alirezarezvani/claude-skills)
- Original Description: Google Workspace administration via gws CLI — Gmail/Drive/Sheets/Calendar/Docs/Chat/Tasks; 43 recipes, persona bundles.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill; category=office-automation; deps=Google credentials

</details>

---

## 16.11 产品技能集（product-skills）

- **中文名称**：产品技能集
- **一句话简介**：一套产品方法技能（用户体验研究、UI 设计系统、竞品拆解等），顺手可用。
- **详细介绍**：一个产品技能集合，覆盖 14 项常用产品能力：产品策略、敏捷产品负责人、UX 研究、UI 设计系统、竞品拆解、落地页生成、SaaS 脚手架、产品分析、实验设计、产品发现、路线图沟通、代码转 PRD、研究摘要等。员工做产品工作时可按场景调用。
- **能力分类**：产品
- **擅长什么**：UX 研究、UI 设计系统、竞品拆解、落地页、产品分析
- **适合做什么**：产品规划、用户体验、竞品分析
- **典型使用场景**：员工要评估一个竞品，让竞品拆解技能产出结构化对比。
- **需要的工具 / 连接**：Claude 类模型；无强制外部连接
- **来源**：alirezarezvani（开源）
- **安全 / 权限提示**：本地模型调用；研究结论建议结合真实数据复核。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: product-skills (alirezarezvani/claude-skills)
- Original Description: 14 product skills: PM toolkit (RICE/PRDs), agile PO, UX researcher, UI design system, competitive teardown, landing page generator, SaaS scaffolder, product analytics, experiment designer, product discovery, roadmap communicator, code-to-prd, research summarizer.
- Source URL: https://github.com/alirezarezvani/claude-skills
- Version/Digest: snapshot 2026-08-19
- License: MIT
- Original Metadata: type=Skill集合; category=product; count=14; deps=Claude

</details>

---

## 16.12 本轮增量汇总

| # | 中文名 | 类型 | 外部候选 | License | 中文产品化 |
|---|---|---|---|---|---|
| 1 | 网页无障碍审计助手 | Skill | 是 | MIT | ✅ |
| 2 | 多智能体协作中枢 | Skill | 是 | MIT | ✅ |
| 3 | AWS 云架构师 | Skill | 是 | MIT | ✅ |
| 4 | 业务增长技能包 | Expert-Team | 是 | MIT | ✅ |
| 5 | 高管智囊团（虚拟董事会） | Expert-Team | 是 | MIT | ✅ |
| 6 | 代码转产品需求助手 | Skill | 是 | MIT | ✅ |
| 7 | 数据质量审计助手 | Skill | 是 | MIT | ✅ |
| 8 | 创始人陪练 | Expert | 是 | MIT | ✅ |
| 9 | 全栈工程师 | Skill | 是 | MIT | ✅ |
| 10 | Google 办公套件自动化 | Skill | 是 | MIT | ✅ |
| 11 | 产品技能集 | Skill集合 | 是 | MIT | ✅ |

> 全部仍为 **Candidate**。License=MIT 清晰，但未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。

---

## 17. 本轮增量（2026-08-19 持续扫描第二批 · MCP 聚合站 + K-Dense 个体）

> 来源：MCP 聚合站发现的开源 MCP 服务器（markitdown / scrapling / figma-context-mcp）+ K-Dense-AI/scientific-agent-skills 个体技能（MIT 仓库级）。以下 7 条均为 High 优先级 + License 清晰（MIT / BSD-3），按 SOP §2 补中文商品卡。全部仍为 **Candidate**，未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。

---

## 17.1 文档转 Markdown 助手（MarkItDown）

- **中文名称**：文档转 Markdown 助手
- **一句话简介**：把各种办公文档和文件一键转成干净的 Markdown，方便后续阅读和让 AI 处理。
- **详细介绍**：一个轻量的文档转换助手，能把 PDF、Word、PPT、Excel、图片（含 OCR）、音频、网页、CSV/JSON/XML、邮件、甚至 YouTube 链接等内容，统一转成结构清晰的 Markdown 文本。转换时保留标题、列表、表格和链接等结构，主要面向文本分析与大模型处理，而不是追求像人读那样的高保真排版。员工做资料清洗、知识入库或让 AI 读文档前，可以先用它规整格式。
- **能力分类**：文档 / 数据
- **擅长什么**：多格式文档解析、结构保留、Markdown 规整
- **适合做什么**：资料入库前的格式统一、让 AI 读取非文本文件、文档预处理
- **典型使用场景**：员工拿到一堆 PDF 和 Word 报告，让助手统一转成 Markdown 后再做摘要或检索。
- **需要的工具 / 连接**：Python 运行环境（pip 安装）；可选 OCR / 云解析插件
- **来源**：Microsoft（开源）
- **安全 / 权限提示**：本地运行、不联网；读取的文档可能含敏感信息，建议在隔离环境处理，避免外发。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: markitdown (microsoft/markitdown)
- Original Description: Python tool for converting files and office documents (PDF/PPTX/DOCX/XLSX/images/audio/HTML/CSV/JSON/XML/Outlook/YouTube) to Markdown for LLM pipelines; includes markitdown-mcp subpackage.
- Source URL: https://github.com/microsoft/markitdown
- Version/Digest: snapshot 2026-08-19（建议固定 commit digest）
- License: MIT
- Original Metadata: type=Tool/Connector(MCP); category=document-conversion; deps=Python; mcp=markitdown-mcp

</details>

---

## 17.2 自适应网页抓取助手（Scrapling）

- **中文名称**：自适应网页抓取助手
- **一句话简介**：让 AI 自动抓取网页、绕过反爬并抽出想要的数据。
- **详细介绍**：一个自适应网页抓取框架，内置 MCP 服务器，专门配合 AI 做网页数据抽取。它会从网站变化中学习、自动重新定位页面元素；开箱即用绕过 Cloudflare 等反爬机制；支持并发爬取、多会话、自动代理轮换与暂停恢复。员工需要从网页批量取数、做竞品监控或资料采集时，可以让它把目标内容抓出来再交给 AI 处理。
- **能力分类**：网页抓取 / 数据
- **擅长什么**：网页抽取、反爬绕过、结构化数据抓取、大规模爬取
- **适合做什么**：公开网页数据采集、竞品页面监控、资料批量获取
- **典型使用场景**：员工要定期抓取一批公开页面做价格或内容对比，让助手自动抽取关键字段。
- **需要的工具 / 连接**：Python 运行环境（`pip install "scrapling[ai]"`）；目标网站可访问
- **来源**：D4Vinci（开源）
- **安全 / 权限提示**：抓取行为须遵守目标站点 robots.txt 与相关法律法规；仅用于合规的公开数据采集，注意频率与隐私边界。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: Scrapling (D4Vinci/Scrapling)
- Original Description: Adaptive web scraping framework with built-in MCP server for AI-assisted scraping and data extraction; bypasses anti-bot, auto-relocates elements, concurrent crawl, proxy rotation.
- Source URL: https://github.com/D4Vinci/Scrapling
- Version/Digest: snapshot 2026-08-19（建议固定 commit digest）
- License: BSD-3-Clause
- Original Metadata: type=Connector(MCP)/Tool; category=web-scraping; deps=Python; mcp=scrapling[ai]

</details>

---

## 17.3 Figma 设计上下文助手（figma-context-mcp）

- **中文名称**：Figma 设计上下文助手
- **一句话简介**：把 Figma 设计稿的布局信息直接喂给编程助手，照着稿子把页面做出来。
- **详细介绍**：一个开源 MCP 服务器，连接 Figma 后，会把设计文件的布局、样式等数据做简化与转译，再交给 Cursor 等编程助手，让 AI 更准确地把设计实现成代码（减少靠截图猜的误差）。它是官方 Figma 连接器的开源替代方案，员工在写前端页面时可以直接贴 Figma 链接让助手照着实现。
- **能力分类**：设计 / 前端
- **擅长什么**：Figma 设计稿解析、设计上下文注入、设计转代码
- **适合做什么**：按设计稿写前端代码、设计还原、UI 实现
- **典型使用场景**：设计师交付 Figma 文件，员工让编程助手基于简化后的设计数据直接生成首版页面。
- **需要的工具 / 连接**：需 Figma API 个人访问令牌（用户自有）；支持 MCP 的编程助手
- **来源**：GLips（开源）
- **安全 / 权限提示**：需用户提供 Figma 访问令牌；请用最小权限令牌并妥善保管，不写入代码库；仅用于读取指定设计文件。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: figma-context-mcp (GLips/figma-context-mcp, Framelink MCP for Figma)
- Original Description: MCP server providing simplified Figma layout/style data to coding agents (Cursor etc.) for one-shot design implementation; open-source alternative to official figma-mcp.
- Source URL: https://github.com/GLips/figma-context-mcp
- Version/Digest: snapshot 2026-08-19（建议固定 commit digest）
- License: MIT
- Original Metadata: type=Connector(MCP); category=design/frontend; deps=Figma API token, MCP client

</details>

---

## 17.4 科学写作助手（K-Dense scientific-writing）

- **中文名称**：科学写作助手
- **一句话简介**：帮你写有证据、可追溯的科研论文和报告。
- **详细介绍**：一个面向科研写作的助手，强调证据可追溯——论文或报告里的引用与数据都能回扣到来源，减少凭空编造。员工做研究报告、技术文档或论文草稿时，可以用它把实验与分析结果组织成结构清晰、可核查的文稿。
- **能力分类**：科研 / 写作
- **擅长什么**：科研写作、引用管理、证据可追溯、报告结构化
- **适合做什么**：论文/报告起草、技术文档撰写、成果整理
- **典型使用场景**：员工完成一轮实验，让助手基于数据与文献产出带引用的初稿。
- **需要的工具 / 连接**：Claude 类模型；可选科学数据库
- **来源**：K-Dense-AI（开源集合）
- **安全 / 权限提示**：写作内容须由作者核对原始数据与引用；不替代同行评审，重要结论需人工复核。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: scientific-writing (K-Dense-AI/scientific-agent-skills)
- Original Description: Evidence-traceable scientific writing (papers/reports) with citable, data-backed provenance.
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-19（仓库级 MIT；单技能 SKILL.md 许可逐条复核）
- License: MIT（仓库级；单技能复核）
- Original Metadata: type=Skill; category=research/writing; deps=Claude

</details>

---

## 17.5 科学数据库检索助手（K-Dense database-lookup）

- **中文名称**：科学数据库检索助手
- **一句话简介**：用一句话查遍几十个科学数据库，把专业数据找出来。
- **详细介绍**：一个统一检索助手，可以用自然语言查询 78+ 个科学数据库（如 PubChem、ChEMBL、UniProt、ClinicalTrials 等），覆盖化学、生物、临床、文献等多个领域。员工做科研或查证时，不必逐个登录不同库，直接描述需求就能拿到结构化结果。
- **能力分类**：科研 / 数据
- **擅长什么**：跨库统一检索、专业数据查询、结构化返回
- **适合做什么**：科研查证、数据收集、文献/化合物/基因检索
- **典型使用场景**：员工要查某个化合物的性质与文献，让助手一次性跨库汇总。
- **需要的工具 / 连接**：Claude 类模型；联网访问各科学数据库
- **来源**：K-Dense-AI（开源集合）
- **安全 / 权限提示**：依赖外部数据库可用性；返回数据须核对原始来源，关键决策结合权威出处。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: database-lookup (K-Dense-AI/scientific-agent-skills)
- Original Description: Unified natural-language lookup across 78+ scientific databases (PubChem/ChEMBL/UniProt/ClinicalTrials etc.).
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-19（仓库级 MIT；单技能复核）
- License: MIT（仓库级；单技能复核）
- Original Metadata: type=Skill; category=research/data; deps=Claude + scientific DBs

</details>

---

## 17.6 文献综述助手（K-Dense literature-review）

- **中文名称**：文献综述助手
- **一句话简介**：自动聚合多篇文献，帮你写出结构化的文献综述。
- **详细介绍**：一个文献综述助手，能聚合 PubMed、PMC、arXiv 等来源的论文，按主题梳理研究脉络、归纳共识与争议，生成结构化的综述初稿。员工做课题调研或写论文背景时，可以先让它把一片领域的已有工作整理清楚。
- **能力分类**：科研 / 文献
- **擅长什么**：文献聚合、研究脉络梳理、综述撰写
- **适合做什么**：课题调研、论文背景、技术现状梳理
- **典型使用场景**：员工要进入一个新研究方向，让助手先产出该领域的文献综述框架。
- **需要的工具 / 连接**：Claude 类模型；联网检索文献库
- **来源**：K-Dense-AI（开源集合）
- **安全 / 权限提示**：综述须核对原始论文与引用；不替代人工文献把关，关键结论以原文为准。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: literature-review (K-Dense-AI/scientific-agent-skills)
- Original Description: Literature review — aggregate PubMed/PMC/arXiv etc. into structured review drafts.
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-19（仓库级 MIT；单技能复核）
- License: MIT（仓库级；单技能复核）
- Original Metadata: type=Skill; category=research/literature; deps=Claude

</details>

---

## 17.7 科学可视化助手（K-Dense scientific-visualization）

- **中文名称**：科学可视化助手
- **一句话简介**：用 matplotlib/seaborn 把科研数据画成规范、好看的科学图。
- **详细介绍**：一个科学绘图助手，基于 matplotlib 与 seaborn 生成科研常用的图表（折线、散点、热图、分布等），遵循学术可视化的规范与配色，帮助员工把分析结果转成可直接放进报告或论文的图。
- **能力分类**：数据 / BI / 科研
- **擅长什么**：科学绘图、图表规范、数据呈现
- **适合做什么**：分析结果可视化、报告配图、科研图表
- **典型使用场景**：员工跑完一轮数据分析，让助手按学术规范生成可发表的图表。
- **需要的工具 / 连接**：Python 运行环境（matplotlib/seaborn）
- **来源**：K-Dense-AI（开源集合）
- **安全 / 权限提示**：图表须与原始数据一致，避免误导性呈现；重要图由作者复核数据源。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: scientific-visualization (K-Dense-AI/scientific-agent-skills)
- Original Description: Scientific plotting/visualization built on matplotlib and seaborn for research-grade figures.
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-19（仓库级 MIT；单技能复核）
- License: MIT（仓库级；单技能复核）
- Original Metadata: type=Skill; category=data/BI/research; deps=Python(matplotlib/seaborn)

</details>

---

## 17.8 本轮增量汇总

| # | 中文名 | 类型 | 外部候选 | License | 中文产品化 |
|---|---|---|---|---|---|
| 1 | 文档转 Markdown 助手 | Tool/Connector(MCP) | 是 | MIT | ✅ |
| 2 | 自适应网页抓取助手 | Connector(MCP) | 是 | BSD-3-Clause | ✅ |
| 3 | Figma 设计上下文助手 | Connector(MCP) | 是 | MIT | ✅ |
| 4 | 科学写作助手 | Skill | 是 | MIT | ✅ |
| 5 | 科学数据库检索助手 | Skill | 是 | MIT | ✅ |
| 6 | 文献综述助手 | Skill | 是 | MIT | ✅ |
| 7 | 科学可视化助手 | Skill | 是 | MIT | ✅ |

> 全部仍为 **Candidate**。License 清晰（MIT / BSD-3），但未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。

---

## 18. 本轮增量（2026-08-31 持续扫描第三批 · MCP 高星生态 + 代码智能专项）

> 来源：MCP 生态高星排行榜 + 代码智能/沙箱/记忆类 MCP 专项核验。以下 4 条均为 High 优先级 + License 清晰（MIT / Apache-2.0），按 SOP §2 补中文商品卡。全部仍为 **Candidate**，未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。
> 本轮另有 `mindsdb`（许可冲突）、`nanobot`、`claude-task-master`、`netdata`、`graphiti` 等 High/Med 条目因 **License=REVIEW** 不满足 SOP §2 门槛，**本轮不产出商品卡**，仅登记于候选包。

---

## 18.1 代码知识图谱助手（codebase-memory-mcp）

- **中文名称**：代码知识图谱助手
- **一句话简介**：把整个代码库整理成一张"关系图"，让员工问一句就知道该改哪儿。
- **详细介绍**：一个代码理解助手，会先把代码库解析成持久化的知识图谱（记录函数、类、调用链、HTTP 路由和跨服务依赖），之后员工可以直接问"谁调用了这个函数""改这里会影响哪些地方"，而不必让 AI 一遍遍翻文件。它支持 158 种编程语言，查询响应在亚毫秒级，据项目方说明可把同类问题的 token 消耗从约 41 万降到约 3 千。以单个可执行文件分发、零依赖，全部处理都在本地完成，代码不会离开本机。
- **能力分类**：研发 / 代码理解
- **擅长什么**：代码结构检索、调用链追踪、改动影响面分析、架构概览
- **适合做什么**：接手陌生代码库、评估改动影响、大型仓库快速定位
- **典型使用场景**：员工要改一个核心函数，先让助手列出所有调用方和受影响的服务。
- **需要的工具 / 连接**：本地代码库；单可执行文件（macOS / Linux / Windows），无需 API 密钥
- **来源**：DeusData（开源）
- **安全 / 权限提示**：全部在本地运行、代码不出本机；但一键安装脚本会修改 AI 工具的配置文件，正式使用前建议先查看脚本或手动配置。当前仍为 0.x 版本（v0.9.0），接口可能变化；厂商标称的性能数据我们尚未独立复现。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: codebase-memory-mcp (DeusData)
- Original Description: High-performance code intelligence MCP server; indexes codebases into a persistent knowledge graph. tree-sitter AST across 158 languages + Hybrid LSP semantic type resolution for 11 languages. 15 MCP tools (index_repository, search_graph, trace_path, query_graph, detect_changes, get_architecture, search_code...). Single static binary, zero dependencies, 100% local.
- Source URL: https://github.com/DeusData/codebase-memory-mcp
- Version/Digest: v0.9.0（2026-07-08）；snapshot 2026-08-31（建议固定 commit digest）
- License: MIT
- Original Metadata: type=Connector(MCP); category=code-intelligence/dev; deps=local codebase; stars≈32k–36.4k（口径不一）; 论文 arXiv:2603.27277; 31 个真实仓库评测 83% 答案质量（厂商标称）

</details>

---

## 18.2 代码语义助手（Serena）

- **中文名称**：代码语义助手
- **一句话简介**：像 IDE 一样按"函数名、类名"理解和改代码，而不是按行号猜。
- **详细介绍**：一个代码读写助手，通过语言服务协议（LSP）在**符号级别**理解和操作代码，支持 40 多种编程语言。员工可以让它查找某个函数在哪里被引用、一次性全局重命名、替换整个函数体，或安全删除带引用检查的符号。它还会把对项目的理解存成可查看的文档，跨会话保留。
- **能力分类**：研发 / 代码编辑
- **擅长什么**：符号级检索、引用查找、全局重命名、安全重构
- **适合做什么**：大型代码库导航、批量重构、精确代码修改
- **典型使用场景**：员工要把一个被广泛调用的函数改名，让助手一次性找出所有引用并同步更新。
- **需要的工具 / 连接**：Python 3.11+ 与 uv；各语言的语言服务器；可选连接 JetBrains IDE 以获得更强的重构能力
- **来源**：Oraios Software（开源）
- **安全 / 权限提示**：**权限很高**——具备本地文件写入和执行终端命令的能力，且默认没有系统级沙箱、也没有密钥检测，等同于把终端交给它。务必只在受信任项目中启用，敏感仓库需先做隔离与人工审查。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: serena (oraios/serena)
- Original Description: A powerful MCP toolkit for coding, providing semantic retrieval and editing capabilities — "the IDE for your agent". LSP-backed symbol-level retrieval/editing/refactoring, 40+ languages, project memory persisted as inspectable markdown, optional JetBrains backend.
- Source URL: https://github.com/oraios/serena
- Version/Digest: v1.5.x；snapshot 2026-08-31
- License: MIT（2025-05-02 由其他许可切换为 MIT）
- Original Metadata: type=Connector(MCP); category=dev/code-intelligence; deps=Python 3.11+ / uv / per-language LSP; stars≈24.8k–26.3k; privilege=High（文件写 + shell 执行，无默认沙箱、无密钥检测）

</details>

---

## 18.3 MCP 服务开发框架（FastMCP）

- **中文名称**：MCP 服务开发框架
- **一句话简介**：用几行 Python 就能做出一个可被 AI 调用的能力服务。
- **详细介绍**：一个用于构建 MCP 服务的 Python 框架。员工只需写一个普通函数，框架会自动生成参数说明、校验和文档，并处理连接、认证与协议细节，让"把公司内部能力接给 AI"这件事从工程活变成几行代码。它已被广泛采用，其早期版本已并入官方 MCP Python 开发工具包。
- **能力分类**：研发 / 能力集成基建
- **擅长什么**：快速封装内部能力为 AI 可调用服务、自动 schema 生成、连接与认证处理
- **适合做什么**：把内部系统/脚本接给 AI 员工、搭建企业自有能力服务
- **典型使用场景**：员工要把公司内部的报表查询脚本封装成 AI 员工可直接调用的能力。
- **需要的工具 / 连接**：Python 与 uv（`uv pip install fastmcp`）
- **来源**：PrefectHQ（开源）
- **安全 / 权限提示**：框架负责协议层，但工具本身的权限控制、输入校验与访问控制需由使用方在应用层实现；对外暴露前请自行做鉴权。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: fastmcp (PrefectHQ/fastmcp，原 jlowin/fastmcp)
- Original Description: The fast, Pythonic way to build MCP servers and clients. Decorator-based; auto-generates schema/validation/docs; three pillars: Servers / Clients / Apps. FastMCP 1.0 incorporated into the official MCP Python SDK in 2024.
- Source URL: https://github.com/PrefectHQ/fastmcp
- Version/Digest: v3.4.x；snapshot 2026-08-31
- License: Apache-2.0
- Original Metadata: type=Tool（框架）; category=infra/mcp-framework; deps=Python + uv; stars≈25.5k–27.2k

</details>

---

## 18.4 桌面操作智能体（UI-TARS / Agent TARS）

- **中文名称**：桌面操作智能体
- **一句话简介**：像人一样"看屏幕"来操作电脑，能处理没有接口的老软件。
- **详细介绍**：一套开源的多模态智能体工具，包含两部分：一是桌面应用，能直接看屏幕截图、理解界面内容，再用鼠标键盘完成操作——不依赖程序接口或网页结构，因此连没有开放接口的老软件也能操作；二是开发者用的命令行/网页版本，可以把浏览器、终端和各类工具（通过 MCP）串成完整流程。
- **能力分类**：自动化 / 多模态
- **擅长什么**：视觉理解界面、模拟鼠标键盘操作、跨软件流程自动化
- **适合做什么**：无接口软件的自动化、跨应用数据搬运、界面操作类重复工作
- **典型使用场景**：员工需要每天从一套没有接口的内部系统里导出数据再录入另一套，让智能体按界面操作完成。
- **需要的工具 / 连接**：需视觉语言模型（可自建或用云端接口）；命令行版需 Node 22+；支持 macOS 与 Windows
- **来源**：ByteDance（开源）
- **安全 / 权限提示**：**权限很高**——能控制鼠标、键盘和浏览器。务必限定可操作范围，删除、提交、付款、发帖等不可逆操作前必须人工确认；不要远程控制入口暴露到公网，凭据与本地数据分开管理。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: UI-TARS-desktop / Agent TARS (bytedance/UI-TARS-desktop)
- Original Description: Open-source multimodal AI agent stack. UI-TARS Desktop = vision-native GUI agent (screenshots → VLM → mouse/keyboard actions, no OCR/DOM dependency), cross-platform. Agent TARS = CLI/Web UI general multimodal agent stack (GUI agent + browser + terminal), MCP-based kernel, can mount MCP servers.
- Source URL: https://github.com/bytedance/UI-TARS-desktop
- Version/Digest: Desktop v0.2.x / Agent TARS CLI v0.3.x；snapshot 2026-08-31
- License: Apache-2.0
- Original Metadata: type=Tool; category=automation/multimodal-GUI-agent; deps=VLM (HuggingFace 或火山引擎) + Node ≥22; stars≈29.5k–34k; 论文 arXiv:2501.12326

</details>

---

## 18.5 本轮增量汇总

| # | 中文名 | 类型 | 外部候选 | License | 安全标记 | 中文产品化 |
|---|---|---|---|---|---|---|
| 1 | 代码知识图谱助手 | Connector(MCP) | 是 | MIT | — | ✅ |
| 2 | 代码语义助手 | Connector(MCP) | 是 | MIT | SECURITY REVIEW（高权限） | ✅ |
| 3 | MCP 服务开发框架 | Tool | 是 | Apache-2.0 | — | ✅ |
| 4 | 桌面操作智能体 | Tool | 是 | Apache-2.0 | SECURITY REVIEW（高权限） | ✅ |

> 全部仍为 **Candidate**。License 清晰（MIT / Apache-2.0），但未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。
> 本轮 High/Med 但因 License=REVIEW 未产出商品卡：`mindsdb`（许可冲突）、`nanobot`、`claude-task-master`、`netdata`（GPL-3.0）、`graphiti` —— 已在候选包登记，待许可确认后补卡。

---

## 19. 本轮增量（2026-08-31 持续扫描第四批 · License 核验解锁 + K-Dense 科研补卡）

> 组成：① **License 核验解锁**——`mindsdb`、`nanobot` 经抓取 LICENSE 原文确认为 MIT，由 REVIEW 解除阻塞，现补 High 优先级商品卡；② **K-Dense 科研补卡**——`hypothesis-generation` / `experimental-design` / `diffdock` / `pathway-enrichment` 为上批已登记的 MIT 个体（Med 优先级），本轮补齐中文卡。
> ⚠️ 反向结果：`claude-task-master` 经核验为 **MIT + Commons Clause v1.0（禁止商用销售）**，已由 REVIEW 改判 **BLOCKED**，**不产出商品卡、不得进入可招募能力**。

---

## 19.1 数据联邦查询助手（MindsDB）

- **中文名称**：数据联邦查询助手
- **一句话简介**：用一个入口查遍公司所有数据源，不用先把数据搬来搬去。
- **详细介绍**：一个开源的数据查询引擎，能把数据库、数据仓库、SaaS 应用、云存储等两百多种数据源接进来，用统一的 SQL 或大白话直接跨源查询和关联，不需要先做数据搬迁。它还能把 PDF、邮件、工单等散落文档汇成可检索的知识库，并支持按定时任务或数据变更自动更新。自带 MCP 接口，AI 员工可以直接查询。
- **能力分类**：数据 / BI
- **擅长什么**：跨源联合查询、文档知识库检索、定时同步
- **适合做什么**：经营数据统一查询、跨系统报表、文档知识库
- **典型使用场景**：员工想同时看销售系统里的订单和表格里的成本，让助手一次查完并自动关联。
- **需要的工具 / 连接**：各数据源凭据；Docker 自托管
- **来源**：MindsDB（开源）
- **安全 / 权限提示**：会接入多套业务系统的凭据与数据，务必逐个使用最小权限账号、在隔离环境部署；注意数据出域范围与合规要求。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: mindsdb (mindsdb/mindsdb)
- Original Description: Open-source federated query engine giving AI agents a single SQL interface across 200+ live data sources (Postgres/MySQL/MongoDB/Snowflake/BigQuery/ClickHouse/Redshift/Databricks/Salesforce/Shopify/Slack/S3/GCS...). Knowledge Bases with hybrid vector+keyword RAG; Jobs (scheduled) and Triggers (data-change). Built-in MCP server; MySQL API :47335, PostgreSQL API :47336, HTTP editor :47334.
- Source URL: https://github.com/mindsdb/mindsdb
- Version/Digest: snapshot 2026-08-31（建议固定 commit digest）
- License: **MIT**（已抓取 LICENSE 原文核验：MIT License / Copyright (c) 2019 MindsDB, Inc.）。**订正**：此前聚合站标注 NOASSERTION 为误，现已解除 REVIEW。注意部分集成 handler / 企业组件可能另有条款，导入前逐 handler 复核。
- Original Metadata: type=Connector(MCP); category=data/federated-query; deps=各数据源凭据 + Docker; stars≈39.6k

</details>

---

## 19.2 轻量智能体框架（nanobot）

- **中文名称**：轻量智能体框架
- **一句话简介**：一个体积小、能自己部署的 AI 智能体框架，带界面、记忆和工具调用。
- **详细介绍**：一个超轻量、可自行部署的 Python AI 智能体框架，内置网页操作界面、工具调用、记忆能力、MCP 支持和多智能体工作流，也提供自动化与聊天应用能力。适合想快速搭起自己的智能体、又不希望背上沉重框架负担的场景。
- **能力分类**：研发 / Agent 基建
- **擅长什么**：智能体搭建、工具调用、记忆与多智能体编排
- **适合做什么**：自建 AI 助手、自动化流程编排
- **典型使用场景**：员工要搭一个每天定时查数据并发通知的小助手，用框架几步就能跑起来。
- **需要的工具 / 连接**：Python；自托管部署
- **来源**：HKUDS（开源）
- **安全 / 权限提示**：自托管，数据留在自己的机器上；对外暴露前请自行补充鉴权与访问控制。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: nanobot (HKUDS/nanobot)
- Original Description: 超轻量级、开源、可自托管的 Python 个人 AI 智能体框架，具备 WebUI、工具、记忆、MCP、多智能体工作流、自动化及聊天应用功能。
- Source URL: https://github.com/HKUDS/nanobot
- Version/Digest: snapshot 2026-08-31（建议固定 commit digest）
- License: **MIT**（已抓取 LICENSE 原文核验：MIT License / Copyright (c) 2025-present Xubin Ren and the nanobot contributors）。**订正**：此前标 REVIEW（未明示），现已解除。
- Original Metadata: type=Tool; category=agent-framework; deps=Python, self-hosted; stars≈46.9k

</details>

---

## 19.3 科学假设生成助手（hypothesis-generation）

- **中文名称**：科学假设生成助手
- **一句话简介**：帮你提出并打磨"能被实验验证"的科学假设。
- **详细介绍**：一个科研假设助手，能根据已有资料和观察结果生成候选科学假设，并对假设做细化与优化，内置防止假设"过拟合到已有数据"的机制，帮助研究者在动手做实验之前先把假设想清楚、想严谨。
- **能力分类**：科研 / 方法论
- **擅长什么**：候选假设生成、假设细化、防过拟合
- **适合做什么**：开题假设设计、研究方向发散与收敛
- **典型使用场景**：研究者手上有一批初步观测数据，让助手提出几个可验证的候选假设并说明验证路径。
- **需要的工具 / 连接**：Claude 类模型
- **来源**：K-Dense-AI（开源）
- **安全 / 权限提示**：本地模型调用；生成的假设仅供研究参考，须经同行评议与实验验证，不构成科研结论。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: hypothesis-generation (K-Dense-AI/scientific-agent-skills)
- Original Description: 候选科学假设生成与优化（hypogenic / hyporefine / arbor 防过拟合）。
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-31（建议固定 commit digest）
- License: MIT（仓库级；单技能 SKILL.md 另有许可则需逐条复核）
- Original Metadata: type=Skill; category=research/methodology; deps=Claude; priority=Med（补卡，非 High）

</details>

---

## 19.4 实验设计助手（experimental-design）

- **中文名称**：实验设计助手
- **一句话简介**：帮你在动手前，把实验方案设计得站得住脚。
- **详细介绍**：一个实验设计助手，按实验设计（DOE）方法帮助规划实验方案，包括样本量估算与统计功效分析，让实验在开工前就具备足够的检出能力，避免做完才发现样本量不够或分组不合理。
- **能力分类**：科研 / 方法论
- **擅长什么**：DOE 实验设计、样本量估算、统计功效规划
- **适合做什么**：实验方案设计、样本量论证、分组方案
- **典型使用场景**：研究者准备开展一组对照实验，让助手先算清需要多少样本才具有统计意义。
- **需要的工具 / 连接**：Python
- **来源**：K-Dense-AI（开源）
- **安全 / 权限提示**：本地计算；涉及人体或动物实验的方案必须通过伦理审查，本工具输出不能替代伦理审查结论。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: experimental-design (K-Dense-AI/scientific-agent-skills)
- Original Description: 实验设计（DOE, experimental-design），样本量与统计功效规划。
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-31
- License: MIT（仓库级）
- Original Metadata: type=Skill; category=research/methodology; deps=Python; priority=Med（补卡，非 High）

</details>

---

## 19.5 分子对接助手（diffdock）

- **中文名称**：分子对接助手
- **一句话简介**：预测小分子会以什么姿态结合到靶点蛋白上。
- **详细介绍**：一个分子对接助手，基于 DiffDock 方法预测小分子与蛋白结合时的空间构象（pose），常用于药物发现早期的虚拟筛选与结合模式分析，帮助研究者在湿实验前先做一轮计算筛选。
- **能力分类**：药物发现 / 科研
- **擅长什么**：分子对接、结合构象预测、虚拟筛选
- **适合做什么**：候选化合物的结合模式初判、早期筛选
- **典型使用场景**：研究者拿到一个候选化合物，让助手预测它与目标蛋白的结合姿态。
- **需要的工具 / 连接**：Python + 机器学习运行环境
- **来源**：K-Dense-AI（开源）
- **安全 / 权限提示**：计算密集型任务；预测结果仅供研究参考，必须经实验验证，**不构成任何药物或医疗结论**。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: diffdock (K-Dense-AI/scientific-agent-skills)
- Original Description: 分子对接 pose 预测（diffdock）。
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-31
- License: MIT（仓库级）
- Original Metadata: type=Skill; category=drug-discovery; deps=Python + ML; priority=Med（补卡，非 High）

</details>

---

## 19.6 功能富集分析助手（pathway-enrichment）

- **中文名称**：功能富集分析助手
- **一句话简介**：从一长串基因列表里，找出真正相关的生物学通路。
- **详细介绍**：一个生物信息分析助手，对差异基因等基因列表做功能富集分析，覆盖 GO、KEGG、Reactome 等常用通路数据库，帮助研究者从成百上千个基因中定位到真正富集的生物学功能与信号通路，并给出可读的解释。
- **能力分类**：生物信息 / 科研
- **擅长什么**：GO / KEGG / Reactome 富集分析、通路解读
- **适合做什么**：差异基因功能注释、通路富集分析
- **典型使用场景**：研究者做完差异表达分析，让助手做富集分析并解释显著通路的含义。
- **需要的工具 / 连接**：Python
- **来源**：K-Dense-AI（开源）
- **安全 / 权限提示**：本地计算；结果需结合实验与领域知识解读，**不构成医学结论**。

<details><summary>Source Truth（内部，不展示给用户）</summary>

- Original Name: pathway-enrichment (K-Dense-AI/scientific-agent-skills)
- Original Description: 功能富集分析（GO / KEGG / Reactome 等，pathway-enrichment）。
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills
- Version/Digest: snapshot 2026-08-31
- License: MIT（仓库级）
- Original Metadata: type=Skill; category=bioinformatics; deps=Python; priority=Med（补卡，非 High）

</details>

---

## 19.7 本轮增量汇总

| # | 中文名 | 类型 | 外部候选 | License | 优先级 | 中文产品化 |
|---|---|---|---|---|---|---|
| 1 | 数据联邦查询助手 | Connector(MCP) | 是 | MIT（本轮核验解锁） | High | ✅ |
| 2 | 轻量智能体框架 | Tool | 是 | MIT（本轮核验解锁） | High | ✅ |
| 3 | 科学假设生成助手 | Skill | 是 | MIT（仓库级） | Med（补卡） | ✅ |
| 4 | 实验设计助手 | Skill | 是 | MIT（仓库级） | Med（补卡） | ✅ |
| 5 | 分子对接助手 | Skill | 是 | MIT（仓库级） | Med（补卡） | ✅ |
| 6 | 功能富集分析助手 | Skill | 是 | MIT（仓库级） | Med（补卡） | ✅ |

> 全部仍为 **Candidate**。License 清晰（MIT），但未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。
> **本轮反向处置**：`claude-task-master` 经 LICENSE 原文核验为 **MIT + Commons Clause v1.0**，禁止商用销售，已改判 **BLOCKED**，不产出商品卡、不得进入可招募能力。`graphiti` 核验为 Apache-2.0（解除 REVIEW），但优先级 Med 且 LOW CURRENT，本轮不产出卡。
