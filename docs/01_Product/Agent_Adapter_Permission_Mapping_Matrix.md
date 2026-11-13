# Curis Agent Adapter Permission Mapping Matrix

Status: Deprecated
Updated: 2026-08-15  
Scope: `User-facing intent -> Agent Adapter -> Provider-native Permission/Sandbox Model`。  
Role: Review Record / Reference；保留 2026-08-15 研究映射快照，不再承担当前兼容性定义。
Superseded by: `ADR-0046-local-agent-computer-access-authority.md`、`Agent_Adapter_Contract.md` §3、`Agent_Adapter_Compatibility_Registry.md` §3。  
Boundary: 不表示 Adapter 已实现，不修改任何本机 Agent 权限。

## 1. 映射等级

| 等级 | 含义 |
| --- | --- |
| EXACT | 原生机制能覆盖该 Curis 模式的必要语义，且没有已知关键维度缺失 |
| APPROXIMATE | 可覆盖主要意图，但 sandbox/approval/network/path/app 等至少一项不同，必须展示差异 |
| UNSUPPORTED | 原生产品或当前安全边界明确不能提供该模式 |
| USER_CONFIGURATION_REQUIRED | 有原生设置，但 Curis 没有受支持的程序化设置通道；必须由用户在 External Agent 内完成 |
| UNKNOWN | 官方或本机证据不足，禁止推断 |

此等级描述**语义映射**。当前 Curis 是否已能应用，单独记录，避免把“未来可映射”写成“当前已设置”。

## 2. User-facing Permission Model

普通用户只看到：

| 选择 | 用户文案 |
| --- | --- |
| 请求批准 | 需要超出正常工作范围、访问额外资源或执行受限制操作时，先问我。 |
| 自动处理（推荐） | 正常工作需要的文件、网络和本地工具尽量自动完成；只有确实需要扩大电脑访问范围时才问我。 |
| 完全访问 | 请求这个 Agent 使用它支持的最宽电脑访问能力，并尽量减少例行确认。 |

内部不把三档固定绑定到某个 sandbox 或 native mode：

```text
请求批准 / 自动处理 / 完全访问
        -> requested intent
        -> Adapter mapping
        -> native permission combination
        -> effective evidence
```

“自动处理”专指：**scoped technical boundary + auto within allowed boundary + ask when boundary expansion is required**。它不是 YOLO、`bypassPermissions`、Full Access 或无限制执行。

## 3. 总矩阵

| Agent | 请求批准 | 自动处理（推荐） | 完全访问 | 原生设置通道 | 当前 Curis 可设置 | 当前 Curis 可验证 |
| --- | --- | --- | --- | --- | --- | --- |
| OpenAI Codex | EXACT（原生）：scoped profile + on-request | EXACT（原生）：workspace/profile boundary + auto within boundary + ask on expansion | EXACT（原生）：danger/full profile；当前 Adapter UNSUPPORTED | CLI / config / profile / Session override | PARTIAL：仅新 session 的 read-only/workspace-write | NO：只回显请求；resume 有漂移风险 |
| Claude Code | EXACT/APPROXIMATE：default + sandbox 组合 | APPROXIMATE：sandbox + `auto/acceptEdits` 组合 | APPROXIMATE：`bypassPermissions`，仍有 hard stop/OS 边界 | CLI / settings / Agent SDK / callback | UNSUPPORTED：无 Adapter | UNSUPPORTED |
| WorkBuddy Desktop | APPROXIMATE：Default Permissions | APPROXIMATE：Default Permissions 的日常自动语义 | APPROXIMATE：Full Access 关闭确认，但完整路径/网络范围未证实 | 官方 UI；机器接口 UNKNOWN | USER_CONFIGURATION_REQUIRED | UNKNOWN |
| Cursor CLI | APPROXIMATE：交互批准 + permission rules | APPROXIMATE：项目 allow/deny + boundary ask | UNKNOWN：无统一最宽电脑访问语义 | global/project config / CLI interaction | UNSUPPORTED：无 Adapter | UNSUPPORTED |
| TRAE Desktop / SOLO | APPROXIMATE：Manual / sandbox confirmation | APPROXIMATE：Sandbox with Allowlist | APPROXIMATE：Auto Run 不等于完整 filesystem/network/App | 产品 UI；稳定权限 API/CLI UNKNOWN | USER_CONFIGURATION_REQUIRED | UNKNOWN |
| Gemini CLI | APPROXIMATE：default + sandbox profile | APPROXIMATE：sandbox + `auto_edit`/tool policy | UNKNOWN：`yolo` 自动批准但仍可能在 sandbox 内 | CLI / env / settings | UNSUPPORTED：无 Adapter | UNSUPPORTED |
| GitHub Copilot CLI | APPROXIMATE：sandbox + boundary approval | APPROXIMATE：local sandbox + path/tool/url allow rules | APPROXIMATE：allow-all + no-sandbox 才接近；仍非 root/任意 App | CLI flags / slash command / settings | UNSUPPORTED：无 Adapter | UNSUPPORTED |
| OpenClaw | APPROXIMATE：sandbox + `ask` | APPROXIMATE：sandbox + `auto` / ask-on-miss | APPROXIMATE：exec full/elevated 只覆盖部分能力层 | CLI / config / approvals / Session commands | UNSUPPORTED：无 Adapter | UNSUPPORTED |

## 4. 可配置性与真实性矩阵

| Agent | 本机 Detected | 原生可程序化设置 | 原生可读取 | 需要用户在原产品设置 | 当前可声明 Granted/Active | 研究状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Codex CLI 0.144.6 | YES | YES | PARTIAL：config/profile 可读，当前 JSONL 无有效权限回执证据 | NO（当前两种 sandbox）；其他维度可能需要 | NO：当前只能声明 Requested/Configured，不能声明 effective granted | VERIFIED |
| Claude Code CLI | NO；只有 Claude Desktop App | YES | PARTIAL：settings 可读，Session effective 需原生回执/探测 | 当前 Curis YES，因为没有 Adapter | NO | RESEARCHED |
| WorkBuddy Desktop 5.3.13 | YES（App） | UNKNOWN | UNKNOWN | YES | NO | PARTIAL |
| Cursor CLI | NO | YES（permission config） | PARTIAL：配置可读，有效 OS/network 状态未闭合 | 当前 Curis YES | NO | RESEARCHED |
| TRAE SOLO CN 0.1.50 | YES（App）；Registry 当前未命中该 App 名称 | UNKNOWN | UNKNOWN | YES | NO | PARTIAL |
| Gemini CLI | NO | YES | PARTIAL：settings/profile 可读，有效执行仍需探测 | 当前 Curis YES | NO | RESEARCHED |
| GitHub Copilot CLI | NO | YES | PARTIAL：settings/status 可读，per-host 网络规则有官方局限 | 当前 Curis YES | NO | RESEARCHED |
| OpenClaw | NO | YES | YES/PARTIAL：policy 可 JSON 读取；host/node 更严格状态仍需合并 | 当前 Curis YES | NO | RESEARCHED |

`Detected` 仅来自本机只读探测；App 检测不等于同名 CLI/机器接口存在。

## 5. 每个 Adapter 的准确映射

### 5.1 Codex

| 用户意图 | Native request candidate | Mapping | 当前实现事实 |
| --- | --- | --- | --- |
| 请求批准 | scoped permission profile + on-request approval | EXACT（原生）/ APPROXIMATE（当前 Curis） | 当前只传 sandbox/cwd，未传 approval |
| 自动处理 | workspace/profile boundary + auto within boundary + ask on expansion | EXACT（原生）/ APPROXIMATE（当前 Curis） | 当前只传 sandbox/cwd，未传 approval/network |
| 完全访问 | danger/full permission profile + compatible approval policy | EXACT（原生）/ UNSUPPORTED（当前 Curis） | constructor 明确拒绝 danger-full-access |

特殊缺口：resume 命令没有重新声明 sandbox/cwd。当前 `permissions` 只是 Adapter 自己的值，不能证明 resumed session 的 effective state。Review 通过前，resume 需要 Workspace write 或更宽权限的任务应视为 `UNKNOWN`。

### 5.2 Claude Code

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | default permission mode + sandbox | EXACT/APPROXIMATE | 默认询问与 sandbox 可组合；具体版本能力仍需 Adapter 探测 |
| 自动处理 | sandbox + `auto` 或 `acceptEdits`/rules 组合 | APPROXIMATE | auto 可能自动拒绝而不是询问；需报告差异 |
| 完全访问 | `bypassPermissions` | APPROXIMATE | 官方仍有 root/sudo 和大规模删除 hard stop；不等于 OS root |

原生 CLI/SDK 可控制，但当前 Curis 无 Adapter。本机 Claude Desktop App 不能替代 Claude Code CLI 证据。

### 5.3 WorkBuddy Desktop

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | Default Permissions | APPROXIMATE | 风险点会询问，但完整技术边界未公开到字段级 |
| 自动处理 | Default Permissions | APPROXIMATE | 日常动作自动、高风险询问，语义接近；有效范围仍需产品自身确认 |
| 完全访问 | Full Access | APPROXIMATE | 证明的是关闭多类确认，不足以证明 host-wide filesystem/network |

当前只能 `USER_CONFIGURATION_REQUIRED`。Curis 不得自动操作 WorkBuddy UI，也不得让用户点击 Full 后回填 `granted=true`。

### 5.4 Cursor CLI

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | interactive approval + project permission rules | APPROXIMATE | permission rules 不等于 OS sandbox |
| 自动处理 | project-local allow rules + boundary deny/ask | APPROXIMATE | network 与 shell 子进程边界未形成统一证明 |
| 完全访问 | 宽路径与 shell allow / headless full-write | UNKNOWN | 没有完整 computer-wide 语义与有效状态证明 |

未来 Adapter 应优先生成/传递最小 permission rules，而不是把 `-p` 的 full write 当 Full Computer Access。

### 5.5 TRAE Desktop / SOLO

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | Manual 或 sandbox confirmation | APPROXIMATE | Manual 的询问频率可能高于 Curis 意图 |
| 自动处理 | Sandbox with Allowlist | APPROXIMATE | network 边界仍有官方已知未完成项 |
| 完全访问 | Auto Run | APPROXIMATE | 只证明减少命令确认，不证明完整文件/网络/App 权限 |

当前必须 `USER_CONFIGURATION_REQUIRED`。开源 TRAE Agent CLI 的可调用性不能替代当前 TRAE SOLO Desktop 权限模式。

### 5.6 Gemini CLI

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | default approval + sandbox profile | APPROXIMATE | profile 的文件/网络组合仍需显式选择 |
| 自动处理 | sandbox profile + auto_edit/tool allow policy | APPROXIMATE | auto_edit 不覆盖所有工具；边界扩张行为需 Adapter 核对 |
| 完全访问 | yolo + sandbox/config combination | UNKNOWN | YOLO 只取消询问且可能自动启用 sandbox |

未来 Adapter 必须同时设置 approval 与 sandbox，不能只传 `--approval-mode yolo`。

### 5.7 GitHub Copilot CLI

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | local sandbox + interactive path/tool/url approval | APPROXIMATE | 仍需确认 built-in/MCP 工具的覆盖面 |
| 自动处理 | local sandbox + cwd path/tool/url allow rules | APPROXIMATE | 默认 sandbox 网络较宽；host rules 有官方局限 |
| 完全访问 | `--allow-all` + `--no-sandbox` | APPROXIMATE | 不赋予 root，不自动获得任意 GUI App/组织权限 |

Copilot 的 allow-all 与 sandbox 是两层。单独 `--yolo` 不能被 Curis 显示为 Full Computer Access。

### 5.8 OpenClaw

| 用户意图 | Native request candidate | Mapping | 差异 |
| --- | --- | --- | --- |
| 请求批准 | sandbox + scoped tool policy + `ask` | APPROXIMATE | 需要同时配置多个 policy 层 |
| 自动处理 | sandbox + scoped mounts + `auto` / ask-on-miss exec | APPROXIMATE | gateway/node/host approvals 可能更严格 |
| 完全访问 | host exec `full` / elevated + broad tool policy | APPROXIMATE | exec full 只放开 host command approval，不代表所有 tools/browser/files |

OpenClaw 的更严格 host approvals 必须优先。Curis 不能只读取 session `/exec` 值就宣称实际 Full。

## 6. Adapter 输出规则

每次 mapping 至少输出：

```text
requested_intent
mapping_result
native_mode
apply_via
can_apply_session
can_apply_persistent
can_read_effective
effective_state
differences[]
evidence
```

普通用户不需要看到所有字段，但产品状态必须由这些事实生成：

| 内部事实 | 用户表达 |
| --- | --- |
| mapping EXACT/APPROXIMATE + effective GRANTED/OBSERVED | 已启用；若差异影响用户则用普通语言说明 |
| USER_CONFIGURATION_REQUIRED | 需要在 WorkBuddy / TRAE 等 External Agent 中设置 |
| requested but no native receipt | 已请求，尚未确认 |
| drift/version/session changed | 需要重新确认 |
| unsupported | 当前接入暂不支持完全访问 |
| unknown | 无法确认是否已生效 |

## 7. 当前架构落点

```text
Employee
  -> Execution Binding owns requested_intent + consent
  -> Agent Adapter owns mapping/apply/read/verify
  -> External Agent owns native permission/sandbox
  -> Session owns effective snapshot + temporary elevation
  -> existing Result / Artifact / Usage / Audit receives evidence refs
```

Computer Access 只决定 Agent 技术上能不能继续。真正的业务取舍、风险或方向问题仍进入 `CEO Decision Package -> CEO 选择 -> AI 自动继续`，不得转译成 shell/文件权限弹窗。

不新增：

- 第二套 Agent Registry；
- 第二套 Employee permission system；
- Workspace 内技术开关墙；
- Curis 自定义 shell command allowlist 语言；
- GUI automation 修改第三方 Agent；
- 把 CEO Decision 改造成命令审批。

## 8. Review 后最小实施顺序候选

1. 先修正 Codex Adapter 的 requested/effective 真实性与 resume 漂移；Full 继续禁用。
2. 把 configurability/mapping/effective 状态加入现有 Agent Registry/Binding Contract，不建新表或新 Runtime。
3. 只有在某 Agent 有真实安装、授权和用例时，才实现该 Adapter 的 permission mapping。
4. GUI-only 产品保持 `USER_CONFIGURATION_REQUIRED`，直到官方机器接口出现。

这些顺序不是本轮实现授权。

**FINAL REVIEW APPROVED — AUTHORITY MOVED TO ADR-0046 AND EXISTING CONTRACTS**
