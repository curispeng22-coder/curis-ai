# Review 052 — D2 部门目录通用化（部门类型目录 reservation）: Boundary Verification

- **Reviewer seat**: 质量运行席
- **Target**: `docs/decisions/ADR-0023-d2-department-catalog-boundaries.md` + `issues/052_adr0017_d2_department_catalog.md`
- **Date**: 2026-07-07
- **Result**: PASS-WITH-NOTES

## Verification performed

- 边界契约具体且增量式：仅新增 1 张系统级目录表 `department_types`（L41–52）+ 2 个契约 stub 模块（`department_manifest.py`、`department_catalog.py`，L69–98、L107–148）+ 幂等 4 行种子（L54–62）+ 只读 facade；零行为变化、无新 endpoint、不改任何读/写路径语义（L35）。
- 禁止区交叉核对：逐条确认任务所列 8 类 forbidden 项（Employee CRUD / 多 Agent / 外部服务与凭证 / L5L6 经济 / 自动改码 / 真实隔离 / 复杂 UI / 向量库）均出现在 ADR-0023「Forbidden Scope」（L179–192），且 deferred 项在「第二部分」（L167–177）明确排除到未来 gate。
- Git 核查：`git status --short backend/app/` 输出为空 → 本 slice 未新增或修改任何 `backend/app/*.py`。磁盘核查：`backend/app/department_manifest.py`、`backend/app/department_catalog.py` 均不存在；`backend/app/database.py` 中无任何 `department_types` 引用（全代码库 grep "department" 在 `backend/app/` 下无命中）。本 slice 在磁盘上仅有的产出为两份文档（ADR-0023、issues/052），无代码泄漏。
- Reservation 刻意不实例化部门（无 `departments` 表、无 CRUD，L65）、不持久化 `company_topology`（L151）、不加 `WHERE department_id` 过滤（L160）、不新增 API endpoint（L188）——与 ADR-0017 D2「设计-only reservation」意图一致。
- D1 不变式保持：`TenantContext.current_tenant_id()` 仍为 `'default'`、`is_multi_tenant()` 仍为 `False`（L162，AC#7）；本 reservation 未触碰 D1 的 `tenant_id` 作用域模型。
- 可测性：issues/052 验收标准 1–8 与 ADR-0023 Verification Plan（L194–213）均为具体、可自动化断言；每条标准都映射到未来 slice 专属断言或 forbidden-scope 扫描（见 Notes，含 2 处轻微收紧建议）。

## Notes

- **N1（L399 待明确事项#1 — 种子范围）**：验收标准 #2 默认「恰好 4 行」，但 ADR 第 8 节把「是否直接种子 4 个规范类型 vs 仅预留空表」列为 gate 待确认项。建议 总控决策席 在开 gate 时明确裁定种子默认方案，否则 AC#2 的 "exactly 4 rows" 与 gate 决议存在不一致风险。建议把默认方案从「待明确」改为「gate 默认批准种子 4 行」，使 AC#2 锁定。（非阻塞，但建议 gate 时一并裁定）
- **N2（L394 测试约定 / AC#5 禁止区扫描）**：当前禁止区关键词仅列 `WHERE department_id`、`app.get("/api/department"`、`app.post("/api/department"`。建议补充 `/api/departments`（复数）与 PUT/DELETE 动词，避免未来实现用复数路径或其他 HTTP 方法绕过扫描。（非阻塞）
- **N3（L184–185 vs L167–177 第二部分）**：「多 Agent / Agent 抽象」明确列入 Forbidden Scope（L185），但「第二部分」未来 gate 排除清单未单独枚举该项（仅列部门实例化、外部平台、L6、Employee CRUD 等）。多 Agent 仍受 Forbidden Scope 约束且 ADR-0017 L20 已列为当前 gate 禁止，不构成泄漏；建议在「第二部分」显式补一句「多 Agent 抽象属未来 gate（非本 reservation）」以保持三处表述一致。（非阻塞）
- **N4（L39 / L422 — `department_types` 不做 `tenant_id` 隔离）**：这是相对于 ADR-0017 D1「所有聚合根预留 `tenant_id`」的刻意偏离（类型注册表而非实例，类比 `tools` 表），已在本 ADR 论证（「互补而非嵌套过滤」）。信息性提示：建议 gate 评审时确认此偏离被 总控决策席/安全边界席 知悉，避免后续误以为 `department_types` 需补 `tenant_id`。（非风险）
- **N5（AC#2「no real credentials/ROI/employee data」）**：该负面断言建议改写为可自动化形式——「每个 `manifest_json` 均为合法 JSON，且 7 个键均解析为占位结构（`capability_set`/`tool_classes`/`quality_lines`/`output_channels`/`guardrail_refs` 为空 list，`roi_schema`/`employee_role_spec` 为空 dict）」。当前表述 testable 但偏弱，建议锁定。（非阻塞）
- **N6（git 状态说明 — 透明披露）**：仓库当前有已提交历史（HEAD = `73001046` D1 reservation），但 `git diff --name-only HEAD` 为空、大量文档为未跟踪态（`??`）。本验证不依赖 diff 隔离「本 slice 改动」，而是直接核查磁盘实现：`backend/app` 无任何 D2 实现文件、`database.py` 无 `department_types` 引用，确认 design-only。若主理人希望本 slice 以独立 commit 明确边界，建议架构师提交 ADR-0023 + issues/052 并标注 `design-only (D2 reservation boundary)`。（信息性）

## Handoff

边界验证 **PASS-WITH-NOTES** → 总控决策席 gate 批准（建议作为 D2 第一阶段 reservation 单独开 gate，参照 D1 零行为变化预留逻辑）+ 产品规划席 accept → 系统交付席 实现 T01–T05 → 质量运行席 实现验证（`backend/tests/test_d2_department.py` 全部通过 + forbidden-scope 扫描干净）。Notes **N1 / N3** 建议 gate 时一并裁定；**N2 / N4 / N5** 供实现与测试阶段采纳，非阻塞。
