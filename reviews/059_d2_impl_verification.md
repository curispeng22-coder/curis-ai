# Review 059 — D2.impl 部门真实实例化（Department Instantiation）: Implementation Verification

- **Reviewer seat**: 质量运行席（严过关 / Edward）
- **Target**: `backend/app/database.py`（additive 新增 `departments` 表）、`backend/app/department_catalog.py`（新增 `Department` dataclass + `create_department`/`list_departments`/`get_department`，落实 `instantiate_department` hook）、`backend/tests/test_d2_impl_department.py`（新增验收 + 禁止区守卫）；`backend/tests/test_d2_department.py`（一致性修正，仅删除一行过时断言）；边界 `docs/decisions/ADR-0026-d2-impl-department-instantiation.md`、切片 `issues/056_adr0017_d2_impl_department_instantiation.md`
- **Implementation commits**: `7617ed2c`（D2.impl 主实现，Kou 寇豆码）、`4ec02a59`（D2 reservation 契约测试一致性修正）
- **Date**: 2026-07-08
- **Result**: PASS-WITH-NOTES
- **智能路由判定**: NoOne（无源码 bug、无测试 bug；Notes 均为信息性 / 非阻断，无需路由 Engineer 修复或自检修正）

## Verification Scope

本验证为 **D2.impl（ADR-0017 第二个子决策 D2 的「部门真实实例化」实现切片）的实现验证**，独立（不抄实现者自检数字、不轻信测试内部 grep）核实 issue 056 的 AC1–AC10 是否真落地、禁止区是否真守严、基座 / 只读 facade 是否真未改。验证手段：

1. 本人独立实跑全量测试（`.venv/bin/python -m unittest discover tests`）；
2. 本人独立 grep 禁止区关键字（扫描 D2.impl 实际改动的 `database.py` / `department_catalog.py`，而非信任测试内部 `_grep_in_modified_files`）；
3. 逐条读码映射 AC 到真实实现（非仅读测试名）；
4. `git diff` 核查改动范围与 additivity、工作树清洁度、whitespace。

## 1. 全量测试实跑（backend/，独立重跑，未引用实现者数字）

- **结果：`Ran 114 tests in 1.742s — OK`（全绿，退出码 0）。** 本人独立执行 `cd backend && .venv/bin/python -m unittest discover tests`，输出 `Ran 114 tests in 1.742s / OK`，与基线宣称一致但由本人实证。
- 按测试文件拆解（`def test_` 行级计数，本人实测）：
  - **D2.impl 新增**：`test_d2_impl_department.py` = **14** 个用例 ✅（AC1–AC9 + D3/D4 facade 签名守卫，跨连接 round-trip + `type_key` KeyError + 单租户不变式 + 禁止区守卫全覆盖）
  - **D4 既有（10）**：`test_d4_governance.py` = 10
  - **D2 reservation 既有（9）**：`test_d2_department.py` = 9（含 `4ec02a59` 一致性修正，未增减用例数）
  - **D3 既有（9+9）**：`test_d3_event_log.py` = 9、`test_d3_observability.py` = 9
  - **D1 既有（7+6+3）**：`test_d1_role_wiring.py` = 7、`test_d1_tenant.py` = 6、`test_d1_verify_script.py` = 3
  - **其他既有**：`test_d2_sandbox.py` = 6、`test_role_context.py` = 3、`test_execution_engine.py` = 38
  - 合计 **38+3+7+6+6+9+14+3+10+9+9 = 114** ✅
- **工作树清洁**：`git diff --name-only HEAD -- backend/app` 为空，无未提交改动污染测试结果。✅

> ⚠️ 信息性差异（见 Notes N1）：commit `7617ed2c` message 与 issue 056 称本切片测试为「10 测试」，本人实测 `test_d2_impl_department.py` 实为 **14** 个 `def test_` 方法。不影响验收（114 真实全绿），仅文档计数口径不一致。

## 2. 禁止区独立扫描（本人实跑 grep，未引用测试内部 grep 结论）

扫描对象为 D2.impl 实际改动的两个文件 `backend/app/database.py` 与 `backend/app/department_catalog.py`（以 `git diff --name-only ca843bba HEAD` 确定的真实改动集为准）。

### 2.1 针对 `database.py` 的 forbidden 关键字扫描
模式：`manage_employees\(|connect_platform\(|WHERE department_id|insert into evolution_events|\.record\(|manage_department_types\(|auto_modify_code|vector|embedding|requests?\.(get|post)|credential|secret|roi_schema|token-output-ratio|insert into department_types|update department_types|delete from department_types`
→ **零命中**（ripgrep 返回 No matches）。✅
- 唯一 `department_types` 引用为第 234 行 `create table if not exists department_types`（建表，ADR-0023 基线）与第 329 行 `"insert or ignore into department_types "`（幂等种子，基线）——经 `git show ca843bba:backend/app/database.py` 确认二者在 D2.impl 之前已存在，**非本切片新增写路径**。AC8「department_types 写：零命中（新）」满足。✅

### 2.2 针对 `department_catalog.py` 的 forbidden 关键字扫描
模式：`manage_employees\(|connect_platform\(|WHERE department_id|insert into evolution_events|\.record\(|manage_department_types\(|auto_modify_code|vector|embedding|requests?\.(get|post)|credential|secret|roi_schema|token-output-ratio`
→ **仅 2 处命中，均为 `def` 占位**：
  - `department_catalog.py:231` `def connect_platform(...)` → 函数体 `raise NotImplementedError`（禁止区，绝对保留）
  - `department_catalog.py:237` `def manage_employees(...)` → 函数体 `raise NotImplementedError`（禁止区，绝对保留）
- 无任何对两者的**调用点**、无写路径、无 credential/secret/外部 SDK（`requests`/外部 HTTP）。✅
- `vector` / `embedding` / `auto_modify_code` / `roi_schema` / `token-output-ratio` / `manage_department_types(` / `insert into evolution_events` / `\.record\(` / `WHERE department_id` 全部零命中。✅

### 2.3 仓库级新 endpoint 扫描
模式：`app\.(get|post|put|delete)\(\s*["']/api/depart`，范围 `backend/app/*.py`
→ **零命中**（未新增任何 department API endpoint）。✅

**结论：AC8 禁止区独立扫描全绿**（Employee CRUD 仅占位 NotImplementedError、无 employees 表/写；外部平台仅占位 NotImplementedError、无凭证/SDK；无 L6/ROI、无 auto_modify_code、无 manage_department_types 真实调用、无 department_types 新增写、无新 endpoint、无 evolution_events 写、无向量/embedding）。

## 3. 逐条映射 AC1–AC10 到真实代码（读码核实，非读测试名）

- **AC1** ✅ `database.py:248-256` 在 `initialize()` 的 `executescript` 内 `create table if not exists departments`，列恰好 7 个：`department_id`(PK,text)、`tenant_id`(text not null default 'default')、`type_key`(text not null)、`display_name`(text not null)、`status`(text not null default 'active')、`created_at`/`updated_at`(text not null default current_timestamp)；无任何 `references`/外键子句（**无 FOREIGN KEY**）。`department_types` 种子由 `_seed_department_catalog`（`:299-334`）以 `INSERT OR IGNORE` 幂等写入 4 个规范类型，不被改写；测试 `test_departments_table_exists_with_seven_columns_and_no_fk` 断言 7 列 + 4 行种子，已随 114 全绿通过。✅
- **AC2** ✅ `department_catalog.py`：新增 `Department` dataclass（`:52-66`，7 字段与表列一一对应）；`create_department`（`:130-183`）、`list_departments`（`:185-200`）、`get_department`（`:202-219`）三方法签名/行为与 issue 一致。既有 `list_types`（`:79-90`）、`get_manifest`（`:92-106`）、`assemble_company_topology`（`:108-127`）**签名与实现均未改动**（D4 reservation 兼容）。✅
- **AC3** ✅ `create_department("business.general","华东业务部")`：`:147-152` 断言单租户不变式后，`resolved_tenant_id` 缺省取 `TenantContext.current_tenant_id()` → `'default'`；`type_key` 透传；`status` 默认 `'active'`；`department_id` 缺省 `uuid.uuid4().hex`（非空）；`created_at`/`updated_at` 由 DB `default current_timestamp` 回填（非空）。测试 `test_create_department_returns_valid_department` 断言 `tenant_id=='default'`、`type_key=='business.general'`、`status=='active'`、id/时间戳非空，已通过。✅
- **AC4** ✅ `create_department` `:154-158`：若 `get_manifest(type_key) is None` → `raise KeyError(f"未知部门类型 type_key=...")`。测试 `test_create_department_unknown_type_key_raises_keyerror`（"unknown.dept"）已通过。✅
- **AC5** ✅ 跨连接真实落库 round-trip：测试 `test_cross_connection_round_trip_persistence` 先 `create_department`，再 `db2 = Database(self.db.path)`（同 SQLite 文件、新连接）`connect()` 后 `catalog2.list_departments()` 含该实例、`catalog2.get_department(id)` 返回且字段正确——证明真持久化（非内存）。112 行 `insert into departments ...` 后 177 行 `select ... where department_id = ?` 回读，DB 落库路径真实。✅
- **AC6** ✅ `instantiate_department`（`:222-228`）已落实为 `return self.create_department(*args, **kwargs)`（不再 `NotImplementedError`）；`connect_platform`（`:231-235`）/`manage_employees`（`:237-241`）仍 `raise NotImplementedError`。测试 `test_instantiate_department_delegates_and_forbidden_hooks_raise` 已通过。✅
- **AC7** ✅ 单租户不变式：`create_department` `:147` `assert not TenantContext.is_multi_tenant()` 且 `:150-152` `tenant_id` 缺省 `'default'`，不引入多租户隔离逻辑（无 `WHERE tenant_id` 过滤之外的隔离代码）。`tenant_context.py`（D1 基座，未被本切片改动）`current_tenant_id()` 仍 `'default'`（`:29-31`）、`is_multi_tenant()` 仍 `False`（`:49-52`）。测试 `test_single_tenant_invariant` 断言所有行 `tenant_id=='default'` + 两者不变式，已通过。✅
- **AC8** ✅ 见 §2 独立扫描——全绿。另：D3 `evolution_event_log.py`、D4 `governance.py` 既有 `record`/`apply_proposal` 非本切片代码，不在 D2.impl 改动文件内，与 AC8 不冲突（与 review 058 N3/N4 同口径）。✅
- **AC9** ✅ D3 `DepartmentObservability` 与 D4 `CompanyGovernance` 仍可 import（测试 `test_d3_d4_facade_importable_and_signatures_preserved` 通过）；其公开方法（`get_department_event_stream`/`get_department_metrics`/`suggest_self_improvement` 与 `get_governance_scope`/`list_company_departments`/`propose_department_toggle`/`list_governance_audit`/`apply_proposal`/`manage_department_types` 含 LOCKED）签名未变；`assemble_company_topology`（`:108-127`）仍返回内存 `CompanyTopology`（不持久化）。`git diff --name-only ca843bba HEAD` 确认这两文件未被改动。✅
- **AC10** ✅ 后端回归 **114 全绿**；既有测试未被错误修改——`git diff --name-only ca843bba HEAD` 仅 4 文件（database.py / department_catalog.py / test_d2_department.py / test_d2_impl_department.py）；`test_d2_department.py` 一致性修正仅删除一行过时 `assertNotIn("departments", tables)` + 补注（见 §4），用例数仍为 9；`database.py` 改动纯 additive 建表（见 §4）。✅

## 4. 一致性审查（diff / 范围 / whitespace）

- **改动范围严格受控**：`git diff --name-only ca843bba HEAD` → 仅
  `backend/app/database.py`、`backend/app/department_catalog.py`、`backend/tests/test_d2_department.py`、`backend/tests/test_d2_impl_department.py`。
  与 issue 056 Allowed files 完全一致；Forbidden files 全部未出现。✅
- **基座 / 只读 facade 零改动（AC10 硬门禁）**：`git diff --name-only ca843bba HEAD -- backend/app/department_observability.py backend/app/governance.py backend/app/tenant_context.py backend/app/evolution_event_log.py backend/app/department_manifest.py backend/app/employee.py` → **空**。D1/D3/D4 基座与 facade 接口完好。✅
- **`database.py` 纯 additive 建表（AC10）**：`git diff ca843bba 7617ed2c -- backend/app/database.py` 实际新增内容仅为 `departments` 表的 `CREATE TABLE IF NOT EXISTS`（含注释块，约 `+14` 行）；**无任何既有表的 DROP / ALTER / 列变更**，无 seed 改动，`department_types` 种子保持基线幂等。✅
- **`test_d2_department.py` 一致性修正透明**：`git show 4ec02a59` 显示仅（a）删除 `self.assertNotIn("departments", tables)` 一行过时断言；（b）在原注释处补注「D2.impl 已新增 departments 表，故本断言不再含 departments，仅守卫 companies/company_topology 不新建」。无逻辑改动、无用例增减。✅
- **Import 一致、无孤儿引用**：`department_catalog.py` 顶部 `from .database import Database` / `from .department_manifest import DepartmentManifest` / `from .tenant_context import TenantContext` 三者均被实际消费（Database 用于构造与 connect；DepartmentManifest 用于 `_row_to_type` 占位 manifest；TenantContext 用于 `current_tenant_id()` / `is_multi_tenant()` 断言）。无孤儿 import。✅
- **whitespace**：`git diff --check` 对两个实现 commit 均无报错。✅

## Notes（信息性，非阻断；不影响 accept）

- **N1（INFO，文档计数口径不一致，非代码问题）**：commit `7617ed2c` message 与 issue 056 文本称本切片验收测试为「10 测试」，本人实测 `backend/tests/test_d2_impl_department.py` 含 **14** 个 `def test_` 方法（AC1 表结构、AC2 创建、AC3 KeyError、AC4 跨连接 round-trip、AC5 实例 hook + 两 forbidden hook、AC6 单租户不变式、AC7×7 禁止区守卫、AC9 D3/D4 facade 守卫）。同时 commit message 的「基线 100 + D4 10 + D2.impl 10 + 旧契约修正」加法并不严格等于 114（实为 post-D4 基线 100 + D2.impl 14 = 114）。**真实全量 = 114 全绿已由本人独立实证**，计数文档差异纯属措辞，无需改码。
- **N2（INFO，禁止区扫描口径透明）**：本验证的 forbidden-scope 独立扫描以 `git diff --name-only ca843bba HEAD` 确定的真实改动文件（`database.py` / `department_catalog.py`）为对象，而非信任测试内部 `_grep_in_modified_files`；并额外对全 `backend/app` 做 endpoint 仓库级扫描。结论与测试内部守卫一致且更严（覆盖 `credential`/`secret`/`roi_schema`/`token-output-ratio` 等测试未列的关键字），全部零命中。
- **N3（INFO，工作树透明披露）**：`git status --short` 含若干预存未跟踪文件（`??`，如 `docs/decisions/ADR-0017-*.md`、`backend/tests/test_d1_verify_script.py`、`*.DS_Store`、`.agents/`、`.workbuddy/` 等），**均非 D2.impl 改动、且 `backend/app/*.py` 无任何 `M/D` 状态**；D2.impl 两个 commit 仅新增 / 修正所述 4 文件。仅作透明披露，非风险。
- **N4（INFO，单租户断言副作用提示）**：`create_department` 在 `:147` 以 `assert not TenantContext.is_multi_tenant()` 守卫单租户不变式。该 `assert` 仅校验当前 `False` 旗帜、不依赖被改模块，且 `tenant_context.py` 未被本切片改动；未来 D1.x 多租户 slice 放开旗帜时此断言会正确阻断——属预期行为，非缺陷。

## Routing

**NoOne** —— 全部 AC1–AC10 逐条读码核实通过；禁止区独立扫描（本人实跑，覆盖测试未列关键字）全绿；全量测试 **114 独立实证全绿**；`database.py` 纯 additive 建表、基座 / 只读 facade 零改动；whitespace 干净、工作树清洁。无源码 bug、无测试 bug。Notes N1–N4 均为信息性 / 非阻断观察（最关键 N1 为「测试计数 14 vs 文档称 10」的纯文档口径差异，真实 114 全绿已实证，明确无需改码）。实现验证通过，转主理人 accept。

## Conclusion

D2.impl 部门真实实例化实现验证 **PASS-WITH-NOTES**：实现严格遵循 ADR-0026 边界——`database.py` 以 **additive** 方式新增公司级 `departments` 聚合根表（7 列、无 FK、无 seed、复用 D1 `tenant_id` 预留列且恒 `'default'`），`department_catalog.py` 新增 `Department` dataclass 与 `create_department`/`list_departments`/`get_department` 三真实落库方法并落实 `instantiate_department` hook（委派 `create_department`），`connect_platform`/`manage_employees` 仍保留为禁止区 `NotImplementedError`；跨连接 round-trip 证明真持久化；单租户不变式、`department_types` 种子幂等、D3/D4 facade 接口、无新 API endpoint、无 `evolution_events` 写、无向量/embedding 全部保持。唯一非阻断观察为验收测试实际 14 例（文档称 10）的计数口径差异，真实 114 全绿已由本人独立实证，无需改码。

## Handoff

实现验证 **PASS-WITH-NOTES** → 主理人（齐活林）accept D2.impl 部门真实实例化切片 → ADR-0017 四个子决策中 D1✅ D2✅(reservation + 本 impl) D3✅ D4✅ 全部收口。后续真实增强（Employee CRUD / 外部平台接入 / L6 ROI / `manage_department_types` 落地 / `evolution_events` 审计写 / 多租户隔离 / 新 API endpoint / 向量内存）均须各自独立小 gate + 总控决策席 + 安全边界席 review，不得借本切片夹带落地。Notes **N1–N4** 均为信息性提示，供 accept 时知悉，**非阻塞、无需代码改动**。
