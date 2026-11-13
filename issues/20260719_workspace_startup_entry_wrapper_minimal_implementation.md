# Workspace 启动入口最小包装器

- 状态：`CLOSED`
- 优先级：`P0`
- 架构复用确认：系统交付席
- 安全复用确认：安全边界席
- 父链：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（`BLOCKED_L2`）

## 唯一目标

将 Workspace 容器入口包入固定 bootstrap，使发生在 `main.py` 现有信号边界之前的 import / create_app / 配置 / schema 失败，只能输出既有四类完整 `stage/signal/failure_code` 或严格单字段 `unknown`。

## 精确范围

- 仅最少入口模块、`deploy/curis/gateway/Dockerfile.workspace` 的 Workspace CMD 与 focused 测试；
- Admin 路径和既有信号契约保持不变；
- 复用既有四类映射与 `unknown` fail-closed 规则。

## 禁止范围

不输出异常原文、路径、堆栈、自由字段或环境值；不新增通用诊断框架、Shell/Python 内联执行、配置、客户端接口或日志存储；不运行 Docker / sentinel、Key、模型、D1、pytest 或外网。

## 顺序与验收

1. 系统交付与安全席仅确认该范围可复用既有契约；
2. 总控确认后才实施；
3. 实施后质量只做 focused 无出网验证；通过后另按既有规则申请一次无秘密 sentinel，D1 始终冻结至可采信分类。

## 已确认的唯一实现路径

新增 `backend/app/workspace_startup.py`，并将 `Dockerfile.workspace` 的 CMD 精确改为 `python -m backend.app.workspace_startup`。bootstrap 仅在 try 内导入 `uvicorn` 与 `backend.app.main:app`：既有 `main.py` 已输出固定信号并 `SystemExit` 时原样退出、不重复；main 信号前的 `ImportError` 只输出既有 `module_import/import_exception/import_failed` 固定 JSON；其他异常只输出 `{failure_code:unknown}`；成功时按现有 `0.0.0.0:8002` 运行 uvicorn。异常对象不绑定、不回显、不重抛；Admin 入口不变。

架构与安全均 `PASS`（仅方案）。本 Issue 不授权实施；已提交总控裁决。

## 总控实施授权与交付索引

- 总控授权：`APPROVE_WORKSPACE_STARTUP_ENTRY_WRAPPER_MINIMAL_IMPLEMENTATION`；
- 授权范围：`backend/app/workspace_startup.py`、`backend/tests/test_workspace_startup_entry.py`、`deploy/curis/gateway/Dockerfile.workspace`；
- 已交付修订：`ed8376f19cc714c82c55c8b75fa1706d63447ddb`；
- 质量 Review：`PASS`，focused 5 OK；本授权不改变父 D1 冻结或无秘密 sentinel 约束。
