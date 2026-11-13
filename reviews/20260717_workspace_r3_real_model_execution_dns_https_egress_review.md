# R3 受控 DNS/HTTPS 出口架构 Review

Issue：`issues/20260717_workspace_r3_real_model_execution_gate.md`  
结论：`PASS`（仅出口架构契约；未实施、未读取凭据）。

## 唯一路径

保留现有 Provider、Model、URL 与 Adapter 不变：Workspace 使用现有 Gateway/`ModelGatewayAdapter`，HTTPS 目标仍为 `api.openai.com:443`，API 仍为 `POST /v1/chat/completions`。在现有 `workspace_internal` 网络与 edge/gateway 部署旁增加一个最小 egress 边界；Workspace 只能访问该内部 egress，不能获得通用互联网出口。

## DNS、SNI 与 allowlist

- Workspace 的外部 DNS 查询只允许递归解析 `api.openai.com`；拒绝其他域名查询、短名绕过、客户端自定义 DNS 和 IP literal 目标。
- egress 只允许目的地 TCP `443`，TLS SNI 必须精确等于 `api.openai.com`；其他 SNI、空 SNI、非 443 端口一律拒绝。
- DNS 结果只作为 `api.openai.com` 的动态地址集合使用，不写死 IP；缓存 TTL 受 DNS 响应约束，解析失败或过期无法刷新时 fail-closed。
- egress 不提供 HTTP CONNECT 的任意目标能力，不启用通用 forward proxy，不允许 `0.0.0.0/0` 或任意域名规则。
- Workspace 仍由 Adapter 固定请求 `/v1/chat/completions`；请求方法、路径和 URL 不由租户、客户端或模型选择器覆盖。egress 仅承担网络目的地边界，不能以 TLS 透传方式伪称它能看到 HTTPS path。

## 直连阻断

Workspace 容器只加入 `workspace_internal`，该网络的默认外连必须指向 egress；移除 Workspace 的公网网卡/默认直连路由，主机或容器防火墙拒绝 Workspace 到非 egress 的 `443`、任意外部 IP、任意 DNS 服务。应用容器不能通过 ingress gateway 反向利用其他路由获得互联网。

## 最少文件范围

只允许在现有部署边界增加/修改：

- `deploy/curis/gateway/docker-compose.yml`：workspace→egress 内部网络、无公网 workspace、最小健康依赖；
- `deploy/curis/gateway/egress.yaml`（或现有 Envoy 模板的等价独立配置）：DNS resolver、TCP 443、精确 SNI allowlist、deny-by-default；
- `deploy/curis/gateway/gateway.env.example`：仅非秘密的 allowlist/端口配置，不写凭据；
- `deploy/curis/gateway/render-config.sh`：生成配置时拒绝非 `api.openai.com` 的 host、非 443 端口和泛化 allowlist；
- `deploy/curis/verify-isolation.sh`：真实网络验收。

不改 Provider、Model、Adapter URL、凭据、前端、数据库、身份/scope、Fallback 或重试策略。

## 真实验收

在运行中的真实容器网络执行，不能只做静态配置扫描：

```bash
# 允许的真实调用仍由现有 R3 E2E 触发，预期 200
curl -fsS "$GW/health" >/dev/null

# egress/防火墙拒绝非批准目的地（每项应失败）
docker compose exec workspace getent hosts example.com
docker compose exec workspace curl --connect-timeout 3 -skS https://example.com/
docker compose exec workspace curl --connect-timeout 3 -skS https://1.1.1.1/
docker compose exec workspace curl --connect-timeout 3 -skS https://api.openai.com:8443/
```

验收还必须确认：`api.openai.com:443` 可解析并可建立 TLS；非批准域名/端口/SNI 失败；Workspace 无法绕过 egress；现有 Adapter 对 `/v1/chat/completions` 成功仍为 200；身份/scope 已通过的 401/403/404 语义不变。不能把网络层成功误报为模型调用成功，真实调用仍需凭据注入和 R3 审计证据。

## 回滚与 fail-closed

发布前保存 compose、egress 配置和网络规则快照。DNS 失败、SNI 不匹配、allowlist 渲染失败、egress 健康检查失败或直连阻断验证失败时禁止启动/发布；运行中异常只允许失败，不允许自动切换公网直连、备用域名、备用 Provider、Fallback 或重试。回滚只能恢复上一版同样受控的 egress 配置；若上一版没有受控出口，则保持 R3 `BLOCKED_L2`，不以旧的通用互联网路径回滚。

## Handoff

该方案满足“仅 `api.openai.com:443/v1/chat/completions`、无通用互联网、无 URL/Provider/Model 变化”的最小架构边界。已交安全边界席复核，并回传产品规划席；实施仍须系统交付按最少文件范围执行并由质量席做真实网络验收。
