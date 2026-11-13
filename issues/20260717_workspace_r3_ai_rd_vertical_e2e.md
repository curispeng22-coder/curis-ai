# Workspace R3 AI 研发部真实纵向执行链路

- 日期：2026-07-17
- 状态：PASS — AI_RD_VERTICAL_E2E_CLOSED
- 固定分支：`feat/roadmap-r1r2`
- 前置提交：`758da525b15adff17c16a063261d8a0d487e7f3e`
- Owner：产品规划席编排剩余 Workflow 完成契约
- Review：质量运行席 → 产品规划席
- 前置：R2 已质量 PASS 并由产品验收关闭
- 当前阻塞：无（Artifact/项目状态闭环已通过）

## 七步真实执行已收口

- Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`，Run 与 7 Step 全部 `succeeded`。
- 7 个 StepResult、Execution、UsageEvent 一一对应；`final_report` 非空，6,018B。
- 真实调用总计 9,622 tokens，成本 `USD 0.01326900`，低于 `USD 0.10`。
- 六角色 binding、可信 CEO、上下文预算、模型/价格/成本/日志脱敏均成立；历史 failed Run 未改。
- 环境已停止，端口与容器全部关闭。
- Review：`reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md`，七步真实执行结论 `PASS`。
- `reviews/20260717_workspace_r3_artifact_project_status_closure_review.md` 已补齐 Artifact 与项目状态闭环，完整链路可验收。

## 目标

只用现有已批准能力，跑通一条可重复的「AI 研发部」真实纵向链路：

`实例化软件公司 → 创建研发项目 → 指定负责人和员工 → 创建目标 → 绑定能力 → 执行 Workflow / Task → 调用真实模型或工具 → 产生成果 → 记录 Token、模型和成本 → 输出项目状态与下一步建议`

本轮只证明一条链路真实闭合，不扩展第二行业、第二场景或新前端。

## 事实源

- `issues/shared/20260717_admin_r3_e2e_handoff.md`
- `issues/20260717_workspace_r2_asset_instantiation_closure.md`
- `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`
- 现有 Workspace Runtime、Workflow / Task、成果、Token 与成本接口

## 执行顺序

1. 先做能力预检：确认一个 `structured_executable` Workflow，以及一个当前已批准、已配置、非 mock/stub 的模型或工具调用路径。
2. 如果没有真实可执行路径，只回传唯一缺口并保持本 Issue BLOCKED；禁止用 mock、手写数据库行或历史结果替代。
3. 通过 Gateway 真实 HTTP，在一个测试租户内实例化 `ccp_ai_software_company`。
4. 创建一个真实研发项目，指定项目负责人和参与员工；创建一个可验收的开发目标。
5. 建立员工与 Skill / Tool、Workflow 的真实绑定，并创建 Task。
6. 自动推进 Workflow，记录每步状态；失败时验证可重试、可人工接管或给出明确失败原因，不得静默跳过。
7. 至少产生一项可打开的代码、文档或 Demo 成果，并能从项目、Task 或 StepResult 追溯。
8. 记录实际模型标识、输入/输出/总 Token、估算成本及计算依据；缺价格不得默认为“真实 0 成本”，必须明确标记成本未知并阻塞验收。
9. 输出项目当前状态、成功或失败原因、下一步建议。

## 必须提供的真实证据

- 固定分支与提交 SHA。
- 租户、Company、Department、Project、负责人、Employees、Goal、Binding、Workflow Run、Task、StepResult 的真实 ID。
- Gateway HTTP 请求链及关键状态码；无令牌 401、跨租户 403/404 仍成立。
- Workflow 每步状态、失败恢复或人工接管记录；不能只给最终状态。
- 成果文件或页面位置，以及从执行记录到成果的可追溯关系。
- 模型、Token、成本记录；数值来自实际执行记录，不得手填。
- 项目状态和下一步建议接口或页面结果。
- 聚焦测试及质量运行席的一次全量回归、真实网络 E2E Review。

## 验收标准

- 单一 AI 研发场景完整闭环，所有关键实体和执行记录可通过真实接口复查。
- 至少一个 Workflow Step 真实调用非 mock/stub 模型或工具并成功。
- 至少一项真实成果可打开、内容非空，并可追溯到 Task / StepResult。
- Token 总量大于 0，模型标识非空；成本有明确值和计算依据。
- 项目状态与下一步建议来自当前执行事实，不是静态文案。
- 无令牌、跨租户和宿主直连边界不退化。
- 全量回归不得出现 R3 新增失败。
- Review 已明确 PASS；无新增阻塞，完整链路 PASS。

## 允许修改

- 为闭合上述单一链路所必需的最少 Workspace Runtime、Workflow / Task、成果、Token / 成本代码与测试。
- 本 Issue、Review，以及 shared R3 交接状态。
- 优先复用现有接口、运行器、种子和验证命令；不新增依赖。

## 禁止范围

- 不开发前端，不新增公司类型、行业包、Marketplace、外部 Connector、Session、Memory、AI 秘书或 CEO Office 新页面。
- 不创建第二条 E2E 场景，不顺手修复既有 19 项失败。
- 不把 mock/stub、直接插库、历史截图、仅有 Task ID 当作真实闭环。
- 不新增或泄露凭据。若需要新外部凭据、出口或安全边界变更，立即交安全边界席，Issue 保持 BLOCKED。
- 不切分支，不夹带无关工作树改动。

## 预期交接

系统交付席完成后直接交质量运行席，附 SHA、完整实体链、HTTP、执行步骤、成果、Token / 模型 / 成本、项目状态、聚焦测试和已知失败。质量运行席独立重跑真实网络 E2E 与一次全量回归，更新 Review 并回产品规划席。
