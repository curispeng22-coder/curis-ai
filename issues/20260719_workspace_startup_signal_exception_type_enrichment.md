# Workspace 启动信号增强：携带异常类型（脱敏）

- 状态：`IN_PROGRESS`
- 优先级：`P0`（接 `docs/pmo/20260719_quota_handoff_plan.md` 唯一目标：定位并最小修复 `create_app_failed`）
- 当前执行席：系统交付席（单主执行模式）
- 父链路：`issues/20260719_workspace_pinned_online_build_postbuild_sentinel.md`（已 `CLOSED`，sentinel 回传 `create_app_failed`）

## 背景

钉版在线构建（SHA `4d04cffa`）的 postbuild sentinel 首次返回可分类失败 `create_app_failed`（stage=create_app / signal=factory_exception / exit=1 / health=503）。该分类来自 `backend/app/main.py:3400` 模块级 `app = create_app()` 抛出的**未特指通用异常**，被 `_signal_for_startup_error` 归为 `create_app_failed` 并 `SystemExit(1)`。

脱敏机制刻意不输出异常原文/堆栈，导致 sentinel 仅 1 行，无法得知真实异常类型，原团队（无 Docker 权限 + 脱敏）从未拿到根因。本地三组复现（全新库 / 现有 `data/workspace.sqlite` 副本 / gateway 变量齐全）均构造成功，排除代码/数据/依赖漂移；缺 issuer/key 会落 `config_rejected` 而非 `create_app_failed`，亦排除。结论：真因在容器运行时环境，须由下次 sentinel 暴露异常类型后方可精准修复。

## 唯一目标

在不破坏脱敏契约（不输出异常原文/堆栈/参数/路径/Key/环境）的前提下，让**已分类**启动失败信号额外携带异常**类型名**（`type(error).__name__`，如 `KeyError`/`ValueError`/`OSError`），使下次 sentinel 直接显示失败构造点类别，支撑精准最小修复。

## 精确修改

- `backend/app/main.py`：
  - 新增 `_classified_signal(stage, signal, error)`：在 `_startup_failure_signal(stage, signal)` 基础上追加 `"exception_type": type(error).__name__`。
  - `_signal_for_startup_error(error)`：对 marked / 默认 `create_app` 路径改用 `_classified_signal` 携带类型。
  - 两处 `module_import` 处理（约 line 72、151）改用 `_classified_signal("module_import","import_exception", error)` 携带类型。
  - `_startup_failure_signal()` 的 `unknown` 分支**保持单字段** `{"failure_code":"unknown"}`，不携带类型。
  - 分类映射、`failure_code` 取值、红分类规则一律不变；不拼接/序列化异常原文。
- `backend/tests/test_workspace_startup_stage_signal.py`：
  - `test_unmarked_startup_error_is_fixed_create_app_failure` 期望字典增加 `"exception_type": "RuntimeError"`，保留 `assertNotIn("sensitive", ...)`。
  - 新增对 `exception_type` 的断言：marked 错误与 `module_import` 调用均携带正确类名，且不含异常文本。
  - `_load_signal_functions` 的 `wanted` 增加 `_classified_signal`。

## 允许范围

仅改动上述两文件；不启动容器/服务、不注 Key、不调用模型/D1、不出网、不跑 pytest 全量（仅本单测）；保持脱敏。

## 禁止范围

禁止输出异常 message/args/stack/traceback/path；禁止改动 `failure_code` 分类或放宽 `unknown` 脱敏；禁止引入新依赖或外部调用。

## 验收

1. `PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python backend/tests/test_workspace_startup_stage_signal.py` 全部通过。
2. 两文件内存 compile 通过；`git diff --check` 通过。
3. 质量席独立复核：分类仅由固定 `(stage,signal)` 映射产生；`exception_type` 仅为类名、不含原文；`unknown` 仍单字段。
4. 下一步：额度已恢复（用户确认），重建镜像并重跑唯一 sentinel，按 `exception_type` 精准最小修复 `create_app_failed` 根因。
