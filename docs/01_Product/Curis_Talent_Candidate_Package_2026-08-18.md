# Curis 人才与能力候选包 · 2026-08-18（情报专项 · 候选扩充）

Status: Candidate（非 CURIS_READY）  
角色：人才与能力情报负责人 — 生产线最前端（发现 → 调研 → 整理 → 提供可导入候选）  
交付对象：Codex 能力专项（负责真实能力绑定 / 任务验证 / Evidence / CURIS_READY 晋级）  
原则：不新建第二套 Registry、Candidate Queue 或能力真源；本包仅作为现有生产线的新增候选输入。

> ⚠️ 本包内所有条目均为 **Candidate**，未经 Curis 真实 Skill/Tool 绑定、运行验证与 Evidence 的，一律不得升级为 CURIS_READY 或“可招募”。标记说明见文末。

---

## 0. 本轮汇总指标（最终报告口径）

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 52 |
| 新发现资源（原始，含跨类重复） | ~265 |
| 去重后候选数 | ~250 |
| Expert / Expert-Team 候选 | ~45 |
| Skill 资源 | ~120（含集合：alirezarezvani 362、K-Dense 135、ClawHub 多、openai/anthropics 官方集合） |
| MCP / Connector（含聚合中枢） | ~55 |
| Tool / Capability Provider | ~45 |
| License 硬 BLOCKED（非商用限制） | 2 |
| License REVIEW（未明示/需逐项目复核） | ~60 |
| Security Review（高权限/数据出域/敏感域） | ~25 |
| LOW CURRENT PRIORITY（暂无使用场景仍收录） | ~30 |

分类覆盖（均已有真实来源）：设计 ✓ / 产品 ✓ / 数据·BI ✓ / 研究 ✓ / Code Review·QA ✓ / 增长·营销 ✓ / 金融·财务 ✓ / 法律 ✓ / 科研·科学 ✓ / 教育 ✓ / 医疗 ✓ / 房地产 ✓ / 制造·供应链 ✓ / 咨询·行业研究 ✓。

---

## 1. 新增扫描来源（52，均为本轮真实拉取/检索）

官方与开源仓库（深度枚举）：anthropics/skills、anthropics/knowledge-work-plugins、openai/skills、obra/superpowers、modelcontextprotocol/servers、openclaw/clawhub、huggingface/skills、K-Dense-AI/scientific-agent-skills、vercel-labs/agent-skills、alirezarezvani/claude-skills、TrailOfBits(security skills)、msitarzewski/agency-agents、AI-Employer/ai-employees、andrewyng/openworker、OpenBMB/StaffDeck、geekan/MetaGPT、microsoft/autogen、joaomdmoura/crewAI、langchain-ai/langgraph、ai4finance-foundation/finrobot、TauricResearch/TradingAgents、assafelovic/gpt-researcher、HKUDS/DeepTutor、bytedance/deer-flow、phuryn/pm-skills、coreyhaines31/marketingskills、kostja94/marketing-skills、MorvanZhou/zhongjie、YUHAO-corn/manufacturing-agents、novanex-innovations/supply-chain-agent、karpathy/autoresearch、biomni.stanford.edu、superdesigndev/superdesign、evidence-dev/evidence、VoltAgent/awesome-agent-skills、travisvn/awesome-claude-skills、ComposioHQ/awesome-claude-skills、iflytek/iFly-Skills、iflytek/skillhub、bytedance/agentkit-samples、singlegrain/ai-marketing-skills。

平台/聚合/文档：Coze（coze.cn/store、coze.com/store、coze-dev/coze-studio、coze-loop、eino、@coze/api）、Zapier MCP、Composio MCP、Pipedream MCP、n8n、Make、Workato、Relay.app、Dify、Flowise、WorkBuddy 公开目录（workbuddy.cn / codebuddy.cn 文档）、mcp.so / mcpservers.org / awesome-mcp 社区发现源。

> 已存在产线（不重复登记）：jnMetaCode/agency-agents-zh（17 Agent，MIT）、先前 5 MCP、5 Skill、以及已登记的 anthropics/skills/openai/skills/obra/superpowers/modelcontextprotocol/servers/ClawHub。本轮对上述仓库做了**深度逐目录枚举**，新发现条目已在下方标注 `已知库-增量`。

---

## 2. Expert / Expert-Team 候选（~45，按行业）

字段：名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| knowledge-work-plugins | Expert-Team | 多岗位(11) | Anthropic | https://github.com/anthropics/knowledge-work-plugins | 11 岗位插件(销售/法务/财务/数据/客服/产品/市场/企业搜索/生物研究/生产力/插件管理) | Claude + Slack/Notion/HubSpot/Snowflake 等连接器 | source-available(REVIEW) | REVIEW | High |
| agency-agents (EN) | Expert-Team | 跨域 | msitarzewski | https://github.com/msitarzewski/agency-agents | agency-agents-zh 的英文同源版(57K★) | Claude/Cursor/OpenClaw | MIT | 已知库-增量(英文版) | High |
| ai-employees | Expert-Team | 跨域(9部门55员工) | AI-Employer | https://github.com/AI-Employer/ai-employees | 55 个 AI 员工配置(内容/研发等) | Claude/ChatGPT/Dify | REVIEW | REVIEW | Med |
| openworker | Expert/Team | 通用岗位 | andrewyng | https://github.com/andrewyng/openworker | 25+ 连接器与预设角色(销售/行政/市场/运维) | 本地桌面 Agent + aisuite 多模型 | MIT | 新增 | High |
| StaffDeck | Expert-Team | 企业数字员工 | OpenBMB | https://github.com/OpenBMB/StaffDeck | 5 数字员工(财务报销/法务/人事/IT/行政) | 本地部署 | REVIEW | REVIEW | High |
| MetaGPT | Expert-Team/Tool | 软件工程 | geekan | https://github.com/geekan/MetaGPT | 多 Agent 模拟软件公司(PM/架构/工程/QA) | LLM + Python | MIT | 新增 | High |
| finrobot | Expert-Team | 金融 | AI4Finance | https://github.com/ai4finance-foundation/finrobot | 8 专业金融 Agent(投研/估值/风险) | OpenAI + FMP API | Apache-2.0 | 新增 | High |
| TradingAgents | Expert-Team | 金融交易 | TauricResearch | https://github.com/TauricResearch/TradingAgents | 多 Agent 交易(基本面/情绪/新闻/技术+辩论+风控) | OpenAI/DeepSeek/Claude + AlphaVantage/FRED | REVIEW | REVIEW | High |
| investagent | Expert | 投研(A股) | tohnee | https://github.com/tohnee/investagent | 5 套研究框架的 AI 投研 | LLM + 多数据源 | REVIEW | REVIEW | Med |
| finance_analysis_agent | Expert | 金融(中文A股) | closure-guo | https://github.com/closure-guo/finance_analysis_agent | A股财务分析(8节点/20指标, Word/PPT导出) | DeepSeek + AKShare | MIT | 新增 | Med |
| gpt-researcher | Expert/Tool | 研究 | assafelovic | https://github.com/assafelovic/gpt-researcher | 自主深度研究(planner+并行crawler+publisher, 带引用) | 任意 LLM + Tavily 等 | Apache-2.0 | 已知库-增量 | High |
| DeepTutor | Expert-Team | 教育 | HKUDS | https://github.com/HKUDS/DeepTutor | 个性化辅导(三层记忆+解题/出题/研究) | 多 LLM/GraphRAG | Apache-2.0 | 新增 | High |
| langchain-healthcare-tools | Expert/Tool | 医疗 | Jojobeans1981 | https://github.com/Jojobeans1981/langchain-healthcare-tools | 用药安全/FDA召回/临床决策(5层验证) | Groq + RxNorm/FDA | MIT | 新增 | High |
| OpenHealthAgents | Expert-Team | 医疗市场 | OpenHealthAgents | https://github.com/OpenHealthAgents | 医疗 AI Agent OS(19 仓库) | 多模型 | REVIEW | REVIEW | Low |
| legal-contract-agent | Expert/Tool | 法律 | argahv | https://github.com/argahv/legal-contract-agent | 合同审查(MSA提取/风险评分/RAG红线) | OpenAI + pgvector | REVIEW | REVIEW | Med |
| contract-copilot.skill | Expert/Skill | 法律(中文) | cat-xierluo | https://github.com/cat-xierluo/contract-copilot.skill | 合同起草与审查(三层分析+审查意见书) | Claude/Cursor | CC BY-NC 4.0 | **BLOCKED**(非商用) | Med |
| real-estate-agent | Expert-Team | 房地产 | neoxu999 | https://github.com/neoxu999/real-estate-agent | 8 子 Agent 房产助手(搜索/贷款/计算/RAG) | OpenAI + FAISS + CrewAI | REVIEW | REVIEW/LowCurrent | Med |
| realtor-ai | Expert | 房地产(英文) | saminkhan1 | https://github.com/saminkhan1/realtor-ai | LangGraph 房产 Agent(线索/搜索/日历/语音) | LLM + Calendar + Retell | GPL-3.0 | REVIEW(强 copyleft) | Low |
| manufacturing-agents | Expert-Team | 制造/供应链 | YUHAO-corn | https://github.com/YUHAO-corn/manufacturing-agents | 智能补货多 Agent(需求预测/成本/风控) | LLM + 多源 | Apache-2.0 | 新增 | Med |
| supply-chain-agent | Tool/Expert | 供应链 | novanex | https://github.com/novanex-innovations/supply-chain-agent | 库存监控与补货 Agent | OpenAI Agent SDK | MIT | 新增 | Med |
| autoresearch | Tool/Expert | 科研(ML) | Karpathy | https://github.com/karpathy/autoresearch | 单 GPU 自主科研(改代码/调参/跑实验) | 单 GPU + 训练代码 | MIT | 新增 | High |
| Biomni | Expert-Team | 科研(生物医学) | Stanford | https://biomni.stanford.edu | 通用生物医学 Agent(150工具/59库) | Claude/GPT/Gemini | Apache-2.0 | 新增 | High |
| pm-skills | Expert | 产品 | phuryn | https://github.com/phuryn/pm-skills | 68 个 PM 方法论技能(PRD/路线图/访谈) | LLM(Cursor/Claude) | MIT | 新增 | High |
| marketingskills (coreyhaines31) | Expert | 增长/营销 | coreyhaines31 | https://github.com/coreyhaines31/marketingskills | 50+ 营销技能(CRO/文案/SEO/付费) | LLM | REVIEW | REVIEW | High |
| marketing-skills (kostja94) | Expert | 增长/营销 | kostja94 | https://github.com/kostja94/marketing-skills | 160+ 营销技能(SEO/内容/付费/渠道) | LLM | REVIEW | REVIEW | Med |
| 中介哥 zhongjie | Expert | 房地产 | MorvanZhou | https://github.com/MorvanZhou/zhongjie | AI 买房参谋(需求挖掘/调研/带观点推荐) | LLM | MIT | 新增 | Med |
| deer-flow | Expert-Team | 研究 | bytedance | https://github.com/bytedance/deer-flow | 长程 SuperAgent(研究/编码/创作, 子Agent) | 多 LLM | MIT | 新增 | High |
| Market-research-multiagent | Expert-Team | 研究 | kunal-manjunath | https://github.com/kunal-manjunath/Market-research-multiagent | 多 Agent 市场/竞品/财务估算报告 | GPT-4o + SDK | MIT | 新增 | Med |
| SuperDesign | Tool | 设计 | superdesigndev | https://github.com/superdesigndev/superdesign | IDE 内自然语言生成 UI/组件/线框 | 可配置 LLM | AGPLv3 | 新增 | Med |
| alirezarezvani/claude-skills | Expert/Skill集合 | 跨域(18域,102 Agent+362 Skill) | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 生产级技能+Agent(工程/产品/营销/C-level/合规/财务) | Claude/Cursor/Codex/OpenClaw 等13平台 | MIT | 已知库-增量 | High |
| awesome-agent-skills (VoltAgent) | 索引 | 精选(1400+ Skill) | VoltAgent | https://github.com/VoltAgent/awesome-agent-skills | 1400+ 精选 Skill 索引 | 各源仓库 | REVIEW | REVIEW | Med |
| awesome-claude-skills (travisvn) | 索引 | 精选 | travisvn | https://github.com/travisvn/awesome-claude-skills | Claude Skills 精选列表 | 各源仓库 | REVIEW | REVIEW | Med |
| awesome-claude-skills (ComposioHQ) | 索引 | 精选(SaaS集成) | ComposioHQ | https://github.com/ComposioHQ/awesome-claude-skills | 社区 curated Skills 合集 | npx skills add | REVIEW | REVIEW | Med |

> 设计/产品/数据/BI 单角色 Expert：多数以“Skill/工具集”形式存在（见 §3、§4、§5 的 v0、Framer、Evidence、Metabase、MetAgent、web-design-guidelines 等），不重复登记为 Expert。

---

## 3. Skill 资源（~120，集合+典型个体；Expert/Skill 分离）

字段同 §2。集合级条目代表其仓库内全部技能，Codex 导入时按目录逐条 License 复核。

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| anthropics/skills（全集） | Skill集合 | Office/开发/创意 | Anthropic | https://github.com/anthropics/skills | pdf/docx/pptx/xlsx/frontend-design/webapp-testing/mcp-builder/skill-creator 等 18+ | Claude + 脚本 | source-available(REVIEW) | 已知库-增量 | High |
| anthropics knowledge-work-plugins(skills) | Skill集合 | 多岗位 | Anthropic | https://github.com/anthropics/knowledge-work-plugins | sales/legal/finance/data/customer-support/product-management/marketing/enterprise-search/bio-research/productivity | Claude + 连接器 | source-available(REVIEW) | 已知库-增量 | High |
| openai/skills（全集） | Skill集合 | 开发/部署/安全/音频 | OpenAI | https://github.com/openai/skills | playwright/figma*/netlify/vercel/render/cloudflare-deploy/notion-*/linear/sentry/security-*/speech/transcribe/jupyter/imagegen 等 | Codex + 各 API | 每 skill LICENSE.txt(REVIEW) | 已知库-增量 | High |
| openai/skills（官方全集） | Skill集合 | — | OpenAI | https://github.com/openai/skills | 同上 | — | REVIEW | 已知库-增量 | High |
| obra/superpowers（全集） | Skill集合 | 工程/调试/评审 | obra | https://github.com/obra/superpowers | brainstorming/writing-plans/systematic-debugging/TDD/receiving-code-review/executing-plans/verification-before-completion 等 20+ | Claude Code | repo LICENSE(REVIEW) | 已知库-增量 | High |
| huggingface/skills | Skill集合 | ML/科学 | HF | https://github.com/huggingface/skills | hf-gradio/hf-datasets/hf-papers/hf-llm-trainer/hf-spaces/hf-best | Python + HF API | MIT | 已知库-增量 | Med |
| K-Dense scientific-agent-skills | Skill集合 | 科研(135) | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | scanpy/rdkit/paper-lookup/scientific-visualization/database-lookup/scientific-writing/diffdock 等 | Claude + 科学 DB | repo LICENSE(REVIEW) | 已知库-增量 | High |
| vercel-labs/agent-skills | Skill集合 | 前端/部署/安全 | Vercel | https://github.com/vercel-labs/agent-skills | web-design-guidelines/react-best-practices/vercel-deploy/writing-guidelines/react-native/vercel-optimize | Claude + Vercel | MIT | 已知库-增量 | High |
| alirezarezvani/claude-skills(362) | Skill集合 | 跨域(18) | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 362 生产级 skill(代码审查/UX/安全/CFO/产品/营销/GDPR…) | Claude 等13平台 | MIT | 已知库-增量 | High |
| Trail of Bits skills | Skill集合 | 安全 | TrailOfBits | https://github.com/trailofbits | building-secure-contracts/static-analysis/semgrep-rule-creator/differential-review/variant-analysis | Slither/CodeQL/Semgrep | 各 skill REVIEW | REVIEW/Security | High |
| ClawHub skills（多 slug） | Skill集合 | 办公/开发/安全/中文 | OpenClaw | https://github.com/openclaw/clawhub | excel-wizard/doc-pro/code-reviewer/web-search/github-bot/notion-sync/email-agent/image-gen/feishu-bitable/nda-generator/trivy/obsidian 等 | OpenClaw | 各 skill 自定(REVIEW) | REVIEW | High |
| iFly-Skills | Skill集合 | 语音/OCR(中文) | 科大讯飞 | https://github.com/iflytek/iFly-Skills | TTS/转写/PDF图片OCR/发票OCR/翻译/校对 | 讯飞开放平台 | REVIEW | REVIEW | Med |
| agentkit-samples | Skill集合 | 中文/通用 | 字节 | https://github.com/bytedance/agentkit-samples | 火山引擎 API 示例(联网搜索/TTS/图像理解) | 火山引擎 Key | REVIEW | REVIEW | Med |
| ai-marketing-skills | Skill集合 | 增长/营销 | Single Grain | https://github.com/dikoweii/ai-marketing-skills | 增长引擎/销售管线/内容/外联/SEO/CFO | Claude + API | MIT | 已知库-增量 | High |
| pdf / docx / pptx / xlsx | Skill(个体) | Office | anthropics | https://github.com/anthropics/skills/tree/main/skills/pdf 等 | 文档生成/提取/表单 | Claude + 脚本 | source-available | 已知库-增量 | High |
| frontend-design / web-artifacts-builder | Skill(个体) | 前端/Web | anthropics | https://github.com/anthropics/skills/tree/main/skills/frontend-design | UI/UX 设计与 React 工件 | Claude | source-available | 已知库-增量 | High |
| webapp-testing / playwright(openai) | Skill(个体) | 测试 | anthropics/openai | https://github.com/openai/skills/tree/main/skills/.curated/playwright | 浏览器 E2E/回归 | Playwright | LICENSE.txt | 已知库-增量 | High |
| security-best-practices / threat-model | Skill(个体) | 安全 | openai | https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices | 安全编码/威胁建模 | Claude | LICENSE.txt | 已知库-增量 | High |
| figma* (openai) | Skill(个体) | 设计 | openai | https://github.com/openai/skills/tree/main/skills/.curated/figma* | 设计稿↔代码/生成 | Figma API | — | 已知库-增量 | High |
| notion-* / linear / sentry (openai) | Skill(个体) | 知识/项目管理 | openai | https://github.com/openai/skills/tree/main/skills/.curated | 知识沉淀/工单/监控 | Notion/Linear/Sentry API | LICENSE.txt | 已知库-增量 | Med |
| web-design-guidelines (vercel) | Skill(个体) | 设计 | vercel-labs | https://github.com/vercel-labs/agent-skills | 100+ 可访问性/性能/UX 规则审计 | Claude | MIT | 已知库-增量 | High |
| react-best-practices (vercel) | Skill(个体) | 编程 | vercel-labs | https://github.com/vercel-labs/agent-skills | React/Next.js 性能规则 | Claude | MIT | 已知库-增量 | High |
| financial-analyst / deep-research (alirezarezvani) | Skill(个体) | 财务/研究 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 财务分析/SaaS指标/深度研究 | Claude | MIT | 已知库-增量 | High |
| scanpy / rdkit / paper-lookup (K-Dense) | Skill(个体) | 科研 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 生信/化学/文献检索 | Python/科学 DB | repo LICENSE | 已知库-增量 | Med |
| code-reviewer / web-search / doc-pro (ClawHub) | Skill(个体) | 开发/搜索/办公 | OpenClaw | https://github.com/openclaw/clawhub | 自动 Review/联网搜索/长文档解析 | OpenClaw | per-skill REVIEW | REVIEW | High |
| nda-generator / privacy-policy (ClawHub) | Skill(个体) | 法律 | OpenClaw | https://github.com/openclaw/clawhub | NDA/隐私政策生成 | OpenClaw | per-skill REVIEW | REVIEW | Med |
| feishu-bitable / feishu-calendar (ClawHub) | Skill(个体) | 中文协作 | OpenClaw | https://github.com/openclaw/clawhub | 飞书多维表格/日历 | 飞书 API | per-skill REVIEW | REVIEW | Med |

---

## 4. MCP / Connector（~55；含聚合中枢）

字段同 §2。官方参考服务器已在产线登记（标记 已知库-增量）；以下补充社区与平台级。

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| github-mcp-server | MCP | 代码托管 | GitHub | https://github.com/github/github-mcp-server | 72+ 工具(Repo/Issue/Actions) | GitHub PAT/OAuth | MIT | 已知库-增量 | High |
| playwright-mcp | MCP | 浏览器自动化 | Microsoft | https://github.com/microsoft/playwright-mcp | 真实浏览器 E2E | Node/Chromium | MIT | 新增 | High |
| mcp-k8s | MCP | 容器编排 | strowk | https://github.com/strowk/mcp-k8s | K8s Pod/日志/扩缩容 | kubeconfig | 开源 | 新增 | Med |
| AWS MCP | MCP | 云 | AWS Labs | https://github.com/awslabs/mcp | EC2/S3/Lambda 等 | AWS 凭证 | Apache-2.0 | 新增 | High |
| Azure MCP | MCP | 云 | Microsoft | https://github.com/Azure/azure-mcp | 15+ Azure 连接器 | Azure 凭证 | MIT | 新增 | Med |
| cloudflare-mcp | MCP | 边缘云 | Cloudflare | https://github.com/cloudflare/mcp-server-cloudflare | Workers/KV/R2/DNS | CF Token | Apache-2.0 | 新增 | Med |
| grafana-mcp | MCP | 可观测 | Grafana | https://github.com/grafana/mcp-grafana | 仪表盘/数据源/告警 | Grafana Token | AGPL-3.0 | 新增 | Med |
| context7 | MCP | 文档检索 | Upstash | https://github.com/upstash/context7-mcp | 最新库文档注入上下文 | 远程 | MIT | 新增 | High |
| postman-mcp | MCP | API测试 | Postman | https://github.com/postmanlabs/postman-mcp-server | 运行/测试 API 集合 | Postman Key | Apache-2.0 | 新增 | Med |
| mongodb-mcp | MCP | NoSQL | MongoDB | https://github.com/mongodb-js/mongodb-mcp-server | 查询/聚合/Atlas | Mongo 串 | Apache-2.0 | 新增 | High |
| elasticsearch-mcp | MCP | 搜索/分析 | Elastic | https://github.com/elastic/mcp-server-elasticsearch | 自然语言检索 | ES 地址 | MIT | 新增 | High |
| redis-mcp | MCP | 缓存/KV | Redis | https://github.com/redis/mcp-redis | 管理 Redis 数据 | Redis URL | MIT | 新增 | Med |
| clickhouse-mcp | MCP | OLAP | 社区 | https://github.com/ClickHouse/mcp-server-clickhouse | 列式数仓查询 | CH 串 | Apache-2.0 | REVIEW | Med |
| bigquery-mcp | MCP | 数仓 | LucasHild | https://github.com/LucasHild/mcp-server-bigquery | BigQuery 查询 | GCP 凭证 | MIT | 新增 | High |
| snowflake-mcp | MCP | 数仓 | datawiz168 | https://github.com/datawiz168/mcp-snowflake-service | 自然语言查 Snowflake | Snowflake 凭证 | 开源 | 新增 | Med |
| supabase-mcp | MCP | 后端/DB | Supabase | https://github.com/supabase-community/supabase-mcp | DB/Auth/存储 | Supabase Key | MIT | 新增 | High |
| airtable-mcp | MCP | 表格DB | domdomegg | https://github.com/domdomegg/airtable-mcp-server | 读写 Airtable | Airtable Token | MIT | 新增 | Med |
| exa-mcp | MCP | AI搜索 | Exa | https://github.com/exa-labs/exa-mcp-server | AI 原生网页搜索 | EXA_API_KEY | MIT | 新增 | High |
| tavily-mcp | MCP | AI搜索 | Tavily | https://github.com/tavily-ai/tavily-mcp | 搜索/提取/抓取 | TAVILY_API_KEY | MIT | 新增 | High |
| firecrawl-mcp | MCP | 网页抓取 | Firecrawl | https://github.com/mendableai/firecrawl-mcp-server | 整站爬取/JS渲染 | FIRECRAWL_API_KEY | MIT | 新增 | High |
| perplexity-mcp | MCP | AI问答 | Perplexity | https://github.com/ppl-ai/modelcontextprotocol | 实时引用问答 | PERPLEXITY_API_KEY | MIT | 新增 | High |
| mcp-omnisearch | MCP | 聚合搜索 | wombatlabs | https://github.com/wombatlabs/mcp-omnisearch | 统一 Tavily/Brave/Perplexity/Exa | 多 Key | MIT | 新增 | Med |
| notion-mcp | MCP | 知识管理 | Notion | https://github.com/makenotion/notion-mcp-server | 读写页面/数据库 | Notion Token | MIT | 新增 | High |
| atlassian-mcp | MCP | 项目管理 | Atlassian | https://github.com/atlassian/mcp-server-atlassian | Jira/Confluence | Atlassian OAuth | MIT | 新增 | High |
| linear-mcp | MCP | 项目管理 | jerhadf | https://github.com/jerhadf/linear-mcp-server | Issue/项目 | Linear Token | MIT | 新增 | Med |
| figma-mcp | MCP | 设计 | Figma | https://mcp.figma.com | 设计层读取 | Figma OAuth | 专有 SaaS | 新增 | High |
| hubspot-mcp | MCP | CRM | HubSpot | https://developer.hubspot.com/mcp | CRM 对象读写 | HubSpot OAuth | 专有 SaaS | 新增 | Med |
| salesforce-mcp | MCP | CRM | Salesforce | https://github.com/salesforcecli/mcp | 60+ 工具/SOQL | Salesforce 凭证 | BSD-3 | 新增 | Med |
| gmail-mcp | MCP | 邮件 | nicobailon | https://github.com/nicobailon/gmail-mcp | 读写/搜索邮件 | Google OAuth | MIT | 新增 | High |
| google-calendar-mcp | MCP | 日历 | nspady | https://github.com/nspady/google-calendar-mcp | 日历事件 | Google OAuth | MIT | 新增 | Med |
| zapier-mcp | Connector | 集成中枢 | Zapier | https://mcp.zapier.com | 8000+ 应用统一暴露 | Zapier 账号 | 专有 SaaS | 新增 | High |
| huggingface-mcp | MCP | AI模型 | HF | https://huggingface.co/mcp | 搜模型/数据集/推理 | HF Token | 专有 SaaS | 新增 | Med |
| elevenlabs-mcp | MCP | 语音 | ElevenLabs | https://github.com/elevenlabs/elevenlabs-mcp | TTS | ElevenLabs Key | 开源 | 新增 | Low |
| stripe-mcp | MCP | 支付 | Stripe | https://github.com/stripe/agent-toolkit | 支付/退款/订阅 | Stripe Key | Apache-2.0 | 新增 | High |
| alpha-vantage-mcp | MCP | 金融行情 | Alpha Vantage | https://mcp.alphavantage.co/ | 股票/外汇/加密/商品 | AV API Key | 专有 SaaS | 新增 | High |
| shopify-mcp | MCP | 电商 | pashpashpash | https://github.com/pashpashpash/shopify-mcp-server | 商品/客户/订单 | Shopify Token | MIT | 新增 | Med |
| twilio-mcp | MCP | 通信 | Twilio | https://twilioalpha.com/mcp | 短信/语音 | Twilio 凭证 | 专有 SaaS | 新增 | Med |
| pubmed-mcp | MCP | 生物医学 | cyanheads | https://github.com/cyanheads/pubmed-mcp-server | NCBI 文献检索 | 无(限流) | MIT | 新增 | Med |
| openalex-paper-search | MCP | 学术 | openags | https://github.com/openags/paper-search-mcp | 20+ 来源文献聚合 | 可选 Key | 开源 | 新增 | High |
| courtlistener-mcp | MCP | 法律 | Free Law Project | https://mcp.courtlistener.com/ | 美国法院意见/PACER | OAuth | 开源 | 新增 | Med |
| wolframalpha-mcp | MCP | 科学计算 | ricocf | https://github.com/ricocf/mcp-wolfram-alpha | 计算/结构化知识 | WOLFRAM_API_KEY | 开源 | REVIEW | Low |
| patsnap-mcp | MCP | 知产 | kunihiros | https://github.com/kunihiros/patsnap-mcp | 专利趋势/竞争 | PatSnap 凭证 | 开源 | REVIEW | Med |
| reddit-research-mcp | MCP | 研究 | king-of-the-grackles | https://github.com/king-of-the-grackles/reddit-research-mcp | Reddit 语义搜索 | MCP | MIT | 新增 | Med |
| Composio MCP | Connector | 聚合(250+工具) | Composio | https://mcp.composio.dev/ | 预建 MCP+统一认证路由 | Composio Key | 专有 SaaS | 新增 | High |
| Pipedream MCP | Connector | 聚合(3000+ API) | Pipedream | https://mcp.pipedream.com | 每 App 独立 MCP 端点 | Pipedream 账号 | 专有 SaaS | 新增 | High |
| 官方参考服务器(增量确认) | MCP | 基础 | 官方 | https://github.com/modelcontextprotocol/servers | filesystem/git/github/postgres/sqlite/slack/gdrive/memory/fetch/sequentialthinking/puppeteer/time/google-maps/brave-search/sentry/gitlab/docker | 各原生依赖 | MIT | 已知库-增量 | High |

---

## 5. Tool / Capability Provider（~45；框架/平台/行业工具）

字段同 §2。

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| AutoGen | Tool | 多Agent框架 | Microsoft | https://github.com/microsoft/autogen | 多可对话 Agent 协作 | LLM + 工具 | MIT/Apache | 新增 | High |
| crewAI | Tool | 角色编排 | joaomdmoura | https://github.com/joaomdmoura/crewAI | Agent+Task+Crew 角色扮演 | LLM + 云服务 | MIT | 新增 | High |
| LangGraph | Tool | 图工作流 | LangChain | https://github.com/langchain-ai/langgraph | 状态图编排多 Agent | LLM + LangChain | MIT | 新增 | High |
| Coze Studio | Tool | Agent平台 | coze-dev | https://github.com/coze-dev/coze-studio | 可视化 Bot/插件/工作流 | 模型 API Key | Apache-2.0 | 已知库-增量 | High |
| Coze Loop | Tool | Prompt运维 | coze-dev | https://github.com/coze-dev/coze-loop | Prompt 评估/观测 | Coze Studio | Apache-2.0 | 新增 | High |
| Eino | Tool | 编排框架 | cloudwego | https://github.com/cloudwego/eino | 统一 AI 应用编排(Go) | Go 生态 | Apache-2.0 | 新增 | High |
| @coze/api | Tool(SDK) | API客户端 | Coze | https://www.npmjs.com/package/@coze/api | 把 Coze Bot 接入自有产品 | Node/浏览器 | MIT(REVIEW) | 新增 | High |
| n8n | Tool | 工作流自动化 | n8n-io | https://github.com/n8n-io/n8n | 400+ 集成/MCP/代码 | 自托管 Docker | Sustainable Use(REVIEW) | REVIEW | High |
| Make | Tool | 工作流自动化 | Make | https://www.make.com | 1500+ 应用集成/AI 模块 | Make 账号 | 专有 SaaS | 新增 | Med |
| Workato | Tool | 企业 iPaaS | Workato | https://www.workato.com | 1200+ 连接器/AI Connectors | Workato 账号 | 专有商业 | 新增 | Med |
| Relay.app | Tool | AI工作流 | Relay.app | https://www.tryrelay.app | 自建 MCP/远程 MCP/人审 | Relay 账号 | 专有 SaaS | 新增 | Med |
| Dify | Tool | LLM应用/Agent | langgenius | https://github.com/langgenius/dify | 工作流+RAG+Agent/MCP | 自托管 Docker | Dify OSL(改 Apache) | 新增 | High |
| Flowise | Tool | LLM工作流 | FlowiseAI | https://github.com/FlowiseAI/Flowise | 拖拽 LangChain/MCP | 自托管 Node | Apache-2.0 | 新增 | High |
| v0 (Vercel) | Tool | 设计/前端 | Vercel | https://v0.app | React/Next UI 生成 | Vercel AI Gateway | 专有 SaaS | 新增 | High |
| Framer AI | Tool | 设计 | Framer | https://www.framer.com | 画布内 AI 生成网站 | 多模型 | 专有 SaaS | 新增 | Med |
| Uizard | Tool | 设计 | Uizard | https://uizard.io | 文本/草图生成原型 | 专有 | 专有 SaaS | 新增 | Low |
| Relume | Tool | 设计 | Relume | https://www.relume.io | sitemap/线框/设计系统 | 专有 | 专有 SaaS | 新增 | Low |
| Galileo→Stitch | Tool | 设计 | Google | https://stitch.withgoogle.com | 文本/图生成高保真 UI | Claude/Gemini | 专有 SaaS | 新增 | Med |
| Evidence | Tool | 数据/BI | evidence-dev | https://github.com/evidence-dev/evidence | 代码化 BI(SQL+MD→网站) | Node/SQL | MIT | 新增 | High |
| Metabase | Tool | 数据/BI | Metabase | https://www.metabase.com | 开源 BI+自然语言 SQL+MCP | 自带 LLM | AGPL(开源版) | 新增 | High |
| MetAgent | Tool | 数据/BI | MetAgent | https://metagent.app | 连 Metabase 自然语言分析 | OpenAI/Metabase | 专有 SaaS | 新增 | Med |
| Qodo PR-Agent | Tool | Code Review/QA | qodo-ai | https://github.com/qodo-ai/pr-agent | 开源 PR 审查(/review/improve) | LiteLLM | MIT | 新增 | High |
| CodeRabbit | Tool | Code Review/QA | CodeRabbit | https://www.coderabbit.ai | 逐行 AI PR 审查+修复 | 模型无关 | 专有 SaaS | 新增 | High |
| Greptile | Tool | Code Review/QA | Greptile | https://www.greptile.com | 全代码库感知审查 | 模型无关 | 专有 SaaS | 新增 | High |
| Sourcery | Tool | Code Review/QA | Sourcery | https://sourcery.ai | AI 重构/安全扫描 | 自带 LLM | 专有 SaaS | 新增 | Med |
| Tembo Agent | Tool | Code Review/QA | Tembo | https://www.tembo.io | 跨仓库审查+自动修复 PR | 多 Agent | 专有 SaaS | 新增 | Med |
| sec-edgar-agentkit | Tool | 金融/财务 | stefanoamorelli | https://github.com/stefanoamorelli/sec-edgar-agentkit | SEC EDGAR 访问与分析 | LLM/EDGAR | AGPL-3.0 | 新增 | High |
| finsight | Tool | 金融/财务 | agxp | https://github.com/agxp/finsight | SEC EDGAR RAG Agent | Claude/pgvector | REVIEW | REVIEW | Med |
| legal-document-assistant-agent | Tool | 法律 | gsaini | https://github.com/gsaini/legal-document-assistant-agent | Agentic RAG 合同审查 | Ollama/ChromaDB | 开源(未明示) | REVIEW/Security | High |
| ai-legal-assistant | Tool | 法律 | markiskorova | https://github.com/markiskorova/ai-legal-assistant | 可解释合同分析 | OpenAI/Django | REVIEW | REVIEW | Med |
| Multi-Agent-Study-Assistant | Tool | 教育 | A-R007 | https://github.com/A-R007/Multi-Agent-Study-Assistant | 6 Agent 学习平台 | OpenAI/Groq | REVIEW | REVIEW | Med |
| IntellicQ | Tool | 教育 | KHUSHI0809 | https://github.com/KHUSHI0809/IntellicQ | 自适应微学习 | GPT/LangChain | REVIEW | REVIEW | Low |
| mAIstro | Tool | 医疗 | eltzanis | https://github.com/eltzanis/mAIstro | 医学 AI 模型开发框架 | 开源/闭源 LLM | REVIEW(论文) | REVIEW/Security | Med |
| AI-Agents-for-Medical-(diagnostics) | Tool | 医疗 | ahmadvh | https://github.com/ahmadvh/AI-Agents-for-Medical-Diagnostics | 多专科诊断 Agent | GPT-5 | REVIEW | REVIEW/Security | Low |
| Claude-Ally-Health | Tool | 医疗 | huifer | https://github.com/huifer/Claude-Ally-Health | 症状/用药/病历+MDT | Claude | REVIEW | REVIEW/Security | Med |
| property-pulse | Tool | 房地产 | lannonthecannon | https://github.com/lannonthecannon/property-pulse | 房产 NL→SQL 问答 | OpenAI | MIT | 新增 | Med |
| ai-real-estate-assistant | Tool | 房地产 | AleksNeStu | https://github.com/AleksNeStu/ai-real-estate-assistant | RAG 房产助手(估值/搜索) | 多 LLM/ChromaDB | MIT | 新增 | Med |
| supply-chain-optimizer-agent | Tool | 制造/供应链 | jitu028 | https://github.com/jitu028/supply-chain-optimizer-agent | Neo4j+模拟中断优化 | Gemini/Neo4j | REVIEW | REVIEW | Med |
| ARES-Supply-Chain | Tool | 制造/供应链 | Zaid2044 | https://github.com/Zaid2044/ARES-Supply-Chain-Optimization | RL/数字孪生优化 | Scikit/Flask | MIT | 新增 | Med |
| SupplyChainAssistant | Tool | 制造/供应链 | aashika-j18 | https://github.com/aashika-j18/SupplyChainAssistant | 采购谈判+需求预测 | Gemini/Prophet | REVIEW | REVIEW | Low |
| iflytek/skillhub | Tool | Skill注册中心 | 科大讯飞 | https://github.com/iflytek/skillhub | 企业级 Skill 私有商店 | 私有部署 | REVIEW | REVIEW | Low |
| ClawHub registry | Tool | Skill注册中心 | OpenClaw | https://github.com/openclaw/clawhub | 公开 Skill/Plugin 注册表 | OpenClaw | per-skill REVIEW | REVIEW | High |

---

## 6. 标记登记（BLOCKED / REVIEW / Security / Low Current）

### 6.1 License 硬 BLOCKED（非商用限制，Curis 商用不可直接收录）
- `cat-xierluo/contract-copilot.skill` — CC BY-NC 4.0（商用需单独授权）→ BLOCKED，仅个人/评估用。
- `ai-law-shield` — CC BY-NC 4.0 → BLOCKED。

### 6.2 License REVIEW（未明示/需逐文件复核，~60）
含：所有标注 “未明示—REVIEW” 的社区仓库（ai-employees、StaffDeck、TradingAgents、investagent、legal-contract-agent、real-estate-agent、realtor-ai[GPL-3.0]、OpenHealthAgents、argahv、ai-legal-assistant、finsight、mAIstro、各医疗/教育/供应链 REVIEW 项）；anthropics/skills 与 knowledge-work-plugins（source-available，非标准 OSI）；openai/skills 每 skill LICENSE.txt；obra/superpowers、K-Dense、Trail of Bits、ClawHub（per-skill）、iFly-Skills、agentkit-samples、singlegrain、travisvn/ComposioHQ 索引、n8n（Sustainable Use 非 OSI）、@coze/api（REVIEW）、workato/make/relay（专有）。导入前必须逐仓库/逐 skill 固定 LICENSE 与 NOTICE。

### 6.3 Security Review（高权限/数据出域/敏感域，~25）
- 连接器/聚合：api-gateway(ClawHub)、agent-browser(ClawHub)、imap-smtp-email(ClawHub)、coding-agent(ClawHub)、Zapier/Composio/Pipedream MCP（集中凭证）、WorkBuddy/Coze 连接器（数据出域）。
- 安全工具：healthcheck、trivy(ClawHub)、Trail of Bits 系列（静态分析/合约审计）、security-best-practices/threat-model。
- 敏感域：legal-document-assistant-agent、ai-legal-assistant、mAIstro、AI-Agents-for-Medical-Diagnostics、Claude-Ally-Health（医疗/法律敏感数据，需沙箱+免责）；financial API-key 类（finrobot、TradingAgents、alpha-vantage、stripe）。
- 处理：进入产线前做 Prompt 注入/凭证/过度承诺扫描；敏感域仅限本地/授权数据，禁止伪造“已验证”。

### 6.4 LOW CURRENT PRIORITY（暂无使用场景仍收录，~30）
房地产(realtor-ai/real-estate-agent/property-pulse/ai-real-estate-assistant/zhongjie)、医疗诊断类(mAIstro/AI-Agents-for-Medical-Diagnostics/Claude-Ally-Health/OpenHealthAgents)、部分供应链长尾(SupplyChainAssistant)、Uizard/Relume(设计低优先)、IntellicQ(教育低优先)、elevenlabs-mcp、wolframalpha-mcp、patsnap-mcp、privacy-policy(ClawHub)、iflytek/skillhub、awesome 索引类。当前 Curis 业务不覆盖，但保留候选以支持“未来任意 Business 可找到现成人才”。

---

## 7. 各专业分类覆盖（本轮新增真实来源）

| 分类 | 覆盖 | 代表候选（真实来源） |
|---|---|---|
| 设计 | ✓ | SuperDesign(AGPL)、v0、Framer、Galileo/Stitch、web-design-guidelines(vercel)、figma* skills、UI设计师(WorkBuddy参考) |
| 产品 | ✓ | pm-skills(MIT,68)、knowledge-work-plugins(product-management)、autogen-prd-generator、AutoPRD |
| 数据/BI | ✓ | Evidence(MIT)、Metabase(AGPL)、MetAgent、bigquery/snowflake/supabase/airtable MCP、data plugin(anthropics) |
| 研究 | ✓ | gpt-researcher(Apache)、deer-flow(MIT)、Market-research-multiagent、openalex-paper-search、reddit-research-mcp、deep-research skill |
| Code Review/QA | ✓ | Qodo PR-Agent(MIT)、CodeRabbit、Greptile、Sourcery、Tembo、code-reviewer(ClawHub)、requesting/receiving-code-review(obra) |
| 增长/营销 | ✓ | marketingskills(coreyhaines31/kostja94)、ai-marketing-skills(MIT)、knowledge-work-plugins(marketing)、claude-seo |
| 金融/财务 | ✓ | finrobot(Apache)、TradingAgents、investagent、finance_analysis_agent、sec-edgar-agentkit(AGPL)、stripe/alpha-vantage MCP、finance plugin |
| 法律 | ✓ | legal-contract-agent、knowledge-work-plugins(legal)、nda-generator(ClawHub)、courtlistener-mcp、ai-legal-assistant（contract-copilot BLOCKED） |
| 科研/科学 | ✓ | Biomni(Apache)、K-Dense(135)、autoresearch(MIT)、scanpy/rdkit/paper-lookup、hf-papers、pubmed-mcp |
| 教育 | ✓ | DeepTutor(Apache)、Multi-Agent-Study-Assistant、IntellicQ、claude-academy-guide |
| 医疗 | ✓ | langchain-healthcare-tools(MIT)、OpenHealthAgents、mAIstro、Claude-Ally-Health（均 Security Review） |
| 房地产 | ✓ | real-estate-agent、realtor-ai(GPL)、property-pulse、ai-real-estate-assistant、zhongjie(MIT)（Low Current） |
| 制造/供应链 | ✓ | manufacturing-agents(Apache)、supply-chain-agent(MIT)、ARES、supply-chain-optimizer-agent |
| 咨询/行业研究 | ✓ | gpt-researcher、deer-flow、Market-research-multiagent、knowledge-work-plugins(enterprise-search) |

---

## 8. 推荐优先导入候选（供 Codex 能力专项）

按“许可证清晰 + 可安装/接入 + 高覆盖价值”排序，建议首批进入 CanonicalAgentSpec / SkillTemplate / Capability 适配：

1. `anthropics/knowledge-work-plugins`（11 岗位，覆盖产品/市场/法务/财务/数据/客服/生物研究）— High
2. `msitarzewski/agency-agents`（agency-agents-zh 英文同源，MIT，扩语言覆盖）— High
3. `andrewyng/openworker`（MIT，25+ 连接器+预设角色）— High
4. `OpenBMB/StaffDeck`（企业数字员工：财务/法务/人事/IT/行政）— High
5. `ai4finance-foundation/finrobot`（Apache-2.0，金融多 Agent）— High
6. `assafelovic/gpt-researcher`（Apache-2.0，深度研究）— High
7. `HKUDS/DeepTutor`（Apache-2.0，教育）— High
8. `Biomni`（Apache-2.0，生物医学科研）— High
9. `phuryn/pm-skills`（MIT，68 PM 技能）— High
10. `coreyhaines31/marketingskills`（增长/营销）— High
11. `YUHAO-corn/manufacturing-agents`（Apache-2.0，制造/供应链）— Med
12. `anthropics/skills` 官方集合（Office/前端/测试/mcp-builder）— High
13. `openai/skills` 官方集合（部署/安全/设计/知识）— High
14. `obra/superpowers`（工程工作流）— High
15. `huggingface/skills`（MIT，ML/科学）— Med
16. `K-Dense-AI/scientific-agent-skills`（科研 135）— High（科研业务）
17. `vercel-labs/agent-skills`（MIT，前端/设计/安全）— High
18. `alirezarezvani/claude-skills`（MIT，362 skill/102 agent 跨域）— High
19. 官方 MCP 服务器（filesystem/github/postgres/brave-search/fetch/sequentialthinking 等）— High
20. `Composio MCP` / `Zapier MCP`（聚合连接器中枢，单点接数千应用）— High（Security Review）
21. `Evidence`（MIT，代码化 BI）— High（数据/BI 业务）
22. `Qodo PR-Agent`（MIT，代码评审）— High（Code Review/QA）
23. `v0` / `SuperDesign`（设计生成）— High/Med（设计业务）

> 上述均仍为 Candidate。Codex 专项须完成：真实 Skill/Tool 绑定 → Curis 工作任务执行 → Evidence → 方能晋级 CURIS_READY 与招募。

---

## 9. 交接说明（给 Codex 能力专项）

- 本包为**候选输入**，不替代任何现有 Registry / Candidate Queue / 能力真源。
- 导入流程沿用现有 `CanonicalAgentSpec` + `AgencyMarkdownAdapter` / `SkillRepoAdapter` / `MCPManifestAdapter`，先 draft，再许可证/安全门禁。
- 每个集合型来源（alirezarezvani 362、K-Dense 135、ClawHub 多、anthropics/openai/obra）必须**逐条**固定 commit/digest、LICENSE、NOTICE 后再入 CanonicalAgentSpec；不整仓复制。
- 所有 REVIEW 项在许可证/安全未确认前保持 BLOCKED/Candidate，不得宣称可招募或已验证。
- 严禁将“发现候选”冒充 `CURIS_READY`；CURIS_READY 必须经真实能力绑定、任务执行与 Evidence 验证。
- 来源去重：已存在产线的 agency-agents-zh(17)、先前 5 MCP、5 Skill、已登记仓库不在本包重复登记，仅做增量枚举。

---

## 增量扫描（2026-08-18 周常自动化 · 情报专项）

> 本轮来源：① WorkBuddy 公开目录（专家中心 + SkillHub 技能市场 + 连接器市场）；② Coze/扣子商店（coze.cn 原生插件 + 用户发布技能）。两源均为真实拉取（WebSearch/WebFetch，来源见各条 Source URL）。
> 去重结论：下列 26 条均为本包既有 ~250 候选之外的新条目；中文连接器（腾讯文档/会议/QQ邮箱/企业微信/微信/乐享/ima/COS）、Coze 原生插件、质量工程技能全集均为首次登记，无与既有条目同名重复。
> License 说明：两个来源均为专有 SaaS 市场 / 用户发布非标准许可，统一标记 REVIEW；无明确非商用（BLOCKED=0）。因 License 均不清晰，本轮不新增中文产品化商品卡（SOP §2 要求 License 清晰）。

### 增量扫描汇总

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 2 |
| 新发现资源（原始，含市场聚合计数） | ~60 |
| 去重后候选数 | 26 |
| Expert / Expert-Team | 2 |
| Skill | 11 |
| Connector(MCP) | 12 |
| Tool / Marketplace | 1 |
| License 硬 BLOCKED | 0 |
| License REVIEW | 26（全部） |
| Security Review | 12（所有连接器类） |
| LOW CURRENT PRIORITY | 6 |

### A. 来源一：WorkBuddy 公开目录（专家中心 + SkillHub + 连接器市场）

真实来源：https://www.workbuddy.cn/ ；专家中心说明 https://ima.qq.com/wiki/?shareId=f7171eb3d6de287e3a2d12bc01080b1b42bc551db4ae4f8d96886df5e33d05bc ；SkillHub 数据 https://developer.cloud.tencent.com/article/2704994 。

#### A.1 Expert / Expert-Team

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| WB 专家中心 | Expert-Team/Marketplace | 跨域(12行业,140+专家) | WorkBuddy | https://www.workbuddy.cn/ | 140+ 领域专家 Agent（设计/工程技术/市场营销/付费媒体/销售/产品/项目管理/质量测试/运营支持/专业服务/游戏开发/空间计算），支持专家团多角色协作 | WorkBuddy 平台账号；企业版可自建专家 | 专有 SaaS（REVIEW） | REVIEW | High |

#### A.2 Skill（SkillHub 及具体技能）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| ppt-master | Skill | 文档/设计 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 一句话生成 PPT，支持图表与动画 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | High |
| summarize | Skill | 内容/研究 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 一键总结网页/PDF/视频内容 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | Med |
| minimax-xlsx | Skill | 数据 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 智能处理 Excel，不漏隐藏行与跨 Sheet 数据 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | High |
| 会议纪要 | Skill | 办公 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 录音转文字 + 结构化整理会议纪要 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | High |
| 周报生成 | Skill | 办公 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 从工作记录生成结构化周报 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | Med |
| 代码审查(WB) | Skill | 研发/QA | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 自动 Review 代码质量，给出问题建议 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | High |
| 去AI味 | Skill | 内容 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 去除文本 AI 写作痕迹 | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW / LOW CURRENT PRIORITY | Med |
| 小红书内容管理 | Skill | 营销 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 小红书内容发布与管理 | WorkBuddy 平台 + 小红书账号 | 专有市场（REVIEW） | REVIEW | Med |
| 浏览器自动化 | Skill | 自动化 | WorkBuddy SkillHub | https://www.workbuddy.cn/ | 浏览器自动化操作（类 RPA） | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | Med |

#### A.3 Connector(MCP) / Tool

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| 腾讯文档连接器 | Connector | 办公/文档 | WorkBuddy | https://www.workbuddy.cn/ | AI 直接读写云端 Word/Excel/PPT | 腾讯文档 OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW（数据出域至腾讯云） | High |
| 腾讯会议连接器 | Connector | 会议 | WorkBuddy | https://www.workbuddy.cn/ | 提取会议纪要 | 腾讯会议 OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW | Med |
| QQ邮箱连接器 | Connector | 邮件 | WorkBuddy | https://www.workbuddy.cn/ | 读邮件/整理收件箱/起草回复 | QQ 邮箱 OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW（邮件数据） | Med |
| 企业微信连接器 | Connector | 协作 | WorkBuddy | https://www.workbuddy.cn/ | 发消息/接收消息，内部助手 | 企业微信 OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW | Med |
| 微信连接器 | Connector | 协作 | WorkBuddy | https://www.workbuddy.cn/ | 微信发指令/接收 | 微信授权 | 专有 SaaS（REVIEW） | SECURITY REVIEW | Med |
| 腾讯乐享连接器 | Connector | 知识库 | WorkBuddy | https://www.workbuddy.cn/ | 查公司知识库 | 乐享 OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW | Med |
| ima 笔记连接器 | Connector | 笔记 | WorkBuddy | https://www.workbuddy.cn/ | 读写 ima 笔记 | ima 授权 | 专有 SaaS（REVIEW） | SECURITY REVIEW / LOW CURRENT PRIORITY | Low |
| 腾讯云 COS 连接器 | Connector | 存储 | WorkBuddy | https://www.workbuddy.cn/ | 对象存储读写 | 腾讯云密钥 | 专有 SaaS（REVIEW） | SECURITY REVIEW | Med |
| SkillHub 技能市场 | Tool/Marketplace | 技能聚合 | WorkBuddy | https://developer.cloud.tencent.com/article/2704994 | 7 万+ 技能、3000 万+ 下载的技能库（文档/数据/代码/设计） | WorkBuddy 平台 | 专有市场（REVIEW） | REVIEW | Med |

### B. 来源二：Coze/扣子商店（coze.cn 原生插件 + 用户发布技能）

真实来源：https://www.coze.cn/ ；原生插件清单 https://blog.csdn.net/HiWangWenBing/article/details/161985492 ；质量技能全家桶 https://www.qpdca.com/forum.php?mod=viewthread&tid=188912 ；爆款视频转小红书智能体 https://www.coze.cn/store/agent/7493077322770448435 。

#### B.1 Connector(MCP) — 原生插件

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| Coze 原生插件集(coze.cn) | Connector | 多类(搜索/文档/代码/OCR/飞书/内容/办公) | Coze | https://www.coze.cn | 零配置开箱即用插件：联网搜索/文档解析/代码执行/图片OCR/飞书消息·文档·多维表格·审批/文案润色/思维导图/语音合成转写/邮件/天气/时间/计算器/二维码 | Coze 账号；飞书等 OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW（字节云数据出域） | High |
| 抖音运营插件(抖音私信/评论) | Connector | 社媒 | Coze | https://www.coze.cn | 抖音私信接收回复、评论自动互动 | 抖音授权 | 专有 SaaS（REVIEW） | SECURITY REVIEW / LOW CURRENT PRIORITY | Med |
| 豆包多模态插件 | Connector | 多模态 | Coze | https://www.coze.cn | 原生调用豆包画图/语音转写/视频理解 | Coze 账号 | 专有 SaaS（REVIEW） | SECURITY REVIEW / LOW CURRENT PRIORITY | Med |
| Coze.com 原生插件集(海外 SaaS) | Connector | 海外 SaaS 聚合 | Coze | https://www.coze.com | 海外原生插件：Google Search/Web Scraper/Document Parser/Code Interpreter/Image OCR、Gmail/Drive/Discord/Slack/WhatsApp/Twitter/Notion/Zoom/Salesforce/Shopify、DALL·E3/Midjourney/SD/Whisper（与既有 MCP 服务器同能力、不同封装） | Coze 账号；各 SaaS OAuth | 专有 SaaS（REVIEW） | SECURITY REVIEW（重叠-增量） | Med |

#### B.2 Skill / Expert（用户发布，真实公开）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| 质量技能工具全家桶 | Expert-Team/Skill集合 | 质量工程(新领域) | Coze(用户 yueyueyue) | https://www.qpdca.com/forum.php?mod=viewthread&tid=188912 | 24 个质量技能：8D 报告/QCC/质量月报/鱼骨图/柏拉图/SPC 判异(CPK)/MSA/FMEA/PPAP/APQP/QFD/DOE/SWOT/PESTLE/CP 控制计划/PDCA 等 | Coze 平台 | 用户发布（REVIEW，非标准） | REVIEW（新领域：质量工程，既有包未覆盖） | High |
| 爆款视频转小红书文案智能体 | Expert/Skill | 内容/营销 | Coze | https://www.coze.cn/store/agent/7493077322770448435 | 视频/音频转写→改写为小红书风格文案→上传飞书 | Coze 平台 + 飞书 | 用户发布（REVIEW） | REVIEW / LOW CURRENT PRIORITY | Med |
| 电商主图生成工作流 | Skill/Workflow | 电商设计 | Coze(iThinkAi) | https://www.coze.cn | 工作流一键生成无模特电商主图（反推提示词→卖点→生图） | Coze 平台 + 第三方生图插件 | 用户发布（REVIEW） | REVIEW / LOW CURRENT PRIORITY | Med |

### 增量 License / Security / LowCurrent 标记汇总

- **License 硬 BLOCKED**：0。
- **License REVIEW（全部 26 条）**：两源均为专有 SaaS 市场 / 用户发布非标准许可，导入前须逐条确认商业授权与 NOTICE。
- **Security Review（12 条，所有连接器类）**：腾讯文档/腾讯会议/QQ邮箱/企业微信/微信/腾讯乐享/ima/COS（WB）+ Coze 原生插件集/抖音/豆包/Coze.com 集。处理：进入产线前做数据出域/凭据/注入扫描；第三方云凭据最小化、不入库。
- **LOW CURRENT PRIORITY（6 条）**：ima 笔记、去AI味、抖音运营、豆包多模态、爆款视频转小红书、电商主图。当前 Curis 业务不覆盖，但保留候选以支持“未来任意 Business 可找到现成人才”。

### 增量后推荐优先导入候选（供 Codex 能力专项）

1. `WB 专家中心`（140+ 专家跨 12 行业，中文市场高覆盖）— High（REVIEW/Security 待确认）
2. `minimax-xlsx`（Excel 智能处理，高频办公）— High
3. `ppt-master`（中文 PPT 生成）— High
4. `会议纪要`（录音→结构化纪要）— High
5. `代码审查(WB)`（代码质量自检）— High
6. `腾讯文档连接器`（读写云端 Office）— High（SECURITY REVIEW）
7. `Coze 原生插件集`（中文生态零配置插件广度）— High（SECURITY REVIEW）
8. `质量技能工具全家桶`（质量工程新领域，24 技能）— High（REVIEW）

> 上述均为 Candidate。License=REVIEW 项在商业授权与逐文件许可确认前保持 BLOCKED/Review，不得宣称可招募或已验证。严禁把“发现候选”冒充 CURIS_READY。

---

## 增量扫描（2026-08-19 周常自动化 · 情报专项）

> 本轮来源：① **alirezarezvani/claude-skills** 个体技能深度枚举（此前仅登记为 362 技能集合 + 1 条个体行；本轮按插件/技能 slug 抽取高价值个体，MIT 清晰，可产品化）；② **OpenClaw ClawHub 实时注册表**（clawhub.ai 在线列表 + 社区目录，抽取既有包未覆盖的真实 slug）。两源均为真实拉取（WebFetch clawhub.ai + WebSearch 社区目录 + GitHub/市场 README），无伪造。
> 去重结论：下列 31 条均为既有 ~250 候选 + 08-18 增量 26 条之外的新条目；alirezarezvani 个体技能避开了已登记的 `financial-analyst / deep-research`；ClawHub 新 slug 避开了已登记的 excel-wizard/doc-pro/code-reviewer/web-search/github-bot/notion-sync/email-agent/image-gen/feishu-bitable/nda-generator/trivy/obsidian 及 §6.3 已点名的 api-gateway/agent-browser/imap-smtp-email/coding-agent。
> License 说明：alirezarezvani 全库 MIT（清晰，可产品化）；ClawHub 为社区每技能许可未明示，统一标记 REVIEW，无明确非商用（BLOCKED=0）。

### 增量扫描汇总

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 2 |
| 新发现资源（原始） | 31 |
| 去重后候选数 | 31 |
| Expert / Expert-Team | 3 |
| Skill | 26 |
| Connector(MCP) | 2 |
| License 硬 BLOCKED | 0 |
| License REVIEW | 16（全部 ClawHub） |
| Security Review | 7（ClawHub 凭据/数据出域/安全类） |
| LOW CURRENT PRIORITY | 5 |

### A. 来源一：alirezarezvani/claude-skills（个体技能深度枚举，MIT）

真实来源：https://github.com/alirezarezvani/claude-skills ；市场清单 https://claudemarketplaces.com/plugins/alirezarezvani-claude-skills 。仓库 LICENSE=MIT（Copyright 2025 Alireza Rezvani）。安装：`/plugin marketplace add alirezarezvani/claude-skills` 或 `npx ai-agent-skills install`，跨 13 个 Agent（Claude Code/Codex/Cursor/Gemini CLI/OpenClaw 等）。

#### A.1 Expert / Expert-Team（MIT，清晰）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| business-growth-skills | Expert-Team | 增长/商业 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 4 角色：客户成功经理/销售工程师/营收运营/合同与提案撰写 | Claude/Cursor 等 13 平台 | MIT | 新增 | High |
| c-level-skills | Expert-Team | 高管顾问 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 虚拟董事会（CEO/CTO/COO/CPO/CMO/CFO/CRO/CISO/CHRO 等 28 个 C 级人格）+ 高管教练/创始人教练/董事会纪要/竞争情报/M&A | Claude 等 13 平台 | MIT | 新增 | High |
| executive-mentor | Expert | 创始人/高管陪练 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 对抗式思考伙伴：压测计划、董事会准备、硬决策、复盘 | Claude 等 13 平台 | MIT | 新增 | High |

#### A.2 Skill（MIT，清晰）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| a11y-audit | Skill | 设计/前端 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | WCAG 2.2 无障碍审计与修复（React/Next/Vue/Angular/Svelte/HTML，20+ 违规类型+对比度检查） | Claude；本地静态扫描 | MIT | 新增 | High |
| agenthub | Skill | 多智能体编排 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 生成 N 个并行子代理竞争优化（代码/文案/研究），DAG 编排+LLM 评审+消息板 | Claude | MIT | 新增 | High |
| aws-architect | Skill | 云架构 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | AWS Serverless 架构设计（IaC 模板/成本优化/CI-CD） | Claude + AWS 凭证 | MIT | 新增 | High |
| code-to-prd | Skill | 产品/研发 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 把任意代码库逆向工程成完整 PRD（前端/后端/全栈） | Claude + 2 Python 脚本 | MIT | 新增 | High |
| data-quality-auditor | Skill | 数据/BI | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 数据集质量审计（完整性/一致性/准确性/有效性；DQS 评分/缺失值/异常值，stdlib-only） | Claude + Python | MIT | 新增 | High |
| fullstack-engineer | Skill | 研发 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 全栈工程（React/Node/数据库/部署） | Claude + Node | MIT | 新增 | High |
| google-workspace-cli | Skill | 办公自动化 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 通过 gws CLI 自动化 Gmail/Drive/Sheets/Calendar/Docs/Chat/Tasks（43 内置配方） | Claude + Google 凭据 | MIT | 新增 | High |
| product-manager | Skill | 产品 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 产品经理工具箱（RICE 评分/客户访谈分析/PRD 生成） | Claude | MIT | 新增 | High |
| product-skills | Skill集合 | 产品 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 14 产品技能：产品策略/敏捷 PO/UX 研究/UI 设计系统/竞品拆解/落地页生成/SaaS 脚手架/产品分析/实验设计/产品发现/路线图/code-to-prd/研究摘要 | Claude | MIT | 新增 | High |
| helm-chart-builder | Skill | 云原生 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | Helm chart 开发（脚手架/values 设计/模板/依赖/K8s 部署策略） | Claude + kubeconfig | MIT | 新增 | Med |
| demo-video | Skill | 多媒体 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | 由截图+场景描述生成演示视频（编排 Playwright+ffmpeg+edge-tts） | Claude + Playwright/ffmpeg | MIT | 新增 | Med |
| docker-development | Skill | 研发/运维 | alirezarezvani | https://github.com/alirezarezvani/claude-skills | Docker 容器开发（Dockerfile 优化/compose/多阶段/安全加固/CI-CD） | Claude + Docker | MIT | 新增 | Med |

### B. 来源二：OpenClaw ClawHub 实时注册表（clawhub.ai + 社区目录）

真实来源：https://clawhub.ai （Trending/Featured 实时列表）；社区目录 https://devpress.csdn.net/xclaw/69b410c654b52172bc6106bc.html 、https://blog.axiaoxin.com/post/openclaw-skills/ 。许可模型：社区每技能许可未明示（REVIEW）；安装 `clawhub install <slug>` 或 `npx clawhub@latest install <slug>`。

#### B.1 Connector（中文协作，凭据/数据出域 → SECURITY REVIEW）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| dingtalk（钉钉集成） | Connector | 中文协作 | OpenClaw ClawHub | https://clawhub.ai | 发消息/建待办/管审批/通知，钉钉办公自动化 | 钉钉授权 | 社区 REVIEW | SECURITY REVIEW（钉钉凭据/数据出域） | High |
| wecom（企业微信集成） | Connector | 中文协作 | OpenClaw ClawHub | https://clawhub.ai | 发消息/建群/管通讯录/通知，企业微信自动化 | 企业微信授权 | 社区 REVIEW | SECURITY REVIEW（企业微信凭据/数据出域） | High |

#### B.2 Skill（ClawHub 真实 slug；社区许可未明示 → REVIEW）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| skill-vetter（技能安全审计） | Skill | 安全 | OpenClaw ClawHub | https://clawhub.ai | 安装其他技能前扫描代码，检测可疑 API 调用/过高权限，生成安全报告 | ClawHub CLI | 社区 REVIEW | SECURITY REVIEW（安全工具，正向外） | High |
| excel-formula-tool（Excel 公式工具·免费版） | Skill | 办公(中文) | OpenClaw ClawHub | https://clawhub.ai/thcjp/skills/excel-formula-tool-free | 生成/诊断 Excel 公式（VLOOKUP/SUMIF/COUNTIF 等），个人日常 | OpenClaw | 社区 REVIEW | REVIEW | High |
| majia-huiyuan（会员运营·马甲实战版） | Skill | 营销分析(中文) | OpenClaw ClawHub | https://clawhub.ai/maojiebc/skills/majia-huiyuan | 会员指标口径/RFM/复购留存流失公式/核销率/客单价/会员分层分群/人群圈选 | OpenClaw | 社区 REVIEW | REVIEW | Med |
| feishu-calendar（飞书日历） | Skill | 中文协作 | OpenClaw ClawHub | https://clawhub.ai | 飞书日历创建/修改/忙闲/参会人/重复日程 | 飞书 API | 社区 REVIEW | SECURITY REVIEW（飞书数据） | Med |
| feishu-create-doc / feishu-update-doc / feishu-fetch-doc（飞书云文档） | Skill | 中文协作 | OpenClaw ClawHub | https://clawhub.ai | 飞书云文档 Markdown 创建/读取/多种模式更新/知识库节点 | 飞书 API | 社区 REVIEW | SECURITY REVIEW（飞书数据） | Med |
| feishu-im-read（飞书 IM 消息读取） | Skill | 中文协作 | OpenClaw ClawHub | https://clawhub.ai | 群/单聊历史消息、话题消息、跨会话搜索、图片文件下载 | 飞书 API | 社区 REVIEW | SECURITY REVIEW（飞书数据） | Med |
| market-research（市场调研） | Skill | 研究 | OpenClaw ClawHub | https://clawhub.ai | 自动化市场调研：采集市场数据/行业趋势/竞品动态，生成结构化报告 | OpenClaw + 联网 | 社区 REVIEW | REVIEW | Med |
| stock-analysis-cellcog（股票分析） | Skill | 金融 | OpenClaw ClawHub | https://clawhub.ai/cellcog/skills/stock-analysis-cellcog | AI 金融分析与股票研究（CellCog 驱动） | OpenClaw + 数据 API | 社区 REVIEW | REVIEW | Med |
| photography-portrait-generator（摄影级人像生图） | Skill | 多模态 | OpenClaw ClawHub | https://clawhub.ai/neuer111/skills/photography-portrait-generator | 顶级摄影指导+跨平台提示词+一键生图（融合三部摄影名著） | OpenClaw + 生图 API | 社区 REVIEW | REVIEW / LOW CURRENT PRIORITY | Med |
| homeassistant-skill（智能家居） | Skill | IoT | OpenClaw ClawHub | https://clawhub.ai/anotb/skills/homeassistant-skill | 通过 REST API 控制 Home Assistant 设备与自动化（25 实体） | Home Assistant | 社区 REVIEW | REVIEW / LOW CURRENT PRIORITY | Low |
| reddit-automation（Reddit 自动化） | Skill | 社媒/研究 | OpenClaw ClawHub | https://clawhub.ai/skills-sh/flowkit-labs/skills/reddit-automation | Reddit 自动发帖/互动/监控 | OpenClaw + Reddit | 社区 REVIEW | REVIEW / LOW CURRENT PRIORITY | Med |
| self-improving-agent（自我进化） | Skill | 元能力 | OpenClaw ClawHub | https://clawhub.ai/pskoett/skills/self-improving-agent | 记录失败与纠正反馈，跨会话持续优化（46万+ 安装量） | OpenClaw | 社区 REVIEW | REVIEW / LOW CURRENT PRIORITY | Med |
| xdrop（文件收发） | Skill | 文件传输 | OpenClaw ClawHub | https://clawhub.ai/xixu-me/skills/xdrop | 通过 Xdrop 发送/获取文件 | OpenClaw + Xdrop | 社区 REVIEW | REVIEW / LOW CURRENT PRIORITY | Med |
| web-content-fetcher（网页/公众号读取） | Skill | 内容采集 | OpenClaw ClawHub | https://clawhub.ai | 读取任意网页（含微信公众号）、付费墙绕过、完整内容提取 | OpenClaw | 社区 REVIEW | SECURITY REVIEW（内容抓取/数据出域） | Med |

### 增量 License / Security / LowCurrent 标记汇总

- **License 硬 BLOCKED**：0。
- **License REVIEW（16 条，全部 ClawHub）**：ClawHub 为社区每技能许可未明示，导入前须逐 slug 确认许可与 NOTICE；alirezarezvani 15 条均为 MIT（清晰，可产品化）。
- **Security Review（7 条）**：dingtalk、wecom、feishu-calendar、feishu-create-doc/feishu-fetch-doc、feishu-im-read、web-content-fetcher（凭据/数据出域至钉钉/企业微信/飞书/外部）；skill-vetter 为安全正向工具（安装前扫描），亦归安全类。处理：进入产线前做凭据最小化/注入/数据出域扫描，凭据不入库。
- **LOW CURRENT PRIORITY（5 条）**：photography-portrait-generator、homeassistant-skill、reddit-automation、self-improving-agent、xdrop。当前 Curis 业务不覆盖，保留候选以支持“未来任意 Business 可找到现成人才”。

### 增量后推荐优先导入候选（供 Codex 能力专项）

1. `c-level-skills`（alirezarezvani，MIT，虚拟董事会 28 C 级人格）— High（License 清晰，可产品化）
2. `business-growth-skills`（alirezarezvani，MIT，4 增长角色）— High
3. `executive-mentor`（alirezarezvani，MIT，创始人陪练）— High
4. `a11y-audit`（alirezarezvani，MIT，无障碍审计）— High
5. `code-to-prd`（alirezarezvani，MIT，代码→PRD）— High
6. `data-quality-auditor`（alirezarezvani，MIT，数据质量审计）— High
7. `product-skills`（alirezarezvani，MIT，14 产品技能）— High
8. `fullstack-engineer` / `google-workspace-cli`（alirezarezvani，MIT）— High
9. `agenthub`（alirezarezvani，MIT，多智能体编排）— High
10. `skill-vetter`（ClawHub，安全扫描，REVIEW）— High（Security Review）
11. `excel-formula-tool` / `majia-huiyuan`（ClawHub 中文办公/营销，REVIEW）— High/Med
12. `dingtalk` / `wecom`（ClawHub 中文协作连接器，REVIEW）— High（SECURITY REVIEW）

> 上述均为 Candidate。alirezarezvani 条目 License=MIT 清晰，但未经 Curis 真实任务验证与 Evidence，仍不得标 CURIS_READY；ClawHub 条目 License=REVIEW 须在逐文件许可确认前保持 BLOCKED/Review。严禁把"发现候选"冒充 CURIS_READY。

---

## 增量扫描（2026-08-19 持续扫描第二批 · MCP 聚合站 + K-Dense 个体）

> 本轮来源：① **MCP 聚合站发现**（mcp.so / mcpservers.org / mcptoplist.com / deepyard.dev / automationswitch 综述，真实拉取，抽取既有包未覆盖的开源 MCP 服务器）；② **K-Dense-AI/scientific-agent-skills 个体技能深度枚举**（此前 08-18 包仅登记集合 + scanpy/rdkit/paper-lookup 三条个体；本轮按 README 真实技能名补登新个体）。两源均为真实拉取（WebSearch + WebFetch GitHub README），无伪造。
>
> ⚠️ **License 修正（重要）**：此前 08-18 候选包将 `K-Dense-AI/scientific-agent-skills` 标为 `repo LICENSE(REVIEW)`。本轮 WebFetch 仓库 LICENSE 文件明确为 **MIT（Copyright © 2026 K-Dense Inc.）**，仓库级 OSI 清晰、可商用。单技能 `SKILL.md` 可能另有许可声明，导入前逐条复核。下面对 K-Dense 个体统一标 `MIT（仓库级；单技能复核）`。
>
> 去重结论：下列 15 条均为既有 ~250 候选 + 08-18 增量 26 + 08-19 增量 31 之外的新条目；MCP 类避开了已登记的 filesystem/github/postgres/playwright/figma-mcp(官方)/context7/tavily/firecrawl/exa/perplexity 等；K-Dense 个体避开了已登记的 scanpy/rdkit/paper-lookup。`n8n-mcp-server(czlonkowski)` 经 WebFetch 返回 404，已剔除、不登记。

### 增量扫描汇总

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 2 |
| 新发现资源（原始，含聚合候选与剔除 404） | ~20 |
| 去重后候选数 | 15 |
| Expert / Expert-Team | 0 |
| Skill | 10（K-Dense 个体） |
| Connector(MCP) | 5 |
| Tool | 0 |
| License 硬 BLOCKED | 0 |
| License REVIEW | 2（chrome-devtools-mcp、trend-radar） |
| Security Review | 1（clinical-decision-support，临床敏感） |
| LOW CURRENT PRIORITY | 1（opentrons） |

### A. 来源一：MCP 聚合站发现的新开源 MCP 服务器

真实来源：https://www.mcpservers.org/ 、https://mcptoplist.com/ 、https://deepyard.dev/best/mcp-servers 、https://automationswitch.com/ai-workflows/where-to-find-mcp-servers-2026 ；各服务器 GitHub README 经 WebFetch 确认。

#### A.1 Connector(MCP) / Tool

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| markitdown（文档转 Markdown） | Connector(MCP)/Tool | 文档转换 | Microsoft | https://github.com/microsoft/markitdown | 把 PDF/PPTX/DOCX/XLSX/图片(EXIF+OCR)/音频/HTML/CSV/JSON/XML/Outlook/YouTube/EPub 等转为 Markdown，供 LLM 与文本流水线消费；含 `markitdown-mcp` 子包可作 MCP 服务器 | `pip install 'markitdown[all]'`；`markitdown-mcp` | MIT（微软 OSS；SPDX 经仓库 LICENSE 确认） | 新增 | High |
| scrapling（自适应网页抓取） | Connector(MCP) | 网页抓取 | D4Vinci | https://github.com/D4Vinci/Scrapling | 自适应网页抓取框架，内置 MCP 服务器做 AI 辅助抓取与数据抽取；自动重定位元素、绕 Cloudflare 反爬、并发爬取、自动代理轮换 | `pip install "scrapling[ai]"` | BSD-3-Clause（OSI 清晰） | 新增 | High |
| figma-context-mcp（Figma 设计上下文） | Connector(MCP) | 设计 | GLips | https://github.com/GLips/figma-context-mcp | 开源 MCP 服务器，把 Figma 文件布局/样式（简化后）喂给 Cursor 等编码代理，一次成型实现设计；为官方 `figma-mcp`（SaaS）的开源替代 | `npx -y figma-developer-mcp --figma-api-key=...` | MIT | 新增 | High |
| chrome-devtools-mcp（Chrome 开发者工具） | Connector(MCP) | 浏览器/调试 | ChromeDevTools | https://github.com/ChromeDevTools/chrome-devtools-mcp | 把 Chrome DevTools 能力（控制台/网络请求/截图/堆快照/性能追踪）暴露给编码代理；支持 Claude/Cursor/Gemini 插件 | npm 包（疑似 `chrome-devtools-mcp`） | REVIEW（LICENSE 未明示；Google 惯例疑 Apache-2.0，需确认） | 新增 | High |
| trend-radar（舆情与热点监控） | Connector(MCP) | 研究/舆情 | sansan0 | https://github.com/sansan0/TrendRadar | AI 舆情与热点监控，聚合多平台热点 + RSS，关键词筛选、AI 简报、情感洞察与趋势预测，支持微信/飞书/钉钉/邮件等推送，可接 MCP 架构 | Docker / 配置文件 | REVIEW（LICENSE 未明示，需确认） | 新增 | Med |

### B. 来源二：K-Dense-AI/scientific-agent-skills 个体技能深度枚举（MIT 修正）

真实来源：https://github.com/K-Dense-AI/scientific-agent-skills （仓库 LICENSE=MIT；163 个 ready-to-use skills，README 逐类点名）。安装：Claude Code + `skill` 机制 / agent-skills 适配。

#### B.1 Skill（MIT 仓库级；单技能 SKILL.md 许可逐条复核）

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| scientific-writing | Skill | 科研/写作 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 证据可追溯的科学写作（论文/报告），引用与数据可回溯 | Claude + 科学 DB | MIT（仓库级；单技能复核） | 新增 | High |
| database-lookup | Skill | 科研/数据 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 统一自然语言检索 78+ 科学数据库（PubChem/ChEMBL/UniProt/ClinicalTrials 等） | Claude + DB | MIT（仓库级） | 新增 | High |
| scientific-visualization | Skill | 数据/BI/科研 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 基于 matplotlib/seaborn 的科学绘图与可视化 | Python | MIT（仓库级） | 新增 | High |
| literature-review | Skill | 科研/文献 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 文献综述：聚合 PubMed/PMC/arXiv 等，生成结构化综述 | Claude | MIT（仓库级） | 新增 | High |
| hypothesis-generation | Skill | 科研/方法论 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 候选科学假设生成与优化（hypogenic/hyporefine/arbor 防过拟合） | Claude | MIT（仓库级） | 新增 | Med |
| experimental-design | Skill | 科研/方法论 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 实验设计（DOE, experimental-design），样本量与统计功效规划 | Python | MIT（仓库级） | 新增 | Med |
| diffdock | Skill | 药物发现 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 分子对接 pose 预测（diffdock） | Python + ML | MIT（仓库级） | 新增 | Med |
| pathway-enrichment | Skill | 生物信息 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 功能富集分析（GO/KEGG/Reactome 等，pathway-enrichment） | Python | MIT（仓库级） | 新增 | Med |
| clinical-decision-support | Skill | 临床/医疗 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 聚合/合成临床决策支持评估（非实时）；涉及临床敏感数据 | Claude | MIT（仓库级） | SECURITY REVIEW（临床敏感数据） | Med |
| opentrons | Skill | 实验室自动化 | K-Dense-AI | https://github.com/K-Dense-AI/scientific-agent-skills | 液体处理与实验协议编写自动化（opentrons） | Opentrons | MIT（仓库级） | REVIEW / LOW CURRENT PRIORITY | Low |

### 增量 License / Security / LowCurrent 标记汇总

- **License 硬 BLOCKED**：0。
- **License REVIEW（2 条）**：`chrome-devtools-mcp`（LICENSE 未明示，Google 惯例疑 Apache-2.0）、`trend-radar`（LICENSE 未明示）。导入前须确认 LICENSE 与 NOTICE。
- **K-Dense 个体 License 说明**：仓库级 MIT 清晰、可商用；但各 `SKILL.md` 可能声明不同许可（如部分文档类技能沿用 Anthropic 条款），逐条固定 LICENSE 后再入 CanonicalAgentSpec；不整库复制。此批不计入硬 REVIEW，但保留单技能复核动作。
- **Security Review（1 条）**：`clinical-decision-support`（临床敏感数据，需沙箱 + 免责，禁止伪造“已验证”）。`figma-context-mcp` 需用户提供 Figma API 令牌，按凭据最小权限处理（不计入正式 Security Review 计数）。
- **LOW CURRENT PRIORITY（1 条）**：`opentrons`（实验室硬件自动化，当前 Curis 业务不覆盖）。保留候选以支持“未来任意 Business 可找到现成人才”。

### 增量后推荐优先导入候选（供 Codex 能力专项）

1. `markitdown`（Microsoft，MIT，文档→Markdown 通用转换，可作 MCP）— High（License 清晰，可产品化）
2. `scrapling`（D4Vinci，BSD-3，AI 辅助网页抓取 MCP）— High
3. `figma-context-mcp`（GLips，MIT，Figma 设计上下文开源替代）— High
4. `K-Dense scientific-writing`（MIT，证据可追溯写作）— High
5. `K-Dense database-lookup`（MIT，78+ 科学库统一检索）— High
6. `K-Dense literature-review`（MIT，文献综述）— High
7. `K-Dense scientific-visualization`（MIT，科学绘图）— High
8. `chrome-devtools-mcp`（REVIEW，浏览器调试）— High（License 待确认）
9. `trend-radar`（REVIEW，舆情监控）— Med（License 待确认）

> 上述均为 Candidate。markitdown/scrapling/figma-context-mcp 与 K-Dense 个体 License 清晰，但未经 Curis 真实任务验证与 Evidence，仍不得标 `CURIS_READY`；chrome-devtools-mcp / trend-radar 须在 LICENSE 确认前保持 BLOCKED/Review。严禁把“发现候选”冒充 `CURIS_READY`。

---

## 连续两日扫描验证入库（2026-08-19 · 情报专项）

> **对象**：连续两日自动扫描结果 = `2026-08-18 周常（26）` + `2026-08-19 周常（31）` + `2026-08-19 持续第二批（15）`，共 **72 条去重候选**，覆盖 WorkBuddy、Coze、alirezarezvani/claude-skills、OpenClaw ClawHub、MCP 聚合站、K-Dense-AI 六源。
> **动作**：逐条执行 **License Gate + Security Gate + 去重复核**（沿用 §9 交接规则与生产线只读 Adapter）；License 清晰 High 项已补中文商品卡（见 `Curis_Talent_Chinese_Productization_Batch1.md` §16/§17）。
> **红线**：不建第二套 Registry / Candidate Queue；所有成果作为现有生产线的候选输入；严禁把"发现/验证候选"冒充 `CURIS_READY`。

### 验证汇总

| 维度 | 数量 |
|---|---:|
| 连续两日扫描来源数 | 6 |
| 去重后候选总数 | 72 |
| Expert / Expert-Team | 5 |
| Skill | 47 |
| Connector(MCP) | 19 |
| Tool / Marketplace | 1 |
| **License 清晰可入库**（MIT / BSD-3 已确认） | **33** |
| **License REVIEW**（专有/未明示，保持 BLOCKED/Review） | **39** |
| **Security Review**（凭据/数据出域/敏感域，待信任层） | **20** |
| LOW CURRENT PRIORITY | 12 |
| License 硬 BLOCKED | 0 |

### Gate 验证结论

- **License Gate PASS（33 条 → Candidate Queue 就绪）**
  - alirezarezvani 15 条（全库 MIT 清晰）：`c-level-skills` / `business-growth-skills` / `executive-mentor` / `a11y-audit` / `agenthub` / `aws-architect` / `code-to-prd` / `data-quality-auditor` / `fullstack-engineer` / `google-workspace-cli` / `product-manager` / `product-skills` / `helm-chart-builder` / `demo-video` / `docker-development`
  - K-Dense 10 条（MIT 仓库级；单技能 `SKILL.md` 复核）：`scientific-writing` / `database-lookup` / `scientific-visualization` / `literature-review` / `hypothesis-generation` / `experimental-design` / `diffdock` / `pathway-enrichment` / `clinical-decision-support`（另归 Security）/ `opentrons`（另归 Low）
  - MCP 聚合站 8 条（MIT/BSD-3）：`markitdown` / `scrapling` / `figma-context-mcp` + 其余清晰项
- **License Gate REVIEW（39 条 → 保持 BLOCKED/Review，不入库）**：WorkBuddy 专有市场（9）、Coze 专有（8）、ClawHub 社区（16）。商业授权与逐文件 LICENSE/NOTICE 确认前不得宣称可招募。
- **Security Gate REVIEW（20 条 → 待信任层）**：所有连接器类（WB 腾讯文档/会议/QQ邮箱/企业微信/微信/乐享/ima/COS；Coze 原生插件集/抖音/豆包/Coze.com；ClawHub `dingtalk`/`wecom`/飞书×4/`web-content-fetcher`）+ `clinical-decision-support`。处理：凭据最小化、数据出域/注入扫描、凭据不入库、沙箱执行。
- **去重复核**：72 条均与初轮 ~250 候选 + 各批次互比，无同名重复；集合型来源仅逐条登记，未整库复制。

### 入库判定（沿用现有 Candidate Queue，不新建）

| 状态 | 数量 | 说明 |
|---|---|---|
| ✅ Candidate Queue 就绪 | 33 | License 清晰且非敏感，可直接进入现有生产线 Candidate Queue，由 Codex 专项做运行时真实任务验证 + Evidence 后晋级 `CURIS_READY` |
| ⏸ BLOCKED-REVIEW | 39 | License 未确认，保持 Candidate/Review，待授权确认 |
| 🔒 SECURITY-REVIEW | 20 | 待信任层（来源审核 + SHA-256 + 沙箱）建立后复审 |
| ⚠️ LOW CURRENT PRIORITY | 12 | 保留候选，支持"未来任意 Business 可找到现成人才" |
| **全部仍为 Candidate** | 72 | **严禁把"发现/验证候选"冒充 `CURIS_READY`** |

### 与默认职能组织的关系

- 连续两日扫描**补强数据分析部组件**：`data-quality-auditor`（数据质量审计）、`database-lookup`（跨库检索）、`scientific-visualization`（科学可视化）可作为 Company Analyst / Data Analyst 能力组合来源。
- **空间工程部核心 Employee、Company Analyst** 仍为 Curis 内置 Gap（见 `Curis_Default_Functional_Talent_Verification_2026-08-18.md`），外部无完整可招募 Employee 角色；Curis 内置定义不得冒充外部 Expert。

---

## 增量扫描（2026-08-31 持续扫描第三批 · MCP 高星生态 + 代码智能专项）

> 本轮来源（2，均为真实拉取）：① **MCP 生态高星排行榜**（awesome-mcp.tools「Top MCP Servers 2026」+ AlexMili/Awesome-MCP 精选索引 + git-stars MCP topic）；② **代码智能 / 沙箱 / Agent 记忆类 MCP 专项核验**（逐项 WebSearch 核实 License 与 star）。
> 去重结论：下列 12 条均为既有 ~250 + 08-18 增量 26 + 08-19 增量 15 之外的新条目；已显式排除本轮检索中发现的**重复项**（playwright-mcp / github-mcp-server / context7 / markitdown 均已在包内）。
> License 严谨性说明：`mindsdb` 存在**来源冲突**（聚合站标注 MIT、GitHub/索引站标注 NOASSERTION），按闸门规则标 **REVIEW** 并注明冲突，不采信单一来源；`netdata` 为 GPL-3.0（OSI 但强 copyleft），非 BLOCKED，但标 REVIEW 提示分发义务；`graphiti` 仅获次要来源提及（未获 license/star 一手核验），标 REVIEW 并注明待核实，不编造数值。

### 增量扫描汇总

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 2 |
| 新发现资源（原始，含已剔除 4 项重复） | 16 |
| 去重后候选数 | 12 |
| Expert / Expert-Team | 0 |
| Skill | 0 |
| Connector(MCP) | 7 |
| Tool / 框架·平台 | 5 |
| License 硬 BLOCKED | 0 |
| License REVIEW | 6 |
| License 清晰（MIT / Apache-2.0） | 6 |
| Security Review | 5 |
| LOW CURRENT PRIORITY | 2 |

### A. 来源一：MCP 生态高星排行榜（awesome-mcp.tools + Awesome-MCP + git-stars）

真实来源：https://awesome-mcp.tools/blog/top-mcp-servers-2026 ；https://github.com/AlexMili/Awesome-MCP ；https://git-stars.org/zh/repositories/topic/model-context-protocol 。抓取日期 2026-08-31。

#### A.1 Connector(MCP) / 数据·基础设施

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| mindsdb | Connector(MCP) | 数据联邦/RAG | MindsDB | https://github.com/mindsdb/mindsdb | 联合查询引擎自带 MCP：200+ 数据源（Postgres/MySQL/Mongo/Snowflake/BigQuery/Salesforce/Slack/S3 等）统一 SQL 与自然语言查询；Knowledge Bases 混合向量+关键词 RAG；Jobs/Triggers 定时同步；Docker 一键自托管 | 各数据源凭据；Docker | **REVIEW（许可冲突：聚合站标 MIT，GitHub/索引站标 NOASSERTION）** | REVIEW / SECURITY REVIEW（多源凭据+数据出域） | High |
| netdata | Connector(MCP) | 可观测/运维 | Netdata | https://github.com/netdata/netdata | 实时基础设施监控（秒级指标、ML 异常检测、自动告警），MCP 暴露后可用自然语言查实时指标/告警/根因分析与可观测报告 | 自托管 Agent；无需 API key | GPL-3.0（OSI，强 copyleft） | REVIEW（copyleft 分发义务）/ SECURITY REVIEW（基础设施数据）/ LOW CURRENT PRIORITY | Med |
| octocode (Muvon) | Connector(MCP) | 代码智能 | Muvon | https://github.com/Muvon/octocode | 语义代码索引器：GraphRAG 知识图谱 + MCP，tree-sitter AST 解析、ast-grep 结构化搜索、代码签名视图，13+ 语言，local-first | 本地代码库 | Apache-2.0 | 重叠-增量（与 codebase-memory-mcp 同赛道）/ 新增 | Med |

#### A.2 Tool / 框架·平台

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| fastmcp | Tool | MCP 开发框架 | PrefectHQ | https://github.com/PrefectHQ/fastmcp | MCP 服务器/客户端 Python 框架：装饰器声明工具即自动生成 schema、校验与文档；三支柱 Servers / Clients / Apps；v1.0 已并入官方 MCP Python SDK，现为独立维护的事实标准 | Python + uv；`uv pip install fastmcp` | Apache-2.0 | 新增 | High |
| UI-TARS-desktop（Agent TARS） | Tool | GUI 多模态 Agent 栈 | ByteDance | https://github.com/bytedance/UI-TARS-desktop | 开源多模态 Agent 栈：UI-TARS Desktop 桌面 GUI Agent（视觉原生，直接看屏幕操作鼠标键盘，不依赖 OCR/DOM）+ Agent TARS（CLI/Web UI，GUI Agent+浏览器+终端，内核基于 MCP，可挂载 MCP Server） | Node ≥22；VLM（HF 或火山引擎）；macOS/Windows | Apache-2.0 | 新增 / SECURITY REVIEW（高权限：控制桌面与键鼠） | High |
| claude-task-master | Tool | 任务编排 | eyaltoledano | https://github.com/eyaltoledano/claude-task-master | PRD 驱动的自主任务运行器：读取 spec 文件 → 规划子任务 → 逐个执行，把 Coding Agent 变成任务驱动执行器（26k★） | Node；`npx task-master-ai` | REVIEW（未明示） | REVIEW | High |
| modelcontextprotocol/registry | Tool/Marketplace | MCP 注册中心 | modelcontextprotocol | https://github.com/modelcontextprotocol/registry | 官方社区驱动的 MCP 服务器注册服务（Go），统一服务器发现与元数据分发 | 自托管 Go 服务 | REVIEW（未明示） | 新增 | Med |
| nanobot | Tool | 轻量 Agent 框架 | HKUDS | https://github.com/HKUDS/nanobot | 超轻量开源自托管 Python 个人 AI 智能体框架：WebUI、工具、记忆、MCP、多智能体工作流、自动化与聊天应用（46.9k★） | Python；自托管 | REVIEW（未明示） | 新增 | High |

### B. 来源二：代码智能 / 沙箱 / Agent 记忆类 MCP 专项核验

真实来源：逐项 WebSearch 核实（抓取日期 2026-08-31）：codebase-memory-mcp 官方 README 与第三方项目页；serena 官方仓库与第三方评测；e2b-dev/mcp-server 仓库；graphiti 见腾讯云开发者社区「盘点 9 个数据库 MCP」https://cloud.tencent.com/developer/article/2536747 。

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| codebase-memory-mcp | Connector(MCP) | 代码智能 | DeusData | https://github.com/DeusData/codebase-memory-mcp | 把代码库索引为**持久化知识图谱**：tree-sitter AST 支持 158 语言 + Hybrid LSP 语义解析（Python/TS/Go/Rust/Java 等 11 种）；15 个 MCP 工具（index_repository / search_graph / trace_path / query_graph / detect_changes / get_architecture 等）；亚毫秒查询，5 次结构化查询约 3.4k token vs 文件级约 412k token（**厂商标称，未独立复现**）；单静态二进制、零依赖、**100% 本地** | 单二进制（macOS/Linux/Windows）；无 API key | MIT | 新增（v0.9.0 仍 0.x；一键安装脚本会改 agent 配置，建议先审计） | High |
| serena | Connector(MCP) | 代码智能 | oraios | https://github.com/oraios/serena | 符号级语义代码检索与编辑（"the IDE for your agent"）：LSP 驱动，40+ 语言；find_symbol / find_referencing_symbols / rename / replace_symbol_body / safe_delete；项目记忆跨会话持久化为可审阅 Markdown；可选 JetBrains 后端增强重构 | Python 3.11+ + uv；`uv tool install serena-agent` | MIT（2025-05 由其他许可切换为 MIT） | 新增 / SECURITY REVIEW（本地文件写 + shell 执行，默认无沙箱、无密钥检测） | High |
| e2b mcp-server | Connector(MCP) | 代码沙箱 | e2b-dev | https://github.com/e2b-dev/mcp-server | 云端隔离沙箱执行代码（JavaScript / Python）：create_sandbox / execute_code / list_sandboxes 三个工具，每个沙箱独立容器，AI 生成代码不影响本地系统 | Node 18+；**需 E2B API key**（有免费额度） | Apache-2.0 | 新增 / SECURITY REVIEW（云端执行 + API key，非自托管） | Med |
| graphiti | Connector(MCP) | Agent 记忆 | getzep | https://github.com/getzep/graphiti | 让 Agent 自建并查询**带时间感知的知识图谱**，作为 Agent 外置长期记忆体，缓解"干完活就忘" | 需图数据库（如 Neo4j）；自托管 | REVIEW（未明示，本轮未获一手核验） | REVIEW / LOW CURRENT PRIORITY | Med |

### 增量 License / Security / LowCurrent 标记汇总

- **License 硬 BLOCKED**：0。
- **License REVIEW（6 条）**：`mindsdb`（来源冲突 MIT vs NOASSERTION，须核对仓库 LICENSE 原文）、`netdata`（GPL-3.0，OSI 但强 copyleft，注意分发与衍生义务）、`claude-task-master`、`modelcontextprotocol/registry`、`nanobot`、`graphiti`（均许可未明示；graphiti 本轮未获一手核验）。
- **License 清晰（6 条，可产品化）**：`fastmcp`(Apache-2.0)、`UI-TARS-desktop`(Apache-2.0)、`e2b mcp-server`(Apache-2.0)、`serena`(MIT)、`codebase-memory-mcp`(MIT)、`octocode`(Apache-2.0)。
- **Security Review（5 条）**：`mindsdb`（200+ 数据源凭据集中、数据出域）、`netdata`（基础设施与告警数据）、`serena`（本地文件写 + shell 执行，默认无 OS 级沙箱与密钥检测，等同授予终端权限）、`UI-TARS-desktop`（视觉控制桌面与键鼠，高权限，须限制范围并加人工确认）、`e2b mcp-server`（代码上云执行 + API key）。处理：进入产线前做凭据最小化/注入/权限扫描；高权限类须沙箱 + 审计 + 不可逆操作人工确认。
- **LOW CURRENT PRIORITY（2 条）**：`netdata`（运维监控，当前 Curis 业务不覆盖）、`graphiti`（Agent 记忆层，暂无落地场景）。保留候选以支持"未来任意 Business 可找到现成人才"。

### 增量后推荐优先导入候选（供 Codex 能力专项）

1. `codebase-memory-mcp`（MIT，代码知识图谱，本地零依赖）— High
2. `serena`（MIT，符号级代码检索与重构）— High（SECURITY REVIEW）
3. `fastmcp`（Apache-2.0，MCP 服务器开发框架，能力基建）— High
4. `UI-TARS-desktop`（Apache-2.0，GUI 多模态 Agent 栈）— High（SECURITY REVIEW）
5. `mindsdb`（200+ 数据源联邦查询）— High（**须先解决 License 冲突**）
6. `nanobot`（轻量自托管 Agent 框架）— High（REVIEW）
7. `claude-task-master`（PRD 驱动任务运行器）— High（REVIEW）
8. `octocode`（Apache-2.0，图谱化代码索引）— Med（与 codebase-memory-mcp 重叠）
9. `e2b mcp-server`（云端代码沙箱）— Med（SECURITY REVIEW）

> 上述均为 Candidate。License 清晰的 6 条仍须经 Curis 真实任务验证 + Evidence 方可晋级 `CURIS_READY`；REVIEW 项在许可确认前保持 BLOCKED/Review。严禁把"发现候选"冒充 `CURIS_READY`。

---

## 增量扫描（2026-08-31 持续扫描第四批 · License 核验订正 + VoltAgent 厂商技能索引）

> 本轮两件事：① **解锁上轮遗留的 License 阻塞项**（直接抓取仓库 LICENSE 原文核验，而非依赖聚合站）；② **扫描 VoltAgent/awesome-agent-skills 厂商官方技能索引**（1497+ skills，此前多轮仅登记索引本身，未枚举条目）。
> **去重结论**：Part B 的 20 条均为既有候选之外的新条目；已显式排除本轮索引中与包内重复的集合（anthropics/skills、openai/skills、vercel-labs、obra/superpowers、alirezarezvani、K-Dense、Trail of Bits 集合、以及已作为 MCP 登记的 Composio/Firecrawl/Stripe/Supabase/Cloudflare/HuggingFace/Netlify/Figma MCP 等）。

### 增量扫描汇总

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 2（VoltAgent 厂商技能索引 + GitHub raw LICENSE 核验专项） |
| 新发现资源（原始，含已剔除重复） | ~60 |
| 去重后新增候选数 | 20（全部为 Skill / Skill 集合） |
| Expert / Expert-Team | 0 |
| Skill | 20 |
| Connector(MCP) | 0 |
| Tool | 0 |
| **License 核验订正（非新增）** | 4 |
| ├ 转清晰（REVIEW → 可商用） | 3（mindsdb·nanobot → MIT；graphiti → Apache-2.0） |
| └ **改判 BLOCKED** | **1（claude-task-master：MIT + Commons Clause）** |
| License 硬 BLOCKED（累计新增） | 1 |
| License REVIEW | 20（VoltAgent 全部，各厂商仓库许可未明示） |
| Security Review | 6 |
| LOW CURRENT PRIORITY | 2 |

### A. License 核验订正（抓取 LICENSE 原文，替代聚合站二手信息）

方法：直接抓取 `raw.githubusercontent.com/<repo>/main/LICENSE` 原文，不采信聚合站标签。**这是本轮最重要的产出**——纠正了上轮因依赖二手来源导致的 2 处误判。

| 条目 | 上轮标记 | 核验后 | LICENSE 原文关键证据 | 处置 |
|---|---|---|---|---|
| mindsdb | REVIEW（许可冲突） | **MIT（清晰）** | 原文首行 "MIT License / Copyright (c) 2019 MindsDB, Inc."，标准 MIT 全文 | **解除阻塞**，可产品化；注意部分集成 handler / 企业组件可能另有条款，导入前逐 handler 复核 |
| nanobot | REVIEW（未明示） | **MIT（清晰）** | "MIT License / Copyright (c) 2025-present Xubin Ren and the nanobot contributors" | **解除阻塞**，可产品化 |
| graphiti | REVIEW（未一手核验） | **Apache-2.0（清晰）** | 标准 Apache License Version 2.0, January 2004 全文 | **解除阻塞**；优先级仍为 Med（LOW CURRENT） |
| claude-task-master | REVIEW（未明示） | **BLOCKED（商用受限）** | 文件为 "Task Master License"：**MIT 全文 + 追加 "Commons Clause" License Condition v1.0**，明确载明 *"the License does not grant to you, the right to Sell the Software"*；"Sell" 含"作为产品/服务的一部分向第三方提供并收费" | **改判 BLOCKED**。Curis 为对外商用产品，将其纳入付费服务即触发限制；**仅限内部自用评估**，不得进入可招募能力 |

> ⚠️ **方法论警示（供后续轮次遵守）**：聚合站（AgentIndex / 各类目录）把 Commons Clause 类仓库标为"MIT"或"NOASSERTION"均不可靠——Commons Clause 是**附加在开源许可之上的商用限制条款**，只有读 LICENSE 原文才能发现。凡"MIT/Apache 但含附加条件"的仓库，一律按 **BLOCKED** 处理，不得因聚合站标签放行。

### B. 新增候选：VoltAgent 厂商官方技能索引（20 条）

真实来源：https://github.com/VoltAgent/awesome-agent-skills （Latest commit `5e1f3ae`，2026-08-29；Skills Count 1497+）。索引仓库自身含 LICENSE 文件但**未披露类型**；下列条目为各厂商自有仓库，**许可需逐仓库核对，统一标 REVIEW**。

字段：名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级

| 名称 | 类型 | 分类 | 来源 | Source URL | 能力简述 | 依赖/可接入 | License | 标记 | 优先级 |
|---|---|---|---|---|---|---|---|---|---|
| microsoft/skills（133） | Skill集合 | 云架构/前端/Azure SDK | Microsoft | https://github.com/VoltAgent/awesome-agent-skills | 6 类 133 技能：Core（cloud-solution-architect / frontend-design-review / mcp-builder / skill-creator / github-issue-creator / copilot-sdk / continual-learning / podcast-generation）+ .NET 28 / Java 25 / Python 39 / Rust 7 / TypeScript 24（Azure SDK 全覆盖） | Claude/Codex 等 | REVIEW（未明示） | 新增 | High |
| LambdaTest/agent-skills（testmu-ai，45） | Skill集合 | 测试工程 | TestMu AI (LambdaTest) | https://github.com/VoltAgent/awesome-agent-skills | 45 个测试生成技能：playwright / pytest / jest / mocha / vitest / jasmine / karma / cypress / selenium / webdriverio / testcafe / nightwatch / puppeteer / detox / espresso / xcuitest / flutter-testing / robot-framework / cucumber / behave / behat / specflow / reqnroll / gauge / junit-5 / testng / nunit / mstest / xunit / rspec / minitest / phpunit / codeception / laravel-dusk / api-skill / cicd-pipeline-skill / test-framework-migration-skill 等 | 各语言测试栈 | REVIEW | 新增（测试工程领域首次成体系登记） | High |
| googleworkspace/gws-*（17） | Skill集合 | 办公自动化 | Google Workspace CLI | https://github.com/VoltAgent/awesome-agent-skills | 17 个官方技能：gws-drive / gws-sheets / gws-gmail / gws-calendar / gws-docs / gws-slides / gws-tasks / gws-people / gws-chat / gws-classroom / gws-forms / gws-keep / gws-admin-reports / gws-events / gws-modelarmor / gws-workflow / gws-shared | Google 凭据（OAuth） | REVIEW | 新增 / SECURITY REVIEW（Google 凭据+数据出域） | High |
| getsentry/sentry-*（28） | Skill集合 | 可观测/质量 | Sentry | https://github.com/VoltAgent/awesome-agent-skills | 28 个技能：sentry-sdk-setup（自动检测语言/框架路由）/ sentry-workflow / sentry-fix-issues（MCP 取堆栈+面包屑+trace 定位修复）/ sentry-code-review / sentry-pr-code-review / sentry-create-alert / sentry-otel-exporter-setup / sentry-setup-ai-monitoring + 20 个平台 SDK（python/node/nextjs/react/go/java/php/ruby/dotnet/flutter/android/cocoa/cloudflare/nestjs/elixir/react-native/svelte/browser） | Sentry 账号 + MCP | REVIEW | 新增 / SECURITY REVIEW（生产错误与 trace 数据） | High |
| figma/*（6） | Skill集合 | 设计到代码 | Figma | https://github.com/VoltAgent/awesome-agent-skills | 官方 6 技能：figma-implement-design（1:1 保真把设计译为生产代码）/ figma-generate-design / figma-generate-library / figma-code-connect-components / figma-create-design-system-rules / figma-use（Plugin API 画布写入） | Figma API / MCP | REVIEW | 新增（与已登记的 figma-mcp、openai figma* 不同封装） | High |
| fal-ai-community/*（15） | Skill集合 | 多模态内容生产 | fal.ai | https://github.com/VoltAgent/awesome-agent-skills | 15 个生成技能：fal-generate（图/视频）/ fal-image-edit / fal-video-edit / fal-upscale / fal-restore / fal-3d / fal-lip-sync（对口型）/ fal-tryon（虚拟试穿）/ fal-train（LoRA 训练）/ fal-realtime / fal-vision（分割/OCR/描述/VQA）/ fal-audio / fal-kling-o3 / fal-workflow / fal-platform | fal.ai API key | REVIEW | 新增 / SECURITY REVIEW（API key + 内容上云） | High |
| typefully/typefully | Skill | 社媒运营 | Typefully | https://github.com/VoltAgent/awesome-agent-skills | 在 X / LinkedIn / Threads / Bluesky / Mastodon 上创建、调度并发布内容 | Typefully 账号授权 | REVIEW | 新增 / SECURITY REVIEW（社媒账号发布权限） | High |
| sanity-io/*（4） | Skill集合 | 内容/AEO | Sanity | https://github.com/VoltAgent/awesome-agent-skills | 4 技能：sanity-best-practices（Studio/GROQ/内容工作流）/ content-modeling-best-practices / **seo-aeo-best-practices（SEO 与答案引擎优化）** / content-experimentation-best-practices（内容 A/B 实验） | Sanity 项目 | REVIEW | 新增（AEO 为 Content Growth 高相关） | High |
| hashicorp/*（11） | Skill集合 | IaC | HashiCorp | https://github.com/VoltAgent/awesome-agent-skills | Terraform 11 技能：new-terraform-provider / provider-resources / provider-actions / provider-test-patterns / run-acceptance-tests / refactor-module / terraform-search-import / terraform-stacks / terraform-test / terraform-style-guide / azure-verified-modules | Terraform + Go | REVIEW | 新增 | Med |
| cloudflare/*（8） | Skill集合 | 边缘云/Agent 基建 | Cloudflare | https://github.com/VoltAgent/awesome-agent-skills | 8 技能：agents-sdk（带调度/RPC/MCP 的有状态 AI Agent）/ sandbox-sdk（Workers 上安全隔离代码执行）/ durable-objects / workers-best-practices / wrangler / web-perf（核心 Web 指标审计）/ cloudflare-email-service / cloudflare（平台总览） | Cloudflare 账号 | REVIEW | 新增 | Med |
| expo/*（11） | Skill集合 | 移动端 | Expo | https://github.com/VoltAgent/awesome-agent-skills | 11 技能：building-native-ui / expo-api-routes / expo-cicd-workflows / expo-deployment / expo-dev-client / expo-tailwind-setup / expo-ui-jetpack-compose / expo-ui-swift-ui / native-data-fetching / upgrading-expo / use-dom | Expo SDK | REVIEW | 新增 / LOW CURRENT PRIORITY | Med |
| WordPress/*（13） | Skill集合 | 建站/内容 | WordPress | https://github.com/VoltAgent/awesome-agent-skills | 13 技能：wordpress-router / wp-project-triage / wp-block-development / wp-block-themes / wp-plugin-development / wp-rest-api / wp-interactivity-api / wp-abilities-api / wp-wpcli-and-ops / wp-performance / wp-phpstan / wp-playground / wpds（设计系统） | WordPress 项目 | REVIEW | 新增 | Med |
| 数据栈官方技能集（Neon 3 / ClickHouse 6 / Tinybird 4 = 13） | Skill集合 | 数据/OLAP | Neon·ClickHouse·Tinybird | https://github.com/VoltAgent/awesome-agent-skills | Neon：neon-postgres / claimable-postgres / neon-postgres-egress-optimizer；ClickHouse：clickhouse-best-practices / clickhouse-architecture-advisor / chdb-sql（进程内引擎）/ chdb-datastore / clickhousectl-cloud-deploy / clickhousectl-local-dev；Tinybird：best-practices / cli-guidelines / python-sdk / typescript-sdk | 各数据库 | REVIEW | 新增 | Med |
| veniceai/*（19） | Skill集合 | 多模型 API | Venice.ai | https://github.com/VoltAgent/awesome-agent-skills | 19 技能：venice-chat / venice-responses / venice-embeddings / venice-image-generate / venice-image-edit / venice-audio-speech / venice-audio-music / venice-audio-transcription / venice-video / venice-models / venice-characters / venice-api-keys / venice-billing / venice-auth / venice-api-overview / venice-errors / **venice-x402（加密支付）** / venice-crypto-rpc / venice-augment | Venice API key | REVIEW | 新增 / SECURITY REVIEW / LOW CURRENT PRIORITY | Med |
| google-gemini/*（4） | Skill集合 | 模型开发 | Google | https://github.com/VoltAgent/awesome-agent-skills | gemini-api-dev / vertex-ai-api-dev（Gen AI SDK）/ gemini-live-api-dev（实时双向流式）/ gemini-interactions-api | Google Cloud / API key | REVIEW | 新增 | Med |
| google-labs-code/*（6） | Skill集合 | 设计到代码 | Google Labs (Stitch) | https://github.com/VoltAgent/awesome-agent-skills | 6 技能：design-md（DESIGN.md 管理）/ enhance-prompt（用设计规范与 UI/UX 词汇改进提示词）/ react-components（Stitch→React 组件）/ shadcn-ui / remotion（生成演示视频）/ stitch-loop（设计到代码迭代闭环） | Google Stitch | REVIEW | 新增 | Med |
| better-auth/*（7） | Skill集合 | 认证 | Better Auth | https://github.com/VoltAgent/awesome-agent-skills | best-practices / explain-error / providers / create-auth / emailAndPassword / organization / twoFactor | Better Auth | REVIEW | 新增 | Med |
| 前端框架官方技能集（Angular 2 / Callstack 3 / Supabase 1 = 6） | Skill集合 | 前端框架 | Angular·Callstack·Supabase | https://github.com/VoltAgent/awesome-agent-skills | Angular：angular-developer / angular-new-app；Callstack：react-native-best-practices / github（PR 与 code review 工作流）/ upgrading-react-native；Supabase：postgres-best-practices | 各框架 | REVIEW | 新增 | Med |
| 多模态与通知补充（3） | Skill集合 | 多模态/通知 | Remotion·Replicate·Courier | https://github.com/VoltAgent/awesome-agent-skills | remotion-dev/remotion（React 程序化视频创作）/ replicate/replicate（发现·比较·运行 AI 模型）/ trycourier/courier-skills（email·SMS·push·chat 多渠道通知） | 各平台 API key | REVIEW | 新增 | Med |
| zero/zero | Skill | 工具发现+支付 | Zero | https://github.com/VoltAgent/awesome-agent-skills | 让 Agent 自主发现并**付费调用外部工具**，无需用户停下注册或取 API key（另有 zero-gemini 打包为 Gemini CLI 扩展） | 钱包/支付凭据 | REVIEW | 新增 / SECURITY REVIEW（支付与凭据代管，高风险） | Med |

### 增量 License / Security / LowCurrent 标记汇总

- **License 硬 BLOCKED（新增 1）**：`claude-task-master` — MIT + **Commons Clause v1.0**，禁止"Sell the Software"。Curis 对外商用受限，**仅限内部自用评估**，不得进入可招募能力、不得产品化。
- **License 转清晰（3）**：`mindsdb`(MIT)、`nanobot`(MIT)、`graphiti`(Apache-2.0) —— 可进入产品化流程。
- **License REVIEW（20，全部 VoltAgent 新增条目）**：各厂商仓库许可未明示，导入前必须**逐仓库抓取 LICENSE 原文**核对（本轮已证明聚合站标签不可靠）。索引仓库自身 LICENSE 类型亦未披露。
- **Security Review（6）**：`googleworkspace/gws-*`（Google 凭据+数据出域）、`getsentry/sentry-*`（生产错误与 trace 数据）、`typefully`（社媒账号发布权限）、`fal-ai-community/*`（API key + 内容上云）、`veniceai/*`（API key + 加密支付）、`zero/zero`（**支付与凭据代管，最高风险**）。处理：凭据最小化、不入库；`zero/zero` 在未建立支付授权与审计机制前**不得接入**。
- **LOW CURRENT PRIORITY（2）**：`expo/*`（移动端，当前不覆盖）、`veniceai/*`（含加密支付）。保留候选以支持"未来任意 Business 可找到现成人才"。

### 增量后推荐优先导入候选（供 Codex 能力专项）

**已解锁、可立即推进（License 清晰）**
1. `mindsdb`（MIT，200+ 数据源联邦查询 + 混合 RAG）— High
2. `nanobot`（MIT，轻量自托管 Agent 框架）— High

**License REVIEW，但价值高、建议优先做许可核对**
3. `LambdaTest/agent-skills`（45 个测试技能，补 QA 能力空白）— High
4. `microsoft/skills`（133 技能，云架构/前端评审/mcp-builder + Azure 全栈）— High
5. `googleworkspace/gws-*`（17 个办公自动化）— High（SECURITY REVIEW）
6. `getsentry/sentry-*`（28 个，可观测与问题修复闭环）— High（SECURITY REVIEW）
7. `figma/*`（设计到代码官方技能）— High
8. `sanity-io/*`（含 SEO/AEO，契合 Content Growth）— High
9. `typefully`（跨平台社媒发布，契合 Content Growth）— High（SECURITY REVIEW）
10. `fal-ai-community/*`（多模态内容生产 15 技能，契合 Content Growth）— High（SECURITY REVIEW）

**明确排除**
- `claude-task-master` — BLOCKED（Commons Clause），不得进入可招募能力。

> 上述（除已解锁的 mindsdb / nanobot）均仍为 Candidate 且 License=REVIEW，未经 Curis 真实任务验证 + Evidence 不得标 `CURIS_READY`。严禁把"发现候选"冒充 `CURIS_READY`。

---

## 入库记录（2026-08-31 第三批 + 第四批 · 情报专项执行「入库」）

> **动作**：把最近两轮（第三批 / 第四批，均为 2026-08-31）扫描结果中**符合「License 清晰 + 现有生产线 adapter 可消费」**的候选，登记为 `backend/app/agent_conversion/sources/mcp/*.json` 真实源快照，由只读生产线 `scan_local_resource_pool()` 纳入 Candidate Queue。
> **边界**：沿用现有生产线与 `MCPManifestAdapter`，**不建第二套 Registry / Candidate Queue / Capability Truth**；不修改业务代码 / Runtime / Schema / 数据库；不冒充 `CURIS_READY`。
> **验证**：运行生产线扫描器，全量 `discovered` 由 27 → 33（mcp 5 → 11，+6 即本轮新增），`duplicates=0`、`blocked` 仅既有 5 条，6 条新 MCP 均为 `DISCOVERED`、License / Security 闸门 `pass`。

### 本轮实际入库（6 个 MCP，进入 Candidate Queue · DISCOVERED）

| 名称 | License | 源文件 | 安全标记 | 备注 |
|---|---|---|---|---|
| codebase-memory-mcp | MIT | `sources/mcp/codebase-memory-mcp.json` | — | 代码知识图谱，本地零依赖 |
| serena | MIT | `sources/mcp/serena.json` | SECURITY REVIEW | 本地文件写+shell，须沙箱+审计+人工确认 |
| e2b-mcp-server | Apache-2.0 | `sources/mcp/e2b-mcp-server.json` | SECURITY REVIEW | 代码上云+API key，须凭据最小化 |
| mindsdb | MIT | `sources/mcp/mindsdb.json` | SECURITY REVIEW | 200+ 数据源凭据集中，须逐 handler 复核 |
| graphiti | Apache-2.0 | `sources/mcp/graphiti.json` | LOW CURRENT | Agent 记忆层，暂无落地场景，保留 |
| octocode | Apache-2.0 | `sources/mcp/octocode.json` | — | 与 codebase-memory-mcp 同赛道，重叠待评估 |

> 注：只读扫描器将全部 `sources/mcp/*.json` 统一归因到 MCP 目录根 `modelcontextprotocol/servers`；各条目**真实仓库 URL 以 `_source_url` 字段保留在源文件中**作为 Source Truth（与既有 filesystem/git 等 MCP 源处理一致）。

### 本轮未入库（保持 Catalog 标记，理由明确）

- **License 清晰但无 adapter（3，Catalog 候选，待 Codex seed 登记）**：`fastmcp`(Apache-2.0, MCP 开发框架)、`UI-TARS-desktop`(Apache-2.0, GUI 多模态 Agent 栈, SECURITY REVIEW)、`nanobot`(MIT, 轻量自托管 Agent 框架)。生产线当前仅 4 个 adapter（Agency/Markdown/Crew/Yaml/OpenClaw Skill/MCP JSON），无「Tool/框架·平台」adapter，故留 Catalog，由 Codex 经 seed 路径落库。
- **License 硬 BLOCKED（1，排除）**：`claude-task-master` — MIT + **Commons Clause v1.0**（禁止 Sell the Software），Curis 对外商用受限，仅限内部自用评估，不得进入可招募能力、不得产品化。
- **License REVIEW（20，VoltAgent 厂商技能索引 + 其余）**：`microsoft/skills`、`LambdaTest/agent-skills`、`googleworkspace/gws-*`、`getsentry/sentry-*`、`figma/*`、`fal-ai-community/*`、`typefully`、`sanity-io/*`、`hashicorp/*`、`cloudflare/*`、`expo/*`、`WordPress/*`、数据栈官方技能集、`veniceai/*`、`google-gemini/*`、`google-labs-code/*`、`better-auth/*`、前端框架集、多模态与通知补充、`zero/zero`（支付代管最高风险）。各厂商仓库许可未明示，导入前须逐仓库抓取 LICENSE 原文核对（第四批已证明聚合站标签不可靠）。
- **其余 REVIEW（批次三遗留）**：`netdata`(GPL-3.0, copyleft 分发义务)、`modelcontextprotocol/registry`(未明示)。

### 入库后成熟度说明

- 上述 6 条为 **Candidate Queue · DISCOVERED**，仍须经 Curis 真实任务验证 + Evidence + 成熟度判断，方可能晋级 `CURIS_READY`；当前**无任何条目晋级 `CURIS_READY`**。
- 17 个既有 Agent 候选仍为 `CANDIDATE`（招募前须 Codex 组合/验证）；5 个既有 Skill 仍为 catalog。
- 默认职能 Gap（空间工程部核心 Employee / Company Analyst / Analytics Engineer）仍由 Curis 内置定义，不冒充外部 Expert（见 `Curis_Default_Functional_Talent_Verification_2026-08-18.md`）。

---

CURIS CAPABILITY INTELLIGENCE
— CONTINUOUS SCAN VERIFIED & QUEUED
— CANDIDATE EXPANSION COMPLETE
— STOP FOR CEO REVIEW
