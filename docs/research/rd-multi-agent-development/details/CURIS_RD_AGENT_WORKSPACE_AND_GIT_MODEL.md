# CURIS RD — AGENT WORKSPACE AND GIT MODEL

**Authority Class**: RESEARCH
**Status**: Draft → Review
**证据**：`E04`（AO adapter 层）、`E05`（AO session/status 源码）、`E06`（claude-squad worktree 源码）、worktrunk skill 文档（L2）、Claude Code worktrees 官方文档（L3）、Codex 官方工程文章（L4）、container-use README+源码（L2）、parallel-code `AGENTS.md`（L2）。

---

## 1. 结论先行

1. **Branch / Worktree / Clone / Sandbox 不是四选一，而是"三层不同职责"**：
   - **Branch = 变化线**（做什么改变，谁与谁的变更算同一线）；
   - **Worktree / Clone / Container = 执行位**（在哪个目录里改）；
   - **Sandbox = 权限边界**（进程能碰什么）。
   成熟系统**同时使用**这三层，而不是把三者混为一谈。
2. **git worktree 是 Curis v1 的正确默认**（理由与证据见 04 号文档 §4）。
3. **Git 该承担的比 Curis 想象的更多**：base ref 记录、变更集边界、冲突检测的**唯一权威**、回滚与审计。**Curis 不应自建任何版本控制语义。**
4. **GitHub 不是必需**：本项目 10/10 系统全部依赖 git，但只有 AO/Copilot/Orca 依赖 GitHub。Curis v1 是**本地 git**，GitHub 是可选远端。

---

## 2. 四种原语的职责拆解（详细）

### 2.1 Branch（分支）

| 问题 | 答案 |
|---|---|
| Git 天然负责什么？ | 变化线、提交图、合并/变基、冲突检测的**最终权威** |
| 成熟系统的命名约定 | Claude Code：`worktree-<name>`；Copilot：`copilot/*`；AO/claude-squad：per-session 分支（claude-squad 记 `branchName` + `isExistingBranch`） |
| Curis 应采纳 | **一律 `work/<work_id>-<slug>`**（Curis 前缀），并**显式记录 base ref/SHA**——因为 AO 的 `DiffBaseSHA`/`DiffBaseRef` 证明"没有 base 的记录，diff 就无法解释" |
| 硬约束 | **执行体不得写 Canonical Branch**（不变量 I3）。Copilot 用"只能推 `copilot/*`"在平台层面强制，Curis 应在**本地**用分支所有权规则强制 |
| 不要做 | 不要自建"分支状态机"；分支状态从 git 查询（`git merge-base`、`git rev-list --count`），像 worktrunk `wt list` 那样 **派生** |

### 2.2 Worktree（工作树）

| 维度 | 事实 |
|---|---|
| 共享什么 | **`.git` 目录（object store + refs）**；本地分支可见；提交写入共享历史 |
| 不共享什么 | 工作目录、index（暂存区）、HEAD |
| 默认落点（业界） | Claude Code：`<repo>/.claude/worktrees/<name>/`；claude-squad：`<configDir>/worktrees/`；worktrunk：由路径模板决定（支持 `hash_port`） |
| 已解决的坑 | ①**端口冲突** → worktrunk `hash_port` 模板；②**依赖目录重复安装** → parallel-code 用 **symlink 把 gitignored 目录链进新 worktree**、worktrunk `wt step copy-ignored`；③**误删既有分支** → claude-squad 的 `isExistingBranch`；④**并发清理** → Claude Code 运行期 `git worktree lock` |
| 已暴露的限制（Claude Code 官方） | `.claude`/worktree 目录为 symlink 时拒绝创建；Git LFS 下 worktree 只拿到指针文件（需手动 `git lfs pull`）；hook 的 `${CLAUDE_PROJECT_DIR}` **仍指向主 checkout**（要拿 worktree 路径必须用 `cwd`） |
| 对 Curis 的启示 | **"工作区路径"必须是一等字段，而不是从 cwd 猜出来的**；hook 类扩展必须显式接收 workspace path |

### 2.3 Clone（独立克隆）

| 维度 | 事实 |
|---|---|
| 优点 | 完全独立 remote/refs；天然的网络与凭据隔离；适合跨机器 |
| 缺点 | **磁盘翻倍**（完整历史）；**基线漂移**（canonical 前进后 clone 落后）；**合并要靠 push/patch 回传**，容易丢 base |
| 结论 | **Curis v1 不采用 as default**；仅在"需要把代码放到另一台机器/另一个容器里"时使用（那其实就是 Option D 的容器档位） |

### 2.4 Container / Sandbox（容器与沙箱）

| 维度 | 事实 |
|---|---|
| 谁在用 | container-use（**每个 agent 一个容器 + 一个分支**，Dagger 驱动，含 `flock.go` 做环境互斥）；Copilot cloud agent（**每个任务一个 GitHub Actions 容器**）；OpenHands（Docker workspace 档）；SWE-agent → **SWE-ReX**（独立成项目的"沙箱化代码执行"层，593★） |
| 容器≠安全（关键证据） | **Codex 官方明确警告**："Worktree isolation does not protect secrets or remote systems from an over-permissioned process."（worktree/容器隔离**不能**保护密钥，关键在权限） |
| 与 Codex 的关系 | Codex 的沙箱是**策略**而非容器：`-s/--sandbox {read-only, workspace-write, danger-full-access}` + `-a/--ask-for-approval {untrusted, on-request, never}` + `--add-dir`（额外可写目录）。本机实测 config 为 `danger-full-access`。 |
| Copilot 的安全设计（最完整样板） | ①agent **只能推 `copilot/*` 前缀分支**；②agent 创建的 PR 上 **Actions 不自动运行**，需有写权限的人显式批准（防通过 workflow 偷 secrets）；③环境**每次迭代重建**（含 review 后迭代） |
| 结论 | 容器应作为**按 Work 显式升级的档位**（Option D），而不是默认。**比容器更重要的是权限档位与 push 目标限制。** |

---

## 3. 冲突：三层防线（必须诚实说明各层的边界）

| 层 | 机制 | 能防什么 | **不能防什么** |
|---|---|---|---|
| L1 结构隔离 | worktree / container per Work | **同文件同区域的并发写覆盖** | **语义冲突**（两个 Work 各自改同一函数的不同分支逻辑，测试各自通过） |
| L2 认领锁 | 任务级文件锁（Claude Code：`~/.claude/tasks/{team}/` 下按任务名的锁文件） | **同一任务被两个执行体同时认领** | **文件写冲突**——Claude Code 官方原文："Locking applies to task claiming, not file writes." |
| L3 收口检测 | merge/rebase 时的 git 冲突 + 测试/CI | **真实冲突在收口时被暴露** | 冲突**不会提前被发现**；本领域**没有任何系统做到"写前冲突预防"** |

### 3.1 Curis 应当做的（不做的事同样重要）

**应做**：
- **按"所有权"而非"意图"切分 Work**（Codex 官方建议原文：split by ownership, not just by intention）——即先算出"这个 Work 会碰哪些文件/契约"，再检查是否与在跑的 Work 重叠。
- **Workspace 分配时做一次"文件集重叠预警"**（不需要精确，只需提示"两个在跑的 Work 都声称会改 `backend/app/task_*.py`"）。
- **收口时强制跑测试/构建**（Copilot 与 Codex 都靠这一步兜底）。
- **冲突发生时把它当成正常状态**（AO 的 `changes_requested` / `ci_failed` 都是正常看板列），而不是异常。

**不应做**：
- ❌ 不要做"文件锁防止写冲突"——会被并行退化成串行，且 Claude Code 已证明这层锁的语义边界。
- ❌ 不要做"提前精确冲突预测"（本领域无先例，投入产出比差）。
- ❌ 不要在同一 worktree 里跑两个 Provider 会话。

---

## 4. 文件归属（回应用户 §16）

### 4.1 五类文件与归属规则

| 文件类型 | 生成位置 | 归属判定 | 未通过 Gate 时 |
|---|---|---|---|
| **Code**（源码） | **只在 Workspace 内产生** | 通过 Gate → 进入 Canonical Branch；未通过 → 随 Workspace 保留或销毁 | 保留在 Workspace 分支，**永不进入 Canonical** |
| **Docs**（项目文档/决策记录） | 分两类：**项目真相类**（架构、决策、计划）应**直接入 Canonical**（走小 PR）；**本次工作的产出文档**在 Workspace 内产生 | 同 Code | 同 Code |
| **Tests** | 与 Code 同仓同时产生 | 同 Code（测试与实现必须同一变更集） | 同 Code |
| **Config** | ⚠️ **高敏**：机器级/凭据级配置**永不入 Workspace**（Copilot 的 secrets 只给 setup 阶段、agent 阶段移除，是同一原则） | 项目级配置走 Code 规则；机器级配置由 Curis 单独管理 | — |
| **Assets**（图片/模型/大文件） | Workspace 内可产生 | ⚠️ 需单独策略：本领域实践是**大文件不入 git**，用 artifact store | 保留在 Workspace |

### 4.2 三条硬规则

1. **写 Project Root 还是写 Execution Workspace？**
   → **一律先写 Workspace**。**唯一例外**：被授权"直接入 Canonical 的小改动"（如文档勘误）——但这必须是**显式授权的窄通道**，且仍需走 Gate。
   *证据*：没有任何成熟系统允许执行体直接写 canonical working tree；Claude Code 甚至用**不可关闭的强制校验**阻止编辑主 checkout。

2. **Result 通过 Review 后如何 Merge？**
   → Merge 是**独立的、显式的动作**，不是执行的自然结尾。AO 把它建模为 `mergeable`/`merged` 状态位，由人在看板上决定；Claude Code **明确不提供自动 merge/PR**。Curis 应把它建模为 **Gate（Decision）**，与既有 `Decision 内嵌 Banner` 的产品形态对齐。

3. **失败 Execution 产生的文件怎么处理？**
   → **默认保留 Workspace + 分支，标记为 failed**，而不是立即删除。
   *理由*：`container-use` 的 "discard failures instantly" 适合**容器**（环境可完全重建）；但 worktree 的失败产物往往**含诊断价值**（复现日志、半成品思路）。
   *建议策略*：Work 进入 `FAILED` → Workspace 保留至「保留期」结束（见 08 号文档）；用户可选择"保留为参考"或"立即销毁"。

### 4.3 Conversation 附件与 Project 归档

| 对象 | 处理 |
|---|---|
| **Conversation 附件**（CEO 上传的截图/文档） | 属于 **Conversation Context**，**不入 git**。落本地 `attachments/`（AO 有独立 `attachmentstore` 模块可参照）。若要进入工程，必须**显式导入**到 Workspace 并在变更集里出现。 |
| **临时 Artifact**（日志、中间产物、录屏） | 落 Workspace 外的 artifact 目录，与 Workspace **同生命周期**；被 Result 引用时只存**指针**。 |
| **Project 删除 / 归档** | Canonical Root 归档（不物理删除 `.git`）；Workspace **全部销毁**（可从 Canonical 重建）；Conversation 保留（因为它是问责记录）；**Decision 记录必须保留**。 |

---

## 5. Git / GitHub 各自承担什么（回应用户 §21、§24-21）

### 5.1 Git 天然负责（Curis 绝不重造）

| Git 能力 | 在 Curis 中的角色 |
|---|---|
| 分支与提交图 | Work 的变化线 |
| object store（worktree 共享） | 多 Workspace 的存储底座 |
| diff / patch | **Provider 交出的统一结果格式**（Codex `apply`、`codex cloud apply` 都是 patch 语义） |
| merge / rebase | 收口动作 |
| **冲突检测** | **唯一权威**——Curis 不得自建冲突判定 |
| reflog / 历史 | 事故回滚与审计 |
| worktree（子命令） | Workspace 底座 |
| lock | Workspace 运行期防清理 |
| ignore（`.gitignore`） | 决定哪些文件不参与变更集（也决定依赖目录能否 symlink 共享） |
| hooks | 本地强制门禁（pre-commit / pre-push）的天然位置 |

### 5.2 GitHub（或任何远端）负责（可选）

| 能力 | Curis v1 态度 |
|---|---|
| 远端备份 / 多机同步 | ✅ 可选（用户自己的远端） |
| PR 作为评审界面 | ⚠️ **可选**——AO/Copilot/Orca 把 PR 当唯一收口通道，但 Curis v1 是单机自用，**PR 不是必需**；Curis 内建的 Decision Gate 才是必需 |
| CI | ⚠️ 可选（本地测试优先） |
| branch protection / 只允许推 `copilot/*` | ⚠️ 这是 Copilot 的平台能力；**本地等价物 = 分支所有权规则 + Gate** |
| Issue 作为任务源 | ❌ v1 不需要（Curis 自己的 Work 模型就是任务源） |

### 5.3 明确的"不要由 Curis 重新开发"清单

1. 版本控制（分支/提交/合并/冲突/历史）——**全部交给 git**。
2. 工作区隔离原语——**用 `git worktree`，不要自己写目录复制逻辑**。
3. diff 的生成与呈现语义——**用 `git diff` / patch**，不要自建"变更描述格式"。
4. 依赖安装与构建——**交给项目自己的包管理器**（Curis 只负责"在 Worktree 就绪后触发"）。
5. 测试执行——**交给项目自己的测试命令**（Curis 只负责触发与收集结果）。
6. 沙箱/权限——**优先消费 Provider 已有的沙箱策略**（Codex `-s`/`-a`；Claude Code 的强制隔离校验），只有 Provider 完全没有时才考虑容器。

---

## 6. 遗留未知

| # | 未知 | 建议 |
|---|---|---|
| U6 | Curis 是否需要"Work 之间共享中间产物"（如 A 的接口定义给 B 用） | 建议 v1 **不共享**，通过 Canonical 收口后再取（最安全，且符合"只有 Gate 后的东西才算真相"） |
| U7 | Workspace 外置目录的默认位置（`~/Curis/workspaces/`？） | 待 CEO 裁定（涉及用户可见的目录约定） |
| U8 | 是否需要 `git worktree lock` 等价机制 | 建议需要（防"运行中被回收"），实现成本极低 |
| U9 | 大文件（资产/模型）策略 | 见 §4.1；建议 v1 只做"不入 git + 指针"，不做 LFS |
