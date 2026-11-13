# Curis Git Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Parent: `docs/Engineering/Curis_Engineering_Convention.md`

---

## 1. Baseline

- 每项任务记录 branch 和完整 commit SHA。
- 开始修改前确认当前分支、HEAD、工作区和未追踪文件。
- 不把分支名、文件更新时间或 Agent 对话当作基线证据。
- 不覆盖已有用户或其他 Agent 变更。
- Agent 接手时先从 Git 和权威入口定位 Approved Current，再开始修改。

## 2. Branches

使用现有最小分支类型：

- `feat/<scope>`
- `fix/<scope>`
- `docs/<scope>`
- `integration/<candidate>`
- 工作区明确要求的 Agent 前缀

`<scope>` 使用小写 kebab-case。一个分支只承载一个批准目标。不得用 Agent 或模型名
代替目标，也不得为每个小文件创建分支。

## 3. Commits

Commit message 使用：

```text
<type>: <imperative summary>
```

允许的常用 type：

- `docs`
- `feat`
- `fix`
- `test`
- `refactor`
- `chore`

一次 commit 只包含一个可审查意图。受影响的 Current 内容、必要同步资产、引用和
治理记录应在同一原子提交中；未受影响资产不要求复制或重导出。无关整理、生成输出
和个人文件不得混入。

## 4. Safe Operations

- 文件移动使用 Git 可追溯移动，并先检查引用。
- 合并前检查 ancestry、冲突、数据库、API、前端和资产影响。
- 能 fast-forward 时优先 fast-forward。
- 未经明确授权不得 merge、push、reset、force push、删分支或删资产。
- 不使用破坏性操作清理不属于当前任务的工作区。

## 5. Current Promotion

一个候选提升为 Approved Current 前必须：

1. 基于已声明 Current。
2. 使用统一的 `YYYY-MM-DD-NNN` Revision ID。
3. Review 为 `PASS` 且获得人工批准。
4. 确认只有一个候选被提升。
5. 完成设计资产包影响检查并同步受影响的规范、效果图、Prototype 和说明。
6. 明确旧 Current 由 Git 追溯，或在必要时保存 Revision/Milestone 快照。
7. 执行任务要求的验证。

Git 提交不能自动赋予文档或资产 Current 身份；Current 身份来自通过 Review 的
权威入口、人工批准和状态。

## 6. Pre-Commit Checks

至少执行：

- 检查当前分支和工作区
- 检查 staged 与 unstaged diff
- 检查变更文件都在授权范围
- `git diff --check`
- 执行任务要求的最小验证
- 检查凭据、生成输出和重复资产

提交后确认 HEAD、commit 文件列表和工作区状态。Push 必须单独获得授权。
