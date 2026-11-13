# FreeLLMAPI Owner-only Experimental Gateway Review

Issue: `issues/20260729_freellmapi_owner_only_experimental_gateway.md`

Baseline HEAD: `a41cacab3aef18d566351491ea9475c0c461bf13`

Status: `PASS（本地契约与回归） / BLOCKED_L2（Owner 真实调用）`

## 结论

FreeLLMAPI Owner-only Experimental Gateway 的本地代码契约、安全边界和 Workspace
回归通过：

- 实验网关首次登记只能为 `inactive`，只接受本机或容器内网 HTTP 地址；
- 只有 loopback 来源且身份与 Local Owner session 一致时，才能调用服务端固定的非敏感
  验证端点；
- 网关不会进入 Workspace 官方模型目录或 Tenant 私有模型目录；
- 真实网络失败、恶意路由元数据和 HTTP 30x 均 fail-closed，不伪装成功；
- 30x 不跟随，`Authorization` 不会被转发到重定向目标；
- Curis 只保存 `env:FREELLMAPI_API_KEY` 引用，不保存统一 Key 或上游供应商 Key；
- Sidecar Compose 仅发布 `127.0.0.1:3101`，未暴露公网；
- Backend 全量、Frontend tests/lint/build 全绿。

安全边界席已对当前实现回传 `PASS`。本轮未注入 Key、未启动或访问 FreeLLMAPI
Sidecar、未连接任何外部供应商。

真实调用继续 `BLOCKED_L2`：Owner Key、Sidecar 和上游供应商 Key 均未供应，因此
“Owner 成功调用一次 FreeLLMAPI”这一真实运行验收尚未发生。本地 fake/loopback HTTP
契约测试不能替代真实 Sidecar 调用。

## 证据

### 来源与工作树

- HEAD：`a41cacab3aef18d566351491ea9475c0c461bf13`
- 分支：`feat/roadmap-r1r2`
- 实现尚在共享工作树，相关增量：
  - `.gitignore`
  - `backend/app/main.py`
  - `backend/app/model_catalog.py`
  - `backend/app/model_gateway.py`
  - `backend/app/model_preferences.py`
  - `backend/tests/test_freellmapi_experimental_gateway.py`
  - `deploy/freellmapi/`
  - `issues/20260729_freellmapi_owner_only_experimental_gateway.md`
- 工作树另有其他 Issue 的既有改动；本 Review 未修改、暂存或归因这些文件。
- `git diff --check`：PASS。

### 聚焦测试

命令：

```text
.venv/bin/python -m pytest backend/tests/test_freellmapi_experimental_gateway.py
```

结果：

```text
6 passed, 0 failed
```

覆盖：

1. 拒绝公网 URL、link-local 地址、首次 `active` 登记和非固定凭证引用；
2. 实验网关不进入 Workspace 官方模型投影或 Tenant 私有模型；
3. Local Owner + loopback + 固定 synthetic prompt 才能验证并激活；
4. 非 Owner / 非 loopback 返回 `403 local_owner_required`；
5. 网络失败返回真实 `502`，网关保持 `inactive`；
6. Sidecar 路由元数据尝试回显 secret 时返回 `502 response_invalid`；
7. HTTP `302` 不跟随，源端收到请求，但重定向目标收到 `0` 次请求；
8. 响应、审计事件不包含 Key、固定 prompt 或模型输出正文。

测试只使用 FastAPI TestClient、内存 fake adapter 与本机临时
`ThreadingHTTPServer`，没有连接 FreeLLMAPI Sidecar 或外部服务。

### Backend 全量

命令：

```text
.venv/bin/python -m pytest backend/tests
```

这是本 Issue 唯一一次 Backend 全量回归。

结果：

```text
1170 passed, 2 skipped, 0 failed
```

耗时：`119.51s`。

### Frontend

测试命令：

```text
pnpm --dir frontend exec node --test \
  tests/mvp-p0-auth-onboarding.test.mjs \
  tests/mvp-s12-experience.test.mjs \
  app/projects/[project_id]/projectRuntimeViewModel.test.mjs \
  app/taskViewModel.test.mjs \
  app/organizationModel.test.mjs \
  app/platform/commercial/commercialConsole.test.mjs
```

结果：`49 passed, 0 failed`。

其他命令：

- `pnpm --dir frontend lint`：PASS
- `pnpm --dir frontend build`：PASS
- Next.js 静态页面：`28`

本 Issue 未新增 Workspace UI。

### Compose 与网络边界

离线解析命令：

```text
FREELLMAPI_ENV_FILE=.env.example docker-compose config --format json
```

结构化结果：

- Compose name：`curis-freellmapi-experimental`
- Image：`ghcr.io/tashfeenahmed/freellmapi:v0.6.4`
- `host_ip`：`127.0.0.1`
- Published：`3101`
- Target：`3001`
- Protocol：`tcp`
- `security_opt`：`no-new-privileges:true`
- 环境仅声明 `ENCRYPTION_KEY`、`FREELLMAPI_HOST_PORT`、`NODE_ENV`、`PORT`

仓库中只有 `.env.example` 占位值，实际 `deploy/freellmapi/.env` 不存在，且
`.gitignore` 已排除该文件。Compose 配置和生产代码没有明文统一 Key 或供应商 Key。

### 部署注入状态

仅检查是否存在，不读取任何值：

```text
HOST_KEY=ABSENT
WORKSPACE_KEY=ABSENT
SIDECAR_ENV_FILE=ABSENT
SIDECAR_CONTAINER=ABSENT
```

因此本轮没有可执行真实调用的部署前提，也没有误接入默认 Curis 启动链。

当前既有 Curis 主链只读健康检查：

- `GET http://127.0.0.1:8080/health`：`200`
- `GET http://127.0.0.1:3001/gateway/api/auth/local/status`：`200`

该结果仅证明现有 Curis 主链可达，不表示 FreeLLMAPI Sidecar 或真实模型调用通过。

### Owner-only 与 Workspace 不可见性

- 验证端点固定为：
  `POST /api/owner/experimental-gateways/freellmapi/verify`
- 必须同时满足：
  - 来源 IP 为 loopback；
  - 存在 Local Owner session；
  - trusted identity 的 role 为 `owner`；
  - trusted identity subject 与 Local Owner subject 一致。
- 独立 Admin token 不能替代 Owner 身份。
- `freellmapi.experimental` 被排除在：
  - Workspace `available_models`；
  - 官方模型 gateway reference；
  - Tenant private model capability。
- 成功验证前不能通过普通状态接口激活。

### 30x 与敏感字段

- `ModelGatewayAdapter` 使用禁止重定向的 HTTP handler。
- 离线 HTTP 测试返回 `302` 后，适配器报告
  `gateway_error / http_status=302 / outbound_attempted=true`。
- 重定向目标未收到请求，证明 `Authorization` 未跨跳转发送。
- 路由元数据必须是受限的 `provider/model` 标识；包含 Key、prompt、非法编码、
  超长或异常字符时整体拒绝。
- 返回与审计仅记录 provider、model、status、HTTP 状态、延迟和 Token；不记录
  prompt、回答、Key、Credential 或原始供应商响应。

## 阻塞项

`BLOCKED_L2 — LIVE_VALIDATION`：

1. Owner 尚未生成并注入 FreeLLMAPI 统一 Key；
2. FreeLLMAPI Sidecar 尚未启动；
3. 上游供应商 Key 尚未由 Owner 写入 Sidecar；
4. 尚未完成一次固定非敏感 prompt 的真实调用；
5. 尚未用真实运行结果验证 provider/model/status/latency/Token 与停用隔离。

这些都是 Owner 运维动作。本质量任务没有权限代注入、代启动或访问外部 Sidecar。

## 建议

1. 产品规划席可接受本地实现、安全边界和回归结果。
2. Issue 状态保持 `IMPLEMENTED / LIVE_VALIDATION_BLOCKED`，不要宣告真实调用完成。
3. Owner 完成 Key 与 localhost Sidecar 供应后，系统交付席只执行 Issue 已固定的一次
   非敏感验证和停用隔离。
4. 质量运行席届时只补真实调用与停用证据，不重复本次 Backend 全量、Frontend 或
   离线边界测试，除非相关代码发生变化。
5. 不得把 FreeLLMAPI 宣传为稳定供应商、固定免费额度或租户可用能力。

Handoff: sent to 产品规划席 / main thread；本地实现 PASS，真实 Owner 调用保持
`BLOCKED_L2`。
