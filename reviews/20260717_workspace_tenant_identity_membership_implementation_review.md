# Workspace 租户身份与成员授权最小实现 Review

日期：2026-07-17
验证席：质量运行席
Issue：`issues/20260717_workspace_tenant_identity_membership_implementation.md`

## 结论

**PASS。** 固定分支、固定修订上的聚焦、全量回归、真实 Gateway 网络隔离、生产 fail-closed 和日志脱敏均已独立复核；本 Issue 的 L2 可以关闭。

## 独立测试结果

- 聚焦命令：`./.venv/bin/python -m pytest -q tests/test_workspace_identity_membership.py`
- 聚焦结果：**6 passed**。
- 全量命令：`./.venv/bin/python -m pytest -q`
- 全量结果：**596 passed / 15 failed / 0 skipped**，51.60s。
- 15 项失败未新增：仍为旧 `default`/`selfuse` 断言与校验、旧 vector 范围检查、前端禁改标签，以及本机缺少 `docker compose` 插件。

## HTTP 与生产模式证据

- 聚焦测试覆盖并通过：合法 membership 访问 200、仅 tenant header 无可信身份 401、非成员 tenant 403、跨租户 Company ID 404。
- revoked、expired、双读不一致均返回 403。
- 生产 Workspace 配置拒绝 self-use；TenantContext 的 subject、tenant、company、role、membership 状态可作用域恢复；日志脱敏断言通过。
- 但上述 HTTP 状态来自可执行 TestClient，不是受信网关后的真实网络部署证据。
- 生产主体仍由应用读取 `X-Curis-Gateway-Subject`、`X-Curis-Gateway-Issuer`、`X-Curis-Gateway-Secret`。缺少边缘层剥离客户端同名 Header、网关注入签名身份、应用端只接受受信网络来源的部署证据。

## 独立复核中断证据

复核开始时工作区位于 `feat/093-readonly-catalog-routes`，Issue、实现文件和测试文件存在；完成聚焦及全量测试后，工作区被外部切换到 `feat/roadmap-r1r2`，上述 Issue、实现和测试文件消失。因此无法在同一修订上继续完成真实网络 HTTP 与生产日志复核。本 Review 保留已完成的独立测试结果，不把跨修订状态混写为通过。

## 最终状态与唯一下一步

状态：**BLOCKED_L2**。

唯一下一步：在固定修订和固定 checkout 上提供受信网关部署，证明客户端同名身份 Header 被剥离、身份只由网关注入且应用仅接受受信来源；随后质量运行席重跑真实网络 200/401/403/404、生产 fail-closed 和日志脱敏。

Handoff: sent to 产品规划席

## 最终独立质量复核

- 分支：`feat/roadmap-r1r2`
- 修订：`ab4419bf80296ef67bb29750654a8bc5c7ac828e`
- 聚焦：`tests/test_workspace_identity_membership.py`，**6 passed**。
- 全量：**599 passed / 19 failed / 0 skipped**，53.31s。
- 19 项与交付席固定分支基线数量一致，没有身份/membership 新增失败；包括旧 tenant 断言/校验、旧 Department/Platform、Admin token、前端标签、vector 范围和 Docker Compose 插件失败。
- Envoy `.generated/envoy.yaml` 使用官方镜像执行 `--mode validate`：配置有效。
- 静态网络边界成立：Gateway 只映射 `127.0.0.1:8080`；Workspace 仅 `expose: 8002`，只加入 `workspace_internal`；该网络标记 `internal: true`；可信来源固定为 `172.30.0.2/32`。
- Header 清理顺序成立：先删除客户端 `X-Curis-Gateway-*`、`X-Auth-Request-*` 和转发 Header，再由 `jwt_authn` 从已验证 JWT 注入 subject/issuer/auth_time，随后删除 `Authorization`。
- 聚焦测试证明生产 self-use/缺网关配置 fail-closed、非可信 CIDR 伪造 Header 返回 401、日志不含原始 subject/token/cookie。

真实 Gateway 环境现已由质量席独立复现，原环境阻塞解除。

最终状态：**PASS，L2 可关闭。**

下一步：产品规划席按本 Review 关闭本 Issue 的 L2；不扩大到本 Issue 明确禁止的出口白名单平台或生产审计平台。

Handoff: sent to 产品规划席

## 固定环境真实 Gateway 复核

- 分支：`feat/roadmap-r1r2`
- 修订：`ab4419bf80296ef67bb29750654a8bc5c7ac828e`
- `quality.env` 权限：`0600`；消息和 Review 未记录 token。
- 仓库现有 `deploy/curis/verify-isolation.sh`：**PASS**。
- 真实 HTTP：Gateway health 200；无 token 401；无效 token 401；伪造 Gateway Header 401；有效 member 200；nonmember tenant 403；跨租户 Company `company-b` 404；应用直连 `127.0.0.1:18002` 不可达。
- 网络：Gateway 仅映射 `127.0.0.1:8080`；Workspace `8002/tcp` 无宿主端口，仅加入 `gateway_workspace_internal`；JWKS fixture 仅加入 `gateway_edge`。
- 日志脱敏：Gateway 与 Workspace 日志未出现短期 member token、完整 subject `quality-member-sub` 或测试 Cookie 标记。
- 自动测试沿用同一分支/修订的独立结果：聚焦 6 passed；全量 599 passed / 19 failed / 0 skipped。19 项与交付基线一致，未新增 identity/membership 失败。
- `git diff --check`：通过。

质量结论：**PASS；L2 可关闭。**

Handoff: sent to 产品规划席
