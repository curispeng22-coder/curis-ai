# D1 execute() 范围 A 专项验证报告（QA 第二层把关）

- **验证人**：严过关（Yan，QA 工程师）
- **日期**：2026-07-20
- **验证对象**：D1 execute() 完整闭环「范围 A（最小真实调用 P0 全量，受控 gate 正式纳入）」
- **代码基准**：分支 `feat/roadmap-r1r2`，解冻 commit `aadef60c` 之后增量（共 5 文件）
- **结论**：✅ **PASS**（含 1 项环境性观察，非范围 A 缺陷）

---

## 一、验证范围与手段

对范围 A 的 5 个文件做**独立第二层把关**（非橡皮图章），覆盖四条红线：

| 维度 | 手段 |
|------|------|
| 脱敏红线 | Grep 全仓 4 个范围 A 源文件：`sk-` / `api_key` / `CURIS_MODEL_GATEWAY_API_KEY` / f-string 拼接原始异常 |
| 降级与错误分类 | 静态审 `D1ExecutionOrchestrator` + 运行 `test_d1_execute.py` 21 用例（A2/A3/A4 + mock 成功路径）|
| 红线 grep 复核（禁止区）| Grep `import openai/requests/anthropic/boto3`、`vector/embedding/connect_platform/manage_employees`；确认 `R3GatewayClient`/`d1_execute` 不读凭证；`git diff` 3 个受保护文件应为空 |
| 既有契约不被破坏 | 读 `main.py` D1 路由块与 `/health`；重跑既有 D1 契约测试 |

测试命令（路径含空格，已加引号）：

```
cd "/Users/yy/Documents/Curis AI Workspace/backend" && \
/Users/yy/.workbuddy/binaries/python/envs/default/bin/python -m pytest tests/test_d1_execute.py -v
```

---

## 二、红线 / grep 复核结果

### 2.1 脱敏红线（最高优先级）— 通过

- `d1_execute.py`：Grep `sk-`/`api_key`/`CURIS_MODEL_GATEWAY_API_KEY`/`f"`/`f'`/`str(error)`/`str(e)`/`{error}` → **零匹配**。所有对外 `detail` 仅为 `D1_UNAVAILABLE_MESSAGE` 或 `D1_TASK_INVALID_DETAIL` 两个固定常量。
- `d1_config.py`：同上 Grep → **零匹配**。唯一 warning 文案为固定常量 `D1_UNAVAILABLE_MESSAGE`。
- `d1_gateway_client.py`：`CURIS_MODEL_GATEWAY_API_KEY` 仅出现在**文档字符串**（声明「绝不读取凭证」），无任何 `os.getenv`/`os.environ` 对该 Key 的读取。
- `main.py`（D1 路由块，行 2052–2067）：503/422/409 文案全部为固定常量；`except D1ExecutionError` 仅透传 `error.status_code` 与 `error.detail`（固定），无 f-string 拼接原始异常。
- `/health` 端点（行 1405–1407）：`return {"status": "ok"}`，**未改动、不泄露内部信息**。

### 2.2 降级与错误分类正确性 — 通过（逻辑复核 + 测试覆盖）

| 触发条件 | 期望 | 代码位置 | 测试覆盖 |
|----------|------|----------|----------|
| `CURIS_D1_FROZEN=true` | 503，detail=固定常量 | `main.py:2059-2060`、`d1_execute.py:127-130` | ✅ `test_route_frozen_returns_503` |
| `execute_enabled=false`（默认）| 503，detail=固定常量 | `main.py:2059-2060` | ✅ `test_route_execute_disabled_returns_503` |
| 网关未配置（凭证缺失）| `CREDENTIAL_MISSING` → 503 | `d1_execute.py:131-135`、`_classify` | ✅ `test_execute_degraded_is_credential_missing_503` |
| 网关不可达/超时 | `GATEWAY_TIMEOUT` → 503 | `d1_execute.py:144-159`、`_classify` | ✅ `test_execute_gateway_timeout_classified_503` |
| 不支持的 task_type | `TASK_INVALID` → 422，detail 固定不传播参数 | `d1_execute.py:120-125` | ✅ `test_execute_unsupported_task_type_is_task_invalid_422` |
| 非模型类 `D1ToolchainError`（scope/工具/审计）| 路由按既有 409 脱敏文案原样上抛 | `main.py:2066-2067`、`d1_execute.py:151-153` | ✅ `test_execute_non_model_d1_error_propagates` |

### 2.3 红线 grep 复核（禁止区）— 通过

- **受保护文件未被改动**：`git diff aadef60c HEAD -- app/d1_single_model_toolchain.py app/model_gateway.py app/local_rd_toolset.py` → **空 diff（三个文件均零改动）**。✅
- **禁止 import**：全仓 `import openai|requests|anthropic|boto3` → 仅命中 `app/connectors/aitoearn_client.py:119`、`app/connectors/social_auto_upload.py:78`（均 `import requests`）。二者均属**既有 connectors 模块，不在范围 A 的 4 个文件内**，范围 A 未引入任何第三方网络/模型库。✅
- **禁止业务使用**：`vector/embedding/connect_platform/manage_employees` → 仅命中 `database.py`（向量库工具目录元数据）、`department_catalog.py`（`connect_platform`/`manage_employees` 方法）。二者均为**既有模块，不在范围 A 文件内**。✅
- **不读凭证**：`d1_execute.py` 与 `d1_gateway_client.py` 均**不读取** `CURIS_MODEL_GATEWAY_API_KEY` 或任何凭证值；`R3GatewayClient` 仅消费注入的 `ModelGatewayAdapter` 实例（`main.py:917`：`R3GatewayClient(default_executor)`）。✅

### 2.4 既有契约不被破坏 — 通过

- D1 路由 `/api/workspace/internal/d1-tenant-reservation/run` 行为契约保持（仅加受控闸门，未改 URL/方法/成功体结构）。
- 单主执行：`d1_execute.py` 复用既有 `D1SingleModelToolchain.execute()`，其内部 `_claim_once` 占锁逻辑未被绕过（编排层不另造并发）。✅
- `/health` 不变。✅

---

## 三、测试重跑结果

```
platform darwin -- Python 3.13.12, pytest-9.1.1
collected 22 items

21 passed, 1 skipped, 1 warning in 0.48s
```

- 21 个用例全过（A2 R3GatewayClient 契约 6 + A3 编排层 status/execute 14 + A4 路由集成 2）。
- 1 个 `@pytest.mark.skip`：真实网关端到端（`test_real_gateway_end_to_end_is_blocked_until_ratified`），待安全边界席裁定凭证接入方式后补，符合设计（不硬编 Key、不读真实凭证）。
- 既有 D1 契约由 `test_d1_execute.py` 的 A4 路由集成测试直接覆盖（frozen→503、execute_disabled→503），其内 `assertNotIn("/", detail)` / `assertNotIn("sk-", detail)` / `assertNotIn("key", detail.lower())` 全部通过。

---

## 四、智能路由判定

- **源码 Bug（反馈工程师）**：无。降级逻辑方向正确、detail 无泄露、grep 无违规 import/凭证读取。
- **测试 Bug（QA 自行修复）**：无。断言正确、mock 得当（FakeGatewayClient / FakeToolchain 隔离充分）。
- **判定 → NoOne（全部通过）**。

> 环境性观察（**非范围 A 缺陷、不影响结论**）：重跑既有 `tests/test_d1_unfreeze.py` 时因 `from backend.app import local_rd_toolset` 在 `backend/` 根目录运行环境下无法解析（`No module named 'backend'`）而**收集失败**。该测试文件与 `local_rd_toolset.py` 均未被范围 A 改动（git diff 为空），属预先存在的测试导入配置问题，不在本次验证范围内。范围 A 的路由契约已由 `test_d1_execute.py` 独立覆盖并全过。

---

## 五、最终结论

### ✅ PASS

范围 A（D1 execute() 受控 gate 正式纳入：错误分类 / 降级状态 / 网关契约隔离）经独立第二层验证，**脱敏红线、降级与错误分类正确性、禁止区 grep、既有契约**四项全部达标；测试 21 passed / 1 skipped，无源码缺陷、无测试缺陷。建议可进入范围 A 闭环留痕，待安全边界席裁定 R3 凭证接入方式后补真实网关端到端用例。

**落盘**：本验证证据已写入 `reviews/20260720_d1_execute_a_qa.md`。
