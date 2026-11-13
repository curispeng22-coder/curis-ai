# macOS Keychain Owner Bootstrap → Google OIDC → Project Runtime

## Status

`PRODUCT_MISMATCH / PARTIAL` — 当前页面只能证明登录、提交、一次本地运行记录和结果面板可见；它仍是运行证据页，不是 Curis 的项目负责人工作台。不得按完成汇报。

下一唯一主线：`issues/20260723_project_owner_workbench_product_flow.md`。同一 Google OIDC → Project Runtime 主线继续收口为“用户入口 → 目标沟通 → 结构化任务确认 → AI 员工 / Workflow 执行 → 计划 / 进度 / 分工 / 成果 / 成本 / 风险 → 批准 / 返工 / 再运行”。

旧复验路径 `22bdfcf4` 不在本 Issue 验收：本 Issue 只保留 `PRODUCT_MISMATCH / PARTIAL` 与历史登录 / 首轮运行证据。其产生的 `task-169503a4` / `graph-1d3c4201e22d` 保留，不删除、不回填、不改写，并迁移到 `issues/20260723_project_owner_workbench_product_flow.md` 作为新产品切片的 next-run 继续动作候选证据。

## Security Disposition

- 直接受影响的 Gateway/Workspace 容器日志已销毁；其余相关日志隔离。禁止读取、复制、回显、导出或继续使用旧授权 code。
- 仅保留非敏感计数（Gateway 9、Workspace 8）、组件、时间窗、清理状态与 request_id 摘要。
- 待总控批准后，同一 Issue 仅修复两层 callback query logging，并以非敏感 loopback probe 验证 `CALLBACK_QUERY_REDACTED=true`。

## Parent

`issues/20260722_google_oidc_project_runtime_vertical_slice.md`

## Objective

仅在 macOS 本机自用环境实现一条真实用户动线：启动器“启用本地 Owner 绑定” → `OWNER_BINDING_READY` → Google OIDC 登录 → Project Runtime 提交目标、启动与查看状态。

## Scope

- 仅 macOS loopback / local 环境；Keychain 作为本机受信控制面，生产不得注册、读取或复用。
- 启动器提供唯一、可理解的“启用本地 Owner 绑定”动作；生成/保存一次性不透明预授权材料，不暴露 Google subject、token、code、Cookie 或 Secret。
- Google OIDC 继续使用固定 Authorization Code web-server flow 与 `openid email profile`；仅验证后的 `issuer + sub` 原子消费预授权并映射 active membership / TenantContext。
- 登录后接入既有 Project Runtime 真实保存、启动与状态读取路径。

## External Configuration Status

- `CLIENT_CREATED_SECRET_NOT_INJECTED`：Owner 已创建 Google OAuth Client；Client Secret 尚未经本机受控隐藏输入注入，且不得写入仓库、Issue、日志或聊天。

## Current Dependency

- `issues/20260722_local_project_runtime_target_provisioning.md`：经批准创建唯一隔离的 local Project Runtime 目标链；质量复核后将实际 tenant/company/ceo/project ID 固定为本 Issue 的唯一后续输入。

## Fixed Local Target

- `tenant_id`: `local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4`
- `company_id`: `local-company-076a4926-4b95-404c-a019-acf36c26108b`
- `ceo_id`: `local-ceo-660378a5-a637-45ff-b6bd-431cd36c7046`
- `project_id`: `local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8`
- `preauthorization_id`: `local-owner-preauth-589a0ce3-97cf-401b-a54b-fb745b6fe579`（已消费；存在一条 active owner membership，非本次 probe 创建）

## Non-goals

- 不建设生产 Secret Manager、多用户治理、邀请/组织系统、第二 IdP 或 Google 业务数据接入。
- 不接受首账号自动 Owner、邮箱/Header/default/Admin token 赋权、业务 API token 透传或 401 伪装完成。

## Acceptance

浏览器真实完成：

1. 用户从本机启动器启用 Owner 绑定；
2. 浏览器 Google 登录并消费一次性绑定；
3. 已绑定用户进入既有 Project Runtime；
4. 提交目标、启动运行、查看真实状态/结果；
5. 未预授权、绑定已消费、登录失败、非成员/跨租户均有可理解提示。

仅 Keychain 存在、接口存在或静态测试通过均不算验收。

## Route

系统交付席单主线程实施与 focused 验证 → 质量运行席独立完成本机浏览器真实登录/绑定/项目操作验收 → 产品收口。
