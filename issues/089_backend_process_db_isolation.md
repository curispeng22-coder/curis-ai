# Issue: 后端进程与数据库隔离

## 编号
089

## Owner
系统交付席（架构师高见远）

## 协调人
主理人齐活林（Admin 交付总监）

## 状态
实施中 / 双进程启动验证完成；逐表数据隔离未完成

## Context
当前后端为单体 FastAPI（backend/app/main.py），通过 `uvicorn backend.app.main:app` 启动，CORS 默认允许 localhost:3000，数据库 `data/curis.sqlite`（CURIS_DB 可覆盖）。Admin 与 Workspace 共用同一进程与同一 DB。需按部署隔离方案实现进程级隔离 + 独立 DB 文件。

## Objective
采用**两个独立后端进程**（推荐方案，不做复杂动态 DB 路由），Admin 与 Workspace 各自拥有独立后端实例与独立 SQLite 文件。

## Admin 使用的后端进程
- 进程 A（Admin 后端）
- 启动：`cd backend && uvicorn backend.app.main:app --host 0.0.0.0 --port 8001`
- 环境变量：`CURIS_PRODUCT=admin`、`CURIS_DB=data/admin.sqlite`、`CURIS_ALLOWED_ORIGINS=http://localhost:3100`

## Workspace 使用的后端进程
- 进程 B（Workspace 后端）
- 启动：`cd backend && uvicorn backend.app.main:app --host 0.0.0.0 --port 8002`
- 环境变量：`CURIS_PRODUCT=workspace`、`CURIS_DB=data/workspace.sqlite`、`CURIS_ALLOWED_ORIGINS=http://localhost:3000`

## admin.sqlite 与 workspace.sqlite 实际路径
- `data/admin.sqlite`
- `data/workspace.sqlite`
- 二者位于仓库 `data/` 目录，互不可见、互不可写；具体路径随 Issue 090 环境变量约定锁定。

## 如何避免共享进程只读取一个 CURIS_DB
- 关键：两个独立进程各自以不同 `CURIS_DB` 启动，而非在单进程内做动态路由。
- 每个进程启动时通过环境变量固化 `CURIS_DB`（main.py:660 已支持 `os.getenv("CURIS_DB", "data/curis.sqlite")`），进程生命周期内只读自己的库。
- 严禁在单进程内根据请求动态切换 DB 连接（本期不做动态路由）。
- `main.py` 的 CORS / 租户中间件按 `CURIS_PRODUCT` 收窄，确保进程只服务对应产品契约。

## 数据迁移和回滚方式
- 迁移：从当前共用库 `data/curis.sqlite` 按产品归属拆分，分别写入 `admin.sqlite` / `workspace.sqlite`。
  - 拆分规则：Admin 资产类（skl_/tl_/wt_/dt_/ccp_/pt_/et_ 等官方资产表）入 `admin.sqlite`；Workspace 运行态（employee_instances / department_instances / 任务 / 成果 / 凭证等运行表）入 `workspace.sqlite`。
  - 具体表级归属由本 Issue 实施阶段的高见远边界设计细化（ADR 级）。
- 回滚：
  - 迁移前对 `data/curis.sqlite` 做完整快照备份（如 `data/curis.sqlite.bak-<日期>`）。
  - 回滚 = 停止双进程、恢复快照、重启单进程（`CURIS_DB=data/curis.sqlite`）。
  - 每个 sqlite 文件独立备份，互不牵连。

## 验收负责人
- 架构边界：架构师高见远
- Admin 侧：主理人齐活林（Admin 交付总监）
- Workspace 侧：产品负责人（本席）
- 数据正确性：QA 严过关（拆分后双库一致性校验）

## 前置依赖
- 依赖 Issue 090 锁定端口（8001/8002）与环境变量命名。
- 依赖后端代码对 `CURIS_PRODUCT` / `CURIS_DB` 的读取就绪（main.py:660 已支持 CURIS_DB；CURIS_PRODUCT 收窄为新增项，属本 Issue 实施范围）。

## 当前进展
- 已新增 `deploy/curis/run-admin-backend.sh`，启动 Admin 后端 `8001`。
- 已新增 `deploy/curis/run-workspace-backend.sh`，启动 Workspace 后端 `8002`。
- 已生成 `data/admin.sqlite` 与 `data/workspace.sqlite`，均由当前活动库复制生成，作为迁移前基线。
- 两个后端实例已同时启动，`/docs` 返回 HTTP 200。
- `CURIS_PRODUCT=admin` 实例拒绝 `/api/workspace/*`，`CURIS_PRODUCT=workspace` 实例拒绝 `/api/platform/*`；健康检查和各自业务入口保持可用。
- 启动时按 `CURIS_PRODUCT` 清理另一产品私有表数据，避免数据库重启后被默认 seed 重新写回。

## 未完成
- 两个数据库已完成首轮表级数据隔离；Admin 副本无 Workspace 运行数据，Workspace 副本无 Admin 平台私有数据。
- 共享模板、租户、工具和运行契约表仍保留在两侧，作为当前兼容基线。
- 后续仍需对共享表做正式契约审查，不得直接删除。

## 执行限制
本 Issue 后续不得直接删除副本中的表；必须先完成逐表归属评审和数据迁移验证。
