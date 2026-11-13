# Workspace：D1 E2E Gateway 启动失败诊断

- 状态：`BLOCKED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 父 Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`

## 已知事实

Owner 隐藏注入后的启动过程完成镜像构建，egress 为 healthy，workspace 与 gateway 容器均显示 started；但 `deploy/curis/start-local.sh` 等待 `http://127.0.0.1:8080/health` 30 秒仍未得到 HTTP 200，随后自动 cleanup，终端显示“Gateway 启动失败”。

## 目标

只读确定 Gateway health 失败的根因，并给出最小修复或安全诊断命令。必须保留失败时的脱敏 gateway / workspace 容器证据，不能让 cleanup 擦除唯一线索。

## 约束

- 不读取、输出或持久化 Key；不调用模型、不读写 D1 目标、不跑 pytest、不出网。
- 不重新执行 Owner 隐藏注入命令；不使用内联通用 Shell / Python 绕过启动链。
- 先检查现有 `start-local.sh`、Compose、Envoy health 路由与 cleanup 时序；若需要重现，必须先回传最小、无模型、无凭据泄露的诊断方案并由产品规划席确认。

## 验收

1. 根因可由文件、容器状态或脱敏日志证明；
2. 明确是 workspace、Envoy/JWKS、健康路由、启动时序还是启动脚本清理策略；
3. 给出最小修复 Issue 或无副作用诊断命令；
4. 父 E2E 仍不恢复，直到质量复核启动链。

## 诊断结论

现有残留证据不能唯一判定 30 秒非 200 的运行根因。可确定的直接缺陷是 `start-local.sh` 只在内存保留最后 HTTP code、失败时不输出，随后 ERR trap 立即 `stop-local` / `docker-compose down` 删除 gateway / workspace / egress 容器证据。生成的 Envoy 配置静态 validate PASS，`/health` 明确允许缺失 JWT 并路由 workspace，因此不能把问题直接归因于 JWT 配置。

唯一后续项：`issues/20260718_workspace_gateway_startup_evidence_preservation_gate.md`。父 D1 继续冻结。
