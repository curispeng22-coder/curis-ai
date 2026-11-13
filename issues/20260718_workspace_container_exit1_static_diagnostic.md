# Workspace：容器启动 Exit 1 静态根因诊断

- 状态：`BLOCKED_L2`
- 优先级：`P0`
- 当前责任席：系统交付席
- 父 Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`

## 已知事实

无模型 sentinel 仅 GET `/health` 时：Gateway 与 egress 正常，Workspace 容器 `exited/1`，Gateway 返回 `503 upstream_unavailable`。现有安全日志只保留分类，未保留原始异常正文。

## 目标

只读定位 Workspace 在当前 Compose、环境变量、数据库、D1 入口和启动命令组合下会退出的具体根因，并指出最小修复点。

## 允许检查

- `docker-compose.yml`、Dockerfile、`start-local.sh`、Workspace 启动命令、`main.py` 与 D1 / LocalRDToolset 的启动期导入和环境读取；
- 静态 Compose config、Python compile / import 级验证（不得启动 server）；
- 必要时只读检查同一 `quality.sqlite` schema 是否满足启动所需表 / 列。

## 禁止范围

- 不启动容器或服务，不注 Key，不调用模型，不运行 D1 POST / pytest，不读写 D1 目标，不出网；
- 不输出原始环境值、密钥、数据库内容或未脱敏容器日志；
- 不改代码或配置。

## 输出

回传唯一根因、可复现的无副作用证据、受影响文件和最小修复建议。若静态证据仍不足，只能提出下一步受控诊断方案，不得猜测。

## 静态核对结果

- Compose / CMD、模块 import / compile、单项身份与模型配置校验、以及 `quality.sqlite` 所需 schema 列均通过；这些只排除了静态语法、单模块导入、单项配置和缺列问题。
- 现有诊断证据不保留 Workspace 异常类别，不能证明完整 uvicorn / `create_app` 组合的退出原因；结论只能是 `unknown`，不能把任一静态 PASS 写成“容器可启动”。
- 唯一下一步：总控与安全席另行批准一次受控运行诊断。该诊断只允许本地 `/health` sentinel，并将 Workspace 末尾日志在内存中映射为固定 failure_code；原文不落盘、不回显，随后立即清理停机。
- 父 D1 E2E 继续冻结：不得重试 Key、启动、模型调用、D1 POST、pytest 或文件写入。
