# Curis Engineering Convention v1.0 Review Report

Status: Review

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Scope: `docs/Engineering/` 七份 Convention 与根目录 `AGENT.md`

---

## 1. Review Conclusion

Conclusion: `PASS`

Freeze Recommendation: `APPROVE`

七份规范在 Current、Revision ID、目录职责、资产包、Agent 接力、Review 与人工批准
条件上已经一致。当前候选可以提交人工审查；获得明确批准后，建议将七份 Convention
从 `Status: Review` 升级为 `Status: Frozen`。

本报告不执行冻结、不修改业务代码、不提交 Git。

## 2. Problems Found

| ID | Problem | Risk |
| --- | --- | --- |
| R-01 | “治理对象只有一个 Current”未明确为业务对象的唯一官方资产包 | 同一页面可能产生多套“官方”设计资产 |
| R-02 | 未明确只有不存在对应资产时才能新建 | Agent 容易绕过 Current 创建副本 |
| R-03 | Agent 不是 Contributor 的边界不够直接 | 可能形成 Codex/WorkBuddy 专属目录或规范 |
| R-04 | 设计同步规则未完整覆盖效果图、规范、Prototype 和说明 | 同一资产包可能出现修订错位 |
| R-05 | Review `PASS` 与人工批准、Approved Current 的转换条件不完整 | 未批准候选可能替代 Current |
| R-06 | Revision 同时使用 `YYYYMMDD_NNN` 和 `rNN` | 日期、流水号和版本命名可能分叉 |
| R-07 | Current 图片等示例包含日期和 Revision | Current 路径不稳定 |
| R-08 | Folder Convention 未回答 Draft/Review 的位置 | 候选可能散落在任意目录 |
| R-09 | Git History、History 目录和 Milestone 快照职责重叠 | 普通修改可能产生大量重复资产 |
| R-10 | Agent 默认读取清单过长，且总规范无任务路由 | 每次任务读取全部规范，增加上下文噪声 |
| R-11 | 缺少跨 Agent 完整接力示例 | Contributor 容易误建自己的 Current |
| R-12 | `AGENT.md` 未包含可定位路径 | 新 Agent 无法稳定找到入口 |

## 3. Corrections Applied

| ID | Correction |
| --- | --- |
| R-01 | 统一定义一个业务对象只有一个 `Approved Current` 资产包 |
| R-02 | 明确 Agent 先查 Current，仅确认没有对应 Current 或可复用资产时才能新建 |
| R-03 | 明确所有 Agent 只是 Contributor，Agent/模型不能用于目录、文件或资产包命名 |
| R-04 | 将效果图、设计规范、Prototype 和说明定义为同一资产包，并要求影响检查和必要同步 |
| R-05 | 统一转换条件为 Review `PASS` + 人工批准，未经批准的 Revision 不得替代 Current |
| R-06 | Revision ID 统一为 `YYYY-MM-DD-NNN`；当天从 `001` 递增，换日重置 |
| R-07 | Current 使用稳定语义名称；只有必要的 Revision/Milestone 快照带 Revision ID |
| R-08 | 明确 Current、Draft/Review、Revision History 和 Milestone 的路径职责 |
| R-09 | 普通修改只依赖 Git；只有人工批准、重要设计节点或 Milestone 保存必要快照 |
| R-10 | 总规范增加任务路由表，明确不要求每次读取全部七份规范 |
| R-11 | 增加 Codex 到 WorkBuddy 的完整设计资产接力示例和禁止项 |
| R-12 | `AGENT.md` 改为包含总规范相对路径的单句入口 |

## 4. Core Rule Coverage

| Required Rule | Result | Location |
| --- | --- | --- |
| 一个业务对象只有一个当前官方资产 | Covered | 总规范 Core Rules；Asset One Current Rule |
| 接手时先查找并维护 Current | Covered | 总规范、Asset、AI Collaboration、Git |
| 禁止 Agent/模型/new/final 等平行资产 | Covered | 总规范、Naming、Asset、AI Collaboration、Review |
| 只有确实不存在对应资产时才能新建 | Covered | 总规范、Asset、AI Collaboration、Review |
| Agent 只是 Contributor | Covered | 总规范、Naming、AI Collaboration |
| 设计资产包联动检查与同步 | Covered | 总规范、Asset、Review、Git |
| 未经批准的 Revision 不能替代 Current | Covered | 总规范、Asset、AI Collaboration、Review |
| 任一时刻只有一个 Approved Current | Covered | 总规范、Asset、Review |

Coverage: `8 / 8`

## 5. Consistency Check

| Topic | Unified Rule | Result |
| --- | --- | --- |
| Document status | Draft / Review / Frozen / Deprecated | Consistent |
| Current | `Approved Current`；Markdown Current 为 Frozen | Consistent |
| Revision ID | `YYYY-MM-DD-NNN` | Consistent |
| Sequence | 当天仓库内从 `001` 递增，换日重置 | Consistent |
| Shared revision | 同次文档、图片、Prototype、Prompt、说明和 Review 共用一个 ID | Consistent |
| Current filename | 稳定语义名称，不带 Agent、模型、final、new、v2 或 Revision ID | Consistent |
| Revision history | 默认由 Git 保存 | Consistent |
| Snapshot | 只为人工批准的重要节点或 Milestone 保存 | Consistent |
| Review transition | `PASS` 后提交人工批准；批准后才能成为 Current | Consistent |
| Folder ownership | 按业务对象聚合，不按格式、工具或 Agent 分散 | Consistent |

Conflicts Remaining: `0`

## 6. Folder Executability

规范现在可以直接回答：

- Current：所属领域现有权威路径；资产包使用稳定的
  `<owner-directory>/assets/<object-id>/`。
- Draft/Review：已有 Current 在任务分支同路径修改；新对象在预定官方路径创建一个
  Draft/Review；二进制对照候选可临时进入 `.review/<revision-id>/`。
- Revision History：普通修改由 Git 保存；必要快照进入
  `docs/99_Archive/<domain>/<object-id>/revisions/<revision-id>/`。
- Milestone：记录进入既有 Issue/Review/Decision/Change Log 目录；必要二进制快照
  进入 `docs/99_Archive/<domain>/<object-id>/milestones/<revision-id>/`。

现有已治理路径无需为了匹配示例立即迁移。

## 7. Multi-Agent Relay Validation

Scenario: `PASS`

验证路径：

```text
Codex 维护 Approved Current
→ 使用同一个 Revision ID 修改规范和效果图
→ Codex 不可用
→ WorkBuddy 读取 Current、Revision ID 和 Git diff
→ WorkBuddy 继续同一候选并同步受影响资产
→ Review PASS
→ 人工批准
→ 新 Revision 成为唯一 Approved Current
→ 原 Current 由 Git 或必要快照追溯
```

禁止项已经明确：WorkBuddy 不得创建 WorkBuddy 设计规范、
`workbuddy-version/` 或其他平行 Current。

## 8. Lightweight Execution Validation

Result: `PASS`

- Agent 只读入口、总规范和任务路由命中的专项规范。
- 普通修改使用 Git diff/history，不复制完整资产包。
- 未受影响的设计资产不强制重新生成，但必须完成影响检查。
- 只有人工批准、重要设计节点或正式 Milestone 保存必要快照。
- 不要求每次任务读取全部七份规范。

## 9. Unresolved Items

规范内容冲突：`0`

待治理动作：

1. 七份 Convention 仍为 `Status: Review`，等待人工批准。
2. 批准后才能统一升级为 `Status: Frozen`。
3. 冻结时再按现有治理规则更新 Current State、Change Log 和必要入口；本阶段不提前
   修改这些文件。

## 10. Files Reviewed

- `docs/Engineering/Curis_Engineering_Convention.md`
- `docs/Engineering/Naming_Convention.md`
- `docs/Engineering/Folder_Convention.md`
- `docs/Engineering/Asset_Convention.md`
- `docs/Engineering/AI_Collaboration_Convention.md`
- `docs/Engineering/Review_Convention.md`
- `docs/Engineering/Git_Convention.md`
- `AGENT.md`
