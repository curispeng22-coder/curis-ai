# MVP Phase 5 / S10 — 知识管理真实闭环 Review

结论：`PASS`

日期：2026-07-29

Issue：`issues/20260729_mvp_phase5_s10_knowledge_management.md`

## 交付事实

- 用户可从 `CURIS_KNOWLEDGE_ROOTS` 明确配置的本地资料根选择并导入真实 Markdown/Text，或手工建立公司、项目、部门资料。
- KnowledgeEntry 按租户持久化标题、正文、摘要、标签、来源、相对路径、内容 SHA、项目/部门归属与时间；重复导入同一路径更新原条目。
- 用户可按标题、正文或标签检索，按公司/项目/部门筛选，并进入详情查看真实正文与来源事实。
- 本地 Connector 拒绝未配置根、绝对路径、目录穿越、软链接逃逸、非 `.md/.txt` 与超限文件；API 不返回或持久化绝对根路径。
- Knowledge 与 Memory 保持分离；未新增 Workspace/Admin、Knowledge Graph、Embedding、云服务、凭证或依赖。
- 修复单一项目/部门在下拉框中视觉已选中但表单状态为空的问题，默认归属现可直接保存。

## 验证证据

- 聚焦后端：`4 passed`。
- Frontend lint：`PASS`。
- Frontend build：`PASS`，26 个页面生成。
- 隔离干净提交候选全量后端回归：`1136 passed, 2 skipped, 0 failed`。
- 真实浏览器：Project `project-51354162-198b-4650-a1f6-3ffafac51e20`。
- 本地文件闭环：`Curis-MVP-验收.md` → Knowledge `knowledge-5946d58a-9672-4596-b9b3-89e89564e7e8` → “真实验收”检索 → 正文、根标签、相对路径和 SHA 详情可见。
- 手工项目资料闭环：`S10 项目检索规则` → Knowledge `knowledge-6d9d0aca-04e9-4bd4-8663-5e4faaacc1a7` → 项目筛选仅显示该条，并展示 `S10 知识项目` 归属。
- Desktop `1440×1000`：`scrollWidth = clientWidth = 1425`。
- Mobile `390×844`：列表 `scrollWidth = clientWidth = 390`；详情 `scrollWidth = clientWidth = 375`，无横向溢出。

## 变更说明

- 新增最小 tenant-scoped KnowledgeEntry 表、服务与 Workspace API。
- 新增受控本地文件 Connector、真实资料列表/检索/导入/创建与详情 UI。
- 修正 S10 Phase 标签，并将下一边界切换到 MVP Phase 6 / S11 基础 Memory。

Handoff: sent to 产品规划席
