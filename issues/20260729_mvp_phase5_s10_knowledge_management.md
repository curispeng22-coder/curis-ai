# MVP Phase 5 / S10 — 知识管理真实闭环

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase5_s10_knowledge_management_review.md`

## Objective

按 Curis v1.0 既定 Knowledge 边界完成“Obsidian/本地文件连接 → 资料入库 → 基础检索 → 资料详情”真实闭环。

## Product Boundary

- 入口属于现有资料中心；不新增 Workspace、Admin、Knowledge Graph、Memory 或第二套文件系统。
- Knowledge 是外部资料，不冒充 User/Project/Employee Memory；Context Engine 留到 S11。
- 复用 Capability Registry 的 Connector 类型语义，但不要求 Platform Admin。
- 本 Sprint 只支持本地 Markdown/Text；不接云盘、GitHub、向量数据库、Embedding 或 OCR。
- 文件读取仅限 `CURIS_KNOWLEDGE_ROOTS` 明确配置的根目录；拒绝未配置、越界、软链接逃逸、超限和非文本文件。
- 不持久化凭证；资料来源、路径、摘要、标签、项目关联与更新时间必须可追溯。
- 缺失事实显示 `未记录`。

## Implementation

- 新增 tenant-scoped KnowledgeEntry 持久化与资料中心 API。
- 新增受控本地文件 Connector：列出已配置根、预览并导入 `.md/.txt`。
- 资料中心展示真实资料、来源、项目、标签和更新时间；支持标题/正文/标签基础检索。
- 资料详情展示持久化正文与来源事实。
- 修正当前状态中将 S10 误标为 Phase 6 的文档标签。

## Allowed Files

- `issues/20260729_mvp_phase5_s10_knowledge_management.md`
- `reviews/20260729_mvp_phase5_s10_knowledge_management_review.md`
- `backend/app/main.py`
- `backend/app/database.py`
- `backend/app/knowledge_service.py`
- `backend/tests/test_mvp_phase5_s10_knowledge_management.py`
- `frontend/lib/knowledge.js`
- `frontend/app/ceo-office/knowledge/page.js`
- `frontend/app/ceo-office/knowledge/entries/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可在资料中心查看安全配置的本地文件根，并导入其中真实 `.md/.txt` 文件。
2. 导入前后端均校验文件根、扩展名、大小与租户；不允许任意路径读取。
3. 手工资料与文件资料均真实持久化，记录来源、路径、摘要、标签、项目关联和时间。
4. 用户可按标题、正文或标签检索，并进入资料详情查看真实正文与来源事实。
5. 重复导入同一租户同一路径更新原条目，不制造重复记录。
6. 无资料、无项目、无标签或无来源时保持真实空态/`未记录`。
7. 不新增依赖、Workspace/Admin、Memory、Knowledge Graph、Embedding、云服务或凭证。
8. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
