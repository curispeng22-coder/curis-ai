# Workspace Gateway 启动失败证据保留与 Sentinel 质量 Review

- Issue：`issues/20260718_workspace_gateway_startup_evidence_preservation_gate.md`
- 分支 / 修订：`feat/roadmap-r1r2` / `00c46737cbfc2c1475698252ca2c5bb347fd45b1`
- 结论：`PASS`
- 范围：只读复核脚本、保留证据与清理终态；未启动、未注 Key、未调用模型、未读写 D1 业务目标、未运行 pytest

## 独立证据

1. 修订范围仅 `deploy/curis/start-local.sh`；`bash -n` 与该修订 `git diff --check` 均通过，正常启动分支未改变其既有服务顺序。
2. Sentinel 使用本地镜像检查及 `docker-compose up --no-build`；临时 SQLite、非秘密 identity/model/audit sentinel 固定在临时目录。egress override 的 listener / cluster 均为空，不提供外部 DNS/TLS 出口。
3. Sentinel 仅有一次本地 `GET http://127.0.0.1:8080/health`；分类器仅允许 `000/401/503/200`。本次证据前缀为 `gateway-startup-20260718T143439Z-4183`，summary 精确记录 `HTTP 503 / upstream_unavailable`。
4. 容器证据显示：Gateway `running/exit 0`、egress `running/healthy/exit 0`、Workspace `exited/exit 1`。因此 listener 已到达，认证未成为本次返回路径，故障分类为 Workspace upstream 不可用。
5. `.generated/runtime` 为当前用户所有的普通目录、权限 `0700`；本前缀共 7 个普通文件，均为当前用户、权限 `0600`，每文件 7 行。Gateway 日志计数 200 且标记 truncated，Workspace 73、egress 105；全部 `redaction_status=passed`。
6. 七文件复扫未命中 Key、Secret、Token、Password、Cookie、JWT、Bearer、Private Key、Authorization 或数据库连接串；内容仅含安全 Review 批准的结构化字段，无原始日志、环境值、请求体、Prompt、文件正文或完整 subject。
7. 清理终态：`3000/3100/8001/8002/8080` 全部 `CLOSED`；Docker 只读列表未发现 Gateway、Workspace、egress 或 JWKS 容器；临时 compose override 与 sentinel data 目录均无残留。
8. `quality.sqlite` 中固定 D1 correlation 的 claim/model/tool/usage 及其他 evolution event 均为 0；对应 Workflow Run、Task、Execution、Tool trace 均为 0。

## 结论与边界

启动证据已在停止前安全保留，并把本次失败稳定分类为 `503 upstream_unavailable`：Gateway 与受控 egress 正常，Workspace 进程退出。无模型 sentinel、脱敏、权限、长度、零副作用和清理要求均满足，结论为 `PASS`。

父 D1 继续冻结；本 PASS 不授权 Owner Key、启动、D1 POST、模型调用或 pytest。本次 7 个诊断文件在质量记录完成后仍按安全契约等待受控删除，不由质量席修改。

Next Seat：产品规划席

Handoff: sent to 产品规划席
