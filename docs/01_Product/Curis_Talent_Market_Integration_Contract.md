# Curis 人才市场集成契约

Status: Review  
日期：2026-08-14  
目标：让外部专家、Skill、MCP、Tool、Connector 以可审计、可撤回、可替换的方式进入 Curis Company Resource 体系。

## 1. 核心原则

1. 市场只负责发现和扩展；设置负责授权/维护/撤销；组织中心负责员工；Workspace 负责实际工作。
2. 外部资源先是 Candidate/Imported Draft，经过许可证、安全、来源和能力检查后才能成为可安装资源。
3. 外部 Agent 只保留引用和 Adapter，不复制私有 Prompt、密钥、知识库或受保护配置。
4. Company、Employee、Skill、Capability、Connector、Workspace 继续使用现有对象与租户边界。
5. 任何缺失模型、能力、连接器、权限或资料都必须返回明确的 `WAITING_CEO` / `BLOCKED` 原因，不创建假员工或假连接。

## 2.1 专家招募最低要求

- `Company`：员工必须属于一个合法 Company。
- `Employee identity`：名称、角色身份和可追溯的来源模板必须明确；可选 Avatar 仅用于展示，支持共享 Avatar Pattern 的上传、预置或 fallback，不是招募/创建门槛。
- `Position / Responsibility`：岗位和职责从专家模板带入，允许在招募时确认或调整。
- `Execution capability`：能力可用，或明确记录能力缺口；能力缺口不自动阻止员工进入公司，但会阻止其被误标为可运行。
- `Permission confirmation`：涉及资料、工具、连接器或外部副作用时，必须完成必要权限确认。
- `Department`：可选；有合适部门时推荐，没有部门时使用空归属创建公司级员工。
- `Business / Workspace`：按招募来源和上下文决定是否绑定，不作为所有招聘的统一前置条件。

## 3. Canonical Talent Manifest

这是现有 `CanonicalAgentSpec` 的市场视图，不新增第二套执行规范。外部适配器最终要归一为以下结构：

```json
{
  "manifest_version": "1.0",
  "asset_kind": "expert|skill|connector|agent|mcp|tool",
  "identity": {
    "name": "",
    "role": "",
    "responsibility": "",
    "description": "",
    "use_cases": [],
    "tags": []
  },
  "source": {
    "kind": "curis|github|clawhub|coze_api|workbuddy_api|openclaw|other",
    "uri": "",
    "version": "",
    "entry_path": "",
    "fetched_at": ""
  },
  "license": {
    "spdx": "",
    "commercial_use": false,
    "attribution_required": true,
    "notice_ref": ""
  },
  "execution": {
    "adapter_kind": "curis_template|agency_markdown|openclaw_skill|clawhub_skill|coze_api|mcp|skill|model|agent_api",
    "model_ref": "",
    "agent_ref": "",
    "workflow_ref": ""
  },
  "composition": {
    "skill_refs": [],
    "tool_refs": [],
    "mcp_refs": [],
    "knowledge_refs": [],
    "connector_refs": [],
    "subagent_refs": []
  },
  "permissions": {
    "effect_classes": [],
    "data_scopes": [],
    "requires_ceo_approval": true
  },
  "security": {
    "scan_status": "pending|pass|fail",
    "credential_patterns": [],
    "prompt_injection_flags": [],
    "overclaim_flags": []
  },
  "curis": {
    "disposition": "candidate|draft|installable|blocked|archived",
    "employee_template_id": "",
    "created_from_template_id": ""
  }
}
```

## 4. 适配器契约

每个来源适配器实现同一组动作：

```text
discover(source_ref) → SourceEntry[]
fetch(SourceEntry) → raw config / API metadata
parse(raw) → CanonicalAgentSpec
security_scan(spec) → pass/fail + findings
license_gate(spec) → allow / draft / block
map(spec) → existing Curis template/capability/resource refs
```

现有可复用实现：

- `AgencyMarkdownAdapter`：公开 Agent Markdown。
- `CrewAIAdapter`：公开 crew YAML。
- `SkillRepoAdapter`：`SKILL.md`。
- `MCPManifestAdapter`：MCP JSON。
- `CanonicalAgentSpec`：统一中间表示。
- `sanitize.py` / `security_scan.py`：文本和风险扫描。
- `seed.py` / `seed_multisource.py`：opt-in、可回滚、draft/candidate 资产。

新增来源的最低要求是复用这些边界，不另建 Source/License/Security 逻辑。

需要补充的最小适配器：

- `OpenClawSkillAdapter`：读取公开 `SKILL.md` 与支持文件，保留来源/版本/锁文件信息；可复用现有 `SkillRepoAdapter` 的解析和安全边界。
- `ClawHubAdapter`：只负责公开注册表发现、版本和来源元数据，不绕过 CLI/权限、不自动安装。

## 5. 现有 Curis API 映射

### 市场读侧

| 用途 | 现有端点 | 事实边界 |
| --- | --- | --- |
| 专家模板 | `GET /api/workspace/employee-templates` | 只返回当前租户可见模板；active 才可招募 |
| 技能 | `GET /api/workspace/skills/templates` | active SkillTemplate；来源/状态必须展示 |
| 能力目录 | `GET /api/workspace/capabilities/registry` | 能力元数据，不等于连接/健康/授权 |
| 连接器运行目录 | `GET /api/connectors` | 当前 registry 与 mock/real 模式，不等于已授权 |
| 公司/部门/员工 | `GET /api/workspace/companies`、`GET /api/workspace/departments`、`GET /api/workspace/employees` | 组织事实源 |

### 招募/装配写侧

| 动作 | 端点 | 要求 |
| --- | --- | --- |
| 创建员工 | `POST /api/workspace/employees` | 必须有合法 company_id、Employee identity、岗位/职责和 active template_id；department_id 可为空；失败不落半成品 |
| 绑定能力 | `PUT /api/workspace/employees/{id}/capabilities` | 走现有岗位 effect_class 授权器 |
| 绑定 Skill | `PUT /api/workspace/employees/{id}/skills` | 只接受当前租户可见且 active 的 SkillTemplate |
| 读取员工 Skill | `GET /api/workspace/employees/{id}/skills` | 作为安装/分配后的持久化证据 |
| 读取员工能力 | `GET /api/workspace/employees/{id}/capabilities` | 作为必要能力检查证据 |
| Skill 纳入公司 | `POST /api/workspace/skills/templates/{id}/install` | 幂等复制官方 Skill 为 tenant_private，保留来源引用；不复制密钥 |
| 外部 Coze Agent | 未来 `POST /api/workspace/external-agents` | 只存 adapter + opaque credential_ref + 外部 ref；当前不伪造端点 |

## 6. 招募装配状态

```text
DISCOVERED
→ DETAIL_OPEN
→ RECRUITING
→ ROLE_SELECTED
→ COMPANY_CONTEXT_CHECK
→ CAPABILITY_CHECK
→ CEO_CONFIRM_REQUIRED
→ EMPLOYEE_CREATED
→ SKILLS_BOUND
→ ORG_VISIBLE
→ WORKSPACE_READY
```

失败状态：

- `BLOCKED_COMPANY_REQUIRED`
- `BLOCKED_TEMPLATE_INACTIVE`
- `BLOCKED_AUTHORIZATION_REQUIRED`
- `FAILED_ROLLBACK_REQUIRED`

`BLOCKED_REQUIRED_CAPABILITY` 是能力检查结果，不是统一的入职失败条件：员工可以先创建并进入组织中心，同时明确标记为暂不可运行，等待后续补齐能力。

部门不是必经状态：

- 有合适的现有部门时，在装配面板自动推荐，可选择绑定。
- 没有部门时，`department_id` 为空，员工仍可直接创建并进入公司和组织中心。
- 后续随着责任重复和组织成长，再把员工归入已有部门或成立新部门。
- Business / Workspace 是否绑定由招募来源和上下文决定，不是所有招聘的统一前置条件。

任何失败都保留原因并回到装配面板；能力缺口可以作为显式缺口随员工创建返回，不把缺口伪装成已可运行。

## 7. Skill 安装契约

- 官方 Skill：安装操作必须幂等；落成 tenant_private 副本或明确标记为当前公司已拥有，保留 `created_from_template_id`、来源、许可证和版本。
- 公开 Skill：只有完成来源、许可证、安全扫描后允许安装；无许可证进入 `draft/blocked`，不能分配给员工。
- Skill 不选择 Model、不解析 Credential、不自行执行；现有 `SkillRuntime` 只提供安全 Instruction excerpt 和绑定关系。
- 分配给员工后必须通过现有 `prompt_excerpt(employee_id)` 进入运行时上下文；真实执行还要通过 Employee Capability Binding 和 Runtime Gate。

## 8. Connector 契约

- 市场展示 Connector 元数据和权限范围，不保存明文凭证。
- 安装是发现/注册动作；授权只在设置完成。
- 只有凭证存在、健康检查通过、租户/公司范围匹配时才显示“可用”。
- mock connector 只能标记为本地同构/演示，不升级为真实连接。
- Connector 的外部副作用必须有 effect class、CEO confirmation 和审计。

## 9. 外部 Agent / Coze Adapter

最小运行契约：

```text
Curis Employee/Workspace request
→ Adapter validates tenant + credential_ref + external_ref
→ external API/SDK call
→ normalize status / output / evidence / usage
→ existing Result/Evidence/CEO decision chain
```

Adapter 不得：

- 读取或复制外部平台的私有 Prompt/Knowledge/凭证。
- 通过抓包、逆向、绕过权限获取 Agent 配置。
- 把 API 可调用误报为已经完成 Curis 员工化或 Workspace 运行。
- 绕过现有 Company/Tenant/Capability/Approval 边界。

公开 OpenClaw/WorkBuddy 生态的额外门禁：

- `agency-agents-zh` 等 MIT/Apache 资源可进入 `candidate`，但仍需逐文件许可证、脚本、依赖、网络和凭证扫描。
- ClawHub 条目必须记录 owner、slug、version、digest/origin，并保留可回滚版本；注册表存在不等于安全或可再分发。
- WorkBuddy 私有专家、私有知识和内部 API 不进入 Adapter；只有公开文件或正式授权 API 才能进入 Curis。

## 10. 验收门

### 资源门

- 来源 URI、版本、许可证、署名和安全扫描可追溯。
- 无明文凭证、隐含越权、Prompt Injection 未处理项。
- active / draft / blocked / archived 状态与 UI 一致。

### 产品门

- 专家发现→详情→招募→EmployeeInstance→组织中心可见。
- Skill 发现→安装→分配→Skill API/Runtime 可读。
- Connector 发现→设置入口；授权/健康未完成时不显示已连接。

### Runtime 门

- 刷新/重启后关系持久化。
- 跨租户、模板失效、能力缺失、授权失败 fail-closed。
- 真实对话/工作必须使用现有 Runtime 与 Evidence 规则；页面、API 200、静态卡片和 mock 不构成完成。

## 11. 2026-08-14 实现回写与现场验收路径

### 已落地的接口与资源

- `GET /api/workspace/talent-market/external-candidates`：只读返回五个公开 Candidate 及来源、许可证、安全扫描和安装/招募门禁。
- `POST /api/workspace/talent-market/recruit`：复用 EmployeeTemplateContract 创建 EmployeeInstance；Department 为空时仍可进入 Company，随后写入默认 Skill Binding 并尝试绑定默认 Tool。
- `POST /api/workspace/skills/templates/{id}/install`、`PUT /api/workspace/employees/{id}/skills`：完成官方 Skill 的 Company Resource 安装和 Employee Binding；员工详情通过 GET 读取持久化绑定。
- `OpenClawSkillAdapter`：发现本地 `SKILL.md`、计算 supporting files 摘要、读取许可证并执行安全初扫；不执行文件。
- `ClawHubAdapter`：要求 owner、slug、version、digest、origin 齐全；只解析公开注册表元数据，不下载、不安装、不授权。

### 现场验收

1. 打开 `/ceo-office/talent-market`，在专家 Tab 看到 Curis-ready 五岗位和公开 Candidate。
2. 选择 Curis-ready 专家，在右侧招募装配中选择 Company；Department 可保持“暂不归属部门”。
3. 确认招募后打开组织中心和员工详情，检查 EmployeeInstance、默认 Skill/Tool Binding 与能力缺口。
4. 在技能 Tab 安装一个 active Skill，再选择员工分配；刷新员工详情，检查 Skill Binding 仍存在。
5. 从员工详情进入现有执行中心；若没有 Workspace/Project/模型/权限上下文，验收结果应为真实阻塞，而不是伪造成功。

### 未完成项

- Candidate 固定版本后的真实 Installable/Recruitable 转换。
- Connector 的设置授权、健康检查、Company Resource 绑定和 Employee/Workspace 分配。
- 用户自有 Coze Agent 的真实授权输入与一次外部调用证据。

## 12. Phase 2 资源与人才成熟度契约

### 资源与人才分层

- Prompt、Agent、Skill、MCP、Tool 首先进入 Resource Candidate Pool。
- 只有完成职业分类、Skill/Tool/MCP 关联、Knowledge/Connector/Model requirement 和适用场景分析后，才形成 Expert Candidate。
- `CURIS_READY` 需要通过真实能力依赖检查、Curis 工作任务、结果/Evidence 和失败恢复验证；资源扫描本身不能升级成熟度。

### Canonical Identity

每条资源必须保留 `source`、`repository`、`path`、`version/commit`、`digest` 和 `license`。相同来源、路径、版本和摘要的资源去重；同名但来源或内容不同的资源保留差异并提示合并建议。

### 生产线输出

生产线只读消费现有 Adapter，输出 `DISCOVERED`、`CANDIDATE`、`COMPOSED`、`VALIDATED`、`CURIS_READY`、`BLOCKED`。它不直接写 EmployeeTemplate、SkillTemplate 或 EmployeeInstance；发布和招募继续走现有资源与组织契约。

---

## 13. 2026-08-18 候选包导入交接（给 Codex 能力专项）

本轮情报专项产出结构化候选包 [`Curis_Talent_Candidate_Package_2026-08-18.md`](./Curis_Talent_Candidate_Package_2026-08-18.md)，含 ~250 条去重后候选（Expert ~45 / Skill ~120 / MCP·Connector ~55 / Tool ~45）。交接约束：

### 13.1 接入边界（沿用 §4 适配器，不另建 Source/License/Security 逻辑）
- 复用 `AgencyMarkdownAdapter`（Agent Markdown）、`SkillRepoAdapter`（SKILL.md）、`MCPManifestAdapter`（MCP JSON）、`CanonicalAgentSpec`、`sanitize.py` / `security_scan.py`。
- 新增来源须先 `discover → fetch → parse → security_scan → license_gate → map`，再入 `candidate/draft`；不整仓复制。

### 13.2 许可证与去重硬规则
- 硬 BLOCKED（非商用）：`cat-xierluo/contract-copilot.skill`、`ai-law-shield`（CC BY-NC 4.0），Curis 商用不可直接收录。
- REVIEW（~60）：所有“未明示”社区仓库、anthropics source-available、openai 每 skill LICENSE、obra/K-Dense/Trail of Bits/ClawHub per-skill、n8n Sustainable Use、专有 SaaS；逐文件固定 LICENSE/NOTICE 后才可转 installable。
- Canonical Identity 去重：相同 `source + path + version + digest` 合并；已存在产线（agency-agents-zh 17、先前 5 MCP/5 Skill、已登记仓库）不重复登记，仅增量枚举。

### 13.3 Security Review（~25）
高权限/数据出域/敏感域（api-gateway、agent-browser、imap-smtp-email、coding-agent、Zapier/Composio/Pipedream MCP、WorkBuddy/Coze 连接器、Trail of Bits 安全系列、法律/医疗/金融敏感数据处理类）须先做 Prompt 注入/凭证/过度承诺扫描；敏感域仅限本地或授权数据，禁止伪造“已验证”。

### 13.4 CURIS_READY 纪律（不可逾越）
候选包内所有条目均为 Candidate。**严禁将“发现候选”冒充 `CURIS_READY`**。晋级必须：真实 Skill/Tool 绑定 → Curis 工作任务执行 → Evidence → 失败恢复验证，且通过现有 Runtime/Evidence 规则与 §10 验收门。当前本轮新增 Curis-ready = 0。

### 13.5 推荐优先导入（首批进入 CanonicalAgentSpec / SkillTemplate / Capability 适配）
`anthropics/knowledge-work-plugins`、`msitarzewski/agency-agents`、`andrewyng/openworker`、`OpenBMB/StaffDeck`、`ai4finance-foundation/finrobot`、`assafelovic/gpt-researcher`、`HKUDS/DeepTutor`、`Biomni`、`phuryn/pm-skills`、`coreyhaines31/marketingskills`、`YUHAO-corn/manufacturing-agents`、`anthropics/skills`、`openai/skills`、`obra/superpowers`、`huggingface/skills`、`K-Dense-AI/scientific-agent-skills`、`vercel-labs/agent-skills`、`alirezarezvani/claude-skills`、官方 MCP 服务器、`Composio/Zapier MCP`、`Evidence`、`Qodo PR-Agent`、`v0`/`SuperDesign`。
