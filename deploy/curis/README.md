# Curis Workspace 本地运行

R1 唯一整套本地入口：

```bash
./deploy/curis/start-local.sh
./deploy/curis/stop-local.sh
```

`start-local.sh` 复用现有 Envoy/JWKS/Workspace compose，并只启动 `frontend/`。默认前端端口为 3001，Workspace 数据库固定为 `data/curis.sqlite`。8002 仅为 Workspace 容器内部端口，宿主 API 唯一入口为 8080。

组件调试入口 `run-workspace-backend.sh` 可通过 `CURIS_WORKSPACE_ENV` 指定配置；不得作为整套基线替代命令。

前端真实目录与命令：

```bash
cd frontend && pnpm install --frozen-lockfile && pnpm build
```

后端聚焦命令：

```bash
.venv/bin/python -m pytest -q backend/tests/test_workspace_identity_membership.py backend/tests/test_product_isolation.py
```

## Workspace 生产可信网关

生产 Workspace 不直接发布 Uvicorn 端口。唯一入口是 `deploy/curis/gateway/docker-compose.yml`：Envoy 验证固定 issuer、audience、JWKS、签名、exp/nbf，并在验证前剥离客户端身份 Header；Workspace 仅位于内部 Docker 网络且只接受固定 gateway 地址。

```bash
cd deploy/curis/gateway
cp gateway.env.example .env
set -a; source .env; set +a
./render-config.sh
docker-compose config
docker-compose up --build -d
```

OIDC/JWKS 只能发布允许算法的签名公钥（模板为 RS256 部署基线）；`CURIS_IDENTITY_AUDIT_KEY` 与真实 token 必须由部署密钥注入。回滚只能恢复仍经过可信网关的上一部署，不得重新暴露 Workspace 应用端口或恢复 Header-only 授权。
