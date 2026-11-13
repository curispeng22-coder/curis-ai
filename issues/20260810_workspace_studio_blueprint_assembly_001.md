# WORKSPACE-STUDIO-BLUEPRINT-ASSEMBLY-001

Status: Completed (Blueprint Draft assembly; Runtime gates open)  
Decision: `PASS_WORKSPACE_STUDIO_BLUEPRINT_ASSEMBLY_UI_WITH_RUNTIME_GATES`

## 1. 目的

把当前“选择类型 + 填写目标 + 创建 Workspace”的最小入口推进为 Blueprint 4.13 定义的
Workspace Studio 装配草案体验。CEO 必须在创建办公室前看见业务结果、阶段责任、AI 岗位、
能力供给、证据标准、失败出口和后续门禁；所有可提交配置写入现有 Runtime Workspace
Blueprint Draft，不以页面状态冒充已物化员工、Simulation PASS 或 CEO 批准。

## 2. 允许范围

- `frontend/app/ceo-office/workspace/studio/page.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应 Review、Current State 与 Change Log

不得修改 Backend、Runtime 状态机、活动数据库、旧 Project / Task 链、真实平台 API、
商业化 Admin、Desktop Packaging、Blueprint 或一级导航。

## 3. 契约

- Studio 显示 `Discover → Blueprint → Compose → Bind → Staff → Simulate → Approve → Operate`，
  但本 Issue 只保存前五步形成的 Blueprint Draft。
- Blueprint 必须包含业务结果、阶段、Role Slot、Capability、Evidence / Acceptance、外部结果来源、
  失败与人工备用路径；缺少可编辑的关键字段时 fail-closed，不允许创建。
- Role Slot 与 Capability 仅是 Blueprint 责任和供给声明，不能显示成已雇佣、已授权或正在运行的 AI 员工。
- Simulation、CEO Approve 与 Operate 必须显示为后续 Runtime 门禁；本页面不得提供伪通过动作。
- 创建仍复用现有 tenant-scoped Runtime Workspace API，不创建第二套 Studio 存储或本地草稿事实源。

## 4. 验收条件

1. RD / XHS / TTK 三种模板均显示业务阶段、责任岗位、能力与模拟场景，并写入 Blueprint Draft。
2. CEO 可编辑 Workspace 名称、目标结果、验收证据与失败 / 人工备用路径；配置检查实时阻止缺项提交。
3. 页面保持 Company OS 壳、一个主要动作、共享 Assistant 浮层和三主题语义令牌。
4. 前端聚焦测试、scoped ESLint、Next build 与 1440×900 浏览器视觉验收通过。
5. Review 明确区分 Blueprint Draft、已物化 Runtime、Simulation 和 CEO Approve。
