# Curis Agent Computer Access Contract Candidate

Status: Deprecated
Updated: 2026-08-15  
Role: Review Record / Reference；Candidate 已完成评审，不再承担当前定义或实现授权。
Superseded by: `ADR-0046-local-agent-computer-access-authority.md`、`Agent_Adapter_Contract.md` §3、`AI_Capability_UI_Contract.md` §5.6。  
Depends on: `Agent_Adapter_Contract.md`、`Agent_Adapter_Compatibility_Registry.md`、`AI_Capability_UI_Contract.md`、`Curis_Local_Agent_Computer_Access_Research.md`。

## 1. 目的

在现有链路中补足 External Agent 权限协商，不建立第二套 Agent、Employee、Workspace 或 Runtime：

```text
Employee
  -> Execution Binding (requested access + user consent)
  -> Agent Adapter (native mapping + apply/read/verify)
  -> External Agent (provider-native sandbox/permission)
  -> Session (effective access snapshot + evidence + expiry)
```

Computer Access 回答的是：

> 这个 External Agent 在本次工作中，技术上可以使用这台电脑的哪些能力？

它不回答业务上“应不应该做”。

## 2. 非目标与不可混同边界

```text
Computer Access != CEO Decision
Computer Access != Business Authority
Computer Access != Employee Responsibility
Computer Access != root/admin/sudo
Computer Access != 绕过 OS / MDM / Provider 安全机制
```

- Computer Access 只定义 filesystem、shell/tools、network、受支持的 external/local apps 技术边界。
- Employee Responsibility、Company Permission、资金/发布/合规/方向决定继续走 Curis 既有责任与 CEO Decision。
- Agent 即使拥有 Full Computer Access，也不能从技术可执行推导出业务已授权。

技术访问满足后，业务链仍然是：

```text
Agent Autonomous Work
-> 真正的业务取舍 / 风险 / 方向问题
-> CEO Decision Package
-> CEO 选择
-> AI 自动继续
```

底层技术权限请求不得包装成 CEO Decision Package；CEO Decision 也不得被技术“完全访问”绕过。

## 3. User-facing Permission Model

产品原则：**前台像 Codex 一样简单，后台由 Adapter Contract 保证真实。**

普通用户只看到三个选择，不需要理解 sandbox、filesystem、network、shell、approval、scope、mapping、effective 或任何 Provider-native 模式。

| 用户看到的选择 | 主文案 | 用户实际表达的意图 |
| --- | --- | --- |
| 请求批准 | 需要超出正常工作范围、访问额外资源或执行受限制操作时，先问我。 | 正常工作可以继续；超出当前安全边界时必须询问 |
| 自动处理（推荐） | 正常工作需要的文件、网络和本地工具尽量自动完成；只有确实需要扩大电脑访问范围时才问我。 | 在允许范围内自动工作，边界扩张时再询问 |
| 完全访问 | 请求这个 Agent 使用它支持的最宽电脑访问能力，并尽量减少例行确认。 | 请求最宽 Provider-native 技术访问；选择不等于已经生效 |

### 3.1 前台展示规则

- 默认选择“自动处理”，但用户确认前不修改 External Agent 的现有配置。
- “自动处理”不是 YOLO、`bypassPermissions`、Full Access 或无限制执行。
- “完全访问”必须作为独立明确动作，优先 Session 级、临时、可撤销。
- 前台只显示用户能采取行动的真实结果：“已启用”“需要在 WorkBuddy / TRAE 中设置”“当前接入暂不支持完全访问”或“无法确认是否已生效”。
- 用户选择“完全访问”后，在 Adapter 验证前不得显示“已启用”。

### 3.2 前台禁止暴露

主界面不得出现：

```text
INSPECT_ONLY
SCOPED_ACCESS
FULL_COMPUTER_ACCESS
workspace-write
sandbox
approval policy
filesystem scope
network policy
mapping / effective
```

### 3.3 UI 文案与内部 Contract 解耦

内部以稳定的 `requested_intent` 表达用户意图，而不是把中文文案绑定到某个 sandbox 或 native mode：

| User-facing | Internal requested intent | 约束 |
| --- | --- | --- |
| 请求批准 | `ASK_WHEN_NEEDED` | 不能固定等同 read-only 或某个 approval flag |
| 自动处理 | `AUTO_WITHIN_BOUNDARY` | scoped technical boundary + auto within boundary + ask on expansion |
| 完全访问 | `REQUEST_WIDEST_NATIVE_ACCESS` | 只请求 Provider 支持的最宽组合，不产生 granted/effective 事实 |

Adapter 再把 intent 翻译为 sandbox、approval、filesystem、shell/tools、network、external apps 的 Provider-native 组合。

## 4. Adapter 内部最小维度

这些是映射与证据字段，不是普通用户设置页上的独立开关。

| 维度 | 最小值域 | 说明 |
| --- | --- | --- |
| filesystem | `READ_WORKSPACE / WRITE_WORKSPACE / OUTSIDE_SELECTED / HOST_WIDE / UNKNOWN` | 记录路径范围与 roots，不从模式名称猜测 |
| shell_tools | `DENIED / SANDBOXED / HOST / UNKNOWN` | python/node/git/npm 作为工具事实/证据，不另造权限系统 |
| network | `DENIED / ASK / ALLOWED / UNKNOWN` | URL allowlist 不能冒充 OS 网络隔离 |
| external_apps | `UNSUPPORTED / ASK / ALLOWED / UNKNOWN` | 浏览器、MCP、GUI App 可分别由原生 capability refs 说明 |
| approval | `ASK_ON_BOUNDARY / AUTO_WITHIN_SCOPE / NO_ROUTINE_ASK / UNKNOWN` | 不等于技术边界 |
| sandbox | `ENFORCED / NOT_ENFORCED / UNKNOWN` | 只有原生状态或可重复证据可写 ENFORCED |

维度可以表达能力不对称。例如 Gemini `yolo + sandbox` 是 `NO_ROUTINE_ASK + ENFORCED`，不能归为已验证 Full Computer Access。

## 5. Canonical Access Record Delta

不替换现有 Agent Adapter Contract，只为其 `permissions` 区域增加以下最小结构：

```json
{
  "requested_intent": "ASK_WHEN_NEEDED | AUTO_WITHIN_BOUNDARY | REQUEST_WIDEST_NATIVE_ACCESS",
  "mapping": {
    "result": "EXACT | APPROXIMATE | UNSUPPORTED | USER_CONFIGURATION_REQUIRED | UNKNOWN",
    "native_mode": "opaque provider-native value",
    "apply_via": "CLI | CONFIG | API | SESSION | USER | NONE"
  },
  "effective": {
    "state": "UNKNOWN | REQUESTED | CONFIGURED | GRANTED | OBSERVED | DRIFTED",
    "filesystem": "...",
    "shell_tools": "...",
    "network": "...",
    "external_apps": "...",
    "approval": "...",
    "sandbox": "...",
    "roots": ["workspace-ref:..."],
    "expires_at": null
  },
  "evidence": {
    "source": "native_status | native_receipt | read_only_probe | user_configuration | unknown",
    "observed_at": "ISO-8601",
    "adapter_version": "opaque",
    "native_version": "opaque"
  }
}
```

规则：

- `requested_intent` 是用户意图，不是授权事实，也不与某个 UI 文案或 native mode 一一绑定；
- `native_mode` 只保存非秘密原生标识，不保存凭证；
- `CONFIGURED` 只证明设置写入/参数被接受；
- `GRANTED` 需要原生状态或 OS/Provider 回执；
- `OBSERVED` 只证明已探测的具体维度，不可外推到未测维度；
- 无证据时使用 `UNKNOWN`，禁止从旧值或 UI 选择推导；
- `roots` 使用 Workspace/resource ref；审计层避免暴露不必要的个人绝对路径。

## 6. 真实状态模型

### 6.1 不可折叠状态

| 状态 | 只证明什么 | 不证明什么 |
| --- | --- | --- |
| Detected | 找到 App/CLI/service | 能配置、已授权、能执行 |
| Configurable | Adapter 有受支持的设置通道 | 设置已写入或已生效 |
| Requested | 用户选择了 Curis 模式 | External Agent 已接受 |
| Configured | 原生参数/config/API 已接受，或用户被引导完成设置 | OS/Provider 实际授予 |
| Granted | 原生来源报告已授予 | 所有维度均实际可用 |
| Observed | 某个受控探测证明具体维度 | 未探测维度或未来 Session |
| Available | 本任务的需求不超过本 Session 的有效权限，且 Agent 其余 readiness 也满足 | 永久权限或业务授权 |

必须保持：

```text
Detected != Configurable != Granted != Available
Requested != Configured != Effective
```

### 6.2 可用性计算原则

只有以下条件共同满足，Computer Access 才可支持本任务 `Available`：

1. Agent 本身满足现有 detected/configured/authorized/healthy 条件；
2. requested intent 的映射不是 `UNSUPPORTED/UNKNOWN`；
3. 任务所需维度均由 `GRANTED` 或针对该维度的 `OBSERVED` 支持；
4. 没有配置漂移、过期或更严格的 OS/组织策略；
5. 业务责任与 CEO Decision 仍按既有 Runtime 独立通过。

## 7. Adapter Permission Negotiation Candidate

现有 Adapter 只需增加四类行为，不需要新的 Runtime：

| 行为 | 目的 | 失败时 |
| --- | --- | --- |
| inspect | 读取版本、可配置性与可安全读取的原生模式 | 返回 UNKNOWN，不猜测 |
| map | 把 requested intent 翻译为原生 sandbox/approval/tool 配置 | 返回映射等级和缺失维度 |
| apply | 仅在用户已明确同意且原生接口支持时传递/写入 | 失败即未配置；不回显 granted |
| verify | 从原生 status/receipt 或安全只读 probe 形成 effective snapshot | 没有证据则 UNKNOWN/USER_CONFIGURATION_REQUIRED |

不要求每个 Agent 都实现四项。Adapter 必须声明：

```text
can_read_access
can_apply_session_access
can_apply_persistent_access
can_verify_effective_access
```

false 是正常能力事实，不是错误。

## 8. 生命周期与归属

### 8.1 Execution Binding

保存：

- 默认 `requested_intent`；
- Workspace refs；
- 用户明确动作的 consent receipt；
- 当前 Agent/Adapter 映射版本；
- 是否允许 Adapter 修改持久原生设置。

不保存：外部账号密码、明文 token、伪造的 granted 标志。

### 8.2 Session

每次新建/恢复都生成 `effective_access_snapshot`：

- Agent/version/adapter version；
- native mapping；
- observed roots 与维度；
- 临时提升、过期、撤销；
- mapping/evidence 状态。

Resume 不得只复用旧快照。必须重新声明或重新读取有效状态；否则标记 `UNKNOWN/DRIFTED`，按更窄模式运行或阻止需要更宽权限的任务。

### 8.3 Agent 切换

只迁移 `requested_intent` 与 Workspace refs，不迁移 `granted/effective`。新 Adapter 必须重新映射：

```text
same requested intent
-> new native mapping
-> new explicit apply/user configuration
-> new effective snapshot
```

`APPROXIMATE` 映射必须显示差异；不能把旧 Agent 的 Full 许可复制到新 Agent。

## 9. 用户动作与默认策略

### 9.1 接入时

- 推荐默认选中“自动处理”，但在用户确认前不修改 External Agent；
- 如果能程序化设置，Adapter 应用并验证，前台只在证据充分后显示“已启用”；
- 如果不能设置，显示“需要在 External Agent 中设置”，完成后仍要验证或标记 UNKNOWN；
- 已有原生配置只读展示为 Inherited，不直接当作 Curis 已授权。

### 9.2 提升时

- Workspace 外特定目录、网络或单次命令优先 Session 临时提升；
- “完全访问”需要独立明确动作，不与“开始任务”捆绑；
- 能限时就限时，Session 结束自动回落；
- Provider 只支持持久设置时，明确说明影响范围并让用户到原产品确认。

### 9.3 减少机械批准

安全不依赖大量技术弹窗，而依赖：

- Workspace sandbox/路径边界；
- 明确 deny 与 fail-closed；
- Session 临时提升与自动过期；
- 高风险文件删除/覆盖的底层硬限制与恢复能力；
- 业务风险进入 CEO Decision；
- 权限回执、漂移和行为证据可审计。

## 10. Full Computer Access Contract

### 10.1 准确定义

> 请求 External Agent 在当前 OS 用户、Provider、组织策略与已连接工具允许的范围内，使用其最宽的本机 filesystem、shell/tool、network 和受支持 external-app 能力，并取消可以取消的例行技术审批。

### 10.2 仍然不允许 Curis 声称

- 已获得 root/admin/sudo；
- 已绕过 OS TCC、Keychain、SIP、MDM、企业 policy；
- 已连接所有 App/browser/MCP/account；
- 已获得业务发布、付款、承诺、数据披露或方向决定权；
- 没有 Provider-native hard stop；
- 用户选择后一定生效。

### 10.3 Provider-native Full 的判定

只有同时满足以下条件，前台才可显示“完全访问 · 已启用”：

1. Adapter 映射为 `EXACT`，或产品文案明确展示 `APPROXIMATE` 差异；
2. 原生模式已被接受；
3. filesystem、shell、network、external-app 中未支持的维度明确显示，而不是隐藏；
4. sandbox/approval 的真实组合有回执或受控证据；
5. 本 Session 未过期、未漂移。

否则只能显示“已请求”“需要在 External Agent 中设置”“当前接入暂不支持完全访问”或“无法确认是否已生效”。

## 11. 对当前 Contract 的最小 Delta

`Agent_Adapter_Contract.md` 当前 `permissions = cwd/scope/sandbox/network/approval` 可保留。Review 通过后，最小追加候选为：

1. `requested_intent`；
2. `mapping.result/native_mode/apply_via`；
3. `effective.state` 与六个维度；
4. `evidence.source/observed_at/versions`；
5. `expires_at/drift`；
6. Adapter 的四个 configurability flags。

当前 Codex Adapter 的专项 Delta Candidate：

- 新 session：继续显式传最小 sandbox；
- resume：必须重新声明/读取并验证权限，不能沿用回显；
- `permissions`：改为 requested + effective，不再只回显 constructor 值；
- approval/network：未实现前明确 UNKNOWN；
- Full：保持不支持，直到独立安全 Review 与真实证据完成。

以上均为 Candidate，不构成代码授权。

## 12. Review 验收问题

- “请求批准 / 自动处理 / 完全访问”是否足够覆盖普通用户任务，而不暴露技术开关？
- “自动处理”是否确认作为推荐默认？
- Full 是否确认默认 Session 级、限时、需独立明确动作？
- GUI-only Agent 是否确认只能 `USER_CONFIGURATION_REQUIRED`，禁止 UI automation？
- Resume 是否确认必须重新验证权限，旧快照不可直接复用？
- Product/UI 是否只保留“已启用 / 需要在 External Agent 中设置 / 当前接入暂不支持 / 无法确认是否已生效”等普通用户语言？

**FINAL REVIEW APPROVED — AUTHORITY MOVED TO ADR-0046 AND EXISTING CONTRACTS**
