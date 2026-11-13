# Workspace：Gateway 启动失败证据保留与 Sentinel 健康诊断 Gate

- 状态：`CLOSED`
- 优先级：`P0`
- 发起：产品规划席
- 决策：总控决策席
- 安全复核：安全边界席
- 父 Issue：`issues/20260718_workspace_d1_e2e_gateway_startup_diagnostic.md`

## 唯一目标

只修复启动失败时的证据丢失，并用非秘密 sentinel 配置做一次无 D1 POST、无模型调用的 Gateway `/health` 重现，区分 listener、认证与 workspace upstream 三类故障。

## 最小变更

仅允许修改 `deploy/curis/start-local.sh`：

1. `wait_for` 失败时输出最后 HTTP code；
2. cleanup 前以 `0600` 保存 `docker-compose ps` 以及 gateway / workspace / egress 各最多 200 行**脱敏**日志；
3. 保存后继续现有停止逻辑，不改变正常启动路径。

## Sentinel 重现

- 仅使用非秘密 sentinel 配置；不读取、注入或输出真实 Key。
- 仅请求 `/health`；禁止 D1 POST、模型调用、文件读写、pytest、前端、外网与任何业务 API。
- 必须记录分类结果：`000`、`401` 或 `503`，及对应脱敏容器证据。

## 安全边界

- 日志内不得保留 Key、Authorization、Cookie、JWT、prompt、文件正文、环境变量或完整 subject；命中即拒绝保存。
- 诊断文件只允许当前用户读取，验证后按现有清理策略移除。
- 不重试 Owner 真实 Key 命令，不恢复 D1 E2E。

## 验收

安全 PASS 后，系统交付实施并用无模型 sentinel 重现；质量运行席独立读取分类和脱敏证据。只有 Gateway 健康根因明确且启动链质量通过，父 D1 才可重新进入静态预检。

## 安全契约已通过

安全边界席已在 `reviews/20260718_workspace_gateway_startup_evidence_preservation_security_review.md` 给出 PASS。仅允许修改 `start-local.sh`：失败时先保存并校验脱敏 `ps`、gateway / workspace / egress 日志，各最多 200 行，目录 0700、文件 0600；只保留组件、阶段、最后 HTTP `000/401/503/200`、固定分类、容器状态、行数/截断/时间/脱敏状态。命中敏感内容或未知字段即不落盘。sentinel 只可一次 GET `127.0.0.1:8080/health`。

## 收口结果

质量运行席确认诊断链 PASS：Gateway / egress 正常，Workspace `exited/1`，因此 `/health` 分类为 `503 upstream_unavailable`；脱敏、权限、长度、零副作用与清理终态均成立。见 `reviews/20260718_workspace_gateway_startup_evidence_preservation_gate_review.md`。该 Gate 只定位到 Workspace 退出，具体退出根因转入 `issues/20260718_workspace_container_exit1_static_diagnostic.md`。
