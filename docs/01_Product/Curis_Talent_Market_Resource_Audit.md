# Curis 人才市场资源来源审计

Status: Review  
日期：2026-08-14  
范围：WorkBuddy / Coze / Codex / Claude Code / GitHub Skill、Agent、MCP、Prompt、Template 及当前 Curis Admin/Workspace 资产。

## 结论先行：Curis 第一批专家从哪里来

上一版“WorkBuddy 只能参考”的结论过于保守。现在确认：WorkBuddy 与 OpenClaw 在 Skill/Agent 生态层存在公开格式互通路径；这允许 Curis 合法复用公开仓库和公开注册表资源，但不允许复制 WorkBuddy 私有专家、私有知识或平台内部配置。

第一批采用双来源：

1. 外部优先：`jnMetaCode/agency-agents-zh`。其公开 README 提供 `--tool openclaw` 与 `--tool workbuddy` 的转换/安装路径，并声明 MIT 许可证；先选 5 个与 Curis 公司运行场景匹配的角色作为 Candidate，经 Adapter、许可证、脚本安全和运行验证后上架。
2. Curis 兜底：当前已经存在且可实例化的 7 个官方员工模板：`et_product_manager`、`et_architect`、`et_backend_engineer`、`et_frontend_engineer`、`et_qa_engineer`、`et_devops_engineer`、`et_tech_lead`。
3. Skill 供给：Curis 现有 55 条 active Skill，加上通过 OpenClaw/ClawHub/GitHub 导入的公开 Skill；全部进入统一 Skill Adapter，不直接把外部文件当作已安装公司资源。
4. Curis 已有的模型 / Agent / Tool / Connector 能力绑定与失败关闭规则继续有效；缺少真实模型或授权时，员工保持不可运行，不用假数据冒充可用。

因此第一版市场展示“外部 Candidate + Curis-ready 专家模板”两层资源。首条可验收纵向链路先用 Curis 模板覆盖 5 个角色；外部专家必须通过同一套招募、能力、权限和 Workspace Runtime 门禁后，才能成为可招募员工。

## 复用判定标准

| 判定 | 含义 | Curis 动作 |
| --- | --- | --- |
| 可直接合法复用 | 公开仓库、明确许可证、允许修改/再分发，且不含受保护凭证或私有数据 | 保存来源、版本、许可证和署名后进入 Adapter |
| API / Adapter 接入 | 资源不能复制，但所有者提供公开 API/SDK，调用方有自己的授权 | 只保存外部引用和凭证引用；运行时走 Adapter |
| 可导入配置 | 公开 Manifest / SKILL.md / MCP JSON / Coze Studio 项目文件，许可证允许 | 导入 CanonicalAgentSpec，先 draft，再审核 |
| 只能参考产品设计 | 闭源产品的 UI、信息层级、交互已公开，但资源配置不可复制 | 只参考流程和布局，不复制品牌素材、Prompt、数据或私有接口 |
| Curis 自己开发 | 没有可复用资源，或 Curis 的公司化招募/员工化/组织关系是独有能力 | 只补 Curis 业务连接，不重写外部执行能力 |
| 暂不使用 | 许可证缺失/冲突、条款不清、来源无法验证、含敏感脚本或受保护资源 | 不安装、不发布、不进入公司资源 |

## 1. WorkBuddy / OpenClaw / CodeBuddy

### 已核实的公开事实

- 官方专家文档把“专家”定义为“人设 + 方法论 + 工具链”的角色机制；专家团是多位专家与协作流程。专家本身不主动获取系统权限，只有用户授权 Skill / MCP 后才间接访问文件或外部服务。
- 官方 Skill Market 文档说明 Skill 是可执行脚本/工作流的工具能力，可能读写本地文件、调用第三方 API、使用凭证；第三方 Skill 需要检查来源、权限和脚本。
- 官方 Agent 文档公开了 Agent Manifest 的结构，包含 system prompt、rules、skills、plugins、mcp、subagents、workspaces 等配置；这证明配置组成，但没有授权 Curis 直接复制 WorkBuddy 专家内容。
- 官方连接器文档把 Connector 定义为外部服务桥梁，授权和第三方服务可用性属于连接器边界。
- 官方产品页公开“100+ 领域专家”“MCP 生态 + 自定义 Skills”等产品宣传信息，但没有证明 WorkBuddy 私有专家目录可批量导出为 Curis 资源。
- `agency-agents-zh` 的公开安装脚本明确包含 `--tool openclaw` 和 `--tool workbuddy`；OpenClaw 路径还明确先转换为 `SOUL.md` 等文件再安装。这证明公开 Agent 角色库可以沿公开转换路径进入两类运行环境，但不等于任意 WorkBuddy 内部专家都可导出。
- ClawHub 是 OpenClaw 的公开 Skill/Plugin Registry，支持搜索、安装、更新和发布；Skill 以 `SKILL.md` 与支持文件构成，来源和版本可追踪。它是 Curis 的候选供给源，不是自动信任源。

### 复用判定

| 项目 | 判定 | 说明 |
| --- | --- | --- |
| WorkBuddy 私有专家 / 专家团配置 | 只能参考产品设计 | 不复制 Prompt、配置、图像、成员关系、私有知识或私有接口 |
| OpenClaw/WorkBuddy 公开 Skill/Agent 格式 | 可通过 Adapter 接入 | 先读取公开文件、来源、版本和许可证，再归一到 `CanonicalAgentSpec` / `SkillTemplate` |
| `agency-agents-zh` | 可直接合法复用候选 | 仓库公开声明 MIT，并提供 OpenClaw/WorkBuddy 转换脚本；逐角色保留来源、版本和许可证，脚本与外部依赖仍需安全扫描 |
| `workbuddy-experts` | 待确认来源 | 当前未找到该精确名称的 canonical 公共仓库/许可证；在获得准确 URL 或公开下载源前不导入。相近公开仓库 `Ldxs001/workbuddy-skills` 含 agent/skills，但仓库已声明冻结，需按目录许可证逐项判断 |
| ClawHub | 可作为候选注册表接入 | 只同步公开元数据和版本；下载后做来源、许可证、脚本、凭证、网络和提示注入扫描，不自动安装 |
| WorkBuddy Agent API 接入 | 仍需官方契约 | 公开生态格式接入不等于 WorkBuddy 私有 Agent API；只有正式授权 API/SDK 才增加 `workbuddy_api` Adapter |
| 产品体验 | 可参考 | Curis 使用自有名称、视觉系统、文案和素材 |

### Curis 采用的组件抽象

WorkBuddy/OpenClaw 的公开资料和 `agency-agents-zh` 文件结构支持以下事实分解：

```text
专家 = 角色身份 + 方法论/Instruction + 模型/Agent + Skill + Tool/MCP + Knowledge + Connector + 权限
专家团 = 多个专家 + 协作流程 + 负责人/整合输出
```

Curis 不新增“专家”组织对象：市场中的专家是 EmployeeTemplate 的产品视图；招募后是 EmployeeInstance；能力仍回到 SkillTemplate、Capability、Tool、Connector 与现有 Runtime。

## 2. Coze / 扣子

### 可复用路径

- Coze 官方 SDK `@coze/api` 支持 Agent Chat 和 Workflow 调用；调用者需要自己的 PAT/OAuth 授权，Agent/Workflow 需要按平台要求发布为 API 服务。
- Coze Studio 是公开 GitHub 项目，README 标明 Apache-2.0；公开能力包括 Prompt、RAG、Plugin、Workflow、Agent、App、知识库、数据库以及 API/SDK。
- Coze Studio 的 API 文档要求先发布 Agent 为 API 服务，再用 Personal Access Token 调用；Workflow 也要求发布并按参数契约执行。
- Coze Studio 的商业版插件在开源版中需要手动配置商业版 Token，使用者承担对应账号权限和费用；这不是 Curis 可无授权共享的公共资源。

### 复用判定

| 项目 | 判定 | Curis 动作 |
| --- | --- | --- |
| 已发布、由用户授权的 Coze Agent | 可通过 API / Adapter 接入 | 保存 bot/app/workflow 外部引用，凭证只进 Curis Credential Vault，运行结果进入现有 Evidence/Result 契约 |
| Coze 公开模板直接导入 Curis | 不作为默认能力 | 未发现跨平台通用的“模板导入 Curis”协议；只有拿到公开项目文件且许可证允许时才做配置导入 |
| Coze Studio 开源引擎 | 可研究/合法复用代码 | Apache-2.0 下逐文件保留 NOTICE/许可证；本专项不 fork、不引入完整 Coze Runtime |
| Coze 商业插件/私有 Agent | API / 条款明确后再接 | 不能复制、打包或伪装成 Curis 官方专家 |

## 3. Codex / Claude Code / GitHub 生态

### 可直接进入 Adapter 的候选

| 来源 | 类型 | 许可证/状态 | Curis 判定 |
| --- | --- | --- | --- |
| `openai/skills` | Codex Skill Catalog | 仓库已标注 deprecated；各 Skill 许可证以目录内 LICENSE 为准 | 参考 Skill 目录格式；逐项导入，不把整个仓库当作当前权威 |
| OpenAI Plugins / skill-only plugin | Skill / Plugin Manifest | 以具体插件许可证为准 | 可按 `.codex-plugin/plugin.json`、SKILL.md、scripts、references 设计 Adapter |
| `anthropics/skills` | Agent Skills | 官方仓库显示 Apache-2.0 | 可逐项导入，保留 LICENSE/NOTICE，并做安全扫描 |
| `modelcontextprotocol/servers` | MCP Server | 项目处于 MIT→Apache-2.0 许可证过渡，历史文件需逐项判断 | 可复用明确标注 MIT/Apache-2.0 的 server；过渡或无明确来源的条目暂缓 |
| `obra/superpowers` | 跨 Harness Skill 工作流 | MIT；公开说明包含 Codex/Claude Code 适配 | 可参考/逐项导入 Skill 内容；不得把其运行时适配假设成 Curis 已有执行能力 |
| `coze-dev/coze-studio` | Agent/Workflow/Plugin/Knowledge 平台 | Apache-2.0 | 研究或局部复用，不复制商业平台资源，不引入整套平台 |
| `jnMetaCode/agency-agents-zh` | Agent 角色库 / OpenClaw-WorkBuddy 转换脚本 | MIT（仓库声明） | 作为第一批外部 Candidate；使用既有 `AgencyMarkdownAdapter`，逐角色导入 |
| OpenClaw ClawHub | Skill / Plugin Registry | 条目许可证逐项判断 | 作为发现源；先候选、扫描、许可证门禁，再进入 Curis 公司资源 |
| `Ldxs001/workbuddy-skills` | WorkBuddy skills/agents 社区合集 | skills MIT、agent Apache-2.0、部分文档 CC BY-SA-4.0；仓库声明冻结 | 只作候选来源，逐目录审核，不整仓复制 |

### 审计后的资源组成

进入 Curis 前必须能表达：

```json
{
  "identity": {"name": "", "role": "", "responsibility": ""},
  "source": {"kind": "github|coze_api|curis|other", "ref": "", "version": ""},
  "license": {"spdx": "", "attribution_required": true},
  "model_or_agent": {"kind": "model|agent|external_api", "ref": ""},
  "skills": [],
  "knowledge": [],
  "tools": [],
  "mcp": [],
  "connectors": [],
  "workflow": {"ref": "", "steps": []},
  "permissions": [],
  "security": {"scan": "pending|pass|fail", "notes": ""}
}
```

Prompt/Instruction、Model、Skill、Tool、MCP、Knowledge、Connector、Workflow/Agent 必须分开记录，不能把一段 Prompt 当成“专家已接入”。

## 4. 当前 Curis 已有资产审计

### Admin / Workspace / Runtime 现状

- `backend/app/capability_catalog.py`：统一能力目录，支持 model / agent / tool / connector / skill / mcp / api / cli / webhook / workflow 等元数据；明确不存明文密钥、不做出站调用。
- `backend/app/skill_runtime.py`：SkillTemplate 列表、租户私有 Skill 创建、员工 Skill 绑定、Instruction excerpt 的凭证/运行时指令过滤。
- `backend/app/employee_templates.py`：EmployeeTemplate、DepartmentTemplate、WorkflowTemplate，以及 EmployeeInstance 创建/更新/能力和工具绑定。
- `backend/app/agent_conversion/`：CanonicalAgentSpec、SkillRepoAdapter、MCPManifestAdapter、Agency/CrewAI Adapter、许可证分类、Prompt Injection/凭证/过度承诺扫描和 opt-in seed。
- `backend/app/connectors/registry.py`：当前注册默认连接器为 AiToEarn 与 SocialAutoUpload；连接器目录不返回凭证，运行模式为 mock/real。
- `frontend/app/ceo-office/capabilities/page.js`：现有能力中心已经覆盖模型、智能体、技能、工具、工作流、连接器、CLI、API、Webhook、MCP；它是资源管理页，不是人才市场浏览体验。
- `frontend/app/ceo-office/organization/`：已有公司、部门、员工模板、员工实例和能力绑定界面，可作为“招募”后的组织落点。

### 数据快照（只读检查）

当前本地 `data/curis.sqlite` / `backend/data/curis.sqlite` 的共同基线：

- `employee_templates`：13 条，其中 7 条 `et_*` active 的 Curis 官方员工模板，6 条 `official.employee.*` draft 候选。
- `skill_templates`：55 条 active（3 条通用官方 Skill + 52 条研发 Skill）。
- `tool_templates`：115 条既有工具模板。
- `employee_instances`：当前基线无稳定的已招募员工可作为市场数据；backend/data 是本机验证残留，不升级为产品事实。
- `official_models`：不同本机验证库存在差异，不能把某个验证库中的条目当成默认生产供给。

代码中另有 opt-in、默认不进入初始化链的资源：Pilot B 12 个 Agent 候选、CrewAI 5 个 Agent/crew 候选、5 个 MCP manifest，以及 Skill 仓库 Adapter。它们多数是 draft/candidate 或需要许可证复核，不能直接作为“已可招募专家”。

### 已有资产可否直接复用

| 资产 | 复用结论 |
| --- | --- |
| 7 个 active `et_*` 员工模板 | 可作为第一批市场专家模板 |
| 55 个 active SkillTemplate | 可作为第一批技能资源；通过现有 SkillRuntime 绑定员工 |
| Pilot B / CrewAI 候选 | 先保持 draft/candidate，完成许可证、来源和执行证据后再上架 |
| MCP manifest | 逐项作为连接器/工具候选，不自动授权或安装 |
| 2 个 Connector registry 默认实现 | 可展示“已注册连接器”，授权/维护仍在设置；不要把 mock 运行当成真实连接 |
| 外部 Agent 转换器 | 可直接复用 CanonicalAgentSpec 与安全扫描，不新增第二套 Manifest |

## 5. 资源来源与风险决策

### 直接使用

- Curis 自有模板、SkillRuntime、CapabilityCatalog、EmployeeTemplateContract、Connector registry。
- 许可证明确且经过逐项审核的公开 Skill/MCP/Agent 配置。

### API / Adapter

- 用户自己拥有并授权的 Coze Agent/Workflow。
- 未来有正式授权契约的 WorkBuddy/其他外部 Agent。

### 只能参考

- WorkBuddy 的市场首页、分类、搜索、卡片、详情结构、专家/技能/连接器分层和“召唤专家”到 Curis“招募”的交互语义。
- WorkBuddy 私有专家目录、私有专家 Prompt、私有知识和内部 API。

### 暂不使用

- 未公开导出协议的 WorkBuddy 专家 Prompt/配置。
- 未提供许可证或无法确认再分发权的个人 Skill 仓库。
- 商业版 Coze 插件、第三方凭证、私有知识库、平台内部 API。

## 6. 官方/公开来源

- WorkBuddy 产品页：<https://www.workbuddy.cn/work/>
- WorkBuddy 专家中心：<https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Expert-Center>
- WorkBuddy 技能市场与安全说明：<https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market>
- WorkBuddy Agent Manifest：<https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/CloudAgent>
- WorkBuddy 连接器：<https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector>
- agency-agents-zh：<https://github.com/jnMetaCode/agency-agents-zh>
- OpenClaw ClawHub：<https://github.com/openclaw/clawhub>
- OpenClaw Skills 文档：<https://docs.openclaw.ai/tools/skills>
- WorkBuddy 社区 skills/agents 合集：<https://github.com/Ldxs001/workbuddy-skills>
- Coze 官方工作流/对话文档：<https://www.coze.com/open/docs/guides/workflow_and_chatflow>
- Coze API SDK：<https://www.npmjs.com/package/@coze/api>
- Coze Studio（Apache-2.0）：<https://github.com/coze-dev/coze-studio>
- OpenAI Skills：<https://github.com/openai/skills>
- OpenAI Plugins：<https://github.com/openai/plugins>
- Anthropic Skills：<https://github.com/anthropics/skills>
- MCP Servers：<https://github.com/modelcontextprotocol/servers>
- MCP 许可证说明：<https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE>
- Superpowers：<https://github.com/obra/superpowers>

## 审计结论

Curis 第一批专家改为“`agency-agents-zh` 等公开 Agent 角色库 Candidate + Curis 已有 EmployeeTemplate 兜底”，通过现有 `AgencyMarkdownAdapter`、Skill Adapter、安全扫描和许可证门禁进入市场。WorkBuddy/OpenClaw 公开生态可以接入；WorkBuddy 私有专家资产仍不可复制，`workbuddy-experts` 的精确公共来源仍需确认。ClawHub 作为公开发现源接入，但不自动信任或安装。

## 7. 2026-08-14 实施回写

### 已进入市场的真实资源

- Curis-ready 首批市场专家使用既有 `et_product_manager`、`et_architect`、`et_frontend_engineer`、`et_backend_engineer`、`et_qa_engineer`，招募后复用 EmployeeInstance、Skill Binding 和组织中心，不新增专家表。
- 现有 55 个 active SkillTemplate 继续通过 SkillRuntime 提供发现、幂等纳入公司资源、员工分配和运行时安全 excerpt 读取。
- 首批 5 个公开 Candidate 已由 `AgencyMarkdownAdapter` 从仓库内快照解析：Product Trend Researcher、Marketing Content Creator、Marketing Growth Hacker、Marketing Social Media Strategist、Finance Financial Analyst。来源记录为 `jnMetaCode/agency-agents-zh`，仓库许可证为 MIT，当前本地快照的安全初扫通过。

### 仍然不能升级的状态

- 上述公开角色目前是 Candidate：本地快照与远端文件的逐项对应关系尚未固定版本/digest，来源状态仍为 `pending_snapshot_verification`，不能直接招募或写入 EmployeeTemplate。UI 明确显示 Candidate / 待验证。
- OpenClaw `SKILL.md` 与 supporting files 已有只读适配器；ClawHub 已有 owner/slug/version/digest/origin 元数据门禁，但未自动下载、安装或执行远程内容。
- Connector registry 仍是可发现目录；授权、健康和 Company Resource 绑定没有凭据证据时不升级为可用。
- Coze 仍只保留官方 API/SDK 适配边界；没有用户自己的授权凭据时不宣称完成真实调用。

## 8. Phase 2 生产线扫描回写

Phase 2 已将 AgencyMarkdownAdapter、CrewYamlAdapter、OpenClawSkillAdapter 和 MCPManifestAdapter 统一接入只读生产线。当前本地公开快照共发现 27 条资源：17 个 Agent、5 个 Skill、5 个 MCP；去重后 27 条，17 个 Agent 进入 Candidate，5 个无许可证 Skill 进入 BLOCKED。

生产线已登记 Anthropic Skills、OpenAI Skills、Superpowers、MCP 官方服务器和 ClawHub 等后续来源，但只登记来源与许可证复核状态，不把仓库整体视为可导入。详情见 [`Talent_Library_Expansion_Report.md`](./Talent_Library_Expansion_Report.md)。

---

## 9. 2026-08-18 新来源审计与复用判定（情报专项 · 扩大 Universe）

本轮对 52 个真实来源做了深度枚举（候选包见 [`Curis_Talent_Candidate_Package_2026-08-18.md`](./Curis_Talent_Candidate_Package_2026-08-18.md)）。新增来源与复用判定如下。

### 9.1 新增可直接合法复用候选（公开仓库 + 明确许可证）

| 来源 | 类型 | 许可证 | Curis 判定 |
| --- | --- | --- | --- |
| `anthropics/knowledge-work-plugins` | 11 岗位 Expert/插件 | source-available（非标准 OSI，REVIEW） | 逐插件 LICENSE 复核后入 Adapter；销售/法务/财务/数据/生物研究优先 |
| `msitarzewski/agency-agents` | 跨域 Expert-Team | MIT | 与 agency-agents-zh 同源英文版，扩充语言覆盖 |
| `andrewyng/openworker` | 通用岗位 Expert/Team | MIT | 25+ 连接器 + 预设角色，可直接合法复用候选 |
| `OpenBMB/StaffDeck` | 企业数字员工 | REVIEW | 财务/法务/人事/IT/行政，逐文件复核 |
| `ai4finance-foundation/finrobot` | 金融 Expert-Team | Apache-2.0 | 可逐项导入 |
| `assafelovic/gpt-researcher` | 研究 Expert/Tool | Apache-2.0 | 可逐项导入 |
| `HKUDS/DeepTutor` | 教育 Expert-Team | Apache-2.0 | 可逐项导入 |
| `Biomni` | 生物医学 Expert-Team | Apache-2.0 | 可逐项导入 |
| `phuryn/pm-skills` | 产品 Expert | MIT | 68 PM 技能，可逐项导入 |
| `alirezarezvani/claude-skills` | 跨域 362 Skill/102 Agent | MIT | 作为集合候选，逐条固定 digest 后入 Adapter |
| `huggingface/skills` | ML/科学 Skill 集合 | MIT | 可逐项导入 |
| `vercel-labs/agent-skills` | 前端/设计/安全 Skill 集合 | MIT | 可逐项导入 |
| `K-Dense-AI/scientific-agent-skills` | 科研 135 Skill | REVIEW | 逐文件许可证复核后导入 |
| `obra/superpowers` | 工程 Skill 集合 | REVIEW | 逐文件复核（已知登记来源，本轮深度枚举） |
| `anthropics/skills`、`openai/skills` | 官方 Skill 集合 | source-available / per-skill LICENSE | 逐目录处理，不整体视为可再分发（已知登记来源，本轮深度枚举） |
| `superdesigndev/superdesign` | 设计 Tool | AGPLv3 | 自托管可用；注意强 copyleft |
| `evidence-dev/evidence` | 数据/BI Tool | MIT | 代码化 BI，可自托管导入 |
| `qodo-ai/pr-agent` | Code Review Tool | MIT | 开源 PR 审查，可直接复用候选 |
| `github/github-mcp-server`、`playwright-mcp`、`mongodb-mcp`、`elasticsearch-mcp`、`bigquery-mcp`、`supabase-mcp`、`exa-mcp`、`tavily-mcp`、`firecrawl-mcp`、`notion-mcp`、`atlassian-mcp`、`stripe-mcp`、`alpha-vantage-mcp`、`pubmed-mcp`、`openalex-paper-search` 等 | MCP | MIT/Apache/BSD/AGPL（逐 server） | 明确标注许可证的 server 可复用；AGPL 项（grafana/Metabase/sec-edgar-agentkit）自托管可用 |
| `Composio MCP` / `Zapier MCP` / `Pipedream MCP` | 聚合 Connector | 专有 SaaS | API/Adapter only，凭证只进 Credential Vault，集中凭证须 Security Review |

### 9.2 只能参考 / 不可导入（明确边界）

| 项目 | 判定 | 说明 |
| --- | --- | --- |
| WorkBuddy 私有专家 / 私有 Skill / 连接器 | 只能参考产品设计 | 不可复制 Prompt/知识/内部 API；公开 SkillHub 技能仅参考，不导出为 Curis 资源 |
| Coze 商店公开 Bot / 插件 | 平台内使用 / reference-only | 商店已禁止公开配置导出；不可复制 Bot，仅参考交互与分类 |
| `cat-xierluo/contract-copilot.skill`、`ai-law-shield` | License 硬 BLOCKED | CC BY-NC 4.0，商用需单独授权，Curis 商用不可直接收录 |
| `saminkhan1/realtor-ai` | License REVIEW | GPL-3.0 强 copyleft，链接进专有产品需法律复核 |
| 所有标注 REVIEW 的社区仓库 | 暂不使用直到逐文件复核 | 许可证未明示，先 candidate/blocked |

### 9.3 本轮关键风险结论
- 非商用限制 2 项硬 BLOCKED；~60 项需逐文件许可证复核；~25 项高权限/敏感域（法律/医疗/金融/聚合连接器/安全工具）须 Security Review 后才能接入。
- 聚合连接器（Composio/Zapier/Pipedream MCP）带来“单点接数千应用”的高价值，但集中凭证与 URL 泄露风险高，必须走 Credential Vault + 托管 OAuth，不本地落明文。
- 医疗/法律/金融域候选仅限本地或用户授权数据，禁止伪造“已验证”。
