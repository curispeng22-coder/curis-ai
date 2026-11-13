# Shared：软件公司包到可执行 Workflow 的来源追溯 L2

- 状态：`APPROVED`
- 发起：Codex / Workspace
- 目标责任：WorkBuddy / Admin + 总控决策席
- 关联主 Issue：`issues/20260718_workspace_company_package_r3_provenance_closure_gate.md`

## 事实

- 当前运行时字段可追到 Company、Department、Employee、Binding、Workflow Instance、Project、Task、Run 与 Usage。
- 公司包 `ccp_ai_software_company` 的实例化记录没有精确 Package 来源。
- 包内 6 个 Workflow Template 全部是 `design_only`。
- 唯一已验证可执行的 `official.workflow.software_rnd_sop` 不在该 Package 内。

所以“官方软件公司包 → 可执行 Workflow → 成功 Run”的来源不能被真实关联证明。

## 已批准方案

总控已批准 Option B：新增版本化、不可变的 Package → `structured_executable` Workflow 桥接关系。

- 新实例服务端必须固化 `company_package_id`、`package_version`、`bridge_id` 与精确 Workflow 版本；
- Run 只能从 Workflow Instance 继承来源；
- Workspace 只读解析与验收；缺失、重复、版本不一致、跨租户、`revoked` 或 `design_only` 一律 fail-closed；
- 不修改历史 `company-a`、历史 Run/Usage 或既有包版本；不作 same-name、default、latest 或客户端推断；
- 不改模型、网关、成本、前端或 Secretary；不新增公开写 API；Admin 仅走受控版本化资产发布路径；
- 真实模型调用未获放行，须待来源链 focused PASS 后另立 Gate。

## 完成条件

获得唯一方案后，由 Admin 提供版本化资产证据，Workspace 以新隔离实例完成真实消费；质量席独立验证 Package、Company、Workflow、Run、Usage、Artifact、Token 与成本为同一来源链路。

实施 Issue：`issues/20260718_workspace_package_workflow_versioned_bridge_implementation.md`。
