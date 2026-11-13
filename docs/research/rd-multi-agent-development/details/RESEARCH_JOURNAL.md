# CURIS RD — MULTI-AGENT DEVELOPMENT ORCHESTRATION 研究日志

**Authority Class**: RESEARCH
**Status**: Review（本轮已收尾：`RD MULTI-AGENT DEVELOPMENT ORCHESTRATION RESEARCH COMPLETE — READY FOR CEO REVIEW`）
**Scope**: 只读研究 + 独立实验；不修改 Curis Authority / Runtime / Code / RD HTML / Figma / Frontend / Backend；不 commit、不 push。
**研究目录**: `docs/research/rd-multi-agent-development/`
**实验目录（git 未跟踪）**: `RD_MULTI_AGENT_RESEARCH_LAB/`

---

## 0. 本轮研究的定位

Curis RD 已收敛为极简产品形态（Project Operating Header + Employee Work Surface + Employee Conversation + Result/Utility + Decision）。本轮不画 UI、不改导航，只回答一个更底层的 P0 问题：

> 多个 Coding Agent 长期协同开发同一个项目，成熟系统到底是怎么组织的？Curis RD 应该继承什么、复用什么、自己拥有什么、绝不重造什么？

研究纪律：**不重复造轮子 / GitHub Source First / 先研究成熟实现，再翻译成 Curis 产品与 Runtime 需求**。

---

## 1. 方法与时间线

| 阶段 | 动作 | 工具 | 产出 |
|---|---|---|---|
| P0 准备 | 建立研究目录、实验目录；确认 `gh` CLI 已登录（`curispeng22-coder`） | Bash | 目录骨架 |
| P1 广度检索 | 8 组 GitHub 关键词检索（`gh search repos --sort stars`） | gh CLI | 候选池 60+ |
| P2 元数据核验 | 对 34 个候选逐个 `gh api repos/...` 取 stars/forks/pushed_at/license/archived/open_issues | gh API | `evidence/E01` |
| P3 源码级 Deep Dive | shallow clone 5 个编排器/隔离工具；读 architecture/源码/adapters | git + Read | `evidence/E03–E07` |
| P4 官方能力核验 | Claude Code 官方文档（agents / worktrees / agent-teams）；Codex 官方工程文章；Copilot cloud agent 官方文档 | WebFetch | `evidence/*` 引用 |
| P5 本机实测 | 本机 Codex CLI 0.144.6 能力探测（子命令 / feature flags / config） | codex CLI | `evidence/E02` |
| P6 建模 | Project Working Space 候选、Context 四分层、Capability Decomposition | 分析 | 本目录 04–10 号文档 |

### 检索式清单（可复现）

```
gh search repos "coding agent orchestrator"     --sort stars --limit 15
gh search repos "parallel coding agents"        --sort stars --limit 15
gh search repos "git worktree ai agent"         --sort stars --limit 15
gh search repos "multi-agent software engineering" --sort stars --limit 15
gh search repos "ai software factory agent"     --sort stars --limit 12
gh search repos "agent teams claude code"       --sort stars --limit 12
gh search repos "orchestrator agent sandbox container" --sort stars --limit 12
```

---

## 2. 执行记录

### 2.1 目录与实验区

- `docs/research/rd-multi-agent-development/{evidence}` 建立成功。
- `RD_MULTI_AGENT_RESEARCH_LAB/{repos,experiments}` 建立成功；**未写入 Curis 正式仓库任何受控目录**（`git status` 中该目录与 research 文档不在既有变更集内）。
- 说明：workspace 根目录 `git status` 中此前已存在大量 `backend/app/**` 修改（历史遗留，非本轮产生）；本轮**未触碰**。

### 2.2 浅克隆清单（L2 证据源）

见 `evidence/E07_CLONE_MANIFEST.txt`：

| 目录 | 体积 | HEAD | 最近提交 |
|---|---|---|---|
| `agent-orchestrator` | 190M | shallow | 2026-09-18 |
| `claude-squad` | 2.7M | shallow | 2026-08-20 |
| `container-use` | 4.7M | shallow | 2026-08-12 |
| `worktrunk` | 23M | shallow | 2026-09-18 |
| `parallel-code` | 48M | shallow | 2026-09-18 |

克隆策略：`git clone --depth 1`（不取全历史，避免无关体积）；**未运行任何 agent、未安装依赖、未执行 demo、未创建临时测试 Repo**——见 §4 的取舍说明。

### 2.3 本机 Codex CLI 实测（L1）

- `which codex` → `/Users/yy/.local/bin/codex`；`codex --version` → `codex-cli 0.144.6`。
- 子命令实测：`exec / review / login / mcp / plugin / mcp-server / app-server / remote-control / app / sandbox / apply / resume / archive / delete / unarchive / fork / cloud[实验] / exec-server[实验] / features / doctor`。
- `codex features list` 关键项：`multi_agent`=**stable/true**、`multi_agent_v2`=under development、`enable_fanout`=under development、`computer_use`=stable/true、`browser_use`=stable/true、`hooks`=stable/true、`plugins`=stable/true、`memories`=experimental/true、`guardian_approval`=stable/true。
- `codex cloud` 子命令：`exec / status / list / apply / diff`。
- 本机 `~/.codex/config.toml`：`sandbox="danger-full-access"`、`model="gpt-6-astra"`、已配置 MCP servers（stitch / node_repl / openaiDeveloperDocs）、本地 marketplaces、`computer-use` MCP（disabled）。
- 结论：**本机已具备一个可编程、可 resume/fork、可并行的成熟 coding agent 运行时**；Claude Code CLI 本机未安装（`claude: NOT INSTALLED`），其能力只能以官方文档核验（L3）。

---

## 3. 研究过程中的纠正与止损

| # | 现象 | 处理 |
|---|---|---|
| C1 | 第三方博客普遍夸大：某文声称 `codex --worktree` 是 CLI flag | **证伪**：本机 `codex --help` 全量 options 中**没有** `--worktree`；worktree 是 **Codex App** 的线程级选择，不是 CLI flag。L1 覆盖 L5。 |
| C2 | 搜索引擎给出的 star 数与事实不符（如把 `ComposioHQ/agent-orchestrator` 作为主体） | **纠正**：真实仓库为 `Untrivial-ai/agent-orchestrator`（12.1k★）；用 `gh api` 逐个核验取代搜索摘要。 |
| C3 | 第三方 wiki（`claude-wiki.com`）披露的 Agent Teams 内部细节（13 个 TeammateTool 操作、feature flag 名）听起来精确 | **降级为 L5/推断**：只用 Anthropic 官方文档能证实的部分；内部实现细节不作为架构结论依据。 |
| C4 | `FoundationAgents/MetaGPT` 最近提交停在 2026-01-21（约 8 个月） | **如实标注**：高星但近期活跃度低，不作为"可直接复用 Orchestrator"候选。 |
| C5 | 一条 `gh api` 批量命令被 SIGTERM（exit 137，超时） | 拆分重跑；未丢证据（元数据已另批取全）。 |
| C6 | 用户原文列出 `AutoGen / Microsoft Agent Framework`、`OpenAI Codex multi-agent` 等方向 | 核验后**降权**：`microsoft/autogen` 最近提交 2026-04-15 且 license 为 CC-BY-4.0（文档类），更适合作为"多智能体会话框架"而非"仓库协作编排器"；Codex 侧以本机 CLI + 官方工程文章为准。 |

---

## 4. 明确未做 / 已知限制（必须如实保留）

1. **未做"让多个测试 Agent 在临时 Repo 上真实跑一轮"的端到端实验**。原因：本轮用户划定的是"研究 → 翻译成 Curis 产品与 Runtime 需求"，而 L1 端到端跑多 Agent 需要付费凭据 + 长时占用 + 真实写入，属于**边界 §23 允许但非必需**。本报告因此对"编排器真机吞吐/冲突率"类结论**一律标注为未实测**，只引用他人公开的实测数字并标注来源等级。
2. **Claude Code 无法在本机实测**（CLI 未安装）→ 全部 Claude Code 结论为 **L3 官方文档**。
3. **stablyai/orca、BloopAI/vibe-kanban 只做到 README + 元数据级（L3/L4）**，未做源码深挖；报告中已按此降级标注。
4. **未验证任何项目的 License 兼容性结论**（只在矩阵里列出 license 事实）。`max-sixty/worktrunk` 的 GitHub license 字段为 `NOASSERTION`，其仓库内声明为 `MIT OR Apache-2.0`（见 `plugins/worktrunk/skills/worktrunk/SKILL.md` frontmatter）——若未来采用需法务确认。
5. **付费/凭据类未执行**：Devin、Google Jules、Codex Cloud、Copilot cloud agent 均为闭源或需订阅，仅以官方文档（L3/L4）评估。

---

## 5. 关键发现速览（详细见 01 号 Study）

1. 这个领域已经**收敛出一个事实标准**：`Canonical Repository → 每 Work 一个隔离工作区（绝大多数是 git worktree）→ 每个 agent 一个进程/会话 → PR 作为唯一回主干的通道 → 人（或另一个 agent）Review → Merge`。
2. `git worktree` 是当前**压倒性主流**的隔离原语（Orca / Agent Orchestrator / claude-squad / Claude Code / worktrunk / parallel-code / vibe-kanban 全部采用）；**容器隔离是少数派但不是异端**（container-use / Copilot cloud agent / OpenHands / SWE-ReX）。
3. **没有任何一个成熟系统让多个 Coding Agent 共享同一个 Working Tree**。共享的是 repo 与 `.git` object store，不是工作目录。
4. **Provider 可替换性已被真实工程解决**：`Untrivial-ai/agent-orchestrator` 的 `adapters/agent/` 下平铺了 30+ 个 agent 适配器（claudecode / codex / aider / cursor / cline / devin / copilot / goose / opencode / qwen …），且 `adapters/reviewer/` 用同一套适配器做"另一个 agent 来 review"。**这是"不要锁死 Provider"的可直接读的参考实现。**
5. **两个官方运行时已经把"多 agent 协作"做成产品原语**：Codex（`multi_agent` 已 stable、`cloud` 任务带 diff/apply、App 内 Local vs Worktree）与 Claude Code（worktrees + subagents + agent teams + agent view + cross-session messaging + `/batch`）。
6. 因此 Curis 的正确答案**不是**"自己做一个多智能体编码框架"，而是：**拥有组织语义与问责（Employee / Responsibility / Work / Decision Gate / 长期运营状态），把执行、隔离、并行、评审原语交给 Provider 与 Git**。

---

## 6. 下一 Gate

本目录 11 份文档 + `evidence/` 齐备后，状态置为：

`RD MULTI-AGENT DEVELOPMENT ORCHESTRATION RESEARCH COMPLETE — READY FOR CEO REVIEW`

等待 CEO 裁定后再进入 RD 定向视觉修订（本轮禁止改 RD HTML）。
