# Curis MCP / Connector Registry

Status: Review  
Updated: 2026-08-14  
Source: 当前 `MCPManifestAdapter`、`McpAdapter`、Connector Registry、MCP 官方规范/Registry 与公开厂商文档。

## 1. 产品边界

MCP 是标准工具协议；Connector 是 Curis 对外部服务连接的产品资源。一个 Connector 可以由 MCP、官方 API 或现有 Curis adapter 实现，但上层 Employee/Workspace 只消费 Capability，不按厂商品牌分支。

```text
MCP/Connector source
→ discover + source/license/security review
→ configure + authorize + health
→ Capability binding
→ Employee / Workspace Runtime
```

## 2. 协议基线

当前 MCP 规范定义的标准 transport 是 `stdio` 与 `Streamable HTTP`；Streamable HTTP 已取代旧 HTTP+SSE。HTTP 授权采用 OAuth 2.1 方向，stdio 凭据应由环境提供。实现必须遵循 [MCP transport 规范](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) 与 [authorization 规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)，并保留 Origin 校验、loopback 绑定、token 不泄露等边界。

## 3. 当前 Registry

| 类别 | 名称/来源 | Connection Method | Discovery | 当前状态 | 真实证据 | Employee bindable | Workspace usable | 下一动作 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MCP Runtime | Curis `McpAdapter` | local stdio JSON-RPC | manifest/manual | READY | 协议级 `initialize + tools/call` 最小路径；无真实外部 server 垂直 Evidence | 否，直到授权/健康/真实调用通过 | 否 | 用一个低风险本地 server 做真实闭环 |
| MCP Candidate | 5 个本地 manifest 快照 | stdio | `MCPManifestAdapter` | DISCOVERABLE | 生产线发现 5 条；未完成逐项运行、许可证和恢复验收 | 否 | 否 | 逐项审计，不批量启用 |
| Connector | AiToEarn | self-hosted HTTP，mock/real | 现有 registry | READY | 代码已有 real mode；本轮无真实外部连接 Evidence | 受现有 Capability 门禁 | 未由本轮证明 | 有目标 Workspace 时单独验证 |
| Connector | SocialAutoUpload | local/service adapter，mock/real | 现有 registry | READY | 已注册；本轮无真实发布 Evidence | 受现有 Capability 门禁 | 未由本轮证明 | 有授权测试账号时单独验证 |
| MCP Registry | Official MCP Registry | Registry API | dynamic | RESEARCHED | 官方 Registry API 可供发现；Curis 尚未接入 | 否 | 否 | 先做只读发现和逐项信任审查 |
| MCP Server | GitHub MCP Server | local/remote，OAuth/token | official source | RESEARCHED | [官方 server](https://github.com/github/github-mcp-server) 已确认；未在 Curis 授权/调用 | 否 | 否 | 有 GitHub 用例与授权后接入 |
| MCP Server | Notion MCP | Streamable HTTP + OAuth | remote hosted | RESEARCHED | [Notion 官方说明](https://developers.notion.com/guides/mcp/overview)已确认 endpoint/授权方式；未接 Curis | 否 | 否 | Streamable HTTP/OAuth 完成后验证 |
| MCP Server | Figma MCP | remote/local，OAuth | official vendor | RESEARCHED | [Figma 官方 MCP 文档](https://developers.figma-gov.com/docs/figma-mcp-server/)已确认；服务仍有访问条件 | 否 | 否 | 先完成协议层，再按账号条件验证 |
| MCP categories | filesystem、fetch、git、memory、time 等参考 server | stdio | official reference repo | RESEARCHED | [官方 reference server repo](https://github.com/modelcontextprotocol/servers)明确其用于参考而非生产即用 | 否 | 否 | 只选择必要、低权限条目做安全验证 |
| Business connectors | Email、Calendar、Drive、Slack、Notion、GitHub、Figma、Database、Browser 等 | MCP 或官方 API | catalog | RESEARCHED | 产品类别已确认；不能推断已有连接 | 否 | 否 | 按 Workspace 需求和最小权限逐项接入 |

## 4. 标准 Connector 记录

每项至少记录：`id`、vendor/source、region、transport、endpoint/command、authorization type、requested scopes、tool/resource/prompt discovery、license、version/digest、security review、configured/authorized/healthy/available、Capability mapping、真实 Evidence 与恢复动作。

`Detected != Configured != Authorized != Healthy != Available`。Registry/list/manifest 只证明可发现；不返回 credential，不把 reference server 或 mock mode 标成可用连接。

## 5. 当前缺口

- Streamable HTTP、OAuth 2.1、动态 tools/resources/prompts discovery 尚未进入 Curis MCP Runtime；
- 尚无一个真实 MCP server 完成 Employee/Workspace → Runtime → Artifact 的隔离验证；
- Official Registry 尚未成为 Curis 的只读发现源；
- 每个第三方 server 的许可证、供应链、权限、数据驻留与失败恢复都需逐项审核。

不为这些缺口创建第二套 Runtime；后续只扩展现有 `McpAdapter`/Capability/Binding 路径。Review 结论：`CAPABILITY ECOSYSTEM REVIEW REQUIRED`。
