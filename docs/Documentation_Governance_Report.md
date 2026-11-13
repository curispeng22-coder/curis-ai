# Curis Documentation Governance Report

Status: Review

Baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

Updated: 2026-07-30

## 1. Executive Conclusion

Curis 文档当前存在明显的多事实源、旧路径、旧阶段状态和设计资产噪声。

第一阶段已经完成：

- 全量文档与设计/原型资产扫描
- 逐文件 Document Inventory
- 当前唯一事实入口
- 文档状态和权威规则
- 文档迁移计划
- 四项当前关键 Decision
- Change Log
- 根 README 和 AGENTS 当前入口修正

本阶段没有移动或删除既有文档，没有修改业务代码，也没有改变产品逻辑。

## 2. Document Count

治理前扫描：

| Type | Count |
| --- | ---: |
| Total | 1,384 |
| Markdown | 1,000 |
| HTML | 144 |
| PNG design/export assets | 191 |
| Mermaid | 28 |
| JSON | 10 |
| JavaScript prototype assets | 5 |
| CSS prototype assets | 4 |
| Design source | 1 |
| MJS prototype asset | 1 |

本阶段新增 10 个治理文档后，完整 Inventory 为：

```text
1,394 files
```

逐文件清单：

`docs/00_Context/DOCUMENT_INVENTORY.md`

## 3. Classification Result

| Classification | Count | Meaning |
| --- | ---: | --- |
| Frozen | 335 | 当前标准或冻结历史证据 |
| Review | 599 | 等待确认或尚未完成权威判定 |
| Draft | 0 | 扫描未自动认定 Draft |
| Deprecated | 460 | 已被当前方向替代，不得作为当前依据 |

有效性分类：

| Validity | Count |
| --- | ---: |
| 当前权威 | 10 |
| 历史证据 | 562 |
| 研究参考 | 50 |
| 待复核 | 312 |
| 非当前有效 | 460 |

模块分布：

| Module | Count |
| --- | ---: |
| Governance | 262 |
| Task / Execution | 154 |
| UI / Design System | 138 |
| Capability | 119 |
| Project | 114 |
| Company / CEO Office | 100 |
| Model / Usage | 99 |
| Business Department | 71 |
| General | 67 |
| Assistant | 66 |
| Employee | 58 |
| Knowledge | 37 |
| Identity / Security | 28 |
| Research | 26 |
| Artifact | 20 |
| Memory | 18 |
| Runtime / Deployment | 17 |

## 4. Current Source Conflicts

### Current State Duplication

以下文件同时承担过“当前状态”职责：

- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `docs/pmo/current-status.md`

新规则：

```text
docs/00_Context/CURRENT_STATE.md
```

是唯一当前事实入口。旧状态文件第一阶段保持原位，但在 Inventory 中标记为
`Deprecated` 和 `Semantic:CURRENT_STATE`，等待后续引用安全迁移。

### Product Baseline Duplication

主要重叠文件：

- `docs/product/CURIS_PRODUCT_BASELINE.md`
- `docs/product/curis-product-vision-current-stage.md`
- `docs/product/prd.md`
- `docs/product-development-spec.md`
- `knowledge/000_Project_Brief.md`
- `knowledge/002_Product_Vision.md`

其中 `curis-product-vision-current-stage.md` 仍把复杂 CEO Office 标为后置，与当前代码
基线冲突，已分类为 Deprecated。其他文件保留为待复核产品输入，Phase 2 再收敛为一个
Frozen Product 文档。

### Architecture Duplication

架构事实散布在：

- `knowledge/003_Architecture.md`
- `docs/system_design.md`
- `docs/architecture/`
- `docs/contracts/`
- 多组 class/sequence Mermaid
- Feature Issue 和 Review

当前架构事实先由 Current State 和四个新 ADR 裁决；Phase 2 再建立
`docs/02_Architecture/` 唯一入口。

### UI And Prototype Duplication

`frontend/design-spec/` 同时包含：

- 当前 CEO Office 设计输入
- `_archive`
- `_samples`
- Curis UI V2
- 390/1024/1440 多尺寸导出
- HTML Prototype

路径中无法直接判断所有文件是否仍被设计或测试引用，因此第一阶段只分类，不移动。

## 5. Exact Duplicate Files

Git Blob 检测发现 6 组、12 个完全相同文件：

1. `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-miniapp-detail.png`
   与 `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-miniapp.png`
2. `frontend/design-spec/curis-ui-v2/docs/ui/exports/1024/project-xhs-workflow-detail.png`
   与 `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1024/project-xhs.png`
3. `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-miniapp-detail.png`
   与 `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-miniapp.png`
4. `frontend/design-spec/curis-ui-v2/docs/ui/exports/1440/project-xhs-workflow-detail.png`
   与 `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/1440/project-xhs.png`
5. `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-miniapp-detail.png`
   与 `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-miniapp.png`
6. `frontend/design-spec/curis-ui-v2/docs/ui/exports/390/project-xhs-workflow-detail.png`
   与 `docs/99_Archive/design/curis-ui-v2/docs/ui/exports/390/project-xhs.png`

第一阶段没有删除这些文件。后续必须先确认 Design Review、HTML 和自动化引用。

Inventory 共标记 400 个 exact 或 semantic duplicate candidates。Semantic 标记表示
同一主题存在多份候选事实，不表示文件内容完全相同。

## 6. Deprecated And Archive Candidates

主要 Deprecated 集合：

| Path/Type | Count | Recommendation |
| --- | ---: | --- |
| `.workbuddy/` documents | 16 | 归档为历史 Agent 探索 |
| `docs/99_Archive/curis_workspace_blueprint/` | 17 | 已归档的历史蓝图 |
| `curis_workspace_blueprint/ADR/` | 2 | 决策记录保留原路径 |
| `docs/sprints/` | 14 | 归档为历史 Sprint |
| `docs/release/` | 29 | 归档为历史发布证据 |
| `docs/demo/` | 6 | 归档为历史 Demo |
| `docs/handoff/` | 2 | 归档为历史交接 |
| `docs/prototypes/` | 1 | 归档为历史 Prototype |
| `frontend/design-spec/curis-ui-v2/` | 266 | 归档为旧 UI V2 |
| CEO Office `_archive/` | 16 | 归档 |
| CEO Office `_samples/` | 13 | 归档为设计样例 |
| HTML documents | 144 | 默认归档，逐个检查引用 |

必须保留但不能继续作为当前方向：

- CEO Office 固定秘书栏方案
- Task-first 默认入口方案
- WorkBuddy/Codex 作为产品基础的探索稿
- 独立 Workspace/Admin 默认运行体系
- 根 `curis.sqlite` 和旧 Admin 数据库方向
- 旧 UI V1/V2/V3 与静态 Prototype
- 已被当前实现替代的阶段 PRD 和架构计划

历史设计决策、Issue、Review 和 Release Evidence 不删除。

## 7. Broken Or Stale References

确认的失效引用：

- 根 README 原先引用不存在的 `docs/curis-takeover/`
- `knowledge/NOW.md` 仍引用不存在的 `docs/curis-takeover/`
- `docs/product/CURIS_PRODUCT_BASELINE.md` 声称日常必读文件包含不存在的
  `docs/delivery/CURRENT_DELIVERY_TARGET.md`
- 原 AGENTS 仍声明 Phase-1C 为当前 Gate

本阶段已修正根 README 和 AGENTS。其他旧文档保持原位并进入迁移计划，避免在未确认时
大范围修改历史内容。

## 8. Status Coverage

治理前：

```text
245 / 1,000 Markdown files
```

存在某种 `Status:` 或 `状态:` 标记，但历史值不统一，包含 Accepted、Completed、
Implementation Report、Phase 状态和自由文本。

本阶段新增统一规则：

- Draft
- Review
- Frozen
- Deprecated

新建治理文档全部使用统一状态。旧文件将在 Phase 2 按文档域逐批补充，不执行全仓机械替换。

## 9. Temporary Garbage Candidates

只读扫描发现：

| Candidate | Observed Size/Count |
| --- | ---: |
| Workspace runtime logs | 40 files |
| `backend/selfuse.log` | 132 KB |
| `deploy/curis/gateway/.generated` | 2.4 MB |
| `frontend/.next` | 1.8 GB |
| `frontend/node_modules` | 436 MB |
| `.pytest_cache` | 152 KB |

这些内容本阶段没有删除。

后续清理必须确认：

- 文件未被 Git 跟踪
- 文件不是 Review Evidence
- 文件可由标准命令重新生成
- 不涉及数据库、密钥、用户数据或历史设计决策

## 10. Migration Recommendation

推荐顺序：

1. 冻结 `00_Context`
2. 收敛 `01_Product`
3. 收敛 `02_Architecture`
4. 确认当前 Design System 后收敛 `03_Design`
5. 整理 `04_Development`
6. 为当前模块建立 `05_Features` 索引
7. 迁移 Research 到 `06_Research`
8. 统一旧 ADR 到 `07_Decisions`
9. 将 Release Notes 和状态变化整理到 `08_Change_Log`
10. 完成引用检查后分批迁入 `99_Archive`
11. 最后处理可再生成的 log、cache 和 generated output

不建议直接执行全仓移动。当前 1,394 个文件中，大量路径可能被 Markdown、测试、构建、
CI、设计验收或自动化引用。

详细方案：

`docs/00_Context/DOCUMENT_MIGRATION_PLAN.md`

## 11. Maintenance Rules

### Agent Start

所有 Agent 只默认读取：

1. `docs/00_Context/CURRENT_STATE.md`
2. 相关模块文档
3. `docs/08_Change_Log/CHANGE_LOG.md` 最近相关记录

不得默认读取全部历史文档。

### Frozen Change

修改 Frozen 文档必须：

1. 更新 Decision
2. 更新 Change Log
3. 更新 Current State
4. 检查仓库引用
5. 记录验证证据

### New Document

新文档必须：

- 使用目标目录
- 包含统一 Status
- 包含 Baseline 和 Updated
- 明确 Module 和 Owner
- 说明是否替代旧文档

### Archive

- Deprecated 文档不再参与当前决策
- 历史 Decision 和 Review 只归档、不删除
- Archive 迁移必须有独立清单和引用审计

## 12. Phase 1 Decision

第一阶段结论：

```text
ANALYSIS AND GOVERNANCE FOUNDATION COMPLETE
MASS MIGRATION NOT STARTED
DELETION NOT STARTED
BUSINESS CODE UNCHANGED
WAITING FOR CONFIRMATION
```
