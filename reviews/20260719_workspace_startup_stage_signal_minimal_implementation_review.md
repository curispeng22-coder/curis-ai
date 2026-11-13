# Workspace 启动阶段信号最小实现质量 Review

- Issue：`issues/20260719_workspace_startup_stage_signal_minimal_implementation.md`
- 固定修订：`09c26a8e90fc8e72ee668b14987670b432a4825b`
- 结论：`PASS`
- 范围：静态代码与 focused unittest；未运行 pytest、Docker、服务或 sentinel，未注 Key、未调用模型 / D1、未出网

## 独立证据

1. 提交范围精确为 `M backend/app/main.py` 与 `A backend/tests/test_workspace_startup_stage_signal.py`，无第三文件；部署脚本、Dockerfile 与 Compose 均未改。
2. stage/signal allowlist 仅含已批准的四类映射；未知、空值、交叉组合统一返回严格单字段 `{"failure_code":"unknown"}`。
3. 数据库分类仅在 `sqlite_errorcode == SQLITE_SCHEMA` 时返回 `schema_incompatible`；普通 `sqlite3.DatabaseError` 返回 unknown 单字段。
4. Identity、Admin、Model 只在既有显式校验拒绝分支标记 `validator_rejection → config_rejected`；未标记的 create_app 异常固定映射 `create_app + factory_exception`，不携带异常文本。
5. Workspace 模式下 ImportError、其他导入异常与 create_app 异常均只输出固定 JSON 并以 `SystemExit(1)` 结束；非 Workspace 分支继续抛出原异常，Admin 行为未改。现有 Workspace CMD 与启动链保持原样。
6. 独立重跑 `PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python backend/tests/test_workspace_startup_stage_signal.py`：`4 tests / OK`；两文件内存 compile 与提交 `git diff --check` 均通过。
7. `3000/3100/8001/8002/8080` 全部 `CLOSED`；固定 D1 correlation 的 claim/model/tool/usage 及其他事件为 0。

## 结论与边界

两文件最小实现符合已关闭证据契约：分类互斥、schema 精确、unknown 单字段、异常原文不进入信号，Workspace / Admin 边界保持，结论为 `PASS`。

本 PASS 不授权 sentinel、启动、Key、模型或 D1。下一次无秘密 sentinel 必须由产品规划席另建 Issue 并取得总控 / 安全授权；父 D1 继续冻结。

## 2026-07-19 正式补派复核

- 当前 HEAD 精确为交付 SHA `09c26a8e90fc8e72ee668b14987670b432a4825b`；该提交仅修改 `backend/app/main.py` 并新增 `backend/tests/test_workspace_startup_stage_signal.py`。
- 重新执行 `PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python backend/tests/test_workspace_startup_stage_signal.py`：`Ran 4 tests`，`OK`。
- 两文件只读内存 compile：`COMPILE_OK=2`；提交级两文件 `diff --check`：通过。
- 静态复核确认分类只由固定 `(stage, signal)` 二元组映射产生；非法组合严格返回单字段 `failure_code=unknown`。新增启动信号路径不拼接、序列化或输出异常原文，也未新增 reason/message/error/stack/path/details/source 等自由字段或通用诊断框架。
- 未运行 pytest、Docker、服务、sentinel、Key、模型、D1 或外网；实现文件与测试文件均未被本席修改。

Next Seat：产品规划席

Handoff: sent to 产品规划席
