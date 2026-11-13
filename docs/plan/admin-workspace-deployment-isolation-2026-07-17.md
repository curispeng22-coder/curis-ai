# Admin / Workspace 部署隔离方案

> 制定依据：总控决策席 2026-07-17 边界治理指令
> 制定人：Admin 交付总监 齐活林（软件团队主理人）
> 阶段范围：**仅边界确认 + 方案设计**。本阶段不迁移代码、不改部署、不新增依赖、不执行 Git 提交/清理。
> 文档三态标记：🌐 Current（当前事实）/ 🎯 Target（目标态）/ 🔧 Interim（过渡态可执行治理）

---

## 1. 边界规则生效确认（指令 1–5）

| # | 规则 | 归属确认 | 执行姿态 |
|---|------|---------|---------|
| 1 | Admin 不直改 Workspace 页面（`page.js` / `ceo-office/**` / `employees/page.js` / Workspace 业务页） | Admin 已确认；`employees/page.js` 既有 Admin 中文化改动已于 07-17 确认**交还 Workspace 团队** | ✅ 立即生效，后续 Admin 不再触碰 |
| 2 | Workspace 不修改 Admin 页面（`platform/**` / 资产工厂 / 平台管理 / 商业化） | Workspace 端（其他团队）已通过交接文档知悉 | ✅ 立即生效 |
| 3 | 任何跨团队修改先建 Issue（文件/团队/部署端/验收人/是否共享后端） | Admin + Workspace 共同遵守 | ✅ 立即生效，Issue 为唯一跨边界入口 |
| 4 | 分别部署：独立启动配置/环境变量/部署目标；不复制覆盖、不共享本地 DB、不互带构建产物/依赖/缓存 | 当前为单体，需按 §3 目标态改造 | 🔧 过渡态先按 Issue 门禁管控，目标态拆分 |
| 5 | 目录边界：`platform/**`=Admin；`ceo-office/**`+`employees/**`=Workspace；`backend/`=共享（改动须 Issue）；`admin-platform/`=预留空目录（非当前实现目录） | 与 07-17 项目空间确认文档一致 | ✅ 立即生效 |

**Admin 立场：上述 1–5 条即日起作为团队强制纪律执行。**

---

## 2. 🌐 当前架构事实基线（只读核查）

| 维度 | 现状 |
|------|------|
| 前端 | **单体** Next.js 16（`frontend/`），`dev` 默认端口 3000；`scripts: dev/build/start/lint`；无 `Dockerfile`/compose/Makefile；无 `.env` |
| 前端 Admin 代码 | `frontend/app/platform/**`（10 个面板，已提交） |
| 前端 Workspace 代码 | `frontend/app/`、`frontend/app/ceo-office/**`、`frontend/app/employees/**`、`frontend/app/control/**`、`frontend/app/page.js`（根页「Curis 工作台」） |
| 共享耦合点 | `app/globals.css`（admin-* 与 ceo-* token 混用）、`app/layout.js`（根 metadata 取向 Workspace）、`app/taskViewModel.mjs`（被 Workspace `page.js` 引用） |
| 后端 | **单体** FastAPI（`backend/app/main.py`），`uvicorn backend.app.main:app` 启动；CORS 默认 `http://localhost:3000`；DB=`data/curis.sqlite`（`CURIS_DB` 可覆盖） |
| 数据库 | 单一 `data/curis.sqlite`（约 1.2MB，活动库）；根 `curis.sqlite` 为已跟踪种子；`backend/data/curis.sqlite` 已确认**无进程使用**（疑似旧副本） |
| 当前分支 | `Admin` |

**结论：当前 Admin 与 Workspace 共用同一前端应用、同一后端、同一数据库——并非物理隔离。指令 4 的"分别部署"是目标态，需后续拆分改造。**

---

## 3. 🎯 目标隔离架构（指令 6 八项）

### 3.1 代码入口
| 产品 | 入口（目标态） | 当前位置 |
|------|--------------|---------|
| Admin 前端 | `frontend-admin/app/**`（独立 Next.js 应用，仅含 `platform/**` 及 Admin 专属页） | 现 `frontend/app/platform/**` |
| Workspace 前端 | `frontend-workspace/app/**`（独立 Next.js 应用，含 `ceo-office/**`、`employees/**`、`page.js`、`control/**`） | 现 `frontend/app/{ceo-office,employees,page.js,control}/**` |
| 共享后端 | `backend/app/main.py`（保持单服务，但按产品契约对外提供 API） | 不变 |

### 3.2 启动命令
| 产品 | 开发 | 生产 |
|------|------|------|
| Admin 前端 | `cd frontend-admin && npm install && npm run dev -- -p 3100` | `npm run build && npm run start -- -p 3100` |
| Workspace 前端 | `cd frontend-workspace && npm install && npm run dev -- -p 3000` | `npm run build && npm run start -- -p 3000` |
| 后端（共享单实例） | `cd backend && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload` | `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000` |
| 后端（进程级隔离*） | Admin 实例 `--port 8001` + `CURIS_DB=admin.sqlite`；Workspace 实例 `--port 8002` + `CURIS_DB=workspace.sqlite` | 同上分端口 |

> \* 进程级隔离为可选增强；最小达标方案为"单后端 + 分离 DB + 前端分应用"。

### 3.3 环境变量
| 变量 | Admin 取值 | Workspace 取值 | 说明 |
|------|-----------|---------------|------|
| `CURIS_PRODUCT` | `admin` | `workspace` | 产品标识，用于后端契约路由/日志 |
| `CURIS_PORT` | `3100` | `3000` | 前端监听端口 |
| `CURIS_DB` | `data/admin.sqlite` | `data/workspace.sqlite` | **各自独立 DB 文件，严禁共享** |
| `CURIS_API_URL` | `http://localhost:8000` | `http://localhost:8000` | 指向共享后端 |
| `CURIS_ALLOWED_ORIGINS` | `http://localhost:3100` | `http://localhost:3000` | 后端 CORS 白名单（按产品收窄） |
| `NODE_ENV` | `development`/`production` | 同左 | 标准 |

> 当前这些变量均**不存在**，属目标态引入项，须通过独立 Issue 落地（不在本阶段）。

### 3.4 数据库边界
- 🎯 **每个产品独立 SQLite 文件**：`admin.sqlite` / `workspace.sqlite`，互不可见、互不可写。
- 共享后端通过 `CURIS_DB`（或 `CURIS_PRODUCT` 映射）选择对应库；不跨库 JOIN、不共享本地文件。
- 种子数据：Admin 资产种子与 Workspace 运行种子分别管理，各自 `seed_*.py`。
- 当前 `data/curis.sqlite` 为过渡态共用库，拆分前保持只读基线，待 DB 分离 Issue 执行后退役。

### 3.5 构建目录
| 产品 | 构建输出 | 约束 |
|------|---------|------|
| Admin 前端 | `frontend-admin/.next/` | 不进入 Workspace 构建树 |
| Workspace 前端 | `frontend-workspace/.next/` | 不进入 Admin 构建树 |
| 后端 | `backend/`（无独立构建产物，Python 源码即部署单元） | — |

> 严禁将一方 `.next/`、依赖目录（`node_modules/`）、缓存（`.pytest_cache/`、`__pycache__/`）带入另一方。

### 3.6 发布目录
- 目标：各自独立部署单元（容器镜像 / 静态托管 / 独立服务进程），发布路径物理隔离。
- Admin 发布物：`frontend-admin/` 构建 + 后端（Admin 契约域）；Workspace 发布物：`frontend-workspace/` 构建 + 后端（Workspace 契约域）。
- **禁止**通过复制文件或手动覆盖方式互相发布；发布须走各自 CI/CD 流水线（独立 artifact / tag）。

### 3.7 回滚方式
| 层级 | 回滚手段 |
|------|---------|
| 前端 | 按产品 Git Tag 回滚（`admin-vX.Y.Z` / `workspace-vX.Y.Z`），重新构建部署前序 Tag |
| 后端 | 共享后端按 `backend-vX.Y.Z` Tag 回滚；若采用进程级隔离则各自回滚 |
| 数据库 | 变更前对对应 `*.sqlite` 做快照备份；回滚 = 恢复该快照（Admin/Workspace 各自独立） |
| 配置 | 环境变量随发布单元版本化管理，回滚配置即回滚发布单元 |

> 当前尚未建立 Tag 体系，须作为前置动作登记 Issue（不执行）。

### 3.8 共享后端变更流程
1. **唯一入口 = Issue**：任何 `backend/` 改动必须建 Issue，字段含：修改文件、所属团队、目标部署端（Admin/Workspace/Shared）、验收负责人、是否共享后端变更。
2. **双lead 会签**：因后端共享，PR 须 Admin 与 Workspace 两侧负责人共同 review 通过方可合入。
3. **契约兼容**：后端 API 须版本化（如 `/api/v1/...`），任一产品侧改动不得破坏另一产品既有契约；破坏性变更须两侧同步发版并登记回滚点。
4. **部署形态**：后端作为单一共享服务部署；Admin / Workspace 前端经 `CURIS_API_URL` 各自指向。DB 分离在后端实例层（按 `CURIS_DB`）实现，前端无感知。
5. **禁止**：未经 Issue 直改 `backend/`；在 `backend/` 写入任一产品私有业务逻辑而不抽象为共享契约。

---

## 4. 🔧 过渡态可执行治理（本阶段即落地，无代码改动）

1. **Issue 强制门禁**：即日起 Admin↔Workspace 任何跨边界改动（含 `backend/`）先建 Issue，模板见 §3.8.1。
2. **禁止互改文件清单（硬约束）**：
   - Admin 禁改：`frontend/app/page.js`、`frontend/app/ceo-office/**`、`frontend/app/employees/**`、Workspace 业务页。
   - Workspace 禁改：`frontend/app/platform/**`、Admin 资产工厂/平台管理/商业化页。
3. **共享耦合点登记（待后续拆分 Issue，本阶段不改）**：
   - `frontend/app/globals.css`：admin-* / ceo-* token 混用 → 未来按产品拆分样式域。
   - `frontend/app/layout.js`：根 metadata 取向 Workspace → 拆分后各应用独立 layout。
   - `frontend/app/taskViewModel.mjs`：被 Workspace `page.js` 引用 → 随前端拆分迁移。
4. **DB 分离前置 Issue 已登记（不执行）**：`admin.sqlite` / `workspace.sqlite` 拆分 + 后端 product-context 改造。
5. **Tag/回滚体系前置 Issue 已登记（不执行）**：建立 `admin-v*` / `workspace-v*` / `backend-v*` Tag 规范。

---

## 5. 风险与待总控决策
| 风险 | 说明 | 建议 |
|------|------|------|
| 单体前端"分别部署"路径未定 | 方案 A：拆两独立 Next.js 应用（干净但需迁移）；方案 B：单应用 + 路由作用域构建配置（改动小但不彻底） | 建议开未来 Gate 由总控裁定，本阶段不执行 |
| 共享 DB 拆分需后端改造 | 需引入 product-context / `CURIS_DB` 路由，属后端变更（须 Issue） | 登记 Issue，待授权实施 |
| 回滚 Tag 体系缺失 | 当前无发布版本标记 | 登记 Issue 建立规范 |
| 进程级后端隔离可选 | 单实例共享 vs 双实例隔离，影响运维复杂度 | 最小达标=单实例+分离DB；按需升级 |

---

## 附：本次核查命令（只读，无副作用）
- `git status --short` / `git worktree list` / `git rev-parse --abbrev-ref HEAD` → 分支 `Admin`
- `ls frontend/app/`、`cat frontend/package.json`、`cat frontend/app/layout.js` → 前端单体结构
- `ls backend/`、`grep main.py:660 CURIS_DB` → 后端单体、DB 路径
- `ls data/`、`lsof data/curis.sqlite` → 活动库 `data/curis.sqlite`，`backend/data/curis.sqlite` 无进程占用
- `ls .env* next.config* Dockerfile docker-compose* Makefile` → 均无（无独立部署配置）
