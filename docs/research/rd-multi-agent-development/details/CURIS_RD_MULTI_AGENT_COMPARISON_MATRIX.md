# CURIS RD — MULTI-AGENT COMPARISON MATRIX

**Authority Class**: RESEARCH
**Status**: Draft → Review
**数据来源**：`evidence/E01_GITHUB_REPO_METADATA.tsv`（L1，`gh api`）+ 各项目源码/官方文档（L2/L3）。
**采集时间**：2026-09-19。

---

## A. 元数据与存活度（L1）

| 项目 | stars | forks | 最近推送 | 创建 | License | Arch | Lang | Open issues | 活跃判定 |
|---|---|---|---|---|---|---|---|---|---|
| `anomalyco/opencode` | 208,420 | — | 2026-09-18 | — | MIT | — | TS | — | 活跃（Provider） |
| `anthropics/claude-code` | 146,239 | 23,758 | 2026-09-18 | 2025-02-22 | 未声明 | — | TS | 12,522 | 活跃（Provider/编排原语） |
| `openai/codex` | 125,138 | 19,405 | 2026-09-18 | 2025-04-13 | Apache-2.0 | — | Rust | 17,766 | 活跃（Provider/编排原语） |
| `OpenHands/OpenHands` | 88,439 | 11,616 | 2026-09-18 | 2024-03-13 | MIT | — | TS | 821 | 活跃 |
| `stablyai/orca` | 71,857 | 4,696 | 2026-09-18 | 2026-03-17 | MIT | — | TS | **6,323** | 活跃（异常） |
| `FoundationAgents/MetaGPT` | 70,489 | 8,958 | **2026-01-21** | 2023-06-30 | MIT | — | Py | 132 | **低活跃** |
| `microsoft/autogen` | 61,049 | — | **2026-04-15** | — | CC-BY-4.0 | — | Py | — | 低活跃 |
| `crewAIInc/crewAI` | 58,738 | — | 2026-09-18 | — | MIT | — | Py | — | 活跃（非仓库编排） |
| `aaif-goose/goose` | 54,441 | — | 2026-09-18 | — | Apache-2.0 | — | Rust | — | 活跃（Provider） |
| `OpenBMB/ChatDev` | 34,339 | 4,299 | 2026-07-24 | 2023-08-28 | Apache-2.0 | — | Py | 73 | 中 |
| `BloopAI/vibe-kanban` | 28,124 | 3,014 | 2026-09-18 | 2025-06-14 | Apache-2.0 | — | Rust | 536 | 活跃 |
| `SWE-agent/SWE-agent` | 20,355 | 2,225 | 2026-09-14 | 2024-04-02 | MIT | — | Py | 114 | 活跃（研究） |
| `e2b-dev/E2B` | 13,874 | — | 2026-09-18 | — | Apache-2.0 | — | Py | — | 活跃（沙箱） |
| `Untrivial-ai/agent-orchestrator` | 12,172 | 1,677 | 2026-09-18 | 2026-02-13 | Apache-2.0 | — | Go | 742 | 活跃 |
| `humanlayer/humanlayer` | 11,579 | — | **2026-06-19** | — | NOASSERTION | — | TS | — | 中 |
| `smtg-ai/claude-squad` | 8,496 | 618 | 2026-08-20 | 2025-03-09 | **AGPL-3.0** | — | Go | 58 | 中 |
| `max-sixty/worktrunk` | 8,002 | 273 | 2026-09-18 | 2025-10-17 | NOASSERTION（仓库内 `MIT OR Apache-2.0`） | — | Rust | 40 | 活跃 |
| `SWE-agent/SWE-ReX` | 593 | — | 2026-09-14 | — | MIT | — | Py | — | 活跃（沙箱接口） |
| `dagger/container-use` | 4,047 | 205 | 2026-08-12 | 2025-05-23 | Apache-2.0 | — | Go | 62 | 中（自标 experimental） |
| `johannesjo/parallel-code` | 1,011 | 137 | 2026-09-18 | 2026-02-18 | MIT | — | TS | 54 | 活跃 |

> 说明：`—` 表示本轮未取该字段，不做推测。**Star 数不是质量证据**（Orca 的 6,323 open issues 即为反例）。

---

## B. 编排 / 隔离 / 交接 三轴对照（L2/L3）

| 项目 | 是否"多 Agent 对同一 repo" | 隔离原语 | Context 交接物 | 回主干通道 | Provider 可替换 |
|---|---|---|---|---|---|
| **Agent Orchestrator** | ✅ 是（worker × N + orchestrator） | **git worktree**（project）/ 独立目录（standalone）；container 仅回收 | 会话自身 + orchestrator 综合规划上下文；`handoff_artifact` | **GitHub PR**（mergeable/merged 派生） | ✅✅ **30+ agent + 30+ reviewer 适配器** |
| **Claude Code** | ✅ 是（agent teams / agent view / batch） | **git worktree**（`.claude/worktrees/`）+ 强制隔离校验；**agent teams 不隔离** | subagent summary / mailbox JSON / 跨会话消息 | 人手动 merge；`/batch` 每个 subagent 开 PR | ❌ workers 必须是 Claude 会话（外部工具须包装成 MCP） |
| **Codex** | ✅ 是（worktree 并行 + `multi_agent` stable） | **git worktree**（App 线程级；CLI 无 flag）+ Cloud 托管环境 | `apply`/patch/diff/commit；exec-plans 文档 | 人 squash&merge；**官方实践中 agent 常自合** | ⚠️ 中等：可作 MCP server 被编排；可消费 MCP；`--oss` 本地模型 |
| **Copilot cloud agent** | ⚠️ 每任务独立 agent（非"协作团队"） | **ephemeral GitHub Actions 容器** | **PR**（commit + description + session logs） | **PR + 人审批**（且 agent PR 上的 Actions 需人批准才跑） | ❌ 平台锁定 |
| **OpenHands** | ⚠️ 支持 delegate/subagent，但**共享 workspace** | 三档：进程内 / Docker / Remote API | 单一 EventLog（可 replay） | 走 GitHub 集成，外部收口 | ✅ 强（LiteLLM 多模型 + **ACP 接 Claude Code/Codex/Gemini CLI**） |
| **container-use** | ✅ 通用（任何 MCP agent） | **容器 + 每个 agent 一个分支** | 命令历史 + 日志 + 分支 | `git checkout <branch>` 人审后 merge | ✅✅ **完全不绑定 agent** |
| **claude-squad** | ✅ 是（多 session） | **git worktree + branch + tmux** | diff 视图；`s` push 分支 | 手动 merge（README 明确常见坑） | ✅ 任何终端 CLI |
| **worktrunk** | ❌ 不是编排器（是 worktree 管道） | **git worktree**（分支寻址） | 无（只管 worktree 生命周期 + hooks） | `wt merge`（squash+rebase+ff+cleanup） | ✅ 工具无关（hook 里可跑任何 agent） |
| **parallel-code** | ✅ 是（多任务 GUI） | **git worktree + 分支 + symlink 依赖** | GUI diff 审阅 + 分支 merge | GUI `Ctrl+Shift+M` merge to main | ✅ Claude/Codex/Gemini/Antigravity/Copilot CLI |
| **Orca** | ✅ 是（多 agent 平铺） | **git worktree per agent** | 单处追踪 + 移动端通知 | 比较 diff 后 merge 胜者 | ✅ Codex/ClaudeCode/OpenCode/Pi…"25+" |
| **vibe-kanban** | ✅ 是（看板调度） | git worktree（描述级） | 看板卡片 + 任务 | 人收口 | ✅ 任意 coding agent |
| **MetaGPT / ChatDev** | ❌ 角色扮演流水线 | 自建 workspace **目录** | 文档产物（PRD/设计/代码） | 无 | ❌ 内部角色固定 |
| **SWE-agent** | ❌ 单 agent | **SWE-ReX 沙箱执行** | patch | 无 | ⚠️ 模型可换 |

---

## C. 12 维能力覆盖矩阵

`✅ 内建一等能力` / `⚠️ 部分或需外部拼装` / `❌ 无`

| 能力维度 | AO | Claude Code | Codex | Copilot CA | OpenHands | container-use | claude-squad | worktrunk | parallel-code |
|---|---|---|---|---|---|---|---|---|---|
| **Project 长期实体** | ✅ | ⚠️（=仓库+文件） | ⚠️（=目录+AGENTS.md+docs） | ✅（仓库+PR/issue） | ⚠️（会话为中心） | ❌ | ❌ | ⚠️（=仓库） | ❌ |
| **Agent 长期身份** | ✅ orchestrator vs worker | ⚠️（session/teammate） | ⚠️（thread/session） | ⚠️（custom agent） | ⚠️（agent 无状态） | ❌ | ❌ | ❌ | ❌ |
| **Task 拆解** | ✅ orchestrator 拆 | ✅ lead 拆 + 自领 | ⚠️（人拆 / subagent） | ⚠️（issue 即任务） | ⚠️（delegate） | ❌ | ❌ | ❌ | ⚠️（人建） |
| **任务依赖** | ⚠️（看板派生） | ✅ **`blockedBy` + 自动解锁** | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ❌ |
| **并行执行** | ✅ | ✅ | ✅ | ✅（多任务并行） | ✅ | ✅ | ✅ | ✅（worktree 层） | ✅ |
| **重试** | ⚠️ | ⚠️ | ⚠️ | ⚠️（新环境重跑） | ✅（事件流重放） | ✅（丢弃环境） | ⚠️（`r` resume） | ❌ | ⚠️ |
| **Review（另一 agent）** | ✅✅ 30+ reviewer 适配器 | ⚠️（交叉校验 workflow） | ✅ `codex review` | ❌ 人 review | ⚠️（安全审查≠评审） | ❌ 人 checkout | ❌ 人看 diff | ❌ | ⚠️ 人看 diff |
| **Merge 权威** | 人（PR approved） | 人 | 人 / 官方实践中 agent 自合 | 人 | 人/外部 | 人 | 人 | `wt merge` | 人（GUI 按钮） |
| **Git 隔离真实性** | ✅ worktree | ✅ worktree + **强制校验** | ✅ worktree | ✅ 容器+分支前缀限制 | ⚠️ 容器 | ✅ **容器+分支** | ✅ worktree | ✅ worktree | ✅ worktree |
| **失败状态枚举** | ✅✅ **15 态 + no_signal** | ⚠️（滞后/无信号不明） | ⚠️ | ⚠️ | ✅ 卡死检测 | ⚠️ | ❌ | ❌ | ⚠️ |
| **跨重启续跑** | ✅✅（detached host + checkpoint） | ⚠️（`/resume` 不恢复 teammate） | ✅ `resume`/`fork` | ❌（环境即焚） | ✅（replay） | ⚠️ | ⚠️（storage.json） | ❌ | ❌ |
| **Provider 可替换** | ✅✅ | ❌（须 MCP 包装） | ⚠️ | ❌ | ✅ | ✅✅ | ✅ | ✅ | ✅ |

---

## D. 隔离原语的工程代价对照

| 原语 | 磁盘成本 | 创建耗时 | 依赖安装 | git 复杂度 | 合并复杂度 | 环境一致性 | 适合场景 |
|---|---|---|---|---|---|---|---|
| **同一 working tree（不推荐）** | 0 | 0 | 0 | 无 | 无（但会互相覆盖） | 完美 | **仅限读-密集/只读调研** |
| **git worktree** | 低（共享 object store） | 秒级 | **需处理**（symlink / copy-ignored / 共享缓存） | **中**（worktree 生命周期、锁定、清理、分支复用） | 中（分支 merge/rebase） | 高（同一机器同一工具链） | **默认选择**（本领域主流） |
| **独立 clone** | 高（整份历史） | 慢 | 需重装或 symlink | 低（各是独立仓库） | 高（需 cross-repo 推送/拉取） | 中 | 需要完全独立 remote / 隔离网络 |
| **容器** | 中-高（镜像层） | 中（镜像缓存后较快） | 镜像内预置 | 低（内部分支） | 中 | **完美**（可复现） | 需要系统级依赖、危险实验、多语言环境 |
| **VM / 托管沙箱** | 云侧 | 慢 | 云侧 setup steps | 低 | 中 | 完美 | 长任务离线执行、跨机器 |

> 注：`git worktree` 的真实工程坑已被三个项目用代码解决——`worktrunk` 的 `hash_port`（端口唯一化）与 `wt step copy-ignored`（共享被忽略目录）、`parallel-code` 的 **symlink gitignored 目录**、`claude-squad` 的 `isExistingBranch`（分支复用不删）。**这三条对本领域是"已解决问题"，Curis 不需要重新发明，但必须知道自己会撞上。**

---

## E. "可直接作为 Curis 底层 Orchestrator" 候选评估

评估尺度：①是否真操作 repo ②是否真多 agent ③是否真并行 ④是否有长期项目状态 ⑤是否 Provider 无关 ⑥是否 local-first ⑦License 是否可商用且非传染 ⑧是否活跃 ⑨是否可被嵌入（有 API/daemon 而非只有 GUI）。

| 候选 | ① | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | 结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Untrivial-ai/agent-orchestrator** | ✅ | ✅ | ✅ | ✅ | ✅✅ | ✅（本地 daemon） | ✅ Apache-2.0 | ✅ | ✅（本地 HTTP daemon + CLI） | **唯一同时满足九项的候选**——但它是"工程师管理台"形态，需要剥离 GitHub/云/移动/计费外围 |
| **OpenHands** | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ MIT | ✅ | ✅（SDK/API） | 可作**执行器与 SDK 层**；多 agent 共享 workspace，不适合"并行改同一 repo" |
| **container-use** | ✅ | ❌ | ✅ | ❌ | ✅✅ | ✅ | ✅ Apache-2.0 | ⚠️（release 停滞） | ✅（MCP server） | 可作**隔离层 MCP 工具**，不能作编排器 |
| **worktrunk** | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ⚠️ NOASSERTION | ✅ | ⚠️（CLI） | 可作**worktree 生命周期层**（或仅作设计参照） |
| **claude-squad** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ **AGPL-3.0** | ⚠️ | ⚠️（TUI） | **AGPL 是采用红线**；仅作设计参照 |
| **parallel-code** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ MIT | ✅ | ❌（GUI 为主） | 设计参照（symlink 依赖方案） |
| **Orca** | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ MIT | 数据异常 | ❌（GUI/移动） | 形态参照，不作复用 |
| **vibe-kanban** | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ Apache-2.0 | ✅ | ⚠️ | 看板形态参照 |
| **Codex CLI** | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ✅ Apache-2.0 | ✅ | ✅ | **是 Worker/Provider，不是 Orchestrator** |
| **Claude Code** | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | 未声明 | ✅ | ⚠️ | **是 Provider，且自带封闭编排层** |

---

## F. 结论性对比（一句话版）

| 问题 | 对比结论 |
|---|---|
| 谁解决了"多个 agent 不互相覆盖"？ | **所有人**：worktree（主流）或容器（少数）。这是已解决问题。 |
| 谁解决了"agent 之间怎么交接"？ | **没有人真正解决**。最好的是 Claude Code 的 mailbox + Codex 的 diff/patch + AO 的 orchestrator 综合上下文；**跨 Provider 的标准交接协议目前不存在**。 |
| 谁解决了"冲突提前检测"？ | **没有人**。全部靠隔离规避 + 事后 merge 冲突。Claude Code 甚至明确说"锁保护认领不保护写入"。 |
| 谁解决了"长期项目上下文"？ | **Codex 官方实践（仓库即记忆）最完整**；AO 的 orchestrator 会话次之；Claude Code 靠 CLAUDE.md。 |
| 谁解决了"失败可恢复"？ | **AO（durable facts + no_signal %2B detached host）** 与 **Codex（resume/fork + 自动 compact）** 最好。 |
| 谁证明了 Provider 可替换？ | **Agent Orchestrator（30+ 适配器）** 与 **container-use（零绑定）**。 |
| 谁证明了"人不必逐行审"？ | **Codex 官方工程文章**（agent-to-agent 审查 + 最小阻塞门禁）。**但这与 Curis v1 单机自用的可信度要求需要 CEO 裁定。** |
