# Review 053 — D2 部门目录通用化（设计预留 / Reservation）: Implementation Verification

- **Reviewer seat**: 质量运行席
- **Target**: `backend/app/database.py` (增量 `department_types` 建表 + `_seed_department_catalog`)、`backend/app/department_manifest.py` (new)、`backend/app/department_catalog.py` (new)、`backend/tests/test_d2_department.py` (new)
- **Date**: 2026-07-07
- **Result**: PASS-WITH-NOTES
- **智能路由判定**: NoOne（无源码 bug、无测试 bug；Notes 均为非阻塞质量项）

## Verification performed（独立核实，未抄工程师自检）

### 1. 全量测试实跑（backend/，`.venv/bin/python -m unittest discover tests`）
- **结果：Ran 81 tests in 1.556s — OK**（全绿，退出码 0）。
- 按测试文件拆解（行级计数 `def test_`）：
  - D2 新增：`test_d2_department.py` = **9** 个用例 ✅
  - 基线（其余全部，未改动）= **72**：`test_execution_engine.py`=38、`test_d3_event_log.py`=9、`test_d2_sandbox.py`=6、`test_d1_role_wiring.py`=7、`test_d1_tenant.py`=6、`test_role_context.py`=3、`test_d1_verify_script.py`=3（其余为 `__pycache__` 噪声）
  - 合计 **72 基线 + 9 D2 = 81**，与任务口径一致。
- **未修改任何既有测试**：`git diff --name-only -- backend/tests` 输出为空（无未提交改动）；`git show --stat c8a30781` 仅 4 个文件且 `backend/tests/` 下只新增 `test_d2_department.py`。

### 2. 禁止区独立扫描（本人实跑 grep，未引用工程师结论）
- **扫描 1**（`WHERE department_id` 及 `/api/department` endpoint）：
  `grep -rnE "WHERE department_id|app\.(get|post|put|delete)\(\"/api/department" app` → **零命中**（exit=1）。
- **扫描 2**（`employee` 引用，限 `department_*.py`）：
  仅出现在 `employee_role_spec` 契约字段声明（`department_manifest.py:27,46,63`）与 `manage_employees` future hook 占位签名（`department_catalog.py:123,126`）。**无任何真实员工 CRUD / 读取 / 写入逻辑**。✅
- **扫描 3**（`departments|company_topology|companies`，限 `database.py` + `department_*.py`）：
  命中均为注释或方法名——`database.py:233`（注释「departments 聚合根表本 slice 不创建」）、`department_catalog.py:8`（docstring 注释）、`department_catalog.py:89`（`assemble_company_topology` 方法名，纯内存投影）。**无 `departments` / `company_topology` / `companies` 持久化建表**。✅
- **future hook 调用性**：全代码库 grep `instantiate_department|connect_platform|manage_employees` 仅在 `department_catalog.py` 内有 3 处定义（L111/117/123）+ 编译缓存，无任何调用点。✅

### 3. 逐条映射 AC 1–8 到真实代码（读码核实，非读测试名）
- **AC1** ✅ `department_types` 表存在且列齐全：`database.py:234-242` 建表，列 = `type_key`(PK) / `category`(NOT NULL) / `display_name`(NOT NULL) / `description` / `manifest_json`(NOT NULL DEFAULT '{}') / `manifest_schema_version`(NOT NULL DEFAULT '0.0') / `is_system`(NOT NULL DEFAULT 1)；测试 `test_d2_department.py:98-103` 用 `pragma table_info` 断言列集合相等。
- **AC2** ✅ 恰好 4 行规范类型且 `manifest_json` 为占位：`database.py:292-313` 定义 `business.general`/`function.hr`/`function.admin`/`function.bi`，每行 `manifest_json="{}"`；`:314-320` `INSERT OR IGNORE`；测试 `:106-117` 断言 `len==4`、key 集合匹配、解析为 `{}`。
- **AC3** ✅ `MANIFEST_FIELDS` 含 7 键：`department_manifest.py:20-28` 声明 `capability_set`/`tool_classes`/`quality_lines`/`output_channels`/`roi_schema`/`guardrail_refs`/`employee_role_spec`；测试 `:120-121` 断言等价。
- **AC4** ✅ Catalog facade 行为正确：`list_types()`（`department_catalog.py:60-71`）SELECT 全表返回非空；`get_manifest("business.general")`（`:73-87`）返回占位 `DepartmentManifest`（字段空结构）；`assemble_company_topology()`（`:89-108`）返回内存 `CompanyTopology`，未知 key 被忽略；测试 `:124-159` 断言占位字段为空 + `companies`/`company_topology`/`departments` 表均不存在。
- **AC5** ✅ 全代码库无 `WHERE department_id` 读路径过滤（扫描 1 零命中 + 测试 `:166-171`）。
- **AC6** ✅ 无新 `/api/department` endpoint（扫描 1 零命中 + 测试 `:174-179`）。
- **AC7** ✅ `TenantContext` 不变式保持：`tenant_context.py:29-31` `current_tenant_id()` 仍 `'default'`、`:49-52` `is_multi_tenant()` 仍 `False`（相对 D1 零改动）；测试 `:161-163` 断言。
- **AC8** ✅ 后端回归绿（81 全绿）、未修改既有测试（git 核查见上）、禁止区扫描干净。

### 4. 一致性审查
- `department_catalog.py:23-24` 正确 `from .database import Database` / `from .department_manifest import DepartmentManifest`；`:141-156` `_row_to_type` 实际消费两者，无孤儿 import。✅
- `database.py:256` `initialize()` 在 D1 `tenant_id` 列预留（`:250-251`）之后确实调用 `self._seed_department_catalog(connection)`。✅
- 种子幂等：`database.py:314-320` 使用 `executemany("insert or ignore ...")`，`initialize()` 可重复调用安全。✅

## Notes（非阻塞；不影响 accept）

- **N1（INFO，承 review 052 N4）**：`department_types` 刻意不做 `tenant_id` 隔离（系统级共享注册表，类比 `tools` 表，`database.py:231-233` 注释已声明）。这是对 ADR-0017 D1「所有聚合根预留 tenant_id」的有意偏离，已在本 ADR 论证（互补而非嵌套过滤）；实现与文档一致，非风险。
- **N2（MINOR，死代码）**：`department_catalog.py:130-139` `_parse_manifest_json` 已定义但未被调用——`_row_to_type`（`:141-156`）直接从行字段构造空结构 `DepartmentManifest`，不解析 `manifest_json` 内容，与「占位不消费」意图一致。该私有辅助为死代码，无害；建议未来清理或在 D2.impl 接线时复用。依据本验证「只验证不改动实现」约束，未自行删除。
- **N3（MINOR，风格偏差）**：ADR-0023 §1.3 将 3 个 future hook 建议为「注释掉的签名」，实现改为实际方法 `raise NotImplementedError`（`department_catalog.py:111/117/123`）。功能等价——未实现、未引用、无副作用、不触禁止区——属合规；仅建议与架构师确认未来 hooks 的呈现风格（注释 vs 可导入 stub），非阻塞。
- **N4（INFO，基线构成）**：本验证实跑基线为 72（相对 review 051 的 63 基线，后续新增了 `test_d3_event_log`=9、`test_d2_sandbox`=6、`test_d1_role_wiring`=7、`test_d1_verify_script`=3、`test_role_context`=3）。任务口径「72 基线 + 9 D2 = 81」在当前 HEAD（`c8a30781`）下准确。

## Handoff

实现验证 **PASS-WITH-NOTES** → 主理人（产品规划席代理，齐活林）accept D2 → 架构师出 D3 边界（元循环 / 自可观测，ADR-0017 D3）→ 同管线推进。Notes **N2 / N3** 为代码整洁项，建议工程师在后续 slice 顺手清理；**N1 / N4** 为信息性提示，供 gate/accept 时知悉，非阻塞。真实 D2 实现（部门实例化 / 外部平台 / L6 / Employee CRUD）仍需独立未来 gate（建议 `D2.impl`）+ 总控决策席 + 安全边界席 review。
