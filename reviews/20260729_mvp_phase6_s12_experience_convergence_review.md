# MVP Phase 6 / S12 — 体验优化与最终收敛 Review

结论：`PASS`

日期：2026-07-29

Issue：`issues/20260729_mvp_phase6_s12_experience_convergence.md`

## 交付事实

- 唯一 App 增加统一 Terra 加载与可恢复错误界面；项目、部门、执行工作台和 Task 详情避免过期请求覆盖当前页面。
- Task 详情与项目工作台在可选事实读取失败时保留核心对象；本地 self-use 执行获得可信 CEO 上下文，执行后处理失败也不会让 Task 永久停在 `RUNNING`。
- 旧 SQLite 合并工具只接受明确路径，先备份主库，再在事务内按主库优先规则幂等补齐共同字段；旧 Evolution/Lesson 记录转为可追溯 Memory。
- 五个旧库文件迁移后已从运行目录移至废纸篓，可恢复；旧 Admin 启动文件已删除，默认启动链只认 `frontend/` 与 `data/curis.sqlite`。
- 未新增依赖、产品入口、Workspace/Admin、实验服务或架构。

## 数据迁移证据

- 主库备份：`data/migration-backups/curis.sqlite.before-s12-20260729T012034016195Z.bak`。
- 首次迁移补入 `330` 条缺失记录，其中 `18` 条历史事件转为 Memory；主库同 ID/唯一默认公司记录保持不覆盖。
- 重复执行测试确认不产生重复数据；失败路径确认事务回滚并恢复备份。
- 主库 `pragma integrity_check = ok`；`pragma foreign_key_check = 0`。
- 可恢复清理目录：`/Users/yy/.Trash/Curis-legacy-db-20260729T092034`，包含根 `curis.sqlite`、`admin.sqlite`、`workspace.sqlite`、`.pre-split` 与 `.pre-r2-orphan`。

## 验证证据

- S12 聚焦后端：`8 passed`；运行稳定性与既有工作流兼容复核：`3 passed`。
- 隔离干净提交候选全量后端回归：`1143 passed, 2 skipped, 0 failed`。
- S12 Frontend 静态测试：`3 passed`；Frontend lint：`PASS`；Frontend build：`PASS`，27 个页面生成。
- 唯一启动：`CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh` 成功启动 Frontend 3001、Workspace 8002、Gateway 8080。
- 浏览器真实闭环：公司 `MVP 最终验收公司` → 部门 `MVP 交付部` → 员工 `MVP 交付负责人` → 项目 `project-755800a8-aab8-460e-b43c-8740619806cb` → 官方模型能力 → Task 执行结果 → 项目 Memory → 下一 Task 复用。
- 首个 Task：`b1919a7a-5c53-471a-ad32-8fcb5c74372b`，Context Package：`context-2b4c69ed-5b04-4a70-990a-dbab2c5e59b3`，状态 `COMPLETED`。
- 沉淀 Memory：`memory-b408beb4-e98d-4183-aaf3-eea30daa9710`，标题 `Curis MVP 最终验收闭环`。
- 下一 Task：`0a2cb2c1-baea-4662-846f-e24429057165`，Context Package：`context-513730f3-0af6-4a1c-8c4a-347365207614`，状态 `COMPLETED`；页面明确展示已检索上述 Memory。
- 浏览器执行走真实 Task、Orchestrator、Context、UsageEvent 与 ResultStore 链；结果由受控本地确定性 Provider 适配器返回，本 Review 不声明外部模型调用。
- Desktop `1440×1000`：`scrollWidth = clientWidth = 1425`；Mobile `390×844`：`scrollWidth = clientWidth = 375`。

## 变更说明

- 收口唯一前端的加载、错误、并发读取和响应式体验。
- 修复 self-use 身份与任务终态稳定性。
- 完成旧库备份、幂等迁移、完整性验证、可恢复清理及发布/回滚文档收口。

Handoff: sent to 产品规划席
