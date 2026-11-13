# Agent Computer Access Runtime Delta Plan

Status: Review

Baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

Updated: 2026-08-15

Module: AI Capability / Agent Adapter Runtime

Owner: Development + Quality Review

Authority: `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`

Implementation Authorization: None；本文件只规划，不是 Issue，不授权修改 Runtime、Schema、Agent 配置或真实权限。

## 1. 目标

让现有 Agent Adapter/Execution Binding/Session 链能够真实区分：

```text
requested_intent
-> native mapping requested/configured
-> effective access evidence
-> Session snapshot
```

不建立第二套 Agent、Binding、Session、审计或权限系统。

## 2. 当前事实与根因

当前 `CodexCliAdapter`：

- 新 session 只接受 `read-only/workspace-write` 并传给 Codex；
- resume 没有重新声明或读取权限；
- 返回的 `permissions` 来自 Adapter 构造参数，是请求值回显；
- 没有 approval/network/effective evidence；
- constructor 明确拒绝 danger-full-access；
- 执行成功、session resume 与 Artifact 回收均不能证明权限实际生效。

根因不是缺少通用权限引擎，而是现有 Adapter Contract 没有把 requested、native configured、effective evidence 和 Session snapshot 分开。

## 3. 范围边界

### In scope for future authorized Issues

- 复用现有 `CodexCliAdapter`、Agent Registry、Execution Binding、Session/Result/Artifact/Audit 路径；
- requested intent 到 Provider-native 参数的逐 Adapter 映射；
- apply/read/verify 真实性；
- Session snapshot、resume 重新验证、expiry/drift；
- 机器字段与普通用户三档状态的可靠投影。

### Explicitly out of scope

- 本轮代码或数据库修改；
- 开启 Full Computer Access；
- 修改真实 Codex/Claude/WorkBuddy/TRAE 等配置；
- Product Blueprint、Frozen Workspace UI 或权限 UI；
- XHS Issue、内容工作台或其他业务 Issue；
- 通用权限引擎、跨 Provider 自定义 policy language；
- GUI automation；
- root/admin、OS TCC/Keychain/MDM 绕过；
- 把 Computer Access 并入 CEO Decision。

## 4. Priority plan

## P0 — Codex requested/effective truth

### P0.1 修复 requested/effective 混淆

目标：当前 `permissions={sandbox,cwd}` 不再被解释为 granted/effective。

Future Issue 最小交付候选：

- 输入使用 `requested_intent`；
- Codex Adapter 生成明确的 `native_mapping`；
- 输出分开 `requested`、`configured`、`effective`、`evidence`；
- 没有原生回执或安全证据时，effective 必须为 `UNKNOWN`；
- 旧调用方若只需要执行结果，继续消费现有 Result/Artifact，不建立平行返回系统。

### P0.2 Resume 重新声明或验证权限

目标：resume 不能沿用旧 snapshot 或 Adapter constructor 回显。

Future Issue 必须选择并验证一种真实路径：

1. 使用当前 Codex 官方支持的 session/config 参数重新声明同一 native mapping；或
2. 从 Codex 官方状态/回执读取有效权限；或
3. 无法完成 1/2 时 fail closed，将 effective 标记为 `UNKNOWN/DRIFTED`，阻止需要更宽权限的任务。

不得假设新 session 的 requested sandbox 自动延续到 resume。

### P0.3 Effective evidence 真实性

证据优先级：

1. Provider-native effective status/receipt；
2. 受控、无破坏性的边界探测；
3. config/command accepted 只能到 `CONFIGURED`；
4. 用户选择、Adapter request echo 或一次任务成功不能成为 `GRANTED/EFFECTIVE`。

探测不得为了验证而开启 Full，不读取用户无关私有文件，不访问真实敏感目录，不修改 Agent 配置。

### P0 acceptance candidate

- 新 session 与 resume 均产生独立 access snapshot；
- requested、configured、effective 在测试中可分别断言；
- 缺少证据时为 UNKNOWN，不自动升级；
- resume mapping 漂移会 fail closed；
- danger/full 与 bypass 继续被拒绝；
- 既有 Result/Artifact/Usage 路径不回归；
- focused tests 只使用临时 Workspace 和非敏感边界。

## P1 — Registry、Binding 与 Session 持久事实

### P1.1 Registry permission configurability

在现有 `AGENT_ADAPTER_REGISTRY` / Compatibility Registry 中增加最小 capability facts：

```text
can_read_access
can_apply_session_access
can_apply_persistent_access
can_verify_effective_access
supported_requested_intents
mapping_evidence
```

这些字段描述 Adapter 能力，不创建另一份 Agent Registry。`RESEARCHED` 不得自动成为 configurable。

### P1.2 Execution Binding requested intent

在现有 Execution Binding 权威对象中保存：

- `requested_intent`；
- user consent receipt/ref；
- authorized resource refs；
- adapter mapping/version reference。

不保存明文 credential，不把 Employee 变成电脑权限 owner，不让 Workspace 自动产生 granted。

### P1.3 Session effective snapshot

每次新建与恢复保存：

- effective state；
- sandbox/filesystem/shell-tools/network/external-app/approval 诊断维度；
- evidence source/time/native+adapter version；
- temporary elevation；
- expiry；
- drift。

Session snapshot 复用现有 Session/Result/Audit 持久路径。是否需要 Schema 变化必须由未来正式 Issue 在代码审计后确定，本计划不授权 Schema。

### P1 acceptance candidate

- `Detected != Configurable != Granted != Available` 在 Registry/API 测试中不可折叠；
- `Requested != Configured != Effective` 在 Binding/Session 测试中不可折叠；
- Agent 切换只迁移 requested intent/resource refs；
- resume、版本变化、native config 变化可产生 drift；
- 用户三档不出现在 Runtime 分支条件中，Runtime 只消费 requested intent 与 effective facts。

## P2 — 真实 Adapter 出现后逐个 mapping

每个 Agent 必须同时具备以下前提后，才建立单独 Issue：

1. 当前机器真实安装并检测到稳定 CLI/API/service；
2. 官方授权通过；
3. 版本锁定；
4. 有真实 Employee/Workspace 用例；
5. 官方 permission/sandbox 控制面可引用；
6. 可以在隔离环境验证 failure/recovery。

逐 Agent Issue 只实现该 Adapter 的 `inspect/map/apply/verify`，不得抽象成通用 policy engine。

- 原生机器接口可设置和验证：按真实能力实现；
- 只能在 WorkBuddy/TRAE 等产品内设置：`USER_CONFIGURATION_REQUIRED`；
- 当前 Adapter 不支持：`UNSUPPORTED`；
- 无法读取有效状态：`UNKNOWN`；
- GUI-only：禁止 UI automation。

## 5. Full Computer Access gate

Full Computer Access 继续禁止真实开启。对应 Adapter 必须全部满足后，才允许提出独立安全 Review：

- `can_apply_session_access=true` 或经批准的 persistent apply；
- `can_verify_effective_access=true`；
- 能明确说明 filesystem、shell/tools、network、external apps 中的支持与缺失；
- 有 Session expiry/revoke/drift；
- OS/root/admin/MDM/Provider hard stop 保持；
- 有隔离环境 failure/recovery evidence；
- 用户选择与 Active 状态分离。

任何一个条件缺失，前台只能显示“当前接入暂不支持完全访问”或“无法确认是否已生效”。

## 6. Future Issue discipline

- P0、P1、每个 P2 Agent 分开建 Issue；
- Issue 必须先审计当前调用方和持久路径，再锁定 allowed files；
- 不允许把 P0/P1 塞入 XHS、Workspace UI 或其他业务 Issue；
- 不允许顺带实现权限 UI、Full、其他 Agent 数量扩张或通用权限引擎；
- Quality 只按本 Issue 的真实 requested/effective evidence 验收，不用 API 200、命令成功或卡片状态代替。

## 7. Planned completion states

| Stage | 计划完成含义 | 不代表 |
| --- | --- | --- |
| P0 complete | Codex requested/effective 与 resume evidence 真实 | Full 可用、其他 Agent 可用 |
| P1 complete | Registry/Binding/Session 能持久表达 Contract | 某 Agent 已 granted/available |
| P2 per Agent complete | 一个真实 Agent 的 mapping 通过独立 Review | 所有 Agent 权限统一或可互换 |

**AGENT COMPUTER ACCESS AUTHORITY SYNC REVIEW REQUIRED**  
**RUNTIME DELTA PLANNED**
