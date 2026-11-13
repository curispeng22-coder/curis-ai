# Workspace R2 资产实例化闭合 Review

日期：2026-07-17  
验证席：质量运行席  
Issue：`issues/20260717_workspace_r2_asset_instantiation_closure.md`

## 结论

**质量 PASS；流程状态继续 BLOCKED。** 修订 `758da525b15adff17c16a063261d8a0d487e7f3e` 已让 Workspace 独立数据库仅保留批准的 Company Template、Company Package、Capability Package，并在真实 Gateway、两次重启和全量回归中通过。当前没有质量技术阻塞；R2 仅待产品规划席验收，R3 仍未授权。

## 固定基线与测试

- 分支：`feat/roadmap-r1r2`
- 首轮修订：`b85f30fb64b18cf74845dc0804f13d9bf8ce0eed`
- 修复修订：`43521be517ad89a7df49876c6b979040e0ef6855`
- Workspace 独立库修订：`758da525b15adff17c16a063261d8a0d487e7f3e`
- `git diff --check`：通过。
- 同一 R2 聚焦集：**66 passed**。
- 全量复跑：`.venv/bin/python -m pytest -q`，**603 passed / 19 failed / 0 skipped**，51.99s。
- R1 Review 固定基线为 **599 passed / 19 failed / 0 skipped**。19 项仍是既有 Admin token、`default/selfuse`、Department/Platform、vector、前端标签和 Docker Compose 插件环境失败；R2 无新增失败。

### 首轮新增的 2 项失败（已解除）

1. `test_capability_packages.py::test_t6_partial_update`：断言已与冻结事实对齐为 `connector_ids=[]`，没有恢复虚假 connector；指定用例通过。
2. `test_v1_wave1_ceo_overview.py::test_ceo_overview_returns_200`：Catalog 已兼容同租户或平台级 `Curis internal`，并新增跨租户排除断言；指定用例通过。

## `43521be` 修订历史复核（阻塞已由 `758da525` 解除）

- 同一修订重启 R1 运行环境后，Admin `8001/api/ceo/overview`：200，租户 `tenant-a` 可见 `ccp_ai_software_company`。
- 独立 Admin HTTP `GET /api/platform/capability-packages/cp_content_ops`：200；`connector_ids=[]`、`workflow_template_ids=[]`、`employee_template_ids=[]`、`status=active`；无令牌为 401。
- 当时 Workspace Gateway `8080/api/ceo/overview`：有效 member 为 200、无令牌 401、跨租户 403；但有效 member 响应的 `company_packages=[]`。
- 当时数据源核对：`quality.sqlite` 的 `company_packages` 表为 0 行。该历史阻塞已由下节 `758da525` 最终复核解除。

## Workspace 独立数据库最终复核

- 当前 Workspace `quality.sqlite`：`company_packages/company_templates/capability_packages` 均为 1 行，ID 分别为 `ccp_ai_software_company`、`ct_ai_software_company`、`cp_content_ops`；非批准行均为 0。
- 公司包依赖全部解析：Department 1、Employee 6、Workflow 6；`sub_package_refs_json=["cp_content_ops"]`。
- `cp_content_ops` 保持 `connector_ids=[]`、`workflow_template_ids=[]`、`employee_template_ids=[]`，未恢复虚假外部能力。
- 连续两次执行统一停止/启动命令后，三张表仍各 1 行；第二次重启后 Gateway CEO Overview 仍返回包 ID。
- Gateway `8080/api/ceo/overview`：合法 member 200，返回 `ccp_ai_software_company`；无令牌 401；跨租户 403。
- Gateway `8080/api/catalog/templates?type=company_template`：200，返回 `ct_ai_software_company`；宿主直连 `8002` 不可达。
- 自动测试同时覆盖新鲜库、既有空库恢复、重复初始化，以及 Workspace 内实例化 Department 1、Employees 6、Workflows 6、`unresolved_refs=0`。

## 真实 HTTP 与实例化证据

质量席在同一修订上以真实网络进程和隔离数据库副本复跑：

- Admin health：200；无 Admin 令牌：401。
- 六条只读目录均为 200，数量依次为 Company Template 1、Company Package 1、Persona 6、Dashboard 9、Tool 115、Workflow 18。
- `POST /api/platform/company-packages/ccp_ai_software_company/instantiate`：200。
- 质量租户：`r2-quality-20260717`。
- Company：`company-7e397e9f-82b7-4817-ba43-93e850225626`。
- Department：`dept-a5ec8ada-32f2-4c75-97ce-dca061bb9b13`。
- 结果：Department 1、Employees 6、Workflow Instances 6、Snapshots 13；`skill_refs/tool_refs/workflow_refs` 全为空。
- 六个 `wl_*` 均经 `workflow_contents.workflow_template_ref` 解析到对应真实 `wt_*`。
- `sub_package_refs_json=["cp_content_ops"]`；该能力包的 connector/workflow/employee 引用均为空，未伪造外部能力。

交付回传的 Company `company-eefb53b2-5adc-4321-b60d-b144257f97f4`、Department `dept-86fdcfa1-a434-46cd-9a55-69a8dfeabf6f` 可对应到交付时 HTTP 响应，但当前 R1 的 `admin.sqlite`、`curis.sqlite` 和 Workspace `quality.sqlite` 均未保留租户 `r2-closure-20260717`；因此质量席另以隔离副本生成上述独立实体证据，不把交付 ID 当成当前运行库持久化证据。

## 租户与运行边界

- Gateway Workspace Company 列表：200。
- Workspace Catalog：200。
- 无令牌：401。
- 跨租户：403。
- 跨租户 Company ID：404。
- Workspace 访问 Admin 路由：404。
- 宿主直连 Workspace `8002`：不可达。

## 孤儿与能力态

- 当前 `data/curis.sqlite`：18 个员工实例中 5 个模板可解析、13 个保留并标记 `deprecated/enabled=0`，未解释数 0。
- 2 个部门实例均已回填到有效模板，未解释数 0。
- 13 类员工运行引用和 3 类部门运行引用合计均为 0；未删除实例。
- 115 个 Tool：全部目录可见，`configured=0`、`executable=0`、`mock_or_stub=1`。
- 18 个 Workflow：2 个 `structured_executable`，16 个 `design_only`。
- 两个 shared Issue 均为 `VERIFIED/CLOSED`。

## 六条件最终判级

| 资产 | 状态 | 依据 |
|---|---|---|
| Company Template | 已真实可用 | 有真实内容、稳定 ID、GET 目录并可经公司包实例化 |
| Company Package | 部分可用 | 实例化、引用、Workspace 独立库和 Gateway 消费均成立；所引用能力包仍是 design-only |
| Persona | 已真实可用 | 6 条真实内容、稳定引用、GET 目录与员工绑定成立 |
| Dashboard | 部分可用 | 9 条目录可查，仍含冻结域内容 |
| Tool | 部分可用（目录）/只有设计（执行） | 115 条可查，但全部 mock、未配置、不可执行 |
| Workflow | 部分可用 | 2 条结构化可执行，16 条仅设计；公司包的 6 条实例化映射成立 |
| `cp_content_ops` / 外部 Connector | 只有设计 | 外部引用已清空，未配置真实连接器、凭据或执行链 |

## 最终状态与下一步

上一轮唯一技术阻塞已解除。质量结论：**PASS**。流程状态按交接约束继续 **BLOCKED**，由产品规划席验收后决定是否关闭 R2；本 Review 不授权进入 R3。

Handoff: sent to 产品规划席
