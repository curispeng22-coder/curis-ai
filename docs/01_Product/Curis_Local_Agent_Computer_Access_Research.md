# Curis Local Agent Computer Access Research

Status: Deprecated
Updated: 2026-08-15  
Scope: Local Agent 的真实 Computer Access、Sandbox、Approval 与 Curis Adapter 可控性。  
Source: 官方产品文档、本机只读 CLI/App/Config 探测、当前 Curis Agent Adapter/Discovery 实现。未开启 Full Access，未修改任何 Agent 权限。
Role: Review Record / Reference；保留研究证据，不再承担当前 Contract 定义。
Superseded by: `ADR-0046-local-agent-computer-access-authority.md`、`Agent_Adapter_Contract.md` §3、`AI_Capability_UI_Contract.md` §5.6。

## 1. 结论摘要

1. 主流 Local Agent 并不存在一套相同的权限模型。成熟实现普遍把两件事分开：
   - **技术边界**：Agent/命令能接触哪些文件、进程、网络与本地能力；
   - **确认策略**：边界内自动执行、越界时询问，或不再询问。
2. `Auto`、`YOLO`、`bypassPermissions`、`Full` 不是跨产品同义词。它们有的只取消询问，有的仍处于 sandbox，有的只放开 host exec，不能直接翻译为 Curis 的 Full Computer Access。
3. 用户侧收敛为“请求批准 / 自动处理（推荐）/ 完全访问”三档。它们只表达用户意图，不与某个 sandbox、approval policy 或 native mode 固定绑定。
4. Computer Access 应属于 **Execution Binding 的默认请求 + Session 的有效快照**。Employee 不直接拥有裸权限，Workspace 只提供授权资源边界。
5. 当前 Curis 只有 Codex CLI Adapter，而且只在**新会话**传入 `read-only` / `workspace-write`。它不传 approval/network，禁止 `danger-full-access`；resume 命令没有重新传入 sandbox，结果中的 `permissions` 只是请求值回显，不是底层已授予证明。
6. 因此当前不能仅因用户选择“完全访问”就显示“已启用”。必须保持：

```text
Detected != Configurable != Granted != Available
Requested != Configured != Effective
```

## 2. 证据等级

| 等级 | 本文含义 |
| --- | --- |
| VERIFIED | 官方资料与本机当前版本、代码或只读探测共同支持该具体事实 |
| PARTIAL | 有官方或本机证据，但版本、能力维度、有效范围或可配置性仍未完全闭合 |
| RESEARCHED | 官方资料已确认产品机制，但本机未安装/未授权/未执行验证 |
| UNKNOWN | 没有足够的官方或本机证据，禁止推断 |

映射等级 `EXACT / APPROXIMATE / UNSUPPORTED / USER_CONFIGURATION_REQUIRED / UNKNOWN` 只用于 Curis 模式到原生机制的适配，不替代上述研究证据等级。

## 3. 当前 Curis 与本机事实

### 3.1 已有架构，不建立第二套 Agent 系统

当前 Review Contract 已定义：

```text
Employee -> Execution Binding -> Agent Adapter -> External Agent
                                      |
                               Result / Artifact / Usage
```

`Agent_Adapter_Contract.md` 已有 `cwd/scope/sandbox/network/approval`，`AI_Capability_UI_Contract.md` 已有 sandbox/network/approval 摘要。本专项缺口不是再建 Agent 系统，而是补充“请求、原生映射、有效授权、证据、漂移”的协商语义。

### 3.2 当前实现证据

- `backend/app/agent_adapter.py:19-92`：`CodexCliAdapter` 只接受 `read-only`、`workspace-write`；新 session 传 `--sandbox` 与 `--cd`；明确拒绝其他值。
- 同文件 `:48-51`：resume 只传 session id，没有重新声明 sandbox、cwd 或 approval。
- 同文件 `:89`：返回的 `permissions` 来自 Adapter 构造参数，不是 Codex 运行态回执。
- `backend/app/main.py:1984-1992`：Runtime 只为 `codex-cli` 构造该 Adapter，默认 `read-only`。
- `backend/app/ai_capability_registry.py:147-197`：已有统一 Agent Registry；Codex 为 `LIVE`，其他条目为 `RESEARCHED`。没有 WorkBuddy 条目；TRAE 的 App 路径也不包含当前本机的 `TRAE SOLO CN.app`。
- 本机只读探测：Codex CLI `0.144.6` 存在；`claude`、`cursor-agent`、`trae-cli`、`gemini`、`copilot`、`openclaw`、`workbuddy` 命令均未找到。
- 本机 App bundle：Claude Desktop `1.24012.9`、TRAE SOLO CN `0.1.50`、WorkBuddy `5.3.13` 存在。Claude Desktop 不等于 Claude Code CLI；App 存在也不等于机器接口可用。
- 本机 Codex 用户配置中存在 `sandbox_mode = "danger-full-access"`，但当前 Curis 新会话显式覆盖为 `read-only` 或 `workspace-write`。这反而证明 Curis 不能把“外部现有配置”“本次请求”“本次有效授权”折叠成一个字段。

以上探测均为只读；没有启动 Agent 任务、没有修改配置、没有执行权限提升。

## 4. 跨产品真实研究

以下每个 Agent 均按同一 13 项检查。`本机` 只描述当前设备，不代表产品普遍能力。

### 4.1 OpenAI Codex — VERIFIED

官方证据：[Sandboxing](https://learn.chatgpt.com/docs/sandboxing)、[Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)、[Permissions](https://learn.chatgpt.com/docs/permissions)。本机证据：Codex CLI `0.144.6` 与当前 Curis Adapter 源码。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 支持 OS 原生 sandbox；传统模式有 `read-only`、`workspace-write`、`danger-full-access`，新版权限 Profile 仍处 Beta | VERIFIED |
| 2 | 文件系统边界 | sandbox/profile 定义可读写路径；CLI/IDE 默认限制在当前 Workspace | VERIFIED |
| 3 | Workspace 外文件 | 受 sandbox/profile 限制；通常需要批准或显式增加 root，Full 模式取消本地 sandbox 限制 | VERIFIED |
| 4 | Shell / CLI | 支持；子进程继承同一 sandbox/network 边界 | VERIFIED |
| 5 | python/node/git/npm | 只要本机存在且 sandbox 允许即可作为 shell 子进程运行；不是独立权限类别 | VERIFIED |
| 6 | 网络 | 默认关闭；`workspace-write` 下可显式开启，也可配置 proxy/domain policy | VERIFIED |
| 7 | 外部 App / 浏览器 | Codex 产品可通过工具/MCP/Computer Use 扩展，但当前 Curis `codex exec` Adapter 没有声明或验证这些能力 | PARTIAL |
| 8 | Ask/Auto/Full | sandbox 与 approval policy 分离；官方示例支持 workspace-write + on-request；Full profile/`danger-full-access` 放开本地 sandbox | VERIFIED |
| 9 | 一次/持久授权 | CLI/session 参数、`-c` 覆盖、config/profile 均可；具体企业策略可限制 | VERIFIED |
| 10 | Full 含义 | 移除 Codex 的本地 sandbox 限制；若同时 bypass approval，则不再由 Codex 逐步询问 | VERIFIED |
| 11 | Full 硬限制 | 不自动成为 root/admin，不绕过 macOS/Linux/Windows 权限、组织策略或服务侧安全限制 | PARTIAL：OS 边界明确，所有服务侧限制未逐项枚举 |
| 12 | CLI/Config/API/Session | CLI 与 config 可控；本轮未证明 Curis 使用的 JSONL `exec` 会返回有效权限回执 | VERIFIED/PARTIAL |
| 13 | Curis 能否设置 | 新会话可真实请求 read-only/workspace-write；不能设置 Full、approval、network；resume 的有效 sandbox 目前 UNKNOWN | VERIFIED |

### 4.2 Anthropic Claude Code — RESEARCHED

官方证据：[Permission modes](https://code.claude.com/docs/en/permission-modes)、[Sandboxing](https://code.claude.com/docs/en/sandboxing)、[Agent SDK permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)。本机仅检测到 Claude Desktop App，未检测到 `claude` CLI。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 支持基于 OS 的 Bash sandbox；只约束 Bash/子进程，Claude 工具权限仍是另一层 | RESEARCHED |
| 2 | 文件系统边界 | 默认可写 cwd；默认可读电脑上大部分文件，但可 deny；受保护路径不会在普通模式下自动放行 | RESEARCHED |
| 3 | Workspace 外文件 | 外部写入通常需要权限；可通过 allow/deny 增加或阻止路径 | RESEARCHED |
| 4 | Shell / CLI | 支持 Bash；sandbox 可拦截命令与子进程 | RESEARCHED |
| 5 | python/node/git/npm | 经 Bash 执行，受同一 sandbox/permission 约束 | RESEARCHED |
| 6 | 网络 | sandbox 可设置允许域名；网络和文件规则可配置 | RESEARCHED |
| 7 | 外部 App / 浏览器 | 支持 Web/MCP 等工具；没有证据证明默认拥有任意 GUI App 控制 | PARTIAL |
| 8 | Ask/Auto/Full | `default`、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions`；不同版本/入口可用性需核对 | RESEARCHED |
| 9 | 一次/持久授权 | CLI `--permission-mode` 为会话级；settings 的 `permissions.defaultMode` 可持久；SDK 有 callback | RESEARCHED |
| 10 | Full 含义 | `bypassPermissions` 跳过权限提示与大部分安全检查；官方只建议隔离容器/VM | RESEARCHED |
| 11 | Full 硬限制 | 官方仍有 root/home 大规模删除 circuit breaker，并拒绝 root/sudo；OS 权限仍在 | RESEARCHED |
| 12 | CLI/Config/API/Session | CLI、settings、Agent SDK 均可程序化控制 | RESEARCHED |
| 13 | Curis 能否设置 | 原生可设置，但当前 Curis 没有 Claude Code Adapter；本机也无 CLI，现阶段 UNSUPPORTED | VERIFIED（Curis/本机）+ RESEARCHED（原生） |

### 4.3 Tencent WorkBuddy Desktop — PARTIAL

官方证据：[Permission Modes](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes)、[Privacy Policy 中的本机能力说明](https://www.workbuddy.ai/document/privacy-policy)。本机 App `5.3.13` 存在，但没有可用 CLI；本文不把同站点的 CodeBuddy CLI 自动等同于 WorkBuddy Desktop。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | Default Permissions 对高风险写入、删除、脚本、命令、网络使用 sandbox/确认；具体实现范围未公开到可映射字段级 | PARTIAL |
| 2 | 文件系统边界 | 任务文件夹/Workspace 是主要工作边界；文档描述本地文件读写与备份保护 | RESEARCHED |
| 3 | Workspace 外文件 | 文档未给出足够稳定的路径规则或机器接口 | UNKNOWN |
| 4 | Shell / CLI | 能运行脚本、命令与外部程序；Default 可能确认，Full 关闭相关确认 | RESEARCHED |
| 5 | python/node/git/npm | 可作为脚本/命令执行，但无逐工具原生保证 | PARTIAL |
| 6 | 网络 | Default 对网络访问进行保护/确认；细粒度边界未证实 | PARTIAL |
| 7 | 外部 App / 浏览器 | 官方描述浏览互联网、外部程序和本地能力；具体 App 白名单/控制协议未证实 | PARTIAL |
| 8 | Ask/Auto/Full | 官方 UI 有 `Default Permissions` 与 `Full Access` 两类 | RESEARCHED |
| 9 | 一次/持久授权 | 模式可由用户切换；一次授权、Session 过期与持久化语义未获得充分官方证据 | UNKNOWN |
| 10 | Full 含义 | 关闭写入、删除、脚本、命令、外部程序等确认流程；官方强调仅短时、可信、可恢复、隔离环境使用 | RESEARCHED |
| 11 | Full 硬限制 | 没有证据表明会提升 OS 管理员权限或绕过 OS；产品自身还保留哪些硬拦截 UNKNOWN | PARTIAL/UNKNOWN |
| 12 | CLI/Config/API/Session | 本轮未找到 WorkBuddy Desktop 官方机器权限接口 | UNKNOWN |
| 13 | Curis 能否设置 | 当前只能检测 App 存在；既没有 Registry 条目也没有 Adapter，必须 `USER_CONFIGURATION_REQUIRED`，且不能声称已读取有效模式 | VERIFIED（Curis/本机） |

### 4.4 Cursor CLI — RESEARCHED

官方证据：[CLI permissions](https://docs.cursor.com/cli/reference/permissions)、[Using the Agent CLI](https://docs.cursor.com/en/cli/using)。本机未检测到 Cursor CLI 或 App。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 官方权限文档证明 allow/deny 与 approval；未找到足够证据证明稳定 OS sandbox | UNKNOWN |
| 2 | 文件系统边界 | `Read`/`Write` glob 规则，deny 优先；可放在全局或项目配置 | RESEARCHED |
| 3 | Workspace 外文件 | 绝对路径规则可指向项目外；是否可访问仍受 OS 权限影响 | RESEARCHED |
| 4 | Shell / CLI | `Shell(command)` 规则可控制命令；交互模式会询问 | RESEARCHED |
| 5 | python/node/git/npm | 可按 shell 命令前缀/规则允许；不是独立能力保证 | RESEARCHED |
| 6 | 网络 | 可由 shell/MCP/web 工具产生，但未找到统一 OS 网络 sandbox 证据 | UNKNOWN |
| 7 | 外部 App / 浏览器 | Web/MCP 能力不等于任意 GUI App 控制；后者 UNKNOWN | PARTIAL |
| 8 | Ask/Auto/Full | 交互式命令可审批；非交互 `-p` 官方说明具有完整写访问，但不等于完整电脑访问 | RESEARCHED |
| 9 | 一次/持久授权 | 交互批准可为当前操作；全局/项目 permission config 可持久 | RESEARCHED |
| 10 | Full 含义 | 官方没有统一的 Full Computer Access 模式；扩大 allow rules 或使用 headless full-write 只覆盖部分维度 | UNKNOWN |
| 11 | Full 硬限制 | deny 优先、OS 权限仍在；网络/GUI/管理员语义未闭合 | PARTIAL |
| 12 | CLI/Config/API/Session | permission config 与 CLI 可控；CLI 仍为 Beta，需版本锁定 | RESEARCHED |
| 13 | Curis 能否设置 | 当前无 Adapter、无本机 CLI；只能设计未来映射，当前 UNSUPPORTED | VERIFIED（Curis/本机） |

### 4.5 TRAE Desktop / TRAE SOLO — PARTIAL

官方证据：[TRAE Sandbox engineering note](https://www.trae.ai/blog/engineering_thought_0108)、[TRAE changelog](https://www.trae.cn/changelog)。本机检测到 `TRAE SOLO CN.app 0.1.50`，没有 `trae-cli`。TRAE IDE 的权限模式与开源 `trae-agent` CLI 不是同一已验证控制面。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 官方提供 Sandbox Beta；macOS 与远程 Linux 支持，来源中的 Windows 仍在建设 | RESEARCHED |
| 2 | 文件系统边界 | project、temp、常见依赖目录可读写；后续版本支持自定义文件规则 | RESEARCHED |
| 3 | Workspace 外文件 | Sandbox 外命令通过 allowlist/确认；自定义路径规则存在，但当前 App 版本未实测 | PARTIAL |
| 4 | Shell / CLI | Agent 可运行终端命令，sandbox 拦截 shell | RESEARCHED |
| 5 | python/node/git/npm | 作为终端命令运行，受 allowlist/sandbox 约束 | RESEARCHED |
| 6 | 网络 | 2026-01 官方工程说明明确网络边界仍在完善；不能宣称已闭合 | PARTIAL |
| 7 | 外部 App / 浏览器 | IDE 有浏览/开发工具能力，但任意本地 App 控制与统一授权协议 UNKNOWN | UNKNOWN |
| 8 | Ask/Auto/Full | `Sandbox with Allowlist`、`Manual`、`Auto Run`；Auto Run 可在 sandbox 外无逐命令确认 | RESEARCHED |
| 9 | 一次/持久授权 | UI allowlist/模式可保存的细节、Session 临时提升语义未被充分确认 | UNKNOWN |
| 10 | Full 含义 | `Auto Run` 是不逐命令询问，不等于已证明的完整文件/网络/App 访问 | RESEARCHED |
| 11 | Full 硬限制 | OS 权限、未完成的网络边界仍在；其他硬限制 UNKNOWN | PARTIAL |
| 12 | CLI/Config/API/Session | 当前官方证据主要是产品 UI/工程说明，没有稳定权限 API/CLI 证据 | UNKNOWN |
| 13 | Curis 能否设置 | 当前只能看到 App；Registry 也未覆盖实际 App 名称。权限必须由用户在 TRAE 内配置，`USER_CONFIGURATION_REQUIRED` | VERIFIED（Curis/本机） |

### 4.6 Google Gemini CLI — RESEARCHED

官方证据：[Configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)、[Sandbox](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html)。本机未检测到 `gemini` CLI。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 支持 macOS Seatbelt 和 Docker/Podman；默认关闭，可由 CLI/env/settings 开启 | RESEARCHED |
| 2 | 文件系统边界 | profile 决定读写；macOS 默认 permissive-open 主要限制项目外写入 | RESEARCHED |
| 3 | Workspace 外文件 | `--include-directories` 可加入最多 5 个目录；sandbox profile 仍决定实际范围 | RESEARCHED |
| 4 | Shell / CLI | 支持 shell tool，受 tool policy 与 sandbox 约束 | RESEARCHED |
| 5 | python/node/git/npm | 作为 shell command 执行，前提是已安装且未被排除 | RESEARCHED |
| 6 | 网络 | 由 sandbox profile 决定；open/closed/proxied profile 的语义不同 | RESEARCHED |
| 7 | 外部 App / 浏览器 | Web/MCP/extension 可扩展；macOS sandbox 下 GUI App 可能不可用，非通用 GUI 控制 | PARTIAL |
| 8 | Ask/Auto/Full | `default`、`auto_edit`、`yolo`；另有 `tools.allowed`。approval 与 sandbox 独立 | RESEARCHED |
| 9 | 一次/持久授权 | CLI 参数可 Session 级，settings 可持久 | RESEARCHED |
| 10 | Full 含义 | `yolo` 自动批准工具，但官方还会默认启用 sandbox；所以 YOLO 不等于 Full Computer Access | RESEARCHED |
| 11 | Full 硬限制 | sandbox/profile、OS 权限与工具排除仍可生效 | RESEARCHED |
| 12 | CLI/Config/API/Session | CLI、env、settings 可程序化设置 | RESEARCHED |
| 13 | Curis 能否设置 | 原生可控，但当前 Curis 无 Adapter、无本机 CLI；当前 UNSUPPORTED | VERIFIED（Curis/本机） |

### 4.7 GitHub Copilot CLI — RESEARCHED

官方证据：[Allowing and denying tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools)、[Using local sandboxing](https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/using-local-sandboxing)、[Configuring local sandbox](https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/configuring-local-sandbox-settings)。本机未检测到 `copilot` CLI。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 支持 OS local sandbox，当前为 experimental/public preview；Windows 有额外版本要求 | RESEARCHED |
| 2 | 文件系统边界 | 默认 cwd/temp 可写，home/system/tool 路径只读，其他磁盘位置阻止；可自定义路径规则 | RESEARCHED |
| 3 | Workspace 外文件 | path permission 或 sandbox filesystem rule 可扩展；默认不开放 | RESEARCHED |
| 4 | Shell / CLI | 支持 shell/tools；allow/deny 与 sandbox 共同约束 | RESEARCHED |
| 5 | python/node/git/npm | 作为 shell/tool 执行；Git/gh 凭证可默认暴露给 sandbox，用户可关闭 | RESEARCHED |
| 6 | 网络 | sandbox 默认允许本地/私有/外网；可关闭。官方警告 per-host 规则跨平台不可靠 | RESEARCHED |
| 7 | 外部 App / 浏览器 | URL/web/MCP 可授权；远程 MCP 不在本地 sandbox 内。任意 GUI App 控制 UNKNOWN | PARTIAL |
| 8 | Ask/Auto/Full | 单次、Session、持久 tool/path/url 授权；`--allow-all`/`--yolo` 放开这些 approvals；sandbox 是独立开关 | RESEARCHED |
| 9 | 一次/持久授权 | 交互可一次或持续；CLI flags 为 Session；settings 可持久 | RESEARCHED |
| 10 | Full 含义 | `--allow-all` 放开 tool/path/url 询问；只有再关闭 sandbox 才接近最宽本机访问，仍不是 root | RESEARCHED |
| 11 | Full 硬限制 | OS/组织策略仍在；sandbox host filtering 有已公开局限；管理员可阻止策略 | RESEARCHED |
| 12 | CLI/Config/API/Session | CLI flags、slash command、settings 可控；programmatic `-p` 支持 | RESEARCHED |
| 13 | Curis 能否设置 | 原生可控，但当前无 Adapter、本机无 CLI；当前 UNSUPPORTED | VERIFIED（Curis/本机） |

### 4.8 OpenClaw — RESEARCHED（补充样本）

纳入原因：已在 Curis Compatibility Registry 中，且它明确展示了“sandbox、tool policy、host exec approval、elevated”多层分离。官方证据：[Sandboxing](https://docs.openclaw.ai/sandboxing)、[Exec approvals](https://docs.openclaw.ai/tools/exec-approvals)。本机未检测到 `openclaw`。

| # | 检查项 | 结论 | 证据状态 |
| --- | --- | --- | --- |
| 1 | Sandbox | 可选 Docker sandbox；tool execution 与可选 browser 可进入隔离环境 | RESEARCHED |
| 2 | 文件系统边界 | sandbox/workspace 配置控制 read/write/edit 等工具；关闭 sandbox 时工具可落到 host | RESEARCHED |
| 3 | Workspace 外文件 | 取决于 sandbox mounts、host/node exec 与 tool policy，不是单一模式 | RESEARCHED |
| 4 | Shell / CLI | `exec` 可在 sandbox/gateway/node host 执行；host 侧另有 approvals | RESEARCHED |
| 5 | python/node/git/npm | 作为 exec 命令，受 execution host、allowlist、sandbox 与 host approval 共同约束 | RESEARCHED |
| 6 | 网络 | sandbox/container/network 配置决定；browser sandbox 使用独立 Docker network | RESEARCHED |
| 7 | 外部 App / 浏览器 | 原生有 browser tool/sandbox；node/companion 可提供本机能力 | RESEARCHED |
| 8 | Ask/Auto/Full | host exec 有 `deny/allowlist/ask/auto/full`；另有 elevated break-glass | RESEARCHED |
| 9 | 一次/持久授权 | `/exec` 可 Session 级；config/approvals/CLI 可持久并可按 Agent/host 设置 | RESEARCHED |
| 10 | Full 含义 | `tools.exec.mode=full` 仅表示 host exec 不弹批准；elevated 还可能绕过 sandbox。两者均不等于全部电脑能力 | RESEARCHED |
| 11 | Full 硬限制 | 更严格的 host approval 仍优先；只有授权 sender 可请求；OS/container/node 边界仍在 | RESEARCHED |
| 12 | CLI/Config/API/Session | CLI/config/approvals document/session command 可控，部分 node policy 只读或需在 node 修改 | RESEARCHED |
| 13 | Curis 能否设置 | 当前只有 Compatibility Registry，无 Adapter、本机无 CLI；当前 UNSUPPORTED | VERIFIED（Curis/本机） |

## 5. 跨产品对照结论

| 结论 | 研究判断 |
| --- | --- |
| Sandbox 是否普遍 | Codex、Claude Code、TRAE、Gemini CLI、Copilot CLI、OpenClaw 有真实官方机制；Cursor 的 OS sandbox 证据不足；WorkBuddy 公开描述不足以形成字段级映射 |
| Approval 是否等于安全边界 | 否。多数产品把 approval 与 sandbox/tool policy 分开 |
| Auto/YOLO 是否等于 Full | 否。Gemini YOLO、Copilot allow-all、TRAE Auto Run 主要改变询问策略，sandbox/OS 边界可能仍在 |
| Full 是否等于 root/admin | 否。没有一个研究样本把普通 Full 模式定义为自动取得管理员/root |
| Workspace 外访问能否统一 | 只能统一表达请求；实际由 path rule、mount、profile、host 或用户配置决定 |
| 浏览器/App 是否应默认并入 | 否。Web fetch、MCP、sandbox browser、任意 GUI App 是不同能力，未支持时必须 `UNSUPPORTED/UNKNOWN` |
| 一次授权是否可行 | CLI 型 Agent 普遍支持 Session 参数或单次批准；GUI-only 产品常需要用户在产品内设置 |
| Curis 是否可直接控制 | 当前只对 Codex 新 session 的两个 sandbox 值有真实控制，其余都是研究候选 |

## 6. User-facing Permission Model

研究后的产品判断是：**前台像 Codex 一样简单，后台由 Adapter Contract 保证真实。**

### 6.1 用户只看三档

| 用户选择 | 建议文案 | 含义 |
| --- | --- | --- |
| 请求批准 | 需要超出正常工作范围、访问额外资源或执行受限制操作时，先问我。 | 正常工作继续；超出当前边界时询问 |
| 自动处理（推荐） | 正常工作需要的文件、网络和本地工具尽量自动完成；只有确实需要扩大电脑访问范围时才问我。 | 边界内自动，不是 YOLO、bypass 或无限制执行 |
| 完全访问 | 请求这个 Agent 使用它支持的最宽电脑访问能力，并尽量减少例行确认。 | 只是请求；是否生效仍取决于 Adapter、External Agent 与底层证据 |

主界面不展示 sandbox、filesystem、network、shell、approval、scope、mapping、effective、`workspace-write` 或内部枚举。

### 6.2 前后台分层

```text
User-facing
请求批准 / 自动处理 / 完全访问
        |
Internal Contract
requested intent
        -> Adapter mapping
        -> provider-native permission combination
        -> effective state + evidence + expiry/drift
```

内部继续保留 sandbox、approval、filesystem、shell/tools、network、external apps。这样同一句“自动处理”可以由不同 Adapter 生成不同原生组合，而不会把 Gemini YOLO、Claude bypassPermissions、WorkBuddy Full 或 TRAE Auto Run 错当成相同机制。

### 6.3 映射示例

| Agent | 请求批准 | 自动处理（推荐） | 完全访问 |
| --- | --- | --- | --- |
| Codex | scoped permission + boundary approval | workspace/profile boundary + auto within boundary + ask on expansion | danger/full profile candidate；当前 Curis Adapter 不支持 |
| Claude Code | default permission + sandbox | sandbox + auto/acceptEdits 组合，需 Adapter 显示差异 | bypassPermissions candidate；当前 Curis 无 Adapter |
| WorkBuddy | Default Permissions | Default Permissions 的日常自动处理语义，细节仍需用户侧产品设置 | Full Access；`USER_CONFIGURATION_REQUIRED`，选择不等于生效 |
| TRAE | Manual 或 sandbox confirmation 组合 | Sandbox with Allowlist | Auto Run 只近似，不证明完整电脑访问；`USER_CONFIGURATION_REQUIRED` |

“请求批准”不固定等于 read-only；“自动处理”不固定等于某个 workspace sandbox；“完全访问”不固定等于某个 native full/yolo 值。

## 7. 安全与用户体验问题回答

### 7.1 适合在 Agent 接入时一次选择

- 选择普通用户模式：请求批准 / 自动处理 / 完全访问。
- 选择适用的 Workspace 或授权根目录。
- 明示是否允许 Curis 调整 External Agent 的原生设置；不默认修改。
- 对无法程序化设置的 Agent，只记录用户选择和引导，不记录“已授予”。

不适合让普通用户逐项配置 `python3/node/git/npm`。它们属于 shell/tool execution 的实例，不应成为四个技术弹窗。

### 7.2 适合 Session 级临时提升

- Workspace 外的特定目录；
- 临时网络访问；
- 单次运行未在 allowlist 的命令；
- 临时请求“完全访问”。

提升必须有范围、来源、开始时间、过期条件和原生回执。Provider 不支持 Session 级时，Curis 不得伪造，只能要求用户到原产品设置，并标记 `USER_CONFIGURATION_REQUIRED`。

### 7.3 Full 下仍应由底层 Agent/OS 阻止

- 超出当前 OS 用户本来拥有的文件、Keychain、隐私、TCC、系统完整性权限；
- root/admin/sudo 提升，除非用户在 OS 层另行明确完成；
- 组织管理员、MDM、企业策略、服务端安全策略禁止的操作；
- Provider 自身硬安全限制；
- Curis 未授权的 External App/Browser/MCP 连接；
- 不是技术权限问题的 CEO 业务决定。

### 7.4 是否默认继承 External Agent 现有配置

**默认读取并显示，不默认扩大继承。** 若 Curis 能显式施加更窄边界，应以本次 Binding 请求为准；若只能继承，必须标记 `INHERITED_UNVERIFIED`，并把超过请求范围的情况视为不可用，而不是静默放行。当前主机 Codex 用户配置比 Curis Adapter 请求更宽，正说明必须显式区分两者。

### 7.5 Curis 修改权限前是否需要明确用户动作

需要。接入时的一次模式选择可以授权 Adapter 写入/传递原生设置；之后扩大范围、切到 Full、改变持久设置均需要新的明确动作。收紧权限可以由用户指令或绑定生命周期自动完成，但仍要记录结果。

### 7.6 Agent 切换后的权限

不得复制旧 Agent 的 `granted=true`。Curis 只复制同一 Binding 的 `requested_intent`，然后由新 Adapter 重新映射、应用、验证；映射不是 EXACT 时先降级或要求用户配置。

### 7.7 权限属于哪一层

- **Employee**：引用 Execution Binding，不拥有裸电脑权限。
- **Execution Binding**：保存默认 `requested_intent`、允许的 Workspace refs、用户同意与 Adapter 映射。
- **Workspace**：定义资源边界/目录，不代表自动授权。
- **Session**：保存本次 `effective_access_snapshot`、临时提升与过期。
- **Agent Adapter**：翻译、施加、读取并报告原生事实。

### 7.8 哪些状态绝不能伪造

绝不能由 Curis 根据请求值推导：`native_configured`、`granted`、`effective`、`sandbox_enforced`、`network_allowed`、`outside_workspace_allowed`、`full_access_active`。没有原生回执或可重复探测时只能是 `UNKNOWN` 或 `USER_CONFIGURATION_REQUIRED`。

## 8. Full Computer Access 的准确边界

Curis Candidate 中的 Full Computer Access 只能表示：

> Curis 请求该 External Agent 在当前 OS 用户、Provider、组织策略和已连接工具允许的范围内，使用其最宽的本机 filesystem、shell/tool、network 与受支持 external-app 能力，并尽量取消例行技术审批。

它明确不表示：

- CEO 已同意某项业务取舍；
- Employee 获得新的职责或业务权限；
- 获得 root/admin/sudo；
- 绕过 OS 隐私、TCC、Keychain、MDM、企业策略或 Provider 安全机制；
- 自动连接所有浏览器、App、MCP、账号与凭证；
- Curis 已验证底层实际生效。

技术访问已经足够但任务仍涉及不可逆发布、对外承诺、资金、合规、品牌方向或重大取舍时，仍进入 Curis CEO Decision。不要用命令弹窗替代业务决策，也不要把 CEO Decision 塞进 Computer Access。

## 9. 当前缺口与停止边界

本轮已确认的 Contract Delta Candidate：

1. 当前 `permissions` 缺少 requested/native/effective/evidence 四层；
2. Codex resume 没有重新声明或验证权限；
3. Agent discovery 没有 permission configurability/effective state；
4. 当前 UI 摘要字段不能证明权限已生效；
5. WorkBuddy 与当前 TRAE SOLO App 尚未进入真实机器接口检测。

这些只是 Review Candidate。本轮没有修改 `Agent_Adapter_Contract.md`、Frozen UI/Shared Pattern、Product Blueprint、Runtime、Agent 配置或本机权限。

**FINAL REVIEW APPROVED — AUTHORITY MOVED TO ADR-0046 AND EXISTING CONTRACTS**
