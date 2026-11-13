# Curis Review Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Parent: `docs/Engineering/Curis_Engineering_Convention.md`

---

## 1. Purpose

Review 用于判断一个候选是否具备人工批准和成为唯一 Approved Current 的条件。
Review 不是变更说明的副本，也不能用陈述代替证据。AI Agent 可以执行检查并建议
`PASS`，但不能代替人工批准。

## 2. Required Review Record

Review 至少记录：

- Objective 和 Issue
- `object-id`
- Current 路径与候选路径
- Baseline branch + full SHA
- Candidate branch + full SHA
- 修改文件和明确非目标
- Revision ID
- 执行的校验及结果
- 引用、资产、数据、安全和兼容性影响
- 剩余风险
- 结论

Review 文件使用：

```text
YYYY-MM-DD-NNN_<object-id>_review.md
```

## 3. Review Gates

### Current Gate

- 已定位唯一 Approved Current。
- 候选基于 Current，而非 History、截图或 Agent 记忆。
- 没有第二个候选被误标为 Current。
- 仅在确认不存在对应资产时新建候选。
- 未经人工批准的 Revision 未替代 Current。

### Naming And Folder Gate

- 文档、图片、Prototype 和 Prompt 命名合规。
- 没有 `final`、`latest`、`new`、`v2`、副本、Agent 版本或模型版本。
- History、Milestone 和 Current 路径职责清晰。

### Asset Gate

- Source 与 Derived 可追溯。
- 同一对象只有一个 Approved Current 资产包。
- 重复资产已复用或分类，不遗留无主副本。
- 移动或删除前已检查所有有效引用。

### Design Synchronization Gate

如变更影响视觉结果，必须同时审查：

- Design Spec
- Prototype 或实现
- 关键状态和 viewport 的效果图
- 同一 Revision ID 的对照证据

Review 必须记录设计规范、效果图、Prototype 和说明的影响检查结果。受影响资产任一
缺失即 `BLOCK`；未受影响资产无需重复生成。

### Collaboration Gate

- Task Packet 范围明确。
- 并行 Agent 没有修改同一对象。
- Handoff 包含 SHA、Revision ID、文件、校验和剩余问题。

### Git Gate

- Diff 只包含授权范围。
- 无意外二进制、生成输出、密钥或业务代码变更。
- `git diff --check` 通过。
- Commit 和分支符合 Git Convention。

## 4. Conclusions

Review 只能给出：

- `PASS`：全部必需门槛满足，可以提交人工批准。
- `BLOCK`：存在未满足门槛，不得提升。
- 合同已定义的特定阻塞状态，例如 `BLOCKED_PENDING_CONTRACT`。

不得使用“基本完成”“看起来可以”“局部通过”替代结论。

## 5. Approval And Promotion

只有同时满足以下条件才能提升：

1. Review 结论为 `PASS`。
2. 获得授权人员的明确批准。
3. 候选仍基于当前 Approved Current，且不存在第二个已批准候选。

提升时：

1. 将一个 Revision 提升为唯一 Approved Current。
2. 原 Current 通过 Git 追溯；只有必要的重要节点才保存 Revision/Milestone 快照。
3. 更新有效引用和 Current 登记。
4. 必要时更新 Frozen Decision、Current State 和 Change Log。
5. 仅在人工批准、重要设计节点或正式 Milestone 时保留必要快照。

Review 结论本身不授权 merge、push、删除或发布；这些动作仍需明确授权。
