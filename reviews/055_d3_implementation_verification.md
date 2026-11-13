# Review 055 — D3 职能型部门「自可观测 / 元循环」（设计预留 / Reservation）: Implementation Verification

- **Reviewer seat**: 质量运行席
- **Target**: `backend/app/department_observability.py` (new, 121 行) + `backend/tests/test_d3_observability.py` (new, 166 行)；复用基座 `backend/app/evolution_event_log.py`、`backend/app/department_catalog.py`、`backend/app/tenant_context.py`
- **Date**: 2026-07-08
- **Result**: PASS-WITH-NOTES
- **智能路由判定**: NoOne（无源码 bug、无测试 bug；Notes 均为信息性 / 非阻塞，无需路由 Engineer 或自检修正）

## Verification performed（独立核实，未抄工程师自检）

### 1. 全量测试实跑（backend/，`.venv/bin/python -m unittest discover tests`）
- **结果：Ran 90 tests in 1.496s — OK**（全绿，退出码 0）。
- 按测试文件拆解（`def test_` 行级计数）：
  - **D3 新增**：`test_d3_observability.py` = **9** 个用例 ✅
  - **基线（81）**：`test_execution_engine.py`=38、`test_d2_department.py`=9、`test_d3_event_log.py`=9、`test_d2_sandbox.py`=6、`test_d1_role_wiring.py`=7、`test_d1_tenant.py`=6、`test_d1_verify_script.py`=3、`test_role_context.py`=3
  - 合计 **81 基线 + 9 D3 = 90**，与任务口径、commit `22c5cd55` message 一致。
- **未修改任何既有测试**：`git diff --name-only HEAD~1 HEAD -- backend` 仅 2 个文件且均为新增（`department_observability.py`、`test_d3_observability.py`）；`git status --short backend/app` 无任何 `M/D` 状态（仓库级仅有若干预存未跟踪文件，详见 Notes N1，不含 `backend/app/*.py` 改动）。既有 81 测试零改动。

### 2. 禁止区独立扫描（本人实跑 grep，未引用工程师结论）
- **扫描 1**（`WHERE department_id` 及 `/api/observ` endpoint）：
  `grep -rnE "WHERE department_id|app\.(get|post|put|delete)\(\"/api/observ" backend/app` → **零命中**（exit=1）。✅
- **扫描 2**（facade 内写语句）：
  `grep -rnE "\.record\(|insert into|update |delete from" backend/app/department_observability.py` → **零命中**（exit=1）。确认 facade 只读、不调 `EvolutionEventLog.record`、不写。✅
- **database.py 零改动（可逆证明）**：`git diff --name-only HEAD~1 HEAD -- backend` 输出中**不含 `database.py`**；`git status --short backend/app` 亦无 `database.py` 改动。本 slice 仅新增 2 文件，`database.py` 不在其中 → 零 schema 增量、完全可逆。✅

### 3. 逐条映射 AC 1–8 到真实代码（读码核实，非读测试名）
- **AC1** ✅ `department_observability.py:49` 声明 `class DepartmentObservability`；`:62-64` 定义 `get_department_event_stream(self, type_key, limit=50)`；`:92` 定义 `get_department_metrics(self, type_key)`；`:110-121` 定义 `suggest_self_improvement` future hook（仅签名占位、抛 `NotImplementedError`）。测试 `test_d3_observability.py:83-89` 用 `hasattr` + `assertRaises(NotImplementedError)` 断言三方法存在且 future hook 占位。
- **AC2** ✅ `get_department_event_stream("function.admin", 10)`：`:78-79` 经 `DepartmentCatalog(self.database).get_manifest(type_key)` 校验索引；`:80-84` 未知 key → `manifest is None` → 抛 `KeyError`（经 catalog `get_manifest` 返回 `None` 转 `KeyError`，与边界验证 N1 约定一致）；`:87-90` `events = self.event_log.get_all()` 取全量只读投影、截断至 `events[-limit:]` 返回 `list[dict]`。元素字段含 `event_id`/`correlation_id`/`event_type`/`payload`/`created_at`（D1 另带 `tenant_id` 列，测试用 `.issubset` 子集断言，`:101-104`，兼容）。测试 `:92-104` 播种 25 条事件、断言 `len==10` 且每元素含 5 字段子集；`:106-108` 断言 `"function.unknown"` 抛 `KeyError`。
- **AC3** ✅ `get_department_metrics("function.bi")`：`:31-46` `DepartmentMetrics` dataclass，`available_fields` 默认 `["call_count","success_rate","quality_line_hits"]`、`schema_version="0.0"`；`:101-107` 内部调 `get_department_event_stream` 包裹、**不回填任何数值**。测试 `:111-132` 断言 `available_fields` 静态相等、实例上**不存在**名为 `call_count`/`success_rate`/`quality_line_hits` 的属性键（`:122-128` 查 `metrics.__dict__.keys()`）、且 `event_stream` 元素亦不含这些键（`:130-132`）——正确区分「静态声明字段列表」与「已计算数值字段」，呼应边界验证 N3。
- **AC4** ✅ 全代码库无 `WHERE department_id` 读路径过滤（扫描 1 零命中 + 测试 `:135-137`）。
- **AC5** ✅ 无新 `/api/observ` endpoint（扫描 1 零命中 + 测试 `:140-142`）。
- **AC6** ✅ `department_observability.py` 内无 `record(` / 无写语句（扫描 2 零命中 + 测试 `:145-152`）。注：测试文件 `:49` 调 `self.event_log.record(...)` 仅为播种测试数据，不在 facade 内，与 AC6 不冲突。
- **AC7** ✅ `TenantContext` 不变式保持：`tenant_context.py:29-31` `current_tenant_id()` 仍 `'default'`、`:49-52` `is_multi_tenant()` 仍 `False`；`department_observability.py` 全程**未 import / 未触碰 `TenantContext`**（读码确认无引用）。测试 `:155-157` 断言两者。
- **AC8** ✅ 后端回归绿（90 全绿）、未修改既有测试（git 核查见上）、禁止区扫描干净、`database.py` 零改动（git diff 不含 `database.py`）。

### 4. 一致性审查
- **Import 一致、无孤儿引用**：`department_observability.py:26-28` 正确 `from .database import Database` / `from .department_catalog import DepartmentCatalog` / `from .evolution_event_log import EvolutionEventLog`，三者均被实际消费——`Database` 用于 `__init__` 类型标注（`:58`）与 `DepartmentCatalog(self.database)`（`:78`）；`DepartmentCatalog` 用于索引校验（`:78-79`）；`EvolutionEventLog` 用于 `self.event_log.get_all()`（`:87`）；`DepartmentMetrics` 在本文件定义并被 `get_department_metrics` 返回（`:102`）。无孤儿 import。✅
- **`get_department_metrics` 复用 `get_department_event_stream` 且不回填数值**：`:101` 直接调 `self.get_department_event_stream(type_key)`，`:102-107` 仅包裹为 `DepartmentMetrics`（未计算、未赋值任何 call_count/success_rate/quality_line_hits）。✅
- **future hook 仅占位**：`suggest_self_improvement`（`:110-121`）仅签名 + `raise NotImplementedError`，未引用、无副作用、不触禁止区。✅
- **边界验证 N1 已被采纳**：本 slice 未在构造注入 `catalog`，而是按边界建议「facade 内部以 `DepartmentCatalog(self.database)` 复用目录索引」（`:78`），索引校验职责划分与 AC2 一致，无漏接。✅

## Notes（信息性，非阻塞；不影响 accept）

- **N1（INFO，工作树透明披露）**：`git status --short` 显示若干**预存未跟踪文件**（`??`，如 `docs/decisions/ADR-0017-*.md`、`backend/tests/test_d1_verify_script.py`、`*.DS_Store`、`.agents/`、`.workbuddy/` 等），**均非 D3 改动、且 `backend/app/*.py` 无任何 `M/D` 状态**。`backend/tests/test_d1_verify_script.py` 虽为未跟踪但属 D1 时代预存文件、被 unittest 发现并计入 90（含其 3 个用例），不在 D3 修改范围内。D3 的 `22c5cd55` commit 与 `git status --short backend/app` 均证实本 slice 仅新增 2 文件、未触碰任何既有文件。仅作透明披露，非风险。（参照 review 054 N5）
- **N2（INFO，边界 N3 已被测试采纳）**：AC3 实现与测试均正确区分「`available_fields` 静态字符串列表」与「`DepartmentMetrics` 实例上名为 `call_count`/`success_rate`/`quality_line_hits` 的已计算属性」，无混淆、无回填。边界验证 N3 的建议已在测试 `:120-132` 落实，无需后续动作。
- **N3（INFO，原生投影字段超集）**：`get_department_event_stream` 返回的是 `EvolutionEventLog.get_all()` 的原生投影，因 D1 在 `evolution_events` 预留了 `tenant_id` 列，元素实际字段为 `{event_id, correlation_id, event_type, payload, created_at, tenant_id}` 超集；测试用 `.issubset` 断言必需 5 字段（`:101-104`），与「只读投影、不建立部门→事件真实关联」意图一致，非缺陷。
- **N4（INFO，基线构成）**：本验证实跑基线为 81（相对 review 053 的 81 基线无变化——D3 之前 HEAD 已为 81，D3 仅新增 9 个 `test_d3_observability.py` 用例）。任务口径「81 基线 + 9 D3 = 90」在 HEAD（`22c5cd55`）下准确。

## Handoff

实现验证 **PASS-WITH-NOTES** → 主理人（产品规划席 delegation，齐活林）accept D3 reservation → 架构师（Bob）出 **D4 边界**（ADR-0017 D4 两级治理 / 部门 manifest 演进边界）→ 同管线推进（边界验证 → 实现 → 实现验证）。Notes **N1–N4** 均为信息性提示，供 gate/accept 时知悉，**非阻塞、无需代码改动**。真实 D3 实现（真实指标关联 / 统计 / 可视化 / meta-loop 自愈 / Employee CRUD / 外部平台）必须各自独立小 gate（建议 `D3.impl`）+ 总控决策席批准并触发**安全边界席 review**，不得借本 reservation slice 夹带落地。本 slice 零 schema 增量、零 `database.py` 改动、完全可逆。
