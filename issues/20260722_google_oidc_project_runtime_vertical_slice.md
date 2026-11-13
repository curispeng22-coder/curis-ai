# Google Workspace OIDC → Project Runtime 可操作纵向切片

## Objective

以 Google 个人账号 OIDC（External / Testing）作为唯一可信登录源，让经受控成员绑定的用户通过浏览器登录后进入既有 Company / Department / Project，并在同一条用户动线中提交目标、启动运行与查看状态。

## Product Acceptance

1. 用户点击“使用 Google Workspace 登录”。
2. 仅已完成受控 active membership 绑定的用户可进入既有 Company / Department / Project。
3. 用户可提交目标、启动运行并查看真实状态/结果。
4. 登录失败、非成员、租户拒绝或权限拒绝均有清楚且可处理的提示。
5. 401 拒绝态、mock、假页面交互不算完成。

## Fixed Protocol

- Google OIDC Authorization Code web-server flow。
- 最小 scope：`openid email profile`。
- 服务端验证 issuer、audience、签名、expiry、nonce、state。
- 仅验证后的 `issuer + sub` 可映射 active membership 与 TenantContext；禁止按邮箱、域名、客户端 Header 或默认主体自动赋权。
- 不接受客户端 tenant/company/ceo/role Header；Google access token 不得交给业务 API；token 不得持久化进业务对象。

## First-Phase Deliverables

交付与安全并行固化，不实施扩展：

1. 精确 callback URL、登录/登出/失败回跳与本地/生产边界；
2. 用户一次性配置清单（Google Cloud OAuth External / Testing Web client、授权重定向 URI、部署秘密注入位置）；
3. verified `issuer + sub` → active membership / TenantContext 的唯一映射、首次浏览器受控成员绑定与 fail-closed 行为；
4. 现有 Project Runtime 入口、真实保存/启动/状态 API 的最小接入点。
5. 首次 Owner 激活：一次性预授权如何显式生成、仅在浏览器动线中消费，以及用户最终需要完成的唯一动作；不得暴露 Google subject 或要求终端/curl/数据库操作。

首次 Owner 激活实施单：`issues/20260722_google_oidc_owner_pre_authorization.md`。

## Boundaries

- 同一主 Issue 内按单主执行线推进，禁止拆成“登录链”与“页面链”。
- 不新增第二身份提供方、默认身份、Header 回退、客户端 token 透传、Admin token 或临时自签方案。
- 不请求 Google 业务数据；生产发布、Google 验证与多用户治理不在本切片预建。
- RealRD 单次取证、Key 准备和容器改造保持暂停。

## Route

系统交付席固化既有接入点与 callback/config 清单；安全边界席固化 Google OIDC 信任边界；产品规划席合并为唯一可实施范围，再交总控确认。
