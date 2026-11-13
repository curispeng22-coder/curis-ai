# Curis Workspace Now

Status: Deprecated

Updated: 2026-07-30

## Current State

- Sprint 0 项目架构收敛：`CLOSED — PASS`。
- MVP Phase 1 / S1 App Shell 与 Terra Design System：`CLOSED — PASS`。
- MVP Phase 1 / S2 Workspace 基础模型：`CLOSED — PASS`。
- Regression Stabilization：`CLOSED — PASS`。
- MVP Phase 2 / S3 AI Employee：`CLOSED — PASS`。
- MVP Phase 3 / S4 Project：`CLOSED — PASS`。
- MVP Phase 3 / S5 Task 与异步执行记录：`CLOSED — PASS`。
- MVP Phase 4 / S6 Capability Registry：`CLOSED — PASS`。
- MVP Phase 4 / S7 Model Gateway：`CLOSED — PASS`。
- MVP Phase 5 / S8 研发模板：`CLOSED — PASS`。
- MVP Phase 5 / S9 内容创作模板：`CLOSED — PASS`。
- MVP Phase 5 / S10 知识管理：`CLOSED — PASS`。
- MVP Phase 6 / S11 基础 Memory 与 Context Package：`CLOSED — PASS`。
- MVP Phase 6 / S12 体验优化与最终收敛：`CLOSED — PASS`。
- 当前 Issue：`issues/20260730_global_assistant_live_model_validation.md`。
- 当前状态：Global Assistant Live Model Chain Validation `CLOSED — PASS`。
- Security Boundary：`PASS`；产品规划席：`ACCEPT`。
- 最近 Review：`reviews/20260730_global_assistant_live_model_validation_review.md`。
- Business Department Organization Model 保持 `IMPLEMENTATION ACCEPTED / BLOCKED_L2`。
- 产品与架构基线：`docs/curis-takeover/` 的 Curis v1.0 接管文档。

## Runtime Baseline

- 唯一前端：`frontend/`。
- 唯一整套入口：`CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh`。
- 停止：`./deploy/curis/stop-local.sh`。
- 主数据库：`data/curis.sqlite`。
- API：可信网关 8080；Workspace 8002 仅容器内部。
- 实验能力：不进入默认启动链；D1 默认冻结且禁止真实执行。

## Verified

- 23/23 个 CEO Office 页面复用唯一 `TerraShell`。
- Terra `Input / Table / Modal / Drawer` 与三种业务卡片已补齐。
- 员工管理页实际采用共享卡片、抽屉和输入原语。
- Frontend lint/build 与 `git diff --check` PASS。
- Desktop / Mobile browser PASS；390×844 无横向溢出。
- S2 聚焦后端测试 2 passed。
- S2 Company / Department / Home 真实浏览器流程 PASS。
- S3 真实员工创建、职责、Capability Profile、状态编辑与组织中心同步 PASS。
- S3 Mobile 390×844：`scrollWidth = clientWidth = 390`。
- S4 真实项目创建、项目中心分组、项目工作台五视图与真实 Project Task 展示 PASS。
- S4 Mobile 390×844：项目中心和工作台均无横向溢出。
- S5 真实项目 Task 创建、员工指派、`202 + job_id`、状态轮询与真实失败展示 PASS。
- S5 Mobile 390×844：项目工作台单列布局可读，无可见横向溢出。
- S6 六类真实 Capability 注册、详情与启停 PASS；五个历史 Skill 幂等迁移并保持许可阻断。
- S6 Mobile 390×844：事实卡、操作、类型筛选与 Skill 卡片单列可读。
- S7 员工绑定模型人工选择、首选模型调用、单次默认模型回退与真实 Token/成本记录 PASS。
- S7 Mobile 390×844：`scrollWidth = clientWidth = 390`，长模型 ID 与回退事实可读。
- S8 真实 Project Task 经 Model Gateway 与 RealRD 完成代码修改、测试和 Git diff 回写 PASS。
- S8 Desktop / Mobile 390×844：六步运行、模型用量、测试与 Git diff 事实可读。
- S8 隔离干净提交候选全量后端回归：1128 passed、3 skipped、0 failed。
- S9 复用既有内容公司包完成 Project → Task → 热点依据 → 三平台文案/SVG → 复盘真实闭环。
- S9 Desktop 1440×1000 与 Mobile 390×844 无横向溢出；三张 SVG 完整加载。
- S9 隔离干净提交候选全量后端回归：1131 passed、3 skipped、0 failed。
- S10 受控本地 Markdown/Text 导入、手工资料、公司/项目筛选、基础检索与来源详情真实闭环 PASS。
- S10 Desktop 1440×1000 与 Mobile 390×844 无横向溢出。
- S10 隔离干净提交候选全量后端回归：1136 passed、2 skipped、0 failed。
- S11 用户/项目/员工 Memory 可真实创建、更新与检索；终态 Task 可由用户确认沉淀经验。
- S11 下一 Task 执行前自动生成 Context Package，并将相关 Memory/Knowledge 真实注入 Prompt。
- S11 Desktop / Mobile 390×844 无横向溢出。
- S11 隔离干净提交候选全量后端回归：1140 passed、2 skipped、0 failed。
- S12 旧库迁移补入 330 条缺失记录，主库完整性与外键检查通过；五个旧库文件已可恢复清理。
- S12 浏览器完成公司到经验沉淀及下一 Task 复用的最终闭环；Desktop/Mobile 无横向溢出。
- S12 隔离干净提交候选全量后端回归：1143 passed、2 skipped、0 failed。
- 当前 Workspace Backend 全量回归：1158 passed、2 skipped、0 failed。
- Frontend tests 49 passed；lint/build 与官方启动链 PASS。
- Local Desktop 信息架构已统一为 `CEO → 业务部门 → 员工 / 项目 → Task → 成果`；Company 保留为技术聚合根。
- 8 个历史 Project 均已归属业务部门，其中 5 个迁入 tenant/company 隔离的“待归属业务部”。
- Artifact 独立持久化并强制关联 Task；最终 Backend 全量 `1158 passed, 2 skipped`，Frontend `49 passed`、lint/build 与官方启动链 PASS。
- `ai_usage_records` 已成为 Token 与 AI 成本唯一事实源；记录追加式、tenant fail-closed，未知计量保持 `NULL`。
- Model Gateway、RealRD 与 D1 的真实出站尝试统一进入账本；Retry/Fallback 分尝试记录，旧 `usage.*` 不再重复承载 Token/成本。
- AI Usage 最终定向复验 `21 passed`；Frontend `49 passed`、lint/build 与官方启动链 PASS；Security Boundary PASS。
- 数字员工执行控制复用现有 Task、Workflow 与 `evolution_events`，支持结构化时间线、
  持久化暂停、补充信息、人工接管、转派、同 Task 恢复和取消；未新增并行 Agent、
  Session 或 Task Run 体系。
- 执行控制最终 Backend 全量 `1175 passed, 2 skipped`；Frontend `49 passed`、
  lint/build、数据库、官方启动链与 Desktop/Mobile 浏览器本地控制闭环 PASS。
- `model_called` 只引用 `usage_record_id`；Token/成本仍只查询 `ai_usage_records`，
  页面不展示 Prompt、回答、隐藏思维链、密钥或原始恢复参数。
- Global Assistant 已从 `TerraShell` 占位 Drawer 升级为根布局级 Provider / Host；
  Identity 全部由用户配置，默认不固定名称、头像、角色、语气或人格。
- Assistant 查询聚合真实 Project、Business Department、Task、Artifact、Memory 与
  AI Usage；执行指令只创建并启动现有 Task，不直接修改业务对象。
- Assistant 最终 Backend 全量 `1180 passed, 2 skipped`；Frontend `52 passed`、
  lint/build、数据库、官方启动链与 Desktop/Mobile Browser PASS。
- Global Assistant 真实固定非敏感指令已完成现有 Task / Capability / Model Gateway
  链：Task `1d634bb3-c154-4d16-98b6-b35b45eb4e8e` 为 `COMPLETED`，生成 1 个
  Artifact。
- 本次真实调用恰有 1 条 AIUsageRecord
  `usage-4ece6cc0-061b-4b96-90c9-adefcebc0686`：228 Tokens、USD
  `0.00023475` estimated、计量 confirmed；`model_called` 只引用该 ID。
- 实际运行快照 Backend 全量 `1179 passed, 3 skipped`；Frontend `59 passed`、
  lint/build PASS；真实 Browser Task 详情与 Console `0 error`。
- Key 未进入聊天、Git、数据库或日志；调用后含 Key 容器已停止，无 Key 重启保持
  fail-closed。安全边界席 PASS，质量运行席 PASS，产品规划席 ACCEPT。

## Boundaries

- 不重写产品，不改变 Curis v1.0 架构。
- 不新建 Workspace/Admin 体系。
- 旧 SQLite 已完成备份、幂等迁移与可恢复清理；后续数据变更必须另立 Issue。
- 所有 MVP 开发必须先进入独立 Issue/Task。

## Next

Global Assistant Runtime v1 及其真实模型正向链已由安全边界席、质量运行席和
产品规划席验收关闭；`BLOCKED_L2_LIVE_VALIDATION` 已解除。Local Owner 认证方案、
AI Usage 唯一事实源和既有产品架构未改变。
