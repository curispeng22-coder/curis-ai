# Curis Asset Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Parent: `docs/Engineering/Curis_Engineering_Convention.md`

---

## 1. Asset Definition

Asset 包括图片、SVG、设计导出、Prototype、Prompt、演示文件、交付包、验收证据和
其他非业务代码成果。依赖、缓存和可再生成构建输出不是 Current 资产。

同一个业务对象的设计效果图、设计规范、Prototype 和相关说明组成一个资产包，
不是四个互不相关的 Current。一个资产包任何时刻只能有一个 `Approved Current`。

每个资产必须具备：

- `object-id`
- Purpose
- Source 或生成方式
- Owner Issue / Review
- Asset role
- Revision ID
- Current 路径或 Archive 路径

## 2. Lifecycle

```text
Draft
→ Review
→ Human Approval
→ Approved Current
→ History
→ Archived / Milestone
→ Delete Candidate
→ Deleted
```

无法确认安全处置的资产从任意非 Current 阶段转为 `Protected`，等待人工确认。

- `Draft`：工作中，不具权威。
- `Review`：唯一候选，等待审查。
- `Human Approval`：授权人员明确批准；AI Agent 的 PASS 建议不能替代该批准。
- `Approved Current`：一个对象唯一有效的官方资产包。
- `History`：已被新 Current 替代，由 Git 或批准的快照追溯。
- `Archived`：有追溯价值，只读保存。
- `Milestone`：重要节点的只读快照，不持续同步为 Current。
- `Protected`：存在依赖或无法确认安全处置，不移动、不删除。
- `Delete Candidate`：无当前用途，等待逐项引用和价值审计。
- `Deleted`：经批准移除，必须保留 Git 和治理记录。

任何资产不得从 `Approved Current` 直接删除。

## 3. One Current Rule

- 同一业务对象只能有一个 `Approved Current` 资产包。
- Agent 接手时先查找并维护 Current；仅确认对应资产不存在时才允许新建候选。
- 已存在 Current 时，禁止以 Agent、模型、`new`、`final` 或 `v2` 名义创建平行资产。
- 新 Revision 只有在 Review `PASS` 且获得人工批准后才能原子替换 Current。
- 旧 Current 由 Git 追溯，只有重要节点才保存 History/Milestone 快照。
- 不确定哪一个是 Current 时，候选保持 Review/Protected，先完成事实确认。

## 4. Source And Derived Assets

- 可编辑源文件是 Source，导出的 PNG/JPG/SVG/HTML 是 Derived。
- Derived 必须能追溯到 Source、Revision ID 和生成方式。
- Source 与 Derived 使用相同 `object-id` 和 Revision ID。
- 仅保留 Derived 而丢失不可再生成 Source 时，必须标记风险。
- 可稳定再生成且无证据价值的输出不得长期跟踪。

## 5. Design Spec And Effect Image Synchronization

设计效果图、设计规范、Prototype 和相关说明属于同一资产包。其中一项发生已确认
变更时，必须先检查其他资产是否受影响，并在同一 Revision ID 下同步更新所有受影响
资产：

1. Current Design Spec
2. 对应 Current Prototype 或实现
3. 受影响 viewport 和关键状态的效果图
4. Review 中的对照证据

四者必须使用同一 `object-id` 与 Revision ID。未受影响的资产不强制重导出，但
Review 必须记录“不受影响”的检查结论。缺少受影响的必需项时结论为 `BLOCK`。
仅改效果图却不检查规范，或仅改规范却不检查效果图，都不能提升为 Current。

## 6. Snapshot Discipline

- 普通文字、样式或小范围修正依赖 Git 历史，不复制完整资产包。
- Review 只保存判断所需证据，不要求为未受影响的资产生成重复文件。
- 只有人工批准、重要设计节点、发布或正式 Milestone 才保存必要快照。
- 快照必须使用 `YYYY-MM-DD-NNN` Revision ID，并与同次修改的 Review 一致。

## 7. Archive And Delete

Archive 条件：

- 已被替代
- 有产品、技术、设计或验收追溯价值
- 路径和引用已完成治理

Safe Delete 条件必须同时满足：

- 无 Markdown、脚本、配置、Agent、构建或部署引用
- 可重新生成
- 无历史决策价值
- 非验收证据
- 已获得明确删除授权

无法确认时标记 `Protected`，不移动、不删除。

## 8. Inventory

受治理资产必须能在现有 Inventory 或专项 Review 中定位。Inventory 记录路径、
类型、状态、有效性、重复关系和处置结果。文件移动、归档或删除后必须在同一变更中
更新 Inventory，不能留下仅靠 Agent 记忆解释的路径。
