# Workspace：软件公司包到 R3 成功 Run 的来源追溯闭环 Gate

- 状态：`BLOCKED_L2`
- 优先级：`P0`
- 发起：产品规划席
- 当前责任席：系统交付席
- 质量复核：质量运行席
- 安全复核：仅当方案涉及身份、租户、凭据、外部出站或历史数据修订时触发

## 目标

证明一条新的、隔离的真实链路：官方软件公司包 `ccp_ai_software_company` 创建出的同一家公司，能一路追溯到其 Department、Employee、Binding、Workflow、Project、Task、Run、Artifact、Token 和成本。

本 Issue 只补来源追溯断点，不扩展产品能力。

## 已知事实与断点

- R2 已证明官方包可在隔离 Workspace 库中生成 `1 Company / 1 Department / 6 Employees / 6 Workflows`。
- R3 已证明另一个 Run 可完成 7 次真实模型调用并产生报告、Token 与成本。
- 当前 `company-a` 没有可验证的 `created_from_template_id`，且成功 Run 的 `official.workflow.software_rnd_sop` 不在 `ccp_ai_software_company` 的可追溯引用内。

因此，R2 与 R3 不能合并称为同一条端到端证据。

## 当前阻塞

系统交付席只读预检确认：现有字段能够串起 Company、Department、Employee、Binding、Workflow Instance、Project、Task、Run 与 Usage；但实例化记录没有精确 Package 来源，且该 Package 的 6 个 Workflow Template 均为 `design_only`，唯一可执行的 `official.workflow.software_rnd_sop` 不在 Package 内。

总控已批准 Shared 版本化桥接方案，子 Issue 已完成质量收口。主 Issue 的剩余证据是同一新隔离实例的真实模型执行；该调用须经单独 Gate 授权，因此保持 `BLOCKED_L2`。

## 允许范围

1. 先只读核对 Company Package、Company、Workflow、实例化记录和现有关联字段，列出最小可验证路径。
2. 使用既有批准 API / 既有实例化路径创建一条新的、隔离的测试链路；不得把历史 `company-a` 或历史失败 Run 伪装成新证据。
3. 若现有字段足以表达来源，只补最小的关联、读取或测试缺口；若需要 schema、历史回填、不可逆数据修改或新外部能力，立即 `BLOCKED_L2` 并经 `issues/shared/` 回传。
4. 真实执行仅在当前 R3 的身份、租户、成本、模型、网关和受控出口边界已单独批准后进行。

## 禁止范围

- 不修改 Admin 官方资产、Package 定义、模型/Provider/Gateway、成本上限、前端、Secretary、Billing 或 Connector。
- 不对历史 `company-a`、历史成功/失败 Run 做猜测性来源回填。
- 不用同名 ID、字符串拼接、默认值、全局最近记录或人工说明代替真实关联。
- 不导出凭据、不读取密钥、不扩大租户或身份权限。

## 验收标准

只有同时满足以下条件，才可写“软件公司包 → Token/成本整链已证明”：

1. 同一 tenant 内的 Company 能追到 `ccp_ai_software_company` 和有效 Company Template。
2. 该 Company 的 Department、6 Employee、6 active Binding、Workflow Instance 都能沿真实外键/实例记录追到该 Company / Package，且无未解释引用。
3. Project、Task、Workflow Run 与实际执行的 Workflow Instance 同源；不接受 `official.workflow.*` 的独立直连作为替代证据。
4. 成功 Run 的每一步 Result、Execution、Usage、Artifact 都与该 Run 对应；Token、`price_version`、成本和最终报告可读。
5. 真实 API / 数据库 / 自动测试至少各有一项证据；跨租户或不可证明关系必须拒绝，不返回部分链路。
6. 质量运行席独立复跑后给出明确结论；如真实模型调用需要新增授权，则先停在 Gate，不得自行调用。

## 路由与交付

1. 系统交付席：先回传最小关联路径、是否需要 L2、以及可执行的最小实现/验证计划；未获该结论前不启动、不注入凭据、不调用模型。
2. 若无需 L2，系统交付席按批准范围实施并提交 focused 证据。
3. 质量运行席：独立核验来源链与真实消费，记录 Review。
4. 产品规划席：只在质量证据证明同一链路后收口；否则保持 `BLOCKED_L2` 或 `OPEN`。

## 关联证据

- `docs/review/2026-07-18_curis-joint-progress-review.md`
- `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`
- `reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md`
- `issues/shared/20260718_workspace_admin_company_package_workflow_provenance_l2.md`
- `issues/20260718_workspace_package_workflow_versioned_bridge_implementation.md`
- `issues/20260718_workspace_company_package_provenance_real_execution_gate.md`
