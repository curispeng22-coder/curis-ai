# Curis AI 能力接入专项集成报告

Status: Review  
Updated: 2026-08-15  
Issue: `issues/20260814_ai_capability_integration_001.md`  
Overall: `COMPUTER ACCESS AUTHORITY SYNCED / CAPABILITY ECOSYSTEM RUNTIME PARTIAL` — Computer Access Contract 已批准并进入权威链；Runtime Delta 只规划未实现。

## 1. 本轮结论

停止按品牌逐个扩 Provider/Agent。Curis 复用现有 New API、Model Gateway、Capability、Talent/Skill 生产线、MCP/Connector adapter、Employee Binding、Task/Usage/Artifact Runtime，收口为：

```text
Model / Skill+Expert / MCP+Connector / External Agent
                        ↓
              Capability / Binding
                        ↓
              Employee / Workspace
                        ↓
          existing Runtime / Usage / Artifact
```

没有创建第二套模型、Skill、MCP、Agent、Employee 或 Runtime；没有修改 Product Blueprint、UI Blueprint、Master Map、Page Map或一级导航。

Local Agent Computer Access 已由 ADR-0046 冻结：用户侧只显示“请求批准 / 自动处理（推荐默认）/ 完全访问”；内部由 requested_intent、Adapter mapping、provider-native permission 与 Session effective evidence 保证真实。它不属于 CEO Decision 或 Business Authority。

## 2. 四个核心 Registry

| Registry | 当前作用 | 产品原则 |
| --- | --- | --- |
| `Model_Provider_Registry.md` | 18 个 Runtime Provider Definition + 企业平台研究项 | 普通用户官方 BYOK；New API/OpenRouter/compatible 为高级聚合；本地模型独立；未来 PLATFORM 来源上层无感 |
| `Skill_Expert_Registry.md` | 统一 Skill 来源治理、Expert 组合与成熟度 | Expert != Employee；扫描/Candidate 不等于 Curis-ready |
| `MCP_Connector_Registry.md` | 标准 MCP transport/auth 与 Connector 状态 | stdio/Streamable HTTP 标准优先；manifest/registry 不等于授权可用 |
| `Agent_Adapter_Compatibility_Registry.md` | 内部 Agent discovery/interface/auth/session/permission 兼容矩阵 | 前台只显示实际 detected/connected；稳定机器接口优先；不做 GUI automation |

## 3. AI CAPABILITY ECOSYSTEM STATUS

### Model Ecosystem

| Readiness | 项目 |
| --- | --- |
| LIVE | Ollama：真实发现 2 个模型，Employee → Runtime → Artifact PASS；现有 New API/Gateway 路由继续保留 |
| READY | 18 个 Provider Definition；OpenAI-compatible、Anthropic Messages、Gemini generateContent 协议路径 |
| DISCOVERABLE | 动态模型列表 Provider 与本机 Ollama/LM Studio 扫描 |
| RESEARCHED | 百度千帆、腾讯混元/TokenHub、AWS Bedrock、Microsoft Foundry/Azure OpenAI |
| BLOCKED | 所有云 BYOK 尚无真实 Key；Desktop USER credential 仅进程内存 |
| UNKNOWN | 未进入 Registry 的长尾 Provider/模型能力/版本化价格 |

### Skill / Expert Ecosystem

| Readiness | 项目 |
| --- | --- |
| LIVE | 55 个 active SkillTemplate 的现有发现/纳入/员工绑定链；Curis 官方专家模板招募链 |
| READY | 现有 `SkillRepoAdapter` / `OpenClawSkillAdapter` / 来源安全边界，等待逐项真实验证 |
| DISCOVERABLE | 17 个外部 Agent Candidate；公开来源只读生产线 |
| RESEARCHED | Agent Skills 开放规范、GitHub Copilot Agent Skills、Anthropic Skills、ClawHub/GitHub 来源 |
| BLOCKED | 5 个无明确许可证 Skill；外部扫描资源新增 Curis-ready 为 0 |
| UNKNOWN | 未审计来源、依赖与真实任务质量 |

### MCP / Connector Ecosystem

| Readiness | 项目 |
| --- | --- |
| LIVE | 本轮无真实外部 MCP 垂直 Evidence |
| READY | 现有 stdio `initialize + tools/call` 最小 adapter；AiToEarn/SocialAutoUpload 既有 connector code path |
| DISCOVERABLE | 5 个 MCP manifest Candidate |
| RESEARCHED | MCP Official Registry、GitHub/Notion/Figma MCP、filesystem/fetch/git/memory/time 参考类别、常见业务 Connector 类别 |
| BLOCKED | Streamable HTTP、OAuth、动态 tool/resource discovery 与真实授权调用尚未实现/验证 |
| UNKNOWN | 每个第三方 server 的许可证、供应链、权限、数据驻留和生产健康 |

### External Agent Import Ecosystem

| Readiness | 项目 |
| --- | --- |
| LIVE | Codex 本机 scan、auth、new、resume、Employee/Workspace → Runtime → Artifact；Computer Access effective evidence 仍为 PARTIAL |
| READY | 通用 Agent Import/Execution Binding/Result/Usage/Artifact contract；Registry 驱动 local discovery |
| DISCOVERABLE | 普通用户扫描当前只返回实际 detected 的 Codex；未安装品牌不显示 |
| RESEARCHED | Claude Code、TRAE Agent、Cursor CLI、OpenClaw、Gemini CLI、GitHub Copilot CLI、Coze |
| BLOCKED | 其他 Agent 缺本机安装/授权/真实执行；GUI-only 没有稳定接口时不支持 programmatic import |
| UNKNOWN | 其他 Agent 未核对版本的 session/cancel/permission mapping；当前 Codex resume effective access 未验证 |

## 4. Unified Capability Ecosystem Matrix

| Category | Name | Source/Vendor | Region | Discovery | Connection Method | Capability | Current Status | Real Evidence | UI Position | Employee Bindable | Workspace Usable | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Ollama | Ollama | Local | `/api/tags` | loopback HTTP | local chat models | LIVE | 2 models + Employee Runtime Artifact | 设置 → AI 与能力 → 模型/本地 | 是 | 是 | 保持现有链 |
| Model | Official BYOK group | 13 vendors | China/Global | dynamic/curated | official API Key | model inference | READY/BLOCKED | 协议测试；无真实 Key | 设置 → AI 与能力 → 模型 | 否，连接前 | 否 | secure credential + 一个真实 Key 验证 |
| Model Gateway | New API/OpenRouter/compatible | user/vendor | China/Global | `/v1/models` | Base URL + API Key | aggregated models | READY | 既有 router/catalog；无本轮用户 gateway | 高级 / 聚合网关 | 连接后 | 连接后 | 有真实 endpoint 时验证 |
| Skill | Active SkillTemplate | Curis | Local | existing API | install to Company | reusable skill | LIVE | 55 active + binding chain | 人才市场 → Skill | 是 | 是 | 保持权威链 |
| Expert | Curis expert templates | Curis | Local | Talent Market | recruit | role composition | LIVE | 现有模板招募链 | 人才市场 → 专家 | 招募后 | 依赖能力 | 用真实任务继续验证 |
| Skill Candidate | Public `SKILL.md` | GitHub/OpenClaw | Global | source adapter | import | skill package | BLOCKED | 5 scanned，license missing | 内部候选/审核 | 否 | 否 | 许可证与安全逐项审核 |
| MCP | MCP manifests | public/local snapshots | Global/Local | manifest | stdio | external tools | DISCOVERABLE | 5 candidates；无真实 vertical | 设置 → AI 与能力 → 连接 | 否 | 否 | 验证一个低风险 server |
| Connector | AiToEarn/SocialAutoUpload | existing OSS/adapters | Local/self-hosted | registry | HTTP/service | content/publish | READY | code path；无本轮真实 external Evidence | 设置 → AI 与能力 → 连接 | 门禁后 | 未由本轮证明 | 有授权测试环境时验证 |
| Agent | Codex | OpenAI | Global/Local | PATH + auth probe | CLI JSONL | coding agent | LIVE | new/resume + Runtime Artifact | 添加 Agent → 检测本地 | 是 | 是 | cancel 按需 |
| Agent | Claude/TRAE/Cursor/OpenClaw/Gemini/Copilot | vendors | China/Global | internal adapter probes | stable CLI/API | external agent | RESEARCHED | 官方接口研究；当前无本机执行 | 仅检测到后显示 | 否 | 否 | 实际安装/授权时逐项验证 |
| Agent | Remote Agent/Coze | vendor/user | Cloud | user import | API/opaque ref | external agent | RESEARCHED | contract only | 添加 Agent → 导入/连接 | 否 | 否 | 有 published object + credential 后验证 |
| Agent | GUI-only product | vendor | Local | app/process | unsupported | detection only | BLOCKED | detection 不等于 interface | 检测结果详情 | 否 | 否 | 显示 unsupported，不做 UI automation |

## 5. 真实 Runtime 证据

### Ollama

- 本机 Ollama `0.32.9` 动态发现 `gemma4:e2b`、`qwen3.5:9b`；真实 compatible 调用返回 `CURIS_OLLAMA_PROVIDER_OK`。
- 隔离 SQLite 中 Employee 绑定后 Task 完成，输出 `CURIS_OLLAMA_EMPLOYEE_OK`，Artifact 数 1。

### Codex

- 本机 `codex-cli 0.144.6`，read-only 临时 git workspace。
- 新 session、同 session resume 与 usage/session 均已真实验证；permission 只证明 Adapter 请求值回显，不能作为 effective evidence。
- Employee/Workspace Task 完成并回收 1 个 Artifact。
- Resume 当前没有重新声明或验证权限；该缺口进入 Computer Access Runtime Delta P0。

以上 ID 与数据来自隔离临时环境，不是生产 Company 数据。

## 6. 验证

- 本轮 Registry/local discovery 聚焦回归：`11 passed in 0.15s`。
- 先前专项聚焦回归：`47 passed`；Provider/Agent/protocol 原聚焦组曾为 `9 passed`，本轮新增两项 discovery guard 后为 11。
- 既有更宽模型套件仍有基线环境相关失败：missing-secret 预期 401、dotenv 环境实际 502；未把该失败计为专项通过，也未扩大范围修正。

本轮新增 guard 证明：未安装 Agent 不返回；仅检测到 GUI 且无稳定机器接口时不可导入。

## 7. UI Contract

`AI_Capability_UI_Contract.md` 现在提供：

- 稳定 Product State 与生态 Readiness；
- Provider/Model、Skill/Expert、MCP/Connector、Agent、Employee Binding 卡片数据；
- Connection/Authorization/Health/ModelList/Capability Profile；
- `DETECT_LOCAL`、通用 `IMPORT`、INSTALL/RECRUIT/CONNECT/BIND 等动作门禁；
- Computer Access 的“请求批准 / 自动处理（推荐）/ 完全访问”三档与“需要外部设置 / 当前不支持 / 无法确认”真实状态；
- loading/empty/error/partial/return/session-only credential 状态。

它只供前端设计消费，不是最终 UI，不修改 Blueprint，也不把 `RESEARCHED`/`DISCOVERABLE` 变成可用。

## 7A. Computer Access Authority Sync

当前权威：

- Frozen Decision：`docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`；
- Adapter Contract：`docs/01_Product/Agent_Adapter_Contract.md` §3；
- UI Contract：`docs/01_Product/AI_Capability_UI_Contract.md` §5.6；
- 动态兼容性事实：`docs/01_Product/Agent_Adapter_Compatibility_Registry.md` §3；
- 当前事实：`docs/00_Context/CURRENT_STATE.md` §12a。

三份 Research/Candidate/Mapping 文档已降为 Deprecated 的 Review Record / Reference，不再承担定义。

Runtime 仅形成 `docs/04_Development/AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md`：

- P0：Codex requested/effective、resume 重新声明/验证、effective evidence；
- P1：Registry configurability、Execution Binding requested_intent、Session snapshot；
- P2：其他 Agent 只在真实 Adapter 出现后逐个 mapping。

Full Computer Access 继续禁止真实开启，直到对应 Adapter 具有真实 `apply + verify`。

## 8. 下一步顺序

P0：完成 Desktop secure USER credential persistence，并用一个真实官方 Provider Key 做 connect/discover/call/leak audit。  
P1：Product/Frontend Review 四类 Registry 与 UI Contract。  
P2：用一个低风险 stdio MCP 做 Employee/Workspace → Runtime → Artifact 闭环，再决定 Streamable HTTP/OAuth Issue。  
P3：只有当目标机器实际安装并授权某 Agent 时，才按 Compatibility Registry 接通对应 adapter。  
P4：外部 Skill/Expert 按许可证、安全、真实任务与恢复 Evidence 逐项升级，不追求数量。  
P5：PLATFORM Credential、Curis managed gateway、套餐与商业计费留给未来 Cloud Issue。

## 9. Review 结论

当前四个生态的产品位置、Registry、真实状态和上层统一 Binding 已确定；Computer Access Contract 已批准并同步权威体系。接入深度仍受真实 credential、安装环境、许可证、MCP 协议与 Adapter effective evidence 限制。

`AGENT COMPUTER ACCESS AUTHORITY SYNC REVIEW REQUIRED / RUNTIME DELTA PLANNED`
