# CURIS RD — PRODUCT TRANSLATION IMPACT

**Authority Class**: RESEARCH
**Status**: Draft → Review
**目的**：把研究结论翻译成"**RD 产品表达与 Runtime 需求**"，并回答用户 §23、§24-23/24。
**边界**：本文件**不改任何 RD HTML**；仅做影响评估与待办清单。

---

## 1. 评估方法

本轮**未改** RD 原型，但**读取**了既有原型源码（`RD_WORKSPACE_HTML_EXPLORATION/`，L2 级证据——直接读文件而非推测）。取样命令：

```
grep -o -i -E ".{0,60}<pat>.{0,60}" "RD Workspace.html" | sort -u
```

关键词出现次数（单文件版，3000 行）：

| 关键词 | 次数 | 说明 |
|---|---|---|
| `provider` | 52 | 已是一等概念 |
| `Codex` | 14 | 已作为具体 Provider 出现在 mock 数据 |
| `Claude` | 13 | 同上 |
| `Git` | 12 | **只出现在"来源 GitHub API_SYNC" 与"不画 Git"的原则文案中** |
| `Workspace` | 4 | **只出现在标题/文件名**（"RD Professional Workspace"），**不是工程工作区概念** |
| `worktree` | **0** | **完全没有** |
| `branch` | **0** | **完全没有** |

---

## 2. 已对齐的部分（好消息：原型的方向是对的）

| 原型既有表达 | 与研究结论是否一致 |
|---|---|
| `Provider 是能力提供方，Employee 是责任归属者`（原型内明文原则） | ✅ **高度一致**。这正是本目录 09 号文档 CO1 的核心，也与 AO 的 adapter 层、container-use 的 "no vendor lock-in" 同向 |
| `work.provider` 字段 + `▶ 执行` 动作（`data-action="exec-provider"`） | ✅ 方向正确：Work 上绑 Provider，而不是人绑 Provider |
| `已拆成两个并行 Work：W-231 走 Codex、W-232 走 Claude Code，互不干扰` | ⚠️ **结论正确但缺机制支撑**（见 §3-2） |
| `回流 Development 重新派发修复，同/异 Provider 均可` | ✅ 与"Provider 可替换（L-b 换 Executor）"一致 |
| `Decision / needs_ceo` 状态存在 | ✅ 与 CO9 Decision Gate 一致 |
| `不画 IDE / Terminal / Git / CI / 部署工具` | ✅ 与"Curis 不做 Provider 的 UI / 不做 git 工具"一致，**但需细化**（见 §3-4） |

---

## 3. 需要修改的产品表达（6 项，按严重度排序）

### IMPACT-1（最高）**Provider 被画成了"对话参与者"，与自身原则矛盾**

**现状（原型原文）**：
```js
{ who: 'provider', name: 'Claude Code', t: '10:12', text: '已加 tenant_id 强制 scope…' }
{ who: 'provider', name: 'Codex', t: '09:14', text: '已应用批量查询重构…' }
```
即：**Codex / Claude Code 直接以发言者身份出现在 Conversation 主面**。

**与本目录结论的冲突**：
- 09 号文档 CO1/CO2：Conversation 是 **CEO ↔ Employee 的持续关系**；Provider 是 **Employee 调用的能力**，不是关系的一端。
- 06 号文档 §3.3：Provider 之间**没有跨系统对话协议**；把 Provider 放进对话，等于把"执行过程"冒充"组织沟通"。
- 原型自己的原则文案也写着"Employee 是责任归属者"——**UI 与原则自相矛盾**。

**建议方向**（不改本轮，供 CEO 裁定后执行）：
- Conversation 主面的发言者**只应是人（CEO）与 Employee**；
- Provider 的输出应作为 **WorkResult（附着在 Work 上的结果对象）**呈现，可由 Employee 引用（如 `ref-diff-230` 的做法已经是正确方向）；
- 若确实需要"看 Provider 说了什么"，那是 **Execution Context 的日志视图**（诊断用），不是对话流的参与者。

### IMPACT-2（高）**"并行 Work 互不干扰"缺少机制表达，且当前表述无法验证**

**现状**：
- 原型断言"已拆成两个并行 Work … 互不干扰"，但全文 **`worktree` / `branch` 出现 0 次**——即**没有任何东西告诉用户"靠什么做到互不干扰"**。
- 研究结论（04 号文档 I2 不变量）：**10/10 成熟实现都靠"每 Work 一个隔离工作区"**；共享 working tree 会互相覆盖。

**建议方向**：
- Work 上应有一个**可查看的"执行位置"表达**（不是 IDE、不是文件树）：例如"隔离工作区 · 分支 `work/W-231-…` · 基线 `a1b2c3d`（只读摘要）"。
- **不需要**展示目录树、不需要暴露 git 命令；但"**这一份 Work 的改动与那一份是分开的**"必须是可见事实，否则 CEO 无法判断风险。

### IMPACT-3（高）**状态挂在 Provider 上，而状态应当是 Work（与事实）的派生**

**现状**：
```js
provider: 'Claude Code', status: 'working'
provider: 'Claude Code', status: 'needs_ceo'
provider: 'Codex', status: 'working'
```

**冲突**：
- 05/08 号文档结论：**状态应由事实派生，且 Work 状态 ≠ Provider 会话状态**；AO 的 `status.go` 把 15 个状态**派生自**会话事实 + PR 事实。
- 把 `status` 挂在 Provider 上会导致：换 Provider 时状态语义断裂；同一 Provider 有多个 Work 时无法区分；`needs_ceo` 这类**组织状态**被错误地归给技术组件。
- 另外，`needs_ceo` 是**组织语义**，Provider 不可能"需要 CEO"——它只能是 **Work 或 Employee 的状态**。

**建议方向**：
- `status` 归 **Work**；`needs_ceo` 归 **Work/Decision**；
- Provider 侧只保留**技术事实**（如 `activity: active / idle / blocked / exited / no_signal`），**并且必须能表达 `no_signal`**（AO 的教训）。

### IMPACT-4（中）**缺少 WorkResult / Verification 两个对象**

**现状**：原型有 `ref-diff-230` 这类引用与 Provider 的文字汇报，但没有把"**结果**"与"**验证**"建模为独立对象。

**冲突**：07 号文档 §3.4 —— **跨 Provider 交接协议不存在**，Curis 必须自己定义 `WorkResult = {diff, files, test_evidence, unresolved, logs_pointer}`；且 F10 证明"agent 自报完成不可靠"，因此 **Verification 必须独立于执行**。

**建议方向**：在 Work 上增加两个可展开的区块（不是新页面）：**结果（diff + 变更文件 + 未解决项）** 与 **验证（谁验的 / 验了什么 / 结论）**。

### IMPACT-5（中）**"不画 Git"这条原则需要细化，否则会丢关键信息**

**现状**：原型原则文案："不画 IDE / Terminal / Git / CI / 部署工具"。

**研究发现**：这条**方向正确但过粗**：
- ✅ 正确的部分：Curis 不该做 git 工具界面（提交图、diff 编辑器、冲突解决器）。
- ⚠️ 会丢的部分：**分支名 / 基线 / 隔离位置**这三样是"风险可见性"的必需信息（04 号文档 I5 不变量）。Claude Code 甚至用**不可关闭的强制校验**来保证 agent 不窜到主工作区——说明"隔离是否真的生效"本身是需要被确认的事实。
- 建议改写为："**不做 git 工具；但必须让『这次改动从哪来、在哪做、与谁隔离』可见。**"

### IMPACT-6（低-中）**缺少"Work → 下一个 Work"的接力表达**

**现状**：原型有"回流 Development 重新派发修复"，但形式是"重新派发"，**不是"接力"**。

**研究结论**（06 号文档 §3.1、07 号 §3.1）：H-A（同 Work 换执行体）、H-B（Work → Work）、H-C（Work → Canonical）是三种不同交接；Curis 三者都需要，且 **H-C 必须建模为 Gate**。

**建议方向**：Work 的结束态应区分"**已完成待收口**"与"**已收口**"，前者可被下游 Work 引用（但**不算真相**）。

---

## 4. 需要建立的 Runtime 需求（不在本轮实现，仅登记）

| # | 需求 | 依据 | 优先级 |
|---|---|---|---|
| R1 | **Workspace 分配与回收**（Option D：worktree 默认） | 04 号文档 §4 | P0 |
| R2 | **WorkspaceRegistry**（path/branch/base_ref/lock/reclaim_policy） | 04 号文档 §4.3 | P0 |
| R3 | **Provider 四槽适配层**（agent / reviewer / workspace / runtime） | 07 号文档 §2 | P0 |
| R4 | **WorkResult 归一化 schema** | 09 号文档 CO7 | P0 |
| R5 | **状态派生层**（持久事实 → 派生状态；含 `no_signal`） | 08 号文档 §2 | P0 |
| R6 | **执行权限档位**（沙箱/审批档，显式选择，不默认全权） | 07 号文档 §4 | P1 |
| R7 | **Verification 触发与记录**（默认换 Provider 验；高风险强制人验） | 09 号文档 CO8 | P1 |
| R8 | **Review 路由**（默认"换一个 Provider 审"） | 07 号文档 §3.1 L-a | P1 |
| R9 | **WorkResult 交接（H-A/H-B）** | 06 号文档 §3 | P1 |
| R10 | **文件集重叠预警**（分配 Workspace 时提示冲突风险，不做锁） | 05 号文档 §3.1 | P2 |
| R11 | **依赖 + 超时兜底**（防"任务状态滞后卡死依赖"） | 06 号 §2 C2 | P2 |
| R12 | **容器档位**（`strategy` 字段预留，v1 不实现） | 04 号文档 §6 U1 | P3 |

---

## 5. 明确"不应进入产品"的东西（防止把 Provider 细节泄漏到 UI）

| 不应出现 | 理由 |
|---|---|
| git 命令、分支图、冲突解决器 | 原型既有原则已定；研究支持 |
| Provider 私有概念的直译（如 "Agent Teams"、"subagent"、"mailbox"、"worktree lock"） | 07 号文档 R1/R3：不得以 Provider 命名产品概念 |
| 目录树 / 文件浏览器 | Provider 有自己的 UI；Curis 不重复 |
| "agent 说它完成了"作为完成依据 | F10 |
| "正在运行中"这种乐观状态 | AO 的 `no_signal` 教训 |
| 会话入口列表 / 终端面板 | 那是 Provider/IDE 的形态（Orca/parallel-code 的做法），不是 Curis 的组织形态 |

---

## 6. 回答用户 §24-24：是否已足够进入 RD 定向视觉修订？

**结论：研究层面已足够，但建议先取 CEO 一次裁定，再进入视觉修订。**

理由（三条）：
1. **底层工作模型已经清楚**：Workspace 模型（Option D）、Context 四分层、Capability Decomposition、交接与失败恢复模型均已成形，且每条都有业界证据；**不会再因为"机制不清楚"而反复推翻视觉。**
2. **但有 6 项产品表达需要先裁定**（§3 IMPACT-1/2/3 是结构性的，会直接改变 Conversation 主面与 Work 卡片的表达）——**先改视觉再裁定，等于返工。**
3. **本轮被明确要求"不做 UI"**，因此正确的下一步是：**CEO 对 §3 与 §4 表一次态 → 再开 RD 定向视觉修订。**

**建议的 Gate 表述（供 CEO 使用）**：
> 是否接受：①Provider 退出 Conversation 主面（改为 WorkResult 对象）；②Work 上增加"隔离位置（分支/基线）"只读表达；③状态归 Work 且必须能表达 `no_signal`；④Workspace 采 Option D（worktree 默认，容器预留）；⑤Provider 四槽适配层与 WorkResult 归一化列入 Runtime P0。

---

## 7. 遗留未知

| # | 未知 | 影响 |
|---|---|---|
| U18 | "隔离位置"在 CEO 视角要展示到什么粒度（只给分支名？还是也给基线 SHA？） | 影响 Work 卡片的信息密度 |
| U19 | Provider 的日志/输出是否需要一个"诊断视图"（默认藏在二级） | 影响 Execution Context 的产品化程度 |
| U20 | 是否允许 CEO 在 Conversation 里直接 @ 某个 Provider | 若允许，会重新把 Provider 拉回对话流（与 IMPACT-1 冲突） |
