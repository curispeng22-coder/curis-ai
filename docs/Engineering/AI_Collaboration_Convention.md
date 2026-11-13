# Curis AI Collaboration Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Parent: `docs/Engineering/Curis_Engineering_Convention.md`

---

## 1. Equal Agent Rule

Codex、WorkBuddy、ChatGPT、Claude、Gemini 及其他 AI Agent 遵守同一工程规范。
所有 Agent 只是 Contributor。Agent 名称不改变事实权威、目录、命名、验收门槛
或 Git 规则，也不能成为目录、文件或资产包命名依据。

禁止创建：

- `<Agent>_Rules.md`
- `<Model>_Current.md`
- 工具专属 Current
- 与本规范内容重复的平行协作规范

工具特有操作说明可以存在，但必须只描述工具使用，并引用本规范，不能覆盖本规范。

## 2. Required Reading

每个 Agent 开始任务前按最小上下文读取：

1. `AGENT.md` 的规范入口。
2. `docs/Engineering/Curis_Engineering_Convention.md`。
3. 总规范路由表命中的专项 Convention。
4. `AGENTS.md` 要求的当前事实和相关 Frozen 文档。
5. 授权实施时再读取 Issue、目标文件和对应 Review。

不要求每次读取全部七份 Engineering 规范，也不得默认读取全部 History、
Deprecated 或 Archive。

## 3. Task Packet

每项工作必须有一个可交接的 Task Packet，至少包含：

- Objective
- Current baseline：branch + full SHA
- `object-id`
- Current source path
- Revision ID
- Allowed files
- Non-goals
- Acceptance criteria
- Required checks
- Owner / active Agent
- Expected Review or handoff

Agent 接手时默认先搜索并维护现有 Current。只有确认对应 Current 或可复用资产确实
不存在时，才允许在预定官方路径新建一个候选。缺少唯一 Current 或允许范围时，
Agent 只能分析并报告阻塞，不能自行创建替代事实。

## 4. Ownership And Concurrent Work

- 同一时刻一个治理对象只有一个 active owner。
- 其他 Agent 可以只读审查，但不能并行修改同一 Current。
- 并行任务必须按对象或文件范围互斥拆分。
- 发现重叠时，后开始的 Agent 停止写入并请求统一 owner。
- Agent 不得覆盖、整理或提交其他 Agent 的未确认变更。

## 5. Modification Rules

- 修改必须从 Current 路径开始。
- 先搜索现有实现、文档和资产，再决定是否新建。
- 已存在 Current 时，不得创建“暂存 Current”、平行规范、Agent 版本、模型版本、
  `new`、`final` 或 `v2` 资产来绕过冲突。
- 需要新修订时只产生一个 Review 候选。
- 未经人工批准的 Revision 不能替代 Current；任何时刻只有一个 Approved Current。
- 设计效果图、设计规范、Prototype 和说明按 Asset Convention 完成影响检查和同步。
- 不得把 Mock、实验、局部测试或模型输出描述为正式完成。

## 6. Handoff

交接必须包含：

- 完成内容
- 未完成内容和明确 blocker
- 修改文件
- Current baseline 与工作分支 SHA
- Revision ID
- 测试/校验命令和结果
- 资产、数据库、API 或安全影响
- 下一 owner 和下一动作
- 工作区是否干净

“已派发”不是完成。任务只有在接收方获得上述事实，或 Review 已明确关闭时才完成。

## 7. Multi-Agent Relay Example

```text
Codex 读取 ceo-office-overview 的 Approved Current
→ Codex 在 2026-07-31-002 下修改设计规范并生成对应效果图
→ Codex 完成影响检查，确认 Prototype 和说明是否需要同步
→ Codex 暂时不可用
→ WorkBuddy 读取同一个 Approved Current、Revision ID 和 Git diff
→ WorkBuddy 继续基于 Current 完成受影响的规范、效果图、Prototype 或说明
→ 所有变更保持在同一个 2026-07-31-002 Review 候选中
→ Review PASS
→ 人工批准
→ 2026-07-31-002 成为唯一 Approved Current
→ 原 Current 通过 Git 历史或必要的 Revision/Milestone 快照追溯
```

WorkBuddy 不得另建 `WorkBuddy_Design_Convention.md`、`workbuddy-version/` 或一份
WorkBuddy 设计规范。它是接力 Contributor，不是新事实源。

## 8. Context And Prompt Safety

- Prompt 不得包含凭据、密钥、隐私数据或隐藏推理。
- Prompt 资产使用统一命名并记录输入/输出契约。
- Agent 只读取任务所需上下文，不复制整个仓库知识到新文档。
- 可复用事实写入 Current 或 Change Log，不依赖某个 Agent 的对话记忆。

## 9. Completion

Agent 宣称完成前必须确认：

- 范围未扩张
- 唯一 Current 未分叉
- 命名和 Revision ID 合规
- 引用有效
- 所需 Review 和验证已通过
- Current 提升已获得人工批准
- 未提交用户无关变更
- 明确报告剩余风险
