# Curis AI Capability UI Contract

> 2026-09-15 Disposition: **CONSUMED SUBSET / PROVENANCE — NOT DEFAULT CURRENT INPUT**。
> 模型能力三态、连接/用途/权限/渐进披露及Browser/专业工具等已接受产品语义已写入[Current Authority](../03_Design/Curis_Company_OS_Shared_Authority.md)及当前Master Map/UI Blueprint。下文保留原Review/历史实现/未接受候选，不整篇升级Frozen；发生冲突只消费已回写Current正文。原ADR-0046已Frozen部分继续按ADR，G1-V～G6-V未验。


Status: Review  
Updated: 2026-08-15  
Source: AI Capability Integration 专项指令、ADR-0046、现有 Provider Registry、Agent Adapter Contract、New API/Gateway、Local Discovery、Employee Binding、Task/Usage/Artifact Runtime 与本机真实验证证据。  
Review Gate: `CAPABILITY ECOSYSTEM REVIEW REQUIRED`
Frozen Scope: §5.6 的 Computer Access 三档、真实状态与渐进式暴露由 ADR-0046 冻结；这不表示权限 UI 或 Runtime 已实现。

## 1. 目的与边界

本文件定义前端设计可以消费的 AI 能力数据、状态和动作权限，不是 UI Blueprint，也不规定最终视觉稿。

当前策略是：

> 完整产品先定形，真实能力分阶段接通。

前端可以为确定需要的 Provider、Model、Agent、Connection、Authorization 与 Employee Binding 设计完整产品位置，但必须显示真实状态；未连接、未安装、未授权或尚未接入的能力不得伪装成可用。

本契约不新增第二套 Provider/Model/Agent Runtime，不修改 Product Blueprint、UI Blueprint、Prototype 或一级导航。运行事实继续来自现有 Registry、Gateway、Credential、Binding、Agent Adapter 与 Task/Artifact 链。

Skill/Expert、MCP/Connector 与外部 Agent 的详情分别来自本专项四个 Registry；本文件只定义统一前端投影，不复制其来源或 Runtime。

## 2. 产品入口

| 用户意图 | 产品位置 | 边界 |
| --- | --- | --- |
| 维护模型、Agent 与 Connector | 头像 → 设置 → AI 与能力 | 配置、授权、健康、默认选择与限制；Agent 只显示真实检测/连接结果 |
| 发现 Skill 与可招聘专家 | 人才市场 | Skill、Expert 分层；Expert 招募后才成为 Employee |
| 连接 MCP/Connector | 设置 → AI 与能力 → 连接 | 标准协议优先，逐项授权与最小权限 |
| 实际使用能力 | Employee Workstation / Workspace | 通过 Employee Execution Binding 使用，不暴露 Runtime 内部结构 |
| 首次缺少必要能力 | Onboarding / Contextual Missing Capability | 给出最短恢复动作，并允许返回原工作 |

不得新增 `AI Center`、`Model Center` 或 `Agent Center` 一级产品入口。

## 3. Canonical Product State

### 3.1 `CapabilityProductState`

| Enum | 用户含义 | 进入条件 |
| --- | --- | --- |
| `AVAILABLE` | 已连接并可使用 | `available=true`，且当前使用所需配置、授权、健康条件均满足 |
| `NOT_CONNECTED` | 产品支持，但用户尚未连接 | 远端 Provider/Agent 尚无用户连接或 credential reference |
| `NOT_INSTALLED` | 本地能力未安装或未检测到 | 本地 CLI/App/Service `detected=false` |
| `AUTH_REQUIRED` | 已发现或已配置，但需要授权 | 需要授权且 `authorized=false` 或授权已失效 |
| `CONFIG_REQUIRED` | 需要补充配置 | 已选择能力，但 Base URL、external ref、model 或必要参数缺失 |
| `HEALTH_UNKNOWN` | 已配置，但当前健康未知 | 配置和授权条件满足，尚未成功完成 health/test probe |
| `UNAVAILABLE` | 当前环境不可使用 | probe 明确失败、版本不兼容或必要服务不可达 |
| `COMING_LATER` | 产品位置已确定，当前版本尚未接入 | 只有产品占位/契约，没有当前可执行实现 |
| `BLOCKED` | 存在明确阻塞 | 有可说明的外部或安全阻塞，且当前动作不能在本产品内恢复 |
| `UNKNOWN` | 当前无法确认 | 证据缺失、扫描异常或状态源冲突 |

### 3.2 状态映射优先级

`detected`、`configured`、`authorized`、`healthy`、`available` 都使用 `true | false | null`；`null` 表示未探测、不适用或无法确认，不能自动当作 `false` 或 `true`。

按下列优先级得到唯一产品状态：

1. 有正式版本占位但无执行实现 → `COMING_LATER`。
2. 有明确不可恢复阻塞 → `BLOCKED`。
3. `available=true` → `AVAILABLE`。
4. 本地能力且 `detected=false` → `NOT_INSTALLED`。
5. 远端能力且 `configured=false`、尚未建立连接 → `NOT_CONNECTED`。
6. 必要配置缺失 → `CONFIG_REQUIRED`。
7. 需要授权且 `authorized=false` → `AUTH_REQUIRED`。
8. 配置和授权满足，但 `healthy=null` → `HEALTH_UNKNOWN`。
9. health/test 明确失败或必要服务不可达 → `UNAVAILABLE`。
10. 其余无法从证据确定 → `UNKNOWN`。

硬规则：`Detected != Available`。模型被发现也只证明 catalog visibility，不证明 Authorized、Healthy、Binding 或真实执行成功。

## 4. Shared State Types

```ts
type CapabilityProductState =
  | "AVAILABLE" | "NOT_CONNECTED" | "NOT_INSTALLED"
  | "AUTH_REQUIRED" | "CONFIG_REQUIRED" | "HEALTH_UNKNOWN"
  | "UNAVAILABLE" | "COMING_LATER" | "BLOCKED" | "UNKNOWN";

type ConnectionState =
  | "CONNECTED" | "DISCONNECTED" | "CONNECTING"
  | "DISCONNECTING" | "ERROR" | "UNKNOWN";

type AuthorizationState =
  | "NOT_REQUIRED" | "AUTHORIZED" | "UNAUTHORIZED"
  | "AUTHORIZING" | "EXPIRED" | "UNKNOWN";

type HealthState =
  | "HEALTHY" | "DEGRADED" | "UNHEALTHY"
  | "NOT_TESTED" | "UNKNOWN";

type EvidenceLevel = "REAL" | "PROTOCOL_TEST" | "CONTRACT_ONLY" | "NONE";
type ExposureLevel = "PRIMARY" | "DETAIL" | "ADVANCED" | "INTERNAL";
type EcosystemReadinessStatus =
  | "LIVE" | "READY" | "DISCOVERABLE"
  | "RESEARCHED" | "BLOCKED" | "UNKNOWN";
```

状态枚举是稳定的机器值；简体中文文案由前端映射，不把中文标签写回业务状态。

## 5. Frontend Data Contract

### 5.1 `CurrentLimitation` 与 `RecommendedNextAction`

```ts
type CurrentLimitation = {
  code: string;
  message: string;                 // 可直接给普通用户阅读，不含 secret/内部异常正文
  recoverable: boolean;
  exposure: "DETAIL" | "ADVANCED";
};

type RecommendedNextAction = {
  action: CapabilityAction;
  label: string;
  enabled: boolean;
  reason?: string;
};

type CapabilityAction =
  | "CONNECT" | "AUTHORIZE" | "CONFIGURE" | "TEST"
  | "USE" | "BIND_EMPLOYEE" | "RESUME_SESSION" | "DISCONNECT"
  | "DETECT_LOCAL" | "IMPORT" | "INSTALL" | "RECRUIT"
  | "SET_COMPUTER_ACCESS" | "OPEN_EXTERNAL_AGENT_SETTINGS";
```

### 5.2 `CapabilityProfile`

```ts
type CapabilitySupport = "SUPPORTED" | "UNSUPPORTED" | "UNKNOWN";

type CapabilityProfile = {
  features: Record<string, CapabilitySupport>;
  evidence: EvidenceLevel;
  evidence_source?: string;
  location: "CLOUD" | "LOCAL" | "HYBRID" | "UNKNOWN";
  context_limit?: number | null;
  cost: { status: "KNOWN" | "UNKNOWN"; source?: string };
};
```

不得根据品牌名推断 `SUPPORTED`。当前只有真实 Provider API、协议测试或真实执行证据能提高 evidence level。

### 5.3 `ModelList`

```ts
type ModelList = {
  state: "NOT_LOADED" | "LOADING" | "LOADED" | "ERROR";
  items: Array<{
    id: string;
    name: string;
    capability_profile: CapabilityProfile;
    selectable: boolean;
    limitation?: CurrentLimitation;
  }>;
  count: number | null;
  discovered_at?: string;
  error_message?: string;
};
```

`count=null` 表示未发现/无法确认；`count=0` 只在已成功发现且返回空列表时使用。

### 5.4 `ProviderCardState`

```ts
type ProviderCardState = {
  id: string;
  name: string;
  category: "OFFICIAL_BYOK" | "ADVANCED_GATEWAY" | "LOCAL_MODEL" | "FUTURE_PLATFORM";
  status: CapabilityProductState;
  connection: ConnectionState;
  authorization: AuthorizationState;
  health: HealthState;
  configured: boolean | null;
  authorized: boolean | null;
  model_count: number | null;
  credential_requirement: "REQUIRED" | "OPTIONAL" | "NOT_REQUIRED" | "PLATFORM_MANAGED";
  credential_persistence: "SESSION_ONLY" | "PERSISTENT" | "PLATFORM_MANAGED" | "UNKNOWN";
  custom_base_url: boolean;
  selected_model_id?: string;
  default_model_id?: string;
  capabilities: CapabilityProfile;
  models: ModelList;
  current_limitations: CurrentLimitation[];
  recommended_next_action: RecommendedNextAction;
  allowed_actions: CapabilityAction[];
};
```

Credential 只表达 requirement、reference metadata 和 persistence；任何 API Key、token 或 secret 都不得进入本契约。

### 5.5 `AgentSessionCapability`

```ts
type AgentSessionCapability = {
  supported: boolean | null;
  resume_supported: boolean | null;
  cancel_supported: boolean | null;
  session_persistence: "PROCESS" | "EXTERNAL" | "PERSISTENT" | "UNKNOWN";
  active_session_id?: string;      // opaque ref；仅在用户有权继续该 session 时返回
};
```

### 5.6 `AgentCardState`

```ts
type ComputerAccessIntent =
  | "ASK_WHEN_NEEDED"
  | "AUTO_WITHIN_BOUNDARY"
  | "REQUEST_WIDEST_NATIVE_ACCESS";

type ComputerAccessState =
  | "REQUESTED"
  | "ACTIVE"
  | "EXTERNAL_CONFIGURATION_REQUIRED"
  | "UNSUPPORTED"
  | "UNKNOWN"
  | "DRIFTED";

type ComputerAccess = {
  requested_intent: ComputerAccessIntent;
  state: ComputerAccessState;
  message: string;
  can_change: boolean;
  evidence_at?: string;
  expires_at?: string | null;
  diagnostics?: {
    exposure: "ADVANCED" | "INTERNAL";
    mapping: "EXACT" | "APPROXIMATE" | "UNSUPPORTED" | "USER_CONFIGURATION_REQUIRED" | "UNKNOWN";
    native_mode?: string;
    sandbox?: "ENFORCED" | "NOT_ENFORCED" | "UNKNOWN";
    filesystem?: string;
    shell_tools?: string;
    network?: string;
    external_apps?: string;
    effective_state?: "UNKNOWN" | "REQUESTED" | "CONFIGURED" | "GRANTED" | "OBSERVED" | "DRIFTED";
  };
};

type AgentCardState = {
  id: string;
  name: string;
  status: CapabilityProductState;
  connection: ConnectionState;
  authorization: AuthorizationState;
  health: HealthState;
  detected: boolean | null;
  configured: boolean | null;
  authorized: boolean | null;
  version?: string;
  capabilities: CapabilityProfile;
  session: AgentSessionCapability;
  computer_access: ComputerAccess;
  bindable: boolean;
  current_limitations: CurrentLimitation[];
  recommended_next_action: RecommendedNextAction;
  allowed_actions: CapabilityAction[];
};
```

Computer Access 用户侧只冻结三档中文标签：

| `requested_intent` | 用户标签 | 用户说明 |
| --- | --- | --- |
| `ASK_WHEN_NEEDED` | 请求批准 | 需要超出正常工作范围、访问额外资源或执行受限制操作时，先问我。 |
| `AUTO_WITHIN_BOUNDARY` | 自动处理（推荐） | 正常工作需要的文件、网络和本地工具尽量自动完成；只有确实需要扩大电脑访问范围时才问我。 |
| `REQUEST_WIDEST_NATIVE_ACCESS` | 完全访问 | 请求这个 Agent 使用它支持的最宽电脑访问能力，并尽量减少例行确认。 |

普通列表、主卡片和首次选择不得显示 sandbox、filesystem、network、shell、approval、scope、mapping、effective 或 Provider-native mode。`diagnostics` 只允许在高级详情或受控诊断中按需返回。

“自动处理”不是 YOLO、bypassPermissions、Full Access 或无限制执行。它表达边界内自动工作、扩大技术边界时再询问。

用户选择“完全访问”只产生 `requested_intent`，不得直接产生 `ACTIVE`。用户状态文案固定遵守：

- `ACTIVE`：已启用；
- `EXTERNAL_CONFIGURATION_REQUIRED`：需要在 `<Agent>` 中设置；
- `UNSUPPORTED`：当前接入暂不支持完全访问；
- `UNKNOWN`：无法确认是否已生效；
- `DRIFTED`：需要重新确认。

Computer Access 只表达电脑技术访问，不表达 CEO Decision、Business Authority 或 Employee Responsibility。

Candidate、CanonicalAgentSpec、Adapter Contract 或 manifest validation 不得令 `bindable=true`；只有当前环境 `AVAILABLE` 且真实执行门禁满足时才可绑定。

Agent 的普通列表不是兼容性 Registry 投影。`GET local discovery` 只返回 `detected=true` 的条目；未安装品牌留在内部 `Agent_Adapter_Compatibility_Registry.md`。远程 Agent 通过一个通用 `IMPORT` 入口输入受支持的 connection/ref，不预铺品牌市场。

### 5.7 `SkillExpertCardState` 与 `MCPConnectorCardState`

```ts
type SourceRecord = {
  source_url: string;
  owner: string;
  license_spdx: string | null;
  version?: string;
  digest?: string;
  security_review: "PASS" | "BLOCKED" | "UNKNOWN";
};

type SkillExpertCardState = {
  id: string;
  kind: "SKILL" | "EXPERT";
  name: string;
  readiness: EcosystemReadinessStatus;
  source: SourceRecord;
  capabilities: CapabilityProfile;
  installed_or_recruited: boolean;
  employee_bindable: boolean;
  workspace_usable: boolean;
  current_limitations: CurrentLimitation[];
  recommended_next_action: RecommendedNextAction;
};

type MCPConnectorCardState = {
  id: string;
  kind: "MCP" | "CONNECTOR";
  name: string;
  readiness: EcosystemReadinessStatus;
  transport: "STDIO" | "STREAMABLE_HTTP" | "OFFICIAL_API" | "CUSTOM" | "UNKNOWN";
  authorization: AuthorizationState;
  health: HealthState;
  source: SourceRecord;
  employee_bindable: boolean;
  workspace_usable: boolean;
  current_limitations: CurrentLimitation[];
  recommended_next_action: RecommendedNextAction;
};
```

缺少许可证或安全审计的 Skill/MCP 不显示安装动作；Expert 只有 `CURIS_READY` 才能 `RECRUIT`；Connector 只有授权、health 与真实调用门禁通过后才可绑定。

### 5.8 `EmployeeExecutionBinding`

```ts
type EmployeeExecutionBinding = {
  employee_id: string;
  target_type: "MODEL" | "AGENT";
  provider_id: string;
  capability_id: string;
  display_name: string;
  status: CapabilityProductState;
  capability_profile: CapabilityProfile;
  requested_intent?: ComputerAccessIntent;
  user_consent_ref?: string;
  resource_refs?: string[];
  computer_access?: ComputerAccess;
  session_capability?: AgentSessionCapability;
  is_default: boolean;
  can_switch: boolean;
  current_limitations: CurrentLimitation[];
};
```

Employee/Workspace 业务代码只依赖 `target_type + capability_id + CapabilityProfile + binding`，不得按 OpenAI、Ollama、Codex、Coze 等品牌分支。

## 6. 当前 Provider 产品投影

以下是 2026-08-14 证据快照，不是永久 seed。前端必须由当前 Registry、连接、授权和 health 数据重新投影。

### 6.1 身份与状态

| id | name | category | status | configured | authorized | health | model_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `openai` | OpenAI | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `anthropic` | Anthropic | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `gemini` | Gemini | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `deepseek` | DeepSeek | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `alibaba_qwen` | 通义 | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `volcengine_doubao` | 豆包 | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `zhipu` | 智谱 | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `minimax` | MiniMax | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `moonshot_kimi` | Kimi | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `mistral` | Mistral AI | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `xai` | xAI | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `groq` | GroqCloud | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `siliconflow` | 硅基流动 | OFFICIAL_BYOK | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `openrouter` | OpenRouter | ADVANCED_GATEWAY | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `newapi` | New API | ADVANCED_GATEWAY | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `openai_compatible` | OpenAI Compatible | ADVANCED_GATEWAY | NOT_CONNECTED | false | null | NOT_TESTED | null |
| `enterprise_gateway` | Enterprise Gateway | ADVANCED_GATEWAY | CONFIG_REQUIRED | false | null | NOT_TESTED | null |
| `ollama` | Ollama | LOCAL_MODEL | AVAILABLE | true | true | HEALTHY | 2 |
| `lm_studio` | LM Studio | LOCAL_MODEL | NOT_INSTALLED | false | null | NOT_TESTED | null |
| `local_compatible` | Local Compatible | LOCAL_MODEL | CONFIG_REQUIRED | false | null | NOT_TESTED | null |
| `curis_platform_managed` | Curis Platform Managed Models | FUTURE_PLATFORM | COMING_LATER | null | null | UNKNOWN | null |

说明：Ollama 的 `authorized=true` 表示当前无授权要求且使用条件满足。所有 Cloud BYOK 未提供真实 Key，不能显示 Authorized/Healthy。`enterprise_gateway` 与 `local_compatible` 当前是复用 OpenAI-compatible 路径的产品占位，不是新的 Runtime definition。

### 6.2 凭据、能力、限制与下一动作

| id/group | credential_requirement | custom_base_url | capabilities | current limitation | next action |
| --- | --- | --- | --- | --- | --- |
| 13 个 OFFICIAL_BYOK | REQUIRED | false | 模型发现/推理；具体模型能力 UNKNOWN | 无真实 Key；授权、健康、真实调用未验证；当前 secret 仅进程内存 | CONNECT |
| `openrouter` | REQUIRED | false | 聚合模型发现/OpenAI-compatible 推理 | 无真实 Key；属于高级聚合入口 | CONNECT |
| `newapi` | REQUIRED | true | 聚合发现/OpenAI-compatible 推理 | 无当前用户网关配置；不是普通用户默认入口 | CONNECT |
| `openai_compatible` | REQUIRED | true | 模型发现/OpenAI-compatible 推理 | 无当前用户 Endpoint/Key | CONNECT |
| `enterprise_gateway` | REQUIRED | true | 复用 OpenAI-compatible gateway contract | 无独立 runtime definition；需企业 Endpoint/Key | CONFIGURE |
| `ollama` | NOT_REQUIRED | true | 本地发现/推理；已验证模型 2 个 | 当前证据只覆盖本机服务与两条测试模型；模型细分能力/价格仍 UNKNOWN | USE |
| `lm_studio` | OPTIONAL | true | 本地发现/OpenAI-compatible 推理 | 本机未检测到可用服务 | CONNECT |
| `local_compatible` | OPTIONAL | true | 复用 OpenAI-compatible local endpoint | 需要 Base URL；未形成独立 runtime definition | CONFIGURE |
| `curis_platform_managed` | PLATFORM_MANAGED | false | 未来托管模型供应 | 本轮不实现 PLATFORM Credential、套餐或托管供应 | CONNECT（disabled，等待未来版本） |

正式 Desktop 安全持久化完成前，所有 USER credential 卡片必须显示：`本次会话可用；重启后需要重新授权`。

## 7. 当前 Agent 产品投影

本机扫描当前只返回：

| id | name | status | Detected / Configured / Authorized / Healthy / Available | session | permission | current limitation | next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `codex` | Codex | AVAILABLE | true / true / true / true / true | new + resume；cancel=false | 当前只证明新 session 请求 read-only；effective UNKNOWN | permission 是请求值回显；resume 未重新声明/验证；cancel 未实现 | USE / BIND_EMPLOYEE / RESUME_SESSION |

新增 Agent 页只有两个主动作：`DETECT_LOCAL` 与 `IMPORT`。Claude Code、TRAE、Cursor、OpenClaw、Gemini CLI、Copilot CLI 等未被当前设备检测到时不显示；Coze 等远程产品只有用户主动建立连接后才生成卡片。GUI App 若被检测到但没有稳定机器接口，显示 `UNAVAILABLE` 和 `DETECTED_BUT_PROGRAMMATIC_IMPORT_UNSUPPORTED`，不提供 UI 自动化。

## 8. Skill / Expert 与 MCP / Connector 当前投影

| Ecosystem | LIVE | READY | DISCOVERABLE | RESEARCHED | BLOCKED |
| --- | --- | --- | --- | --- | --- |
| Skill / Expert | 55 active SkillTemplate、现有 Curis 专家模板链 | `SKILL.md` parser/安全边界 | 17 Agent Candidate、外部快照 | Agent Skills/GitHub/ClawHub 等来源 | 5 个无许可证 Skill；0 个新 Curis-ready |
| MCP / Connector | 无本轮真实 MCP 垂直证据 | stdio 最小 adapter、2 个现有 Connector code path | 5 个 MCP manifest | Official Registry、GitHub/Notion/Figma、业务连接器类别 | Streamable HTTP/OAuth/真实授权与调用尚未完成 |

前端从对应 Registry/API 投影卡片，不把以上聚合数字生成假资源。Candidate/manifest 可以查看来源和限制，但默认不能安装、招募或绑定。

## 9. Action Permission Matrix

状态只给出第一层允许范围，最终动作还必须通过右侧 guard。

| Action | 允许出现的状态 | 必须满足的 guard |
| --- | --- | --- |
| CONNECT | NOT_CONNECTED、NOT_INSTALLED、UNAVAILABLE | 产品当前支持连接；本地未安装时动作应进入安装/重新检测指引 |
| AUTHORIZE | AUTH_REQUIRED | 已检测/已配置；存在官方授权方式；不得绕过外部授权 |
| CONFIGURE | NOT_CONNECTED、CONFIG_REQUIRED、HEALTH_UNKNOWN、UNAVAILABLE | 当前用户拥有配置权；官方固定 Base URL 不允许编辑 |
| TEST | HEALTH_UNKNOWN、UNAVAILABLE、AVAILABLE | 必要配置已齐；授权已满足或不需要；测试不能写成 Use 成功 |
| USE | AVAILABLE | capability 当前 available，且工作区/权限/必要上下文满足 |
| BIND_EMPLOYEE | AVAILABLE | `bindable=true`；Employee/Company/Tenant 边界通过；不能绑定 Candidate/contract-only 对象 |
| RESUME_SESSION | AVAILABLE | 有 opaque session ref、`resume_supported=true`，且当前用户/Workspace 有权继续 |
| DISCONNECT | AVAILABLE、AUTH_REQUIRED、HEALTH_UNKNOWN、UNAVAILABLE | USER-owned connection；不得删除 PLATFORM credential；保留必要审计与绑定恢复提示 |
| DETECT_LOCAL | 任意 Agent 列表状态 | 只返回当前设备实际检测结果；扫描错误不得伪造空安装列表 |
| IMPORT | 通用远程/本地 Agent 入口 | 受支持的稳定接口、来源和授权齐全；禁止任意命令与 UI automation |
| INSTALL | DISCOVERABLE 的 Skill/MCP | 许可证、安全、依赖与兼容性通过；安装不等于 Available |
| RECRUIT | AVAILABLE 的 Expert | 必须 `CURIS_READY`；招募后创建 EmployeeInstance，而非复用 Expert 对象 |
| SET_COMPUTER_ACCESS | 已检测且有 Execution Binding 的 Agent | 只写 requested_intent/user consent；不得直接写 ACTIVE/GRANTED/EFFECTIVE |
| OPEN_EXTERNAL_AGENT_SETTINGS | EXTERNAL_CONFIGURATION_REQUIRED | 只打开官方设置指引或原生入口；禁止 UI automation，完成后仍需 verify |

`COMING_LATER`、`BLOCKED`、`UNKNOWN` 默认没有执行动作，只显示限制和可验证的恢复/后续说明。

## 10. 渐进式暴露

| Level | 默认内容 | 不应混入 |
| --- | --- | --- |
| PRIMARY | 名称、产品状态、当前选择、一个主要动作 | Base URL、Credential ref、协议、trace、完整 capability matrix |
| DETAIL | ModelList、CapabilityProfile、Health、CurrentLimitation、Session support | secret、internal binding id、Runtime state machine |
| ADVANCED | Base URL、Credential 管理入口、Permission、协议、高级 Gateway | 明文 credential、内部 trace、适配器实现 |
| INTERNAL | adapter_id、trace、state machine、internal binding id、runtime implementation | 普通用户 UI |

普通卡片只接收 PRIMARY；用户展开后再请求/显示 DETAIL；ADVANCED 只在高级配置中出现；INTERNAL 仅供受控诊断/开发工具，默认 API 不返回。

Computer Access 是上述暴露规则的特例：PRIMARY/DETAIL 最多显示三档用户语言与真实结果；sandbox/network/filesystem/shell/mapping/effective evidence 只能进入 ADVANCED/INTERNAL。

## 11. 产品与接入分类

### DESIGN NOW

- Provider、Model、Skill/Expert、MCP/Connector、Agent 的产品位置与真实状态。
- Connection、Authorization、Health、限制和恢复动作。
- Model 发现/选择/默认切换。
- Employee Execution Binding、当前 Provider/Capability/Permission/Session 能力。
- Computer Access 的“请求批准 / 自动处理（推荐）/ 完全访问”三档 Contract；本轮不实现权限 UI。
- 设置 → AI 与能力、Onboarding 缺能力提示、Workspace/Workstation 使用入口。

### CONNECT LATER

- 按内部 Compatibility Registry 验证真正安装/授权的 Agent，不按品牌列表批量接入。
- Streamable HTTP/OAuth MCP 与首条真实 MCP 垂直链。
- 更多 Cloud Provider 的真实 BYOK connect/discover/call/leak audit。
- Codex cancel，以及更完整的 Git/Browser/Terminal 专业控制能力。
- Custom Agent 的受控 adapter 实现。

### INTERNAL

- Provider Registry protocol fields、Curis Model Router、credential_ref 解析。
- Task/Usage/Artifact trace、内部 binding id、Runtime state machine 与 adapter implementation。
- Candidate/source/license/security 生产线内部状态。

### FUTURE

- `PLATFORM` Credential。
- Curis Platform Managed Models / Curis Admin 统一供应网关。
- 套餐模型供应与商业计费；不进入当前 Local Desktop 实现范围。

## 12. 前端必须支持的状态体验

- loading：状态源读取中，不先显示 Available。
- empty：无 Provider/Model/Agent 连接时给出连接入口，不生成示例成功数据。
- error：说明连接、授权、配置或健康中的哪一步失败；错误不回显外部 response body 或 secret。
- partial：例如 Provider 已连接但 ModelList 尚未加载，显示 `HEALTH_UNKNOWN`/加载状态，不折叠为 Available。
- return：连接/授权/测试完成后回到原设置卡片或原 Workspace 缺能力位置。
- credential session-only：明确“本次会话可用 / 重启需要重新授权”。

## 13. Review 条件

本契约通过 Product Capability Contract Review 后，前端才能以其作为 AI 能力设置与绑定的设计输入。Review 只确认产品位置、状态、数据和动作边界，不接受以下推论：

- 文档占位等于 Runtime 已实现。
- Provider Definition 等于真实 Key 已连接。
- Detected/Candidate/manifest 等于 Agent Available。
- 协议测试等于真实云调用。
- 页面已设计等于产品能力已交付。

当前结论：`CAPABILITY ECOSYSTEM REVIEW REQUIRED`。
