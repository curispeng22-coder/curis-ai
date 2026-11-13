# Workspace 镜像 Pin、一次在线构建与构建后 Sentinel 质量 Review

- Issue：`issues/20260719_workspace_pinned_online_build_postbuild_sentinel.md`
- 交付 SHA：`4d04cffa04906c476e84ce6617afa69336229031`
- 质量结论：`PASS / RUNTIME_NOT_HEALTHY`

## 独立复核

- `git show 4d04cffa` 仅包含 `deploy/curis/gateway/Dockerfile.workspace` 与 `deploy/curis/gateway/docker-compose.yml`；Python 固定为 `sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6`，Compose 两处 Envoy 均固定为 `sha256:caa5b411be1633b90023592a34a7e010c933d6e60206c758f631485e53006865`。
- 交付席正式回传唯一在线 build 为 `success`、`source_allowlist_match=true`；允许来源精确为 `auth.docker.io`、`registry-1.docker.io`、`pypi.org`、`files.pythonhosted.org`。静态复核 Dockerfile 与 `backend/requirements.txt` 未发现额外 URL、镜像或包源。
- 新镜像 `image_id=sha256:f90c82e14535ae00e02951229fb1fb4c03fe051828c5db52e0c081d027073ada`，`created=2026-07-19T15:17:38.987030039+08:00`；`Entrypoint=null`，`Cmd=["python","-m","backend.app.workspace_startup"]`，与交付文件匹配。
- SBOM 为 CycloneDX 1.5，共 117 packages；质量席独立计算 SHA-256 为 `b044321b5fafe9eb281b67c722232ee2608cbe8cf527f7282ed12492dc809be0`，其容器组件哈希与上述 image_id 一致。
- 唯一 postbuild sentinel 已消费：Workspace `exit=1`，唯一 `GET /health=503`，`stage=create_app`、`signal=factory_exception`、`failure_code=create_app_failed`，`log_lines=1`、`redaction=passed`、`cleanup=completed`。
- 交付证据声明模型 Key/config absent；无模型、D1、pytest、业务请求或重试。质量席遵守禁令，未自行执行 Docker、启动或请求。

## 结论

本 Issue 的 pin、唯一受控在线 build、镜像身份核对、唯一 sentinel 与 cleanup 均通过。Workspace 仍未健康启动，唯一运行阻塞为 `create_app_failed`；该固定分类交产品规划席决定后续，D1 当前不由质量席自行解冻。

Next Seat：产品规划席

Handoff: sent to 产品规划席
