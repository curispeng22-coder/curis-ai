# WORKSPACE-STAFFING-PROPOSAL-RUNTIME-001 Review

Status: Completed (proposal materialization; activation gates open)  
Decision: `PASS_WORKSPACE_STAFFING_PROPOSAL_RUNTIME_WITH_ACTIVATION_GATES`  
Date: 2026-08-10

## 1. 结论

Workspace Studio 的岗位与能力计划已从 Blueprint 字段推进为可查询、可恢复、可审计的
Runtime Proposal。保存 `STUDIO_DRAFT` 时，同一 SQLite 事务建立 `ROLE_SLOT=DRAFT`、
`AI_EMPLOYEE=PROPOSED`、`CAPABILITY_BINDING=PROPOSED` 及责任 / 能力关系；缺失 CEO
Assistant 或契约非法时，Workspace 与候选组织对象一起回滚。

本 Review 只通过候选方案物化，不授权员工、能力或 Workspace 激活。CEO Desk 与共享
Assistant 均把候选员工和已在岗员工分开；Simulation 与 CEO 明确批准仍是后续门禁。

## 2. 实际改动

- RD / XHS / TTK Studio 模板使用稳定 `requirement:*` 引用，并保存岗位所需能力关系。
- Workspace 创建事务复用现有 Runtime Foundation 表与状态机，不新增 Schema 或 Registry。
- Workspace / Company 安全投影返回岗位、候选员工、能力需求的允许字段，不返回 prompt、
  credential、secret 或原始 payload。
- CEO Desk 显示候选岗位方案，但 AI 员工数量只计算非 `PROPOSED` 员工和 CEO Assistant；
  能力统计只把 `AUTHORIZED / ACTIVE` 计为已授权。
- Assistant 简报单独提示待审查候选数量，不把候选方案伪装成在岗员工。
- 浏览器验收发现并修复 CEO Desk 窄列内候选卡被两列压缩的问题；宽屏右栏改为可读单列，
  长组织版本安全截断。

## 3. 证据

- Backend 聚焦回归：`12 passed`；Python compile：通过。
- Frontend Runtime 聚焦回归：`15 passed`；scoped ESLint：通过。
- Next production build：`44/44` 路由生成通过。
- 临时 SQLite 浏览器创建 `workspace-2dfa5760-7681-4e21-b4ee-48c3efe7fcde`，状态
  `DRAFT`；持久化 3 个 `ROLE_SLOT=DRAFT`、3 个 `AI_EMPLOYEE=PROPOSED`、4 个
  `CAPABILITY_BINDING=PROPOSED` 与 15 条 Runtime Link。
- 上述 10 个候选组织对象使用同一
  `org-workspace-2dfa5760-7681-4e21-b4ee-48c3efe7fcde-v1`；能力均为
  `PROPOSED_NOT_AUTHORIZED`，候选员工均为 `PROPOSED_NOT_HIRED`。
- API 安全投影检查未出现 `secret` 或 `prompt` 字段；事务回滚测试确认缺少 CEO Assistant
  时不遗留 Workspace 或 Proposal。
- 浏览器验证 Studio `6/6` 配置检查、候选方案提交、CEO Desk `AI 员工 1 / 候选员工 3 /
  能力需求 4 / 已授权 0`，以及 Assistant “另有 3 位候选方案待审查”。视觉证据位于
  `/tmp/curis-workspace-staffing-evidence/`。
- 临时库 `PRAGMA integrity_check = ok`；活动 `data/curis.sqlite` 未作为服务或测试目标，
  复核 SHA-256 为 `884b2adeba5a61fb3bce68ddcf6d81b1453a730fb5df8740678537fe363d7662`。
- `git diff --check`：通过。

## 4. 边界

- 未修改数据库 Schema、Runtime 状态机 / Registry、活动数据库、旧 Project / Task 链、
  真实平台 API、商业化 Admin、Desktop Packaging、Blueprint 或一级导航。
- 旧 Blueprint 不自动生成候选组织；仅显式 `lifecycleMode=STUDIO_DRAFT` 且契约完整时物化。
- 未提供授权、雇佣、上线或自动批准命令；没有 Simulation PASS 或真实外部结果。
- 本轮只使用临时 SQLite 做浏览器写入；无 stage、commit 或 push。

## 5. 未关闭事项

1. 独立 Issue 建立隔离 Simulation，并验证岗位缺席、能力未授权、执行失败与恢复路径。
2. Simulation 通过后，由 CEO 明确批准 Role Slot、AI Employee、Capability Binding 与
   Workspace 激活；失败时保持可回滚。
3. 为 Blueprint Revision / Version Diff / Impact Map 建立组织与 Simulation 失效传播。
4. 当前源码尚未重打包进新鲜 Curis.app；Desktop 分发门保持开放。
