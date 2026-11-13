# CURIS RD — CURIS-OWNED VS PROVIDER-OWNED

**Authority Class**: RESEARCH
**Status**: Draft → Review（**能力拆分提案，非 Authority**）
**方法**：对每一项能力问三个问题——①成熟系统里有没有人已经做好？②是不是 Provider/工具天然负责？③如果 Curis 不做，会不会违反 Curis 四原则或既有红线？
**证据**：本目录 02（Deep Dives）、03（Comparison Matrix）、04–08 号文档。

---

## 0. 一页结论

| 归属类 | 数量 | 一句话 |
|---|---|---|
| **Provider-owned**（Codex / Claude Code / …） | 12 项 | **执行、隔离、审查、压缩、沙箱**——这些已由 Provider 做好，Curis 不得重造 |
| **Orchestrator-owned**（可直接复用的开源 Runtime） | 6 项 | **并行会话监管、worktree 生命周期、四槽适配层**——有参考实现，可借设计甚至借用 |
| **Git-owned**（git / 远端） | 9 项 | **版本控制、diff、冲突检测、历史**——git 是唯一权威 |
| **Curis-owned**（必须自己拥有） | **11 项** | **组织语义、问责、Work 编排、归一化、Gate、长期运营状态** |
| **Human Gate**（必须人介入） | 7 项 | **范围/架构/凭据/商业/权限边界/高风险合并** |

**核心判断（直接回答用户 §12）**：

> Curis **不应该**做一个 Multi-Agent Coding Framework。成熟系统已经把它做完了。
> Curis 真正缺的是**"组织与问责层"**：谁负责、干什么、用谁的能力、结果算不算、谁拍的板、明天怎么接着干。
> 这一层**开源项目里一个都没有**——因为开源项目的用户是"一个工程师指挥一群 agent"，而 Curis 的用户是"一个人运营一家公司"。

---

## 1. Curis-owned（11 项，必须自己拥有）

| # | 能力 | 为什么必须 Curis 拥有 | 关联既有裁定/原则 |
|---|---|---|---|
| **CO1** | **Employee 身份与职责**（Responsibility Holder） | 开源项目**没有"员工"**：AO 有 worker/orchestrator 会话但**不是长期组织身份**；Claude Code 的 teammate 是**运行期进程**；Codex 的 thread 是**会话**。Curis 的 Employee 跨 Work、跨会话、跨 Provider 长期存在。 | 四原则③"员工=动态调用能力的岗位" |
| **CO2** | **Employee ↔ Conversation 的持续关系** | 类比：无。Claude Code 明确"teammate 不继承 lead 对话历史"；AO 的会话上下文不跨会话。**Curis 的 Conversation 是唯一"跨 Work 的关系记忆"。** | 既有 RD 形态：Employee Conversation 主面 |
| **CO3** | **Work 的定义与生命周期**（目标/验收/依赖/所有权/结算） | 各系统有 task/session/issue，但**都不含"验收标准 + 所有权切分 + 结算归一"**这一组语义。Claude Code 的 task 只有三态 + blockedBy；Copilot 的 task = issue。 | 四原则①"全自动任务流是核心" |
| **CO4** | **Assignment（Work → Provider 指派）** | 开源系统里 agent 是"选出来的"，不是"指派给某个负责人的"。**把 Work 指派给 Employee、再由 Employee 选 Provider**，这层语义不存在。 | 四原则②③ |
| **CO5** | **Workspace 分配与回收（Curis 拥有分配策略）** | AO 有 worktree 但绑定"工程师手动建 session"；Claude Code 的 worktree 由**用户敲命令**创建。**没有系统按"Work 语义"自动分配隔离工作区。** | 本目录 04 号文档 Option D |
| **CO6** | **Provider 抽象与路由（四槽位）** | AO 有 30+ 适配器——**但它是为单机工程师设计的**，不含"名额/能力/成本/可用性/用户偏好"的路由语义。Curis 需要**路由决策**，不是适配器列表。 | 四原则②"能力可替换不写死" |
| **CO7** | **WorkResult 归一化**（diff + 证据 + 未解决项 + 日志指针） | **跨 Provider 交接协议不存在**（本目录 06 号文档 §3.4）。每个 Provider 产物形态不同（Codex patch/apply、Claude Code 无自动 PR、container-use 分支）。**归一化层是空位。** | 四原则④"让目标→执行→验收→返工→完成更自动" |
| **CO8** | **Verification（独立于执行的验收）** | AO 有 reviewer 适配器，但**它的触发是"看板有人点"**；Curis 需要**按 Work 定义自动触发验证**，且必须解决 F10（agent 自报完成不可靠）。 | 既有"验收→返工"链路 |
| **CO9** | **Decision Gate（含内嵌 Banner）** | 开源系统的 Gate 是"人点 PR merge"或"人批准权限"。**Curis 的 Gate 是产品对象**（未决决策必须可见、可追溯、可阻塞）。 | 既有 RD 形态：Decision 内嵌 Banner |
| **CO10** | **长期运营状态**（项目事实持久 + 状态派生 + 审计） | AO 有 durable facts，但它是**单机工程师的看板状态**；Curis 需要"**为什么这么做**"的问责记录（Decision/Conversation/Work 历史）。 | 与 AO 的"事实 vs 派生"**同构但不同用途** |
| **CO11** | **升级与例外处理**（谁能越界、什么时候必须上人） | 开源系统把人当"操作员"；Curis 需要**预算/权限/范围/合规的例外路径**（对应既有 L2 Gate 7 项）。 | 既有 L2 Gate 与安全边界席 |

### 1.1 Curis-owned 的设计参照（不是从零想）

| Curis-owned | 最接近的参考实现 | 差在哪 |
|---|---|---|
| CO3 Work | Claude Code task（三态 + blockedBy + 自动解锁） | 缺"验收标准 / 所有权 / 结算" |
| CO5 Workspace 分配 | AO `adapters/workspace/router` + `SessionMetadata` | AO 由人建 session；Curis 由 Work 派生 |
| CO6 Provider 路由 | AO `adapters/agent`（30+） | AO 靠人下拉选择；Curis 需自动路由 + 显式覆盖 |
| CO10 长期状态 | AO "durable facts vs derived status" | 语义同构，内容不同（组织 vs 工程） |
| CO9 Gate | Copilot（PR + 人审批 + Actions 需批准） | Curis 的 Gate 是产品内对象，不依附 GitHub |

---

## 2. Provider-owned（12 项，不得重造）

| # | 能力 | 谁已做好 | 证据 |
|---|---|---|---|
| **PO1** | **代码生成与编辑** | Codex / Claude Code / Aider / OpenCode / Goose | 全部 Provider 的核心能力 |
| **PO2** | **在仓库内自主探索与定位** | Codex（AGENTS.md + docs 地图）、Claude Code（CLAUDE.md + skills） | Codex 官方文章 |
| **PO3** | **命令执行与工具调用** | 全部 Provider | 本机 Codex `exec` |
| **PO4** | **diff / patch 的产生** | Codex `apply`、`codex cloud diff/apply` | L1 实测 |
| **PO5** | **代码审查（同 Provider 内建）** | `codex review`（一等子命令） | L1 实测 |
| **PO6** | **上下文压缩** | Codex `/compact` + `remote_compaction_v2`；OpenHands Condenser | L1/L4 |
| **PO7** | **会话恢复** | Codex `resume` / `fork`；Claude Code `/resume` | L1/L3 |
| **PO8** | **沙箱与权限档位** | Codex `-s {read-only,workspace-write,danger-full-access}` + `-a {untrusted,on-request,never}`；Claude Code permission modes + 强制隔离校验 | L1/L3 |
| **PO9** | **Provider 内部的多 agent 协作** | Codex `multi_agent`（**stable**）；Claude Code agent teams（experimental） | L1/L3 |
| **PO10** | **测试/构建/静态检查的执行** | 项目自身的工具链（Provider 只负责触发） | 通用事实 |
| **PO11** | **浏览器与桌面自动化** | Codex `browser_use` / `computer_use`（均 stable）；Orca Design Mode | L1 |
| **PO12** | **Provider 自身的 UI/终端** | Codex App、Claude Code TUI、Orca、parallel-code | L4 |

> **规则**：Curis 若实现其中任何一项，就等于**在 Provider 之上做了一层更差的重复实现**，并**破坏可替换性**。

---

## 3. Orchestrator-owned（6 项，可复用/可借设计）

| # | 能力 | 参考实现 | Curis 应"借"什么 | 风险 |
|---|---|---|---|---|
| **OO1** | **多会话并行监管 + 状态派生** | AO（daemon + SQLite + CDC + SSE；状态读取时派生） | **架构模式**（durable facts vs derived status）；否**不**直接依赖其运行时 | AO 外围越界 |
| **OO2** | **Workspace 生命周期（worktree）** | worktrunk（分支寻址 + hooks + `hash_port` + `copy-ignored`）；claude-squad（`isExistingBranch`）；parallel-code（symlink 依赖） | **约定与坑清单**；License 需核（worktrunk = NOASSERTION） | 直接依赖会引入 Rust/Go 工具链 |
| **OO3** | **容器化隔离（可选档位）** | container-use（MCP server，零 agent 绑定，Apache-2.0） | 若 v1 要做容器档，**这是唯一"可当 MCP 工具复用"的实现** | 仓库自标 experimental；release 停滞 |
| **OO4** | **四槽适配层设计**（agent / reviewer / workspace / runtime） | AO `backend/internal/adapters/*` | **目录结构与接口切分**（这是"可替换"最直接的落地形态） | 需要适配层自身有测试 |
| **OO5** | **事件流 + replay** | OpenHands EventLog（append-only、可增量确定性 replay） | 若要"执行可复现"，这是最完整的模型 | OpenHands 体量大 |
| **OO6** | **沙箱化执行接口** | SWE-ReX（独立项目，593★，MIT） | 若要"任意命令都进沙箱"，这是**独立可复用**的层 | 研究项目，非产品 |

> **判决**：`Untrivial-ai/agent-orchestrator` 是**唯一九项全满足**的候选（见 03 号文档 §E），但**建议把它当"参考架构"而非"被依赖的运行时"**——理由：①它绑定 GitHub/Cloud/移动/计费外围；②Curis 需要的是组织层，不是工程师管理台；③引入它意味着 Curis 的运行时要跟着它的发布节奏走。**若未来要真正复用，属 L2 Gate。**

---

## 4. Git-owned（9 项，由 git/远端天然负责）

| # | 能力 | 由谁 | Curis 的角色 |
|---|---|---|---|
| **GO1** | 版本控制（提交图） | git | 只读事实 |
| **GO2** | 分支 | git | **命名约定 + 所有权规则** |
| **GO3** | worktree（隔离底座） | git | **分配/回收策略**（CO5） |
| **GO4** | diff / patch | git | **消费为 WorkResult 的一部分**（CO7） |
| **GO5** | merge / rebase | git | **触发时机由 Gate 决定**（CO9） |
| **GO6** | **冲突检测** | git（**唯一权威**） | 只做"文件集重叠预警"，不做冲突判定 |
| **GO7** | 历史 / reflog（审计与回滚） | git | 审计入口 |
| **GO8** | hooks（本地强制门禁） | git | 挂"提交前必须过测试"类规则 |
| **GO9** | 远端同步 / 备份 / CI（可选） | GitHub 等 | 可选，非 v1 必需 |

---

## 5. Human Gate（7 项，必须人介入）

| # | Gate | 触发条件 | 为什么不能自动 | 对应既有裁定 |
|---|---|---|---|---|
| **HG1** | **范围 / 架构变更** | Work 会改变项目结构、契约、目录约定 | 属于产品决策 | 既有固定顺序 Blueprint → Design → Code |
| **HG2** | **凭据 / 登录** | Provider 或工具需要登录、需要 key | 既有硬约束：密钥只驻 `.env`；且**禁重试登录/绕 CAPTCHA/切账号** | 既有 `WAITING_FOR_USER` |
| **HG3** | **高风险合并**（不可逆 / 影响数据 / 影响发布） | 涉及数据迁移、删除、对外发布 | 不可逆 | 既有 Gate 语义 |
| **HG4** | **权限边界扩张** | agent 请求超出当前权限档 | 安全边界 | 既有 L2 Gate ⑤⑥ |
| **HG5** | **商业 / 收费 / 新市场 / Marketplace** | 触发既有 7 项 L2 Gate | 超出既有裁定范围 | 既有 L2 Gate ①–④⑦ |
| **HG6** | **`effect_unknown`**（写操作结果未知） | 写已发出、结果不可确认 | 自动重放会产生重复副作用 | 既有 G4 |
| **HG7** | **Agent 自我报告完成的最终确认**（首次 / 高风险 Work） | Verification 与执行体结论冲突，或首次运行新 Provider | F10：agent 自报完成不可靠 | 本目录 06 号文档 |

---

## 6. 绝不重新开发的清单（用户 §22 直接回答）

1. **不做 Multi-Agent Coding Framework**（编排、并行、隔离、审查已由 Provider + 开源 Orchestrator 完成）。
2. **不做版本控制语义**（分支/提交/合并/冲突/历史 → git）。
3. **不做工作区隔离原语**（→ `git worktree`；可选容器 → container-use 式方案）。
4. **不做 diff / patch 格式**（→ git / Provider）。
5. **不做 agent 内部的上下文压缩**（→ Provider `compact`/Condenser）。
6. **不做 Provider 内部的 subagent / agent teams 机制**（→ Provider 自己，Codex `multi_agent` 已 stable）。
7. **不做浏览器/桌面自动化引擎**（→ Provider `browser_use`/`computer_use`；或既有 CGAP-01 Playwright 结论）。
8. **不做代码审查模型**（→ `codex review` 类能力 + 换 Provider 评审）。
9. **不做测试框架**（→ 项目自身工具链）。
10. **不做项目地图的机械校验器以外的知识库系统**（可借 Codex 官方实践：linters + CI + doc-gardening agent）。
11. **不把 GitHub PR 做成 v1 的必需通道**（单机本地自用；PR 是可选远端能力）。

---

## 7. 与既有红线的对齐检查

| 红线 | 本拆分是否触碰 |
|---|---|
| v1 = 单机本地桌面自用 | ✅ 未触碰（Provider 与 git 都是本地；容器档位为可选未实现字段） |
| 暂不建设：独立 Admin / 物理多租户 / 计费订阅 / 多真实员工协作 / 深度 CRM-ERP / Marketplace 开放生态 | ✅ 未触碰（CO1 的 Employee 是**单机单用户**的组织语义，不是多租户员工协作） |
| v1 允许：连接自己的外部模型/Agent/Skill/Tool（API key 自用） | ✅ **本拆分正是这条允许项的落地**（Provider 抽象 + BYOK） |
| 能力可替换不写死 | ✅ 十一次拆分中 Provider-owned/Orchestrator-owned 的存在就是为了保证此条 |
| 不得另造状态名 | ✅ 复用 `WAITING_FOR_USER` / `EFFECT_UNKNOWN`；新增术语（Workspace / WorkResult）均标注为**提案**，待 CEO 裁定 |
| 仅结构候选，不得当 Authority | ✅ 本文件 `Authority Class: RESEARCH` |
