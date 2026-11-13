# Workspace 镜像 Pin、一次受控在线构建与构建后 Sentinel

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 安全依据：`reviews/20260719_workspace_startup_failure_single_sentinel_diagnostic_review.md`
- 父链：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（保持冻结）

## 唯一目标

只把现有两条镜像引用固定为已核验 digest，执行一次受控在线 Workspace build；构建成功后仅对新镜像执行一次启动、`GET /health` 与 cleanup，并交质量复核。

## 精确修改

- `deploy/curis/gateway/Dockerfile.workspace`：`python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6`
- `deploy/curis/gateway/docker-compose.yml`：`envoyproxy/envoy:v1.31-latest@sha256:caa5b411be1633b90023592a34a7e010c933d6e60206c758f631485e53006865`

## 允许来源

仅 `auth.docker.io`、`registry-1.docker.io`、`pypi.org`、`files.pythonhosted.org`。

## 禁止范围

禁止 Key、模型、D1、pytest、业务请求、其他域名、其他镜像、其他包源和任何重试。构建失败即停并回传固定失败类别；不得 pull 其他内容。

## 验收

1. 仅两条镜像引用被 pin；
2. 一次在线 build 仅使用允许来源；
3. 成功后仅一次新镜像启动、`GET /health`、cleanup；
4. 质量独立确认来源、image_id、Cmd / Entrypoint、allowlist 分类和零 Key / 模型 / D1 / pytest / 业务请求；
5. D1 仍冻结，除非得到可采信启动分类。

## 收口结果

质量确认 `4d04cffa`：两条 digest、四个允许域名、唯一在线 build、image / Cmd / Entrypoint、cleanup 与全部禁止项均通过。构建后唯一 sentinel 返回 `503`，可采信分类为 `create_app_failed`。本 Issue 已完成；D1 仍冻结，后续仅在额度切换恢复后处理该分类。
