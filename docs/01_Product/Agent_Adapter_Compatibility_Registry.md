# Curis Agent Adapter Compatibility Registry

Status: Review  
Updated: 2026-08-15  
Source: ADR-0046、当前 Codex Adapter/本地扫描、通用 Agent Adapter Contract、各产品官方 CLI/API 文档与本机证据。  
Authority: Computer Access 状态与映射规则遵循 ADR-0046 和 `Agent_Adapter_Contract.md` §3；本 Registry 只记录逐 Agent 可变兼容性事实。

## 1. 产品规则

本文件是内部兼容性 Registry，不是前端 Agent 目录。前端“添加 Agent → 检测本地”只返回当前设备实际检测到的产品；未安装品牌不得以 `NOT_INSTALLED` 卡片默认铺满界面。远程/云端 Agent 通过通用“连接或导入”入口配置，也不形成 Agent Marketplace。

品牌差异留在 Adapter：

```text
Local/Remote Discovery
→ Detected → Configured → Authorized → Healthy → Available
→ Generic Agent Import Contract
→ Employee Capability Binding
→ existing Runtime / Usage / Artifact
```

稳定 CLI/API/JSON/stream/session 接口优先。GUI-only 产品只能标记 `DETECTED_BUT_PROGRAMMATIC_IMPORT_UNSUPPORTED`，不做 UI 自动化。

权限状态必须保持：

```text
Detected != Configurable != Granted != Available
Requested != Configured != Effective
```

## 2. Compatibility Matrix

| Agent | Vendor/Region | Discovery | Machine interface | Auth | Session/Resume | Permission/Sandbox | Artifact | 当前状态 | 真实证据 | 下一动作 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Codex | OpenAI / Global | `codex` in PATH | CLI JSONL | local login probe | new + resume | PARTIAL：新 session 可请求 read-only/workspace-write；effective 未验证 | Curis ResultStore | LIVE（执行）/ PERMISSION PARTIAL | 本机 0.144.6 完成 scan、new、resume、Employee/Workspace → Artifact；permission 只是请求值回显 | Computer Access P0：requested/effective、resume、evidence |
| Claude Code | Anthropic / Global | `claude` in PATH | CLI `-p`, JSON/stream-json | CLI auth | session/resume supported | 原生可配置；当前 Curis 无 Adapter mapping | 可经通用 contract | RESEARCHED | [官方 CLI 文档](https://docs.anthropic.com/en/docs/claude-code/cli-usage)证明稳定机器接口；本机未验证 | 真实安装/授权/用例出现后实现 mapping |
| TRAE Agent | ByteDance / China/Global | `trae-cli` in PATH | open-source CLI `run`/trajectory | provider/env dependent | trajectory available；resume 待验证 | USER_CONFIGURATION_REQUIRED / mapping 待真实 Adapter | 可经通用 contract | RESEARCHED | [公开官方仓库](https://github.com/bytedance/trae-agent)确认 CLI；不能与 TRAE IDE GUI 能力混同 | 真实 Adapter 出现后验证，禁止 UI automation |
| Cursor CLI | Cursor / Global | `cursor-agent` in PATH | CLI print/headless JSON/stream-json | CLI login/API | session id + resume | headless 可能具写权限，必须收紧 | 可经通用 contract | RESEARCHED | [输出格式](https://docs.cursor.com/en/cli/reference/output-format)与[headless 文档](https://docs.cursor.com/en/cli/headless)已确认；CLI beta，本机未验证 | 有安装环境后先 read-only/approval 验证 |
| OpenClaw | OpenClaw / Global | `openclaw` in PATH/service | CLI agent JSON、ACP | local config/provider | session id/usage；resume 待验证 | tools/network scopes 待映射 | 可经通用 contract | RESEARCHED | [Agent CLI](https://docs.openclaw.ai/cli/agent)与[ACP](https://docs.openclaw.ai/cli/acp)已确认；本机未验证 | 安装、授权和 capability boundary 后验证 |
| Gemini CLI | Google / Global | `gemini` in PATH | headless JSON/stream-json | Google/API key | session metadata；resume 待验证 | sandbox/tools 待映射 | 可经通用 contract | RESEARCHED | [官方 headless 文档](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)已确认；本机未验证 | 安装、授权后验证结构化输出 |
| GitHub Copilot CLI | GitHub / Global | `copilot` in PATH | CLI `-p` programmatic mode | GitHub OAuth/token/BYOK | resume supported；结构化事件待验证 | path/tool/url permission 待映射 | 可经通用 contract | RESEARCHED | [官方 programmatic reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference)已确认；未形成 Curis 版本锁定证据 | 需要实际用例时锁定官方接口再接 |
| Coze | ByteDance / China/Global | remote connection only | published agent/API | token/OAuth dependent | 平台相关 | remote scopes | 可经通用 contract | RESEARCHED | 当前只有 opaque ref/transport contract，无 Published Agent/credential | 有真实 Published Agent 后验证 |
| GUI-only IDE/Agent | 各厂商 | app bundle/process | none/stable interface unknown | app session | unknown | unknown | unsupported | BLOCKED | 可检测不代表可编程导入 | 显示 detected + unsupported；不做 UI automation |

## 3. Computer Access Compatibility

用户侧固定为“请求批准 / 自动处理（推荐）/ 完全访问”；本表只记录 Adapter 能否真实翻译、应用和验证。

| Agent | mapping evidence | inspect/read | apply session | apply persistent | verify effective | 当前 UI 真实性 |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | PARTIAL | PARTIAL | PARTIAL：仅新 session sandbox | NO | NO | 可显示执行 Available；Computer Access 只能 UNKNOWN/未验证，Full UNSUPPORTED |
| Claude Code | RESEARCHED | 原生支持；Curis 未实现 | Curis NO | Curis NO | Curis NO | 当前不显示；真实 Adapter 前不得宣称已配置 |
| WorkBuddy Desktop | PARTIAL / GUI-only | UNKNOWN | NO | NO | NO | `USER_CONFIGURATION_REQUIRED`；显示“需要在 WorkBuddy 中设置” |
| TRAE Desktop / SOLO | PARTIAL / GUI-only | UNKNOWN | NO | NO | NO | `USER_CONFIGURATION_REQUIRED`；显示“需要在 TRAE 中设置” |
| Cursor CLI | RESEARCHED | 原生配置可读；Curis 未实现 | Curis NO | Curis NO | Curis NO | 当前不显示；Full mapping UNKNOWN |
| Gemini CLI | RESEARCHED | 原生 settings/profile 可读；Curis 未实现 | Curis NO | Curis NO | Curis NO | 当前不显示；YOLO 不等于完全访问 |
| GitHub Copilot CLI | RESEARCHED | 原生 settings/status 可读；Curis 未实现 | Curis NO | Curis NO | Curis NO | 当前不显示；allow-all 与 sandbox 分开 |
| OpenClaw | RESEARCHED | 原生 policy 可读；Curis 未实现 | Curis NO | Curis NO | Curis NO | 当前不显示；exec full 只覆盖部分能力 |

Full Computer Access 继续禁止真实开启，直到对应 Adapter 同时具有真实 `apply + verify`。其他 Agent 只有在真实 Adapter、安装、授权和用例出现后逐个实现 mapping，不建立通用权限引擎。

## 4. Generic Import Contract

沿用 `Agent_Adapter_Contract.md`，最小字段为：

- identity/vendor/version/source/region；
- discovery method 与 connection method；
- auth reference、configured/authorized/healthy/available；
- task input、structured output/event stream、usage；
- session id/resume/cancel；
- requested_intent、user consent、resource refs、native mapping、effective access evidence；
- sandbox、filesystem、shell/tools、network、external apps、approval 仅作为 Adapter 内部诊断维度；
- artifact mapping、error/recovery、compatibility evidence。

多个 Agent 协作仍由 Curis Workspace/Employee/Task Runtime 编排；Adapter 只负责单个外部 Agent 的稳定机器接口，不在 Adapter 内再造多 Agent Runtime。

## 5. 当前本机前台投影

当前扫描只返回真实检测到的 Codex。Claude Code、TRAE、Cursor、OpenClaw、Gemini CLI、Copilot CLI 等若未检测到，不进入普通用户列表；其兼容性记录只保留在本内部 Registry。App 被检测到但没有稳定机器接口时，返回 `available=false` 与 `DETECTED_BUT_PROGRAMMATIC_IMPORT_UNSUPPORTED`。

Computer Access Authority：`APPROVED / RUNTIME DELTA PLANNED`。其余生态兼容性继续保持 `CAPABILITY ECOSYSTEM REVIEW REQUIRED`。
