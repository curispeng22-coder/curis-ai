# Curis Settings / Application Configuration Research

Status: Review  
Review state: SETTINGS PRODUCT CONFIGURATION REVIEW REQUIRED  
Research date: 2026-08-17  
Source: official product documentation, current local Curis authority documents, and prior local product observations  
Scope: research and recommendation only; not Product Blueprint, UI Blueprint, Runtime, or implementation authority

## 1. Executive Summary

Curis Settings should be the place where a person or company maintains durable defaults, connections, permissions, application behavior, data handling, and account/support information. It should not become a second place for configuring every Employee, Role, Business, Workspace, Conversation, or Task.

The strongest reference pattern is not a large preference form. It is a layered configuration model:

```text
Policy ceiling
  → Company defaults
    → Business / Role / Employee / Workspace inherited defaults
      → Conversation / Task run-time choice
```

This is a research recommendation only. The precedence and override contract remain Review Required. A lower scope must never silently weaken a higher security ceiling, and a requested permission must never be presented as effective access without provider-native verification.

Recommended Curis V1 Settings groups:

1. Personal & Appearance
2. Company Defaults
3. Models & AI Providers
4. Permissions & Security
5. Application & Data
6. Account & Help

V1 should be narrow. It should make providers, defaults, access intent, notifications, appearance, company basics, and data export understandable. Billing, device sync, advanced retention policy, fleet administration, arbitrary model routing, and a universal “full access” switch should remain later or out of Settings until their runtime contracts exist.

## 2. Curis Settings Mission

### User need

The CEO needs one reliable place to answer:

- Who am I, which company am I operating, and how should the desktop behave?
- Which model and Agent Provider can Curis use?
- What access may an agent request, and what has actually been verified?
- Which company-wide defaults should new work inherit?
- What data is retained, where can it be exported, and what can be cleared?
- Where are help, version, account, and support actions?

### Settings is responsible for

- Maintaining durable user, company, application, provider, security, and data defaults.
- Showing the current connection/configuration state and the limits of that state.
- Routing to the owning detail page when a setting belongs to an Employee, Role, Business, Workspace, Conversation, or Task.
- Making changes traceable and explaining when they take effect.

### Settings is not responsible for

- Creating the operating plan for a Business.
- Defining an Employee’s responsibility, personality, or day-to-day work.
- Editing a Workspace’s project context or changing a Task’s business state.
- Acting as a generic plugin marketplace or workflow DAG builder.
- Claiming access, provider health, or execution capability that has not been verified.

## 3. Boundary with Curis Business Objects

| Object | Owns | Settings relationship |
|---|---|---|
| User | identity, personal preferences, notification and appearance defaults | direct Settings owner |
| Company | company identity and company-wide defaults | direct Settings owner for defaults; operating details stay in Company/Organization |
| Business | business definition, lifecycle, objectives, decisions | link to owning page; not duplicated in Settings |
| Role | responsibility and authority in the organization | link to Role/Organization detail; may inherit company defaults |
| Employee | identity, role, responsibility, provider assignment, current work | provider/access defaults may be inherited; employee-specific configuration stays on Employee detail |
| Workspace | actual work context, files, tasks, artifacts, results | workspace may override permitted defaults; configuration stays in Workspace detail |
| Conversation / Task | current execution context and run-time choices | temporary override only unless explicitly saved as a default |
| Provider | credentials, endpoint, model catalog, health, adapter capability | direct Settings owner for connection and availability; provider-native detail remains provider-owned |

The distinction matters because Settings is cross-layer maintenance, while Organization owns employees and responsibility, and Workspace owns actual work. A global Settings page must not become a hidden control plane for business work.

## 4. Competitor Research by User Task

### 4.1 Maintain account and data behavior

ChatGPT places Data Controls under the profile menu and separates model-training choice, Temporary Chats, memory/personalization, export, and account deletion. The important reference is the separation of data controls from conversation work, not the exact menu labels. Temporary Chats are a distinct retention behavior rather than a cosmetic mode. [OpenAI Data Controls](https://help.openai.com/en/articles/7730893-chatgpt-data-controls)

Curis implication: expose data handling as a small, comprehensible group. Do not mix it with provider credentials or company operating policy.

### 4.2 Connect tools and control approvals

OpenAI’s app permissions distinguish connected-app permission from memory, personalization, retention, and training. Permission options include always ask, ask for changes, ask for important actions, and never ask; app-specific overrides can replace the default. Approval before an action is represented as an approval card, while the actual source-system scope still controls what is possible. [OpenAI Apps in ChatGPT](https://help.openai.com/en/articles/11487775-apps-in-chatgpt)

Curis implication: “permission setting” must show scope, default approval behavior, effective source, and actual verification separately. A permission toggle alone is insufficient.

### 4.3 Configure an agent in a development environment

Claude Code exposes permission modes and tool allow/deny controls, supports resume/continue, and uses separate authentication and provider paths. Its documented hierarchy gives managed policy priority over CLI, project, and user settings. It also documents proxy, gateway, model, budget, rate-limit, and audit concerns as separate concerns. [Claude Code CLI usage](https://docs.anthropic.com/en/docs/claude-code/cli-usage), [Claude Code IAM](https://docs.anthropic.com/ko/docs/claude-code/iam), [Claude Code LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)

Curis implication: Agent Provider and Model Provider are different configuration objects. Permission mode is an execution concern, not a model preference.

### 4.4 Configure a professional workstation

VS Code provides a mature scope model: User settings are global, Workspace settings apply to a project and override User settings, and Profiles group settings, extensions, and layout. Settings Sync is opt-in and has merge/replace and machine-specific limitations. [VS Code settings](https://code.visualstudio.com/docs/configure/settings), [VS Code Profiles](https://code.visualstudio.com/docs/configure/profiles), [VS Code Settings Sync](https://code.visualstudio.com/docs/configure/settings-sync)

Curis implication: use explicit scope labels and inherited-value explanation. Do not flatten User, Company, Employee, Workspace, and current-run configuration into one form.

### 4.5 Current evidence status for other requested references

- Codex Desktop / ChatGPT coding: official and local evidence confirms provider-native work concepts such as project/session/worktree, model, skills, permissions, and execution state. Exact current Desktop Settings IA was not fully confirmed in this pass: `UNVERIFIED`.
- Cursor: prior local research confirms Composer/context/mode/model/permission/tool patterns; exact current global Settings IA for this pass: `UNVERIFIED`.
- WorkBuddy, EvoFlow, Coze, 豆包: no reliable current official Settings evidence was established in this pass: `UNVERIFIED`. They must not be used as confirmed facts.

## 5. Decision Matrix

| 设置项 | 设置对象 | 为什么需要 | 修改影响 | 风险 | Curis V1 | Later | 不应进入 Settings | 推荐位置 |
|---|---|---|---|---|---|---|---|---|
| Profile | USER | 识别当前 CEO 与审计主体 | 新会话、记录、通知显示 | 身份混淆 | Yes | — | Employee identity | Personal |
| Language / locale | USER / APPLICATION | 让文本、日期、数字可读 | 新界面和后续输出 | 既有记录格式混乱 | Yes | per-workspace locale | Business language policy | Personal |
| Timezone | USER / APPLICATION | 让计划、提醒、审计时间准确 | 新计划和通知 | 时间误判 | Yes | workspace override | Task schedule itself | Personal |
| Theme / appearance | USER / APPLICATION | 长时间桌面使用需要可读性 | 立即影响界面 | 低 | Yes | profiles | Brand system | Appearance |
| Notifications | USER / APPLICATION | 让 CEO 及时知道 Needs CEO / failure / result | 立即影响提醒 | 漏看或打扰 | Yes | per-event routing | Employee status | Application |
| Shortcuts | USER / APPLICATION | 高频工作减少摩擦 | 立即影响快捷键 | 冲突 | Basic | import/export | Business command policy | Personal / Advanced |
| Company profile | COMPANY | 让员工和结果使用正确公司上下文 | 新建对象和显示 | 错公司上下文 | Yes, basic | legal/billing profile | Business definition | Company |
| Company approval default | COMPANY | 让新工作有安全起点 | 新任务默认行为 | 过宽授权 | Proposal / Gap | policy profiles | Per-action approval result | Company / Security |
| Automation/risk default | COMPANY | 统一公司风险容忍度 | 新运行默认 | 自动化越权 | Proposal / Gap | policy editor | Workflow design | Company |
| New employee permission default | COMPANY | 新员工不能默认获得过宽权限 | 新员工初始配置 | 权限扩散 | Proposal / Gap | role policies | Employee responsibility | Company / Organization |
| Budget / usage ceiling | COMPANY | 控制模型和 Agent 成本 | 后续调用可能被限制 | 中断、误计费 | Later | budget policies | One-off task budget | Company / Billing |
| Retention default | COMPANY / APPLICATION | 明确数据保留原则 | 新数据生命周期 | 不可恢复删除 | Later / Gap | per-workspace policy | Business knowledge policy | Data |
| Model Provider connection | PROVIDER | 让 Curis 知道可用模型来源 | 新运行可选；当前运行不变 | 密钥泄露、错误 endpoint | Yes, if real adapter exists | gateway routing | Model choice in every Employee | Models & AI |
| API key / credential reference | PROVIDER | 连接 BYOK Provider | 新连接/测试 | 明文泄露 | Yes, secure reference only | enterprise vault | Prompt/artifact | Models & AI |
| Endpoint / model discovery | PROVIDER | 适配自托管或兼容 API | 连接测试和模型列表 | SSRF、错误模型 | Basic | advanced routing | Conversation content | Models & AI |
| Default model | USER / COMPANY | 减少每次选择 | 新运行默认 | 成本/质量偏差 | Yes, status-aware | per-role defaults | Force all employees | Models & AI |
| Agent Provider availability | AGENT PROVIDER | Codex/Claude Code 等是执行环境，不是模型 | 新运行可选 | 认证/安装误判 | Yes, health/status | provider policy | Rename as Model Provider | Models & AI |
| Default approval mode | USER / COMPANY | 定义通常何时询问人 | 新运行默认 | 过度自动化 | Proposal / Gap | policy hierarchy | Claim effective access | Permissions |
| Computer access intent | USER / COMPANY / EMPLOYEE | 让访问请求有明确意图 | 新运行请求策略 | requested ≠ effective | Proposal / Gap | managed policy | Full-access button | Permissions |
| Connector permission | USER / COMPANY | 控制外部数据和写操作 | 新 connector action | 越权、数据外泄 | Basic if connector exists | per-app policy | Connector discovery | Permissions |
| Credential management | PROVIDER / CONNECTOR | 便于撤销、轮换和查看状态 | 后续连接行为 | 秘密暴露 | Status-only V1 | vault/rotation | Show raw secret | Permissions |
| Audit log link | COMPANY / USER | 解释谁在何时改变了什么 | 只读追溯 | 日志泄露、噪声 | Link/status if existing | full audit | Activity feed duplication | Security |
| Startup / background | APPLICATION / DEVICE | 控制桌面进程和长任务 | 下一次启动或立即 | 意外耗电/运行 | Later | device policy | Agent schedule | Application |
| Proxy / network | APPLICATION / DEVICE / PROVIDER | 支持企业网络和 provider 连接 | 新连接/重启 | 连接失败、隐私 | Later / native only | managed network | Arbitrary network bypass | Application |
| Local storage / cache | APPLICATION / DEVICE | 解释数据落点与空间占用 | 新缓存/清理 | 数据丢失 | Basic visibility | relocation | Business data browser | Data |
| Export | USER / COMPANY | 用户需要可携带和审计数据 | 生成导出 artifact | 敏感数据外泄 | Yes, bounded | scheduled export | Backup promise | Data |
| Clear cache / delete data | USER / COMPANY | 用户需要恢复空间或删除数据 | 可能不可逆 | 数据损失 | Cache only | retention/delete center | Silent delete | Data |
| Devices / sync | USER / APPLICATION | 多设备连续工作 | 跨设备复制状态 | 冲突、隐私 | Later | account sync | Workspace collaboration | Account |
| Billing / subscription | ACCOUNT | 商业化后管理付费和发票 | 账户权益 | 财务/合规 | Later / UNKNOWN | invoices, seats | Company budget policy | Account |
| About / update / help | APPLICATION / ACCOUNT | 版本、支持、法律信息 | update may restart | 假更新、停机 | Yes | release channels | Product roadmap | Help |

## 6. V1 Must Support

The following are the smallest useful Settings baseline, subject to runtime verification:

1. Profile, language/locale, timezone, theme, and desktop notification defaults.
2. Basic Company profile; company-wide defaults only where an existing runtime can consume them.
3. Model Provider connection status, secure credential reference, endpoint/model discovery where supported, connection test, and default model selection.
4. Agent Provider status and authentication/installation health, explicitly separate from Model Provider.
5. Permission and Computer Access status that distinguishes requested intent, native mapping, configured state, verification, and effective state. Unsupported states must show `UNKNOWN` or `UNVERIFIED`.
6. Connector permission status and a route to credential/audit detail where those systems exist.
7. Data export, local storage/cache visibility, and cache clearing with explicit confirmation. Do not invent retention durations.
8. Help, version, update check, terms, privacy, and licenses.

## CURIS SETTINGS V1 BASELINE

| Setting | Why | Where | Default | Effect timing | Override | Risk |
|---|---|---|---|---|---|---|
| Profile | identify the CEO and audit actor | Personal | current authenticated identity | immediate | none | identity confusion |
| Language / locale | readable UI and dates | Personal | system locale | next render | permitted Workspace display override later | format confusion |
| Timezone | accurate schedules and notifications | Personal | system timezone | new schedules | Workspace display override later | missed timing |
| Theme | sustained desktop readability | Personal / Appearance | system theme | immediate | none in V1 | low |
| Desktop notifications | surface Needs CEO, failure, and result | Application | OS/app default | immediate | event-level later | missed or excessive alerts |
| Company profile | correct company context | Company | current Company record | new objects | no lower-scope identity override | wrong context |
| Default model | avoid repeated model choice | Models & AI | provider-reported safe default | next run | current Conversation/Task may choose | cost/quality |
| Model Provider connection | make provider availability truthful | Models & AI | disconnected until verified | connection/status immediate; run next start | provider-specific | secret/endpoint |
| Agent Provider status | show whether Codex/Claude Code adapter can execute | Models & AI | unavailable until health verified | next run | Employee/Workspace assignment | auth/install mismatch |
| Approval/access status | explain what can be requested | Permissions & Security | ask when needed / provider default where no Curis control exists | next run | higher policy ceiling | requested mistaken for granted |
| Connector permissions | control external data/action approval | Permissions & Security | provider/source default, explicitly shown | next action | app/source override if supported | external write |
| Export | portability and audit | Data | manual export | on request | Company export later | sensitive output |
| Cache visibility/clear | space recovery without deleting business truth | Application & Data | cache managed by app | clear immediately; active work must be protected | none | data loss |
| Help/version/update | recoverability and trust | Account & Help | current version | update-specific | none | stale client |

## 7. Recommended Settings IA

```text
Settings
├── Personal & Appearance
│   ├── Profile
│   ├── Language, locale & timezone
│   ├── Appearance
│   ├── Notifications
│   └── Shortcuts (advanced)
├── Company Defaults
│   ├── Company profile
│   ├── Approval & risk defaults (only where supported)
│   ├── Automation defaults (only where supported)
│   └── Usage / retention (later or read-only until contracted)
├── Models & AI Providers
│   ├── Model Providers
│   ├── Agent Providers
│   ├── Defaults
│   └── Connection and health
├── Permissions & Security
│   ├── Computer Access
│   ├── Connector permissions
│   ├── Credential status
│   └── Audit / verification
├── Application & Data
│   ├── Startup & background (later)
│   ├── Local storage and cache
│   ├── Export / clear
│   └── Network / update (native or later)
└── Account & Help
    ├── Account, devices & sync (later)
    ├── Usage / billing (later)
    ├── Help & feedback
    └── About, terms, privacy & licenses
```

The IA should be progressive disclosure: ordinary users see stable high-value controls first; advanced provider, network, credential, and retention details appear only when a connected provider or supported runtime makes them meaningful.

## 8. Avatar Quick Menu Contract

### Keep

- Personal profile: opens Personal settings or account identity.
- Settings: opens the full Settings IA.
- Appearance: quick theme choice, with “More appearance settings” route.
- Help / feedback: support and recovery entry.
- About / version: version and update information.
- Log out: account action when account mode exists.

### Conditional

- Model / AI Providers: useful as a shortcut only if it opens status and connection maintenance, not a second provider manager.
- Company switcher: only when multiple Companies are actually supported; otherwise it creates false hierarchy.

### Do not put in the avatar menu

- Employee, Business, Role, Workspace, or Task configuration.
- A global “Full Computer Access” switch.
- Arbitrary workflow controls.
- Hidden credential values.

## 9. Model Provider vs Agent Provider

### Model Provider

Represents where inference comes from: provider identity, API key or secure credential reference, endpoint, available models, default model, discovery, connection test, usage/cost visibility, and health.

### Agent Provider

Represents how an agent executes work: Codex, Claude Code, Cursor-like adapter, local CLI, or another supported execution environment. It includes installation/authentication/health, native tool and permission capabilities, session/resume behavior, and adapter compatibility.

They may use the same underlying vendor but must not be merged. A model connection can be healthy while an Agent Provider is unavailable; an Agent Provider can be installed while no usable model credential exists.

### V1 rules

- Never store raw API keys in conversation, artifacts, or visible logs.
- Show “connected”, “tested”, “available for new runs”, and “effective for current run” as different concepts.
- Connection tests must be provider-specific and must not be replaced by a static green badge.
- Default model changes affect new runs unless a current run explicitly chooses another model.
- A model catalog must show why a model is unavailable rather than silently omitting it.

## 10. Permission / Access / Approval Contract

Curis should show four distinct states:

1. Requested intent: what the user or policy asks for.
2. Native mapping: how the provider/OS translates that request.
3. Configured state: what Curis persisted as configuration.
4. Verified/effective state: what the provider actually grants now.

If provider-native evidence is absent, effective state is `UNKNOWN`, not granted. This is especially important for Computer Access and Full Access. The UI may explain a request, route the user to a native permission flow, or report that manual configuration is required; it must not fabricate a successful grant.

Recommended conceptual policy order, not yet frozen:

```text
Managed / policy ceiling
  > Company default
    > Role / Employee / Workspace inherited default
      > Conversation / Task run-time choice
```

A run-time choice may narrow access but should not widen a higher ceiling. Provider-native approval remains authoritative for the actual action. “Automatic”, “confirm”, and “ask when needed” should describe approval behavior, not bypass operating-system or provider security.

## 11. Company Settings

### Appropriate for Settings

- Company name, logo/basic identity, locale defaults, and company-level notification/approval defaults when a real consumer exists.
- Links to Organization, Employees, Workspaces, and company audit/usage pages.
- A clear explanation of which defaults affect new Employees or new Workspaces.

### Keep in owning pages

- Employee responsibility, role, provider assignment, personality, and current work.
- Business objectives, lifecycle, workflow, and decisions.
- Workspace files, context, tasks, artifacts, and results.
- Per-employee or per-workspace operational configuration that requires business context.

Company Settings should never be a disguised Organization editor or a second Workspace admin console.

## 12. Application / Desktop

V1 should be conservative:

- Support appearance, notifications, version, help, and bounded local storage/cache visibility.
- Prefer native OS behavior for proxy, device permissions, credential storage, and network controls.
- Defer startup, background execution, multi-device sync, lock-screen behavior, arbitrary download directories, and update channels until the Desktop Runtime contract defines lifecycle, failure, recovery, and privacy behavior.
- “Background work” is not merely a checkbox. It requires durable task state, resume/recovery, notification semantics, cancellation, and resource policy.

## 13. Data / Memory / Retention

Curis should use three conceptual layers:

- Current Truth First: current business and execution state.
- History by Business Significance: decisions, handoffs, outcomes, and meaningful changes.
- Raw Trace by Retention: detailed tool calls, logs, and low-level execution evidence.

Ordinary users need to understand what is current, what is retained as meaningful history, and what raw trace can be cleared. They do not need an infrastructure console.

V1 candidate:

- Explain data categories in plain language.
- Export user/company-owned data through a bounded, inspectable artifact.
- Show local storage/cache status.
- Clear cache separately from deleting business truth.
- Defer configurable retention periods, automated deletion schedules, backup promises, and memory-policy composition until the data contract exists.

Never expose “clear history” as a single destructive action that conflates conversation history, business records, audit evidence, raw trace, and cached files.

## 14. Local-first V1 vs Commercialization

Local-first V1 can responsibly support:

- local identity and Company context;
- official BYOK Model Provider connections where a real adapter exists;
- local Agent Provider status and health;
- local notification, appearance, cache, and export controls;
- clear support/version/legal links.

Later commercial/account capabilities include subscriptions, invoices, seats, cloud usage, devices, synchronization, organization administration, centralized budgets, managed provider gateways, and enterprise retention. They should not be simulated as working Settings in a local-first build.

## 15. Later / Advanced

Defer until corresponding contracts and evidence exist:

- managed policy hierarchy and admin-enforced overrides;
- per-Role / per-Employee / per-Workspace defaults;
- provider routing, fallback, cost budgets, and rate limits;
- device sync and conflict resolution;
- background/scheduled work controls;
- configurable retention and legal hold;
- credential vault rotation and enterprise network policy;
- billing, subscription, invoices, seats, and usage dashboards;
- advanced profiles that bundle layout, provider, and notification settings.

These are not “missing buttons”; each requires ownership, persistence, effective-state evidence, failure/recovery, and audit semantics.

## 16. What Should Not Be Settings

- Company operating plan or business strategy.
- Employee responsibility, role, handoff, or current work.
- Workspace files, code, diff, terminal, test, review, Git, or result surfaces.
- Conversation prompts and current task instructions.
- A generic tool/plugin marketplace.
- A DAG editor for multi-agent work.
- Hidden provider credentials.
- A global bypass/full-access control without native verification.
- Every possible configuration exposed “for completeness”.

## 17. Current Runtime Gap

Current Curis evidence requires careful wording:

- The provider registry and adapter contracts exist as product/architecture inputs, but registry definitions do not prove a live usable credential or successful provider call.
- Official BYOK is the local Desktop model-supply direction; many provider definitions remain unconnected without real credentials.
- Codex/local Agent Provider detection and health have partial evidence, but configured Computer Access is distinct from effective access. Without provider-native receipt, effective access must remain `UNKNOWN`.
- Permission UI is not implemented as a completed Runtime capability.
- Cloud BYOK health/auth/calls remain unverified where real credentials are absent.
- Startup/background, sync, billing, retention controls, and universal credential management are not established as completed Settings capabilities.

This document therefore recommends Settings contracts and placement. It does not claim that the recommended controls currently work.

## 18. Risks and Unresolved Questions

1. What is the authoritative scope/override policy after Company, Role, Employee, and Workspace Runtime semantics are reviewed?
2. Which provider-native permission receipts can Curis reliably consume?
3. Which secrets are stored in OS Keychain, and what is the revoke/rotate behavior?
4. Which data categories are Current Truth, significant History, or Raw Trace?
5. Is account mode part of V1, or is the first release strictly local-first?
6. Does a provider connection test guarantee model availability, or only endpoint/auth reachability?
7. Which application settings require restart, and how is an active run protected from a setting change?
8. What can be exported without exposing credentials, private prompts, or third-party data?

## 19. Recommendations

1. Treat Settings as a maintenance and authorization surface, not a universal admin console.
2. Start with six groups and progressive disclosure.
3. Make scope and effect timing visible on every non-trivial setting.
4. Separate Model Provider from Agent Provider in language, storage, health, and navigation.
5. Use explicit `UNVERIFIED` / `UNKNOWN` states for unsupported or unproven capabilities.
6. Keep Employee, Business, Role, and Workspace configuration on their owning pages.
7. Ship only provider and permission controls that have a real underlying adapter, secure storage, and verification path.
8. Defer commercial, sync, retention, and background-work controls until their business/runtime contracts are reviewed.

## Confirmed References

- OpenAI Data Controls: https://help.openai.com/en/articles/7730893-chatgpt-data-controls
- OpenAI Apps in ChatGPT: https://help.openai.com/en/articles/11487775-apps-in-chatgpt
- OpenAI Plugins in Codex: https://help.openai.com/en/articles/20001256-plugins-in-codex/
- OpenAI Skills: https://help.openai.com/en/articles/20001066
- Anthropic Claude Code CLI usage: https://docs.anthropic.com/en/docs/claude-code/cli-usage
- Anthropic Claude Code IAM: https://docs.anthropic.com/ko/docs/claude-code/iam
- Anthropic Claude Code LLM gateway: https://docs.anthropic.com/en/docs/claude-code/llm-gateway
- Anthropic Claude Code proxy: https://docs.anthropic.com/en/docs/claude-code/corporate-proxy
- VS Code settings: https://code.visualstudio.com/docs/configure/settings
- VS Code Profiles: https://code.visualstudio.com/docs/configure/profiles
- VS Code Settings Sync: https://code.visualstudio.com/docs/configure/settings-sync

## Unverified References

- Exact current Codex Desktop Settings IA.
- Exact current Cursor global Settings IA.
- Current WorkBuddy, EvoFlow, Coze, and 豆包 Settings behavior.
- Any commercial/account/billing behavior not verified from current official documentation.

## Directly Reusable Patterns

- Profile-menu entry into Settings.
- Separate data controls from conversation work.
- Per-app permission override with approval before external action.
- User / Workspace / Profile scope labels and inherited-value explanation.
- Provider-native permission modes and explicit resume/continue behavior.
- Secure credential references rather than visible secrets.
- Status distinctions between configured, tested, available, and effective.
- Progressive disclosure for advanced controls.

## Curis-Specific Additions

- Company defaults without replacing Company/Organization/Workspace ownership.
- Employee and Role inheritance with explicit responsibility boundaries.
- Agent Provider vs Model Provider split.
- Requested intent → native mapping → configured → verified/effective access states.
- Current Truth / significant History / Raw Trace retention explanation.
- Needs CEO, handoff, and result-return implications for company operation.

## Do Not Copy

- A single global “full access” switch.
- A flat preference dump containing every object’s configuration.
- Treating a model provider as an Agent Provider.
- Treating a connection badge as proof of effective execution.
- A Settings page that duplicates Organization, Business, Employee, or Workspace pages.
- A hidden admin console for ordinary CEOs.
- Unverified competitor features written as Curis requirements.

## CEO Review Required

This document is a Review artifact, not a frozen decision. The next step is CEO review of the V1 baseline, scope/override direction, local-first boundary, and the list of runtime gaps. No UI design or implementation should start from this document until those decisions are separately accepted.
