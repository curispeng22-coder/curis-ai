# Curis Agent Adapter Contract

Status: Review  
Updated: 2026-08-15  
Source: AI 能力接入专项、ADR-0046、Talent Market Integration Contract、Codex 官方 non-interactive/App Server 文档、当前 Runtime/Artifact/Usage 代码。  
Frozen Scope: §3 Computer Access Contract 由 `ADR-0046-local-agent-computer-access-authority.md` 冻结；其余兼容性与实现细节继续按当前证据维护。

## 1. 定义

Agent 不是 Model。Model 完成一次推理；Agent 拥有身份、上下文、权限、执行过程、产物与可继续的 session。Employee 只依赖 Execution Binding：

```text
Employee → Execution Binding → Agent Adapter → External Agent
                                  ↓
                         Result / Artifact / Usage
```

Curis 负责组织、上下文、调度、权限和结果回收，不复制成熟 Agent 的专业执行能力。

## 2. Canonical Contract

| 区域 | 必需字段 | 说明 |
| --- | --- | --- |
| identity | adapter_id、external_ref、display_name、version | external_ref 是外部标识，不复制私有定义 |
| capabilities | typed Capability Profile + evidence | 不按 Codex/Claude 品牌名做业务判断 |
| session | session_id、created/resumed、resume_supported、effective_access_snapshot | session id 是 opaque external ref；resume 必须重新验证访问状态 |
| input | task、workspace/project context refs、attachments refs | 只给经授权上下文 |
| output | final text、structured result、status | 必须区分 intermediate/final |
| artifacts/files | artifact refs、file-change refs、digest | Curis 回收，不默认授予写权限 |
| tool usage | tool name、status、receipt | 不复制 hidden reasoning |
| status/progress | queued/running/waiting/blocked/completed/failed/cancelled | 真实外部状态 |
| permissions | requested_intent、native_mapping、effective evidence、expiry/drift | 技术维度保留在 Adapter 内部，不直接暴露给普通用户 |
| usage/cost | tokens/calls/cost/source/version | unknown 必须可表达 |
| health | detected/configured/authorized/healthy/available | 状态不可折叠 |
| control | cancel/resume capability and result | 不支持时明确 false |

## 3. Computer Access Contract

本节是 ADR-0046 冻结的当前权威。产品原则是：

> 前台像 Codex 一样简单，后台由 Adapter Contract 保证真实。

### 3.1 User-facing

普通用户只看到：

- **请求批准**：需要超出正常工作范围、访问额外资源或执行受限制操作时，先问用户。
- **自动处理（推荐默认）**：正常工作需要的文件、网络和本地工具尽量自动完成；只有确实需要扩大电脑访问范围时才询问。
- **完全访问**：请求 External Agent 使用其支持的最宽本机文件、网络、Shell/CLI 和本地工具能力，并尽量减少例行技术确认。

这些文案只表达意图。主界面不显示 sandbox、filesystem、network、shell、approval、scope、mapping、effective、`workspace-write` 或 Provider-native 模式。

### 3.2 Internal authority

```text
requested_intent
-> Agent Adapter mapping
-> provider-native permission / sandbox / approval
-> effective access evidence
-> Session snapshot
```

内部字段最小集合：

| Owner | Required contract |
| --- | --- |
| Execution Binding | `requested_intent`、user consent receipt/ref、authorized resource refs |
| Agent Adapter | `inspect`、`map`、`apply`、`verify`、configurability flags |
| Session | `effective_access_snapshot`、evidence、temporary elevation、expiry、drift |

Adapter configurability flags：

```text
can_read_access
can_apply_session_access
can_apply_persistent_access
can_verify_effective_access
```

Adapter 内部继续表达 sandbox、approval、filesystem、shell/tools、network、external apps、effective state 与 evidence。“自动处理”必须映射为 scoped technical boundary + auto within allowed boundary + ask on expansion，不能直接映射为 YOLO、bypassPermissions 或 Full。

### 3.3 Truth state

```text
Detected != Configurable != Granted != Available
Requested != Configured != Effective
```

- 用户选择只生成 `requested_intent`。
- `Configured` 只证明原生参数/config/API 被接受或用户已完成外部设置。
- `Granted` 需要原生状态或可信回执。
- `Effective` 需要当前 Session 的 evidence；未验证维度保持 `UNKNOWN`。
- `Available` 还必须满足 Agent authorization、health、binding 与当前任务需求。
- Resume 必须重新声明或验证有效访问；不得直接复用旧 snapshot。
- Agent 切换只迁移 `requested_intent + resource refs`，不得继承 `granted/effective`。

无法真实映射时固定返回：

- `USER_CONFIGURATION_REQUIRED`：需要在 External Agent 中设置；
- `UNSUPPORTED`：当前接入暂不支持；
- `UNKNOWN`：无法确认是否已生效。

### 3.4 Full 与 CEO Decision 硬边界

完全访问只请求 Provider 支持的最宽电脑技术访问，且优先 Session 级、临时、可撤销。只有 Adapter 具备真实 `apply + verify` 才能显示已启用。

```text
Computer Access != CEO Decision
Computer Access != Business Authority
Computer Access != Employee Responsibility
Full != root/admin
Full != 已生效
```

OS、TCC、Keychain、MDM、企业策略和 Provider hard stop 始终有效。技术访问满足后，真正业务取舍、风险或方向问题仍进入 `CEO Decision Package -> CEO 选择 -> AI 自动继续`。

### 3.5 当前实现状态

当前 Runtime 尚未实现本节完整 Contract：Codex 新 session 只传 `read-only/workspace-write` 请求值；结果中的 permissions 是 Adapter 回显，不是 effective evidence；resume 没有重新声明或验证权限。Full 继续禁止真实开启。

规划见 `docs/04_Development/AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md`。本节冻结不表示 Runtime 已交付。

## 4. Local Discovery 状态

- `Detected`：找到 CLI/app/service；不等于授权。
- `Configured`：存在可调用配置或 manifest。
- `Authorized`：官方登录/credential 状态通过。
- `Healthy`：版本/health probe 成功。
- `Available`：本次可执行所需状态全部满足。
- `Unavailable`：未检测到或必要状态失败。

扫描不得自动授权、写入工作区或创建 Employee。

扫描由内部 `AGENT_ADAPTER_REGISTRY` 数据驱动，统一检查 PATH/CLI、应用、配置与授权探针；普通用户 API 只返回当前设备 `detected=true` 的条目。兼容性 Registry 不是前端品牌目录，未安装 Agent 不显示。仅发现 GUI App 而没有稳定机器接口时返回 `DETECTED_BUT_PROGRAMMATIC_IMPORT_UNSUPPORTED`，禁止 UI automation。

面向前端时，这五个事实轴必须映射为
`AVAILABLE / NOT_CONNECTED / NOT_INSTALLED / AUTH_REQUIRED / CONFIG_REQUIRED /
HEALTH_UNKNOWN / UNAVAILABLE / COMING_LATER / BLOCKED / UNKNOWN`，具体优先级和动作权限见
`docs/01_Product/AI_Capability_UI_Contract.md`。尤其 `Detected != Available`。

## 5. Codex Adapter

当前实现使用官方本地 CLI：

- 新会话：`codex exec --json --sandbox read-only --cd <authorized cwd> -`
- 恢复：`codex exec resume --json <session_id> -`
- 协议：JSONL event stream。
- 提取：`thread.started`、`item.completed(agent_message/file_change)`、`turn.completed(usage)`。
- 默认权限：read-only；只有 capability metadata 明确选择 `workspace-write` 时提升。
- 禁止：danger-full-access、bypass approvals、硬编码模型、硬编码本机 Codex 路径。
- 结果：output、session_id、progress event types、usage、requested permission echo、resume flag、artifact refs；当前没有 effective access evidence。

真实验证：本机 Codex `0.144.6` 完成新 session `019ffef0-6982-79a0-acf7-e0ab5f5f6cbf`，输出 `CURIS_CODEX_ADAPTER_OK`；随后按同一 session resume，输出 `CURIS_CODEX_RESUME_OK`。另通过 Employee/Workspace Task 在临时只读 git 项目输出 `CURIS_CODEX_WORKSPACE_OK` 并回收 1 个 Curis Artifact。

当前 ceiling：adapter 使用一次 `subprocess.run`，因此 session resume 已支持，但 resume 未重新声明/验证权限，运行中 cancel 也尚未支持。需要取消时升级为受控长驻 process/App Server，而不是给当前接口虚报 cancel。

## 6. Agent 兼容性来源

Codex 的真实状态保留为 `AVAILABLE`。Claude Code、TRAE、Cursor、OpenClaw、Gemini CLI、GitHub Copilot CLI、Coze 与 GUI-only 产品的 discovery、machine interface、auth、session、permission 和当前 Evidence 统一记录在 `docs/01_Product/Agent_Adapter_Compatibility_Registry.md`。

该内部 Registry 中的 `RESEARCHED` 不产生前端卡片、Employee binding 或 Runtime capability。远程 Agent 由通用 Import Contract 建立用户连接后才进入产品状态。

## 7. Coze 与人才市场安全边界

只保存 `external_ref + opaque credential_ref`。不得复制 Prompt、Knowledge、Credential 或私有 Agent 配置。Talent Market 的 Candidate/CanonicalAgentSpec 负责发现与治理；Agent Adapter 负责经授权执行，两者不能相互冒充。

## 8. Custom Manifest 最小字段

```json
{
  "id": "agent.example",
  "name": "Example",
  "adapter": "http | mcp | codex_cli | claude_code_cli | coze",
  "capabilities": ["research"],
  "external_ref": "published-object-ref",
  "credential_ref": "vault://tenant/.../credential/..."
}
```

Manifest validation 不等于安装、授权或执行。当前不允许 manifest 提供任意 shell command；需要新增 adapter 时先通过 source/license/security/permission Review。
