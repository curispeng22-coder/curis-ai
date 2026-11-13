# Issue: Admin / Workspace 前端代码拆分

## 编号
088

## Owner
系统交付席（架构师高见远 + 工程师寇豆码）

## 协调人
主理人齐活林（Admin 交付总监）

## 状态
实施中 / 首步完成：已建立两个独立前端目录并保留原 `frontend/` 回滚基线

## Context
依据《Admin / Workspace 部署隔离方案》（docs/plan/admin-workspace-deployment-isolation-2026-07-17.md）与 2026-07-17 总控边界治理指令。当前前端为单体 Next.js 16 应用（frontend/），同时承载 Admin（/platform）与 Workspace（/、/ceo-office、/employees、/control）。需拆分为两个独立前端应用以实现分别部署，物理隔离构建产物与依赖。

## Objective
将单体前端拆分为 `frontend-admin/` 与 `frontend-workspace/` 两个独立 Next.js 应用，功能等价、各自独立构建与发布。

## 目录方案
- `frontend-admin/`（独立 Next.js 16 应用，仅含 Admin 资产工厂）
  - `frontend-admin/app/platform/**`（迁入自 frontend/app/platform/**）
  - `frontend-admin/app/layout.js`、`frontend-admin/app/globals.css`（提取 admin-* 样式域）
  - `frontend-admin/package.json`（next/react/react-dom/tailwind 等独立依赖树）
  - `frontend-admin/next.config.js`
- `frontend-workspace/`（独立 Next.js 16 应用，含 Workspace 运营界面）
  - `frontend-workspace/app/page.js`、`frontend-workspace/app/ceo-office/**`、`frontend-workspace/app/employees/**`、`frontend-workspace/app/control/**`
  - `frontend-workspace/app/layout.js`（根 metadata 取向 Workspace「Curis 工作台」）
  - `frontend-workspace/app/globals.css`（ceo-* 样式域）
  - `frontend-workspace/app/taskViewModel.mjs`（随 Workspace 迁入）
  - `frontend-workspace/package.json`、`next.config.js`

## 页面迁移清单
| 源路径（当前） | 目标路径 | 归属 |
|---|---|---|
| frontend/app/platform/** | frontend-admin/app/platform/** | Admin |
| frontend/app/globals.css（admin-* 部分） | frontend-admin/app/globals.css | Admin |
| frontend/app/layout.js（Admin 实例） | frontend-admin/app/layout.js | Admin |
| frontend/app/page.js | frontend-workspace/app/page.js | Workspace |
| frontend/app/ceo-office/** | frontend-workspace/app/ceo-office/** | Workspace |
| frontend/app/employees/** | frontend-workspace/app/employees/** | Workspace |
| frontend/app/control/** | frontend-workspace/app/control/** | Workspace |
| frontend/app/taskViewModel.mjs | frontend-workspace/app/taskViewModel.mjs | Workspace |
| frontend/app/globals.css（ceo-* 部分） | frontend-workspace/app/globals.css | Workspace |

## 共享组件和样式处理方式
- `globals.css` 当前混用 admin-*/ceo-* token：拆分时按产品提取各自样式域，禁止互带。
- `layout.js`：各应用独立根布局，metadata 各自取向（Admin 资产工厂 / Workspace 工作台）。
- `taskViewModel.mjs` 仅被 Workspace page.js 引用，整体随 Workspace 迁入。
- 若未来存在真正跨产品无状态通用组件（如按钮基元），应抽为独立共享包，**不在本期范围**；本期原则：各自复制最小必要样式，杜绝共享耦合。

## 迁移顺序
1. 在 `frontend-admin/` 与 `frontend-workspace/` 各初始化独立 Next.js 脚手架（package.json / next.config.js / 空 app/）。
2. 迁移 Admin 侧：platform/** + admin-* 样式 + Admin layout。
3. 迁移 Workspace 侧：page.js + ceo-office/** + employees/** + control/** + taskViewModel.mjs + ceo-* 样式 + Workspace layout。
4. 各自 `npm install` + `npm run build` 验证独立构建通过。
5. 联调各自指向共享后端（CURIS_API_URL，见 Issue 090 / 089）。

## 回滚方式
- 每步迁移对应一个 Git commit；回滚 = 切换至迁移前 commit 或 `git revert`。
- 保留原 `frontend/` 单体直至两侧独立构建均验证通过且 Issue 090 发布流程就绪，再删除原 `frontend/`（删除动作单独 PR，需双 lead 确认）。
- 前端拆分不涉及数据库，无需 DB 回滚。

## 验收负责人
- Admin 侧：主理人齐活林（Admin 交付总监）
- Workspace 侧：产品负责人（本席）
- 联合验收：两侧负责人共同确认独立构建通过、功能等价、无共享耦合残留

## 前置依赖
- 依赖 Issue 090 锁定端口、环境变量、Git Tag 与构建目录约定。
- `frontend/app/employees/page.js` 的未提交改动已由产品负责人接收为 Workspace 交接内容；拆分前仍需由交付席在独立提交中保留该改动，禁止覆盖或丢失。

## 执行限制
当前已完成：
- `frontend-admin/` 已承载 Admin `platform/**`、独立 layout 与样式。
- `frontend-workspace/` 已承载 Workspace 首页、CEO Office、员工目录、控制台和 view model。
- 原 `frontend/` 保留，未删除、未迁移覆盖。
- 两侧依赖树独立生成，未新增产品依赖。

当前未完成：
- 尚未删除或停用原 `frontend/`。
- 尚未完成 API、后端进程、数据库和发布流水线隔离。
- 尚未完成联合浏览器验收。
