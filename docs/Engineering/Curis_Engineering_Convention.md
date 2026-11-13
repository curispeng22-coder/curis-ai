# Curis Engineering Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

---

## 1. Purpose

本规范统一 Curis 的开发过程，使 Codex、WorkBuddy、ChatGPT、Claude、Gemini
及其他 AI Agent 能在同一事实、同一命名和同一资产链路上连续工作。

本规范只约束工程协作，不定义 Curis 产品功能，不实现 Runtime，不替代产品、
架构、设计或开发领域的 Frozen 文档。

## 2. Authority And Scope

工程规范唯一入口是：

`docs/Engineering/Curis_Engineering_Convention.md`

本目录其余文档是该规范的专项章节，不是平行规范：

| Task Type | Required Sub-convention |
| --- | --- |
| 新建、重命名文档或资产 | `Naming_Convention.md` |
| 新建目录、移动或归档 | `Folder_Convention.md` |
| 图片、设计规范、Prototype、Prompt、证据 | `Asset_Convention.md`；涉及命名时再读 `Naming_Convention.md` |
| 多 Agent 接力、并行协作、交接 | `AI_Collaboration_Convention.md` |
| 审查、批准、Current 提升 | `Review_Convention.md` |
| 分支、Commit、合并或发布 | `Git_Convention.md` |

如专项章节与总规范冲突，以本文件为准。专项章节之间发生冲突时，停止修改并在
本文件中统一规则，不得创建第三份解释文档。

Agent 不需要每次读取全部七份规范。工程任务只读取 `AGENT.md`、本总规范和路由表
命中的专项规范；项目事实、Issue 和目标文件仍按 `AGENTS.md` 的最小上下文规则读取。

## 3. Core Rules

1. 同一个业务对象只能有一个当前官方资产包，即一个 `Approved Current`。
2. 任何时刻只能有一个 `Approved Current`；未经人工批准的 Revision 不能替代它。
3. Agent 接手任务时默认先查找并维护现有 Current，所有修改必须基于 Current。
4. 已存在 Current 时，禁止按 Agent 名称、模型名称或 `new`、`latest`、`final`、
   `v2` 等方式创建平行资产。
5. 只有确认不存在对应 Current 或可复用资产时，才允许在预定官方路径新建一个候选。
6. Codex、WorkBuddy、ChatGPT、Claude、Gemini 及其他 Agent 只是 Contributor，
   不能成为目录、文件、资产包或规范的命名依据。
7. 设计效果图、设计规范、Prototype 和相关说明属于同一资产包；其中一项发生已确认
   变更时，必须检查并同步更新其他受影响资产。
8. Current 使用稳定路径；Revision 由 Git 和统一 Revision ID 追溯，不通过复制
   完整资产包表达普通修改。
9. 被替代内容通过 Git 或批准的 Revision/Milestone 快照追溯，不与 Current 竞争权威。
10. Milestone 是必要的阶段证据，不自动成为 Current。
11. 修改前检查现有对象、引用和负责人；修改后更新受影响引用、Review 和必要记录。
12. 不能确定唯一 Current 时停止新建，先完成事实归一。

## 4. Governed Object

治理对象是需要持续维护且可能产生多个修订的业务或工程实体，例如：

- 一个产品或工程规范
- 一个页面、组件或流程
- 一套设计稿或效果图
- 一个 Prototype
- 一个 Prompt
- 一个 Issue、Review 或 Milestone
- 一组具有共同用途的交付资产

每个对象必须有稳定的 `object-id`。`object-id` 使用小写英文和连字符，例如
`ceo-office-overview`。同一对象的文档、图片、Prototype、Prompt、说明和 Review
组成一个资产包，必须复用同一个 `object-id`。

## 5. Status And Authority

文档状态统一使用：

- `Status: Draft`
- `Status: Review`
- `Status: Frozen`
- `Status: Deprecated`

资产角色统一使用：

- `Draft`
- `Review`
- `Approved Current`
- `History`
- `Milestone`
- `Protected`
- `Delete Candidate`
- `Deleted`

`Status` 是文档治理状态；资产角色是生命周期和权威角色，两者不得混用。
Markdown 的 `Approved Current` 必须是 `Status: Frozen`。非 Markdown 资产必须由
Frozen 入口或已获人工批准的 Review 明确登记为 `Approved Current`。

## 6. Current, History And Milestone

### Current

- `Current` 在本规范中是 `Approved Current` 的简称。
- 一个业务对象只能有一个 Current 资产包。
- Current 必须有稳定路径和明确权威来源。
- Review 候选不能覆盖 Current，直到 Review `PASS` 且获得人工批准。
- Current 文件名不得包含 Agent、模型、`new`、`latest`、`final` 或 Revision ID。

### History

- 普通修改默认由 Git 历史追溯，不复制完整资产包。
- 只有人工批准的重要设计节点或需要独立保留的 Revision 才创建必要快照。
- 独立历史文档必须标记 `Status: Deprecated` 或进入 `docs/99_Archive/`。
- History 只读；恢复历史内容时必须从 Current 发起新 Revision。

### Milestone

- 只保存人工批准、重要设计节点、发布或验收所需的必要快照。
- Milestone 使用统一 Revision ID。
- Milestone 记录当时事实，不持续同步为 Current。

## 7. Revision Rule

- Revision ID 唯一格式为 `YYYY-MM-DD-NNN`。
- `NNN` 使用三位数，从 `001` 开始，在仓库内按当天递增；日期变化后重新从
  `001` 开始。
- 同一次修改涉及的文档、图片、Prototype、Prompt、说明和 Review 共用同一个
  Revision ID。
- Current 保持稳定文件名；获批后在文档元数据或 Current 登记记录中更新
  `Revision ID`。
- 小修改仅依赖 Git 历史，不强制创建 History 或完整资产包副本。
- 只有需要独立保存的 History/Milestone 快照才在文件名中加入 Revision ID。
- 禁止使用 `rNN`、`v2`、`revA`、`final-final` 或 Agent 名称表达 Revision。

## 8. Change Flow

```text
Locate Current
→ Confirm scope and ownership
→ Modify Current in the task branch, or create one candidate only when Current is absent
→ Check and update affected assets and references under one Revision ID
→ Review
→ Human approval
→ Promote the approved Revision as the only Current
→ Preserve prior state through Git or an approved snapshot
```

任何步骤都不得通过复制文件绕过 Review。若变更不需要新资产，不创建空目录、
占位文档、完整资产包副本或“以后使用”的模板。

## 9. Lightweight Execution

- 普通修改直接在任务分支维护 Current，由 Git 保存差异。
- 不要求每次修改创建 History、Milestone、效果图或完整资产包副本。
- 只在资产确实受影响时同步更新；必须完成影响检查并在 Review 记录结论。
- 只有人工批准、重要设计节点或正式 Milestone 才保存必要快照。
- Agent 不默认读取全部七份规范，只读取路由命中的专项规范。

## 10. Compliance

每项工作至少检查：

- 是否定位并基于唯一 Approved Current
- 是否复用既有 `object-id`
- 是否产生平行规范或重复资产
- 命名、目录和 Revision ID 是否合规
- 引用是否有效
- 设计资产包是否完成影响检查和必要同步
- Review 是否 `PASS`，需要提升时是否获得人工批准
- Git 变更是否只包含授权范围

不满足上述条件的交付状态为 `BLOCK`，不能宣称完成。

## 11. References

- `AGENT.md`
- `AGENTS.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/00_Context/DOCUMENT_STATUS_RULES.md`
- `docs/04_Development/Curis_Development_Guide.md`
- `docs/08_Change_Log/CHANGE_LOG.md`
