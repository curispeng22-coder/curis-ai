# Workspace 租户身份、成员授权与可信网关 L2 收口

- 日期：2026-07-17
- 状态：CLOSED — L2 PASS
- 当前分支：`feat/roadmap-r1r2`
- Owner：系统交付席
- Review：安全边界席 → 质量运行席 → 产品规划席

## 结论

只完成这一条生产安全闭环：

`OIDC/JWT 可信网关 → 可信主体 → active membership → TenantContext → 租户资源作用域`

此前应用层实现已通过聚焦测试，但复核期间切换分支后实现文件不在当前树，且可信网关部署边界未成立。本 Issue 必须在固定分支恢复完整实现并补齐真实网关，不得复用跨分支测试结果宣称完成。

## 事实源

- 架构与安全契约：`reviews/20260717_workspace_tenant_identity_membership_implementation_security_boundary_review.md`
- 质量证据与阻塞：`reviews/20260717_workspace_tenant_identity_membership_implementation_review.md`
- 总负责人已批准原唯一实现 Issue；本文件恢复同一 Issue，不新增产品范围。

## 必须实现

1. 生产入口只允许受信 OIDC/JWT 网关访问 Workspace 应用。
2. 网关固定验证签名、算法、issuer、audience、exp、nbf 和 JWKS；失败一律 fail-closed。
3. 网关删除客户端提供的 `Authorization` 及所有 `X-Curis-Gateway-*`、`X-Forwarded-*`、`X-Auth-Request-*` 身份 Header，再从已验证 token 的固定 `sub` 注入最小主体字段。
4. Workspace 应用只接受内部 gateway 网络来源；应用端口不得公网可达。
5. 服务端以可信主体查询 active membership；revoked、expired、缺失或 tenant/company 不一致均拒绝。
6. `X-Tenant-Id` 只选择目标租户，不能单独授权。
7. 服务端建立 TenantContext，并对 Company、Department、Project、Employee、Workflow、Result、Usage 做租户作用域；跨租户资源按契约返回 404。
8. 本地 self-use 仅允许明确的开发/测试模式；生产启用 self-use 或缺少 gateway 配置必须拒绝启动或拒绝请求。
9. 日志不得包含 token、cookie、Authorization、client secret 或完整身份 claims。
10. membership 表采用 additive 迁移；旧数据双读只能 fail-closed，回滚不得恢复 Header-only 授权或公网直连应用端口。

## 允许修改

- `backend/app/tenant_context.py`
- `backend/app/main.py`：只允许身份中间件接入；必须保留当前未提交的 Admin token 变更
- `backend/app/database.py`
- `backend/app/identity_membership.py`
- `backend/app/resource_scope_policy.py`
- 与上述资源作用域直接相关且能说明必要性的后端文件
- `backend/tests/test_workspace_identity_membership.py`
- 直接相关的既有租户测试
- `deploy/curis/gateway/`
- `deploy/curis/workspace.env.example`
- `deploy/curis/README.md`
- `deploy/curis/release-checklist.md`
- `deploy/curis/verify-isolation.sh`
- `reviews/20260717_workspace_tenant_identity_membership_implementation_review.md`

## 禁止范围

- 不改前端、Admin 产品功能、Billing、Marketplace、Credential Vault、Workflow Runtime。
- 不实现完整 RBAC、出口白名单平台或生产审计平台。
- 不写入真实密钥、token、cookie、client secret 或生产凭据。
- 不切换分支，不覆盖 `data/sample_publish_package.md`，不丢弃当前工作区已有改动。
- 不以 TestClient、伪造 Header 或 mock 网关替代真实网络验收。

## 验收标准

### A. 应用与成员授权

- 有效 token + active membership + tenant-a：200。
- 无 token、无可信主体、无效 token：401。
- tenant-b 无 active membership、revoked、expired、双读不一致：403。
- 使用 tenant-a 身份访问 tenant-b 资源 ID：404。
- 仅提供 `X-Tenant-Id` 或伪造 `X-Curis-Gateway-*`：401。
- 生产 self-use、缺 issuer/audience/JWKS/gateway 配置：fail-closed。

### B. 真实网关网络

- 所有命令按安全契约对真实 `$GW` 执行并记录 200/401/403/404。
- `$APP` 原始端口从非受信网络不可达或拒绝。
- 网关确实剥离客户端同名 Header，身份只来自已验证 JWT。
- JWKS/issuer/audience/签名验证失败时不得直通应用。
- 网关与应用日志均通过敏感字段检查。

### C. 回归

- 聚焦测试全部通过。
- 全量回归记录通过/失败/跳过数；不得新增失败。
- 质量运行席必须在同一分支、同一修订、同一部署上独立复核。

## 交付物

- 变更文件与必要性。
- additive 迁移、双读和回滚说明。
- 聚焦与全量测试结果。
- 真实网络 200/401/403/404、应用端口隔离和 Header 剥离证据。
- 日志脱敏证据。
- 安全 Review 与质量 Review。

## 交接

系统交付席完成后必须直接交安全边界席；安全通过后交质量运行席；质量完成后回产品规划席。任何一项缺失均保持 `BLOCKED_L2`。

## 产品验收

- 安全边界席：PASS。
- 质量运行席：PASS。
- 固定分支/修订：`feat/roadmap-r1r2` @ `ab4419bf80296ef67bb29750654a8bc5c7ac828e` 加本 Issue 已验证工作树。
- 真实网络：200/401/403/404、伪造 Header 401、应用直连不可达。
- 自动测试：聚焦 6 passed；全量 599 passed / 19 failed / 0 skipped，未新增 identity/membership 失败。
- 结论：本 Issue L2 关闭；后续只进入 R1 统一运行基线，不扩展本 Issue 禁止范围。
