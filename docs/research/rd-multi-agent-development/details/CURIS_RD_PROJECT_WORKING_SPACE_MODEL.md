# CURIS RD — PROJECT WORKING SPACE MODEL

**Authority Class**: RESEARCH
**Status**: Draft → Review（**候选模型，不得当 Authority**）
**依赖证据**：`E01`（元数据）、`E03/E04/E05`（Agent Orchestrator 源码）、Claude Code worktrees 官方文档（L3）、Codex 官方工程文章（L4）、container-use / claude-squad / parallel-code / worktrunk 源码（L2）。

---

## 0. 先定义术语（避免"Project"一词被用成三种意思）

| 术语 | 定义 | Curis 现有一致性 |
|---|---|---|
| **Canonical Project Root** | 该项目的**唯一工程真相目录**（含 `.git`、源码、文档、测试、配置、项目指令）。物理上只有一个。 | ✅ 与既有裁定一致：Project = RD Workspace 内的 **Project Context**，不升格为组织层级 |
| **Repository** | Canonical Project Root 内的 git 仓库（`.git`）。历史与对象库的唯一持有者。 | 新增术语（此前隐含） |
| **Workspace（工作区）** | **一次 Work 的隔离工作目录**，从 Canonical Project Root 派生，完成后再回到 Canonical。 | 新增术语，是本文件核心 |
| **Working Tree** | git 意义上的工作树（某个分支的检出）。**Curis 内部禁止"多个 Work 共享同一个 Working Tree"**。 | 新增术语 |
| **Work** | 一个有目标的执行单元（Curis 既有词），对应"一个隔离 Workspace + 一个 Provider 会话"。 | ✅ 复用既有词 |
| **Canonical Branch** | 被认定为"已收口"的分支（本地单机场景即 `main`）。**只有通过 Gate 的 Work 才能进入**。 | 新增术语 |

**判定**：Curis 此前把"Project"当"语境"，本模型把"**Project Root 是资产**、**Workspace 是消耗品**"这一区分显式化。**Project Root 长期存在；Workspace 可随时销毁重建。**

---

## 1. 不变量（Invariants，任何候选方案都必须满足）

| # | 不变量 | 依据 |
|---|---|---|
| I1 | **Canonical Project Root 永远只有一份**，且永远是唯一工程真相源 | 全部 10 个成熟实现 |
| I2 | **同一个 Working Tree 不得被两个执行体同时写入** | 全部 10 个实现无一例外 |
| I3 | **执行体不得直接写 Canonical Branch** | Copilot cloud agent（只能推 `copilot/*`）；Claude Code（强制隔离校验阻止编辑主 checkout） |
| I4 | **Workspace 是消耗品**：可销毁、可从 Canonical 重建、销毁不损失已收口成果 | container-use "discard failures instantly"；claude-squad worktree 清理 |
| I5 | **每个 Workspace 必须记住自己的 Base Ref/SHA**（否则 diff 无意义） | AO `SessionMetadata.DiffBaseSHA / DiffBaseRef`（源码级） |
| I6 | **收口必须经过显式 Gate**（人，或人预先授权的规则） | Copilot（人审批）、Claude Code（无自动 merge）、AO（mergeable 由人决定） |
| I7 | **Workspace 的隔离强度必须可配置**，而不是写死一种 | Codex `-s read-only\|workspace-write\|danger-full-access`；AO `workspace/router`；OpenHands 三档 |
| I8 | **Workspace 生命周期必须有 owner**（谁创建、谁清理、何时清理） | Claude Code worktree 清理规则（干净自动删 / 有改动询问 / `-p` 不清理）；worktrunk `wt remove` |

---

## 2. 三种候选（用户指定 A/B/C）+ 第四种（研究新增 D）

### Option A — Single Project Root + Git Worktree per Work

```
Canonical Project Root  (~/Curis/projects/<project>)
├── .git/                      ← 唯一 object store，全部 worktree 共享
├── (source, docs, tests, config, instructions)
└── .curis/workspaces/
    ├── W-001/   branch: work/W-001-<slug>   base: <sha>
    ├── W-002/   branch: work/W-002-<slug>   base: <sha>
    └── W-007/   branch: work/W-007-<slug>   base: <sha>
```

| 维度 | 评估 |
|---|---|
| **Context continuity** | ✅ 最高——每个 worktree 有完整源码与历史，agent 直接读真实代码 |
| **Isolation** | ⚠️ 中——文件系统/分支隔离可靠；**但共享工具链、端口、依赖目录、本机环境**（如同时跑 dev server 会撞端口） |
| **Disk cost** | ✅ 低（共享 object store；仅工作树文件 + 依赖目录） |
| **Git complexity** | ⚠️ 中——worktree 增删、锁定、分支复用、清理时机、`worktree prune` |
| **Merge complexity** | ⚠️ 中——分支 merge/rebase；冲突在此时才显现 |
| **Provider compatibility** | ✅ 最高——任何 CLI agent 只需 `cd <worktree> && <agent>`；Codex `-C`、Claude Code `--worktree` 都原生支持 |
| **Recovery** | ✅ 好——worktree 就是普通目录，崩溃后仍在；分支与提交已在共享 object store 中 |
| **Security** | ⚠️ 中——工作区与主目录同一用户权限；agent 理论上可 `cd` 出去（需靠 Codex sandbox / Claude Code 强制校验补） |
| **Local-first** | ✅ 完全本地，零外部依赖 |
| **业界验证** | ✅✅ 最强——本领域主流（Orca/AO/claude-squad/worktrunk/parallel-code/Claude Code/vibe-kanban） |

### Option B — Canonical Repo + Sandbox / Clone per Agent Execution

```
Canonical Project Root
└── (只读基线 / 收口目标)

Execution Sandbox N（独立 clone 或容器）
├── git clone <canonical> → 完整历史副本 或
├── container: 镜像 + 挂载 canonical 的分支
└── agent 在沙箱内工作 → 产出 patch / push 到 canonical 的分支
```

| 维度 | 评估 |
|---|---|
| **Context continuity** | ⚠️ 中——clone 有一致历史但**漂移风险**（canonical 前进后，沙箱基线变旧）；容器需挂载或重建才拿到最新 |
| **Isolation** | ✅✅ 最高——文件系统 + 进程 + 网络 + 运行时全隔离（可复现环境） |
| **Disk cost** | ❌ 高（clone 整份历史；容器还有镜像层） |
| **Git complexity** | ✅ 低（沙箱内是独立仓库，无需管 worktree） |
| **Merge complexity** | ❌ 高（需要 cross-repo 推送或 patch 传输，容易丢 base） |
| **Provider compatibility** | ✅ 高（agent 只需能在容器里跑；但需要 Provider 支持 headless/非交互） |
| **Recovery** | ✅ 好（沙箱丢弃即可重建） |
| **Security** | ✅✅ 最高——这是唯一能真正限制"agent 越界访问本机文件/凭据"的方案 |
| **Local-first** | ⚠️ 本地容器可行（Docker/OrbStack），但引入容器运行时依赖 |
| **业界验证** | ✅ container-use（容器+分支）、Copilot cloud agent（Actions 容器）、OpenHands（Docker）、SWE-ReX |

### Option C — Provider-native Workspace

```
Curis 不自己管理 Workspace，而是消费 Provider 的原语：
  Codex      → App 线程的 Local / Worktree 选择；或 codex cloud 任务
  Claude Code→ claude --worktree <name>（.claude/worktrees/<name>/）
  OpenHands  → Workspace（local/docker/remote）
  其他        → 各自的隔离机制
Curis 只记录"这个 Work 用了哪个 Provider 的哪个 Workspace 标识"
```

| 维度 | 评估 |
|---|---|
| **Context continuity** | ✅ 好（Provider 自己保证） |
| **Isolation** | ✅ 好（Provider 自己实现，且往往比自己写更严格——Claude Code 有强制隔离校验） |
| **Disk cost** | ✅ 低-中（沿用 Provider 默认位置） |
| **Git complexity** | ✅✅ **最低**（Curis 不碰 git worktree 生命周期） |
| **Merge complexity** | ❌ **最高且不可控**——不同 Provider 的 workspace 落在不同位置、不同分支命名、不同清理规则；**统一收口极难** |
| **Provider compatibility** | ❌ **最差**——Claude Code 的 worktree 只能被 Claude Code 用；Codex 的 App worktree 甚至**不能被 CLI 调用**（本机实测：CLI 无 `--worktree`）。**这与 Curis 的"能力可替换不写死"直接冲突。** |
| **Recovery** | ⚠️ 取决于 Provider（Claude Code `-p` 模式不清理但也不恢复；Codex 有 resume） |
| **Security** | ⚠️ 取决于 Provider，不可统一审计 |
| **Local-first** | ✅（Codex/Claude Code 本地） |
| **业界验证** | ⚠️ 有先例但**无跨 Provider 统一先例**；Orca/AO/parallel-code 之所以自己管 worktree，正是因为 Provider-native 不统一 |

### Option D（研究新增）— Hybrid：Canonical Root + Worktree 为默认底座 + 容器为可选档位 + Provider-native 仅作加速

```
Canonical Project Root
└── Workspace Allocator（Curis 拥有）
    ├── 默认 → git worktree（Option A 的全部优点）
    ├── 需要强隔离时 → 容器（Option B 的能力，按 Work 显式选择）
    └── 若 Provider 原生更优 → 允许 Provider 自建，但必须"登记回 Curis"（Workspace Registry）
```

| 维度 | 评估 |
|---|---|
| **Context continuity** | ✅ 高（默认 worktree 保真；容器档位继承同一 base SHA） |
| **Isolation** | ✅ 可调（默认中，危险 Work 升级到高） |
| **Disk cost** | ✅ 默认低；仅少数 Work 付容器成本 |
| **Git complexity** | ⚠️ 中（Curis 必须自己做 worktree 生命周期——**但这是已被 worktrunk/parallel-code/claude-squad 解决过的问题**） |
| **Merge complexity** | ✅ 可控（统一 base SHA + 统一分支命名 = 统一收口） |
| **Provider compatibility** | ✅✅ 最高（只要 Provider 能 `cd` 到某个目录跑，就能用） |
| **Recovery** | ✅ 好（worktree 落盘 + 登记表） |
| **Security** | ✅ 可调（默认本机权限，敏感 Work 上容器） |
| **Local-first** | ✅（默认零外部依赖） |
| **业界验证** | ✅ 组合式——AO 正是"worktree 默认 + container 回收"；OpenHands 正是"三档 Workspace" |

---

## 3. 决策表

| 判据 | A | B | C | **D** |
|---|---|---|---|---|
| Context continuity | 高 | 中 | 高 | **高** |
| Isolation | 中 | 高 | 高 | **中→高（可调）** |
| Disk cost | 低 | 高 | 低-中 | **低** |
| Git complexity | 中 | 低 | 极低 | **中** |
| Merge complexity | 中 | 高 | 极高 | **中** |
| Provider compatibility | 高 | 高 | **极低** | **最高** |
| Recovery | 高 | 高 | 中 | **高** |
| Security | 中 | 高 | 不可统一 | **可调** |
| Local-first | 高 | 中 | 高 | **高** |
| 与 Curis 四原则兼容 | 高 | 中 | **冲突（写死 Provider）** | **最高** |

---

## 4. 推荐：**Option D（以 A 为默认底座的混合模型）**

### 4.1 推荐理由（每条都有证据）

1. **Option C 必须否决**：它的致命缺陷不是技术，而是**它把"工作区形态"交给 Provider 决定** → 违反 Curis 硬约束"能力可替换不写死"。实证：Codex 的 worktree 是 **App 线程级**选择，本机 `codex --help` 中**不存在** `--worktree` 参数（L1 实测）→ 若 Curis 依赖 Provider-native，就**无法程序化**创建隔离工作区。Claude Code 的 worktree 则被锁在 `.claude/worktrees/` 且**只有 Claude Code 会用**。
2. **Option B 不作为默认**：隔离更强但**磁盘与合并代价高**，且 Curis v1 是**单机本地自用**——引入容器运行时（Docker/OrbStack）对"桌面自用"是额外依赖。业界也只有少数派采用。
3. **Option A 是默认底座**：本领域**压倒性主流**，且**已被三个开源项目把坑填平**（`hash_port` 端口唯一化 / symlink 或 copy-ignored 共享依赖目录 / `isExistingBranch` 分支复用策略）。
4. **Option D = A + 按需升级**：保留 A 的全部优点（零依赖、低磁盘、高 Provider 兼容），并在**同一套 Workspace Registry 下**允许"这个 Work 用容器"。
5. **与既有裁定不冲突**：Project **不升格**为组织层级（`Company→Department→Business→Workspace` 不变），Project 仍是 RD Workspace 内的 Project Context；本模型只是把"Project Context 的物理形态"定义清楚。

### 4.2 Option D 的 Workspace 生命周期（提案，待 CEO 裁定）

```
① ALLOCATE   Work 被创建 → 分配 Workspace
             决定：strategy（worktree | container）
                    base_ref（默认 Canonical Branch 当前 SHA）
                    branch_name（work/<work_id>-<slug>）
             → 生成 WorkspaceRecord（见 §4.3）

② READY      Workspace 就绪（依赖目录已链接/安装，端口已分配）
             ⚠️ 此步之前不得启动 Provider

③ RUN        Provider 会话在 Workspace 内执行
             全程保留：base SHA、会话 id、日志、工具事件

④ SETTLE     Work 结束（成功/失败/超时/用户中止）
             产出统一物：diff + 变更文件清单 + 测试结果 + 日志指针

⑤ REVIEW     Review 由"另一个 Provider 会话"或人执行（见 07 号文档）

⑥ INTEGRATE  通过 Gate → 变更进入 Canonical Branch
             ❌ 未通过 Gate → 不得进入 Canonical

⑦ RECLAIM    按策略回收：保留（有未收口成果）/ 销毁（失败或已收口）
             锁必须先释放；被复用的既有分支不得删除
```

### 4.3 WorkspaceRecord（提案字段，供 Runtime 设计参考 —— **非 Authority**）

| 字段 | 含义 | 证据来源 |
|---|---|---|
| `workspace_id` | Curis 内部唯一 id | — |
| `work_id` | 所属 Work | Curis 既有 |
| `project_id` | 所属 Project | Curis 既有 |
| `strategy` | `worktree` / `container` | AO `adapters/workspace/{gitworktree,router,scratch}` |
| `repo_path` | Canonical Project Root | AO `WorkspaceRepoPath` |
| `workspace_path` | 本次工作目录 | AO `WorkspacePath` |
| `branch_name` | 本次分支 | AO `Branch`；claude-squad `branchName` |
| `base_ref` / `base_sha` | 基线 | AO `DiffBaseRef` / `DiffBaseSHA`；claude-squad `baseCommitSHA` |
| `is_reused_branch` | 是否复用既有分支（**决定回收时是否可删**） | claude-squad `isExistingBranch` |
| `allocated_port` | 本工作区独占的 dev server 端口 | worktrunk `hash_port` |
| `lock_state` | 是否被锁定（运行中不可清理） | Claude Code `git worktree lock`；container-use `flock.go` |
| `provider_binding` | 本次由哪个 Provider 会话执行（**可中途替换**） | AO adapter 层 |
| `created_at` / `reclaimed_at` | 生命周期 | — |
| `reclaim_policy` | 保留 / 销毁 | Claude Code 清理规则 |

### 4.4 明确不采纳的三种"简化"

| 不采纳 | 理由 |
|---|---|
| ❌ 所有 Work 共享 Canonical Working Tree | 10/10 成熟实现均不做；I2 不变量 |
| ❌ 用"文件锁"防止写冲突 | Claude Code 官方明确"锁保护任务认领，不保护文件写入"；锁会把并行退化成串行 |
| ❌ 让 agent 直接 commit 到 Canonical Branch | 违反 I3；Copilot 直接在设计上禁止（只能推 `copilot/*`） |

---

## 5. 与 Curis v1 边界的对齐检查

| 检查项 | 结论 |
|---|---|
| 是否引入"物理多租户 / 对外售卖"？ | ❌ 无。Workspace 是**本机目录**。 |
| 是否引入新版费/订阅依赖？ | ❌ 无。Option D 默认零外部依赖。 |
| 是否把 Project 升格为组织层级？ | ❌ 无。Project 仍是 RD Workspace 内 Project Context。 |
| 是否引入"多人真实协作"？ | ❌ 无。单机单用户。 |
| 是否与"能力可替换不写死"一致？ | ✅ 一致，且**优于** Option C。 |
| 是否与"全自动任务流是核心"一致？ | ✅ 一致：Workspace 分配/回收、Settle 产物归一化、Gate 路由正是自动化缺口所在。 |

---

## 6. 遗留未知

| # | 未知 | 影响 | 建议下一步 |
|---|---|---|---|
| U1 | Curis v1 是否需要容器档位，还是**先只做 worktree** | 影响 Runtime 首版工作量 | 建议 v1 **只做 worktree**，把 `strategy` 字段留在契约里不实现 |
| U2 | Workspace 放在 Canonical Root 内部（`.curis/workspaces/`）还是外部（`~/Curis/workspaces/<project>/`） | 内部会污染 `git status`（需 `.gitignore`），外部则跨设备迁移更简单 | 建议**外部**，并以 `.worktreeinclude` 式约定共享依赖 |
| U3 | 依赖目录共享方式：symlink vs copy-ignored vs 不共享 | 直接影响并行 N 个 Work 的可行性 | 建议 v1 采 parallel-code 的 symlink 方案（最简单、可逆） |
| U4 | 一个 Work 是否允许多个 Workspace（多分支并行试错） | 影响数据模型 | 建议**允许**（`work_id` → `N workspace`） |
| U5 | Workspace 的自动回收时机（Work 结束后立即？次日？保留 N 天？） | 影响磁盘与"第二天继续" | 见 08 号文档 Long-running 部分 |
