# Workspace 启动信号覆盖缺口裁决

- 状态：`CLOSED`
- 优先级：`P0`
- 架构意见：系统交付席
- 安全复核：安全边界席
- 父链：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（`BLOCKED_L2`）

## 唯一目标

只读确定：为何 `main.py` 的既有固定枚举没有覆盖真实 `exit=1`，以及最小、非原文、可判定信号应落在哪个既有启动边界。

## 输出

只回传一个方案：覆盖缺口、精确既有落点、固定枚举和 fail-closed 条件；不得提出多方案、通用框架或扩展范围。

## 禁止

不改实现，不运行 Docker / sentinel，不注 Key，不调用模型 / D1，不跑 pytest、不出网；不读取或回传原始日志、stderr、异常文本、环境原文、凭据或自由字段。

## 唯一裁决方案

缺口不在已批准的四类枚举，而在同一 stderr 证据流：Workspace 进入 `create_app` 后，Admin 专属警告先输出非 allowlist 文本，导致最外层 `app=create_app()` 的合法固定信号也因整流脱敏失败被整体丢弃。

唯一落点仍为 `backend/app/main.py`：保留既有最外层异常出口作为唯一信号边界；仅在 Workspace 产品路径抑制该 Admin 专属警告，使证据流恰好一行固定 JSON。既有四组映射不变；普通数据库异常与未知组合只允许 `{failure_code:unknown}`。0 行、多行、额外字段、非法组合或敏感命中一律 `unknown`。

架构与安全均 `PASS`（只读方案）。本 Issue 不授权实现或 sentinel；父 D1 继续冻结，方案已回传总控裁决。
