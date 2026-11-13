# Review 054 — D3 职能型部门「自可观测 / 元循环」（reservation）: Boundary Verification

- **Reviewer seat**: 质量运行席
- **Target**: `docs/decisions/ADR-0024-d3-self-observability-boundaries.md` + `issues/054_adr0017_d3_self_observability.md`
- **Date**: 2026-07-08
- **Result**: PASS-WITH-NOTES

## Verification performed

- **边界契约具体且增量式**：仅新增 1 个只读 facade 模块 `backend/app/department_observability.py`（L37–93，方法体为空骨架，纯设计占位）+ 1 个测试文件 `backend/tests/test_d3_observability.py`（L198、L316）；零行为变化、无新 endpoint、不改任何读/写路径语义（L31）。复用既有 `evolution_events`（ADR-0016 D3）与 `department_types`/`DepartmentCatalog`（ADR-0023 D2）作为索引（L99–103），**零 schema 增量**（`database.py` 不在允许文件内，L202、L342）。
- **禁止区交叉核对**：逐条确认任务所列 forbidden 项（真实统计/BI/可视化 / L6 经济 / 外部服务与凭证 / 部门实例化 / Employee CRUD / 多 Agent / 复杂 UI / 向量库 / 新增写路径 / 解除自动改码 gate）均落在 ADR-0024 的「Forbidden Scope」（L130–142）与/或「第二部分」（L118–128）未来 gate 排除清单中：
  - 真实统计/聚合/BI（第二部分 #2，L123；Forbidden L132）；可视化/仪表盘/复杂 UI（第二部分 #3，L124；Forbidden L139）；
  - L6 经济/ROI、token 产出比（第二部分 #2，L123；Forbidden L134）；
  - 外部平台/凭证/合规面（第二部分 #6，L127；Forbidden L135）；
  - 部门实例化 / `departments` 表 / `department_types` 持久化扩展 / 部门→事件 FK（第二部分 #5，L126；Forbidden L133）；
  - Employee CRUD / L2L5 员工层 / 角色技能配置事实接口（第二部分 #7，L128；Forbidden L136）；
  - 新增写路径（Forbidden L137；Invariant L110；事件日志保持 ADR-0016 追加写不变式）；
  - 解除自动改码禁令 / human-approval gate（Forbidden L142；Gate L365；Consequences L172）。
  → 本 reservation slice 未夹带任何真实实现（facade 方法体为空，L73–93）。
- **Git 核查（只改文档）**：`git diff --name-only HEAD` 输出为空（无已提交改动）；`git status --short` 仅出现未跟踪（`??`）文档：`docs/decisions/ADR-0024-d3-self-observability-boundaries.md`、`docs/adr-0024-class-diagram.mermaid`、`docs/adr-0024-sequence-diagram.mermaid`、`issues/054_adr0017_d3_self_observability.md`，**无任何 `backend/app/*.py`**。**磁盘核查**：`backend/app/department_observability.py` 经 Glob 确认不存在（`**/department_observability.py` → No files found），`backend/app/database.py` 未被触碰。本 slice 在磁盘上仅有的产出为四份文档，无代码泄漏，与 ADR-0017 D3「设计-only 预留」意图一致。
- **复用基座确认（真实存在、签名匹配，无「引用不存在的方法」缺陷）**：
  - `EvolutionEventLog.get_all(self) -> list[dict[str, Any]]` —— 实际存在（`backend/app/evolution_event_log.py` L44–49），与 ADR-0024 L35/L95/L226（类图）引用一致。✓
  - `EvolutionEventLog.get_by_correlation_id(self, correlation_id) -> list[dict[str, Any]]` —— 实际存在（L36–42），ADR-0024 L101 将其作为 D3.impl 概念性未来关联路径引用，方法真实存在。✓
  - `EvolutionEventLog.record(self, *, correlation_id, event_type, payload) -> dict[str, Any]` —— 实际存在（L21–34），类图 L228 引用一致。✓（本 slice 严禁调用，见 Forbidden L137。）
  - `DepartmentCatalog.get_manifest(self, type_key) -> DepartmentManifest | None` —— 实际存在（`backend/app/department_catalog.py` L73–87），与 ADR-0024 L35/L76/L95/L102/L231（类图）引用一致。✓
  - `DepartmentCatalog.list_types(self) -> list[DepartmentType]` —— 实际存在（L60–71），类图 L232 引用一致。✓
  - ⚠️ 关键语义核对：`get_manifest` 对未知 `type_key` **返回 `None`（不抛异常）**（L85–86）。因此 ADR-0024 / issue 054 要求的「未知 `type_key` 抛 `KeyError`」（AC#2，L45/L108）必须由**未来 facade 内部**将 `None` 转为 `KeyError`。该责任划分明确、与 AC#2 一致，是设计约定而非缺陷；但测试作者须断言「facade 抛 KeyError」，而非「`get_manifest` 抛 KeyError」。
  - `TenantContext.current_tenant_id()`（L29）、`TenantContext.is_multi_tenant()`（L50）实际存在于 `backend/app/tenant_context.py`，AC#7 可自动化断言。✓
- **D1 不变式保持**：ADR-0024 L113、L343 明确 `TenantContext` 单租户哨兵 `'default'` 不被触碰，`current_tenant_id()` 仍为 `'default'`、`is_multi_tenant()` 仍为 `False`；本 reservation 未改动 D1 的 `tenant_id` 作用域模型。✓
- **可测性**：issues/054 验收标准 AC#1–#8（L44–51）与 ADR-0024 Verification Plan（L144–164）均为**具体、可自动化断言**，每条标准均可映射到未来 slice 专属断言或 forbidden-scope 扫描（详见 Notes，含 3 处轻微收紧建议）。

## Notes

- **N1（L68–72 vs L35/L73–80 — catalog 注入不一致）**：`DepartmentObservability.__init__` 仅注入 `database` 与 `event_log`（L69–71），未注入 `DepartmentCatalog`；但 `get_department_event_stream` 又要求「经 `DepartmentCatalog.get_manifest(type_key)` 校验 type_key」（L35/L76）。未来实现必须从 `self.database` 内部构造 `DepartmentCatalog(self.database)` 再调用 `get_manifest`，或把 `catalog` 也纳入构造注入。建议 ADR/issue 在「共享知识」(L334–343) 或 T02（L314）显式写明「facade 内部以 `DepartmentCatalog(self.database)` 复用目录索引」，避免 Engineer 误以为 catalog 已注入或漏接校验。（非阻塞，实现/测试阶段采纳）
- **N2（L139 vs L118–128 — 多 Agent / 向量库 未进「第二部分」枚举）**：「不做多 Agent、不抽象 agent、不做复杂 UI/dashboard、不用向量库/embedding」列入 Forbidden Scope（L139），但「第二部分」未来 gate 排除清单（L118–128）仅枚举部门实例化、外部平台、L6、Employee CRUD、统计/可视化、meta-loop 自愈，**未单独列出多 Agent 与向量库**。二者仍受 L139 + ADR-0017 L20（当前 gate 禁止）约束，不构成泄漏；但建议「第二部分」显式补一句「多 Agent 抽象 / 向量库属未来 gate（非本 reservation）」，使三处表述一致（与 D2 N3 同构）。（非阻塞）
- **N3（L46 / AC#3 — `available_fields` 与「已计算数值字段」易混淆）**：AC#3 表述「`available_fields == ["call_count","success_rate","quality_line_hits"]` 且**无已计算的数值指标字段**（无 `call_count`/`success_rate`/`quality_line_hits` 键或回填值）」。需特别区分：`available_fields` 是**静态声明的元素值列表**（含这些字符串），而「已计算字段」是指 DepartmentMetrics 上**名为** `call_count`/`success_rate`/`quality_line_hits` 且被回填数值的**属性**。建议把 AC#3 收紧为「`DepartmentMetrics` 实例上**不存在**名为 `call_count`/`success_rate`/`quality_line_hits` 的属性（或这些属性不为数值）」，与 `available_fields` 的静态字符串值明确区分，避免测试误将 `available_fields` 中的字符串当作「已计算字段」而误判。（非阻塞，建议测试阶段采纳）
- **N4（L341 — 禁止区扫描关键词已优于 D2）**：ADR-0024 测试约定（L341）已包含 `WHERE department_id`、`app.get("/api/observ"`、`app.post("/api/observ"`、`\.record\(`、`insert into`、`update `、`delete from`，并额外补充 `statistics.` / `mean(` / `success_rate =` 等统计计算关键词，优于 D2 的扫描集。可选增强：因 endpoint 前缀 `/api/observ` 已覆盖 `/api/observability` 等变体，PUT/DELETE 亦被同一前缀捕获，现有扫描集已足够；仅作信息性提示，无需改动。（信息性）
- **N5（git 状态说明 — 透明披露）**：仓库当前 `git diff --name-only HEAD` 为空、大量文档为未跟踪态（`??`），包括 ADR-0024 与 issues/054 本身。本验证不依赖 diff 隔离「本 slice 改动」，而是直接核查磁盘实现：`backend/app` 下无任何 D3 实现文件、`database.py` 无改动、facade 方法体为空骨架，确认 design-only。若主理人希望本 slice 以独立 commit 明确边界，建议架构师提交「ADR-0024 + issues/054 + 两张 mermaid 图」并标注 `design-only (D3 reservation boundary)`。（信息性，参照 D2 N6）

## Handoff

边界验证 **PASS-WITH-NOTES** → 主理人（产品规划席 delegation，预授权路线下代表 总控决策席）accept + gate（建议作为 D3 第一阶段 reservation 单独开 gate，参照 D1/D2 零行为变化预留逻辑：只读 facade + 索引占位，无行为变更、零 schema 增量）→ 系统交付席 实现 T01–T04（零 schema 增量，比 D1/D2 更轻、更可逆）→ 质量运行席 实现验证（`backend/tests/test_d3_observability.py` 全部通过 + forbidden-scope 扫描干净 + 后端回归含 D1/D2 全绿）。Notes **N1**（catalog 内部构造约定）建议实现 T02 阶段采纳；**N2 / N3** 建议 gate 评审或测试阶段一并裁定/采纳；**N4 / N5** 信息性、非阻塞。真实 D3 实现（真实指标关联 / 统计 / 可视化 / meta-loop 自愈 / Employee CRUD / 外部平台）必须各自独立小 gate（总控决策席批准）并触发 **安全边界席 review**，不得借本 reservation slice 夹带落地。
