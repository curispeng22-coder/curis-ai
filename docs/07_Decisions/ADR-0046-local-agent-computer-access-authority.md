# ADR-0046：Local Agent Computer Access Authority

Status: Frozen

Date: 2026-08-15

Baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

Updated: 2026-08-15

Module: AI Capability / Agent Adapter

Decision Owner: CEO

Supersedes: Computer Access definitions in the three Review Record / Reference documents listed below.

## Decision

Curis 对 External Local Agent 的电脑访问采用“用户侧极简、Adapter 内部严谨”的统一模型，不建立第二套 Agent 或权限系统。

用户侧只提供三档：

1. **请求批准**：需要超出正常工作范围、访问额外资源或执行受限制操作时，先问用户。
2. **自动处理（推荐默认）**：正常工作需要的文件、网络和本地工具尽量自动完成；只有确实需要扩大电脑访问范围时才询问。
3. **完全访问**：请求 External Agent 使用其支持的最宽本机文件、网络、Shell/CLI 和本地工具能力，并尽量取消例行技术确认。

普通用户界面不展示 sandbox、filesystem、network policy、shell policy、approval policy、scope、mapping、effective 或 Provider-native 模式。

## Internal contract

```text
requested_intent
-> Agent Adapter mapping
-> provider-native permission / sandbox / approval
-> effective access evidence
-> Session snapshot
```

内部必须继续表达 sandbox、approval、filesystem、shell/tools、network、external apps、effective state、evidence、temporary elevation、expiry 与 drift。用户三档不与某个固定 sandbox 或 native mode 一一绑定。

“自动处理”固定表达用户意图：

```text
scoped technical boundary
+ auto within allowed boundary
+ ask when boundary expansion is required
```

它不是 YOLO、`bypassPermissions`、Full Access 或无限制执行。

## Ownership

### Execution Binding

- `requested_intent`
- user consent receipt/ref
- authorized resource refs

### Agent Adapter

- `inspect`
- `map`
- `apply`
- `verify`
- `can_read_access`
- `can_apply_session_access`
- `can_apply_persistent_access`
- `can_verify_effective_access`

### Session

- `effective_access_snapshot`
- evidence
- temporary elevation
- expiry
- drift

Resume 必须重新声明或验证有效访问状态。Agent 切换只能迁移 `requested_intent` 与资源 refs，不能继承 `granted/effective`。

## Truth boundaries

```text
Computer Access != CEO Decision
Computer Access != Business Authority
Computer Access != Employee Responsibility
Full != root/admin
Full != 已生效
Detected != Configurable != Granted != Available
Requested != Configured != Effective
```

技术访问满足后，真正的业务取舍、风险或方向问题仍按以下链路处理：

```text
Agent Autonomous Work
-> CEO Decision Package
-> CEO 选择
-> AI 自动继续
```

技术权限请求不得包装成 CEO Decision；CEO Decision 也不得被“完全访问”绕过。

## User-facing truth states

- Adapter 可真实 apply + verify：验证后才显示“已启用”。
- 只能由 External Agent 设置：显示“需要在 <Agent> 中设置”。
- 当前 Adapter 不支持：显示“当前接入暂不支持完全访问”。
- 无有效证据：显示“无法确认是否已生效”。

用户选择“完全访问”只产生 requested intent，不产生 Active、Granted 或 Effective 事实。

## Runtime consequence

- 当前不实现 Runtime，不修改真实 Agent 权限。
- Full Computer Access 继续禁止真实开启，直到对应 Adapter 同时具备真实 `apply + verify`。
- 当前 Codex Adapter 的 requested/effective 混淆、resume 未重新声明/验证权限和 effective evidence 缺失列为 Runtime Delta P0。
- 其他 Agent 只有在真实 Adapter、安装、授权和用例出现后，才逐个实现 mapping。
- 不新建通用权限引擎，不进入 XHS Issue，不修改 Product Blueprint 或 Frozen Workspace UI。

Runtime 规划入口：`docs/04_Development/AGENT_COMPUTER_ACCESS_RUNTIME_DELTA_PLAN.md`。

## Authority and evidence

当前权威落点：

- `docs/01_Product/Agent_Adapter_Contract.md`
- `docs/01_Product/AI_Capability_UI_Contract.md`
- `docs/01_Product/Agent_Adapter_Compatibility_Registry.md`
- `docs/00_Context/CURRENT_STATE.md`

以下文件降为 Review Record / Reference，不再承担当前定义：

- `docs/01_Product/Curis_Local_Agent_Computer_Access_Research.md`
- `docs/01_Product/Curis_Agent_Computer_Access_Contract_Candidate.md`
- `docs/01_Product/Agent_Adapter_Permission_Mapping_Matrix.md`

## Consequences

- 前台保持三个普通语言选择，后台保留逐 Agent 真实差异。
- `python3/node/git/npm` 属于本机工具能力，不逐项要求普通用户授权。
- GUI-only Agent 继续使用 `USER_CONFIGURATION_REQUIRED`，禁止 UI automation。
- OS、root/admin、TCC、Keychain、MDM、组织策略和 Provider hard stop 始终有效。
- 本 ADR 是 Contract 权威，不是 Runtime 完成、UI 实现或权限已生效证据。
