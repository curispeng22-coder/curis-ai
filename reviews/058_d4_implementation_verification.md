# Review 058 — D4 两级治理（Two-Tier Governance reservation）: Implementation Verification

- **Reviewer seat**: 质量运行席
- **Target**: `backend/app/governance.py` (new, 206 行) + `backend/tests/test_d4_governance.py` (new, 187 行)；复用基座 `backend/app/department_catalog.py` (D2)、`backend/app/evolution_event_log.py` (ADR-0016 D3)、`backend/app/tenant_context.py` (D1)
- **Date**: 2026-07-08
- **Result**: PASS-WITH-NOTES
- **智能路由判定**: NoOne（无源码 bug、无测试 bug；Notes 均为信息性 / 非阻断，无需路由 Engineer 修复或自检修正）

## Verification Scope

本验证为 **D4（ADR-0017 第四个子决策：两级治理 reservation）的实现验证**，独立于工程师（寇豆码 / Kou，commit `b97728d4`）自检，逐条核实 issue 055 的 AC1–AC10 是否真落地、禁止区是否真守严、基座签名是否真复用。验证手段：实跑全量测试、独立 grep 禁止区关键字、读码映射 AC 到真实实现（非仅读测试名）、一致性审查。

## 1. 全量测试实跑（backend/，`.venv/bin/python -m unittest discover tests`）

- **结果：Ran 100 tests in 1.730s — OK**（全绿，退出码 0）。
- 按测试文件拆解（`def test_` 行级计数）：
  - **D4 新增**：`test_d4_governance.py` = **10** 个用例 ✅（AC1–AC10 + 构造注入结构性自检）
  - **基线（90）**：`test_execution_engine.py`=38、`test_d3_event_log.py`=9、`test_d2_department.py`=9、`test_d2_sandbox.py`=6、`test_d1_role_wiring.py`=7、`test_d1_tenant.py`=6、`test_d1_verify_script.py`=3、`test_role_context.py`=3、`test_d3_observability.py`=9
  - 合计 **90 基线 + 10 D4 = 100**，与 commit `b97728d4` message「100 tests」一致。
- **未修改任何既有测试**：`git show --stat b97728d4` 仅 2 文件（均新增 `governance.py`、`test_d4_governance.py`，+393）；`git diff --name-only -- backend/app/database.py` 为空（零 schema 增量）。既有 90 测试零改动。

## 2. 禁止区独立扫描（本人实跑 grep，未引用工程师结论）

- **governance.py 专项扫描**（任务指定 8 关键字）：
  `grep -rnE "WHERE department_id|app\.(get|post|put|delete)\(\"/api/govern|\.record\(|insert into|update |delete from|manage_department_types\(|apply_proposal\(" backend/app/governance.py`
  → **仅 2 处命中，均为 `def` 签名占位**：
  - `governance.py:196` `def apply_proposal(...)`
  - `governance.py:202` `def manage_department_types(...)`
  - 其余关键字（`WHERE department_id` / `.record\(` / `insert into` / `update ` / `delete from` / `app.get("/api/govern"` / `app.post("/api/govern"`）**零命中**。✅
- **仓库级扫描（AC6/AC7）**：`grep -rnE "WHERE department_id|app\.(get|post|put|delete)\(\"/api/govern" backend/app` → **零命中**（exit=1）。✅
- 透明披露：D3 既有 `evolution_event_log.py` 的 `record()` 定义与 `governor_sandbox.py` 预存 `_apply_proposal` 非 D4 代码；D4 的 `governance.py` 不调用 `record`、不写任何表，与 AC5/AC6/AC7 不冲突（同 D3/D4 边界验证 N3/N4 结论）。

## 3. 逐条映射 AC1–AC10 到真实代码（读码核实，非读测试名）

- **AC1** ✅ `governance.py:81` 声明 `class CompanyGovernance`；`:103-118` `get_governance_scope`、`:120-143` `list_company_departments`、`:145-173` `propose_department_toggle`、`:175-193` `list_governance_audit`；`:196-200` `apply_proposal` 与 `:202-206` `manage_department_types` 为 future hook（`raise NotImplementedError`）。三 dataclass：`GovernanceScope`（`:34-51`）、`DepartmentGovernanceView`（`:54-64`）、`GovernanceProposal`（`:67-78`）。
- **AC2** ✅ `get_governance_scope(ceo_id, ["business.general","function.hr"])`（`:103-118`）：`:110` `topology = self._catalog.assemble_company_topology(...)` → D2 内存 `CompanyTopology`（不持久化）；`:114` `locked_actions=list(self.LOCKED_ACTIONS)`，其中 `LOCKED_ACTIONS`（`:90-95`）= `["manage_department_types","lift_human_approval_gate","auto_modify_code","cross_company_policy"]`（四动作齐备）；`:116` `selectable_type_keys=self._catalog.list_types()`。稳健比对：`set(t.type_key for t in scope.selectable_type_keys) == set(t.type_key for t in DepartmentCatalog(database).list_types())` → 两者同源相等，AC2 满足。⚠️ 表示层说明见 Notes N1。
- **AC3** ✅ `list_company_departments(ceo_id, ["business.general","function.hr"])`（`:120-143`）：按 `selected_type_keys` 投影为 `list[DepartmentGovernanceView]`，长度 = `len(selected_type_keys)` = 2；每元素 `requires_human_approval=True`（`:140`）。✅
- **AC4** ✅ `propose_department_toggle(ceo_id,"function.hr",False,selected)`（`:145-173`）：`:158-163` 经 `get_manifest(type_key)` 索引校验，未知 key 返回 `None` → 转 `KeyError`（与边界验证 N2 约定一致）；`:164-173` 返回 `GovernanceProposal`，`status="proposed"`（`:171`）、`requires_human_approval=True`（`:170`）、`proposed_at=datetime.now(timezone.utc).isoformat()`（`:169`，合法 UTC ISO8601）。未知 `type_key` 抛 `KeyError`。✅
- **AC5** ✅ `propose_department_toggle` 源码（`:145-173`）无 `record(`/`insert into`/`update `/`delete from`；仅调 `get_manifest` 与构造内存 `GovernanceProposal`，不写 `department_types`。独立 grep（§2）佐证零命中。✅
- **AC6** ✅ 全代码库无 `WHERE department_id` 读路径过滤（§2 仓库级扫描零命中 + 测试 `test_d4_governance.py:152-154`）。✅
- **AC7** ✅ 无新 `/api/govern` endpoint（§2 仓库级扫描零命中 + 测试 `:157-159`）。`governance.py` 全程无 `app.get/post/put/delete`。✅
- **AC8** ✅ `governance.py` 内对 `apply_proposal`/`manage_department_types` 无任何真实调用——仅有 `:196`、`:202` 两处 `def` 占位（均 `raise NotImplementedError`）；独立 grep（§2）确认仅 2 处 `def` 命中、无调用点。✅
- **AC9** ✅ `TenantContext` 不变式保持：`tenant_context.py`（D1）`current_tenant_id()` 仍 `'default'`、`is_multi_tenant()` 仍 `False`；`governance.py` 全程**未 import / 未触碰 `TenantContext`**（读码确认无引用）。测试 `:176-178` 断言两者。✅
- **AC10** ✅ 后端回归绿（100 全绿）、未修改既有测试（git 核查见 §1）、禁止区扫描干净、`database.py` 零改动（`git diff --name-only -- backend/app/database.py` 为空，零 schema 增量、完全可逆）。✅

## 4. 一致性审查

- **Import 一致、无孤儿引用**：`governance.py:29-31` 正确 `from .database import Database` / `from .department_catalog import CompanyTopology, DepartmentCatalog, DepartmentType` / `from .evolution_event_log import EvolutionEventLog`，三者均被实际消费——`Database` 用于 `__init__`（`:97`）；`DepartmentCatalog` 用于构造 `self._catalog`（`:100`）并调 `assemble_company_topology`/`list_types`/`get_manifest`；`EvolutionEventLog` 用于构造 `self._event_log`（`:101`）并调 `get_all()`（`:185`）；`CompanyTopology`/`DepartmentType` 用于类型标注（`:45`/`:50`）。无孤儿 import。✅
- **构造注入约定（边界 N1 已被采纳）**：`__init__` 仅注入 `database`（`:97-98`），内部以 `DepartmentCatalog(self.database)` / `EvolutionEventLog(self.database)` 复用基座（`:100-101`），与边界验证 N1 建议一致，无漏接、无假设 catalog/event_log 已注入。✅
- **`LOCKED_ACTIONS` 声明合规（边界 N2 已规避）**：实现将 `LOCKED_ACTIONS` 声明为**平级类属性列表字面量**（`:90-95`），未误用 `field(default_factory=...)`（边界草图曾有的 dataclass-only 语法隐患），正确。✅
- **future hook 仅占位**：`apply_proposal`（`:196-200`）/ `manage_department_types`（`:202-206`）仅签名 + `raise NotImplementedError`，未引用、无副作用、不触禁止区。✅
- **审计只读投影合规**：`list_governance_audit`（`:175-193`）经 `self._event_log.get_all()` 只读投影（`:185`），按 `event_type` 前缀 `'governance.'` 过滤（`:189`）、截断至 `limit`（`:191-192`），**不调 `record`、不新增写**，D3 追加写不变式保持。✅

## Notes（信息性，非阻断；不影响 accept）

- **N1（INFO，表示层与 diagram 措辞不一致但语义等价）**：`GovernanceScope.selectable_type_keys` 实现持有 `list[DepartmentType]`（`:50`，即 `DepartmentCatalog.list_types()` 真实返回），而 ADR-0025 类图中该字段标注为 `list[str]`（L383–397）。两者语义等价——AC2 以 `type_key` 集合比对即相等（§3 AC2）。实现采用真实返回类型更严谨，**无需改码**；仅建议后续若修订 ADR-0025 类图，将 `selectable_type_keys` 标注与真实返回对齐（信息性，非阻塞）。
- **N2（INFO，边界 N1 已采纳）**：`__init__` 内部构造 `self._catalog`/`self._event_log`（`:100-101`），与边界验证 N1 的「facade 内部复用基座」约定一致，实现正确，无后续动作。
- **N3（INFO，边界 N2 已规避）**：`LOCKED_ACTIONS` 以平级类属性列表字面量声明（`:90-95`），规避了边界草图中 `field(default_factory=...)` 用于非 @dataclass 类的语法隐患，实现正确。
- **N4（INFO，工作树透明披露）**：`git status --short` 含若干预存未跟踪文件（`??`，如 `docs/decisions/ADR-0017-*.md`、`backend/tests/test_d1_verify_script.py`、`*.DS_Store`、`.agents/` 等），**均非 D4 改动、且 `backend/app/*.py` 无任何 `M/D` 状态**；commit `b97728d4` 仅新增 2 文件、未触碰任何既有文件，`database.py` 零 delta。仅作透明披露，非风险（参照 review 055 N1）。

## Routing

**NoOne** —— 所有 AC1–AC10 逐条读码核实通过，禁止区独立扫描干净（仅 2 处 `def` 占位、无写/端点/WHERE 命中），全量测试 100 全绿，零 schema 增量；无源码 bug、无测试 bug。Notes N1–N4 均为信息性 / 非阻断观察（最关键的 N1 为表示层与 ADR 类图措辞不一致但语义等价，明确无需改码）。实现验证通过，转主理人 accept。

## Conclusion

D4 两级治理 reservation 实现验证 **PASS-WITH-NOTES**：实现严格复用 D2 `DepartmentCatalog`/`CompanyTopology` 与 ADR-0016 D3 `EvolutionEventLog.get_all()` 作为 CEO 级治理作用域边界与审计只读接缝；`CompanyGovernance` 仅只读作用域 + 受限提案，无持久化、不解除 gate、不自动改码、不实例化、不接外部；`LOCKED_ACTIONS` 四动作锁定声明齐备，future hook 仅 `NotImplementedError` 占位；D1 `TenantContext` 不变式完好；`database.py` 零改动、完全可逆。唯一非阻断观察为 `selectable_type_keys` 表示层（`list[DepartmentType]` vs ADR 类图 `list[str]`）措辞差异，语义等价且 AC2 满足，无需改码。

## Handoff

实现验证 **PASS-WITH-NOTES** → 主理人（产品规划席 delegation，齐活林）accept D4 reservation → ADR-0017 四个子决策（D1✅ D2✅ D3✅ D4✅）reservation 边界与实现全部收口。真实 D4 实现（提案落地 `apply_proposal` / 平台级管理后台 `manage_department_types` / 真实公司持久化 / 解除任何 gate / 跨公司策略 / 外部平台）必须各自独立小 gate（建议 `D4.impl` / `D4.platform`）+ 总控决策席 + 安全边界席 review，不得借本 reservation slice 夹带落地。Notes **N1–N4** 均为信息性提示，供 gate/accept 时知悉，**非阻塞、无需代码改动**。
