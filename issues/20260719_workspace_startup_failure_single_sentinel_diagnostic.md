# Workspace 启动失败单次无秘密 Sentinel 诊断

- 状态：`CLOSED`
- 优先级：`P0`
- 当前执行席：系统交付席 `019f6c48-8999-7ac1-aade-119ac71b483d`
- 当前复核席：质量运行席 `019f6cb7-3e8d-7313-91d9-95b226c9ed2e`
- 前置：`issues/20260719_workspace_startup_stage_signal_minimal_implementation.md`（`CLOSED`）
- 父 E2E：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（保持冻结）

## 唯一动作

仅一次本地启动后执行 `GET 127.0.0.1:8080/health`，按已闭合契约回传结构化启动分类和立即清理证据。

## 允许回传

仅固定枚举和清理事实：`component`、`container_exit_code`、`health_code`、`log_lines_seen`、`redaction_status`、`cleanup_status`、`timestamp`；完整合法映射时可含 `failed_stage`、`failure_signal`、`failure_code`。其他情况仅 `failure_code=unknown`。

## 禁止范围

不注 Key，不调用模型或 D1 POST，不运行 pytest、不出网；不回传原始日志、stderr、异常文本、自由字段、Header、环境原文或凭据。诊断后立即 cleanup；不得重试。

## 验收

回传 `结论 + SHA/命令 + 唯一阻塞`，不超过 120 字。若得到具体 `failure_code`，产品规划席直接建立唯一修复 Issue；若 `unknown`，保持 D1 冻结并由总控裁决。

## 本次结果

质量线程的平台拒绝 Docker API socket；既有启动与 `GET /health` 均未执行，五端口关闭。该线程的 `failure_code=unknown` 仅表示未取得运行证据，不得作为代码根因或建立修复单。总控已指定同一条未消耗诊断由系统交付席执行，质量席仅复核回传证据；D1 继续冻结。

## 收口结果

交付执行后的质量复核为 `PASS`（仅单次诊断与 cleanup）：`09c26a8e`、单次性及零 Key / 模型 / D1 / pytest / 外网成立，五端口关闭。由于脱敏状态不是 `passed`，回传只能采信单字段 `failure_code=unknown`；没有可用根因分类，不得建立代码修复 Issue。父 D1 保持 `BLOCKED_L2`，待总控裁决。

## 76b6d2ba 后续执行授权

`issues/20260719_workspace_admin_warning_suppression_minimal_fix.md` 已质量 `PASS`。总控明确授权直接复用本 Issue 的无秘密 single-sentinel 规则，在 `76b6d2ba` 上执行一次本地启动、`GET /health` 与 cleanup；此为修复后的唯一执行，不新增 Gate。仍禁止 Key、模型、D1 POST、pytest、外网和第二次重试。

## 最终执行结果

`76b6d2ba` 上唯一 sentinel 与 `GET /health` 已消费并完成 cleanup，五端口关闭；但未形成合法 `stage/signal`，只能采信 `failure_code=unknown`。本 Issue 不可重试，父 D1 保持 `BLOCKED_L2`，等待总控裁决。

## ed8376f1 第三次执行授权

入口包装器 `ed8376f1` 已质量 `PASS`。总控明确授权在该修订上执行第三次且唯一的无秘密 sentinel：一次 Workspace 启动、`GET /health`、cleanup；复用既有 allowlist `stage/signal/failure_code`。仍禁止 Key、模型、D1 POST、pytest、外网与第二次重试。

## 第三次执行结果

`ed8376f1` 的第三次且唯一 sentinel 已消费：`health_code=000`、未形成合法 `stage/signal`，只能采信 `failure_code=unknown`；cleanup 完成、五端口关闭。禁止重试，不得据此推断应用层根因；父 D1 保持 `BLOCKED_L2`。

## 唯一追加：运行镜像 / CMD 来源核对

总控已停止入口信号循环。本 Issue 仅追加一次只读核对：系统交付席读取 Docker inspect 与 compose resolved config，回传仅 `image_id`、镜像创建时间、Workspace Entrypoint / Cmd 是否等于 `ed8376f1` 预期、容器 `State.StartedAt` / `ExitCode`。任何自由文本、环境、日志或未列字段一律丢弃。

不得 start / build / Key / 模型 / D1 / pytest / 外网。核对结果直接决定唯一修复：镜像陈旧则受控重建；入口未起则最小命令修复；不再新增 Gate 或规划循环。

## 来源核对结果

所有允许字段均为 `null`：`image_id`、创建时间、Workspace Entrypoint / Cmd、`State.StartedAt`、`ExitCode`；因此没有可用运行来源可判断镜像陈旧或入口未起。该结果不得推断为任一代码或镜像根因；D1 继续冻结，等待总控在“受控重建”与“保留阻塞”之间裁决。

## 总控授权：离线重建与构建后唯一 Sentinel

总控 `APPROVE_OFFLINE_WORKSPACE_IMAGE_REBUILD_AND_ONE_POSTBUILD_SENTINEL`：在本 Issue 内仅对 Workspace 服务执行一次本地离线重建，禁止 pull、外网和 Key；回传仅构建成功/失败、`image_id`、创建时间、resolved Entrypoint / Cmd 与 `ed8376f1` 匹配布尔值。构建失败即停并回传唯一失败类别；构建成功才对新镜像执行一次启动、`GET /health`、cleanup 并交质量复核。禁止重试、模型、D1、pytest 与新 Gate。

## 离线重建结果

构建结果：`failure_code=offline_build_failed`。新 `image_id`、创建时间、resolved Entrypoint / Cmd 均为 `null`，匹配为 `false`；按授权失败即停，未启动、未 `GET /health`、未消费 sentinel，五端口关闭、相关容器不存在。D1 继续冻结，等待总控裁决。

## 唯一追加：受控镜像依赖恢复契约

仅派安全席裁决最小在线构建依赖契约：只允许 Dockerfile 已有的固定 registry / image / digest；若没有 digest，保持 `BLOCKED_L2`。契约必须固定 build 阶段允许域名、禁止 Key / 模型 / D1 / pytest，且仅回传产物来源、SBOM 与 image_id；失败即停。安全 `PASS` 后仍须总控单独批准一次在线受控 build，当前不得执行。

## 安全裁决

`BLOCKED_L2`：现有 Workspace Dockerfile 仅有未固定 digest 的 `python:3.14-slim`，Compose Envoy 也仅有未固定 digest 的 `envoyproxy/envoy:v1.31-latest`；没有可核对的固定 registry / image@digest 或已批准的 build 域名闭集。不得 build、pull、联网、Key、模型、D1 或 pytest。继续条件仅为总控 / Owner 提供现有且已批准的 registry / image@digest 与固定 build 域名。

## 总控授权：受控 Digest 解析

Owner 已允许外部镜像依赖恢复。系统交付席仅可访问现有 Dockerfile / Compose 引用所需的官方镜像 registry / token 域名，读取 manifest 取得精确 `image@sha256` 与最小域名闭集；不得 build、pull 镜像层、启动、注 Key 或触及 D1。实际 digest 与域名回传安全席确认；安全 `PASS` 后自动建立唯一 pin + 一次受控在线 build Issue。

Owner 另批准构建阶段仅访问 `pypi.org` 与 `files.pythonhosted.org`。来源锁定时仅允许这两域名及已核验的 `auth.docker.io`、`registry-1.docker.io`；不得扩展其他域名、镜像、包源、Key、模型、D1 或 pytest。若 `requirements` 无可接受的版本锁定，安全结论必须 fail-closed 并指出精确缺口。

## 来源锁定收口

安全 `PASS`：`python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6` 与 `envoyproxy/envoy:v1.31-latest@sha256:caa5b411be1633b90023592a34a7e010c933d6e60206c758f631485e53006865`；唯一允许域名为 `auth.docker.io`、`registry-1.docker.io`、`pypi.org`、`files.pythonhosted.org`。后续仅进入 pin + 一次受控在线 build Issue。
