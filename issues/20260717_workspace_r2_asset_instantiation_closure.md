# Workspace R2 资产与实例化完整性收口

- 日期：2026-07-17
- 状态：CLOSED — PASS
- 固定分支：`feat/roadmap-r1r2`
- 前置提交：`306b9a1182d2a8a510154cdb6883009459e70728`
- Owner：系统交付席
- Review：质量运行席 → 产品规划席
- 前置：R1 已 PASS

## 目标

不新增资产、不扩展外部连接器，只把现有 Admin 官方资产在 Workspace 的“读取、实例化、绑定、状态标记”闭合，并按六条件真实判级。

## 事实源

- `issues/shared/20260717_admin_company_package_verify.md`
- `issues/shared/20260717_admin_orphan_instances.md`
- `docs/plan/admin-asset-completion-standard.md`
- 当前分支已包含 Admin R1/R2 提交和 6 条只读 Catalog 路由。

## 必须完成

1. Workspace 真实消费 `ccp_ai_software_company`，证明实例化产出 Company、1 Department、6 Employees、6 Workflow Instances，`unresolved_refs` 为空。
2. 验证 6 个 `wl_*` 经 `workflow_contents.workflow_template_ref` 解析到真实 `wt_*`；不再把已成立的映射误报为悬空。
3. 验证 `sub_package_refs_json` 仅保留真实 `cp_content_ops`；外部 connector 引用保持冻结/design-only，不伪造可用。
4. 处理 18 个孤儿员工和 2 个孤儿部门：先查真实运行引用；无运行引用则回填到有效模板 ID，有引用或映射不唯一则标记 deprecated，禁止删除业务数据。
5. 独立验证 Company Template、Company Package、Persona、Dashboard、Tool、Workflow 等 6 条只读 Catalog 路由可查询、租户隔离成立。
6. 验证 Tool 能力态四字段和 Workflow 能力态三状态与真实执行能力一致；mock/stub、design-only 不得标“已真实可用”。
7. 按资产六条件输出每类资产最终状态：已真实可用 / 部分可用 / 只有设计 / 尚未开始。
8. 更新两个 shared Issue：公司包验证转 VERIFIED/CLOSED；孤儿实例转 ACKNOWLEDGED→IN_PROGRESS→VERIFIED/CLOSED。

## 允许修改

- 与现有资产引用、实例化断点、孤儿实例安全回填/弃用、只读 Catalog 消费直接相关的最少后端文件和测试。
- 两个 shared Issue 状态与本 Issue Review。
- 不新增依赖；优先复用现有实例化服务、目录 API、种子和测试。

## 禁止范围

- 不新增公司类型、行业包、Marketplace、外部 connector、OAuth、真实凭据或真实计费。
- 不把 `cp_content_ops` 的外部连接器壳补成假实现。
- 不开发前端，不修改 Workflow Runtime、Session、Memory 或 R3 业务闭环。
- 不删除孤儿业务数据，不切分支，不夹带无关改动。

## 验收标准

- 公司包实例化真实结果：Company 1、Department 1、Employees 6、Workflow Instances 6、unresolved 0。
- 所有实例 template_id 可解析，或被明确标记 deprecated；未解释孤儿数为 0。
- 6 条只读 Catalog 路由均有真实 HTTP 200 及租户隔离证据。
- Tool/Workflow 状态与可执行能力一致，禁止虚假“已可用”。
- shared Issue 状态链完整。
- 系统交付席聚焦测试通过；质量运行席一次全量回归和真实 HTTP/实例化复核通过，无新增失败。
- Review 明确逐类资产状态；任一核心项缺失不得进入 R3。

## 预期交接

系统交付席完成后直接交质量运行席，附提交 SHA、实例 ID/数量、HTTP 路由、孤儿处置、状态标记、聚焦测试与 shared Issue 状态。质量运行席更新 Review 并回产品规划席。

## 产品验收

- 验收提交：`758da525b15adff17c16a063261d8a0d487e7f3e`。
- 质量 Review：`reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`，结论 PASS。
- 聚焦测试：66 passed；全量回归：603 passed / 19 failed，未新增失败。
- Workspace 独立数据库可幂等获得批准的官方公司包、公司模板和能力包；连续两次统一停启后保留，未直连 Admin 数据库。
- Gateway 真实 HTTP：CEO Overview 200 且返回 `ccp_ai_software_company`；Catalog 200；无令牌 401；跨租户 403；宿主 8002 不可达。
- 产品规划席验收通过，R2 关闭，授权进入独立 R3 Issue。
