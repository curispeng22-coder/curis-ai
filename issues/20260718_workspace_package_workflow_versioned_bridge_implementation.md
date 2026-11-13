# Workspace：Package 到可执行 Workflow 的版本化桥接实施

- 状态：`CLOSED`
- 优先级：`P0`
- 发起：产品规划席
- 当前责任席：系统交付席
- 质量复核：质量运行席
- Shared 依据：`issues/shared/20260718_workspace_admin_company_package_workflow_provenance_l2.md`

## 目标

实现唯一批准的不可变版本化桥接：官方软件公司包只能精确指向一个 `structured_executable` Workflow 版本；新实例把 Package、版本、桥接和 Workflow 版本的来源快照固化到服务端记录，Run 只能从对应 Workflow Instance 继承该快照。

## 最小范围

1. Admin 受控版本化资产发布路径创建桥接关系；不修改既有包版本，不提供公开写 API。
2. 新 Company / Workflow Instance 服务端固化 `company_package_id`、`package_version`、`bridge_id`、精确 `workflow_template_id` 与版本。
3. Workspace 只读解析、实例化前校验和来源查询使用该快照；Run 从 Workflow Instance 继承，不接受请求覆盖。
4. 添加 focused tests，覆盖正向精确版本和以下拒绝：缺失、重复、版本不一致、跨租户、`revoked`、`design_only`、客户端覆盖、same-name/default/latest 推断。

## 禁止范围

- 不修改历史 `company-a`、历史 Run、Usage 或旧 Package 版本。
- 不把 `design_only` 标成可执行；不改模型、网关、成本、前端、Secretary 或 Connector。
- 不启动模型、不注入凭据、不进行真实模型调用。

## 验收标准

1. 新隔离实例可通过真实 Package / 桥接记录获得精确可执行 Workflow Instance，所有来源字段一致且不可变。
2. Run 只继承该 Workflow Instance 的来源快照，客户端输入不能改变来源。
3. 任一来源关系不可证明或状态不符合即 fail-closed；没有 partial、fallback 或 latest 推断。
4. 系统交付 focused tests 通过；质量运行席独立复跑并写 Review。
5. 本 Issue PASS 只授权进入“来源链真实模型执行 Gate”的申请，不授权模型调用本身。

## 路由

系统交付席实施 → 质量运行席独立复核 → 产品规划席收口。若需要改动身份、租户、凭据、外部服务、历史数据或既有 Package 版本，立即回 `BLOCKED_L2` 并经 Shared 队列返回总控。

## 当前质量阻塞

质量复核发现：Workflow Instance 创建后，即使对应 bridge 已 `revoked`，Run 创建仍返回 HTTP 201。`workflow_runtime` 只比对 ID、版本和 capability，没有在 Task / Run 写入前校验 bridge 的 active 状态、`revoked_at` 与 tenant 可见性。

唯一修复项已由质量席验证通过：`issues/20260718_workspace_package_workflow_bridge_revocation_failclosed_fix.md`。现重派父 Issue 静态收口；真实模型调用仍未授权。

## 收口结果

质量运行席在 `bc9b55ec` 对正向来源快照，以及 missing、duplicate、version、cross-tenant、revoked、design_only、override、name/default/latest 的 fail-closed 行为完成独立复核；focused 16 passed，compileall PASS。桥接实施收口，但不授权真实模型调用。见 `reviews/20260718_workspace_package_workflow_versioned_bridge_implementation_review.md`。
