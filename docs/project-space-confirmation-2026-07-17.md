# Curis 项目空间整理 — 归属确认清单（交接版）

> **生成日期**：2026-07-17
> **生成方**：齐活林（交付总监）/ 软件开发团队主理人
> **用途**：项目空间整理确认，转交 **Workspace 端团队** 参考
> **性质**：⚠️ 仅确认，未执行任何删除 / 移动 / 覆盖 / Git 清理。本文档所有结论基于只读核查。

---

## 0. 核查方法（只读）

- `git status --short` — 未提交 / 未跟踪文件
- `git worktree list` — 工作树与活跃分支
- `cat .gitignore` — 已忽略的构建产物 / 缓存 / 数据库
- `grep` 于 `backend/app/main.py:660`、`backend/app/database.py:157` — 实际数据库路径
- `ls` / `git ls-files` — 目录内容与 Git 跟踪状态

**当前主分支**：`Admin`（commit `8f4b62bd`）。

---

## 1. 逐项归属确认清单

| 文件 / 目录 | 所属团队 | 当前用途 | 状态 | 是否影响当前任务 | 建议动作 | 负责人 |
|---|---|---|---|---|---|---|
| `frontend/app/employees/page.js` | Workspace 端（其他团队 UI 范围）；本团队曾做 i18n 修改 | Workspace 员工目录页面（最小版本 + 编辑） | **保留** | 是 — `git status` 为 `M`（已跟踪未提交） | 确认归属后提交；本团队改动随员工目录任务一并提交或交还 Workspace 端 | Workspace 端 UI 团队（本团队修改部分为遗留，待交接） |
| `backend/tests/`（新增/未提交测试） | 本团队 QA（严过关） | Wave-1/Wave-2 验证证据 + 员工目录 QA（13 个未跟踪文件 + `conftest.py` 已改） | **保留** | 是 — 全部未提交，属本团队交付物 | 单 commit 整体提交（标注 QA/Wave 证据），不混入源码 | 严过关（QA） |
| `docs/prd/` | 本团队 PM（许清楚） | 含 `workspace-employee-directory.md`（员工目录 PRD，未提交） | **保留** | 否 | 提交归档 | 许清楚（PM） |
| `docs/research/` | 本团队 PM / 架构 | agent-conversion 多源转换、aiearn 内容营销、平台资质追踪等（7 个未提交文件） | **保留** | 否 | 提交归档 | 许清楚 / 高见远 |
| `docs/plan/` | 本团队 架构 / PM | v1-selfuse 架构、content-department 开发规范、agent-conversion 设计等（多 md/mermaid 未提交） | **保留** | 否 | 提交归档 | 高见远（架构） |
| `.agents/skills/` | **待确认** | 15 个设计/UI 类技能（brandkit、design-taste-frontend、gpt-taste、high-end-visual-design、image-to-code、imagegen-frontend-*、industrial-brutalist-ui、minimalist-ui、redesign-existing-projects、stitch-design-taste、full-output-enforcement） | **待确认** | 否 | 确认来源与用途后再决定纳入版本管理或移除 | 待确认 |
| `.worktrees/`（6 个 Codex 分支） | Codex（CTO）分支，非本团队 | phase1b/phase1c、ai-secretary、company-runtime-office-view、low-token-workflow-v2 并行开发 | **保留 / 待确认** | 否 | 逐棵确认活跃性后用 `git worktree remove`/`prune` 清理 | Codex（CTO）/ 总控协调 |
| `Curis AI Workspace Worktrees/` | Codex（CTO）分支 | 含 `phase9a-workspace-metering`，`git worktree list` 标记 **prunable**（孤儿工作树） | **可清理** | 否 | `git worktree prune` 清理残留注册；确认无未保存改动后移除目录 | Codex（CTO）/ 总控协调 |

---

## 2. 特别确认

### A. 哪些工作树仍有活动任务

| 工作树 | 分支 | 活跃性判断 |
|---|---|---|
| 主分支（本仓库根） | `Admin` (8f4b62bd) | **活跃** — 含未提交测试/文档/员工页改动 |
| `.worktrees/phase1c-ceo-office-first-slice` | `codex/phase1c-ceo-office-first-slice` | **疑似活跃** — 对应 `TASKS.md` 当前 Sprint「Phase-1C CEO Office UI First Slice」 |
| `.worktrees/phase1c-company-project-bootstrap-ui` | `codex/phase1c-company-project-bootstrap-ui` | **疑似活跃** — Phase-1C 相关 |
| `.worktrees/phase1b-skill-runtime-integration` | `codex/phase1b-*` | 早期 Sprint，**疑似已完成/闲置 → 待确认** |
| `.worktrees/low-token-workflow-v2` | `codex/low-token-workflow-v2` | 早期实验，**疑似已完成/闲置 → 待确认** |
| `.worktrees/ai-secretary-planning` | `codex/ai-secretary-planning` | 无对应已知 Sprint，**待确认** |
| `.worktrees/company-runtime-office-view` | `codex/company-runtime-office-view` | 无对应已知 Sprint，**待确认** |
| `Curis AI Workspace Worktrees/phase9a-workspace-metering` | `codex/phase9a-workspace-metering` | **已 orphaned（prunable）** — 无活动任务，**可清理** |

> 明确活跃 = 主分支 `Admin` + phase1c 两个；其余 Codex 工作树需逐棵确认，不建议直接删。

### B. 哪些 Admin 文件尚未提交

本团队（Admin 分支）未提交内容：

- **已跟踪未提交（M）**：`backend/tests/conftest.py`、`frontend/app/employees/page.js`、`data/sample_publish_package.md`、`.workbuddy/memory/2026-07-12.md`、`.workbuddy/memory/MEMORY.md`、`knowledge/NOW.md`
- **未跟踪（??）**：`backend/tests/` 下 13 个测试/helper、`docs/prd|research|plan|design` 多个文档、`docs/*.mermaid`、`docs/product/*`、`.agents/skills/`、`skills-lock.json`、`.workbuddy/memory/2026-07-13.md`、`Curis AI Workspace Worktrees/`
- **已干净提交**：`frontend/app/platform/*`（Admin 资产工厂控制台 10 个面板）全部已提交，无未提交改动 ✅

### C. `curis.sqlite` 与 `backend/data/curis.sqlite` 是否保留

| 文件 | 大小 | 跟踪状态 | 结论 |
|---|---|---|---|
| 根 `curis.sqlite` | 835KB | **已 git 跟踪**（种子库） | **保留** — 规范种子数据，已入库 |
| `data/curis.sqlite` | 1.2MB | 被 `data/*.sqlite` 忽略 | **保留（本地运行时）** — `main.py:660` 默认 `os.getenv("CURIS_DB", "data/curis.sqlite")`，即应用**实际活动库** |
| `backend/data/curis.sqlite` | 737KB | 被 `backend/data/*.sqlite` 忽略 | **待确认（疑似陈旧副本）** — 默认路径是 `data/curis.sqlite`，此文件极可能是早先用 `CURIS_DB=backend/data/...` 启动遗留；清理无 git 影响，但建议先确认无进程指向它 |
| `backend/data/_wave2_smoke.sqlite` | 737KB | 被 `backend/data/*.sqlite` 忽略 | **可清理** — Wave-2 冒烟测试产物 |

### D. `admin-platform/` 是否作为 Admin 独立代码目录

**结论：目前不是活跃代码目录，仅为预留占位。**

- 内容仅 `README.md`（已跟踪）+ 空 `docs/` + `.DS_Store`，**无任何实现代码**。
- README 写明其定位是「商业平台管理产品」的**未来**归属地（`admin-platform/app|docs|tests/`），但当前真实 Admin 代码在：
  - 前端：`frontend/app/platform/`（资产工厂控制台，已提交）
  - 后端：`backend/`（Admin 相关端点）
- **状态：保留（作为预留命名空间，非当前代码载体）**；如需落地独立目录，应先开 Issue 明确迁移范围。

### E. Admin 是否同意后续清理缓存 / 旧环境 / 无效工作树

以下**全部已被 `.gitignore` 忽略**（`.next/`、`node_modules/`、`frontend/.next/`、`frontend/node_modules/`、`__pycache__/`、`*.pyc`、`.pytest_cache/`、`.venv/`、`.worktrees/`、`.pnpm-store/`），清理**不影响 git 提交**：

- `.next/`、`frontend/node_modules/` — **可清理**（前端构建产物）
- `.pytest_cache/`、`__pycache__/`、所有 `*.pyc` — **可清理**（测试/Python 缓存）
- `.venv.stale-20260711-033226`（**陈旧虚拟环境，非当前 `.venv`**）、`.pnpm-store/` — **可清理**
- `.worktrees/` 内**已完成/无效**工作树 — 建议用 `git worktree remove` / `git worktree prune` 清理（正规 git 操作，非直接删文件）；`Curis AI Workspace Worktrees/phase9a` 已 prunable，优先清理

> **Admin（齐活林组）立场：同意后续按上述方式清理**，但要求：
> ① 工作树须逐棵确认活跃性后再清；
> ② 用 git 正规命令而非裸删；
> ③ `backend/data/curis.sqlite` 先确认无活动进程再清；
> ④ 清理前如有需要可先 `cp` 备份。

---

## 3. 交接要点（给 Workspace 端团队）

1. **`frontend/app/employees/page.js` 是 Workspace 端文件**，本团队（Admin）曾做过中文化修改且尚未提交，请 Workspace 端团队接手其归属与提交。
2. **`admin-platform/` 目前是空占位**，真实 Admin 前端在 `frontend/app/platform/`、后端在 `backend/`；不要误以为 Admin 代码在 `admin-platform/` 下。
3. **活动数据库是 `data/curis.sqlite`**（运行时），根 `curis.sqlite` 是已入库种子；`backend/data/curis.sqlite` 疑似旧副本，清理前请确认。
4. **Codex 工作树（`.worktrees/`、`Curis AI Workspace Worktrees/`）与本团队无关**，清理由 Codex / 总控协调，勿在本团队 Admin 分支操作。
5. **缓存与陈旧 venv（`.next/`、`node_modules/`、`__pycache__/`、`.pytest_cache/`、`.venv.stale-*`）均已被 git 忽略**，可安全清理，不影响提交。

---

*本文档为只读确认产物，所有"建议动作"均需相关负责人显式确认后方可执行。*
