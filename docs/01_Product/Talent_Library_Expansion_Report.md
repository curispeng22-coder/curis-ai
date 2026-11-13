# Curis 人才库扩充与人才生产线工作报告

Status: Review  
日期：2026-08-14  
所属专项：Curis 人才市场 Phase 2  
依据：Phase 2 用户指令、ADR-0045、Master Map v2.0、Page Map v1.0、人才市场三份专项文档、当前代码扫描证据。

## 1. 本轮结论

人才生产线的只读扫描骨架已经接入现有 `CanonicalAgentSpec`、Agency、CrewAI、OpenClaw 和 MCP Adapter。当前不把扫描资源直接写成 EmployeeTemplate：

```text
公开来源
→ 生产线扫描
→ License / Security Gate
→ CanonicalAgentSpec
→ 去重身份
→ 职业分类
→ 能力组合建议
→ Candidate / BLOCKED
→ 后续验证
→ Curis-ready
```

当前真实事实是：Curis-ready 专家仍为既有 5 个；本轮新增 17 个外部 Agent Candidate，尚未声称可招募。

现有平台 Admin 已增加“人才生产线”只读观察面板，提供 Candidate Queue、成熟度、来源、许可证和安全状态；它不进入普通用户一级导航，也没有自动发布或招募动作。

## 2. 扫描来源

### 已扫描本地公开快照

| 来源 | Adapter | 资源 | 许可状态 | 当前状态 |
|---|---|---:|---|---|
| `jnMetaCode/agency-agents-zh` | AgencyMarkdownAdapter | 12 Agent | MIT 仓库许可；快照待固定 | Candidate |
| CrewAI examples | CrewYamlAdapter | 5 Agent | 逐项复核 | Candidate |
| Curis OpenClaw/Skill 快照 | OpenClawSkillAdapter | 5 Skill | 未声明许可证 | BLOCKED |
| MCP server 快照 | MCPManifestAdapter | 5 MCP | 许可证转型/逐项复核 | Resource Candidate |

### 已登记但尚未导入的公开来源

- [Anthropic Skills](https://github.com/anthropics/skills)：官方 Agent Skills 仓库；仓库说明包含 Apache-2.0 与 source-available 内容，必须逐目录处理，不能整体视为可再分发。
- [OpenAI Skills](https://github.com/openai/skills)：官方来源目录，待许可证和具体目录扫描。
- [Superpowers](https://github.com/obra/superpowers)：开发工作流 Skill 来源，待固定版本和许可证复核。
- [Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)：MCP 来源，必须按 server 和 LICENSE 逐项处理。
- [OpenClaw / ClawHub](https://docs.openclaw.ai/clawhub/quickstart)：公开注册表，不等于资源许可、安全或可运行。

## 3. 扫描计数

生产线本地快照扫描结果：

| 指标 | 数量 |
|---|---:|
| discovered | 27 |
| 去重后 | 27 |
| 重复 | 0 |
| Agent | 17 |
| Skill | 5 |
| MCP | 5 |
| Candidate | 17 |
| BLOCKED | 5 |
| Composed | 0 |
| Validated | 0 |
| Curis-ready（本轮新增） | 0 |

人才市场合计为：5 个既有 Curis-ready + 17 个外部 Candidate。未通过验证的资源不会进入招募动作。

## 4. Agent Candidate 分类

| 分类 | Candidate |
|---|---:|
| 产品 | 3 |
| 增长 | 4 |
| 数据 | 2 |
| 商业 | 5 |
| 内容 | 1 |
| 研发 | 1 |
| 研究 | 1 |
| 设计 | 0 |

真实 Candidate 包括 Product Feedback Synthesizer、Product Trend Researcher、Marketing Content Creator、Content Writer、Code Reviewer、Senior Research Analyst、Growth Strategist 等；没有现成 UI/UX 角色快照时不人工补齐设计分类。

## 5. 能力组合现状

每条 Agent Candidate 已保留：

- 身份、职责、职业分类；
- 来源仓库、路径、快照摘要、许可证状态；
- Security Scan 结果；
- Skill / Tool / MCP 候选；
- Knowledge / Connector / Model requirement 占位字段；
- 工作流步骤数量；
- `recruitable=false` 和当前成熟度。

当前 17 个外部 Agent 都还没有完成 Curis 真实 Skill/Tool 绑定、运行验证和 Evidence，因此 `COMPOSED`、`VALIDATED`、`CURIS_READY` 仍为 0。这个结果是刻意保守的，不以角色文本存在冒充职业能力包完成。

## 6. 阻塞与处理

- 5 个 Skill 快照缺少许可证声明，进入 BLOCKED；不能安装或分配。
- Agency / CrewAI 本地快照尚未固定远端 commit/digest，来源状态为 `pending_snapshot_verification`。
- MCP 许可证存在项目级转型和 server 级差异，必须逐项复核。
- 没有真实模型、Tool、Connector 和业务任务 Evidence 时，不能把 Candidate 升级为 Curis-ready。

## 7. 下一步

1. 固定 Agency/CrewAI/MCP/Skill 快照的 commit、文件 digest 和 LICENSE 路径。
2. 为 17 个 Agent Candidate 生成真实 Skill/Tool 组合建议，并映射到当前 active SkillTemplate / Capability Catalog。
3. 先验证内容、研究、Code Review、增长四类，形成少量 `COMPOSED → VALIDATED` 专家。
4. 只有通过真实 Curis 工作任务、运行证据和失败恢复验证的角色，才进入 `CURIS_READY` 和招募动作。
5. 继续扫描 Anthropic Skills、OpenAI Skills、Superpowers 和 ClawHub，但不因数量压力批量导入。

---

## 8. 2026-08-18 候选扩充轮（情报专项 · 扩大 Universe）

本轮身份为「人才与能力情报负责人」，负责生产线最前端（发现 → 调研 → 整理 → 提供可导入候选），不新建第二套 Registry / Candidate Queue / 能力真源。详细候选包见 [`Curis_Talent_Candidate_Package_2026-08-18.md`](./Curis_Talent_Candidate_Package_2026-08-18.md)。

### 8.1 本轮结论
上一轮（2026-08-14）仅完成来源审计与浅层登记（17 Agent / 5 Skill / 5 MCP），设计/产品/数据·BI/研究/法律/金融/教育/科研等分类偏薄。本轮对 52 个真实来源做了**深度逐目录枚举**，显著扩大候选宇宙，重点补齐了设计、产品、数据/BI、研究、Code Review/QA、增长/营销、金融/财务、法律、科研、教育、医疗、房地产、制造/供应链、咨询/行业研究等专业覆盖。

### 8.2 扫描计数（本轮）

| 指标 | 数量 |
|---|---:|
| 新扫描来源数 | 52 |
| 新发现资源（原始） | ~265 |
| 去重后候选数 | ~250 |
| Expert / Expert-Team 候选 | ~45 |
| Skill 资源 | ~120（含集合：alirezarezvani 362、K-Dense 135、ClawHub 多、官方集合） |
| MCP / Connector | ~55 |
| Tool / Capability Provider | ~45 |
| License 硬 BLOCKED | 2（contract-copilot.skill、ai-law-shield，均为 CC BY-NC 非商用） |
| License REVIEW（需逐项目复核） | ~60 |
| Security Review（高权限/敏感域） | ~25 |
| LOW CURRENT PRIORITY（暂无场景仍收录） | ~30 |

### 8.3 新发现高价值来源（节选）
- `anthropics/knowledge-work-plugins`：官方 11 岗位插件（销售/法务/财务/数据/客服/产品/市场/企业搜索/生物研究/生产力）。
- `msitarzewski/agency-agents`：agency-agents-zh 英文同源（MIT，57K★），扩语言覆盖。
- `andrewyng/openworker`（MIT）、`OpenBMB/StaffDeck`：通用/企业数字员工。
- `ai4finance-foundation/finrobot`（Apache-2.0）、`TauricResearch/TradingAgents`：金融多 Agent。
- `assafelovic/gpt-researcher`（Apache-2.0）、`bytedance/deer-flow`（MIT）：深度研究。
- `HKUDS/DeepTutor`（Apache-2.0）、`Biomni`（Apache-2.0）：教育/生物医学科研。
- `phuryn/pm-skills`（MIT, 68）、`coreyhaines31/marketingskills`：产品/营销方法论。
- `alirezarezvani/claude-skills`（MIT, 362 skill / 102 agent）、`K-Dense-AI/scientific-agent-skills`（135）：跨域/科研。
- 聚合连接器中枢：`Composio MCP`、`Zapier MCP`、`Pipedream MCP`（单点接数千应用）。
- 设计/BI：`v0`、`SuperDesign`、`Evidence`（MIT）、`Metabase`（AGPL）、`Qodo PR-Agent`（MIT）。

### 8.4 处理纪律
- 集合型来源（alirezarezvani 362、K-Dense 135、ClawHub、anthropics/openai/obra）必须**逐条**固定 commit/digest、LICENSE、NOTICE 后再入 CanonicalAgentSpec，不整仓复制。
- 所有 REVIEW 项在许可证/安全未确认前保持 BLOCKED/Candidate，不得宣称可招募或已验证。
- 严禁将“发现候选”冒充 `CURIS_READY`；CURIS_READY 仍须 Codex 能力专项完成真实能力绑定、任务执行与 Evidence 验证。
- 已存在产线（agency-agents-zh 17、先前 5 MCP、5 Skill、已登记仓库）不重复登记，仅做增量枚举。
