# Review 056 — D4 两级治理（Two-Tier Governance）: Boundary Verification

- **Reviewer seat**: 质量运行席
- **Target**: `docs/decisions/ADR-0025-d4-two-tier-governance-boundaries.md` + `issues/055_adr0017_d4_two_tier_governance.md`
- **Date**: 2026-07-08
- **Result**: PASS-WITH-NOTES
- **智能路由判定**: NoOne（设计-only 边界，无后端代码泄漏、无 schema delta、无签名不一致 MUST-FIX；Notes 均为非阻塞设计一致性提示，转交架构师/工程师实现阶段采纳）

## Verification Scope

本验证为 **D4（ADR-0017 第四个子决策：两级治理 reservation）的边界验证（设计-only）**，不是代码验证——实现尚未编写（`governance.py` / `test_d4_governance.py` 尚不存在于磁盘）。验证对象仅为边界契约文件（`ADR-0025` + `issue 055`），逐条核对任务给定的 A–F 六项目标，并独立佐证「零后端代码泄漏 / 零 schema delta / 禁止区合规 / 复用基座签名匹配 / 无新 endpoint / 任务清单自洽」。禁止区扫描与 git 核查均独立实跑，未引用边界文档自身结论。

## Checks Performed

### A. 设计-only / 零后端代码泄漏
- `git status --short backend/app/` → **空**（无任何 `backend/app/*.py` 改动/新增）。✅
- `git diff --stat` → 空（工作树相对 HEAD 无已提交改动）。✅
- `git status --short` 全量未跟踪项仅含文档：`docs/decisions/ADR-0025-d4-two-tier-governance-boundaries.md`、`issues/055_adr0017_d4_two_tier_governance.md`，**无 `backend/app/` 任何文件**。✅
- `ls backend/app/governance.py` → 不存在（设计-only 正确状态）。✅
- **结论：本边界仅新增 docs + issues，零后端代码泄漏。A 通过。**

### B. 零 schema delta
- `issue 055` Allowed Files（L38–45）仅列 `governance.py` (new)、`test_d4_governance.py` (new)、`ADR-0025`、`issue 055`；**`database.py` 明确不在列**（L45 注释：「本 reservation 零 schema 增量」）。✅
- `ADR-0025` §2 文件清单（L265–274，注 L274）同样排除 `database.py`。✅
- `git diff --name-only -- backend/app/database.py` → 空（零 schema 增量、可逆性证明，与 D3 同构）。✅
- ADR-0025 系统设计中无任何 `CREATE TABLE` / `ALTER` / 新增表列（仅复用既有 `department_types` 与 `evolution_events`）。✅
- **结论：B 通过（零 schema delta）。**

### C. 禁止区合规
- ADR-0025 Forbidden Scope（L198–211）逐条覆盖：平台级后台 / 解除 gate / 自动改码 / 真实实例化 / 外部平台 / L6 ROI / Employee CRUD / 新增写路径 / 新 endpoint / 多 Agent / 向量库 / 触碰 D1 `TenantContext` / 触碰 `department_types` 增删 / `WHERE department_id` 过滤，均列为禁止。
- 未来 gate 排除清单（L186–196）明确 `apply_proposal` / `manage_department_types` 等实现留待 `D4.impl` / `D4.platform`，并触发安全边界席 review。
- `LOCKED_ACTIONS` 已声明（L113–118）：`["manage_department_types","lift_human_approval_gate","auto_modify_code","cross_company_policy"]` —— 四个锁定动作齐备。✅
- future hook 仅签名占位：`apply_proposal`（L152–153）、`manage_department_types`（L155–156）均标注「本 reservation 不实现」，按 issue 055（L16）约定抛 `NotImplementedError`。✅
- **结论：C 通过（禁止区设计上完整且锁定声明到位）。**

### D. 复用基座签名匹配
逐方法核对 ADR-0025 对既有基座的调用签名，全部与磁盘真实实现一致（详见「Reused-Base Signature Match」节）：
- `DepartmentCatalog.list_types()` / `get_manifest(type_key)` 真实存在且签名一致。✅
- `CompanyTopology` 字段（`ceo_id` / `selected_type_keys` / `manifests` / `assembled_at`）与 ADR-0025 `GovernanceScope.topology` 及 `list_company_departments` 投影 `topology.manifests` 一致；**ADR 复用同一 `CompanyTopology`，未新建拓扑类**。✅
- `EvolutionEventLog.get_all()` 真实存在；ADR-0025 `list_governance_audit` 的「`get_all()` 只读投影 → 按 `event_type` 前缀 `'governance.'` 过滤 → 截断至 `limit`」调用方式与 D3 `department_observability.py` 的 `self.event_log.get_all()` 用法（L87）一致。✅
- **结论：D 通过（无签名不一致，无 MUST-FIX）。**

### E. 无新 API 端点 / 无 WHERE department_id / 无 record() 写
- 新 facade 设计为只读 + 受限提案：ADR-0025 系统设计中「复用 FastAPI（仅既有 endpoint，不新增任何路由）」（L258）；Forbidden L207 禁新 endpoint。✅
- 无 `WHERE department_id` 过滤：Invariant L179「全代码库无新增读路径 WHERE department_id = ?」；Forbidden L211 同。✅
- 无 `record()` 写：`propose_department_toggle` 仅构造内存 `GovernanceProposal`（L161、L177–178），`list_governance_audit` 仅只读投影（L162、L142–149），二者**均不调用 `EvolutionEventLog.record`**；事件日志追加写不变式保持（L169）。✅
- 独立扫描佐证：`grep -rnE "WHERE department_id|app\.(get|post|put|delete)\(\"/api/govern|manage_department_types\(|apply_proposal\(" backend/app` → 仅在 `governor_sandbox.py`（预存在的 Evolution Governor 沙箱，非 D4 代码，详见 Findings N3）出现 `_apply_proposal` 字样，无 D4 泄漏、无 `/api/govern` endpoint、无 `WHERE department_id`。✅
- **结论：E 通过。**

### F. 任务清单自洽
- T01–T04（L451–456）均为 additive：`governance.py` (new) + `test_d4_governance.py` (new)，不涉及 `database.py`。✅
- 依赖顺序正确：T01（无依赖）→ T02（依赖 T01）→ T03（依赖 T01,T02）→ T04（依赖 T01–T03），与 D3 T01–T04 同构；T02 实现四个读方法、T03 补断言与禁止区扫描。✅
- **结论：F 通过。**

## Findings

- **N1（mirror D3 review 054 N1，非阻塞）**：`CompanyGovernance.__init__(self, database: Database)`（L120–121）仅注入 `database`，但需调用 `DepartmentCatalog.assemble_company_topology/list_types/get_manifest` 与 `EvolutionEventLog.get_all()`。与 D3 `DepartmentObservability` 同构，未来实现须**在 facade 内部以 `DepartmentCatalog(self.database)` / `EvolutionEventLog(self.database)` 复用基座**（而非假设已注入）。建议 ADR/issue 在「共享知识」(L474–486) 或 T02 显式写明该内部构造约定，避免 Engineer 误判注入关系。（非阻塞，实现阶段采纳）
- **N2（mirror D3 review 054 N1 语义，非阻塞）**：`DepartmentCatalog.get_manifest(type_key)` 对未知 key **返回 `None`（不抛异常）**（`department_catalog.py` L85–86）。ADR-0025 要求 `propose_department_toggle` 对未知 `type_key` **抛 `KeyError`**（L161、Invariant L177）。该「None→KeyError」转换责任已明确落在未来 facade 内部（与 D3 一致），非缺陷；建议测试作者断言「facade 抛 KeyError」而非「`get_manifest` 抛 KeyError」。（非阻塞）
- **N3（透明披露，INFO）**：独立 forbidden-scope grep 在 `backend/app/governor_sandbox.py:35,66` 命中 `_apply_proposal`（预存在的 Evolution Governor 沙箱方法），**非 D4 `CompanyGovernance.apply_proposal` future hook、非 D4 代码**——`git status backend/app` 为空、`governor_sandbox.py` 不在 D4 Allowed Files，确认非 D4 泄漏。仅作透明说明，不构成禁止区违规。（信息性）
- **N4（透明披露，INFO）**：`evolution_event_log.py` 的 `record()` 内含合法 `insert into evolution_events`（L25），属 D3 基座既有写方法，**非 D4 新增**；D4 `list_governance_audit` 严禁调用 `record`（L162、L169、L178），设计上已守住该不变式。（信息性）

## Forbidden-Zone Compliance

| 禁止项（ADR-0025 L198–211 / L186–196） | 边界处置 | 证据 |
|---|---|---|
| 平台级后台 / `manage_department_types` 增删 | 仅 future hook 占位（NotImplementedError） | L155–156 |
| 解除 human-approval gate / 自动改码 | `requires_human_approval=True`、`apply_proposal` 仅 hook | L90、L101、L152–153 |
| 真实实例化 / `departments`·`companies`·`company_topology` 表 | 复用 D2 内存 `CompanyTopology`，不持久化 | L37、L167 |
| 外部平台 / 凭证 / 合规面 | 未触碰 | Forbidden L203 |
| L6 经济 / ROI / token 产出比 | 未触碰 | Forbidden L204 |
| Employee CRUD / `employee_role_spec` 仅占位 | 仅契约字段，不消费 | Forbidden L205 |
| 新增写路径（调 `record`） | `propose_department_toggle` 不调 `record`，只读投影 | L162、L169、L178 |
| 新 API endpoint / 改读写字义 | 仅既有 endpoint，不新增路由 | L258、Forbidden L207 |
| 多 Agent / agent 抽象 / 复杂 UI / 向量库 | 未触碰 | Forbidden L208 |
| 触碰 D1 `TenantContext` 不变式 | 不触碰单租户哨兵 `'default'` | Invariant L181、Forbidden L209 |
| `department_types` 增删 / `WHERE department_id` 过滤 | 仅读目录、不写、不加读路径过滤 | Invariant L179、Forbidden L210–211 |

独立扫描结果：除 N3 所述预存在 `governor_sandbox.py` 外，无 `WHERE department_id`、无 `/api/govern` endpoint、无 D4 `apply_proposal(`/`manage_department_types(` 真实调用。**禁止区合规。**

## Reused-Base Signature Match

| ADR-0025 调用 | 基座真实签名（文件:行） | 匹配 |
|---|---|---|
| `DepartmentCatalog.list_types()` | `def list_types(self) -> list[DepartmentType]`（`department_catalog.py:60–71`） | ✅ |
| `DepartmentCatalog.get_manifest(type_key)` | `def get_manifest(self, type_key) -> DepartmentManifest \| None`（`department_catalog.py:73–87`） | ✅ |
| `DepartmentCatalog.assemble_company_topology(ceo_id, selected_type_keys)` | `def assemble_company_topology(self, ceo_id, selected_type_keys) -> CompanyTopology`（`department_catalog.py:89–108`） | ✅ |
| `CompanyTopology` 字段投影（`topology.manifests` 等） | `ceo_id` / `selected_type_keys` / `manifests` / `assembled_at`（`department_catalog.py:40–47`） | ✅（复用同一类，未新建） |
| `EvolutionEventLog.get_all()` | `def get_all(self) -> list[dict[str, Any]]`（`evolution_event_log.py:44–49`） | ✅ |
| D3 用法参照 `self.event_log.get_all()`（截断至 limit） | `department_observability.py:87`（`events = events[-limit:]`） | ✅（D4 同「get_all → 过滤 → 截断」模式） |

> ⚠️ 关键语义：① `get_manifest` 对未知 key 返回 `None`，`KeyError` 由未来 facade 内部转换（见 N2）；② `CompanyGovernance` 仅注入 `database`，`DepartmentCatalog` / `EvolutionEventLog` 须内部构造（见 N1）——均非签名不一致。

## Conclusion

**Result：PASS-WITH-NOTES。** D4 边界为纯设计-only reservation：git 核查证明 `backend/app/` 零代码泄漏、零 schema delta（与 D3 同构、完全可逆）；禁止区在设计与锁定声明上完整（`LOCKED_ACTIONS` 四动作齐备、future hook 仅占位）；复用基座签名全部匹配（D2 `DepartmentCatalog` / `CompanyTopology` + ADR-0016 D3 `EvolutionEventLog.get_all()`），无 MUST-FIX 签名不一致；无新 endpoint、无 `WHERE department_id`、无 `record()` 写；T01–T4 任务清单自洽且全 additive。仓库全量测试 **90 全绿**（Ran 90 tests, OK），边界未影响测试。Notes N1–N4 均为非阻塞设计一致性提示（内部构造约定、None→KeyError 转换、透明披露），转交架构师/工程师实现阶段采纳。**智能路由：NoOne**（无源码 bug、无测试 bug，无需回退 Engineer 或自修）。

## Sign-off

边界验证 **PASS-WITH-NOTES** → 主理人（产品规划席 delegation，预授权路线下代表 总控决策席）accept + gate（建议作为 D4 第一阶段 reservation 单独开 gate，参照 D1/D2/D3 零行为变化预留逻辑：只读作用域封装 + 受限提案 facade，无行为变更、零 schema 增量）→ 系统交付席 实现 T01–T04（零 schema 增量，比 D1/D2 更轻、更可逆）→ 质量运行席 实现验证（`backend/tests/test_d4_governance.py` 全部通过 + forbidden-scope 扫描干净 + 后端回归含 D1–D3 全绿）。Notes **N1**（catalog/event_log 内部构造约定）建议实现 T02 阶段采纳；**N2** 建议测试阶段采纳；**N3 / N4** 信息性、非阻塞。真实 D4 实现（提案落地 `apply_proposal` / 平台级管理后台 `manage_department_types` / 真实公司持久化 / 解除任何 gate / 跨公司策略 / 外部平台）必须各自独立小 gate（建议 `D4.impl` / `D4.platform`）+ 总控决策席 + 安全边界席 review，不得借本 reservation slice 夹带落地。ADR-0017 四个子决策（D1✅ D2✅ D3✅ D4✅）reservation 边界全部收口。
