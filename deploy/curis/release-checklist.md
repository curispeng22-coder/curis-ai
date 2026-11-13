# Curis Workspace 发布检查清单

## 本地隔离基线

- Workspace 前端：3001
- Workspace 后端：8002，`data/curis.sqlite`
- Gateway：8080；Workspace 8002 仅内部网络，不发布宿主端口
- 唯一整套启动/停止：`deploy/curis/start-local.sh` / `deploy/curis/stop-local.sh`
- 唯一活动数据库：`data/curis.sqlite`；旧 Admin/Workspace/根数据库已迁移清理

## 发布前必须通过

- `frontend` 构建通过
- `deploy/curis/verify-isolation.sh` 通过
- Workspace 不可访问 `/api/platform/*`
- 数据库快照已生成
- 未把 `.next/`、`node_modules/`、`.env` 或 SQLite 文件放入发布包
- Envoy OIDC issuer、audience、JWKS 与允许算法已固定，配置校验通过
- 客户端 `Authorization`、`X-Curis-Gateway-*`、`X-Forwarded-*`、`X-Auth-Request-*` 已在验证/转发边界剥离
- Workspace 容器无宿主机端口，仅 gateway 位于外部网络
- `CURIS_L2_VERIFY=1 deploy/curis/verify-isolation.sh` 的 200/401/403/404 与直连拒绝通过
- gateway/Workspace 日志敏感字段扫描通过

## 当前未建立

- Git Tag
- CI/CD 流水线
- 生产域名和部署平台
- 正式回滚演练
