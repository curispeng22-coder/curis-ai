# Gateway 启动失败证据保留与 Sentinel 安全 Review

- Issue：`issues/20260718_workspace_gateway_startup_evidence_preservation_gate.md`
- 结论：`PASS`（仅失败诊断安全契约；不授权真实 Key、D1 POST、模型、pytest 或外网）
- 允许修改：仅 `deploy/curis/start-local.sh`

## 允许保留的最小证据

诊断只在既有 `wait_for` 失败路径触发，且必须先保存、校验，再执行现有停止逻辑。允许字段固定为：

- `event`：`startup_failure` 或 `sentinel_health`
- `component`：`admin`、`gateway`、`workspace`、`egress`
- `phase`：`wait_for`、`sentinel`
- `http_code`：最后一次 `000`、`401`、`503`；正常健康仅允许记录 `200`
- `failure_class`：`listener_unavailable`、`auth_rejected`、`upstream_unavailable`、`process_exited`、`timeout`、`health_ok`
- `container`、`state`、`health`、`exit_code`：仅固定 Compose 服务/容器名和枚举/整数
- `line_count`、`truncated`、`redaction_status`、`timestamp`、脱敏日志文件名

`docker-compose ps` 只能保留上述结构化字段；gateway/workspace/egress 日志最多各 200 行，最多保留脱敏后的诊断行，不保留完整环境、命令行、挂载、请求体或文件内容。单行超限、字段不在白名单或脱敏扫描失败时，整份证据拒绝落盘。

## 必须拒绝或删除的内容

任何命中以下内容的行直接丢弃；无法确认是否安全时 fail-closed，不保存原文：

- `CURIS_*KEY`、`API_KEY`、`SECRET`、`TOKEN`、`PASSWORD`、`COOKIE`、`JWT`、`BEARER`、`PRIVATE_KEY`、PEM/证书块、数据库连接串；
- `Authorization`、`Cookie`、Gateway 身份 Header、完整 subject、成员 token、请求 Header、环境变量值；
- Prompt、模型原文、D1 payload、文件正文、pytest 输出原文、业务 API 响应、外部 URL/query 或完整堆栈中携带的敏感值。

日志只允许保留组件、阶段、固定 `/health` 路径、状态码、固定失败分类及必要的容器状态；不得用“先落盘再扫描”替代写前脱敏。

## 权限、长度与清理

- 诊断目录固定为既有 `.generated/runtime`，目录权限 `0700`；每个诊断文件必须为当前用户所有、普通文件、权限严格 `0600`，拒绝符号链接和路径替换。
- 每个 `ps`/组件日志文件最多 200 行；写入前先脱敏、计数和复扫，任一检查失败不保存该文件。终端只输出状态码、固定分类和安全文件名，不输出日志内容或凭据。
- 自动 `ERR` cleanup 必须保留已验证的诊断文件，不能先 `stop-local` 再丢失容器证据；正常成功启动路径不改变。
- 只有质量席确认已读取并记录证据后，才按现有清理策略删除本次明确列出的诊断文件；清理失败只报告，不扩大删除范围，不删除 pid、配置或其他 runtime 文件。

## Sentinel 边界

- Sentinel 只能使用非秘密配置和一次受控本地 `GET http://127.0.0.1:8080/health`；不读取/注入/输出真实 Key，不继承 Authorization/Cookie，不访问 D1 POST、模型、文件、pytest、前端或外网。
- 失败分类只允许 `000`（listener/连接不可达）、`401`（认证边界拒绝）、`503`（Workspace upstream 不健康）；`200` 仅表示健康，不产生任何业务副作用。
- Sentinel 请求不得携带请求体、业务 Header、租户/CEO Header 或模型配置；超时、异常、未知状态和任何额外请求均 fail-closed，并记录固定分类而非原始错误文本。

## 边界结论

本 PASS 仅批准上述失败诊断与无秘密健康重现契约，允许系统交付席在 `start-local.sh` 内实现并由质量席验证。它不恢复 D1、Provenance、Owner Key 注入或任何模型执行；实现前后均不得读取或传递凭据值。

Next Seat：产品规划席
Handoff: sent to 产品规划席
