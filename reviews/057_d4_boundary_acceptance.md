# D4 Two-Tier Governance 边界接受 (产品规划席 delegation → 主理人齐活林)

- Date: 2026-07-08
- Acceptor seat: 产品规划席 (delegated to 主理人齐活林, 2026-07-07 23:27 起)
- Target: ADR-0025 + reviews/056 + issues/055
- Decision: **ACCEPT (boundary)** + **GATE APPROVED (D4 reservation)**
- Gate basis: ADR-0017 option-a roadmap 已预授权 D1–D4 design-only reservation gates；本次边界 ACCEPT 即视为 D4 reservation gate 通行，无需总控决策席二次批准（非 scope 扩张 / 非规划冲突）。
- Rationale: 质量运行席 (Yan) 边界验证结果 **PASS-WITH-NOTES**（reviews/056）。逐条 A–F 独立佐证（未抄边界文档结论）：
  - **A 设计-only / 零后端代码泄漏** ✅ `git status --short backend/app/` 为空；`governance.py` 不存在；本边界仅新增 docs + issues。
  - **B 零 schema delta** ✅ issue 055 Allowed Files 与 ADR-0025 §2 均排除 `database.py`；`git diff --name-only -- backend/app/database.py` 为空。
  - **C 禁止区合规** ✅ Forbidden Scope + 未来 gate 排除清单覆盖全部禁止项；`LOCKED_ACTIONS` 四动作齐备（`manage_department_types` / `lift_human_approval_gate` / `auto_modify_code` / `cross_company_policy`）；`apply_proposal` / `manage_department_types` 仅 `NotImplementedError` 占位。
  - **D 复用基座签名匹配** ✅ `DepartmentCatalog.list_types()` / `get_manifest(type_key)` / `assemble_company_topology(ceo_id, selected_type_keys)`、`CompanyTopology` 字段、`EvolutionEventLog.get_all()` 调用方式与 D3 `department_observability.py` 一致——无 MUST-FIX。
  - **E 无新 endpoint / 无 WHERE department_id / 无 record() 写** ✅ 设计为只读 + 受限提案；独立 grep `backend/app` 零命中（预存 `governor_sandbox.py:_apply_proposal` 非 D4 泄漏）。
  - **F 任务清单自洽** ✅ T01–T04 全 additive（governance.py + test_d4_governance.py），依赖顺序正确，与 D3 同构。
  - **测试实跑** ✅ `backend/` 全量 90 tests 全绿（边界未影响测试）。
  - Notes N1–N4 均为非阻塞设计一致性提示（含 governor_sandbox.py 预存 `_apply_proposal` 与 evolution_event_log.record 既有写，均非 D4 泄漏），转交实现阶段。
- Next: 系统交付席 (Kou) implements D4 reservation T01–T04 (`backend/app/governance.py` 只读 facade + `DepartmentGovernanceView`/`GovernanceScope`/`GovernanceProposal` dataclasses + `test_d4_governance.py`, zero schema delta)，然后 质量运行席 (Yan) implementation verification。
- 真实 D4 实现（apply_proposal / manage_department_types / 真实公司持久化 / 解除 gate / 跨公司策略 / 外部平台）须各自独立小 gate（建议 D4.impl / D4.platform）+ 总控决策席 + 安全边界席 review。

> ADR-0017 四个子决策 reservation 边界至此全部收口（D1✅ D2✅ D3✅ D4✅ boundary）。
