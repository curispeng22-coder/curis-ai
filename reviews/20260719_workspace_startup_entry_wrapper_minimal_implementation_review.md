# Workspace 启动入口最小包装器质量 Review

- Issue：`issues/20260719_workspace_startup_entry_wrapper_minimal_implementation.md`
- 固定 SHA：`ed8376f19cc714c82c55c8b75fa1706d63447ddb`
- 分支：`feat/roadmap-r1r2`
- 结论：`PASS`

## 独立核验

- 提交范围仅新增 `backend/app/workspace_startup.py`、新增 `backend/tests/test_workspace_startup_entry.py`、修改 `deploy/curis/gateway/Dockerfile.workspace`。
- Workspace CMD 精确切换为 `python -m backend.app.workspace_startup`；Admin 启动入口未修改。
- bootstrap 在 `try` 内导入 `uvicorn` 与 `backend.app.main:app`；既有 main 启动信号产生的 `SystemExit` 原样继续，不重复输出。
- main 信号边界前的 `ImportError` 仅输出固定 `module_import + import_exception → import_failed` JSON；其他加载或 uvicorn 启动异常严格输出单字段 `failure_code=unknown`。
- 异常对象未绑定、拼接、序列化或重抛；无异常原文、路径、堆栈、自由字段、配置或通用诊断框架。
- 独立执行 `PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python -m unittest -v backend.tests.test_workspace_startup_entry`：`Ran 5 tests`，`OK`。
- 两个 Python 文件只读内存 compile：`COMPILE_OK=2`；提交级三文件 `diff --check`：通过；三份实现文件工作树无额外差异。

## 范围

未运行 Docker、服务、sentinel、Key、模型、D1、pytest 或外网；未修改实现。

唯一阻塞：无。

Next Seat：产品规划席

Handoff: sent to 产品规划席
