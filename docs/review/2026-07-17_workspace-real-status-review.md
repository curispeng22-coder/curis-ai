# 2026-07-17 Workspace 真实状态复盘

- 复盘日期：2026-07-17
- 复盘口径：只认固定提交上的文件、接口、测试和真实页面；设计稿、目录项、mock、历史口头回传不算真实可用
- 状态只使用：已真实可用、部分可用、只有设计、尚未开始

## 一、结论

Workspace 当前整体为：**部分可用**。

真正站住的是底层运行基线、租户身份边界、Company / Department 的官方资产实例化，以及一部分 Project、Employee、Workflow、Task 运行底座。R1、R2 已有固定提交和独立质量证据，合法租户可通过 Gateway 使用，跨租户访问会被拒绝。

现在还不能把它说成完整的 AI Company System。最关键的「真实模型执行 → 成果 → Token / 模型 / 成本 → 项目状态与建议」纵向闭环仍未完成。代码和自动测试已经到位，但部署环境没有注入批准凭据，所以质量席没有执行真实 OpenAI 请求，也没有用 mock 冒充成功。R3 当前只能保持阻塞。

CEO Office 也没有完成定稿验收。仓库已有 `/ceo-office` 页面，但根路径 `/` 仍是 Task-first 工作台；Phase-1C 要求的默认 CEO Office、真实核心 Project、组织健康、完整状态和多端页面验收没有对应 Review。

## 二、各模块真实状态与原因

| 模块 | 状态 | 结论和原因 | 真实证据 |
| --- | --- | --- | --- |
| Company | 已真实可用 | 官方软件公司包可以进入 Workspace 独立数据库，并通过真实 HTTP 实例化 Company；重启后资产仍存在。 | `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`；`POST /api/platform/company-packages/ccp_ai_software_company/instantiate` 为 200；Gateway `/api/ceo/overview` 为 200；固定提交 `758da525b15adff17c16a063261d8a0d487e7f3e`。 |
| Department | 已真实可用 | 公司实例化会生成真实 Department；已有部门模板回填和孤儿清理证据，未解释项为 0。 | `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`；独立实例化结果 Department 1；现有 2 个部门实例均回填有效模板。 |
| Project | 部分可用 | Project 数据、接口和租户范围已有底座，但还没有完成一次带真实模型、成果和成本的研发项目闭环。 | `docs/review/dashboard-data-readiness.md`；`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`；`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`。 |
| Employee | 部分可用 | 6 个 Persona 可查、可随公司实例化并形成 6 个 Employee；但员工运行能力、真实工具、跨项目工作状态还未闭合。 | `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`；Persona 目录 6 条、实例化 Employees 6；115 个 Tool 全部 `configured=0`、`executable=0`、`mock_or_stub=1`。 |
| 租户身份与成员授权 | 已真实可用 | 受信 Gateway、成员授权和跨租户拒绝已通过真实网络复核；客户端伪造身份 Header 无效，应用端口不能直连。 | `reviews/20260717_workspace_tenant_identity_membership_implementation_review.md`；真实 HTTP 200 / 401 / 403 / 404；`deploy/curis/verify-isolation.sh` 通过。 |
| Goal → Decision → Project → Execution 闭环 | 部分可用 | Goal、Project、Workflow、Task 和执行证据各自有部分底座；旧系统也有 evolution decision 证据，但还没有一个产品级 Decision 把 Goal、Project 和真实执行贯通。 | `reviews/006_sprint_1_ceo_readable_visualization_polish_review.md`；`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`；R3 要求的完整实体链和真实 E2E 尚未取得 PASS。 |
| 员工多项目 Session | 尚未开始 | 当前没有可验收的员工多项目 Session Issue、接口、测试或页面；R3 明确禁止顺带开发 Session。 | `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 的禁止范围。 |
| 员工上下文隔离 | 部分可用 | 租户、Project、Workflow、Capability 作用域已经有 fail-closed 自动测试；但员工在多个 Project 间切换、恢复和隔离上下文还没有真实 E2E。 | `reviews/20260717_workspace_r3_real_model_execution_gate_review.md`；项目越界在出网前返回 403；`reviews/20260717_workspace_tenant_identity_membership_implementation_review.md`。 |
| Memory | 部分可用 | 已有可追溯的 Project Memory 和 Execution Summary 文档读模型，可以减少上下文扫描；它不是员工运行时 Memory，也没有多项目会话记忆。 | `reviews/010_project_memory_first_slice_review.md`；`reviews/036_project_memory_execution_summary_review.md`；`reviews/009_project_memory_foundation_architecture_boundaries_review.md` 明确排除 Employee Memory 和运行时集成。 |
| Agent Mode | 只有设计 | 当前没有独立 Agent Mode 的运行契约、可执行 Issue、真实接口和 E2E；现有 Role Profile 不等于自主 Agent 执行模式。 | `reviews/012_sprint_3_role_profiles_first_slice_review.md`；`reviews/018_ai_task_executor_mvp_readiness_review.md` 的禁止范围仍排除 agent abstraction / multi-agent。 |
| Workflow Mode | 部分可用 | Workflow / Task 执行底座和步骤证据存在，但 R2 只有 2 个 Workflow 为 `structured_executable`，其余 16 个只是设计；真实模型步骤还未通过网络验收。 | `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`；`reviews/006_sprint_1_ceo_readable_visualization_polish_review.md`；`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`。 |
| Hybrid Mode | 尚未开始 | 没有 Agent 与 Workflow 混合调度的批准契约、Issue、接口、测试或页面证据。 | 当前唯一 R3 Issue `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 只批准单一 Workflow 纵向链路，没有 Hybrid 范围。 |
| Workflow 自动推进 | 部分可用 | 本地 Task / Workflow 可以推进并留下步骤、trace 和最终状态；但当前批准的真实模型步骤没有跑出 200，不能证明生产式自动推进闭环。 | `reviews/006_sprint_1_ceo_readable_visualization_polish_review.md`；Task 状态 `COMPLETED`、workflow / trace 各 5；`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`。 |
| Workflow 失败恢复 | 部分可用 | 已有错误、429、超限、无凭据等 fail-closed 测试，能给出明确失败；但真实 Provider 失败后的运行恢复、重放和业务级恢复尚未完成真实 E2E。 | `reviews/20260717_workspace_r3_real_model_execution_gate_review.md`；43 个聚焦测试通过，覆盖 401、403、422、429、0 重试、无 Fallback。 |
| Workflow 人工接管 | 只有设计 | R3 验收提出“可人工接管或给出明确失败原因”，但当前只有失败原因和契约，没有人工接管接口、页面和真实记录。 | `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`；当前 R3 Review 未提供人工接管证据。 |
| 成果中心：文档 | 部分可用 | 仓库已有可打开、可追溯的 Project Memory、Execution Summary 和发布文档成果；但还不是统一成果中心，也未证明来自当前真实 R3 执行。 | `reviews/010_project_memory_first_slice_review.md`；`reviews/036_project_memory_execution_summary_review.md`；`reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`。 |
| 成果中心：代码 | 部分可用 | 执行系统和代码交付本身存在，但没有在当前 R3 中完成“StepResult → 代码成果”的真实可追溯验收。 | `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 要求至少一项代码、文档或 Demo 成果；质量 Review 尚未取得该证据。 |
| 成果中心：Demo | 部分可用 | 有 Local/Demo 启停、Smoke Helper 和运行说明，但不是由项目执行自动产出的 Demo 成果中心。 | `reviews/034_local_demo_api_smoke_helper_review.md`；`reviews/032_local_demo_operator_release_notes_package_review.md`；R1 Review 的 3000 / 3100 / 8001 / 8080 运行证据。 |
| 成果中心：网站 | 尚未开始 | 没有“Workflow 产出并托管网站”的批准 Issue、运行链和验收页面。 | 当前 R3 Issue 只要求单一代码、文档或 Demo 成果，没有网站发布范围。 |
| 成果中心：视频 | 尚未开始 | 没有视频生成 Provider、存储、审计、页面和 E2E。 | 当前批准的唯一外部路径只允许 OpenAI Chat Completions；`reviews/20260717_workspace_r3_real_model_execution_security_review.md`。 |
| 成果中心：报告 | 部分可用 | 已有 meta-development report、Review 和执行摘要；但没有面向 CEO 的统一报告收件箱，也没有当前 R3 项目报告闭环。 | `reviews/002_tool_system_v1_6_meta_development_review.md`；`reviews/036_project_memory_execution_summary_review.md`；`issues/phase1c_ceo_office_ui_first_slice.md` 明确不包含 Important Reports Inbox。 |
| Token 和模型记录 | 部分可用 | UsageEvent、模型标识、Token 上限、价格和脱敏审计契约已实现并通过自动测试；真实 OpenAI 200 和真实 Token 尚未取得。 | `docs/review/dashboard-data-readiness.md`；`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`；固定实现提交 `8f426be98503a13455a6e0a5f3392cee92582246`。 |
| 项目成本 | 部分可用 | `estimated_cost` 可以按 UsageEvent 聚合，但只是估算消耗，不是账单；当前 R3 未产生真实调用成本，项目级汇总也未完成验收。 | `docs/review/dashboard-data-readiness.md`；`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`。 |
| AI 秘书 | 尚未开始 | 没有批准的 AI 秘书产品契约、入口、消息链和 E2E；R3 明确禁止顺带开发。 | `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 的禁止范围。 |
| 员工沟通入口 | 尚未开始 | 当前入口仍是 Task 编辑器，没有员工私聊、群聊、消息回执或跨项目沟通的验收链。 | 当前页面 `frontend/app/page.js`；R3 明确不扩展新前端和 AI 秘书。 |
| CEO Office 定稿与实际前端 | 部分可用 | `/ceo-office` 页面文件已存在，但 `/` 仍是 Task-first 页面；Phase-1C 要求的默认 CEO Office 尚无质量 Review，因此不能按定稿验收。 | `frontend/app/ceo-office/page.js`；`frontend/app/page.js` 仍以“任务入口 / 任务编辑器 / 任务历史”为主；`issues/phase1c_ceo_office_ui_first_slice.md`；预期 `reviews/phase1c_ceo_office_ui_first_slice_review.md` 当前不存在。 |
| Codex / WorkBuddy 团队迁移能力 | 只有设计 | 跨团队职责、Shared Issue、状态和回传规则已经形成文档，可指导人工迁移；但没有团队、线程、记忆、Issue 状态的自动迁移工具和独立验收。 | `docs/review/2026-07-17_Codex_Workspace跨团队协作与当前开发规则.md`；`docs/review/2026-07-17_WorkBuddy_Admin跨团队协作与当前开发规则.md`；`docs/team-v2/SEAT_THREAD_ROUTING.md`。 |

## 三、运行与质量基线

- 租户身份 L2：真实 Gateway 200 / 401 / 403 / 404、应用直连不可达、日志脱敏，质量结论可关闭。证据：`reviews/20260717_workspace_tenant_identity_membership_implementation_review.md`。
- R1：统一启停、四个公开入口 200、Workspace 应用端口 8002 不公开、Admin / Workspace 数据库隔离、两个前端 build 通过。固定提交：`306b9a1182d2a8a510154cdb6883009459e70728`。证据：`reviews/20260717_workspace_r1_unified_runtime_baseline_review.md`。
- R2：官方资产进入 Workspace 独立库，真实实例化 1 Company / 1 Department / 6 Employees / 6 Workflows，`unresolved=0`；聚焦 66 通过，全量 603 通过、19 个既有失败。固定提交：`758da525b15adff17c16a063261d8a0d487e7f3e`。证据：`reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`。
- R3 Gate：实现和自动测试没有新增失败；聚焦 43 通过，全量 609 通过、19 个既有失败。当前唯一阻塞是部署环境没有注入 `CURIS_MODEL_GATEWAY_API_KEY`，所以没有真实模型 200、Token、模型和成本证据。固定提交：`8f426be98503a13455a6e0a5f3392cee92582246`。证据：`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`。

## 四、建议

### 当前真正能用什么

1. 本地统一启停的 Admin、Workspace Gateway、Admin 前端和 Workspace 前端。
2. 受信 Gateway 下的租户身份、活动成员授权和跨租户隔离。
3. 官方软件公司资产的只读目录、Workspace 独立数据库消费和 Company 实例化。
4. Company、Department、Employee、Workflow Instance 的基础实体与查询。
5. 本地 Task / Workflow 执行、步骤证据、trace、Project Memory 和执行摘要。

### 最大缺口

最大缺口不是“再做更多页面”，而是还没有一条真实业务纵向闭环：真实模型调用成功后，成果、Token、模型、成本、项目状态和下一步建议必须同时可复查。当前 R3 只差批准凭据的安全注入和一次独立真实网络重验，但在这个证据出来前不能宣称闭环可用。

### 必须补齐顺序

1. 部署负责人安全注入唯一批准凭据，不在消息、文件、日志或数据库中暴露值。
2. 质量运行席只补跑一次 R3 真实网络路径，取得真实 200、Token、模型、成本和脱敏审计证据。
3. R3 Gate 通过后，系统交付席完成单一 AI 研发项目纵向 E2E；质量席独立复核成果和项目状态。
4. 纵向闭环通过后，再完成 Phase-1C CEO Office 默认首页与真实数据验收。
5. 最后再分别立项员工多项目 Session / Memory、人工接管、成果中心、AI 秘书和员工沟通，不混成一个大 Issue。

### 应暂停事项

1. 暂停第二 Provider、第二模型、Fallback、外部 Connector 和新凭据路径。
2. 暂停 Agent Mode、Hybrid Mode、多项目 Session、员工聊天和 AI 秘书实现。
3. 暂停网站、视频、Marketplace、Billing、ROI 和复杂 Dashboard。
4. 暂停继续扩充 Tool / Workflow 目录；先把一个现有 Workflow 的真实执行闭合。
5. 暂停把 `/ceo-office` 现有页面当成已定稿产品，也暂停用 mock 数据补齐 CEO 视图。

### L2 Gate事项

1. 已关闭：租户身份、成员授权、受信 Gateway、Header 剥离、应用直连拒绝和日志脱敏。
2. 当前阻塞：R3 真实模型部署凭据尚未注入；在真实 200、Token、模型、成本和审计证据完成前保持阻塞。
3. 固定批准范围：OpenAI API、`gpt-5.4-mini-2026-03-17`、现有 `ModelGatewayAdapter/newapi`、仅 `api.openai.com:443/v1/chat/completions`、60 秒、0 重试、无 Fallback、单次调用、成本硬上限 USD 0.10。
4. 任何新增 Provider、模型、出口域名、凭据来源、Connector、视频/网站发布或跨租户数据路径，都必须另开 L2 Gate，不得沿用本次批准。
