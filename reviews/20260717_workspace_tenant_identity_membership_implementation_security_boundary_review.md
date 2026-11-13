# 生产可信网关边界补充 Review

Issue：`issues/20260717_workspace_tenant_identity_membership_implementation`
结论：BLOCKED_L2 的最小收口契约；不改代码。

## 唯一方案

生产只允许“OIDC/JWT 可信网关 → Workspace 应用”这一条入口。网关是唯一验证 OIDC/JWT 的组件；Workspace 不信任客户端身份 Header，也不把 `X-Tenant-Id` 当作身份或授权证明。

现有栈的最小实现是增加一个受控 ingress/gateway 部署层，反向代理到现有 Workspace Uvicorn 端口。应用端口只绑定内部网络/loopback，不对公网暴露。认证失败在网关终止，不能到达应用。

## Header 契约

网关在转发前必须删除客户端提供的以下 Header：

- `X-Curis-Gateway-Subject`
- `X-Curis-Gateway-Issuer`
- `X-Curis-Gateway-Auth-Time`
- `X-Forwarded-User`、`X-Forwarded-Email`、`X-Auth-Request-User`
- 客户端自带的 `Authorization`（由网关验证后不得原样转发）

网关验证通过后，只由网关重新注入最小字段：`X-Curis-Gateway-Subject`、`X-Curis-Gateway-Issuer`、`X-Curis-Gateway-Auth-Time`、`X-Curis-Gateway-Request-Id`。字段值来自已验证 token/issuer，不来自请求 Header。应用仅接受来自内部 gateway 网络的请求；直接访问应用端口必须失败或不可路由。

## OIDC/JWT 验证契约

网关必须固定 issuer、JWKS 来源和允许 audience；验证签名、`iss`、`aud`、`exp`、`nbf`（存在时）及算法白名单，拒绝未签名、过期、issuer/audience 不匹配或 JWKS 获取失败的 token。JWKS 缓存失效且无法刷新时 fail-closed。不得把任意 JWT claim 映射成主体，主体只取固定 issuer 约定的不可变 `sub`。

## 最小部署文件范围

仅允许新增/修改：

- `deploy/curis/gateway/`：gateway 配置、路由、Header 清理/注入和 OIDC/JWKS 非秘密配置模板；
- `deploy/curis/workspace.env.example`：内部监听地址及 gateway 共享边界配置名，不写秘密；
- `deploy/curis/README.md`、`release-checklist.md`：启动顺序、端口暴露和回滚说明；
- `deploy/curis/verify-isolation.sh`：真实网络验收命令。

不改应用业务代码、数据库、前端、Admin、身份系统、出口白名单或生产审计实现。OIDC client secret 只能由部署密钥注入，不能进入仓库、Header、日志或响应。

## 真实网络验收

以下命令必须针对 gateway 公网/内网地址 `$GW` 执行；Workspace 原始端口 `$APP` 不得公网可达：

```bash
curl -fsS -o /dev/null -w '%{http_code}\n' "$GW/health"                 # 200
curl -sS -o /dev/null -w '%{http_code}\n' "$GW/api/workspace/companies" # 401，无 token
curl -sS -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer invalid' "$GW/api/workspace/companies" # 401
curl -sS -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer <member-token>' -H 'X-Tenant-Id: tenant-a' "$GW/api/workspace/companies" # 200
curl -sS -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer <member-token>' -H 'X-Tenant-Id: tenant-b' "$GW/api/workspace/companies" # 403
curl -sS -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer <member-token>' "$GW/api/workspace/resources/not-found" # 404
curl -sS -o /dev/null -w '%{http_code}\n' -H 'X-Curis-Gateway-Subject: forged' -H 'X-Tenant-Id: tenant-a' "$GW/api/workspace/companies" # 401
curl -sS -o /dev/null -w '%{http_code}\n' "$APP/health" # 必须不可达/拒绝，不得绕过 gateway
```

最后一项不得以“应用自行信任 Header”通过。测试还必须确认网关访问日志和应用日志不含 token、cookie、Authorization 原文或 client secret。

## 回滚与 fail-closed

切换前保留当前部署包和 gateway 配置快照。网关配置、OIDC discovery、JWKS、issuer/audience、内部网络 ACL 或 Header 清理任一校验失败，禁止上线；运行中验证异常则返回 401/503，不能降级直通应用。回滚只能恢复上一版“仍经可信网关”的部署；不得恢复公网直连、客户端主体 Header 授权或旧 `X-Curis-Gateway-*` 直读路径。无法证明应用端口隔离时保持 BLOCKED_L2。

## Handoff

完成最小生产可信网关契约；不代表实现或生产发布通过。应直接交安全边界席复核，安全 PASS 后再由产品规划席创建/推进实现 Issue。
