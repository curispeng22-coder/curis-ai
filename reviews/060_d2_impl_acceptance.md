# Review 060 — D2.impl 部门真实实例化（Department Instantiation）: Slice Acceptance

- **Accepting seat**: 主理人（齐活林 / Delivery Director，产品规划席 delegation）
- **Target issue**: `issues/056_adr0017_d2_impl_department_instantiation.md`
- **Boundary**: `docs/decisions/ADR-0026-d2-impl-department-instantiation.md`
- **Date**: 2026-07-08
- **Decision**: ACCEPTED — issue 056 CLOSED

## Acceptance Basis

本切片为 ADR-0017 四个子决策中**首个从 design-only reservation 走向真实落库的实现切片**，且**超出 option-a 预授权范围**，故以独立小 gate（ADR-0026 + issue 056）提交，经 总控决策席 2026-07-08 批准 + 安全边界席 review 随选确认后实现。

收口依据（逐席证据链）：
1. **系统交付席 (Kou)** 实现 `7617ed2c`：additive `departments` 表（7 列、无 FK、无 seed、复用 D1 `tenant_id` 预留列恒 `'default'`）+ `DepartmentCatalog.create_department`/`list_departments`/`get_department` 三真实落库方法，落实 `instantiate_department` hook；`connect_platform`/`manage_employees` 仍为禁止区 `NotImplementedError`。主理人一致性修复 `4ec02a59`（删过时 reservation 契约断言，保 clean checkout 全绿）。
2. **质量运行席 (Yan)** 实现验证 `reviews/059`（commit `67ab1616`）PASS-WITH-NOTES、路由 NoOne：独立实跑全量 **114 tests OK**；AC1–AC10 逐条读码核实通过；禁止区独立 grep 全绿；`database.py` 纯 additive 建表、基座/facade 零改动；whitespace 干净、工作树清洁。
3. **主理人独立复核**：`git show 67ab1616 --stat` 确认仅 +98 行 reviews/059（未触碰实现代码）；项目 `.venv` 独立重跑 `unittest discover tests` 实证 114 OK。

## Scope & Forbidden-Zone Confirmation

- ✅ 范围严格受控：`git diff --name-only ca843bba HEAD` 仅 4 文件（database.py / department_catalog.py / test_d2_department.py / test_d2_impl_department.py），与 issue 056 Allowed files 完全一致；Forbidden files 全部未出现。
- ✅ 禁止区零触碰：Employee CRUD（仅占位 NotImplementedError，无 employees 表/写）、外部平台（仅占位 NotImplementedError，无凭证/SDK）、真实多租户（仍单租户 `'default'`，无隔离逻辑）、L6 ROI、auto_modify_code、manage_department_types（ADR-0025 LOCKED 不落地）、department_types 写、新 API endpoint、evolution_events 写、向量/embedding —— 全部零命中。
- ✅ D3 `DepartmentObservability` / D4 `CompanyGovernance` facade 接口与 import 路径完好；`assemble_company_topology` 仍返回内存 `CompanyTopology`；D1 `TenantContext` 单租户不变式保持。
- ✅ 单租户纪律保持，`tenant_id` 恒 `'default'`，无多租户隔离逻辑引入。

## Non-blocking Notes (acknowledged, no code change)

- N1（INFO）：实现测试实际 14 例（文档/commit message 称 10），真实全量 114 已实证全绿，纯文档计数口径差异，无需改码。

## Decision

**ACCEPT D2.impl 部门真实实例化切片** —— issue 056 CLOSED。ADR-0017 四个子决策（D1✅ D2✅reservation + D2.impl✅ D3✅ D4✅）至此全部收口（reservation 全收，且 D2 已跨出真实实例化第一步）。

后续真实增强（Employee CRUD / 外部平台接入 / L6 ROI / `manage_department_types` 落地 / `evolution_events` 审计写 / 多租户隔离 / 新 API endpoint / 向量内存）均须各自独立小 gate + 总控决策席 + 安全边界席 review，不得借本切片夹带落地。

## Handoff

切片收口 → 团队 `software-curis-d2impl` 完成本职；后续切片（D1.impl / D3.impl / D4.impl / D4.platform 等）须各自独立 gate 后启动。按用户 2026-07-08 指令，收口后挂飞书条件提醒（15 分钟内无下一步指令则向「Curis 开发通知」推送软性 nudge）。
