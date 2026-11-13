# D1 Runtime Role Wiring 边界验证 (质量运行席)

- Date: 2026-07-07
- Reviewer seat: 质量运行席 (CONV-SEAT-QUALITY-001)
- Target: ADR-0019 + issues/045
- Verdict: PASS-WITH-NOTES

## A) Forbidden-scope compliance: PASS-WITH-NOTES

ADR-0019 的 "Allowed Files / Modules"（第 14–20 行）仅触及 `role_context.py`（只读）、`prompt_builder.py`、`employee.py` 及后端测试，且明确声明 no new tables / no schema / no persistence / no API semantic change / no UI change。该允许面未落入任何禁止区，与以下来源一致：

- ADR-0016 Forbidden Scope（第 48–56 行）：D1 未触及 L5/L6、Employee CRUD、multi-agent、business modules、complex UI 等。
- ADR-0018 carried-forward（003 第 115–121 行）：全部沿用。
- PROJECT_HANDOFF 禁止区（第 304–323 行）：D1 未触及 ROI、公司组织、Employee CRUD、multi-agent、business modules、复杂 UI、task-role 关联、task evidence、API 语义变更、persistence/schema、自动代码自改等。
- 002 Non-Goals（第 60–69 行）：Company/Employee CRUD、multi-agent、business modules、ROI、advanced UI、自动代码自改均未被 D1 放行。

**Notes（文字完整性，非功能性缺口）：** ADR-0019 第 38 行称其 Forbidden Scope "same as issues/045 + ADR-0016"，但其列举项未逐字包含：(1) ADR-0016 的 external services / channels / secrets；(2) PROJECT_HANDOFF 第 315 行的 vector DB / embeddings / agent memory / Employee memory；(3) 第 321 行的 architecture lock bypass / uncontrolled architecture changes / Evolution Governor policy weakening；(4) 第 322 行的 mock data / simulation 替代发布验证。这些项在 D1 范围内实际不可能被触及，且仍分别由其源文档强制禁止，故不构成功能性放行缺口；建议在 产品规划席 接受时确认 "same as" 的指代已涵盖上述源条款，或于 ADR-0019 显式补充以免后续误读。

## B) Behavior-contract fidelity: PASS-WITH-NOTES

ADR-0019 Behavior Contract（第 22–28 行）逐条对应 ADR-0016 Sub-decision A（第 25–27 行）：

- "Explicit profile-id only; never implicit default" ↔ ADR-0016 "No implicit default role"。
- "Missing/invalid profile id → behavior unchanged (omitted, no error)" ↔ ADR-0016 "If the profile id is missing or invalid, behavior is unchanged"。
- "MAY only add prompt/context guidance" ↔ ADR-0016 "may only add prompt/context guidance"。
- "MUST NOT: select tools, route work, change task state, trigger evolution …" ↔ ADR-0016 同款约束，并额外带入 003 第 118 行的 create/select agents、mutate workflows、alter learning/meta/evolution、change API/storage semantics。

全部 003 第 115–121 行 carried-forward 约束均被带入（仅一处措辞差异，见下）。未新增任何超出 Sub-decision A 的权限：实际接线动作由 ADR-0018 显式解除第 114 行 block，属授权范围。

**Notes（minor）：** 003 第 120 行要求 carried-forward 约束包含 "deterministic lookup, compact context excerpt, context-size reduction, fallback behavior, forbidden-scope scan evidence"。ADR-0019 通过 "additive excerpt only" / "valid profile id → additive excerpt only" 隐含了 compact excerpt 与 context-size 控制，但未逐字重申 "context-size reduction"。issues/045 的 Acceptance Criteria 亦未显式点名。建议 产品规划席 接受时确认 issues/045 的紧凑 excerpt 设计已覆盖 context-size reduction，或在实现阶段以断言锁定。其余四项（deterministic lookup=显式 profile id、fallback=missing/invalid unchanged、forbidden-scope scan=rg 关键字）均已落实。

## C) Unblock scope tightness: PASS

ADR-0018 明确仅解除 Sub-decision A（Runtime Role Wiring），D3（append-only event log）与 D2（governor sandbox）及 L5/L6 全部维持 blocked（第 29–32 行）。ADR-0019 的 Allowed Files 仅限 prompt_builder/employee/role_context 与测试，未触碰 `evolution_events`（D3）或任何 sandbox 机制（D2），未引入新表/新持久化/新 API 语义。ADR-0019 第 8 行显式声明切片的顺序 D1 → D3 → D2，尊重批准顺序，未假设 D3/D2 已解禁。结论：unblock 范围严格收紧在 Sub-decision A 内。

## D) Verification plan completeness: PASS

ADR-0019 Verification Plan（第 30–36 行）覆盖全部要求：

- 标准 diff 守卫：`git diff --name-only HEAD -- backend frontend`（第 32 行）。
- `git diff --check`（第 33 行）。
- forbidden-scope 守卫：`rg` 关键字 → 变更文件零匹配（第 34 行，对应 ADR-0016 第 80 行 rg 守卫）。
- 切片专属断言：`role_context` 被 import（prompt_builder/employee）、missing/invalid profile id → 输出不变、valid profile id → 仅 additive excerpt（第 35 行，完整对应 ADR-0016 第 85 行 Slice A 要求）。
- 额外回归：现有后端测试套件通过（第 36 行）。

无缺失项。

## Known gaps / open questions

- (A) ADR-0019 Forbidden Scope 文字称 "same as issues/045 + ADR-0016"，但枚举未逐字含 external services、vector/embeddings/memory、architecture lock bypass、mock data 替代等项；功能无缺口，建议接受时澄清指代或显式补充。
- (B) 003 第 120 行 "context-size reduction" 未在 ADR-0019 / issues/045 中逐字重申，建议由 issues/045 的紧凑 excerpt 设计覆盖或以断言锁定。

## Next

若 PASS → 路由 产品规划席 接受；接受后 系统交付席 按 issues/045 实现。

（本验证结论为 PASS-WITH-NOTES，属 PASS 范畴，建议路由 产品规划席 接受。质量运行席 仅记录边界验证，不代为接受——接受为 产品规划席 职责。）
