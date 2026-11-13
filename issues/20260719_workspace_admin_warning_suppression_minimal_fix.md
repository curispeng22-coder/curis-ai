# Workspace 启动 Admin 警告抑制最小修复

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 授权：总控 `APPROVE_WORKSPACE_ADMIN_WARNING_SUPPRESSION_MINIMAL_FIX`
- 复用方案：`issues/20260719_workspace_startup_signal_coverage_gap_decision.md`（`CLOSED`）
- 父链：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（保持冻结）

## 唯一目标

仅在 Workspace 启动路径抑制 Admin 专属、非 allowlist 的警告，使既有最外层启动信号成为唯一允许 JSON 行。

## 精确范围

- 只允许修改 `backend/app/main.py` 及其现有 focused 启动信号测试；
- Workspace 路径不输出该 Admin 警告；Admin 路径保持原行为；
- 已批准的四类信号映射、single-field `unknown` 和单行回传格式不变。

## 禁止范围

不改信号契约、Docker、Key、模型、D1、pytest、外网；不新增模块、框架、配置、日志存储或客户端接口；不运行 sentinel。

## 验收

系统交付只跑 focused 检查并交质量。质量只验证 Workspace / Admin 路径差异、唯一允许 JSON 与既有单次 sentinel 回传格式；通过后可直接复用既有 sentinel 执行规则，无需重新审议。

## 收口

质量 Review 在 `76b6d2ba` 给出 `PASS`：仅两文件，Workspace 警告受抑制、Admin 原行为和 `ADMIN_STRICT` 保持，固定映射与单行 JSON 不变。下一步直接复用既有 single-sentinel 执行规则。
