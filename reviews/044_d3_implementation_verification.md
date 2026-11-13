# D3 Append-Only Evolution Event Log 实现验证 (质量运行席)

- Date: 2026-07-07
- Reviewer seat: 质量运行席 (CONV-SEAT-QUALITY-001)
- Target: issues/047 + ADR-0020 + changed files (backend/app/{database,evolution_governor,main,orchestrator,result_store}.py, 新增 backend/app/evolution_event_log.py, backend/tests/test_d3_event_log.py)
- Verdict: PASS
- Evidence: 57 项测试全部通过；git diff --name-only 仅列出预期的 5 个改动文件 + 2 个未跟踪新增文件；git diff --check 退出码 0；backend/app 禁止区关键词扫描 0 命中（含 `update evolution_events` / `delete from evolution_events` 0 命中）。
- Behavior-contract fidelity: PASS（5 项全部符合 ADR-0020 契约）
- Known gaps / open questions: none（实现期仅需承接 reviews/042 的 3 条文档级 note，不阻断接受）
- Next: 若 PASS → 路由 产品规划席 接受实现；接受后 D3 切片关闭，按 ADR-0016 顺序进入 D2 (Evolution Governor Sandbox, issues/046)。

## A) 验证证据

### A.1 测试套件
```
cd backend && .venv/bin/python -m unittest discover -s tests -p "test_*.py"
Ran 57 tests in 0.810s — OK
```
57 项测试全部通过（含新增 `test_d3_event_log.py` 的 9 项聚焦断言），无失败、无错误。

### A.2 改动范围 (git diff --name-only HEAD -- backend frontend)
仅列出 5 个既有文件，与预期一致：
- backend/app/database.py
- backend/app/evolution_governor.py
- backend/app/main.py
- backend/app/orchestrator.py
- backend/app/result_store.py

新增（未跟踪，git status 确认）：
- backend/app/evolution_event_log.py  (??)
- backend/tests/test_d3_event_log.py   (??)

范围与 ADR-0020 / issues/047 完全一致；frontend 无任何改动。

### A.3 空白检查 (git diff --check HEAD -- backend frontend)
退出码 `0`，无尾随空白 / 合并冲突标记等。

### A.4 禁止区关键词扫描 (Grep，范围 backend/app)
正则分组：`Employee CRUD|employee expansion|multi-agent|agent abstraction|company organization|ROI|business module|external channel|dashboard|automatic code self-modification|task-role|task evidence|vector database|embeddings|external memory|implicit default|tool selection|route work|change task state|trigger evolution`
→ **0 命中**。

附加扫描：
- `update evolution_events` → **0 命中**
- `delete from evolution_events` → **0 命中**

**预存在 drop-table 注记（非问题）**：`database.py` 的 `_reset_legacy_tasks_table`（line 235–249）含 `drop table if exists executions; drop table if exists execution_results; drop table if exists tasks;`，此为 D3 之前既有的遗留迁移代码，**非本次 D3 引入**，且其删除对象仅为 legacy 的 `tasks`/`executions`/`execution_results`，**不触碰 `evolution_events`**。记录为 non-issue，不影响本验证结论。

## B) 行为契约保真度 (对照 ADR-0020)

### B.1 evolution_events 表以 `create table if not exists` 追加创建
`database.py:223` 在 `initialize()` 的 `executescript` 中以 `create table if not exists evolution_events (...)` 追加，与同脚本内其余 `create table if not exists` 并列；未对任何既有表执行 DROP / ALTER，也无 UPDATE/DELETE 路径写入日志表。✓

### B.2 EvolutionEventLog 仅暴露 record (INSERT) + 只读 getter，无 update/delete/mutate
`evolution_event_log.py` 仅含 `record()`（INSERT）、`get_by_correlation_id()`（SELECT）、`get_all()`（SELECT）及静态 `_event_from_row()`。`test_no_update_or_delete_method` 断言类无 `update`/`delete`/`mutate` 属性；模块内亦无 UPDATE/DELETE SQL 字符串（见 A.4）。仅写路径为 INSERT，日志构造即防篡改。✓

### B.3 ResultStore（带 event_log）按供给 correlation_id 发出 lock/simulation/decision/rollback 事件；无 event_log 时不发出
四个 save 方法在写入后调用 `self._emit(...)`：`save_architecture_lock`→`lock`（result_store.py:646）、`save_evolution_simulation`→`simulation`（:686）、`save_rollback_record`→`rollback`（:727）、`save_evolution_decision`→`decision`（:780）。`_emit`（:839–841）守卫 `self.event_log is not None and correlation_id is not None`；当 `event_log=None` 或旧调用未传 `correlation_id` 时静默不 emit。`test_store_without_event_log_emits_nothing` 确认回归为零。✓

### B.4 EvolutionGovernor.evaluate() 生成单一 correlation_id，串联三次 store save，发出 proposal 事件，并在返回 dict 中带 correlation_id；无 event_log 时为 no-op
`evolution_governor.py:24` 每次 `evaluate()` 生成 `correlation_id = str(uuid.uuid4())`，传入 `save_evolution_simulation`（:100）、`save_rollback_record`（:111）、`save_evolution_decision`（:126）；当 `proposal is not None and self.event_log is not None` 时 `event_log.record(..., event_type="proposal", ...)`（:53–54）；并 `decision_record["correlation_id"] = correlation_id`（:128）返回。`test_governor_emits_correlated_events` 验证五类事件中四类（proposal/simulation/decision/rollback）共享同一 `correlation_id`；`test_governor_without_event_log_is_noop` 验证无 event_log 时日志无新增。✓

### B.5 main.py 新增只读 GET /api/evolution-events 端点，加性、既有端点语义不变
`main.py:130–134` 新增 `@app.get("/api/evolution-events")`，按可选 `correlation_id` 调用 `event_log.get_by_correlation_id` 或 `event_log.get_all()`，纯只读。既有端点（`/api/task*`、`/api/tools`、`/api/tool/*` 等）定义与语义均未改动。✓

## C) 结论
所有客观证据（57 测试通过、改动范围收敛、diff --check 0、禁止区 0 命中、五类事件均真实写路径、仅 INSERT 不变量成立、向后兼容 no-op 成立）与 ADR-0020 契约逐条吻合，无阻断项。本验证 **PASS**。reviews/042 的 3 条文档级 note 属接受后边界澄清，实现侧已通过代码与测试满足其实质要求（如 `ResultStore.__init__` 已显式 `self.event_log = event_log`，orchestrator 引用 `store.event_log` 成立）。

接受权属 产品规划席；质量运行席不在此代为接受。
