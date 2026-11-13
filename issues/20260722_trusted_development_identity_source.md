# Trusted Development Identity Source

## Objective

以只读事实核对确认仓内或当前本地环境是否已有可复用、已批准的 OIDC/OAuth 签发或交换源，使 Project Runtime 可在不绕过 Gateway 的前提下获得可信开发身份。

## Scope

- 仅核对既有 OIDC/OAuth issuer、授权端点、JWKS、受信客户端或既有 token 交换路径的事实与证据。
- 有既有来源：返回精确来源、受信边界、所需配置和最小接入范围，供后续唯一实施单使用。
- 无既有来源：只记录“无可复用来源”，提交产品级身份基础设施选择；不得自造 JWT、BFF 自签、默认 token 或新 issuer。

## Non-goals

- 不改代码、数据、配置或部署；不启动服务、不注入密钥、不签发 token、不访问外网。
- 不伪造 Header、不关闭 Gateway、不直连 8002、不使用 Admin token 或长期凭据。

## Acceptance

1. 给出“可复用来源存在 / 不存在”的唯一结论及文件、配置或运行证据。
2. 若存在，说明 issuer、audience、签发/交换责任边界和最小接入输入；不得读取或输出密钥、token、Cookie、claims 原文。
3. 若不存在，明确不实施临时绕过，转为产品级可信 OIDC/issuer 选择。

## Route

系统交付席单主线程只读核对 → 安全边界席确认可信边界 → 产品规划席提交总控裁决。

## Conclusion

**Status: CLOSED — NO_REUSABLE_TRUSTED_SOURCE**。

当前不存在可复用且已批准的可信 OIDC/OAuth 签发或交换源。现有 Gateway 只有 JWT 验证材料，不构成客户端签发路径；本 Issue 不实施 BFF、自签 JWT、默认 token 或任何绕过。Project Runtime 页面真实操作需独立授权产品级可信身份入口。
