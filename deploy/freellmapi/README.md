# FreeLLMAPI Owner-only Experimental Gateway

Issue：`issues/20260729_freellmapi_owner_only_experimental_gateway.md`。
这是独立、可停用的 Owner 本地实验 Sidecar，不进入 Workspace 模型目录。

## 一句话
FreeLLMAPI 使用官方镜像 `ghcr.io/tashfeenahmed/freellmapi:v0.6.4`，
仅发布到 `127.0.0.1:3101`。Curis 只保存
`env:FREELLMAPI_API_KEY` 引用，不保存统一 Key 或上游供应商 Key。

## 三条安全红线
1. **只走非敏感数据**：绝不发客户 / 隐私 / 生产关键内容流经此网关（提示词会转发到实际路由的上游供应商）。
2. **只绑内网**：FreeLLMAPI 的 Dashboard / 统一 Key / `/v1` 只映射 `127.0.0.1` 或容器内部网络，**绝不暴露公网**。
3. **密钥隔离**：FreeLLMAPI 统一 Key → Curis 的 `FREELLMAPI_API_KEY`；上游供应商 Key → 只存 FreeLLMAPI Sidecar，Curis 永不接触。

## 1. 启动 Sidecar

```bash
cd deploy/freellmapi
cp .env.example .env
openssl rand -hex 32
# 将输出写入本地 .env 的 ENCRYPTION_KEY；不要提交或粘贴到 Issue/日志
chmod 600 .env
docker-compose pull
docker-compose up -d
docker-compose ps
```

只允许 Compose 中的 `127.0.0.1:3101:3001`；不得改成 `0.0.0.0`。
在本机 Dashboard `http://127.0.0.1:3101` 添加 Owner 自有上游 Key。
这些 Key 由 FreeLLMAPI 加密保存在它自己的 Sidecar 数据卷，Curis 不读取。

## 2. 注入 Curis 统一 Key

从本机 Dashboard 复制统一 Key，仅写入 Curis Workspace Backend 的运行环境：

```text
FREELLMAPI_API_KEY=<Owner 本机统一 Key>
```

不得写入仓库、数据库、Issue、日志或前端。

## 3. 在 Curis Admin 登记

首次登记必须为 `inactive`，且只允许本机/容器内网 URL：

   ```bash
   curl -X POST http://<curis-admin>/api/platform/gateways \
     -H "Authorization: Bearer ${CURIS_PLATFORM_ADMIN_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "gateway_id": "freellmapi.experimental",
       "name": "FreeLLMAPI Experimental",
       "type": "newapi",
       "base_url": "http://127.0.0.1:3101",
       "credential_ref": "env:FREELLMAPI_API_KEY",
       "default_model": "auto",
       "status": "inactive"
     }'
   ```

## 4. Owner-local 验证并启用

验证端点只接受本地 Owner session 和 loopback 来源。它使用服务端固定的非敏感
synthetic prompt；返回 provider、model、状态、延迟与 Token，不返回 prompt、回答或 Key。
成功后该网关才会变为 `active`。

```bash
cookie_jar="$(mktemp)"
trap 'rm -f "$cookie_jar"' EXIT
curl -sS -c "$cookie_jar" -X POST http://127.0.0.1:8000/api/auth/local/session
curl -sS -b "$cookie_jar" -X POST \
  http://127.0.0.1:8000/api/owner/experimental-gateways/freellmapi/verify
```

该验证是审计事件，不进入业务 Token/成本聚合。

## 5. 停用

```bash
curl -X PUT http://<curis-admin>/api/platform/gateways/freellmapi.experimental \
  -H "Authorization: Bearer ${CURIS_PLATFORM_ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"action":"disable"}'
docker-compose down
```

数据卷默认保留；`docker-compose down -v` 会删除 Sidecar 数据与加密 Key 记录，不属于常规停用。

## 阻塞项速查
| 阻塞 | 谁处理 |
|---|---|
| 生成 Sidecar `ENCRYPTION_KEY` | Owner 本机 |
| 添加上游供应商 Key | Owner 在本机 Sidecar |
| 注入 `FREELLMAPI_API_KEY` | Owner 写入 Workspace Backend env |
| 执行一次真实验证 | Owner-local session |
