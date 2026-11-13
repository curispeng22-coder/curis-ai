# Workspace create_app_failed 根因修复（D1 toolchain 启动韧性）

- 状态：`IN_PROGRESS`
- 优先级：`P0`
- 当前责任席：系统交付席（单主执行模式）
- 父链：`docs/pmo/20260719_quota_handoff_plan.md`（唯一目标：处理 `create_app_failed` 恢复 /health）
- 关联：`issues/20260719_workspace_startup_signal_exception_type_enrichment.md`（信号增强，已 PASS，用于暴露本根因）

## 根因（已用增强信号 + 容器内 traceback 确证）

- `main.py:901`：`d1_toolchain = build_d1_toolchain(default_executor, event_log)` 在 `create_app()` 顶层**无条件**执行。
- `local_rd_toolset.py:83`：`root = WORKSPACE_ROOT.resolve(strict=True)`。
- `local_rd_toolset.py:21`：`WORKSPACE_ROOT = Path("/Users/yy/Documents/Curis AI Workspace")`——**硬编码 macOS 绝对路径**。
- 容器内为 Linux，`/Users` 不存在 → `resolve(strict=True)` 抛 `FileNotFoundError` → 归类 `create_app_failed`。
- 增强信号实测：`{"exception_type":"FileNotFoundError","failed_stage":"create_app","failure_code":"create_app_failed","failure_signal":"factory_exception"}`。
- 结论：原 sentinel 的 `create_app_failed` 一直就是此 FileNotFoundError；此前因脱敏无 traceback 而长期不可见。

## 决策

- D1 真实 E2E 仍冻结（`0/1`），本次**不启用 D1**，只让 `create_app()` 在 D1 toolchain 构建失败时不再中断启动，使 `/health` 恢复可用。
- **不修改** `WORKSPACE_ROOT`（那是本地 macOS 开发的既有依赖，属独立议题）。

## 精确修改（`backend/app/main.py`，仅此一文件）

1. **line 901 包韧性 try/except**：
   ```python
   try:
       d1_toolchain = build_d1_toolchain(default_executor, event_log)
   except (FileNotFoundError, OSError, D1ToolchainError, LocalRDToolError) as error:
       logger.warning("D1 toolchain unavailable at startup; continuing without it (D1 frozen)")
       d1_toolchain = None
   ```
   - 需引入 `LocalRDToolError`：`from .local_rd_toolset import LocalRDToolError`（放在 line 115 附近的 import 区）。`D1ToolchainError` 已导入。
   - 日志必须脱敏：**禁止**拼接 `str(error)` / 路径 / traceback；只输出固定文案。
   - 若模块级 `logger` 不存在，紧接 import 区后加 `logger = logging.getLogger(__name__)`。

2. **line 2040 守护 D1 路由**（避免 `d1_toolchain=None` 时 `AttributeError`）：
   ```python
   try:
       if d1_toolchain is None:
           raise HTTPException(status_code=503, detail="D1 toolchain unavailable")
       return d1_toolchain.execute()
   except D1ToolchainError as error:
       raise HTTPException(status_code=409, detail="D1 toolchain rejected") from error
   ```

## 验收

- `py_compile backend/app/main.py` OK。
- 现有 `backend/tests/test_workspace_startup_stage_signal.py` 仍 7 passed（不破坏）。
- 重建 `gateway-workspace:latest` 并重跑 sentinel（占位密钥 + 本地 JWKS）：`/health` 返回 **200** 而非 503/`create_app_failed`；容器 stderr 不再有启动失败信号。
- 脱敏红线不变：信号仅含 `failure_code` 等固定字段；日志无路径/密钥。
- 提交（unstaged 或独立 commit 均可，归属 Workspace）。

## 禁止范围

- 不启用 D1（不接模型、不跑真实工具 E2E）。
- 不改 `WORKSPACE_ROOT`。
- 不引入新依赖 / 新镜像 / 其他域名。
