# Curis 产品文档迁移与归档规则

**Status: Frozen**  
**生效日期：2026-08-14**  
**唯一入口：** [`PRODUCT_DOCUMENT_POINTER.md`](./PRODUCT_DOCUMENT_POINTER.md)

## 1. 唯一真相目录

产品定义、设计、架构、开发说明、研究、审计和决策，统一写入：

`/Users/yy/Documents/Curis AI Workspace/docs/`

`.codex/worktrees/*`、临时工作目录和仓库根目录不是产品真相，只能作为实现现场或迁移暂存区。

## 2. 分类规则

| 内容 | 唯一路径 |
| --- | --- |
| 当前状态、文档指针、清单、治理规则 | `docs/00_Context/` |
| 产品定义、唯一 Blueprint、Master Map、Page Map、研究、人才市场、开发队列 | `docs/01_Product/` |
| 系统、运行时、数据与部署架构 | `docs/02_Architecture/` |
| 视觉、交互、页面、设计系统 | `docs/03_Design/` |
| 开发规范、实现说明、测试约定 | `docs/04_Development/` |
| 已确认的产品/架构决策 | `docs/07_Decisions/` |
| 审计、验收、证据、Review | `docs/reviews/` |
| 历史材料 | `docs/99_Archive/`（仅在迁移任务中处理） |

## 3. 唯一文件规则

- 当前 Blueprint 只有 `docs/01_Product/Curis_Product_Blueprint.html`，不得创建 Blueprint_v2 或平行 Blueprint。
- 已有 Master Map、Page Map、人才市场、研究和队列文件，优先更新原文件，不以 `_new`、日期副本替代。
- 文件状态只使用 `Draft`、`Review`、`Frozen`、`Deprecated`。
- 历史文件不直接删除；先登记来源、引用和迁移目标，再由独立清理任务归档。

## 4. 会话交付格式

每个会话完成文档工作后，必须回报：

1. 绝对路径与文件状态；
2. 文档来源（研究、产品决策、实现事实或审计证据）；
3. 是否更新 `PRODUCT_DOCUMENT_POINTER.md`、`CURRENT_STATE.md` 或 `CHANGE_LOG.md`；
4. 下一步和仍未解决的问题。

新会话开始前只需读取 `AGENTS.md`、`CURRENT_STATE.md`、相关 Frozen 文档、最新 Change Log 和本规则，再由文档指针定位具体材料。

## 5. 开发消费规则

主开发只消费文档指针指向的主目录文件、Frozen 决策和正式 Issue/Review。worktree 中的孤立文档、根目录临时副本和未登记研究结论不得直接成为开发依据。

