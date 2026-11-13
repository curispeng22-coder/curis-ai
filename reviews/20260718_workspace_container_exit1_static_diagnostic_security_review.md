# Workspace 容器 Exit=1 静态诊断安全 Review

- Issue：`issues/20260718_workspace_container_exit1_static_diagnostic.md`
- 结论：`PASS`（仅一次无秘密诊断契约；不授权启动、注Key、模型、D1 POST、pytest 或出网）

## 允许的诊断动作

- 只读取固定 Workspace 容器的退出状态与末尾最多 200 行日志；不读取环境变量、命令行、挂载、请求体或数据库内容。
- 日志必须流式进入内存分类器，禁止 `tee`、临时文件、runtime 文件、持久化日志或原文回传；管道错误、超长行、编码异常和读取异常均直接归类 `unknown`。
- 仅执行一次无秘密本地 Sentinel `GET http://127.0.0.1:8080/health`；不得携带请求体、Authorization、Cookie、租户/CEO Header 或模型配置。允许的健康状态仅为 `000/200/401/503`。
- 分类完成后立即执行既有 cleanup/停机；不得为诊断重启、重试、重新注Key或保留 Workspace 容器。

## 唯一 failure_code

只允许以下五个值：

- `import_failed`
- `database_init_failed`
- `identity_config_rejected`
- `model_config_rejected`
- `unknown`

只有固定错误类型的无敏感匹配才可映射到前四项；任何敏感命中、未知文本、多个类别同时命中、分类器异常或证据不足均必须输出 `unknown`。不得输出异常正文、堆栈、模块路径、数据库路径、环境值或推测原因。

## 敏感拒绝边界

以下任一命中即丢弃当前流内容并将 `failure_code=unknown`：Key、Secret、Token、Password、Cookie、JWT、Bearer、Authorization、私钥/证书块、数据库连接串、完整 subject/member token、Prompt、模型原文、D1 payload、文件正文、请求 Header 或环境变量值。不得通过部分脱敏后继续分类。

对外或审计只允许返回固定结构字段：`component=workspace`、`container_exit_code=1`、`failure_code`、`health_code`、`log_lines_seen`、`redaction_status`、`cleanup_status`、`timestamp`。其中 `redaction_status` 只能为 `passed/unknown`，`cleanup_status` 只能为 `completed/failed`；不得附带原始错误文本。

## 零副作用与清理

- 诊断过程不写任何文件，不修改数据库、Run、Usage、D1 目标或配置；不运行模型、pytest、业务 API 或外网请求。
- 结果先完成内存分类并输出固定字段，再停止现有容器；无论分类成功、敏感命中还是异常，都必须清理并保持 `unknown` fail-closed。
- cleanup 失败只能记录固定 `cleanup_status=failed`，不得暴露清理命令输出或扩大清理范围；不得将 cleanup 失败伪装成新的 `failure_code`。
- shell 诊断期间禁止 `set -x`；所有 Docker/HTTP 原始 stderr 必须进入受控丢弃流，不得回显给终端或写入文件。

## 边界

本 PASS 仅批准一次受控的 Workspace exit=1 静态分类诊断。实现后仍需质量席证明：无原文落盘、五值白名单、敏感命中统一 `unknown`、Sentinel 仅本地 GET、cleanup 完成且端口关闭。父 D1 继续冻结。

Next Seat：产品规划席
Handoff: sent to 产品规划席
