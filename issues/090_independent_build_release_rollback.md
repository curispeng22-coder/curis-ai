# Issue: 独立构建、发布与回滚

## 编号
090

## Owner
系统交付席（工程师寇豆码）+ 主理人齐活林（协调）

## 协调人
主理人齐活林（Admin 交付总监）

## 状态
实施中 / 前端独立构建入口已完成

## Context
依据部署隔离方案 §3.2/3.3/3.5/3.6/3.7。当前无独立启动配置、无 .env、无 Dockerfile/compose、无 Git Tag 体系；前端单体 dev 端口 3000，后端 uvicorn 默认。需建立分别部署所需的启动命令、端口、环境变量、构建/发布目录与回滚规范。

## Objective
为 Admin 与 Workspace 各自定义独立构建、发布与回滚参数，确保互不干扰。

## Admin 启动命令和端口
- 前端：`cd frontend-admin && npm install && npm run build && npm run start -- -p 3100`（dev：`npm run dev -- -p 3100`）
- 后端进程：`cd backend && uvicorn backend.app.main:app --host 0.0.0.0 --port 8001`（详见 Issue 089）
- 端口汇总：Admin 前端 3100 / Admin 后端 8001

## Workspace 启动命令和端口
- 前端：`cd frontend-workspace && npm install && npm run build && npm run start -- -p 3000`（dev：`npm run dev -- -p 3000`）
- 后端进程：`cd backend && uvicorn backend.app.main:app --host 0.0.0.0 --port 8002`（详见 Issue 089）
- 端口汇总：Workspace 前端 3000 / Workspace 后端 8002

## 独立环境变量
| 变量 | Admin | Workspace |
|---|---|---|
| CURIS_PRODUCT | admin | workspace |
| CURIS_PORT | 3100 | 3000 |
| CURIS_DB | data/admin.sqlite | data/workspace.sqlite |
| CURIS_API_URL | http://localhost:8001 | http://localhost:8002 |
| CURIS_ALLOWED_ORIGINS | http://localhost:3100 | http://localhost:3000 |
| NODE_ENV | production / development | production / development |

- 变量通过各自 `.env.admin` / `.env.workspace`（或部署平台环境变量）注入，不共享文件。

## 独立构建目录
- Admin：`frontend-admin/.next/`
- Workspace：`frontend-workspace/.next/`
- 严禁将一方 `.next/`、node_modules/、缓存带入另一方。

## 独立发布包
- Admin 发布物：frontend-admin 构建 + 后端 Admin 契约域；独立 artifact / 容器镜像 tag `admin-v*`。
- Workspace 发布物：frontend-workspace 构建 + 后端 Workspace 契约域；独立 artifact / 容器镜像 tag `workspace-v*`。
- 禁止通过复制/覆盖互相发布；各自 CI/CD 流水线。

## Git Tag 规则
- `admin-vX.Y.Z`：Admin 前端 + 相关资产变更发布点
- `workspace-vX.Y.Z`：Workspace 前端 + 运行态变更发布点
- `backend-vX.Y.Z`：共享后端变更发布点（双产品共用）
- 标签基于对应产品分支/目录变更打标；回滚即 checkout 前序 tag 重新构建发布。

## 回滚流程
1. 前端回滚：`git checkout <product>-v<previous>` → 重新 `npm run build && npm run start`。
2. 后端回滚：`git checkout backend-v<previous>` → 重启对应进程（8001/8002）。
3. 数据库回滚：变更前对对应 `*.sqlite` 做快照；回滚 = 恢复快照（Admin/Workspace 各自独立）。
4. 配置回滚：环境变量随发布单元版本化，回滚配置即回滚发布单元。

## 验收负责人
- Admin 侧：主理人齐活林（Admin 交付总监）
- Workspace 侧：产品负责人（本席）
- 回滚演练：QA 严过关

## 前置依赖
- 无硬前置；但 Issue 088（前端拆分）与 Issue 089（后端/DB 隔离）消费本 Issue 的端口/环境变量/Tag 约定，建议本 Issue 先锁定基础约定。

## 执行限制
当前已完成：
- Admin 与 Workspace 已分别拥有独立前端目录和配置。
- Admin 默认 API 指向 `http://localhost:8001`。
- Workspace 默认 API 指向 `http://localhost:8002`。
- 两侧已分别完成 `pnpm build`。

当前未完成：
- 尚未配置真实后端 8001/8002 进程。
- 尚未创建 `admin.sqlite` / `workspace.sqlite`。
- 尚未建立 Git Tag、发布流水线和回滚演练。
