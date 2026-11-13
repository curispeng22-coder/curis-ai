# AiToEarn 自托管部署（Wave 2 · D1）

来源：[github.com/yikart/AiToEarn](https://github.com/yikart/AiToEarn)（MIT，v2.4，~18.8k★）。

Curis 仅取其**生成地基**（Create / Publish 规划 / Engage 分析）作为内部微服务，
**不碰 Relay、不接任何 aitoearn 在线服务**（ToS §5.1 禁转授权，白标违法）。

## 部署步骤

```bash
# 1) 拉取上游（真实仓库不进提交，已在 .gitignore 忽略 ./aiToEarn）
git clone https://github.com/yikart/AiToEarn.git ./aiToEarn

# 2) 配置环境变量（占位符 → 真实自有 key，禁止提交）
cp .env.example .env
#   编辑 .env：填入 OPENAI/ANTHROPIC/GEMINI 自有 key；RELAY 一律留空

# 3) 去品牌（可选但推荐）：应用 ./debrand.patch 覆盖前端品牌资源
#   cd ./aiToEarn && git apply ../debrand.patch

# 4) 起服务（仅生成地基）
docker compose up -d

# 5) 验证内部生成 API
curl -X POST http://localhost:8080/api/create \
  -H "Authorization: Bearer $AITOEARN_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"春季护肤选题","platforms":["xhs","douyin"]}'
```

## Curis 侧对接

`backend/app/connectors/aitoearn_client.py` 在 `CURIS_CONNECTOR_MODE=real` 且
`AITOEARN_URL=http://localhost:8080` 时，经内网 POST `/api/create` 调用本服务；
自有 AI key 由 Curis Vault 解析后仅注入请求头，**绝不落库、绝不转发 Relay**。

## 资源不足降级

完整上游含 Mongo/Redis/RustFS 等重依赖。资源有限时可仅运行生成/规划模块
（已用 `profiles: [generate]` 隔离），把 `docker-compose.yml` 的 Mongo/Redis 服务
注释掉即可；Curis 侧 connector 仍走 `/api/create`，不受影响。

## 合规红线（不可逾越）

- ❌ 不配置任何 Relay / aitoearn 在线服务费。
- ❌ 不以白标方式把 Relay 提供给任何第三方。
- ✅ AI key 仅用我们自有；.env 真实值不进 git（见 .gitignore）。
