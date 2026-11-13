# 请 Workspace 验证 Company Package 实例化消费

状态：VERIFIED/CLOSED（Workspace 已验证消费）
路径：issues/shared/20260717_admin_company_package_verify.md
发起团队：Admin
目标团队：Workspace
归属模块：Company Package → Workspace 运行态
是否阻塞：否
是否触发 L2：否

## 结论
Admin 修复公司包悬空引用（Issue 091）后，需 Workspace 证明能真实消费实例化结果（部门 / 员工 / Workflow），以闭合「可被 Workspace 实例化或绑定」完成标准条件。

## 真实证据（Admin 侧，修复后提供）
- `CompanyInstantiationService.instantiate` 产出 `department_instances` / `employee_instances` / `workflow_instances`。
- 修复后 `workflow_refs` 指向真实 `wt_*`/`official.workflow.*`，实例化工作流 > 0。

## Admin 侧修复完成（2026-07-17，Issue 091 已 CLOSED）
- `CompanyInstantiationService.instantiate` 端到端验证：`departments=1 / employees=6 / workflows=6`，`unresolved_refs` 全空。
- `workflow_refs_json` 保持 6 条 `wl_*` 且正确指向真实 `wt_*` / `official.workflow.*`（库内 `workflow_contents` 已含 6 个 `wl_*` 种子，实例化工作流 > 0，纠正了早期"wl_* 全悬空→工作流=0"的误判）。
- 同步修正：`sub_package_refs_json` 清理为 `["cp_content_ops"]`；`connector_ids` 置 `[]`（L2 冻结，外部连接器生态不自主补）；`official.employee.*` 10 行绑定补全（6 个 `software_rnd` 镜像真实 `et_*`，4 个 `content_growth` 填 persona）。
- 回滚点：`data/admin.sqlite.20260717.pre-split`。
- 现请 Workspace 按下方"需要 Workspace 完成"验证消费，验证通过状态转 VERIFIED。

## 需要 Workspace 完成
- 确认能从实例化结果拉起对应部门 / 员工 / Workflow 运行态；
- 反馈所需字段 / ID / 版本快照缺口；
- 提交消费验证结果（commit 或测试），状态转 VERIFIED。

## Admin 验收方式
- Workspace 验证通过（状态 VERIFIED）才算真正关闭；
- Admin 不直接改 Workspace Runtime / 前端。

## 禁止越界
Admin 不修改 Workspace Runtime、Task、Workflow Runtime、Employee Session 或 CEO Office 前端。

## Workspace 验证结论（2026-07-17）

- 真实 HTTP 实例化 `ccp_ai_software_company`：Company `company-eefb53b2-5adc-4321-b60d-b144257f97f4`，Department 1、Employees 6、Workflow Instances 6、Snapshots 13，`unresolved_refs` 三项全空。
- 6 个 `wl_*` 均经 `workflow_contents.workflow_template_ref` 解析到真实 `wt_*`；`sub_package_refs_json=["cp_content_ops"]`。
- `cp_content_ops.connector_ids=[]`，外部 connector 未伪造；能力包仍按 design-only 边界判定。
- 6 条 Catalog HTTP 均为 200；Workspace 侧 Admin 路由 404，跨租户 403，无令牌 401，伪造 `tenant_id` 查询参数不能改写身份租户。
- 能力态：Company Template / Persona 为已真实可用；Company Package 为实例化范围已验证；Dashboard / Tool / Workflow 为部分可用；Tool 执行为 mock/stub，16 个 `wt_*` 为 design-only；外部 Connector / `cp_content_ops` 执行为只有设计。

## 质量运行席独立消费复核（2026-07-17）

- 修订：`feat/roadmap-r1r2@8f426be98503a13455a6e0a5f3392cee92582246`。
- 可复现命令：

```text
cd backend
./.venv/bin/python -m pytest -q \
  tests/test_r2_instantiation_evidence.py::R2InstantiationEvidenceTest::test_instantiate_yields_workflow_instances_and_no_unresolved \
  tests/test_r2_instantiation_evidence.py::R2InstantiationEvidenceTest::test_workspace_db_restores_and_keeps_official_company_package \
  tests/test_v1_wave1_rd_runtime.py::test_rd_runtime_run_return_shape
```

- 结果：`3 passed / 0 failed`，0.90s。
- 消费证据：真实 `CompanyInstantiationService` 与数据库写入产出 Department 1、Employees 6、Workflow Instances 6、Snapshots 13，三类 `unresolved_refs` 全空；6 条 `wl_*` 与真实 Workflow Template 映射一致。
- Workspace 独立库在包行被清空后可由初始化恢复批准的 Company/Company Template/Capability Package，并再次实例化 1/6/6。
- 实例化后的研发部门可拉起 `RdWorkflowRuntime`，返回 `completed`、6 Steps，并生成 `wfr-*` / `wfi-rd-*` 运行 ID。该项只验证运行态消费，不把 scaffold 产物表述为真实模型执行。
- 所需字段、ID 映射和版本快照无新增缺口；结论：**VERIFIED**。
