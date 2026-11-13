# D1 execute() 范围 B 专项验证报告（QA 第二层把关）

- **验证人**：严过关（Yan，QA 工程师）
- **日期**：2026-07-20
- **验证对象**：D1 execute() 范围 B（B1 落库仓储 + B2/B4 编排层 `_record_outcome` 双 sink + B3 只读状态端点 + B5 测试）
- **代码基准**：分支 `feat/roadmap-r1r2`，范围 A 已闭环于 `88594bb9`；B 增量提交 `09911824`（IS_PASS=YES）
- **结论**：✅ **PASS**

---

## 一、验证范围与手段

| 聚焦项 | 手段 |
|--------|------|
| 落库内容脱敏抽检 | ① Grep 4 个源文件 `sk-`/`api_key`/`CURIS_MODEL_GATEWAY_API_KEY`/f-string；② **真实临时 DB** 调 `D1ExecutionLogRepository.insert` + `recent()` 读出，断言字段值；③ PRAGMA `table_info` 确认列集合严格等于脱敏白名单 |
| 只读状态端点三态 | 静态审 `main.py:2078-2081` + 运行 `D1StatusEndpointTest`（frozen/ready）；`/health` 复核 |
| 错误分类增强 | 静态审 `d1_execute.py` `execute()`/`_record_outcome`（B2 三类落库 + `finally` 统一记录 + sink=None no-op）+ 运行 `D1ExecutionOrchestratorPersistenceTest`/`D1ExecutionObservabilityTest` |
| 红线核验 | `git diff` 受保护文件应为空；`git show 09911824 --stat` 确认 6 文件；`/health` 未触碰；无新 pip 依赖；零新 UI |
| 测试重跑 | `pytest tests/test_d1_execute.py -v` → 预期 31 passed / 1 skipped |

---

## 二、落库内容脱敏抽检 — 通过

### 2.1 真实临时 DB insert + recent() 读出（独立第二层）
```
RECENT_COUNT 2
ROW 2 | 'selfuse' | 'd1-tenant-reservation' | 'gateway_timeout' | 'gateway_timeout' | 33 | 0 | '2026-07-19 16:36:07'
ROW 1 | 'selfuse' | 'd1-tenant-reservation' | 'succeeded'       | None             | 12 | 140 | '2026-07-19 16:36:07'
```
插入成功与失败两类记录后读出，两类记录所有字段均为受控值（tenant_id=固定 'selfuse'、task_type=配置常量、status/error_category=枚举 value 或 None、duration_ms/token_count=整数、created_at=时间戳）。断言 `('/' not in blob)`、`('sk-' not in blob)`、`('key' not in blob)` **全部通过**——无路径/Key/参数/堆栈泄露。

### 2.2 列集合严格白名单（PRAGMA 复核）
```
COLUMNS ['id','tenant_id','task_type','status','error_category','duration_ms','token_count','created_at']
OK schema is strict desensitized whitelist
```
`d1_execution_log` 表仅含上述 8 列，与范围 B 要求的白名单完全一致；`database.py:394-403` DDL 注释亦声明不写 path/stack/key/request-parameter。

### 2.3 源文件 grep 复核（4 文件）
- `d1_execute.py`：对 `sk-`/`api_key`/`CURIS_MODEL_GATEWAY_API_KEY` **零匹配**。存在 2 处 f-string（`correlation_id=f"d1-execution:{recorded_task_type}"`、`event_type=f"d1.execution.{status}"`），二者均仅拼接**配置常量**与**已脱敏 status 枚举值**，不携带原始异常/路径/Key/请求参数，合规。
- `d1_config.py` / `d1_gateway_client.py` / `models/d1_execution_log.py`：对敏感 token / 真实 f-string 泄露 **零匹配**（`d1_gateway_client.py` 仅文档字符串声明「绝不读取凭证」；`d1_config.py` 的命中为 `{"off"}` 字面量误报，非 f-string）。

---

## 三、只读状态端点三态 — 通过

- `main.py:2078-2081`：`GET /api/workspace/internal/d1-tenant-reservation/status` 仅返回 `{"status": d1_orchestrator.status().value}`，三态 `frozen`/`ready`/`degraded` 由编排层 `status()` 推导；无表单、不泄露凭证/路径/堆栈。
- 测试 `D1StatusEndpointTest`：`test_status_ready`（响应 ∈ {ready, degraded, frozen}）、`test_status_frozen_when_config_frozen`（CURIS_D1_FROZEN=true → `{"status":"frozen"}` + `assertNotIn("key", ...)`）均通过。
- `/health` 端点（main.py:1405-1407）未改动，仍返回 `{"status":"ok"}`，不泄露内部信息。

---

## 四、错误分类增强 — 通过

`d1_execute.py` `execute()` 结构（`try/except D1ExecutionError / except D1ToolchainError / finally`）：
- **D1ExecutionError**（受控四类）：`outcome_status = error.category.value`、`outcome_category = error.category.value`（仅记枚举 value，不记原始异常）✅
- **非模型 D1ToolchainError**（scope/工具/审计）：`outcome_status = "toolchain_rejected"`、`outcome_category = "toolchain_rejected"`（脱敏上抛 + 记一条 toolchain_rejected 供可观测）✅
- **成功**：`outcome_status = "succeeded"`、`token_count = summary["total_tokens"]` ✅
- **finally 统一记录**：无论成功/失败均调 `_record_outcome`，双 sink（execution_log 落库 + event_log 发 `d1.execution.<status>` 事件）✅
- **sink=None 安全 no-op**：`_execution_log is not None` / `_event_log is not None` 守卫，`test_no_sink_does_not_record` 验证隔离单测不报错 ✅
- task_type 列仅记 `self._config.execute_task_type`（配置常量），绝不记调用方传入参数 ✅

测试覆盖：`D1ExecutionOrchestratorPersistenceTest`（success 带 token / gateway_timeout 分类行 / task_invalid 行 / no-sink no-op）、`D1ExecutionObservabilityTest`（success/failure 各发对应事件且 payload 无 "key"）全过。

---

## 五、红线 / 契约核验 — 通过

- **受保护文件零改动**：`git diff aadef60c HEAD -- d1_single_model_toolchain.py model_gateway.py local_rd_toolset.py` → **空 diff**。
- **提交范围**：`git show --stat 09911824` 仅 6 文件（d1_execute.py / database.py / main.py / models/__init__.py / models/d1_execution_log.py / tests/test_d1_execute.py），440+ / 40−，与声明一致；**未破坏 shared 核心 schema**（仅新增 append-only  desensitized 表，由 `Database.initialize()` 注册）。
- **不读凭证**：R3GatewayClient / d1_execute / d1_execution_log 均不读 `CURIS_MODEL_GATEWAY_API_KEY` 或任何凭证值。
- **无新增 pip 依赖**：`requirements/pyproject/setup.py` 在 B 提交中无变更。
- **零新增 UI**：`templates/`、`static/`、`.html/.js/.css` 在 B 提交中无变更。
- **`/health` 未改动**：B 提交对 main.py 的 diff 未触碰 health 端点。
- 单主占锁 `_claim_once` 仍由既有 `D1SingleModelToolchain.execute()` 复用，编排层未另造并发。

---

## 六、测试重跑结果

```
collected 32 items
31 passed, 1 skipped, 1 warning in 0.83s
```

| 分组 | 用例数 | 覆盖 |
|------|--------|------|
| R3GatewayClient（A2） | 6 | 网关契约 |
| D1ExecutionOrchestrator.status（A3） | 5 | 三态矩阵 |
| D1ExecutionOrchestrator.execute（A3） | 8 | 错误分类/降级/成功 |
| D1 路由集成（A4） | 2 | frozen/execute_disabled → 503 固定文案 |
| D1ExecutionLogRepository（B1） | 2 | 真实 DB 建表+insert+recent/count_by_status |
| D1ExecutionOrchestratorPersistence（B2） | 4 | 成功/超时/非法 task/无 sink |
| D1ExecutionObservability（B4） | 2 | 成功/失败 EvolutionaryEvent |
| D1StatusEndpoint（B3） | 2 | ready/frozen 三态 |
| real gateway e2e | 1 skipped | 待安全边界席裁定凭证接入 |

21 个 A 期用例 + 10 个 B 期用例 = 31 passed；1 skipped 为真实网关端到端（设计内，待安全边界席裁定）。

---

## 七、智能路由判定

- **源码 Bug（反馈工程师）**：无。降级方向、错误分类落库、双 sink no-op、状态端点三态均正确。
- **测试 Bug（QA 自行修复）**：无。断言正确、Fake 隔离得当、真实 DB 抽检通过。
- **判定 → NoOne（全部通过）**。

> 环境性观察（**非范围 B 缺陷、不影响结论**）：既有 `tests/test_d1_unfreeze.py` 因 `from backend.app import ...` 在 backend/ 根目录运行无法解析而收集失败（预存 import 路径问题，git diff 为空，不在 B 范围）。范围 B 的落库/状态/分类契约已由 `test_d1_execute.py` 独立覆盖并全过。

---

## 八、最终结论

### ✅ PASS

范围 B（落库 + 可观测 + 只读状态端点）经独立第二层验证，**落库脱敏（真实 insert/readback + 列白名单）、状态端点三态、错误分类增强（三类落库 + finally 统一 + sink no-op）、红线（受保护文件零改动 / 不读凭证 / 无新依赖 / 零 UI / /health 不变）** 全部达标；测试 31 passed / 1 skipped，无源码缺陷、无测试缺陷。建议进入范围 B 闭环留痕，并待安全边界席裁定 R3 凭证接入后补真实网关端到端用例。

**落盘**：本验证证据已写入 `reviews/20260720_d1_execute_b_qa.md`。
